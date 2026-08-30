from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

snapshot = Path(sys.argv[1]).resolve()
slot = sys.argv[2]
expected = {
    "311": (Path("D:/Pontius-tools/py311/Scripts/python.exe"), (3, 11, 15),
            "3.11.15 (main, Jul 23 2026, 14:42:43) [MSC v.1944 64 bit (AMD64)]"),
    "314": (Path("D:/Pontius/.venv/Scripts/python.exe"), (3, 14, 6),
            "3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)]"),
}[slot]
assert Path(sys.executable).resolve() == expected[0].resolve()
assert sys.implementation.name == "cpython"
assert tuple(sys.version_info[:3]) == expected[1]
assert sys.version == expected[2]
assert Path.cwd().resolve() == snapshot
assert os.environ["PYTHONPATH"] == str(snapshot / "src")
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert os.environ["PONTIUS_GIT"] == "C:/Program Files/Git/cmd/git.exe"
assert "PATH" not in os.environ
print(json.dumps({"identity_before_payload_import": {
    "executable": sys.executable, "implementation": sys.implementation.name,
    "full_version": sys.version, "cwd": str(Path.cwd()),
    "pythonpath": os.environ["PYTHONPATH"], "git": os.environ["PONTIUS_GIT"],
    "environment_keys": sorted(os.environ), "flags": ["-B", "-P"],
}}, sort_keys=True), flush=True)

