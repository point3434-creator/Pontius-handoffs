"""Rehash completed immutable evidence; never imports candidate or payload."""
import collections
import hashlib
import json
from pathlib import Path
import stat
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode
slot, receipt_sha = sys.argv[1:]
assert slot in ("311", "314")
report_path = T / ("coordinator-v28-primitive-" + slot + "-verification-v1.json")
assert not report_path.exists()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def raw(path):
    path = Path(path)
    assert path.is_absolute() and ".." not in path.parts
    for part in (path, *path.parents):
        info = part.lstat()
        assert not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert stat.S_ISREG(path.stat().st_mode)
    return path.read_bytes()

def checked(path, wanted):
    value = raw(path)
    assert sha(value) == wanted, str(path)
    return value

def verify(selected, wanted):
    path = C / ("v28-primitive-first01-" + selected + "-seed0-receipt.json")
    receipt = json.loads(checked(path, wanted))
    r = receipt
    assert r["schema"] == "v28-production-primitive-control-v1"
    assert r["slot"] == selected and r["seed"] == "0" and r["label"] == "first01"
    assert all(r[key] is True for key in ("success", "integrity_ok", "result_ok", "payload_started"))
    assert all(type(r[key]) is int and r[key] == 0 for key in ("exit", "process_returncode"))
    assert not r.get("error") and not r.get("cleanup_error") and not r.get("timeout")
    assert all(r[key] == [] for key in ("after_file_errors", "after_original_errors", "integrity_errors"))
    assert r["head_before"] == r["head_after"] == r["base_commit"] == "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
    assert r["control_sha256"] == "64fcb3ef0aaaf57f63643b3e306fe0f0b65f47c4d5ba8c5fc107dbe68186fcac"
    assert r["config_sha256"] == "0f11763dd21c681e401282aa1a4a2cd1c4568c8686fbbc3589b9e0887a2f7050"
    assert r["candidate_sha256"] == "4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e"
    count = 1782 if selected == "311" else 1787
    assert r["before"] == r["after"] and len(r["before"]) == count
    assert r["tracked_file_count"] == 1761
    snapshot = Path(r["snapshot"])
    assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots"))
    manifest = checked(Path(r["payload_directory"]) / "manifest.json", r["manifest_sha256"])
    assert json.loads(manifest) == r["before"] and r["manifest_after_sha256"] == sha(manifest)
    for relative, digest in r["before"].items():
        assert not Path(relative).is_absolute() and ".." not in Path(relative).parts
        checked(snapshot / relative, digest)
    expected_dirty = {"?? " + relative for relative in r["before"] if relative.startswith(".storage-v28-primitive/")}
    expected_dirty.add("?? .storage-v28-primitive/manifest.json")
    assert set(r["dirty_after"].splitlines()) == expected_dirty
    assert r["input_hashes_before"] == r["input_hashes_after"]
    for key, path in r["input_paths"].items():
        checked(path, r["input_hashes_before"][key])
    outputs = {key: checked(entry["path"], entry["sha256"]) for key, entry in r["outputs"].items()}
    assert not outputs["stderr"]
    setup = json.loads(outputs["setup"])
    assert all(key in r and r[key] == value for key, value in setup.items())
    records = [json.loads(line) for line in outputs["stdout"].splitlines()]
    control_records = [record["v28_primitive_control"] for record in records if "v28_primitive_control" in record]
    assert control_records == r["retained_control_records"]
    assert [v["kind"] for v in control_records] == ["identity_before_payload_imports", "static_extraction_verified", "phase_result", "phase_result", "phase_result", "completed"]
    identity = control_records[0]
    patch = [3, 11, 15] if selected == "311" else [3, 14, 6]
    executable = r"D:\Pontius-tools\py311\Scripts\python.exe" if selected == "311" else r"D:\Pontius\.venv\Scripts\python.exe"
    assert identity["version_info"] == patch and identity["executable"] == executable
    assert identity["cwd"] == str(snapshot) and identity["implementation"] == "cpython"
    assert identity["environment"] == r["environment"] and identity["hash_seed"] == "0"
    assert identity["manifest_sha256"] == sha(manifest) and identity["verified_files"] == count
    assert identity["pontius_imported"] is False
    assert all(flag in identity["flags"] for flag in ("dont_write_bytecode=1", "safe_path=True", "no_site=1"))
    assert control_records[1]["production_nodes_verified"] == 47
    assert control_records[1]["static_only"] is True
    assert control_records[1]["extracted_sha256"] == r["config"]["prototype"]["sha256"]
    assert control_records[-1] == {"kind": "completed", "ok": True}
    case_groups = {}
    for phase, key, cases, runs in (("storage", "storage_oracle_case", 28, 34), ("cursor", "cursor_oracle_case", 16, 28), ("indexed", "indexed_storage_case", 16, 31)):
        case_groups[phase] = [record[key] for record in records if key in record]
        assert len(case_groups[phase]) == runs
        entry = next(item for item in control_records if item.get("phase") == phase)
        summary = entry["summary"]
        assert summary["planned_cases"] == cases and summary["planned_runs"] == summary["completed_runs"] == runs
        assert summary["all_completed"] is True and summary["failures"] == []
        assert summary["runtime"] == patch and summary["hash_seed"] == "0"
        assert type(summary["maximum_meter_limit"]) is int and summary["maximum_meter_limit"] == 262144
        if phase == "indexed":
            assert summary["accounting_complete"] is True and summary["fitness_passed"] is True
            assert len(summary["growth_comparisons"]) == 14 and summary["fitness_failures"] == []
            assert all(item["passed"] is True for item in summary["growth_comparisons"])
    accounting = json.loads(raw(T / r["config"]["accounting"]["path"]))
    old = json.loads(raw(T / r["config"]["old_accounting"]["path"]))
    new = sorted(set(accounting["categories"]) - set(old["categories"]))
    assert len(new) == 16
    category_witnesses = {name: [] for name in new}
    for phase, cases in case_groups.items():
        for case in cases:
            for name in new:
                units = case["meter_counts"].get(name, 0)
                assert type(units) is int and units >= 0
                if units:
                    category_witnesses[name].append({"phase": phase, "case": case["case"], "run_phase": case["phase"], "reported_units": units})
    return r, case_groups, category_witnesses

