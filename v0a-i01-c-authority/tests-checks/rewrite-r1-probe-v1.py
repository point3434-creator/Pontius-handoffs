"""Frozen rewrite R1 Gate A: six original public cases/eight Models; no work on import."""
import ast
import builtins
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys


PACKS = {
    "storage": {
        "file": "storage-composition-cases-v1.json",
        "sha256": "faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709",
        "schema": "pontius-storage-composition-cases-v1",
        "planned_cases": 4, "planned_projections": 4,
        "ids": ("shared-list-consumed", "shared-list-dormant",
                "class-adoption-unsafe", "class-adoption-safe"),
    },
    "name_environment": {
        "file": "name-environment-cases-v1.json",
        "sha256": "d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c",
        "schema": "pontius-engineering-name-environment-family-v1",
        "planned_cases": 24, "planned_projections": 58,
        "ids": ("hidden-cell-joined-reached", "hidden-cell-joined-dormant"),
    },
}
PACK_HASHES = {scope: metadata["sha256"] for scope, metadata in PACKS.items()}
GATE_A_IDS = tuple(name for metadata in PACKS.values() for name in metadata["ids"])
POPULATION_SHA = "3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce"

PLAN_SHA = '8cec0f3af002f04b20c82dee62d29f0601a87047249ab2dfcde5a164ca73826d'
OBSERVER_MAP_SHA = 'af8df00ceb6b02bb5730eee56754ce78badcab6102ce861d726eed704522bfbd'
CONSUME_SEGMENT_SHA = 'd910a8af42711e5130b93af9e55b8917dbd8b48433e29e1ab3cd51df63b7af5c'
PAYLOAD = ".rewrite-r1-gate-a"
SCHEMA = "pontius-rewrite-r1-gate-a-v1"
SLOTS = {
    "311": (r"D:\Pontius-tools\py311\Scripts\python.exe", (3, 11, 15)),
    "314": (r"D:\Pontius\.venv\Scripts\python.exe", (3, 14, 6)),
}
CAPS = {
    "MAXIMUM_ANALYSIS_HELPER_DEPTH": 64, "MAXIMUM_ANALYSIS_CHILD_DEPTH": 4,
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS": 4096,
    "MAXIMUM_ANALYSIS_CARDINALITY": 2147483647, "MAXIMUM_ANALYSIS_WORK_UNITS": 262144,
}


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
    require(tuple(population["gates"]["A"]["ordered_case_ids"]) == GATE_A_IDS,
            "exact Gate A selection")
    require(population["gates"]["A"]["public_analysis_count"] == 6
            and population["gates"]["A"]["independent_model_projections"] == 8,
            "frozen Gate A counts")
    require(set(raw_by_scope) == set(PACKS), "exact original pack set")
    combined = []
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
            require(hashlib.sha256(case_canonical(case)).hexdigest()
                    == binding["case_record_canonical_sha256"], "selected record binding")
            for field, target in (("source", "source"), ("oracle_source", "model")):
                value = case[field]
                require(type(value) is str and value.endswith("\n") and "\r" not in value,
                        "original source format")
                require(hashlib.sha256(value.encode("utf-8")).hexdigest()
                        == binding[target]["sha256"], "original source/model binding")
                ast.parse(value, filename="<GateA-unexecuted-source-or-Model>")
            require(case["classification"] == binding["classification"], "classification binding")
            combined.append((scope, case))
    require(tuple(case["id"] for scope, case in combined) == GATE_A_IDS, "exact Gate A order")
    require(dict(Counter(case["classification"] for scope, case in combined))
            == {"clean": 2, "refuse": 3, "permitted-refusal": 1}, "Gate A classifications")
    require(sum(1 if scope == "storage" else len(case["witnesses"])
                for scope, case in combined) == 8, "Gate A exact eight Models")
    return combined


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
    require(len(manifest) == 1770 + (5 if slot == "314" else 0), "manifest count")
    hashes(snapshot, manifest)
    run = json.loads(checked(payload / "run.json").read_bytes())
    require(run["schema"] == SCHEMA and run["slot"] == slot, "run config")
    source_sha = run["generator_sha256"]
    require(type(source_sha) is str and len(source_sha) == 64
            and all(c in "0123456789abcdef" for c in source_sha), "candidate digest")
    require(run["pack_sha256"] == PACK_HASHES
            and run["plan_sha256"] == PLAN_SHA and run["population_sha256"] == POPULATION_SHA
            and run["observer_map_sha256"] == OBSERVER_MAP_SHA, "run input identity")
    probe_sha = digest(checked(Path(__file__).absolute()).read_bytes())
    require(probe_sha == run["probe_sha256"], "probe pin")
    require(digest(checked(payload / "control.py").read_bytes()) == run["control_sha256"], "control pin")
    require(digest(checked(payload / "plan.md").read_bytes()) == PLAN_SHA, "plan bytes")
    require(digest(checked(payload / "observer-map.json").read_bytes()) == OBSERVER_MAP_SHA,
            "observer map bytes")
    population_raw = checked(payload / "population.json").read_bytes()
    require(digest(population_raw) == POPULATION_SHA, "frozen population bytes")
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
                "generator_sha256": source_sha, "probe_sha256": probe_sha}
    print(json.dumps({"identity_before_imports": identity}), flush=True)
    require(not any(n == "pontius" or n.startswith("pontius.") for n in sys.modules),
            "Pontius imported before generator")
    resolution = importlib.util.find_spec("pontius")
    require(resolution is not None and resolution.origin is not None
            and Path(resolution.origin).resolve() == (snapshot / "src/pontius/__init__.py").resolve(),
            "wrong read-only package resolution")
    cases = load_cases({scope: checked(payload / metadata["file"]).read_bytes()
                        for scope, metadata in PACKS.items()}, population_raw)
    spec = importlib.util.spec_from_file_location("rewrite_r1_gate_a_generator", source_path)
    require(spec is not None and spec.loader is not None, "generator import spec")
    generator = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = generator
    spec.loader.exec_module(generator)

    require({name: getattr(generator, name) for name in CAPS} == CAPS
            and all(type(getattr(generator, name)) is int for name in CAPS), "caps changed")
    semantic_failures, oracle_errors, analyzer_errors, accounting_errors = [], [], [], []
    analyzed, projections = 0, 0
    observer = BudgetObserver(generator)
    observer.install()
    methods_restored = False
    try:
        for scope, case in cases:
            actuals, oracle_passed, oracle_error = [], False, None
            try:
                if scope == "storage":
                    actual, oracle_passed = storage_oracle(case)
                    actuals = [actual]
                else:
                    actuals, errors = project_oracles(case)
                    oracle_passed = not errors
                projections += len(actuals)
            except Exception as error:
                oracle_error = {"type": type(error).__name__, "message": str(error)}
            review, analyzer_error, metrics, accounting_error = None, None, None, None
            if not oracle_passed:
                oracle_errors.append(case["id"])
            else:
                observer.begin(case["id"])
                try:
                    review = (storage_public_review(generator, case["source"].encode("utf-8"))
                              if scope == "storage" else public_review(case["source"].encode("utf-8")))
                    analyzed += 1
                except Exception as error:
                    analyzer_error = {"type": type(error).__name__, "message": str(error)}
                    analyzer_errors.append(case["id"])
                finally:
                    metrics = observer.end()
                try:
                    validate_budget_metrics(metrics, case["id"])
                except Exception as error:
                    accounting_error = {"type": type(error).__name__, "message": str(error)}
                    accounting_errors.append(case["id"])
            rows = review["receipt"]["expanded_rows"] if review is not None else []
            argv = [row["argv"] for row in rows if row["capability_kind"] == "subprocess"]
            blockers = review["unresolved_dynamic_blockers"] if review is not None else []
            semantic_ok = bool(oracle_passed and review is not None
                               and public_verdict(scope, case, argv, blockers))
            if not semantic_ok:
                semantic_failures.append(case["id"])
            print(json.dumps({
                "rewrite_gate_a_case": case["id"], "original_pack": scope,
                "classification": case["classification"],
                "source_sha256": digest(case["source"].encode("utf-8")),
                "oracle_sha256": digest(case["oracle_source"].encode("utf-8")),
                "unreachable_events": case["unreachable_events"],
                "expected_projections": ([case["expected"]] if scope == "storage" else case["witnesses"]),
                "required_argv": case["required_argv"] if scope == "storage" else [["-m", "fixed"]],
                "oracle_actuals": actuals, "oracle_passed": oracle_passed, "oracle_error": oracle_error,
                "analyzer_error": analyzer_error, "argv": argv, "expanded_rows": rows,
                "blockers": blockers, "semantic_passed": semantic_ok,
                "receipt_sha256": digest(canonical(review["receipt"])) if review is not None else None,
                "budget_metrics": metrics, "accounting_error": accounting_error,
            }, allow_nan=False), flush=True)
    finally:
        methods_restored = observer.restore()
    require(methods_restored, "original budget methods not restored")
    require({name: getattr(generator, name) for name in CAPS} == CAPS
            and all(type(getattr(generator, name)) is int for name in CAPS), "caps changed during run")
    hashes(snapshot, manifest)
    require(digest(checked(payload / "manifest.json").read_bytes()) == manifest_sha, "manifest changed")
    summary = {"rewrite_gate_a_summary": True, "schema": SCHEMA, "slot": slot,
               "generator_sha256": source_sha, "pack_sha256": PACK_HASHES, "probe_sha256": probe_sha,
               "plan_sha256": PLAN_SHA, "population_sha256": POPULATION_SHA,
               "observer_map_sha256": OBSERVER_MAP_SHA, "planned_cases": 6, "case_count": 6,
               "projections": projections, "analyzed_cases": analyzed,
               "semantic_failures": semantic_failures, "oracle_errors": oracle_errors,
               "analyzer_errors": analyzer_errors, "accounting_errors": accounting_errors,
               "completed": analyzed == 6 and projections == 8 and not oracle_errors
                            and not analyzer_errors and not accounting_errors,
               "classifications": {"clean": 2, "refuse": 3, "permitted-refusal": 1}, "caps": CAPS,
               "original_methods_restored": methods_restored,
               "budget_scope": "all original creations/requests inside every complete public envelope",
               "observer_overhead_is_not_original_charged_work": True,
               "gate": "A", "GateB_not_run": True}
    print(json.dumps(summary, allow_nan=False), flush=True)
    return int(bool(semantic_failures or oracle_errors or analyzer_errors or accounting_errors))


if __name__ == "__main__":
    raise SystemExit(main())
