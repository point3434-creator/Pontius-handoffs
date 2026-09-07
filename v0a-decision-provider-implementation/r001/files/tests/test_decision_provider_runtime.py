"""Finite provider dispatch controls with independent mailbox observations."""
from __future__ import annotations

import unittest
from unittest.mock import patch

from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.no_limit_betting import CALL
from pontius.river import parse_cards
from pontius.v0a.clock import ClockInvalidError
from pontius.v0a.model import (
    DeliveryReceipt, DeliveryStatus, FailureCode, HandAction, HandStartedEvent,
    MailboxRejectionError, OpponentActionEvent,
)
from pontius.v0a.runtime import HandRuntime


class Clock:
    def __init__(self):
        self.now = 0
        self.reads = 0
        self.jump_read = None

    def __call__(self):
        self.reads += 1
        if self.reads == self.jump_read:
            self.now = 14_000_000_000
        return self.now


class Mailbox:
    def __init__(self):
        self.envelopes = []

    def deliver(self, envelope):
        self.envelopes.append(envelope)
        return DeliveryReceipt(envelope.hand_id, envelope.action_index)


def started(cards="As Ah", seat=3):
    return HandStartedEvent(
        hand_id="pontius-v0a-event-interface-v2-correctness-runtime", event_index=0,
        button=0, controlled_seat=seat, starting_stacks=(200,) * 6,
        small_blind=1, big_blind=2, private_cards=tuple(sorted(parse_cards(*cards.split()))))


