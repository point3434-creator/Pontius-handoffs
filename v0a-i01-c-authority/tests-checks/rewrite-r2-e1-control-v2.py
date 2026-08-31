"""Finite four-case builtin-environment control; authoring is not run permission.

Run this controller with exact floor Python 3.11.15 and -I -S -B -P.
Arguments: LABEL SLOT RETAINED_SOURCE_ABSOLUTE SOURCE_SHA --control-sha256 SHA
For SLOT=314 also supply --floor-receipt ABSOLUTE --floor-sha256 SHA.
An absolute T candidate plus its exact SHA is required. The core W watch must match the explicit candidate SHA; protected16 are watched.
Child uses -B -P, scrubbed environment, snapshot/src PYTHONPATH, hash seed 0.
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
import uuid

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
CHECKS = ROOT / "tests-checks"
REPOSITORY = Path(r"D:\Pontius")
SNAPSHOTS = Path(r"D:\pontius-snapshots")
GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
BASE = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
BASE_GENERATOR_SHA = "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
WATCH = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-core-v1\tools\generate_test_inventory.py")
PROTECTED = {'.github/workflows/ci.yml': 'ce3bcf3a2feed6f232d5af131a04e21ba82ed32794838e48297fc780c110a386', 'src/pontius/v0a/__init__.py': '86d349c4b79f150a4439df8d63c8d20854572895aaf7960f27647e7b1f198a8a', 'src/pontius/v0a/clock.py': '42bd18d36a6353dbbcc44df1113eafa40ee5581b3e2479761990ab5c21c074bb', 'src/pontius/v0a/model.py': '3936d0216cdfc1b79500aac22908edd5e724b8da341801fcbafefa7c27a58e18', 'src/pontius/v0a/replay.py': 'ccd18b6540af9799a9feca9cd9884b4871fec7434012e911e37abdc0b1373a53', 'src/pontius/v0a/runtime.py': '307115a9a50be0a80b0cbba997f26f385abcbe1abdc32bd749495eb4692084ee', 'src/pontius/v0a/trace.py': '4358b82b77defeb8bae3a40ab46f1cdfef61d49189b836577040e3e1e22081a1', 'tests/test-inventory.json': '6b866ea24975ee448511f72662f4d04e7f56eba026c0b797bbfa3f4dc7f4008d', 'tests/test-profiles.toml': '5862820a7c316dd9e4bbfe0997ba09f861f8cce257897da6a9a8da659e6912f1', 'tests/test_inventory_and_profiles.py': 'c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf', 'tests/test_v0a_boundaries.py': 'f81387bbf46dfeaf7de8dbcc4f47c2ff04ac06f23f9fd3d1bdd84bf2f210f807', 'tests/test_v0a_contract_faults.py': 'fa7b35f334ebdc232e3d1789db0923ca32ca28ffa0a0a4db741de3a7470cbcf8', 'tests/test_v0a_hand_replay.py': '0a46d155256c4d5727bf53cbc7d8b8ec811d37d777b5c3d7996d8b31ecd822c0', 'tests/test_v0a_replay.py': '1905b75cef434830cf60a7ddc0faf3b5f58cf3bee4947a9be408a017fa0d9c88', 'tests/test_v0a_trace.py': '6de564516a2b866b8b13789bcdff213062911a794bb726a9c9361e785a465d02', 'tools/check_stabilization_boundaries.py': '3dbf89f1a81661bc12fd7e7ea3625b1cb472d9d2f239496ff51ee348e859b4d6'}
PROBE = CHECKS / "rewrite-r2-e1-probe-v1.py"
PROBE_SHA = "7ac823d560034a140275d2447bf68bbe1f98adc8c250e61d46aedada018656a3"
PACK = CHECKS / "rewrite-r2-e1-cases-v1.json"
PACK_SHA = "59b8457a2323634d883fb2c9b0ff82a1e60cd980c5f2a4b50e627c8ca32cdb9b"
SCHEDULE = CHECKS / "rewrite-r2-e1-spec-v1.md"
SCHEDULE_SHA = "4fcb92ed30a86be1664d9b1981e5e8dc8c47d5d76eaab7b08dc09db74abc9f11"
SLOTS = {
    "311": (Path(r"D:\Pontius-tools\py311\Scripts\python.exe"), (3, 11, 15)),
    "314": (Path(r"D:\Pontius\.venv\Scripts\python.exe"), (3, 14, 6)),
}
CAPS = {
    "MAXIMUM_ANALYSIS_HELPER_DEPTH": 64, "MAXIMUM_ANALYSIS_CHILD_DEPTH": 4,
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS": 4096,
    "MAXIMUM_ANALYSIS_CARDINALITY": 2147483647, "MAXIMUM_ANALYSIS_WORK_UNITS": 262144,
}
SCHEMA = "pontius-r2-e1-v1"
PAYLOAD = ".rewrite-r2-e1"
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


def validate_result(stdout, stderr, exit_code, setup, pack):
    require(type(exit_code) is int and exit_code in (0, 1), "non-case child exit")
    require(b"\r" not in stdout, "stdout not LF")
    require(stderr == b"", "unexpected child stderr")
    lines = stdout.splitlines()
    require(len(lines) == len(pack["cases"]) + 2 and all(lines), "stdout record line count")
    records = []
    for line in lines:
        try:
            value = json.loads(line)
        except (ValueError, UnicodeError) as error:
            raise RuntimeError("stdout line is not JSON") from error
        require(type(value) is dict, "stdout record is not an object")
        records.append(value)
    require(records and set(records[0]) == {"identity_before_imports"}, "missing first pre-import identity")
    identities = [r["identity_before_imports"] for r in records if "identity_before_imports" in r]
    require(len(identities) == 1, "identity count")
    identity = identities[0]
    exe, version = SLOTS[setup["slot"]]
    require(identity["implementation"] == "cpython" and identity["version_info"] == list(version)
            and Path(identity["executable"]).resolve() == exe.resolve(), "actual child runtime")
    require(identity["cwd"] == setup["snapshot"] and identity["environment"] == setup["environment"]
            and identity["manifest_sha256"] == setup["manifest_sha256"]
            and identity["verified_files"] == len(setup["before"])
            and identity["generator_sha256"] == setup["generator_sha256"] and identity["probe_sha256"] == PROBE_SHA,
            "identity context")
    cases = [r for r in records if "rewrite_r2_e1_case" in r]
    require(tuple(r["rewrite_r2_e1_case"] for r in cases)
            == tuple(c["id"] for c in pack["cases"]), "missing/extra/reordered cases")
    require(len(records) == len(pack["cases"]) + 2, "extra result records")
    semantic_failures, oracle_errors, analyzer_errors = [], [], []
    analyzed = 0
    for actual, expected in zip(cases, pack["cases"], strict=True):
        for key in ("schedule_id", "classification", "source_sha256", "oracle_sha256", "expected",
                    "unreachable_events", "required_argv"):
            require(actual[key] == expected[key], "case drift: " + expected["id"] + "/" + key)
        oracle_ok = (actual["oracle_error"] is None and actual["oracle_actual"] == expected["expected"]
                     and not any(e in actual["oracle_actual"]["trace"] for e in expected["unreachable_events"]))
        require(actual["oracle_passed"] is oracle_ok, "oracle result inconsistency")
        if not oracle_ok:
            oracle_errors.append(expected["id"])
        if actual["analyzer_error"] is not None:
            analyzer_errors.append(expected["id"])
        public = actual["public_result"]
        if public is not None:
            require(type(public) is dict and type(public["receipt"]) is dict
                    and actual["analyzer_error"] is None and oracle_ok, "unexpected public result")
            require(actual["public_result_sha256"] == sha(canonical(public)),
                    "full public result digest")
            require(actual["receipt_sha256"] == sha(canonical(public["receipt"])),
                    "public receipt digest")
            require(actual["expanded_rows"] == public["receipt"]["expanded_rows"]
                    and actual["blockers"] == public["unresolved_dynamic_blockers"],
                    "raw public result/row/blocker disagreement")
            analyzed += 1
        else:
            require(actual["public_result_sha256"] is None and actual["receipt_sha256"] is None
                    and actual["expanded_rows"] == [] and actual["blockers"] == [],
                    "missing public result has projected evidence")
            require(not oracle_ok or actual["analyzer_error"] is not None,
                    "analyzer completed without a public result")
        argv = [r["argv"] for r in actual["expanded_rows"] if r["capability_kind"] == "subprocess"]
        require(actual["argv"] == argv, "argv differs from public rows")
        kind = expected["classification"]
        public_ok = (bool(actual["blockers"]) if kind == "refuse" else
                     bool(actual["blockers"]) or argv == expected["required_argv"] if kind == "permitted-refusal"
                     else not actual["blockers"] and argv == expected["required_argv"])
        semantic_ok = bool(oracle_ok and actual["analyzer_error"] is None
                           and actual["receipt_sha256"] is not None and public_ok)
        require(actual["semantic_passed"] is semantic_ok, "semantic inconsistency")
        require(actual["passed"] is semantic_ok, "case result inconsistency")
        if not semantic_ok:
            semantic_failures.append(expected["id"])
    summaries = [r for r in records if r.get("rewrite_r2_e1_summary") is True]
    require(len(summaries) == 1 and records[-1] == summaries[0], "missing/extra/final summary")
    summary = summaries[0]
    require(summary["schema"] == SCHEMA and summary["slot"] == setup["slot"]
            and summary["generator_sha256"] == setup["generator_sha256"] and summary["pack_sha256"] == PACK_SHA
            and summary["probe_sha256"] == PROBE_SHA and summary["schedule_sha256"] == SCHEDULE_SHA,
            "summary pins")
    require(all(type(summary[field]) is int for field in
                ("planned_cases", "case_count", "projections", "analyzed_cases")),
            "summary count types")
    require(summary["planned_cases"] == summary["case_count"] == summary["projections"] == 4
            and summary["analyzed_cases"] == analyzed, "summary scope")
    require(type(summary["classifications"]) is dict
            and all(type(count) is int for count in summary["classifications"].values())
            and summary["classifications"] == {"clean": 2, "refuse": 2}
            and type(summary["caps"]) is dict
            and all(type(limit) is int for limit in summary["caps"].values())
            and summary["caps"] == CAPS, "summary classifications/caps")
    require(summary["semantic_failures"] == semantic_failures
            and summary["oracle_errors"] == oracle_errors and summary["analyzer_errors"] == analyzer_errors,
            "summary disagrees with cases")
    completed = summary["analyzed_cases"] == 4 and not oracle_errors and not analyzer_errors
    require(summary["completed"] is bool(completed), "completion mismatch")
    require(exit_code == int(bool(semantic_failures or oracle_errors or analyzer_errors)),
            "child exit mismatch")
    return {"identity": identity, "summary": summary, "cases_observed": len(cases),
            "completed": bool(completed), "semantic_ok": not semantic_failures}


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
    prefix = "rewrite-r2-e1-" + args.label + "-" + args.slot
    outputs = {key: CHECKS / (prefix + suffix) for key, suffix in (
        ("setup", "-setup.json"), ("receipt", "-receipt.json"),
        ("stdout", ".stdout.txt"), ("stderr", ".stderr.txt"), ("log", ".txt"))}
    require(not any(p.exists() for p in outputs.values()), "retained output collision")
    streams = {key: p.open("x+b") for key, p in outputs.items()}
    setup = {"schema": SCHEMA, "slot": args.slot, "label": args.label, "base": BASE,
             "overlay_source": args.overlay_source, "generator_sha256": args.overlay_sha256,
             "watch_source": str(WATCH), "watch_sha256": source_sha,
             "probe_sha256": PROBE_SHA, "pack_sha256": PACK_SHA, "schedule_sha256": SCHEDULE_SHA}
    receipt = {**setup, "completed": False, "integrity_ok": False, "success": False, "payload_started": False}
    process, snapshot, temp, manifest_sha, exit_code = None, None, None, None, None
    before, input_paths, input_hashes, files = {}, {}, {}, {}
    phase = "preflight"
    write_json(streams["setup"], setup)
    try:
        overlay = checked(args.overlay_source)
        require(overlay.parent == ROOT and overlay.name.startswith("rewrite-r2-")
                and overlay.suffix == ".py", "candidate must be an explicit retained T source")
        control = checked(Path(__file__).absolute())
        require(control.is_relative_to(CHECKS) and valid_digest(args.control_sha256), "root control pin")
        input_paths = {"overlay": overlay, "watch": WATCH, "probe": PROBE, "pack": PACK,
                       "schedule": SCHEDULE, "control": control}
        input_hashes = {"overlay": source_sha, "watch": source_sha, "probe": PROBE_SHA,
                        "pack": PACK_SHA, "schedule": SCHEDULE_SHA, "control": args.control_sha256}
        require(len(PROTECTED) == 16, "protected path count")
        input_paths.update({"protected:" + name: WATCH.parent.parent / name for name in PROTECTED})
        input_hashes.update({"protected:" + name: value for name, value in PROTECTED.items()})
        inputs = {key: checked(p).read_bytes() for key, p in input_paths.items()}
        require({key: sha(raw) for key, raw in inputs.items()} == input_hashes, "original input pin mismatch")
        pack = json.loads(inputs["pack"])
        require(all(type(pack[field]) is int
                    for field in ("planned_cases", "planned_projections"))
                and pack["planned_cases"] == pack["planned_projections"] == len(pack["cases"]) == 4
                and pack["pack_name"] == "rewrite-r2-e1-v1", "frozen pack scope")
        require(type(pack["classifications"]) is dict
                and all(type(count) is int for count in pack["classifications"].values())
                and pack["classifications"] == {"clean": 2, "refuse": 2},
                "frozen classification counts")
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
                        "probe_sha256", "pack_sha256", "schedule_sha256", "control_sha256"):
                require(floor[key] == setup[key], "floor context mismatch: " + key)
            require(floor["integrity_ok"] is True and floor["completed"] is True
                    and floor["success"] is True and type(floor["exit"]) is int and floor["exit"] == 0
                    and type(floor["process_returncode"]) is int
                    and floor["process_returncode"] == floor["exit"]
                    and "error" not in floor and "cleanup_error" not in floor,
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
                        "watch_source", "watch_sha256", "probe_sha256", "pack_sha256",
                        "schedule_sha256", "control_sha256", "snapshot", "temp",
                        "manifest_sha256", "tracked_file_count", "payload_file_count", "before",
                        "environment", "command", "timeout_seconds", "input_hashes_before", "input_paths"):
                require(floor_setup[key] == floor[key], "floor setup/receipt mismatch: " + key)
            require(floor_setup["slot"] == "311", "floor setup is not actual floor")
            require(pinned_outputs["log"] == pinned_outputs["stdout"]
                    + b"\nCONTROL STDERR\n" + pinned_outputs["stderr"], "floor raw log framing")
            proof = validate_result(pinned_outputs["stdout"], pinned_outputs["stderr"],
                                    floor["exit"], floor_setup, pack)
            require(proof["completed"] and proof["semantic_ok"] and proof["summary"] == floor["summary"]
                    and proof["identity"] == floor["identity"], "floor output completion")
            require(floor["success"] is bool(proof["semantic_ok"] and floor["exit"] == 0),
                    "floor success/semantic result mismatch")
            floor_snapshot = checked(Path(floor["snapshot"]), True)
            require(floor_snapshot.is_relative_to(SNAPSHOTS), "floor snapshot outside root")
            require(file_hashes(floor_snapshot, floor["before"]) == floor["before"], "floor snapshot now changed")
            require(sha(checked(floor_snapshot / PAYLOAD / "manifest.json").read_bytes())
                    == floor["manifest_sha256"], "floor manifest now changed")
            setup["floor_receipt"] = {"path": str(floor_path), "sha256": args.floor_sha256,
                                      "exit": floor["exit"], "snapshot_files_rehashed": len(floor["before"]),
                                      "semantic_RED_permitted": False}
        else:
            require(args.floor_receipt is None and args.floor_sha256 is None, "311 takes no floor receipt")
        phase = "clone"
        checked(SNAPSHOTS, True)
        checked(REPOSITORY, True)
        parent = SNAPSHOTS / ("rewrite-r2-e1-" + uuid.uuid4().hex)
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
               "probe_sha256": PROBE_SHA, "pack_sha256": PACK_SHA, "schedule_sha256": SCHEDULE_SHA,
               "control_sha256": args.control_sha256, "overlay_source": str(overlay),
               "watch_source": str(WATCH), "watch_sha256": source_sha}
        files = {"probe.py": inputs["probe"], "cases.json": inputs["pack"], "control.py": inputs["control"],
                 "schedule.md": inputs["schedule"], "retained-source.py": inputs["overlay"], "run.json": canonical(run),
                 **floor_files}
        payload = snapshot / PAYLOAD
        payload.mkdir()
        checked(payload, True)
        for name, raw in files.items():
            create(payload / name, raw)
            before[PAYLOAD + "/" + name] = sha(raw)
        require(len(files) == 6 + (5 if args.slot == "314" else 0)
                and len(before) == len(tracked) + len(files), "complete manifest count")
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
        result = validate_result(outputs["stdout"].read_bytes(), outputs["stderr"].read_bytes(),
                                 exit_code, setup, pack)
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
                              and "error" not in receipt and "cleanup_error" not in receipt and exit_code == 0)
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
