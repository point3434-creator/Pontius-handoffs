"""Coordinator verification of already-completed, isolated storage trials."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
WORK = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
LABEL = "storage-prototype-v2-oracle-v2-01"
OUT = ROOT / "coordinator-storage-verification-v1.json"
CONTROL_COPY = ROOT / "coordinator-verify-storage-prototype-v1.py"
PINS = {
    "engineer-storage-prototype-v2.py": "22cc3966435fd4e6e0cecbcbb242275e72d34b36c835b4e960c7c712613822ff",
    "engineer-storage-control-v2.py": "8a1d17448ad7a7298a5fda5a78261c04ad4567996b3f474b8853b915a06b400e",
    "engineer-storage-run-config-v1.json": "07351a2ba5b508c43a5eee009a9be5365b18e1a6d01cb156ce9f55402786d316",
    "tests-checks/storage-oracle-v2.py": "6a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba",
    "tests-checks/storage-oracle-cases-v2.json": "3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f",
}
RECEIPTS = {
    ("311", "0"): "904feb5c199253f0b478e947df23e3d4a50242ecbbbbd0e231ef601ee4c149f1",
    ("311", "1"): "4cb46d012c071c447708be605c363dd25d0f399a6187cf5d3554ea0f65e0de84",
    ("311", "17"): "8d962e9971311a691e71972dd9ca3ebd33db92134866c95c85a3201b51575b98",
    ("314", "0"): "ce7b69ec24a4dd351c2be86ea4a0b08a277fb5cc3ed9e8e2e99a7ae486f09e93",
    ("314", "1"): "d41d2d7f78cb4a7bfdb62bfa4a7a7acebf7ba5001f48bfdfbff643b761852216",
    ("314", "17"): "b2bd3f97361ed58c5a501277ed87db00973983d53cda91e308fe8580e21820a1",
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
assert sys.dont_write_bytecode and not sys.flags.optimize
assert not OUT.exists() and not CONTROL_COPY.exists()
for relative, digest in PINS.items():
    assert sha((ROOT / relative).read_bytes()) == digest, relative
pack = json.loads((ROOT / "tests-checks/storage-oracle-cases-v2.json").read_bytes())
old = json.loads((ROOT / "tests-checks/storage-oracle-cases-v1.json").read_bytes())
assert pack["cases"][:20] == old["cases"]
expected_cases = {case["id"] for case in pack["cases"]}
expected_faults = {(case["id"], offset) for case in pack["cases"]
                   for operation in case["operations"] if operation["op"] == "fault_read"
                   for offset in operation["offsets"]}
assert len(expected_cases) == 28 and len(expected_faults) == 6
results, cross_slot = [], {}
for (slot, seed), digest in RECEIPTS.items():
    receipt_path = ROOT / "engineer-checks" / f"{LABEL}-{slot}-seed{seed}-receipt.json"
    raw = receipt_path.read_bytes()
    assert sha(raw) == digest
    receipt = json.loads(raw)
    assert receipt["exit"] == 0
    assert receipt["base_commit"] == "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
    assert receipt["tracked_file_count"] == 1761
    assert receipt["before"] == receipt["after"]
    assert receipt["prototype_sha256"] == PINS["engineer-storage-prototype-v2.py"]
    assert receipt["control_sha256"] == PINS["engineer-storage-control-v2.py"]
    assert receipt["config_sha256"] == PINS["engineer-storage-run-config-v1.json"]
    assert receipt["oracle"]["sha256"] == PINS["tests-checks/storage-oracle-v2.py"]
    assert receipt["cases"]["sha256"] == PINS["tests-checks/storage-oracle-cases-v2.json"]
    snapshot = Path(receipt["snapshot"])
    for relative, file_digest in receipt["before"].items():
        assert sha((snapshot / relative).read_bytes()) == file_digest, relative
    manifest = (snapshot / ".storage-prototype/manifest.json").read_bytes()
    assert sha(manifest) == receipt["snapshot_manifest_sha256"] == receipt["manifest_after_sha256"]
    identity = receipt["identity_before_payload_imports"]
    expected_version = [3, 11, 15] if slot == "311" else [3, 14, 6]
    assert identity["version_info"] == expected_version and identity["hash_seed"] == seed
    assert identity["environment"]["PYTHONPATH"] == str(snapshot / "src")
    assert identity["environment"]["PONTIUS_GIT"] == r"C:\Program Files\Git\cmd\git.exe"
    assert identity["cwd"] == str(snapshot)
    log_raw = Path(receipt["log"]).read_bytes()
    assert sha(log_raw) == receipt["log_sha256"]
    assert receipt["stderr_sha256"] == sha(b"")
    assert sha(log_raw) == receipt["stdout_sha256"]
    records = [json.loads(line) for line in log_raw.splitlines()]
    assert records[0]["identity_before_payload_imports"] == identity
    cases = [record["storage_oracle_case"] for record in records if "storage_oracle_case" in record]
    assert len(cases) == 34
    assert {(case["case"], case["phase"]) for case in cases} == (
        {(case, "baseline") for case in expected_cases} | expected_faults)
    assert not any("storage_oracle_failure" in record for record in records)
    summary = records[-1]["storage_summary"]
    assert summary == receipt["summary"]
    assert summary["all_completed"] and summary["failures"] == []
    assert summary["completed_runs"] == summary["planned_runs"] == 34
    for case in cases:
        assert sum(case["phase_units"].values()) == case["meter_used"] <= 262144
        assert sum(case["meter_counts"].values()) == case["meter_used"]
        if case["phase"] != "baseline":
            fault = case["fault"]
            assert fault["retry_cost"] == fault["clean_first_read_cost"]
            assert fault["retry_counts"] == fault["clean_first_read_counts"]
            assert fault["used_after_failure"] > fault["configured_limit"]
            assert fault["validation_reads_excluded_from_equivalence"]
    # Same seed gets independently recomputed builtin set order in each slot.
    comparable = [{key: case[key] for key in ("case", "phase", "observations", "callbacks",
                   "retained_versions", "fault", "meter_used", "meter_counts", "phase_units")}
                  for case in cases]
    if slot == "311":
        cross_slot[seed] = comparable
    else:
        assert comparable == cross_slot[seed]
    grid = [{"case": case["case"], "parameters": case["parameters"],
             "phase_units": case["phase_units"], "total": case["meter_used"]}
            for case in cases if case["family"] == "cost-grid"]
    assert len(grid) == 8
    results.append({"slot": slot, "seed": seed, "receipt_sha256": digest,
                    "log_sha256": sha(log_raw), "cases": len(cases), "grid": grid,
                    "snapshot_rehashed_files": len(receipt["before"]),
                    "manifest_sha256": sha(manifest)})
preserved = {
    WORK / "tools/generate_test_inventory.py": "3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1",
    WORK / "tests/test_inventory_and_profiles.py": "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd",
    Path(r"D:\Pontius\CLAUDE.md"): "af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76",
    Path(r"D:\Pontius\docs\workflow.md"): "d9de38ede87fb619b3045a60ee7fab137ae23ba3b580c0a6d6b3ca14e567a170",
}
for path, digest in preserved.items():
    assert sha(path.read_bytes()) == digest, path
control_raw = Path(__file__).read_bytes()
report = {
    "schema": "coordinator-storage-prototype-verification-v1",
    "results": results, "completed_checks": sum(result["cases"] for result in results),
    "input_pins": PINS, "all_twenty_predecessor_cases_preserved": True,
    "matching_seed_cross_interpreter_records_equal": True,
    "preserved_source_and_controller_files": {str(path): digest for path, digest in preserved.items()},
    "verification_control_sha256": sha(control_raw),
    "limits": ["Pure storage compatibility only; no production transfer or cells executed.",
               "Includes construction, terminal order, repeated order, validation and retained-version audit costs.",
               "No ordinary-corpus or production-performance claim.",
               "Storage oracle plan v2 note was finalized after execution; case/oracle/control bytes were pinned before all six runs."],
}
with CONTROL_COPY.open("xb") as stream:
    stream.write(control_raw)
encoded = (json.dumps(report, indent=2) + "\n").encode()
with OUT.open("xb") as stream:
    stream.write(encoded)
print(json.dumps({"output": str(OUT), "sha256": sha(encoded), "checks": report["completed_checks"],
                  "cross_slot_equal": True, "source_preserved": True}, indent=2))
