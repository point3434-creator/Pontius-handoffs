from pathlib import Path
import hashlib,json,re,subprocess
root=Path(r"D:\Pontius-handoffs")
source=Path(r"D:\Pontius")
git=r"C:\Program Files\Git\cmd\git.exe"
def g(repo,*args):return subprocess.check_output([git,"-C",str(repo),*args])
def h(b):return hashlib.sha256(b).hexdigest()
candidate="0207430a37e1e5b31c8da8da7aa57da1bc5c88ee"
manifest="ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef"
packet=root/"v0a-i01-impl/r004"
assert g(source,"rev-parse","refs/heads/review/v0a-i01-impl/r004").decode().strip()==candidate
base=g(source,"rev-parse",candidate+"^").decode().strip()
assert base=="b357d333fc2393b7fc7dcf31f30c86616208c817"
names=g(source,"diff","--name-only",base,candidate).decode().splitlines()
rows=[]
for name in names:rows.append((h(g(source,"show",candidate+":"+name))+"  "+name+"\n").encode())
derived=b"".join(sorted(rows))
assert derived==(packet/"manifest.sha256").read_bytes()
assert h(derived)==manifest
snaps=json.loads((packet/"checks/codex-snapshots.json").read_text())["snapshots"]
for snap in snaps.values():
    assert g(snap,"rev-parse","HEAD").decode().strip()==candidate
    assert not g(snap,"status","--porcelain").strip()
for slot in ("311","314"):
    receipt=json.loads((packet/f"checks/coordinator-{slot}-receipt.json").read_text())
    for item in receipt["results"]:
        data=Path(item["log"]).read_bytes()
        assert h(data)==item["sha256"] and item["exit"]==0
    for suite,n in [("hand_replay",35),("trace",25),("replay",31),("contract_faults",22)]:
        text=(packet/f"checks/coordinator-{slot}-{suite}.txt").read_text()
        assert re.search(r"Ran "+str(n)+r" tests? in ",text) and re.search(r"\nOK\s*$",text)
    obs=json.loads((packet/f"checks/coordinator-{slot}-probe.txt").read_text().splitlines()[-1])["observations"]
    sweeps=[v for v in obs if v["probe"]=="all_observation_faults"]
    assert sum(v["count"] for v in sweeps)==628
    assert all(not v["failures"] for v in sweeps)
    writer=[v for v in obs if v["probe"]=="real_trace_refusal"]
    assert len(writer)==6 and writer[0]["reason"] is None and writer[0]["secondary"]==["trace_write_failed"]
    for v in writer[-2:]:assert v["reason"]=="clock_invalid" and v["secondary"]==["trace_write_failed"]
    abort=json.loads((packet/f"checks/coordinator-{slot}-abort.txt").read_text().splitlines()[-1])["observations"]
    assert len(abort)==57
    reds=[v for v in abort if v.get("fault_at")==16]
    assert len(reds)==3 and all(v["reason"]=="event_order" and v["secondary"]==[] and v["retained"]==[] for v in reds)
for label in ("probe","abort"):
    a=json.loads((packet/f"checks/coordinator-311-{label}.txt").read_text().splitlines()[-1])
    b=json.loads((packet/f"checks/coordinator-314-{label}.txt").read_text().splitlines()[-1])
    assert a==b
assert g(source,"rev-parse","HEAD").decode().strip()=="d1ed3cbda6107d61ea8e77133871720af04970cd"
assert h((source/"CLAUDE.md").read_bytes())=="af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76"
assert h((source/"docs/workflow.md").read_bytes())=="46fd7af39c330cea8086d49a5d92a14fc7874ed781b2269084f8b1f9c947f3b7"
# Stage verification: every newly staged r004 artifact must preserve issued bytes.
staged=g(root,"diff","--cached","--name-only").decode().splitlines()
for name in staged:
    if name.startswith("v0a-i01-impl/r004/"):
        assert g(root,"show",":"+name)==(root/name).read_bytes(),name+" staging changed issued bytes"
print(json.dumps(dict(candidate=candidate,manifest=manifest,manifest_rows=len(names),snapshots_clean=len(snaps),focused_per_slot=113,clock_schedules_per_slot=628,abort_fault_schedules_per_slot=56,writer_schedules_per_slot=6,observations_match_across_slots=True,source_changes_preserved=True,staged_paths=len(staged),all_new_r004_blobs_byte_exact=True),indent=2))

