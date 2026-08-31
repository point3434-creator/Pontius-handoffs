"""Rewrite R2 Gate B snapshot control; authoring is not run permission.

Run this controller with exact floor Python 3.11.15 and -I -S -B -P.
Arguments: LABEL SLOT RETAINED_SOURCE_ABSOLUTE SOURCE_SHA --control-sha256 SHA --worktree-sha256 SHA
For SLOT=314 also supply --floor-receipt ABSOLUTE --floor-sha256 SHA.
An absolute T candidate plus its exact SHA is required. The independent W watch stays v20.
Child uses -B -P, scrubbed environment, snapshot/src PYTHONPATH, hash seed 0.
"""
import argparse
import ast
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import uuid

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
CHECKS = ROOT / "tests-checks"
REPOSITORY = Path(r"D:\Pontius")
SNAPSHOTS = Path(r"D:\pontius-snapshots")
GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
BASE = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
BASE_GENERATOR_SHA = "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
WATCH = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1\tools\generate_test_inventory.py")
WATCH_SHA = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
PROBE = CHECKS / "rewrite-r2-identity-probe-v2.py"
PROBE_SHA = 'c654355be85a85fe53bb00c7e55201e6ccc969edb227d4159b26d415669bee38'

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

PLAN = CHECKS / "rewrite-r2-identity-plan-v2.md"
PLAN_SHA = '4351e0f61ff81f6fbb1800df669a642501f10c40e72de80430d4d396b0b6e1db'
OBSERVER_MAP_SHA = '5463f81a8c3714e0970585c6b4b2eb9dd2bd547105c4ae6a8f9f53f0a08d699c'
OBSERVER_MAP = CHECKS / "rewrite-r2-identity-observer-map-v2.json"
POPULATION = CHECKS / "rewrite-r2-identity-population-v2.json"
DEPTH_PROVENANCE = ROOT / "engineer-depth-budget-probe-v3.py"
CORE_WATCH = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-core-v1\tools\generate_test_inventory.py")
SLOTS = {
    "311": (Path(r"D:\Pontius-tools\py311\Scripts\python.exe"), (3, 11, 15)),
    "314": (Path(r"D:\Pontius\.venv\Scripts\python.exe"), (3, 14, 6)),
}
CAPS = {
    "MAXIMUM_ANALYSIS_HELPER_DEPTH": 64, "MAXIMUM_ANALYSIS_CHILD_DEPTH": 4,
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS": 4096,
    "MAXIMUM_ANALYSIS_CARDINALITY": 2147483647, "MAXIMUM_ANALYSIS_WORK_UNITS": 262144,
}
SCHEMA = "pontius-rewrite-r2-identity-v2"
PAYLOAD = ".rewrite-r2-identity-v2"
GENERATOR = "tools/generate_test_inventory.py"
TIMEOUT = 60  # Infrastructure watchdog, not a new analyzer admission cap.


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


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("utf-8")


def valid_digest(value):
    return type(value) is str and re.fullmatch("[0-9a-f]{64}", value) is not None


def checked(path, directory=False):
    path = Path(path)
    require(path.is_absolute() and ".." not in path.parts, "unsafe absolute path")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        require(not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT,
                "reparse path: " + str(ancestor))
        if ancestor != path:
            require(stat.S_ISDIR(info.st_mode), "non-directory ancestor")
    require(stat.S_ISDIR(path.stat().st_mode) if directory else stat.S_ISREG(path.stat().st_mode),
            "wrong path kind: " + str(path))
    return path


