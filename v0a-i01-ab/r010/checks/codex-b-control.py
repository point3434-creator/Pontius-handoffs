import hashlib, json, os, pathlib, stat, subprocess, sys, uuid
P=pathlib.Path
ROOT=P(r'D:\Pontius-handoffs\v0a-i01-ab\r010')
REPO=P(r'D:\Pontius')
G=P(r'C:\Program Files\Git\cmd\git.exe')
C='29c02f6fbd5eb0b7ddc9e816ef28f570b9839358'
BASE='d1ed3cbda6107d61ea8e77133871720af04970cd'
EXPECTED='8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb'
SLOTS={'311':(P(r'D:\Pontius-tools\py311\Scripts\python.exe'),'3.11.15'),'314':(P(r'D:\Pontius\.venv\Scripts\python.exe'),'3.14.6')}
def req(ok,message):
    if not ok: raise RuntimeError(message)
def validate(path):
    req(path.is_absolute() and '..' not in path.parts,'nonabsolute')
    for item in (path,*path.parents):
        x=item.lstat(); req(not (getattr(x,'st_file_attributes',0)&stat.FILE_ATTRIBUTE_REPARSE_POINT),'reparse '+str(item))
    return path
def h(raw): return hashlib.sha256(raw).hexdigest()
def write(path,raw):
    with path.open('xb') as f:f.write(raw)
