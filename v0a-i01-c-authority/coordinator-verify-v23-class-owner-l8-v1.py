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

pack_raw = read(C / "class-owner-late-store-cases-v1.json")
assert h(pack_raw) == "08fce0e37eaeb24192c4f227677d7625097748ccb2cbc79470df4699718a9b47"
pack = json.loads(pack_raw)
failed = ["L01-local-direct-unsafe", "L03-local-contained-unsafe", "L05-local-captured-unsafe", "L07-module-class-unsafe"]
pins = {"311": "147beb79bd5182a92fe32a21e32d3b3e80b3e95ca7440cd887645bedf8b5c5e3",
        "314": "b1ebed05ad93a5bd0dbd2b444034d6cd5e3b8717e36de052a95d2e3c460f6a5a"}
l8_runs, previous = [], None
for slot, pin in pins.items():
    raw = read(C / ("class-owner-late-store-v23-red01-" + slot + "-receipt.json"))
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
    manifest_raw = read(snapshot / ".class-owner-late-store/manifest.json")
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
        assert actual["class_owner_late_store_case"] == expected["id"]
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
    l8_runs.append({"slot": slot, "receipt_sha256": pin, "snapshot": str(snapshot),
                   "files_rehashed": len(r["before"]) + 1, "cases": 8, "passed": 4, "wrong_clean_cases": failed})
report = {"schema": "coordinator-v23-class-owner-l8-verification-v1", "runs": l8_runs,
          "complete_case_records_equal_across_interpreters": True,
          "payload_executed_by_verifier": False,
          "interpretation": "All four unsafe late-member alias cases silently authorize the fixed sink on v23; all four clean controls pass. Models and analyzers complete without errors, with original caps. This is new observed RED supporting the already drafted class-owner repair; not an implementation verdict.",
          "disposition": "Retain both frozen runs. Existing44 expectations stay fixed. No integration or broader payload authorized by this evidence reader."}
data = (json.dumps(report, indent=2) + "\n").encode()
for name, raw in {"coordinator-v23-class-owner-l8-verification-v1.json": data,
                  "coordinator-verify-v23-class-owner-l8-v1.py": Path(__file__).read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({"report_sha256": h(data), "files_rehashed": sum(r["files_rehashed"] for r in l8_runs),
                  "wrong_clean_each_slot": 4, "clean_passed_each_slot": 4, "oracle_or_analyzer_errors": 0}))
