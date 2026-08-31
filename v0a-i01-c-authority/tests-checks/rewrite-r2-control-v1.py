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
PROBE = CHECKS / "rewrite-r2-probe-v1.py"
PROBE_SHA = 'abc1a22b76691ab8881e5301f532fad32171183abb11221debc93e7428e48310'

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
        "ids": ("hidden-cell-joined-reached", "hidden-cell-joined-dormant",
                "scale-n8-s4-d0-normal", "scale-n64-s4-d0-normal",
                "scale-n8-s4-d2-exceptional", "scale-n64-s4-d2-exceptional"),
    },
}
PACK_HASHES = {scope: metadata["sha256"] for scope, metadata in PACKS.items()}
GATE_B_IDS = ('shared-list-consumed', 'shared-list-dormant', 'class-adoption-unsafe', 'class-adoption-safe', 'hidden-cell-joined-reached', 'hidden-cell-joined-dormant', 'helper65', 'generator70', 'scale-n8-s4-d0-normal', 'scale-n64-s4-d0-normal', 'scale-n8-s4-d2-exceptional', 'scale-n64-s4-d2-exceptional')
CONTINUATION_MAXIMUM = 196608
TESTS_SHA = 'c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf'
DEPTH_PROVENANCE_SHA = '7aa9f188b2917fec149485501eafcc4d516d3104a10b026e5ec33262b24962ae'
DEPTH_CASES = {'helper65': {'method': 'test_round4_analysis_budget_red_contracts_are_independent', 'fixture_sha256': '94b070b8fcf2e66c42e1a779558e830d7caae670366f9313faf0989c722818c6', 'regex': '^analysis helper depth exceeds 64$'}, 'generator70': {'method': 'test_round4_source_order_and_branch_bounds_red_contracts_are_independent', 'fixture_sha256': '635e682b2253cd44201e2afdb95c288b9973f5629ec4eeb3c5bfd078743eb5e3', 'regex': '^analysis deferred generator depth exceeds 64$'}}
POPULATION_SHA = "3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce"

PLAN = CHECKS / "rewrite-r2-plan-v1.md"
PLAN_SHA = 'ea2ca1217f133a708c763568cc7494a2ac600b4db351e00a696600836d53f5f7'
OBSERVER_MAP_SHA = '1dfd899dc7c7a1c9bbf1ff0ee17bc8b4fd4be1eadf3c81f759eb1b0176630228'
OBSERVER_MAP = CHECKS / "rewrite-r2-observer-map-v1.json"
POPULATION = ROOT / "rewrite-early-population-v1.json"
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
SCHEMA = "pontius-rewrite-r2-gate-b-v1"
PAYLOAD = ".rewrite-r2-gate-b"
GENERATOR = "tools/generate_test_inventory.py"
TIMEOUT = 60  # Infrastructure watchdog, not a new analyzer admission cap.


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
    require(tuple(population["gates"]["A"]["ordered_case_ids"]) == GATE_B_IDS[:6],
            "unchanged Gate A prefix")
    gate = population["gates"]["B"]
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
    """Post-execution engineering predicate; never modifies or calls a budget."""
    return [{"case": identifier, "epoch": entry["epoch"],
             "observed_work": entry["last_observed_work"], "maximum": CONTINUATION_MAXIMUM}
            for entry in metrics["epochs"]
            if entry["last_observed_work"] > CONTINUATION_MAXIMUM]

