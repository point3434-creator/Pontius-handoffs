"""One exact helper1050/helper65/generator70 source; scalar-only radix diagnosis, no sensitive execution."""
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
parser.add_argument("--case", required=True, choices=("helper1050", "helper65", "generator70"))
CASE = parser.parse_args().case
ROOT = Path.cwd()
GENERATOR_SHA = "1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951"
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
CASE_METHODS = {'helper1050': 'test_analysis_budgets_contain_deep_helpers_and_invalid_ranges', 'helper65': 'test_round4_analysis_budget_red_contracts_are_independent', 'generator70': 'test_round4_source_order_and_branch_bounds_red_contracts_are_independent'}
EXPECTATIONS = {'helper1050': 'analysis.*(?:depth|budget)', 'helper65': '^analysis helper depth exceeds 64$', 'generator70': '^analysis deferred generator depth exceeds 64$'}
FIXTURE_SHAS = {'helper1050': '148ffd41c2a5d5616a4b8d1cf8bc297f488ae8f6ddc1109d1d2842afa9183754', 'helper65': '94b070b8fcf2e66c42e1a779558e830d7caae670366f9313faf0989c722818c6', 'generator70': '635e682b2253cd44201e2afdb95c288b9973f5629ec4eeb3c5bfd078743eb5e3'}
case = fixtures.DesignReviewTests(CASE_METHODS[CASE])
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
        "publication_costs": {}, "bulk_shapes": collections.Counter(),
        "full_join_sharing": collections.Counter(),
    }
    records_by_id[id(self)] = entry
    records.append(entry)


def key(frame):
    return (frame.f_code.co_qualname + ":" + str(frame.f_lineno)
            if frame is not None else "<root>")


def phase_of(frame):
    """Disjoint nearest original component; name kinds and pipeline stages are separate views."""
    current = frame
    while current is not None:
        name = current.f_code.co_qualname
        if name == "_name_radix_copy_leaf":
            return "radix_leaf_copy"
        if name in {"_name_radix_freeze", "_name_radix_seal_leaf"}:
            return "radix_freeze"
        if name in {"_name_radix_edit", "_name_radix_edit_records", "_name_radix_records", "_name_radix_group"}:
            return "radix_edit"
        if name == "_name_radix_bulk":
            return "radix_bulk"
        if name == "_name_radix_lookup":
            return "name_lookup"
        if name == "_transfer_authority":
            return "authority_transfer"
        if name == "_ExecutionState._transferred_name_entry":
            return "entry_transfer_or_certificate"
        if name == "_ExecutionState._write_cells":
            return "cell_write"
        if name.startswith("_AuthorityMap.") or name.startswith("_ObservedAuthorityMap."):
            return "authority_map"
        if name == "_AuthorityState.fork":
            return "authority_fork"
        if name == "_AuthorityState.join":
            return "authority_join"
        if name in {"_name_realize_order", "_name_ordered_items", "_name_keys",
                    "_ExecutionState.items", "_ExecutionState.keys", "_ExecutionState.values"}:
            return "ordering"
        if name in {"_name_prepare_publication", "_name_charge_publication_commit", "_name_commit_publication"}:
            return "publication"
        if name == "_NameVersion.from_unique_entries":
            parent = current.f_back
            context = parent.f_code.co_qualname if parent is not None else ""
            return ("bulk_constructor_preparation" if context == "_ExecutionState.__init__"
                    else "bulk_full_join_preparation" if context == "_SourceOrderedResolver._merge_states"
                    else "bulk_other_preparation")
        if name == "_NameCursor.snapshot":
            return "snapshot"
        if name in {"_NameCursor.fork", "_NameVersion.fork", "_ExecutionState.copy"}:
            return "fork"
        if name == "_join_name_versions":
            return "version_join"
        if name == "_ExecutionState.__init__":
            return "constructor"
        if name in {"_NameCursor._replace_entry", "_ExecutionState.__setitem__",
                    "_ExecutionState._project", "_ExecutionState.__delitem__",
                    "_ExecutionState._project_pop", "_ExecutionState.update"}:
            return "assignment_or_overlay"
        if name == "_SourceOrderedResolver._merge_states":
            return "state_join"
        if name.startswith("_SourceOrderedResolver."):
            return "other"
        current = current.f_back
    return "other"


