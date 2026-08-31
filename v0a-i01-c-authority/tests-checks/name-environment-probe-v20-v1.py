"""Pinned public-boundary structural diagnosis; sensitive programs remain bytes."""
import ast
import builtins
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority\tests-checks")
SOURCE_SHA = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
BASELINE_SOURCE_SHA = "3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1"
MEASUREMENT_PLAN_SHA = "e6191d4f764aadde2daefb678baebcfa076bc9bb4f5a8bd01a82526b65871649"
CRITERIA_SHA = "5ed54466f7b646afa6982bc2778018a5bf00a171d7379ee3c5a64cbaea92e2ba"
PACK_SHA = "d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c"
PLAN_SHA = "969b3acb781cca11ccd10b26eddaab300a5af7a24b4199ae235136a68f4f62ef"

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

raw = (ROOT / "name-environment-cases-v1.json").read_bytes()
assert digest(raw) == PACK_SHA
assert digest((ROOT / "name-environment-plan-v1.md").read_bytes()) == PLAN_SHA
pack = json.loads(raw)
assert pack["source_sha256"] == BASELINE_SOURCE_SHA
assert digest((ROOT / "name-environment-v20-measurement-plan-v1.md").read_bytes()) == MEASUREMENT_PLAN_SHA
assert digest((ROOT / "name-environment-v20-outcome-criteria-v1.md").read_bytes()) == CRITERIA_SHA
assert len(pack["cases"]) == pack["planned_cases"] == 24
assert sum(len(case["witnesses"]) for case in pack["cases"]) == 58
assert len({case["id"] for case in pack["cases"]}) == 24
assert Counter(case["classification"] for case in pack["cases"]) == {
    "clean": 19, "refuse": 4, "permitted-refusal": 1}
source_path = Path.cwd() / "tools/generate_test_inventory.py"
assert digest(source_path.read_bytes()) == SOURCE_SHA
spec = importlib.util.spec_from_file_location("name_environment_generator", source_path)
generator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = generator
spec.loader.exec_module(generator)
original_consume = generator._AnalysisBudget.consume
original_merge = generator._merge_flow_values
original_merge_states = generator._SourceOrderedResolver._merge_states
caps = {name: getattr(generator, name) for name in (
    "MAXIMUM_ANALYSIS_HELPER_DEPTH", "MAXIMUM_ANALYSIS_CHILD_DEPTH",
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS", "MAXIMUM_ANALYSIS_CARDINALITY",
    "MAXIMUM_ANALYSIS_WORK_UNITS")}
assert tuple(caps.values()) == (64, 4, 4096, 2147483647, 262144)
current = None
scopes = []
merge_contexts = []
join_contexts = []
ordered_depth = 0
charge_origin = None
patches = []
instrumentation_errors = []
CANDIDATE_ORIGINS = {14509: "unrelated-root", 14516: "changed-history", 14520: "pending-entry"}


def new_metrics():
    return {
        "charged_unit_sum_across_budgets": 0, "consume_calls": 0,
        "largest_individual_budget_work": 0, "original_budget_failures": [],
        "events": Counter(), "physical_completed": Counter(),
        "physical_by_phase": Counter(), "charged_callers": Counter(),
        "charged_parents": Counter(), "charged_phases": Counter(),
        "name_charged_kinds": Counter(), "name_charged_phases": Counter(),
        "normalization_paths": Counter(), "callback_paths": Counter(),
        "candidate_requests": Counter(), "merge_paths": Counter(),
        "projected_merge_normalizations": 0, "projected_merge_operands": 0,
        "ambient_merge_normalizations": 0, "ambient_merge_operands": 0,
    }


def phase():
    if ordered_depth:
        return "ordered-read"
    if join_contexts:
        return "version-join/" + join_contexts[-1]["base"]
    if merge_contexts:
        return "state-merge/" + merge_contexts[-1]["path"]
    return scopes[-1] if scopes else "other"


def event(name, amount=1):
    if current is not None:
        current["events"][name] += amount


def physical(name, amount=1):
    if current is not None:
        current["physical_completed"][name] += amount
        current["physical_by_phase"][phase() + "/" + name] += amount


def ambient(name):
    return type(name) is str and name.startswith("ambient_")


def original_frame(frame):
    # At most two observer wrapper frames; never scan a deep runtime stack.
    for _ in range(2):
        if frame is not None and frame.f_code.co_filename == __file__:
            frame = frame.f_back
    return frame


