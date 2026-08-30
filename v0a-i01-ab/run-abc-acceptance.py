"""Run only the ADR0485 permitted broader wall after two final CLEAN reviews."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(r"D:\Pontius-handoffs\v0a-i01-ab")
G=r"C:\Program Files\Git\cmd\git.exe"
FLOOR=r"D:\Pontius-tools\py311\Scripts\python.exe"
round_id=sys.argv[1]
assert round_id.startswith('r') and len(round_id)==4 and round_id[1:].isdigit()
packet=ROOT/round_id
candidate=json.loads((packet/'candidate.json').read_text(encoding='utf-8'))
ready=json.loads((packet/'checks/broader-gate-readiness.json').read_text(encoding='utf-8'))
assert ready['candidate']==candidate['commit'] and ready['manifest']==candidate['manifest_sha256']
assert ready['defect_verdicts']==['CLEAN','CLEAN']
for rel,sha in ready['review_sha256'].items():
 assert hashlib.sha256((packet/rel).read_bytes()).hexdigest()==sha
labels=[('status','module:pontius.status_generation',['--check']),('status-tests','tests/test_status_generation.py',[]),('evidence-model','tests/test_evidence_errors_and_model.py',[]),('evidence-manifests','tests/test_evidence_manifests.py',[]),('manifest-generation','tests/test_evidence_manifest_generation.py',[]),('orchestration-import','tests/test_test_orchestration_import_boundary.py',[]),('orchestration-config','tests/test_test_orchestration_configuration.py',[]),('inventory','tests/test_inventory_and_profiles.py',[]),('old-boundary','tests/test_stabilization_boundaries.py',[]),('retained-inventory','tests/test_retained_evidence_inventory.py',[]),('inventory-check','tools/generate_test_inventory.py',['--check']),('boundary','tools/check_stabilization_boundaries.py',[]),('v0a-boundary','tests/test_v0a_boundaries.py',[]),('v0a-hand','tests/test_v0a_hand_replay.py',[]),('v0a-trace','tests/test_v0a_trace.py',[]),('v0a-replay','tests/test_v0a_replay.py',[]),('v0a-faults','tests/test_v0a_contract_faults.py',[])]
results=[]
for slot in ('311','314'):
 label='acceptance-'+round_id+'-'+slot
 env=dict(os.environ)
 env.update(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='core.autocrlf',GIT_CONFIG_VALUE_0='false')
 subprocess.run([FLOOR,'-B','-P',str(ROOT/'snapshot-run-abc.py'),'prepare',label,candidate['commit']],env=env,check=True)
 metadata=ROOT/(label+'-snapshot.json')
 setup=json.loads(metadata.read_text(encoding='utf-8'))
 for rel,sha in setup['source_sha256'].items():
  blob=subprocess.run([G,'-C',setup['snapshot'],'cat-file','blob',candidate['commit']+':'+rel],capture_output=True,check=True).stdout
  assert hashlib.sha256(blob).hexdigest()==sha,rel
 for name,target,args in labels:
  runlabel='acceptance-'+round_id+'-'+name
  print(slot+' '+target+' '+ ' '.join(args)+' START',flush=True)
  proc=subprocess.run([FLOOR,'-B','-P',str(ROOT/'snapshot-run-abc.py'),'run',str(metadata),slot,runlabel,target,*args],capture_output=True)
  receipt=ROOT/'abc-checks'/(runlabel+'-'+slot+'-receipt.json')
  data=json.loads(receipt.read_text(encoding='utf-8'))
  assert data['exit']==proc.returncode and not data['changed_paths']
  assert data['before_sha256']==setup['source_sha256']==data['after_sha256']
  assert hashlib.sha256(Path(data['log']).read_bytes()).hexdigest()==data['sha256']
  results.append({'slot':slot,'target':target,'args':args,'exit':proc.returncode,'receipt':str(receipt),'receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest()})
  print(slot+' '+target+' EXIT '+str(proc.returncode),flush=True)
with (packet/'checks/broader-gate-results.json').open('x',encoding='utf-8',newline='\n') as f:
 json.dump({'candidate':candidate,'scope':'ADR0485 permitted broader CI + five v0a suites; no guarded profile or full scientific population','results':results},f,indent=2);f.write('\n')
sys.exit(0 if all(r['exit']==0 for r in results) else 1)
