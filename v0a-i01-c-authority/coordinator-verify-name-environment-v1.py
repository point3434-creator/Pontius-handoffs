"""Independently check structural-family receipts; no repository code executes."""
from pathlib import Path
import hashlib
import json
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
sha = lambda raw: hashlib.sha256(raw).hexdigest()
assert sys.version_info[:3] == (3, 11, 15)
assert Path(sys.executable).resolve() == Path(r"D:\Pontius-tools\py311\Scripts\python.exe").resolve()
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
slots = {
    "311": ((3, 11, 15), r"D:\Pontius-tools\py311\Scripts\python.exe", "7e72792ac56de1ca4d3db7f544803f08bcf0ed3e636e538beadd35350c22802a"),
    "314": ((3, 14, 6), r"D:\Pontius\.venv\Scripts\python.exe", "1976c3156a0c38edb47e696cd344638903141a8265d6cf197ec80895b1de0e0b"),
}
case_pack = (C / "name-environment-cases-v1.json").read_bytes()
assert sha(case_pack) == "d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c"
cases = {item["id"]: item for item in json.loads(case_pack)["cases"]}
all_results = {}
proof = []
for slot, (version, executable, pin) in slots.items():
    receipt_path = C / f"red-name-env-v19-{slot}-{slot}-receipt.json"
    raw = receipt_path.read_bytes()
    assert sha(raw) == pin
    r = json.loads(raw)
    assert r["exit"] == 1 and r["slot"] == slot
    assert r["identity"]["version_info"] == list(version)
    assert Path(r["identity"]["executable"]).resolve() == Path(executable).resolve()
    assert r["generator_sha256"] == "3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1"
    assert r["tests_sha256"] == "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
    assert r["all_tracked_paths_unchanged"] == 1761
    assert sha((C / "name-environment-control-v1.py").read_bytes()) == r["control_sha256"]
    assert sha((C / "name-environment-probe-v1.py").read_bytes()) == r["probe_sha256"]
    log = Path(r["log"]).read_bytes()
    assert sha(log) == r["log_sha256"]
    records = [json.loads(line) for line in log.splitlines() if line.startswith(b"{")]
    summary, = [item for item in records if "name_environment_summary" in item]
    assert summary["exit_reason"] == "structural-repeated-work"
    assert not any(summary[name] for name in ("oracle_errors", "semantic_errors", "analysis_errors"))
    assert summary["exercised"] == 24 and summary["exercised_projections"] == 58
    results = {item["name_environment_case"]: item for item in records if "name_environment_case" in item}
    assert set(results) == set(cases)
    for name, item in results.items():
        case = cases[name]
        assert item["semantic_passed"] and not item["oracle_errors"]
        assert item["witnesses"] == case["witnesses"]
        assert item["source_sha256"] == sha(case["source"].encode())
        assert item["oracle_sha256"] == sha(case["oracle_source"].encode())
    zero_change_pairs = [item for item in summary["structural_pairs"] if item["changed"] == 0]
    assert len(zero_change_pairs) == 4
    assert all(item["structural_repeated_work"] and item["semantic_controls_passed"] for item in zero_change_pairs)
    all_results[slot] = results
    proof.append({"slot": slot, "receipt_sha256": pin, "log_sha256": sha(log),
                  "semantic_cases": 24, "oracle_projections": 58, "structural_red_pairs": 4})
counter_names = (
    "physical_name_copy_calls", "physical_name_copy_entries", "physical_ambient_copy_entries",
    "projected_merge_normalizations", "projected_merge_operands", "ambient_merge_normalizations",
    "ambient_merge_operands", "charged_unit_sum_across_budgets", "consume_calls",
    "largest_individual_budget_work")
for name in cases:
    for key in counter_names:
        assert all_results["311"][name]["metrics"][key] == all_results["314"][name]["metrics"][key], (name, key)
report = {"standing": "Evidence verification only; structural RED, not corpus or cold approval.",
          "verified_slots": proof, "cross_slot_counter_fields_identical": list(counter_names),
          "case_pack_sha256": sha(case_pack), "control_sha256": sha(Path(__file__).read_bytes())}
out = T / "coordinator-name-environment-verification-v1.json"
with out.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2)
    stream.write("\n")
print(json.dumps({"receipt": str(out), "sha256": sha(out.read_bytes()), "cases_per_slot": 24}))
