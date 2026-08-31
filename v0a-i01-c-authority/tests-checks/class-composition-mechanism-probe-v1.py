"""Two finite class-composition scopes with delegating scalar-only diagnostics."""

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


EXTENSION_SHA = "50e88cedf77f902012237ccd88700c911fa8f3681c8dada380cca6c3142659ac"
V19_SHA = "3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1"
EXTENSION_IDS = (
    "scalar-class-normal-unsafe", "scalar-class-normal-safe",
    "scalar-class-change-then-raise-unsafe", "scalar-class-change-then-raise-safe",
    "scalar-class-raise-before-change-unsafe", "scalar-class-raise-before-change-safe",
)


def load_extension(path):
    raw = path.read_bytes()
    require(digest(raw) == EXTENSION_SHA, "scalar extension pack changed")
    pack = json.loads(raw)
    require(pack["schema"] == "pontius-scalar-class-composition-cases-v1", "extension schema")
    require(pack["planned_cases"] == pack["planned_projections"] == 6, "extension counts")
    require(tuple(case["id"] for case in pack["cases"]) == EXTENSION_IDS, "extension order")
    require(Counter(case["classification"] for case in pack["cases"])
            == {"clean": 3, "refuse": 3}, "extension classifications")
    for case in pack["cases"]:
        for field, hash_field in (("source", "source_sha256"),
                                  ("oracle_source", "oracle_sha256")):
            raw_source = case[field].encode()
            require(digest(raw_source) == case[hash_field], "extension source pin")
            ast.parse(raw_source)
    return pack


def observe_generator(generator):
    """Delegating instrumentation; retain only scalar JSON and original callables."""
    selected = {"case": None, "event": 0, "class_depth": 0}
    resolver = generator._SourceOrderedResolver
    originals = []

    def value_description(value):
        if value is None:
            return {"present": False}
        if not isinstance(value, generator._FlowValue):
            return {"present": True, "type": type(value).__name__}
        proof = value.helper_provenance
        scalar = (value.value
                  if type(value.value) in (str, int, float, bool, type(None)) else None)
        definition = value.callable_definition
        return {
            "present": True, "kind": value.kind, "scalar": scalar,
            "scalar_type": type(value.value).__name__, "sensitive": value.sensitive,
            "reason": value.reason, "authority_ref_count": len(value.authority_refs),
            "helper_proof": (None if proof is None else {
                "kind": proof.kind, "key": proof.key, "bound": proof.bound}),
            "callable": getattr(definition, "name", None),
        }

    def describe_state(values):
        if not isinstance(values, dict):
            return {"state_type": type(values).__name__}
        result = {"state_type": type(values).__name__, "projected": {
            name: value_description(dict.get(values, name))
            for name in ("owner", "armed", "module")}}
        if not isinstance(values, generator._ExecutionState):
            return result
        authority = values.authority
        # Direct backing dictionaries avoid every metered Mapping operation.
        bindings = values.bindings.data
        cells = authority.cells.data
        objects = authority.objects.data
        result["authority_enabled"] = authority.enabled
        result["budget_units"] = authority.budget.work_units
        result["bound_cells"] = {
            name: [value_description(dict.get(cells, identity))
                   for identity in dict.get(bindings, name, ())]
            for name in ("owner", "armed", "module")
        }
        captured = {}
        for name in ("read", "change"):
            value = dict.get(values, name)
            records = []
            if isinstance(value, generator._FlowValue):
                for identity in value.authority_refs:
                    record = dict.get(objects, identity)
                    records.append({"missing_record": True} if record is None else {
                        "captures": [
                            {"name": capture_name, "cells": [
                                value_description(dict.get(cells, cell)) for cell in alternatives]}
                            for capture_name, alternatives in record.cells
                            if capture_name in ("owner", "armed", "module")
                        ]})
            captured[name] = records
        result["callable_captures"] = captured
        return result

    def emit(event, values, node=None, context=None, **extra):
        units = (values.authority.budget.work_units
                 if isinstance(values, generator._ExecutionState) else None)
        record = {"case": selected["case"], "event": event, "event_index": selected["event"],
                  "class_depth": selected["class_depth"], "state": describe_state(values)}
        selected["event"] += 1
        if node is not None:
            record["node"] = {"type": type(node).__name__, "line": getattr(node, "lineno", None),
                              "name": getattr(node, "name", getattr(node, "id", None))}
        if context is not None:
            record["context"] = {
                "helper_registry": bool(context.helper_registry),
                "active_helper_effects": len(context.active_helper_effects),
                "local_names": sorted(context.lexical_scope.local_names),
                "nonlocal_names": sorted(context.lexical_scope.nonlocal_names),
            }
        record.update(extra)
        print(json.dumps({"class_adoption_mechanism": record}), flush=True)
        if units is not None:
            require(values.authority.budget.work_units == units,
                    "diagnostic observation consumed analysis budget")

    def install(owner, name, factory):
        original = getattr(owner, name)
        originals.append((owner, name, original))
        setattr(owner, name, factory(original))

    def statements_wrapper(original):
        def wrapped(self, statements, values):
            node = statements[0] if len(statements) == 1 else None
            is_class = isinstance(node, ast.ClassDef) and node.name == "Local"
            is_raise = isinstance(node, ast.Raise) and selected["class_depth"] > 0
            if not (is_class or is_raise):
                return original(self, statements, values)
            label = "class" if is_class else "class_direct_raise"
            emit(label + ".before", values, node, self)
            if is_class:
                selected["class_depth"] += 1
            try:
                result = original(self, statements, values)
            except BaseException as error:
                emit(label + ".exception", values, node, self, error_type=type(error).__name__)
                raise
            else:
                emit(label + ".after", result, node, self)
                return result
            finally:
                if is_class:
                    selected["class_depth"] -= 1
        return wrapped

    def environment_wrapper(original):
        def wrapped(self, value, values):
            name = getattr(value.callable_definition, "name", None)
            if name not in {"read", "change"}:
                return original(self, value, values)
            emit("call_environment.before", values, context=self, callable_name=name)
            result = original(self, value, values)
            emit("call_environment.after", result, context=self, callable_name=name)
            return result
        return wrapped

    def effect_wrapper(original):
        def wrapped(self, node, value, arguments, keywords, values):
            name = node.func.id if isinstance(node.func, ast.Name) else None
            if name not in {"read", "change"}:
                return original(self, node, value, arguments, keywords, values)
            emit("helper_effect.before", values, node, self, callable_name=name)
            try:
                return original(self, node, value, arguments, keywords, values)
            finally:
                emit("helper_effect.after", values, node, self, callable_name=name)
        return wrapped

    def snapshot_wrapper(original):
        def wrapped(self, node, values, value, arguments=None):
            result = original(self, node, values, value, arguments)
            name = node.func.id if isinstance(node.func, ast.Name) else None
            if name in {"read", "change"}:
                emit("call_snapshot.caller", values, node, self, callable_name=name)
                snapshot = dict.get(self.flow.values_by_call, id(node))
                emit("call_snapshot.retained", snapshot, node, self, callable_name=name)
            return result
        return wrapped

    def assignment_wrapper(original):
        def wrapped(self, target, value, values):
            observed = isinstance(target, ast.Name) and target.id in {"owner", "armed"}
            before = len(self.flow.standalone_blockers)
            if observed:
                emit("assignment.before", values, target, self,
                     assigned=value_description(value))
            result = original(self, target, value, values)
            if observed:
                blockers = [{"line": getattr(site, "lineno", None), "reason": reason}
                            for site, reason in self.flow.standalone_blockers[before:]]
                emit("assignment.after", values, target, self, new_blockers=blockers,
                     rebound_names=sorted(self._helper_rebound_names))
            return result
        return wrapped

    def body_wrapper(original):
        def wrapped(node, **keywords):
            if node.name in {"read", "change"}:
                emit("recursive_review.entry", keywords.get("entry_values"), node,
                     closure_depth=keywords.get("closure_depth", 0))
            return original(node, **keywords)
        return wrapped

    install(resolver, "_statements", statements_wrapper)
    install(resolver, "_call_environment", environment_wrapper)
    install(resolver, "_apply_helper_call_effects", effect_wrapper)
    install(resolver, "_snapshot_call", snapshot_wrapper)
    install(resolver, "_assign", assignment_wrapper)
    install(generator, "_review_body", body_wrapper)
    return selected, originals

