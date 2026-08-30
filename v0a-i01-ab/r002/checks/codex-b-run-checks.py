import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

SLOT = sys.argv[1]
EXPECTED = {"311": ((3, 11, 15), r"D:\Pontius-tools\py311\Scripts\python.exe"), "314": ((3, 14, 6), r"D:\Pontius\.venv\Scripts\python.exe")}[SLOT]
assert sys.version_info[:3] == EXPECTED[0], sys.version
assert Path(sys.executable).resolve() == Path(EXPECTED[1]).resolve()
SNAP = Path(r"D:\pontius-snapshots\v0a-i01-ab-r002-cold-b-20260830")
CHECKS = Path(r"D:\Pontius-handoffs\v0a-i01-ab\r002\checks")
assert Path.cwd().resolve() == SNAP.resolve()
assert os.environ["PYTHONPATH"] == str(SNAP / "src")
assert os.environ["PONTIUS_GIT"] == r"C:\Program Files\Git\cmd\git.exe"
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
bootstrap = CHECKS / "codex-b-payload.py"
mode = sys.argv[2]
payloads = ([str(SNAP / "tests" / name) for name in ("test_v0a_hand_replay.py", "test_v0a_contract_faults.py", "test_v0a_replay.py", "test_v0a_trace.py")] if mode == "focused" else [str(CHECKS / mode)])
receipts = []
for payload in payloads:
    command = [sys.executable, "-B", "-P", str(bootstrap), SLOT, payload]
    result = subprocess.run(command, capture_output=True, text=True, env=os.environ.copy(), cwd=SNAP)
    receipt = {"command": command, "cwd": str(SNAP), "exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    receipts.append(receipt)
    print(json.dumps(receipt), flush=True)
receipt_path = CHECKS / ("codex-b-" + SLOT + "-" + mode.replace(".py", "") + ".json")
with receipt_path.open("x", encoding="utf-8", newline="\n") as output:
    json.dump({"python": sys.version, "executable": sys.executable, "environment": dict(os.environ), "results": receipts}, output, indent=2)
    output.write("\n")
assert all(item["exit"] == 0 for item in receipts), "Check failure; retained receipts"