commit = "47d08d8c1556d776358e15811e3e98b859fd6a8b"
base = "b357d333fc2393b7fc7dcf31f30c86616208c817"
manifest_expected = "cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a"
packet = Path("D:/Pontius-handoffs/v0a-i01-impl/r003")
def git(*args):
    return subprocess.run([os.environ["PONTIUS_GIT"], "-C", str(snapshot), *args],
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
assert git("rev-parse", "HEAD").decode().strip() == commit
assert git("rev-parse", commit + "^").decode().strip() == base
fields = git("diff-tree", "-r", "-z", "--no-commit-id", "--no-renames",
             "--name-status", base, commit).split(b"\0")
rows = []
for index in range(0, len(fields) - 1, 2):
    status, path = fields[index:index + 2]
    digest = ("0" * 64 if status == b"D" else
              hashlib.sha256(git("cat-file", "blob", commit + ":" + path.decode())).hexdigest())
    rows.append(digest.encode() + b"  " + path + b"\n")
manifest = b"".join(sorted(rows))
assert hashlib.sha256(manifest).hexdigest() == manifest_expected
assert manifest == (packet / "manifest.sha256").read_bytes()
assert not git("status", "--porcelain")
print(json.dumps({"manifest": {"commit": commit, "base": base, "rows": len(rows),
    "sha256": hashlib.sha256(manifest).hexdigest(), "whole_row_sort": True,
    "packet_bytes_identical": True}}, sort_keys=True), flush=True)

from pontius.holdem_cards import OneSeatCardState
from pontius.immutable_blueprint import BlueprintActionEntry, BlueprintDecisionKey
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.no_limit_betting import NoLimitBettingState, raise_to
from pontius.v0a.model import ActionMailbox, HandStartedEvent
from pontius.v0a.runtime import HandRuntime
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost
import pontius.v0a.runtime as runtime_module

assert Path(runtime_module.__file__).resolve() == snapshot / "src/pontius/v0a/runtime.py"
print(json.dumps({"payload_origin": runtime_module.__file__}), flush=True)

class StepClock:
    def __init__(self, *, fail_at=None, jump_at=None, jump=0):
        self.reads = 0
        self.now = 1000
        self.fail_at = fail_at
        self.jump_at = jump_at
        self.jump = jump
    def __call__(self):
        self.reads += 1
        if self.reads == self.fail_at:
            raise ValueError("cold-a scheduled source fault")
        if self.reads == self.jump_at:
            self.now += self.jump
        value = self.now
        self.now += 1000
        return value

start = HandStartedEvent(hand_id="cold-a-policy", event_index=0, button=0,
    controlled_seat=3, starting_stacks=(200,) * 6, small_blind=1, big_blind=2,
    private_cards=(0, 13))
state = NoLimitBettingState.new_hand(button=0, starting_stacks=(200,) * 6,
                                    small_blind=1, big_blind=2)
cards = OneSeatCardState.preflop(controlled_seat=3, private_hand=(0, 13))
key = BlueprintDecisionKey.from_state(cards=cards, betting=state, decision=state.legal_decision())
empty = ImmutableBlueprintActionSource(source_id="cold-a-bound-empty")
class DigestOverride(ImmutableBlueprintActionSource):
    @property
    def digest(self):
        return empty.digest
class CanonicalOverride(ImmutableBlueprintActionSource):
    def canonical_bytes(self):
        return empty.canonical_bytes()

policy_results = []
for source in (empty,
               DigestOverride(source_id=empty.source_id, entries=(BlueprintActionEntry(key, raise_to(6)),)),
               CanonicalOverride(source_id=empty.source_id, entries=(BlueprintActionEntry(key, raise_to(6)),))):
    mailbox = ActionMailbox()
    runtime = HandRuntime(blueprint=source, mailbox=mailbox, clock=StepClock())
    result = runtime.dispatch(start)
    actual_canonical = hashlib.sha256(ImmutableBlueprintActionSource.canonical_bytes(source)).hexdigest()
    policy_results.append({"source_type": type(source).__name__, "status": result.status,
        "actual_canonical_sha256": actual_canonical, "reported_sha256": source.digest,
        "recorded_sha256": result.decision.blueprint_sha256,
        "selected_action": result.decision.selected_action.kind,
        "raise_to": result.decision.selected_action.raise_to,
        "selection_reason": result.decision.selection_reason.value,
        "failure": None if result.failure is None else result.failure.code.value,
        "real_mailbox_acceptances": len(mailbox.accepted)})
assert policy_results[0]["selected_action"] == "call"
for row in policy_results[1:]:
    assert row["status"] == "decided" and row["selected_action"] == "raise"
    assert row["recorded_sha256"] == policy_results[0]["recorded_sha256"]
    assert row["actual_canonical_sha256"] != row["recorded_sha256"]
print(json.dumps({"r2_01_policy_binding": policy_results}, sort_keys=True), flush=True)

host_results = []
for fixture in (FIXTURE_A, FIXTURE_B):
    baseline_clock = StepClock()
    baseline = ReplayHost(fixture, run_id=f"{PROTOCOL_ID}-correctness-cold-a-count-{slot}-{fixture.name}",
        blueprint=empty, clock=baseline_clock).run()
    assert baseline.receipt.passed
    faults = []
    for fail_at in range(1, baseline_clock.reads + 1):
        clock = StepClock(fail_at=fail_at)
        outcome = ReplayHost(fixture,
            run_id=f"{PROTOCOL_ID}-correctness-cold-a-fault-{slot}-{fixture.name}-{fail_at}",
            blueprint=empty, clock=clock).run()
        assert not outcome.receipt.passed, fail_at
        assert not outcome.receipt.accounting_complete, fail_at
        assert clock.reads == fail_at, (fail_at, clock.reads)
        faults.append({"read": fail_at,
            "failure": None if outcome.receipt.failure_reason is None else outcome.receipt.failure_reason.value,
            "secondary": [code.value for code in outcome.receipt.secondary_failures],
            "real_mailbox_acceptances": len(outcome.decisions)})
    host_results.append({"fixture": fixture.name, "baseline_reads": baseline_clock.reads,
        "fault_positions_run": len(faults), "all_closed_failed": True,
        "clock_source_not_retried": True,
        "receipt_without_typed_cause_at_reads": [r["read"] for r in faults if r["failure"] is None and not r["secondary"]]})
print(json.dumps({"r2_03_exhaustive_source_faults": host_results}, sort_keys=True), flush=True)

# Observe real returned snapshots without replacing ledger computation.
real_outer = runtime_module.ActionClockLedger
class ObservedOuter(real_outer):
    records = []
    def finish_transition_boundary(self, *args, **kwargs):
        result = super().finish_transition_boundary(*args, **kwargs)
        if hasattr(result, "deadline_crossed"):
            self.records.append(("boundary", result))
        return result
    def snapshot(self):
        result = super().snapshot()
        self.records.append(("ready", result))
        return result
    def finish_action(self):
        result = super().finish_action()
        self.records.append(("closing", result))
        return result

runtime_module.ActionClockLedger = ObservedOuter
flag_cases = 0
try:
    baseline_clock = StepClock()
    HandRuntime(blueprint=empty, mailbox=ActionMailbox(), clock=baseline_clock).dispatch(start)
    for delay in (14_000_000_001, 16_000_000_000):
        for jump_at in range(2, baseline_clock.reads):
            for fail_at in range(jump_at + 1, baseline_clock.reads + 1):
                ObservedOuter.records = []
                clock = StepClock(fail_at=fail_at, jump_at=jump_at, jump=delay)
                result = HandRuntime(blueprint=empty, mailbox=ActionMailbox(), clock=clock).dispatch(start)
                assert result.status == "failed"
                timing = result.failure.timing
                known_deadline = any(s.deadline_crossed for _, s in ObservedOuter.records)
                known_cutoff = any(s.work_remaining_seconds <= 0.0 for stage, s in ObservedOuter.records
                                   if stage != "closing")
                if known_deadline:
                    assert timing is not None and timing.deadline_crossed is True, (jump_at, fail_at)
                if known_cutoff:
                    assert timing is not None and timing.work_cutoff_crossed is True, (jump_at, fail_at)
                flag_cases += 1
finally:
    runtime_module.ActionClockLedger = real_outer
print(json.dumps({"r2_02_snapshot_preservation": {"cases": flag_cases,
    "all_established_flags_preserved": True, "baseline_decision_reads": baseline_clock.reads}}, sort_keys=True), flush=True)
assert not git("status", "--porcelain")
print(json.dumps({"complete": True, "snapshot_pristine_after": True}), flush=True)