def main():
    require(len(sys.argv) == 7, "usage: probe SLOT GENERATOR_SHA OLD_PACK NEW_PACK PROBE_SHA SCOPE")
    slot, source_sha, pack_name, extension_name, probe_sha, scope = sys.argv[1:]
    require(scope in {"original-class2", "scalar-class6"}, "unknown finite scope")
    require(source_sha == V19_SHA, "mechanism probe requires exact retained v19")
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
    original_pack = load_pack(pack_path)
    extension_pack = load_extension(Path(extension_name))
    selected_cases = (original_pack["cases"][2:] if scope == "original-class2"
                      else extension_pack["cases"])
    selected_sha = PACK_SHA if scope == "original-class2" else EXTENSION_SHA
    source_path = Path.cwd() / "tools/generate_test_inventory.py"
    require(digest(source_path.read_bytes()) == source_sha, "generator pin mismatch")
    require(Path(importlib.util.find_spec("pontius").origin).resolve()
            == (Path.cwd() / "src/pontius/__init__.py").resolve(), "wrong package resolution")
    spec = importlib.util.spec_from_file_location("storage_composition_generator", source_path)
    generator = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = generator
    spec.loader.exec_module(generator)
    require({name: getattr(generator, name) for name in CAPS} == CAPS, "analysis caps changed")
    diagnostic, original_callables = observe_generator(generator)
    failures, oracle_errors, analyzer_errors = [], [], []
    analyzed = 0
    for case in selected_cases:
        diagnostic["case"] = case["id"]
        diagnostic["event"] = 0
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
    for owner, name, original in original_callables:
        setattr(owner, name, original)
    require({name: getattr(generator, name) for name in CAPS} == CAPS, "caps changed during probe")
    require(digest(source_path.read_bytes()) == source_sha, "generator changed during probe")
    print(json.dumps({
        "storage_composition_summary": True, "generator_sha256": source_sha,
        "probe_sha256": probe_sha, "pack_sha256": selected_sha,
        "planned_cases": len(selected_cases),
        "original_pack_sha256": PACK_SHA, "extension_pack_sha256": EXTENSION_SHA,
        "scope": scope,
        "case_count": len(selected_cases), "analyzed_cases": analyzed,
        "projections": len(selected_cases),
        "failures": failures, "oracle_errors": oracle_errors, "analyzer_errors": analyzer_errors,
        "classifications": dict(Counter(case["classification"] for case in selected_cases)),
        "caps": CAPS,
    }), flush=True)
    return int(bool(failures or oracle_errors or analyzer_errors))


if __name__ == "__main__":
    raise SystemExit(main())
