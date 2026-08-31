"""Four fixed public storage-composition checks; no payload runs on import."""

import ast
import builtins
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

PACK_SHA = "faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709"
CASE_IDS = (
    "shared-list-consumed", "shared-list-dormant",
    "class-adoption-unsafe", "class-adoption-safe",
)
SLOTS = {
    "311": (r"D:\Pontius-tools\py311\Scripts\python.exe", (3, 11, 15)),
    "314": (r"D:\Pontius\.venv\Scripts\python.exe", (3, 14, 6)),
}
CAPS = {
    "MAXIMUM_ANALYSIS_HELPER_DEPTH": 64,
    "MAXIMUM_ANALYSIS_CHILD_DEPTH": 4,
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS": 4096,
    "MAXIMUM_ANALYSIS_CARDINALITY": 2147483647,
    "MAXIMUM_ANALYSIS_WORK_UNITS": 262144,
}


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("utf-8")


def load_pack(path):
    raw = path.read_bytes()
    require(digest(raw) == PACK_SHA, "case pack changed")
    pack = json.loads(raw)
    require(pack["schema"] == "pontius-storage-composition-cases-v1", "case schema")
    require(type(pack["planned_cases"]) is int and pack["planned_cases"] == 4, "case count")
    require(type(pack["planned_projections"]) is int
            and pack["planned_projections"] == 4, "projection count")
    require(tuple(case["id"] for case in pack["cases"]) == CASE_IDS, "case identities/order")
    require(Counter(case["classification"] for case in pack["cases"])
            == {"clean": 2, "refuse": 2}, "classification changed")
    for case in pack["cases"]:
        for field, hash_field in (("source", "source_sha256"),
                                  ("oracle_source", "oracle_sha256")):
            value = case[field]
            require(type(value) is str and "\r" not in value and value.endswith("\n"),
                    "source format: " + case["id"])
            require(digest(value.encode()) == case[hash_field], "source digest: " + case["id"])
        # Parsing source is not execution. Only the separately authored oracle is compiled.
        ast.parse(case["source"], filename="<sensitive-bytes-only>")
    return pack


def oracle(case):
    source = case["oracle_source"]
    require("subprocess" not in source and "pontius" not in source, "unsafe oracle text")
    tree = ast.parse(source, filename="<harmless-storage-composition>")
    require(not any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree)),
            "oracle may not import")
    allowed = {name: getattr(builtins, name) for name in ("__build_class__", "staticmethod")}
    namespace = {"__builtins__": allowed, "__name__": "harmless_composition"}
    exec(compile(tree, "<harmless-storage-composition>", "exec", dont_inherit=True), namespace)
    try:
        result = namespace["Model"]().test_static()
    except Exception as error:
        result = type(error).__name__
    actual = {"trace": namespace["_events"], "result": result}
    return actual, (actual == case["expected"] and not any(
        event in actual["trace"] for event in case["unreachable_events"]))


def public_review(generator, source):
    relative = "tests/test_storage_composition.py"
    stable_id = relative + "::ReviewTests::test_static"
    assignment = {"profile_name": "current", "payload_id": "current:" + relative,
                  "expectation": {"kind": "pass"}}
    census = {"test_file_count": 1, "stable_id_count": 1,
              "stable_ids_sha256": digest((stable_id + "\n").encode())}
    inventory = {
        "schema_version": "pontius-test-inventory-v1", "baseline_commit": "1" * 40,
        "baseline_discovery": census, "discovery": census,
        "entries": [{"stable_id": stable_id, "relative_path": relative,
                     "case_name": "ReviewTests", "method_name": "test_static",
                     "assignment": assignment, "baseline_assignment": assignment}],
    }
    return generator.derive_design_review(
        baseline_commit="1" * 40, baseline_root_tree_oid="2" * 40,
        inventory_document=inventory, inventory_document_bytes=canonical(inventory),
        sources={relative: source}, item_universe=(("stable_id", stable_id),))


