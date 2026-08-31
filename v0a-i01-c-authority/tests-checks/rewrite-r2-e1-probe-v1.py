"""Fixed four-case captured builtin-environment probe; authoring does not authorize execution."""
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
import types

PACK_SHA = "59b8457a2323634d883fb2c9b0ff82a1e60cd980c5f2a4b50e627c8ca32cdb9b"
SCHEDULE_SHA = "4fcb92ed30a86be1664d9b1981e5e8dc8c47d5d76eaab7b08dc09db74abc9f11"
PAYLOAD = ".rewrite-r2-e1"
SCHEMA = "pontius-r2-e1-v1"
CASE_IDS = ("E01-standard", "E02-module-empty", "E03-module-empty-deleted", "E04-local-empty")

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


def load_pack(path):
    raw = checked(path).read_bytes()
    require(digest(raw) == PACK_SHA, "casepack pin")
    pack = json.loads(raw)
    require(pack["schema"] == "pontius-builtin-context-cases-v1"
            and pack["pack_name"] == "rewrite-r2-e1-v1"
            and pack["execution_authorized"] is False, "casepack schema/standing")
    requirement = pack["requirements"]
    require(requirement["finding_preparation_sha256"]
            == "effe5454d347cf2a42dbc90e913a2f2be0e5adb31acf91c2495c58b9877dc50c"
            and requirement["source_sha256"]
            == "7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d"
            and requirement["authorizing_commit"] == "4bb64a2c06900a57a40785df09a6bf7d0c66ddd9"
            and requirement["fixed12_unchanged"] is True
            and requirement["helper_valued_maps_used"] is False
            and requirement["source_AST_only"] is True, "frozen requirement basis")
    require(all(type(pack[field]) is int for field in ("planned_cases", "planned_projections"))
            and pack["planned_cases"] == pack["planned_projections"] == 4, "finite counts")
    require(tuple(case["id"] for case in pack["cases"]) == CASE_IDS, "case order")
    require(tuple(case["schedule_id"] for case in pack["cases"])
            == ("E01", "E02", "E03", "E04"), "schedule identities")
    require(type(pack["classifications"]) is dict
            and all(type(count) is int for count in pack["classifications"].values())
            and pack["classifications"] == {"clean": 2, "refuse": 2}
            and dict(Counter(case["classification"] for case in pack["cases"]))
            == pack["classifications"], "classifications")
    envelope = pack["public_envelope"]
    require(envelope["source_relative_path"] == "tests/test_structural_review.py"
            and envelope["stable_ids"] == ["tests/test_structural_review.py::ReviewTests::test_static"]
            and canonical(envelope["inventory_document"])
            == envelope["inventory_document_bytes_utf8"].encode("utf-8")
            and digest(envelope["inventory_document_bytes_utf8"].encode("utf-8"))
            == envelope["inventory_document_bytes_sha256"], "adopted public envelope")
    for case in pack["cases"]:
        for field, hash_field in (("source", "source_sha256"), ("oracle_source", "oracle_sha256")):
            value = case[field]
            require(type(value) is str and value.endswith("\n") and "\r" not in value,
                    "source format")
            require(digest(value.encode()) == case[hash_field], "case source pin")
            ast.parse(value, filename="<unexecuted-source-check>")
        tree = ast.parse(case["source"])
        classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        require(len(classes) == 1 and classes[0].name == "ReviewTests", "source class entry")
        methods = [node for node in classes[0].body if isinstance(node, ast.FunctionDef)]
        require(len(methods) == 1 and methods[0].name == "test_static"
                and not methods[0].decorator_list, "source method entry")
    return pack


def oracle(case):
    tree = ast.parse(case["oracle_source"], filename="<independent-harmless-builtins-model>")
    require(not any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree)),
            "harmless model imports")
    forbidden = {"subprocess", "sys", "os", "pontius", "exec", "eval", "compile", "open", "__import__"}
    require(not any(isinstance(node, ast.Name) and node.id in forbidden for node in ast.walk(tree)),
            "harmless model forbidden name")
    namespace = {
        "__builtins__": {"ValueError": builtins.ValueError, "NameError": builtins.NameError},
        "__name__": "independent_builtin_context_model",
        "_STANDARD_BUILTINS": dict(vars(builtins)), "_FUNCTION_TYPE": types.FunctionType,
    }
    # Only the separately authored, pinned harmless Model is executed.
    exec(compile(tree, "<independent-harmless-builtins-model>", "exec", dont_inherit=True), namespace)
    function = namespace["_function"]
    context = namespace["_context"]
    captured = namespace["_builtin_context"]
    require(type(function) is types.FunctionType and function.__globals__ is context
            and function.__builtins__ is captured and function.__closure__ is None
            and function.__code__.co_freevars == (), "actual captured builtin context")
    result, exception = None, None
    try:
        result = function()
    except NameError as error:
        exception = {"type": type(error).__name__, "name": error.name}
    actual = {"trace": list(namespace["_events"]), "result": result, "exception": exception,
              "captured_builtins_empty": captured == {},
              "module_key_present": "__builtins__" in context}
    passed = actual == case["expected"] and not any(
        event in actual["trace"] for event in case["unreachable_events"])
    return actual, passed


