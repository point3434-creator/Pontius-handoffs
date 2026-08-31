"""Frozen R2 identity premise:12 public cases/24 Models; exact R1 adapter; no work on import."""
import ast
import builtins
from collections import Counter
import hashlib
import importlib.util
import json
import os
import re
import textwrap
from pathlib import Path
import stat
import sys


PACKS = {
    "storage": {
        "file": "storage-composition-cases-v1.json",
        "sha256": "faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709",
        "schema": "pontius-storage-composition-cases-v1",
        "planned_cases": 4,
        "planned_projections": 4,
        "ids": [
            "shared-list-consumed",
            "shared-list-dormant",
            "class-adoption-unsafe",
            "class-adoption-safe"
        ]
    },
    "name_environment": {
        "file": "name-environment-cases-v1.json",
        "sha256": "d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c",
        "schema": "pontius-engineering-name-environment-family-v1",
        "planned_cases": 24,
        "planned_projections": 58,
        "ids": [
            "hidden-cell-joined-reached",
            "hidden-cell-joined-dormant"
        ]
    },
    "identity": {
        "file": "rewrite-r2-identity-cases-v1.json",
        "sha256": "4834971b9d63aa182c1207959721b6bb65f742a106541d96975945060134d9ea",
        "schema": "pontius-rewrite-r2-identity-premise-cases-v1",
        "planned_cases": 4,
        "planned_projections": 16,
        "ids": [
            "identity-scale-n8-s4-d0-normal",
            "identity-scale-n64-s4-d0-normal",
            "identity-scale-n8-s4-d2-exceptional",
            "identity-scale-n64-s4-d2-exceptional"
        ]
    }
}
PACK_HASHES = {scope: metadata["sha256"] for scope, metadata in PACKS.items()}
GATE_B_IDS = tuple(["shared-list-consumed","shared-list-dormant","class-adoption-unsafe","class-adoption-safe","hidden-cell-joined-reached","hidden-cell-joined-dormant","helper65","generator70","identity-scale-n8-s4-d0-normal","identity-scale-n64-s4-d0-normal","identity-scale-n8-s4-d2-exceptional","identity-scale-n64-s4-d2-exceptional"])
CONTINUATION_MAXIMUM = 196608
TESTS_SHA = 'c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf'
DEPTH_PROVENANCE_SHA = '7aa9f188b2917fec149485501eafcc4d516d3104a10b026e5ec33262b24962ae'
DEPTH_CASES = {'helper65': {'method': 'test_round4_analysis_budget_red_contracts_are_independent', 'fixture_sha256': '94b070b8fcf2e66c42e1a779558e830d7caae670366f9313faf0989c722818c6', 'regex': '^analysis helper depth exceeds 64$'}, 'generator70': {'method': 'test_round4_source_order_and_branch_bounds_red_contracts_are_independent', 'fixture_sha256': '635e682b2253cd44201e2afdb95c288b9973f5629ec4eeb3c5bfd078743eb5e3', 'regex': '^analysis deferred generator depth exceeds 64$'}}
POPULATION_SHA = "8ab800c1361ca53f4f294bd32e308ecb7061e031b60d32dc74d7fdf52cc5ce3b"

PLAN_SHA = 'd4e3b07268e291863d90b35711485d1679f6ce826d01e3429604fdc375ae0182'
OBSERVER_MAP_SHA = 'a685562866deec86553d8ca06b458269f06e3f015418401325e7c4d43c1a232b'
CONSUME_SEGMENT_SHA = 'd910a8af42711e5130b93af9e55b8917dbd8b48433e29e1ab3cd51df63b7af5c'
PAYLOAD = ".rewrite-r2-identity"
SCHEMA = "pontius-rewrite-r2-identity-v1"
SLOTS = {
    "311": (r"D:\Pontius-tools\py311\Scripts\python.exe", (3, 11, 15)),
    "314": (r"D:\Pontius\.venv\Scripts\python.exe", (3, 14, 6)),
}
CAPS = {
    "MAXIMUM_ANALYSIS_HELPER_DEPTH": 64, "MAXIMUM_ANALYSIS_CHILD_DEPTH": 4,
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS": 4096,
    "MAXIMUM_ANALYSIS_CARDINALITY": 2147483647, "MAXIMUM_ANALYSIS_WORK_UNITS": 262144,
}


ADAPTER_SOURCE_SHA = "c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f"
ADAPTER_ID = "r1-baseline-only"
BASELINE_HOOKS = tuple(["_c_state","_c_fork","_c_snapshot","_c_copy_dict","_c_cell_write","_c_eval","_c_statement","_c_join","_c_invoke","_c_call","_c_sink","_c_review_outcomes"])
MECHANISM_AVAILABILITY = {name: True for name in BASELINE_HOOKS}
MECHANISM_AVAILABILITY.update({name: False for name in ["_c_identity_compare","_c_raise_known","_c_handle_known_exception","_c_resume_generator"]})
EXTRA_INPUTS = {
    "prior_population": {
        "relative": "rewrite-early-population-v1.json",
        "payload": "prior-population.json",
        "sha256": "3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce"
    },
    "coverage": {
        "relative": "tests-checks/rewrite-r2-identity-coverage-v1.json",
        "payload": "identity-coverage.json",
        "sha256": "05e24952ff5672554012bfb784215d76e44f7d95b2f3dbd1e3c0f8672d13ec38"
    },
    "spec": {
        "relative": "tests-checks/rewrite-r2-identity-observer-controller-spec-v1.md",
        "payload": "observer-spec.md",
        "sha256": "4d4ed42a3fb132eb79c3a40bcb943268cbb2883a28152176c52d05c845791b52"
    },
    "authorization": {
        "relative": "rewrite-r2-harness-authoring-disposition-v1.md",
        "payload": "authoring-disposition.md",
        "sha256": "34cb19a6ec98ea5b92219a50f9622f7aec2ed3c84139b4e78f7e7e9f02aed5ab"
    },
    "addendum": {
        "relative": "rewrite-r2-plan-addendum-v1.md",
        "payload": "plan-addendum.md",
        "sha256": "1a1a6bc7f8ef4c56a72735670ff0bb65e883f3aa559abec7b4fec01af6991998"
    },
    "source_model_diff": {
        "relative": "tests-checks/rewrite-r2-identity-source-model-differences-v1.diff",
        "payload": "source-model.diff",
        "sha256": "d132ded3312b936a5510a4c498f39c06d3a4a6259903cd8ddef0269211e110a6"
    }
}
EXTRA_HASHES = {name: item["sha256"] for name, item in EXTRA_INPUTS.items()}
BASE_PAYLOAD_NAMES = frozenset(["authoring-disposition.md","control.py","depth-provenance.py","identity-coverage.json","name-environment-cases-v1.json","observer-map.json","observer-spec.md","plan-addendum.md","plan.md","population.json","prior-population.json","probe.py","retained-source.py","rewrite-r2-identity-cases-v1.json","run.json","source-model.diff","storage-composition-cases-v1.json"])
RESERVE_BASIS = "requested_units_per_original_epoch"


