"""Independent byte/receipt audit only; imports no Pontius code or test payload."""
import ast
import hashlib
import json
from pathlib import Path
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
SOURCE = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
TESTS = "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
OUT = T / "coordinator-v20-diagnostics-verification-v3.json"
COPY = T / "coordinator-verify-authority-v20-diagnostics-v3.py"
pins = {
    "engineer-checks/release20-design-311-receipt.json": "fbecc06b5f59318468d225cfae4f43fa2b6f8ebf92554e841b6b6da50c75a2e6",
    "engineer-checks/release20-design-311-setup.json": "16e4e127a86eec6c8ad776f9cfe96be641c8a840bcbd08eff5bb42025424b375",
    "engineer-checks/release20-design-311.txt": "a29a12d166f10ac3ef9e0b99c46df654159f0af1b242ad7963b7d5e5743b5713",
    "engineer-checks/chain32-v20-diagnosis01-311-receipt.json": "03c82035d15ed8218e8a0ac9907eb189738402215e4bd4e93a72de6d81c14a47",
    "engineer-checks/chain32-v20-diagnosis01-311.txt": "f4f2a44d96667f8d2b13ccf4de816b1f18541e737381d010763c33762d5d876a",
    "tests-checks/snapshot-name-environment-v20-01.json": "69776f3ddd31d2d6c2ad49dcfc11f3bef190537aaa219dcbe4a7f8412dc7681b",
    "tests-checks/red-name-environment-v20-01-311-receipt.json": "073271c7de10694fa72d938c9babee4a21dacaa764eacac9241f623d8f80e2b1",
    "tests-checks/red-name-environment-v20-01-311.txt": "43d76a321846089bfc6b8ff5cb9b7f4ad97c2c9f019470287cab27ed1c882a81",
    "tests-checks/red-name-env-v19-311-311-receipt.json": "7e72792ac56de1ca4d3db7f544803f08bcf0ed3e636e538beadd35350c22802a",
    "tests-checks/name-environment-probe-v20-v1.py": "a45f9818129daabeed96ef5e8cfb1844df6a50bf128a17af9b654bb730c15691",
    "tests-checks/name-environment-cases-v1.json": "d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c",
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(relative):
    return json.loads((T / relative).read_bytes())


def verify_map(root, expected):
    actual = {name: sha((root / name).read_bytes()) for name in expected}
    assert actual == expected, [name for name in expected if actual[name] != expected[name]]
    return len(actual)


def records(log):
    return [json.loads(line) for line in log.read_bytes().splitlines()
            if line.startswith(b"{")]


assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
assert sys.dont_write_bytecode and not sys.flags.optimize
assert not OUT.exists() and not COPY.exists()
for relative, expected in pins.items():
    assert sha((T / relative).read_bytes()) == expected, relative
assert sha((W / "tools/generate_test_inventory.py").read_bytes()) == SOURCE
assert sha((T / "engineer-generator-v20.py").read_bytes()) == SOURCE
assert sha((W / "tests/test_inventory_and_profiles.py").read_bytes()) == TESTS

design = read("engineer-checks/release20-design-311-receipt.json")
assert design["exit"] == 1 and design["before"] == design["after"]
assert design["generator_overlay_sha256"] == SOURCE
design_count = verify_map(Path(design["snapshot"]), design["after"])
design_text = (T / "engineer-checks/release20-design-311.txt").read_text()
assert "Ran 53 tests" in design_text and "FAILED (failures=2, errors=1)" in design_text
assert design["identity_before_imports"]["identity_before_imports"]["version_info"] == [3, 11, 15]

diagnostic = read("engineer-checks/chain32-v20-diagnosis01-311-receipt.json")
assert diagnostic["exit"] == 2 and diagnostic["before"] == diagnostic["after"]
assert diagnostic["production_source_sha256"] == SOURCE
diagnostic_count = verify_map(Path(diagnostic["snapshot"]), diagnostic["after"])
failure = diagnostic["diagnostic_failure"]
assert failure["caps_unchanged"] and failure["original_consume_code_unchanged"]
assert failure["original_init_code_unchanged"] and failure["original_name_meter_code_unchanged"]
assert (failure["work_before"], failure["requested_units"], failure["work_after"]) == (262144, 1, 262145)
budget = failure["failing_budget"]
assert sum(budget["phase_units"].values()) == budget["counted_units"] == 262145
assert diagnostic["diagnostic_completion"]["original_methods_restored"]

meta = read("tests-checks/snapshot-name-environment-v20-01.json")
public = read("tests-checks/red-name-environment-v20-01-311-receipt.json")
assert public["exit"] == 0 and public["identity"]["version_info"] == [3, 11, 15]
assert meta["generator_sha256"] == public["generator_sha256"] == SOURCE
assert public["metadata_sha256"] == pins["tests-checks/snapshot-name-environment-v20-01.json"]
public_count = verify_map(Path(meta["snapshot"]), meta["source_hashes"])
data = records(T / "tests-checks/red-name-environment-v20-01-311.txt")
cases = [row for row in data if "name_environment_case" in row]
summaries = [row for row in data if "name_environment_summary" in row]
assert len(cases) == 24 and len(summaries) == 1
summary = summaries[0]
assert summary["exercised"] == 24 and summary["exercised_projections"] == 58
assert not any(summary[field] for field in (
    "semantic_errors", "analysis_errors", "oracle_errors", "instrumentation_errors"))
pack = read("tests-checks/name-environment-cases-v1.json")
expected_cases = {case["id"]: case for case in pack["cases"]}
old_receipt = read("tests-checks/red-name-env-v19-311-311-receipt.json")
old_log = Path(old_receipt["log"])
assert sha(old_log.read_bytes()) == old_receipt["log_sha256"]
old_cases = {row["name_environment_case"]: row for row in records(old_log)
             if "name_environment_case" in row}
for row in cases:
    expected = expected_cases[row["name_environment_case"]]
    assert row["semantic_passed"] and row["witnesses"] == expected["witnesses"]
    assert row["witnesses"] == old_cases[row["name_environment_case"]]["witnesses"]
    assert row["source_sha256"] == sha(expected["source"].encode())
    assert row["oracle_sha256"] == sha(expected["oracle_source"].encode())
    metrics = row["metrics"]
    assert sum(metrics["charged_phases"].values()) == metrics["charged_unit_sum_across_budgets"]
    assert sum(metrics["name_charged_kinds"].values()) == sum(metrics["name_charged_phases"].values())
old_probe = ast.parse((T / "tests-checks/name-environment-probe-v1.py").read_bytes())
new_probe = ast.parse((T / "tests-checks/name-environment-probe-v20-v1.py").read_bytes())
for name in ("public_review", "project_oracles"):
    old = next(node for node in old_probe.body if isinstance(node, ast.FunctionDef) and node.name == name)
    new = next(node for node in new_probe.body if isinstance(node, ast.FunctionDef) and node.name == name)
    assert ast.dump(old, include_attributes=False) == ast.dump(new, include_attributes=False)

old_total = sum(row["metrics"]["charged_unit_sum_across_budgets"] for row in old_cases.values())
new_total = sum(row["metrics"]["charged_unit_sum_across_budgets"] for row in cases)
result = {
    "standing": "Independent static receipt/byte audit; v20 is rejected, not acceptance or a cold verdict.",
    "source_sha256": SOURCE, "inputs_sha256": pins,
    "snapshot_paths_rehashed": {"design": design_count, "chain32": diagnostic_count, "public24": public_count},
    "design53": {"exit": 1, "failures": 2, "errors": 1},
    "chain32": {"exit": 2, "failure": {key: failure[key] for key in (
        "work_before", "requested_units", "work_after", "limit")}, "phase_units": budget["phase_units"],
        "name_units": sum(budget["name_kind_units"].values())},
    "public24": {"exit": 0, "cases": 24, "oracle_projections": 58,
        "semantic_errors": [], "analysis_errors": [], "instrumentation_errors": [],
        "unchanged_oracle_and_public_function_asts": True, "v19_charged_total": old_total,
        "v20_charged_total": new_total, "ratio": new_total / old_total,
        "largest_individual_budget": max(row["metrics"]["largest_individual_budget_work"] for row in cases)},
    "limits": "Floor-only v20 evidence; no 3.14, matrix, ordinary corpus generation, integration or cold verdict.",
}
with COPY.open("xb") as stream:
    stream.write(Path(__file__).read_bytes())
with OUT.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(result, stream, indent=2)
    stream.write("\n")
print(json.dumps({"report": str(OUT), "sha256": sha(OUT.read_bytes()), "public24": result["public24"]}))
