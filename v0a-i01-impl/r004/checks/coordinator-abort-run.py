from pathlib import Path
import json,os,subprocess,hashlib
root=Path(r'D:\Pontius-handoffs\v0a-i01-impl\r004\checks')
snap=Path(r'D:\pontius-snapshots\v0a-r004-coordinator-d566b71fc28d46d99b7885eb12433efa\harness')
git=r'C:\Program Files\Git\cmd\git.exe'
env={key:os.environ[key] for key in ('SYSTEMROOT','WINDIR','TEMP','TMP') if key in os.environ}
env['PYTHONPATH']=str(snap/'src');env['PONTIUS_GIT']=git
def clean():
    assert subprocess.check_output([git,'-C',str(snap),'rev-parse','HEAD']).decode().strip()=='0207430a37e1e5b31c8da8da7aa57da1bc5c88ee'
    assert not subprocess.check_output([git,'-C',str(snap),'status','--porcelain']).strip()
clean()
for slot,python,version in [('311',r'D:\Pontius-tools\py311\Scripts\python.exe','3.11.15'),('314',r'D:\Pontius\.venv\Scripts\python.exe','3.14.6')]:
    argv=[python,'-B','-P',str(root/'coordinator-abort-probe.py'),python,version]
    p=subprocess.run(argv,cwd=snap,env=env,capture_output=True)
    log=root/('coordinator-'+slot+'-abort.txt')
    with log.open('xb') as f:f.write(p.stdout+p.stderr)
    clean()
    with (root/('coordinator-'+slot+'-abort-receipt.json')).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(dict(candidate='0207430a37e1e5b31c8da8da7aa57da1bc5c88ee',manifest_sha256='ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef',command=argv,exit=p.returncode,snapshot=str(snap),environment=env,source_pristine=True,sha256=hashlib.sha256(log.read_bytes()).hexdigest()),f,indent=2);f.write('\n')
    assert p.returncode==0
    obs=json.loads(p.stdout.decode().splitlines()[-1])['observations']
    print(json.dumps(dict(slot=slot,count=len(obs),relevant=[x for x in obs if x['reason']=='event_order'])))