def raw_name_count(value):
    """Exact builtin/private scalars only; never public mapping access."""
    if type(value) is dict:
        return len(value)
    if type(value) is generator._ExecutionState:
        names = vars(value).get("_names")
        if type(names) is generator._NameCursor:
            size = object.__getattribute__(names, "_size")
            return size if type(size) is int else None
    if type(value) is generator._NameVersion:
        size = object.__getattribute__(value, "_size")
        return size if type(size) is int else None
    return None


def raw_full_join_sharing(local):
    """Ephemeral raw reads; the returned signature contains only bool/int tuples."""
    inputs, states = local.get("name_inputs"), local.get("states")
    versions = inputs if type(inputs) is tuple else ()
    sources = states if type(states) in (list, tuple) else ()
    exact_versions = bool(versions) and all(
        type(value) is generator._NameVersion for value in versions)
    exact_sources = bool(sources) and len(sources) == len(versions) and all(
        type(value) is generator._ExecutionState for value in sources)
    meter, resolver = local.get("meter"), local.get("self")
    exact_meter = type(meter) is generator._NameMeter
    budget = (vars(resolver).get("budget")
              if type(resolver) is generator._SourceOrderedResolver else None)
    same_roots = exact_versions and all(
        object.__getattribute__(value, "_root")
        is object.__getattribute__(versions[0], "_root") for value in versions)
    same_meter = exact_versions and exact_sources and exact_meter and all(
        object.__getattribute__(value, "_meter") is meter for value in versions)
    same_budget = exact_sources and exact_meter and budget is not None and (
        object.__getattribute__(meter, "budget") is budget)
    disabled = exact_sources
    for source in sources:
        if type(source) is not generator._ExecutionState:
            disabled = same_meter = same_budget = False
            continue
        authority, cursor = vars(source).get("authority"), vars(source).get("_names")
        if type(authority) is generator._AuthorityState:
            disabled = disabled and vars(authority).get("enabled") is False
            same_budget = same_budget and vars(authority).get("budget") is budget
        else:
            disabled = same_budget = False
        same_meter = same_meter and type(cursor) is generator._NameCursor and (
            object.__getattribute__(cursor, "_meter") is meter)
    pending_rows = []
    for version in versions:
        size, pending, known = -1, -1, False
        if type(version) is generator._NameVersion:
            size = object.__getattribute__(version, "_size")
            size = size if type(size) is int and size >= 0 else -1
            root = object.__getattribute__(version, "_root")
            if root is None:
                pending, known = 0, True
            elif type(root) is generator._NameRadixLeaf:
                raw = object.__getattribute__(root, "pending")
                if type(raw) is tuple:
                    pending, known = len(raw), True
            elif type(root) is generator._NameRadixBranch:
                raw = object.__getattribute__(root, "pending_count")
                if type(raw) is int and raw >= 0:
                    pending, known = raw, True
        pending_rows.append((size, pending, known, known and size >= 0 and pending == size))
    all_pending = exact_versions and all(row[3] for row in pending_rows)
    return (len(versions), len(sources), exact_versions, exact_sources, same_roots,
            disabled, same_meter, same_budget, tuple(pending_rows), all_pending,
            exact_versions and exact_sources and same_roots and disabled
            and same_meter and same_budget and all_pending)


def record_bulk_shape(entry, frame):
    if frame is None:
        return
    name, local = frame.f_code.co_qualname, frame.f_locals
    if name == "_ExecutionState.__init__":
        shape = ("constructor", raw_name_count(local.get("values")),
                 raw_name_count(local.get("parent")), ())
    elif name == "_SourceOrderedResolver._merge_states":
        inputs, names = local.get("name_inputs"), local.get("names")
        counts = tuple(raw_name_count(item) for item in inputs) if type(inputs) is tuple else ()
        shape = ("full_join", len(names) if type(names) is set else None, None, counts)
        entry["full_join_sharing"][raw_full_join_sharing(local)] += 1
    else:
        shape = ("other", None, None, ())
    entry["bulk_shapes"][shape] += 1


