"""Static authoring only for approved v30 generator70 diagnostic; never dispatch payload."""
from pathlib import Path
import ast
import difflib
import hashlib
import json
import subprocess

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
PINS = {
 "engineer-generator-v30-storage.py": "1a28fce14cfdd2ee30d9892b7d2719aba8ec152d99d1e3c915660648cf9756fd",
 "engineer-depth-budget-probe-v4.py": "559b099f96a4fcfb9b88eb05338a45ad2184ca5e153a360ee0123e0ee7969379",
 "tests-depth-budget-control-v4.py": "d62807554ffd50b7552879c5a7eb8b4b940e729063ab041d36ee9e79b823c8a5",
 "engineer-v30-generator70-diagnostic-plan-v1.md": "51bbcd9bceab7f68dd6c7778dd584111e5e69e9a772fd85ecb614872eefdc3b9",
 "tests-checks/focused-v2-v30-first01-design-311-receipt.json": "ae46f1f92f9f7de5e554f5cc1f51694a4bd69d6856acce12e099389319a6391d",
}
OLD_SOURCE = "1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951"
NEW_SOURCE = PINS["engineer-generator-v30-storage.py"]
ORIGINAL_TEST_SHA = "c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf"
WATCH_SHA = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
for relative, expected in PINS.items():
    assert digest((T / relative).read_bytes()) == expected, relative
raw_probe = (T / "engineer-depth-budget-probe-v4.py").read_bytes()
raw_control = (T / "tests-depth-budget-control-v4.py").read_bytes()
raw_candidate = (T / "engineer-generator-v30-storage.py").read_bytes()

