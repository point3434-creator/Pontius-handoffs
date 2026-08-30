from pathlib import Path
import os,subprocess,hashlib,json,uuid,tempfile,difflib
repo=Path(r"D:\Pontius")
packet=Path(r"D:\Pontius-handoffs\coverage-guidance\r002")
git=r"C:\Program Files\Git\cmd\git.exe"
def g(*args,env=None,input=None):
    return subprocess.run([git,"-C",str(repo),*args],env=env,input=input,capture_output=True,check=True).stdout
def h(b):return hashlib.sha256(b).hexdigest()
base=g("rev-parse","HEAD").decode().strip()
assert base=="d1ed3cbda6107d61ea8e77133871720af04970cd"
before=(packet/"checks/workflow-before.txt").read_bytes()
working=(repo/"docs/workflow.md").read_bytes()
assert h(before)=="231d99e785d5245647636ad7db15b5b28568590da8d20f06f1135e27592bf92d"
assert h(working)=="d9de38ede87fb619b3045a60ee7fab137ae23ba3b580c0a6d6b3ca14e567a170"
assert h((repo/"CLAUDE.md").read_bytes())=="af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76"
text=working.decode()
d=text.index("**Design verdict (required).**");e=text.index("### Stage 4",d)
design=text[d:e]
t=text.index("Also state one required design verdict");u=text.index("On a fix round,",t)
template=text[t:u]
assert design in before.decode() and template in before.decode()
projected=text.replace(design,"").replace(template,"").replace("severity-ordered, one entry per finding, design verdict stated separately.","severity-ordered, one entry per finding.")
blob=projected.encode()
assert b"\r" not in blob and blob.endswith(b"\n") and not blob.endswith(b"\n\n")
for name,data in [("workflow-working-after.txt",working),("workflow-candidate.txt",blob)]:
    with (packet/"checks"/name).open("xb") as f:f.write(data)
index=repo/".git/index";index_before=h(index.read_bytes())
idx=Path(tempfile.gettempdir()).resolve()/("pontius-coverage-freeze-"+uuid.uuid4().hex+".idx")
assert idx.parent==Path(tempfile.gettempdir()).resolve() and not idx.exists()
env=os.environ.copy();env["GIT_INDEX_FILE"]=str(idx)
ref="refs/heads/review/coverage-guidance/r002"
try:
    g("read-tree",base,env=env)
    oid=g("hash-object","-w","--stdin",input=blob).decode().strip()
    g("update-index","--add","--cacheinfo","100644,"+oid+",docs/workflow.md",env=env)
    tree=g("write-tree",env=env).decode().strip()
    commit=g("commit-tree",tree,"-p",base,"-m","Review coverage guidance r002 (snapshot only)",env=env).decode().strip()
finally:
    idx.unlink(missing_ok=True)
assert h(index.read_bytes())==index_before
g("update-ref",ref,commit,"0"*40)
assert g("diff-tree","--no-commit-id","--name-only","-r",base,commit).decode().splitlines()==["docs/workflow.md"]
assert g("cat-file","blob",commit+":docs/workflow.md")==blob
g("diff","--check",base,commit)
rows=(h(blob)+"  docs/workflow.md\n").encode();manifest=h(rows)
with (packet/"manifest.sha256").open("xb") as f:f.write(rows)
data=dict(schema_version="pontius-handoff-candidate-v1",task_id="coverage-guidance",round="r002",ref=ref,commit=commit,base=base,tree=tree,manifest_sha256=manifest,date="2026-08-30")
with (packet/"candidate.json").open("x",encoding="utf-8",newline="\n") as f:json.dump(data,f,indent=2);f.write("\n")
record=dict(candidate=data,working_before_sha256=h(before),working_after_sha256=h(working),candidate_file_sha256=h(blob),claude_md_preserved=True,primary_index_preserved=True,primary_head_unchanged=True,pending_design_blocks_preserved=True,scope="Coverage guidance only; pending mandatory-design additions excluded from candidate and unchanged in working file.")
with (packet/"checks/freeze-verification.json").open("x",encoding="utf-8",newline="\n") as f:json.dump(record,f,indent=2);f.write("\n")
with (packet/"checks/working-refinement.patch").open("x",encoding="utf-8",newline="\n") as f:f.write("".join(difflib.unified_diff(before.decode().splitlines(keepends=True),working.decode().splitlines(keepends=True),fromfile="workflow-before",tofile="workflow-after")))
print(json.dumps(data,indent=2))
