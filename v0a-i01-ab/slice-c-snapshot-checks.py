"""Non-evidentiary focused Slice C correctness launcher; never an experiment owner."""
from pathlib import Path
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import uuid

GIT = Path("C:/Program Files/Git/cmd/git.exe")
TREE = Path("D:/Pontius-worktrees/codex-v0a-i01-c-integration")
PACKET = Path("D:/Pontius-handoffs/v0a-i01-ab")
BASE = "6cdf7b00dac653a9a295bbb86cdc3b5782317491"
PATHS = (
    ".github/workflows/ci.yml", "tools/check_stabilization_boundaries.py",
    "tools/generate_test_inventory.py", "tests/test_v0a_boundaries.py",
    "tests/test_inventory_and_profiles.py", "tests/test-inventory.json",
    "tests/test-profiles.toml",
)
SLOTS = (
    (Path("D:/Pontius-tools/py311/Scripts/python.exe"), (3, 11, 15)),
    (Path("D:/Pontius/.venv/Scripts/python.exe"), (3, 14, 6)),
)

def main():
    phase = sys.argv[1]
    assert phase in {"red", "green"}
    token = uuid.uuid4().hex[:12]
    floor = Path("D:/Pontius-worktrees")
    scratch = floor / ("slice-c-" + phase + "-" + token)
    scratch.mkdir()
    temp = scratch / "temp"
    temp.mkdir()
    env = {key: os.environ[key] for key in ("SYSTEMROOT", "WINDIR", "COMSPEC") if key in os.environ}
    env.update({
        "PATH": str(Path(env["SYSTEMROOT"]) / "System32"),
        "TEMP": str(temp), "TMP": str(temp), "PONTIUS_GIT": str(GIT),
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
    })
    assert GIT.is_absolute() and GIT.is_file()
    assert not (GIT.lstat().st_file_attributes & 0x400)
    records = []
    for executable, expected in (SLOTS[:1] if phase == "red" else SLOTS):
        snapshot = scratch / ("snapshot-" + ".".join(map(str, expected)))
        subprocess.run(
            [str(GIT), "clone", "--quiet", "--no-hardlinks", "--single-branch",
             "--branch", "review/v0a-i01-ab/r005", "D:/Pontius", str(snapshot)],
            env=env, cwd=scratch, check=True,
        )
        subprocess.run([str(GIT), "-C", str(snapshot), "checkout", "--quiet", "--detach", BASE],
                       env=env, cwd=scratch, check=True)
        hashes = {}
        for relative in PATHS:
            raw = (TREE / relative).read_bytes()
            (snapshot / relative).write_bytes(raw)
            hashes[relative] = hashlib.sha256(raw).hexdigest()
        child_env = dict(env, PYTHONPATH=str(snapshot / "src"))
        commands = [("tests/test_v0a_boundaries.py",)]
        if phase == "green":
            commands += [("tests/test_stabilization_boundaries.py",),
                         ("tools/check_stabilization_boundaries.py",)]
        for args in commands:
            stem = Path(args[0]).stem
            log = PACKET / f"slice-c-{phase}-{token}-{expected[0]}{expected[1]}-{stem}.log"
            wrapper = (
                "import sys, os, json, platform, runpy; "
                f"assert sys.version_info[:3] == {expected!r}, sys.version; "
                "assert platform.python_implementation() == 'CPython'; "
                "assert sys.flags.dont_write_bytecode and sys.flags.safe_path; "
                f"assert os.getcwd() == {str(snapshot)!r}; "
                f"assert os.environ['PYTHONPATH'] == {str(snapshot / 'src')!r}; "
                "print(json.dumps({'executable':sys.executable, 'version':sys.version, "
                "'implementation':platform.python_implementation(), 'cwd':os.getcwd(), "
                "'pythonpath':os.environ['PYTHONPATH'], 'git':os.environ['PONTIUS_GIT'], "
                "'temp':os.environ['TEMP'], 'sys_path':sys.path}), flush=True); "
                f"sys.argv={list(args)!r}; runpy.run_path({args[0]!r}, run_name='__main__')"
            )
            command = [str(executable), "-B", "-P", "-c", wrapper]
            print(f"Running {phase} {expected} {args[0]} in {snapshot}", flush=True)
            with log.open("wb") as output:
                result = subprocess.run(command, cwd=snapshot, env=child_env,
                                        stdout=output, stderr=subprocess.STDOUT, timeout=1800)
            record = {"phase":phase, "version":expected, "snapshot":str(snapshot),
                      "command":command, "environment":child_env, "exit":result.returncode,
                      "log":str(log), "overlay_sha256":hashes}
            records.append(record)
            print(f"Exit {result.returncode}; log {log}", flush=True)
            receipt = PACKET / f"slice-c-{phase}-{token}-receipt.json"
            receipt.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8", newline="\n")
            if result.returncode and phase == "green":
                return result.returncode
    print(f"Receipt {receipt}", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
