"""Fresh two-file provenance repair checks, no generation/capability writer."""
import hashlib,json,os,subprocess,sys,uuid
from pathlib import Path
ROOT=Path(r"D:\Pontius-handoffs\v0a-i01-ab")
WORK=Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-provenance")
BASE='00db06624ab25f10cd181badccf92c87a78f17ee'
G=r"C:\Program Files\Git\cmd\git.exe"
label,slot,*targets=sys.argv[1:]
assert label and all(c.isalnum() or c=='-' for c in label)
assert slot in ('311','314') and targets and all(x.startswith('DesignReviewTests.test_') for x in targets)
parent=Path(r"D:\pontius-snapshots")/('c-provenance-'+label+'-'+slot+'-'+uuid.uuid4().hex)
parent.mkdir();snapshot=parent/'harness';temporary=parent/'temp';temporary.mkdir()
for args in (['-c','core.autocrlf=false','clone','--shared','--no-checkout',r"D:\Pontius",str(snapshot)],['-C',str(snapshot),'-c','core.autocrlf=false','checkout','--detach',BASE]):
 subprocess.run([G,*args],capture_output=True,check=True)
paths=('tools/generate_test_inventory.py','tests/test_inventory_and_profiles.py')
for p in paths:(snapshot/p).write_bytes((WORK/p).read_bytes())
hashes={p:hashlib.sha256((snapshot/p).read_bytes()).hexdigest() for p in paths}
env={k:os.environ[k] for k in ('SYSTEMROOT','WINDIR','COMSPEC') if k in os.environ}
env.update(PATH=str(Path(env['SYSTEMROOT'])/'System32'),TEMP=str(temporary),TMP=str(temporary),PYTHONPATH=str(snapshot/'src'),PONTIUS_GIT=G,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='NUL')
exe,version=(r"D:\Pontius-tools\py311\Scripts\python.exe",'3.11.15') if slot=='311' else (r"D:\Pontius\.venv\Scripts\python.exe",'3.14.6')
payload=ROOT/'c-binding-payload.py'
command=[exe,'-B','-P',str(payload),version,exe,*targets]
result=subprocess.run(command,cwd=snapshot,env=env,capture_output=True)
assert hashes=={p:hashlib.sha256((snapshot/p).read_bytes()).hexdigest() for p in paths}
data=(result.stdout+result.stderr).replace(b'\r\n',b'\n')
log=ROOT/('c-provenance-'+label+'-'+slot+'.txt')
with log.open('xb') as f:f.write(data)
receipt=dict(label=label,slot=slot,base=BASE,snapshot=str(snapshot),temporary=str(temporary),overlay_sha256=hashes,command=command,environment=env,exit=result.returncode,log=str(log),sha256=hashlib.sha256(data).hexdigest(),payload_sha256=hashlib.sha256(payload.read_bytes()).hexdigest())
with (ROOT/('c-provenance-'+label+'-'+slot+'-receipt.json')).open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(data.decode(errors='replace')[-8000:]);print('exit',result.returncode)
sys.exit(result.returncode)
