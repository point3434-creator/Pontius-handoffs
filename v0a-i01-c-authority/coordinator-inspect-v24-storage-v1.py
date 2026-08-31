"""Root static verification and bounded first-dispatch disposition for v24."""
from pathlib import Path
import ast
import hashlib
import io
import json
import tokenize

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
h = lambda raw: hashlib.sha256(raw).hexdigest()
pins = {
    "engineer-generator-v22.py": "61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3",
    "engineer-generator-v24-storage.py": "156ee88a99abb26edeaaf178841c72e89f2bdc15696c37ef91f4dcc54b767431",
    "engineer-name-radix-prototype-v1.py": "0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71",
    "engineer-generator-v24-storage-namespacing-v1.json": "39858fc73cdd3b2279184de3838f1d70533aacc9d382a477494caf39bf07c38a",
    "engineer-generator-v24-storage-static-v1.json": "1ba6352dc8a7130f361ef962cdee7816d348c3322bb6c4179b56de2a41dca29e",
    "engineer-generator-v24-storage-handoff-v1.md": "66f72788e7f4081704ddd5392f00cdc12d49c477b4750b4ea0dd6ba58bc400a3",
    "tests-focused-control-v1.py": "2676cc5e58db5a1e70044610de1876c96e23b38cd1a55c4f22f47aaa59118eba",
}
raws = {name: (T / name).read_bytes() for name in pins}
assert {name: h(raw) for name, raw in raws.items()} == pins
old_raw, new_raw = raws["engineer-generator-v22.py"], raws["engineer-generator-v24-storage.py"]
old, new = ast.parse(old_raw), ast.parse(new_raw)
compile(new, "v24-static-only", "exec")
dump = lambda n: ast.dump(n, include_attributes=False)
def nodes(tree):
    result = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            result[node.name] = node
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    result[target.id] = node
    return result
a, b = nodes(old), nodes(new)
mapping = json.loads(raws["engineer-generator-v24-storage-namespacing-v1.json"])["mapping"]
tokens = list(tokenize.tokenize(io.BytesIO(raws["engineer-name-radix-prototype-v1.py"]).readline))
renamed = tokenize.untokenize([
    token._replace(string=mapping.get(token.string, token.string))
    if token.type == tokenize.NAME else token for token in tokens
])
prototype = nodes(ast.parse(renamed))
primitives = [name for original, name in mapping.items() if original != "Meter"]
assert len(primitives) == len(set(primitives)) == 47
for name in primitives:
    assert dump(prototype[name]) == dump(b[name]), name
allowed_old = {name for name in a if name.startswith(("_Name", "_name_", "_NAME_"))}
allowed_old.add("_MAXIMUM_NAME_SEALED_LAYERS")
allowed_old.add("_join_name_versions")
special = {"_ExecutionState", "_SourceOrderedResolver"}
protected = []
for name, node in a.items():
    if name in allowed_old or name in special:
        continue
    assert name in b and dump(node) == dump(b[name]), name
    protected.append(name)
assert not b.keys() - a.keys() - set(primitives)
assert not a.keys() - b.keys() - allowed_old
def methods(node):
    return {n.name: n for n in node.body if isinstance(n, ast.FunctionDef)}
for cls, changed in (("_ExecutionState", "__init__"), ("_SourceOrderedResolver", "_merge_states")):
    am, bm = methods(a[cls]), methods(b[cls])
    assert am.keys() == bm.keys()
    for name in am:
        if name != changed:
            assert dump(am[name]) == dump(bm[name]), cls + "." + name
            protected.append(cls + "." + name)
am, bm = methods(a["_ExecutionState"]), methods(b["_ExecutionState"])
assert dump(am["__init__"].body[-1]) == dump(bm["__init__"].body[-1])
prefix_len = len(am["__init__"].body) - 1
assert [dump(n) for n in am["__init__"].body[:prefix_len]] == [dump(n) for n in bm["__init__"].body[:prefix_len]]
am, bm = methods(a["_SourceOrderedResolver"]), methods(b["_SourceOrderedResolver"])
old_body, new_body = am["_merge_states"].body, bm["_merge_states"].body
assert len(old_body) == len(new_body)
differences = [i for i, (x, y) in enumerate(zip(old_body, new_body)) if dump(x) != dump(y)]
assert len(differences) == 1
assert isinstance(old_body[differences[0]], ast.If)
assert dump(old_body[differences[0]].test) == dump(new_body[differences[0]].test)
for name in ("_NameMeter", "_AnalysisBudget", "_FlowValue", "_transfer_authority"):
    assert dump(a[name]) == dump(b[name]), name
baseline = json.loads((T / "coordinator-preservation-baseline-v2.json").read_bytes())["paths"]
baseline["tools/generate_test_inventory.py"] = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
baseline["tests/test_inventory_and_profiles.py"] = "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
assert {p: h((W / p).read_bytes()) for p in baseline} == baseline
report = {
    "schema": "coordinator-v24-storage-inspection-v1", "pins": pins,
    "candidate_executed_or_imported": False, "prototype_definitions_and_constants_exact": primitives,
    "protected_outer_definitions_and_methods": protected,
    "generic_constructor_loop_and_setup_exact": True, "sparse_merge_and_prefix_exact": True,
    "protected_w_paths": baseline,
    "manual_review": [
        "Root read complete two adapter blocks, constructor/merge surrounding control, exact namespacing map and candidate handoff.",
        "Primitive source/accounting previously read and verified before558 fixed checks; this check independently recovers identical namespaced ASTs.",
        "Unique constructor retains inherited exact Entry or original transfer/name-validation/cell-write order, then installs completed version.",
        "Full merge retains builtin union iteration and every ordered input transfer/cell effect; sparse merge is unchanged.",
        "No external use of removed layer/order/history private fields found. Generic Mapping constructor remains original.",
    ],
    "disposition": "No blocker in bounded adapter review. Run original design53 on real311, fresh exact-r010 snapshot with this source overlay, unchanged tests and caps. This is the first production-fitness test, not acceptance.",
    "limits": "v24 retains v22 semantic defects; do not combine with v23, run broad gates or claim integration. If focused floor fails, retain result and diagnose before any expansion.",
}
raw = (json.dumps(report, indent=2) + "\n").encode()
for name, data in {"coordinator-v24-storage-inspection-v1.json": raw,
                   "coordinator-inspect-v24-storage-v1.py": Path(__file__).read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(data)
print(json.dumps({"report_sha256": h(raw), "primitive_definitions_and_constants": len(primitives),
                  "protected_definitions": len(protected), "payload_executed": False}))
