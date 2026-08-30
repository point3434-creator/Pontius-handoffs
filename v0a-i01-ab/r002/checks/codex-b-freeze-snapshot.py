import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

assert sys.version_info[:3] == (3, 11, 15), sys.version
assert Path(sys.executable).resolve() == Path(r"D:\Pontius-tools\py311\Scripts\python.exe").resolve()
GIT = r"C:\Program Files\Git\cmd\git.exe"
ROOT = Path(r"D:\Pontius")
PACKET = Path(r"D:\Pontius-handoffs\v0a-i01-ab\r002")
SNAP = Path(r"D:\pontius-snapshots\v0a-i01-ab-r002-cold-b-20260830")
COMMIT = "2f4287f68a83fac4225a05a91daffdb3f2977a43"
BASE = "256bcf5b1e721c70216f4d8937166cbb9c25a7ce"
REF = "refs/heads/review/v0a-i01-ab/r002"
TREE = "7d1383a1a7b2cf05442e4ef4fe8a9189708b2263"
MANIFEST = "55f7ebf8827c79a6d6c70b1bf26508d87527b8c7113d2458fb4c3dfb5fed0957"
def git(*args, cwd=ROOT):
    return subprocess.run([GIT, "-C", str(cwd), *args], capture_output=True, check=True).stdout
assert git("rev-parse", REF).decode().strip() == COMMIT
assert git("rev-parse", COMMIT + "^").decode().strip() == BASE
assert git("rev-parse", COMMIT + "^{tree}").decode().strip() == TREE
changed = git("diff-tree", "--no-renames", "-r", "--no-commit-id", "--name-status", "-z", BASE, COMMIT).decode().split("\0")
rows = []
blobs = {}
for index in range(0, len(changed)-1, 2):
    status, name = changed[index:index+2]
    raw = git("cat-file", "blob", COMMIT + ":" + name)
    digest = hashlib.sha256(raw).hexdigest()
    rows.append(digest + "  " + name + "\n")
    blobs[name] = {"status": status, "sha256": digest, "bytes": len(raw), "cr": raw.count(b"\r"), "bom": raw.startswith(b"\xef\xbb\xbf")}
manifest_bytes = "".join(sorted(rows)).encode()
assert set(blobs) == {"src/pontius/v0a/runtime.py", "src/pontius/v0a/replay.py", "tests/test_v0a_hand_replay.py", "tests/test_v0a_contract_faults.py"}
assert hashlib.sha256(manifest_bytes).hexdigest() == MANIFEST
assert (PACKET / "manifest.sha256").read_bytes() == manifest_bytes
candidate = json.loads((PACKET / "candidate.json").read_text())
assert all(candidate[key] == value for key, value in {"commit": COMMIT, "base": BASE, "ref": REF, "tree": TREE, "manifest_sha256": MANIFEST}.items())
assert not SNAP.exists(), "Fresh snapshot name already exists"
assert SNAP.parent.resolve() == Path(r"D:\pontius-snapshots").resolve()
subprocess.run([GIT, "-c", "core.autocrlf=false", "clone", "--shared", "--no-checkout", str(ROOT), str(SNAP)], check=True, capture_output=True)
git("-c", "core.autocrlf=false", "checkout", "--detach", COMMIT, cwd=SNAP)
assert git("rev-parse", "HEAD", cwd=SNAP).decode().strip() == COMMIT
assert git("status", "--porcelain", cwd=SNAP) == b""
for name, details in blobs.items():
    assert hashlib.sha256((SNAP / name).read_bytes()).hexdigest() == details["sha256"]
receipt = {"reviewer": "Codex /root/ab_r002_cold_b", "commit": COMMIT, "base": BASE, "tree": TREE, "manifest_sha256": MANIFEST, "snapshot": str(SNAP), "python": sys.version, "executable": sys.executable, "git": GIT, "blobs": blobs, "status": "verified"}
with (PACKET / "checks" / "codex-b-freeze-snapshot.json").open("x", encoding="utf-8", newline="\n") as output:
    json.dump(receipt, output, indent=2)
    output.write("\n")
print(json.dumps(receipt, indent=2))
