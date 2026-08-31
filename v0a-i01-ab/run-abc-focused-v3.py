import sys,json,hashlib,importlib.util,subprocess,re
from pathlib import Path
sys.stdout.reconfigure(line_buffering=True)
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
p=R/'snapshot-run-abc-v2.py'
if sha(p.read_bytes())!='62bf07eb88845dfc30c3820aeb8c899ccfbe8111d811192485e2826a5ecfc20c':raise RuntimeError('harness changed')
spec=importlib.util.spec_from_file_location('focused_snapshot',p);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h);h.require_control_runtime()
meta,msha,slot,label=sys.argv[1:];h.require(re.fullmatch('[a-z0-9-]+',label) is not None,'label')
setup=h.load_setup(meta,msha)
out=R/(label+'-'+slot+'-summary.json')
if out.exists():raise RuntimeError('output exists')
targets=[('tests/test_inventory_and_profiles.py',()),('tests/test_stabilization_boundaries.py',()),('tests/test_v0a_boundaries.py',()),('tests/test_v0a_hand_replay.py',()),('tests/test_v0a_trace.py',()),('tests/test_v0a_replay.py',()),('tests/test_v0a_contract_faults.py',()),('tools/generate_test_inventory.py',('--check',)),('tools/check_stabilization_boundaries.py',())]
results=[]
for i,(target,args) in enumerate(targets,1):
 runlabel=label+'-'+str(i).zfill(2)
 rc=h.run(meta,msha,slot,runlabel,target,*args)
 rp=R/'abc-checks'/(runlabel+'-'+slot+'-receipt.json');r=json.loads(rp.read_text());log=Path(r['log']).read_text()
 count=re.search(r'Ran (\d+) tests? in ([0-9.]+)s',log)
 results.append({'target':target,'args':list(args),'exit':rc,'receipt':str(rp),'receipt_sha256':sha(rp.read_bytes()),'tests':int(count[1]) if count else None,'seconds':float(count[2]) if count else None,'summary':log.splitlines()[-1] if log.splitlines() else ''})
with out.open('x',encoding='utf-8',newline='\n') as f:json.dump({'metadata_sha256':msha,'slot':slot,'source_sha256':setup['source_sha256'],'driver_sha256':sha(Path(__file__).read_bytes()),'results':results},f,indent=2);f.write('\n')
print(json.dumps({'summary':str(out),'all_green':all(r['exit']==0 for r in results)}))
raise SystemExit(0 if all(r['exit']==0 for r in results) else 1)
