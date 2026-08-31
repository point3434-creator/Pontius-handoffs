"""Coordinator AST/hash inspection only: imports neither prototype nor oracle."""
from pathlib import Path
import ast
from collections import defaultdict
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
sha = lambda raw: hashlib.sha256(raw).hexdigest()
pins = {
    "engineer-name-radix-prototype-v1.py": "0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71",
    "engineer-name-cursor-prototype-v1.py": "67acb279510924311266b985e15e95e53ae9d0a11d64a50d108f254a690deb2a",
    "engineer-name-radix-accounting-v1.json": "79f64e5e7bbb429bedd108654b69c8ab5893973ee742517b543129f762f68f2b",
    "engineer-name-radix-ownership-v1.md": "e7ce84bee0e87dec6ca85656225a733a87b2d6fdac7acd43457bb1436b976aa6",
    "tests-checks/indexed-storage-p-boundary-clarification-v1.md": "cdc1f9aa5f66114d744e2bc66728f4a64f85032a7b25399a9c0a4c728cb28cb8",
    "coordinator-preservation-baseline-v2.json": "a2f848258a6f7622161e92962b594568400bc4582bb32461aedd3c41a85d768e",
}
raws = {name: (T / name).read_bytes() for name in pins}
assert {name: sha(raw) for name, raw in raws.items()} == pins
new = ast.parse(raws["engineer-name-radix-prototype-v1.py"])
old = ast.parse(raws["engineer-name-cursor-prototype-v1.py"])
definitions = lambda tree: {node.name: node for node in tree.body
    if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
old_defs, new_defs = definitions(old), definitions(new)
dump = lambda node: ast.dump(node, include_attributes=False)
preserved = ["Meter", "BudgetExceeded", "Entry", "_check_name", "_History", "_history",
             "_Order", "_order", "_known_order", "_seal_order_table", "_realize_order",
             "_charge_cache_commit", "_commit_order", "_keys", "_ordered_items", "_common_history"]
assert all(dump(old_defs[name]) == dump(new_defs[name]) for name in preserved)
public = []
for owner in ("NameVersion", "NameCursor"):
    before = definitions(old_defs[owner])
    after = definitions(new_defs[owner])
    for name, node in before.items():
        if not name.startswith("_"):
            assert dump(node.args) == dump(after[name].args), (owner, name)
            public.append(owner + "." + name)
    assert set(after) - set(before) == ({"from_unique_entries"} if owner == "NameVersion" else set())
assert dump(old_defs["join"].args) == dump(new_defs["join"].args)
old_cursor, new_cursor = definitions(old_defs["NameCursor"]), definitions(new_defs["NameCursor"])
assert all(dump(node) == dump(new_cursor[name]) for name, node in old_cursor.items()
           if name not in {"_entry", "_replace_entry"})
sites = defaultdict(list)
class ChargeInventory(ast.NodeVisitor):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "charge":
            assert len(node.args) in (1, 2) and not node.keywords
            kind = ast.literal_eval(node.args[0])
            assert type(kind) is str
            units = ast.unparse(node.args[1]) if len(node.args) == 2 else "1"
            sites[kind].append({"line": node.lineno, "units": units})
        self.generic_visit(node)
ChargeInventory().visit(new)
mapping = json.loads(raws["engineer-name-radix-accounting-v1.json"])
assert mapping["prototype_sha256"] == pins["engineer-name-radix-prototype-v1.py"]
assert set(sites) == set(mapping["categories"])
for kind, actual in sites.items():
    expected = [{"line": site["line"], "units": site["units"]}
                for site in mapping["categories"][kind]["source_sites"]]
    assert sorted(actual, key=lambda item: item["line"]) == sorted(expected, key=lambda item: item["line"]), kind
    assert mapping["categories"][kind]["metric"] in {"P", "non-P"}
for node in ast.walk(new):
    if isinstance(node, ast.Import):
        assert all(alias.name == "sys" for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        assert node.module in {"__future__", "dataclasses", "types"}
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        assert node.func.id not in {"exec", "eval", "compile", "__import__"}
baseline = json.loads(raws["coordinator-preservation-baseline-v2.json"])
preserved_paths = {name: digest for name, digest in baseline["paths"].items()
                   if name not in {"tools/generate_test_inventory.py", "tests/test_inventory_and_profiles.py"}}
assert len(preserved_paths) == 15
assert {name: sha((W / name).read_bytes()) for name in preserved_paths} == preserved_paths
assert sha((W / "tools/generate_test_inventory.py").read_bytes()) == "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
assert sha((W / "tests/test_inventory_and_profiles.py").read_bytes()) == "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
report = {
    "schema": "coordinator-radix-prototype-inspection-v1", "payload_executed": False,
    "inputs": pins, "protected_ast_equal": preserved, "public_signatures_equal": public,
    "new_public_api": "NameVersion.from_unique_entries", "accounted_categories": len(sites),
    "accounting_sites_match_source": True, "p_boundary_resolved_before_results": True,
    "preserved_paths": preserved_paths, "watch_unchanged": True,
    "manual_inspection": [
        "Read complete prototype and ownership map; immutable roots share no private editors.",
        "Publication and cache charges precede commit; prior snapshots retain legitimate owners.",
        "Bulk input validation and direct partitioning do not loop immutable insertion.",
        "Dictionary attempts exclude hidden CPython equality probes; observer counts are separate.",
        "Current-source accounting map is exhaustive; fixed wrapper fields remain non-P but in C.",
    ],
    "limitations": "Runtime correctness, collision activation, cost, retention and retry remain unverified; no production port authorized.",
}
for relative, raw in {
    "coordinator-radix-prototype-inspection-v1.json": (json.dumps(report, indent=2) + "\n").encode(),
    "coordinator-inspect-radix-prototype-v1.py": Path(__file__).read_bytes(),
}.items():
    with (T / relative).open("xb") as stream:
        stream.write(raw)
print(json.dumps({"inspected": True, "report_sha256": sha((T / "coordinator-radix-prototype-inspection-v1.json").read_bytes()),
                  "categories": len(sites), "preserved_paths": len(preserved_paths)}))