def public_review(generator, source):
    relative = "tests/test_structural_review.py"
    stable = relative + "::ReviewTests::test_static"
    assignment = {"profile_name": "current", "payload_id": "current:" + relative,
                  "expectation": {"kind": "pass"}}
    census = {"test_file_count": 1, "stable_id_count": 1,
              "stable_ids_sha256": digest((stable + "\n").encode())}
    inventory = {
        "schema_version": "pontius-test-inventory-v1", "baseline_commit": "1" * 40,
        "baseline_discovery": census, "discovery": census,
        "entries": [{"stable_id": stable, "relative_path": relative,
                     "case_name": "ReviewTests", "method_name": "test_static",
                     "assignment": assignment, "baseline_assignment": assignment}],
    }
    encoded = (json.dumps(inventory, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return generator.derive_design_review(
        baseline_commit="1" * 40, baseline_root_tree_oid="2" * 40,
        inventory_document=inventory, inventory_document_bytes=encoded,
        sources={relative: source}, item_universe=(("stable_id", stable),))


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
    payload_names = {"probe.py", "cases.json", "control.py", "schedule.md", "retained-source.py", "run.json"}
    if slot == "314":
        payload_names.update({"floor-receipt.json", "floor-setup.json", "floor-stdout.txt",
                              "floor-stderr.txt", "floor-log.txt"})
    require({name[len(PAYLOAD) + 1:] for name in manifest if name.startswith(PAYLOAD + "/")}
            == payload_names and len(manifest) == 1761 + len(payload_names), "manifest payload/count")
    hashes(snapshot, manifest)
    run = json.loads(checked(payload / "run.json").read_bytes())
    require(run["schema"] == SCHEMA and run["slot"] == slot, "run config")
    source_sha = run["generator_sha256"]
    require(type(source_sha) is str and len(source_sha) == 64
            and all(c in "0123456789abcdef" for c in source_sha), "candidate digest")
    require(run["pack_sha256"] == PACK_SHA
            and run["schedule_sha256"] == SCHEDULE_SHA, "run input identity")
    probe_sha = digest(checked(Path(__file__).absolute()).read_bytes())
    require(probe_sha == run["probe_sha256"], "probe pin")
    require(digest(checked(payload / "control.py").read_bytes()) == run["control_sha256"], "control pin")
    require(digest(checked(payload / "schedule.md").read_bytes()) == SCHEDULE_SHA, "schedule bytes")
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
    pack = load_pack(payload / "cases.json")
    spec = importlib.util.spec_from_file_location("rewrite_r2_e1_generator", source_path)
    require(spec is not None and spec.loader is not None, "generator import spec")
    generator = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = generator
    spec.loader.exec_module(generator)
    require(all(type(getattr(generator, name)) is int for name in CAPS)
            and {name: getattr(generator, name) for name in CAPS} == CAPS, "caps changed")
    semantic_failures, oracle_errors, analyzer_errors = [], [], []
    analyzed = 0
    for case in pack["cases"]:
        actual, oracle_passed, oracle_error = None, False, None
        try:
            actual, oracle_passed = oracle(case)
        except Exception as error:
            oracle_error = {"type": type(error).__name__, "message": str(error)}
        review, analyzer_error = None, None
        if not oracle_passed:
            oracle_errors.append(case["id"])
        else:
            try:
                review = public_review(generator, case["source"].encode())
                analyzed += 1
            except Exception as error:
                analyzer_error = {"type": type(error).__name__, "message": str(error)}
                analyzer_errors.append(case["id"])
        rows = review["receipt"]["expanded_rows"] if review is not None else []
        argv = [row["argv"] for row in rows if row["capability_kind"] == "subprocess"]
        blockers = review["unresolved_dynamic_blockers"] if review is not None else []
        public_ok = (bool(blockers) if case["classification"] == "refuse" else
                     bool(blockers) or argv == case["required_argv"]
                     if case["classification"] == "permitted-refusal" else
                     not blockers and argv == case["required_argv"])
        semantic_ok = bool(oracle_passed and review is not None and public_ok)
        if not semantic_ok:
            semantic_failures.append(case["id"])
        print(json.dumps({
            "rewrite_r2_e1_case": case["id"], "schedule_id": case["schedule_id"],
            "classification": case["classification"], "source_sha256": case["source_sha256"],
            "oracle_sha256": case["oracle_sha256"], "expected": case["expected"],
            "unreachable_events": case["unreachable_events"], "required_argv": case["required_argv"],
            "oracle_actual": actual, "oracle_passed": oracle_passed, "oracle_error": oracle_error,
            "analyzer_error": analyzer_error, "argv": argv, "expanded_rows": rows,
            "blockers": blockers, "semantic_passed": semantic_ok, "passed": semantic_ok,
            "public_result": review,
            "public_result_sha256": digest(canonical(review)) if review is not None else None,
            "receipt_sha256": digest(canonical(review["receipt"])) if review is not None else None,
        }, allow_nan=False), flush=True)
    require(all(type(getattr(generator, name)) is int for name in CAPS)
            and {name: getattr(generator, name) for name in CAPS} == CAPS, "caps changed during run")
    hashes(snapshot, manifest)
    require(digest(checked(payload / "manifest.json").read_bytes()) == manifest_sha, "manifest changed")
    summary = {"rewrite_r2_e1_summary": True, "schema": SCHEMA, "slot": slot,
               "generator_sha256": source_sha, "pack_sha256": PACK_SHA, "probe_sha256": probe_sha,
               "schedule_sha256": SCHEDULE_SHA, "planned_cases": 4, "case_count": 4,
               "projections": 4, "analyzed_cases": analyzed,
               "semantic_failures": semantic_failures,
               "oracle_errors": oracle_errors, "analyzer_errors": analyzer_errors,
               "completed": analyzed == 4 and not oracle_errors and not analyzer_errors,
               "classifications": pack["classifications"], "caps": CAPS}
    print(json.dumps(summary), flush=True)
    return int(bool(semantic_failures or oracle_errors or analyzer_errors))


if __name__ == "__main__":
    raise SystemExit(main())