def require(value, reason):
    if not value:
        raise RuntimeError(reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("utf-8")


def checked(path):
    require(path.is_absolute() and ".." not in path.parts, "unsafe child path")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        require(not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT,
                "child reparse path")
        if ancestor != path:
            require(stat.S_ISDIR(info.st_mode), "child non-directory ancestor")
    require(stat.S_ISREG(path.lstat().st_mode), "child non-regular input")
    return path


def hashes(snapshot, manifest):
    actual = {}
    for name, wanted in manifest.items():
        relative = Path(name)
        require(not relative.is_absolute() and not relative.drive and ".." not in relative.parts,
                "unsafe manifest name")
        actual[name] = digest(checked(snapshot / relative).read_bytes())
        require(actual[name] == wanted, "manifest input changed: " + name)
    return actual


def case_canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")



def load_cases(raw_by_scope, population_raw):
    require(hashlib.sha256(population_raw).hexdigest() == POPULATION_SHA, "frozen population")
    population = json.loads(population_raw)
    require(population["schema"] == "pontius-rewrite-r2-identity-successor-population-v1", "successor population schema")
    require(tuple(population["gates"]["A"]["ordered_case_ids"]) == GATE_B_IDS[:6],
            "unchanged Gate A prefix")
    gate = population["gates"]["B_identity"]
    require(tuple(gate["ordered_case_ids"]) == GATE_B_IDS
            and gate["public_analysis_count"] == 12 and gate["independent_model_projections"] == 24
            and gate["depth_assertions"] == 2
            and gate["engineering_continuation_work_maximum"] == CONTINUATION_MAXIMUM
            and gate["production_work_cap_unchanged"] == 262144, "exact frozen Gate B")
    require(set(raw_by_scope) == set(PACKS), "exact original pack set")
    selected = {}
    for scope, metadata in PACKS.items():
        raw = raw_by_scope[scope]
        require(hashlib.sha256(raw).hexdigest() == metadata["sha256"], "original pack pin")
        pack = json.loads(raw)
        require(pack["schema"] == metadata["schema"], "original pack schema")
        require(type(pack["planned_cases"]) is int
                and pack["planned_cases"] == metadata["planned_cases"]
                and type(pack["planned_projections"]) is int
                and pack["planned_projections"] == metadata["planned_projections"],
                "original complete pack counts")
        require(len(pack["cases"]) == metadata["planned_cases"]
                and len({case["id"] for case in pack["cases"]}) == metadata["planned_cases"],
                "original complete pack uniqueness")
        by_id = {case["id"]: case for case in pack["cases"]}
        for identifier in metadata["ids"]:
            case = by_id[identifier]
            binding = population["cases"][identifier]
            require(binding["envelope_ref"] in population["envelopes"], "resolved public envelope")
            require(binding["pack_ref"] == "tests-checks/" + metadata["file"], "case pack reference")
            require(hashlib.sha256(case_canonical(case)).hexdigest()
                    == binding["case_record_canonical_sha256"], "selected original record")
            for field, target in (("source", "source"), ("oracle_source", "model")):
                value = case[field]
                require(type(value) is str and value.endswith("\n") and "\r" not in value,
                        "original source format")
                require(hashlib.sha256(value.encode("utf-8")).hexdigest()
                        == binding[target]["sha256"], "original source/model identity")
                ast.parse(value, filename="<GateB-unexecuted-source-or-Model>")
            require(case["classification"] == binding["classification"], "original classification")
            selected[identifier] = (scope, case)
    require(len(selected) == 10, "ten original Model cases")
    require(sum(1 if scope == "storage" else len(case["witnesses"])
                for scope, case in selected.values()) == 24, "exact24 Models")
    for identifier, expected in DEPTH_CASES.items():
        binding = population["cases"][identifier]
        require(binding["classification"] == "exact-depth-error"
                and binding["model"] is None and binding["model_projection_count"] == 0
                and binding["envelope_ref"] == "original_design_review", "original depth kind")
        require(binding["source"]["sha256"] == expected["fixture_sha256"]
                and binding["oracle"]["exception"] == "InventoryError"
                and binding["oracle"]["regex"] == expected["regex"], "original depth expectation")
        require(binding["original_method"]["symbol"].split(".")[-1] == expected["method"],
                "original depth owner method")
        selected[identifier] = ("depth", binding)
    require(set(selected) == set(GATE_B_IDS), "no extra cases")
    result = [selected[identifier] for identifier in GATE_B_IDS]
    require(dict(Counter(case["classification"] for scope, case in result))
            == {"clean": 6, "refuse": 3, "permitted-refusal": 1, "exact-depth-error": 2},
            "Gate B classifications")
    return result


def public_verdict(scope, case, argv, blockers):
    if case["classification"] == "refuse":
        return bool(blockers)
    if scope == "storage":
        return not blockers and argv == case["required_argv"]
    if case["classification"] == "permitted-refusal":
        return bool(blockers) or argv == [["-m", "fixed"]]
    return not blockers and argv == [["-m", "fixed"]]


def storage_oracle(case):
    source = case["oracle_source"]
    require("subprocess" not in source and "pontius" not in source, "unsafe oracle text")
    tree = ast.parse(source, filename="<harmless-storage-composition>")
    require(not any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree)),
            "oracle may not import")
    allowed = {name: getattr(builtins, name) for name in ("__build_class__", "staticmethod")}
    namespace = {"__builtins__": allowed, "__name__": "harmless_composition"}
    exec(compile(tree, "<harmless-storage-composition>", "exec", dont_inherit=True), namespace)
    try:
        result = namespace["Model"]().test_static()
    except Exception as error:
        result = type(error).__name__
    actual = {"trace": namespace["_events"], "result": result}
    return actual, (actual == case["expected"] and not any(
        event in actual["trace"] for event in case["unreachable_events"]))





def storage_public_review(generator, source):
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


def budget_context(frame):
    """Return scalars only; never retain frames, ASTs, stores or budget objects."""
    rows = []
    while frame is not None:
        row = {"function": frame.f_code.co_qualname, "line": frame.f_lineno,
               "file": Path(frame.f_code.co_filename).name}
        local = frame.f_locals
        for name in ("relative_path", "item_id", "stable_id", "name"):
            value = local.get(name)
            if type(value) is str:
                row[name] = value
        rows.append(row)
        frame = frame.f_back
    return rows


def budget_origin(frame):
    return (frame.f_code.co_qualname + ":" + str(frame.f_lineno)
            if frame is not None else "<root>")


def budget_phase(frame):
    """Nearest matching original entry wins; unrecognized paths remain explicit."""
    stages = (
        ("_definition_time_protocol_resolver", "definition_time_protocol"),
        ("_unittest_receiver_attributes", "unittest_preflight"),
        ("_source_ordered_helper_return", "source_ordered_helper_return"),
        ("review_flow", "review_flow"),
    )
    while frame is not None:
        short = frame.f_code.co_name
        for name, label in stages:
            if short == name:
                return label
        frame = frame.f_back
    return "other"


