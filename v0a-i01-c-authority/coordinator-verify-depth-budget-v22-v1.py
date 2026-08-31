"""Rehash completed v22 diagnostics and check accounting; no analyzer import."""
from pathlib import Path
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
PINS = {
    "helper1050": "7ebaa9657dbd47f91ecad3d5f20c18930a84b746d05feda356b8bc21247bcfe2",
    "generator70": "bbb9b75f161f7d9a06f1295d5cf3ae5a62ba11f1dfe1e01f152fb9d246059f57",
}
BASE = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
SOURCE = "61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3"
CONTROL = "bbdc550c042fe62c8c19e838ffe35a9cabc09f22fdd4d941bdb0d9d0a41599a5"
PROBE = "8db7415b97750e8880b25351be76b6fdf75d767a03a3a589d739113a73b6cae0"
CAPS = {"MAXIMUM_ANALYSIS_CARDINALITY": 2147483647,
        "MAXIMUM_ANALYSIS_CHILD_DEPTH": 4,
        "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS": 4096,
        "MAXIMUM_ANALYSIS_HELPER_DEPTH": 64,
        "MAXIMUM_ANALYSIS_WORK_UNITS": 262144}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def create(name, raw):
    with (T / name).open("xb") as stream:
        stream.write(raw)


results = []
for case, pin in PINS.items():
    path = T / ("tests-checks/depth-budget-v22-cost02-" + case + "-311-receipt.json")
    raw = path.read_bytes()
    assert sha(raw) == pin
    receipt = json.loads(raw)
    assert receipt["schema"] == "c-authority-depth-budget-control-v1"
    assert receipt["slot"] == "311" and receipt["case"] == case
    assert receipt["exit"] == receipt["actual_process_returncode"] == 0
    assert receipt["diagnostic_completed"] is receipt["integrity"] is True
    assert receipt["timed_out"] is False and receipt["errors"] == []
    assert receipt["outcome"] == "diagnostic_completed_not_product_verdict"
    assert receipt["base_commit"] == receipt["head_after"] == BASE
    assert receipt["source_sha256"] == SOURCE
    assert receipt["control_sha256"] == CONTROL and receipt["probe_sha256"] == PROBE
    assert receipt["before"] == receipt["after"]
    snapshot = Path(receipt["snapshot"])
    assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots"))
    for name, expected in receipt["before"].items():
        assert not Path(name).is_absolute() and ".." not in Path(name).parts
        assert sha((snapshot / name).read_bytes()) == expected, name
    manifest_name = ".depth-budget-diagnostic/manifest.json"
    manifest = (snapshot / manifest_name).read_bytes()
    assert sha(manifest) == receipt["manifest_sha256"]
    manifest_data = json.loads(manifest)
    assert manifest_data["base_commit"] == BASE
    assert manifest_data["schema"] == "c-authority-depth-budget-manifest-v1"
    assert manifest_data["tracked_count"] == 1761
    assert manifest_data["files"] == {k: v for k, v in receipt["before"].items()
                                     if k != manifest_name}
    assert receipt["inputs_before"] == receipt["inputs_after"]
    for item in receipt["inputs_before"].values():
        assert sha(Path(item["path"]).read_bytes()) == item["sha256"]
    outputs = {}
    for role, item in receipt["outputs"].items():
        outputs[role] = Path(item["path"]).read_bytes()
        assert sha(outputs[role]) == item["sha256"]
        assert len(outputs[role]) == item["bytes"]
    assert outputs["stderr"] == b"" and outputs["log"] == outputs["stdout"]
    setup = json.loads(outputs["setup"])
    assert setup["before"] == receipt["before"]
    assert setup["dirty_before"] == receipt["dirty_after"]
    assert setup["inputs"] == receipt["inputs_before"]
    assert len(setup["original"]) == receipt["tracked_count"] == 1761
    records = [json.loads(line) for line in outputs["stdout"].splitlines()]
    assert len(records) == 5
    identity = records[0]["identity_before_payload_imports"]
    assert identity == receipt["verification"]["identity"]
    assert identity["version_info"] == [3, 11, 15]
    assert identity["executable"] == r"D:\Pontius-tools\py311\Scripts\python.exe"
    assert identity["dont_write_bytecode"] is identity["safe_path"] is True
    assert identity["environment"] == setup["environment"]
    failure = records[2]["depth_budget_failure"]
    refusal = records[3]["depth_budget_refusal"]
    complete = records[4]["depth_budget_diagnostic_complete"]
    assert complete == receipt["verification"]["completion"]
    assert complete["completed"] is complete["diagnostic_only"] is True
    assert complete["caps_unchanged"] is complete["original_methods_restored"] is True
    assert complete["requested_units_accounted"] is True
    assert complete["review_returned"] is False
    assert complete["caps"] == CAPS and complete["budget_failures"] == 1
    assert complete["refusal"] == refusal["reason"] == "analysis work units exceed 262144"
    assert failure["work_before"] == 262143
    assert failure["work_after"] == failure["work_before"] + failure["requested_units"]
    assert failure["limit"] == 262144
    for name in ["caps_unchanged", "original_consume_code_unchanged",
                 "original_init_code_unchanged", "original_name_meter_code_unchanged"]:
        assert failure[name] is True
    for epoch in complete["all_original_budgets"]:
        assert epoch["counted_units"] == epoch["work_after"] - epoch["initial_work"]
        assert sum(epoch["phase_units"].values()) == epoch["counted_units"]
        assert sum(epoch["stage_units"].values()) == epoch["counted_units"]
    failing = failure["failing_budget"]
    assert failing["epoch"] == complete["failing_epoch"]
    assert failing["counted_units"] == failure["work_after"]
    assert sum(failing["phase_units"].values()) == failing["counted_units"]
    stack = failure["stack"]
    activity_keys = ["_active_deferred_generator_probes_count",
                     "_active_deferred_local_generators_count",
                     "_active_local_helper_returns_count", "active_helper_effects_count"]
    for frame in stack:
        for key in activity_keys:
            if key in frame:
                assert frame[key] == 0
        for key in ["values_authority_enabled", "current_authority_enabled"]:
            if key in frame:
                assert frame[key] is False
    phases = failing["phase_units"]
    events = failing["events"]
    if case == "helper1050":
        assert failing["epoch"] == 1 and failure["requested_units"] == 2
        assert phases["publication"] == 117670 and phases["compaction"] == 93844
        assert events["changed_publications_committed"] == 544
        assert events["compaction/completed"] == 67 and events["compaction/calls"] == 68
        assert any(f["function"] == "_definition_time_protocol_resolver" for f in stack)
        assert any(f.get("ast_statement", {}).get("name") == "helper_540" for f in stack)
        mechanism = "Growing-prefix publication and full compaction during definition registration"
    else:
        assert failing["epoch"] == 6 and failure["requested_units"] == 6
        assert phases["ordering"] == 89193 and phases["assignment_or_overlay"] == 67584
        assert phases["lookup"] == 37727 and phases["state_join"] == 22560
        assert events["state_merge/completed"] == 145
        assert events.get("version_join/calls", 0) == 0
        assert any(f.get("ast_node", {}) == {"kind": "GeneratorExp", "line": 53} for f in stack)
        assert any(f["function"] == "_unittest_receiver_attributes" for f in stack)
        mechanism = "Repeated full name-table reconstruction and ordering during receiver preflight"
    results.append({"case": case, "receipt": str(path), "receipt_sha256": pin,
                    "stdout_sha256": receipt["outputs"]["stdout"]["sha256"],
                    "snapshot_files_rehashed": len(receipt["before"]),
                    "failing_epoch": failing["epoch"], "work_before": failure["work_before"],
                    "requested_units": failure["requested_units"],
                    "phase_units": phases, "events": events, "mechanism": mechanism,
                    "no_active_helper_or_deferred_execution": True})

