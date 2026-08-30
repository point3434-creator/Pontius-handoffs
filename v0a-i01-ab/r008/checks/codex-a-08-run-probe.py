import json,pathlib,subprocess,sys,time
checks=pathlib.Path(r'D:\Pontius-handoffs\v0a-i01-ab\r008\checks'); info=json.loads((checks/'codex-a-02-identity.json').read_text());root=pathlib.Path(info['snapshot']);env=info['scrubbed_environment'];env['PYTHONPATH']=str(root/'src')
version,label,target=sys.argv[1:]
py={'3.11.15':r'D:\Pontius-tools\py311\Scripts\python.exe','3.14.6':r'D:\Pontius\.venv\Scripts\python.exe'}[version]
cmd=[py,'-B','-P',str(checks/'codex-a-04-bootstrap.py'),version,str(root),str(checks/target)]
with (checks/f'codex-a-{label}-{version}.log').open('x',encoding='utf-8',newline='\n') as f:
 f.write(json.dumps({'command':cmd,'environment':env})+'\n');f.flush();start=time.monotonic();result=subprocess.run(cmd,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT);f.write(json.dumps({'exit':result.returncode,'elapsed_seconds':time.monotonic()-start})+'\n')
print('exit',result.returncode)