def jout(path,value): write(path,(json.dumps(value,indent=2)+'\n').encode())
def env(temp,snapshot=None):
    w=validate(P(os.environ['SYSTEMROOT'])); s=validate(w/'System32')
    e={'SYSTEMROOT':str(w),'WINDIR':str(w),'COMSPEC':str(s/'cmd.exe'),'PATH':str(s),'TEMP':str(temp),'TMP':str(temp),'PONTIUS_GIT':str(G),'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'NUL','GIT_CONFIG_SYSTEM':'NUL','GIT_ATTR_NOSYSTEM':'1','PYTHONNOUSERSITE':'1'}
    if snapshot:e['PYTHONPATH']=str(snapshot/'src')
    return e
def git(repo,temp,*args):
    validate(G)
    return subprocess.run([str(G),'-c','core.autocrlf=false','-c','core.hooksPath=NUL','-c','init.templateDir=','-c','core.attributesFile=NUL','-c','core.fsmonitor=false','-C',str(repo),*args],cwd=repo,env=env(temp),capture_output=True,check=True).stdout
req(sys.implementation.name=='cpython' and sys.version_info[:3]==(3,11,15),'wrong control version')
req(P(sys.executable).resolve()==SLOTS['311'][0].resolve(),'wrong control executable')
req(sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode,'control flags')
mode=sys.argv[1]
if mode=='prepare':
    validate(ROOT/'checks'); temp=REPO/('codex-b-r010-snapshot-'+uuid.uuid4().hex); temp.mkdir(); (temp/'temp').mkdir()
    req(git(REPO,temp/'temp','rev-parse','--verify','refs/heads/review/v0a-i01-ab/r010').decode().strip()==C,'ref mismatch')
    fields=git(REPO,temp/'temp','diff-tree','-r','-z','--no-renames','--no-commit-id','--name-status',BASE,C).decode().strip('\0').split('\0')
    rows=[]; paths=[]
    for status,path in zip(fields[::2],fields[1::2]):
        paths.append(path); digest='0'*64 if status=='D' else h(git(REPO,temp/'temp','cat-file','blob',C+':'+path)); rows.append(digest+'  '+path+'\n')
    raw=''.join(sorted(rows)).encode(); req(h(raw)==EXPECTED,'manifest mismatch'); req(raw==(ROOT/'manifest.sha256').read_bytes(),'manifest rows differ')
    preservation={}
    ab=[p for p in paths if p.startswith('src/pontius/v0a/') or p in ['tests/test_v0a_contract_faults.py','tests/test_v0a_hand_replay.py','tests/test_v0a_replay.py','tests/test_v0a_trace.py']]
    other=['.github/workflows/ci.yml','tools/check_stabilization_boundaries.py','tests/test_v0a_boundaries.py']
    for ref,ps in [('ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1',ab),('00db06624ab25f10cd181badccf92c87a78f17ee',other)]:
        for p in ps:
            a=git(REPO,temp/'temp','cat-file','blob',C+':'+p); b=git(REPO,temp/'temp','cat-file','blob',ref+':'+p); req(a==b,'preservation '+p); preservation[p]={'reference':ref,'sha256':h(a)}
    delta=git(REPO,temp/'temp','diff','--no-renames','--name-only','8d240db477b8c141e6142e055dbfbedc75c6a2f8',C).decode().splitlines()
    req(set(delta)=={'tools/generate_test_inventory.py','tests/test_inventory_and_profiles.py','tests/test-inventory.json'},'actual fix delta')
    snapshot=temp/'harness'; git(temp,temp/'temp','clone','--shared','--no-checkout',str(REPO),str(snapshot)); git(snapshot,temp/'temp','checkout','--detach',C)
    hashes={p:h(git(snapshot,temp/'temp','cat-file','blob',C+':'+p)) for p in paths}
    req(all(h((snapshot/p).read_bytes())==d for p,d in hashes.items()),'checkout mismatch')
    state={'candidate':C,'manifest':EXPECTED,'snapshot':str(snapshot),'temp':str(temp/'temp'),'hashes':hashes,'preservation':preservation,'fix_delta':delta,'environment':env(temp/'temp',snapshot),'control_identity':{'executable':sys.executable,'version':sys.version},'control_sha256':h(P(__file__).read_bytes())}
    label=sys.argv[2]; jout(ROOT/'checks'/('codex-b-'+label+'-setup.json'),state)
    write(ROOT/'checks'/('codex-b-'+label+'-manifest.sha256'),raw)
    print(json.dumps(state,indent=2))
elif mode=='run':
    label,slot,kind,target,*args=sys.argv[2:]; state=json.loads((ROOT/'checks'/('codex-b-'+label+'-setup.json')).read_text()); snap=validate(P(state['snapshot'])); temp=validate(P(state['temp'])); exe,version=SLOTS[slot];validate(exe)
    req(git(snap,temp,'rev-parse','HEAD').decode().strip()==C,'HEAD mismatch')
    req(not git(snap,temp,'status','--porcelain','--untracked-files=all'),'dirty clone before')
    wrapper="""import sys,json,runpy,os,importlib.util\nfrom pathlib import Path\nexe,version,target,*args=sys.argv[1:]\nassert sys.implementation.name=='cpython' and '.'.join(map(str,sys.version_info[:3]))==version\nassert Path(sys.executable).resolve()==Path(exe).resolve()\nassert sys.flags.safe_path and sys.dont_write_bytecode and not sys.flags.optimize\nprint(json.dumps({'identity_before_imports':{'executable':sys.executable,'version':sys.version,'version_info':list(sys.version_info[:3]),'implementation':sys.implementation.name}}),flush=True)\nassert Path(importlib.util.find_spec('pontius').origin).resolve()==(Path.cwd()/'src/pontius/__init__.py').resolve()\nsys.argv=[target,*args]\nrunpy.run_path(target,run_name='__main__')\n"""
    command=[str(exe),'-B','-P','-c',wrapper,str(exe),version,target,*args]
    before={p:h((snap/p).read_bytes()) for p in state['hashes']}; req(before==state['hashes'],'source changed')
    result=subprocess.run(command,cwd=snap,env=state['environment'],capture_output=True)
    after={p:h((snap/p).read_bytes()) for p in state['hashes']}; dirty=git(snap,temp,'status','--porcelain','--untracked-files=all').decode()
    log=ROOT/'checks'/('codex-b-'+label+'-'+kind+'-'+slot+'.txt');write(log,(result.stdout+result.stderr).replace(b'\r\n',b'\n'))
    receipt={'candidate':C,'manifest':EXPECTED,'command':command,'exit':result.returncode,'environment':state['environment'],'snapshot':str(snap),'log':str(log),'log_sha256':h(log.read_bytes()),'before':before,'after':after,'dirty_after':dirty,'identity_before_imports':json.loads(result.stdout.splitlines()[0]),'control_sha256':h(P(__file__).read_bytes())}
    jout(ROOT/'checks'/('codex-b-'+label+'-'+kind+'-'+slot+'-receipt.json'),receipt)
    req(before==after and not dirty,'clone mutated')
    print(json.dumps({'log':str(log),'exit':result.returncode,'output':(result.stdout+result.stderr).decode(errors='replace')},indent=2))
else: raise RuntimeError('unknown mode')
