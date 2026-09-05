"""Read-only raw Git/packet audit; optional post-acceptance receipt audit."""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
GIT = r"C:\Program Files\Git\cmd\git.exe"
WORK = ROOT / "authoring"
BASE = "5e56e4454f7b8ccb360d3e36245abc33318349bb"

def git(*args, cwd=WORK):
    return subprocess.check_output(
        [GIT, "-c", f"safe.directory={cwd.as_posix()}", "-C", str(cwd), *args],
        stderr=subprocess.PIPE,
    )

packet = ROOT / "packets" / sys.argv[1]
identity = json.loads((packet / "candidate.json").read_bytes())
commit = identity["commit"]
assert identity["base"] == BASE
assert git("rev-parse", identity["ref"]).decode().strip() == commit
assert git("rev-parse", commit + "^").decode().strip() == BASE
assert git("rev-parse", commit + "^{tree}").decode().strip() == identity["tree"]
paths = git("diff", "--name-only", "--no-renames", BASE, commit).decode().splitlines()
assert set(paths) <= {"tests/test_inventory_and_profiles.py", "tests/test-inventory.json", "tests/test-profiles.toml"}
rows = []
for path in paths:
    raw = git("cat-file", "blob", f"{commit}:{path}")
    assert raw == (packet / "files" / path).read_bytes(), path
    rows.append(hashlib.sha256(raw).hexdigest() + "  " + path + "\n")
manifest = "".join(sorted(rows)).encode("ascii")
assert manifest == (packet / "manifest.sha256").read_bytes()
assert hashlib.sha256(manifest).hexdigest() == identity["manifest_sha256"]
old = json.loads(git("cat-file", "blob", BASE + ":tests/test-inventory.json"))
new = json.loads(git("cat-file", "blob", commit + ":tests/test-inventory.json"))
print("Frozen identity/raw blobs match:", commit, len(paths), "paths")
print("Inventory entries:", len(old["entries"]), "->", len(new["entries"]))
old_entries = {entry["stable_id"]: entry for entry in old["entries"]}
new_entries = {entry["stable_id"]: entry for entry in new["entries"]}
assert all(new_entries[key] == value for key, value in old_entries.items())
added = set(new_entries) - set(old_entries)
assert added == {
    "tests/test_inventory_and_profiles.py::AtomicAndGitBoundaryTests::" + name
    for name in (
        "test_windows_controlled_reuse_preserves_native_resources",
        "test_windows_controlled_reuse_detects_production_replay",
        "test_windows_controlled_reuse_releases_unpublished_and_leaked_handles",
    )
}
print("All original entries unchanged; exactly three authorized controls added")
if sys.argv[1] == "r002":
    import ast
    path = "tests/test_inventory_and_profiles.py"
    prior = git("cat-file", "blob", "76309774b551a874b8f9c677bc59e51299cee0e4:" + path)
    current = git("cat-file", "blob", commit + ":" + path)
    parsed = ast.parse(current)
    resets = 0
    for node in ast.walk(parsed):
        if isinstance(node, ast.Constant) and node.value == "c62e275fa42bcb8cc9bef4a382990793adc03ecc9d9db1b6fcd35aeb9b23372e":
            node.value = "37b7508932c784b6898999b2c024eeb8e004aa492b10cf1a948a1028f3cc9ed2"
            resets += 1
    assert resets == 1 and ast.dump(ast.parse(prior)) == ast.dump(parsed)
    assert git("cat-file", "blob", commit + ":tests/test-inventory.json") == (ROOT / "packets/r001/files/tests/test-inventory.json").read_bytes()
    added_lines = [line[1:] for line in git("diff", "-U0", BASE, commit, "--", path).decode().splitlines() if line.startswith("+") and not line.startswith("+++")]
    assert all(len(line) <= 100 for line in added_lines)
    assert b"\r" not in current and not current.startswith(b"\xef\xbb\xbf")
    assert current.endswith(b"\n") and all(line.rstrip() == line for line in current.splitlines())
    print("Correction AST unchanged except one derived census literal; added-line hygiene passes")
if "--acceptance" in sys.argv:
    total = 0
    methods = {}
    import re
    for slot in ("311", "314"):
        for sequence in range(1, 20):
            receipt = ROOT / "run-records" / f"broad-{sys.argv[1]}-{sequence:02}-{slot}.json"
            records = json.loads(receipt.read_bytes())
            assert len(records) == 2 and all(r["exit_code"] == 0 for r in records), receipt
            record = records[-1]
            assert record["argv"][:2] == ["-B", "-P"]
            snapshot = pathlib.Path(record["snapshot"])
            for path in paths:
                assert (snapshot / path).read_bytes() == (packet / "files" / path).read_bytes(), (receipt, path)
            assert set(git("diff", "--name-only", cwd=snapshot).decode().splitlines()) <= set(paths), receipt
            match = re.search(r"Ran (\d+) tests? in", record["stderr"])
            methods[slot] = methods.get(slot, 0) + (int(match[1]) if match else 0)
            total += 1
    print("Acceptance exits, flags, and post-run source audit:", total, "commands", methods)
