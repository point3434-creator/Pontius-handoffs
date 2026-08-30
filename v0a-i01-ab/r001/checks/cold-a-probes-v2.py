"""Independent R2-03 real-boundary probes. No production monkeypatches."""
import dataclasses
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
from collections import Counter

expected = sys.argv[1]
assert platform.python_version() == expected
assert sys.flags.safe_path and sys.flags.dont_write_bytecode
SNAP = Path(r"D:\pontius-snapshots\v0a-i01-ab-r001-cold-a-20260830")
CHECKS = Path(r"D:\Pontius-handoffs\v0a-i01-ab\r001\checks")
assert Path.cwd() == SNAP
assert os.environ["PYTHONPATH"] == str(SNAP / "src")
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.clock import ClockInvalidError, ClockReversedError, MonotonicWitness
from pontius.v0a.model import ActionMailbox
from pontius.v0a.replay import (
    FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost, chip_depth_settlement,
)
from pontius.v0a import clock as clock_module, runtime as runtime_module, replay as replay_module
for module in (clock_module, runtime_module, replay_module):
    assert Path(module.__file__).is_relative_to(SNAP / "src")

rows = []
failures = []
controls = {}
hooks = []
KINDS = ("bool", "negative", "reverse", "source_error", "base_error", "hostile_reverse")

class HostileReverse(ClockReversedError):
    def __getattribute__(self, name):
        if name in ("__class__", "__traceback__", "__context__", "__cause__", "args"):
            hooks.append(name)
            raise RuntimeError("hostile metadata")
        return super().__getattribute__(name)
    def __str__(self):
        hooks.append("str")
        raise RuntimeError("hostile rendering")
    def __repr__(self):
        hooks.append("repr")
        raise RuntimeError("hostile repr")
    def __setattr__(self, name, value):
        if name == "__traceback__":
            hooks.append("set_traceback")
            raise RuntimeError("hostile traceback write")
        return super().__setattr__(name, value)

class Source:
    def __init__(self, at=None, kind="bool", events=None):
        self.calls = 0
        self.at = at
        self.kind = kind
        self.events = [] if events is None else events
        self.failed_at = None
    def __call__(self):
        self.calls += 1
        if self.calls != self.at:
            return 100000 + self.calls * 1000
        code = ("clock_reversed" if self.kind in ("reverse", "hostile_reverse")
                else "clock_invalid")
        self.events.append({"origin": "source", "code": code, "call": self.calls,
                            "kind": self.kind})
        self.failed_at = self.calls
        if self.kind == "bool":
            return True
        if self.kind == "negative":
            return -1
        if self.kind == "reverse":
            if self.calls == 1:
                raise ClockReversedError("first source reports reversal")
            return 100000 + (self.calls - 2) * 1000
        if self.kind == "source_error":
            raise OSError("source lost")
        if self.kind == "base_error":
            raise KeyboardInterrupt()
        if self.kind == "hostile_reverse":
            raise HostileReverse()
        raise AssertionError("unknown scheduled kind")

def host_for(fixture, source, oracle=chip_depth_settlement):
    return ReplayHost(
        fixture, run_id=f"{PROTOCOL_ID}-correctness-cold-a-{len(rows)}",
        blueprint=ImmutableBlueprintActionSource(source_id="cold-a-frozen-policy"),
        clock=source, settlement_oracle=oracle,
    )

def cause_codes(outcome):
    receipt = outcome.receipt
    return [code.value for code in (receipt.failure_reason, *receipt.secondary_failures)
            if code is not None]

def stable_decision(record):
    data = dataclasses.asdict(record)
    data.pop("timing")
    data.pop("failure_reason")
    return data

def checked_run(category, fixture, source, host, wanted_events, *, full=False,
                detail=None, run_kwargs=None):
    escaped = False
    outcome = None
    try:
        outcome = host.run(**(run_kwargs or {}))
    except BaseException:
        escaped = True
    errors = []
    wanted = [item["code"] for item in wanted_events]
    actual = None if escaped else cause_codes(outcome)
    if escaped:
        errors.append("escaped_without_receipt")
    elif actual != wanted:
        errors.append("ordered_cause_mismatch")
    if not escaped:
        if wanted and outcome.receipt.passed:
            errors.append("false_success")
        if not wanted and not outcome.receipt.passed:
            errors.append("false_failure")
        decisions = {item.action_index: item for item in outcome.decisions}
        accepted = host.mailbox.accepted
        if len(decisions) != len(accepted) or len(decisions) != host.runtime.accepted_delivery_count:
            errors.append("accepted_decision_count")
        baseline = controls[fixture.name]["decisions"]
        for key, envelope in accepted.items():
            record = decisions.get(envelope.action_index)
            if record is None or record.selected_action != envelope.action:
                errors.append("accepted_action_lost")
            elif stable_decision(record) != stable_decision(baseline[envelope.action_index]):
                errors.append("accepted_context_changed")
            elif record.timing.status.value == "completed" and record != baseline[record.action_index]:
                errors.append("completed_decision_changed")
        if full and len(decisions) != fixture.expected_controlled_actions:
            errors.append("late_fault_erased_actions")
        if source.failed_at is not None:
            if source.calls != source.failed_at:
                errors.append("dead_source_retried")
            if outcome.receipt.accounting_complete:
                errors.append("fault_claimed_complete_accounting")
        # Repeated public observations cannot invent or drop occurrences.
        if [c.value for c in host.runtime.closure_failures] != wanted:
            errors.append("reobservation_changes_journal")
        host.runtime.finalize_accounting()
        if [c.value for c in host.runtime.closure_failures] != wanted:
            errors.append("repeated_finalize_changes_journal")
    row = {"category": category, "fixture": fixture.name, "detail": detail,
           "source_calls": source.calls, "events": list(wanted_events),
           "wanted": wanted, "actual": actual, "errors": sorted(set(errors)),
           "accepted": None if escaped else len(host.mailbox.accepted)}
    rows.append(row)
    if errors:
        failures.append(row)
    return outcome

