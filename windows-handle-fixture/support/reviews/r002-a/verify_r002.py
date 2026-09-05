"""Independent read-only verification of the frozen r002 correction."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(r"D:\Pontius\tmp\windows-handle-fixture-r001")
WORK = ROOT / "authoring"
GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
R001 = "76309774b551a874b8f9c677bc59e51299cee0e4"
R002 = "c7de23de276c50463d831f3983fede82a5400ce8"
BASE = "5e56e4454f7b8ccb360d3e36245abc33318349bb"
SOURCE = "tests/test_inventory_and_profiles.py"
INVENTORY = "tests/test-inventory.json"
PROFILES = "tests/test-profiles.toml"
OLD_CENSUS = "37b7508932c784b6898999b2c024eeb8e004aa492b10cf1a948a1028f3cc9ed2"
NEW_CENSUS = "c62e275fa42bcb8cc9bef4a382990793adc03ecc9d9db1b6fcd35aeb9b23372e"


def git(*args: str) -> bytes:
    return subprocess.run(
        [
            str(GIT),
            "-c",
            f"safe.directory={WORK.as_posix()}",
            "-C",
            str(WORK),
            *args,
        ],
        check=True,
        capture_output=True,
    ).stdout


def blob(commit: str, path: str) -> bytes:
    return git("cat-file", "blob", f"{commit}:{path}")


def changed_paths(older: str, newer: str) -> list[str]:
    raw = git(
        "diff-tree",
        "-r",
        "-z",
        "--no-commit-id",
        "--name-status",
        "--no-renames",
        older,
        newer,
    )
    fields = raw.decode("utf-8", "surrogateescape").split("\0")
    result: list[str] = []
    index = 0
    while index + 1 < len(fields) and fields[index]:
        result.append(fields[index + 1])
        index += 2
    return result


def added_widths(older: str, newer: str, path: str) -> list[int]:
    raw = git("diff", "--no-ext-diff", "--unified=0", older, newer, "--", path)
    return [
        len(line[1:])
        for line in raw.decode("utf-8", "strict").splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]


class NormalizeCensus(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if node.value in {OLD_CENSUS, NEW_CENSUS}:
            return ast.copy_location(ast.Constant(value="<derived-census>"), node)
        return node


packet = ROOT / "packets" / "r002"
identity = json.loads((packet / "candidate.json").read_bytes())
assert set(identity) == {
    "schema_version",
    "task_id",
    "round",
    "ref",
    "commit",
    "base",
    "tree",
    "manifest_sha256",
    "date",
}
assert identity["schema_version"] == "pontius-handoff-candidate-v1"
assert identity["task_id"] == "windows-handle-fixture"
assert identity["round"] == "r002"
assert identity["commit"] == R002
assert identity["base"] == BASE
assert git("rev-parse", identity["ref"]).decode().strip() == R002
assert git("rev-parse", f"{R002}^").decode().strip() == BASE
assert git("rev-parse", f"{R002}^{{tree}}").decode().strip() == identity["tree"]

base_paths = changed_paths(BASE, R002)
assert base_paths == [INVENTORY, SOURCE], base_paths
rows: list[str] = []
for path in base_paths:
    raw = blob(R002, path)
    assert raw == (packet / "files" / path).read_bytes()
    rows.append(f"{hashlib.sha256(raw).hexdigest()}  {path}\n")
manifest = "".join(sorted(rows)).encode("ascii")
assert manifest == (packet / "manifest.sha256").read_bytes()
manifest_digest = hashlib.sha256(manifest).hexdigest()
assert manifest_digest == identity["manifest_sha256"]

r001_to_r002 = changed_paths(R001, R002)
assert r001_to_r002 == [SOURCE], r001_to_r002
assert blob(R001, INVENTORY) == blob(R002, INVENTORY)
assert blob(R001, PROFILES) == blob(R002, PROFILES)

old_source = blob(R001, SOURCE)
new_source = blob(R002, SOURCE)
assert old_source.count(OLD_CENSUS.encode("ascii")) == 1
assert new_source.count(NEW_CENSUS.encode("ascii")) == 1
old_tree = NormalizeCensus().visit(ast.parse(old_source, filename=f"{R001}:{SOURCE}"))
new_tree = NormalizeCensus().visit(ast.parse(new_source, filename=f"{R002}:{SOURCE}"))
ast.fix_missing_locations(old_tree)
ast.fix_missing_locations(new_tree)
assert ast.dump(old_tree, include_attributes=False) == ast.dump(
    new_tree, include_attributes=False
)

r001_added_widths = added_widths(BASE, R001, SOURCE)
r002_added_widths = added_widths(R001, R002, SOURCE)
assert sorted(width for width in r001_added_widths if width > 100) == [101, 103, 104, 106, 107]
assert all(width <= 100 for width in r002_added_widths)
assert not new_source.startswith(b"\xef\xbb\xbf")
assert b"\r" not in new_source
assert new_source.endswith(b"\n")
assert all(line.rstrip(b" \t") == line for line in new_source.splitlines())

parsed = ast.parse(new_source, filename=f"{R002}:{SOURCE}")
adapter = next(
    node
    for node in parsed.body
    if isinstance(node, ast.ClassDef) and node.name == "_ControlledWindowsHandles"
)
source_lines = new_source.decode("utf-8").splitlines()
adapter_nonblank = sum(
    bool(line.strip()) for line in source_lines[adapter.lineno - 1 : adapter.end_lineno]
)
assert adapter_nonblank <= 200

print(f"ref={R002}")
print(f"base={BASE}")
print(f"tree={identity['tree']}")
print(f"manifest={manifest_digest}")
print("manifest_rows=")
for row in sorted(rows):
    print(row, end="")
print(f"base_to_r002_paths={base_paths}")
print(f"r001_to_r002_paths={r001_to_r002}")
print("inventory_bytes_unchanged=True")
print("profile_bytes_unchanged=True")
print("normalized_ast_equal=True")
print(f"r001_overlong_added={sorted(width for width in r001_added_widths if width > 100)}")
print(f"r002_max_added_width={max(r002_added_widths)}")
print(f"adapter_nonblank={adapter_nonblank}")
print("exactness=LF,no-BOM,no-trailing-whitespace,final-LF")
