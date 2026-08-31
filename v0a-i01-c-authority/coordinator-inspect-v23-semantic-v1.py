"""Root static candidate verification; no candidate import or payload execution."""
from pathlib import Path
import ast
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
sha = lambda raw: hashlib.sha256(raw).hexdigest()
pins = {
    "engineer-generator-v22.py": "61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3",
    "engineer-generator-v23-semantic.py": "53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499",
    "engineer-checks/generator-v23-semantic-static-v1.json": "64439a89ea77835aabf68f29290ad6d491ca1602a4e6ee5bdfed1034c3e709e0",
    "engineer-generator-v23-semantic-category-inventory-v1.md": "48d803bb88096ae9a7796f50b74e48c1c8a7136cc06f747061d8bbc4ac2af275",
    "coordinator-preservation-baseline-v2.json": "a2f848258a6f7622161e92962b594568400bc4582bb32461aedd3c41a85d768e",
}
raws = {name: (T / name).read_bytes() for name in pins}
assert {name: sha(raw) for name, raw in raws.items()} == pins
old_raw = raws["engineer-generator-v22.py"]
new_raw = raws["engineer-generator-v23-semantic.py"]
old, new = ast.parse(old_raw), ast.parse(new_raw)
compile(new, "v23-static-only", "exec")
defs = lambda tree: {n.name: n for n in tree.body if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))}
dump = lambda n: ast.dump(n, include_attributes=False)
a, b = defs(old), defs(new)
changed = sorted(k for k in a.keys() & b.keys() if dump(a[k]) != dump(b[k]))
added, removed = sorted(b.keys() - a.keys()), sorted(a.keys() - b.keys())
author = json.loads(raws["engineer-checks/generator-v23-semantic-static-v1.json"])
assert changed == sorted(author["changed_top_level"])
assert added == sorted(author["added_top_level"])
assert not removed
def source(raw, node):
    return b"".join(raw.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])
storage = author["exact_name_storage_nodes"]
assert len(storage) == len(set(storage)) == 27
for name in storage:
    assert dump(a[name]) == dump(b[name]), name
    assert source(old_raw, a[name]) == source(new_raw, b[name]), name
assert dump(a["_AnalysisBudget"]) == dump(b["_AnalysisBudget"])
assert source(old_raw, a["_AnalysisBudget"]) == source(new_raw, b["_AnalysisBudget"])
for name in ("_transfer_authority", "_FlowValue"):
    assert dump(a[name]) == dump(b[name]), name
def constants(tree):
    return {target.id: dump(n) for n in tree.body if isinstance(n, ast.Assign)
            for target in n.targets if isinstance(target, ast.Name) and target.id.startswith("MAXIMUM_ANALYSIS_")}
assert constants(old) == constants(new)
methods = {}
for name in changed:
    if not isinstance(a[name], ast.ClassDef):
        continue
    am = {n.name: n for n in a[name].body if isinstance(n, ast.FunctionDef)}
    bm = {n.name: n for n in b[name].body if isinstance(n, ast.FunctionDef)}
    assert not am.keys() - bm.keys(), name
    methods[name] = sorted(k for k in bm if k not in am or dump(am[k]) != dump(bm[k]))
assert methods == {name: sorted(names) for name, names in author["changed_or_added_methods"].items()}
am = {n.name: n for n in a["_ExecutionState"].body if isinstance(n, ast.FunctionDef)}
bm = {n.name: n for n in b["_ExecutionState"].body if isinstance(n, ast.FunctionDef)}
for name in ("cell", "_write_cells"):
    assert [dump(n) for n in am[name].body] == [dump(n) for n in bm[name].body]
assert dump(am["_transferred_name_entry"]) == dump(bm["_transferred_name_entry"])
baseline = json.loads(raws["coordinator-preservation-baseline-v2.json"])["paths"]
expected = dict(baseline)
expected["tools/generate_test_inventory.py"] = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
expected["tests/test_inventory_and_profiles.py"] = "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
assert {p: sha((W / p).read_bytes()) for p in expected} == expected
report = {
    "schema": "coordinator-v23-semantic-inspection-v1", "pins": pins,
    "candidate_imported_or_executed": False,
    "changed_top_level": changed, "added_top_level": added, "changed_methods": methods,
    "exact_storage_nodes": storage, "caps_and_budget_exact": True,
    "transfer_and_flowvalue_exact": True, "protected_w_paths_rehashed": expected,
    "manual_review": [
        "Root read the whole added/changed v22 delta and category inventory; pure deleted duplicate comprehension body was compared structurally.",
        "Current cell content, lexical-origin tokens, class successor projection, shared Name routes and actual-callable historical replay inspected.",
        "Independent source review raises three unresolved comprehension/deferred-generator paths; this is not a CLEAN verdict.",
    ],
    "open_source_concerns": [
        "Comprehension target discovery includes Load names beneath Attribute/Subscript targets.",
        "Mixed direct and previously merged generator alternatives may discard deferred states.",
        "Initially empty class generator with changed outer iterator may bypass conservative sensitivity refusal.",
    ],
    "dispatch_disposition": "Run existing fixed original10/class12/Name8/comprehension6 diagnostically against this exact candidate. No integration or success claim; any repair is a new candidate.",
    "dispatch_order": "Actual311 first.314 only after same-candidate completed intact floor with no oracle/analyzer/infrastructure errors. Existing semantic RED may replicate.",
    "limits": "No payload here. Existing pack expectations and caps remain fixed. Source concerns await independent note and public reproduction.",
}
data = (json.dumps(report, indent=2) + "\n").encode()
for name, raw in {
    "coordinator-v23-semantic-inspection-v1.json": data,
    "coordinator-inspect-v23-semantic-v1.py": Path(__file__).read_bytes(),
}.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({"report_sha256": sha(data), "payload_executed": False, "protected_paths": len(expected)}))
