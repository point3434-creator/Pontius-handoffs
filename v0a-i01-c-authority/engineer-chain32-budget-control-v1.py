"""Frozen floor-only chain32 diagnostic controller. Preparation is not execution."""
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
WORKSPACE = Path(r"D:\Pontius")
GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
EXE = Path(r"D:\Pontius-tools\py311\Scripts\python.exe")
VERSION = "3.11.15"
BASE_COMMIT = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
SOURCE = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1\tools\generate_test_inventory.py")
SOURCE_SHA = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
BASE_SOURCE_SHA = "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
TEST_SHA = "c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf"
PROBE = ROOT / "engineer-chain32-budget-probe-v1.py"
PROBE_SHA = "c37f214c65462565290e3f6eae1dce16d7e2c4adc7f343d81f5a82b087c3dbc9"


def req(value, message):
    if not value:
        raise RuntimeError(message)


def h(raw):
    return hashlib.sha256(raw).hexdigest()


def validate(path):
    req(path.is_absolute() and ".." not in path.parts, "unsafe path")
    for parent in (path, *path.parents):
        info = parent.lstat()
        req(not (getattr(info, "st_file_attributes", 0)
                 & stat.FILE_ATTRIBUTE_REPARSE_POINT), "reparse " + str(parent))
    return path


