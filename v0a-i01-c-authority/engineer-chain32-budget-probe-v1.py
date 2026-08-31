"""One exact 32-generator-chain analysis; scalar-only observation, no fixture execution."""
import ast
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import textwrap

ROOT = Path.cwd()
GENERATOR_SHA = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
TEST_SHA = "c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf"
generator_path = ROOT / "tools/generate_test_inventory.py"
test_path = ROOT / "tests/test_inventory_and_profiles.py"
assert hashlib.sha256(generator_path.read_bytes()).hexdigest() == GENERATOR_SHA
assert hashlib.sha256(test_path.read_bytes()).hexdigest() == TEST_SHA
assert sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15)
assert sys.flags.safe_path and sys.dont_write_bytecode and not sys.flags.optimize
spec = importlib.util.spec_from_file_location("chain32_design_fixtures", test_path)
fixtures = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = fixtures
spec.loader.exec_module(fixtures)
case = fixtures.DesignReviewTests(
    "test_round4_source_order_and_branch_bounds_red_contracts_are_independent")
case.setUp()
generator = case.generator
assert Path(generator.__file__).resolve() == generator_path.resolve()
original_init = generator._AnalysisBudget.__init__
original_consume = generator._AnalysisBudget.consume
init_code = original_init.__code__
consume_code = original_consume.__code__
name_meter_code = generator._NameMeter.charge.__code__
cap_names = (
    "MAXIMUM_ANALYSIS_HELPER_DEPTH", "MAXIMUM_ANALYSIS_CHILD_DEPTH",
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS", "MAXIMUM_ANALYSIS_CARDINALITY",
    "MAXIMUM_ANALYSIS_WORK_UNITS")
caps = {name: getattr(generator, name) for name in cap_names}
assert tuple(caps.values()) == (64, 4, 4096, 2147483647, 262144)
records_by_id = {}
records = []
failure_count = 0
failure_epoch = None


def observed_init(self, *args, **keywords):
    original_init(self, *args, **keywords)
    # Only scalar identity/counters escape this wrapper. No budget/cache/AST reference.
    entry = {
        "epoch": len(records) + 1, "initial_work": self.work_units,
        "after": self.work_units, "calls": collections.Counter(),
        "units": collections.Counter(), "parents": collections.Counter(),
        "thirds": collections.Counter(), "phases": collections.Counter(),
        "name_kinds": collections.Counter(), "name_origins": collections.Counter(),
        "name_kind_phase": collections.Counter(),
    }
    records_by_id[id(self)] = entry
    records.append(entry)


def key(frame):
    return (frame.f_code.co_qualname + ":" + str(frame.f_lineno)
            if frame is not None else "<root>")


def phase_of(frame):
    """Exclusive nearest storage boundary; major nesting and origin details stay visible."""
    fallback = "other"
    current = frame
    while current is not None:
        name = current.f_code.co_qualname
        if name == "_ExecutionState.__init__":
            return "constructor"
        if name in {"_SourceOrderedResolver._merge_states", "_join_name_versions"}:
            return "join"
        if (name.startswith("_name_realize")
                or name.startswith("_NameVersion.ordered_items")
                or name in {"_ExecutionState.items", "_ExecutionState.keys", "_ExecutionState.values"}):
            return "ordering"
        if name in {"_name_find", "_ExecutionState.get", "_ExecutionState.__getitem__",
                    "_ExecutionState.__contains__", "_NameVersion.get"}:
            fallback = "lookup"
        elif name in {"_ExecutionState.__setitem__", "_ExecutionState._project",
                      "_ExecutionState.__delitem__", "_ExecutionState._project_pop",
                      "_ExecutionState.update"}:
            fallback = "assignment_or_overlay"
        elif name == "_ExecutionState.copy":
            return "fork"
        if name.startswith("_SourceOrderedResolver."):
            return fallback
        current = current.f_back
    return fallback


def sorted_rows(counter, labels):
    return [dict(zip(labels, item if isinstance(item, tuple) else (item,)), units=units)
            for item, units in counter.most_common()]


def summary(entry, detailed=False):
    value = {
        "epoch": entry["epoch"], "initial_work": entry["initial_work"],
        "work_after": entry["after"], "counted_units": sum(entry["units"].values()),
        "phase_units": dict(entry["phases"]), "name_kind_units": dict(entry["name_kinds"]),
    }
    if detailed:
        value.update({
            "consume_origins": [
                {"caller": caller, "units": units, "calls": entry["calls"][caller]}
                for caller, units in entry["units"].most_common()],
            "consume_parent_origins": sorted_rows(entry["parents"], ("caller", "parent")),
            "consume_third_origins": sorted_rows(entry["thirds"], ("caller", "parent", "third")),
            "name_origins": sorted_rows(entry["name_origins"], ("kind", "origin")),
            "name_kind_phase_units": sorted_rows(entry["name_kind_phase"], ("kind", "phase")),
        })
    return value


