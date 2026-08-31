"""Rehash three completed diagnostics and reconcile original work accounting."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import stat

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
PINS = {
    "generator70": "79339c7b8106d1eee699b41acf7c1c77b1eb54e382eef1483c5a99627b753eec",
}
BASE = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
SOURCE = "1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951"
CONTROL = "d62807554ffd50b7552879c5a7eb8b4b940e729063ab041d36ee9e79b823c8a5"
PROBE = "559b099f96a4fcfb9b88eb05338a45ad2184ca5e153a360ee0123e0ee7969379"
CAPS = {"MAXIMUM_ANALYSIS_CARDINALITY": 2147483647, "MAXIMUM_ANALYSIS_CHILD_DEPTH": 4,
        "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS": 4096, "MAXIMUM_ANALYSIS_HELPER_DEPTH": 64,
        "MAXIMUM_ANALYSIS_WORK_UNITS": 262144}
h = lambda raw: hashlib.sha256(raw).hexdigest()
def read(path):
    assert path.is_absolute() and ".." not in path.parts
    for ancestor in (path, *path.parents):
        assert not getattr(ancestor.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path.read_bytes()

results = []
for case, pin in PINS.items():
    path = T / ("tests-checks/depth-budget-v26-sharing01-" + case + "-311-receipt.json")
    raw = read(path)
    assert h(raw) == pin
    r = json.loads(raw)
    assert r["slot"] == "311" and r["case"] == case
    assert type(r["exit"]) is int and r["exit"] == r["actual_process_returncode"] == 0
    assert r["diagnostic_completed"] is True and r["integrity"] is True
    assert r["timed_out"] is False and r["errors"] == []
    assert r["outcome"] == "diagnostic_completed_not_product_verdict"
    assert r["base_commit"] == r["head_after"] == BASE
    assert r["source_sha256"] == SOURCE and r["control_sha256"] == CONTROL and r["probe_sha256"] == PROBE
    assert len(r["before"]) == 1766 and r["before"] == r["after"]
    snapshot = Path(r["snapshot"])
    assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots"))
    for name, expected in r["before"].items():
        rel = Path(name)
        assert not rel.is_absolute() and not rel.drive and ".." not in rel.parts
        assert h(read(snapshot / rel)) == expected
    assert read(snapshot / ".git/HEAD").decode().strip() == BASE
    manifest_name = ".depth-budget-diagnostic/manifest.json"
    manifest = read(snapshot / manifest_name)
    assert h(manifest) == r["manifest_sha256"]
    m = json.loads(manifest)
    assert m["base_commit"] == BASE and m["tracked_count"] == 1761
    assert m["files"] == {name: sha for name, sha in r["before"].items() if name != manifest_name}
    assert r["inputs_before"] == r["inputs_after"]
    for item in r["inputs_before"].values():
        assert h(read(Path(item["path"]))) == item["sha256"]
    outputs = {role: read(Path(item["path"])) for role, item in r["outputs"].items()}
    for role, item in r["outputs"].items():
        assert h(outputs[role]) == item["sha256"] and len(outputs[role]) == item["bytes"]
    assert outputs["stderr"] == b"" and outputs["log"] == outputs["stdout"]
    setup = json.loads(outputs["setup"])
    assert setup["before"] == r["before"] and setup["dirty_before"] == r["dirty_after"]
    assert setup["inputs"] == r["inputs_before"] and len(setup["original"]) == 1761
    assert {name for name, sha in setup["original"].items() if r["before"][name] != sha} == {"tools/generate_test_inventory.py"}
    rows = [json.loads(line) for line in outputs["stdout"].splitlines()]
    assert len(rows) == 5
    identity = rows[0]["identity_before_payload_imports"]
    scope = rows[1]["depth_budget_scope"]
    failure = rows[2]["depth_budget_failure"]
    refusal = rows[3]["depth_budget_refusal"]
    complete = rows[4]["depth_budget_diagnostic_complete"]
    assert identity == r["verification"]["identity"] and complete == r["verification"]["completion"]
    assert [failure] == r["verification"]["failure_records"]
    assert identity["version_info"] == [3, 11, 15] and identity["cwd"] == str(snapshot)
    assert identity["executable"] == r"D:\Pontius-tools\py311\Scripts\python.exe"
    assert identity["dont_write_bytecode"] is True and identity["safe_path"] is True
    assert identity["environment"] == setup["environment"] and "PYTHONHASHSEED" not in identity["environment"]
    assert complete["completed"] is True and complete["diagnostic_only"] is True
    assert all(complete[key] is True for key in ("caps_unchanged", "original_methods_restored", "requested_units_accounted"))
    assert complete["caps"] == CAPS and complete["budget_failures"] == 1 and complete["review_returned"] is False
    assert complete["refusal"] == refusal["reason"] == "analysis work units exceed 262144"
    assert complete["fixture_sha256"] == scope["fixture_sha256"]
    assert complete["original_expectation"] == scope["original_expectation"]
    assert failure["work_after"] == failure["work_before"] + failure["requested_units"] > 262144
    assert failure["work_before"] <= 262144 and failure["requested_units"] > 0
    assert all(failure[key] is True for key in ("caps_unchanged", "original_consume_code_unchanged",
                                               "original_init_code_unchanged", "original_name_meter_code_unchanged"))
    for epoch in complete["all_original_budgets"]:
        total = epoch["work_after"] - epoch["initial_work"]
        assert total == epoch["counted_units"] == sum(epoch["phase_units"].values()) == sum(epoch["stage_units"].values())
        assert epoch["component_units"] == epoch["phase_units"]
        assert sum(epoch["name_kind_units"].values()) <= total
        costs = epoch["publication_preparation_costs"]
        assert sum(item["calls"] for item in costs) == epoch["events"].get("publication_preparation/exits", 0)
        assert sum(item["calls"] for item in costs if item["completed"]) == epoch["events"].get("publication_preparation/completed", 0)
        assert all(type(item["completed"]) is bool and type(item["dirty"]) is bool for item in costs)
        for item in costs:
            assert all(type(item[key]) is int and item[key] >= 0
                       for key in ("tail_entries", "base_names", "calls", "units", "minimum_units", "maximum_units"))
            assert item["calls"] > 0
            assert item["minimum_units"] * item["calls"] <= item["units"] <= item["maximum_units"] * item["calls"]
    sharing_rows = []
    for epoch in complete["all_original_budgets"]:
        facts = epoch["full_join_sharing_facts"]
        assert sum(row["attempts"] for row in facts) == epoch["events"].get(
            "bulk_input_iterator_requests/_SourceOrderedResolver._merge_states/charge_attempts", 0)
        for row in facts:
            assert type(row["attempts"]) is int and row["attempts"] > 0
            assert type(row["input_count"]) is int and row["input_count"] == len(row["per_root_pending"])
            assert type(row["source_count"]) is int
            flags = ("exact_name_version_inputs", "exact_execution_state_sources", "published_roots_same_by_identity",
                     "all_source_authorities_disabled", "same_meter", "same_budget", "all_roots_pending")
            assert all(type(row[key]) is bool for key in (*flags, "restricted_C_guard_facts"))
            assert row["restricted_C_guard_facts"] is all(row[key] for key in flags)
            for pending in row["per_root_pending"]:
                assert type(pending["size"]) is type(pending["pending_count"]) is int
                assert type(pending["pending_count_known"]) is type(pending["all_pending"]) is bool
                assert pending["all_pending"] is (pending["pending_count_known"] and pending["size"] >= 0
                                                  and pending["size"] == pending["pending_count"])
            sharing_rows.append({"epoch": epoch["epoch"], **row})
    assert sharing_rows
    assert sum(row["attempts"] for row in sharing_rows) == 36
    assert all(row["published_roots_same_by_identity"] is False and row["restricted_C_guard_facts"] is False
               for row in sharing_rows)
    event_budget = failure["failing_budget"]
    final_budget, = [row for row in complete["all_original_budgets"] if row["epoch"] == complete["failing_epoch"]]
    assert event_budget["epoch"] == final_budget["epoch"]
    assert event_budget["work_after"] == final_budget["work_after"] == failure["work_after"]
    assert event_budget["component_units"] == final_budget["component_units"]
    # Preserve inclusive post-unwind accounting separately from the disjoint work partition.
    groups = {}
    for item in final_budget["publication_preparation_costs"]:
        key = (item["tail_entries"], item["dirty"], item["completed"])
        group = groups.setdefault(key, {"calls": 0, "units": 0, "minimum_units": item["minimum_units"],
                                      "maximum_units": item["maximum_units"], "base_min": item["base_names"], "base_max": item["base_names"]})
        group["calls"] += item["calls"]
        group["units"] += item["units"]
        group["minimum_units"] = min(group["minimum_units"], item["minimum_units"])
        group["maximum_units"] = max(group["maximum_units"], item["maximum_units"])
        group["base_min"] = min(group["base_min"], item["base_names"])
        group["base_max"] = max(group["base_max"], item["base_names"])
    results.append({"case": case, "receipt": str(path), "receipt_sha256": pin,
                    "snapshot": str(snapshot), "snapshot_files_rehashed": len(r["before"]),
                    "fixture_sha256": scope["fixture_sha256"], "refusal": complete["refusal"],
                    "original_expectation": complete["original_expectation"],
                    "failing_epoch": final_budget["epoch"], "original_budgets": complete["original_budget_count"],
                    "work_before": failure["work_before"], "requested_units": failure["requested_units"],
                    "component_units": final_budget["component_units"], "events": final_budget["events"],
                    "bulk_input_shapes": final_budget["bulk_input_shapes"],
                    "publication_preparation_inclusive_units": sum(x["units"] for x in final_budget["publication_preparation_costs"]),
                    "publication_groups": [dict(zip(("tail_entries", "dirty", "completed"), key), **value) for key, value in groups.items()],
                    "top_name_kinds": Counter(final_budget["name_kind_units"]).most_common(20),
                    "top_original_charge_parents": event_budget["consume_parent_origins"][:20],
                    "failure_stack": failure["stack"],
                    "pipeline_events": complete["pipeline_events"], "full_join_sharing_facts": sharing_rows,
                    "restricted_C_guard_hits": 0,
                    "disposition": "The proposed identical-root shortcut has zero hits in the measured failing path; do not implement it as this case's remedy. A broader context-local disabled-transfer proof would require separate design authorization."})

report = {"schema": "coordinator-v26-sharing-verification-v1", "results": results,
          "source_sha256": SOURCE, "caps_unchanged": True, "payload_executed_by_verifier": False,
          "standing": "One completed diagnostic measures the proposed shared-root guard, while reproducing the existing work-cap failure. No product pass, optimization approval or cold verdict. Separate semantic repair remains necessary.",
          "limitations": "Hash seed remains absent as in original design tests; do not infer strict cross-run cost ratios. Inclusive publication totals overlap the disjoint component partition. Observer overhead is not a runtime benchmark."}
data = (json.dumps(report, indent=2) + "\n").encode()
for name, raw in {"coordinator-v26-sharing-verification-v1.json": data,
                  "coordinator-verify-sharing-v26-v1.py": Path(__file__).read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({"report_sha256": h(data), "files_rehashed": sum(r["snapshot_files_rehashed"] for r in results),
                  "results": [{k: r[k] for k in ("case", "failing_epoch", "component_units", "events", "publication_preparation_inclusive_units", "restricted_C_guard_hits", "full_join_sharing_facts")} for r in results]}, indent=2))
