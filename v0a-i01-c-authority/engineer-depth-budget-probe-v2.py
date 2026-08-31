"""One selected exact helper1050/generator70 analysis; scalar-only diagnosis, no sensitive source execution."""
import ast
import argparse
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import textwrap

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--case", required=True, choices=("helper1050", "generator70"))
CASE = parser.parse_args().case
ROOT = Path.cwd()
GENERATOR_SHA = "61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3"
TEST_SHA = "c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf"
generator_path = ROOT / "tools/generate_test_inventory.py"
test_path = ROOT / "tests/test_inventory_and_profiles.py"
assert hashlib.sha256(generator_path.read_bytes()).hexdigest() == GENERATOR_SHA
assert hashlib.sha256(test_path.read_bytes()).hexdigest() == TEST_SHA
assert sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15)
assert sys.flags.safe_path and sys.dont_write_bytecode and not sys.flags.optimize
spec = importlib.util.spec_from_file_location("depth_budget_design_fixtures", test_path)
fixtures = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = fixtures
spec.loader.exec_module(fixtures)
case = fixtures.DesignReviewTests(
    "test_analysis_budgets_contain_deep_helpers_and_invalid_ranges" if CASE == "helper1050"
    else "test_round4_source_order_and_branch_bounds_red_contracts_are_independent")
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
patches = []
stage_stack = []
pipeline_events = collections.Counter()


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
        "stage_units": collections.Counter(), "events": collections.Counter(),
        "creation_stack": stack_info(sys._getframe(1)),
    }
    records_by_id[id(self)] = entry
    records.append(entry)


def key(frame):
    return (frame.f_code.co_qualname + ":" + str(frame.f_lineno)
            if frame is not None else "<root>")


def phase_of(frame):
    """Nearest real cursor/storage boundary; pipeline-stage sums are separate."""
    fallback = "other"
    current = frame
    while current is not None:
        name = current.f_code.co_qualname
        if name == "_name_compact":
            return "compaction"
        if name in {"_name_prepare_publication", "_name_charge_publication_commit",
                    "_name_commit_publication", "_name_seal_layer",
                    "_NameCursor.snapshot"}:
            return "publication"
        if name in {"_name_realize_order", "_name_ordered_items", "_name_keys",
                    "_ExecutionState.items", "_ExecutionState.keys", "_ExecutionState.values"}:
            return "ordering"
        if name == "_ExecutionState.__init__":
            return "constructor"
        if name == "_join_name_versions":
            return "version_join"
        if name == "_SourceOrderedResolver._merge_states":
            return "state_join"
        if name in {"_NameCursor._replace_entry", "_ExecutionState.__setitem__",
                    "_ExecutionState._project", "_ExecutionState.__delitem__",
                    "_ExecutionState._project_pop", "_ExecutionState.update"}:
            return "assignment_or_overlay"
        if name in {"_NameCursor.fork", "_NameVersion.fork", "_ExecutionState.copy"}:
            return "fork"
        if name in {"_name_lookup_layers", "_ExecutionState.get",
                    "_ExecutionState.__getitem__", "_ExecutionState.__contains__",
                    "_NameVersion.get", "_NameCursor.get", "_NameCursor._entry",
                    "_NameVersion._entry"}:
            fallback = "lookup"
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
        "stage_units": dict(entry["stage_units"]), "events": dict(entry["events"]),
        "creation_stack": entry["creation_stack"],
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
    local = frame.f_locals
    for field in ("relative_path", "item_id", "stable_id", "source_path", "marker", "name"):
        supplied = local.get(field)
        if type(supplied) is str:
            value[field] = supplied
    for field in ("depth", "closure_depth", "child_depth", "helper_depth",
                  "generator_depth", "index"):
        supplied = local.get(field)
        if type(supplied) is int:
            value[field] = supplied
    for field in ("compatible", "record", "enabled"):
        supplied = local.get(field)
        if type(supplied) is bool:
            value[field] = supplied
    for field in ("node", "definition", "method", "function", "statement", "expression"):
        supplied = local.get(field)
        if isinstance(supplied, ast.AST):
            description = {"kind": type(supplied).__name__}
            line = getattr(supplied, "lineno", None)
            if type(line) is int:
                description["line"] = line
            name = getattr(supplied, "name", None)
            if type(name) is str:
                description["name"] = name
            if isinstance(supplied, ast.Call):
                target = supplied.func
                if isinstance(target, ast.Name):
                    description["callee_name"] = target.id
                elif isinstance(target, ast.Attribute):
                    description["callee_attribute"] = target.attr
            value["ast_" + field] = description
    owner = local.get("self")
    if type(owner) is generator._SourceOrderedResolver:
        attributes = vars(owner)
        for field in ("_evaluation_depth",):
            supplied = attributes.get(field)
            if type(supplied) is int:
                value[field] = supplied
        # Exact builtin collection length only; no production Mapping/cursor API.
        for field in ("active_helper_effects", "_active_deferred_generator_probes",
                      "_active_deferred_local_generators", "_active_local_helper_returns"):
            supplied = attributes.get(field)
            if type(supplied) in (set, frozenset):
                value[field + "_count"] = len(supplied)
    for field in ("values", "environment", "current", "result", "class_values"):
        supplied = local.get(field)
        if type(supplied) is generator._ExecutionState:
            # Failure can interrupt copy() before authority is installed.
            attributes = vars(supplied)
            if "authority" not in attributes:
                value[field + "_authority_status"] = "missing"
                continue
            authority = attributes["authority"]
            if type(authority) is not generator._AuthorityState:
                value[field + "_authority_status"] = "unexpected-type"
                continue
            authority_attributes = vars(authority)
            if "enabled" not in authority_attributes:
                value[field + "_authority_status"] = "enabled-missing"
                continue
            enabled = authority_attributes["enabled"]
            if type(enabled) is not bool:
                value[field + "_authority_status"] = "enabled-not-bool"
                continue
            value[field + "_authority_status"] = "present"
            value[field + "_authority_enabled"] = enabled
    return value


