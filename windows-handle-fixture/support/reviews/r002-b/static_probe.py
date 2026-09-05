import ast
import difflib
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(r"D:\Pontius\tmp\windows-handle-fixture-r001")
WORK = ROOT / "authoring"
PACKET = ROOT / "packets" / "r002"
GIT = r"C:\Program Files\Git\cmd\git.exe"
BASE = "5e56e4454f7b8ccb360d3e36245abc33318349bb"
R1 = "76309774b551a874b8f9c677bc59e51299cee0e4"
CANDIDATE = "c7de23de276c50463d831f3983fede82a5400ce8"
EXPECTED_TREE = "014ee05a5014181bd63471247e5ee09607bb2346"
EXPECTED_MANIFEST = "f5e06a5fa9d0fdf37888d29f8bfe6b395b6fc40a4c6f87258f66c95aa17421ed"
SOURCE = "tests/test_inventory_and_profiles.py"
INVENTORY = "tests/test-inventory.json"
OLD_CENSUS = "37b7508932c784b6898999b2c024eeb8e004aa492b10cf1a948a1028f3cc9ed2"
NEW_CENSUS = "c62e275fa42bcb8cc9bef4a382990793adc03ecc9d9db1b6fcd35aeb9b23372e"


def git(*args):
    return subprocess.run(
        [GIT, "-C", str(WORK), *args], check=True, capture_output=True
    ).stdout


def blob(commit, path):
    return git("cat-file", "blob", f"{commit}:{path}")


def changed_paths(first, second):
    raw = git(
        "diff-tree", "-r", "-z", "--no-commit-id", "--name-status",
        "--no-renames", first, second,
    )
    fields = raw.decode("utf-8", "surrogateescape").split("\0")
    rows = []
    index = 0
    while index + 1 < len(fields) and fields[index]:
        rows.append((fields[index], fields[index + 1]))
        index += 2
    return rows


def added_line_widths(first, second, path):
    raw = git("diff", "--no-ext-diff", "--no-renames", "--unified=0", first, second, "--", path)
    lines = raw.decode("utf-8", "surrogateescape").splitlines()
    added = [line[1:] for line in lines if line.startswith("+") and not line.startswith("+++")]
    return len(added), max(map(len, added), default=0), [line for line in added if len(line) > 100]


def hygiene(data):
    lines = data.splitlines()
    return {
        "bom": data.startswith(b"\xef\xbb\xbf"),
        "cr": b"\r" in data,
        "final_lf": data.endswith(b"\n"),
        "trailing": sum(line.endswith((b" ", b"\t")) for line in lines),
    }


