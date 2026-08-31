"""Original ten composition replay control; authoring is not run permission.

Run this controller with exact floor Python 3.11.15 and -I -S -B -P.
Arguments: LABEL SLOT RETAINED_SOURCE_ABSOLUTE SOURCE_SHA --control-sha256 SHA
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
PROBE = CHECKS / "original-composition-ten-probe-v1.py"
PROBE_SHA = "e2564b1d1d61c0a92e449f80eb5118eb72141b3fabd9022cf2b2881d1c56927e"

PACKS = {
    "storage": {
        "file": "storage-composition-cases-v1.json",
        "sha256": "faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709",
        "schema": "pontius-storage-composition-cases-v1",
        "ids": ("shared-list-consumed", "shared-list-dormant",
                "class-adoption-unsafe", "class-adoption-safe"),
        "classifications": {"clean": 2, "refuse": 2},
    },
    "scalar": {
        "file": "scalar-class-composition-cases-v1.json",
        "sha256": "50e88cedf77f902012237ccd88700c911fa8f3681c8dada380cca6c3142659ac",
        "schema": "pontius-scalar-class-composition-cases-v1",
        "ids": ("scalar-class-normal-unsafe", "scalar-class-normal-safe",
                "scalar-class-change-then-raise-unsafe", "scalar-class-change-then-raise-safe",
                "scalar-class-raise-before-change-unsafe", "scalar-class-raise-before-change-safe"),
        "classifications": {"clean": 3, "refuse": 3},
    },
}
PACK_HASHES = {scope: metadata["sha256"] for scope, metadata in PACKS.items()}

PLAN = CHECKS / "original-composition-ten-plan-v1.md"
PLAN_SHA = "3b330b732d99bdf02bae7b270a57f1d9cc0352fe1db573f5148c751084ad3f1a"
SLOTS = {
    "311": (Path(r"D:\Pontius-tools\py311\Scripts\python.exe"), (3, 11, 15)),
    "314": (Path(r"D:\Pontius\.venv\Scripts\python.exe"), (3, 14, 6)),
}
CAPS = {
    "MAXIMUM_ANALYSIS_HELPER_DEPTH": 64, "MAXIMUM_ANALYSIS_CHILD_DEPTH": 4,
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS": 4096,
    "MAXIMUM_ANALYSIS_CARDINALITY": 2147483647, "MAXIMUM_ANALYSIS_WORK_UNITS": 262144,
}
SCHEMA = "pontius-original-composition-ten-v1"
PAYLOAD = ".original-composition-ten"
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



def load_cases(raw_by_scope):
    require(set(raw_by_scope) == set(PACKS), "exact original pack set")
    combined = []
    for scope, metadata in PACKS.items():
        raw = raw_by_scope[scope]
        require(hashlib.sha256(raw).hexdigest() == metadata["sha256"], "original pack pin: " + scope)
        pack = json.loads(raw)
        count = len(metadata["ids"])
        require(pack["schema"] == metadata["schema"], "original pack schema")
        require(type(pack["planned_cases"]) is int and pack["planned_cases"] == count
                and type(pack["planned_projections"]) is int and pack["planned_projections"] == count,
                "original finite counts")
        require(tuple(case["id"] for case in pack["cases"]) == metadata["ids"], "original case order")
        require(dict(Counter(case["classification"] for case in pack["cases"]))
                == metadata["classifications"], "original classifications")
        for case in pack["cases"]:
            for field, hash_field in (("source", "source_sha256"), ("oracle_source", "oracle_sha256")):
                value = case[field]
                require(type(value) is str and value.endswith("\n") and "\r" not in value,
                        "original source format")
                require(hashlib.sha256(value.encode("utf-8")).hexdigest() == case[hash_field],
                        "original source/model digest")
                # Both are parsed; only the original harmless Model runner compiles its model.
                ast.parse(value, filename="<unexecuted-original-composition-bytes>")
            combined.append((scope, case))
    require(len(combined) == 10, "original combined scope")
    return combined



def validate_result(stdout, exit_code, setup, cases):
    require(type(exit_code) is int, "child exit must be exact integer")
    require(b"\r" not in stdout and stdout.endswith(b"\n"), "stdout not complete LF")
    lines = stdout.splitlines()
    require(len(lines) == 12 and all(line.startswith(b"{") for line in lines),
            "exact identity/ten-case/summary stream")
    records = [json.loads(line) for line in lines]
    require(all(type(record) is dict for record in records), "JSON record type")
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
            and setup["timeout_seconds"] == TIMEOUT, "replayed child command/watchdog")
    for flag in ("dont_write_bytecode=1", "no_user_site=1", "optimize=0", "isolated=0",
                 "ignore_environment=0", "no_site=0", "safe_path=True"):
        require(flag in identity["flags"], "replayed child flags: " + flag)
    observed = records[1:-1]
    require(tuple(record.get("original_composition_case") for record in observed)
            == tuple(case["id"] for scope, case in cases), "exact original case order")
    semantic_failures, oracle_errors, analyzer_errors = [], [], []
    analyzed = 0
    for actual, (scope, expected) in zip(observed, cases, strict=True):
        require(actual["original_pack"] == scope, "original pack attribution")
        for key in ("classification", "source_sha256", "oracle_sha256", "expected",
                    "unreachable_events", "required_argv"):
            require(actual[key] == expected[key], "original case drift: " + expected["id"] + "/" + key)
        oracle_ok = (actual["oracle_error"] is None and actual["oracle_actual"] == expected["expected"]
                     and not any(event in actual["oracle_actual"]["trace"]
                                 for event in expected["unreachable_events"]))
        require(actual["oracle_passed"] is oracle_ok, "oracle result inconsistency")
        if not oracle_ok:
            oracle_errors.append(expected["id"])
        if actual["analyzer_error"] is not None:
            analyzer_errors.append(expected["id"])
        has_receipt = actual["receipt_sha256"] is not None
        require(not has_receipt or valid_digest(actual["receipt_sha256"]), "public receipt digest")
        require(not has_receipt or (oracle_ok and actual["analyzer_error"] is None),
                "receipt despite skipped/failed analyzer")
        if has_receipt:
            analyzed += 1
        require(type(actual["expanded_rows"]) is list and type(actual["blockers"]) is list,
                "public result containers")
        argv = [row["argv"] for row in actual["expanded_rows"] if row["capability_kind"] == "subprocess"]
        require(actual["argv"] == argv, "argv differs from public rows")
        public_ok = (bool(actual["blockers"]) if expected["classification"] == "refuse" else
                     not actual["blockers"] and argv == expected["required_argv"])
        semantic_ok = bool(oracle_ok and actual["analyzer_error"] is None and has_receipt and public_ok)
        require(actual["semantic_passed"] is semantic_ok, "semantic inconsistency")
        if not semantic_ok:
            semantic_failures.append(expected["id"])
    summary = records[-1]
    require(summary.get("original_composition_summary") is True, "final summary")
    require(summary["schema"] == SCHEMA and summary["slot"] == setup["slot"]
            and summary["generator_sha256"] == setup["generator_sha256"]
            and summary["pack_sha256"] == PACK_HASHES
            and summary["probe_sha256"] == PROBE_SHA and summary["plan_sha256"] == PLAN_SHA,
            "summary pins")
    for key in ("planned_cases", "case_count", "projections"):
        require(type(summary[key]) is int and summary[key] == 10, "summary exact scope: " + key)
    require(type(summary["analyzed_cases"]) is int and summary["analyzed_cases"] == analyzed,
            "analyzed count disagrees with public receipts")
    require(summary["classifications"] == {"clean": 5, "refuse": 5}
            and all(type(value) is int for value in summary["classifications"].values())
            and summary["caps"] == CAPS
            and all(type(value) is int for value in summary["caps"].values()), "classifications/caps")
    require(summary["semantic_failures"] == semantic_failures
            and summary["oracle_errors"] == oracle_errors and summary["analyzer_errors"] == analyzer_errors,
            "summary disagrees with cases")
    completed = analyzed == 10 and not oracle_errors and not analyzer_errors
    require(summary["completed"] is completed, "completion mismatch")
    require(exit_code == int(bool(semantic_failures or oracle_errors or analyzer_errors)), "child exit mismatch")
    return {"identity": identity, "summary": summary, "cases_observed": len(observed),
            "completed": completed, "semantic_ok": not semantic_failures}


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
    parser.add_argument("--floor-receipt")
    parser.add_argument("--floor-sha256")
    args = parser.parse_args()
    require(valid_digest(args.overlay_sha256), "explicit candidate digest")
    source_sha = args.overlay_sha256
    require(re.fullmatch("[a-z0-9][a-z0-9-]{0,60}", args.label), "label")
    checked(ROOT, True)
    checked(CHECKS, True)
    prefix = "original-composition-ten-" + args.label + "-" + args.slot
    outputs = {key: CHECKS / (prefix + suffix) for key, suffix in (
        ("setup", "-setup.json"), ("receipt", "-receipt.json"),
        ("stdout", ".stdout.txt"), ("stderr", ".stderr.txt"), ("log", ".txt"))}
    require(not any(p.exists() for p in outputs.values()), "retained output collision")
    streams = {key: p.open("x+b") for key, p in outputs.items()}
    setup = {"schema": SCHEMA, "slot": args.slot, "label": args.label, "base": BASE,
             "overlay_source": args.overlay_source, "generator_sha256": args.overlay_sha256,
             "watch_source": str(WATCH), "watch_sha256": WATCH_SHA,
             "probe_sha256": PROBE_SHA, "pack_sha256": PACK_HASHES, "plan_sha256": PLAN_SHA}
    receipt = {**setup, "completed": False, "integrity_ok": False, "success": False, "payload_started": False}
    process, snapshot, temp, manifest_sha, exit_code = None, None, None, None, None
    before, input_paths, input_hashes, files = {}, {}, {}, {}
    phase = "preflight"
    write_json(streams["setup"], setup)
    try:
        overlay = checked(args.overlay_source)
        require(overlay.parent == ROOT and overlay.name.startswith("engineer-generator-")
                and overlay.suffix == ".py", "candidate must be an explicit retained T source")
        control = checked(Path(__file__).absolute())
        require(control.is_relative_to(CHECKS) and valid_digest(args.control_sha256), "root control pin")
        input_paths = {"overlay": overlay, "watch": WATCH, "probe": PROBE,
                       **{scope: CHECKS / metadata["file"] for scope, metadata in PACKS.items()},
                       "plan": PLAN, "control": control}
        input_hashes = {"overlay": source_sha, "watch": WATCH_SHA, "probe": PROBE_SHA,
                        **PACK_HASHES, "plan": PLAN_SHA, "control": args.control_sha256}
        inputs = {key: checked(p).read_bytes() for key, p in input_paths.items()}
        require({key: sha(raw) for key, raw in inputs.items()} == input_hashes, "original input pin mismatch")
        cases = load_cases({scope: inputs[scope] for scope in PACKS})
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
            for key in ("base", "overlay_source", "generator_sha256", "watch_source", "watch_sha256",
                        "probe_sha256", "pack_sha256", "plan_sha256", "control_sha256"):
                require(floor[key] == setup[key], "floor context mismatch: " + key)
            require(floor["integrity_ok"] is True and floor["completed"] is True
                    and floor["payload_started"] is True and type(floor["exit"]) is int
                    and floor["exit"] in (0, 1) and "error" not in floor and "cleanup_error" not in floor,
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
                        "watch_source", "watch_sha256", "probe_sha256", "pack_sha256", "plan_sha256",
                        "control_sha256", "snapshot", "temp", "before", "manifest_sha256", "environment",
                        "command", "timeout_seconds", "tracked_file_count", "payload_file_count",
                        "input_hashes_before", "input_paths"):
                require(floor_setup[key] == floor[key], "floor raw setup mismatch: " + key)
            require(type(floor["tracked_file_count"]) is int and floor["tracked_file_count"] == 1761
                    and type(floor["payload_file_count"]) is int and floor["payload_file_count"] == 7
                    and len(floor["before"]) == 1768, "floor exact manifest scope")
            require(pinned_outputs["log"] == pinned_outputs["stdout"] + b"\nCONTROL STDERR\n"
                    + pinned_outputs["stderr"], "floor combined log replay")
            proof = validate_result(pinned_outputs["stdout"], floor["exit"], floor_setup, cases)
            require(proof["completed"] is True and proof["summary"] == floor["summary"]
                    and proof["identity"] == floor["identity"]
                    and proof["semantic_ok"] is floor["semantic_ok"]
                    and floor["success"] is bool(floor["exit"] == 0), "floor output completion")
            floor_snapshot = checked(Path(floor["snapshot"]), True)
            require(floor_snapshot.name == "snapshot" and floor_snapshot.parent.parent == SNAPSHOTS
                    and Path(floor["temp"]) == floor_snapshot.parent / "temp", "floor snapshot/temp layout")
            floor_tracked = git(floor_snapshot, Path(floor["temp"]), "ls-tree", "-r", "-z",
                                "--name-only", BASE).decode().split("\0")[:-1]
            floor_payload_names = {"probe.py", *(metadata["file"] for metadata in PACKS.values()),
                                   "control.py", "plan.md", "retained-source.py", "run.json"}
            require(len(floor_tracked) == len(set(floor_tracked)) == 1761
                    and set(floor["before"]) == set(floor_tracked) |
                        {PAYLOAD + "/" + name for name in floor_payload_names}, "floor exact manifest keys")
            require(git(floor_snapshot, Path(floor["temp"]), "rev-parse", "HEAD").decode().strip() == BASE,
                    "floor HEAD now changed")
            floor_dirty = git(floor_snapshot, Path(floor["temp"]), "status", "--porcelain=v1",
                              "-z", "--untracked-files=all").decode()
            require(set(floor_dirty.split("\0")[:-1]) ==
                    {" M " + GENERATOR, *("?? " + PAYLOAD + "/" + name
                      for name in (*floor_payload_names, "manifest.json"))}, "floor status now changed")
            require(file_hashes(floor_snapshot, floor["before"]) == floor["before"], "floor snapshot now changed")
            floor_manifest_raw = checked(floor_snapshot / PAYLOAD / "manifest.json").read_bytes()
            require(sha(floor_manifest_raw) == floor["manifest_sha256"]
                    and json.loads(floor_manifest_raw) == floor["before"], "floor manifest now changed")
            setup["floor_receipt"] = {"path": str(floor_path), "sha256": args.floor_sha256,
                                      "exit": floor["exit"], "snapshot_files_rehashed": len(floor["before"]),
                                      "semantic_RED_permitted": True}
        else:
            require(args.floor_receipt is None and args.floor_sha256 is None, "311 takes no floor receipt")
        phase = "clone"
        checked(SNAPSHOTS, True)
        checked(REPOSITORY, True)
        parent = SNAPSHOTS / ("original-composition-ten-" + uuid.uuid4().hex)
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
        require(git(snapshot, temp, "status", "--porcelain=v1", "-z", "--untracked-files=all")
                == b" M tools/generate_test_inventory.py\0", "extra overlay paths")
        tracked = git(snapshot, temp, "ls-tree", "-r", "-z", "--name-only", BASE).decode().split("\0")[:-1]
        require(len(tracked) == len(set(tracked)) == 1761, "tracked count")
        before = file_hashes(snapshot, tracked)
        require(before[GENERATOR] == source_sha, "copied overlay pin")
        run = {"schema": SCHEMA, "slot": args.slot, "generator_sha256": source_sha,
               "probe_sha256": PROBE_SHA, "pack_sha256": PACK_HASHES, "plan_sha256": PLAN_SHA,
               "control_sha256": args.control_sha256, "overlay_source": str(overlay),
               "watch_source": str(WATCH), "watch_sha256": WATCH_SHA}
        files = {"probe.py": inputs["probe"],
                 **{metadata["file"]: inputs[scope] for scope, metadata in PACKS.items()},
                 "control.py": inputs["control"], "plan.md": inputs["plan"],
                 "retained-source.py": inputs["overlay"], "run.json": canonical(run),
                 **floor_files}
        payload = snapshot / PAYLOAD
        payload.mkdir()
        checked(payload, True)
        for name, raw in files.items():
            create(payload / name, raw)
            before[PAYLOAD + "/" + name] = sha(raw)
        require(len(before) == 1768 + (5 if args.slot == "314" else 0), "complete manifest count")
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
                expected_dirty = {" M " + GENERATOR, *("?? " + PAYLOAD + "/" + name for name in (*files, "manifest.json"))}
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
                              and receipt.get("semantic_ok") is True
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

