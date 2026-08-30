from pathlib import Path
# Reuse the create-only diagnostic's identity/manifest/import prelude verbatim.
# It asserts the interpreter before its first pontius import.
prelude_path = Path("D:/Pontius-handoffs/v0a-i01-impl/r003/checks/cold-a-diagnostics.py")
prelude = prelude_path.read_text(encoding="utf-8").split("class StepClock:", 1)[0]
exec(compile(prelude, str(prelude_path), "exec"))
import traceback

class ClockWithCause:
    def __init__(self, fail_at, kind):
        self.reads = 0
        self.now = 1000
        self.fail_at = fail_at
        self.kind = kind
        self.site = []
    def __call__(self):
        self.reads += 1
        if self.reads == self.fail_at:
            self.site = [{"name": frame.name, "line": frame.lineno,
                          "file": Path(frame.filename).name}
                         for frame in traceback.extract_stack()[-8:-1]]
            if self.kind == "invalid":
                raise ValueError("cold-a host accounting clock fault")
            return 0
        value = self.now
        self.now += 1000
        return value

source = ImmutableBlueprintActionSource(source_id="cold-a-host-cause")
rows = []
for kind in ("invalid", "reversed"):
    for fail_at in range(134, 139):
        clock = ClockWithCause(fail_at, kind)
        host = ReplayHost(FIXTURE_A,
            run_id=f"{PROTOCOL_ID}-correctness-cold-a-cause-{slot}-{kind}-{fail_at}",
            blueprint=source, clock=clock)
        outcome = host.run()
        terminal = json.loads(outcome.trace.splitlines()[-1])
        receipt = outcome.receipt
        assert clock.reads == fail_at
        assert not receipt.passed and not receipt.accounting_complete
        assert receipt.failure_reason is None and receipt.secondary_failures == ()
        rows.append({"fault_kind": kind, "fault_read": fail_at, "site": clock.site,
            "receipt": {"passed": receipt.passed,
                "accounting_complete": receipt.accounting_complete,
                "failure_reason": receipt.failure_reason,
                "secondary_failures": receipt.secondary_failures,
                "terminal_publication_compute_seconds": receipt.terminal_publication_compute_seconds},
            "failure_rows": len(outcome.failures),
            "terminal_claims": {name: terminal[name] for name in (
                "complete", "passed", "accounting_complete", "failure_reason")}})
print(json.dumps({"r2_03_dropped_host_clock_causes": rows}, sort_keys=True))
assert not git("status", "--porcelain")
print(json.dumps({"complete": True, "snapshot_pristine_after": True}))