def create(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def create_json(path, value):
    create(path, (json.dumps(value, indent=2) + "\n").encode())


def environment_for(temp, snapshot=None):
    windows = validate(Path(os.environ["SYSTEMROOT"]))
    system = validate(windows / "System32")
    environment = {
        "SYSTEMROOT": str(windows), "WINDIR": str(windows),
        "COMSPEC": str(system / "cmd.exe"), "PATH": str(system),
        "TEMP": str(temp), "TMP": str(temp), "PONTIUS_GIT": str(validate(GIT)),
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "NUL",
        "GIT_CONFIG_SYSTEM": "NUL", "GIT_ATTR_NOSYSTEM": "1",
        "PYTHONNOUSERSITE": "1",
    }
    if snapshot is not None:
        environment["PYTHONPATH"] = str(snapshot / "src")
    return environment


def git(repository, temp, *arguments):
    command = [
        str(validate(GIT)), "-c", "core.autocrlf=false",
        "-c", "core.hooksPath=NUL", "-c", "init.templateDir=",
        "-c", "core.attributesFile=NUL", "-c", "core.fsmonitor=false",
        "-C", str(repository), *arguments,
    ]
    return subprocess.run(command, cwd=repository, env=environment_for(temp),
                          capture_output=True, check=True).stdout


req(sys.implementation.name == "cpython"
    and sys.version_info[:3] == (3, 11, 15), "control version")
req(Path(sys.executable).resolve() == EXE.resolve(), "control executable")
req(sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
    and sys.dont_write_bytecode and not sys.flags.optimize, "control flags")
label, control_sha = sys.argv[1:]
req(re.fullmatch("[a-z0-9][a-z0-9-]{0,70}", label) is not None, "label")
req(re.fullmatch("[0-9a-f]{64}", control_sha) is not None, "control digest")
control_path = validate(Path(__file__).absolute())
control_raw = control_path.read_bytes()
req(h(control_raw) == control_sha, "control changed")
source_raw = validate(SOURCE).read_bytes()
req(h(source_raw) == SOURCE_SHA, "production source changed")
probe_raw = validate(PROBE).read_bytes()
req(h(probe_raw) == PROBE_SHA, "probe changed")
validate(EXE)
folder = WORKSPACE / ("engineer-chain32-" + uuid.uuid4().hex)
req(folder.absolute().is_relative_to(WORKSPACE.absolute()), "snapshot outside workspace")
folder.mkdir()
validate(folder)
temp = folder / "temp"
temp.mkdir()
validate(temp)
snapshot = folder / "snapshot"
git(folder, temp, "clone", "--shared", "--no-checkout", str(WORKSPACE), str(snapshot))
validate(snapshot)
git(snapshot, temp, "checkout", "--detach", BASE_COMMIT)
req(not git(snapshot, temp, "status", "--porcelain", "--untracked-files=all"),
    "dirty initial snapshot")
tracked = git(snapshot, temp, "ls-files", "-z").decode("utf-8").split("\0")[:-1]
base = {name: h(validate(snapshot / name).read_bytes()) for name in tracked}
req(base["tools/generate_test_inventory.py"] == BASE_SOURCE_SHA, "base generator changed")
req(base["tests/test_inventory_and_profiles.py"] == TEST_SHA, "base tests changed")
(snapshot / "tools/generate_test_inventory.py").write_bytes(source_raw)
before = {name: h(validate(snapshot / name).read_bytes()) for name in tracked}
req({name for name in base if base[name] != before[name]}
    == {"tools/generate_test_inventory.py"}, "unexpected tracked overlay")
payload = snapshot / ".chain32-diagnostic"
payload.mkdir()
validate(payload)
wrapper = r'''import sys,json,os,hashlib,importlib.util,runpy
from pathlib import Path
exe,version,manifest_sha,payload_name=sys.argv[1:]
assert sys.implementation.name=='cpython' and '.'.join(map(str,sys.version_info[:3]))==version
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert sys.flags.safe_path and sys.dont_write_bytecode and not sys.flags.optimize
assert not sys.flags.isolated and not sys.flags.ignore_environment and not sys.flags.no_site
assert 'PYTHONHASHSEED' not in os.environ
snapshot=Path.cwd()
assert os.environ.get('PYTHONPATH')==str(snapshot/'src')
assert Path(os.environ['PONTIUS_GIT'])==Path(r'C:\Program Files\Git\cmd\git.exe')
assert Path(importlib.util.find_spec('pontius').origin).resolve()==(snapshot/'src/pontius/__init__.py').resolve()
payload=snapshot/payload_name
assert payload.is_relative_to(snapshot)
manifest_raw=(payload/'manifest.json').read_bytes()
assert hashlib.sha256(manifest_raw).hexdigest()==manifest_sha
manifest=json.loads(manifest_raw)
for name,digest in manifest.items():
    assert hashlib.sha256((snapshot/name).read_bytes()).hexdigest()==digest
print(json.dumps({'identity_before_payload_imports':{'executable':sys.executable,'version':sys.version,'version_info':list(sys.version_info[:3]),'implementation':sys.implementation.name,'cwd':str(snapshot),'flags':str(sys.flags),'hash_seed':'unspecified, matching original design control','hash_probe':hash('pontius-chain32-diagnostic'),'environment':dict(os.environ),'manifest_sha256':manifest_sha}}),flush=True)
runpy.run_path(str(payload/'probe.py'),run_name='__main__')
'''
files = {"probe.py": probe_raw, "control.py": control_raw, "wrapper.py": wrapper.encode()}
for name, raw in files.items():
    create(payload / name, raw)
    before[".chain32-diagnostic/" + name] = h(raw)
manifest_raw = (json.dumps(before, indent=2) + "\n").encode()
create(payload / "manifest.json", manifest_raw)
manifest_sha = h(manifest_raw)
environment = environment_for(temp, snapshot)
command = [str(EXE), "-B", "-P", str(payload / "wrapper.py"),
           str(EXE), VERSION, manifest_sha, ".chain32-diagnostic"]
checks = ROOT / "engineer-checks"
checks.mkdir(exist_ok=True)
validate(checks)
prefix = label + "-311"
setup = {
    "scope": "one existing review_evidence(chained_source(32)) only",
    "base_commit": BASE_COMMIT, "tracked_file_count": len(tracked),
    "label": label, "slot": "311", "snapshot": str(snapshot), "temp": str(temp),
    "command": command, "environment": environment,
    "control_sha256": control_sha, "probe_sha256": PROBE_SHA,
    "production_source_sha256": SOURCE_SHA, "test_sha256": TEST_SHA,
    "snapshot_manifest_sha256": manifest_sha, "base": base, "before": before,
}
create_json(checks / (prefix + "-setup.json"), setup)
try:
    result = subprocess.run(command, cwd=snapshot, env=environment,
                            capture_output=True, timeout=60)
    code, stdout, stderr = result.returncode, result.stdout, result.stderr
except subprocess.TimeoutExpired as error:
    code, stdout, stderr = 124, error.stdout or b"", error.stderr or b""
    stderr += b"\nCONTROL: chain32 diagnostic timed out after60 seconds\n"
log = checks / (prefix + ".txt")
create(log, stdout + stderr)
after = {name: h((snapshot / name).read_bytes()) for name in before}
manifest_after = h((payload / "manifest.json").read_bytes())
dirty = git(snapshot, temp, "status", "--porcelain", "--untracked-files=all").decode("utf-8")
expected_dirty = {" M tools/generate_test_inventory.py"} | {
    "?? .chain32-diagnostic/" + name for name in (*files, "manifest.json")}
originals_after = {
    "source": h(SOURCE.read_bytes()), "probe": h(PROBE.read_bytes()),
    "control": h(control_path.read_bytes()),
}
identity = failure = completion = None
for line in stdout.splitlines():
    try:
        record = json.loads(line)
    except (ValueError, UnicodeError):
        continue
    if not isinstance(record, dict):
        continue
    if "identity_before_payload_imports" in record:
        identity = record["identity_before_payload_imports"]
    if "chain32_budget_failure" in record:
        req(failure is None, "duplicate failure report")
        failure = record["chain32_budget_failure"]
    if "chain32_diagnostic_complete" in record:
        completion = record["chain32_diagnostic_complete"]
receipt = {
    **setup, "dirty_after": dirty, "exit": code, "stdout_sha256": h(stdout),
    "stderr_sha256": h(stderr), "log": str(log), "log_sha256": h(stdout + stderr),
    "after": after, "manifest_after_sha256": manifest_after,
    "originals_after": originals_after, "identity_before_payload_imports": identity,
    "diagnostic_failure": failure, "diagnostic_completion": completion,
}
receipt_path = checks / (prefix + "-receipt.json")
create_json(receipt_path, receipt)
req(before == after and manifest_sha == manifest_after, "snapshot changed")
req(set(dirty.splitlines()) == expected_dirty, "unexpected snapshot changes")
req(originals_after == {"source": SOURCE_SHA, "probe": PROBE_SHA,
                         "control": control_sha}, "input changed during payload")
req(identity is not None, "missing pre-import identity")
print(json.dumps({
    "exit": code, "receipt": str(receipt_path),
    "receipt_sha256": h(receipt_path.read_bytes()), "log_sha256": h(stdout + stderr),
    "budget_failure_recorded": failure is not None, "completion": completion,
}, indent=2))
raise SystemExit(code != 0)
