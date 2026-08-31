"""Root role-aware source and slot verification for the minimal v26 correction."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import symtable

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
h = lambda raw: hashlib.sha256(raw).hexdigest()
pins = {
    "engineer-generator-v24-storage.py": "156ee88a99abb26edeaaf178841c72e89f2bdc15696c37ef91f4dcc54b767431",
    "engineer-generator-v26-storage.py": "1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951",
    "engineer-name-radix-prototype-v1.py": "0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71",
    "engineer-generator-v24-storage-namespacing-v1.json": "39858fc73cdd3b2279184de3838f1d70533aacc9d382a477494caf39bf07c38a",
    "engineer-generator-v26-storage-from-v24.diff": "838433dd56ce774bf52111978880a13a2a9f658ec34a13e6241e4dd2d54df2b5",
}
raws = {name: (T / name).read_bytes() for name in pins}
assert {name: h(raw) for name, raw in raws.items()} == pins
old_raw, new_raw, proto_raw = [raws[name] for name in (
    "engineer-generator-v24-storage.py", "engineer-generator-v26-storage.py", "engineer-name-radix-prototype-v1.py")]
old, new, proto = map(ast.parse, (old_raw, new_raw, proto_raw))
compile(new, "v26-static-only", "exec")
mapping = json.loads(raws["engineer-generator-v24-storage-namespacing-v1.json"])["mapping"]
def scope_check(scope):
    for child in scope.get_children():
        assert not [symbol.get_name() for symbol in child.get_symbols()
                    if symbol.get_name() in mapping and (symbol.is_local() or symbol.is_free())]
        scope_check(child)
scope_check(symtable.symtable(proto_raw.decode(), "prototype", "exec"))
class GlobalNames(ast.NodeTransformer):
    def visit_Name(self, node):
        node.id = mapping.get(node.id, node.id)
        return node
def named(tree):
    result = {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            result[n.name] = n
        elif isinstance(n, ast.Assign):
            for target in n.targets:
                if isinstance(target, ast.Name):
                    result[target.id] = n
    return result
a, b = named(old), named(new)
dump = lambda n: ast.dump(n, include_attributes=False)
checked, rejected_old = [], []
for original, target in mapping.items():
    if original == "Meter":
        continue
    reference = copy.deepcopy(named(proto)[original])
    if isinstance(reference, (ast.FunctionDef, ast.ClassDef)):
        reference.name = target
    reference = GlobalNames().visit(reference)
    assert dump(reference) == dump(b[target]), target
    checked.append(target)
    if dump(reference) != dump(a[target]):
        rejected_old.append(target)
assert len(checked) == 47 and rejected_old
old_nodes, new_nodes = list(ast.walk(old)), list(ast.walk(new))
assert len(old_nodes) == len(new_nodes)
changes = []
for x, y in zip(old_nodes, new_nodes, strict=True):
    assert type(x) is type(y)
    if isinstance(x, ast.Attribute) and x.attr != y.attr:
        assert {"_name_history": "_history", "_name_order": "_order"}[x.attr] == y.attr
        changes.append((x.lineno, x.attr, y.attr))
        x.attr = y.attr
assert len(changes) == 17 and dump(old) == dump(new)
for cls in ("_NameVersion", "_NameCursor"):
    for version, tree, should_pass in (("v24", ast.parse(old_raw), False), ("v26", new, True)):
        node = named(tree)[cls]
        declaration, = [n for n in node.body if isinstance(n, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == "__slots__" for t in n.targets)]
        slots = set(ast.literal_eval(declaration.value))
        writes = {n.attr for n in ast.walk(node) if isinstance(n, ast.Attribute)
                  and isinstance(n.ctx, ast.Store) and isinstance(n.value, ast.Name) and n.value.id == "self"}
        assert (not writes - slots) is should_pass, (version, cls)
report = {"schema": "coordinator-v26-storage-inspection-v1", "pins": pins,
          "changed_attributes": changes, "prototype_roles_verified": checked,
          "v24_rejected_by_role_comparison": rejected_old,
          "v24_slot_check_rejects_and_v26_passes": True,
          "all_other_ast_fields_exact": True, "candidate_executed_or_imported": False,
          "manual_review": "Read all17 attribute corrections and full category root-cause note. No adapter work, algorithm, charge, cap, test or semantic changes. Reference comparison keeps attributes/strings/method/parameter names exact and only namespaces audited module names.",
          "disposition": "Run unchanged design53 on real311 in a fresh snapshot. v24 failure retained; no314/matrix/corpus expansion until floor success. No W/main integration."}
raw = (json.dumps(report, indent=2) + "\n").encode()
for name, data in {"coordinator-v26-storage-inspection-v1.json": raw,
                   "coordinator-inspect-v26-storage-v1.py": Path(__file__).read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(data)
print(json.dumps({"report_sha256": h(raw), "changed_attributes": len(changes), "reference_nodes": len(checked)}))