class BudgetObserver:
    def __init__(self, module):
        self.module = module
        self.original_init = module._AnalysisBudget.__init__
        self.original_consume = module._AnalysisBudget.consume
        self.original_codes = (self.original_init.__code__, self.original_consume.__code__)
        self.current = None
        self.by_id = {}
        self.unscoped_events = 0

    def install(self):
        observer = self
        original_init, original_consume = self.original_init, self.original_consume

        def observed_init(budget, *args, **keywords):
            if observer.current is None:
                observer.unscoped_events += 1
                return original_init(budget, *args, **keywords)
            context = budget_context(sys._getframe(1))
            observer.current["initialization_attempts"] += 1
            try:
                result = original_init(budget, *args, **keywords)
            except BaseException as error:
                observer.current["initialization_errors"].append({
                    "type": type(error).__name__, "message": str(error), "creation_stack": context})
                raise
            initial = object.__getattribute__(budget, "work_units")
            require(type(initial) is int and initial >= 0, "original budget initial integer")
            entry = {"epoch": len(observer.current["epochs"]) + 1, "initial_work": initial,
                     "last_observed_work": initial, "requested_units": 0, "consume_calls": 0,
                     "completed_consume_calls": 0, "exceptional_consume_calls": 0,
                     "origins": {}, "phase_units": {}, "creation_stack": context,
                     "consume_exceptions": []}
            observer.current["epochs"].append(entry)
            # An id reused after destruction is overwritten by this new epoch.
            # An old live budget cannot share an id; no budget reference escapes.
            observer.by_id[id(budget)] = entry
            return result

        def observed_consume(budget, units=1):
            if observer.current is None:
                observer.unscoped_events += 1
                return original_consume(budget, units)
            entry = observer.by_id.get(id(budget))
            require(entry is not None, "consume without observed original initialization")
            before = object.__getattribute__(budget, "work_units")
            require(type(units) is int and units >= 0 and type(before) is int,
                    "original integer charge contract")
            require(before == entry["last_observed_work"], "unobserved original work mutation")
            frame = sys._getframe(1)
            origin = budget_origin(frame)
            parent = budget_origin(frame.f_back)
            phase = budget_phase(frame)
            row = entry["origins"].setdefault(origin + " <- " + parent, {"calls": 0, "units": 0})
            row["calls"] += 1
            row["units"] += units
            entry["phase_units"][phase] = entry["phase_units"].get(phase, 0) + units
            entry["consume_calls"] += 1
            entry["requested_units"] += units
            try:
                result = original_consume(budget, units)
            except BaseException as error:
                entry["exceptional_consume_calls"] += 1
                entry["consume_exceptions"].append({
                    "type": type(error).__name__, "message": str(error),
                    "before": before, "requested_units": units,
                    "after": object.__getattribute__(budget, "work_units"),
                    "stack": budget_context(frame)})
                raise
            else:
                entry["completed_consume_calls"] += 1
                return result
            finally:
                entry["last_observed_work"] = object.__getattribute__(budget, "work_units")
                # frame references are call-local, never stored in observer records.
                del frame

        self.observed_init = observed_init
        self.observed_consume = observed_consume
        self.module._AnalysisBudget.__init__ = observed_init
        self.module._AnalysisBudget.consume = observed_consume

    def begin(self, identifier):
        require(self.current is None, "overlapping case budgets")
        self.by_id = {}
        self.current = {"case": identifier, "epochs": [], "initialization_attempts": 0,
                        "initialization_errors": []}

    def end(self):
        result = self.current
        require(result is not None, "no active case budget scope")
        self.current = None
        self.by_id = {}
        result["epoch_count"] = len(result["epochs"])
        result["requested_units_across_epochs"] = sum(e["requested_units"] for e in result["epochs"])
        result["maximum_epoch_observed_work"] = max(
            (e["last_observed_work"] for e in result["epochs"]), default=0)
        result["unscoped_events"] = self.unscoped_events
        # This is the final observed consume value, not a retained end-of-life object read.
        result["last_observed_work_is_final_consume_value"] = True
        return result

    def restore(self):
        require(self.current is None, "restore during analysis")
        intact = (self.module._AnalysisBudget.__init__ is self.observed_init
                  and self.module._AnalysisBudget.consume is self.observed_consume)
        self.module._AnalysisBudget.__init__ = self.original_init
        self.module._AnalysisBudget.consume = self.original_consume
        return bool(intact and self.module._AnalysisBudget.__init__ is self.original_init
                    and self.module._AnalysisBudget.consume is self.original_consume
                    and self.original_init.__code__ is self.original_codes[0]
                    and self.original_consume.__code__ is self.original_codes[1])


def validate_budget_metrics(metrics, identifier):
    require(type(metrics) is dict and metrics["case"] == identifier, "budget case identity")
    epochs = metrics["epochs"]
    require(type(epochs) is list and len(epochs) > 0, "original budget scope empty")
    require(type(metrics["epoch_count"]) is int and metrics["epoch_count"] == len(epochs),
            "budget epoch count")
    require(type(metrics["initialization_attempts"]) is int
            and metrics["initialization_attempts"] == len(epochs)
            and metrics["initialization_errors"] == [], "budget initialization coverage")
    require(metrics["unscoped_events"] == 0 and type(metrics["unscoped_events"]) is int
            and metrics["last_observed_work_is_final_consume_value"] is True, "budget scope gaps")
    for index, entry in enumerate(epochs, 1):
        for field in ("epoch", "initial_work", "last_observed_work", "requested_units",
                      "consume_calls", "completed_consume_calls", "exceptional_consume_calls"):
            require(type(entry[field]) is int and entry[field] >= 0, "budget integer: " + field)
        require(entry["epoch"] == index, "budget creation sequence")
        require(entry["initial_work"] + entry["requested_units"] == entry["last_observed_work"],
                "original requested work reconciliation")
        require(entry["consume_calls"] == entry["completed_consume_calls"]
                + entry["exceptional_consume_calls"], "consume completion reconciliation")
        require(len(entry["consume_exceptions"]) == entry["exceptional_consume_calls"],
                "consume exception count")
        require(type(entry["origins"]) is dict and type(entry["phase_units"]) is dict,
                "budget disjoint maps")
        require(all(type(k) is str and type(v) is dict
                    and type(v["calls"]) is int and v["calls"] >= 0
                    and type(v["units"]) is int and v["units"] >= 0
                    for k, v in entry["origins"].items()), "origin metrics types")
        require(all(type(k) is str and type(v) is int and v >= 0
                    for k, v in entry["phase_units"].items()), "phase metrics types")
        require(sum(v["units"] for v in entry["origins"].values()) == entry["requested_units"]
                and sum(v["calls"] for v in entry["origins"].values()) == entry["consume_calls"]
                and sum(entry["phase_units"].values()) == entry["requested_units"],
                "disjoint original work sums")
        require(type(entry["creation_stack"]) is list and entry["creation_stack"], "creation context")
        for event in entry["consume_exceptions"]:
            require(all(type(event[k]) is int for k in ("before", "requested_units", "after")),
                    "exception charge integers")
            require(event["before"] + event["requested_units"] == event["after"],
                    "exceptional original charge")
            require(event["type"] == "InventoryError"
                    and event["message"] == "analysis work units exceed 262144"
                    and event["after"] > CAPS["MAXIMUM_ANALYSIS_WORK_UNITS"],
                    "unchanged canonical work refusal")
    require(type(metrics["requested_units_across_epochs"]) is int
            and metrics["requested_units_across_epochs"] == sum(e["requested_units"] for e in epochs),
            "all-epoch request sum")
    require(type(metrics["maximum_epoch_observed_work"]) is int
            and metrics["maximum_epoch_observed_work"] == max(e["last_observed_work"] for e in epochs),
            "maximum epoch observed work")
    return True

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


fixtures = None


