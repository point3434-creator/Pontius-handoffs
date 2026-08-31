from pathlib import Path
import ast,hashlib,json,pprint,sys
R=Path(__file__).resolve().parent;W=Path(r"D:\Pontius-worktrees\codex-v0a-i01-abc")
sha=lambda b:hashlib.sha256(b).hexdigest()
census_path=Path(sys.argv[1]);pin=sys.argv[2];label=sys.argv[3]
assert sha(census_path.read_bytes())==pin
c=json.loads(census_path.read_bytes());p=W/"tests/test_inventory_and_profiles.py";raw=p.read_bytes();text=raw.decode();tree=ast.parse(text)
assert sha(raw)==c['source_corpus']['raw_sha256']['tests/test_inventory_and_profiles.py']
assert sha((W/'tools/generate_test_inventory.py').read_bytes())==c['input_sha256']['tools/generate_test_inventory.py']
cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='CheckedInInventoryTests')
m=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='test_working_discovery_binds_every_entry_and_introduced_id')
lines=text.splitlines(keepends=True); offsets=[0]
for line in lines:offsets.append(offsets[-1]+len(line))
changes=[];replacements=[]
reasons={'dynamic sensitive call result is unresolved','unregistered CuPy call is unresolved','deferred generator consumption is dynamically unresolved'}
for call in ast.walk(m):
 if not(isinstance(call,ast.Call) and isinstance(call.func,ast.Attribute) and call.func.attr=='assertEqual' and len(call.args)==2):continue
 first,target=call.args;field=None;value=None
 if ast.unparse(first)=="review['analysis_census']":field='analysis_census';value=c[field]
 elif ast.unparse(first)=='len(blockers)':field='blocker_count';value=c[field]
 elif isinstance(first,ast.Call) and ast.unparse(first).startswith('Counter('):
  field='blocker_reason_counts';value=c[field];assert isinstance(target,ast.Call) and ast.unparse(target.func)=='Counter';target=target.args[0]
 elif isinstance(first,ast.ListComp):
  strings={n.value for n in ast.walk(first) if isinstance(n,ast.Constant) and type(n.value) is str}
  found=strings & reasons
  if found:assert len(found)==1;field=next(iter(found));value=[tuple(x) for x in c['blocker_locations_by_reason'][field]]
 if field is None:continue
 before=ast.literal_eval(target)
 formatted=pprint.pformat(value,width=100-target.col_offset,sort_dicts=False)
 out=[]
 for i,line in enumerate(formatted.splitlines()):
  rendered=(' '*target.col_offset if i else '')+line
  if len(rendered)>100 and ': ' in rendered:
   key,val=rendered.split(': ',1);indent=len(rendered)-len(rendered.lstrip())
   rendered=key+':\n'+' '*(indent+4)+val
  assert all(len(l)<=100 for l in rendered.splitlines()),repr(rendered)
  out.append(rendered)
 replacement='\n'.join(out)
 start=offsets[target.lineno-1]+target.col_offset;end=offsets[target.end_lineno-1]+target.end_col_offset
 replacements.append((start,end,replacement));changes.append({'field':field,'before':before,'after':value})
assert len(replacements)==6,[x['field'] for x in changes]
for start,end,replacement in sorted(replacements,reverse=True):text=text[:start]+replacement+text[end:]
new=ast.parse(text)
newcls=next(n for n in new.body if isinstance(n,ast.ClassDef) and n.name==cls.name)
newmethod=next(n for n in newcls.body if isinstance(n,ast.FunctionDef) and n.name==m.name)
newcls.body[newcls.body.index(newmethod)]=m
assert ast.dump(new)==ast.dump(tree)
assert '\r' not in text
out=R/(label+'.json');assert not out.exists()
p.write_bytes(text.encode())
with out.open('x',encoding='utf-8',newline='\n') as f:json.dump({'input_census':str(census_path),'input_census_sha256':pin,'before_sha256':sha(raw),'after_sha256':sha(p.read_bytes()),'only_method':m.name,'all_other_module_ast_unchanged':True,'changes':changes},f,indent=2);f.write('\n')
print(json.dumps({'receipt':str(out),'test_sha256':sha(p.read_bytes()),'fields':[x['field'] for x in changes]}))