HOOKS = r'''
def merge_snapshot(context):
    """Copy observer-owned scalar containers; never inspect a production object."""
    def checked(value):
        if value is None or type(value) in (bool, int, str):
            return value
        if type(value) is tuple:
            return tuple(checked(item) for item in value)
        if type(value) is list:
            return [checked(item) for item in value]
        if type(value) in (dict, collections.Counter):
            assert all(type(key) is str for key in value)
            return {key: checked(item) for key, item in value.items()}
        raise AssertionError("non-scalar merge observation")
    return checked(context)


def merge_local_decisions(context, frame):
    """Read decisions already computed in original locals; do not repeat a guard."""
    local = frame.f_locals
    for name in ("stable_sources", "exact_first", "disabled_join", "compatible"):
        value = local.get(name)
        if type(value) is bool:
            context["decisions"][name] = value
    if "base" in local:
        context["decisions"]["common_history_result_known"] = True
        context["decisions"]["common_history_present"] = local["base"] is not None
    for name, output, expected in (
            ("candidate_names", "candidate_names", dict),
            ("names", "union_names", set)):
        value = local.get(name)
        if type(value) is expected:
            context["decisions"][output] = len(value)
    index = local.get("index")
    if type(index) is int:
        context["decisions"]["last_input_index"] = index
    # Snapshot sizes are descriptive only; they do not assert shared entries.
    inputs = local.get("name_inputs")
    if type(inputs) is tuple:
        context["input_name_counts"] = tuple(raw_name_count(value) for value in inputs)


def merge_observe_charge(entry, frame, parent, third, kind, units, phase):
    """Observe existing call positions before delegation; no checkpoint is a commit."""
    if not merge_stack or merge_stack[-1]["epoch"] != entry["epoch"]:
        return None
    context = merge_stack[-1]
    context["exclusive_requested_units"] += units
    context["component_units"][phase] += units
    if kind is not None:
        context["name_kind_units"][kind] += units
    label = None
    original_frame = None
    if frame.f_code is merge_code and frame.f_lineno == BRANCH_REACH_LINE:
        label = "disabled_branch_reached"
        original_frame = frame
        context["branch_reached"] = True
    elif kind is not None and kind.startswith("disabled_join_"):
        label = kind
        current = parent
        while current is not None:
            if current.f_code is merge_code:
                original_frame = current
                break
            current = current.f_back
        if kind == "disabled_join_guard_function_allocation":
            context["guard_scope_reached"] = True
        if kind == "disabled_join_input_iterator_allocations":
            context["result_guard_passed"] = True
        if kind == "disabled_join_common_history_checks":
            context["all_input_guards_passed"] = True
        if kind == "disabled_join_order_dictionary_allocation":
            context["selected_body_reached"] = True
        if parent is not None and parent.f_code.co_qualname == (
                "_SourceOrderedResolver._merge_states.<locals>.disabled_input"):
            context["last_guard_checkpoint"] = kind
            pending = parent.f_locals.get("pending")
            if type(pending) is int:
                context["decisions"]["last_computed_pending_count"] = pending
    elif (kind is not None and parent is not None
          and parent.f_code is common_history_code
          and third is not None and third.f_code is merge_code):
        label = "common_history_call/" + kind
        original_frame = third
        # The original if disabled_join already selected this call.
        context["all_input_guards_passed"] = True
    elif (kind == "bulk_input_iterator_requests" and third is not None
          and third.f_code is merge_code):
        label = "legacy_full_build_reached"
        original_frame = third
        context["fallback_reached"] = True
    elif kind == "adapter_merge_values_generator_allocation":
        label = "per_name_normalization_preparation"
    if label is None:
        return None
    context["checkpoint_attempts"][label] += 1
    context["last_checkpoint_attempt"] = label
    if original_frame is not None and label in {
            "disabled_branch_reached", "disabled_join_guard_function_allocation",
            "disabled_join_input_iterator_allocations", "disabled_join_input_pair_allocation",
            "disabled_join_common_history_checks", "disabled_join_cardinality_choice",
            "disabled_join_order_dictionary_allocation", "disabled_join_result_install_reference",
            "legacy_full_build_reached"}:
        merge_local_decisions(context, original_frame)
    if label == "legacy_full_build_reached":
        facts = context["decisions"]
        if facts.get("stable_sources") is False or facts.get("exact_first") is False:
            reason = "computed_preliminary_guard_false"
        elif not context["guard_scope_reached"]:
            reason = "preliminary_meter_or_budget_guard_not_entered"
        elif facts.get("disabled_join") is False:
            reason = "computed_result_or_input_guard_false"
        elif (facts.get("common_history_result_known") is True
              and facts.get("common_history_present") is False):
            reason = "computed_common_history_absent"
        elif (type(facts.get("candidate_names")) is int
              and type(facts.get("union_names")) is int
              and facts["candidate_names"] >= facts["union_names"]):
            reason = "computed_candidate_set_not_sparse"
        else:
            reason = "unknown"
        context["fallback_reason"] = reason
    return label


def merge_observe_success(entry, label):
    """Original consume returned; only its charge, not the following action, completed."""
    if label is None:
        return
    assert merge_stack and merge_stack[-1]["epoch"] == entry["epoch"]
    context = merge_stack[-1]
    context["checkpoint_charge_successes"][label] += 1
    context["last_checkpoint_charge_success"] = label
    if label == "disabled_join_result_install_reference":
        context["install_charge_succeeded"] = True


def merge_operation_event(entry, event):
    if merge_stack and merge_stack[-1]["epoch"] == entry["epoch"]:
        merge_stack[-1]["operation_events"][event] += 1


def merge_scope():
    original = generator._SourceOrderedResolver._merge_states
    assert original.__code__ is merge_code
    def wrapped(*args, **keywords):
        budget = args[0].budget
        entry = records_by_id[id(budget)]
        entry["events"]["state_merge/calls"] += 1
        context = {
            "epoch": entry["epoch"], "ordinal": entry["events"]["state_merge/calls"],
            "work_before": budget.work_units, "work_after": None,
            "inclusive_requested_units": None, "exclusive_requested_units": 0,
            "component_units": collections.Counter(), "name_kind_units": collections.Counter(),
            "checkpoint_attempts": collections.Counter(),
            "checkpoint_charge_successes": collections.Counter(),
            "operation_events": collections.Counter(), "decisions": {},
            "input_name_counts": (), "branch_reached": False,
            "guard_scope_reached": False, "result_guard_passed": False,
            "all_input_guards_passed": False, "selected_body_reached": False,
            "install_charge_succeeded": False, "fallback_reached": False,
            "fallback_reason": None, "last_guard_checkpoint": None,
            "last_checkpoint_attempt": None, "last_checkpoint_charge_success": None,
            "returned": False, "outcome": None,
        }
        merge_stack.append(context)
        try:
            answer = original(*args, **keywords)
            context["returned"] = True
            entry["events"]["state_merge/completed"] += 1
            return answer
        finally:
            assert merge_stack[-1] is context
            merge_stack.pop()
            context["work_after"] = budget.work_units
            context["inclusive_requested_units"] = budget.work_units - context["work_before"]
            assert sum(context["component_units"].values()) == context["exclusive_requested_units"]
            assert sum(context["name_kind_units"].values()) <= context["exclusive_requested_units"]
            assert context["inclusive_requested_units"] >= context["exclusive_requested_units"]
            if context["returned"] and context["install_charge_succeeded"]:
                context["outcome"] = "disabled_install_completed"
            elif context["returned"] and context["fallback_reached"]:
                context["outcome"] = "legacy_full_build_returned"
            elif context["returned"]:
                context["outcome"] = "other_merge_returned"
            else:
                # Even a selected body or a paid install charge is not completion.
                context["outcome"] = "interrupted_or_exception"
            entry["merge_calls"].append(merge_snapshot(context))
            entry["events"]["state_merge/exits"] += 1
    install(generator._SourceOrderedResolver, "_merge_states", wrapped)


def merge_summary(entry):
    rows = entry["merge_calls"]
    outcomes = collections.Counter()
    costs = {}
    for row in rows:
        outcomes[row["outcome"]] += 1
        label = row["outcome"]
        used = row["inclusive_requested_units"]
        item = costs.setdefault(label, {
            "calls": 0, "inclusive_units": 0, "minimum_units": used, "maximum_units": used})
        item["calls"] += 1
        item["inclusive_units"] += used
        item["minimum_units"] = min(item["minimum_units"], used)
        item["maximum_units"] = max(item["maximum_units"], used)
    return {
        "completed_wrapper_exits": len(rows), "outcomes": dict(outcomes),
        "inclusive_costs_by_outcome": costs, "calls": rows,
        "active_calls": [merge_snapshot(row) for row in merge_stack if row["epoch"] == entry["epoch"]],
        "meaning": "Flags describe reached original sites. Charge success is not action success; only original merge return after the install charge proves completed installation. Inclusive costs overlap nested calls and publication costs.",
    }

'''