# Independently observe the whole source-call population and settlement entry.
for fixture in (FIXTURE_A, FIXTURE_B):
    source = Source()
    observed_entry = []
    def oracle(**kwargs):
        observed_entry.append(source.calls)
        return chip_depth_settlement(**kwargs)
    host = host_for(fixture, source, oracle)
    result = host.run()
    assert result.receipt.passed
    controls[fixture.name] = {
        "calls": source.calls, "settlement_entry": observed_entry[0],
        "decisions": {item.action_index: item for item in result.decisions},
    }

# Every actually reached clock read, including initial/transition/response/delivery,
# settlement, terminal construction and finalization; whole cause list, not membership.
for fixture in (FIXTURE_A, FIXTURE_B):
    for kind in KINDS:
        for at in range(1, controls[fixture.name]["calls"] + 1):
            source = Source(at, kind)
            host = host_for(fixture, source)
            checked_run("whole_source_sweep", fixture, source, host, source.events,
                        detail={"kind": kind, "at": at})

# Public settlement callback: original source vs dead-witness refusal, caught source,
# independent equal code and ordinary failure. No ledger or runtime helper is replaced.
for fixture in (FIXTURE_A, FIXTURE_B):
    for where in ("entry", "body"):
        for kind in KINDS:
            for response in ("echo", "caught_return", "caught_mismatch",
                             "caught_ordinary", "caught_independent_same_code"):
                events = []
                source = Source(kind=kind, events=events)
                if where == "entry":
                    source.at = controls[fixture.name]["settlement_entry"]
                witness = MonotonicWitness(source)
                def oracle(**kwargs):
                    if where == "body":
                        source.at = source.calls + 1
                    if response == "echo":
                        witness()
                    else:
                        try:
                            witness()
                        except (ClockInvalidError, ClockReversedError):
                            pass
                    if response == "caught_ordinary":
                        events.append({"origin": "body", "code": "settlement_mismatch"})
                        raise ValueError("settlement cannot finish")
                    if response == "caught_independent_same_code":
                        code = ("clock_reversed" if kind in ("reverse", "hostile_reverse")
                                else "clock_invalid")
                        events.append({"origin": "independent_body", "code": code})
                        raise (ClockReversedError("separate") if code == "clock_reversed"
                               else ClockInvalidError("separate"))
                    result = chip_depth_settlement(**kwargs)
                    if response == "caught_mismatch":
                        events.append({"origin": "comparison", "code": "settlement_mismatch"})
                        result = dataclasses.replace(
                            result, final_stacks=tuple(x + 1 for x in result.final_stacks))
                    return result
                host = host_for(fixture, witness, oracle)
                checked_run("witness_identity", fixture, source, host, events, full=True,
                            detail={"where": where, "kind": kind, "response": response})

class HostileOrdinary(Exception):
    def __getattribute__(self, name):
        if name in ("__class__", "__traceback__", "__context__", "__cause__", "args"):
            hooks.append(name)
            raise RuntimeError("hostile metadata")
        return super().__getattribute__(name)
    def __str__(self):
        hooks.append("str")
        raise RuntimeError("hostile str")
    def __repr__(self):
        hooks.append("repr")
        raise RuntimeError("hostile repr")
    def __setattr__(self, name, value):
        if name == "__traceback__":
            hooks.append("set_traceback")
            raise RuntimeError("hostile traceback")
        return super().__setattr__(name, value)

class PretendClock(Exception):
    @property
    def __class__(self):
        hooks.append("spoofed_class")
        return ClockReversedError

class BadArgument:
    def __str__(self):
        hooks.append("argument_str")
        raise RuntimeError("argument cannot render")

