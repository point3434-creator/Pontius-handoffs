import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(r"D:\Pontius-handoffs\v0a-i01-ab")
setup=json.loads((ROOT/"abc-draft-snapshot.json").read_text(encoding="utf-8"))
label,slot,target,*args=sys.argv[1:]
exe,version=((r"D:\Pontius-tools\py311\Scripts\python.exe","3.11.15") if slot=="311" else (r"D:\Pontius\.venv\Scripts\python.exe","3.14.6"))
w=Path(setup["snapshot"])
wrapper="""import sys,runpy,json,importlib.util
from pathlib import Path
exe,version,target,*args=sys.argv[1:]
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert '.'.join(map(str,sys.version_info[:3]))==version
assert sys.flags.safe_path and sys.dont_write_bytecode
origin=Path(importlib.util.find_spec('pontius.v0a.trace').origin)
assert origin.resolve()==(Path.cwd()/'src/pontius/v0a/trace.py').resolve()
print(json.dumps(dict(identity_before_payload_import=dict(executable=sys.executable,version=sys.version,trace_origin=str(origin)))),flush=True)
sys.argv=[target,*args]
runpy.run_path(target,run_name='__main__')
"""
command=[exe,'-B','-P','-c',wrapper,exe,version,target,*args]
result=subprocess.run(command,cwd=w,env=setup['environment'],capture_output=True)
data=(result.stdout+result.stderr).replace(b'\r\n',b'\n')
checks=ROOT/'abc-draft-checks';checks.mkdir(exist_ok=True)
log=checks/(label+'-'+slot+'.txt')
with log.open('xb') as f:f.write(data)
r=dict(label=label,slot=slot,snapshot=str(w),base=setup['base'],command=command,environment=setup['environment'],exit=result.returncode,log=str(log),sha256=hashlib.sha256(data).hexdigest(),after_sha256={p:hashlib.sha256((w/p).read_bytes()).hexdigest() for p in setup['overlay_sha256']})
with (checks/(label+'-'+slot+'-receipt.json')).open('x',encoding='utf-8',newline='\n') as f:json.dump(r,f,indent=2);f.write('\n')
print(data.decode(errors='replace')[-8000:])
print('exit',result.returncode,flush=True)
sys.exit(result.returncode)