def apply(text, old, new, edits):
    assert text.count(old) == 1, old[:150]
    edits.append((old, new))
    return text.replace(old, new, 1)

probe_edits, control_edits = [], []
p = raw_probe.decode("utf-8")
assert "\r" not in p
old_doc = '"""One exact helper1050/helper65/generator70 source; scalar-only radix diagnosis, no sensitive execution."""'
p = apply(p, old_doc, '"""One original generator70 case on frozen v30; scalar-only branch/cost diagnosis."""', probe_edits)
p = apply(p, 'choices=("helper1050", "helper65", "generator70")', 'choices=("generator70",)', probe_edits)
p = apply(p, 'GENERATOR_SHA = "' + OLD_SOURCE + '"', 'GENERATOR_SHA = "' + NEW_SOURCE + '"', probe_edits)
p = apply(p, 'pipeline_events = collections.Counter()\n', 'pipeline_events = collections.Counter()\nmerge_stack = []\nmerge_code = generator._SourceOrderedResolver._merge_states.__code__\ncommon_history_code = generator._name_common_history.__code__\nBRANCH_REACH_LINE = 22418  # Exact pinned v30 AST statement, verified at authoring.\n', probe_edits)
p = apply(p, '        "full_join_sharing": collections.Counter(),\n', '        "full_join_sharing": collections.Counter(),\n        "merge_calls": [],\n', probe_edits)
p = apply(p, '\ndef sorted_rows(counter, labels):\n', HOOKS + '\ndef sorted_rows(counter, labels):\n', probe_edits)
p = apply(p, '        "creation_stack": entry["creation_stack"],\n', '        "creation_stack": entry["creation_stack"],\n        "merge_observations": merge_summary(entry),\n', probe_edits)
p = apply(p, '    if frame.f_code is name_meter_code:\n', '    kind = None\n    if frame.f_code is name_meter_code:\n', probe_edits)
p = apply(p, '    try:\n        answer = original_consume(self, units)\n', '    checkpoint = merge_observe_charge(entry, frame, parent, third, kind, units, phase)\n    try:\n        answer = original_consume(self, units)\n', probe_edits)
p = apply(p, '        assert self.work_units == before + units\n        return answer\n', '        assert self.work_units == before + units\n        merge_observe_success(entry, checkpoint)\n        return answer\n', probe_edits)
p = apply(p, '        entry["events"][label + "/calls"] += 1\n        try:\n', '        entry["events"][label + "/calls"] += 1\n        merge_operation_event(entry, label + "/calls")\n        try:\n', probe_edits)
p = apply(p, '            entry["events"][label + "/completed"] += 1\n', '            entry["events"][label + "/completed"] += 1\n            merge_operation_event(entry, label + "/completed")\n', probe_edits)
p = apply(p, '            entry["events"][label + "/exits"] += 1\n', '            entry["events"][label + "/exits"] += 1\n            merge_operation_event(entry, label + "/exits")\n', probe_edits)
p = apply(p, '    counted(generator._SourceOrderedResolver, "_merge_states",\n            lambda args, keywords: args[0].budget, "state_merge")\n', '    merge_scope()\n', probe_edits)
p = apply(p, '    assert not stage_stack\n', '    assert not stage_stack\n    assert not merge_stack\n', probe_edits)
p = apply(p, '    assert sum(record["name_kinds"].values()) <= sum(record["units"].values())\n', '    assert sum(record["name_kinds"].values()) <= sum(record["units"].values())\n    assert len(record["merge_calls"]) == record["events"]["state_merge/exits"]\n    assert record["events"]["state_merge/calls"] == record["events"]["state_merge/exits"]\n    assert sum(row["returned"] for row in record["merge_calls"]) == record["events"]["state_merge/completed"]\n    assert sum(row["exclusive_requested_units"] for row in record["merge_calls"]) <= sum(record["units"].values())\n', probe_edits)
p = apply(p, '        "diagnostic_population": list(CASE_METHODS),\n', '        "diagnostic_population": [CASE],\n        "branch_observer_complete": True,\n', probe_edits)
p = apply(p, '"scope": "Only selected helper1050/helper65/generator70 original fixture; no bounded32, other tests, matrix, corpus or dev slot",', '"scope": "Only original generator70 fixture on v30; no helper1050/helper65/bounded32, other tests, matrix, corpus or dev slot",', probe_edits)
p = apply(p, 'Bulk events/shapes are attempts, not completed-build claims.",', 'Bulk events/shapes are attempts, not completed-build claims. Merge-exclusive components partition work inside the innermost same-budget merge; merge-inclusive deltas overlap nested calls and publication costs. Only an original return after the final install charge counts as completed disabled installation.",', probe_edits)
probe_raw = p.encode("utf-8")
probe_sha = digest(probe_raw)