ERRORS = {
    "ordinary": lambda: ValueError("plain"),
    "bad_argument": lambda: ValueError(BadArgument()),
    "hostile": HostileOrdinary,
    "spoofed": PretendClock,
    "stop_iteration": lambda: StopIteration("stop"),
    "system_exit": lambda: SystemExit(99),
    "generator_exit": GeneratorExit,
    "hostile_typed_reverse": HostileReverse,
}
# Error presentation and transfer at both real public operation bodies. For terminal
# publication the real writer reaches a failing path conversion; no writer double.
for fixture in (FIXTURE_A, FIXTURE_B):
    for boundary in ("settlement", "publication"):
        for error_name, factory in ERRORS.items():
            for cleanup_kind in (None, "bool", "reverse", "source_error"):
                events = []
                source = Source(events=events)
                error = factory()
                def fault():
                    if cleanup_kind is not None:
                        source.kind = cleanup_kind
                        source.at = source.calls + 1
                    code = ("clock_reversed" if error_name == "hostile_typed_reverse"
                            else "settlement_mismatch" if boundary == "settlement"
                            else "trace_write_failed")
                    events.append({"origin": "body", "code": code, "error_kind": error_name})
                    raise error
                def oracle(**kwargs):
                    fault()
                class Destination:
                    def __fspath__(self):
                        fault()
                host = host_for(fixture, source,
                                oracle if boundary == "settlement" else chip_depth_settlement)
                with tempfile.TemporaryDirectory(prefix="cold-a-probe-", dir=CHECKS) as temp:
                    kwargs = ({"destination": Destination(), "run_root": Path(temp)}
                              if boundary == "publication" else {})
                    checked_run("hostile_operation", fixture, source, host, events, full=True,
                                detail={"boundary": boundary, "error": error_name,
                                        "cleanup": cleanup_kind}, run_kwargs=kwargs)

# Three independent occurrences, using real output refusal as the later writer fault.
# The source is scheduled separately; if it fails at entry the oracle remains active.
for fixture in (FIXTURE_A, FIXTURE_B):
    for source_where in (None, "settlement_entry", "settlement_exit",
                         "publication_entry", "publication_exit", "finalize"):
        for kind in ("bool", "reverse"):
            events = []
            source = Source(kind=kind, events=events)
            entry = controls[fixture.name]["settlement_entry"]
            offsets = {"settlement_entry": 0, "settlement_exit": 1,
                       "publication_entry": 2, "publication_exit": 3, "finalize": 4}
            if source_where is not None:
                source.at = entry + offsets[source_where]
            def oracle(**kwargs):
                events.append({"origin": "body", "code": "settlement_mismatch"})
                raise ValueError("independent settlement failure")
            host = host_for(fixture, source, oracle)
            with tempfile.TemporaryDirectory(prefix="cold-a-real-writer-", dir=CHECKS) as temp:
                path = Path(temp) / "already-present.jsonl"
                sentinel = b"untouched-existing-output\n"
                path.write_bytes(sentinel)
                class Destination:
                    def __fspath__(self):
                        events.append({"origin": "real_create_new_refusal",
                                       "code": "trace_write_failed"})
                        return str(path)
                checked_run("compound_real_writer", fixture, source, host, events, full=True,
                            detail={"source_where": source_where, "kind": kind},
                            run_kwargs={"destination": Destination(), "run_root": Path(temp)})
                assert path.read_bytes() == sentinel

# A real writer failure alone remains later than a genuine fresh typed body clock error.
for fixture in (FIXTURE_A, FIXTURE_B):
    for typed in ("invalid", "reversed"):
        events = []
        source = Source(events=events)
        def oracle(**kwargs):
            events.append({"origin": "typed_body",
                           "code": "clock_reversed" if typed == "reversed" else "clock_invalid"})
            raise ClockReversedError("body") if typed == "reversed" else ClockInvalidError("body")
        host = host_for(fixture, source, oracle)
        with tempfile.TemporaryDirectory(prefix="cold-a-body-write-", dir=CHECKS) as temp:
            path = Path(temp) / "exists"
            path.write_bytes(b"preserve")
            class Destination:
                def __fspath__(self):
                    events.append({"origin": "real_create_new_refusal", "code": "trace_write_failed"})
                    return str(path)
            checked_run("typed_body_then_writer", fixture, source, host, events, full=True,
                        detail={"typed": typed},
                        run_kwargs={"destination": Destination(), "run_root": Path(temp)})
            assert path.read_bytes() == b"preserve"

summary = {
    "version": sys.version, "executable": sys.executable,
    "module_files": [clock_module.__file__, runtime_module.__file__, replay_module.__file__],
    "counts": dict(Counter(row["category"] for row in rows)),
    "total": len(rows), "failed": len(failures), "metadata_hooks_touched": hooks,
    "controls": {key: {"source_calls": value["calls"],
                      "settlement_entry": value["settlement_entry"],
                      "accepted_decisions": len(value["decisions"])}
                 for key, value in controls.items()},
}
data = {"summary": summary, "failures": failures, "rows": rows}
output = CHECKS / ("cold-a-probes-v2-data-" + expected.replace(".", "") + ".json")
with output.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(data, stream, indent=2)
    stream.write("\n")
print(json.dumps(summary, sort_keys=True))
print("data_sha256", hashlib.sha256(output.read_bytes()).hexdigest())
sys.exit(1 if failures or hooks else 0)