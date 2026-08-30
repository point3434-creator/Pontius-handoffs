"""Independent cold A public-boundary schedules; no production mutation."""
from dataclasses import fields, replace
import unittest

from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.model import (
    ActionEnvelope, ActionMailbox, DeliveryReceipt, DeliveryStatus, FailureCode,
    HandAction, HandStartedEvent, MailboxRejectionError, OpponentActionEvent,
    ShowdownResultEvent, StreetRevealedEvent, TimingStatus,
)
from pontius.v0a.runtime import HandRuntime

OBSERVATIONS = []
HAND = "cold-a-r004"
START = dict(hand_id=HAND, event_index=0, button=0, controlled_seat=2,
             starting_stacks=(20,) * 6, small_blind=1, big_blind=2,
             private_cards=(0, 13))
class Clock:
    def __init__(self):
        self.reads = 0
        self.fail_on = None
        self.now = 1000
    def __call__(self):
        self.reads += 1
        if self.reads == self.fail_on:
            return True
        self.now += 1000
        return self.now

def loose(record, **changes):
    parent = type(record)
    sub = type("ColdUnchecked" + parent.__name__, (parent,),
               {"__post_init__": lambda self: None})
    values = {f.name: getattr(record, f.name) for f in fields(parent)}
    values.update(changes)
    return sub(**values)

def create(*, mailbox=None, clock=None, controlled=2, stacks=None):
    mailbox = ActionMailbox() if mailbox is None else mailbox
    clock = Clock() if clock is None else clock
    runtime = HandRuntime(
        blueprint=ImmutableBlueprintActionSource(source_id="cold-a-empty"),
        mailbox=mailbox, clock=clock)
    kw = dict(START, controlled_seat=controlled)
    if stacks is not None:
        kw["starting_stacks"] = stacks
    return runtime, mailbox, clock, HandStartedEvent(**kw)

def opponent(runtime, index, *, kind=None):
    state = runtime.state
    assert state is not None and state.acting_seat != 2
    if kind is None:
        kind = "call" if state.legal_decision().to_call else "check"
    return OpponentActionEvent(HAND, index, state.street.value,
                               state.acting_seat, HandAction(kind, None))

def reach(stage, *, folded=False, all_in=False):
    runtime, mailbox, clock, start = create(stacks=(2,) * 6 if all_in else None)
    if stage == "start":
        return runtime, mailbox, clock, start
    assert runtime.dispatch(start).status == "accepted"
    index = 1
    if stage == "opponent":
        return runtime, mailbox, clock, opponent(runtime, index)
    def finish_round(index):
        while not runtime.state.round_complete and not runtime.state.is_terminal:
            actor = runtime.state.acting_seat
            kind = "fold" if folded and actor in (0, 3, 4, 5) else None
            out = runtime.dispatch(opponent(runtime, index, kind=kind))
            assert out.status in ("accepted", "decided"), out
            index += 1
        return index
    index = finish_round(index)
    flop = StreetRevealedEvent(HAND, index, "flop", (20, 21, 22))
    if stage == "reveal":
        return runtime, mailbox, clock, flop
    for street, cards in (("flop", (20, 21, 22)), ("turn", (30,)), ("river", (40,))):
        out = runtime.dispatch(StreetRevealedEvent(HAND, index, street, cards))
        assert out.status in ("accepted", "decided"), out
        index += 1
        index = finish_round(index)
    ranks = (None, 4, 9, None, None, None) if folded else (1, 2, 9, 3, 4, 5)
    return runtime, mailbox, clock, ShowdownResultEvent(HAND, index, ranks)

class ColdABoundaryTests(unittest.TestCase):
    def no_effect(self, runtime, mailbox, clock, event, expected=FailureCode.INVALID_EVENT,
                  unadmitted=True):
        state, accepted, reads = runtime.state, mailbox.accepted, clock.reads
        out = runtime.dispatch(event)
        self.assertEqual(out.status, "failed")
        self.assertIs(out.failure.code, expected)
        if unadmitted:
            self.assertIsNone(out.failure.event_index)
        self.assertEqual(runtime.state, state)
        self.assertEqual(mailbox.accepted, accepted)
        self.assertFalse(runtime.hand_complete)
        self.assertGreater(clock.reads, reads)
        self.assertIs(out.failure.delivery_status, DeliveryStatus.NOT_ATTEMPTED)
        return out

def add(name, fn):
    setattr(ColdABoundaryTests, "test_" + name, fn)

# Construction bypasses are ordinary subclasses, never private field forging.
for stage in ("start", "opponent", "reveal", "showdown"):
    for label, change in (
        ("subclass", {}), ("schema", {"schema_version": "wrong"}),
        ("bool_index", {"event_index": True}),
        ("float_index", {"event_index": 1.0}),
        ("mutable_id", {"hand_id": []}),
    ):
        def test(self, stage=stage, change=change):
            rt, box, clk, valid = reach(stage)
            self.no_effect(rt, box, clk, loose(valid, **change))
        add("event_" + stage + "_" + label, test)

