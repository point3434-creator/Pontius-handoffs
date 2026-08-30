from pathlib import Path
import json,os,subprocess,sys,hashlib
packet=Path(r'D:\Pontius-handoffs\v0a-i01-impl\r004')
snap=Path(r'D:\pontius-snapshots\v0a-r004-coordinator-d566b71fc28d46d99b7885eb12433efa\harness')
git=r'C:\Program Files\Git\cmd\git.exe'
slot=sys.argv[1]
python,version={'311':(r'D:\Pontius-tools\py311\Scripts\python.exe','3.11.15'),'314':(r'D:\Pontius\.venv\Scripts\python.exe','3.14.6')}[slot]
env={key:os.environ[key] for key in ('SYSTEMROOT','WINDIR','TEMP','TMP') if key in os.environ}
env['PYTHONPATH']=str(snap/'src');env['PONTIUS_GIT']=git
def gitrun(*args):return subprocess.check_output([git,'-C',str(snap),*args])
assert gitrun('rev-parse','HEAD').decode().strip()=='0207430a37e1e5b31c8da8da7aa57da1bc5c88ee'
assert not gitrun('status','--porcelain').strip()
wrapper="import sys,json,runpy; from pathlib import Path; expected,version,target=sys.argv[1:4]; assert Path(sys.executable).resolve()==Path(expected).resolve(); assert sys.implementation.name=='cpython'; assert '.'.join(map(str,sys.version_info[:3]))==version; assert sys.flags.safe_path and sys.dont_write_bytecode; print(json.dumps(dict(identity_before_payload_import=dict(executable=sys.executable,implementation=sys.implementation.name,full_version=sys.version))),flush=True); sys.argv=[target,'-v']; runpy.run_path(target,run_name='__main__')"
commands=[('probe',[python,'-B','-P',str(packet/'checks/coordinator-probe.py'),python,version])]
for name in ('hand_replay','trace','replay','contract_faults'):
    commands.append((name,[python,'-B','-P','-c',wrapper,python,version,'tests/test_v0a_'+name+'.py']))
results=[]
for label,argv in commands:
    done=subprocess.run(argv,cwd=snap,env=env,capture_output=True)
    log=packet/('checks/coordinator-'+slot+'-'+label+'.txt')
    with log.open('xb') as f:f.write(done.stdout+done.stderr)
    results.append(dict(command=argv,exit=done.returncode,log=str(log),sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
assert not gitrun('status','--porcelain').strip()
receipt=dict(candidate='0207430a37e1e5b31c8da8da7aa57da1bc5c88ee',manifest_sha256='ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef',slot=slot,snapshot=str(snap),environment=env,results=results,source_pristine=True)
with (packet/('checks/coordinator-'+slot+'-receipt.json')).open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt,indent=2))
if any(r['exit'] for r in results):sys.exit(1)
