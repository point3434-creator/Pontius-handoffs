"""Independent custody and public-result check of both class Name-boundary runs."""
from pathlib import Path
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
PINS = {
    "311": "5285ffaf0ad76c3cf0170e5dc101da343ead3f750dc3a027378ea358dc721cf5",
    "314": "3916d1258069dd0191af44dd2fd38847f12d951aab819339ac101e5ddf62b829",
}
PACK_SHA = "31c50af8fda3cebc65e44d655db600dd1029a3e110b711a82d475750ece05a1c"
EXPECTED_FAILURES = ["class-free-read-safe", "class-same-value-shadow-safe",
                     "class-direct-nonlocal-unsafe", "class-direct-global-safe-refused"]
sha = lambda raw: hashlib.sha256(raw).hexdigest()
pack_raw = (T / "tests-checks/class-name-boundary-cases-v1.json").read_bytes()
assert sha(pack_raw) == PACK_SHA
pack = json.loads(pack_raw)
results, all_cases = [], []
for slot, pin in PINS.items():
    path = T / ("tests-checks/class-name-boundary-v19-red01-" + slot + "-receipt.json")
    raw = path.read_bytes()
    assert sha(raw) == pin
    receipt = json.loads(raw)
    assert receipt["schema"] == "pontius-class-name-boundary-v1"
    assert receipt["slot"] == slot and receipt["completed"] is True
    assert receipt["integrity_ok"] is True and receipt["success"] is False
    assert receipt["exit"] == receipt["process_returncode"] == 1
    assert "error" not in receipt and "cleanup_error" not in receipt
    assert receipt["before"] == receipt["after"]
    snapshot = Path(receipt["snapshot"])
    assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots"))
    for name, expected in receipt["before"].items():
        assert not Path(name).is_absolute() and ".." not in Path(name).parts
        assert sha((snapshot / name).read_bytes()) == expected, name
    manifest = snapshot / ".class-name-boundary/manifest.json"
    assert sha(manifest.read_bytes()) == receipt["manifest_sha256"] == receipt["manifest_after_sha256"]
    assert json.loads(manifest.read_bytes()) == receipt["before"]
    assert receipt["input_hashes_before"] == receipt["input_hashes_after"]
    for name, expected in receipt["input_hashes_before"].items():
        assert sha(Path(receipt["input_paths"][name]).read_bytes()) == expected, name
    outputs = {}
    for role, item in receipt["outputs"].items():
        outputs[role] = Path(item["path"]).read_bytes()
        assert sha(outputs[role]) == item["sha256"]
    assert outputs["log"] == outputs["stdout"] + b"\nCONTROL STDERR\n" + outputs["stderr"]
    records = [json.loads(line) for line in outputs["stdout"].splitlines()]
    assert len(records) == 10
    identity = records[0]["identity_before_imports"]
    assert identity == receipt["identity"]
    assert identity["version_info"] == ([3, 11, 15] if slot == "311" else [3, 14, 6])
    assert identity["generator_sha256"] == "3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1"
    cases = records[1:-1]
    failures = []
    for actual, expected in zip(cases, pack["cases"], strict=True):
        assert actual["class_name_boundary_case"] == expected["id"]
        assert actual["oracle_passed"] is True and actual["oracle_error"] is None
        assert actual["oracle_actual"] == expected["expected"]
        assert not set(actual["oracle_actual"]["trace"]).intersection(expected["unreachable_events"])
        assert actual["analyzer_error"] is None and actual["receipt_sha256"] is not None
        assert actual["source_sha256"] == sha(expected["source"].encode()) == expected["source_sha256"]
        assert actual["oracle_sha256"] == sha(expected["oracle_source"].encode()) == expected["oracle_sha256"]
        argv = [r["argv"] for r in actual["expanded_rows"] if r["capability_kind"] == "subprocess"]
        assert actual["argv"] == argv
        kind = expected["classification"]
        passed = (bool(actual["blockers"]) if kind == "refuse" else
                  bool(actual["blockers"]) or argv == expected["required_argv"]
                  if kind == "permitted-refusal" else
                  not actual["blockers"] and argv == expected["required_argv"])
        assert actual["semantic_passed"] is actual["passed"] is bool(passed)
        if not passed:
            failures.append(expected["id"])
    summary = records[-1]
    assert summary == receipt["summary"] and summary["completed"] is True
    assert summary["semantic_failures"] == failures == EXPECTED_FAILURES
    assert summary["oracle_errors"] == summary["analyzer_errors"] == []
    for name in ["class-direct-nonlocal-unsafe", "class-direct-global-safe-refused"]:
        row = next(c for c in cases if c["class_name_boundary_case"] == name)
        assert row["argv"] == [["-m", "outer"]] and row["blockers"] == []
    results.append({"slot": slot, "receipt": str(path), "receipt_sha256": pin,
                    "log_sha256": receipt["outputs"]["log"]["sha256"],
                    "rehash_file_count_including_manifest": len(receipt["before"]) + 1,
                    "semantic_failures": failures, "harmless_models_passed": 8,
                    "analyzer_errors": 0})
    all_cases.append(cases)
assert all_cases[0] == all_cases[1]
report = {"schema": "coordinator-class-name-boundary-red-verification-v1",
          "pack_sha256": PACK_SHA, "results": results,
          "complete_per_case_records_equal_across_runtimes": True,
          "standing": "Replicated prerepair v19 RED; not a semantic implementation or cold verdict"}
def create(name, raw):
    with (T / name).open("xb") as f:
        f.write(raw)
create("coordinator-class-name-boundary-red-verification-v1.json",
       (json.dumps(report, indent=2) + "\n").encode())
create("coordinator-verify-class-name-boundary-red-v1.py", Path(__file__).read_bytes())
note = """# Class Name boundary: replicated prerepair result

All eight harmless models pass on actual Python3.11.15 and3.14.6. All eight
public analyzer calls complete without errors on each slot. Four fixed
requirements fail identically: free-read-safe and same-value-shadow-safe are
refused; the unsafe direct class nonlocal write is silently lost and produces
a clean outer action row; the harmless global-write counterpart is also clean
despite the preregistered required conservative refusal for module writes.

These last two findings have different force. N05 is a demonstrated unsafe
authorization. N08 violates the fixed module-write refusal boundary although
its independent model completes harmlessly. N01/N04/N07 are refused; those
passes alone do not prove precise class lookup or global-write modeling.
N06's refusal is expressly permitted. No expectation was changed after results.

The coordinator rehashed both full snapshots, original inputs, manifests and
raw outputs. Complete per-case records are identical across slots. Exact pins
are in coordinator-class-name-boundary-red-verification-v1.json.

The ownership/class-frame design and final Name addendum v2 now have replicated
prerepair evidence. Class-local absence/fallback and repeated-join requirements
remain explicit implementation-inspection obligations beyond this finite eight.
No semantic source has been implemented yet. All existing class12/original
composition cases, A/B paths, caps and test contracts remain unchanged.
"""
create("coordinator-class-name-boundary-red-disposition-v1.md", note.encode())
print(json.dumps({"verified": True, "cases_each_slot": 8, "failures_each_slot": 4,
                  "snapshot_files_rehashed": sum(r["rehash_file_count_including_manifest"] for r in results),
                  "report_sha256": sha((T / "coordinator-class-name-boundary-red-verification-v1.json").read_bytes()),
                  "note_sha256": sha((T / "coordinator-class-name-boundary-red-disposition-v1.md").read_bytes())}))
