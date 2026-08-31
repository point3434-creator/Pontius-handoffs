import sys
assert sys.version_info[:3] == (3, 11, 15), sys.version
assert sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode
assert sys.flags.safe_path
import ast, hashlib, json
from pathlib import Path

base = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority\rewrite-r1-base-generator.py")
source = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-core-v1\tools\generate_test_inventory.py")
fragment = Path(r"C:\Users\point\AppData\Local\Temp\pontius-r1-task1-fragment-b02.py.txt")
old, current, added = base.read_bytes(), source.read_bytes(), fragment.read_bytes()
sha = lambda b: hashlib.sha256(b).hexdigest()
assert sha(old) == "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
assert sha(added) == "e4260d423bc6fa5d7a66c527f30dd87cfb3be86392d01967bbac5c40cf23cd3c"
assert sha(current) == "ff889b1ee3595d23d2109d15d87f80d8f5c153b3db524aaef3eb53b1797dcab1"
assert current.count(added) == 1
assert current.replace(added, b"", 1) == old
assert b"\r" not in current and not current.startswith(b"\xef\xbb\xbf")
old_tree = ast.parse(old, filename=str(base))
new_tree = ast.parse(current, filename=str(source))
fragment_tree = ast.parse(added, filename=str(fragment))
def names(node):
    if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
        return [node.name]
    if isinstance(node, ast.Assign):
        return [t.id for t in node.targets if isinstance(t, ast.Name)]
    return []
new_names = {n for node in fragment_tree.body for n in names(node)}
old_names = {n for node in old_tree.body for n in names(node)}
assert not new_names.intersection(old_names)
assert all(n.startswith(("_C", "_c_")) for n in new_names)
remaining = ast.Module(body=[n for n in new_tree.body if not set(names(n)).intersection(new_names)], type_ignores=[])
assert ast.dump(remaining, include_attributes=False) == ast.dump(old_tree, include_attributes=False)
for node in fragment_tree.body:
    if isinstance(node, ast.ClassDef):
        assert all(not isinstance(s, ast.AnnAssign) or not isinstance(s.target, ast.Name) or s.target.id != "budget"
                   for s in node.body) or node.name == "_CContext"
        decorator = node.decorator_list[0]
        assert isinstance(decorator, ast.Call)
        assert any(k.arg == "eq" and isinstance(k.value, ast.Constant) and k.value.value is False
                   for k in decorator.keywords)
    assert isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.Assign))
for node in ast.walk(fragment_tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        assert node.func.id not in {"eval", "exec", "compile", "_AnalysisBudget", "_SourceOrderedResolver", "_review_body"}
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Attribute) and target.attr == "write_token":
                assert isinstance(target.value, ast.Name) and target.value.id == "state"
report = {
    "kind": "AST-only Task1 preservation; no candidate import or function execution",
    "runtime": list(sys.version_info[:3]), "source": str(source),
    "source_sha256": sha(current), "source_bytes": len(current),
    "base_sha256": sha(old), "fragment_sha256": sha(added),
    "inserted_lines": len(added.splitlines()), "removed_lines": 0,
    "original_bytes_exact_after_removing_insertion": True,
    "original_ast_exact": True, "new_names_do_not_collide": True,
    "evaluator_wiring_unchanged": True, "new_budget_constructors": 0,
    "snapshot_tables_banks_do_not_retain_budget": True,
    "new_definitions": [{"name": n.name, "line": n.lineno, "end_line": n.end_lineno}
                        for n in new_tree.body if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name in new_names]
}
print(json.dumps(report, sort_keys=True, indent=2))
