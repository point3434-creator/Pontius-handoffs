"""Rehash the frozen v28 design run; execute no candidate or test code."""
from pathlib import Path
import hashlib
import json
import stat

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
PIN = "2002eab44b3ff699ad55298972696ad90aec2c2c38a9019cef12c848a9c0807a"
SOURCE = "4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e"
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def read(path):
    assert path.is_absolute() and ".." not in path.parts
    for ancestor in (path, *path.parents):
        assert not getattr(ancestor.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path.read_bytes()

raw = read(T / "tests-checks/focused-v28-first01-design-311-receipt.json")
assert digest(raw) == PIN
r = json.loads(raw)
assert r["source_sha256"] == SOURCE
assert r["integrity"] is True and r["timed_out"] is False and r["success"] is False
assert type(r["exit"]) is int and r["exit"] == r["actual_process_returncode"] == 1
assert r["errors"] == [] and r["outcome"] == "focused_test_failure"
assert r["inputs_before"] == r["inputs_after"]
for item in r["inputs_before"].values():
    assert digest(read(Path(item["path"]))) == item["sha256"]
snapshot = Path(r["snapshot"])
assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots"))
assert r["before"] == r["after"] and len(r["before"]) == 1766
for name, pin in r["before"].items():
    rel = Path(name)
    assert not rel.is_absolute() and not rel.drive and ".." not in rel.parts
    assert digest(read(snapshot / rel)) == pin
assert read(snapshot / ".git/HEAD").decode().strip() == "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
manifest_raw = read(snapshot / ".focused-authority/manifest.json")
assert digest(manifest_raw) == r["manifest_sha256"] == "07efb743b30e7cea58da2f05cf5ab8bbedc2d9d89eded420fa8cde4710416307"
manifest = json.loads(manifest_raw)
assert len(manifest["files"]) == 1765 and manifest["tracked_count"] == 1761
assert all(r["before"][name] == pin for name, pin in manifest["files"].items())
outputs = {key: read(Path(item["path"])) for key, item in r["outputs"].items()}
assert all(digest(outputs[key]) == item["sha256"] for key, item in r["outputs"].items())
assert outputs["log"] == (outputs["stdout"] + outputs["stderr"]).replace(b"\r\n", b"\n")
setup = json.loads(outputs["setup"])
assert setup["before"] == r["before"] and len(setup["original"]) == 1761
assert {name for name, pin in setup["original"].items() if r["before"][name] != pin} == {"tools/generate_test_inventory.py"}
rows = [json.loads(line)["focused_control"] for line in outputs["stdout"].splitlines() if line.startswith(b'{"focused_control"')]
identity, = [row for row in rows if row["event"] == "identity"]
summary, = [row for row in rows if row["event"] == "unittest_summary"]
assert identity == r["verification"]["identity"] and summary == r["verification"]["summary"]
assert identity["version"] == [3, 11, 15] and identity["source_sha256"] == SOURCE
assert type(summary["tests_run"]) is int and summary["tests_run"] == 53 and summary["complete_population"] is True
assert len(summary["started_ids"]) == len(summary["completed_ids"]) == 53
assert len(set(summary["started_ids"])) == 53 and summary["started_ids"] == summary["completed_ids"]
failed = [
    "focused_frozen_tests.DesignReviewTests.test_analysis_budgets_contain_deep_helpers_and_invalid_ranges",
    "focused_frozen_tests.DesignReviewTests.test_round4_source_order_and_branch_bounds_red_contracts_are_independent",
]
assert summary["failures"] == failed
assert summary["errors"] == summary["skips"] == summary["expected_failures"] == summary["unexpected_successes"] == []
helper65 = "focused_frozen_tests.DesignReviewTests.test_round4_analysis_budget_red_contracts_are_independent"
assert helper65 in summary["completed_ids"] and not any(helper65 in name for name in failed)
stderr = outputs["stderr"].decode()
assert stderr.count('does not match "analysis work units exceed 262144"') == 2
assert all("line " + line in stderr for line in ("4949", "14551"))
clarification = T / "coordinator-helper1050-contract-clarification-v1.json"
assert digest(read(clarification)) == "020b99d9e5fef402baf964eafd14fbda4416dc35bb2f095d27a7f3594d5de447"
report = {
    "schema": "coordinator-v28-design-verification-v1", "receipt_sha256": PIN,
    "source_sha256": SOURCE, "snapshot": str(snapshot), "manifest_sha256": r["manifest_sha256"],
    "files_rehashed": 1766, "version": identity["version"], "tests_run": 53,
    "passed": 51, "failed": failed, "errors": 0, "skips": 0,
    "helper65_exact_depth_method_passed": True,
    "helper1050": "Canonical work-cap refusal is allowed by the test's intended depth-or-budget category but not matched by its current regex. Original method remains failed; no expectation/source/cap changed.",
    "generator70": "Exact-depth method still gets work-cap refusal. Substantive analyzer fitness gate remains failed.",
    "payload_executed_by_verifier": False,
    "disposition": "Retain A+B result without integration. Primitive freeze evidence still required; no dev/matrix/corpus expansion from this failed design candidate. Identical-root C has zero measured hits and stays out."
}
data = (json.dumps(report, indent=2) + "\n").encode()
for name, content in {
    "coordinator-v28-design-verification-v1.json": data,
    "coordinator-verify-v28-design-v1.py": Path(__file__).read_bytes(),
}.items():
    with (T / name).open("xb") as stream:
        stream.write(content)
print(json.dumps({"report_sha256": digest(data), "files_rehashed": 1766, "tests_run": 53, "passed": 51, "failed": 2, "errors": 0}))
