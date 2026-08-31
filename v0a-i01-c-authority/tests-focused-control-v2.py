"""Finite focused controller. Root review is required before every dispatch.

Controller: actual CPython 3.11.15 with -I -S -B -P.
Payload: selected actual interpreter with -B -P, fresh r010 snapshot.
Only design53 or the immutable matrix192 is admitted. V2 pins the reviewed v5 test correction for both. No mutable W input.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time
import traceback
import uuid

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
WORKSPACE = Path(r"D:\Pontius")
SNAPSHOTS = Path(r"D:\pontius-snapshots")
WATCH = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1"
             r"\tools\generate_test_inventory.py")
GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
BASE = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
ORIGINAL_SOURCE_SHA = "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
ORIGINAL_TESTS_SHA = "c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf"
CANDIDATE_TESTS_SHA = "48c4620bf5585a76d500b3c9bf4cad4559a04d4f544bc3808832d37b58b03add"
WRAPPER = ROOT / "tests-focused-wrapper-v1.py"
WRAPPER_SHA = "839e30c19b825defae4fea30ec899a43cd0ad346953215421b81478ffc20ca35"
POPULATION = ROOT / "tests-focused-population-v2.json"
POPULATION_SHA = "449ffdd9898d06b43c5d707b01d4e6e387be64ee7f32b2f914e6b58604acb8ea"
CANDIDATE_TESTS = ROOT / "tests-candidate-v5.py"
SLOTS = {
    "311": (Path(r"D:\Pontius-tools\py311\Scripts\python.exe"), [3, 11, 15]),
    "314": (Path(r"D:\Pontius\.venv\Scripts\python.exe"), [3, 14, 6]),
}
SCHEMA = "c-authority-focused-control-v2"
PAYLOAD = ".focused-authority-v2"
SOURCE_RELATIVE = "tools/generate_test_inventory.py"
TEST_RELATIVE = "tests/test_inventory_and_profiles.py"
TRACKED_COUNT = 1761
TIMEOUT = 60


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def valid_sha(value):
    return type(value) is str and re.fullmatch("[0-9a-f]{64}", value) is not None


def checked(path, regular=False):
    require(path.is_absolute() and ".." not in path.parts, "unsafe absolute path")
    for ancestor in (path, *path.parents):
        information = ancestor.lstat()
        require(not (getattr(information, "st_file_attributes", 0)
                     & stat.FILE_ATTRIBUTE_REPARSE_POINT), "reparse path: " + str(ancestor))
        if ancestor != path:
            require(stat.S_ISDIR(information.st_mode), "nondirectory ancestor")
    if regular:
        require(stat.S_ISREG(path.lstat().st_mode), "nonregular input: " + str(path))
    return path


def handoff_file(value, suffix):
    path = Path(value)
    require(path.is_relative_to(ROOT) and path.suffix == suffix,
            "input must be an absolute retained handoff " + suffix)
    return checked(path, regular=True)


def pinned(path, expected):
    require(valid_sha(expected), "SHA256 argument")
    raw = checked(path, regular=True).read_bytes()
    require(digest(raw) == expected, "input hash mismatch: " + str(path))
    return raw


def create(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def save_stream(stream, value):
    # The exclusively created receipt is unpublished until this invocation ends.
    stream.seek(0)
    stream.write(encoded(value))
    stream.truncate()
    stream.flush()
    os.fsync(stream.fileno())


def environment_for(temp, snapshot=None):
    windows = checked(Path(os.environ["SYSTEMROOT"]))
    system = checked(windows / "System32")
    environment = {
        "SYSTEMROOT": str(windows), "WINDIR": str(windows),
        "COMSPEC": str(checked(system / "cmd.exe", regular=True)),
        "PATH": str(system), "TEMP": str(temp), "TMP": str(temp),
        "PONTIUS_GIT": str(checked(GIT, regular=True)),
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "NUL",
        "GIT_CONFIG_SYSTEM": "NUL", "GIT_ATTR_NOSYSTEM": "1",
        "PYTHONNOUSERSITE": "1",
    }
    if snapshot is not None:
        environment["PYTHONPATH"] = str(snapshot / "src")
    return environment


def git(repository, temp, *arguments):
    command = [
        str(checked(GIT, regular=True)), "-c", "core.autocrlf=false",
        "-c", "core.hooksPath=NUL", "-c", "init.templateDir=",
        "-c", "core.attributesFile=NUL", "-c", "core.fsmonitor=false",
        "-C", str(repository), *arguments,
    ]
    return subprocess.run(command, cwd=repository, env=environment_for(temp),
                          check=True, capture_output=True, timeout=TIMEOUT,
                          creationflags=subprocess.CREATE_NO_WINDOW).stdout


def names_from(raw):
    return [name.decode("utf-8") for name in raw.split(b"\0") if name]


def file_hashes(snapshot, names):
    result = {}
    for name in names:
        relative = Path(name)
        require(not relative.is_absolute() and not relative.drive
                and ".." not in relative.parts, "unsafe snapshot name")
        target = snapshot / relative
        require(target.is_relative_to(snapshot), "snapshot path containment")
        result[name] = digest(checked(target, regular=True).read_bytes())
    return result


def output_records(raw):
    records = []
    invalid = []
    for number, line in enumerate(raw.decode("utf-8", errors="replace").splitlines(), 1):
        if not line.startswith("{"):
            continue
        try:
            value = json.loads(line)
        except (ValueError, TypeError):
            invalid.append(number)
            continue
        if type(value) is dict:
            records.append(value)
    return records, invalid


def assess(raw, population, kind, identity_expected):
    records, invalid_lines = output_records(raw)
    controls = [row["focused_control"] for row in records if "focused_control" in row]
    require(all(type(row) is dict for row in controls), "control record type")
    identities = [row for row in controls if row.get("event") == "identity"]
    summaries = [row for row in controls if row.get("event") == "unittest_summary"]
    population_rows = [row for row in controls if row.get("event") == "population"]
    started = [row.get("id") for row in controls if row.get("event") == "test_started"]
    finished = [row.get("id") for row in controls if row.get("event") == "test_finished"]
    bootstrap_errors = [row for row in controls if row.get("event") == "bootstrap_error"]
    expected = population[kind]
    expected_ids = ["focused_frozen_tests." + expected["class_name"] + "." + name
                    for name in expected["methods"]]
    errors = []
    identity_valid = False
    if len(identities) == 1:
        identity = identities[0]
        identity_valid = all(identity.get(key) == value
                             for key, value in identity_expected.items())
        identity_valid = identity_valid and (
            identity.get("safe_path") is True
            and identity.get("dont_write_bytecode") is True
            and type(identity.get("tracked_count")) is int
            and identity["tracked_count"] == TRACKED_COUNT
            and all(type(identity.get(key)) is int and identity[key] == value
                    for key, value in {"optimize": 0, "no_site": 0, "no_user_site": 1,
                                       "isolated": 0, "ignore_environment": 0}.items()))
    if not identity_valid:
        errors.append("identity missing, duplicated, or mismatched")
    complete = False
    successful = False
    summary = summaries[0] if len(summaries) == 1 else None
    if summary is not None:
        complete = (summary.get("complete_population") is True
                    and type(summary.get("tests_run")) is int
                    and summary["tests_run"] == expected["planned_methods"]
                    and type(summary.get("planned_methods")) is int
                    and summary["planned_methods"] == expected["planned_methods"]
                    and summary.get("kind") == kind
                    and summary.get("started_ids") == expected_ids
                    and summary.get("completed_ids") == expected_ids
                    and started == expected_ids and finished == expected_ids)
        successful = summary.get("successful") is True and all(
            summary.get(key) == [] for key in
            ("failures", "errors", "skips", "expected_failures", "unexpected_successes"))
    population_valid = (
        len(population_rows) == 1 and population_rows[0].get("kind") == kind
        and type(population_rows[0].get("planned_methods")) is int
        and population_rows[0]["planned_methods"] == expected["planned_methods"]
        and population_rows[0].get("ids") == expected_ids)
    if not complete or not population_valid:
        errors.append("unittest population incomplete or mismatched")
    if invalid_lines:
        errors.append("malformed JSON output lines")
    if bootstrap_errors:
        errors.append("bootstrap error record")
    matrix = None
    if kind == "matrix":
        families = expected["families"]
        summaries_by_family = [row for row in records if "matrix_summary" in row]
        cases = [row for row in records if "matrix" in row and "classification" in row]
        case_errors = [row for row in records if "matrix" in row
                       and ("oracle_error" in row or "analyzer_error" in row)]
        ids = [(row.get("matrix"), row.get("case")) for row in cases]
        family_counts = Counter(row.get("matrix") for row in cases)
        classifications = Counter(row.get("classification") for row in cases)
        projections = sum(len(row["witnesses"]) for row in cases
                          if type(row.get("witnesses")) is list)
        shape_valid = all(
            type(row.get("case")) is str and bool(row["case"])
            and valid_sha(row.get("source_sha256")) and valid_sha(row.get("oracle_sha256"))
            and type(row.get("witnesses")) is list
            and all(type(witness) is dict and type(witness.get("trace")) is list
                    and type(witness.get("choice")) is bool
                    for witness in row["witnesses"])
            and type(row.get("argv")) is list and type(row.get("blockers")) is list
            and type(row.get("unreachable_events")) is list for row in cases)
        family_summaries_valid = (
            len(summaries_by_family) == len(families)
            and Counter(row.get("matrix_summary") for row in summaries_by_family)
            == Counter({family: 1 for family in families}))
        if family_summaries_valid:
            for row in summaries_by_family:
                count = families[row["matrix_summary"]]
                family_summaries_valid = family_summaries_valid and all(
                    type(row.get(key)) is int and row[key] == count
                    for key in ("planned", "generated", "exercised"))
                family_summaries_valid = family_summaries_valid and all(
                    row.get(key) == [] for key in
                    ("unreachable_cases", "oracle_errors", "analyzer_errors"))
        matrix_complete = (
            shape_valid and family_summaries_valid and not case_errors
            and len(cases) == expected["planned_cases"]
            and len(set(ids)) == len(cases) and dict(family_counts) == families
            and projections == expected["planned_projections"]
            and dict(classifications) == expected["classifications"])
        matrix = {
            "complete": matrix_complete, "planned_cases": expected["planned_cases"],
            "case_records": len(cases), "unique_case_ids": len(set(ids)),
            "planned_projections": expected["planned_projections"],
            "projections": projections, "family_counts": dict(family_counts),
            "classifications": dict(classifications), "family_summaries": summaries_by_family,
            "case_error_records": case_errors,
            "last_completed_case": list(ids[-1]) if ids else None,
        }
        if not matrix_complete:
            errors.append("matrix population, harmless oracle, or analyzer execution incomplete")
        complete = complete and matrix_complete
    return {
        "identity_valid": identity_valid, "identity": identities[0] if len(identities) == 1 else None,
        "population_valid": population_valid, "complete": complete,
        "successful": successful and complete and identity_valid
                      and not errors and not bootstrap_errors,
        "summary": summary, "matrix": matrix, "validation_errors": errors,
        "bootstrap_errors": bootstrap_errors, "invalid_json_lines": invalid_lines,
        "started_method_count": len(started), "finished_method_count": len(finished),
        "last_started_test": started[-1] if started else None,
        "last_finished_test": finished[-1] if finished else None,
    }


def floor_binding(path, expected_sha, inputs, kind, tests_sha):
    raw = pinned(path, expected_sha)
    value = json.loads(raw)
    require(value.get("schema") == SCHEMA and value.get("slot") == "311"
            and value.get("kind") == kind, "matching floor kind/schema required")
    require(value.get("success") is True and value.get("integrity") is True
            and value.get("timed_out") is False and type(value.get("exit")) is int
            and value["exit"] == 0 and type(value.get("actual_process_returncode")) is int
            and value["actual_process_returncode"] == 0, "successful completed floor required")
    require(value.get("source_path") == inputs["source"]["path"]
            and value.get("source_sha256") == inputs["source"]["sha256"]
            and value.get("control_sha256") == inputs["control"]["sha256"]
            and value.get("watch_sha256") == inputs["watch"]["sha256"]
            and value.get("tests_sha256") == tests_sha, "floor candidate or watch mismatch")
    for name, item in inputs.items():
        if name != "floor":
            require(value.get("inputs_before", {}).get(name) == item
                    and value.get("inputs_after", {}).get(name) == item,
                    "floor input mismatch: " + name)
    verification = value.get("verification", {})
    require(verification.get("successful") is True and verification.get("complete") is True
            and verification.get("identity_valid") is True, "floor verification incomplete")
    identity = verification.get("identity", {})
    require(identity.get("version") == SLOTS["311"][1]
            and Path(identity.get("executable", "")).resolve()
            == SLOTS["311"][0].resolve(), "floor actual interpreter")
    # Bind retained floor outputs and their raw bytes, not a coordinator assertion alone.
    for role in ("stdout", "stderr", "log", "setup"):
        item = value.get("outputs", {}).get(role)
        require(type(item) is dict and valid_sha(item.get("sha256")), "floor output binding")
        pinned(handoff_file(item["path"], ".json" if role == "setup" else ".txt"),
               item["sha256"])
    return raw


def parse():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", required=True)
    parser.add_argument("--slot", choices=tuple(SLOTS), required=True)
    parser.add_argument("--kind", choices=("design", "matrix"), required=True)
    parser.add_argument("--source-path", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--control-sha", required=True)
    parser.add_argument("--watch-sha", required=True)
    parser.add_argument("--floor-receipt")
    parser.add_argument("--floor-sha")
    return parser.parse_args()


def run(arguments):
    require(sys.implementation.name == "cpython"
            and list(sys.version_info[:3]) == SLOTS["311"][1], "controller actual floor version")
    require(Path(sys.executable).resolve() == checked(SLOTS["311"][0], regular=True).resolve(),
            "controller executable")
    require(sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
            and sys.dont_write_bytecode and sys.flags.optimize == 0, "controller flags")
    require(re.fullmatch("[a-z0-9][a-z0-9-]{0,63}", arguments.label) is not None,
            "safe unique label")
    for value in (arguments.source_sha, arguments.control_sha, arguments.watch_sha):
        require(valid_sha(value), "explicit source/control/watch SHA256 required")
    require((arguments.slot == "314") == bool(arguments.floor_receipt)
            and bool(arguments.floor_receipt) == bool(arguments.floor_sha),
            "only dev requires exact matching floor receipt and SHA")
    checked(ROOT)
    checks = checked(ROOT / "tests-checks")
    checked(SNAPSHOTS)
    source = handoff_file(arguments.source_path, ".py")
    self_path = handoff_file(str(Path(__file__).absolute()), ".py")
    inputs = {
        "source": {"path": str(source), "sha256": arguments.source_sha},
        "control": {"path": str(self_path), "sha256": arguments.control_sha},
        "wrapper": {"path": str(WRAPPER), "sha256": WRAPPER_SHA},
        "population": {"path": str(POPULATION), "sha256": POPULATION_SHA},
        "watch": {"path": str(WATCH), "sha256": arguments.watch_sha},
    }
    inputs["candidate_tests"] = {"path": str(CANDIDATE_TESTS), "sha256": CANDIDATE_TESTS_SHA}
    if arguments.floor_receipt:
        inputs["floor"] = {
            "path": str(handoff_file(arguments.floor_receipt, ".json")),
            "sha256": arguments.floor_sha,
        }
    prefix = "focused-v2-" + arguments.label + "-" + arguments.kind + "-" + arguments.slot
    paths = {role: checks / (prefix + suffix) for role, suffix in {
        "receipt": "-receipt.json", "setup": "-setup.json",
        "stdout": ".stdout.txt", "stderr": ".stderr.txt", "log": ".txt",
    }.items()}
    require(not any(path.exists() for path in paths.values()), "create-only output already exists")
    streams = {}
    try:
        for role, path in paths.items():
            streams[role] = path.open("xb")
        receipt = {
            "schema": SCHEMA, "label": arguments.label, "slot": arguments.slot,
            "kind": arguments.kind, "source_path": str(source),
            "source_sha256": arguments.source_sha, "control_sha256": arguments.control_sha,
            "watch_path": str(WATCH), "watch_sha256": arguments.watch_sha,
            "tests_sha256": CANDIDATE_TESTS_SHA,
            "base_commit": BASE, "tracked_count": TRACKED_COUNT,
            "controller_executable": str(Path(sys.executable).resolve()),
            "controller_version": list(sys.version_info[:3]), "timeout_seconds": TIMEOUT,
            "inputs_before": inputs, "inputs_after": {}, "before": {}, "after": {},
            "actual_process_returncode": None, "exit": 2, "timed_out": False,
            "success": False, "integrity": False, "verification": None,
            "stage": "input_validation", "errors": [], "payload_pid": None,
            "watchdog_scope": "owned direct payload process only; no descendant-tree claim",
        }
        setup = {"schema": "c-authority-focused-setup-v1", "inputs": inputs}
        snapshot = None
        temp = None
        before = {}
        status_before = None
        command = None
        process = None
        started_at = None
        population = None
        try:
            raw_inputs = {name: pinned(Path(item["path"]), item["sha256"])
                          for name, item in inputs.items()}
            population = json.loads(raw_inputs["population"])
            require(population["schema"] == "c-authority-focused-population-v1"
                    and population["tracked_count"] == TRACKED_COUNT
                    and population["base_commit"] == BASE, "population metadata")
            if arguments.slot == "314":
                floor_binding(Path(inputs["floor"]["path"]), inputs["floor"]["sha256"],
                              inputs, arguments.kind, receipt["tests_sha256"])
            receipt["stage"] = "fresh_snapshot"
            folder = SNAPSHOTS / ("focused-authority-" + uuid.uuid4().hex)
            folder.mkdir()
            checked(folder)
            temp = folder / "temp"
            temp.mkdir()
            snapshot = folder / "snapshot"
            git(WORKSPACE, temp, "clone", "--shared", "--no-checkout",
                str(WORKSPACE), str(snapshot))
            git(snapshot, temp, "checkout", "--detach", BASE)
            require(git(snapshot, temp, "rev-parse", "HEAD").decode().strip() == BASE,
                    "snapshot HEAD")
            require(not git(snapshot, temp, "status", "--porcelain=v1", "--untracked-files=all"),
                    "dirty initial checkout")
            tracked = names_from(git(snapshot, temp, "ls-files", "-z"))
            require(len(tracked) == TRACKED_COUNT and len(set(tracked)) == TRACKED_COUNT,
                    "full r010 tracked population")
            original = file_hashes(snapshot, tracked)
            require(original[SOURCE_RELATIVE] == ORIGINAL_SOURCE_SHA
                    and original[TEST_RELATIVE] == ORIGINAL_TESTS_SHA, "r010 original source/tests")
            for relative, expected in ((SOURCE_RELATIVE, ORIGINAL_SOURCE_SHA),
                                       (TEST_RELATIVE, ORIGINAL_TESTS_SHA)):
                require(digest(git(snapshot, temp, "cat-file", "blob", BASE + ":" + relative))
                        == expected, "original blob binding")
            (snapshot / SOURCE_RELATIVE).write_bytes(raw_inputs["source"])
            (snapshot / TEST_RELATIVE).write_bytes(raw_inputs["candidate_tests"])
            payload = snapshot / PAYLOAD
            payload.mkdir()
            payload_files = {
                "control.py": raw_inputs["control"], "wrapper.py": raw_inputs["wrapper"],
                "population.json": raw_inputs["population"],
            }
            if arguments.slot == "314":
                payload_files["floor-receipt.json"] = raw_inputs["floor"]
            for name, raw in payload_files.items():
                create(payload / name, raw)
            executable, version = SLOTS[arguments.slot]
            checked(executable, regular=True)
            environment = environment_for(temp, snapshot)
            job = {
                "schema": "c-authority-focused-job-v1", "snapshot": str(snapshot),
                "payload": PAYLOAD, "temp": str(temp), "executable": str(executable),
                "version": version, "environment": environment, "kind": arguments.kind,
                "base_commit": BASE, "source_sha256": arguments.source_sha,
                "tests_sha256": receipt["tests_sha256"], "test_relative": TEST_RELATIVE,
                "control_sha256": arguments.control_sha, "wrapper_sha256": WRAPPER_SHA,
                "population_sha256": POPULATION_SHA,
                "manifest_count": TRACKED_COUNT + len(payload_files) + 1,
            }
            job_raw = encoded(job)
            create(payload / "job.json", job_raw)
            manifest_names = sorted(tracked + [
                PAYLOAD + "/" + name for name in [*payload_files, "job.json"]])
            manifest = {
                "schema": "c-authority-focused-manifest-v1", "base_commit": BASE,
                "tracked_count": TRACKED_COUNT, "files": file_hashes(snapshot, manifest_names),
            }
            manifest_raw = encoded(manifest)
            create(payload / "manifest.json", manifest_raw)
            names = sorted(manifest_names + [PAYLOAD + "/manifest.json"])
            before = file_hashes(snapshot, names)
            require(before[SOURCE_RELATIVE] == arguments.source_sha
                    and before[TEST_RELATIVE] == receipt["tests_sha256"], "overlay bytes")
            allowed_changes = sorted(name for name in (SOURCE_RELATIVE, TEST_RELATIVE)
                                     if before[name] != original[name])
            require(sorted(names_from(git(snapshot, temp, "diff", "--name-only", "-z")))
                    == allowed_changes, "unexpected tracked overlay")
            expected_untracked = sorted(name for name in names if name not in original)
            require(sorted(names_from(git(snapshot, temp, "ls-files", "--others", "-z")))
                    == expected_untracked, "unexpected untracked overlay")
            status_before = git(snapshot, temp, "status", "--porcelain=v1", "-z",
                                "--untracked-files=all")
            command = [str(executable), "-B", "-P", str(payload / "wrapper.py"),
                       str(payload / "job.json"), digest(job_raw), digest(manifest_raw)]
            identity_expected = {
                "schema": "c-authority-focused-wrapper-v1", "kind": arguments.kind,
                "version": version, "executable": str(executable.resolve()),
                "cwd": str(snapshot), "source_sha256": arguments.source_sha,
                "tests_sha256": receipt["tests_sha256"], "control_sha256": arguments.control_sha,
                "wrapper_sha256": WRAPPER_SHA, "population_sha256": POPULATION_SHA,
                "base_commit": BASE, "manifest_sha256": digest(manifest_raw),
                "manifest_count": len(manifest_names),
            }
            setup.update({
                "base_commit": BASE, "tracked_count": TRACKED_COUNT, "snapshot": str(snapshot),
                "temp": str(temp), "original": original, "before": before,
                "command": command, "environment": environment,
                "manifest_sha256": digest(manifest_raw), "job_sha256": digest(job_raw),
                "expected_identity": identity_expected, "expected_population": population[arguments.kind],
                "dirty_before": status_before.decode("utf-8"),
            })
            save_stream(streams["setup"], setup)
            receipt.update({"stage": "payload", "snapshot": str(snapshot),
                            "temp": str(temp), "before": before, "command": command,
                            "manifest_sha256": digest(manifest_raw)})
            started_at = time.monotonic()
            process = subprocess.Popen(
                command, cwd=snapshot, env=environment, stdout=streams["stdout"],
                stderr=streams["stderr"], creationflags=subprocess.CREATE_NO_WINDOW)
            receipt["payload_pid"] = process.pid
            try:
                process.wait(timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                receipt["timed_out"] = True
                process.kill()
                process.wait(timeout=10)
            receipt["actual_process_returncode"] = process.returncode
            receipt["elapsed_seconds"] = round(time.monotonic() - started_at, 6)
            for role in ("stdout", "stderr"):
                streams[role].flush()
                os.fsync(streams[role].fileno())
            stdout = paths["stdout"].read_bytes()
            verification = assess(stdout, population, arguments.kind, identity_expected)
            receipt["verification"] = verification
            if receipt["timed_out"]:
                receipt["exit"] = 124
                receipt["outcome"] = "watchdog_timeout_incomplete"
            elif process.returncode != 0:
                receipt["exit"] = process.returncode if process.returncode > 0 else 2
                receipt["outcome"] = (
                    "focused_test_failure" if process.returncode == 1
                    and verification["identity_valid"] and verification["population_valid"]
                    and not verification["bootstrap_errors"] else "payload_or_bootstrap_failure")
            elif not verification["successful"]:
                receipt["exit"] = 2
                receipt["outcome"] = "verification_incomplete_or_invalid"
            else:
                receipt["exit"] = 0
                receipt["outcome"] = "focused_pass_pending_integrity"
        except BaseException as error:
            receipt["errors"].append({"stage": receipt["stage"], "type": type(error).__name__,
                                      "message": str(error)})
            receipt["exit"] = 124 if receipt["timed_out"] else 2
            receipt["outcome"] = "watchdog_timeout_incomplete" if receipt["timed_out"] else "infrastructure_failure"
            traceback.print_exc(file=sys.stderr)
        finally:
            if process is not None and process.poll() is None:
                try:
                    process.kill()
                    process.wait(timeout=10)
                except BaseException as error:
                    receipt["errors"].append({"stage": "owned_process_cleanup",
                                              "type": type(error).__name__, "message": str(error)})
                receipt["actual_process_returncode"] = process.returncode
            receipt["stage"] = "integrity_and_retention"
            if started_at is not None:
                receipt["elapsed_seconds"] = round(time.monotonic() - started_at, 6)
            for role in ("stdout", "stderr"):
                streams[role].flush()
                os.fsync(streams[role].fileno())
            if "snapshot" not in setup:
                save_stream(streams["setup"], setup)
            try:
                receipt["inputs_after"] = {
                    name: {"path": item["path"], "sha256":
                           digest(checked(Path(item["path"]), regular=True).read_bytes())}
                    for name, item in inputs.items()}
                if snapshot is not None and before:
                    receipt["after"] = file_hashes(snapshot, list(before))
                    receipt["head_after"] = git(snapshot, temp, "rev-parse", "HEAD").decode().strip()
                    status_after = git(snapshot, temp, "status", "--porcelain=v1", "-z",
                                       "--untracked-files=all")
                    receipt["dirty_after"] = status_after.decode("utf-8")
                    all_untracked_after = sorted(names_from(git(
                        snapshot, temp, "ls-files", "--others", "-z")))
                    receipt["untracked_after"] = all_untracked_after
                    receipt["integrity"] = (
                        before == receipt["after"] and inputs == receipt["inputs_after"]
                        and receipt["head_after"] == BASE and status_after == status_before
                        and all_untracked_after == sorted(
                            name for name in before if name.startswith(PAYLOAD + "/")))
            except BaseException as error:
                receipt["errors"].append({"stage": "integrity", "type": type(error).__name__,
                                          "message": str(error)})
            if not receipt["integrity"]:
                if not receipt["timed_out"]:
                    receipt["exit"] = 2
                    receipt["outcome"] = "infrastructure_integrity_failure"
            receipt["success"] = (
                receipt["exit"] == 0 and receipt["integrity"] is True
                and not receipt["errors"] and receipt["verification"] is not None
                and receipt["verification"]["successful"] is True)
            if receipt["success"]:
                receipt["outcome"] = "focused_pass"
            elif receipt["exit"] == 0:
                receipt["exit"] = 2
                receipt["outcome"] = "verification_or_retention_failure"
            stdout = paths["stdout"].read_bytes()
            stderr = paths["stderr"].read_bytes()
            # Raw streams remain separate and exact; combined convenience log is LF normalized.
            log = (stdout + stderr).replace(b"\r\n", b"\n")
            streams["log"].write(log)
            streams["log"].flush()
            os.fsync(streams["log"].fileno())
            receipt["outputs"] = {
                role: {"path": str(paths[role]), "sha256": digest(paths[role].read_bytes()),
                       "bytes": paths[role].stat().st_size}
                for role in ("stdout", "stderr", "log", "setup")}
            receipt["stage"] = "finished"
            save_stream(streams["receipt"], receipt)
        print(json.dumps({
            "receipt": str(paths["receipt"]), "receipt_sha256": digest(paths["receipt"].read_bytes()),
            "exit": receipt["exit"], "actual_process_returncode": receipt["actual_process_returncode"],
            "success": receipt["success"], "integrity": receipt["integrity"],
            "outcome": receipt.get("outcome"), "timed_out": receipt["timed_out"],
            "snapshot": receipt.get("snapshot"), "payload_pid": receipt["payload_pid"],
            "verification": receipt["verification"],
        }, sort_keys=True))
        return receipt["exit"]
    finally:
        for stream in streams.values():
            stream.close()


if __name__ == "__main__":
    raise SystemExit(run(parse()))
