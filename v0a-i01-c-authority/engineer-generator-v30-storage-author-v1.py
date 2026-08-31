import ast,copy,difflib,hashlib,json
from pathlib import Path
T=Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W=Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
PRE="b53b905cd20dd97d7d09a3b81f955bf27498a572ce8a6d82e20f007993ab9466"
PLAN="a6fbc28533102f86341daac86cb76761517e2b2770421d29c6b8d94381bdf983"
REVIEW="f397975e37f00ea9512563e91dea9bc89ae7f9dda2ce96ab2f5ed5ba1dc610ad"
sha=lambda b:hashlib.sha256(b).hexdigest()
jd=lambda d:(json.dumps(d,indent=2,sort_keys=True)+"\n").encode()
def pin(name,p):
 b=(T/name).read_bytes();assert sha(b)==p,(name,sha(b));return b
old_bytes=pin("engineer-generator-v29-storage.py",PRE);old=old_bytes.decode()
pin("engineer-v30-enumerate-accounting-plan-v1.md",PLAN)
pin("tests-checks/v29-disabled-join-engineering-review-codex-a-v1.md",REVIEW)
old_account=json.loads(pin("engineer-generator-v29-storage-accounting-v1.json","5074f3509e47d1de642b30f5351dd953997397b4e29a841cc59ae92c6c7d292d"))
old_pres=json.loads(pin("engineer-generator-v29-storage-preservation-v1.json","bcc97e505a42dfb093bc4ada0de3d62d76b83d03b1016319aa7b889f1111a2dc"))
new_names={"disabled_join_input_pair_allocation","disabled_join_input_pair_reference_copies"}
assert not (new_names & set(old_account["categories"]))
needle='                            for index, state in enumerate(states):\n                                join_meter.charge("disabled_join_input_visits", 2)'
added=('                                join_meter.charge("disabled_join_input_pair_allocation")\n'
       '                                join_meter.charge("disabled_join_input_pair_reference_copies", 2)\n')
assert old.count(needle)==1
new=old.replace(needle,needle.replace('                                join_meter.charge',added+'                                join_meter.charge',1))
assert new.count(added)==1
raw=new.encode();source_sha=sha(raw)
assert new.replace(added,"").encode()==old_bytes
oa,na=ast.parse(old),ast.parse(new)
def dump(n):return ast.dump(n,include_attributes=False)
def seg(s,n):return ast.get_source_segment(s,n)
def top(a,name):return next(n for n in a.body if getattr(n,"name",None)==name)
def method(a,c,name):return next(n for n in top(a,c).body if getattr(n,"name",None)==name)
# Remove only the two new expression statements, preserving every other AST node.
class RemoveExactCalls(ast.NodeTransformer):
 def __init__(self):self.removed=[]
 def visit_Expr(self,n):
  c=n.value
  if isinstance(c,ast.Call) and isinstance(c.func,ast.Attribute) and isinstance(c.func.value,ast.Name) and c.func.value.id=="join_meter" and c.func.attr=="charge" and c.args and isinstance(c.args[0],ast.Constant) and c.args[0].value in new_names:
   self.removed.append(dump(n));return None
  return self.generic_visit(n)
remover=RemoveExactCalls();inverse=remover.visit(copy.deepcopy(na))
assert len(remover.removed)==2 and dump(inverse)==dump(oa)
merged=method(na,"_SourceOrderedResolver","_merge_states")
loop=next(n for n in ast.walk(merged) if isinstance(n,ast.For) and isinstance(n.iter,ast.Call) and isinstance(n.iter.func,ast.Name) and n.iter.func.id=="enumerate" and len(n.iter.args)==1 and isinstance(n.iter.args[0],ast.Name) and n.iter.args[0].id=="states")
assert [n.value.args[0].value for n in loop.body[:3]]==["disabled_join_input_pair_allocation","disabled_join_input_pair_reference_copies","disabled_join_input_visits"]
assert len(loop.body[0].value.args)==1
assert isinstance(loop.body[1].value.args[1],ast.Constant) and loop.body[1].value.args[1].value==2
assert isinstance(loop.body[2].value.args[1],ast.Constant) and loop.body[2].value.args[1].value==2
def inventory(a):
 out={}
 class V(ast.NodeVisitor):
  def __init__(self):self.path=[]
  def visit_ClassDef(self,n):self.path.append(n.name);self.generic_visit(n);self.path.pop()
  def visit_FunctionDef(self,n):self.path.append(n.name);self.generic_visit(n);self.path.pop()
  visit_AsyncFunctionDef=visit_FunctionDef
  def visit_Call(self,n):
   if isinstance(n.func,ast.Attribute) and n.func.attr=="charge":
    assert n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str)
    out.setdefault(n.args[0].value,[]).append({"function":".".join(self.path),"line":n.lineno,"units":ast.unparse(n.args[1]) if len(n.args)>1 else "1"})
   self.generic_visit(n)
 V().visit(a);return out
