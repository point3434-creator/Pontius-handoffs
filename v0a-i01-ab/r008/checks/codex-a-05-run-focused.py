import json, os, pathlib, subprocess, sys, time
checks=pathlib.Path(r'D:\Pontius-handoffs\v0a-i01-ab\r008\checks')
info=json.loads((checks/'codex-a-02-identity.json').read_text())
root=pathlib.Path(info['snapshot'])
env=info['scrubbed_environment']; env['PYTHONPATH']=str(root/'src')
version=sys.argv[1]
py={'3.11.15':r'D:\Pontius-tools\py311\Scripts\python.exe','3.14.6':r'D:\Pontius\.venv\Scripts\python.exe'}[version]
commands=[('boundaries',['tests/test_v0a_boundaries.py']),('inventory',['tests/test_inventory_and_profiles.py']),('legacy-boundaries',['tests/test_stabilization_boundaries.py']),('hand',['tests/test_v0a_hand_replay.py']),('trace',['tests/test_v0a_trace.py']),('replay',['tests/test_v0a_replay.py']),('faults',['tests/test_v0a_contract_faults.py']),('generator-check',['tools/generate_test_inventory.py','--check']),('boundary-cli',['tools/check_stabilization_boundaries.py'])]
for label,args in commands:
    command=[py,'-B','-P',str(checks/'codex-a-04-bootstrap.py'),version,str(root),str(root/args[0]),*args[1:]]
    path=checks/f'codex-a-06-{version}-{label}.log'
    with path.open('x',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps({'command':command,'cwd':str(root),'environment':env})+'\n'); f.flush()
        started=time.monotonic()
        completed=subprocess.run(command,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
        elapsed=time.monotonic()-started
        f.write(json.dumps({'exit':completed.returncode,'elapsed_seconds':elapsed})+'\n')
    print(json.dumps({'label':label,'version':version,'exit':completed.returncode,'seconds':elapsed,'receipt':str(path)}),flush=True)
    if completed.returncode: raise SystemExit(completed.returncode)
result=subprocess.run([info['git'],'-C',str(root),'status','--porcelain','--untracked-files=all'],cwd=root,env=env,capture_output=True,check=True)
assert not result.stdout,result.stdout
print('Snapshot remains clean',flush=True)