"""Rehash the frozen v28 plus reviewed test-correction design run; execute no candidate or test code."""
from pathlib import Path
import hashlib
import json
import stat

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
PIN = "bba7e6c5368fd0a513fb43e008f7b7d4437f0629ad14e4db5f1b79efb9f557f1"
SOURCE = "4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e"
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def read(path):
    assert path.is_absolute() and ".." not in path.parts
    for ancestor in (path, *path.parents):
        assert not getattr(ancestor.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path.read_bytes()

raw = read(T / "tests-checks/focused-v2-v28-testfix01-design-311-receipt.json")
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
manifest_raw = read(snapshot / ".focused-authority-v2/manifest.json")
assert digest(manifest_raw) == r["manifest_sha256"] == "1dd3bff060fa74f8ea15d084d217650a5c4d9f4ffab8dd90920e18185d6a7ec4"
manifest = json.loads(manifest_raw)
assert len(manifest["files"]) == 1765 and manifest["tracked_count"] == 1761
assert all(r["before"][name] == pin for name, pin in manifest["files"].items())
outputs = {key: read(Path(item["path"])) for key, item in r["outputs"].items()}
assert all(digest(outputs[key]) == item["sha256"] for key, item in r["outputs"].items())
assert outputs["log"] == (outputs["stdout"] + outputs["stderr"]).replace(b"\r\n", b"\n")
setup = json.loads(outputs["setup"])
assert setup["before"] == r["before"] and len(setup["original"]) == 1761
assert {name for name, pin in setup["original"].items() if r["before"][name] != pin} == {"tools/generate_test_inventory.py", "tests/test_inventory_and_profiles.py"}
rows = [json.loads(line)["focused_control"] for line in outputs["stdout"].splitlines() if line.startswith(b'{"focused_control"')]
identity, = [row for row in rows if row["event"] == "identity"]
summary, = [row for row in rows if row["event"] == "unittest_summary"]
assert identity == r["verification"]["identity"] and summary == r["verification"]["summary"]
assert identity["version"] == [3, 11, 15] and identity["source_sha256"] == SOURCE
assert r["schema"] == "c-authority-focused-control-v2"
assert identity["tests_sha256"] == r["tests_sha256"] == "48c4620bf5585a76d500b3c9bf4cad4559a04d4f544bc3808832d37b58b03add"
assert digest(read(T / "engineer-budget-assertion-candidate-review-v1.md")) == "faf1bdb169669c5e252cfe679e8e4ed0fb08f522a5a14d1c753d0c56664de10c"

assert type(summary["tests_run"]) is int and summary["tests_run"] == 53 and summary["complete_population"] is True
assert len(summary["started_ids"]) == len(summary["completed_ids"]) == 53
assert len(set(summary["started_ids"])) == 53 and summary["started_ids"] == summary["completed_ids"]
failed = [
    "focused_frozen_tests.DesignReviewTests.test_round4_source_order_and_branch_bounds_red_contracts_are_independent",
]
assert summary["failures"] == failed
assert summary["errors"] == summary["skips"] == summary["expected_failures"] == summary["unexpected_successes"] == []
helper65 = "focused_frozen_tests.DesignReviewTests.test_round4_analysis_budget_red_contracts_are_independent"
assert helper65 in summary["completed_ids"] and not any(helper65 in name for name in failed)
assert "focused_frozen_tests.DesignReviewTests.test_analysis_budgets_contain_deep_helpers_and_invalid_ranges" in summary["completed_ids"]

stderr = outputs["stderr"].decode()
assert stderr.count('does not match "analysis work units exceed 262144"') == 1
assert 'AssertionError: "^analysis deferred generator depth exceeds 64$" does not match "analysis work units exceed 262144"' in stderr
clarification = T / "coordinator-helper1050-contract-clarification-v1.json"
assert digest(read(clarification)) == "020b99d9e5fef402baf964eafd14fbda4416dc35bb2f095d27a7f3594d5de447"
report = {
    "schema": "coordinator-v28-testfix-verification-v2", "receipt_sha256": PIN,
    "source_sha256": SOURCE, "tests_sha256": r["tests_sha256"], "snapshot": str(snapshot), "manifest_sha256": r["manifest_sha256"],
    "files_rehashed": 1766, "version": identity["version"], "tests_run": 53,
    "passed": 52, "failed": failed, "errors": 0, "skips": 0,
    "helper65_exact_depth_method_passed": True,
    "helper1050": "The independently reviewed v5 regex now matches the same canonical work-cap refusal. This new candidate passes the method; prior original-test failures remain unchanged. No production code or cap changed.",
    "generator70": "Exact-depth method still gets work-cap refusal. Substantive analyzer fitness gate remains failed.",
    "payload_executed_by_verifier": False,
    "verifier_correction": "V1 stopped before report output on a mistaken physical traceback line assumption (14553 regex literal versus14551 with-statement). V2 binds the exact failure method and both canonical messages. No payload or evidence changed.",
    "disposition": "Isolated assertion correction confirmed; v28 plus v5 still fails generator70 exact-depth. Primitive evidence and the bounded join repair remain pending. No dev/matrix/corpus expansion or integration."
}
data = (json.dumps(report, indent=2) + "\n").encode()
for name, content in {
    "coordinator-v28-testfix-verification-v2.json": data,
    "coordinator-verify-v28-testfix-v2.py": Path(__file__).read_bytes(),
}.items():
    with (T / name).open("xb") as stream:
        stream.write(content)
print(json.dumps({"report_sha256": digest(data), "files_rehashed": 1766, "tests_run": 53, "passed": 52, "failed": 1, "errors": 0}))
