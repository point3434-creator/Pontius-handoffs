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
SOURCE_SHA = "3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1"
PACK_SHA = "d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c"
PLAN_SHA = "969b3acb781cca11ccd10b26eddaab300a5af7a24b4199ae235136a68f4f62ef"

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

raw = (ROOT / "name-environment-cases-v1.json").read_bytes()
assert digest(raw) == PACK_SHA
assert digest((ROOT / "name-environment-plan-v1.md").read_bytes()) == PLAN_SHA
pack = json.loads(raw)
assert pack["source_sha256"] == SOURCE_SHA
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
original_copy = generator._ExecutionState.copy
original_merge = generator._merge_flow_values
original_codes = tuple(fn.__code__ for fn in (original_consume, original_copy, original_merge))
caps = {name: getattr(generator, name) for name in (
    "MAXIMUM_ANALYSIS_HELPER_DEPTH", "MAXIMUM_ANALYSIS_CHILD_DEPTH",
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS", "MAXIMUM_ANALYSIS_CARDINALITY",
    "MAXIMUM_ANALYSIS_WORK_UNITS")}
assert tuple(caps.values()) == (64, 4, 4096, 2147483647, 262144)
current = None


def new_metrics():
    return {
        "physical_name_copy_calls": 0, "physical_name_copy_entries": 0,
        "physical_ambient_copy_entries": 0, "projected_merge_normalizations": 0,
        "projected_merge_operands": 0, "ambient_merge_normalizations": 0,
        "ambient_merge_operands": 0, "charged_unit_sum_across_budgets": 0,
        "consume_calls": 0, "largest_individual_budget_work": 0,
        "charged_callers": Counter(), "charged_parents": Counter(),
        "original_budget_failures": [],
    }


def tracked_consume(self, units=1):
    if current is not None:
        current["charged_unit_sum_across_budgets"] += units
        current["consume_calls"] += 1
        current["largest_individual_budget_work"] = max(
            current["largest_individual_budget_work"], self.work_units + units)
        frame = sys._getframe(1)
        key = frame.f_code.co_qualname + ":" + str(frame.f_lineno)
        parent = frame.f_back
        parent_key = (parent.f_code.co_qualname + ":" + str(parent.f_lineno)
                      if parent is not None else "<root>")
        current["charged_callers"][key] += units
        current["charged_parents"][key + " <- " + parent_key] += units
    try:
        return original_consume(self, units)
    except generator.InventoryError as error:
        if current is not None:
            current["original_budget_failures"].append({
                "reason": str(error), "work_after": self.work_units,
                "requested_units": units})
        raise


def tracked_copy(self):
    if current is not None:
        # Exact v19 copy immediately invokes dict.__init__(result, self).
        # This observer traversal is diagnostic overhead, not a production charge.
        current["physical_name_copy_calls"] += 1
        current["physical_name_copy_entries"] += len(self)
        current["physical_ambient_copy_entries"] += sum(
            name.startswith("ambient_") for name in self)
    return original_copy(self)


def tracked_merge(name, values):
    frame = sys._getframe(1)
    if current is not None and frame.f_code.co_qualname == "_SourceOrderedResolver._merge_states":
        current["projected_merge_normalizations"] += 1
        current["projected_merge_operands"] += len(values)
        if name.startswith("ambient_"):
            current["ambient_merge_normalizations"] += 1
            current["ambient_merge_operands"] += len(values)
    return original_merge(name, values)


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


def serializable_metrics(metrics):
    answer = dict(metrics)
    for key in ("charged_callers", "charged_parents"):
        answer[key] = dict(metrics[key].most_common())
    return answer


generator._AnalysisBudget.consume = tracked_consume
generator._ExecutionState.copy = tracked_copy
generator._merge_flow_values = tracked_merge
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
    generator._AnalysisBudget.consume = original_consume
    generator._ExecutionState.copy = original_copy
    generator._merge_flow_values = original_merge

assert tuple(fn.__code__ for fn in (original_consume, original_copy, original_merge)) == original_codes
assert {name: getattr(generator, name) for name in caps} == caps
by_id = {result["name_environment_case"]: result for result in results}
pairs = []
fields = ("physical_ambient_copy_entries", "ambient_merge_normalizations", "ambient_merge_operands")
for ambient in (8, 64):
    for exit_kind in ("normal", "exceptional"):
        for changed in (0, 2):
            ids = [f"scale-n{ambient}-s{count}-d{changed}-{exit_kind}" for count in (2, 4)]
            low, high = (by_id[name] for name in ids)
            values = {field: [low["metrics"][field], high["metrics"][field]] for field in fields}
            dimensions = [field for field, (a, b) in values.items() if b > a and b > ambient]
            pairs.append({"case_ids": ids, "ambient": ambient, "changed": changed,
                          "exit": exit_kind, "values": values, "increased_dimensions": dimensions,
                          "semantic_controls_passed": low["semantic_passed"] and high["semantic_passed"],
                          "structural_repeated_work": bool(dimensions)})
structural_red = any(pair["changed"] == 0 and pair["structural_repeated_work"]
                     and pair["semantic_controls_passed"] for pair in pairs)
exit_code = 3 if oracle_errors else 2 if semantic_errors or analysis_errors else 1 if structural_red else 0
summary = {
    "name_environment_summary": "versioned-name-environment-structural-v1",
    "planned": 24, "generated": len(pack["cases"]), "exercised": len(results),
    "planned_projections": 58, "exercised_projections": projections,
    "unreachable_cases": [], "oracle_errors": oracle_errors,
    "semantic_errors": semantic_errors, "analysis_errors": analysis_errors,
    "classifications": dict(Counter(case["classification"] for case in pack["cases"])),
    "structural_pairs": pairs, "structural_red": structural_red,
    "caps_unchanged": caps, "original_methods_delegated": True,
    "source_sha256": SOURCE_SHA, "case_pack_sha256": PACK_SHA, "plan_sha256": PLAN_SHA,
    "physical_counts_are_not_charged_units": True, "no_budget_objects_or_ast_caches_retained": True,
    "exit": exit_code,
    "exit_reason": ("oracle-error" if oracle_errors else "public-semantic-or-analysis-error"
                    if semantic_errors or analysis_errors else "structural-repeated-work"
                    if structural_red else "no-structural-red-demonstrated"),
}
print(json.dumps(summary), flush=True)
raise SystemExit(exit_code)
