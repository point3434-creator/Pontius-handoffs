"""Rehash and independently recompute all eight v23 diagnostic outcomes."""
from pathlib import Path
import hashlib
import json
import stat
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
h = lambda raw: hashlib.sha256(raw).hexdigest()
SOURCE = "53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499"
CONFIG = {
    "original-composition-ten": {
        "payload": ".original-composition-ten", "case_key": "original_composition_case",
        "packs": {"storage-composition-cases-v1.json": "faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709",
                  "scalar-class-composition-cases-v1.json": "50e88cedf77f902012237ccd88700c911fa8f3681c8dada380cca6c3142659ac"},
        "pins": {"311": "57b0e9a5478f4f7f7c94ff46cc28f45ab0ca7b38b474149e124da3bdf900e5cd",
                 "314": "e74caa55ac367b5442ed34bb0e52b7a56ead23cfeaafeda24f5a202b8e90e63f"},
        "failed": [], "count": 10, "files": 1768,
    },
    "class-extension": {
        "payload": ".class-semantic-extension", "case_key": "class_extension_case",
        "packs": {"class-semantic-extension-cases-v1.json": "925ae5b9354377a5957f0c32c8bf5b58fea01612498b835abd6392f9cc87d268"},
        "pins": {"311": "7536482e030cb2d31267c06bd4ad537e1a82c9bdd3dfb427887d27af023f1e1a",
                 "314": "cd19e112b59cdc77c21c7144111eb4e36e44dfc3d2dc9020c6868b94978c21f5"},
        "failed": ["forwarded-grandparent-unsafe"], "count": 12, "files": 1767,
    },
    "class-name-boundary": {
        "payload": ".class-name-boundary", "case_key": "class_name_boundary_case",
        "packs": {"class-name-boundary-cases-v1.json": "31c50af8fda3cebc65e44d655db600dd1029a3e110b711a82d475750ece05a1c"},
        "pins": {"311": "e296229f1aa8b5ac84fe74cd38f36e0fffd1665b6a061b3e7fabb0ea44da9a51",
                 "314": "0787e1f253921ed230a9928d027f521233a31da193b27d37da4249bb0246f164"},
        "failed": [], "count": 8, "files": 1767,
    },
    "class-comprehension-boundary": {
        "payload": ".class-comprehension-boundary", "case_key": "class_comprehension_boundary_case",
        "packs": {"class-comprehension-boundary-cases-v1.json": "9df895eb5bd645a5e4ef05be0f7c0a3db76df458ca023bbfbd36407ee3496b71"},
        "pins": {"311": "dc63d862c17135c03d3907e27c0343dd7da3db0f392ec7d58bd876c79abad3b9",
                 "314": "78307562073d44cdd4f89afe8383b45febc0915b70b4c502f5f2ad16c16cb534"},
        "failed": ["Q05-deferred-cell-unsafe"], "count": 6, "files": 1767,
    },
}

