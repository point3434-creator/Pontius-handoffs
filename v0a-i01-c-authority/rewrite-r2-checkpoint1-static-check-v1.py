import sys
assert sys.version_info[:3]==(3,11,15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.safe_path
import ast,copy,difflib,hashlib,json,pathlib
T=pathlib.Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
raw=(T/"rewrite-r1-task5-source-v2.py").read_bytes()
assert hashlib.sha256(raw).hexdigest()=="c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f"
edits_path=T/"rewrite-r2-checkpoint1-edits-v1.json"
ops=json.loads(edits_path.read_bytes())
before=raw.decode();after=before
for edit in ops:
 assert after.count(edit["old"])==1,edit["label"]
 after=after.replace(edit["old"],edit["new"])
retained=T/"rewrite-r2-checkpoint1-source-v1.py"
assert retained.read_bytes()==after.encode()
assert hashlib.sha256(retained.read_bytes()).hexdigest()=="41b4de563da886a7c674d49b25acd4332ba208906b403ec244d1a4aea856ee05"
base=ast.parse(before,type_comments=True);candidate=ast.parse(after,type_comments=True)
def key(n):
 if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)):return n.name
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):return n.targets[0].id
 return None
old={key(n):n for n in base.body if key(n)}
new={key(n):n for n in candidate.body if key(n)}
expected_changed={"_CChoice","_CValue","_c_value_key","_c_choice","_c_truth","_c_eval","_c_statement"}
expected_new={"_CBooleanUnknown","_c_identity_compare"}
assert set(new)-set(old)==expected_new
changed={k for k in old if ast.dump(old[k],include_attributes=False)!=ast.dump(new[k],include_attributes=False)}
assert changed==expected_changed,changed
reversed_text=after
for edit in reversed(ops):
 assert reversed_text.count(edit["new"])==1,edit["label"]
 reversed_text=reversed_text.replace(edit["new"],edit["old"])
assert reversed_text==before
for name in ["_AnalysisBudget","_bind_helper_arguments","_c_binding_read","_COutcome","_CContext","_CCallObservation","_c_out","_c_follow","_c_call","_c_invoke","_c_fail","_c_join","_c_fork","_c_snapshot","_c_identity","_c_state","_c_copy_dict","_c_own_cells","_c_own_objects","_c_new_activation","_c_cell_read","_c_cell_write","_c_object_read","_c_object_write","_c_new_object"]:
 assert ast.get_source_segment(before,old[name])==ast.get_source_segment(after,new[name]),name
opcodes=difflib.SequenceMatcher(a=before.splitlines(keepends=True),b=after.splitlines(keepends=True),autojunk=False).get_opcodes()
plus=sum(j2-j1 for tag,i1,i2,j1,j2 in opcodes if tag in {"insert","replace"})
minus=sum(i2-i1 for tag,i1,i2,j1,j2 in opcodes if tag in {"delete","replace"})
assert plus+minus<=1500
lines=after.splitlines()
for tag,i1,i2,j1,j2 in opcodes:
 if tag in {"insert","replace"}:
  for num in range(j1,j2):
   assert len(lines[num])<=100,(num+1,len(lines[num]),lines[num])
   assert lines[num].rstrip()==lines[num]
assert "\r" not in after and not after.startswith("\ufeff")
proof={"source_sha256":hashlib.sha256(after.encode()).hexdigest(),"added":plus,"deleted":minus,"total":plus+minus,"changed_nodes":sorted(changed),"added_nodes":sorted(expected_new),"reverse_to_c8fc_exact":True,"unchanged_protected_core_nodes":True,"added_line_style":True,"syntax_only":True,"checker_writes":False}
print(json.dumps(proof,indent=2))