def tracked_consume(self, units=1):
    frame = sys._getframe(1)
    if (current is not None and merge_contexts
            and frame.f_code is original_merge_states.__code__):
        local = frame.f_locals
        if local.get("compatible") is False and "binding_plan" in local:
            if not local["result"].authority.enabled:
                reason = "legacy-disabled-authority"
            elif "seen" in local:
                reason = "legacy-cell-overlap-or-missing"
            else:
                reason = "legacy-incompatible-input-or-meter"
            merge_contexts[-1]["path"] = reason
    if current is not None:
        current["charged_unit_sum_across_budgets"] += units
        current["consume_calls"] += 1
        current["largest_individual_budget_work"] = max(
            current["largest_individual_budget_work"], self.work_units + units)
        caller = frame.f_code.co_qualname + ":" + str(frame.f_lineno)
        parent = original_frame(frame.f_back)
        parent_name = (parent.f_code.co_qualname + ":" + str(parent.f_lineno)
                       if parent is not None else "<root>")
        if charge_origin is not None and frame.f_code.co_qualname == "_NameMeter.charge":
            parent_name = charge_origin
        current["charged_callers"][caller] += units
        current["charged_parents"][caller + " <- " + parent_name] += units
        current["charged_phases"][phase()] += units
    try:
        return original_consume(self, units)
    except generator.InventoryError as error:
        if current is not None:
            current["original_budget_failures"].append({
                "reason": str(error), "work_after": self.work_units,
                "requested_units": units})
        raise


original_name_charge = generator._NameMeter.charge


def tracked_name_charge(self, kind, units=1):
    global charge_origin
    caller = sys._getframe(1)
    previous = charge_origin
    charge_origin = caller.f_code.co_qualname + ":" + str(caller.f_lineno)
    if current is not None:
        current["name_charged_kinds"][kind] += units
        current["name_charged_phases"][phase()] += units
        if kind == "candidate_lookup" and join_contexts:
            parent = caller.f_back
            origin = CANDIDATE_ORIGINS.get(parent.f_lineno, "unknown")
            name = caller.f_locals["name"]
            if origin == "unknown":
                instrumentation_errors.append("unmapped candidate source line " + str(parent.f_lineno))
            origins = join_contexts[-1]["origins"]
            origins.setdefault(name, set()).add(origin)
            current["candidate_requests"][origin] += 1
            if ambient(name):
                current["candidate_requests"]["ambient/" + origin] += 1
    try:
        return original_name_charge(self, kind, units)
    finally:
        charge_origin = previous


def install(owner, name, replacement):
    original = getattr(owner, name)
    patches.append((owner, name, original, original.__code__))
    setattr(owner, name, replacement)


def scoped_method(owner, name, label):
    original = getattr(owner, name)
    def wrapped(*args, **kwargs):
        scopes.append(label)
        event(label + "/calls")
        try:
            return original(*args, **kwargs)
        finally:
            scopes.pop()
    install(owner, name, wrapped)


def allocation_init(owner, label, fields):
    original = owner.__init__
    def wrapped(self, *args, **kwargs):
        original(self, *args, **kwargs)
        physical(label + "_allocations")
        physical(label + "_field_reference_initializations", fields)
    install(owner, "__init__", wrapped)


original_node = generator._name_node


def tracked_node(meter, name, entry, left, right):
    caller = sys._getframe(1)
    origin = caller.f_code.co_qualname
    result = original_node(meter, name, entry, left, right)
    physical("name_node_allocations")
    physical("name_node_field_reference_initializations", 7)
    if ambient(name):
        physical("ambient_name_node_allocations")
        physical("ambient_node_field_reference_initializations", 7)
    event("node_completed_origin/" + origin)
    return result


original_order = generator._name_order


def tracked_order(meter, kind, parents=(), name=None, cache=None):
    result = original_order(meter, kind, parents, name, cache)
    physical("name_order_allocations")
    physical("name_order_field_reference_initializations", 4)
    if parents:
        physical("completed_order_parent_tuple_allocations")
        physical("completed_order_parent_tuple_references", len(parents))
    if ambient(name):
        physical("ambient_order_name_reference_initializations")
    return result


original_realize = generator._name_realize


def tracked_realize(meter, root):
    event("name_realize_calls")
    result = original_realize(meter, root)
    _keys, staged = result
    event("name_realize_completed")
    # Read only tuples already constructed by production; no new realization.
    for order, keys in staged.items():
        if order.kind != "empty" and keys:
            physical("completed_materialized_key_tuple_allocations")
            physical("completed_materialized_key_tuple_references", len(keys))
            physical("ambient_materialized_key_tuple_references",
                     sum(ambient(name) for name in keys))
    return result


