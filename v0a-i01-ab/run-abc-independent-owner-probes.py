import sys,json,hashlib,importlib.util,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
hp=R/'snapshot-run-abc-v2.py'
if sha(hp.read_bytes())!='62bf07eb88845dfc30c3820aeb8c899ccfbe8111d811192485e2826a5ecfc20c':raise RuntimeError('harness hash differs')
spec=importlib.util.spec_from_file_location('bound_snapshot',hp);h=importlib.util.module_from_spec(spec);sys.modules[spec.name]=h;spec.loader.exec_module(h)
h.require_control_runtime()
meta,msha,slot,label=sys.argv[1:]
s=h.load_setup(meta,msha);snap=Path(s['snapshot']);exe,version=h.SLOTS[slot]
outputs=[]
for name in ('owner','effective-input'):
 p=R/('abc-provenance-v2-'+name+'-probe.py');raw=p.read_bytes();before=h.source_hashes(snap)
 if before!=s['source_sha256']:raise RuntimeError('source mismatch')
 log=R/(label+'-'+name+'-'+slot+'.txt');out=R/(label+'-'+name+'-'+slot+'-receipt.json')
 if log.exists() or out.exists():raise RuntimeError('outputs exist')
 cmd=[exe,'-B','-P',str(p),exe,version]
 result=subprocess.run(cmd,cwd=snap,env=s['environment'],capture_output=True)
 data=(result.stdout+result.stderr).replace(b'\r\n',b'\n')
 with log.open('xb') as f:f.write(data)
 after=h.source_hashes(snap)
 if before!=after or raw!=p.read_bytes():raise RuntimeError('probe changed source/payload')
 h.load_setup(meta,msha)
 identity=json.loads(result.stdout.splitlines()[0])['identity_before_import']
 if Path(identity['executable']).resolve()!=Path(exe).resolve() or not identity['version'].startswith(version+' '):raise RuntimeError('identity differs')
 receipt={'metadata_sha256':msha,'command':cmd,'snapshot':str(snap),'environment':s['environment'],'before_sha256':before,'after_sha256':after,'exit':result.returncode,'log_sha256':sha(data),'payload_sha256':sha(raw),'runner_sha256':sha(Path(__file__).read_bytes()),'runtime_identity':identity}
 with out.open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,indent=2);f.write('\n')
 outputs.append({'receipt':str(out),'exit':result.returncode})
print(json.dumps(outputs))
raise SystemExit(0 if all(o['exit']==0 for o in outputs) else 1)