def create(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def write_json(stream, value):
    stream.seek(0)
    stream.write((json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode())
    stream.truncate()
    stream.flush()
    os.fsync(stream.fileno())


def environment(temp, snapshot=None):
    windows = checked(os.environ["SYSTEMROOT"], True)
    system = checked(windows / "System32", True)
    result = {
        "SYSTEMROOT": str(windows), "WINDIR": str(windows),
        "COMSPEC": str(checked(system / "cmd.exe")), "PATH": str(system),
        "TEMP": str(temp), "TMP": str(temp), "PONTIUS_GIT": str(checked(GIT)),
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "NUL", "GIT_CONFIG_SYSTEM": "NUL",
        "GIT_ATTR_NOSYSTEM": "1", "PYTHONNOUSERSITE": "1",
    }
    if snapshot is not None:
        result.update({"PYTHONPATH": str(snapshot / "src"), "PYTHONHASHSEED": "0"})
    return result


def git(repository, temp, *arguments):
    command = [str(checked(GIT)), "-c", "core.autocrlf=false", "-c", "core.hooksPath=NUL",
               "-c", "init.templateDir=", "-c", "core.attributesFile=NUL", "-c", "core.fsmonitor=false",
               "-C", str(repository), *arguments]
    return subprocess.run(command, cwd=repository, env=environment(temp), check=True,
                          capture_output=True, timeout=TIMEOUT,
                          creationflags=subprocess.CREATE_NO_WINDOW).stdout


def file_hashes(snapshot, names):
    result = {}
    for name in names:
        relative = Path(name)
        require(not relative.is_absolute() and not relative.drive and ".." not in relative.parts,
                "unsafe manifest path")
        result[name] = sha(checked(snapshot / relative).read_bytes())
    return result



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


def validate_lifecycle(record):
    require(type(record) is dict and record["schema"] == "pontius-r2-observer-lifecycle-v1",
            "observer lifecycle schema")
    for key in ("acquired", "closed", "budget_methods_restored",
                "mechanism_methods_restored", "complete"):
        require(type(record[key]) is bool, "lifecycle exact Boolean: " + key)
    require(type(record["events"]) is list and type(record["errors"]) is list
            and type(record["acquisition_stage"]) is str, "lifecycle scalar containers")
    for event in record["events"]:
        require(type(event) is dict and set(event) == {"stage", "completed"}
                and type(event["stage"]) is str and type(event["completed"]) is bool,
                "lifecycle event")
    for error in record["errors"]:
        require(type(error) is dict and set(error) == {"stage", "type", "message"}
                and all(type(value) is str for value in error.values()), "lifecycle error")
    normal_stages = ["budget.construct", "budget.install", "budget.begin",
                     "mechanism.construct", "mechanism.install", "mechanism.restore",
                     "mechanism.result", "budget.end", "budget.restore"]
    normal_stages.extend("force-hook:" + name for name in BASELINE_HOOKS)
    normal_stages.extend(("force-budget:__init__", "force-budget:consume",
                          "verify-mechanism", "verify-budget"))
    structurally_complete = (
        record["acquired"] and record["closed"] and record["acquisition_stage"] == "complete"
        and record["budget_methods_restored"] and record["mechanism_methods_restored"]
        and not record["errors"] and record["events"] ==
        [{"stage": stage, "completed": True} for stage in normal_stages])
    require(record["complete"] is structurally_complete, "lifecycle completion replay")
    return structurally_complete


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


def validate_result(stdout, exit_code, setup, cases, coverage):
    require(type(exit_code) is int, "child exit exact integer")
    require(b"\r" not in stdout and stdout.endswith(b"\n"), "stdout complete LF")
    lines = stdout.splitlines()
    require(len(lines) == 14 and all(line.startswith(b"{") for line in lines),
            "exact identity/twelve-case/summary stream")
    records = [json.loads(line) for line in lines]
    require(all(type(record) is dict for record in records), "JSON record types")
    require(set(records[0]) == {"identity_before_imports"}, "first pre-import identity")
    identity = records[0]["identity_before_imports"]
    exe, version = SLOTS[setup["slot"]]
    require(identity["implementation"] == "cpython" and identity["version_info"] == list(version)
            and all(type(n) is int for n in identity["version_info"])
            and Path(identity["executable"]).resolve() == exe.resolve(), "actual child runtime")
    require(identity["cwd"] == setup["snapshot"] and identity["environment"] == setup["environment"]
            and identity["manifest_sha256"] == setup["manifest_sha256"]
            and type(identity["verified_files"]) is int
            and identity["verified_files"] == len(setup["before"])
            and identity["generator_sha256"] == setup["generator_sha256"]
            and identity["probe_sha256"] == PROBE_SHA
            and identity["adapter"] == ADAPTER_ID
            and identity["adapter_source_sha256"] == ADAPTER_SOURCE_SHA
            and identity["extra_input_sha256"] == EXTRA_HASHES, "identity context")
    require(setup["environment"] == environment(checked(Path(setup["temp"]), True),
                                                checked(Path(setup["snapshot"]), True)),
            "replayed scrubbed environment")
    expected_command = [str(exe), "-B", "-P", str(Path(setup["snapshot"]) / PAYLOAD / "probe.py"),
                        setup["slot"], setup["manifest_sha256"], sha(canonical(setup["environment"]))]
    require(setup["command"] == expected_command and type(setup["timeout_seconds"]) is int
            and setup["timeout_seconds"] == TIMEOUT, "replayed command/watchdog")
    for flag in ("dont_write_bytecode=1", "no_user_site=1", "optimize=0", "isolated=0",
                 "ignore_environment=0", "no_site=0", "safe_path=True"):
        require(flag in identity["flags"], "child flag: " + flag)

    observed = records[1:-1]
    require(tuple(record.get("rewrite_gate_b_case") for record in observed) == GATE_B_IDS,
            "exact frozen Gate B order")
    semantic_failures, oracle_errors, analyzer_errors, accounting_errors = [], [], [], []
    continuation_failures, mechanism_failures, mechanism_errors = [], [], []
    lifecycle_failures, lifecycle_errors = [], []
    mechanism_restorations = []
    attempted, returned_receipts, expected_depth_errors, projections = 0, 0, 0, 0
    for actual, (scope, expected) in zip(observed, cases, strict=True):
        identifier, is_depth = expected["id"], scope == "depth"
        require(actual["original_pack"] == scope and actual["classification"] == expected["classification"],
                "original case attribution")
        source_digest = expected["source"]["sha256"] if is_depth else sha(expected["source"].encode("utf-8"))
        model_digest = None if is_depth else sha(expected["oracle_source"].encode("utf-8"))
        expected_projections = [] if is_depth else [expected["expected"]] if scope == "storage" else expected["witnesses"]
        required_argv = None if is_depth else expected["required_argv"] if scope == "storage" else [["-m", "fixed"]]
        unreachable = [] if is_depth else expected["unreachable_events"]
        require(actual["source_sha256"] == source_digest and actual["oracle_sha256"] == model_digest,
                "original source/Model identity")
        require(actual["expected_projections"] == expected_projections
                and actual["required_argv"] == required_argv and actual["unreachable_events"] == unreachable,
                "unchanged expected projections/argv")
        require(type(actual["oracle_actuals"]) is list, "Model actual container")
        projections += len(actual["oracle_actuals"])
        oracle_ok = (actual["oracle_error"] is None and actual["oracle_actuals"] == expected_projections
                     and not any(event in witness["trace"] for witness in actual["oracle_actuals"]
                                 for event in unreachable))
        require(actual["oracle_passed"] is oracle_ok, "Model result inconsistency")
        if not oracle_ok:
            oracle_errors.append(identifier)
        else:
            attempted += 1
        error = actual["public_exception"]
        if error is not None:
            require(type(error) is dict and type(error["type"]) is str and type(error["message"]) is str
                    and type(error["is_inventory_error"]) is bool, "actual exception record")
        depth_match = bool(is_depth and error is not None and error["is_inventory_error"]
                           and re.search(DEPTH_CASES[identifier]["regex"], error["message"]))
        require(actual["expected_depth_error"] is depth_match
                and actual["depth_expectation"] == (DEPTH_CASES[identifier]["regex"] if is_depth else None),
                "original exact depth assertion")
        if depth_match:
            expected_depth_errors += 1
        expected_analyzer_error = None if depth_match else error
        require(actual["analyzer_error"] == expected_analyzer_error, "analysis exception attribution")
        if expected_analyzer_error is not None:
            analyzer_errors.append(identifier)
        has_receipt = actual["receipt_sha256"] is not None
        require(not has_receipt or valid_digest(actual["receipt_sha256"]), "public receipt digest")
        require(not has_receipt or (oracle_ok and error is None), "receipt despite failed/skipped analysis")
        if has_receipt:
            returned_receipts += 1
        require(type(actual["expanded_rows"]) is list and type(actual["blockers"]) is list,
                "public result containers")
        require(has_receipt or not actual["expanded_rows"] and not actual["blockers"],
                "rows/blockers without returned review")
        argv = [row["argv"] for row in actual["expanded_rows"] if row["capability_kind"] == "subprocess"]
        require(actual["argv"] == argv, "argv differs from public rows")
        semantic_ok = bool(oracle_ok and (depth_match if is_depth else
                           has_receipt and error is None and public_verdict(scope, expected, argv, actual["blockers"])))
        require(actual["semantic_passed"] is semantic_ok, "semantic result inconsistency")
        if not semantic_ok:
            semantic_failures.append(identifier)
        require(actual["original_methods_restored"] is True, "budget methods not restored")
        if actual["accounting_error"] is not None:
            accounting_errors.append(identifier)
            require(actual["reserve_violations"] == [], "reserve verdict despite failed accounting")
        elif oracle_ok:
            validate_budget_metrics(actual["budget_metrics"], identifier)
            violations = reserve_violations(actual["budget_metrics"], identifier)
            require(actual["reserve_violations"] == violations, "postexecution reserve mismatch")
            continuation_failures.extend(violations)
        else:
            require(actual["budget_metrics"] is None and actual["reserve_violations"] == [],
                    "budget scope despite skipped Model")
        if oracle_ok:
            require(type(actual["observer_lifecycle"]) is dict, "attempted observer lifecycle")
            if actual["lifecycle_error"] is not None:
                lifecycle_errors.append(identifier)
                require(actual["lifecycle_verdict"] is None, "verdict despite lifecycle validation error")
            else:
                lifecycle_verdict = validate_lifecycle(actual["observer_lifecycle"])
                require(actual["lifecycle_verdict"] is lifecycle_verdict, "lifecycle replay differs")
                if not lifecycle_verdict:
                    lifecycle_failures.append(identifier)
        else:
            require(actual["observer_lifecycle"] is None and actual["lifecycle_verdict"] is None
                    and actual["lifecycle_error"] is None, "lifecycle despite skipped analysis")
        if oracle_ok:
            mechanism = actual["mechanism"]
            require(type(mechanism) is dict, "mechanism record for attempted analysis")
            mechanism_restorations.append(mechanism["original_methods_restored"])
            if actual["mechanism_error"] is not None:
                mechanism_errors.append(identifier)
                require(actual["mechanism_verdict"] is None, "verdict despite mechanism validation error")
            else:
                verdict = validate_mechanism(mechanism, identifier, coverage, actual["budget_metrics"])
                require(actual["mechanism_verdict"] == verdict, "mechanism replay differs")
                if not verdict["met"]:
                    mechanism_failures.append(identifier)
        else:
            require(actual["mechanism"] is None and actual["mechanism_verdict"] is None
                    and actual["mechanism_error"] is None, "mechanism despite skipped public analysis")
    summary = records[-1]
    require(summary.get("rewrite_gate_b_summary") is True, "final Gate B summary")
    require(summary["schema"] == SCHEMA and summary["slot"] == setup["slot"]
            and summary["generator_sha256"] == setup["generator_sha256"]
            and summary["pack_sha256"] == PACK_HASHES and summary["probe_sha256"] == PROBE_SHA
            and summary["plan_sha256"] == PLAN_SHA and summary["population_sha256"] == POPULATION_SHA
            and summary["observer_map_sha256"] == OBSERVER_MAP_SHA
            and summary["tests_sha256"] == TESTS_SHA
            and summary["depth_provenance_sha256"] == DEPTH_PROVENANCE_SHA
            and summary["adapter"] == ADAPTER_ID
            and summary["adapter_source_sha256"] == ADAPTER_SOURCE_SHA
            and summary["extra_input_sha256"] == EXTRA_HASHES
            and summary["reserve_basis"] == RESERVE_BASIS, "summary input pins")
    for key in ("planned_cases", "case_count"):
        require(type(summary[key]) is int and summary[key] == 12, "summary exact scope")
    for key, value in (("projections", projections), ("attempted_analyses", attempted),
                       ("returned_receipts", returned_receipts), ("expected_depth_errors", expected_depth_errors)):
        require(type(summary[key]) is int and summary[key] == value, "summary count: " + key)
    require(summary["classifications"] == {"clean": 6, "refuse": 3, "permitted-refusal": 1, "exact-depth-error": 2}
            and all(type(value) is int for value in summary["classifications"].values())
            and summary["caps"] == CAPS and all(type(value) is int for value in summary["caps"].values()),
            "classifications/caps")
    require(summary["semantic_failures"] == semantic_failures and summary["oracle_errors"] == oracle_errors
            and summary["analyzer_errors"] == analyzer_errors and summary["accounting_errors"] == accounting_errors,
            "summary/case consistency")
    require(summary["original_methods_restored"] is True
            and summary["observer_overhead_is_not_original_charged_work"] is True
            and summary["gate"] == "B" and summary["no_wider_population_run"] is True,
            "scope/observer restoration")
    require(type(summary["continuation_work_maximum"]) is int
            and summary["continuation_work_maximum"] == CONTINUATION_MAXIMUM
            and summary["reserve_is_postexecution_only"] is True
            and summary["reserve_violations"] == continuation_failures
            and summary["reserve_ok"] is (not accounting_errors and attempted == 12 and not continuation_failures),
            "requested-unit continuation reserve consistency")
    completed = (attempted == 12 and returned_receipts == 10 and expected_depth_errors == 2
                 and projections == 24 and not oracle_errors and not analyzer_errors and not accounting_errors)
    require(summary["completed"] is completed, "Gate B completion mismatch")
    observation_complete = attempted == 12 and projections == 24 and not oracle_errors
    require(summary["observation_complete"] is observation_complete, "finite observation mismatch")
    mechanism_ok = not mechanism_failures and not mechanism_errors
    restoration = len(mechanism_restorations) == 12 and all(mechanism_restorations)
    require(summary["mechanism_failures"] == mechanism_failures
            and summary["mechanism_errors"] == mechanism_errors
            and summary["mechanism_ok"] is mechanism_ok
            and summary["mechanism_methods_restored"] is restoration, "mechanism summary replay")
    lifecycle_ok = not lifecycle_failures and not lifecycle_errors and attempted == 12
    require(summary["lifecycle_failures"] == lifecycle_failures
            and summary["lifecycle_errors"] == lifecycle_errors
            and summary["lifecycle_ok"] is lifecycle_ok, "lifecycle summary replay")
    require(exit_code == int(bool(semantic_failures or oracle_errors or analyzer_errors
                                  or accounting_errors or continuation_failures or mechanism_failures or mechanism_errors
                                  or lifecycle_failures or lifecycle_errors)),
            "child exit mismatch")
    return {"identity": identity, "summary": summary, "cases_observed": len(observed),
            "completed": completed, "semantic_ok": not semantic_failures,
            "accounting_ok": not accounting_errors,
            "reserve_ok": not accounting_errors and attempted == 12 and not continuation_failures,
            "observation_complete": observation_complete, "mechanism_ok": mechanism_ok,
            "mechanism_methods_restored": restoration, "lifecycle_ok": lifecycle_ok}


def main():
    require(sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15), "control runtime")
    require(Path(sys.executable).resolve() == checked(SLOTS["311"][0]).resolve(), "control executable")
    require(sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
            and sys.dont_write_bytecode and not sys.flags.optimize, "control requires -I -S -B -P")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("label")
    parser.add_argument("slot", choices=tuple(SLOTS))
    parser.add_argument("overlay_source")
    parser.add_argument("overlay_sha256")
    parser.add_argument("--control-sha256", required=True)
    parser.add_argument("--worktree-sha256", required=True)
    parser.add_argument("--floor-receipt")
    parser.add_argument("--floor-sha256")
    args = parser.parse_args()
    require(valid_digest(args.overlay_sha256), "explicit candidate digest")
    source_sha = args.overlay_sha256
    require(source_sha == ADAPTER_SOURCE_SHA, "R1 baseline adapter only; successor review required")
    require(valid_digest(args.worktree_sha256), "explicit core worktree watch digest")
    require(re.fullmatch("[a-z0-9][a-z0-9-]{0,60}", args.label), "label")
    checked(ROOT, True)
    checked(CHECKS, True)
    prefix = "rewrite-r2-identity-v2-" + args.label + "-" + args.slot
    outputs = {key: CHECKS / (prefix + suffix) for key, suffix in (
        ("setup", "-setup.json"), ("receipt", "-receipt.json"),
        ("stdout", ".stdout.txt"), ("stderr", ".stderr.txt"), ("log", ".txt"))}
    require(not any(p.exists() for p in outputs.values()), "retained output collision")
    streams = {key: p.open("x+b") for key, p in outputs.items()}
    setup = {"schema": SCHEMA, "slot": args.slot, "label": args.label, "base": BASE,
             "overlay_source": args.overlay_source, "generator_sha256": args.overlay_sha256,
             "watch_source": str(WATCH), "watch_sha256": WATCH_SHA,
             "probe_sha256": PROBE_SHA, "pack_sha256": PACK_HASHES, "plan_sha256": PLAN_SHA,
             "population_sha256": POPULATION_SHA, "observer_map_sha256": OBSERVER_MAP_SHA,
             "core_watch_source": str(CORE_WATCH), "core_watch_sha256": args.worktree_sha256,
             "tests_sha256": TESTS_SHA, "depth_provenance_sha256": DEPTH_PROVENANCE_SHA,
             "continuation_work_maximum": CONTINUATION_MAXIMUM,
             "adapter": ADAPTER_ID, "adapter_source_sha256": ADAPTER_SOURCE_SHA,
             "extra_input_sha256": EXTRA_HASHES, "reserve_basis": RESERVE_BASIS}
    receipt = {**setup, "completed": False, "integrity_ok": False, "success": False, "payload_started": False}
    process, snapshot, temp, manifest_sha, exit_code = None, None, None, None, None
    before, input_paths, input_hashes, files = {}, {}, {}, {}
    phase = "preflight"
    write_json(streams["setup"], setup)
    try:
        overlay = checked(args.overlay_source)
        require(overlay.parent == ROOT and overlay.suffix == ".py",
                "candidate must be an explicit retained T source")
        control = checked(Path(__file__).absolute())
        require(control.is_relative_to(CHECKS) and valid_digest(args.control_sha256), "root control pin")
        input_paths = {"overlay": overlay, "watch": WATCH, "probe": PROBE,
                       **{scope: CHECKS / metadata["file"] for scope, metadata in PACKS.items()},
                       "plan": PLAN, "control": control, "population": POPULATION,
                       "observer_map": OBSERVER_MAP, "core_watch": CORE_WATCH,
                       "depth_provenance": DEPTH_PROVENANCE,
                       **{key: ROOT / entry["relative"] for key, entry in EXTRA_INPUTS.items()}}
        input_hashes = {"overlay": source_sha, "watch": WATCH_SHA, "probe": PROBE_SHA,
                        **PACK_HASHES, "plan": PLAN_SHA, "control": args.control_sha256,
                        "population": POPULATION_SHA, "observer_map": OBSERVER_MAP_SHA,
                        "core_watch": args.worktree_sha256, "depth_provenance": DEPTH_PROVENANCE_SHA,
                        **EXTRA_HASHES}
        inputs = {key: checked(p).read_bytes() for key, p in input_paths.items()}
        require({key: sha(raw) for key, raw in inputs.items()} == input_hashes, "original input pin mismatch")
        cases = load_cases({scope: inputs[scope] for scope in PACKS}, inputs["population"])
        coverage = validate_identity_inputs({key: inputs[key] for key in EXTRA_INPUTS}, inputs["population"])
        setup["control_sha256"] = args.control_sha256
        floor_files = {}
        if args.slot == "314":
            require(args.floor_receipt is not None and valid_digest(args.floor_sha256), "314 requires pinned311 receipt")
            floor_path = checked(args.floor_receipt)
            require(floor_path.is_relative_to(CHECKS), "floor outside checks")
            floor_raw = floor_path.read_bytes()
            require(sha(floor_raw) == args.floor_sha256, "floor receipt pin")
            floor = json.loads(floor_raw)
            require(floor["schema"] == SCHEMA and floor["slot"] == "311", "floor schema/slot")
            for key in ("base", "overlay_source", "generator_sha256", "watch_source", "watch_sha256", "core_watch_source", "core_watch_sha256",
                        "population_sha256", "observer_map_sha256", "tests_sha256", "depth_provenance_sha256",
                        "continuation_work_maximum", "adapter", "adapter_source_sha256",
                        "extra_input_sha256", "reserve_basis",
                        "probe_sha256", "pack_sha256", "plan_sha256", "control_sha256"):
                require(floor[key] == setup[key], "floor context mismatch: " + key)
            require(floor["integrity_ok"] is True and floor["completed"] is True
                    and floor["payload_started"] is True and type(floor["exit"]) is int
                    and floor["exit"] == 0 and floor["success"] is True and floor["semantic_ok"] is True
                    and floor["accounting_ok"] is True and floor["reserve_ok"] is True
                    and floor["mechanism_ok"] is True and floor["mechanism_methods_restored"] is True
                    and floor["observation_complete"] is True and floor["lifecycle_ok"] is True
                    and "error" not in floor
                    and "cleanup_error" not in floor,
                    "floor incomplete/integrity failed")
            require(floor["before"] == floor["after"] and floor["tracked_file_count"] == 1761
                    and floor["manifest_after_sha256"] == floor["manifest_sha256"], "floor manifest receipt")
            for key in input_paths:
                require(floor["input_hashes_before"][key] == input_hashes[key]
                        and floor["input_hashes_after"][key] == input_hashes[key], "floor input changed")
            floor_files["floor-receipt.json"] = floor_raw
            input_paths["floor_receipt"] = floor_path
            input_hashes["floor_receipt"] = args.floor_sha256
            pinned_outputs = {}
            for key in ("setup", "stdout", "stderr", "log"):
                entry = floor["outputs"][key]
                p = checked(entry["path"])
                require(p.is_relative_to(CHECKS), "floor output outside checks")
                raw = p.read_bytes()
                require(sha(raw) == entry["sha256"], "floor retained output changed: " + key)
                pinned_outputs[key] = raw
                floor_files["floor-" + key + (".json" if key == "setup" else ".txt")] = raw
                input_paths["floor_" + key] = p
                input_hashes["floor_" + key] = entry["sha256"]
            floor_setup = json.loads(pinned_outputs["setup"])
            for key in ("schema", "slot", "label", "base", "overlay_source", "generator_sha256",
                        "watch_source", "watch_sha256", "core_watch_source", "core_watch_sha256",
                        "population_sha256", "observer_map_sha256", "tests_sha256", "depth_provenance_sha256",
                        "continuation_work_maximum", "adapter", "adapter_source_sha256",
                        "extra_input_sha256", "reserve_basis", "probe_sha256", "pack_sha256", "plan_sha256",
                        "control_sha256", "snapshot", "temp", "before", "manifest_sha256", "environment",
                        "command", "timeout_seconds", "tracked_file_count", "payload_file_count",
                        "input_hashes_before", "input_paths"):
                require(floor_setup[key] == floor[key], "floor raw setup mismatch: " + key)
            require(type(floor["tracked_file_count"]) is int and floor["tracked_file_count"] == 1761
                    and type(floor["payload_file_count"]) is int and floor["payload_file_count"] == len(BASE_PAYLOAD_NAMES)
                    and len(floor["before"]) == 1761 + len(BASE_PAYLOAD_NAMES), "floor exact manifest scope")
            require(pinned_outputs["log"] == pinned_outputs["stdout"] + b"\nCONTROL STDERR\n"
                    + pinned_outputs["stderr"], "floor combined log replay")
            proof = validate_result(pinned_outputs["stdout"], floor["exit"], floor_setup, cases, coverage)
            require(proof["completed"] is True and proof["summary"] == floor["summary"]
                    and proof["identity"] == floor["identity"]
                    and proof["semantic_ok"] is floor["semantic_ok"]
                    and proof["accounting_ok"] is True and floor["accounting_ok"] is True
                    and proof["reserve_ok"] is True and floor["reserve_ok"] is True
                    and proof["mechanism_ok"] is True and proof["mechanism_methods_restored"] is True
                    and proof["observation_complete"] is True and proof["lifecycle_ok"] is True
                    and floor["success"] is True, "floor output completion")
            floor_snapshot = checked(Path(floor["snapshot"]), True)
            require(floor_snapshot.name == "snapshot" and floor_snapshot.parent.parent == SNAPSHOTS
                    and Path(floor["temp"]) == floor_snapshot.parent / "temp", "floor snapshot/temp layout")
            floor_tracked = git(floor_snapshot, Path(floor["temp"]), "ls-tree", "-r", "-z",
                                "--name-only", BASE).decode().split("\0")[:-1]
            floor_payload_names = BASE_PAYLOAD_NAMES
            require(len(floor_tracked) == len(set(floor_tracked)) == 1761
                    and set(floor["before"]) == set(floor_tracked) |
                        {PAYLOAD + "/" + name for name in floor_payload_names}, "floor exact manifest keys")
            require(git(floor_snapshot, Path(floor["temp"]), "rev-parse", "HEAD").decode().strip() == BASE,
                    "floor HEAD now changed")
            floor_dirty = git(floor_snapshot, Path(floor["temp"]), "status", "--porcelain=v1",
                              "-z", "--untracked-files=all").decode()
            require(set(floor_dirty.split("\0")[:-1]) ==
                    ({(" M " + GENERATOR)} if source_sha != BASE_GENERATOR_SHA else set()) |
                    {"?? " + PAYLOAD + "/" + name for name in (*floor_payload_names, "manifest.json")},
                    "floor status now changed")
            require(file_hashes(floor_snapshot, floor["before"]) == floor["before"], "floor snapshot now changed")
            require(floor["before"]["tests/test_inventory_and_profiles.py"] == TESTS_SHA,
                    "floor original tests identity")
            floor_manifest_raw = checked(floor_snapshot / PAYLOAD / "manifest.json").read_bytes()
            require(sha(floor_manifest_raw) == floor["manifest_sha256"]
                    and json.loads(floor_manifest_raw) == floor["before"], "floor manifest now changed")
            setup["floor_receipt"] = {"path": str(floor_path), "sha256": args.floor_sha256,
                                      "exit": floor["exit"], "snapshot_files_rehashed": len(floor["before"]),
                                      "successful_floor_required": True}
        else:
            require(args.floor_receipt is None and args.floor_sha256 is None, "311 takes no floor receipt")
        phase = "clone"
        checked(SNAPSHOTS, True)
        checked(REPOSITORY, True)
        parent = SNAPSHOTS / ("rewrite-r2-identity-v2-" + uuid.uuid4().hex)
        parent.mkdir()
        checked(parent, True)
        temp = parent / "temp"
        temp.mkdir()
        checked(temp, True)
        snapshot = parent / "snapshot"
        git(parent, temp, "clone", "--shared", "--no-checkout", str(REPOSITORY), str(snapshot))
        checked(snapshot, True)
        git(snapshot, temp, "checkout", "--detach", BASE)
        require(git(snapshot, temp, "rev-parse", "HEAD").decode().strip() == BASE, "snapshot HEAD")
        require(not git(snapshot, temp, "status", "--porcelain=v1", "-z", "--untracked-files=all"), "initial snapshot dirty")
        require(sha(checked(snapshot / GENERATOR).read_bytes()) == BASE_GENERATOR_SHA, "r010 source")
        (snapshot / GENERATOR).write_bytes(inputs["overlay"])
        expected_overlay = b"" if source_sha == BASE_GENERATOR_SHA else b" M tools/generate_test_inventory.py\0"
        require(git(snapshot, temp, "status", "--porcelain=v1", "-z", "--untracked-files=all")
                == expected_overlay, "extra overlay paths")
        tracked = git(snapshot, temp, "ls-tree", "-r", "-z", "--name-only", BASE).decode().split("\0")[:-1]
        require(len(tracked) == len(set(tracked)) == 1761, "tracked count")
        before = file_hashes(snapshot, tracked)
        require(before[GENERATOR] == source_sha, "copied overlay pin")
        require(before["tests/test_inventory_and_profiles.py"] == TESTS_SHA, "original test blob")
        run = {"schema": SCHEMA, "slot": args.slot, "generator_sha256": source_sha,
               "probe_sha256": PROBE_SHA, "pack_sha256": PACK_HASHES, "plan_sha256": PLAN_SHA,
               "control_sha256": args.control_sha256, "overlay_source": str(overlay),
               "watch_source": str(WATCH), "watch_sha256": WATCH_SHA,
               "population_sha256": POPULATION_SHA, "observer_map_sha256": OBSERVER_MAP_SHA,
               "core_watch_source": str(CORE_WATCH), "core_watch_sha256": args.worktree_sha256,
               "tests_sha256": TESTS_SHA, "depth_provenance_sha256": DEPTH_PROVENANCE_SHA,
               "continuation_work_maximum": CONTINUATION_MAXIMUM,
             "adapter": ADAPTER_ID, "adapter_source_sha256": ADAPTER_SOURCE_SHA,
             "extra_input_sha256": EXTRA_HASHES, "reserve_basis": RESERVE_BASIS}
        files = {"probe.py": inputs["probe"],
                 **{metadata["file"]: inputs[scope] for scope, metadata in PACKS.items()},
                 "control.py": inputs["control"], "plan.md": inputs["plan"],
                 "retained-source.py": inputs["overlay"], "run.json": canonical(run),
                 "population.json": inputs["population"], "observer-map.json": inputs["observer_map"],
                 "depth-provenance.py": inputs["depth_provenance"],
                 **{entry["payload"]: inputs[key] for key, entry in EXTRA_INPUTS.items()},
                 **floor_files}
        require(set(files) == BASE_PAYLOAD_NAMES | set(floor_files), "released payload set")
        payload = snapshot / PAYLOAD
        payload.mkdir()
        checked(payload, True)
        for name, raw in files.items():
            create(payload / name, raw)
            before[PAYLOAD + "/" + name] = sha(raw)
        require(len(before) == 1761 + len(BASE_PAYLOAD_NAMES) + (5 if args.slot == "314" else 0), "complete manifest count")
        manifest_raw = canonical(before)
        manifest_sha = sha(manifest_raw)
        create(payload / "manifest.json", manifest_raw)
        env = environment(temp, snapshot)
        exe, version = SLOTS[args.slot]
        checked(exe)
        command = [str(exe), "-B", "-P", str(payload / "probe.py"), args.slot, manifest_sha, sha(canonical(env))]
        setup.update({"input_hashes_before": input_hashes, "input_paths": {k: str(p) for k, p in input_paths.items()},
                      "tracked_file_count": 1761, "payload_file_count": len(files), "before": before,
                      "snapshot": str(snapshot), "temp": str(temp), "manifest_sha256": manifest_sha,
                      "command": command, "environment": env, "timeout_seconds": TIMEOUT})
        receipt.update(setup)
        write_json(streams["setup"], setup)
        phase = "payload"
        receipt["payload_started"] = True
        process = subprocess.Popen(command, cwd=snapshot, env=env, stdout=streams["stdout"], stderr=streams["stderr"],
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        print(json.dumps({"child_pid": process.pid, "stdout": str(outputs["stdout"])}), flush=True)
        try:
            exit_code = process.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)
            exit_code = 124
            receipt["timeout"] = True
            raise RuntimeError("infrastructure watchdog expired after 60 seconds")
        phase = "result-validation"
        streams["stdout"].flush()
        result = validate_result(outputs["stdout"].read_bytes(), exit_code, setup, cases, coverage)
        receipt.update(result)
        require(result["observation_complete"], "finite public observation scope incomplete")
    except BaseException as error:
        receipt["error"] = {"phase": phase, "type": type(error).__name__, "message": str(error)}
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            try:
                process.wait(timeout=10)
            except BaseException as error:
                receipt["cleanup_error"] = {"type": type(error).__name__, "message": str(error)}
        receipt["exit"] = exit_code
        receipt["process_returncode"] = process.returncode if process is not None else None
        integrity_errors = []
        if snapshot is not None and before and manifest_sha is not None:
            after, after_errors = {}, []
            for name in before:
                try:
                    after.update(file_hashes(snapshot, [name]))
                except BaseException as error:
                    after_errors.append({"path": name, "type": type(error).__name__, "message": str(error)})
            receipt.update({"after": after, "after_file_errors": after_errors})
            try:
                require(not after_errors and after == before, "manifest files changed/missing")
                manifest_after = sha(checked(snapshot / PAYLOAD / "manifest.json").read_bytes())
                receipt["manifest_after_sha256"] = manifest_after
                require(manifest_after == manifest_sha, "manifest changed")
                require(git(snapshot, temp, "rev-parse", "HEAD").decode().strip() == BASE, "HEAD changed")
                dirty = git(snapshot, temp, "status", "--porcelain=v1", "-z", "--untracked-files=all")
                receipt["status_after"] = dirty.decode()
                expected_dirty = ({" M " + GENERATOR} if source_sha != BASE_GENERATOR_SHA else set()) | {
                    "?? " + PAYLOAD + "/" + name for name in (*files, "manifest.json")}
                require(set(dirty.decode().split("\0")[:-1]) == expected_dirty, "unexpected snapshot changes")
            except BaseException as error:
                integrity_errors.append({"check": "snapshot", "type": type(error).__name__, "message": str(error)})
        else:
            integrity_errors.append({"check": "snapshot", "message": "snapshot not fully prepared"})
        after_inputs, original_errors = {}, []
        for key, path in input_paths.items():
            try:
                after_inputs[key] = sha(checked(path).read_bytes())
            except BaseException as error:
                original_errors.append({"input": key, "type": type(error).__name__, "message": str(error)})
        receipt.update({"input_hashes_after": after_inputs, "after_original_errors": original_errors})
        if original_errors or not input_hashes or after_inputs != input_hashes:
            integrity_errors.append({"check": "originals", "message": "retained inputs/W watch missing or changed"})
        receipt["integrity_errors"] = integrity_errors
        receipt["integrity_ok"] = not integrity_errors
        for key in ("stdout", "stderr"):
            streams[key].flush()
            os.fsync(streams[key].fileno())
        stdout, stderr = outputs["stdout"].read_bytes(), outputs["stderr"].read_bytes()
        partial_records = []
        for line in stdout.splitlines():
            try:
                value = json.loads(line)
            except (ValueError, UnicodeError):
                continue
            if isinstance(value, dict):
                partial_records.append(value)
        receipt["retained_partial_records"] = partial_records
        log = stdout + b"\nCONTROL STDERR\n" + stderr
        if "error" in receipt:
            log += b"\nCONTROL FAILURE\n" + canonical(receipt["error"])
        streams["log"].write(log)
        streams["log"].flush()
        os.fsync(streams["log"].fileno())
        receipt["outputs"] = {key: {"path": str(outputs[key]), "sha256": sha(outputs[key].read_bytes())}
                              for key in ("setup", "stdout", "stderr", "log")}
        receipt["success"] = (receipt["completed"] is True and receipt["integrity_ok"]
                              and receipt.get("semantic_ok") is True and receipt.get("accounting_ok") is True
                              and receipt.get("reserve_ok") is True and receipt.get("mechanism_ok") is True
                              and receipt.get("mechanism_methods_restored") is True and receipt.get("lifecycle_ok") is True
                              and "error" not in receipt and "cleanup_error" not in receipt
                              and type(exit_code) is int and exit_code == 0)
        write_json(streams["receipt"], receipt)
        for stream in streams.values():
            stream.close()
    print(json.dumps({"receipt": str(outputs["receipt"]), "receipt_sha256": sha(outputs["receipt"].read_bytes()),
                      "exit": exit_code, "completed": receipt["completed"], "integrity_ok": receipt["integrity_ok"],
                      "semantic_ok": receipt.get("semantic_ok"),
                      "error": receipt.get("error")}), flush=True)
    return 2 if "error" in receipt or "cleanup_error" in receipt or not receipt["integrity_ok"] else int(not receipt["success"])


if __name__ == "__main__":
    raise SystemExit(main())