c = raw_control.decode("utf-8")
assert "\r" not in c
c = apply(c, '"""Three-case v26 floor-only budget diagnostic control, for root review before use.', '"""One-case v30 generator70 floor-only diagnostic control, for root review before use.', control_edits)
c = apply(c, 'SOURCE_SHA = "' + OLD_SOURCE + '"', 'SOURCE_SHA = "' + NEW_SOURCE + '"', control_edits)
c = apply(c, 'PROBE_SHA = "' + PINS["engineer-depth-budget-probe-v4.py"] + '"', 'PROBE_SHA = "' + probe_sha + '"', control_edits)
c = apply(c, 'PROBE = ROOT / "engineer-depth-budget-probe-v4.py"', 'PROBE = ROOT / "engineer-depth-budget-probe-v5.py"', control_edits)
c = apply(c, 'CASES = ("helper1050", "helper65", "generator70")', 'CASES = ("generator70",)', control_edits)
c = apply(c, 'req(job["case"] in ("helper1050", "helper65", "generator70"), "bounded case")', 'req(job["case"] == "generator70", "bounded case")', control_edits)
c = apply(c, 'and completion.get("original_expectation") == EXPECTATIONS[case])', 'and completion.get("original_expectation") == EXPECTATIONS[case]\n                and completion.get("diagnostic_population") == ["generator70"]\n                and completion.get("branch_observer_complete") is True\n                and completion.get("requested_units_accounted") is True)', control_edits)
c = apply(c, '"fixed v26 candidate and reviewed probe required")', '"fixed v30 candidate and reviewed probe required")', control_edits)
control_raw = c.encode("utf-8")
control_sha = digest(control_raw)

