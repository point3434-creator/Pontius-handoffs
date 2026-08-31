"""Static-only v31 authoring; no candidate import/execution."""
import ast, difflib, hashlib, json, os, pathlib, subprocess, sys
T=pathlib.Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W=pathlib.Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
BASE=T/"engineer-generator-v25-semantic.py"
OPS=pathlib.Path(__file__).with_suffix(".json")
assert sys.version_info[:3]==(3,11,15) and sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
def read(path):
    for p in (path,*path.parents):
        assert not getattr(p.stat(follow_symlinks=False),"st_file_attributes",0)&0x400,p
    assert path.is_file()
    return path.read_bytes()
def sha(raw): return hashlib.sha256(raw).hexdigest()
def dump(n): return ast.dump(n,include_attributes=False)
base_raw=read(BASE); assert sha(base_raw)=="481098d0be86d27f1664d0705a44a91d50b3a1361280a4e28c82bc366a541853"
base=base_raw.decode(); source=base
assert sha(read(T/"engineer-generator-v25-review-successor-plan-v1.md"))=="56c1b494349ea3b70af3eee2f26d9bf99fab72db1725b5b833b4af187be4ac34"
ops=json.loads(read(OPS))
def region(text,op):
    parent=ast.parse(text)
    if op.get("cls"):parent=next(n for n in parent.body if isinstance(n,ast.ClassDef) and n.name==op["cls"])
    node=parent if op["kind"]=="class_replace_in" else next(n for n in parent.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==op["name"])
    lines=text.splitlines(True); start=min([node.lineno,*[d.lineno for d in getattr(node,"decorator_list",())]])
    return sum(map(len,lines[:start-1])),sum(map(len,lines[:node.end_lineno]))
for i,op in enumerate(ops):
    try:
        kind=op["kind"]
        if kind=="replace":
            assert source.count(op["old"])==1
            source=source.replace(op["old"],op["new"])
        elif kind=="insert_before":
            assert source.count(op["anchor"])==1
            source=source.replace(op["anchor"],op["text"]+op["anchor"])
        else:
            a,b=region(source,op); piece=source[a:b]
            if kind.endswith("_replace_in"):
                count=piece.count(op["old"]); assert count and (op.get("all") or count==1),(count,op["old"])
                piece=piece.replace(op["old"],op["new"]); source=source[:a]+piece+source[b:]
            elif kind in {"function_replace","method_replace"}:source=source[:a]+op["text"]+source[b:]
            elif kind=="method_insert_before":source=source[:a]+op["text"]+source[a:]
            else:raise AssertionError(kind)
        ast.parse(source)
    except Exception as e:raise AssertionError((i,kind,op.get("name"),str(e))) from e
if "--inspect" in sys.argv:
    for name in sys.argv[sys.argv.index("--inspect")+1].split(","):
        node=ast.parse(source)
        for part in name.split("."):node=next(n for n in node.body if getattr(n,"name",None)==part)
        print("INSPECT "+name);print("\n".join(source.splitlines()[node.lineno-1:node.end_lineno]))
    raise SystemExit(0)
tree=ast.parse(source); bt=ast.parse(base)
def nodes(t):return {n.name:n for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))}
old,new=nodes(bt),nodes(tree)
def piece(s,n):
    lines=s.splitlines(True); first=min([n.lineno,*[d.lineno for d in getattr(n,"decorator_list",())]])
    return "".join(lines[first-1:n.end_lineno])
v25proof=json.loads(read(T/"engineer-checks/generator-v25-semantic-static-v1.json"))
storage=v25proof["exact_name_storage_nodes"]
for name in storage:assert piece(base,old[name])==piece(source,new[name]),name
first=min([old[storage[0]].lineno,*[d.lineno for d in old[storage[0]].decorator_list]])
newfirst=min([new[storage[0]].lineno,*[d.lineno for d in new[storage[0]].decorator_list]])
assert "".join(base.splitlines(True)[first-1:old[storage[-1]].end_lineno])=="".join(source.splitlines(True)[newfirst-1:new[storage[-1]].end_lineno])
for name in ("_ExecutionState","_AnalysisBudget"):assert piece(base,old[name])==piece(source,new[name]),name
assert dump(old["_merge_flow_values"].body[0])==dump(new["_merge_flow_values"].body[0])
def ordinary(t):return [dump(n) for n in t.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))]
assert ordinary(bt)==ordinary(tree)
changed=[n for n in old if dump(old[n])!=dump(new[n])]
added=[n for n in new if n not in old]
allowed={"_ordered_flow_roots","_join_member_obligations","_merge_flow_values","_SourceOrderedResolver","_transfer_authority","_AuthorityState"}
assert set(changed)<=allowed,changed
cases=v25proof["frozen_case_pins"]
for name,wanted in cases.items():assert sha(read(T/"tests-checks"/name))==wanted,name
calls=[]
def walk(n,owner=()):
    if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):owner=(*owner,n.name)
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {"_merge_flow_values","_merge_legacy_flow_values"}:
        kw=[x for x in n.keywords if x.arg=="budget"];assert len(kw)==1
        calls.append({"owner":".".join(owner),"line":n.lineno,"callee":n.func.id,"budget":ast.unparse(kw[0].value)})
    for child in ast.iter_child_nodes(n):walk(child,owner)
walk(tree)
methods={}
for cls in changed:
    if isinstance(old[cls],ast.ClassDef):
        a=nodes(old[cls]);b=nodes(new[cls]);methods[cls]=[n for n in b if n not in a or dump(a[n])!=dump(b[n])]
summary={"source_sha256":sha(source.encode()),"bytes":len(source.encode()),"changed":changed,"added":added,"methods":methods,"merge_calls":calls,"ops":len(ops),"no_candidate_execution":True}
print(json.dumps(summary,indent=2))
if "--preview" in sys.argv:
    out=pathlib.Path(__file__).with_name("pontius-v31-preview.py")
    out.write_bytes(source.encode())
if "--issue" in sys.argv:raise AssertionError("issuance logic not enabled until static handoff complete")