def stack_info(frame):
    result = []
    while frame is not None:
        result.append(frame_info(frame))
        frame = frame.f_back
    return result


def exception_stack(error):
    result = []
    traceback = error.__traceback__
    while traceback is not None:
        row = frame_info(traceback.tb_frame)
        row["exception_line"] = traceback.tb_lineno
        result.append(row)
        traceback = traceback.tb_next
    return result


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
    entry["stage_units"][" > ".join(stage_stack) or "<none>"] += units
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
        assert entry["initial_work"] + sum(entry["units"].values()) == self.work_units
        assert sum(entry["phases"].values()) == sum(entry["units"].values())
        assert sum(entry["stage_units"].values()) == sum(entry["units"].values())
        if failure_count == 1:
            stack = []
            current = frame
            while current is not None:
                stack.append(frame_info(current))
                current = current.f_back
            print(json.dumps({
                "depth_budget_failure": {
                    "case": CASE,
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



def install(owner, name, replacement):
    original = getattr(owner, name)
    patches.append((owner, name, original, original.__code__))
    setattr(owner, name, replacement)


def counted(owner, name, budget_from_args, label):
    original = getattr(owner, name)
    def wrapped(*args, **keywords):
        budget = budget_from_args(args, keywords)
        entry = records_by_id[id(budget)]
        entry["events"][label + "/calls"] += 1
        try:
            result = original(*args, **keywords)
            entry["events"][label + "/completed"] += 1
            if label == "publication_commit":
                plan = args[1]
                if plan.changed:
                    entry["events"]["changed_publications_committed"] += 1
                    if plan.compacted:
                        entry["events"]["compacted_publications_committed"] += 1
            return result
        finally:
            entry["events"][label + "/exits"] += 1
    install(owner, name, wrapped)


def stage_scope(name):
    original = getattr(generator, name)
    def wrapped(*args, **keywords):
        point = name
        node = args[0] if args else keywords.get("method", keywords.get("definition"))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            point += "/" + node.name + ":" + str(node.lineno)
        pipeline_events[point + "/calls"] += 1
        stage_stack.append(point)
        try:
            result = original(*args, **keywords)
            pipeline_events[point + "/completed"] += 1
            return result
        finally:
            stage_stack.pop()
    install(generator, name, wrapped)


def install_hooks():
    install(generator._AnalysisBudget, "__init__", observed_init)
    install(generator._AnalysisBudget, "consume", observed_consume)
    counted(generator._ExecutionState, "__init__",
            lambda args, keywords: keywords["budget"] if "budget" in keywords else args[2],
            "execution_constructor")
    counted(generator._SourceOrderedResolver, "_merge_states",
            lambda args, keywords: args[0].budget, "state_merge")
    for name, label in (
        ("_name_ordered_items", "ordered_items"), ("_name_keys", "ordered_keys"),
        ("_name_prepare_publication", "publication_preparation"),
        ("_name_commit_publication", "publication_commit")):
        counted(generator, name, lambda args, keywords: args[0]._meter.budget, label)
    for name, label in (("_name_compact", "compaction"), ("_name_seal_layer", "layer_sealing"),
                        ("_join_name_versions", "version_join")):
        counted(generator, name, lambda args, keywords: args[0].budget, label)
    for name in ("snapshot", "fork"):
        counted(generator._NameCursor, name,
                lambda args, keywords: args[0]._meter.budget, "cursor_" + name)
    for name in ("_unittest_entry_preflight", "_unittest_receiver_attributes",
                 "_review_body", "_source_ordered_helper_return"):
        stage_scope(name)

def helper1050_source():
    helper_lines = ['import subprocess', 'import sys', 'import unittest', '']
    for index in range(1050):
        helper_lines.append(f'def helper_{index}():')
        if index == 1049:
            helper_lines.extend(('    subprocess.run(', "        [sys.executable, '-m', 'deep-helper'],", '        timeout=5,', '        check=False,', '    )'))
        else:
            helper_lines.append(f'    return helper_{index + 1}()')
        helper_lines.append('')
    helper_lines.extend(('class ReviewTests(unittest.TestCase):', '    def test_static(self):', '        helper_0()', '    def test_denied(self): pass'))
    return '\n'.join(helper_lines).encode('utf-8') + b'\n'

def generator70_source():

    def chained_source(depth: int) -> str:
        lines = ['g0 = (cp.arange(1) for _ in range(1))']
        lines.extend((f'g{index} = (sum(g{index - 1}) for _ in range(1))' for index in range(1, depth)))
        lines.append(f'sum(g{depth - 1})')
        return '\n'.join(lines)
    deep_source = f"import cupy as cp\nimport unittest\nclass ReviewTests(unittest.TestCase):\n    def test_static(self):\n{textwrap.indent(chained_source(70), '        ')}\n    def test_denied(self): pass\n"
    return fixtures._source(deep_source)


fixture = helper1050_source() if CASE == "helper1050" else generator70_source()
assert type(fixture) is bytes
print(json.dumps({
    "depth_budget_scope": {
        "case": CASE, "source_sha256": GENERATOR_SHA, "tests_sha256": TEST_SHA,
        "fixture_sha256": hashlib.sha256(fixture).hexdigest(), "fixture_bytes": len(fixture),
        "review_envelope": "Original DesignReviewTests._review default child source, inventory and item universe",
        "original_expectation": ("analysis.*(?:depth|budget)" if CASE == "helper1050"
                                 else "^analysis deferred generator depth exceeds 64$"),
        "case_construction": "Original frozen construction statements only; generated sensitive source is never executed",
        "phase_definition": phase_of.__doc__,
        "diagnostic_only": True,
    }}, sort_keys=True), flush=True)
review = None
refusal = None
install_hooks()
try:
    review = case._review(sources={"tests/test_review.py": fixture})
except generator.InventoryError as error:
    refusal = str(error)
    print(json.dumps({"depth_budget_refusal": {
        "case": CASE, "reason": refusal, "budget_failures": failure_count,
        "failing_epoch": failure_epoch, "stack": exception_stack(error),
        "diagnostic_only": True,
    }}, sort_keys=True), flush=True)
finally:
    for owner, name, original, code in reversed(patches):
        assert original.__code__ is code
        setattr(owner, name, original)
    assert all(getattr(owner, name) is original and original.__code__ is code
               for owner, name, original, code in patches)
    assert original_init.__code__ is init_code
    assert original_consume.__code__ is consume_code
    assert generator._NameMeter.charge.__code__ is name_meter_code
    assert {name: getattr(generator, name) for name in caps} == caps
    assert not stage_stack
    assert hashlib.sha256(generator_path.read_bytes()).hexdigest() == GENERATOR_SHA
    assert hashlib.sha256(test_path.read_bytes()).hexdigest() == TEST_SHA
for record in records:
    assert record["initial_work"] + sum(record["units"].values()) == record["after"]
    assert sum(record["phases"].values()) == sum(record["units"].values())
    assert sum(record["stage_units"].values()) == sum(record["units"].values())
    assert sum(record["name_kinds"].values()) <= sum(record["units"].values())
print(json.dumps({
    "depth_budget_diagnostic_complete": {
        "case": CASE, "completed": True, "diagnostic_only": True,
        "source_sha256": GENERATOR_SHA, "tests_sha256": TEST_SHA,
        "fixture_sha256": hashlib.sha256(fixture).hexdigest(),
        "budget_failures": failure_count, "failing_epoch": failure_epoch,
        "original_budget_count": len(records),
        "all_original_budgets": [summary(record) for record in records],
        "pipeline_events": dict(pipeline_events),
        "original_methods_restored": all(getattr(owner, name) is original
                                        for owner, name, original, _code in patches),
        "caps_unchanged": {name: getattr(generator, name) for name in caps} == caps,
        "caps": caps, "review_returned": review is not None, "refusal": refusal,
        "requested_units_accounted": True,
        "scope": "Only the selected existing fixture; no bounded32, other tests, matrix, corpus or dev slot",
    }}, sort_keys=True), flush=True)
raise SystemExit(0)
