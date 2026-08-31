"""Verify already completed cursor trials, without importing any payload."""
from pathlib import Path
import hashlib
import json
import os
import stat
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
CONFIG_SHA = "afb9d33f3ec5110e822a0a7e44710fbe025940985ecf82ce7ffc533c084ab958"
RECEIPTS = {
    ("311", "0"): "68bb5e2a0c4a3249dd2d0cd1674208af46d3f6c1b58049699e569adaab3cbf28",
    ("311", "1"): "f03d92ad6466c8a20a2fde75956306909686db45ddbce3e2f3260db39fa677f1",
    ("311", "17"): "dbb52820e80ba5973c5ce26fe1b39d058ce414cfd247ca907b5d0219fe873b0c",
    ("314", "0"): "7be6e976d27f5bcf3d0eb25d5a6c59790dd5ef7c4678edd06b594d3a3683db62",
    ("314", "1"): "8464020e0e5f9f0f70b4e21bd7a722cb3999339111f46a892202b8346f04cc60",
    ("314", "17"): "9f3509f6d33397c7fb67fecf06e21877ea114626fbdec43e435c2f20ac078519",
}


def h(raw):
    return hashlib.sha256(raw).hexdigest()


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
    raw = read(T / "engineer-cursor-prototype-v1-config.json")
    assert h(raw) == CONFIG_SHA
    config = json.loads(raw)
    for key in ("prototype", "old_oracle", "old_cases", "cursor_oracle", "cursor_cases"):
        assert h(read(T / config[key]["path"])) == config[key]["sha256"]
    old_pack = json.loads(read(T / config["old_cases"]["path"]))
    new_pack = json.loads(read(T / config["cursor_cases"]["path"]))
    old_expected = {(c["id"], "baseline") for c in old_pack["cases"]}
    old_expected |= {(c["id"], offset) for c in old_pack["cases"]
                     for op in c["operations"] if op["op"] == "fault_read"
                     for offset in op["offsets"]}
    new_expected = {(c["id"], "baseline") for c in new_pack["cases"]}
    new_expected |= {(c["id"], offset) for c in new_pack["cases"] if c["kind"] == "atomic"
                     for offset in c["offsets"]}
    assert len(old_expected) == 34 and len(new_expected) == 28
    slots, comparable = [], {}
    snapshots = set()
    for (slot, seed), pin in RECEIPTS.items():
        path = T / "engineer-checks" / f"cursor-prototype-v1-01-{slot}-seed{seed}-receipt.json"
        receipt_raw = read(path)
        assert h(receipt_raw) == pin
        r = json.loads(receipt_raw)
        assert r["success"] is True and r["integrity_ok"] is True and r["exit"] == 0
        assert r["config_sha256"] == CONFIG_SHA
        assert r["before"] == r["after"] and r["input_hashes_before"] == r["input_hashes_after"]
        assert r["head_before"] == r["head_after"] == "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
        assert r["tracked_file_count"] == 1761
        snapshot = Path(r["snapshot"])
        assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots")) and snapshot not in snapshots
        snapshots.add(snapshot)
        for name, expected in r["before"].items():
            relative = Path(name)
            assert not relative.is_absolute() and not relative.drive and ".." not in relative.parts
            assert h(read(snapshot / relative)) == expected, name
        for key, expected in r["input_hashes_before"].items():
            assert h(read(Path(r["input_paths"][key]))) == expected, key
        manifest_raw = read(snapshot / ".storage-cursor-prototype/manifest.json")
        assert h(manifest_raw) == r["manifest_sha256"] == r["manifest_after_sha256"]
        assert json.loads(manifest_raw) == r["before"]
        identity, = r["identity_records"]
        assert identity["version_info"] == ([3, 11, 15] if slot == "311" else [3, 14, 6])
        assert identity["hash_seed"] == seed and identity["pontius_imported"] is False
        assert identity["verified_files"] == len(r["before"]) == (1770 if slot == "311" else 1771)
        assert identity["cwd"] == str(snapshot)
        assert identity["environment"]["PYTHONPATH"] == str(snapshot / "src")
        assert identity["environment"]["PONTIUS_GIT"] == r"C:\Program Files\Git\cmd\git.exe"
        stdout = read(Path(r["stdout"]))
        assert h(stdout) == r["stdout_sha256"]
        assert read(Path(r["stderr"])) == b"" and r["stderr_sha256"] == h(b"")
        assert h(read(Path(r["log"]))) == r["log_sha256"]
        records = [json.loads(line) for line in stdout.splitlines()]
        assert not any("storage_oracle_failure" in x or "cursor_oracle_failure" in x for x in records)
        old = [x["storage_oracle_case"] for x in records if "storage_oracle_case" in x]
        new = [x["cursor_oracle_case"] for x in records if "cursor_oracle_case" in x]
        assert len(old) == 34 and {(x["case"], x["phase"]) for x in old} == old_expected
        assert len(new) == 28 and {(x["case"], x["phase"]) for x in new} == new_expected
        for phase, count in zip(r["phase_results"], (34, 28), strict=True):
            summary = phase["summary"]
            assert phase["ok"] is True and summary["all_completed"] is True and summary["failures"] == []
            assert summary["completed_runs"] == summary["planned_runs"] == count
            assert summary["maximum_meter_limit"] == 262144
        for case in old + new:
            assert sum(case["phase_units"].values()) == case["meter_used"] <= 262144
            assert sum(case["meter_counts"].values()) == case["meter_used"]
            assert sum(e["units"] for e in case["cost_events"]) == case["meter_used"]
        baselines = {x["case"]: x for x in new if x["phase"] == "baseline"}
        for case in new:
            if case["phase"] == "baseline":
                continue
            b = baselines[case["case"]]
            fault = case["fault"]
            assert fault["used_after_failure"] > fault["configured_limit"]
            assert fault["retry_units"] == b["calibration"]["units"]
            assert fault["retry_counts"] == b["calibration"]["counts"]
            assert case["after_target_costs"] == b["after_target_costs"]
            assert case["continuation_observations"] == b["continuation_observations"]
        if slot == "311":
            comparable[seed] = (old, new)
        else:
            assert (old, new) == comparable[seed], "same-seed public records differ"
        slots.append({
            "slot": slot, "seed": seed, "receipt_sha256": pin, "log_sha256": r["log_sha256"],
            "snapshot": str(snapshot), "rehashed_files": len(r["before"]),
            "manifest_sha256": h(manifest_raw), "old_runs": len(old), "cursor_runs": len(new),
            "maximum_case_units": max(x["meter_used"] for x in old + new),
        })
    preserved = {
        W / "tools/generate_test_inventory.py": "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679",
        W / "tests/test_inventory_and_profiles.py": "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd",
        Path(r"D:\Pontius\CLAUDE.md"): "af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76",
        Path(r"D:\Pontius\docs\workflow.md"): "d9de38ede87fb619b3045a60ee7fab137ae23ba3b580c0a6d6b3ca14e567a170",
    }
    for path, pin in preserved.items():
        assert h(read(path)) == pin, str(path)
    report = {
        "schema": "coordinator-cursor-prototype-verification-v1",
        "config_sha256": CONFIG_SHA, "slots": slots, "completed_runs": 372,
        "old_runs": 204, "cursor_runs": 168, "same_seed_cross_slot_records_equal": True,
        "operation_retry_and_continuation_equal_to_pristine": True,
        "preserved": {str(p): pin for p, pin in preserved.items()},
        "limits": ["Pure storage experiment, not production fit or authority-transfer verification.",
                   "No production write lease, cold approval, integration or commit is implied.",
                   "Meter units compare charged operations, not runtime or physical work."],
    }
    output = {
        "coordinator-cursor-verification-v1.json": (json.dumps(report, indent=2) + "\n").encode(),
        "coordinator-verify-cursor-prototype-v1.py": Path(__file__).read_bytes(),
    }
    assert not any((T / name).exists() for name in output)
    for name, raw in output.items():
        with (T / name).open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    print(json.dumps({name: h(raw) for name, raw in output.items()}, indent=2))


if __name__ == "__main__":
    main()
