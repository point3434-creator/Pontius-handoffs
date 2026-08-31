"""Independent read-only verification of the latest bounded failed runs."""
from pathlib import Path
import hashlib
import json
import stat

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
h = lambda raw: hashlib.sha256(raw).hexdigest()
def read(path):
    assert path.is_absolute() and ".." not in path.parts
    for ancestor in (path, *path.parents):
        assert not getattr(ancestor.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path.read_bytes()
def snapshot_hashes(r):
    path = Path(r["snapshot"])
    assert path.is_relative_to(Path(r"D:\pontius-snapshots"))
    assert r["before"] == r["after"]
    for name, digest in r["before"].items():
        rel = Path(name)
        assert not rel.is_absolute() and not rel.drive and ".." not in rel.parts
        assert h(read(path / rel)) == digest
    assert read(path / ".git/HEAD").decode().strip() == "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
    outputs = {key: read(Path(item["path"])) for key, item in r["outputs"].items()}
    assert all(h(outputs[key]) == item["sha256"] for key, item in r["outputs"].items())
    return path, outputs

v26_pin = "284ddc5bbadbcc2f46c89b8a0ae782eeadade716090d3788ae122d591b1ef7fe"
v26_raw = read(C / "focused-v26-first01-design-311-receipt.json")
assert h(v26_raw) == v26_pin
r = json.loads(v26_raw)
assert r["source_sha256"] == "1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951"
assert r["integrity"] is True and r["timed_out"] is False and r["success"] is False
assert type(r["exit"]) is int and r["exit"] == r["actual_process_returncode"] == 1
assert r["errors"] == [] and r["outcome"] == "focused_test_failure"
assert r["inputs_before"] == r["inputs_after"]
for item in r["inputs_before"].values():
    assert h(read(Path(item["path"]))) == item["sha256"]
snapshot, outputs = snapshot_hashes(r)
assert len(r["before"]) == 1766
manifest_raw = read(snapshot / ".focused-authority/manifest.json")
assert h(manifest_raw) == r["manifest_sha256"]
manifest = json.loads(manifest_raw)
assert len(manifest["files"]) == 1765 and manifest["tracked_count"] == 1761
assert all(r["before"][name] == digest for name, digest in manifest["files"].items())
assert outputs["log"] == (outputs["stdout"] + outputs["stderr"]).replace(b"\r\n", b"\n")
setup = json.loads(outputs["setup"])
assert setup["before"] == r["before"] and len(setup["original"]) == 1761
assert {name for name, value in setup["original"].items() if r["before"][name] != value} == {"tools/generate_test_inventory.py"}
rows = [json.loads(line)["focused_control"] for line in outputs["stdout"].splitlines() if line.startswith(b'{"focused_control"')]
identity, = [row for row in rows if row["event"] == "identity"]
summary, = [row for row in rows if row["event"] == "unittest_summary"]
assert identity == r["verification"]["identity"] and summary == r["verification"]["summary"]
assert identity["version"] == [3, 11, 15] and identity["source_sha256"] == r["source_sha256"]
assert type(summary["tests_run"]) is int and summary["tests_run"] == 53 and summary["complete_population"] is True
assert len(summary["started_ids"]) == len(summary["completed_ids"]) == 53
failed_methods = [
    "focused_frozen_tests.DesignReviewTests.test_analysis_budgets_contain_deep_helpers_and_invalid_ranges",
    "focused_frozen_tests.DesignReviewTests.test_round4_analysis_budget_red_contracts_are_independent (boundary='helper-depth')",
    "focused_frozen_tests.DesignReviewTests.test_round4_source_order_and_branch_bounds_red_contracts_are_independent",
]
assert summary["failures"] == failed_methods and summary["errors"] == summary["skips"] == []
assert summary["expected_failures"] == summary["unexpected_successes"] == []
stderr = outputs["stderr"].decode()
assert stderr.count('does not match "analysis work units exceed 262144"') == 3
assert all("line " + line in stderr for line in ("4949", "20446", "14551"))
v26_report = {"receipt_sha256": v26_pin, "source_sha256": r["source_sha256"],
              "snapshot": str(snapshot), "files_rehashed": 1766, "tests_run": 53,
              "passed": 50, "failed": failed_methods, "errors": 0,
              "interpretation": "Slot-construction failure fixed. All three remaining failures are work-cap refusal before required depth checks; real adapter fitness still rejected. No matrix/dev/corpus expansion."}

pack_raw = read(C / "class-comprehension-extension-cases-v1.json")
assert h(pack_raw) == "eb5551c054fc89da28fd2e4db433f56f7a3dbbd4cdb70509070a89fe362c74fd"
pack = json.loads(pack_raw)
failed = ["R01-attribute-receiver-unsafe", "R03-indexed-receiver-unsafe", "R05-nested-generator-join-unsafe", "R07-initially-empty-generator-grown-unsafe"]
pins = {"311": "5c56ae9cc8a0c6a46be61e10ca7786505caa8173145878d18df0842ddc62add1",
        "314": "6df879fcdf435dda1ba5a234ab2f41eaf6f0358e028789985c5d68b11e1267e8"}
r8_runs, previous = [], None
for slot, pin in pins.items():
    raw = read(C / ("class-comprehension-extension-v23-red01-" + slot + "-receipt.json"))
    assert h(raw) == pin
    r = json.loads(raw)
    assert r["generator_sha256"] == "53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499"
    assert r["completed"] is True and r["integrity_ok"] is True and r["success"] is False
    assert type(r["exit"]) is int and r["exit"] == r["process_returncode"] == 1
    assert "error" not in r and "cleanup_error" not in r
    assert r["input_hashes_before"] == r["input_hashes_after"]
    for key, digest in r["input_hashes_before"].items():
        assert h(read(Path(r["input_paths"][key]))) == digest
    snapshot, outputs = snapshot_hashes(r)
    manifest_raw = read(snapshot / ".class-comprehension-extension/manifest.json")
    assert h(manifest_raw) == r["manifest_sha256"] == r["manifest_after_sha256"]
    assert json.loads(manifest_raw) == r["before"]
    assert outputs["stderr"] == b"" and outputs["log"] == outputs["stdout"] + b"\nCONTROL STDERR\n"
    assert all(r[key] == value for key, value in json.loads(outputs["setup"]).items())
    rows = [json.loads(line) for line in outputs["stdout"].splitlines()]
    assert len(rows) == 10 and rows == r["retained_partial_records"]
    identity = rows[0]["identity_before_imports"]
    assert identity == r["identity"] and identity["version_info"] == ([3, 11, 15] if slot == "311" else [3, 14, 6])
    assert identity["cwd"] == str(snapshot) and identity["environment"] == r["environment"]
    assert identity["manifest_sha256"] == r["manifest_sha256"]
    assert identity["verified_files"] == len(r["before"]) == (1767 if slot == "311" else 1772)
    cases = rows[1:-1]
    for actual, expected in zip(cases, pack["cases"], strict=True):
        assert actual["class_comprehension_extension_case"] == expected["id"]
        for key in ("classification", "source_sha256", "oracle_sha256", "expected", "required_argv", "unreachable_events"):
            assert actual[key] == expected[key]
        assert h(expected["source"].encode()) == expected["source_sha256"] and h(expected["oracle_source"].encode()) == expected["oracle_sha256"]
        assert actual["oracle_error"] is None and actual["analyzer_error"] is None
        assert actual["oracle_passed"] is True and actual["oracle_actual"] == expected["expected"]
        assert not set(expected["unreachable_events"]) & set(actual["oracle_actual"]["trace"])
        assert actual["blockers"] == [] and actual["argv"] == [["-m", "fixed"]]
        assert actual["semantic_passed"] is (expected["id"] not in failed)
        assert actual["argv"] == [row["argv"] for row in actual["expanded_rows"] if row["capability_kind"] == "subprocess"]
    summary = rows[-1]
    assert summary == r["summary"] and summary["completed"] is True
    assert all(type(summary[k]) is int and summary[k] == 8 for k in ("planned_cases", "case_count", "projections", "analyzed_cases"))
    assert summary["semantic_failures"] == failed and summary["oracle_errors"] == summary["analyzer_errors"] == []
    if previous is not None:
        assert cases == previous
    previous = cases
    r8_runs.append({"slot": slot, "receipt_sha256": pin, "snapshot": str(snapshot),
                   "files_rehashed": len(r["before"]) + 1, "cases": 8, "passed": 4, "wrong_clean_cases": failed})
report = {"schema": "coordinator-v26-r8-verification-v1", "v26": v26_report,
          "r8": r8_runs, "r8_complete_case_records_equal_across_interpreters": True,
          "payload_executed_by_verifier": False,
          "disposition": "Both lanes remain rejected. v26 requires measured cost diagnosis; v25 semantic implementation awaits plan review. Preserve every fixed expectation and all failed predecessors."}
data = (json.dumps(report, indent=2) + "\n").encode()
for name, raw in {"coordinator-v26-r8-verification-v1.json": data,
                  "coordinator-verify-v26-r8-results-v1.py": Path(__file__).read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({"report_sha256": h(data), "files_rehashed": 1766 + sum(r["files_rehashed"] for r in r8_runs),
                  "v26_passed": 50, "v26_total": 53, "r8_wrong_clean_each_slot": 4}))
