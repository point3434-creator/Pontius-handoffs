"""Independently rehash completed indexed trials; do not import any payload."""
from pathlib import Path
import hashlib
import json
import re
import stat
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
CONFIG_SHA = "60485a4ea41ab146e89c4da4fb0bfd8cfad98c0908322025e62512dfd1ce97aa"
BASE = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
h = lambda raw: hashlib.sha256(raw).hexdigest()

def read(path):
    assert path.is_absolute() and ".." not in path.parts
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        assert not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path.read_bytes()

def main():
    assert sys.version_info[:3] == (3, 11, 15)
    assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
    assert sys.dont_write_bytecode and not sys.flags.optimize
    assert len(sys.argv) >= 4 and len(sys.argv) % 2 == 0
    label = sys.argv[1]
    assert re.fullmatch("[a-z0-9-]+", label)
    raw = read(T / "engineer-indexed-storage-config-v1.json")
    assert h(raw) == CONFIG_SHA
    config = json.loads(raw)
    for entry in config.values():
        if type(entry) is dict and set(entry) == {"path", "sha256"}:
            assert h(read(T / entry["path"])) == entry["sha256"]
    packs = {key: json.loads(read(T / config[key]["path"]))
             for key in ("old_cases", "cursor_cases", "indexed_cases")}
    expected_old = {(c["id"], "baseline") for c in packs["old_cases"]["cases"]}
    expected_old |= {(c["id"], offset) for c in packs["old_cases"]["cases"]
                     for op in c["operations"] if op["op"] == "fault_read" for offset in op["offsets"]}
    expected_cursor = {(c["id"], "baseline") for c in packs["cursor_cases"]["cases"]}
    expected_cursor |= {(c["id"], offset) for c in packs["cursor_cases"]["cases"]
                        if c["kind"] == "atomic" for offset in c["offsets"]}
    expected_indexed = {(c["id"], "baseline") for c in packs["indexed_cases"]["cases"]}
    expected_indexed |= {(c["id"], offset) for c in packs["indexed_cases"]["cases"]
                         if c["family"] == "atomic" for offset in packs["indexed_cases"]["fault_offsets"]}
    assert [len(x) for x in (expected_old, expected_cursor, expected_indexed)] == [34, 28, 31]
    accounting = json.loads(read(T / config["accounting"]["path"]))["categories"]
    runs, comparable, snapshots = [], {}, set()
    for relative, pin in zip(sys.argv[2::2], sys.argv[3::2], strict=True):
        match = re.fullmatch(r"engineer-checks/indexed-radix-v1-first01-(311|314)-seed(0|1|17)-receipt.json", relative)
        assert match and re.fullmatch("[a-f0-9]{64}", pin)
        slot, seed = match.groups()
        receipt_raw = read(T / relative)
        assert h(receipt_raw) == pin
        r = json.loads(receipt_raw)
        assert r["success"] is True and r["integrity_ok"] is True and r["result_ok"] is True
        assert type(r["exit"]) is int and r["exit"] == 0
        assert r["config_sha256"] == CONFIG_SHA and r["config"] == config
        assert r["before"] == r["after"] and r["input_hashes_before"] == r["input_hashes_after"]
        assert r["head_before"] == r["head_after"] == BASE
        snapshot = Path(r["snapshot"])
        assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots")) and snapshot not in snapshots
        snapshots.add(snapshot)
        assert read(snapshot / ".git/HEAD").decode().strip() == BASE
        assert r["tracked_file_count"] == 1761
        for name, digest in r["before"].items():
            rel = Path(name)
            assert not rel.is_absolute() and not rel.drive and ".." not in rel.parts
            assert h(read(snapshot / rel)) == digest, name
        manifest_raw = read(snapshot / ".storage-indexed-prototype/manifest.json")
        assert h(manifest_raw) == r["manifest_sha256"] == r["manifest_after_sha256"]
        assert json.loads(manifest_raw) == r["before"]
        for key, digest in r["input_hashes_before"].items():
            assert h(read(Path(r["input_paths"][key]))) == digest, key
        outputs = {key: read(Path(item["path"])) for key, item in r["outputs"].items()}
        assert all(h(outputs[key]) == item["sha256"] for key, item in r["outputs"].items())
        setup = json.loads(outputs["setup"])
        assert all(r[key] == value for key, value in setup.items())
        assert outputs["stderr"] == b""
        assert outputs["log"] == outputs["stdout"] + b"\nCONTROL STDERR\n"
        records = [json.loads(line) for line in outputs["stdout"].splitlines()]
        control = [x["indexed_control"] for x in records if "indexed_control" in x]
        assert control == r["retained_control_records"]
        assert [x["kind"] for x in control] == ["identity_before_payload_imports", *(["phase_result"] * 3), "completed"]
        assert control[-1]["ok"] is True and r["completed_records"] == [control[-1]]
        identity = control[0]
        assert r["identity_records"] == [identity] and r["phase_results"] == control[1:4]
        assert identity["version_info"] == ([3, 11, 15] if slot == "311" else [3, 14, 6])
        assert identity["executable"] == (r"D:\Pontius-tools\py311\Scripts\python.exe" if slot == "311" else r"D:\Pontius\.venv\Scripts\python.exe")
        assert identity["hash_seed"] == seed and identity["pontius_imported"] is False
        assert identity["verified_files"] == len(r["before"]) == (1774 if slot == "311" else 1779)
        assert identity["cwd"] == str(snapshot) and identity["environment"] == r["environment"]
        assert identity["manifest_sha256"] == r["manifest_sha256"]
        assert identity["prototype_sha256"] == config["prototype"]["sha256"]
        assert identity["accounting_sha256"] == config["accounting"]["sha256"]
        groups = [[x[key] for x in records if key in x] for key in
                  ("storage_oracle_case", "cursor_oracle_case", "indexed_storage_case")]
        assert not any(set(x) & {"storage_oracle_failure", "cursor_oracle_failure", "indexed_storage_failure"}
                       for x in records)
        for phase, cases, expected, count in zip(control[1:4], groups,
                (expected_old, expected_cursor, expected_indexed), (34, 28, 31), strict=True):
            assert len(cases) == count and {(x["case"], x["phase"]) for x in cases} == expected
            summary = phase["summary"]
            assert phase["ok"] is True and summary["all_completed"] is True and summary["failures"] == []
            assert summary["completed_runs"] == summary["planned_runs"] == count
            for case in cases:
                assert sum(case["meter_counts"].values()) == case["meter_used"] <= 262144
                assert sum(event["units"] for event in case["cost_events"]) == case["meter_used"]
        indexed = groups[-1]
        baselines = {x["case"]: x for x in indexed if x["phase"] == "baseline"}
        for case in indexed:
            assert case["accounting_complete"] is True
            for event in case["cost_events"]:
                assert set(event["counts"]) <= set(accounting)
                assert sum(event["counts"].values()) == event["units"]
                assert sum(n for k, n in event["counts"].items() if accounting[k]["metric"] == "P") == event["physical_events"]
            if case["phase"] != "baseline":
                b, fault = baselines[case["case"]], case["fault"]
                assert fault["used_after_failure"] > fault["configured_limit"] >= fault["used_before"]
                assert fault["retry_units"] == b["calibration"]["units"]
                assert fault["retry_counts"] == b["calibration"]["counts"]
                assert case["continuation_costs"] == b["continuation_costs"]
                assert case["continuation_observations"] == b["continuation_observations"]
        release = baselines["I11-published-owner-release"]
        assert release["positive_old_owner"] is True
        assert release["successful_changed_publications"] == 1
        assert release["obsolete_values_released"] == {"victim-overwrite": True, "victim-delete": True}
        collision = baselines["I07-collisions-64"]["collision_evidence"]
        assert collision["terminal_collision_required"] is True and collision["terminal_collision_exercised"] is True
        assert collision["terminal_collision_units"] > 0 and collision["equality_calls"] > 0
        summary = control[3]["summary"]
        assert summary["accounting_complete"] is True and summary["fitness_passed"] is True
        comparisons = summary["growth_comparisons"]
        assert len(comparisons) == 14 and summary["fitness_failures"] == []
        for row in comparisons:
            key = "units" if row["metric"] == "units" else "physical_events"
            small, large = (sum(baselines[row[name]]["phase_costs"].get(p, {}).get(key, 0)
                                for p in row["phases"]) for name in ("smaller_case", "larger_case"))
            small_case = next(c for c in packs["indexed_cases"]["cases"] if c["id"] == row["smaller_case"])
            denominator = max(small, 1 if key == "units" else small_case["n"])
            factor = 6 if row["family"] == "bulk-build-plus-order" else 8
            assert row["smaller"] == small and row["larger"] == large
            assert row["maximum_larger"] == factor * denominator and large <= factor * denominator
            assert row["complete"] is True and row["passed"] is True
        equal = None
        if slot == "311":
            comparable[seed] = groups
        elif seed in comparable:
            equal = comparable[seed] == groups
        runs.append({"slot": slot, "seed": seed, "receipt_sha256": pin, "snapshot": str(snapshot),
                     "manifest_sha256": h(manifest_raw), "rehashed_files": len(r["before"]) + 1,
                     "runs": 93, "same_seed_cross_slot_records_equal": equal,
                     "indexed_case_units": {x["case"]: x["meter_used"] for x in indexed if x["phase"] == "baseline"},
                     "growth_comparisons": comparisons, "collision": collision})
    for relative, digest in json.loads(read(T / "coordinator-preservation-baseline-v2.json"))["paths"].items():
        if relative not in {"tools/generate_test_inventory.py", "tests/test_inventory_and_profiles.py"}:
            assert h(read(W / relative)) == digest
    assert h(read(W / "tools/generate_test_inventory.py")) == "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
    assert h(read(W / "tests/test_inventory_and_profiles.py")) == "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
    report = {"schema": "coordinator-indexed-verification-v1", "config_sha256": CONFIG_SHA,
              "runs": runs, "completed_runs": 93 * len(runs), "preserved_15_paths": True,
              "payload_executed_by_verifier": False,
              "limits": "Pure-store finite tests, not production fitness, wall-time speed or final acceptance."}
    report_raw = (json.dumps(report, indent=2) + "\n").encode()
    for name, data in {
        f"coordinator-indexed-verification-{label}.json": report_raw,
        f"coordinator-verify-indexed-prototype-{label}.py": Path(__file__).read_bytes(),
    }.items():
        with (T / name).open("xb") as stream:
            stream.write(data)
    print(json.dumps({"report_sha256": h(report_raw), "completed_runs": report["completed_runs"],
                      "rehashed_files": sum(run["rehashed_files"] for run in runs)}))

if __name__ == "__main__":
    main()