report = {"schema": "coordinator-v22-depth-budget-verification-v1", "results": results,
          "source_sha256": SOURCE, "caps_unchanged": True,
          "standing": "Two completed diagnostic REDs, not a product or cold-review pass"}
create("coordinator-v22-depth-budget-verification-v1.json",
       (json.dumps(report, indent=2) + "\n").encode())
create("coordinator-verify-depth-budget-v22-v1.py", Path(__file__).read_bytes())
note = """# v22: both original budget failures mechanically located

The coordinator independently rehashed both complete diagnostic snapshots,
input/output files, runtime identity and all budget-epoch accounting. See
coordinator-v22-depth-budget-verification-v1.json for exact receipt/output pins.

The helper1050 case exhausts its first budget while registering helper_540,
before any helper body runs. Publication and full compaction use 211514 of
262145 charged units (80.69%). The current store repeatedly copies growing
prefixes after eight small publications.

The generator70 case exhausts epoch six while creating g48 in receiver
preflight, before deferred consumption. Ordering uses 89193 units, projected
assignment 67584, and lookup 37727. All 145 state merges use the full legacy
route; no sparse version join runs. This is a second storage cost pattern.

Neither trace measures deep execution or establishes a wall-time ratio.
All five caps and original budget methods are unchanged. Diagnostic exit zero
means evidence collection completed: v22 remains rejected by two original
design assertions. Matrix/dev/public24/corpus acceptance remain held.

A simple dict/COW replacement is not justified: real per-definition forks
would still copy growing dictionaries when honestly charged. An isolated
indexed-store and linear bulk-construction experiment is being specified,
with independent growth, collision, retention and failure-atomicity schedules.
No production source lease, W modification, cap change or integration follows
from these diagnostics. Class/capture semantic repair remains a separate lane.

The prior helper1050 diagnostic v1 failed in the probe's partial-state formatter;
its receipt/log remain retained. These v2 diagnostics correct only that probe
guard and its pinned controller filename; source and fixtures are unchanged.
"""
create("coordinator-v22-depth-budget-disposition-v1.md", note.encode())
print(json.dumps({"verified": True, "cases": len(results),
                  "snapshot_files_rehashed": sum(x["snapshot_files_rehashed"] for x in results),
                  "report_sha256": sha((T / "coordinator-v22-depth-budget-verification-v1.json").read_bytes()),
                  "note_sha256": sha((T / "coordinator-v22-depth-budget-disposition-v1.md").read_bytes())}))
