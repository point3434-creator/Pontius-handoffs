"""Fresh snapshot verification of one immutable r003 candidate."""
import hashlib,json,os,subprocess,sys,uuid
from pathlib import Path
PACKET=Path('D:/Pontius-handoffs/v0a-i01-impl/r003')
GIT='C:/Program Files/Git/cmd/git.exe'
META=json.loads((PACKET/'candidate.json').read_bytes())
python=Path(sys.argv[1]).resolve(strict=True); version=sys.argv[2]; label=sys.argv[3]
report=PACKET/'checks'/(label+'-verification.json')
assert not report.exists(), 'Receipt already exists'
root=Path('D:/pontius-snapshots')/('v0a-i01-r003-'+uuid.uuid4().hex)
harness=root/'harness'; temp=root/'temp'; temp.mkdir(parents=True)
env={key:os.environ[key] for key in ('SystemRoot','WINDIR','ComSpec','PATHEXT') if key in os.environ}
env.update({'PATH':str(python.parent)+';'+os.environ['SystemRoot']+'/System32','TEMP':str(temp),'TMP':str(temp),
 'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'NUL','GIT_NO_REPLACE_OBJECTS':'1','GIT_LITERAL_PATHSPECS':'1'})
def git(repo,*args):
    return subprocess.run([GIT,'-C',str(repo),*args],env=env,check=True,capture_output=True).stdout
assert git('D:/Pontius','rev-parse',META['ref']).decode().strip()==META['commit']
assert git('D:/Pontius','rev-parse',META['commit']+'^').decode().strip()==META['base']
assert git('D:/Pontius','rev-parse',META['commit']+'^{tree}').decode().strip()==META['tree']
paths=git('D:/Pontius','diff-tree','-r','--no-commit-id','--no-renames','--name-only',META['base'],META['commit']).decode().splitlines()
assert set(paths)=={'src/pontius/v0a/__init__.py','src/pontius/v0a/model.py','src/pontius/v0a/clock.py','src/pontius/v0a/runtime.py','src/pontius/v0a/trace.py','src/pontius/v0a/replay.py','tests/test_v0a_hand_replay.py','tests/test_v0a_trace.py','tests/test_v0a_replay.py','tests/test_v0a_contract_faults.py'}
rows=sorted(hashlib.sha256(git('D:/Pontius','cat-file','blob',META['commit']+':'+path)).hexdigest()+'  '+path+'\n' for path in paths)
raw=''.join(rows).encode(); assert raw==(PACKET/'manifest.sha256').read_bytes()
assert hashlib.sha256(raw).hexdigest()==META['manifest_sha256']
subprocess.run([GIT,'-c','core.autocrlf=false','-c','core.eol=lf','clone','--local','--no-hardlinks','--no-checkout','D:/Pontius',str(harness)],env=env,check=True,capture_output=True)
git(harness,'-c','core.autocrlf=false','-c','core.eol=lf','checkout','--detach',META['commit'])
assert not (harness/'.git/objects/info/alternates').exists()
assert not git(harness,'status','--porcelain')
env.update({'PYTHONPATH':str(harness/'src'),'PYTHONDONTWRITEBYTECODE':'1','PYTHONSAFEPATH':'1','PYTHONNOUSERSITE':'1','PYTHONHASHSEED':'0','PYTHONUTF8':'1','PONTIUS_GIT':GIT})
def child(args):
    return subprocess.run([str(python),'-B','-P',*args],cwd=harness,env=env,capture_output=True,text=True)
identity_probe=child(['-c','import sys,json; print(json.dumps(dict(executable=sys.executable,implementation=sys.implementation.name,full_version=sys.version,version=list(sys.version_info[:3]))))'])
assert identity_probe.returncode==0,identity_probe.stderr
identity=json.loads(identity_probe.stdout)
assert identity['implementation']=='cpython'
assert '.'.join(map(str,identity['version'][:2]))==version
assert os.path.normcase(identity['executable'])==os.path.normcase(str(python))
identity_log=PACKET/'checks'/(label+'-identity.json')
assert not identity_log.exists()
identity_log.write_text(json.dumps(identity,indent=2)+'\n',encoding='utf-8',newline='\n')
imports=child(['-c','import sys,json,pontius.v0a.runtime as r; print(json.dumps(dict(runtime_file=r.__file__,tracked_dependency_imports=sorted(set(n.split(".")[0] for n in sys.modules if n.split(".")[0] in ("cupy","numpy","torch"))))))'])
assert imports.returncode==0,imports.stderr
imports=json.loads(imports.stdout)
assert Path(imports['runtime_file']).resolve()==harness/'src/pontius/v0a/runtime.py'
assert not set(imports['tracked_dependency_imports']) & {'cupy','torch'}
results=[]
for name,args in [(name,['tests/test_v0a_'+name+'.py','-v']) for name in ('hand_replay','trace','replay','contract_faults')]:
    result=child(args); log=PACKET/'checks'/(label+'-'+name+'.txt')
    assert not log.exists()
    log.write_text(result.stdout+result.stderr,encoding='utf-8',newline='\n')
    results.append({'argv':[str(python),'-B','-P',*args],'exit':result.returncode,'log':str(log)})
    print(json.dumps({'name':name,'exit':result.returncode,'output':(result.stdout+result.stderr)[-450:]}),flush=True)
assert not git(harness,'status','--porcelain')
for row in rows:
    digest,path=row.rstrip('\n').split('  ',1)
    assert hashlib.sha256((harness/path).read_bytes()).hexdigest()==digest
outcome={'candidate':META['commit'],'manifest_sha256':META['manifest_sha256'],'snapshot':str(harness),'identity':identity,'identity_asserted_before_payload_import':True,'import_provenance':imports,'snapshot_pristine':True,'results':results,'scope':'Four r003 focused correctness suites; no broad suite or experiment'}
report.write_text(json.dumps(outcome,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'receipt':str(report),'identity':identity}),flush=True)
raise SystemExit(0 if all(r['exit']==0 for r in results) else 1)