def prepare_depth_case(identifier, snapshot, source_sha):
    """Original setup and builder only; never invokes the multi-subtest method."""
    global fixtures
    test_path = snapshot / "tests/test_inventory_and_profiles.py"
    require(digest(checked(test_path).read_bytes()) == TESTS_SHA, "original c467 tests")
    if fixtures is None:
        spec = importlib.util.spec_from_file_location("rewrite_r2_original_depth_fixtures", test_path)
        require(spec is not None and spec.loader is not None, "original test import spec")
        fixtures = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = fixtures
        spec.loader.exec_module(fixtures)
    require(Path(fixtures.__file__).resolve() == test_path.resolve()
            and Path(fixtures.SNAPSHOT_ROOT).resolve() == snapshot.resolve()
            and Path(fixtures.GENERATOR_PATH).resolve()
                == (snapshot / "tools/generate_test_inventory.py").resolve(), "original fixture paths")
    case = fixtures.DesignReviewTests(DEPTH_CASES[identifier]["method"])
    case.setUp()
    module = case.generator
    require(Path(module.__file__).resolve() == (snapshot / "tools/generate_test_inventory.py").resolve()
            and digest(checked(Path(module.__file__)).read_bytes()) == source_sha,
            "fresh original setup candidate")
    require({name: getattr(module, name) for name in CAPS} == CAPS
            and all(type(getattr(module, name)) is int for name in CAPS), "fresh candidate caps")
    source = helper65_source() if identifier == "helper65" else generator70_source()
    require(type(source) is bytes and digest(source) == DEPTH_CASES[identifier]["fixture_sha256"],
            "original frozen depth source bytes")
    ast.parse(source, filename="<unexecuted-original-depth-source>")
    return case, module, source


def reserve_violations(metrics, identifier):
    """Post-execution requested-unit predicate; never calls or modifies a budget."""
    return [{"case": identifier, "epoch": entry["epoch"],
             "requested_units": entry["requested_units"],
             "initial_work": entry["initial_work"],
             "last_observed_work": entry["last_observed_work"],
             "maximum": CONTINUATION_MAXIMUM}
            for entry in metrics["epochs"]
            if entry["requested_units"] > CONTINUATION_MAXIMUM]


def validate_identity_inputs(raw_inputs, population_raw):
    require(set(raw_inputs) == set(EXTRA_INPUTS), "exact identity provenance set")
    for key, metadata in EXTRA_INPUTS.items():
        require(hashlib.sha256(raw_inputs[key]).hexdigest() == metadata["sha256"],
                "identity provenance pin: " + key)
    prior = json.loads(raw_inputs["prior_population"])
    current = json.loads(population_raw)
    require(set(current["cases"]) == set(GATE_B_IDS), "exact successor descriptors")
    for identifier in GATE_B_IDS[:8]:
        require(current["cases"][identifier] == prior["cases"][identifier],
                "unchanged original descriptor")
        reference = current["cases"][identifier]["envelope_ref"]
        require(current["envelopes"][reference] == prior["envelopes"][reference],
                "unchanged resolved envelope")
    coverage = json.loads(raw_inputs["coverage"])
    require(coverage["case_pack_sha256"] == PACK_HASHES["identity"],
            "coverage case pin")
    require(tuple(row["new_id"] for row in coverage["differences"]) == GATE_B_IDS[8:],
            "coverage selection")
    for row in coverage["differences"]:
        binding = current["cases"][row["new_id"]]
        require(row["new_source_sha256"] == binding["source"]["sha256"]
                and row["new_model_sha256"] == binding["model"]["sha256"],
                "coverage source/Model identity")
    return coverage


def project_identity_oracles(case):
    """Only the frozen Model(region) projection; never seeds the public analyzer."""
    pure = case["oracle_source"]
    require("subprocess" not in pure and "pontius" not in pure, "unsafe identity Model text")
    tree = ast.parse(pure, filename="<harmless-identity-oracle>")
    require(not any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree)),
            "identity Model cannot import")
    allowed = {name: getattr(builtins, name) for name in (
        "__build_class__", "staticmethod", "type", "str", "object",
        "ValueError", "TypeError", "KeyError", "IndexError")}
    actuals, errors = [], []
    require(tuple(w["region"] for w in case["witnesses"]) == ("true", "false", "none", "other"),
            "exact identity Model regions")
    for witness in case["witnesses"]:
        region = witness["region"]
        require(type(region) is str, "exact-string region")
        namespace = {"__builtins__": allowed, "__name__": "harmless_identity_projection"}
        exec(compile(tree, "<harmless-identity-oracle>", "exec", dont_inherit=True), namespace)
        instance = namespace["Model"](region)
        try:
            result = instance.test_static()
        except Exception as error:
            result = type(error).__name__
        actual = {"region": region, "trace": namespace["_events"], "result": result,
                  "ambient_result": list(instance.ambient_result),
                  "work_result": list(instance.work_result)}
        if actual != witness:
            errors.append({"expected": witness, "actual": actual})
        if any(event in actual["trace"] for event in case["unreachable_events"]):
            errors.append({"unreachable_event_was_reached": actual["trace"]})
        actuals.append(actual)
    return actuals, errors


