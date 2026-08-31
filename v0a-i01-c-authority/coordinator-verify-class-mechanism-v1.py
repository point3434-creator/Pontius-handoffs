"""Recheck retained class evidence and primary mechanism without executing fixtures."""
from pathlib import Path
import hashlib
import json
import os
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
CHECKS = T / "tests-checks"
PINS = {
    ("original-class2", "311"): "9c26c08e8fab39c11e0c49ccd952274b0a31eb98899b51d2bd3f419cf9ad0f32",
    ("original-class2", "314"): "b8429565b8179962c00e3207c6669d294ceb678bf255b9f09250d1cb26e31314",
    ("scalar-class6", "311"): "9c86569d53b6664bf5a6f1912607255c253412dac70d2bd74bfb1dda454b6be9",
    ("scalar-class6", "314"): "97ff9ac31ad8a1eb3f75f3dcde461e1c2ff392ed1d705481cd5e9b45f156ff2d",
}
V19_SHA = "3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1"


def h(raw):
    return hashlib.sha256(raw).hexdigest()


def normalize(value):
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items() if k != "budget_units"}
    if isinstance(value, list):
        return [normalize(v) for v in value]
    return value


assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
assert h((T / "engineer-generator-v19.py").read_bytes()) == V19_SHA
results, previous = [], {}
for (scope, slot), pin in PINS.items():
    path = CHECKS / f"class-composition-{scope}-v19-mechanism01-{slot}-receipt.json"
    raw = path.read_bytes()
    assert h(raw) == pin
    r = json.loads(raw)
    assert r["schema"] == "pontius-class-composition-mechanism-receipt-v1"
    assert r["infrastructure_ok"] is True and r["infrastructure_errors"] == []
    assert r["exit"] == 1 and r["oracle_errors"] == [] and r["summary"]["analyzer_errors"] == []
    assert r["generator_sha256"] == V19_SHA
    assert r["before"] == r["after"] and len(r["before"]) == r["all_tracked_paths_unchanged"] == 1761
    snapshot = Path(r["snapshot"])
    assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots"))
    for name, digest in r["before"].items():
        relative = Path(name)
        assert not relative.is_absolute() and not relative.drive and ".." not in relative.parts
        assert h((snapshot / relative).read_bytes()) == digest
    log_raw = Path(r["log"]).read_bytes()
    assert h(log_raw) == r["log_sha256"]
    assert r["identity"]["version_info"] == ([3, 11, 15] if slot == "311" else [3, 14, 6])
    assert r["identity"]["cwd"] == str(snapshot)
    records = [json.loads(line) for line in log_raw.splitlines() if line.startswith(b"{")]
    cases = [x for x in records if "storage_composition_case" in x]
    events = [x["class_adoption_mechanism"] for x in records if "class_adoption_mechanism" in x]
    assert len(cases) == r["cases_observed"] == (2 if scope == "original-class2" else 6)
    assert len(events) == r["mechanism_events"]
    for case in cases:
        assert case["oracle_passed"] is True and case["oracle_actual"] == case["expected"]
        assert case["analyzer_error"] is None and case["oracle_error"] is None
    assert [c["storage_composition_case"] for c in cases if not c["semantic_passed"]] == r["failures"]
    if slot == "311":
        previous[scope] = (cases, normalize(events))
    else:
        assert cases == previous[scope][0]
        assert normalize(events) == previous[scope][1]
    if scope == "scalar-class6":
        for name, initial, changed in (
            ("scalar-class-normal-unsafe", False, True),
            ("scalar-class-normal-safe", True, False),
        ):
            selected = [e for e in events if e["case"] == name and e["state"].get("authority_enabled")]
            environment = [e for e in selected if e["event"] == "call_environment.after"
                           and e.get("callable_name") == "change"]
            assert environment and all(e["state"]["bound_cells"]["armed"] == [] for e in environment)
            assert all(e["state"]["callable_captures"]["change"] == [{"captures": []}]
                       for e in environment)
            assignment = [e for e in selected if e["event"] == "assignment.after"
                          and e["class_depth"] > 0 and e["node"]["name"] == "armed"]
            assert assignment and all(e["state"]["projected"]["armed"]["scalar"] is changed
                                      and e["state"]["bound_cells"]["armed"] == [] for e in assignment)
            after = [e for e in selected if e["event"] == "class.after"]
            assert len(after) == 1
            assert after[0]["state"]["projected"]["armed"]["scalar"] is initial
            assert [c["scalar"] for c in after[0]["state"]["bound_cells"]["armed"]] == [initial]
        for name in ("scalar-class-raise-before-change-unsafe", "scalar-class-raise-before-change-safe"):
            selected = [e for e in events if e["case"] == name and e["state"].get("authority_enabled")]
            raised = [e for e in selected if e["event"] == "class_direct_raise.after"]
            assert raised
            assert any(e["event"] == "helper_effect.before" and e.get("callable_name") == "change"
                       and e["event_index"] > raised[0]["event_index"] and e["class_depth"] > 0
                       for e in selected), "unreachable setter was not observed after direct raise"
    results.append({
        "scope": scope, "slot": slot, "receipt_sha256": pin, "log_sha256": r["log_sha256"],
        "snapshot_rehashed_files": 1761, "failures": r["failures"], "events": len(events),
    })
report = {
    "schema": "coordinator-class-mechanism-verification-v1", "results": results,
    "same_scope_cross_slot_cases_equal": True,
    "same_scope_cross_slot_traces_equal_except_budget_units": True,
    "supported_mechanisms": [
        "Write-only nonlocal setter lacks a captured destination; assignment changes its private projection while outer cell stays original.",
        "Explicit class raise returns normally to the item loop, which subsequently invokes an unreachable setter.",
    ],
    "correction": "Updated-cell/stale-projection was an initial lead, not the first cause demonstrated by these normal cases.",
    "limits": [
        "Protected namespace guard and any post-capture projection consequences require a coherent semantic repair.",
        "Refusal of two unsafe exception cases does not establish correct exception analysis.",
        "Source fixtures were not executed by this verifier or the diagnostic; only independent harmless models were executed.",
        "No production source change, cold verdict, integration or acceptance is implied.",
    ],
}
outputs = {
    "coordinator-class-mechanism-verification-v1.json": (json.dumps(report, indent=2) + "\n").encode(),
    "coordinator-verify-class-mechanism-v1.py": Path(__file__).read_bytes(),
}
assert not any((T / name).exists() for name in outputs)
for name, raw in outputs.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
print(json.dumps({name: h(raw) for name, raw in outputs.items()}, indent=2))
