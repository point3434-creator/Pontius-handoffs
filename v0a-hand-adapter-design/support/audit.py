"""Read-only document-candidate identity audit; not runtime acceptance."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

assert sys.version_info[:3] == (3, 11, 15)
assert sys.dont_write_bytecode and sys.flags.safe_path
ROOT = Path(__file__).resolve().parent
WORK = ROOT / "authoring"
PACKET = ROOT / "packets/r001"
BASE = "7a387e995e3b37232d2379332927247a4d49c64e"
COMMIT = "21474e3d5b105c1709205df1eb5543417abb5a0a"
GIT = r"C:\Program Files\Git\cmd\git.exe"
ALLOWED = {
    "docs/architecture/v0a-hand-adapter-r001/brief.md",
    "docs/architecture/v0a-hand-adapter-r001/design.md",
    "docs/architecture/v0a-hand-adapter-r001/source-opening-draft.md",
}


def git(*args):
    return subprocess.check_output(
        [GIT, "-c", f"safe.directory={WORK.as_posix()}", "-C", str(WORK), *args]
    )


identity = json.loads((PACKET / "candidate.json").read_bytes())
assert identity["commit"] == COMMIT and identity["base"] == BASE
assert git("rev-parse", identity["ref"]).decode().strip() == COMMIT
assert git("rev-parse", COMMIT + "^").decode().strip() == BASE
assert git("rev-parse", COMMIT + "^{tree}").decode().strip() == identity["tree"]
assert git("rev-parse", "HEAD").decode().strip() == BASE
assert not git("diff", "--cached", "--name-only")
paths = git("diff", "--no-renames", "--name-only", BASE, COMMIT).decode().splitlines()
assert len(paths) == 3 and set(paths) == ALLOWED
rows = []
for path in paths:
    raw = git("cat-file", "blob", f"{COMMIT}:{path}")
    assert raw == (PACKET / "files" / path).read_bytes() == (WORK / path).read_bytes()
    assert b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf")
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    assert all(line.rstrip() == line and len(line.decode()) <= 100 for line in raw.splitlines())
    rows.append(hashlib.sha256(raw).hexdigest() + "  " + path + "\n")
manifest = "".join(sorted(rows)).encode("ascii")
assert manifest == (PACKET / "manifest.sha256").read_bytes()
assert hashlib.sha256(manifest).hexdigest() == identity["manifest_sha256"]
proposal = git("cat-file", "blob", f"{COMMIT}:docs/architecture/v0a-hand-adapter-r001/source-opening-draft.md").decode()
pins = []
for line in proposal.splitlines():
    if len(line) > 42 and line[40:42] == "  " and all(c in "0123456789abcdef" for c in line[:40]):
        pin, path = line.split("  ", 1)
        assert git("rev-parse", f"{BASE}:{path}").decode().strip() == pin, path
        pins.append(path)
assert len(pins) == 6
git("diff", "--check", BASE, COMMIT)
print("PASS: exact ref, parent, tree and three-path documentation-only scope")
print("PASS: raw packet/working/blob bytes and whole-row-sorted LF manifest")
print("PASS: six proposed registration exceptions pin the actual base blobs")
print("PASS: all other base blobs unchanged; authoring HEAD/index unchanged")
print("PASS: LF-only, no BOM/trailing whitespace, final LF, lines <=100 columns")
print("Candidate:", COMMIT)
print("Manifest:", identity["manifest_sha256"])
print("LIMIT: no implementation, project import, payload/test run or runtime acceptance")
