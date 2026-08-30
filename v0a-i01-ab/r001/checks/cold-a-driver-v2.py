"""Cold-A orchestration only; payloads are children in the detached snapshot."""
import hashlib
import json
import os
from pathlib import Path
import platform
import stat
import subprocess
import sys
import time

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-ab\r001")
SNAP = Path(r"D:\pontius-snapshots\v0a-i01-ab-r001-cold-a-20260830")
GIT = r"C:\Program Files\Git\cmd\git.exe"
PAIR = ("256bcf5b1e721c70216f4d8937166cbb9c25a7ce",
        "7a4cbf46c9eb34693d605ae43a0b9048b709d65f9c3fed40610c5c1b5ae3b384")
BASE = "c74b80628a89938ca585ef3240b5c267a7174d0f"
expected, phase = sys.argv[1:3]
executable = {"3.11.15": r"D:\Pontius-tools\py311\Scripts\python.exe",
              "3.14.6": r"D:\Pontius\.venv\Scripts\python.exe"}[expected]
assert platform.python_implementation() == "CPython"
assert platform.python_version() == expected
assert os.path.normcase(sys.executable) == os.path.normcase(executable)
assert Path.cwd() == SNAP
assert sys.flags.safe_path and sys.flags.dont_write_bytecode
assert os.environ["PYTHONPATH"] == str(SNAP / "src")
assert os.environ["PONTIUS_GIT"] == GIT
assert stat.S_ISREG(os.stat(GIT).st_mode)
assert not os.stat(GIT).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT

def git(*args):
    return subprocess.run([GIT, "-C", str(SNAP), *args], env=os.environ.copy(),
                          cwd=SNAP, capture_output=True, check=True).stdout

def digest(data):
    return hashlib.sha256(data).hexdigest()

def manifest():
    assert git("rev-parse", "HEAD").decode().strip() == PAIR[0]
    assert git("rev-parse", "HEAD^").decode().strip() == BASE
    fields = git("diff-tree", "-r", "-z", "--no-renames", "--no-commit-id",
                 "--name-status", BASE, PAIR[0]).split(b"\0")
    rows = []
    details = []
    for i in range(0, len(fields) - 1, 2):
        status, path = fields[i:i+2]
        blob = None if status == b"D" else git("cat-file", "blob",
                                             PAIR[0] + ":" + path.decode())
        value = "0" * 64 if blob is None else digest(blob)
        rows.append(value.encode() + b"  " + path + b"\n")
        checkout = SNAP / path.decode()
        details.append({"status": status.decode(), "path": path.decode(),
                        "blob_sha256": value, "blob_bytes": len(blob or b""),
                        "checkout_sha256": digest(checkout.read_bytes()),
                        "blob_crlf": (blob or b"").count(b"\r\n")})
    data = b"".join(sorted(rows))
    assert digest(data) == PAIR[1]
    assert data == (ROOT / "manifest.sha256").read_bytes()
    assert git("status", "--porcelain") == b""
    return {"commit": PAIR[0], "manifest_sha256": digest(data),
            "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
            "base": BASE, "paths": details, "status": "clean"}

receipt = {"expected_version": expected, "actual_version": sys.version,
           "implementation": platform.python_implementation(),
           "executable": sys.executable, "cwd": str(Path.cwd()),
           "sys_flags": {"safe_path": sys.flags.safe_path,
                         "dont_write_bytecode": sys.flags.dont_write_bytecode},
           "env": dict(sorted(os.environ.items())), "manifest": manifest(),
           "phase": phase, "commands": []}

def run(command, label):
    started = time.monotonic()
    result = subprocess.run(command, cwd=SNAP, env=os.environ.copy(),
                            capture_output=True, text=True, encoding="utf-8",
                            errors="backslashreplace")
    entry = {"label": label, "argv": command, "exit": result.returncode,
             "duration_seconds": time.monotonic() - started,
             "stdout": result.stdout, "stderr": result.stderr}
    receipt["commands"].append(entry)
    print(label, "exit", result.returncode, flush=True)
    return result.returncode

identity_code = ("import sys,platform,os,json; "
                 "assert platform.python_version()==" + repr(expected) + "; "
                 "import pontius.v0a.clock as c,pontius.v0a.runtime as r,"
                 "pontius.v0a.replay as p; "
                 "print(json.dumps({'version':sys.version,'executable':sys.executable,"
                 "'cwd':os.getcwd(),'files':[c.__file__,r.__file__,p.__file__]}))")
exit_code = run([executable, "-B", "-P", "-c", identity_code], "payload_identity")
if exit_code == 0 and phase == "focused":
    for name in ("test_v0a_hand_replay.py", "test_v0a_trace.py",
                 "test_v0a_replay.py", "test_v0a_contract_faults.py"):
        exit_code |= run([executable, "-B", "-P", str(SNAP / "tests" / name)], name)
elif exit_code == 0 and phase.startswith("probes"):
    exit_code |= run([executable, "-B", "-P",
                      str(ROOT / "checks" / ("cold-a-" + phase + ".py")),
                      expected], phase)
receipt["post_manifest"] = manifest()
out = ROOT / "checks" / ("cold-a-v2-" + phase + "-" + expected.replace(".", "") + ".json")
with out.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(receipt, stream, indent=2)
    stream.write("\n")
print("receipt", str(out), digest(out.read_bytes()), flush=True)
sys.exit(exit_code)