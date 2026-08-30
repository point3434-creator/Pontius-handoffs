import sys
import platform
sys.stdout.reconfigure(encoding="utf-8", newline="\n")
sys.stderr.reconfigure(encoding="utf-8", newline="\n")
assert sys.executable == sys.argv[1], (sys.executable, sys.argv[1])
assert platform.python_version() == sys.argv[2]
assert platform.python_implementation() == "CPython"
print("BOOTSTRAP", repr(sys.executable), platform.python_implementation(), platform.python_version(), flush=True)
import os
import json
import hashlib
import subprocess
from pathlib import Path
snapshot=Path.cwd()
assert str(snapshot) == r"D:\pontius-snapshots\v0a-r005-cold-b-e6ac13a682804562a53621e8fab883e1\harness"
assert os.environ["PYTHONPATH"] == str(snapshot / "src")
git=os.environ["PONTIUS_GIT"]
assert git == r"C:\Program Files\Git\cmd\git.exe"
packet=Path(r"D:\Pontius-handoffs\v0a-i01-impl\r005")
candidate=json.loads((packet/"candidate.json").read_text())
commit="a8582e6d6b53b55415dab79c4a54e252d00b74ad"
base="b357d333fc2393b7fc7dcf31f30c86616208c817"
expected="e9b0baf12e258d66a92169d38137cbf2f42317158b6515ac377f745bbc52093a"
assert candidate["commit"] == commit and candidate["base"] == base and candidate["manifest_sha256"] == expected
def run(*args):
    return subprocess.run([git,"-C",r"D:\Pontius",*args],check=True,capture_output=True).stdout
assert run("rev-parse",candidate["ref"]).decode().strip() == commit
assert run("rev-parse",commit+"^{tree}").decode().strip() == candidate["tree"]
fields=run("diff","--name-status","--no-renames","-z",base,commit).decode().split("\0")
rows=[]
for i in range(0,len(fields)-1,2):
    status,path=fields[i:i+2]
    blob=run("cat-file","blob",commit+":"+path)
    digest=hashlib.sha256(blob).hexdigest()
    assert (snapshot/path).read_bytes() == blob, path
    rows.append((digest+"  "+path+"\n").encode())
manifest=b"".join(sorted(rows))
assert manifest == (packet/"manifest.sha256").read_bytes()
assert hashlib.sha256(manifest).hexdigest() == expected
print("FROZEN_PAIR_VERIFIED",commit,expected,"files",len(rows))
for path in ["docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md","docs/briefs/v0a-increment-1-brief.md","src/pontius/action_clock.py","src/pontius/no_limit_betting.py","docs/architecture/dependency-baseline.toml"]:
    blob=run("cat-file","blob",commit+":"+path)
    assert (snapshot/path).read_bytes() == blob
    print("DEPENDENCY_BLOB",path,hashlib.sha256(blob).hexdigest())
print("R004",run("rev-parse","refs/heads/review/v0a-i01-impl/r004").decode().strip())
print("IDENTITY_PASS")
