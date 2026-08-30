"""Explicit combined-snapshot preparation and permitted-gate runner."""
import hashlib,importlib.util,json,os,subprocess,sys,uuid
from pathlib import Path
ROOT=Path(r"D:\Pontius-handoffs\v0a-i01-ab")
WORK=Path(r"D:\Pontius-worktrees\codex-v0a-i01-abc")
G=r"C:\Program Files\Git\cmd\git.exe"
BASE="d1ed3cbda6107d61ea8e77133871720af04970cd"
PATHS=tuple("src/pontius/v0a/"+n+".py" for n in ("__init__","clock","model","replay","runtime","trace"))+tuple("tests/"+n+".py" for n in ("test_v0a_contract_faults","test_v0a_hand_replay","test_v0a_replay","test_v0a_trace"))+(".github/workflows/ci.yml","tools/check_stabilization_boundaries.py","tools/generate_test_inventory.py","tests/test_v0a_boundaries.py","tests/test_inventory_and_profiles.py","tests/test-inventory.json","tests/test-profiles.toml")
ALLOWED={"module:pontius.status_generation","tests/test_status_generation.py","tests/test_evidence_errors_and_model.py","tests/test_evidence_manifests.py","tests/test_evidence_manifest_generation.py","tests/test_test_orchestration_import_boundary.py","tests/test_test_orchestration_configuration.py","tests/test_inventory_and_profiles.py","tests/test_stabilization_boundaries.py","tests/test_retained_evidence_inventory.py","tools/generate_test_inventory.py","tools/check_stabilization_boundaries.py","tools/ci_native_diagnostics.py","tests/test_v0a_boundaries.py","tests/test_v0a_hand_replay.py","tests/test_v0a_trace.py","tests/test_v0a_replay.py","tests/test_v0a_contract_faults.py"}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def create(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2);f.write('\n')
mode,*args=sys.argv[1:]
if mode=='prepare':
    label,source=args
    parent=Path(r"D:\pontius-snapshots")/(label+'-'+uuid.uuid4().hex)
    parent.mkdir();snapshot=parent/'harness';temporary=parent/'temp';temporary.mkdir()
    subprocess.run([G,'clone','--shared','--no-checkout',r"D:\Pontius",str(snapshot)],capture_output=True,check=True)
    base=BASE if source=='working' else source
    subprocess.run([G,'-C',str(snapshot),'checkout','--detach',base],capture_output=True,check=True)
    if source=='working':
        for path in PATHS:
            (snapshot/path).parent.mkdir(parents=True,exist_ok=True)
            (snapshot/path).write_bytes((WORK/path).read_bytes())
    env={k:os.environ[k] for k in ('SYSTEMROOT','WINDIR','COMSPEC') if k in os.environ}
    env.update(PATH=str(Path(env['SYSTEMROOT'])/'System32'),TEMP=str(temporary),TMP=str(temporary),PYTHONPATH=str(snapshot/'src'),PONTIUS_GIT=G,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='NUL')
    receipt=dict(label=label,source=source,base=base,snapshot=str(snapshot),temporary=str(temporary),environment=env,source_sha256={p:digest(snapshot/p) for p in PATHS})
    metadata=ROOT/(label+'-snapshot.json');create(metadata,receipt);print(metadata)
elif mode=='run':
    metadata,slot,label,target,*payload_args=args
    assert target in ALLOWED,target
    if target=='tools/generate_test_inventory.py':assert payload_args in (['--write'],['--check'])
    setup=json.loads(Path(metadata).read_text(encoding='utf-8'));snapshot=Path(setup['snapshot'])
    exe,version=((r"D:\Pontius-tools\py311\Scripts\python.exe",'3.11.15') if slot=='311' else (r"D:\Pontius\.venv\Scripts\python.exe",'3.14.6'))
    wrapper="""import sys,runpy,json,importlib.util
from pathlib import Path
exe,version,target,*args=sys.argv[1:]
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert '.'.join(map(str,sys.version_info[:3]))==version
assert sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps(dict(identity_before_payload_import=dict(executable=sys.executable,version=sys.version))),flush=True)
origin=Path(importlib.util.find_spec('pontius.v0a.trace').origin)
assert origin.resolve()==(Path.cwd()/'src/pontius/v0a/trace.py').resolve()
sys.argv=[target,*args]
if target.startswith('module:'):runpy.run_module(target.split(':',1)[1],run_name='__main__')
else:runpy.run_path(target,run_name='__main__')
"""
    command=[exe,'-B','-P','-c',wrapper,exe,version,target,*payload_args]
    before={p:digest(snapshot/p) for p in PATHS}
    result=subprocess.run(command,cwd=snapshot,env=setup['environment'],capture_output=True)
    data=(result.stdout+result.stderr).replace(b'\r\n',b'\n')
    directory=ROOT/'abc-checks';directory.mkdir(exist_ok=True)
    log=directory/(label+'-'+slot+'.txt')
    with log.open('xb') as f:f.write(data)
    after={p:digest(snapshot/p) for p in PATHS}
    changed=[p for p in PATHS if before[p]!=after[p]]
    allowed_changes={'tests/test-inventory.json','tests/test-profiles.toml'} if payload_args==['--write'] and target=='tools/generate_test_inventory.py' else set()
    assert set(changed)<=allowed_changes,changed
    receipt=dict(label=label,slot=slot,base=setup['base'],snapshot=str(snapshot),command=command,environment=setup['environment'],exit=result.returncode,log=str(log),sha256=digest(log),before_sha256=before,after_sha256=after,changed_paths=changed)
    create(directory/(label+'-'+slot+'-receipt.json'),receipt)
    print(data.decode(errors='replace')[-5000:]);print('exit',result.returncode,flush=True)
    sys.exit(result.returncode)
else:raise SystemExit('unknown operation')
