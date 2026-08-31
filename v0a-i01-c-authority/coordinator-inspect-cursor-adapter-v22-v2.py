"""Independent AST and preservation inspection; no candidate import or execution."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import os
import re
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
V20_SHA = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
PROTO_SHA = "67acb279510924311266b985e15e95e53ae9d0a11d64a50d108f254a690deb2a"
BASELINE_SHA = "a2f848258a6f7622161e92962b594568400bc4582bb32461aedd3c41a85d768e"


def h(raw):
    return hashlib.sha256(raw).hexdigest()


def dump(node):
    return ast.dump(node, include_attributes=False)


def definitions(tree):
    return {n.name: n for n in tree.body if isinstance(n, (ast.ClassDef, ast.FunctionDef))}


def stable_outer(tree):
    body = []
    skipping = False
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "_NAME_MISSING" for t in n.targets
        ):
            continue  # This unchanged sentinel moved inside the storage block.
        if isinstance(n, ast.ClassDef) and n.name == "_NameMeter":
            skipping = True
        if skipping:
            if isinstance(n, ast.ClassDef) and n.name == "_ExecutionState":
                skipping = False
            continue
        if isinstance(n, ast.ClassDef) and n.name == "_SourceOrderedResolver":
            n = copy.copy(n)
            n.body = [c for c in n.body if not isinstance(c, ast.FunctionDef) or c.name != "_merge_states"]
        body.append(n)
    return ast.Module(body=body, type_ignores=[])


assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
assert len(sys.argv) == 3 and all(re.fullmatch("[a-f0-9]{64}", s) for s in sys.argv[1:])
source_sha, map_sha = sys.argv[1:]
source_path = T / "engineer-generator-v22.py"
source = source_path.read_bytes()
assert h(source) == source_sha
mapping_raw = (T / "engineer-name-cursor-v22-namespacing.json").read_bytes()
assert h(mapping_raw) == map_sha
mapping = json.loads(mapping_raw)
assert mapping["candidate_sha256"] == source_sha and mapping["prototype_sha256"] == PROTO_SHA
old_raw = (T / "engineer-generator-v20.py").read_bytes()
prototype_raw = (T / "engineer-name-cursor-prototype-v1.py").read_bytes()
assert h(old_raw) == V20_SHA and h(prototype_raw) == PROTO_SHA
old, candidate, prototype = (ast.parse(x) for x in (old_raw, source, prototype_raw))
old_defs, new_defs = definitions(old), definitions(candidate)
assert dump(stable_outer(old)) == dump(stable_outer(candidate)), "unapproved change outside storage and merge"
sentinels = []
for tree in (old, candidate):
    nodes = [n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == "_NAME_MISSING" for t in n.targets)]
    assert len(nodes) == 1
    sentinels.append(dump(nodes[0]))
assert sentinels[0] == sentinels[1], "moved sentinel definition changed"
protected = ("_NameMeter", "_AnalysisBudget", "_AuthorityMap", "_ObservedAuthorityMap",
             "_AuthorityState", "_AuthorityRecord", "_FlowValue")
for name in protected:
    assert dump(old_defs[name]) == dump(new_defs[name]), name
old_methods = definitions(old_defs["_ExecutionState"])
new_methods = definitions(new_defs["_ExecutionState"])
for name in ("cell", "_write_cells", "_transferred_name_entry", "pop", "setdefault"):
    assert dump(old_methods[name]) == dump(new_methods[name]), name
assert [dump(n) for n in old_methods["__delitem__"].body[1:]] == [
    dump(n) for n in new_methods["__delitem__"].body[1:]], "captured-cell deletion changed"


class Rename(ast.NodeTransformer):
    def visit_Name(self, node):
        node = copy.copy(node)
        node.id = mapping["identifier_map"].get(node.id, node.id)
        return node

    def visit_ClassDef(self, node):
        node.name = mapping["identifier_map"].get(node.name, node.name)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        node.name = mapping["identifier_map"].get(node.name, node.name)
        return self.generic_visit(node)


transplanted = {}
for node in prototype.body:
    if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name not in {"Meter", "BudgetExceeded"}:
        expected = Rename().visit(copy.deepcopy(node))
        assert expected.name in new_defs
        assert dump(expected) == dump(new_defs[expected.name]), expected.name
        transplanted[expected.name] = h(dump(expected).encode())
assert len(transplanted) == 26
for name, value in (("_MAXIMUM_NAME_SEALED_LAYERS", 8),):
    assignments = [n for n in candidate.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
    assert len(assignments) == 1 and ast.literal_eval(assignments[0].value) == value
expected_adapter_changes = {
    "__init__", "__getitem__", "__len__", "__contains__", "get", "items", "keys",
    "values", "_project", "_project_pop", "__setitem__", "__delitem__", "update", "clear", "copy",
}
changed_methods = {name for name in old_methods if dump(old_methods[name]) != dump(new_methods[name])}
assert changed_methods <= expected_adapter_changes and set(old_methods) == set(new_methods)
for name in ("__setitem__", "__init__"):
    assert any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
               and n.func.id == "_name_check_name" for n in ast.walk(new_methods[name])), name
baseline_raw = (T / "coordinator-preservation-baseline-v2.json").read_bytes()
assert h(baseline_raw) == BASELINE_SHA
baseline = json.loads(baseline_raw)
preserved = {}
for name, pin in baseline["paths"].items():
    if name in {"tools/generate_test_inventory.py", "tests/test_inventory_and_profiles.py"}:
        continue
    assert h((W / name).read_bytes()) == pin, name
    preserved[name] = pin
assert len(preserved) == 15
assert h((W / "tools/generate_test_inventory.py").read_bytes()) == V20_SHA
assert h((W / "tests/test_inventory_and_profiles.py").read_bytes()) == "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
report = {
    "schema": "coordinator-cursor-adapter-v22-inspection-v2",
    "candidate_sha256": source_sha, "predecessor_sha256": V20_SHA,
    "prototype_sha256": PROTO_SHA, "namespacing_map_sha256": map_sha,
    "transplanted_definitions": transplanted, "protected_classes": list(protected),
    "changed_adapter_methods": sorted(changed_methods),
    "all_other_top_level_and_resolver_methods_ast_equal": True,
    "preserved_ab_other_c_and_generated_paths": preserved,
    "W_unchanged_v20": True, "candidate_imported_or_executed": False,
    "verification_history": "The v1 verifier stopped before output: its storage boundary excluded the unchanged _NAME_MISSING declaration moved across _NameMeter. v2 verifies that declaration separately and keeps the same outside-change restriction. No candidate was imported or executed.",
    "limits": ["Static engineering inspection; no behavior or production-fit claim.",
               "Class/capture/exception semantic logic remains unchanged and defective.",
               "This receipt is not a cold verdict, source installation or commit authorization."],
}
outputs = {
    "coordinator-cursor-adapter-v22-inspection-v2.json": (json.dumps(report, indent=2) + "\n").encode(),
    "coordinator-inspect-cursor-adapter-v22-v2.py": Path(__file__).read_bytes(),
    "coordinator-inspect-cursor-adapter-v22-v1.py": Path(r"D:\Pontius\codex-inspect-cursor-adapter-v22.py").read_bytes(),
}
assert not any((T / name).exists() for name in outputs)
for name, raw in outputs.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
print(json.dumps({name: h(raw) for name, raw in outputs.items()}, indent=2))
