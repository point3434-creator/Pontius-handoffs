import sys
assert sys.implementation.name == 'cpython' and sys.version_info[:3] == (3,11,15)
import datetime, hashlib, json, os, pathlib, subprocess
packet = pathlib.Path(r'D:\Pontius-handoffs\v0a-i01-ab\r001')
checks = packet / 'checks'
root = pathlib.Path(json.loads((checks/'cold-b-identity.json').read_text())['snapshot']).resolve()
version = sys.argv[1]
assert version in ('3.11.15','3.14.6')
python = pathlib.Path(r'D:\Pontius-tools\py311\Scripts\python.exe' if version=='3.11.15' else r'D:\Pontius\.venv\Scripts\python.exe')
suffix = '311' if version=='3.11.15' else '314'
temp = pathlib.Path(r'D:\Pontius-snapshots') / ('cold-b-tmp-'+suffix)
temp.mkdir(exist_ok=True)
env = {k:os.environ[k] for k in ('SYSTEMROOT','WINDIR','COMSPEC') if k in os.environ}
env.update({'TEMP':str(temp),'TMP':str(temp),'PYTHONPATH':str(root/'src'),'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','PONTIUS_GIT':r'C:\Program Files\Git\cmd\git.exe'})
items = [(name, root/'tests'/('test_v0a_'+name+'.py')) for name in ('hand_replay','trace','replay','contract_faults')]
if len(sys.argv)>2:
    items=[('diagnostic', checks/sys.argv[2])]
results=[]
for name,target in items:
    cmd=[str(python),'-B','-P',str(checks/'cold-b-payload.py'),version,str(root),str(target)]
    result=subprocess.run(cmd, env=env,cwd=root,capture_output=True)
    log=checks/('cold-b-v2-'+name+'-'+suffix+'.log')
    with log.open('xb') as f:
        f.write(b'STDOUT\n'+result.stdout+b'\nSTDERR\n'+result.stderr)
    row={'name':name,'command':cmd,'cwd':str(root),'env':env,'exit':result.returncode,'log':str(log),'sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
    results.append(row)
    print(json.dumps({'name':name,'exit':result.returncode,'stdout_tail':result.stdout.decode(errors='replace')[-1000:],'stderr_tail':result.stderr.decode(errors='replace')[-1000:]}),flush=True)
receipt=checks/('cold-b-v2-'+('diagnostic' if len(sys.argv)>2 else 'focused')+'-'+suffix+'.json')
with receipt.open('x',encoding='utf-8',newline='\n') as f:
    json.dump({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},f,indent=2); f.write('\n')
assert all(r['exit']==0 for r in results), 'Payload failed; inspect immutable logs'
