"""Read-only design-candidate audit; no project code or runtime acceptance."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

assert sys.version_info[:3] == (3, 11, 15)
assert sys.dont_write_bytecode and sys.flags.safe_path
ROOT = Path(__file__).resolve().parent
WORK = ROOT / "authoring"
PACKET = ROOT / "packets/r003"
STAGE = ROOT / "staging-r003"
BASE = "7a387e995e3b37232d2379332927247a4d49c64e"
COMMIT = "02e24f143b8df4b2f03e8a94c58ab57905a8b2b6"
PRIOR = "21474e3d5b105c1709205df1eb5543417abb5a0a"
GIT = r"C:\Program Files\Git\cmd\git.exe"
NAMES = ("brief.md", "design.md", "source-opening-draft.md")
ALLOWED = {f"docs/architecture/v0a-hand-adapter-r002/{name}" for name in NAMES}


def git(*args):
    return subprocess.check_output(
        [GIT, "--no-replace-objects", "-c", f"safe.directory={WORK.as_posix()}",
         "-C", str(WORK), *args]
    )


def object_bytes(kind, oid):
    raw = git("cat-file", kind, oid)
    header = f"{kind} {len(raw)}\0".encode("ascii")
    assert hashlib.sha1(header + raw).hexdigest() == oid
    return raw


identity = json.loads((PACKET / "candidate.json").read_bytes())
assert identity["commit"] == COMMIT and identity["base"] == BASE
assert git("rev-parse", identity["ref"]).decode().strip() == COMMIT
object_bytes("commit", COMMIT)
object_bytes("tree", identity["tree"])
assert git("rev-parse", COMMIT + "^").decode().strip() == BASE
assert git("rev-parse", COMMIT + "^{tree}").decode().strip() == identity["tree"]
assert git("rev-parse", "HEAD").decode().strip() == BASE
assert not git("diff", "--cached", "--name-only")
assert not git("diff", "--name-only")
paths = git("diff", "--no-renames", "--name-only", BASE, COMMIT).decode().splitlines()
assert len(paths) == 3 and set(paths) == ALLOWED
rows = []
for path in paths:
    oid = git("rev-parse", f"{COMMIT}:{path}").decode().strip()
    raw = object_bytes("blob", oid)
    assert raw == (PACKET / "files" / path).read_bytes() == (STAGE / path).read_bytes()
    assert b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf")
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    assert all(line.rstrip() == line and len(line.decode()) <= 100 for line in raw.splitlines())
    rows.append(hashlib.sha256(raw).hexdigest() + "  " + path + "\n")
    terminal_lfs = len(raw) - len(raw.rstrip(b"\n"))
    print(f"FILE: {path}: {len(raw)} bytes, {raw.count(bytes([10]))} LF, "
          f"{terminal_lfs} terminal LF bytes")
manifest = "".join(sorted(rows)).encode("ascii")
assert manifest == (PACKET / "manifest.sha256").read_bytes()
assert hashlib.sha256(manifest).hexdigest() == identity["manifest_sha256"]
proposal = git("cat-file", "blob", f"{COMMIT}:docs/architecture/v0a-hand-adapter-r002/source-opening-draft.md").decode()
pins = []
for line in proposal.splitlines():
    if len(line) > 42 and line[40:42] == "  " and all(c in "0123456789abcdef" for c in line[:40]):
        pin, path = line.split("  ", 1)
        assert git("rev-parse", f"{BASE}:{path}").decode().strip() == pin, path
        pins.append(path)
assert len(pins) == 6
prior_identity = json.loads((ROOT / "packets/r001/candidate.json").read_bytes())
assert git("rev-parse", prior_identity["ref"]).decode().strip() == PRIOR
prior_rows = []
for name in NAMES:
    old_path = f"docs/architecture/v0a-hand-adapter-r001/{name}"
    old = git("cat-file", "blob", f"{PRIOR}:{old_path}")
    assert old == (ROOT / "packets/r001/files" / old_path).read_bytes()
    assert old == (WORK / old_path).read_bytes()
    prior_rows.append(hashlib.sha256(old).hexdigest() + "  " + old_path + "\n")
    if name != "design.md":
        new = git("cat-file", "blob", f"{COMMIT}:docs/architecture/v0a-hand-adapter-r002/{name}")
        assert old.replace(b"r001", b"r002").rstrip(b"\n") == new.rstrip(b"\n")
prior_manifest = "".join(sorted(prior_rows)).encode("ascii")
assert prior_manifest == (ROOT / "packets/r001/manifest.sha256").read_bytes()
assert hashlib.sha256(prior_manifest).hexdigest() == prior_identity["manifest_sha256"]
r002 = json.loads((ROOT / "packets/r002/candidate.json").read_bytes())
assert git("rev-parse", r002["ref"]).decode().strip() == r002["commit"]
r002_rows = []
for path in sorted(ALLOWED):
    old = git("cat-file", "blob", f'{r002["commit"]}:{path}')
    assert old == (ROOT / "packets/r002/files" / path).read_bytes()
    assert old == (WORK / path).read_bytes()
    new = git("cat-file", "blob", f"{COMMIT}:{path}")
    assert old.endswith(b"\n\n") and new == old[:-1]
    r002_rows.append(hashlib.sha256(old).hexdigest() + "  " + path + "\n")
r002_manifest = "".join(sorted(r002_rows)).encode("ascii")
assert r002_manifest == (ROOT / "packets/r002/manifest.sha256").read_bytes()
assert hashlib.sha256(r002_manifest).hexdigest() == r002["manifest_sha256"]
git("diff", "--check", BASE, COMMIT)
git("diff", "--check", r002["commit"], COMMIT)
print("PASS: raw Git object hashes, ref, parent, tree and exact three-path docs-only scope")
print("PASS: raw packet/working/blob bytes and whole-row-sorted LF manifest")
print("PASS: six registration pins; all other base blobs and authoring HEAD/index unchanged")
print("PASS: r001 ref/manifest/raw files retained byte-exact")
print("PASS: brief/opening preserve original content; r001-to-r002 version labels only")
print("PASS: LF-only, no BOM/trailing whitespace, final LF, lines <=100 columns")
print("PASS: r003 differs from r002 by exactly one removed EOF LF in each file")
print("PASS: r002 ref/manifest/raw packet and original working files unchanged")
print("Candidate:", COMMIT)
print("Manifest:", identity["manifest_sha256"])
print("LIMIT: no implementation, project import, payload/test run or runtime acceptance")