def validate_result(stdout, exit_code, setup, cases):
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
            and identity["probe_sha256"] == PROBE_SHA, "identity context")
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
    continuation_failures = []
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
    summary = records[-1]
    require(summary.get("rewrite_gate_b_summary") is True, "final Gate B summary")
    require(summary["schema"] == SCHEMA and summary["slot"] == setup["slot"]
            and summary["generator_sha256"] == setup["generator_sha256"]
            and summary["pack_sha256"] == PACK_HASHES and summary["probe_sha256"] == PROBE_SHA
            and summary["plan_sha256"] == PLAN_SHA and summary["population_sha256"] == POPULATION_SHA
            and summary["observer_map_sha256"] == OBSERVER_MAP_SHA
            and summary["tests_sha256"] == TESTS_SHA
            and summary["depth_provenance_sha256"] == DEPTH_PROVENANCE_SHA, "summary input pins")
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
            and summary["reserve_ok"] is (not continuation_failures), "continuation reserve consistency")
    completed = (attempted == 12 and returned_receipts == 10 and expected_depth_errors == 2
                 and projections == 24 and not oracle_errors and not analyzer_errors and not accounting_errors)
    require(summary["completed"] is completed, "Gate B completion mismatch")
    require(exit_code == int(bool(semantic_failures or oracle_errors or analyzer_errors
                                  or accounting_errors or continuation_failures)), "child exit mismatch")
    return {"identity": identity, "summary": summary, "cases_observed": len(observed),
            "completed": completed, "semantic_ok": not semantic_failures,
            "accounting_ok": not accounting_errors, "reserve_ok": not continuation_failures}


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
    require(valid_digest(args.worktree_sha256), "explicit core worktree watch digest")
    require(re.fullmatch("[a-z0-9][a-z0-9-]{0,60}", args.label), "label")
    checked(ROOT, True)
    checked(CHECKS, True)
    prefix = "rewrite-r2-gate-b-" + args.label + "-" + args.slot
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
             "continuation_work_maximum": CONTINUATION_MAXIMUM}
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
                       "depth_provenance": DEPTH_PROVENANCE}
        input_hashes = {"overlay": source_sha, "watch": WATCH_SHA, "probe": PROBE_SHA,
                        **PACK_HASHES, "plan": PLAN_SHA, "control": args.control_sha256,
                        "population": POPULATION_SHA, "observer_map": OBSERVER_MAP_SHA,
                        "core_watch": args.worktree_sha256, "depth_provenance": DEPTH_PROVENANCE_SHA}
        inputs = {key: checked(p).read_bytes() for key, p in input_paths.items()}
        require({key: sha(raw) for key, raw in inputs.items()} == input_hashes, "original input pin mismatch")
        cases = load_cases({scope: inputs[scope] for scope in PACKS}, inputs["population"])
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
                        "continuation_work_maximum",
                        "probe_sha256", "pack_sha256", "plan_sha256", "control_sha256"):
                require(floor[key] == setup[key], "floor context mismatch: " + key)
            require(floor["integrity_ok"] is True and floor["completed"] is True
                    and floor["payload_started"] is True and type(floor["exit"]) is int
                    and floor["exit"] == 0 and floor["success"] is True and floor["semantic_ok"] is True
                    and floor["accounting_ok"] is True and floor["reserve_ok"] is True and "error" not in floor
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
                        "continuation_work_maximum", "probe_sha256", "pack_sha256", "plan_sha256",
                        "control_sha256", "snapshot", "temp", "before", "manifest_sha256", "environment",
                        "command", "timeout_seconds", "tracked_file_count", "payload_file_count",
                        "input_hashes_before", "input_paths"):
                require(floor_setup[key] == floor[key], "floor raw setup mismatch: " + key)
            require(type(floor["tracked_file_count"]) is int and floor["tracked_file_count"] == 1761
                    and type(floor["payload_file_count"]) is int and floor["payload_file_count"] == 10
                    and len(floor["before"]) == 1771, "floor exact manifest scope")
            require(pinned_outputs["log"] == pinned_outputs["stdout"] + b"\nCONTROL STDERR\n"
                    + pinned_outputs["stderr"], "floor combined log replay")
            proof = validate_result(pinned_outputs["stdout"], floor["exit"], floor_setup, cases)
            require(proof["completed"] is True and proof["summary"] == floor["summary"]
                    and proof["identity"] == floor["identity"]
                    and proof["semantic_ok"] is floor["semantic_ok"]
                    and proof["accounting_ok"] is True and floor["accounting_ok"] is True
                    and proof["reserve_ok"] is True and floor["reserve_ok"] is True
                    and floor["success"] is True, "floor output completion")
            floor_snapshot = checked(Path(floor["snapshot"]), True)
            require(floor_snapshot.name == "snapshot" and floor_snapshot.parent.parent == SNAPSHOTS
                    and Path(floor["temp"]) == floor_snapshot.parent / "temp", "floor snapshot/temp layout")
            floor_tracked = git(floor_snapshot, Path(floor["temp"]), "ls-tree", "-r", "-z",
                                "--name-only", BASE).decode().split("\0")[:-1]
            floor_payload_names = {"probe.py", *(metadata["file"] for metadata in PACKS.values()),
                                   "control.py", "plan.md", "retained-source.py", "run.json",
                                   "population.json", "observer-map.json", "depth-provenance.py"}
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
        parent = SNAPSHOTS / ("rewrite-r2-gate-b-" + uuid.uuid4().hex)
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
               "continuation_work_maximum": CONTINUATION_MAXIMUM}
        files = {"probe.py": inputs["probe"],
                 **{metadata["file"]: inputs[scope] for scope, metadata in PACKS.items()},
                 "control.py": inputs["control"], "plan.md": inputs["plan"],
                 "retained-source.py": inputs["overlay"], "run.json": canonical(run),
                 "population.json": inputs["population"], "observer-map.json": inputs["observer_map"],
                 "depth-provenance.py": inputs["depth_provenance"],
                 **floor_files}
        payload = snapshot / PAYLOAD
        payload.mkdir()
        checked(payload, True)
        for name, raw in files.items():
            create(payload / name, raw)
            before[PAYLOAD + "/" + name] = sha(raw)
        require(len(before) == 1771 + (5 if args.slot == "314" else 0), "complete manifest count")
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
        result = validate_result(outputs["stdout"].read_bytes(), exit_code, setup, cases)
        receipt.update(result)
        require(result["completed"], "finite oracle/analyzer scope incomplete")
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
                              and receipt.get("reserve_ok") is True
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

