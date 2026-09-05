"""Read-only raw-object and receipt audit for the five-file adoption candidate."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

assert sys.version_info[:3] == (3, 11, 15)
assert sys.dont_write_bytecode and sys.flags.safe_path
require_post_clean = "--require-post-clean" in sys.argv[1:]
ROOT = Path(__file__).resolve().parent
WORK = ROOT / "authoring"
PACKET = ROOT / "packets/r001"
BASE = "7a387e995e3b37232d2379332927247a4d49c64e"
COMMIT = "36c31477d87028aeec31339d28ccc089ffcaa31d"
DESIGN = "02e24f143b8df4b2f03e8a94c58ab57905a8b2b6"
DESIGN_PACKET = ROOT.parent / "v0a-hand-adapter-design-r001/packets/r003"
NAMES = ("brief.md", "design.md", "source-opening-draft.md")
DOCS = {f"docs/architecture/v0a-hand-adapter-r002/{name}" for name in NAMES}
ALLOWED = DOCS | {"STATUS.md", "docs/decisions/ADR-0493-open-the-one-hand-file-adapter-source-round.md"}
GIT = r"C:\Program Files\Git\cmd\git.exe"


def git(*args):
    return subprocess.check_output([GIT, "--no-replace-objects", "-c",
        f"safe.directory={WORK.as_posix()}", "-C", str(WORK), *args])


def object_bytes(kind, oid):
    raw = git("cat-file", kind, oid)
    assert hashlib.sha1(f"{kind} {len(raw)}\0".encode() + raw).hexdigest() == oid
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
paths = git("diff", "--no-renames", "--name-only", BASE, COMMIT).decode().splitlines()
assert len(paths) == 5 and set(paths) == ALLOWED
rows = []
for path in paths:
    oid = git("rev-parse", f"{COMMIT}:{path}").decode().strip()
    raw = object_bytes("blob", oid)
    assert raw == (PACKET / "files" / path).read_bytes() == (WORK / path).read_bytes()
    assert b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf")
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    assert all(line.rstrip() == line for line in raw.splitlines())
    if path != "STATUS.md":
        assert all(len(line.decode()) <= 100 for line in raw.splitlines())
    if path in DOCS:
        assert raw == git("cat-file", "blob", f"{DESIGN}:{path}")
        assert raw == (DESIGN_PACKET / "files" / path).read_bytes()
    rows.append(hashlib.sha256(raw).hexdigest() + "  " + path + "\n")
    for phase in ("focused", "post-clean"):
        for slot in ("311", "314"):
            for check in ("status", "tests"):
                snapshot = ROOT / f"snapshots/{phase}-{check}-{slot}"
                if require_post_clean:
                    assert snapshot.exists(), snapshot
                if phase == "focused" or snapshot.exists():
                    assert (snapshot / path).read_bytes() == raw, (snapshot, path)
    print(f"FILE {path}: {len(raw)} bytes, {raw.count(bytes([10]))} LF")
manifest = "".join(sorted(rows)).encode()
assert manifest == (PACKET / "manifest.sha256").read_bytes()
assert hashlib.sha256(manifest).hexdigest() == identity["manifest_sha256"]
proposal = (PACKET / "files/docs/architecture/v0a-hand-adapter-r002/source-opening-draft.md").read_text()
pins = []
for line in proposal.splitlines():
    if len(line) > 42 and line[40:42] == "  " and all(c in "0123456789abcdef" for c in line[:40]):
        pin, path = line.split("  ", 1)
        assert git("rev-parse", f"{BASE}:{path}").decode().strip() == pin
        pins.append(path)
assert len(pins) == 6
for seat, digest in (
    ("a", "ed499e3b4764aa1f8d7afe4a206f965f8f870cc67e409aae50c45c3e1f5e5765"),
    ("b", "0320d1f877a0567013bd0c9a992be68bcc5a300c505d8b114cb99d3694190e99"),
):
    assert hashlib.sha256((DESIGN_PACKET / f"reviews/review-{seat}.md").read_bytes()).hexdigest() == digest
assert (WORK / "STATUS.md").read_bytes() == (ROOT / "snapshots/generate-311/STATUS.md").read_bytes().replace(b"\r\n", b"\n")
receipt_counts = {"focused": 0, "post-clean": 0}
for phase in ("focused", "post-clean"):
    for slot in ("311", "314"):
        for check in ("status", "tests"):
            receipt = ROOT / f"run-records/{phase}-{check}-{slot}.json"
            if require_post_clean:
                assert receipt.exists(), receipt
            if phase == "focused" or receipt.exists():
                records = json.loads(receipt.read_bytes())
                assert len(records) == 2 and all(r["exit_code"] == 0 for r in records)
                assert records[1]["argv"] == (["-B", "-P", "-m", "pontius.status_generation", "--check"] if check == "status" else ["-B", "-P", "tests/test_status_generation.py"])
                if check == "tests":
                    assert "Ran 12 tests" in records[1]["stderr"] and "\nOK\n" in records[1]["stderr"].replace("\r\n", "\n")
                receipt_counts[phase] += 1
git("diff", "--check", BASE, COMMIT)
print("PASS: raw Git hashes/ref/parent/tree, exact five-path scope and packet/working bytes")
print("PASS: whole-row-sorted digest-first LF manifest and document hygiene")
print("PASS: three exact design copies, original review digests and six unchanged registration pins")
print("PASS: generated STATUS; matching snapshot bytes and successful receipts:", receipt_counts)
print("LIMIT: metadata verification only; no adapter implementation or runtime acceptance")
print("Candidate:", COMMIT)
print("Manifest:", identity["manifest_sha256"])