def read(path):
    assert path.is_absolute() and ".." not in path.parts
    for ancestor in (path, *path.parents):
        assert not getattr(ancestor.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path.read_bytes()

assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
assert h(read(T / "engineer-generator-v23-semantic.py")) == SOURCE
runs = []
for group, config in CONFIG.items():
    expected_cases = []
    for name, digest in config["packs"].items():
        raw = read(C / name)
        assert h(raw) == digest
        expected_cases.extend(json.loads(raw)["cases"])
    assert len(expected_cases) == config["count"]
    previous = None
    for slot, pin in config["pins"].items():
        raw = read(C / (group + "-v23-diag01-" + slot + "-receipt.json"))
        assert h(raw) == pin
        r = json.loads(raw)
        expected_exit = int(bool(config["failed"]))
        assert r["completed"] is True and r["integrity_ok"] is True
        assert r["success"] is (expected_exit == 0) and r["semantic_ok"] is (expected_exit == 0)
        assert type(r["exit"]) is int and type(r["process_returncode"]) is int
        assert r["exit"] == r["process_returncode"] == expected_exit
        assert "error" not in r and "cleanup_error" not in r
        assert r["generator_sha256"] == SOURCE
        assert r["before"] == r["after"] and r["input_hashes_before"] == r["input_hashes_after"]
        snapshot = Path(r["snapshot"])
        assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots"))
        for name, digest in r["before"].items():
            rel = Path(name)
            assert not rel.is_absolute() and not rel.drive and ".." not in rel.parts
            assert h(read(snapshot / rel)) == digest, name
        manifest = read(snapshot / config["payload"] / "manifest.json")
        assert h(manifest) == r["manifest_sha256"] == r["manifest_after_sha256"]
        assert json.loads(manifest) == r["before"]
        assert read(snapshot / ".git/HEAD").decode().strip() == "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
        for key, digest in r["input_hashes_before"].items():
            assert h(read(Path(r["input_paths"][key]))) == digest
        outputs = {key: read(Path(item["path"])) for key, item in r["outputs"].items()}
        assert all(h(outputs[key]) == item["sha256"] for key, item in r["outputs"].items())
        assert outputs["stderr"] == b"" and outputs["log"] == outputs["stdout"] + b"\nCONTROL STDERR\n"
        assert all(r[key] == value for key, value in json.loads(outputs["setup"]).items())
        records = [json.loads(line) for line in outputs["stdout"].splitlines()]
        route_records = [item for item in records if "class_extension_route" in item]
        assert len(route_records) == (2 if group == "class-extension" else 0)
        assert len(records) == config["count"] + 2 + len(route_records)
        assert records == r["retained_partial_records"]
        if route_records:
            assert [item["class_extension_route"] for item in route_records] == r["route_events"]
        identity = records[0]["identity_before_imports"]
        assert identity == r["identity"]
        assert identity["version_info"] == ([3, 11, 15] if slot == "311" else [3, 14, 6])
        assert identity["executable"] == (r"D:\Pontius-tools\py311\Scripts\python.exe" if slot == "311" else r"D:\Pontius\.venv\Scripts\python.exe")
        assert identity["cwd"] == str(snapshot) and identity["environment"] == r["environment"]
        assert identity["manifest_sha256"] == r["manifest_sha256"]
        assert identity["verified_files"] == len(r["before"]) == config["files"] + (5 if slot == "314" else 0)
        cases = [item for item in records if config["case_key"] in item]
        assert len(cases) == config["count"]
        assert [case[config["case_key"]] for case in cases] == [case["id"] for case in expected_cases]
        failed = []
        for actual, expected in zip(cases, expected_cases, strict=True):
            for key in ("classification", "source_sha256", "oracle_sha256", "expected", "required_argv", "unreachable_events"):
                assert actual[key] == expected[key]
            assert h(expected["source"].encode()) == expected["source_sha256"]
            assert h(expected["oracle_source"].encode()) == expected["oracle_sha256"]
            assert actual["oracle_passed"] is True and actual["oracle_actual"] == expected["expected"]
            assert actual["oracle_error"] is None and actual["analyzer_error"] is None
            assert not set(actual["oracle_actual"]["trace"]) & set(expected["unreachable_events"])
            argv = [row["argv"] for row in actual["expanded_rows"] if row["capability_kind"] == "subprocess"]
            assert actual["argv"] == argv
            classification = expected["classification"]
            clean = not actual["blockers"] and argv == expected["required_argv"]
            passed = bool(actual["blockers"]) if classification == "refuse" else (
                clean if classification == "clean" else bool(actual["blockers"]) or clean)
            assert actual["semantic_passed"] is passed
            assert isinstance(actual["receipt_sha256"], str) and len(actual["receipt_sha256"]) == 64
            if not passed:
                failed.append(expected["id"])
                assert classification == "refuse" and actual["blockers"] == []
            if "route_evidence" in actual:
                assert actual["route_evidence"]["coverage_ok"] is True
                if actual["route_evidence"]["required"]:
                    assert actual["route_evidence"]["status"] == "entry-and-row"
        assert failed == config["failed"]
        summary = records[-1]
        assert summary == r["summary"] and summary["completed"] is True
        assert all(type(summary[k]) is int and summary[k] == config["count"]
                   for k in ("analyzed_cases", "case_count", "projections", "planned_cases"))
        assert summary["semantic_failures"] == failed and summary["oracle_errors"] == summary["analyzer_errors"] == []
        if previous is not None:
            assert cases == previous, group
        previous = cases
        runs.append({"group": group, "slot": slot, "receipt_sha256": pin, "manifest_sha256": h(manifest),
                     "snapshot": str(snapshot), "rehashed_files": len(r["before"]) + 1,
                     "cases": config["count"], "passed": config["count"] - len(failed),
                     "semantic_failures": failed, "same_case_records_across_interpreters": slot == "314"})
report = {"schema": "coordinator-v23-semantic-verification-v2", "runs": runs,
          "source_sha256": SOURCE, "payload_executed_by_verifier": False,
          "cases_each_interpreter": 36, "passed_each_interpreter": 34,
          "wrong_clean_cases": ["forwarded-grandparent-unsafe", "Q05-deferred-cell-unsafe"],
          "verifier_correction": "Unissued v1 wrongly assumed class12 emitted only identity+cases+summary, omitting its two predeclared recursive route records. v1 stopped before report creation. v2 validates those two records separately against the retained receipt; no payload rerun or changed case expectations.",
          "disposition": "v23 remains rejected. Preserve 34 passing requirements, repair the two demonstrated transport/activation residuals plus source-proved related paths in a new candidate. No main integration."}
data = (json.dumps(report, indent=2) + "\n").encode()
for name, raw in {"coordinator-v23-semantic-verification-v2.json": data,
                  "coordinator-verify-v23-semantic-v2.py": Path(__file__).read_bytes(),
                  "coordinator-verify-v23-semantic-v1-failed.py": Path(r"D:\Pontius\codex-verify-v23-semantic-v1.py").read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({"report_sha256": h(data), "rehashed_files": sum(r["rehashed_files"] for r in runs),
                  "cases_each_interpreter": 36, "passed_each_interpreter": 34, "same_case_records": True}))
