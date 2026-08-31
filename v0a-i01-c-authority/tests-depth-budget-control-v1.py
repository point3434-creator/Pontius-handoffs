"""Two-case floor-only budget diagnostic control, for root review before use.

Invoke with actual CPython 3.11.15 and -I -S -B -P.
No candidate/probe import or payload occurs unless main is explicitly dispatched.
"""
import argparse
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
EXE = Path(r"D:\Pontius-tools\py311\Scripts\python.exe")
VERSION = [3, 11, 15]
BASE = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
BASE_SOURCE_SHA = "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
TEST_SHA = "c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf"
SOURCE_RELATIVE = "tools/generate_test_inventory.py"
TEST_RELATIVE = "tests/test_inventory_and_profiles.py"
PROBE = ROOT / "engineer-depth-budget-probe-v1.py"
CASES = ("helper1050", "generator70")
TRACKED_COUNT = 1761
TIMEOUT = 60
PAYLOAD = ".depth-budget-diagnostic"
SCHEMA = "c-authority-depth-budget-control-v1"


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def is_sha(value):
    return type(value) is str and re.fullmatch("[0-9a-f]{64}", value) is not None


def checked(path, regular=False):
    require(path.is_absolute() and ".." not in path.parts, "unsafe absolute path")
    for part in (path, *path.parents):
        info = part.lstat()
        require(not (getattr(info, "st_file_attributes", 0)
                     & stat.FILE_ATTRIBUTE_REPARSE_POINT), "reparse path: " + str(part))
        if part != path:
            require(stat.S_ISDIR(info.st_mode), "nondirectory ancestor")
    require(stat.S_ISREG(path.lstat().st_mode) if regular else path.is_dir(),
            "wrong path kind: " + str(path))
    return path


def retained(value):
    path = Path(value)
    require(path.is_absolute() and path.is_relative_to(ROOT) and path.suffix == ".py",
            "candidate must be a retained T Python file")
    return path


def pinned(path, expected):
    require(is_sha(expected), "invalid SHA256")
    raw = checked(path, regular=True).read_bytes()
    require(digest(raw) == expected, "input hash mismatch: " + str(path))
    return raw


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")