# Static validation only: parse/compile source, never execute probe/control/candidate.
old_pt, pt = ast.parse(raw_probe), ast.parse(probe_raw)
old_ct, ct = ast.parse(raw_control), ast.parse(control_raw)
candidate_tree = ast.parse(raw_candidate)
for raw, filename in ((probe_raw, "engineer-depth-budget-probe-v5.py"),
                      (control_raw, "tests-depth-budget-control-v5.py")):
    compile(raw, filename, "exec")
def defs(tree):
    return {node.name: node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
old_defs, new_defs = defs(old_pt), defs(pt)
def body(node):
    return ast.dump(node, include_attributes=False)
for name in ("helper1050_source", "helper65_source", "generator70_source",
             "phase_of", "raw_name_count", "raw_full_join_sharing", "record_bulk_shape",
             "frame_info", "stack_info", "exception_stack", "install",
             "publication_preparation", "stage_scope"):
    assert body(old_defs[name]) == body(new_defs[name]), name

def inverse(text, edits):
    for old, new in reversed(edits):
        assert text.count(new) == 1, new[:150]
        text = text.replace(new, old, 1)
    return text.encode("utf-8")
assert inverse(p, probe_edits) == raw_probe
assert inverse(c, control_edits) == raw_control

observed = new_defs["observed_consume"]
original_calls = [node for node in ast.walk(observed) if isinstance(node, ast.Call)
                  and isinstance(node.func, ast.Name) and node.func.id == "original_consume"]
assert len(original_calls) == 1
assert body(original_calls[0]) == body(next(node for node in ast.walk(old_defs["observed_consume"])
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    and node.func.id == "original_consume"))
assert any(isinstance(node, ast.Raise) and node.exc is None for node in ast.walk(observed))
merge_wrapper = next(node for node in new_defs["merge_scope"].body if isinstance(node, ast.FunctionDef))
merge_calls = [node for node in ast.walk(merge_wrapper) if isinstance(node, ast.Call)
               and isinstance(node.func, ast.Name) and node.func.id == "original"]
assert len(merge_calls) == 1 and len(merge_calls[0].args) == 1
assert isinstance(merge_calls[0].args[0], ast.Starred)

sor = next(node for node in candidate_tree.body if isinstance(node, ast.ClassDef)
           and node.name == "_SourceOrderedResolver")
merge = next(node for node in sor.body if isinstance(node, ast.FunctionDef)
             and node.name == "_merge_states")
anchor = [node for node in ast.walk(merge) if isinstance(node, ast.Expr) and node.lineno == 22418]
assert len(anchor) == 1 and ast.unparse(anchor[0]) == "self.budget.consume()"
sites = {}
for node in ast.walk(merge):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "charge":
        if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            key = node.args[0].value
            if key.startswith("disabled_join_") or key.startswith("adapter_bulk"):
                sites.setdefault(key, []).append(node.lineno)
assert sites["disabled_join_result_install_reference"] == [22546]
assert sites["disabled_join_common_history_checks"] == [22479]
assert sites["disabled_join_cardinality_choice"] == [22501]
assert sites["disabled_join_order_dictionary_allocation"] == [22504]

def assignment(tree, name):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return node
    raise AssertionError(name)
assert ast.literal_eval(assignment(ct, "CASES").value) == ("generator70",)
assert ast.literal_eval(assignment(pt, "GENERATOR_SHA").value) == NEW_SOURCE
old_wrapper = ast.literal_eval(assignment(old_ct, "WRAPPER").value)
new_wrapper = ast.literal_eval(assignment(ct, "WRAPPER").value)
assert new_wrapper.replace('req(job["case"] == "generator70", "bounded case")',
                          'req(job["case"] in ("helper1050", "helper65", "generator70"), "bounded case")') == old_wrapper
compile(new_wrapper, "<v5-bootstrap>", "exec")
assert body(assignment(old_pt, "EXPECTATIONS")) == body(assignment(pt, "EXPECTATIONS"))
assert body(assignment(old_pt, "FIXTURE_SHAS")) == body(assignment(pt, "FIXTURE_SHAS"))
assert body(assignment(old_pt, "cap_names")) == body(assignment(pt, "cap_names"))
assert body(assignment(old_ct, "TIMEOUT")) == body(assignment(ct, "TIMEOUT"))
assert body(assignment(old_ct, "TEST_SHA")) == body(assignment(ct, "TEST_SHA"))
# Read the original test blob as data only. Match exact builder/envelope ASTs.
original_test = subprocess.check_output([
    r"C:\Program Files\Git\cmd\git.exe", "-C", r"D:\Pontius", "show",
    "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358:tests/test_inventory_and_profiles.py"],
    creationflags=subprocess.CREATE_NO_WINDOW)
assert digest(original_test) == ORIGINAL_TEST_SHA
test_tree = ast.parse(original_test)
test_class = next(node for node in test_tree.body if isinstance(node, ast.ClassDef)
                  and node.name == "DesignReviewTests")
method = next(node for node in test_class.body if isinstance(node, ast.FunctionDef)
              and node.name == "test_round4_source_order_and_branch_bounds_red_contracts_are_independent")
fixture_owner = next(node for node in test_class.body if isinstance(node, ast.FunctionDef)
                     and node.name == "_fix15_frozen_review_boundary_contracts")
assert any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
           and node.func.attr == fixture_owner.name for node in ast.walk(method))