class MechanismObserver:
    """Exact R1 adapter. Future fields/helpers require a separately frozen successor."""
    HOOKS = ("_c_state", "_c_fork", "_c_snapshot", "_c_copy_dict", "_c_cell_write",
             "_c_eval", "_c_statement", "_c_join", "_c_invoke", "_c_call",
             "_c_sink", "_c_review_outcomes")
    FUTURE = ("_c_identity_compare", "_c_raise_known", "_c_handle_known_exception",
              "_c_resume_generator")

    def __init__(self, module, budgets, source_sha):
        require(source_sha == ADAPTER_SOURCE_SHA, "unsupported source adapter; new review required")
        self.module, self.budgets = module, budgets
        self.originals, self.wrappers, self.codes = {}, {}, {}
        self.by_state_id, self.events, self.errors = {}, [], []
        self.counters, self.copy_counts, self.stack = {}, {}, []
        self.birth_serial, self.span_serial = 0, 0
        self.depth_origin = None
        self.restored = False

    def error(self, stage, error):
        self.errors.append({"stage": stage, "type": type(error).__name__, "message": str(error)})

    def state_birth(self, state, create=False):
        require(type(state) is self.module._CState, "adapter exact state")
        key = id(state)
        if create:
            self.birth_serial += 1
            self.by_state_id[key] = self.birth_serial
        require(key in self.by_state_id, "unobserved state allocation")
        return self.by_state_id[key]

    def value(self, value):
        if type(value) is self.module._CAtom:
            kind = object.__getattribute__(value, "kind")
            require(type(kind) is str, "atom kind")
            data = object.__getattribute__(value, "data")
            if kind == "literal" and type(data) in (type(None), bool, int, str):
                return {"kind": "literal", "type": type(data).__name__, "value": data}
            if kind == "literal" and type(data) is float:
                return {"kind": "literal-float", "finite": data == data and abs(data) != float("inf")}
            return {"kind": kind}
        if type(value) is self.module._CRef:
            number = object.__getattribute__(value, "object_id")
            require(type(number) is int, "object reference integer")
            return {"kind": "ref", "object_id": number}
        require(type(value) is self.module._CChoice, "adapter exact value")
        alternatives = object.__getattribute__(value, "alternatives")
        require(type(alternatives) is tuple, "choice tuple")
        return {"kind": "choice", "alternatives": len(alternatives)}

    def outcomes(self, results):
        require(type(results) is tuple, "original outcome tuple")
        answer = []
        for outcome in results:
            require(type(outcome) is self.module._COutcome, "adapter exact outcome")
            control = object.__getattribute__(outcome, "control")
            legacy = object.__getattribute__(outcome, "exception_tag")
            require(type(control) is str and (legacy is None or type(legacy) is str), "control fields")
            answer.append({"birth": self.state_birth(object.__getattribute__(outcome, "state")),
                           "control": control, "legacy_exception_tag": legacy,
                           "value": self.value(object.__getattribute__(outcome, "result"))})
        return answer

    def emit(self, kind, span, **fields):
        self.events.append({"n": len(self.events) + 1, "kind": kind,
                            "span": span["span"], "epoch": span["epoch"],
                            "site": span["site"], **fields})

    def start(self, name, args, kwargs, caller):
        self.span_serial += 1
        ctx = args[0] if args else kwargs["ctx"]
        budget = object.__getattribute__(ctx, "budget")
        entry = self.budgets.by_id.get(id(budget))
        require(entry is not None, "mechanism without observed original budget")
        path = object.__getattribute__(ctx, "path")
        require(type(path) is str, "context path")
        site = self.stack[-1]["site"] if self.stack else None
        if name in ("_c_eval", "_c_statement"):
            node = args[3] if len(args) > 3 else kwargs["node"]
            site = {"path": path, "kind": type(node).__name__,
                    "line": int(getattr(node, "lineno", 0)),
                    "column": int(getattr(node, "col_offset", 0))}
        elif name in ("_c_invoke", "_c_call", "_c_sink"):
            index = 2 if name == "_c_sink" else 3
            node = args[index] if len(args) > index else kwargs["call"]
            site = {"path": path, "kind": type(node).__name__,
                    "line": int(getattr(node, "lineno", 0)),
                    "column": int(getattr(node, "col_offset", 0))}
        statement = next((s["span"] for s in reversed(self.stack) if s["name"] == "_c_statement"), None)
        span = {"span": self.span_serial, "name": name, "epoch": entry["epoch"],
                "budget_id": id(budget), "requested_before": entry["requested_units"],
                "site": site, "statement_span": statement, "caller": caller}
        if name in ("_c_fork", "_c_snapshot", "_c_cell_write"):
            state = args[1] if len(args) > 1 else kwargs["state"]
            span["birth"] = self.state_birth(state)
        if name == "_c_cell_write":
            cell = args[2] if len(args) > 2 else kwargs["cell"]
            value = args[3] if len(args) > 3 else kwargs["value"]
            require(type(cell) is self.module._CCellRef, "adapter exact cell")
            activation, variable = object.__getattribute__(cell, "activation_id"), object.__getattribute__(cell, "name")
            require(type(activation) is int and type(variable) is str, "cell scalar route")
            span.update({"activation": activation, "variable": variable, "value": self.value(value)})
        if name == "_c_copy_dict":
            source = args[1] if len(args) > 1 else kwargs["source"]
            require(type(source) is dict, "adapter copy source is exact dict")
            span["entries"] = len(source)
        if name == "_c_join":
            supplied = args[1] if len(args) > 1 else kwargs["alternatives"]
            span["supplied_count"] = len(supplied) if type(supplied) in (list, tuple) else None
        if name == "_c_invoke":
            helper_path = object.__getattribute__(ctx, "helper_path")
            require(type(helper_path) is tuple, "helper context tuple")
            span["helper_depth"] = len(helper_path)
        row = self.counters.setdefault(name, {"attempts": 0, "completed": 0, "raised": 0,
                                               "inclusive_requested_units": 0})
        row["attempts"] += 1
        self.stack.append(span)
        return span

    def finish(self, span, args, kwargs, result, failure):
        require(self.stack and self.stack[-1] is span, "mechanism nesting")
        try:
            name = span["name"]
            entry = self.budgets.by_id.get(span["budget_id"])
            require(entry is not None and entry["epoch"] == span["epoch"], "current epoch changed")
            units = entry["requested_units"] - span["requested_before"]
            require(type(units) is int and units >= 0, "span requested units")
            row = self.counters[name]
            row["inclusive_requested_units"] += units
            row["raised" if failure is not None else "completed"] += 1
            if name == "_c_copy_dict":
                key = str(span["epoch"]) + "|" + span["caller"] + "|" + str(span["entries"])
                copy = self.copy_counts.setdefault(key, {"epoch": span["epoch"], "caller": span["caller"],
                    "entries": span["entries"], "attempts": 0, "completed": 0,
                    "attempted_entries": 0, "completed_entries": 0})
                copy["attempts"] += 1
                copy["attempted_entries"] += span["entries"]
                if failure is None:
                    copy["completed"] += 1
                    copy["completed_entries"] += span["entries"]
            if failure is not None:
                if (name == "_c_invoke" and self.depth_origin is None
                        and isinstance(failure, self.module.InventoryError)
                        and str(failure) == "analysis helper depth exceeds 64"):
                    self.depth_origin = span["span"]
                    self.emit("depth_rejection", span, depth_kind="helper",
                              incoming_depth=span["helper_depth"], message=str(failure))
                return
            if name == "_c_state":
                self.emit("birth", span, birth=self.state_birth(result, True))
            elif name == "_c_fork":
                self.emit("fork", span, parent=span["birth"], birth=self.state_birth(result, True))
            elif name == "_c_snapshot":
                require(type(result) is self.module._CView, "snapshot view")
                self.emit("snapshot", span, birth=span["birth"])
            elif name == "_c_cell_write":
                require(type(result) is bool, "cell write result")
                if result:
                    self.emit("write", span, birth=span["birth"], activation=span["activation"],
                              variable=span["variable"], value=span["value"])
            elif name == "_c_join":
                self.emit("join", span, supplied_count=span["supplied_count"],
                          statement_span=span["statement_span"], outcomes=self.outcomes(result))
            elif name == "_c_eval" and span["site"]["kind"] in ("Compare", "GeneratorExp"):
                self.emit("evaluation_exit", span, outcomes=self.outcomes(result))
            elif name == "_c_statement" and span["site"]["kind"] in ("If", "Try", "Raise"):
                self.emit("statement_exit", span, outcomes=self.outcomes(result))
            elif name == "_c_sink":
                self.emit("sink_exit", span, outcomes=self.outcomes(result))
            elif name == "_c_review_outcomes":
                supplied = args[1] if len(args) > 1 else kwargs["outcomes"]
                self.emit("review_exit", span, owned=kwargs.get("owned"),
                          outcomes=self.outcomes(supplied))
        finally:
            self.stack.pop()

    def wrap(self, name, original):
        observer = self
        def observed(*args, **kwargs):
            span = None
            try:
                frame = sys._getframe(1)
                caller = frame.f_code.co_name
                del frame
                span = observer.start(name, args, kwargs, caller)
            except Exception as error:
                observer.error("before:" + name, error)
            try:
                result = original(*args, **kwargs)
            except BaseException as error:
                if span is not None:
                    try:
                        observer.finish(span, args, kwargs, None, error)
                    except Exception as observation_error:
                        observer.error("after-error:" + name, observation_error)
                raise
            else:
                if span is not None:
                    try:
                        observer.finish(span, args, kwargs, result, None)
                    except Exception as observation_error:
                        observer.error("after:" + name, observation_error)
                return result
        return observed

    def install(self):
        require(not any(name in vars(self.module) for name in self.FUTURE),
                "R1-only adapter cannot guess future hooks")
        try:
            for name in self.HOOKS:
                original = vars(self.module).get(name)
                require(type(original) is type(self.install.__func__)
                        and original.__module__ == self.module.__name__
                        and original.__name__ == name, "exact baseline callable: " + name)
                wrapped = self.wrap(name, original)
                self.originals[name], self.wrappers[name] = original, wrapped
                self.codes[name] = original.__code__
                setattr(self.module, name, wrapped)
        except BaseException:
            for name, original in self.originals.items():
                setattr(self.module, name, original)
            raise

    def restore(self):
        intact = all(vars(self.module).get(name) is wrapper for name, wrapper in self.wrappers.items())
        for name, original in self.originals.items():
            setattr(self.module, name, original)
        self.restored = intact and all(vars(self.module).get(name) is original
                                      for name, original in self.originals.items()) and all(
            original.__code__ is self.codes[name] for name, original in self.originals.items())
        return self.restored

    def result(self):
        if self.stack:
            self.errors.append({"stage": "end", "type": "IncompleteSpan",
                                "message": "mechanism nesting not closed"})
        return {"schema": "pontius-rewrite-r2-identity-mechanism-v1",
                "source_sha256": ADAPTER_SOURCE_SHA, "adapter": "r1-baseline-only",
                "availability": dict(MECHANISM_AVAILABILITY),
                "original_methods_restored": self.restored, "errors": self.errors,
                "counters": self.counters, "copy_counts": list(self.copy_counts.values()),
                "events": self.events, "inclusive_spans_are_not_disjoint_totals": True,
                "legacy_tags_are_not_known_raises": True}


