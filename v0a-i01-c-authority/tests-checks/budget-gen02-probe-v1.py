"""Read-only ordinary --check with an observing wrapper around original consume."""
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

path = Path.cwd() / "tools/generate_test_inventory.py"
assert hashlib.sha256(path.read_bytes()).hexdigest() == (
    "b56551af864fe13c78219dc8392dfaac8b88a0d538a4de1427229e3c0fa8874a")
spec = importlib.util.spec_from_file_location("budget_diagnostic_generator", path)
generator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = generator
spec.loader.exec_module(generator)
original = generator._AnalysisBudget.consume
original_code = original.__code__
assert generator.MAXIMUM_ANALYSIS_WORK_UNITS == 262144
budgets = {}
failure_count = 0


def frame_info(frame):
    out = {"function": frame.f_code.co_qualname, "line": frame.f_lineno}
    if frame.f_code.co_filename == str(path):
        out["file"] = "tools/generate_test_inventory.py"
    else:
        out["file"] = Path(frame.f_code.co_filename).name
    for key in ("relative_path", "item_id", "stable_id", "source_path"):
        value = frame.f_locals.get(key)
        if isinstance(value, str):
            out[key] = value
    for key in ("node", "definition", "method", "function"):
        value = frame.f_locals.get(key)
        if hasattr(value, "lineno") and hasattr(value, "name"):
            out[key] = {"name": value.name, "line": value.lineno}
    return out


def authority_mode(frame):
    observed = frame
    for _ in range(18):
        if observed is None:
            break
        owner = observed.f_locals.get("self")
        if type(owner).__name__ == "_AuthorityState":
            return "enabled" if owner.enabled else "disabled", frame_info(observed)
        if type(owner).__name__ == "_ExecutionState":
            return "enabled" if owner.authority.enabled else "disabled", frame_info(observed)
        if type(owner).__name__ == "_SourceOrderedResolver":
            return "enabled" if owner.helper_registry else "disabled", frame_info(observed)
        observed = observed.f_back
    return "unattributed", None


def tracked(self, units=1):
    global failure_count
    frame = sys._getframe(1)
    key = frame.f_code.co_qualname + ":" + str(frame.f_lineno)
    entry = budgets.setdefault(id(self), {
        "budget": self, "calls": collections.Counter(), "units": collections.Counter(),
        "authority_units": collections.Counter(), "authority_witnesses": {},
        "parents": collections.Counter(), "walk_roots": collections.Counter(),
    })
    entry["calls"][key] += 1
    entry["units"][key] += units
    parent = frame.f_back
    parent_key = (parent.f_code.co_qualname + ":" + str(parent.f_lineno)
                  if parent is not None else "<root>")
    entry["parents"][(key, parent_key)] += units
    if frame.f_code.co_name in {"_metered_ast_walk", "_has_yield_in_lexical_body",
                               "_bounded_local_generator_dependencies"}:
        root = frame.f_locals.get("node", frame.f_locals.get("definition"))
        if hasattr(root, "name") and hasattr(root, "lineno"):
            entry["walk_roots"][(key, root.name, root.lineno)] += units
    if frame.f_code.co_qualname.startswith(("_Authority", "_ExecutionState")):
        mode, witness = authority_mode(frame)
        entry["authority_units"][(key, mode)] += units
        entry["authority_witnesses"].setdefault((key, mode), witness)
    before = self.work_units
    try:
        return original(self, units)
    except generator.InventoryError as error:
        failure_count += 1
        stack = []
        current = frame
        while current is not None:
            stack.append(frame_info(current))
            current = current.f_back
        report = {
            "budget_failure": str(error), "work_before": before, "requested_units": units,
            "work_after": self.work_units, "limit": generator.MAXIMUM_ANALYSIS_WORK_UNITS,
            "original_code_unchanged": original.__code__ is original_code,
            "budget_index": list(budgets).index(id(self)), "total_budget_instances": len(budgets),
            "caller_units": [{"caller": key, "units": count, "calls": entry["calls"][key]}
                             for key, count in entry["units"].most_common()],
            "authority_units": [
                {"caller": key, "mode": mode, "units": count,
                 "scope_witness": entry["authority_witnesses"][(key, mode)]}
                for (key, mode), count in entry["authority_units"].most_common()
            ],
            "caller_parent_units": [
                {"caller": key, "parent": parent, "units": count}
                for (key, parent), count in entry["parents"].most_common()
            ],
            "walk_root_units": [
                {"caller": key, "definition": name, "source_line": line, "units": count}
                for (key, name, line), count in entry["walk_roots"].most_common()
            ],
            "stack": stack,
        }
        print(json.dumps(report), flush=True)
        raise


generator._AnalysisBudget.consume = tracked
exit_code = generator.main(["--check"])
assert original.__code__ is original_code
assert generator.MAXIMUM_ANALYSIS_WORK_UNITS == 262144
print(json.dumps({"ordinary_check_exit": exit_code, "observed_budget_failures": failure_count,
                  "original_consume_delegated": True, "limit_unchanged": 262144,
                  "budget_instances": len(budgets)}), flush=True)
raise SystemExit(exit_code)

