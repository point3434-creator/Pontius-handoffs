"""Original ten frozen composition witnesses; no payload work on import."""
import ast
import builtins
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys


PACKS = {
    "storage": {
        "file": "storage-composition-cases-v1.json",
        "sha256": "faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709",
        "schema": "pontius-storage-composition-cases-v1",
        "ids": ("shared-list-consumed", "shared-list-dormant",
                "class-adoption-unsafe", "class-adoption-safe"),
        "classifications": {"clean": 2, "refuse": 2},
    },
    "scalar": {
        "file": "scalar-class-composition-cases-v1.json",
        "sha256": "50e88cedf77f902012237ccd88700c911fa8f3681c8dada380cca6c3142659ac",
        "schema": "pontius-scalar-class-composition-cases-v1",
        "ids": ("scalar-class-normal-unsafe", "scalar-class-normal-safe",
                "scalar-class-change-then-raise-unsafe", "scalar-class-change-then-raise-safe",
                "scalar-class-raise-before-change-unsafe", "scalar-class-raise-before-change-safe"),
        "classifications": {"clean": 3, "refuse": 3},
    },
}
PACK_HASHES = {scope: metadata["sha256"] for scope, metadata in PACKS.items()}

PLAN_SHA = "3b330b732d99bdf02bae7b270a57f1d9cc0352fe1db573f5148c751084ad3f1a"
PAYLOAD = ".original-composition-ten"
SCHEMA = "pontius-original-composition-ten-v1"
SLOTS = {
    "311": (r"D:\Pontius-tools\py311\Scripts\python.exe", (3, 11, 15)),
    "314": (r"D:\Pontius\.venv\Scripts\python.exe", (3, 14, 6)),
}
CAPS = {
    "MAXIMUM_ANALYSIS_HELPER_DEPTH": 64, "MAXIMUM_ANALYSIS_CHILD_DEPTH": 4,
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS": 4096,
    "MAXIMUM_ANALYSIS_CARDINALITY": 2147483647, "MAXIMUM_ANALYSIS_WORK_UNITS": 262144,
}