source_helper = next(node for node in ast.walk(fixture_owner) if isinstance(node, ast.FunctionDef)
                     and node.name == "chained_source")
probe_helper = next(node for node in ast.walk(new_defs["generator70_source"])
                    if isinstance(node, ast.FunctionDef) and node.name == "chained_source")
assert body(source_helper) == body(probe_helper)
deep_original = next(node for node in fixture_owner.body if isinstance(node, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == "deep_source" for t in node.targets))
deep_probe = next(node for node in new_defs["generator70_source"].body if isinstance(node, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "deep_source" for t in node.targets))
assert body(deep_original) == body(deep_probe)
expected = "^analysis deferred generator depth exceeds 64$"
assert any(isinstance(node, ast.Constant) and node.value == expected for node in ast.walk(fixture_owner))
assert body(next(node for node in ast.walk(pt) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Attribute) and node.func.attr == "_review")) == body(
                 next(node for node in ast.walk(old_pt) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Attribute) and node.func.attr == "_review"))

new_names = sorted(set(new_defs) - set(old_defs))
static = {
 "schema": "c-authority-depth-budget-v5-static-v1", "status": "authored_not_executed",
 "source_sha256": NEW_SOURCE, "probe_sha256": probe_sha, "control_sha256": control_sha,
 "plan_sha256": PINS["engineer-v30-generator70-diagnostic-plan-v1.md"],
 "red_receipt_sha256": PINS["tests-checks/focused-v2-v30-first01-design-311-receipt.json"],
 "predecessor_pins": PINS, "case": "generator70", "population": ["generator70"],
 "original_tests_sha256": ORIGINAL_TEST_SHA,
 "fixture_sha256": "635e682b2253cd44201e2afdb95c288b9973f5629ec4eeb3c5bfd078743eb5e3",
 "inverse_probe_exact": True, "inverse_control_exact": True,
 "original_builder_AST_preserved": True, "original_deep_source_AST_preserved": True,
 "original_fixture_owner": fixture_owner.name, "original_test_calls_fixture_owner": True,
 "static_author_v1_stopped_before_any_harness_write": "original builder is in called _fix15 helper, not direct test body",
 "original_review_call_AST_preserved": True, "all_three_retained_builder_ASTs_unchanged": True,
 "original_consume_delegation_calls": 1, "original_merge_delegation_calls": 1,
 "source_write_bytes": 0, "tests_write_bytes": 0, "payload_executed": False,
 "original_NameMeter_not_wrapped": True, "five_cap_names_and_assertion_retained": True,
 "wrapper_delta": "only case allowlist narrowed to generator70",
 "new_probe_definitions": new_names, "checkpoint_source_lines": sites,
 "reach_source_line": 22418, "scope": "single retained generator70 floor-only diagnostic",
 "runtime_limit": "60 seconds owned direct child; no new Git or descendant watchdog claim",
 "observer_retention": "observer-only dictionaries/counters contain scalar leaves; merge contexts copied/validated on exit and failure summary",
 "restoration": "original install/finally protocol retained, plus empty merge stack and all-call outcome reconciliation",
 "interpretation": "charge attempts/successes are distinct from action completion; budget interruption remains incomplete/unknown",
}
files = {
 "engineer-depth-budget-probe-v5.py": probe_raw,
 "tests-depth-budget-control-v5.py": control_raw,
 "engineer-depth-budget-probe-v5-from-v4.diff": "".join(difflib.unified_diff(
     raw_probe.decode().splitlines(True), p.splitlines(True),
     fromfile="engineer-depth-budget-probe-v4.py", tofile="engineer-depth-budget-probe-v5.py")).encode(),
 "tests-depth-budget-control-v5-from-v4.diff": "".join(difflib.unified_diff(
     raw_control.decode().splitlines(True), c.splitlines(True),
     fromfile="tests-depth-budget-control-v4.py", tofile="tests-depth-budget-control-v5.py")).encode(),
 "engineer-depth-budget-v5-static-v1.json": (json.dumps(static, sort_keys=True, indent=2) + "\n").encode(),
}
for relative in files:
    assert not (T / relative).exists(), relative