original_items = generator._NameVersion.ordered_items


def tracked_items(self):
    global ordered_depth
    uncached = self._items_cache is None
    event("ordered_items_calls/" + ("first" if uncached else "cached"))
    ordered_depth += 1
    try:
        result = original_items(self)
        count = len(result)
        ambient_count = sum(ambient(name) for name, _value in result)
        event("ordered_items_completed/" + ("first" if uncached else "cached"))
        if count:
            physical("completed_items_result_tuple_allocations")
            physical("completed_items_result_tuple_references", count)
            physical("ambient_items_result_tuple_entries", ambient_count)
        if uncached:
            physical("completed_items_index_dictionary_allocations")
            physical("completed_items_index_name_entries", count)
            physical("ambient_items_index_name_entries", ambient_count)
            physical("completed_items_index_field_references", 2 * count)
            physical("completed_items_pair_tuple_allocations", count)
            physical("completed_items_pair_tuple_references", 2 * count)
        return result
    finally:
        ordered_depth -= 1


original_keys = generator._ExecutionState.keys


def tracked_keys(self):
    result = original_keys(self)
    count = len(result)
    physical("completed_adapter_key_dictionary_allocations")
    physical("completed_adapter_key_dictionary_entries", count)
    physical("ambient_adapter_key_dictionary_entries", sum(ambient(name) for name in result))
    physical("completed_adapter_key_dictionary_references", 2 * count)
    return result


original_copy = generator._ExecutionState.copy
original_fork = generator._NameVersion.fork


def tracked_copy(self):
    event("execution_state_copy_calls")
    result = original_copy(self)
    physical("execution_state_wrapper_allocations")
    physical("execution_state_wrapper_field_references", 3)
    event("execution_state_copy_completed")
    # Pinned body shares _names; no len/iteration of state occurs here.
    return result


def tracked_fork(self):
    event("name_version_fork_calls")
    result = original_fork(self)
    event("name_version_fork_completed")
    return result


def tracked_merge_states(self, states):
    context = {"path": "empty" if not states else "singleton" if len(states) == 1 else "setup"}
    merge_contexts.append(context)
    event("state_merge_calls")
    try:
        return original_merge_states(self, states)
    finally:
        if current is not None:
            current["merge_paths"][context["path"]] += 1
        merge_contexts.pop()


original_common_base = generator._name_common_base


def tracked_common_base(meter, states):
    result = original_common_base(meter, states)
    if join_contexts:
        join_contexts[-1]["base"] = "common-base" if result is not None else "unrelated-roots"
        if merge_contexts:
            merge_contexts[-1]["path"] = "version/" + join_contexts[-1]["base"]
    event("common_base_calls/" + ("found" if result is not None else "absent"))
    return result


original_join = generator._join_name_versions


def tracked_join(meter, states, merge):
    context = {"base": "setup", "origins": {}}
    join_contexts.append(context)
    event("version_join_calls")
    def observed_merge(name, supplied):
        if current is not None:
            origins = "+".join(sorted(context["origins"].get(name, {"unclassified"})))
            key = context["base"] + "/" + origins
            current["callback_paths"][key + "/calls"] += 1
            current["callback_paths"][key + "/operands"] += len(supplied)
            if ambient(name):
                current["callback_paths"]["ambient/" + key + "/calls"] += 1
                current["callback_paths"]["ambient/" + key + "/operands"] += len(supplied)
        return merge(name, supplied)
    try:
        return original_join(meter, states, observed_merge)
    finally:
        event("version_join_exit/" + context["base"])
        join_contexts.pop()


def tracked_merge(name, values):
    frame = sys._getframe(1)
    caller = frame.f_code.co_qualname
    projected = caller in {
        "_SourceOrderedResolver._merge_states",
        "_SourceOrderedResolver._merge_states.<locals>.merge_name",
    } and frame.f_code.co_filename == str(source_path)
    if current is not None and projected:
        path = "legacy-direct" if caller.endswith("._merge_states") else (
            "version/" + (join_contexts[-1]["base"] if join_contexts else "unclassified"))
        current["projected_merge_normalizations"] += 1
        current["projected_merge_operands"] += len(values)
        current["normalization_paths"][path + "/calls"] += 1
        current["normalization_paths"][path + "/operands"] += len(values)
        if ambient(name):
            current["ambient_merge_normalizations"] += 1
            current["ambient_merge_operands"] += len(values)
            current["normalization_paths"]["ambient/" + path + "/calls"] += 1
            current["normalization_paths"]["ambient/" + path + "/operands"] += len(values)
    return original_merge(name, values)