def require(value, reason):
    if not value:
        raise RuntimeError(reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("utf-8")


def checked(path):
    require(path.is_absolute() and ".." not in path.parts, "unsafe child path")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        require(not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT,
                "child reparse path")
        if ancestor != path:
            require(stat.S_ISDIR(info.st_mode), "child non-directory ancestor")
    require(stat.S_ISREG(path.lstat().st_mode), "child non-regular input")
    return path


def hashes(snapshot, manifest):
    actual = {}
    for name, wanted in manifest.items():
        relative = Path(name)
        require(not relative.is_absolute() and not relative.drive and ".." not in relative.parts,
                "unsafe manifest name")
        actual[name] = digest(checked(snapshot / relative).read_bytes())
        require(actual[name] == wanted, "manifest input changed: " + name)
    return actual


def load_cases(raw_by_scope):
    require(set(raw_by_scope) == set(PACKS), "exact original pack set")
    combined = []
    for scope, metadata in PACKS.items():
        raw = raw_by_scope[scope]
        require(hashlib.sha256(raw).hexdigest() == metadata["sha256"], "original pack pin: " + scope)
        pack = json.loads(raw)
        count = len(metadata["ids"])
        require(pack["schema"] == metadata["schema"], "original pack schema")
        require(type(pack["planned_cases"]) is int and pack["planned_cases"] == count
                and type(pack["planned_projections"]) is int and pack["planned_projections"] == count,
                "original finite counts")
        require(tuple(case["id"] for case in pack["cases"]) == metadata["ids"], "original case order")
        require(dict(Counter(case["classification"] for case in pack["cases"]))
                == metadata["classifications"], "original classifications")
        for case in pack["cases"]:
            for field, hash_field in (("source", "source_sha256"), ("oracle_source", "oracle_sha256")):
                value = case[field]
                require(type(value) is str and value.endswith("\n") and "\r" not in value,
                        "original source format")
                require(hashlib.sha256(value.encode("utf-8")).hexdigest() == case[hash_field],
                        "original source/model digest")
                # Both are parsed; only the original harmless Model runner compiles its model.
                ast.parse(value, filename="<unexecuted-original-composition-bytes>")
            combined.append((scope, case))
    require(len(combined) == 10, "original combined scope")
    return combined


def storage_oracle(case):
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


def scalar_oracle(case):
    source = case["oracle_source"]
    require("subprocess" not in source and "pontius" not in source, "unsafe oracle text")
    tree = ast.parse(source, filename="<harmless-storage-composition>")
    require(not any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree)),
            "oracle may not import")
    allowed = {name: getattr(builtins, name)
               for name in ("__build_class__", "staticmethod", "ValueError")}
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
    require(len(sys.argv) == 4, "usage: probe SLOT MANIFEST_SHA ENVIRONMENT_SHA")
    slot, manifest_sha, environment_sha = sys.argv[1:]
    require(slot in SLOTS, "slot")
    executable, version = SLOTS[slot]
    require(sys.implementation.name == "cpython" and sys.version_info[:3] == version,
            "wrong real interpreter")
    require(Path(sys.executable).resolve() == checked(Path(executable)).resolve(), "wrong executable")
    require(sys.dont_write_bytecode and sys.flags.safe_path and sys.flags.no_user_site
            and not sys.flags.optimize and not sys.flags.isolated and not sys.flags.ignore_environment
            and not sys.flags.no_site, "requires child -B -P and scrubbed no-user-site environment")
    snapshot = Path.cwd()
    require(snapshot.is_relative_to(Path(r"D:\pontius-snapshots")), "not D-local snapshot")
    require(os.environ.get("PYTHONPATH") == str(snapshot / "src"), "PYTHONPATH")
    require(os.environ.get("PYTHONHASHSEED") == "0", "fixed hash seed")
    require(os.environ.get("PONTIUS_GIT") == r"C:\Program Files\Git\cmd\git.exe", "Git")
    actual_environment = dict(os.environ)
    require(digest(canonical(actual_environment)) == environment_sha, "exact child environment")
    payload = snapshot / PAYLOAD
    manifest_raw = checked(payload / "manifest.json").read_bytes()
    require(digest(manifest_raw) == manifest_sha, "manifest pin")
    manifest = json.loads(manifest_raw)
    require(len(manifest) == 1768 + (5 if slot == "314" else 0), "manifest count")
    hashes(snapshot, manifest)
    run = json.loads(checked(payload / "run.json").read_bytes())
    require(run["schema"] == SCHEMA and run["slot"] == slot, "run config")
    source_sha = run["generator_sha256"]
    require(type(source_sha) is str and len(source_sha) == 64
            and all(c in "0123456789abcdef" for c in source_sha), "candidate digest")
    require(run["pack_sha256"] == PACK_HASHES
            and run["plan_sha256"] == PLAN_SHA, "run input identity")
    probe_sha = digest(checked(Path(__file__).absolute()).read_bytes())
    require(probe_sha == run["probe_sha256"], "probe pin")
    require(digest(checked(payload / "control.py").read_bytes()) == run["control_sha256"], "control pin")
    require(digest(checked(payload / "plan.md").read_bytes()) == PLAN_SHA, "plan bytes")
    source_path = snapshot / "tools/generate_test_inventory.py"
    require(digest(checked(source_path).read_bytes()) == source_sha
            and digest(checked(payload / "retained-source.py").read_bytes()) == source_sha, "exact retained candidate")
    sys.stdout.reconfigure(newline="\n")
    sys.stderr.reconfigure(newline="\n")
    identity = {"executable": sys.executable, "implementation": sys.implementation.name,
                "version": sys.version, "version_info": list(sys.version_info[:3]),
                "cwd": str(snapshot), "flags": str(sys.flags), "environment": actual_environment,
                "manifest_sha256": manifest_sha, "verified_files": len(manifest),
                "generator_sha256": source_sha, "probe_sha256": probe_sha}
    print(json.dumps({"identity_before_imports": identity}), flush=True)
    require(not any(n == "pontius" or n.startswith("pontius.") for n in sys.modules),
            "Pontius imported before generator")
    resolution = importlib.util.find_spec("pontius")
    require(resolution is not None and resolution.origin is not None
            and Path(resolution.origin).resolve() == (snapshot / "src/pontius/__init__.py").resolve(),
            "wrong read-only package resolution")
    cases = load_cases({scope: checked(payload / metadata["file"]).read_bytes()
                        for scope, metadata in PACKS.items()})
    spec = importlib.util.spec_from_file_location("original_composition_generator", source_path)
    require(spec is not None and spec.loader is not None, "generator import spec")
    generator = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = generator
    spec.loader.exec_module(generator)
    require({name: getattr(generator, name) for name in CAPS} == CAPS, "caps changed")

    semantic_failures, oracle_errors, analyzer_errors = [], [], []
    analyzed = 0
    for scope, case in cases:
        actual, oracle_passed, oracle_error = None, False, None
        try:
            actual, oracle_passed = (storage_oracle(case) if scope == "storage" else scalar_oracle(case))
        except Exception as error:
            oracle_error = {"type": type(error).__name__, "message": str(error)}
        review, analyzer_error = None, None
        if not oracle_passed:
            oracle_errors.append(case["id"])
        else:
            try:
                review = public_review(generator, case["source"].encode("utf-8"))
                analyzed += 1
            except Exception as error:
                analyzer_error = {"type": type(error).__name__, "message": str(error)}
                analyzer_errors.append(case["id"])
        rows = review["receipt"]["expanded_rows"] if review is not None else []
        argv = [row["argv"] for row in rows if row["capability_kind"] == "subprocess"]
        blockers = review["unresolved_dynamic_blockers"] if review is not None else []
        public_ok = (bool(blockers) if case["classification"] == "refuse" else
                     not blockers and argv == case["required_argv"])
        semantic_ok = bool(oracle_passed and review is not None and public_ok)
        if not semantic_ok:
            semantic_failures.append(case["id"])
        print(json.dumps({
            "original_composition_case": case["id"], "original_pack": scope,
            "classification": case["classification"], "source_sha256": case["source_sha256"],
            "oracle_sha256": case["oracle_sha256"], "expected": case["expected"],
            "unreachable_events": case["unreachable_events"], "required_argv": case["required_argv"],
            "oracle_actual": actual, "oracle_passed": oracle_passed, "oracle_error": oracle_error,
            "analyzer_error": analyzer_error, "argv": argv, "expanded_rows": rows,
            "blockers": blockers, "semantic_passed": semantic_ok,
            "receipt_sha256": digest(canonical(review["receipt"])) if review is not None else None,
        }, allow_nan=False), flush=True)
    require({name: getattr(generator, name) for name in CAPS} == CAPS, "caps changed during run")
    hashes(snapshot, manifest)
    require(digest(checked(payload / "manifest.json").read_bytes()) == manifest_sha, "manifest changed")
    summary = {"original_composition_summary": True, "schema": SCHEMA, "slot": slot,
               "generator_sha256": source_sha, "pack_sha256": PACK_HASHES, "probe_sha256": probe_sha,
               "plan_sha256": PLAN_SHA, "planned_cases": 10, "case_count": 10,
               "projections": 10, "analyzed_cases": analyzed,
               "semantic_failures": semantic_failures,
               "oracle_errors": oracle_errors, "analyzer_errors": analyzer_errors,
               "completed": analyzed == 10 and not oracle_errors and not analyzer_errors,
               "classifications": {"clean": 5, "refuse": 5}, "caps": CAPS}
    print(json.dumps(summary, allow_nan=False), flush=True)
    return int(bool(semantic_failures or oracle_errors or analyzer_errors))


if __name__ == "__main__":
    raise SystemExit(main())