for relative, expected_pin in PINS.items():
    assert digest((T / relative).read_bytes()) == expected_pin, relative
watch = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1\tools\generate_test_inventory.py")
assert digest(watch.read_bytes()) == WATCH_SHA
for relative, raw in files.items():
    with (T / relative).open("xb") as stream:
        stream.write(raw)
artifacts = {relative: {"sha256": digest(raw), "bytes": len(raw)} for relative, raw in files.items()}
handoff = f"""# Depth-budget diagnostic v5: exact v30 / generator70 only

Authoring-only release. Root approved plan {PINS['engineer-v30-generator70-diagnostic-plan-v1.md']}. No candidate, probe, controller or generated fixture was imported/executed by this author. Static validation parsed/compiled inert source and read original r010 test bytes through Git.

Candidate remains engineer-generator-v30-storage.py SHA {NEW_SOURCE}. Original tests remain {ORIGINAL_TEST_SHA}; generator70 fixture remains 635e682b2253cd44201e2afdb95c288b9973f5629ec4eeb3c5bfd078743eb5e3 and exact deferred-depth expectation unchanged. W watch remains {WATCH_SHA}.

## Issued artifacts

""" + "\n".join(f"- {name}: SHA {item['sha256']}, {item['bytes']} bytes." for name, item in artifacts.items()) + f"""

## Observation boundary

The existing consume observer delegates the same original call once. NameMeter remains unwrapped; original code and all five caps are checked/restored. The existing counted merge observer is replaced by one original-delegating scalar scope; no doubled merge call. Scope contexts retain only scalar leaves, dictionaries/counters of those leaves, and descriptive input-count tuples. No history traversal, entry lookup, mapping/cursor call or authority helper is added for branch observation.

Actual computed locals are captured at existing checkpoints. Raw sizes are descriptive and are not converted into shared-root/entry claims. The original base result and candidate/union counts are read only after construction. A failed request can retain these already-computed observations, but its charge is not marked successful. Result/input pass flags require already-selected original guarded blocks. Fallback reasons are classified only at the original full-build event; interruption before that event is not inferred into a fallback. Last guard checkpoints remain checkpoint labels, not independently rerun predicates.

Only original merge return after a successful final-install charge counts as disabled installation completed. A selected body, paid preparation or failed install request never does. Final post-unwind records retain inclusive merge/publication costs, failed requests, disjoint component units and NameMeter categories as separate views. Inclusive values overlap; they must not be added to the component partition. Existing full-build raw sharing facts remain descriptive predecessor observations.

Probe/control/embedded wrapper allow only generator70. Unselected helper builder bodies remain unchanged and unreachable by CLI. The original test helper, deep-source assignment, review call, fixture hash and exact-depth expectation were statically matched. Original consume arguments, exception propagation, phase classifier and publication wrapper were preserved.

## Root-owned dispatch after source review

- Control: tests-depth-budget-control-v5.py, SHA {control_sha}.
- Probe: engineer-depth-budget-probe-v5.py, SHA {probe_sha}.
- Proposed label v30-branch01, --case generator70, actual CPython3.11.15 only.
- Use inherited explicit source/probe/control/watch SHA arguments and retained absolute source path; every invocation creates a fresh D-local r010 snapshot.
- Preserve original absent-hashseed policy, scrubbed environment, pre-import identity, original1761 tracked population, isolated payload/manifest, create-only outputs, full before/after custody and 60-second owned direct-child watchdog.
- No payload by author, dev slot, further case, retry, optimization, test/cap/unit changes or source installation is authorized here.

Static proof is inspection evidence, not runtime validation. The v30 focused52/53 remains red; an eventual intact diagnostic receipt will mean diagnostic completion only, never product acceptance.
"""
handoff_raw = handoff.encode()
handoff_path = T / "engineer-depth-budget-v5-handoff-v1.md"
assert not handoff_path.exists()
with handoff_path.open("xb") as stream:
    stream.write(handoff_raw)
for relative, expected_pin in PINS.items():
    assert digest((T / relative).read_bytes()) == expected_pin, relative
assert digest(watch.read_bytes()) == WATCH_SHA
print(json.dumps({"artifacts": artifacts, "handoff": {
    "path": str(handoff_path), "sha256": digest(handoff_raw), "bytes": len(handoff_raw)},
    "source_unchanged": True, "payload_executed": False}, sort_keys=True, indent=2))