before,after=inventory(oa),inventory(na)
assert set(after)-set(before)==new_names and set(before)<=set(after)
for name,sites in before.items():
 assert [{k:v for k,v in x.items() if k!="line"} for x in sites]==[{k:v for k,v in x.items() if k!="line"} for x in after[name]],name
categories={}
for name,row in old_account["categories"].items():
 value=copy.deepcopy(row);value["source_sites"]=after[name];categories[name]=value
 for k,v in row.items():
  if k!="source_sites":assert categories[name][k]==v
categories["disabled_join_input_pair_allocation"]={
 "metric":"non-P","operation":"One semantic yielded-pair allocation/materialization at the first loop-body boundary, before the existing input visit/guard use; not a fresh CPython heap tuple claim.",
 "origin":"v30 enumerate-pair accounting correction","source_sites":after["disabled_join_input_pair_allocation"]}
categories["disabled_join_input_pair_reference_copies"]={
 "metric":"P","operation":"The yielded pair's two reference copies, separately charged without reassigning the meanings of old iterator or input-visit categories.",
 "origin":"v30 enumerate-pair accounting correction","source_sites":after["disabled_join_input_pair_reference_copies"]}
primitive=[]
for item in old_pres["primitive_definitions_and_constants"]:
 name=item["name"]
 def target(a):
  if item["kind"] in ("FunctionDef","ClassDef"):return top(a,name)
  return next(n for n in a.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
 p,q=target(oa),target(na);assert seg(old,p)==seg(new,q)
 primitive.append({"name":name,"kind":item["kind"],"source_sha256":sha(seg(new,q).encode()),"unchanged_from_v29":True})
assert len(primitive)==47
caps={}
for n in oa.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith("MAXIMUM_ANALYSIS_"):
  name=n.targets[0].id;q=next(x for x in na.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in x.targets))
  assert dump(n)==dump(q);caps[name]=ast.unparse(q.value)
assert len(caps)==5
protected={}
for name in old_pres["protected_definitions"]:
 a,b=top(oa,name),top(na,name);assert seg(old,a)==seg(new,b)
 protected[name]={"source_sha256":sha(seg(new,b).encode()),"AST_sha256":sha(dump(b).encode())}
unchanged_methods=0
for n in top(oa,"_SourceOrderedResolver").body:
 if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!="_merge_states":
  assert seg(old,n)==seg(new,method(na,"_SourceOrderedResolver",n.name));unchanged_methods+=1
w_before={name:sha((W/name).read_bytes()) for name in old_pres["W_after"]}
assert len(w_before)==1761 and w_before==old_pres["W_after"]
assert (T/"engineer-generator-v29-storage.py").read_bytes()==old_bytes
w_after={name:sha((W/name).read_bytes()) for name in w_before};assert w_after==w_before
diff="".join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile="engineer-generator-v29-storage.py",tofile="engineer-generator-v30-storage.py"))
disposition=f"""# Root disposition: v30 enumerate-pair accounting successor

Recorded at the root coordinator's explicit request on2026-08-31. Root read the
independent v29 correctness inspection {REVIEW} and frozen accounting plan {PLAN},
then authorized this create-only source successor. This records root authority;
it is not the author's independent acceptance or a payload authorization.

Exact predecessor v29 {PRE}.
Retained v30 source {source_sha}.
Only the two charge calls in the plan are permitted. At the first enumerate-loop
body boundary, add one semantic pair allocation/materialization and its two
reference copies, before the unchanged input visit/guard use. Do not replace
enumerate, modify the algorithm, reinterpret old categories, change limits, alter
tests/oracles, or amend another source method.

v29's source-accounting finding remains recorded. Its qualified semantic review
does not certify v30 runtime fitness. The new charges follow the adopted semantic
allocation model, not a claim of a fresh CPython heap tuple on every iteration.
Original consumed units are neither reduced nor refunded, including a failing
request. The five caps and existing publication/refusal behavior stay unchanged.

Retain every v29 artifact and W/main unchanged. Root inspects exact source, delta,
accounting and inverse preservation proof before any dispatch. No source payload,
W/main installation or semantic-candidate composition is authorized by this note.
"""
account=copy.deepcopy(old_account)
account["schema"]="pontius-v30-production-name-accounting-v1"
account["source_sha256"]=source_sha
account["predecessor_sha256"]=PRE
account["categories"]=categories
account["new_categories"]=sorted(new_names)
account["v29_new_categories_retained_unchanged"]=old_account["new_categories"]
account["v30_delta_units"]="One allocation unit plus two reference-copy units per reached loop body; failed requests retain the original consume/raise behavior."
account["previous_accounting_sha256"]="5074f3509e47d1de642b30f5351dd953997397b4e29a841cc59ae92c6c7d292d"
# Refresh line locations of old direct consume sites without changing their meaning.
old_merged=method(oa,"_SourceOrderedResolver","_merge_states")
old_calls=[n for n in ast.walk(old_merged) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="consume"]
new_calls=[n for n in ast.walk(merged) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="consume"]
assert [dump(n) for n in old_calls]==[dump(n) for n in new_calls]
line_map={a.lineno:b.lineno for a,b in zip(old_calls,new_calls)}
for site in account["new_direct_original_budget_consumes"]:
 site["line"]=line_map[site["line"]]
