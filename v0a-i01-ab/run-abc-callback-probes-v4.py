import sys,json,hashlib,importlib.util,subprocess,re
from pathlib import Path
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
hp=R/'snapshot-run-abc-v2.py'
if sha(hp.read_bytes())!='62bf07eb88845dfc30c3820aeb8c899ccfbe8111d811192485e2826a5ecfc20c':raise RuntimeError('harness differs')
spec=importlib.util.spec_from_file_location('callback_snapshot',hp)
h=importlib.util.module_from_spec(spec);sys.modules[spec.name]=h;spec.loader.exec_module(h)
h.require_control_runtime()
meta,msha,slot,label=sys.argv[1:]
h.require(re.fullmatch('[a-z0-9-]+',label) is not None,'label')
s=h.load_setup(meta,msha);snap=Path(s['snapshot']);exe,version=h.SLOTS[slot]
payloads=[
 ('closure','coordinator-closure-escape-probe.py','8d1aec927fcc0875724788c1340c14c0fdc83ccd3489f356d38d4b447475808e'),
 ('metamorphic','coordinator-provenance-metamorphic.py',None),
 ('forwarding','codex-a-probe-forwarding.py','c56e1a8aae327d2f9c1fa25ecbd58a38f5074abc37e107b61ad5fa360e16ff3e'),
]
metapin=json.loads((R/'r009/checks/coordinator-provenance-metamorphic-311-receipt.json').read_text())['payload_sha256']
payloads[1]=(payloads[1][0],payloads[1][1],metapin)
bootstrap="""import sys,json,runpy
from pathlib import Path
path,exe,version=sys.argv[1:]
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert '.'.join(map(str,sys.version_info[:3]))==version
assert sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps({'identity_before_import':{'executable':sys.executable,'version':sys.version}}),flush=True)
sys.argv=[path,exe,version]
runpy.run_path(path,run_name='__main__')
"""
def objects(data):
 text=data.decode('utf-8'); decoder=json.JSONDecoder(); out=[]
 while text.strip():
  text=text.lstrip();value,end=decoder.raw_decode(text);out.append(value);text=text[end:]
 return out
outputs=[]
for name,filename,pin in payloads:
 p=R/'r009/checks'/filename;raw=p.read_bytes()
 if sha(raw)!=pin:raise RuntimeError('issued payload differs')
 before=h.source_hashes(snap)
 if before!=s['source_sha256']:raise RuntimeError('source mismatch')
 log=R/(label+'-'+name+'-'+slot+'.txt');out=R/(label+'-'+name+'-'+slot+'-receipt.json')
 if log.exists() or out.exists():raise RuntimeError('outputs exist')
 cmd=[exe,'-B','-P','-c',bootstrap,str(p),exe,version]
 result=subprocess.run(cmd,cwd=snap,env=s['environment'],capture_output=True)
 data=(result.stdout+result.stderr).replace(b'\r\n',b'\n')
 with log.open('xb') as f:f.write(data)
 after=h.source_hashes(snap)
 if before!=after or raw!=p.read_bytes():raise RuntimeError('source/payload changed')
 h.load_setup(meta,msha)
 parsed=objects(result.stdout);identity=parsed[0]['identity_before_import']
 assert Path(identity['executable']).resolve()==Path(exe).resolve()
 assert identity['version'].startswith(version+' ')
 rows=[o for o in parsed if 'identity_before_import' not in o]
 failures=[];cases=[]
 if name=='forwarding':
  assert len(rows)==21 and rows[-1]['cases']==20
  cases=rows[:-1]
  for case in cases:
   if case['pure_error']!='TypeError' or case['pure_events'] or not case['blockers']:
    failures.append(case['case'])
 else:
  assert len(rows)==1;cases=rows[0]['results']
  assert len(cases)==(10 if name=='closure' else 3)
  for case in cases:
   mutation=name=='metamorphic' or case['expected_mutation']
   valid=(case['projection']=='TypeError' and bool(case['blockers'])) if mutation else (
    case['projection']=='fixed' and not case['blockers'] and len(case['process_rows'])==1)
   if not valid:failures.append(case['case'])
 rc=0 if result.returncode==0 and not failures else 1
 receipt={'metadata_sha256':msha,'command':cmd,'snapshot':str(snap),'environment':s['environment'],'before_sha256':before,'after_sha256':after,'payload_exit':result.returncode,'contract_exit':rc,'contract_cases':len(cases),'contract_failures':failures,'log_sha256':sha(data),'payload_sha256':sha(raw),'runner_sha256':sha(Path(__file__).read_bytes()),'runtime_identity':identity}
 with out.open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,indent=2);f.write('\n')
 outputs.append({'name':name,'receipt':str(out),'exit':rc,'failures':failures})
 print(json.dumps(outputs[-1]),flush=True)
raise SystemExit(0 if all(o['exit']==0 for o in outputs) else 1)
