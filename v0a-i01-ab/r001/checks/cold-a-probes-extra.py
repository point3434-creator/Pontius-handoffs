"""Supplemental cold-A supported event-abort and higher-order occurrence probes."""
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
SNAP = Path(r"D:\Pontius-handoffs\v0a-i01-ab\r001\checks\cold-a-snapshot")
CHECKS = SNAP.parent
assert Path.cwd() == SNAP
assert os.environ["PYTHONPATH"] == str(SNAP / "src")
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.clock import ClockInvalidError, ClockReversedError, MonotonicWitness
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost, chip_depth_settlement
from pontius.v0a import clock, runtime, replay
for module in (clock, runtime, replay):
    assert Path(module.__file__).is_relative_to(SNAP / "src")

rows = []
class Source:
    def __init__(self, events, kind="invalid", at=None, abort=False):
        self.calls = 0
        self.events = events
        self.kind = kind
        self.at = at
        self.abort = abort
        self.failed = None
    def __call__(self):
        self.calls += 1
        frame = sys._getframe()
        names = []
        while frame is not None:
            names.append(frame.f_code.co_name)
            frame = frame.f_back
        hit = self.calls == self.at or (self.abort and "abort_transition_boundary" in names)
        if hit:
            code = "clock_reversed" if self.kind == "reversed" else "clock_invalid"
            self.events.append({"origin": "source", "code": code, "call": self.calls})
            self.failed = self.calls
            if self.kind == "reversed":
                return 100000 + (self.calls - 2) * 1000
            if self.kind == "source":
                raise OSError("source refuses")
            return True
        return 100000 + self.calls * 1000

def host_for(fixture, source, oracle=chip_depth_settlement):
    return ReplayHost(
        fixture, run_id=f"{PROTOCOL_ID}-correctness-cold-a-extra-{len(rows)}",
        blueprint=ImmutableBlueprintActionSource(source_id="cold-a-extra"),
        clock=source, settlement_oracle=oracle)

def codes(result):
    return [c.value for c in (result.receipt.failure_reason, *result.receipt.secondary_failures)
            if c is not None]

def stable(record):
    value = dataclasses.asdict(record)
    value.pop("timing")
    value.pop("failure_reason")
    return value

controls = {}
for fixture in (FIXTURE_A, FIXTURE_B):
    source = Source([])
    entry = []
    def oracle(**kwargs):
        entry.append(source.calls)
        return chip_depth_settlement(**kwargs)
    host = host_for(fixture, source, oracle)
    result = host.run()
    assert result.receipt.passed
    controls[fixture.name] = {"entry": entry[0],
                             "decisions": {d.action_index: d for d in result.decisions}}

def run_check(label, fixture, source, host, events, **kwargs):
    result = None
    escaped = False
    try:
        result = host.run(**kwargs)
    except BaseException:
        escaped = True
    problems = []
    wanted = [item["code"] for item in events]
    actual = None if escaped else codes(result)
    if escaped:
        problems.append("no_receipt")
    elif actual != wanted:
        problems.append("cause_conservation")
    if not escaped:
        if result.receipt.passed:
            problems.append("false_success")
        if source.failed is None or source.calls != source.failed:
            problems.append("fault_unreached_or_retried")
        accepted = host.mailbox.accepted
        by_index = {item.action_index: item for item in result.decisions}
        if len(accepted) != len(by_index):
            problems.append("accepted_decision_count")
        if host.runtime.accepted_delivery_count != len(accepted):
            problems.append("accepted_runtime_count")
        for envelope in accepted.values():
            record = by_index.get(envelope.action_index)
            control = controls[fixture.name]["decisions"].get(envelope.action_index)
            if record is None or control is None or stable(record) != stable(control):
                problems.append("delivered_decision_changed")
        if result.receipt.accounting_complete:
            problems.append("fault_accounting_complete")
    row = {"category": label, "fixture": fixture.name, "events": list(events),
           "actual": actual, "wanted": wanted, "source_calls": source.calls,
           "problems": problems,
           "accepted": None if escaped else len(host.mailbox.accepted)}
    rows.append(row)

# Independent invalid input: wrong controlled actor at early and late scripted
# positions. Stack observation selects the real sealed abort path for injection;
# it does not replace the ledger. Input validity defines the expected event code.
for fixture in (FIXTURE_A, FIXTURE_B):
    for position in (0, len(fixture.script)-1):
        script = list(fixture.script)
        script[position] = dataclasses.replace(script[position], seat=fixture.controlled_seat)
        rejected = dataclasses.replace(fixture, script=tuple(script))
        for kind in ("invalid", "reversed", "source"):
            events = [{"origin": "known_invalid_event", "code": "event_order",
                       "script_position": position}]
            source = Source(events, kind=kind, abort=True)
            host = host_for(rejected, source)
            run_check("real_rejected_event_abort", fixture, source, host, events)

# One genuine source fault, a separate body exception with the same enum, and a
# separate real writer-path conversion error with that enum: three actual causes.
# Repeated dead-witness reads are caught and must not add a fourth/fifth.
for fixture in (FIXTURE_A, FIXTURE_B):
    for kind in ("invalid", "reversed"):
        for where in ("entry", "cleanup"):
            events = []
            entry = controls[fixture.name]["entry"]
            source = Source(events, kind=kind, at=entry if where == "entry" else entry+1)
            witness = MonotonicWitness(source)
            error_type = ClockReversedError if kind == "reversed" else ClockInvalidError
            code = "clock_reversed" if kind == "reversed" else "clock_invalid"
            def oracle(**kwargs):
                if where == "entry":
                    for _ in range(3):
                        try:
                            witness()
                        except (ClockInvalidError, ClockReversedError):
                            pass
                events.append({"origin": "independent_oracle_error", "code": code})
                raise error_type("a separate oracle occurrence")
            class Destination:
                def __fspath__(self):
                    for _ in range(3):
                        try:
                            witness()
                        except (ClockInvalidError, ClockReversedError):
                            pass
                    events.append({"origin": "independent_writer_path_error", "code": code})
                    raise error_type("a separate destination occurrence")
            host = host_for(fixture, witness, oracle)
            with tempfile.TemporaryDirectory(prefix="cold-a-triple-", dir=CHECKS) as temp:
                run_check("three_equal_codes", fixture, source, host, events,
                          destination=Destination(), run_root=Path(temp))

summary = {"version": sys.version, "executable": sys.executable,
           "counts": dict(Counter(row["category"] for row in rows)),
           "total": len(rows), "failed": sum(bool(row["problems"]) for row in rows)}
output = CHECKS / ("cold-a-probes-extra-data-" + expected.replace(".", "") + ".json")
with output.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump({"summary": summary, "rows": rows}, stream, indent=2)
    stream.write("\n")
print(json.dumps(summary, sort_keys=True))
print("data_sha256", hashlib.sha256(output.read_bytes()).hexdigest())
sys.exit(1 if summary["failed"] else 0)