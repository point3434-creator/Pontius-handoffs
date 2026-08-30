"""Focused correctness runner: fresh D-local snapshot and asserted floor-first identity."""
import hashlib, json, os, subprocess, sys, uuid
from pathlib import Path

G = r"C:\Program Files\Git\cmd\git.exe"
ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-ab")
WORK = Path(r"D:\Pontius-worktrees\codex-v0a-i01-publication-v2")
BASE = "6cdf7b00dac653a9a295bbb86cdc3b5782317491"
PATHS = ("src/pontius/v0a/runtime.py", "src/pontius/v0a/replay.py",
         "src/pontius/v0a/trace.py", "tests/test_v0a_replay.py", "tests/test_v0a_trace.py")
label, slot, scope = sys.argv[1:4]
if label.startswith("red"):
    BASE = "6cdf7b00dac653a9a295bbb86cdc3b5782317491"
    PATHS = tuple(name for name in PATHS if name.startswith("tests/"))
exe, version = ((r"D:\Pontius-tools\py311\Scripts\python.exe", "3.11.15")
                if slot == "311" else (r"D:\Pontius\.venv\Scripts\python.exe", "3.14.6"))
def git(where, *args):
    return subprocess.run([G, "-C", str(where), *args], capture_output=True, check=True).stdout
snapshot = Path(r"D:\pontius-snapshots") / ("ab-" + label + "-" + uuid.uuid4().hex) / "harness"
snapshot.parent.mkdir()
subprocess.run([G, "clone", "--shared", "--no-checkout", r"D:\Pontius", str(snapshot)],
               capture_output=True, check=True)
git(snapshot, "checkout", "--detach", BASE)
hashes = {}
for name in PATHS:
    data = (WORK / name).read_bytes()
    (snapshot / name).write_bytes(data)
    hashes[name] = hashlib.sha256(data).hexdigest()
environment = {key: os.environ[key] for key in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP")
               if key in os.environ}
environment.update(PYTHONPATH=str(snapshot / "src"), PONTIUS_GIT=G)
wrapper = """import sys,runpy,json
from pathlib import Path
exe,version,target,*tests=sys.argv[1:]
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert sys.implementation.name=='cpython'
assert '.'.join(map(str,sys.version_info[:3]))==version
assert sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps(dict(identity_before_payload_import=dict(executable=sys.executable,version=sys.version))),flush=True)
sys.argv=[target,*tests]
runpy.run_path(target,run_name='__main__')
"""
suites = (("test_v0a_replay.py", ["IncrementalPublicationTests"]),
          ("test_v0a_trace.py", ["StableTraceWriterTests"])) if scope=="regressions" else tuple(
    (name, []) for name in ("test_v0a_hand_replay.py", "test_v0a_trace.py",
                            "test_v0a_replay.py", "test_v0a_contract_faults.py"))
checks = ROOT / "publication-v2-checks"
checks.mkdir(parents=True, exist_ok=True)
receipt = dict(label=label, slot=slot, base=BASE, snapshot=str(snapshot), overlay_sha256=hashes,
               environment=environment, results=[])
for name, tests in suites:
    target = "tests/" + name
    command = [exe, "-B", "-P", "-c", wrapper, exe, version, target, *tests]
    result = subprocess.run(command, cwd=snapshot, env=environment, capture_output=True)
    data = (result.stdout + result.stderr).replace(b"\r\n", b"\n")
    output = checks / (label + "-" + slot + "-" + Path(name).stem + ".txt")
    with output.open("xb") as f: f.write(data)
    receipt["results"].append(dict(command=command, exit=result.returncode, log=str(output),
                                   sha256=hashlib.sha256(data).hexdigest()))
    print(name, "exit", result.returncode, data.decode(errors="replace")[-900:], flush=True)
for name, expected in hashes.items():
    assert hashlib.sha256((snapshot / name).read_bytes()).hexdigest() == expected
receipt["overlay_unchanged_after_execution"] = True
output = checks / (label + "-" + slot + "-receipt.json")
with output.open("xb") as f: f.write((json.dumps(receipt, indent=2) + "\n").encode())
print("receipt", str(output), flush=True)
