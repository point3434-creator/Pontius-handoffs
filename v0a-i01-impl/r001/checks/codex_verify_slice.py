"""Fresh snapshot verification of one immutable Slice A candidate."""
import hashlib,json,os,subprocess,sys,uuid
from pathlib import Path
PACKET=Path('D:/Pontius-handoffs/v0a-i01-impl/r001')
GIT='C:/Program Files/Git/cmd/git.exe'
META=json.loads((PACKET/'candidate.json').read_bytes())
python=Path(sys.argv[1]).resolve(strict=True); version=sys.argv[2]; label=sys.argv[3]
report=PACKET/'checks'/(label+'-verification.json')
assert not report.exists(), 'Receipt already exists'
root=Path('D:/pontius-snapshots')/('v0a-i01-slice-a-'+uuid.uuid4().hex)
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
assert set(paths)=={'src/pontius/v0a/__init__.py','src/pontius/v0a/model.py','src/pontius/v0a/clock.py','src/pontius/v0a/runtime.py','tests/test_v0a_hand_replay.py'}
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
identity=child(['-c','import sys,json,pontius.v0a.runtime as r; print(json.dumps(dict(executable=sys.executable,version=list(sys.version_info[:3]),runtime_file=r.__file__,optional_imports=[n for n in sys.modules if n.split(".")[0] in ("cupy","numpy","torch") ])))'])
assert identity.returncode==0,identity.stderr
identity=json.loads(identity.stdout)
assert '.'.join(map(str,identity['version'][:2]))==version
assert Path(identity['runtime_file']).resolve()==harness/'src/pontius/v0a/runtime.py'
assert not identity['optional_imports']
results=[]
for name,args in [('suite',['tests/test_v0a_hand_replay.py','-v']),('probes',[str(PACKET/'checks/codex_adversarial_probes.py')])]:
    result=child(args); log=PACKET/'checks'/(label+'-'+name+'.txt')
    assert not log.exists()
    log.write_text(result.stdout+result.stderr,encoding='utf-8',newline='\n')
    results.append({'argv':[str(python),'-B','-P',*args],'exit':result.returncode,'log':str(log)})
    print(json.dumps({'name':name,'exit':result.returncode,'output':result.stdout+result.stderr}),flush=True)
assert not git(harness,'status','--porcelain')
for row in rows:
    digest,path=row.rstrip('\n').split('  ',1)
    assert hashlib.sha256((harness/path).read_bytes()).hexdigest()==digest
outcome={'candidate':META['commit'],'manifest_sha256':META['manifest_sha256'],'snapshot':str(harness),'identity':identity,'snapshot_pristine':True,'results':results,'scope':'Slice A correctness suite and bounded public-boundary diagnostics; no broad suite or experiment'}
report.write_text(json.dumps(outcome,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'receipt':str(report),'identity':identity}),flush=True)
raise SystemExit(0 if all(r['exit']==0 for r in results) else 1)
