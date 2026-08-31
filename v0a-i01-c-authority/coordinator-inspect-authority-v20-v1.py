"""Independent static scope/preservation inspection; never imports repository code."""
import ast
import hashlib
import json
from pathlib import Path
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
OLD_SHA = "3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1"
NEW_SHA = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
OUT = T / "coordinator-v20-inspection-v1.json"
COPY = T / "coordinator-inspect-authority-v20-v1.py"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def symbols(tree):
    found = {}
    def visit(node, prefix=""):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + child.name
                found.setdefault(name, []).append(child)
                visit(child, name + ".")
            else:
                visit(child, prefix)
    visit(tree)
    return found


def dump(node):
    return ast.dump(node, include_attributes=False)


assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
assert sys.dont_write_bytecode and not sys.flags.optimize
assert not OUT.exists() and not COPY.exists()
old_raw = (T / "engineer-generator-v19.py").read_bytes()
new_raw = (T / "engineer-generator-v20.py").read_bytes()
assert sha(old_raw) == OLD_SHA and sha(new_raw) == NEW_SHA
assert (W / "tools/generate_test_inventory.py").read_bytes() == new_raw
old_text, new_text = old_raw.decode(), new_raw.decode()
old_tree, new_tree = ast.parse(old_text), ast.parse(new_text)
old_symbols, new_symbols = symbols(old_tree), symbols(new_tree)
protected = ["_transfer_authority", "_AuthorityMap", "_ObservedAuthorityMap",
             "_AuthorityState", "_AuthorityRecord", "_FlowValue", "_AnalysisBudget",
             "_ExecutionState._write_cells", "_ExecutionState.cell"]
for name in protected:
    assert len(old_symbols[name]) == len(new_symbols[name]) == 1
    assert dump(old_symbols[name][0]) == dump(new_symbols[name][0]), name
caps = ("MAXIMUM_ANALYSIS_HELPER_DEPTH", "MAXIMUM_ANALYSIS_CHILD_DEPTH",
        "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS", "MAXIMUM_ANALYSIS_CARDINALITY",
        "MAXIMUM_ANALYSIS_WORK_UNITS")
def cap_nodes(tree):
    return {target.id: node for node in tree.body if isinstance(node, ast.Assign)
            for target in node.targets if isinstance(target, ast.Name) and target.id in caps}
old_caps, new_caps = cap_nodes(old_tree), cap_nodes(new_tree)
assert set(old_caps) == set(new_caps) == set(caps)
assert {key: dump(value) for key, value in old_caps.items()} == {
    key: dump(value) for key, value in new_caps.items()}
allowed = ["_call_environment", "_apply_helper_call_effects", "_merge_states",
           "_resume_deferred_local_generator", "_instantiate_deferred_local_generator",
           "_simple_local_helper_deferred_return"]
old_lines, new_lines = old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)
replacements = []
for name in allowed:
    full_name = "_SourceOrderedResolver." + name
    assert len(old_symbols[full_name]) == len(new_symbols[full_name]) == 1
    old_node, new_node = old_symbols[full_name][0], new_symbols[full_name][0]
    replacements.append((new_node.lineno - 1, new_node.end_lineno,
                         old_lines[old_node.lineno - 1:old_node.end_lineno]))
old_start = old_symbols["_ExecutionState"][0].lineno - 1
new_start = next(i for i, line in enumerate(new_lines) if line.strip() == "_NAME_MISSING = object()")
old_stop = old_symbols["_FlowExceptionalState"][0].decorator_list[0].lineno - 1
new_stop = new_symbols["_FlowExceptionalState"][0].decorator_list[0].lineno - 1
replacements.append((new_start, new_stop, old_lines[old_start:old_stop]))
inverse = list(new_lines)
for start, stop, restored in sorted(replacements, reverse=True):
    inverse[start:stop] = restored
assert "".join(inverse).encode() == old_raw, "change outside declared regions"
static_raw = (T / "engineer-checks/v20-storage-port-static.json").read_bytes()
assert sha(static_raw) == "12bfc43364de5e98279acb8669dfb0bacfb39f6bce4cd58628e531eccfacec3d"
static = json.loads(static_raw)
assert static["source_sha256"] == NEW_SHA and len(static["after"]) == 1761
for relative, digest in static["after"].items():
    assert sha((W / relative).read_bytes()) == digest, relative
assert [path for path in static["before"] if static["before"][path] != static["after"][path]] == [
    "tools/generate_test_inventory.py"]
baseline_raw = (T / "coordinator-preservation-baseline-v2.json").read_bytes()
assert sha(baseline_raw) == "a2f848258a6f7622161e92962b594568400bc4582bb32461aedd3c41a85d768e"
baseline = json.loads(baseline_raw)
scope = {"tools/generate_test_inventory.py", "tests/test_inventory_and_profiles.py"}
preserved = {path: digest for path, digest in baseline["paths"].items() if path not in scope}
assert len(preserved) == 15
for path, digest in preserved.items():
    assert sha((W / path).read_bytes()) == digest
assert sha((W / "tests/test_inventory_and_profiles.py").read_bytes()) == (
    "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd")
report = {"standing": "Static engineering inspection only; permits focused execution, not acceptance.",
          "source_sha256": NEW_SHA, "predecessor_sha256": OLD_SHA,
          "exact_inverse_to_predecessor": True, "protected_ast_unchanged": protected,
          "caps_unchanged": {key: ast.literal_eval(value.value) for key, value in new_caps.items()},
          "modified_regions": ["persistent names and ExecutionState", *allowed],
          "tracked_paths_rehashed": 1761, "preserved_paths": preserved,
          "released_v4_tests_unchanged": True, "production_payloads_run": [],
          "review_note": "No concrete semantic defect found in constructor, projection, adoption, "
                         "ordered fallback or distinct-cell path. Construction/fallback/ordering "
                         "cost and full public behavior remain execution obligations."}
control_raw = Path(__file__).read_bytes()
report["control_sha256"] = sha(control_raw)
with COPY.open("xb") as stream:
    stream.write(control_raw)
encoded = (json.dumps(report, indent=2) + "\n").encode()
with OUT.open("xb") as stream:
    stream.write(encoded)
print(json.dumps({"receipt": str(OUT), "sha256": sha(encoded), "source": NEW_SHA,
                  "preserved": len(preserved), "inverse_exact": True}, indent=2))