def main():
    require(len(sys.argv) == 5, "usage: probe SLOT GENERATOR_SHA PACK_PATH PROBE_SHA")
    slot, source_sha, pack_name, probe_sha = sys.argv[1:]
    require(slot in SLOTS and re.fullmatch("[0-9a-f]{64}", source_sha), "invalid source/slot")
    executable, version = SLOTS[slot]
    require(sys.implementation.name == "cpython" and sys.version_info[:3] == version,
            "wrong payload interpreter")
    require(Path(sys.executable).resolve() == Path(executable).resolve(), "wrong executable")
    require(sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize
            and sys.flags.no_user_site, "wrong payload flags")
    require(Path.cwd().is_relative_to(Path(r"D:\pontius-snapshots")), "not snapshot cwd")
    require(os.environ.get("PYTHONPATH") == str(Path.cwd() / "src"), "wrong PYTHONPATH")
    require(os.environ.get("PONTIUS_GIT") == r"C:\Program Files\Git\cmd\git.exe",
            "wrong absolute Git")
    require(digest(Path(__file__).read_bytes()) == probe_sha, "probe changed")
    identity = {
        "executable": sys.executable, "implementation": sys.implementation.name,
        "version": sys.version, "version_info": list(sys.version_info[:3]),
        "cwd": str(Path.cwd()), "pythonpath": os.environ.get("PYTHONPATH"),
        "flags": str(sys.flags),
    }
    sys.stdout.reconfigure(newline="\n")
    sys.stderr.reconfigure(newline="\n")
    print(json.dumps({"identity_before_imports": identity}), flush=True)
    pack_path = Path(pack_name)
    require(pack_path.is_absolute(), "nonabsolute pack path")
    pack = load_pack(pack_path)
    source_path = Path.cwd() / "tools/generate_test_inventory.py"
    require(digest(source_path.read_bytes()) == source_sha, "generator pin mismatch")
    require(Path(importlib.util.find_spec("pontius").origin).resolve()
            == (Path.cwd() / "src/pontius/__init__.py").resolve(), "wrong package resolution")
    spec = importlib.util.spec_from_file_location("storage_composition_generator", source_path)
    generator = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = generator
    spec.loader.exec_module(generator)
    require({name: getattr(generator, name) for name in CAPS} == CAPS, "analysis caps changed")
    failures, oracle_errors, analyzer_errors = [], [], []
    analyzed = 0
    for case in pack["cases"]:
        actual, oracle_passed, oracle_error = None, False, None
        try:
            actual, oracle_passed = oracle(case)
        except Exception as error:
            oracle_error = {"type": type(error).__name__, "message": str(error)}
        review, analyzer_error, passed = None, None, False
        if not oracle_passed:
            oracle_errors.append(case["id"])
        else:
            try:
                review = public_review(generator, case["source"].encode("utf-8"))
                analyzed += 1
            except Exception as error:
                analyzer_error = {"type": type(error).__name__, "message": str(error)}
                analyzer_errors.append(case["id"])
        argv, blockers, rows = [], [], []
        if review is not None:
            rows = review["receipt"]["expanded_rows"]
            argv = [row["argv"] for row in rows if row["capability_kind"] == "subprocess"]
            blockers = review["unresolved_dynamic_blockers"]
            passed = (bool(blockers) if case["classification"] == "refuse" else
                      not blockers and argv == case["required_argv"])
        if not passed:
            failures.append(case["id"])
        print(json.dumps({
            "storage_composition_case": case["id"], "classification": case["classification"],
            "source_sha256": case["source_sha256"], "oracle_sha256": case["oracle_sha256"],
            "expected": case["expected"], "oracle_actual": actual, "oracle_passed": oracle_passed,
            "oracle_error": oracle_error, "analyzer_error": analyzer_error,
            "unreachable_events": case["unreachable_events"],
            "required_argv": case["required_argv"],
            "argv": argv, "expanded_rows": rows, "blockers": blockers, "semantic_passed": passed,
            "receipt_sha256": digest(canonical(review["receipt"])) if review is not None else None,
        }), flush=True)
    require({name: getattr(generator, name) for name in CAPS} == CAPS, "caps changed during probe")
    require(digest(source_path.read_bytes()) == source_sha, "generator changed during probe")
    print(json.dumps({
        "storage_composition_summary": True, "generator_sha256": source_sha,
        "probe_sha256": probe_sha, "pack_sha256": PACK_SHA, "planned_cases": 4,
        "case_count": len(pack["cases"]), "analyzed_cases": analyzed, "projections": 4,
        "failures": failures, "oracle_errors": oracle_errors, "analyzer_errors": analyzer_errors,
        "classifications": {"clean": 2, "refuse": 2}, "caps": CAPS,
    }), flush=True)
    return int(bool(failures or oracle_errors or analyzer_errors))


if __name__ == "__main__":
    raise SystemExit(main())