def validate_mechanism(metrics, identifier, coverage, budget_metrics):
    """Validate baseline scalar evidence; unavailable future roles cannot pass."""
    require(type(metrics) is dict and metrics["schema"] == "pontius-rewrite-r2-identity-mechanism-v1",
            "mechanism schema")
    require(metrics["source_sha256"] == ADAPTER_SOURCE_SHA and metrics["adapter"] == "r1-baseline-only",
            "exact baseline source adapter")
    require(metrics["availability"] == MECHANISM_AVAILABILITY
            and all(type(v) is bool for v in metrics["availability"].values()), "mechanism availability")
    require(metrics["original_methods_restored"] is True
            and metrics["inclusive_spans_are_not_disjoint_totals"] is True
            and metrics["legacy_tags_are_not_known_raises"] is True, "mechanism restoration/limits")
    require(type(metrics["errors"]) is list and type(metrics["events"]) is list
            and type(metrics["counters"]) is dict and type(metrics["copy_counts"]) is list,
            "mechanism record containers")
    epoch_ids = {e["epoch"] for e in budget_metrics["epochs"]} if budget_metrics is not None else set()
    for name, count in metrics["counters"].items():
        require(name in BASELINE_HOOKS and set(count) ==
                {"attempts", "completed", "raised", "inclusive_requested_units"}, "hook counter shape")
        require(all(type(n) is int and n >= 0 for n in count.values()), "hook counter integers")
        require(count["attempts"] == count["completed"] + count["raised"], "hook completion partition")
    for copy in metrics["copy_counts"]:
        require(copy["epoch"] in epoch_ids and type(copy["caller"]) is str
                and all(type(copy[k]) is int and copy[k] >= 0 for k in
                        ("entries", "attempts", "completed", "attempted_entries", "completed_entries")),
                "copy scalar fields")
        require(copy["completed"] <= copy["attempts"]
                and copy["attempted_entries"] == copy["entries"] * copy["attempts"]
                and copy["completed_entries"] == copy["entries"] * copy["completed"],
                "attempted/completed copy accounting")
    states, forks, writes, births, helper_rejections = {}, 0, 0, 0, []
    joins, sinks = [], []
    for ordinal, event in enumerate(metrics["events"], 1):
        require(type(event) is dict and type(event["n"]) is int and event["n"] == ordinal
                and type(event["span"]) is int and event["span"] > 0
                and type(event["epoch"]) is int and event["epoch"] in epoch_ids, "ordered event identity")
        site = event["site"]
        require(site is None or (type(site) is dict and type(site["path"]) is str
                and type(site["kind"]) is str and type(site["line"]) is int
                and type(site["column"]) is int), "scalar source site")
        kind = event["kind"]
        if kind == "birth":
            require(type(event["birth"]) is int and event["birth"] > 0 and event["birth"] not in states,
                    "fresh state birth")
            states[event["birth"]] = {}
            births += 1
        elif kind == "fork":
            require(type(event["birth"]) is int and event["birth"] > 0 and event["birth"] not in states
                    and type(event["parent"]) is int and event["parent"] in states, "fork lineage")
            # Copy the completed-write facts NOW, at the fork ordinal, not after replay.
            states[event["birth"]] = dict(states[event["parent"]])
            births += 1
            forks += 1
        elif kind == "write":
            require(event["birth"] in states and type(event["activation"]) is int
                    and type(event["variable"]) is str and type(event["value"]) is dict, "completed write")
            states[event["birth"]][(event["activation"], event["variable"])] = event["value"]
            writes += 1
        elif kind == "snapshot":
            require(event["birth"] in states, "snapshot live birth")
        elif kind in ("join", "evaluation_exit", "statement_exit", "sink_exit", "review_exit"):
            require(type(event["outcomes"]) is list, "outcome projections")
            for outcome in event["outcomes"]:
                require(type(outcome) is dict and outcome["birth"] in states
                        and type(outcome["control"]) is str
                        and (outcome["legacy_exception_tag"] is None
                             or type(outcome["legacy_exception_tag"]) is str)
                        and type(outcome["value"]) is dict, "scalar outcome")
            if kind == "join":
                require(event["supplied_count"] is None or
                        type(event["supplied_count"]) is int and event["supplied_count"] >= 0,
                        "supplied join count")
                joins.append(event)
            if kind == "sink_exit":
                sinks.append(event)
            if kind == "review_exit":
                require(type(event["owned"]) is bool, "review ownership")
        elif kind == "depth_rejection":
            require(event["depth_kind"] == "helper" and type(event["incoming_depth"]) is int
                    and event["incoming_depth"] > 64
                    and event["message"] == "analysis helper depth exceeds 64", "original helper depth")
            helper_rejections.append(event)
        else:
            raise RuntimeError("unrecognized baseline mechanism event")
    require(len(helper_rejections) <= 1, "propagation is not another depth origin")
    complete = not metrics["errors"]
    required, unavailable, predicates = [], [], {}
    if identifier.startswith("identity-"):
        row = next(r for r in coverage["differences"] if r["new_id"] == identifier)
        outer_line = row["source_identity_lines"][0]
        leaf_joins = [e for e in joins if e["site"] is not None
                      and e["site"]["kind"] == "If" and e["site"]["line"] == outer_line
                      and e["supplied_count"] == 4 and len(e["outcomes"]) == 4
                      and len({o["birth"] for o in e["outcomes"]}) == 4
                      and all(o["control"] in ("normal", "raise") for o in e["outcomes"])]
        required = ["identity_decisions", "four_leaf_join", "alternative_sink_occurrences"]
        unavailable = ["identity_decisions", "alternative_sink_occurrences"]
        predicates = {"identity_decisions": "unavailable",
                      "four_leaf_join": bool(leaf_joins) if complete else "incomplete",
                      "alternative_sink_occurrences": "unavailable"}
        if "d2-exceptional" in identifier:
            required += ["work_raise_handler_pairs"]
            unavailable += ["work_raise_handler_pairs"]
            predicates["work_raise_handler_pairs"] = "unavailable"
    elif identifier == "generator70":
        required, unavailable = ["deferred_depth_origin"], ["deferred_depth_origin"]
        predicates = {"deferred_depth_origin": "unavailable"}
    elif identifier == "helper65":
        required = ["helper_depth_origin"]
        predicates = {"helper_depth_origin": bool(helper_rejections) if complete else "incomplete"}
    return {"complete": complete, "required": required, "unavailable": unavailable,
            "predicates": predicates,
            "met": complete and not unavailable and all(v is True for v in predicates.values()),
            "lineage": {"births": births, "forks": forks, "completed_writes": writes,
                        "inheritance_at_fork_ordinal": True},
            "helper_depth_origins": len(helper_rejections),
            "future_known_raises_handlers_resumes": "unavailable",
            "sink_helper_normal_returns": sum(sum(o["control"] == "normal" for o in e["outcomes"])
                                              for e in sinks)}