pres={"schema":"pontius-v30-storage-preservation-v1","source_sha256":source_sha,
 "predecessor_sha256":PRE,"caps":caps,"protected_definitions":protected,
 "primitive_definitions_and_constants":primitive,"W_before":w_before,"W_after":w_after,
 "all1761_W_paths_unchanged":True,"W_written":False,"source_imported_or_executed":False}
artifacts={
 "engineer-generator-v30-storage.py":raw,
 "engineer-generator-v30-storage-from-v29.diff":diff.encode(),
 "engineer-generator-v30-storage-accounting-v1.json":jd(account),
 "engineer-generator-v30-storage-preservation-v1.json":jd(pres),
 "coordinator-enumerate-accounting-disposition-v1.md":disposition.encode(),
}
proof={"schema":"pontius-v30-storage-static-v1","source_sha256":source_sha,"source_bytes":len(raw),
 "predecessor_sha256":PRE,"approved_plan_sha256":PLAN,"independent_v29_review_sha256":REVIEW,
 "only_two_Expr_Call_statements_inserted":True,"inverse_bytes_recover_v29":True,
 "inverse_AST_recovers_v29":True,"old_name_charge_categories_count":len(before),
 "old_name_category_meanings_and_call_units_unchanged":True,
 "old_direct_consume_calls_AST_unchanged":True,
 "new_charge_sites":{k:after[k] for k in sorted(new_names)},
 "all47_primitives_source_exact":True,"all5caps_unchanged":True,
 "unchanged_other_SOR_methods":unchanged_methods,"all1761_W_paths_unchanged":True,
 "loop_structure_unchanged":True,"source_parsed_only":True,
 "source_imported_or_executed":False,"payload_executed":False,"W_written":False,
 "artifacts":{name:sha(data) for name,data in artifacts.items()},
 "limits":["Static authoring proof only. No analyzer, fixture, test or oracle payload executed.",
 "The two calls close the recorded semantic-accounting omission; runtime fitness remains unmeasured.",
 "No previous v29/original test result is relabeled by this successor."]}
artifacts["engineer-generator-v30-storage-static-v1.json"]=jd(proof)
handoff=f"""# v30 storage handoff: two accounting calls, unexecuted

Source engineer-generator-v30-storage.py SHA256 {source_sha}, {len(raw)} bytes.
Exact predecessor v29 {PRE}.
Only two charge calls are inserted at{loop.body[0].lineno}-{loop.body[1].lineno},
before the existing enumerate input visit/guard use. No enumerate, algorithm,
test, oracle, cap, existing category meaning or existing charge units changed.

The exact inverse recovers every v29 byte and AST. All47 primitives, all five
analysis caps, all{unchanged_methods} other SOR methods and all1761 W tracked bytes
are preserved. All{len(before)} old named categories retain their meanings and
source call units; allocation1/non-P and reference copies2/P are added explicitly.
The semantic-work model does not claim a new physical CPython tuple each iteration.

Root authorization, the approved plan, the qualified independent v29 review and
the retained accounting finding are bound in the source disposition/static proof.
No source/test/oracle payload, W/main install, or semantic composition occurred.
Root source inspection precedes dispatch; no runtime-success claim is made.
"""
artifacts["engineer-generator-v30-storage-handoff-v1.md"]=handoff.encode()
for name in artifacts:assert not (T/name).exists(),"create-only path exists: "+name
for name,data in artifacts.items():
 with (T/name).open("xb") as f:f.write(data)
 assert (T/name).read_bytes()==data
print(json.dumps({"source_sha256":source_sha,"source_bytes":len(raw),
 "inserted_lines":[loop.body[0].lineno,loop.body[1].lineno],
 "old_categories":len(before),"new_categories":sorted(new_names),
 "files":{name:sha(data) for name,data in artifacts.items()}},indent=2))
