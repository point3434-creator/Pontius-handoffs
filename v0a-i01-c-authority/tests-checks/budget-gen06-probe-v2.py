"""Read-only ordinary --check; count immediate consume callers without retaining budgets."""
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

path = Path.cwd() / "tools/generate_test_inventory.py"
assert hashlib.sha256(path.read_bytes()).hexdigest() == (
    "3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1")
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


planner_global = {}


def record_planner(entry, reason, item):
    # Aggregate integers only; no frame, budget, state, value, or AST is retained.
    for destination in (entry["planner_summary"], planner_global):
        group = destination.setdefault(reason, {"count": 0, "metrics": {}})
        group["count"] += 1
        for key in ("N", "K", "B_seen", "E_seen", "planned_cost", "lookup_reduction"):
            value = item.get(key)
            metric = group["metrics"].setdefault(
                key, {"known": 0, "unknown": 0, "min": None, "max": None, "sum": 0})
            if value is None:
                metric["unknown"] += 1
                continue
            metric["known"] += 1
            metric["sum"] += value
            metric["min"] = value if metric["min"] is None else min(metric["min"], value)
            metric["max"] = value if metric["max"] is None else max(metric["max"], value)


def observe_planner(entry, frame, parent):
    merge_name = "_SourceOrderedResolver._merge_states"
    if frame.f_code.co_qualname == merge_name:
        if frame.f_lineno == 21288:
            assert entry["planner_pending"] is None
            local = frame.f_locals
            n = len(local["names"])
            k = len(local["result"].bindings.data)
            item = {"frame_id": id(frame), "N": n, "K": k,
                    "B_seen": None, "E_seen": None, "planned_cost": 3 + 2 * k}
            if item["planned_cost"] >= n:
                record_planner(entry, "fixed_cost_fallback", item)
            else:
                item["B_seen"] = item["E_seen"] = 0
                entry["planner_pending"] = item
        elif frame.f_lineno == 21295:
            item = entry["planner_pending"]
            assert item is not None and item["frame_id"] == id(frame)
            local = frame.f_locals
            if local["name"] in local["names"]:
                item["B_seen"] += 1
                item["E_seen"] += len(local["cells"])
    if frame.f_code.co_qualname != "_transfer_authority" or parent is None:
        return False
    if parent.f_code.co_qualname == merge_name:
        item = entry["planner_pending"]
        if item is not None and item["frame_id"] == id(parent):
            local = parent.f_locals
            assert local["binding_plan"] is not None
            assert item["B_seen"] == len(local["binding_plan"])
            item["planned_cost"] = local["planned_cost"]
            item["lookup_reduction"] = item["N"] - item["planned_cost"]
            assert item["lookup_reduction"] > 0
            record_planner(entry, "optimized_selected", item)
            entry["planner_pending"] = None
        entry["optimized_transfer_charges"] += 1
        return True
    if parent.f_code.co_qualname == "_ExecutionState.__setitem__":
        third = parent.f_back
        item = entry["planner_pending"]
        if (third is not None and third.f_code.co_qualname == merge_name
                and item is not None and item["frame_id"] == id(third)):
            local = third.f_locals
            item["planned_cost"] = local["planned_cost"]
            if item["planned_cost"] >= item["N"]:
                reason = "estimated_cost_fallback"
            elif local.get("identity") in local["seen"]:
                reason = "overlapping_cell_fallback"
            else:
                reason = "missing_cell_fallback"
            record_planner(entry, reason, item)
            entry["planner_pending"] = None
    return False


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
            "planner_summary": {}, "planner_pending": None,
            "optimized_transfer_charges": 0, "optimized_transfer_entry_charges_succeeded": 0,
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
    optimized_transfer = observe_planner(entry, frame, parent)
    entry["after"] = before + units
    try:
        answer = original(self, units)
        if optimized_transfer:
            entry["optimized_transfer_entry_charges_succeeded"] += 1
        return answer
    except generator.InventoryError as error:
        failure_count += 1
        if entry["planner_pending"] is not None:
            record_planner(entry, "incomplete_at_budget_failure", entry["planner_pending"])
            entry["planner_pending"] = None
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
            "planner_summary": entry["planner_summary"],
            "planner_global_summary": planner_global,
            "optimized_transfer_charges": entry["optimized_transfer_charges"],
            "optimized_transfer_entry_charges_succeeded": entry["optimized_transfer_entry_charges_succeeded"],
            "planner_scope": "enabled multi-state merges; B/E are visited eligible-prefix counts, exact for selected plans; selection is not completion",
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
                  "instrumentation": "caller/immediate-parent plus selected third-level/planner events; final stack only; no budget retention"}),
      flush=True)
raise SystemExit(exit_code)