class ProviderRuntimeTests(unittest.TestCase):
    def assert_record(self, record):
        from pontius.decision_provider.codec import decision_payload, validate_decision
        self.assertEqual(validate_decision(decision_payload(record))["hand_id"], record.hand_id)

    def runtime(self, mailbox=None, clock=None, **kwargs):
        return HandRuntime(blueprint=ImmutableBlueprintActionSource(source_id="provider-test"),
                           mailbox=mailbox or Mailbox(), clock=clock or Clock(),
                           strategy="baseline-rules-v1", source_manifest_sha256="1" * 64, **kwargs)

    def test_premium_dispatch_applies_and_delivers_one_legal_raise(self):
        mailbox = Mailbox()
        try:
            runtime = HandRuntime(
                blueprint=ImmutableBlueprintActionSource(source_id="provider-test"),
                mailbox=mailbox, clock=Clock(), strategy="baseline-rules-v1",
                source_manifest_sha256="1" * 64)
        except TypeError as error:
            self.fail(f"selectable runtime is unavailable: {error}")
        result = runtime.dispatch(started())
        self.assertEqual(result.status, "decided")
        self.assertEqual(len(mailbox.envelopes), 1)
        action = mailbox.envelopes[0].action
        self.assertEqual((action.kind, action.raise_to), ("raise", 4))
        self.assertEqual(result.decision.selection_origin, "provider")
        self.assertEqual(result.decision.applied_action, action)
        self.assertEqual(result.decision.delivered_action, action)
        self.assertEqual(runtime.state.stacks[3], 196)

    def test_fixed_preflop_actions_and_free_check(self):
        for cards, kind, chips in (("9c 9d", "call", 198), ("7c 2d", "fold", 200)):
            with self.subTest(cards=cards):
                runtime = self.runtime()
                result = runtime.dispatch(started(cards))
                self.assertEqual(result.decision.selected_action.kind, kind)
                self.assertEqual(runtime.state.stacks[3], chips)
        runtime = self.runtime()
        first = started("7c 2d", seat=2)
        self.assertEqual(runtime.dispatch(first).status, "accepted")
        for index, seat in enumerate((3, 4, 5, 0, 1), 1):
            result = runtime.dispatch(OpponentActionEvent(
                hand_id=first.hand_id, event_index=index, seat=seat, street="preflop",
                action=HandAction("call", None)))
        self.assertEqual(result.decision.selected_action.kind, "check")
        self.assertEqual(result.decision.proposal.reason, "free_check")

    def test_legacy_default_and_explicit_blueprint_are_equal(self):
        results = []
        for options in ({}, {"strategy": "blueprint-v1"}):
            mailbox = Mailbox()
            runtime = HandRuntime(
                blueprint=ImmutableBlueprintActionSource(source_id="provider-test"),
                mailbox=mailbox, clock=Clock(), **options)
            results.append(runtime.dispatch(started()))
        self.assertEqual(results[0], results[1])
        self.assertEqual(results[0].decision.selected_action.kind, "call")

    def test_provider_error_abstention_invalid_and_stale_fallback(self):
        from pontius.decision_provider.model import DecisionProposal
        from pontius.decision_provider.providers import BaselineProvider
        def throwing(provider, observation):
            raise ValueError("controlled provider failure")
        cases = ((throwing, "error"),
                 (lambda p, o: DecisionProposal(o.decision_sha256, None, "abstain"), "abstained"),
                 (lambda p, o: object(), "invalid"),
                 (lambda p, o: DecisionProposal("0" * 64, CALL, "premium_call"), "invalid"))
        for behavior, expected in cases:
            with self.subTest(outcome=expected), \
                    patch.object(BaselineProvider, "propose", behavior):
                mailbox = Mailbox()
                result = self.runtime(mailbox).dispatch(started())
                self.assertEqual(result.status, "decided")
                self.assertEqual(result.decision.provider_outcome, expected)
                self.assertEqual(result.decision.selection_origin, "blueprint_fallback")
                self.assertEqual(result.decision.selected_action.kind, "call")
                self.assertEqual(len(mailbox.envelopes), 1)
                self.assert_record(result.decision)

    def test_late_outcome_is_preserved_at_cutoff_edges(self):
        from pontius.decision_provider.providers import BaselineProvider
        original = BaselineProvider.propose
        for elapsed in (13_999_999_999, 14_000_000_000, 14_000_000_001,
                        15_000_000_000, 15_000_000_001):
            for kind in ("proposed", "error", "invalid"):
                with self.subTest(elapsed=elapsed, outcome=kind):
                    clock, mailbox = Clock(), Mailbox()
                    def scheduled(provider, observation):
                        proposal = original(provider, observation)
                        clock.now = elapsed
                        if kind == "error":
                            raise ValueError("scheduled")
                        return object() if kind == "invalid" else proposal
                    with patch.object(BaselineProvider, "propose", scheduled):
                        result = self.runtime(mailbox, clock).dispatch(started())
                    record = result.decision
                    self.assert_record(record)
                    self.assertEqual(record.provider_outcome, kind)
                    self.assertEqual(len(mailbox.envelopes), 1)
                    if elapsed >= 14_000_000_000:
                        self.assertEqual(record.selection_reason, "provider_late")
                        self.assertEqual(record.selected_action.kind, "call")
                        self.assertEqual(result.status, "failed")
                        code = (FailureCode.ACTION_DEADLINE_EXCEEDED if elapsed > 15_000_000_000
                                else FailureCode.WORK_CUTOFF_EXCEEDED)
                        self.assertEqual(result.failure.code, code)
                    else:
                        self.assertEqual(result.status, "decided")

    def test_known_cutoff_skips_provider(self):
        from pontius.decision_provider.providers import BaselineProvider
        clock = Clock()
        clock.jump_read = 3
        with patch.object(BaselineProvider, "propose", side_effect=AssertionError) as propose:
            result = self.runtime(clock=clock).dispatch(started())
        self.assertEqual(propose.call_count, 0)
        self.assertEqual(result.decision.provider_outcome, "not_called")
        self.assertEqual(result.decision.selection_reason, "provider_skipped_cutoff")
        self.assertEqual(result.failure.code, FailureCode.WORK_CUTOFF_EXCEEDED)
        self.assert_record(result.decision)

    def test_delivery_rejection_and_unknown_retain_local_application(self):
        for error, expected in ((MailboxRejectionError(), DeliveryStatus.REJECTED),
                                (RuntimeError(), DeliveryStatus.UNKNOWN)):
            mailbox = Mailbox()
            def delivery(envelope):
                mailbox.envelopes.append(envelope)
                raise error
            mailbox.deliver = delivery
            result = self.runtime(mailbox).dispatch(started())
            self.assertEqual(result.status, "failed")
            self.assertEqual(len(mailbox.envelopes), 1)
            self.assertEqual(result.decision.delivery_status, expected)
            self.assertEqual(result.decision.applied_action.kind, "raise")
            self.assertIsNone(result.decision.delivered_action)
            self.assert_record(result.decision)

    def test_failure_after_accepted_delivery_remains_accepted(self):
        mailbox, clock = Mailbox(), Clock()
        original = mailbox.deliver
        def delivery(envelope):
            receipt = original(envelope)
            clock.now = True
            return receipt
        mailbox.deliver = delivery
        result = self.runtime(mailbox, clock).dispatch(started())
        self.assertEqual(result.failure.code, FailureCode.CLOCK_INVALID)
        self.assertEqual(result.decision.delivery_status, DeliveryStatus.ACCEPTED)
        self.assertEqual(result.decision.delivered_action.kind, "raise")
        self.assert_record(result.decision)

    def test_clock_and_changed_identity_are_fatal_without_delivery(self):
        from pontius.decision_provider.providers import BaselineProvider
        for cause in ("clock", "identity", "reversal"):
            mailbox, clock = Mailbox(), Clock()
            clock.now = 100
            runtime = self.runtime(mailbox, clock)
            original = BaselineProvider.propose
            def corrupt(provider, observation):
                proposal = original(provider, observation)
                if cause == "clock":
                    raise ClockInvalidError("scheduled")
                if cause == "reversal":
                    clock.now = 99
                else:
                    runtime.source_manifest_sha256 = "2" * 64
                return proposal
            with patch.object(BaselineProvider, "propose", corrupt):
                result = runtime.dispatch(started())
            self.assertEqual(result.status, "failed")
            self.assertEqual(len(mailbox.envelopes), 0)
            expected = {"clock": FailureCode.CLOCK_INVALID, "reversal": FailureCode.CLOCK_REVERSED,
                        "identity": FailureCode.SOURCE_BINDING_MISMATCH}[cause]
            self.assertEqual(result.failure.code, expected)
            self.assert_record(result.decision)

    def test_codec_roundtrip_and_rejection(self):
        from pontius.decision_provider.codec import decision_payload, validate_decision
        record = self.runtime().dispatch(started()).decision
        payload = decision_payload(record)
        self.assertEqual(validate_decision(payload), payload)
        self.assertEqual(payload["schema_version"], "pontius-provider-decision-v1")
        for field, value in (("action_index", True), ("config_sha256", "bad"),
                             ("provider_outcome", "error"),
                             ("selection_origin", "blueprint_fallback"),
                             ("delivered_action", None), ("unexpected", 1)):
            broken = dict(payload, **{field: value})
            with self.subTest(field=field), self.assertRaises((TypeError, ValueError)):
                validate_decision(broken)

    def test_removed_or_mutated_provider_binding_cannot_revert_to_legacy(self):
        for mutation in ("removed", "identity"):
            with self.subTest(mutation=mutation):
                mailbox = Mailbox()
                runtime = self.runtime(mailbox)
                if mutation == "removed":
                    runtime._provider = None
                else:
                    object.__setattr__(runtime._provider.identity, "config_sha256", "2" * 64)
                result = runtime.dispatch(started())
                self.assertEqual(result.status, "failed")
                self.assertEqual(result.failure.code, FailureCode.SOURCE_BINDING_MISMATCH)
                self.assertEqual(mailbox.envelopes, [])

    def test_process_control_is_not_an_ordinary_provider_fallback(self):
        from pontius.decision_provider.providers import BaselineProvider
        for exception in (KeyboardInterrupt, SystemExit):
            mailbox = Mailbox()
            with patch.object(BaselineProvider, "propose", side_effect=exception), \
                    self.assertRaises(exception):
                self.runtime(mailbox).dispatch(started())
            self.assertEqual(mailbox.envelopes, [])

    def test_provider_cannot_mutate_engine_observation(self):
        from pontius.decision_provider.providers import BaselineProvider
        original = BaselineProvider.propose
        def tamper(provider, observation):
            object.__setattr__(observation, "remaining_work_ns", True)
            return original(provider, observation)
        with patch.object(BaselineProvider, "propose", tamper):
            result = self.runtime().dispatch(started())
        self.assertEqual(result.status, "decided")
        self.assertEqual(result.decision.selected_action.kind, "raise")

    def test_delivery_deadline_edges_preserve_selected_and_delivered_action(self):
        for elapsed in (14_999_999_999, 15_000_000_000, 15_000_000_001):
            with self.subTest(elapsed=elapsed):
                mailbox, clock = Mailbox(), Clock()
                original = mailbox.deliver
                def delivery(envelope):
                    receipt = original(envelope)
                    clock.now = elapsed
                    return receipt
                mailbox.deliver = delivery
                result = self.runtime(mailbox, clock).dispatch(started())
                self.assertEqual(len(mailbox.envelopes), 1)
                self.assertEqual(result.decision.selected_action.kind, "raise")
                self.assertEqual(result.decision.delivered_action.kind, "raise")
                self.assertEqual(result.decision.timing.work_cutoff_crossed, False)
                self.assertEqual(result.status, "failed" if elapsed > 15_000_000_000 else "decided")
                self.assert_record(result.decision)

    def test_strategy_and_manifest_admission(self):
        for options in ({"strategy": "unregistered"}, {"strategy": True},
                        {"strategy": "baseline-rules-v1"},
                        {"strategy": "baseline-rules-v1", "source_manifest_sha256": "BAD"}):
            with self.subTest(options=options), self.assertRaises((TypeError, ValueError)):
                HandRuntime(blueprint=ImmutableBlueprintActionSource(source_id="provider-test"),
                            mailbox=Mailbox(), clock=Clock(), **options)


if __name__ == "__main__":
    unittest.main()