def frame_info(frame):
    value = {
        "function": frame.f_code.co_qualname, "line": frame.f_lineno,
        "file": ("tools/generate_test_inventory.py"
                 if frame.f_code.co_filename == str(generator_path)
                 else Path(frame.f_code.co_filename).name)}
    for field in ("relative_path", "item_id", "stable_id", "source_path"):
        supplied = frame.f_locals.get(field)
        if type(supplied) is str:
            value[field] = supplied
    for field in ("node", "definition", "method", "function"):
        supplied = frame.f_locals.get(field)
        if isinstance(supplied, (ast.FunctionDef, ast.AsyncFunctionDef)):
            value["ast_" + field] = {"name": supplied.name, "line": supplied.lineno}
    return value


def observed_consume(self, units=1):
    global failure_count, failure_epoch
    entry = records_by_id[id(self)]
    before = self.work_units
    assert entry["after"] == before
    frame = sys._getframe(1)
    parent = frame.f_back
    third = parent.f_back if parent is not None else None
    caller_key, parent_key, third_key = key(frame), key(parent), key(third)
    phase = phase_of(frame)
    entry["calls"][caller_key] += 1
    entry["units"][caller_key] += units
    entry["parents"][(caller_key, parent_key)] += units
    entry["thirds"][(caller_key, parent_key, third_key)] += units
    entry["phases"][phase] += units
    if frame.f_code is name_meter_code:
        kind = frame.f_locals["kind"]
        assert type(kind) is str and frame.f_locals["self"].budget is self
        entry["name_kinds"][kind] += units
        entry["name_origins"][(kind, parent_key)] += units
        entry["name_kind_phase"][(kind, phase)] += units
    try:
        answer = original_consume(self, units)
        entry["after"] = self.work_units
        assert self.work_units == before + units
        return answer
    except generator.InventoryError:
        entry["after"] = self.work_units
        failure_count += 1
        failure_epoch = entry["epoch"]
        assert entry["initial_work"] == 0
        assert sum(entry["units"].values()) == self.work_units
        assert sum(entry["phases"].values()) == self.work_units
        if failure_count == 1:
            stack = []
            current = frame
            while current is not None:
                stack.append(frame_info(current))
                current = current.f_back
            print(json.dumps({
                "chain32_budget_failure": {
                    "work_before": before, "requested_units": units,
                    "work_after": self.work_units, "limit": caps["MAXIMUM_ANALYSIS_WORK_UNITS"],
                    "original_consume_code_unchanged": original_consume.__code__ is consume_code,
                    "original_init_code_unchanged": original_init.__code__ is init_code,
                    "original_name_meter_code_unchanged": generator._NameMeter.charge.__code__ is name_meter_code,
                    "caps_unchanged": {name: getattr(generator, name) for name in caps} == caps,
                    "failing_budget": summary(entry, detailed=True),
                    "all_original_budget_summaries": [summary(record) for record in records],
                    "stack": stack,
                    "retention": "Only integer identities, strings and numeric counters retained; no budgets, states, values, frames or AST caches",
                }}, sort_keys=True), flush=True)
        raise


# Byte-equivalent to chained_source(32) and review_evidence(body), with no prefix.
lines = ["g0 = (cp.arange(1) for _ in range(1))"]
lines.extend(f"g{index} = (sum(g{index - 1}) for _ in range(1))" for index in range(1, 32))
lines.append("sum(g31)")
body = "\n".join(lines)
source = (
    "import cupy as cp\n"
    "import unittest\n"
    "class ReviewTests(unittest.TestCase):\n"
    "    def test_static(self):\n"
    f"{textwrap.indent(body, '        ')}\n"
    "    def test_denied(self): pass\n")
fixture = fixtures._source(source)
print(json.dumps({
    "diagnostic_scope": "Only existing review_evidence(chained_source(32)); no prior cases, deep70, runtime body, matrix or corpus",
    "generator_sha256": GENERATOR_SHA, "test_sha256": TEST_SHA,
    "fixture_sha256": hashlib.sha256(fixture).hexdigest(),
    "fixture_bytes": len(fixture), "phase_definition": phase_of.__doc__,
}), flush=True)
generator._AnalysisBudget.__init__ = observed_init
generator._AnalysisBudget.consume = observed_consume
exit_code = 0
review = None
try:
    review = case._review(sources={"tests/test_review.py": fixture})
except generator.InventoryError as error:
    if str(error) != "analysis work units exceed 262144" or failure_count == 0:
        raise
    exit_code = 2
finally:
    assert original_init.__code__ is init_code
    assert original_consume.__code__ is consume_code
    assert generator._NameMeter.charge.__code__ is name_meter_code
    assert {name: getattr(generator, name) for name in caps} == caps
    generator._AnalysisBudget.__init__ = original_init
    generator._AnalysisBudget.consume = original_consume
    assert hashlib.sha256(generator_path.read_bytes()).hexdigest() == GENERATOR_SHA
    assert hashlib.sha256(test_path.read_bytes()).hexdigest() == TEST_SHA
print(json.dumps({
    "chain32_diagnostic_complete": {
        "exit": exit_code, "budget_failures": failure_count, "failing_epoch": failure_epoch,
        "original_budget_count": len(records),
        "all_original_budgets": [summary(record) for record in records],
        "original_methods_restored": generator._AnalysisBudget.consume is original_consume
                                     and generator._AnalysisBudget.__init__ is original_init,
        "caps_unchanged": caps,
        "review_returned": review is not None,
    }}, sort_keys=True), flush=True)
raise SystemExit(exit_code)
