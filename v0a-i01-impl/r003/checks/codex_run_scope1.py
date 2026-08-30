"""Fresh frozen-clone runner for coordinator slice-1 diagnostics."""
import json,os,subprocess,sys,uuid,hashlib
from pathlib import Path
packet=Path('D:/Pontius-handoffs/v0a-i01-impl/r003'); git='C:/Program Files/Git/cmd/git.exe'
executable,version,label=sys.argv[1:]
meta=json.loads((packet/'candidate.json').read_bytes())
area=Path('D:/pontius-snapshots')/('r003-coordinator-'+uuid.uuid4().hex)
root=area/'harness'; temp=area/'temp'; temp.mkdir(parents=True)
env={k:os.environ[k] for k in ('SystemRoot','WINDIR','ComSpec','PATHEXT') if k in os.environ}
env.update(PATH=str(Path(executable).parent)+';'+os.environ['SystemRoot']+'/System32',TEMP=str(temp),TMP=str(temp),
           GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='NUL',GIT_NO_REPLACE_OBJECTS='1',GIT_LITERAL_PATHSPECS='1')
def call(args,**kwargs): return subprocess.run(args,env=env,capture_output=True,check=True,**kwargs).stdout
call([git,'-c','core.autocrlf=false','-c','core.eol=lf','clone','--local','--no-hardlinks','--no-checkout','D:/Pontius',str(root)])
call([git,'-C',str(root),'-c','core.autocrlf=false','-c','core.eol=lf','checkout','--detach',meta['commit']])
raw=(packet/'manifest.sha256').read_bytes(); assert hashlib.sha256(raw).hexdigest()==meta['manifest_sha256']
for row in raw.decode().splitlines():
    digest,path=row.split('  ',1)
    blob=call([git,'-C',str(root),'cat-file','blob',meta['commit']+':'+path])
    assert blob==(root/path).read_bytes() and hashlib.sha256(blob).hexdigest()==digest
assert not (root/'.git/objects/info/alternates').exists()
env.update(PYTHONPATH=str(root/'src'),PYTHONNOUSERSITE='1',PYTHONSAFEPATH='1',PYTHONDONTWRITEBYTECODE='1',
           PYTHONUTF8='1',PYTHONHASHSEED='0',PONTIUS_GIT=git)
argv=[executable,'-B','-P',str(packet/'checks/codex_scope1_probes.py'),executable,version]
result=subprocess.run(argv,cwd=root,env=env,capture_output=True,text=True)
log=packet/'checks'/f'{label}-scope1.txt'
with log.open('x',encoding='utf-8',newline='\n') as file: file.write(result.stdout+result.stderr)
assert not call([git,'-C',str(root),'status','--porcelain'])
report=dict(candidate=meta['commit'],manifest_sha256=meta['manifest_sha256'],argv=argv,cwd=str(root),
            exit=result.returncode,log=str(log),source_pristine=True,scope='r003 slice1 correctness only')
with (packet/'checks'/f'{label}-scope1-receipt.json').open('x',encoding='utf-8',newline='\n') as file:
    json.dump(report,file,indent=2); file.write('\n')
print(json.dumps(report))
if result.returncode: print(result.stdout+result.stderr)
else:
    output=json.loads(result.stdout.splitlines()[-1])
    for row in output['observations']:
        print(json.dumps({k:v for k,v in row.items() if k!='details'}))
sys.exit(result.returncode)