original_find = generator._name_find


def tracked_find(meter, node, name):
    event("name_find_calls")
    if ambient(name):
        event("ambient_name_find_calls")
    return original_find(meter, node, name)


original_transfer = generator._transfer_authority


def tracked_transfer(*args, **kwargs):
    caller = sys._getframe(1).f_code.co_qualname
    event("transfer_calls/" + caller)
    return original_transfer(*args, **kwargs)


def serializable_metrics(metrics):
    return {key: dict(value.most_common()) if isinstance(value, Counter) else value
            for key, value in metrics.items()}


install(generator._AnalysisBudget, "consume", tracked_consume)
install(generator._NameMeter, "charge", tracked_name_charge)
install(generator, "_name_node", tracked_node)
install(generator, "_name_order", tracked_order)
install(generator, "_name_realize", tracked_realize)
install(generator._NameVersion, "ordered_items", tracked_items)
install(generator._ExecutionState, "keys", tracked_keys)
install(generator._ExecutionState, "copy", tracked_copy)
install(generator._NameVersion, "fork", tracked_fork)
install(generator._SourceOrderedResolver, "_merge_states", tracked_merge_states)
install(generator, "_name_common_base", tracked_common_base)
install(generator, "_join_name_versions", tracked_join)
install(generator, "_merge_flow_values", tracked_merge)
install(generator, "_name_find", tracked_find)
install(generator, "_transfer_authority", tracked_transfer)
allocation_init(generator._NameEntry, "name_entry", 2)
allocation_init(generator._NameVersion, "name_version", 7)
for name, label in (
        ("__init__", "state-construction"), ("update", "state-adoption"),
        ("_project", "raw-projection"), ("_transferred_name_entry", "transfer-entry")):
    scoped_method(generator._ExecutionState, name, label)


def public_review(source):
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


def project_oracles(case):
    pure = case["oracle_source"]
    assert "subprocess" not in pure and "pontius" not in pure
    tree = ast.parse(pure, filename="<harmless-name-environment-oracle>")
    assert not any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree))
    allowed = {name: getattr(builtins, name) for name in (
        "__build_class__", "staticmethod", "ValueError", "TypeError", "KeyError", "IndexError")}
    actuals, errors = [], []
    for witness in case["witnesses"]:
        namespace = {"__builtins__": allowed, "__name__": "harmless_projection"}
        exec(compile(tree, "<harmless-name-environment-oracle>", "exec", dont_inherit=True),
             namespace)
        instance = namespace["Model"]()
        instance.choice = witness["choice"]
        try:
            result = instance.test_static()
        except Exception as error:
            result = type(error).__name__
        actual = {"choice": witness["choice"], "trace": namespace["_events"], "result": result}
        for name in ("ambient_result", "work_result"):
            if name in witness:
                actual[name] = list(getattr(instance, name))
        if actual != witness:
            errors.append({"expected": witness, "actual": actual})
        if any(event in actual["trace"] for event in case["unreachable_events"]):
            errors.append({"unreachable_event_was_reached": actual["trace"]})
        actuals.append(actual)
    return actuals, errors


results = []
oracle_errors = []
semantic_errors = []
analysis_errors = []
projections = 0
try:
    for case in pack["cases"]:
        witnesses, errors = project_oracles(case)
        projections += len(witnesses)
        if errors:
            oracle_errors.append({"case": case["id"], "errors": errors})
        current = new_metrics()
        review = None
        problem = None
        try:
            review = public_review(case["source"].encode())
        except Exception as error:
            problem = {"type": type(error).__name__, "message": str(error)}
            analysis_errors.append({"case": case["id"], "error": problem})
        metrics = serializable_metrics(current)
        current = None
        argv, blockers = [], []
        semantic_passed = False
        if review is not None:
            argv = [row["argv"] for row in review["receipt"]["expanded_rows"]
                    if row["capability_kind"] == "subprocess"]
            blockers = review["unresolved_dynamic_blockers"]
            if case["classification"] == "refuse":
                semantic_passed = bool(blockers)
            elif case["classification"] == "permitted-refusal":
                semantic_passed = bool(blockers) or argv == [["-m", "fixed"]]
            else:
                semantic_passed = not blockers and argv == [["-m", "fixed"]]
        if not semantic_passed:
            semantic_errors.append(case["id"])
        result = {
            "name_environment_case": case["id"], "classification": case["classification"],
            "source_sha256": digest(case["source"].encode()),
            "oracle_sha256": digest(case["oracle_source"].encode()),
            "witnesses": witnesses, "oracle_errors": errors,
            "argv": argv, "blockers": blockers, "analysis_error": problem,
            "semantic_passed": semantic_passed, "metrics": metrics,
            "proved_unexecuted_events": case["unreachable_events"],
        }
        results.append(result)
        print(json.dumps(result), flush=True)
