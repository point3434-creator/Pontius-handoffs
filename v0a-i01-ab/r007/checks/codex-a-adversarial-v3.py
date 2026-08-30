"""Independent checks; no production helper replacements or candidate edits."""
import ctypes, json, sys, tempfile
from ctypes import wintypes
from pathlib import Path
from dataclasses import replace
from hashlib import sha256
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.model import FailureCode
from pontius.v0a.runtime import HandRuntime
from pontius.v0a.replay import ReplayHost, FIXTURE_A, FIXTURE_B, PROTOCOL_ID
import pontius.v0a.replay as replay
import pontius.v0a.trace as trace

NANO = 1_000_000_000
class Clock:
    def __init__(self):
        self.now = 1000
        self.fail_next = False
        self.failed = False
        self.reads_after_failure = 0
    def __call__(self):
        if self.failed:
            self.reads_after_failure += 1
            raise AssertionError("source sampled after failure")
        if self.fail_next:
            self.failed = True
            return True
        return self.now

def policy():
    return ImmutableBlueprintActionSource(source_id="codex-a-independent")

def host_for(fixture, clock, name):
    return ReplayHost(fixture, run_id=f"{PROTOCOL_ID}-correctness-codex-a-{name}",
                      blueprint=policy(), clock=clock)

def causes(outcome):
    receipt = outcome.receipt
    return [x.value for x in ((receipt.failure_reason,) + receipt.secondary_failures) if x]

def verify(content, fixture):
    return replay.verify_successful_trace(content, fixture=fixture, blueprint=policy(),
        source_commit="0"*40, source_manifest_sha256="0"*64,
        expected_mode="correctness", expected_clock_kind="deterministic_test")

def measured_native_control(fixture, label):
    clock = Clock()
    host = host_for(fixture, clock, label)
    totals = {"pre": 0, "post": 0, "publication": 0}
    calls = {}
    publication = False
    checked_boundaries = 0
    costs = {
        replay.Fixture.configuration_sha256.__code__: 1,
        ReplayHost._events.__code__: 2,
        trace.TraceBuilder.add_event.__code__: 3,
        trace.TraceBuilder.add_decision.__code__: 5,
        trace.TraceBuilder.add_failure.__code__: 7,
        replay.semantic_sha256.__code__: 11,
        trace.TraceWriter.append.__code__: 13,
        trace.TraceBuilder.close.__code__: 17,
        trace.TraceWriter.finish.__code__: 19,
        trace._NativeHandle.close.__code__: 23,
        replay.chip_depth_settlement.__code__: 29,
    }
    with tempfile.TemporaryDirectory(prefix="codex-a-measured-") as temporary:
        root = Path(temporary)
        target = root / "trace.jsonl"
        def observe(frame, event, arg):
            nonlocal publication, checked_boundaries
            if event != "call":
                return
            code = frame.f_code
            if code is HandRuntime.dispatch.__code__ and host.mailbox.accepted:
                rows = [json.loads(row) for row in target.read_bytes().splitlines()]
                delivered = [row for row in rows if row["record_type"] == "decision"]
                assert len(delivered) == len(host.mailbox.accepted)
                checked_boundaries += 1
            if code is trace.TraceBuilder.close.__code__:
                publication = True
            if code in costs:
                amount = costs[code]
                category = "publication" if publication else "post" if host.runtime.betting_terminal else "pre"
                totals[category] += amount
                calls[code.co_name] = calls.get(code.co_name, 0) + 1
                clock.now += amount * NANO
        old = sys.getprofile()
        sys.setprofile(observe)
        try:
            outcome = host.run(destination=target, run_root=root)
        finally:
            sys.setprofile(old)
        terminal = trace.parse_trace(outcome.trace).terminal
        assert outcome.receipt.passed, causes(outcome)
        assert target.read_bytes() == outcome.trace
        assert sha256(outcome.trace).hexdigest() == outcome.receipt.trace_sha256
        assert terminal["preparation_compute_seconds"] == totals["pre"], (terminal, totals)
        assert terminal["post_terminal_compute_seconds"] == totals["post"], (terminal, totals)
        assert outcome.receipt.terminal_publication_compute_seconds == totals["publication"]
        assert all(record.timing.elapsed_ns == 0 for record in outcome.decisions)
        assert outcome.settlement.payouts == fixture.expected_payouts
        assert len(outcome.decisions) == fixture.expected_controlled_actions
        assert verify(outcome.trace, fixture).payouts == fixture.expected_payouts
        assert checked_boundaries > 0
        print(json.dumps({"case": label, "totals_seconds": totals, "operation_calls": calls,
                          "published_boundaries": checked_boundaries}), flush=True)