def main():
    global generator
    require(len(sys.argv) == 4, "usage: probe SLOT MANIFEST_SHA ENVIRONMENT_SHA")
    slot, manifest_sha, environment_sha = sys.argv[1:]
    require(slot in SLOTS, "slot")
    executable, version = SLOTS[slot]
    require(sys.implementation.name == "cpython" and sys.version_info[:3] == version,
            "wrong real interpreter")
    require(Path(sys.executable).resolve() == checked(Path(executable)).resolve(), "wrong executable")
    require(sys.dont_write_bytecode and sys.flags.safe_path and sys.flags.no_user_site
            and not sys.flags.optimize and not sys.flags.isolated and not sys.flags.ignore_environment
            and not sys.flags.no_site, "requires child -B -P and scrubbed no-user-site environment")
    snapshot = Path.cwd()
    require(snapshot.is_relative_to(Path(r"D:\pontius-snapshots")), "not D-local snapshot")
    require(os.environ.get("PYTHONPATH") == str(snapshot / "src"), "PYTHONPATH")
    require(os.environ.get("PYTHONHASHSEED") == "0", "fixed hash seed")
    require(os.environ.get("PONTIUS_GIT") == r"C:\Program Files\Git\cmd\git.exe", "Git")
    actual_environment = dict(os.environ)
    require(digest(canonical(actual_environment)) == environment_sha, "exact child environment")
    payload = snapshot / PAYLOAD
    manifest_raw = checked(payload / "manifest.json").read_bytes()
    require(digest(manifest_raw) == manifest_sha, "manifest pin")
    manifest = json.loads(manifest_raw)
    require(len(manifest) == 1761 + len(BASE_PAYLOAD_NAMES) + (5 if slot == "314" else 0), "manifest count")
    hashes(snapshot, manifest)
    run = json.loads(checked(payload / "run.json").read_bytes())
    require(run["schema"] == SCHEMA and run["slot"] == slot, "run config")
    source_sha = run["generator_sha256"]
    require(source_sha == ADAPTER_SOURCE_SHA and run["adapter"] == ADAPTER_ID
            and run["adapter_source_sha256"] == ADAPTER_SOURCE_SHA
            and run["extra_input_sha256"] == EXTRA_HASHES
            and run["reserve_basis"] == RESERVE_BASIS, "released source adapter/provenance")
    require(type(source_sha) is str and len(source_sha) == 64
            and all(c in "0123456789abcdef" for c in source_sha), "candidate digest")
    require(run["pack_sha256"] == PACK_HASHES
            and run["plan_sha256"] == PLAN_SHA and run["population_sha256"] == POPULATION_SHA
            and run["observer_map_sha256"] == OBSERVER_MAP_SHA
            and run["tests_sha256"] == TESTS_SHA
            and run["depth_provenance_sha256"] == DEPTH_PROVENANCE_SHA
            and run["continuation_work_maximum"] == CONTINUATION_MAXIMUM, "run input identity")
    probe_sha = digest(checked(Path(__file__).absolute()).read_bytes())
    require(probe_sha == run["probe_sha256"], "probe pin")
    require(digest(checked(payload / "control.py").read_bytes()) == run["control_sha256"], "control pin")
    require(digest(checked(payload / "plan.md").read_bytes()) == PLAN_SHA, "plan bytes")
    require(digest(checked(payload / "observer-map.json").read_bytes()) == OBSERVER_MAP_SHA,
            "observer map bytes")
    require(digest(checked(payload / "depth-provenance.py").read_bytes()) == DEPTH_PROVENANCE_SHA,
            "depth provenance source bytes")
    require(digest(checked(snapshot / "tests/test_inventory_and_profiles.py").read_bytes()) == TESTS_SHA,
            "original depth test module bytes")
    population_raw = checked(payload / "population.json").read_bytes()
    require(digest(population_raw) == POPULATION_SHA, "frozen population bytes")
    coverage = validate_identity_inputs(
        {key: checked(payload / item["payload"]).read_bytes() for key, item in EXTRA_INPUTS.items()},
        population_raw)
    source_path = snapshot / "tools/generate_test_inventory.py"
    require(digest(checked(source_path).read_bytes()) == source_sha
            and digest(checked(payload / "retained-source.py").read_bytes()) == source_sha, "exact retained candidate")
    source_text = checked(source_path).read_bytes().decode("utf-8")
    source_tree = ast.parse(source_text, filename=str(source_path))
    budgets = [n for n in source_tree.body if type(n) is ast.ClassDef and n.name == "_AnalysisBudget"]
    require(len(budgets) == 1, "single original budget class")
    consumes = [n for n in budgets[0].body if type(n) is ast.FunctionDef and n.name == "consume"]
    require(len(consumes) == 1 and digest(ast.get_source_segment(source_text, consumes[0]).encode())
            == CONSUME_SEGMENT_SHA, "original consume source unchanged")
    del source_tree, budgets, consumes
    sys.stdout.reconfigure(newline="\n")
    sys.stderr.reconfigure(newline="\n")
    identity = {"executable": sys.executable, "implementation": sys.implementation.name,
                "version": sys.version, "version_info": list(sys.version_info[:3]),
                "cwd": str(snapshot), "flags": str(sys.flags), "environment": actual_environment,
                "manifest_sha256": manifest_sha, "verified_files": len(manifest),
                "generator_sha256": source_sha, "probe_sha256": probe_sha,
                "adapter": ADAPTER_ID, "adapter_source_sha256": ADAPTER_SOURCE_SHA,
                "extra_input_sha256": EXTRA_HASHES}
    print(json.dumps({"identity_before_imports": identity}), flush=True)
    require(not any(n == "pontius" or n.startswith("pontius.") for n in sys.modules),
            "Pontius imported before generator")
    resolution = importlib.util.find_spec("pontius")
    require(resolution is not None and resolution.origin is not None
            and Path(resolution.origin).resolve() == (snapshot / "src/pontius/__init__.py").resolve(),
            "wrong read-only package resolution")
    cases = load_cases({scope: checked(payload / metadata["file"]).read_bytes()
                        for scope, metadata in PACKS.items()}, population_raw)
    spec = importlib.util.spec_from_file_location("rewrite_r2_gate_b_generator", source_path)
    require(spec is not None and spec.loader is not None, "generator import spec")
    generator = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = generator
    spec.loader.exec_module(generator)


    require({name: getattr(generator, name) for name in CAPS} == CAPS
            and all(type(getattr(generator, name)) is int for name in CAPS), "caps changed")
    semantic_failures, oracle_errors, analyzer_errors, accounting_errors = [], [], [], []
    continuation_failures, mechanism_failures, mechanism_errors = [], [], []
    mechanism_restorations = []
    attempted, returned_receipts, expected_depth_errors, projections = 0, 0, 0, 0
    for scope, case in cases:
        identifier = case["id"]
        is_depth = scope == "depth"
        depth_case, active_generator = None, generator
        if is_depth:
            depth_case, active_generator, source = prepare_depth_case(identifier, snapshot, source_sha)
            actuals, oracle_passed, oracle_error = [], True, None
        else:
            source = case["source"].encode("utf-8")
            actuals, oracle_passed, oracle_error = [], False, None
            try:
                if scope == "storage":
                    actual, oracle_passed = storage_oracle(case)
                    actuals = [actual]
                else:
                    actuals, errors = (project_identity_oracles(case) if scope == "identity"
                                       else project_oracles(case))
                    oracle_passed = not errors
                projections += len(actuals)
            except Exception as error:
                oracle_error = {"type": type(error).__name__, "message": str(error)}
        review, analyzer_error, metrics, accounting_error = None, None, None, None
        public_exception, depth_match, methods_restored = None, False, True
        violations, mechanism, mechanism_verdict, mechanism_error = [], None, None, None
        if not oracle_passed:
            oracle_errors.append(identifier)
        else:
            observer = BudgetObserver(active_generator)
            observer.install()
            observer.begin(identifier)
            mechanism_observer = MechanismObserver(active_generator, observer, source_sha)
            mechanism_observer.install()
            try:
                attempted += 1
                try:
                    if is_depth:
                        review = depth_case._review(sources={"tests/test_review.py": source})
                    else:
                        review = (storage_public_review(generator, source) if scope == "storage"
                                  else public_review(source))
                except Exception as error:
                    public_exception = {"type": type(error).__name__, "message": str(error),
                                        "is_inventory_error": isinstance(error, active_generator.InventoryError)}
                    depth_match = bool(is_depth and public_exception["is_inventory_error"]
                                       and re.search(DEPTH_CASES[identifier]["regex"], str(error)))
                    if depth_match:
                        expected_depth_errors += 1
                    else:
                        analyzer_error = public_exception
                        analyzer_errors.append(identifier)
                finally:
                    mechanism_observer.restore()
                    mechanism = mechanism_observer.result()
                    mechanism_restorations.append(mechanism["original_methods_restored"])
                    metrics = observer.end()
            finally:
                if observer.current is not None:
                    metrics = observer.end()
                methods_restored = observer.restore()
            require(methods_restored, "original budget methods not restored")
            require({name: getattr(active_generator, name) for name in CAPS} == CAPS
                    and all(type(getattr(active_generator, name)) is int for name in CAPS),
                    "active candidate caps changed")
            try:
                validate_budget_metrics(metrics, identifier)
                violations = reserve_violations(metrics, identifier)
                continuation_failures.extend(violations)
            except Exception as error:
                accounting_error = {"type": type(error).__name__, "message": str(error)}
                accounting_errors.append(identifier)
            try:
                mechanism_verdict = validate_mechanism(mechanism, identifier, coverage, metrics)
                if not mechanism_verdict["met"]:
                    mechanism_failures.append(identifier)
            except Exception as error:
                mechanism_error = {"type": type(error).__name__, "message": str(error)}
                mechanism_errors.append(identifier)
        rows = review["receipt"]["expanded_rows"] if review is not None else []
        argv = [row["argv"] for row in rows if row["capability_kind"] == "subprocess"]
        blockers = review["unresolved_dynamic_blockers"] if review is not None else []
        if review is not None:
            returned_receipts += 1
        semantic_ok = bool(oracle_passed and
                           (depth_match if is_depth else
                            review is not None and public_verdict(scope, case, argv, blockers)))
        if not semantic_ok:
            semantic_failures.append(identifier)
        print(json.dumps({
            "rewrite_gate_b_case": identifier, "original_pack": scope,
            "classification": case["classification"], "source_sha256": digest(source),
            "oracle_sha256": None if is_depth else digest(case["oracle_source"].encode("utf-8")),
            "unreachable_events": [] if is_depth else case["unreachable_events"],
            "expected_projections": ([] if is_depth else
                                     [case["expected"]] if scope == "storage" else case["witnesses"]),
            "required_argv": None if is_depth else case["required_argv"] if scope == "storage" else [["-m", "fixed"]],
            "oracle_actuals": actuals, "oracle_passed": oracle_passed, "oracle_error": oracle_error,
            "depth_expectation": DEPTH_CASES[identifier]["regex"] if is_depth else None,
            "expected_depth_error": depth_match, "public_exception": public_exception,
            "analyzer_error": analyzer_error, "argv": argv, "expanded_rows": rows,
            "blockers": blockers, "semantic_passed": semantic_ok,
            "receipt_sha256": digest(canonical(review["receipt"])) if review is not None else None,
            "budget_metrics": metrics, "accounting_error": accounting_error,
            "original_methods_restored": methods_restored, "reserve_violations": violations,
            "mechanism": mechanism, "mechanism_verdict": mechanism_verdict,
            "mechanism_error": mechanism_error,
        }, allow_nan=False), flush=True)
    require({name: getattr(generator, name) for name in CAPS} == CAPS
            and all(type(getattr(generator, name)) is int for name in CAPS), "caps changed during run")
    hashes(snapshot, manifest)
    require(digest(checked(payload / "manifest.json").read_bytes()) == manifest_sha, "manifest changed")
    summary = {"rewrite_gate_b_summary": True, "schema": SCHEMA, "slot": slot,
               "generator_sha256": source_sha, "pack_sha256": PACK_HASHES, "probe_sha256": probe_sha,
               "plan_sha256": PLAN_SHA, "population_sha256": POPULATION_SHA,
               "observer_map_sha256": OBSERVER_MAP_SHA, "tests_sha256": TESTS_SHA,
               "depth_provenance_sha256": DEPTH_PROVENANCE_SHA,
               "adapter": ADAPTER_ID, "adapter_source_sha256": ADAPTER_SOURCE_SHA,
               "extra_input_sha256": EXTRA_HASHES, "reserve_basis": RESERVE_BASIS,
               "mechanism_failures": mechanism_failures, "mechanism_errors": mechanism_errors,
               "mechanism_ok": not mechanism_failures and not mechanism_errors,
               "mechanism_methods_restored": len(mechanism_restorations) == 12 and all(mechanism_restorations),
               "observation_complete": attempted == 12 and projections == 24 and not oracle_errors,
               "planned_cases": 12, "case_count": 12, "projections": projections,
               "attempted_analyses": attempted, "returned_receipts": returned_receipts,
               "expected_depth_errors": expected_depth_errors,
               "semantic_failures": semantic_failures, "oracle_errors": oracle_errors,
               "analyzer_errors": analyzer_errors, "accounting_errors": accounting_errors,
               "completed": attempted == 12 and returned_receipts == 10 and expected_depth_errors == 2
                            and projections == 24 and not oracle_errors
                            and not analyzer_errors and not accounting_errors,
               "classifications": {"clean": 6, "refuse": 3, "permitted-refusal": 1, "exact-depth-error": 2},
               "caps": CAPS, "original_methods_restored": True,
               "budget_scope": "all original creations/requests inside every complete public envelope",
               "observer_overhead_is_not_original_charged_work": True,
               "gate": "B", "continuation_work_maximum": CONTINUATION_MAXIMUM,
               "reserve_violations": continuation_failures,
               "reserve_ok": not accounting_errors and attempted == 12 and not continuation_failures,
               "reserve_is_postexecution_only": True, "no_wider_population_run": True}
    print(json.dumps(summary, allow_nan=False), flush=True)
    return int(bool(semantic_failures or oracle_errors or analyzer_errors
                    or accounting_errors or continuation_failures or mechanism_failures or mechanism_errors))


if __name__ == "__main__":
    raise SystemExit(main())