for label, change in (
    ("kind", {"kind": "wager"}), ("bool_raise", {"kind": "raise", "raise_to": True}),
    ("float_raise", {"kind": "raise", "raise_to": 6.0}),
    ("negative_raise", {"kind": "raise", "raise_to": -1}),
    ("extra_payload", {"kind": "call", "raise_to": 7}),
    ("valid_subclass", {}),
):
    def test(self, change=change):
        rt, box, clk, valid = reach("opponent")
        action = loose(HandAction("call", None), **change)
        exact = replace(valid, action=action)
        self.assertIs(type(exact), OpponentActionEvent)
        self.no_effect(rt, box, clk, exact)
    add("nested_action_" + label, test)

for label, ranks in (
    ("mutable_list", [None, 4, 9, None, None, None]),
    ("empty_list", []), ("empty_tuple", ()),
    ("nested_empty", (None, (), (9,), None, None, None)),
    ("tuple_bool", (None, (True,), (9,), None, None, None)),
):
    def test(self, ranks=ranks):
        rt, box, clk, valid = reach("showdown", folded=True)
        self.no_effect(rt, box, clk, loose(valid, strengths=ranks))
    add("showdown_" + label, test)

for label, ranks in (
    ("mixed_domain", (None, 4, (9,), None, None, None)),
    ("missing_live", (None, None, 9, None, None, None)),
    ("extra_folded", (1, 4, 9, None, None, None)),
    ("all_missing", (None,) * 6),
):
    def test(self, ranks=ranks):
        rt, box, clk, valid = reach("showdown", folded=True)
        out = self.no_effect(rt, box, clk, replace(valid, strengths=ranks), unadmitted=False)
        self.assertEqual(out.failure.event_index, valid.event_index)
        with self.assertRaises(RuntimeError):
            rt.settle()
    add("showdown_context_" + label, test)

for folded, all_in in ((False, False), (True, False), (False, True)):
    for rank_domain in ("int", "tuple"):
        def test(self, folded=folded, all_in=all_in, rank_domain=rank_domain):
            rt, box, clk, valid = reach("showdown", folded=folded, all_in=all_in)
            ranks = valid.strengths
            if rank_domain == "tuple":
                ranks = tuple(None if rank is None else (rank, 0) for rank in ranks)
            before = box.accepted
            self.assertEqual(rt.dispatch(replace(valid, strengths=ranks)).status, "accepted")
            self.assertTrue(rt.hand_complete)
            settlement = rt.settle()
            expected_pot = 4 if folded else 12
            self.assertEqual(settlement.payouts, (0, 0, expected_pot, 0, 0, 0))
            expected_stacks = tuple(rt.state.stacks[i] + settlement.payouts[i] for i in range(6))
            self.assertEqual(settlement.final_stacks, expected_stacks)
            self.assertEqual(rt.settle(), settlement)
            self.assertEqual(box.accepted, before)
            OBSERVATIONS.append(dict(control="showdown", folded=folded, all_in=all_in,
                                     ranks=rank_domain, payouts=list(settlement.payouts)))
        add(f"valid_settlement_folded_{folded}_allin_{all_in}_{rank_domain}", test)

class Hostile:
    hits = 0
    def __getattribute__(self, name):
        type(self).hits += 1
        raise AssertionError("unadmitted attribute consulted")

for state_name in ("fresh", "dead", "complete", "clock_first"):
    def test(self, state_name=state_name):
        Hostile.hits = 0
        rt, box, clk, start = create()
        expected = FailureCode.INVALID_EVENT
        if state_name == "dead":
            rt.dispatch(object())
            expected = FailureCode.EVENT_ORDER
        if state_name == "complete":
            rt, box, clk, event = reach("showdown")
            self.assertEqual(rt.dispatch(event).status, "accepted")
            expected = FailureCode.EVENT_ORDER
        if state_name == "clock_first":
            clk.fail_on = 1
            expected = FailureCode.CLOCK_INVALID
        before = box.accepted
        out = rt.dispatch(Hostile())
        self.assertIs(out.failure.code, expected)
        self.assertIsNone(out.failure.event_index)
        self.assertEqual(Hostile.hits, 0)
        self.assertEqual(box.accepted, before)
        OBSERVATIONS.append(dict(metadata=state_name, code=out.failure.code.value))
    add("safe_metadata_" + state_name, test)

# Invalid event primary remains ahead of a fault during boundary cleanup.
def cause_order(self):
    rt, box, clk, start = create()
    clk.fail_on = 2
    out = rt.dispatch(object())
    self.assertIs(out.failure.code, FailureCode.INVALID_EVENT)
    self.assertEqual(rt.closure_failures, (FailureCode.INVALID_EVENT, FailureCode.CLOCK_INVALID))
    self.assertFalse(box.accepted)
add("invalid_event_then_cleanup_clock_order", cause_order)

