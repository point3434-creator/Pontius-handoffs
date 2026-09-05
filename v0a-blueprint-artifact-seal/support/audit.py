"""Read-only identity and incorporation audit for the frozen integration."""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
WORK = ROOT / "authoring"
PACKET = ROOT / "packets" / sys.argv[1]
BASE = "c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98"
PAYLOAD = "c7de23de276c50463d831f3983fede82a5400ce8"
CODEC = "5e56e4454f7b8ccb360d3e36245abc33318349bb"
GIT = r"C:\Program Files\Git\cmd\git.exe"


def git(*args):
    return subprocess.check_output(
        [GIT, "-c", f"safe.directory={WORK.as_posix()}", "-C", str(WORK), *args]
    )


def blob(commit, path):
    return git("cat-file", "blob", f"{commit}:{path}")


identity = json.loads((PACKET / "candidate.json").read_bytes())
commit = identity["commit"]
assert identity["base"] == BASE
assert git("rev-parse", identity["ref"]).decode().strip() == commit
assert git("rev-parse", commit + "^").decode().strip() == BASE
assert git("rev-parse", commit + "^{tree}").decode().strip() == identity["tree"]
assert git("rev-parse", PAYLOAD + "^").decode().strip() == CODEC
paths = git("diff", "--name-only", BASE, commit).decode().splitlines()
payload_paths = git("diff", "--name-only", BASE, PAYLOAD).decode().splitlines()
metadata = {"STATUS.md", "docs/decisions/ADR-0491-source-seal-the-portable-blueprint-artifact.md"}
assert len(payload_paths) == 12 and len(paths) == 14
assert set(paths) == set(payload_paths) | metadata
assert set(git("diff", "--name-only", PAYLOAD, commit).decode().splitlines()) == metadata
rows = []
for path in paths:
    raw = blob(commit, path)
    assert raw == (PACKET / "files" / path).read_bytes(), path
    if path in payload_paths:
        assert raw == blob(PAYLOAD, path), path
    rows.append(hashlib.sha256(raw).hexdigest() + "  " + path + "\n")
manifest = "".join(sorted(rows)).encode("ascii")
assert manifest == (PACKET / "manifest.sha256").read_bytes()
assert hashlib.sha256(manifest).hexdigest() == identity["manifest_sha256"]
adr = blob(commit, next(path for path in metadata if path != "STATUS.md"))
assert b"\r" not in adr and adr.isascii() and adr.endswith(b"\n")
assert not adr.endswith(b"\n\n")
assert all(line.rstrip() == line for line in adr.splitlines())
assert all(len(line) <= 100 for line in adr.splitlines() if not line.startswith(b"- "))
status = blob(commit, "STATUS.md")
assert b"\r" not in status and not status.startswith(b"\xef\xbb\xbf")
assert status.endswith(b"\n") and not status.endswith(b"\n\n")
assert all(line.rstrip() == line for line in status.splitlines())
if sys.argv[1] == "r002":
    prior = "5ba903fcb4ea4b5e4559baa6846fed99730d020b"
    assert git("diff", "--name-only", prior, commit).decode().splitlines() == ["STATUS.md"]
    assert blob(prior, "STATUS.md").replace(b"\r\n", b"\n") == status
git("diff", "--check", BASE, commit)
print("PASS: ref, parent, tree, raw blobs, 14-row manifest and ADR hygiene")
print("PASS: all 12 payload files exactly equal accepted combined candidate")
print("PASS: only ADR-0491 and generated STATUS differ from accepted payload")
print("Candidate:", commit)
print("Manifest:", identity["manifest_sha256"])
if "--acceptance" in sys.argv:
    for slot, version in (("311", "3.11.15"), ("314", "3.14.6")):
        for name, args in (
            ("status", ["-m", "pontius.status_generation", "--check"]),
            ("tests", ["tests/test_status_generation.py"]),
        ):
            receipt = ROOT / f"run-records/acceptance-r002-{name}-{slot}.json"
            records = json.loads(receipt.read_bytes())
            assert len(records) == 2 and all(row["exit_code"] == 0 for row in records)
            assert records[0]["stdout"].startswith(version + " ")
            record = records[1]
            assert record["argv"] == ["-B", "-P", *args]
            if name == "tests":
                assert "Ran 12 tests in" in record["stderr"]
                assert record["stderr"].endswith("OK\r\n")
            snapshot = pathlib.Path(record["snapshot"])
            for path in paths:
                assert (snapshot / path).read_bytes() == blob(commit, path), (receipt, path)
    print("PASS: four metadata commands, both exact slots, 12 tests each, post-run raw blobs")
