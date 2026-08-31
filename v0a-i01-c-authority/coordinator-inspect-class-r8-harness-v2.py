"""Root source-only inspection of eight independent class regression witnesses."""
from pathlib import Path
import ast
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
h = lambda raw: hashlib.sha256(raw).hexdigest()
pins = {
    "class-comprehension-extension-cases-v1.json": "eb5551c054fc89da28fd2e4db433f56f7a3dbbd4cdb70509070a89fe362c74fd",
    "class-comprehension-extension-spec-v1.md": "ed292bcf0207aad474e8293cf055c17de6409b9d851f95a8b8225d4375848dc6",
    "class-comprehension-extension-probe-v2.py": "231bcddb04eb5f3f93135c46bc03f1ed6275195949f4189a700d2f0eb3571426",
    "class-comprehension-extension-control-v2.py": "34c16309d974e40909bc352d509308b19d2fa4fd42f06386d27430fcf07526e2",
    "class-comprehension-boundary-probe-v1.py": "b0232750b89fba7939a093e81e9e4b8a183d23371f6464eaa8d3443bedf49138",
    "class-comprehension-boundary-control-v1.py": "775157055e5a9b6234307ef552536a25bb6049fd76e001e352fc954eac258eba",
}
raws = {name: (C / name).read_bytes() for name in pins}
assert {name: h(raw) for name, raw in raws.items()} == pins
dump = lambda node: ast.dump(node, include_attributes=False)
def defs(raw):
    tree = ast.parse(raw)
    compile(tree, "static-only", "exec")
    return {node.name: node for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef))}
changes = {}
for kind in ("probe", "control"):
    old = defs(raws[f"class-comprehension-boundary-{kind}-v1.py"])
    new = defs(raws[f"class-comprehension-extension-{kind}-v2.py"])
    assert old.keys() == new.keys()
    changes[kind] = sorted(name for name in old if dump(old[name]) != dump(new[name]))
    assert changes[kind] == (["load_pack", "main", "oracle"] if kind == "probe" else ["main", "validate_result"])
pack = json.loads(raws["class-comprehension-extension-cases-v1.json"])
assert pack["classifications"] == {"refuse": 4, "clean": 3, "permitted-refusal": 1}
assert len(pack["cases"]) == 8
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
            return None
        return self.generic_visit(node)
for case in pack["cases"]:
    assert h(case["source"].encode()) == case["source_sha256"]
    assert h(case["oracle_source"].encode()) == case["oracle_sha256"]
    source = ast.parse(case["source"])
    model = ast.parse(case["oracle_source"])
    assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(model))
    sc, = [n for n in source.body if isinstance(n, ast.ClassDef)]
    mc, = [n for n in model.body if isinstance(n, ast.ClassDef)]
    sm, = [n for n in sc.body if isinstance(n, ast.FunctionDef) and n.name == "test_static"]
    mm, = [n for n in mc.body if isinstance(n, ast.FunctionDef) and n.name == "test_static"]
    assert dump(sm) == dump(ModelEvents().visit(mm)), case["id"]
    assert [dump(n) for n in sc.body if isinstance(n, ast.Assign)] == [dump(n) for n in mc.body if isinstance(n, ast.Assign)]
probe = ast.parse(raws["class-comprehension-extension-probe-v2.py"])
summary, = [n for n in ast.walk(probe) if isinstance(n, ast.Dict)
            and any(isinstance(k, ast.Constant) and k.value == "class_comprehension_extension_summary" for k in n.keys)]
fields = {k.value: v for k, v in zip(summary.keys, summary.values) if isinstance(k, ast.Constant)}
assert all(isinstance(fields[k], ast.Constant) and type(fields[k].value) is int and fields[k].value == 8
           for k in ("planned_cases", "case_count", "projections"))
report = {"schema": "coordinator-class-r8-harness-inspection-v2", "pins": pins,
          "changed_functions": changes, "source_model_control_correspondence": 8,
          "schema_summary_count_fields_exact": True, "payload_executed": False,
          "manual_review": [
              "Read all8 sources/independent Models/spec and completecomp6-to-v1 plusv1-to-v2 harness deltas.",
              "Root caught stale projections6 in unexecutedv1;v2 fixes it and exacttypes without changing any case expectation.",
              "Model adds only harmless list/NameError builtins; sensitive source stays AST-only.",
              "Existing fresh snapshot,60s directchildwatchdog,actual311-first,fullmanifest/input/output/floorreplay rules unchanged.",
          ],
          "disposition": "Dispatch frozenv23 on311 first to reproduce the three source concerns. Samecandidate314 only aftercomplete/intactfloor; diagnosticsemanticRED allowed. No candidate edit authorized here."}
raw = (json.dumps(report, indent=2) + "\n").encode()
for name, data in {"coordinator-class-r8-harness-inspection-v2.json": raw,
                   "coordinator-inspect-class-r8-harness-v2.py": Path(__file__).read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(data)
print(json.dumps({"report_sha256": h(raw), "cases": 8, "payload_executed": False}))
