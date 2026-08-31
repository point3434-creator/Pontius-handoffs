"""Verify retained six-case RED evidence without running Models or analyzer."""
from pathlib import Path
import hashlib
import json
import stat
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
h = lambda raw: hashlib.sha256(raw).hexdigest()
PINS = {"311": "7f778350c5d338917a1c980455ba27e3fb0418f3ee1a213615e5d5cfd8d7a296",
        "314": "7b56396209611527bbb39ca01f0a3890f5d5817a97e845b509ee8f0933be20b0"}
SOURCE = "61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3"
PACK = "9df895eb5bd645a5e4ef05be0f7c0a3db76df458ca023bbfbd36407ee3496b71"
FAILED = ["Q02-eager-cell-safe", "Q03-class-first-iterable-unsafe", "Q05-deferred-cell-unsafe"]

def read(path):
    assert path.is_absolute() and ".." not in path.parts
    for ancestor in (path, *path.parents):
        assert not getattr(ancestor.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path.read_bytes()

assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
pack_raw = read(C / "class-comprehension-boundary-cases-v1.json")
assert h(pack_raw) == PACK
pack = json.loads(pack_raw)
runs, all_cases = [], []
for slot, pin in PINS.items():
    prefix = "class-comprehension-boundary-v22-red01-" + slot
    raw = read(C / (prefix + "-receipt.json"))
    assert h(raw) == pin
    r = json.loads(raw)
    assert r["completed"] is True and r["integrity_ok"] is True and r["success"] is False
    assert type(r["exit"]) is int and r["exit"] == r["process_returncode"] == 1
    assert "error" not in r and "cleanup_error" not in r
    assert r["generator_sha256"] == SOURCE and r["pack_sha256"] == PACK
    assert r["before"] == r["after"] and r["input_hashes_before"] == r["input_hashes_after"]
    snapshot = Path(r["snapshot"])
    assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots"))
    for name, digest in r["before"].items():
        rel = Path(name)
        assert not rel.is_absolute() and not rel.drive and ".." not in rel.parts
        assert h(read(snapshot / rel)) == digest, name
    manifest = read(snapshot / ".class-comprehension-boundary/manifest.json")
    assert h(manifest) == r["manifest_sha256"] == r["manifest_after_sha256"]
    assert json.loads(manifest) == r["before"]
    assert read(snapshot / ".git/HEAD").decode().strip() == "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
    for key, digest in r["input_hashes_before"].items():
        assert h(read(Path(r["input_paths"][key]))) == digest
    outputs = {key: read(Path(item["path"])) for key, item in r["outputs"].items()}
    assert all(h(outputs[key]) == item["sha256"] for key, item in r["outputs"].items())
    assert outputs["stderr"] == b"" and outputs["log"] == outputs["stdout"] + b"\nCONTROL STDERR\n"
    setup = json.loads(outputs["setup"])
    assert all(r[key] == value for key, value in setup.items())
    records = [json.loads(line) for line in outputs["stdout"].splitlines()]
    assert len(records) == 8 and records == r["retained_partial_records"]
    identity = records[0]["identity_before_imports"]
    assert identity == r["identity"]
    assert identity["version_info"] == ([3, 11, 15] if slot == "311" else [3, 14, 6])
    assert identity["executable"] == (r"D:\Pontius-tools\py311\Scripts\python.exe" if slot == "311" else r"D:\Pontius\.venv\Scripts\python.exe")
    assert identity["cwd"] == str(snapshot) and identity["environment"] == r["environment"]
    assert identity["manifest_sha256"] == r["manifest_sha256"]
    assert identity["verified_files"] == len(r["before"]) == (1767 if slot == "311" else 1772)
    cases = records[1:-1]
    assert [case["class_comprehension_boundary_case"] for case in cases] == [case["id"] for case in pack["cases"]]
    for actual, expected in zip(cases, pack["cases"], strict=True):
        for key in ("classification", "source_sha256", "oracle_sha256", "expected", "required_argv", "unreachable_events"):
            assert actual[key] == expected[key]
        assert h(expected["source"].encode()) == expected["source_sha256"]
        assert h(expected["oracle_source"].encode()) == expected["oracle_sha256"]
        assert actual["oracle_passed"] is True and actual["oracle_actual"] == expected["expected"]
        assert actual["oracle_error"] is None and actual["analyzer_error"] is None
        assert not set(actual["oracle_actual"]["trace"]) & set(expected["unreachable_events"])
        assert actual["semantic_passed"] is (expected["id"] not in FAILED)
        if expected["id"] in FAILED[1:]:
            assert actual["blockers"] == [] and actual["argv"] == [["-m", "fixed"]]
        elif expected["id"] == FAILED[0]:
            assert actual["blockers"] and actual["argv"] == []
    summary = records[-1]
    assert summary == r["summary"] and summary["completed"] is True
    assert summary["analyzed_cases"] == summary["case_count"] == summary["projections"] == 6
    assert summary["semantic_failures"] == FAILED and summary["oracle_errors"] == summary["analyzer_errors"] == []
    all_cases.append(cases)
    runs.append({"slot": slot, "receipt_sha256": pin, "manifest_sha256": h(manifest),
                 "snapshot": str(snapshot), "rehashed_files": len(r["before"]) + 1,
                 "semantic_failures": FAILED, "models_passed": 6, "analyzer_calls_completed": 6})
assert all_cases[0] == all_cases[1]
report = {"schema": "coordinator-class-comprehension-red-verification-v1", "runs": runs,
          "same_case_records_across_interpreters": True, "source_sha256": SOURCE,
          "pack_sha256": PACK, "wrong_clean_cases": FAILED[1:], "wrong_refused_case": FAILED[0],
          "payload_executed_by_verifier": False,
          "disposition": "Existing v22 semantic RED at the already enumerated implicit class-scope boundary; preserve expectations and repair shared mechanism."}
report_raw = (json.dumps(report, indent=2) + "\n").encode()
for name, data in {
    "coordinator-class-comprehension-red-verification-v1.json": report_raw,
    "coordinator-verify-class-comprehension-red-v1.py": Path(__file__).read_bytes(),
}.items():
    with (T / name).open("xb") as stream:
        stream.write(data)
print(json.dumps({"report_sha256": h(report_raw), "rehashed_files": sum(run["rehashed_files"] for run in runs),
                  "failures_each_slot": FAILED, "same_case_records": True}))
