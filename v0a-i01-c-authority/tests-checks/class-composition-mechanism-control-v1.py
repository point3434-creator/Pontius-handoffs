"""Finite v19 class mechanism control; root must inspect exact bytes before execution."""

import argparse
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
V19_SHA = "3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1"
PROBE = CHECKS / "class-composition-mechanism-probe-v1.py"
PROBE_SHA = "4e2e0cb1f472a6cf7f0c38bd699f4fc54c084db29e5f903305e88f1358dbe83e"
PACK = CHECKS / "storage-composition-cases-v1.json"
PACK_SHA = "faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709"
EXTENSION = CHECKS / "scalar-class-composition-cases-v1.json"
EXTENSION_SHA = "50e88cedf77f902012237ccd88700c911fa8f3681c8dada380cca6c3142659ac"
WATCH = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1"
             r"\tools\generate_test_inventory.py")
WATCH_SHA = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
SLOTS = {
    "311": (Path(r"D:\Pontius-tools\py311\Scripts\python.exe"), (3, 11, 15)),
    "314": (Path(r"D:\Pontius\.venv\Scripts\python.exe"), (3, 14, 6)),
}
GENERATOR = "tools/generate_test_inventory.py"
CASE_IDS = {
    "original-class2": ("class-adoption-unsafe", "class-adoption-safe"),
    "scalar-class6": (
        "scalar-class-normal-unsafe", "scalar-class-normal-safe",
        "scalar-class-change-then-raise-unsafe", "scalar-class-change-then-raise-safe",
        "scalar-class-raise-before-change-unsafe", "scalar-class-raise-before-change-safe",
    ),
}
# Infrastructure watchdog only, not a scientific or analyzer admission wall.
CHILD_TIMEOUT_SECONDS = 60


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def valid_digest(value):
    return type(value) is str and re.fullmatch("[0-9a-f]{64}", value) is not None


def checked(value, directory=False):
    path = Path(value)
    require(path.is_absolute() and ".." not in path.parts, "nonabsolute/traversing path")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        require(not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT,
                "reparse path: " + str(ancestor))
    info = path.stat()
    require(stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode),
            "wrong path kind: " + str(path))
    return path