r, groups, witnesses = verify(slot, receipt_sha)
equal = None
if slot == "314":
    floor, floor_groups, _ = verify("311", "8c2dcb38a6fb00a977b10f7ef3e354066d093fd76d5f920ed3f50d68ba82f3f7")
    assert groups == floor_groups
    equal = True
report = {"schema": "coordinator-v28-primitive-verification-v1", "slot": slot, "seed": "0", "receipt_sha256": receipt_sha,
          "rehash_files": len(r["before"]), "runs_passed": sum(len(v) for v in groups.values()),
          "all_raw_records_and_input_output_hashes_checked": True,
          "same_seed_complete_case_records_equal_to_floor": equal,
          "new_category_witnesses": witnesses, "unexercised_new_categories": [name for name, rows in witnesses.items() if not rows],
          "limits": ["Finite primitive evidence only; no production-budget adapter, constructor B, resolver, corpus or integration claim.",
                     "Positive category counts establish exercised operations, not exhaustive branch or behavior coverage."]}
copy = T / "coordinator-verify-v28-primitive-v1.py"
self_raw = Path(__file__).read_bytes()
if copy.exists():
    assert copy.read_bytes() == self_raw
else:
    with copy.open("xb") as stream:
        stream.write(self_raw)
report_raw = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
with report_path.open("xb") as stream:
    stream.write(report_raw)
print(json.dumps({"report": str(report_path), "sha256": sha(report_raw), "files": len(r["before"]), "runs": report["runs_passed"], "new_categories_exercised": sum(bool(v) for v in witnesses.values()), "unexercised": report["unexercised_new_categories"], "same_seed_records_equal": equal}))