def create(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def save(stream, value):
    # Same exclusive unpublished output stream; no issued artifact is overwritten.
    stream.seek(0)
    stream.write(json_bytes(value))
    stream.truncate()
    stream.flush()
    os.fsync(stream.fileno())


def environment_for(temp, snapshot=None):
    windows = checked(Path(os.environ["SYSTEMROOT"]))
    system = checked(windows / "System32")
    environment = {
        "SYSTEMROOT": str(windows), "WINDIR": str(windows),
        "COMSPEC": str(checked(system / "cmd.exe", regular=True)), "PATH": str(system),
        "TEMP": str(temp), "TMP": str(temp),
        "PONTIUS_GIT": str(checked(GIT, regular=True)),
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "NUL",
        "GIT_CONFIG_SYSTEM": "NUL", "GIT_ATTR_NOSYSTEM": "1",
        "PYTHONNOUSERSITE": "1",
    }
    if snapshot is not None:
        environment["PYTHONPATH"] = str(snapshot / "src")
    return environment


def git(repository, temp, *arguments):
    return subprocess.run(
        [str(checked(GIT, regular=True)), "-c", "core.autocrlf=false",
         "-c", "core.hooksPath=NUL", "-c", "init.templateDir=",
         "-c", "core.attributesFile=NUL", "-c", "core.fsmonitor=false",
         "-C", str(repository), *arguments],
        cwd=repository, env=environment_for(temp), check=True, capture_output=True,
        timeout=TIMEOUT, creationflags=subprocess.CREATE_NO_WINDOW,
    ).stdout


def names(raw):
    return [item.decode("utf-8") for item in raw.split(b"\0") if item]


def hashes(snapshot, relative_names):
    found = {}
    for name in relative_names:
        relative = Path(name)
        require(not relative.is_absolute() and not relative.drive
                and ".." not in relative.parts, "unsafe manifest name")
        path = snapshot / relative
        require(path.is_relative_to(snapshot), "manifest path escape")
        found[name] = digest(checked(path, regular=True).read_bytes())
    return found


WRAPPER = r'''"""Pre-import identity and complete snapshot binding for one diagnostic."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import runpy
import stat
import sys
import traceback

def req(value, message):
    if not value:
        raise RuntimeError(message)

def h(raw):
    return hashlib.sha256(raw).hexdigest()

def checked(path, regular=True):
    req(path.is_absolute() and ".." not in path.parts, "unsafe bootstrap path")
    for parent in (path, *path.parents):
        info = parent.lstat()
        req(not (getattr(info, "st_file_attributes", 0)
                 & stat.FILE_ATTRIBUTE_REPARSE_POINT), "bootstrap reparse path")
        if parent != path:
            req(stat.S_ISDIR(info.st_mode), "bootstrap ancestor")
    req(stat.S_ISREG(path.lstat().st_mode) if regular else path.is_dir(),
        "bootstrap path kind")
    return path

def main():
    sys.stdout.reconfigure(newline="\n")
    sys.stderr.reconfigure(newline="\n")
    req(len(sys.argv) == 4, "bootstrap arguments")
    job_path = checked(Path(sys.argv[1]))
    raw = job_path.read_bytes()
    req(h(raw) == sys.argv[2], "job bytes")
    job = json.loads(raw)
    req(job["schema"] == "c-authority-depth-budget-job-v1", "job schema")
    req(job["case"] in ("helper1050", "generator70"), "bounded case")
    req(sys.implementation.name == "cpython"
        and list(sys.version_info[:3]) == [3, 11, 15], "actual floor patch")
    req(Path(sys.executable).resolve() == checked(Path(job["executable"])).resolve(),
        "actual floor executable")
    req(sys.flags.safe_path and sys.dont_write_bytecode and not sys.flags.optimize
        and not sys.flags.isolated and not sys.flags.ignore_environment
        and not sys.flags.no_site and sys.flags.no_user_site == 1, "payload flags")
    snapshot = checked(Path(job["snapshot"]), regular=False)
    req(Path.cwd().resolve() == snapshot.resolve(), "snapshot cwd")
    req(Path(__file__).resolve() == snapshot / job["payload"] / "wrapper.py",
        "bootstrap location")
    req(job_path == snapshot / job["payload"] / "job.json", "job location")
    req(dict(os.environ) == job["environment"], "scrubbed environment mismatch")
    req(os.environ["PYTHONPATH"] == str(snapshot / "src"), "snapshot PYTHONPATH")
    req(os.environ["TEMP"] == job["temp"] and os.environ["TMP"] == job["temp"],
        "D-local temporary directory")
    checked(Path(job["temp"]), regular=False)
    checked(Path(os.environ["PONTIUS_GIT"]))
    req("PYTHONHASHSEED" not in os.environ, "original focused hash-seed behavior")
    req(not any(name == "pontius" or name.startswith("pontius.")
                for name in sys.modules), "premature repository import")
    manifest_path = checked(snapshot / job["payload"] / "manifest.json")
    manifest_raw = manifest_path.read_bytes()
    req(h(manifest_raw) == sys.argv[3], "manifest bytes")
    manifest = json.loads(manifest_raw)
    req(manifest["schema"] == "c-authority-depth-budget-manifest-v1"
        and manifest["base_commit"] == job["base_commit"]
        and type(manifest["tracked_count"]) is int
        and manifest["tracked_count"] == 1761, "manifest identity")
    req(len(manifest["files"]) == 1765, "manifest population")
    for name, expected in manifest["files"].items():
        relative = Path(name)
        req(not relative.is_absolute() and not relative.drive and ".." not in relative.parts,
            "relative manifest path")
        req(h(checked(snapshot / relative).read_bytes()) == expected, "file hash: " + name)
    req(manifest["files"]["tools/generate_test_inventory.py"] == job["source_sha256"],
        "candidate hash")
    req(manifest["files"]["tests/test_inventory_and_profiles.py"] == job["tests_sha256"],
        "original fixture hash")
    for name in ("probe", "control"):
        req(manifest["files"][job["payload"] + "/" + name + ".py"] == job[name + "_sha256"],
            name + " hash")
    spec = importlib.util.find_spec("pontius")
    req(spec is not None and spec.origin is not None
        and Path(spec.origin).resolve() == snapshot / "src/pontius/__init__.py",
        "project resolution")
    print(json.dumps({"identity_before_payload_imports": {
        "schema": "c-authority-depth-budget-identity-v1", "case": job["case"],
        "executable": str(Path(sys.executable).resolve()),
        "version_info": list(sys.version_info[:3]), "version": sys.version,
        "implementation": sys.implementation.name, "cwd": str(snapshot),
        "safe_path": bool(sys.flags.safe_path), "dont_write_bytecode": sys.dont_write_bytecode,
        "optimize": sys.flags.optimize, "isolated": sys.flags.isolated,
        "ignore_environment": sys.flags.ignore_environment, "no_site": sys.flags.no_site,
        "no_user_site": sys.flags.no_user_site, "environment": dict(os.environ),
        "source_sha256": job["source_sha256"], "tests_sha256": job["tests_sha256"],
        "probe_sha256": job["probe_sha256"], "control_sha256": job["control_sha256"],
        "manifest_sha256": sys.argv[3], "tracked_count": 1761, "manifest_count": 1765,
    }}, sort_keys=True), flush=True)
    sys.argv = [str(snapshot / job["payload"] / "probe.py"), "--case", job["case"]]
    runpy.run_path(sys.argv[0], run_name="__main__")

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException as error:
        print(json.dumps({"depth_budget_bootstrap_error": {
            "type": type(error).__name__, "message": str(error)}}, sort_keys=True), flush=True)
        traceback.print_exc()
        raise SystemExit(2)
'''


def records(raw):
    parsed, malformed = [], []
    for number, line in enumerate(raw.decode("utf-8", errors="replace").splitlines(), 1):
        if not line.startswith("{"):
            continue
        try:
            value = json.loads(line)
        except ValueError:
            malformed.append(number)
            continue
        if type(value) is dict:
            parsed.append(value)
    return parsed, malformed


def assess(raw, case, expected_identity, source_sha):
    parsed, malformed = records(raw)
    identities = [row["identity_before_payload_imports"] for row in parsed
                  if "identity_before_payload_imports" in row]
    completions = [row["depth_budget_diagnostic_complete"] for row in parsed
                   if "depth_budget_diagnostic_complete" in row]
    failures = [row["depth_budget_failure"] for row in parsed if "depth_budget_failure" in row]
    bootstrap_errors = [row["depth_budget_bootstrap_error"] for row in parsed
                        if "depth_budget_bootstrap_error" in row]
    identity = identities[0] if len(identities) == 1 and type(identities[0]) is dict else None
    identity_valid = identity is not None and all(
        identity.get(key) == value for key, value in expected_identity.items())
    if identity_valid:
        identity_valid = (identity.get("safe_path") is True
                          and identity.get("dont_write_bytecode") is True
                          and all(type(identity.get(key)) is int and identity[key] == value
                                  for key, value in {"optimize": 0, "isolated": 0,
                                                     "ignore_environment": 0, "no_site": 0,
                                                     "no_user_site": 1, "tracked_count": 1761,
                                                     "manifest_count": 1765}.items()))
    completion = completions[0] if len(completions) == 1 and type(completions[0]) is dict else None
    complete = (completion is not None and completion.get("case") == case
                and completion.get("completed") is True
                and completion.get("caps_unchanged") is True
                and completion.get("original_methods_restored") is True
                and completion.get("source_sha256") == source_sha
                and completion.get("tests_sha256") == TEST_SHA)
    return {
        "identity": identity, "identity_valid": identity_valid, "completion": completion,
        "complete": complete, "failure_records": failures, "bootstrap_errors": bootstrap_errors,
        "malformed_json_lines": malformed, "json_record_count": len(parsed),
        "valid": bool(identity_valid and complete and not malformed and not bootstrap_errors),
        "meaning": "Diagnostic completion is not a product pass or a cold review verdict.",
    }


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", required=True)
    parser.add_argument("--case", choices=CASES, required=True)
    parser.add_argument("--source-path", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--probe-sha", required=True)
    parser.add_argument("--control-sha", required=True)
    parser.add_argument("--watch-sha", required=True)
    return parser.parse_args()


def run(args):
    require(sys.implementation.name == "cpython" and list(sys.version_info[:3]) == VERSION,
            "controller actual floor version")
    require(Path(sys.executable).resolve() == checked(EXE, regular=True).resolve(),
            "controller actual executable")
    require(sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
            and sys.dont_write_bytecode and not sys.flags.optimize, "controller isolation")
    require(re.fullmatch("[a-z0-9][a-z0-9-]{0,63}", args.label) is not None, "unique safe label")
    require(all(is_sha(value) for value in
                (args.source_sha, args.probe_sha, args.control_sha, args.watch_sha)),
            "all input SHA256 values must be explicit")
    source = retained(args.source_path)
    control = retained(str(Path(__file__).absolute()))
    checked(ROOT)
    checks = checked(ROOT / "tests-checks")
    checked(SNAPSHOTS)
    inputs = {
        "source": {"path": str(source), "sha256": args.source_sha},
        "probe": {"path": str(PROBE), "sha256": args.probe_sha},
        "control": {"path": str(control), "sha256": args.control_sha},
        "watch": {"path": str(WATCH), "sha256": args.watch_sha},
    }
    prefix = "depth-budget-" + args.label + "-" + args.case + "-311"
    paths = {name: checks / (prefix + suffix) for name, suffix in {
        "setup": "-setup.json", "receipt": "-receipt.json", "stdout": ".stdout.txt",
        "stderr": ".stderr.txt", "log": ".txt",
    }.items()}
    require(not any(path.exists() for path in paths.values()), "create-only outputs exist")
    streams = {}
    try:
        for name, path in paths.items():
            streams[name] = path.open("xb")
        receipt = {
            "schema": SCHEMA, "label": args.label, "case": args.case, "slot": "311",
            "scope": "One exact original fixture through its original _review envelope; static source only.",
            "base_commit": BASE, "tracked_count": TRACKED_COUNT,
            "source_path": str(source), "source_sha256": args.source_sha,
            "tests_sha256": TEST_SHA, "probe_sha256": args.probe_sha,
            "control_sha256": args.control_sha, "watch_sha256": args.watch_sha,
            "inputs_before": inputs, "inputs_after": {}, "before": {}, "after": {},
            "controller_executable": str(Path(sys.executable).resolve()),
            "controller_version": VERSION, "timeout_seconds": TIMEOUT,
            "timed_out": False, "payload_pid": None, "actual_process_returncode": None,
            "exit": 2, "integrity": False, "diagnostic_completed": False,
            "product_verdict": "not issued by this diagnostic controller",
            "watchdog_scope": "owned direct payload process; no descendant-tree claim",
            "stage": "input_validation", "errors": [], "verification": None,
        }
        setup = {"schema": "c-authority-depth-budget-setup-v1", "inputs": inputs}
        snapshot, temporary, process, started_at = None, None, None, None
        before, original, status_before = {}, {}, None
        try:
            raw_inputs = {name: pinned(Path(item["path"]), item["sha256"])
                          for name, item in inputs.items()}
            receipt["stage"] = "fresh_snapshot"
            folder = SNAPSHOTS / ("depth-budget-" + uuid.uuid4().hex)
            folder.mkdir()
            checked(folder)
            temporary = folder / "temp"
            temporary.mkdir()
            snapshot = folder / "snapshot"
            git(folder, temporary, "clone", "--shared", "--no-checkout",
                str(WORKSPACE), str(snapshot))
            checked(snapshot)
            git(snapshot, temporary, "checkout", "--detach", BASE)
            require(git(snapshot, temporary, "rev-parse", "HEAD").decode().strip() == BASE,
                    "snapshot commit")
            require(not git(snapshot, temporary, "status", "--porcelain=v1", "--untracked-files=all"),
                    "dirty initial snapshot")
            tracked = names(git(snapshot, temporary, "ls-files", "-z"))
            committed = names(git(snapshot, temporary, "ls-tree", "-r", "-z", "--name-only", BASE))
            require(len(tracked) == TRACKED_COUNT and len(set(tracked)) == TRACKED_COUNT
                    and set(tracked) == set(committed), "exact r0101761 population")
            original = hashes(snapshot, tracked)
            require(original[SOURCE_RELATIVE] == BASE_SOURCE_SHA
                    and original[TEST_RELATIVE] == TEST_SHA, "original source/test bytes")
            (snapshot / SOURCE_RELATIVE).write_bytes(raw_inputs["source"])
            require(names(git(snapshot, temporary, "diff", "--name-only", "-z"))
                    == [SOURCE_RELATIVE], "only candidate source overlay allowed")
            payload = snapshot / PAYLOAD
            payload.mkdir()
            payload_files = {"probe.py": raw_inputs["probe"], "control.py": raw_inputs["control"],
                             "wrapper.py": WRAPPER.encode("utf-8")}
            for name, raw in payload_files.items():
                create(payload / name, raw)
            environment = environment_for(temporary, snapshot)
            job = {
                "schema": "c-authority-depth-budget-job-v1", "case": args.case,
                "snapshot": str(snapshot), "temp": str(temporary), "payload": PAYLOAD,
                "executable": str(EXE), "environment": environment, "base_commit": BASE,
                "source_sha256": args.source_sha, "tests_sha256": TEST_SHA,
                "probe_sha256": args.probe_sha, "control_sha256": args.control_sha,
            }
            job_raw = json_bytes(job)
            create(payload / "job.json", job_raw)
            manifest_names = sorted(tracked + [PAYLOAD + "/" + name
                                               for name in [*payload_files, "job.json"]])
            manifest_raw = json_bytes({
                "schema": "c-authority-depth-budget-manifest-v1", "base_commit": BASE,
                "tracked_count": TRACKED_COUNT, "files": hashes(snapshot, manifest_names),
            })
            create(payload / "manifest.json", manifest_raw)
            before = hashes(snapshot, manifest_names + [PAYLOAD + "/manifest.json"])
            require(before[SOURCE_RELATIVE] == args.source_sha
                    and before[TEST_RELATIVE] == TEST_SHA, "exact source-only candidate")
            expected_untracked = sorted(name for name in before if name not in original)
            require(sorted(names(git(snapshot, temporary, "ls-files", "--others", "-z")))
                    == expected_untracked, "unexpected snapshot payload")
            status_before = git(snapshot, temporary, "status", "--porcelain=v1", "-z",
                                "--untracked-files=all")
            command = [str(EXE), "-B", "-P", str(payload / "wrapper.py"),
                       str(payload / "job.json"), digest(job_raw), digest(manifest_raw)]
            expected_identity = {
                "schema": "c-authority-depth-budget-identity-v1", "case": args.case,
                "executable": str(EXE.resolve()), "version_info": VERSION,
                "implementation": "cpython", "cwd": str(snapshot), "environment": environment,
                "source_sha256": args.source_sha, "tests_sha256": TEST_SHA,
                "probe_sha256": args.probe_sha, "control_sha256": args.control_sha,
                "manifest_sha256": digest(manifest_raw),
            }
            setup.update({
                "case": args.case, "base_commit": BASE, "tracked_count": TRACKED_COUNT,
                "snapshot": str(snapshot), "temp": str(temporary), "original": original,
                "before": before, "command": command, "environment": environment,
                "job_sha256": digest(job_raw), "manifest_sha256": digest(manifest_raw),
                "wrapper_sha256": digest(WRAPPER.encode("utf-8")),
                "expected_identity": expected_identity, "dirty_before": status_before.decode(),
            })
            save(streams["setup"], setup)
            receipt.update({"stage": "payload", "snapshot": str(snapshot), "temp": str(temporary),
                            "command": command, "before": before,
                            "manifest_sha256": digest(manifest_raw)})
            started_at = time.monotonic()
            process = subprocess.Popen(
                command, cwd=snapshot, env=environment, stdout=streams["stdout"],
                stderr=streams["stderr"], creationflags=subprocess.CREATE_NO_WINDOW)
            receipt["payload_pid"] = process.pid
            print(json.dumps({"depth_budget_owned_child": process.pid, "case": args.case,
                              "stdout": str(paths["stdout"]), "stderr": str(paths["stderr"])},
                             sort_keys=True), flush=True)
            try:
                process.wait(timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                receipt["timed_out"] = True
                process.kill()
                process.wait(timeout=10)
            receipt["actual_process_returncode"] = process.returncode
            for name in ("stdout", "stderr"):
                streams[name].flush()
                os.fsync(streams[name].fileno())
            verification = assess(paths["stdout"].read_bytes(), args.case,
                                  expected_identity, args.source_sha)
            receipt["verification"] = verification
            if receipt["timed_out"]:
                receipt["exit"] = 124
                receipt["outcome"] = "watchdog_timeout_incomplete"
            elif process.returncode != 0:
                receipt["exit"] = process.returncode if process.returncode > 0 else 2
                receipt["outcome"] = "diagnostic_payload_failure"
            elif not verification["valid"]:
                receipt["exit"] = 2
                receipt["outcome"] = "diagnostic_evidence_incomplete_or_invalid"
            else:
                receipt["exit"] = 0
                receipt["outcome"] = "diagnostic_complete_pending_integrity"
        except BaseException as error:
            receipt["errors"].append({"stage": receipt["stage"], "type": type(error).__name__,
                                      "message": str(error)})
            receipt["exit"] = 124 if receipt["timed_out"] else 2
            receipt["outcome"] = ("watchdog_timeout_incomplete" if receipt["timed_out"]
                                  else "diagnostic_infrastructure_failure")
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
            if started_at is not None:
                receipt["elapsed_seconds"] = round(time.monotonic() - started_at, 6)
            receipt["stage"] = "integrity_and_retention"
            for name in ("stdout", "stderr"):
                streams[name].flush()
                os.fsync(streams[name].fileno())
            if "snapshot" not in setup:
                save(streams["setup"], setup)
            try:
                receipt["inputs_after"] = {
                    name: {"path": item["path"],
                           "sha256": digest(checked(Path(item["path"]), regular=True).read_bytes())}
                    for name, item in inputs.items()}
                if snapshot is not None and before:
                    receipt["after"] = hashes(snapshot, list(before))
                    head = git(snapshot, temporary, "rev-parse", "HEAD").decode().strip()
                    status = git(snapshot, temporary, "status", "--porcelain=v1", "-z",
                                 "--untracked-files=all")
                    untracked = sorted(names(git(snapshot, temporary, "ls-files", "--others", "-z")))
                    receipt.update({"head_after": head, "dirty_after": status.decode(),
                                    "untracked_after": untracked})
                    receipt["integrity"] = (
                        before == receipt["after"] and inputs == receipt["inputs_after"]
                        and head == BASE and status == status_before
                        and untracked == sorted(name for name in before if name.startswith(PAYLOAD + "/")))
            except BaseException as error:
                receipt["errors"].append({"stage": "integrity", "type": type(error).__name__,
                                          "message": str(error)})
            if not receipt["integrity"] and not receipt["timed_out"]:
                receipt["exit"] = 2
                receipt["outcome"] = "diagnostic_infrastructure_integrity_failure"
            receipt["diagnostic_completed"] = (
                receipt["exit"] == 0 and receipt["integrity"] is True and not receipt["errors"]
                and receipt["verification"] is not None and receipt["verification"]["valid"] is True)
            if receipt["diagnostic_completed"]:
                receipt["outcome"] = "diagnostic_completed_not_product_verdict"
            elif receipt["exit"] == 0:
                receipt["exit"] = 2
                receipt["outcome"] = "diagnostic_retention_failure"
            stdout, stderr = paths["stdout"].read_bytes(), paths["stderr"].read_bytes()
            log = (stdout + stderr).replace(b"\r\n", b"\n")
            streams["log"].write(log)
            streams["log"].flush()
            os.fsync(streams["log"].fileno())
            receipt["outputs"] = {
                name: {"path": str(paths[name]), "sha256": digest(paths[name].read_bytes()),
                       "bytes": paths[name].stat().st_size}
                for name in ("setup", "stdout", "stderr", "log")}
            receipt["stage"] = "finished"
            save(streams["receipt"], receipt)
        print(json.dumps({
            "case": args.case, "exit": receipt["exit"], "outcome": receipt["outcome"],
            "diagnostic_completed": receipt["diagnostic_completed"], "integrity": receipt["integrity"],
            "timed_out": receipt["timed_out"], "payload_pid": receipt["payload_pid"],
            "actual_process_returncode": receipt["actual_process_returncode"],
            "receipt": str(paths["receipt"]), "receipt_sha256": digest(paths["receipt"].read_bytes()),
            "snapshot": receipt.get("snapshot"),
        }, sort_keys=True))
        return receipt["exit"]
    finally:
        for stream in streams.values():
            stream.close()


if __name__ == "__main__":
    raise SystemExit(run(arguments()))