def main():
    ref = git("rev-parse", "refs/heads/review/windows-handle-fixture/r002").decode().strip()
    tree = git("rev-parse", f"{CANDIDATE}^{{tree}}").decode().strip()
    parent = git("rev-parse", f"{CANDIDATE}^").decode().strip()
    assert ref == CANDIDATE
    assert tree == EXPECTED_TREE
    assert parent == BASE
    print("IDENTITY", ref, parent, tree)

    base_changed = changed_paths(BASE, CANDIDATE)
    correction_changed = changed_paths(R1, CANDIDATE)
    assert base_changed == [("M", INVENTORY), ("M", SOURCE)]
    assert correction_changed == [("M", SOURCE)]
    print("BASE_CHANGED", base_changed)
    print("CORRECTION_CHANGED", correction_changed)

    rows = []
    for status, path in base_changed:
        digest = "0" * 64 if status.startswith("D") else hashlib.sha256(blob(CANDIDATE, path)).hexdigest()
        rows.append(f"{digest}  {path}\n")
        if not status.startswith("D"):
            assert (PACKET / "files" / path).read_bytes() == blob(CANDIDATE, path)
    manifest_bytes = "".join(sorted(rows)).encode()
    manifest_digest = hashlib.sha256(manifest_bytes).hexdigest()
    assert manifest_bytes == (PACKET / "manifest.sha256").read_bytes()
    assert manifest_digest == EXPECTED_MANIFEST
    candidate_json = json.loads((PACKET / "candidate.json").read_text(encoding="utf-8"))
    assert candidate_json["commit"] == CANDIDATE
    assert candidate_json["base"] == BASE
    assert candidate_json["tree"] == EXPECTED_TREE
    assert candidate_json["manifest_sha256"] == EXPECTED_MANIFEST
    print("MANIFEST", manifest_digest)
    for row in sorted(rows):
        print("MANIFEST_ROW", row.rstrip())

    r1_source_bytes = blob(R1, SOURCE)
    source_bytes = blob(CANDIDATE, SOURCE)
    inventory_bytes = blob(CANDIDATE, INVENTORY)
    assert blob(R1, INVENTORY) == inventory_bytes
    print("HYGIENE_SOURCE", hygiene(source_bytes))
    print("HYGIENE_INVENTORY", hygiene(inventory_bytes))
    assert hygiene(source_bytes) == {"bom": False, "cr": False, "final_lf": True, "trailing": 0}
    assert hygiene(inventory_bytes) == {"bom": False, "cr": False, "final_lf": True, "trailing": 0}

    for first, label in ((BASE, "BASE_TO_R002_SOURCE"), (R1, "R001_TO_R002_SOURCE")):
        count, longest, over = added_line_widths(first, CANDIDATE, SOURCE)
        print("ADDED_WIDTH", label, count, longest, len(over))
        assert not over

    r1_source = r1_source_bytes.decode("utf-8")
    source = source_bytes.decode("utf-8")
    r1_tree = ast.parse(r1_source)
    candidate_tree = ast.parse(source)
    old_values = [n.value for n in ast.walk(r1_tree) if isinstance(n, ast.Constant) and n.value == OLD_CENSUS]
    new_values = [n.value for n in ast.walk(candidate_tree) if isinstance(n, ast.Constant) and n.value == NEW_CENSUS]
    assert len(old_values) == 1
    assert len(new_values) == 1
    assert not any(isinstance(n, ast.Constant) and n.value == NEW_CENSUS for n in ast.walk(r1_tree))
    assert not any(isinstance(n, ast.Constant) and n.value == OLD_CENSUS for n in ast.walk(candidate_tree))
    for node in ast.walk(candidate_tree):
        if isinstance(node, ast.Constant) and node.value == NEW_CENSUS:
            node.value = OLD_CENSUS
    assert ast.dump(r1_tree, include_attributes=False) == ast.dump(candidate_tree, include_attributes=False)
    print("AST_EQUIVALENT_AFTER_ONE_CENSUS_NORMALIZATION", True)

    before_lines = r1_source.splitlines()
    after_lines = source.splitlines()
    changes = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=before_lines, b=after_lines).get_opcodes():
        if tag != "equal":
            changes.append((tag, (i1 + 1, i2), (j1 + 1, j2), before_lines[i1:i2], after_lines[j1:j2]))
    print("TEXTUAL_CHANGE_GROUPS", len(changes))
    for tag, before_span, after_span, before, after in changes:
        print("CHANGE", tag, before_span, after_span)
        for line in before:
            print("-", line)
        for line in after:
            print("+", line)
    assert len(changes) == 5

    module = ast.parse(source)
    classes = {node.name: node for node in module.body if isinstance(node, ast.ClassDef)}
    adapter_nonblank = 0
    for name in ("_RoutedWindowsCall", "_ControlledWindowsHandles"):
        node = classes[name]
        adapter_nonblank += sum(bool(line.strip()) for line in after_lines[node.lineno - 1:node.end_lineno])
    assert adapter_nonblank <= 200
    print("ADAPTER_NONBLANK", adapter_nonblank)

    base_inventory = json.loads(blob(BASE, INVENTORY))
    candidate_inventory = json.loads(inventory_bytes)
    base_entries = {entry["stable_id"]: entry for entry in base_inventory["entries"]}
    candidate_entries = {entry["stable_id"]: entry for entry in candidate_inventory["entries"]}
    added = sorted(candidate_entries.keys() - base_entries.keys())
    removed = sorted(base_entries.keys() - candidate_entries.keys())
    changed = sorted(
        key for key in base_entries.keys() & candidate_entries.keys()
        if base_entries[key] != candidate_entries[key]
    )
    assert len(added) == 3 and not removed and not changed
    print("INVENTORY_ADDED", *added, sep="\n")
    print("INVENTORY_REMOVED", removed)
    print("INVENTORY_CHANGED", changed)


if __name__ == "__main__":
    main()