finally:
    current = None
    for owner, name, original, _code in reversed(patches):
        setattr(owner, name, original)

assert not scopes and not merge_contexts and not join_contexts and ordered_depth == 0
assert all(getattr(owner, name) is original and original.__code__ is code
           for owner, name, original, code in patches)
assert {name: getattr(generator, name) for name in caps} == caps
by_id = {result["name_environment_case"]: result for result in results}
pairs = []
for ambient_count in (8, 64):
    for exit_kind in ("normal", "exceptional"):
        for changed in (0, 2):
            ids = [f"scale-n{ambient_count}-s{count}-d{changed}-{exit_kind}" for count in (2, 4)]
            low, high = (by_id[name] for name in ids)
            values = {field: [low["metrics"][field], high["metrics"][field]]
                      for field in ("ambient_merge_normalizations", "ambient_merge_operands",
                                    "charged_unit_sum_across_budgets",
                                    "largest_individual_budget_work")}
            pairs.append({"case_ids": ids, "ambient": ambient_count, "changed": changed,
                          "exit": exit_kind, "values": values,
                          "semantic_controls_passed": low["semantic_passed"] and high["semantic_passed"],
                          "physical_completed": [low["metrics"]["physical_completed"],
                                                 high["metrics"]["physical_completed"]],
                          "normalization_paths": [low["metrics"]["normalization_paths"],
                                                  high["metrics"]["normalization_paths"]],
                          "merge_paths": [low["metrics"]["merge_paths"], high["metrics"]["merge_paths"]]})
for result in results:
    metrics = result["metrics"]
    if sum(metrics["charged_phases"].values()) != metrics["charged_unit_sum_across_budgets"]:
        instrumentation_errors.append("original charge phase mismatch: " + result["name_environment_case"])
    if sum(metrics["name_charged_phases"].values()) != sum(metrics["name_charged_kinds"].values()):
        instrumentation_errors.append("name charge phase mismatch: " + result["name_environment_case"])
exit_code = 4 if instrumentation_errors else 3 if oracle_errors else 2 if semantic_errors or analysis_errors else 0
summary = {
    "name_environment_summary": "versioned-name-environment-v20-measurement-v1",
    "planned": 24, "generated": len(pack["cases"]), "exercised": len(results),
    "planned_projections": 58, "exercised_projections": projections,
    "unreachable_cases": [], "oracle_errors": oracle_errors,
    "semantic_errors": semantic_errors, "analysis_errors": analysis_errors,
    "instrumentation_errors": instrumentation_errors,
    "classifications": dict(Counter(case["classification"] for case in pack["cases"])),
    "structural_pairs": pairs, "structural_verdict": "reported-by-path-with-frozen-criteria",
    "caps_unchanged": caps, "original_methods_delegated": True,
    "source_sha256": SOURCE_SHA, "baseline_source_sha256": BASELINE_SOURCE_SHA,
    "case_pack_sha256": PACK_SHA, "semantic_plan_sha256": PLAN_SHA,
    "measurement_plan_sha256": MEASUREMENT_PLAN_SHA, "criteria_sha256": CRITERIA_SHA,
    "state_copy_full_name_entries": 0,
    "state_copy_zero_basis": "pinned body shares the name version; counts are not inferred from state size",
    "physical_counts_are_not_charged_units": True,
    "physical_counts_scope": "completed selected source-proven boundaries; lower bounds if an operation throws",
    "node_allocations_are_not_v19_dict_entry_copies": True,
    "name_charges_are_subset_of_original_budget": True,
    "ordered_work": "production-demanded only; first/cached calls and phases reported, no forced materialization",
    "no_budget_objects_or_ast_caches_retained": True,
    "exit": exit_code,
    "exit_reason": ("instrumentation-error" if instrumentation_errors else "oracle-error" if oracle_errors
                    else "public-semantic-or-analysis-error" if semantic_errors or analysis_errors
                    else "semantic-controls-passed-structural-costs-reported"),
}
print(json.dumps(summary), flush=True)
raise SystemExit(exit_code)
