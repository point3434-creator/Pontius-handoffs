"""Independently check the retained first v22 design run; execute no candidate."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
CHECKS = ROOT / "tests-checks"
RECEIPT = CHECKS / "focused-v22-first01-design-311-receipt.json"
RECEIPT_SHA = "0ce67a5f0846dd67655234cc27d51a560ee3711dda8f5b0a9194432ff6ee62fd"
SOURCE_SHA = "61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3"
OUTPUT = ROOT / "coordinator-v22-focused-red-verification-v1.json"
NOTE = ROOT / "coordinator-v22-first-floor-disposition-v1.md"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def emit_new(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
assert not OUTPUT.exists() and not NOTE.exists()
raw = RECEIPT.read_bytes()
assert sha(raw) == RECEIPT_SHA
receipt = json.loads(raw)
assert receipt["schema"] == "c-authority-focused-control-v1"
assert receipt["kind"] == "design" and receipt["slot"] == "311"
assert receipt["source_sha256"] == SOURCE_SHA
assert receipt["integrity"] is True and receipt["timed_out"] is False
assert receipt["success"] is False
assert receipt["exit"] == receipt["actual_process_returncode"] == 1
assert receipt["outcome"] == "focused_test_failure" and receipt["errors"] == []
assert receipt["inputs_before"] == receipt["inputs_after"]
for item in receipt["inputs_before"].values():
    assert sha(Path(item["path"]).read_bytes()) == item["sha256"], item["path"]
snapshot = Path(receipt["snapshot"])
assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots"))
assert receipt["before"] == receipt["after"] and len(receipt["before"]) == 1766
for name, expected in receipt["before"].items():
    relative = Path(name)
    assert not relative.is_absolute() and ".." not in relative.parts
    assert sha((snapshot / relative).read_bytes()) == expected, name
manifest = json.loads((snapshot / ".focused-authority/manifest.json").read_bytes())
assert len(manifest["files"]) == 1765 and manifest["tracked_count"] == 1761
assert all(receipt["before"][name] == expected
           for name, expected in manifest["files"].items())
outputs = {}
for role, item in receipt["outputs"].items():
    data = Path(item["path"]).read_bytes()
    assert sha(data) == item["sha256"] and len(data) == item["bytes"], role
    outputs[role] = data
assert outputs["log"] == (outputs["stdout"] + outputs["stderr"]).replace(b"\r\n", b"\n")
setup = json.loads(outputs["setup"])
assert setup["before"] == receipt["before"] and len(setup["original"]) == 1761
assert {name for name, value in setup["original"].items()
        if receipt["before"][name] != value} == {"tools/generate_test_inventory.py"}
rows = [json.loads(line)["focused_control"] for line in outputs["stdout"].splitlines()
        if line.startswith(b'{"focused_control"')]
identity, = [row for row in rows if row["event"] == "identity"]
summary, = [row for row in rows if row["event"] == "unittest_summary"]
assert identity == receipt["verification"]["identity"]
assert identity["version"] == [3, 11, 15]
assert Path(identity["executable"]) == Path(r"D:\Pontius-tools\py311\Scripts\python.exe")
assert identity["source_sha256"] == SOURCE_SHA
assert summary == receipt["verification"]["summary"]
assert summary["tests_run"] == 53 and summary["complete_population"] is True
assert summary["errors"] == summary["skips"] == summary["expected_failures"] == []
assert summary["unexpected_successes"] == []
expected_failures = [
    "focused_frozen_tests.DesignReviewTests.test_analysis_budgets_contain_deep_helpers_and_invalid_ranges",
    "focused_frozen_tests.DesignReviewTests.test_round4_source_order_and_branch_bounds_red_contracts_are_independent",
]
assert summary["failures"] == expected_failures
assert len(summary["started_ids"]) == len(summary["completed_ids"]) == 53
stderr = outputs["stderr"].decode()
assert stderr.count("does not match \"analysis work units exceed 262144\"") == 2
assert "line 4949" in stderr and "line 14551" in stderr
result = {
    "schema": "coordinator-v22-focused-red-verification-v1",
    "receipt": str(RECEIPT), "receipt_sha256": RECEIPT_SHA,
    "source_sha256": SOURCE_SHA, "snapshot_files_rehashed": len(receipt["before"]),
    "tests_run": 53, "passed": 51, "failures": expected_failures, "errors": 0,
    "actual_interpreter": identity["version"], "outputs": receipt["outputs"],
    "integrity_independently_verified": True,
    "interpretation": "Work-cap rejection precedes expected depth rejection in helper1050 and generator70 fixtures.",
    "scope_limit": "Not a full function pass for either failed method; later assertions in those methods did not run.",
    "next": "Hold matrix, dev and public24 expansion. Diagnose exact failing cases with original budget/caps unchanged.",
}
emit_new(OUTPUT, (json.dumps(result, indent=2) + "\n").encode())
note = f"""# v22 first floor disposition

Engineering evidence, not a cold review or an integration verdict.

The first retained v22 candidate ({SOURCE_SHA}) completed all 53 original
design test methods on actual CPython 3.11.15: 51 passed, two failed, no errors,
skips or timeout. Receipt SHA-256: {RECEIPT_SHA}.

Both failures are work-cap rejection before the expected depth rejection:
the 1050-helper source at original test line 4949, and the 70-generator source
at line 14551. The unchanged 32-generator assertion before the latter was
reached and passed; this closes the specific v20 chain32 failure only. Later
assertions after an exception in a failed method are not counted as exercised.

The coordinator independently rehashed all 1766 tracked/payload files and all
retained input/output pins. The snapshot contains 1761 original tracked paths;
only its generator differs from r010. W remains v20 and the retained candidate
is untouched. See {OUTPUT.name}.

Matrix, public24, dev-slot and corpus expansion remain held. The next allowed
engineering step is a floor-only diagnosis of these exact two failing source
cases. Sensitive fixtures remain AST-only; original consume logic, caps, tests,
and semantic expectations are unchanged. No message-only permission can turn
these failures into a pass. No source integration, main commit or main push
has occurred.
"""
emit_new(NOTE, note.encode())
emit_new(ROOT / "coordinator-verify-v22-focused-red-v1.py", Path(__file__).read_bytes())
print(json.dumps({"verified": True, "report": str(OUTPUT),
                  "report_sha256": sha(OUTPUT.read_bytes()),
                  "note_sha256": sha(NOTE.read_bytes())}))