kernel = ctypes.WinDLL("kernel32", use_last_error=True)
set_flags = kernel.SetHandleInformation
set_flags.argtypes, set_flags.restype = (wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD), wintypes.BOOL
get_flags = kernel.GetHandleInformation
get_flags.argtypes, get_flags.restype = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)), wintypes.BOOL
native_close = kernel.CloseHandle
native_close.argtypes, native_close.restype = (wintypes.HANDLE,), wintypes.BOOL


def native_close_schedule(number, closing_clock, existing=False):
    clock = Clock()
    host = host_for(FIXTURE_A, clock, f"native-close-{number}-{closing_clock}")
    protected, attempts, observed_errors, writers = [], [], [], []
    total_handles = None
    with tempfile.TemporaryDirectory(prefix="codex-a-close-") as temporary:
        root = Path(temporary)
        target = root / "trace.jsonl"
        if existing:
            target.write_bytes(b"existing sentinel")
        def observe(frame, event, arg):
            nonlocal total_handles
            if frame.f_code is trace.TraceWriter.close.__code__ and event == "call":
                writer = frame.f_locals["self"]
                if not writers:
                    writers.append(writer)
                    total_handles = len(writer._handles)
            if frame.f_code is trace._NativeHandle.close.__code__:
                if event == "call":
                    handle = frame.f_locals["self"].value.value
                    assert handle is not None
                    attempts.append(handle)
                    if len(protected) < number:
                        assert set_flags(wintypes.HANDLE(handle), 2, 2), ctypes.get_last_error()
                        flags = wintypes.DWORD()
                        assert get_flags(wintypes.HANDLE(handle), ctypes.byref(flags))
                        assert flags.value & 2
                        protected.append(handle)
                elif event == "exception":
                    error = arg[1]
                    if isinstance(error, trace.TraceWriteError):
                        observed_errors.append({"type": type(error).__name__, "args": error.args})
                elif event == "return" and closing_clock and len(attempts) == total_handles:
                    clock.fail_next = True
            return observe
        old = sys.gettrace()
        sys.settrace(observe)
        try:
            outcome = host.run(destination=target, run_root=root)
            count = len(attempts)
            writers[0].close()
            assert len(attempts) == count, "close-once violated"
        finally:
            sys.settrace(old)
            # Test-created protection is removed and only the explicitly saved
            # still-open native handles are reclaimed. No production state edit.
            for handle in protected:
                assert set_flags(wintypes.HANDLE(handle), 2, 0), ctypes.get_last_error()
                assert native_close(wintypes.HANDLE(handle)), ctypes.get_last_error()
        expected = ["trace_write_failed"] * (number + int(existing))
        if closing_clock:
            expected += ["clock_invalid"]
        assert causes(outcome) == expected, (causes(outcome), expected, observed_errors)
        assert len(observed_errors) == number, observed_errors
        assert len(attempts) == total_handles and len(set(attempts)) == total_handles
        assert not outcome.receipt.passed and outcome.receipt.trace_sha256 is None
        assert len(outcome.decisions) == len(host.mailbox.accepted) == (1 if existing else 4)
        terminal = trace.parse_trace(outcome.trace).terminal
        if existing:
            assert target.read_bytes() == b"existing sentinel"
            assert not terminal["passed"]
        else:
            assert target.read_bytes() == outcome.trace
            assert terminal["passed"] and terminal["complete"], "prepublication cut was altered"
            verify(outcome.trace, FIXTURE_A)  # Trace cannot establish later host completion.
        assert clock.reads_after_failure == 0
        if closing_clock:
            assert not outcome.receipt.accounting_complete
            assert outcome.receipt.terminal_publication_compute_seconds is None
        moved = root / "released.jsonl"
        target.rename(moved)
        print(json.dumps({"case": "native-close", "protected_handles": number,
            "closing_clock_fault": closing_clock, "existing_target": existing, "native_close_attempts": len(attempts),
            "actual_native_errors": observed_errors, "receipt_causes": causes(outcome),
            "terminal_cut_passed": terminal["passed"], "host_passed": outcome.receipt.passed}), flush=True)

def main():
    measured_native_control(FIXTURE_A, "A")
    measured_native_control(FIXTURE_B, "B")
    all_in = replace(FIXTURE_A, starting_stacks=(2,)*6, script=FIXTURE_A.script[:4],
                     expected_controlled_actions=1)
    measured_native_control(all_in, "automatic-all-in-runout")
    for number, clock_fault in ((1, False), (2, False), (2, True)):
        native_close_schedule(number, clock_fault)
    native_close_schedule(2, True, existing=True)
    print("INDEPENDENT_CASES_PASSED=7", flush=True)