def create_bytes(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def create_json(path, value):
    create_bytes(path, (json.dumps(value, indent=2, allow_nan=False) + "\n").encode())


def environment(temporary, snapshot=None):
    windows = checked(os.environ["SYSTEMROOT"], True)
    system = checked(windows / "System32", True)
    command = checked(system / "cmd.exe")
    result = {
        "SYSTEMROOT": str(windows), "WINDIR": str(windows),
        "COMSPEC": str(command), "PATH": str(system),
        "TEMP": str(temporary), "TMP": str(temporary), "PONTIUS_GIT": str(GIT),
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "NUL",
        "GIT_CONFIG_SYSTEM": "NUL", "GIT_ATTR_NOSYSTEM": "1", "PYTHONNOUSERSITE": "1",
    }
    if snapshot is not None:
        result["PYTHONPATH"] = str(snapshot / "src")
    return result


def git(repository, temporary, *arguments):
    command = [
        str(checked(GIT)), "-c", "core.autocrlf=false", "-c", "core.hooksPath=NUL",
        "-c", "init.templateDir=", "-c", "core.attributesFile=NUL",
        "-c", "core.fsmonitor=false", "-C", str(repository), *arguments,
    ]
    return subprocess.run(command, cwd=repository, env=environment(temporary),
                          check=True, capture_output=True, timeout=60,
                          creationflags=subprocess.CREATE_NO_WINDOW).stdout


def tracked_hashes(snapshot, names):
    answer = {}
    for name in names:
        relative = Path(name)
        require(not relative.is_absolute() and ".." not in relative.parts, "unsafe tracked path")
        answer[name] = sha(checked(snapshot / relative).read_bytes())
    return answer


def require_control_runtime():
    executable, version = SLOTS["311"]
    require(sys.implementation.name == "cpython" and sys.version_info[:3] == version,
            "control requires actual CPython 3.11.15")
    require(Path(sys.executable).resolve() == executable.resolve(), "wrong control executable")
    require(sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
            and sys.dont_write_bytecode and not sys.flags.optimize, "requires -I -S -B -P")


def floor_receipt(path, digest, overlay, overlay_sha, control_sha, scope):
    require(path is not None and valid_digest(digest), "314 requires pinned 311 receipt")
    receipt_path = checked(path)
    require(receipt_path.is_relative_to(CHECKS), "floor receipt outside checks")
    raw = receipt_path.read_bytes()
    require(sha(raw) == digest, "floor receipt changed")
    receipt = json.loads(raw)
    require(receipt["schema"] == "pontius-class-composition-mechanism-receipt-v1"
            and receipt["slot"] == "311", "wrong floor receipt")
    require(receipt["base"] == BASE and receipt["overlay_source"] == str(overlay)
            and receipt["generator_sha256"] == overlay_sha, "different floor source")
    require(receipt["scope"] == scope and receipt["extension_sha256"] == EXTENSION_SHA,
            "different floor scope/extension")
    require(receipt["pack_sha256"] == PACK_SHA and receipt["probe_sha256"] == PROBE_SHA
            and receipt["control_sha256"] == control_sha, "different floor harness")
    require(receipt["infrastructure_ok"] is True
            and receipt["cases_observed"] == len(CASE_IDS[scope]),
            "floor infrastructure incomplete")
    require(receipt["oracle_errors"] == []
            and receipt["summary"]["analyzer_errors"] == [], "floor oracle/analyzer failed")
    require(receipt["identity"]["version_info"] == list(SLOTS["311"][1]), "floor identity")
    require(receipt["exit"] in (0, 1), "floor did not finish its finite probe")
    return {"path": str(receipt_path), "sha256": digest, "exit": receipt["exit"]}


def main():
    require_control_runtime()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("label")
    parser.add_argument("slot", choices=tuple(SLOTS))
    parser.add_argument("scope", choices=tuple(CASE_IDS))
    parser.add_argument("overlay_source")
    parser.add_argument("overlay_sha256")
    parser.add_argument("--control-sha256", required=True)
    parser.add_argument("--floor-receipt")
    parser.add_argument("--floor-sha256")
    arguments = parser.parse_args()
    require(re.fullmatch("[a-z0-9][a-z0-9-]{0,60}", arguments.label), "invalid label")
    require(valid_digest(arguments.overlay_sha256), "invalid explicit overlay digest")
    for directory in (ROOT, CHECKS, REPOSITORY, SNAPSHOTS):
        checked(directory, True)
    checked(GIT)
    overlay = checked(arguments.overlay_source)
    require(overlay.is_relative_to(ROOT) and overlay.suffix == ".py",
            "overlay must be an explicitly retained T Python source")
    overlay_raw = overlay.read_bytes()
    require(sha(overlay_raw) == arguments.overlay_sha256, "overlay pin mismatch")
    require(overlay == ROOT / "engineer-generator-v19.py"
            and arguments.overlay_sha256 == V19_SHA, "exact retained v19 required")
    probe_raw, pack_raw = checked(PROBE).read_bytes(), checked(PACK).read_bytes()
    require(sha(probe_raw) == PROBE_SHA and sha(pack_raw) == PACK_SHA, "harness pin mismatch")
    extension_raw = checked(EXTENSION).read_bytes()
    require(sha(extension_raw) == EXTENSION_SHA, "extension pin mismatch")
    require(sha(checked(WATCH).read_bytes()) == WATCH_SHA, "W watch changed")
    control_raw = checked(Path(__file__)).read_bytes()
    control_sha = sha(control_raw)
    require(valid_digest(arguments.control_sha256)
            and control_sha == arguments.control_sha256, "root-pinned control SHA mismatch")
    floor = None
    if arguments.slot == "314":
        floor = floor_receipt(arguments.floor_receipt, arguments.floor_sha256,
                              overlay, arguments.overlay_sha256, control_sha, arguments.scope)
    else:
        require(arguments.floor_receipt is None and arguments.floor_sha256 is None,
                "311 does not accept a floor receipt")
    stem = "class-composition-" + arguments.scope + "-" + arguments.label + "-" + arguments.slot
    setup_path = CHECKS / (stem + "-setup.json")
    log_path = CHECKS / (stem + ".txt")
    receipt_path = CHECKS / (stem + "-receipt.json")
    require(not any(path.exists() for path in (setup_path, log_path, receipt_path)),
            "label already retained; choose a new label")
    parent = SNAPSHOTS / ("class-composition-" + uuid.uuid4().hex)
    parent.mkdir()
    temporary = parent / "temp"
    temporary.mkdir()
    snapshot = parent / "snapshot"
    git(parent, temporary, "clone", "--shared", "--no-checkout", str(REPOSITORY), str(snapshot))
    git(snapshot, temporary, "checkout", "--detach", BASE)
    require(git(snapshot, temporary, "rev-parse", "HEAD").decode().strip() == BASE, "wrong HEAD")
    require(not git(snapshot, temporary, "status", "--porcelain=v1", "-z",
                    "--untracked-files=all"), "initial snapshot dirty")
    require(sha(checked(snapshot / GENERATOR).read_bytes()) == BASE_GENERATOR_SHA,
            "not exact r010 generator")
    (snapshot / GENERATOR).write_bytes(overlay_raw)
    before_status = git(snapshot, temporary, "status", "--porcelain=v1", "-z",
                        "--untracked-files=all")
    require(before_status == b" M tools/generate_test_inventory.py\0", "extra overlay paths")
    names_raw = git(snapshot, temporary, "ls-tree", "-r", "-z", "--name-only", BASE)
    names = names_raw.decode("utf-8").rstrip("\0").split("\0")
    require(len(names) == 1761 and len(set(names)) == 1761, "r010 tracked count")
    before = tracked_hashes(snapshot, names)
    require(before[GENERATOR] == arguments.overlay_sha256, "copied overlay mismatch")
    probe_copy = parent / PROBE.name
    pack_copy = parent / PACK.name
    create_bytes(probe_copy, probe_raw)
    create_bytes(pack_copy, pack_raw)
    extension_copy = parent / EXTENSION.name
    control_copy = parent / Path(__file__).name
    create_bytes(extension_copy, extension_raw)
    create_bytes(control_copy, control_raw)
    executable, version = SLOTS[arguments.slot]
    checked(executable)
    command = [
        str(executable), "-B", "-P", str(probe_copy), arguments.slot,
        arguments.overlay_sha256, str(pack_copy), str(extension_copy), PROBE_SHA, arguments.scope,
    ]
    child_environment = environment(temporary, snapshot)
    setup = {
        "schema": "pontius-class-composition-mechanism-setup-v1", "base": BASE,
        "slot": arguments.slot, "label": arguments.label, "scope": arguments.scope,
        "overlay_source": str(overlay), "extension_sha256": EXTENSION_SHA,
        "production_watch_sha256": WATCH_SHA,
        "generator_sha256": arguments.overlay_sha256, "baseline_generator_sha256": V19_SHA,
        "frozen_r010_generator_sha256": BASE_GENERATOR_SHA,
        "pack_sha256": PACK_SHA, "probe_sha256": PROBE_SHA, "control_sha256": control_sha,
        "snapshot": str(snapshot), "temporary": str(temporary), "before": before,
        "command": command, "environment": child_environment, "floor_receipt": floor,
        "watchdog_seconds": CHILD_TIMEOUT_SECONDS,
    }
    create_json(setup_path, setup)
    exit_code, child_error = None, None
    with log_path.open("xb") as log:
        try:
            process = subprocess.Popen(command, cwd=snapshot, env=child_environment,
                                       stdout=log, stderr=subprocess.STDOUT,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
            print(json.dumps({"child_pid": process.pid, "log": str(log_path)}), flush=True)
            try:
                exit_code = process.wait(timeout=CHILD_TIMEOUT_SECONDS)
            except subprocess.TimeoutExpired:
                child_error = "infrastructure watchdog expired"
                process.terminate()
                try:
                    exit_code = process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    exit_code = process.wait(timeout=10)
            except BaseException:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=10)
                raise
        except BaseException as error:
            child_error = type(error).__name__ + ": " + str(error)
    output = log_path.read_bytes()
    errors = []
    if child_error is not None:
        errors.append(child_error)
    after, after_status = {}, None
    try:
        after = tracked_hashes(snapshot, names)
        after_status = git(snapshot, temporary, "status", "--porcelain=v1", "-z",
                           "--untracked-files=all")
        require(git(snapshot, temporary, "rev-parse", "HEAD").decode().strip() == BASE,
                "snapshot HEAD changed")
        require(after == before and after_status == before_status, "snapshot paths changed")
        require(sha(checked(probe_copy).read_bytes()) == PROBE_SHA
                and sha(checked(pack_copy).read_bytes()) == PACK_SHA
                and sha(checked(extension_copy).read_bytes()) == EXTENSION_SHA
                and sha(checked(control_copy).read_bytes()) == control_sha,
                "copied harness changed")
        require(sha(checked(PROBE).read_bytes()) == PROBE_SHA
                and sha(checked(PACK).read_bytes()) == PACK_SHA
                and sha(checked(overlay).read_bytes()) == arguments.overlay_sha256,
                "retained input changed")
        require(sha(checked(EXTENSION).read_bytes()) == EXTENSION_SHA
                and sha(checked(Path(__file__)).read_bytes()) == control_sha
                and sha(checked(WATCH).read_bytes()) == WATCH_SHA, "extension/control/W changed")
    except Exception as error:
        errors.append(type(error).__name__ + ": " + str(error))
    records = []
    try:
        require(b"\r" not in output, "log is not LF")
        records = [json.loads(line) for line in output.splitlines() if line.startswith(b"{")]
    except Exception as error:
        errors.append(type(error).__name__ + ": " + str(error))
    identity, summary = {}, {}
    cases = [record for record in records if "storage_composition_case" in record]
    oracle_errors, failures = [], []
    try:
        identity = records[0]["identity_before_imports"]
        require(identity["version_info"] == list(version)
                and Path(identity["executable"]).resolve() == executable.resolve()
                and identity["cwd"] == str(snapshot), "wrong payload identity")
        summaries = [record for record in records if record.get("storage_composition_summary")]
        require(len(summaries) == 1, "missing/duplicate probe summary")
        summary = summaries[0]
        require(tuple(case["storage_composition_case"] for case in cases)
                == CASE_IDS[arguments.scope],
                "missing/extra/reordered case records")
        expected_cases = (json.loads(pack_raw)["cases"][2:]
                          if arguments.scope == "original-class2"
                          else json.loads(extension_raw)["cases"])
        for case, expected in zip(cases, expected_cases, strict=True):
            require(case["classification"] == expected["classification"]
                    and case["source_sha256"] == expected["source_sha256"]
                    and case["oracle_sha256"] == expected["oracle_sha256"], "case identity drift")
            oracle_ok = (case["oracle_passed"] is True
                         and case["oracle_actual"] == expected["expected"])
            if not oracle_ok:
                oracle_errors.append(expected["id"])
            passed = (oracle_ok and case["analyzer_error"] is None
                      and (bool(case["blockers"]) if expected["classification"] == "refuse" else
                           not case["blockers"] and case["argv"] == expected["required_argv"]))
            require(case["semantic_passed"] is passed, "semantic result inconsistency")
            if not passed:
                failures.append(expected["id"])
        require(summary["failures"] == failures and summary["oracle_errors"] == oracle_errors,
                "summary differs from case records")
        require(summary["generator_sha256"] == arguments.overlay_sha256
                and summary["probe_sha256"] == PROBE_SHA
                and summary["original_pack_sha256"] == PACK_SHA
                and summary["extension_pack_sha256"] == EXTENSION_SHA
                and summary["scope"] == arguments.scope
                and summary["pack_sha256"] == (PACK_SHA if arguments.scope == "original-class2"
                                               else EXTENSION_SHA),
                "summary identity mismatch")
        require(summary["analyzed_cases"] == len(expected_cases)
                and summary["analyzer_errors"] == [], "analyzer did not finish finite scope")
        require(any("class_adoption_mechanism" in record for record in records),
                "mechanism observations missing")
        require(exit_code == int(bool(failures)), "exit/result mismatch")
    except Exception as error:
        errors.append(type(error).__name__ + ": " + str(error))
    receipt = {
        **setup, "schema": "pontius-storage-composition-receipt-v1",
        "setup_sha256": sha(setup_path.read_bytes()), "exit": exit_code,
        "log": str(log_path), "log_sha256": sha(output), "after": after,
        "status_after": after_status.decode("utf-8") if after_status is not None else None,
        "all_tracked_paths_unchanged": len(before) if after == before else 0,
        "identity": identity, "summary": summary, "cases_observed": len(cases),
        "oracle_errors": oracle_errors, "failures": failures,
        "mechanism_events": sum("class_adoption_mechanism" in record for record in records),
        "infrastructure_errors": errors, "infrastructure_ok": not errors,
    }
    create_json(receipt_path, receipt)
    print(json.dumps({"receipt": str(receipt_path),
                      "receipt_sha256": sha(receipt_path.read_bytes()),
                      "exit": exit_code, "failures": failures, "infrastructure_errors": errors}),
          flush=True)
    return 2 if errors else int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