def sorted_rows(counter, labels):
    return [dict(zip(labels, item if isinstance(item, tuple) else (item,)), units=units)
            for item, units in counter.most_common()]


def summary(entry, detailed=False):
    value = {
        "epoch": entry["epoch"], "initial_work": entry["initial_work"],
        "work_after": entry["after"], "counted_units": sum(entry["units"].values()),
        "phase_units": dict(entry["phases"]), "name_kind_units": dict(entry["name_kinds"]),
        "stage_units": dict(entry["stage_units"]), "events": dict(entry["events"]),
        "component_units": dict(entry["phases"]),
        "publication_preparation_costs": [
            dict(zip(("tail_entries", "base_names", "dirty", "completed"), signature), **amounts)
            for signature, amounts in sorted(entry["publication_costs"].items())
        ],
        "bulk_input_shapes": [
            {"kind": shape[0], "source_or_unique_names": shape[1], "parent_names": shape[2],
             "input_names": list(shape[3]), "attempts": count}
            for shape, count in entry["bulk_shapes"].items()
        ],
        "full_join_sharing_facts": [
            {"input_count": facts[0], "source_count": facts[1],
             "exact_name_version_inputs": facts[2], "exact_execution_state_sources": facts[3],
             "published_roots_same_by_identity": facts[4],
             "all_source_authorities_disabled": facts[5],
             "same_meter": facts[6], "same_budget": facts[7],
             "per_root_pending": [
                 {"size": row[0], "pending_count": row[1], "pending_count_known": row[2],
                  "all_pending": row[3]} for row in facts[8]],
             "all_roots_pending": facts[9], "restricted_C_guard_facts": facts[10],
             "attempts": count}
            for facts, count in entry["full_join_sharing"].items()
        ],
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
        if kind in {"bulk_input_iterator_requests", "bulk_return_reference"}:
            origin = third.f_code.co_qualname if third is not None else "<root>"
            entry["events"][kind + "/" + origin + "/charge_attempts"] += 1
            if kind == "bulk_input_iterator_requests":
                record_bulk_shape(entry, third)
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
            if label == "publication_commit" and args[1].changed:
                entry["events"]["changed_publications_committed"] += 1
            return result
        finally:
            entry["events"][label + "/exits"] += 1
    install(owner, name, wrapped)


def publication_preparation():
    original = generator._name_prepare_publication
    def wrapped(cursor):
        meter = object.__getattribute__(cursor, "_meter")
        budget = meter.budget
        entry = records_by_id[id(budget)]
        tail = object.__getattribute__(cursor, "_tail")
        base = object.__getattribute__(cursor, "_base")
        assert type(tail) is dict and type(base) is generator._NameVersion
        tail_size = len(tail)
        base_size = object.__getattribute__(base, "_size")
        assert type(base_size) is int
        dirty = bool(tail) or object.__getattribute__(cursor, "_order") is not object.__getattribute__(base, "_order")
        before = budget.work_units
        completed = False
        entry["events"]["publication_preparation/calls"] += 1
        try:
            answer = original(cursor)
            assert type(answer.changed) is bool and answer.changed == dirty
            completed = True
            entry["events"]["publication_preparation/completed"] += 1
            return answer
        finally:
            used = budget.work_units - before
            signature = (tail_size, base_size, dirty, completed)
            totals = entry["publication_costs"].setdefault(signature,
                {"calls": 0, "units": 0, "minimum_units": used, "maximum_units": used})
            totals["calls"] += 1
            totals["units"] += used
            totals["minimum_units"] = min(totals["minimum_units"], used)
            totals["maximum_units"] = max(totals["maximum_units"], used)
            entry["events"]["publication_preparation/exits"] += 1
    install(generator, "_name_prepare_publication", wrapped)


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
    counted(generator._ExecutionState, "copy",
            lambda args, keywords: args[0].authority.budget, "execution_copy")
    counted(generator._AuthorityState, "fork",
            lambda args, keywords: args[0].budget, "authority_fork")
    counted(generator._SourceOrderedResolver, "_merge_states",
            lambda args, keywords: args[0].budget, "state_merge")
    for name, label in (
        ("_name_ordered_items", "ordered_items"), ("_name_keys", "ordered_keys"),
        ("_name_commit_publication", "publication_commit")):
        counted(generator, name, lambda args, keywords: args[0]._meter.budget, label)
    publication_preparation()
    counted(generator, "_join_name_versions",
            lambda args, keywords: args[0].budget, "version_join")
    counted(generator, "_transfer_authority",
            lambda args, keywords: args[1].authority.budget, "authority_transfer")
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

def helper65_source():
    helper_lines = ['import subprocess', 'import sys', 'import unittest', '']
    for index in range(65):
        helper_lines.append(f'def helper_{index}():')
        if index == 64:
            helper_lines.extend(('    subprocess.run(', "        [sys.executable, '-m', 'deep-helper'],", '        timeout=5, check=False,', '    )'))
        else:
            helper_lines.append(f'    return helper_{index + 1}()')
        helper_lines.append('')
    helper_lines.extend(('class ReviewTests(unittest.TestCase):', '    def test_static(self): helper_0()', '    def test_denied(self): pass'))
    return '\n'.join(helper_lines).encode('utf-8') + b'\n'

def generator70_source():

    def chained_source(depth: int) -> str:
        lines = ['g0 = (cp.arange(1) for _ in range(1))']
        lines.extend((f'g{index} = (sum(g{index - 1}) for _ in range(1))' for index in range(1, depth)))
        lines.append(f'sum(g{depth - 1})')
        return '\n'.join(lines)
    deep_source = f"import cupy as cp\nimport unittest\nclass ReviewTests(unittest.TestCase):\n    def test_static(self):\n{textwrap.indent(chained_source(70), '        ')}\n    def test_denied(self): pass\n"
    return fixtures._source(deep_source)


fixture = {"helper1050": helper1050_source, "helper65": helper65_source,
           "generator70": generator70_source}[CASE]()
assert type(fixture) is bytes
assert hashlib.sha256(fixture).hexdigest() == FIXTURE_SHAS[CASE]
print(json.dumps({
    "depth_budget_scope": {
        "case": CASE, "source_sha256": GENERATOR_SHA, "tests_sha256": TEST_SHA,
        "fixture_sha256": hashlib.sha256(fixture).hexdigest(), "fixture_bytes": len(fixture),
        "review_envelope": "Original DesignReviewTests._review default child source, inventory and item universe",
        "original_expectation": EXPECTATIONS[CASE],
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
        "original_expectation": EXPECTATIONS[CASE],
        "diagnostic_population": list(CASE_METHODS),
        "budget_failures": failure_count, "failing_epoch": failure_epoch,
        "original_budget_count": len(records),
        "all_original_budgets": [summary(record) for record in records],
        "pipeline_events": dict(pipeline_events),
        "original_methods_restored": all(getattr(owner, name) is original
                                        for owner, name, original, _code in patches),
        "caps_unchanged": {name: getattr(generator, name) for name in caps} == caps,
        "caps": caps, "review_returned": review is not None, "refusal": refusal,
        "requested_units_accounted": True,
        "scope": "Only selected helper1050/helper65/generator70 original fixture; no bounded32, other tests, matrix, corpus or dev slot",
        "accounting_note": "component_units/phase_units alias one disjoint partition; NameMeter kinds and stages are separate views. Preparation deltas include nested radix work and failed requests, not extra work. Final completion contains post-unwind failure costs; commit completion is separate. Bulk events/shapes are attempts, not completed-build claims.",
    }}, sort_keys=True), flush=True)
raise SystemExit(0)
