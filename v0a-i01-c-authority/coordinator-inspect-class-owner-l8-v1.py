"""Static root inspection: the sensitive fixtures are never executed here."""
from pathlib import Path
import ast
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
def h(raw):
    return hashlib.sha256(raw).hexdigest()
def dump(node):
    return ast.dump(node, include_attributes=False)
pins = {
    "class-owner-late-store-cases-v1.json": "08fce0e37eaeb24192c4f227677d7625097748ccb2cbc79470df4699718a9b47",
    "class-owner-late-store-spec-v1.md": "d122e974986d3022b2a95a531b8ca7c92a25dd845b2dc006983bd43a68a205a1",
    "class-owner-late-store-probe-v1.py": "6fa50f3268c4e672e03819adde462d5a044f00dfa7b849b0d273450f14ffcf22",
    "class-owner-late-store-control-v1.py": "1a1a0483b118e41de5e343c6dff11e8cc577928fd37daeb0c7dd0b9a5aeb7b1c",
    "class-comprehension-extension-probe-v2.py": "231bcddb04eb5f3f93135c46bc03f1ed6275195949f4189a700d2f0eb3571426",
    "class-comprehension-extension-control-v2.py": "34c16309d974e40909bc352d509308b19d2fa4fd42f06386d27430fcf07526e2",
}
raws = {name: (C / name).read_bytes() for name in pins}
assert {name: h(raw) for name, raw in raws.items()} == pins
changes = {}
for kind in ("probe", "control"):
    trees = [ast.parse(raws[name]) for name in (
        f"class-comprehension-extension-{kind}-v2.py",
        f"class-owner-late-store-{kind}-v1.py")]
    for tree in trees:
        compile(tree, "static-only", "exec")
    old, new = [{n.name: n for n in tree.body if isinstance(n, (ast.ClassDef, ast.FunctionDef))} for tree in trees]
    assert old.keys() == new.keys()
    changes[kind] = sorted(name for name in old if dump(old[name]) != dump(new[name]))
    assert changes[kind] == (["load_pack", "main", "oracle"] if kind == "probe" else ["main", "validate_result"])
pack = json.loads(raws["class-owner-late-store-cases-v1.json"])
assert pack["classifications"] == {"refuse": 4, "clean": 4}
assert type(pack["planned_cases"]) is int and pack["planned_cases"] == pack["planned_projections"] == len(pack["cases"]) == 8
old_count = 0
for name, item in pack["preserved_old_case_packs"].items():
    raw = (C / name).read_bytes()
    assert h(raw) == item["sha256"] and len(json.loads(raw)["cases"]) == item["cases"]
    old_count += item["cases"]
assert old_count == 44

class ModelEvents(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id == "Model":
            node.id = "ReviewTests"
        return node
    def visit_Expr(self, node):
        call = node.value
        if (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                and isinstance(call.func.value, ast.Name) and call.func.value.id == "_events"
                and call.func.attr == "append"):
            assert len(call.args) == 1 and isinstance(call.args[0], ast.Constant) and type(call.args[0].value) is str and not call.keywords
            return None
        return self.generic_visit(node)

checked_cases = []
for i, case in enumerate(pack["cases"], 1):
    assert case["schedule_id"] == f"L{i:02d}"
    assert case["classification"] == ("refuse" if i % 2 else "clean")
    assert h(case["source"].encode()) == case["source_sha256"]
    assert h(case["oracle_source"].encode()) == case["oracle_sha256"]
    source, model = ast.parse(case["source"]), ast.parse(case["oracle_source"])
    assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(model))
    forbidden = {"subprocess", "sys", "os", "pontius", "exec", "eval", "compile", "open", "__import__"}
    assert not any(isinstance(n, ast.Name) and n.id in forbidden for n in ast.walk(model))
    for call in (n for n in ast.walk(model) if isinstance(n, ast.Call)):
        assert ast.unparse(call.func) in {"_events.append", "read", "captured", "self._launch", "tuple"}
    sc, = [n for n in source.body if isinstance(n, ast.ClassDef) and n.name == "ReviewTests"]
    mc, = [n for n in model.body if isinstance(n, ast.ClassDef) and n.name == "Model"]
    sm, = [n for n in sc.body if isinstance(n, ast.FunctionDef) and n.name == "test_static"]
    mm, = [n for n in mc.body if isinstance(n, ast.FunctionDef) and n.name == "test_static"]
    assert dump(sm) == dump(ModelEvents().visit(mm)), case["id"]
    assert [dump(n) for n in source.body if isinstance(n, ast.ClassDef) and n.name == "Bare"] == [dump(n) for n in model.body if isinstance(n, ast.ClassDef) and n.name == "Bare"]
    sink, = [n for n in mc.body if isinstance(n, ast.FunctionDef) and n.name == "_launch"]
    expected_sink = ast.parse('@staticmethod\ndef _launch(module="fixed"):\n    _events.append("sink")\n    return module\n').body[0]
    assert dump(sink) == dump(expected_sink)
    assert not set(case["expected"]["trace"]) & set(case["unreachable_events"])
    assert case["expected"]["result"] == ("TypeError" if i % 2 else "fixed")
    assert case["required_argv"] == (None if i % 2 else [["-m", "fixed"]])
    # The untransformed original model is only compiled, never called.
    compile(case["oracle_source"], "static-only-model", "exec")
    checked_cases.append(case["id"])
for index in (0, 2, 4):
    unsafe, dormant = pack["cases"][index:index + 2]
    assert unsafe["source"].replace("if True:", "if False:") == dormant["source"]
probe = ast.parse(raws["class-owner-late-store-probe-v1.py"])
summary, = [n for n in ast.walk(probe) if isinstance(n, ast.Dict)
            and any(isinstance(k, ast.Constant) and k.value == "class_owner_late_store_summary" for k in n.keys)]
fields = {k.value: v for k, v in zip(summary.keys, summary.values) if isinstance(k, ast.Constant)}
assert all(isinstance(fields[k], ast.Constant) and type(fields[k].value) is int and fields[k].value == 8
           for k in ("planned_cases", "case_count", "projections"))
report = {
    "schema": "coordinator-class-owner-l8-inspection-v1", "pins": pins,
    "changed_functions": changes, "checked_cases": checked_cases,
    "old_case_count_rehashed": old_count, "source_model_ast_correspondence": 8,
    "payload_executed": False,
    "manual_review": [
        "Read all eight sensitive source strings only as text/AST, all harmless Models, complete spec and both full R8 harness deltas.",
        "Aliases predate the store. Local unsafe/dormant pairs differ only by literal consumption guard; module-origin control deliberately stores scalar0.",
        "Sink body and all Model call forms are harmless. Independent real execution will check fixed traces before invoking the public analyzer on unexecuted sensitive bytes.",
        "Existing identity-before-imports, snapshot custody, original caps, actual311-first and bounded direct-child watchdog retained. No private analyzer observer added."
    ],
    "disposition": "Authorize root-owned serialized v23 diagnostic311, then same-candidate314 only after complete/intact floor evidence. Semantic RED may replicate; no infrastructure failure may. No source edit or integration."
}
raw = (json.dumps(report, indent=2) + "\n").encode()
for name, data in {"coordinator-class-owner-l8-inspection-v1.json": raw,
                   "coordinator-inspect-class-owner-l8-v1.py": Path(__file__).read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(data)
print(json.dumps({"report_sha256": h(raw), "new_cases": 8, "old_cases_rehashed": old_count, "payload_executed": False}))
