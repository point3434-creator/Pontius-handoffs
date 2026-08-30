"""Run coordinator probes with frozen snapshot provenance and scrubbed env."""
import os, json, subprocess, sys, hashlib
from pathlib import Path
packet = Path('D:/Pontius-handoffs/v0a-i01-impl/r002')
label, version = sys.argv[1:]
receipt = json.loads((packet/'checks'/f'{label}-verification.json').read_bytes())
snapshot=Path(receipt['snapshot']); executable=receipt['identity']['executable']
temp=snapshot.parent/('coordinator-temp-'+version); temp.mkdir()
env={key:os.environ[key] for key in ('SystemRoot','WINDIR','ComSpec','PATHEXT') if key in os.environ}
env.update(PATH=str(Path(executable).parent)+';'+os.environ['SystemRoot']+'/System32',TEMP=str(temp),TMP=str(temp),
    PYTHONPATH=str(snapshot/'src'),PYTHONDONTWRITEBYTECODE='1',PYTHONSAFEPATH='1',PYTHONNOUSERSITE='1',PYTHONHASHSEED='0',PYTHONUTF8='1',
    PONTIUS_GIT='C:/Program Files/Git/cmd/git.exe',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='NUL',GIT_NO_REPLACE_OBJECTS='1',GIT_LITERAL_PATHSPECS='1')
for row in (packet/'manifest.sha256').read_text().splitlines():
    digest,path=row.split('  ',1)
    assert hashlib.sha256((snapshot/path).read_bytes()).hexdigest()==digest
argv=[executable,'-B','-P',str(packet/'checks/codex_host_storage_probes.py'),version,executable]
result=subprocess.run(argv,cwd=snapshot,env=env,capture_output=True,text=True)
log=packet/'checks'/f'{label}-host-storage.txt'
with log.open('x',encoding='utf-8',newline='\n') as file: file.write(result.stdout+result.stderr)
status=subprocess.run([env['PONTIUS_GIT'],'-C',str(snapshot),'status','--porcelain'],env=env,capture_output=True,check=True).stdout
assert not status
print(json.dumps({'argv':argv,'cwd':str(snapshot),'exit':result.returncode,'log':str(log),'snapshot_pristine':True}))
print(result.stdout+result.stderr)
sys.exit(result.returncode)
