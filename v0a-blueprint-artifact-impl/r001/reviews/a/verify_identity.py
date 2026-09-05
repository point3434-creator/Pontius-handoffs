from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess


REPOSITORY = Path(r"D:\Pontius\tmp\v0a-blueprint-artifact-impl-r001\authoring")
PACKET = Path(r"D:\Pontius\tmp\v0a-blueprint-artifact-impl-r001\packets\r001")
COMMIT = "6fb7f840d31d946e6b5dcb45faf82939dafd46ec"
BASE = "c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98"
EXPECTED_TREE = "6f8e17c12da42ad901c90bc764fc39958cca5854"
EXPECTED_MANIFEST = "26b8fb178aecaf3dccf038ee2e108dc4ce913f7f07baff10cff5efbe11011aee"


def git(*arguments: str) -> bytes:
    return subprocess.run(
        [r"C:\Program Files\Git\cmd\git.exe", "-C", str(REPOSITORY), *arguments],
        check=True,
        capture_output=True,
    ).stdout


assert git("rev-parse", "refs/heads/review/v0a-blueprint-artifact-impl/r001").strip().decode() == COMMIT
assert git("rev-parse", f"{COMMIT}^{{tree}}").strip().decode() == EXPECTED_TREE
assert git("rev-parse", f"{COMMIT}^").strip().decode() == BASE
raw = git("diff-tree", "-r", "-z", "--no-commit-id", "--name-status", COMMIT + "^", COMMIT)
fields = raw.decode("utf-8", "surrogateescape").split("\0")
rows: list[str] = []
paths: list[str] = []
index = 0
while index + 1 < len(fields) and fields[index]:
    status = fields[index][0]
    path = fields[index + 1]
    digest = "0" * 64 if status == "D" else hashlib.sha256(
        git("cat-file", "blob", f"{COMMIT}:{path}")
    ).hexdigest()
    rows.append(f"{digest}  {path}\n")
    paths.append(path)
    index += 2

assert len(rows) == 12
manifest_bytes = "".join(sorted(rows)).encode("utf-8")
assert hashlib.sha256(manifest_bytes).hexdigest() == EXPECTED_MANIFEST
assert (PACKET / "manifest.sha256").read_bytes() == manifest_bytes
for path in paths:
    assert (PACKET / "files" / Path(path)).read_bytes() == git("cat-file", "blob", f"{COMMIT}:{path}")
print(f"identity PASS commit={COMMIT} tree={EXPECTED_TREE} manifest={EXPECTED_MANIFEST} rows={len(rows)}")
for row in sorted(rows):
    print(row, end="")
