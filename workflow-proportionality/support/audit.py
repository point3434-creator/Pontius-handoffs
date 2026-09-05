"""Read-only raw Git and packet identity audit; no policy-equivalence claim."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "authoring"
PACKET = ROOT / "packets/r001"
BASE = "53773cb9e7489d8cfa32b4e0ceadea37c5980023"
GIT = r"C:\Program Files\Git\cmd\git.exe"
ALLOWED = {
    "CLAUDE.md", "docs/workflow.md", "STATUS.md",
    "docs/decisions/ADR-0492-adopt-proportionate-engineering-review.md",
}


def git(*args):
    return subprocess.check_output(
        [GIT, "-c", f"safe.directory={WORK.as_posix()}", "-C", str(WORK), *args]
    )


identity = json.loads((PACKET / "candidate.json").read_bytes())
commit = identity["commit"]
assert identity["base"] == BASE
assert git("rev-parse", identity["ref"]).decode().strip() == commit
assert git("rev-parse", commit + "^").decode().strip() == BASE
assert git("rev-parse", commit + "^{tree}").decode().strip() == identity["tree"]
assert git("rev-parse", "HEAD").decode().strip() == BASE
assert not git("diff", "--cached", "--name-only")
paths = git("diff", "--no-renames", "--name-only", BASE, commit).decode().splitlines()
assert set(paths) == ALLOWED and len(paths) == 4
rows = []
for path in paths:
    raw = git("cat-file", "blob", f"{commit}:{path}")
    assert raw == (PACKET / "files" / path).read_bytes(), path
    assert raw == (WORK / path).read_bytes(), path
    assert b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf"), path
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n"), path
    assert all(line.rstrip() == line for line in raw.splitlines()), path
    rows.append(hashlib.sha256(raw).hexdigest() + "  " + path + "\n")
manifest = "".join(sorted(rows)).encode("ascii")
assert manifest == (PACKET / "manifest.sha256").read_bytes()
assert hashlib.sha256(manifest).hexdigest() == identity["manifest_sha256"]
git("diff", "--check", BASE, commit)
manual = git("diff", "--numstat", BASE, commit, "--", ".", ":(exclude)STATUS.md")
count = sum(int(x) for row in manual.decode().splitlines() for x in row.split("\t")[:2])
assert count < 300, count
added = git("diff", "--no-ext-diff", "-U0", BASE, commit, "--", ".", ":(exclude)STATUS.md")
for line in added.decode().splitlines():
    if line.startswith("+") and not line.startswith("+++"):
        assert len(line[1:]) <= 100, line
print("PASS: exact ref, parent, tree, four-path scope, raw blobs and sorted manifest")
print("PASS: all other base blobs unchanged; authoring HEAD/index unchanged")
print("PASS: LF-only, no BOM/trailing whitespace, final LF, added prose <=100 columns")
print(f"PASS: {count} manually added/removed lines, below the 300-line budget")
print("Candidate:", commit)
print("Manifest:", identity["manifest_sha256"])
if "--acceptance" not in sys.argv:
    print("LIMIT: this identity audit does not establish policy acceptance")
else:
    for slot, version in (("311", "3.11.15"), ("314", "3.14.6")):
        for name, args in (
            ("status", ["-m", "pontius.status_generation", "--check"]),
            ("tests", ["tests/test_status_generation.py"]),
        ):
            receipt = ROOT / f"run-records/acceptance-r001-{name}-{slot}.json"
            records = json.loads(receipt.read_bytes())
            assert len(records) == 2 and all(row["exit_code"] == 0 for row in records)
            assert records[0]["stdout"].startswith(version + " ")
            record = records[1]
            assert record["argv"] == ["-B", "-P", *args]
            if name == "tests":
                assert "Ran 12 tests in" in record["stderr"]
                assert record["stderr"].rstrip().endswith("OK")
            snapshot = Path(record["snapshot"])
            for path in paths:
                assert (snapshot / path).read_bytes() == git(
                    "cat-file", "blob", f"{commit}:{path}"
                ), (receipt, path)
    print("PASS: four metadata commands, both exact slots, 12 tests per slot")
    print("PASS: all 16 post-run snapshot file comparisons match frozen blobs")
    print("LIMIT: metadata tests do not establish future policy-judgment quality")