GOOD_ENVELOPE = ActionEnvelope(HAND, 1, 3, "preflop", HandAction("call", None))
for label, change in (
    ("subclass", {}), ("bool_index", {"action_index": True}),
    ("float_index", {"action_index": 1.0}), ("zero_index", {"action_index": 0}),
    ("bool_seat", {"seat": True}), ("large_seat", {"seat": 6}),
    ("street", {"street": "elsewhere"}), ("mutable_id", {"hand_id": []}),
    ("non_ascii", {"hand_id": "caf\u00e9"}), ("empty_id", {"hand_id": ""}),
):
    def test(self, change=change):
        box = ActionMailbox()
        with self.assertRaises(MailboxRejectionError):
            box.deliver(loose(GOOD_ENVELOPE, **change))
        self.assertEqual(box.accepted, {})
        receipt = box.deliver(GOOD_ENVELOPE)
        self.assertIs(type(receipt), DeliveryReceipt)
        self.assertEqual(receipt, DeliveryReceipt(HAND, 1))
        accepted = box.accepted
        self.assertEqual(accepted, {(HAND, 1): GOOD_ENVELOPE})
        with self.assertRaises(MailboxRejectionError):
            box.deliver(GOOD_ENVELOPE)
        self.assertEqual(box.accepted, accepted)
        accepted.clear()
        self.assertEqual(len(box.accepted), 1)
    add("mailbox_" + label, test)

def nested_envelope(self):
    box = ActionMailbox()
    exact = replace(GOOD_ENVELOPE, action=loose(HandAction("raise", 6), kind="wrong"))
    self.assertIs(type(exact), ActionEnvelope)
    with self.assertRaises(MailboxRejectionError):
        box.deliver(exact)
    self.assertEqual(box.accepted, {})
    box.deliver(GOOD_ENVELOPE)
    stored = box.accepted[(HAND, 1)]
    self.assertIs(type(stored), ActionEnvelope)
    self.assertIs(type(stored.action), HandAction)
    self.assertIsNot(stored, GOOD_ENVELOPE)
    self.assertIsNot(stored.action, GOOD_ENVELOPE.action)
add("mailbox_exact_outer_nested_invalid_then_valid", nested_envelope)

ACK_CASES = (
    ("subclass", lambda good: loose(good)),
    ("bool_alias", lambda good: loose(good, action_index=True)),
    ("float_alias", lambda good: loose(good, action_index=1.0)),
    ("mutable_id", lambda good: loose(good, hand_id=[])),
    ("wrong_exact_index", lambda good: DeliveryReceipt(HAND, 2)),
    ("wrong_exact_hand", lambda good: DeliveryReceipt("other-hand", 1)),
    ("none", lambda good: None),
    ("hostile", lambda good: Hostile()),
)
for label, transform in ACK_CASES:
    def test(self, transform=transform, label=label):
        box = ActionMailbox()
        attempts = []
        class Forward:
            def deliver(self, envelope):
                attempts.append(envelope)
                good = box.deliver(envelope)
                return transform(good)
        rt, _, clk, start = create(mailbox=Forward(), controlled=3)
        out = rt.dispatch(start)
        self.assertEqual(out.status, "failed")
        self.assertIs(out.failure.code, FailureCode.DELIVERY_AMBIGUOUS)
        self.assertIs(out.failure.delivery_status, DeliveryStatus.UNKNOWN)
        self.assertIsNone(out.failure.delivered_action)
        self.assertEqual(rt.accepted_delivery_count, 0)
        self.assertEqual(len(attempts), 1)
        self.assertEqual(len(box.accepted), 1)
        self.assertEqual(box.accepted[(HAND, 1)].action, HandAction("call", None))
        self.assertEqual(rt.state.total_contributions[3], 2)
        self.assertIs(out.failure.timing.status, TimingStatus.INTERRUPTED)
        self.assertIsNone(out.failure.timing.emission_observed_ns)
        second = rt.dispatch(Hostile())
        self.assertIs(second.failure.code, FailureCode.EVENT_ORDER)
        self.assertEqual(len(attempts), 1)
        self.assertEqual(len(box.accepted), 1)
        OBSERVATIONS.append(dict(ack=label, attempted=1, actual_deliveries=1,
                                 acknowledged=rt.accepted_delivery_count,
                                 classification=out.failure.delivery_status.value))
    add("forwarded_ack_" + label, test)

for fail_after in (False, True):
    def test(self, fail_after=fail_after):
        box, clk, attempts = ActionMailbox(), Clock(), []
        class Forward:
            def deliver(self, envelope):
                attempts.append(envelope)
                receipt = box.deliver(envelope)
                if fail_after:
                    clk.fail_on = clk.reads + 1
                return receipt
        rt, _, _, start = create(mailbox=Forward(), clock=clk, controlled=3)
        out = rt.dispatch(start)
        self.assertEqual(len(attempts), 1)
        self.assertEqual(len(box.accepted), 1)
        self.assertEqual(rt.accepted_delivery_count, 1)
        self.assertIsNotNone(out.decision)
        if fail_after:
            self.assertIs(out.failure.code, FailureCode.CLOCK_INVALID)
            self.assertIs(out.failure.delivery_status, DeliveryStatus.ACCEPTED)
            self.assertEqual(out.failure.delivered_action, HandAction("call", None))
        else:
            self.assertEqual(out.status, "decided")
            self.assertIsNone(out.failure)
    add("forwarded_valid_ack_clock_failure_" + str(fail_after), test)
