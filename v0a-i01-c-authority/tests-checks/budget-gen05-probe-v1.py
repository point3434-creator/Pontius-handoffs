"""Read-only ordinary --check; count immediate consume callers without retaining budgets."""
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

path = Path.cwd() / "tools/generate_test_inventory.py"
assert hashlib.sha256(path.read_bytes()).hexdigest() == (
    "d97ea66ef606144bb635f522856af3a5cd08819368af981a0a408c84c1e6cc99")
spec = importlib.util.spec_from_file_location("budget_diagnostic_generator", path)
generator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = generator
spec.loader.exec_module(generator)
original = generator._AnalysisBudget.consume
original_code = original.__code__
caps = {name: getattr(generator, name) for name in (
    "MAXIMUM_ANALYSIS_HELPER_DEPTH", "MAXIMUM_ANALYSIS_CHILD_DEPTH",
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS", "MAXIMUM_ANALYSIS_CARDINALITY",
    "MAXIMUM_ANALYSIS_WORK_UNITS")}
assert tuple(caps.values()) == (64, 4, 4096, 2147483647, 262144)
budgets = {}
budget_epochs = 0
failure_count = 0


def frame_info(frame):
    out = {"function": frame.f_code.co_qualname, "line": frame.f_lineno,
           "file": ("tools/generate_test_inventory.py"
                    if frame.f_code.co_filename == str(path)
                    else Path(frame.f_code.co_filename).name)}
    for key in ("relative_path", "item_id", "stable_id", "source_path"):
        value = frame.f_locals.get(key)
        if isinstance(value, str):
            out[key] = value
    for key in ("node", "definition", "method", "function"):
        value = frame.f_locals.get(key)
        if hasattr(value, "lineno") and hasattr(value, "name"):
            out["ast_" + key] = {"name": value.name, "line": value.lineno}
    return out


def tracked(self, units=1):
    global failure_count, budget_epochs
    before = self.work_units
    entry = budgets.get(id(self))
    # No reference to self is retained: its AST caches may die normally.
    # A reused identity at a reset work counter starts a new observed epoch.
    if entry is None or entry["after"] != before:
        budget_epochs += 1
        entry = budgets[id(self)] = {
            "epoch": budget_epochs, "after": before, "initial_work": before,
            "calls": collections.Counter(), "units": collections.Counter(),
            "parents": collections.Counter(), "thirds": collections.Counter(),
        }
    frame = sys._getframe(1)
    key = frame.f_code.co_qualname + ":" + str(frame.f_lineno)
    parent = frame.f_back
    parent_key = (parent.f_code.co_qualname + ":" + str(parent.f_lineno)
                  if parent is not None else "<root>")
    entry["calls"][key] += 1
    entry["units"][key] += units
    entry["parents"][(key, parent_key)] += units
    if parent is not None and (
        frame.f_code.co_qualname == "_transfer_authority"
        and parent.f_code.co_qualname == "_ExecutionState.__setitem__"
        or frame.f_code.co_qualname == "_AuthorityMap.__getitem__"
        and parent.f_code.co_qualname in {"Mapping.__contains__", "Mapping.get"}
    ):
        third = parent.f_back
        third_key = (third.f_code.co_qualname + ":" + str(third.f_lineno)
                     if third is not None else "<root>")
        entry["thirds"][(key, parent_key, third_key)] += units
    entry["after"] = before + units
    try:
        return original(self, units)
    except generator.InventoryError as error:
        failure_count += 1
        stack = []
        current = frame
        while current is not None:
            stack.append(frame_info(current))
            current = current.f_back
        counted = sum(entry["units"].values())
        assert entry["initial_work"] == 0 and counted == self.work_units
        report = {
            "budget_failure": str(error), "work_before": before, "requested_units": units,
            "work_after": self.work_units, "limit": generator.MAXIMUM_ANALYSIS_WORK_UNITS,
            "original_code_unchanged": original.__code__ is original_code,
            "caps_unchanged": {name: getattr(generator, name) for name in caps} == caps,
            "observed_budget_epoch": entry["epoch"], "observed_epochs": budget_epochs,
            "counted_units_equal_entire_budget": counted == self.work_units,
            "no_budget_objects_retained": True,
            "caller_units": [{"caller": key, "units": count, "calls": entry["calls"][key]}
                             for key, count in entry["units"].most_common()],
            "caller_parent_units": [
                {"caller": key, "parent": parent, "units": count}
                for (key, parent), count in entry["parents"].most_common()
            ],
            "selected_third_level_units": [
                {"caller": key, "parent": parent, "third": third, "units": count}
                for (key, parent, third), count in entry["thirds"].most_common()
            ],
            "stack": stack,
        }
        print(json.dumps(report), flush=True)
        raise


generator._AnalysisBudget.consume = tracked
exit_code = generator.main(["--check"])
assert original.__code__ is original_code
assert {name: getattr(generator, name) for name in caps} == caps
print(json.dumps({"ordinary_check_exit": exit_code, "observed_budget_failures": failure_count,
                  "original_consume_delegated": True, "caps_unchanged": caps,
                  "observed_budget_epochs": budget_epochs,
                  "instrumentation": "caller/immediate-parent plus selected third-level; final stack only; no budget retention"}),
      flush=True)
raise SystemExit(exit_code)
