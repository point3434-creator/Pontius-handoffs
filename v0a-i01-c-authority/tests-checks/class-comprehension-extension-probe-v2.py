"""Fixed eight-case class/comprehension boundary probe; authoring does not authorize execution."""
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

PACK_SHA = "eb5551c054fc89da28fd2e4db433f56f7a3dbbd4cdb70509070a89fe362c74fd"
SCHEDULE_SHA = "ed292bcf0207aad474e8293cf055c17de6409b9d851f95a8b8225d4375848dc6"
PAYLOAD = ".class-comprehension-extension"
SCHEMA = "pontius-class-comprehension-extension-v1"
CASE_IDS = (
    "R01-attribute-receiver-unsafe",
    "R02-attribute-receiver-dormant",
    "R03-indexed-receiver-unsafe",
    "R04-indexed-receiver-dormant",
    "R05-nested-generator-join-unsafe",
    "R06-nested-generator-join-safe",
    "R07-initially-empty-generator-grown-unsafe",
    "R08-initially-empty-generator-dormant",
)

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
    require(pack["schema"] == "pontius-storage-composition-cases-v1"
            and pack["pack_name"] == "class-comprehension-extension-v1", "casepack schema")
    require(pack["requirements"]["class_name_addendum_sha256"]
            == "de7b5417b2cc899710af0a32332360f31546b6264d1cb58896104a362568e93f"
            and pack["requirements"]["candidate_v23_inspected"] is True
            and pack["requirements"]["extension_results_opened"] is False
            and pack["requirements"]["root_table_approved"] is True
            and pack["requirements"]["source_basis_v23_sha256"]
            == "53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499",
            "frozen requirement basis")
    require(all(type(pack[field]) is int
                for field in ("planned_cases", "planned_projections"))
            and pack["planned_cases"] == pack["planned_projections"] == 8, "finite counts")
    require(tuple(case["id"] for case in pack["cases"]) == CASE_IDS, "case order")
    require(tuple(case["schedule_id"] for case in pack["cases"])
            == tuple("R" + str(n).zfill(2) for n in range(1, 9)), "schedule identities")
    require(type(pack["classifications"]) is dict
            and all(type(count) is int for count in pack["classifications"].values())
            and pack["classifications"] == {"clean": 3, "refuse": 4, "permitted-refusal": 1}
            and dict(Counter(case["classification"] for case in pack["cases"]))
            == pack["classifications"], "classifications")
    for case in pack["cases"]:
        for field, hash_field in (("source", "source_sha256"), ("oracle_source", "oracle_sha256")):
            value = case[field]
            require(type(value) is str and value.endswith("\n") and "\r" not in value,
                    "source format")
            require(digest(value.encode()) == case[hash_field], "case source pin")
            ast.parse(value, filename="<unexecuted-source-check>")
    return pack


def oracle(case):
    source = case["oracle_source"]
    tree = ast.parse(source, filename="<independent-harmless-model>")
    require(not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree)),
            "harmless model imports")
    forbidden = {"subprocess", "sys", "os", "pontius", "exec", "eval", "compile", "open", "__import__"}
    require(not any(isinstance(n, ast.Name) and n.id in forbidden for n in ast.walk(tree)),
            "harmless model forbidden name")
    allowed = {name: getattr(builtins, name)
               for name in ("__build_class__", "staticmethod", "tuple", "list", "NameError")}
    namespace = {"__builtins__": allowed, "__name__": "independent_class_comprehension_extension_model"}
    # Only the separately authored, pinned harmless Model is executed.
    exec(compile(tree, "<independent-harmless-model>", "exec", dont_inherit=True), namespace)
    try:
        result = namespace["Model"]().test_static()
    except TypeError:
        result = "TypeError"
    actual = {"trace": list(namespace["_events"]), "result": result}
    passed = actual == case["expected"] and not any(
        event in actual["trace"] for event in case["unreachable_events"])
    return actual, passed


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
    # Sensitive source bytes are passed only to the real public static review API.
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
    require(len(manifest) == 1767 + (5 if slot == "314" else 0), "manifest count")
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
    spec = importlib.util.spec_from_file_location("class_comprehension_extension_generator", source_path)
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
            "class_comprehension_extension_case": case["id"], "schedule_id": case["schedule_id"],
            "classification": case["classification"], "source_sha256": case["source_sha256"],
            "oracle_sha256": case["oracle_sha256"], "expected": case["expected"],
            "unreachable_events": case["unreachable_events"], "required_argv": case["required_argv"],
            "oracle_actual": actual, "oracle_passed": oracle_passed, "oracle_error": oracle_error,
            "analyzer_error": analyzer_error, "argv": argv, "expanded_rows": rows,
            "blockers": blockers, "semantic_passed": semantic_ok, "passed": semantic_ok,
            "receipt_sha256": digest(canonical(review["receipt"])) if review is not None else None,
        }, allow_nan=False), flush=True)
    require(all(type(getattr(generator, name)) is int for name in CAPS)
            and {name: getattr(generator, name) for name in CAPS} == CAPS, "caps changed during run")
    hashes(snapshot, manifest)
    require(digest(checked(payload / "manifest.json").read_bytes()) == manifest_sha, "manifest changed")
    summary = {"class_comprehension_extension_summary": True, "schema": SCHEMA, "slot": slot,
               "generator_sha256": source_sha, "pack_sha256": PACK_SHA, "probe_sha256": probe_sha,
               "schedule_sha256": SCHEDULE_SHA, "planned_cases": 8, "case_count": 8,
               "projections": 8, "analyzed_cases": analyzed,
               "semantic_failures": semantic_failures,
               "oracle_errors": oracle_errors, "analyzer_errors": analyzer_errors,
               "completed": analyzed == 8 and not oracle_errors and not analyzer_errors,
               "classifications": pack["classifications"], "caps": CAPS}
    print(json.dumps(summary), flush=True)
    return int(bool(semantic_failures or oracle_errors or analyzer_errors))


if __name__ == "__main__":
    raise SystemExit(main())
