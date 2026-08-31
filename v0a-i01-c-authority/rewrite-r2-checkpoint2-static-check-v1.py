import sys
assert sys.implementation.name == "cpython" and sys.version_info[:3] == (3,11,15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.safe_path
from pathlib import Path
import ast
import difflib
import hashlib
import json
T=Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
before=(T/"rewrite-r2-checkpoint1-source-v1.py").read_bytes()
r1=(T/"rewrite-r1-task5-source-v2.py").read_bytes()
assert hashlib.sha256(before).hexdigest()=="41b4de563da886a7c674d49b25acd4332ba208906b403ec244d1a4aea856ee05"
assert hashlib.sha256(r1).hexdigest()=="c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f"
ops=json.loads((T/"rewrite-r2-checkpoint2-edits-v1.json").read_bytes())
text=before.decode()
for index,op in enumerate(ops):
    assert text.count(op["old"])==1,(index,text.count(op["old"]),op["old"][:80])
    text=text.replace(op["old"],op["new"],1)
after=text.encode()
retained=(T/"rewrite-r2-checkpoint2-source-v1.py").read_bytes()
assert hashlib.sha256(retained).hexdigest()=="7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d"
assert after==retained
a,b=ast.parse(before),ast.parse(after)
reversed_text=text
for op in reversed(ops):
    assert reversed_text.count(op["new"])==1
    reversed_text=reversed_text.replace(op["new"],op["old"],1)
assert reversed_text.encode()==before
def named(tree):
    result={}
    for node in tree.body:
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
            result[node.name]=node
        elif isinstance(node,(ast.Assign,ast.AnnAssign)):
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target,ast.Name): result[target.id]=node
    return result
old,new=named(a),named(b)
changed=[name for name in old if name in new and ast.dump(old[name])!=ast.dump(new[name])]
added=[name for name in new if name not in old]
removed=[name for name in old if name not in new]
def delta(base):
    operations=difflib.SequenceMatcher(a=base.splitlines(keepends=True),b=after.splitlines(keepends=True),autojunk=False).get_opcodes()
    plus=sum(j2-j1 for tag,i1,i2,j1,j2 in operations if tag in {"replace","insert"})
    minus=sum(i2-i1 for tag,i1,i2,j1,j2 in operations if tag in {"replace","delete"})
    return {"added":plus,"deleted":minus,"total":plus+minus}
assert delta(r1)["total"]<=1500
assert not removed
preserved = ["_AnalysisBudget","_bind_helper_arguments","_c_binding_read","_CContext",
"_c_identity_compare","_c_truth","_c_fork","_c_snapshot","_c_join","_c_new_activation",
"_c_cell_write","_c_object_write","_c_statements","_c_eval_many","_c_store","_c_scope",
"_c_construct_class","_c_construct_function","_c_sink","_c_emit_sink","_process_review_rows"]
for name in preserved:
    assert ast.get_source_segment(before.decode(),old[name])==ast.get_source_segment(text,new[name]),name
changes=difflib.SequenceMatcher(a=before.decode().splitlines(),b=text.splitlines(),autojunk=False).get_opcodes()
style=[]
for tag,i1,i2,j1,j2 in changes:
    if tag in {"replace","insert"}:
        for index,line in enumerate(text.splitlines()[j1:j2],j1+1):
            if len(line)>100 or line.rstrip()!=line: style.append({"line":index,"length":len(line),"text":line})
assert not style,style
assert b"\r" not in after and not after.startswith(b"\xef\xbb\xbf")
def call_rows(tree, targets):
    rows=[]
    class Scan(ast.NodeVisitor):
        def __init__(self): self.owners=[]
        def visit_FunctionDef(self,node):
            self.owners.append(node.name); self.generic_visit(node); self.owners.pop()
        def visit_Call(self,node):
            if isinstance(node.func,ast.Name) and node.func.id in targets:
                rows.append({"owner":".".join(self.owners),"line":node.lineno,
                             "target":node.func.id,"call":ast.unparse(node)})
            self.generic_visit(node)
    Scan().visit(tree)
    return rows
targets={"_COutcome","_CContext","_CCallObservation","_c_out","_CExceptionType",
         "_CException","_CExceptionOrigin","_c_raise_known"}
census=call_rows(b,targets)
assert [row["owner"] for row in census if row["target"]=="_COutcome"]==["_c_out"]
assert [row["owner"] for row in census if row["target"]=="_CExceptionType"]==["_c_read_name"]
assert [row["owner"] for row in census if row["target"]=="_CException"]==["_c_invoke"]
assert [row["owner"] for row in census if row["target"]=="_CExceptionOrigin"]==["_c_raise_known"]
assert [row["owner"] for row in census if row["target"]=="_c_raise_known"]==["_c_statement"]
fail_calls=[n for n in ast.walk(new["_c_fail"]) if isinstance(n,ast.Call)
            and isinstance(n.func,ast.Name) and n.func.id=="_c_out"]
assert len(fail_calls)==1
fail_kw={k.arg:ast.unparse(k.value) for k in fail_calls[0].keywords}
assert fail_kw.get("control")=="'refused'" and "exception" not in fail_kw
for owner in ("_c_follow","_c_call"):
    for call in ast.walk(new[owner]):
        if isinstance(call,ast.Call) and isinstance(call.func,ast.Name) and call.func.id=="_c_out":
            supplied={k.arg for k in call.keywords}
            assert {"control","exception","exception_value","exception_origin","explicit",
                    "excluded_handlers","issues","trace"} <= supplied
def legacy_tags(tree):
    rows=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=="_c_fail":
            if any(k.arg=="exception" for k in node.keywords):
                rows.append(ast.dump(node,include_attributes=False))
    return rows
assert len(legacy_tags(a))==6 and legacy_tags(a)==legacy_tags(b)
assert not any(isinstance(n,ast.Attribute) and n.attr=="completed"
               for n in ast.walk(new["_c_review_outcomes"]))
assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="_CIssue"
               for n in ast.walk(new["_c_raise_known"]))
summaries=[n.args[0] for n in ast.walk(new["_c_call"])
           if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
           and isinstance(n.func.value,ast.Name) and n.func.value.id=="summaries"
           and n.func.attr=="append"]
assert len(summaries)==1 and isinstance(summaries[0],ast.Tuple) and len(summaries[0].elts)==9
print(json.dumps({"source_sha256":hashlib.sha256(after).hexdigest(),"bytes":len(after),
"checkpoint2":delta(before),"cumulative_r2":delta(r1),"changed_nodes":changed,
"added_nodes":added,"preserved_core":preserved,"reverse_exact":True,
"style":True,"candidate_imported":False,"payload_executed":False,
"outcome_census":census,"legacy_tagged_failures":6,"all_legacy_failures_refused":True,
"completion_tuple_fields":9,"proof_producers_unique":True,"historical_completed_not_terminal":True},indent=2))
