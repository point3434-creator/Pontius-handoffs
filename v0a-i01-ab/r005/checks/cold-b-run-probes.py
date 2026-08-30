import hashlib, json, os, pathlib, subprocess, sys
snapshot=pathlib.Path(sys.argv[1]); checks=pathlib.Path('D:/Pontius-handoffs/v0a-i01-ab/r005/checks')
env={k:os.environ[k] for k in ('SYSTEMROOT','WINDIR','TEMP','TMP') if k in os.environ}
env.update(PONTIUS_GIT='C:/Program Files/Git/cmd/git.exe',PYTHONPATH=str(snapshot/'src'),
           PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',PYTHONUTF8='1')
for tag,exe,version in [('311','D:/Pontius-tools/py311/Scripts/python.exe','3.11.15'),('314','D:/Pontius/.venv/Scripts/python.exe','3.14.6')]:
    argv=[exe,'-B','-P',str(checks/'cold-b-probe.py')]
    p=subprocess.run(argv,cwd=snapshot,env=env,capture_output=True)
    log=checks/('cold-b-'+tag+'-probe.log'); log.write_bytes(p.stdout+p.stderr)
    receipt={'argv':argv,'cwd':str(snapshot),'environment':env,'exit_code':p.returncode,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
    (checks/('cold-b-'+tag+'-probe-receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
    print(json.dumps(receipt)); print((p.stdout+p.stderr).decode('utf8','replace'))
    assert p.returncode==0
    assert json.loads(p.stdout)['version']==version
