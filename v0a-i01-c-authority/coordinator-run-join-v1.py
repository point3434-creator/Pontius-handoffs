import hashlib,json,os,pathlib,stat,subprocess,sys,uuid
P=pathlib.Path
ROOT=P(r'D:\Pontius-handoffs\v0a-i01-c-authority')
OLD=P(r'D:\Pontius-handoffs\v0a-i01-ab\r010')
REPO=P(r'D:\Pontius'); W=P(r'D:\Pontius\engineer-authority-b4a5641b7aca4ca4a4d730c9a8a02369\harness')
G=P(r'C:\Program Files\Git\cmd\git.exe'); C='29c02f6fbd5eb0b7ddc9e816ef28f570b9839358'
SLOTS={'311':(P(r'D:\Pontius-tools\py311\Scripts\python.exe'),'3.11.15'),'314':(P(r'D:\Pontius\.venv\Scripts\python.exe'),'3.14.6')}
PROBES={'join':(ROOT/'coordinator-join-probe-v1.py','1d91f234169e17833c7a40c35674564a6b6daa687d658cb06d93dbecd7341995')}
def req(ok,message):
    if not ok: raise RuntimeError(message)
def validate(path):
    req(path.is_absolute() and '..' not in path.parts,'nonabsolute')
    for item in (path,*path.parents):
        x=item.lstat();req(not(getattr(x,'st_file_attributes',0)&stat.FILE_ATTRIBUTE_REPARSE_POINT),'reparse '+str(item))
    return path
def h(raw):return hashlib.sha256(raw).hexdigest()
def write(path,raw):
    with path.open('xb') as f:f.write(raw)
def out(path,value):write(path,(json.dumps(value,indent=2)+'\n').encode())
def env(temp,snap=None):
    win=validate(P(os.environ['SYSTEMROOT']));system=validate(win/'System32')
    e={'SYSTEMROOT':str(win),'WINDIR':str(win),'COMSPEC':str(system/'cmd.exe'),'PATH':str(system),'TEMP':str(temp),'TMP':str(temp),'PONTIUS_GIT':str(G),'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'NUL','GIT_CONFIG_SYSTEM':'NUL','GIT_ATTR_NOSYSTEM':'1','PYTHONNOUSERSITE':'1'}
    if snap:e['PYTHONPATH']=str(snap/'src')
    return e
def git(repo,temp,*args):
    validate(G)
    return subprocess.run([str(G),'-c','core.autocrlf=false','-c','core.hooksPath=NUL','-c','init.templateDir=','-c','core.attributesFile=NUL','-c','core.fsmonitor=false','-C',str(repo),*args],cwd=repo,env=env(temp),capture_output=True,check=True).stdout
req(sys.implementation.name=='cpython' and sys.version_info[:3]==(3,11,15),'control version')
req(P(sys.executable).resolve()==SLOTS['311'][0].resolve(),'control exe')
req(sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode,'control flags')
label,slot,kind=sys.argv[1:]
req(kind in PROBES,'kind')
checks=ROOT/'coordinator-checks'; checks.mkdir(exist_ok=True)
folder=REPO/('coordinator-authority-'+uuid.uuid4().hex);folder.mkdir();temp=folder/'temp';temp.mkdir();snap=folder/'harness'
validate(W/'tools/generate_test_inventory.py')
overlay=(W/'tools/generate_test_inventory.py').read_bytes()
req(h(overlay)=='33f944158ca20df62724d83d44a680440c455653100ba28d67b69954849cd8a5','issued iteration05 source changed')
git(folder,temp,'clone','--shared','--no-checkout',str(REPO),str(snap));git(snap,temp,'checkout','--detach',C)
req(not git(snap,temp,'status','--porcelain','--untracked-files=all'),'dirty initial')
rows=(OLD/'manifest.sha256').read_text().splitlines();before={}
for row in rows:
    digest,path=row.split('  ',1);raw=git(snap,temp,'cat-file','blob',C+':'+path)
    req(h(raw)==digest and (snap/path).read_bytes()==raw,'frozen bytes '+path);before[path]=digest
(snap/'tools/generate_test_inventory.py').write_bytes(overlay);before['tools/generate_test_inventory.py']=h(overlay)
exe,version=SLOTS[slot];validate(exe)
if kind in PROBES:
    target,digest=PROBES[kind];req(h(target.read_bytes())==digest,'probe changed')
else:target=snap/'tests/test_inventory_and_profiles.py';digest=h(target.read_bytes())
wrapper='''import sys,json,os,importlib.util,runpy,unittest\nfrom pathlib import Path\nexe,version,kind,target=sys.argv[1:]\nassert sys.implementation.name=='cpython' and '.'.join(map(str,sys.version_info[:3]))==version\nassert Path(sys.executable).resolve()==Path(exe).resolve()\nassert sys.flags.safe_path and sys.dont_write_bytecode and not sys.flags.optimize\nprint(json.dumps({'identity_before_imports':{'executable':sys.executable,'version':sys.version,'version_info':list(sys.version_info[:3]),'implementation':sys.implementation.name,'cwd':str(Path.cwd()),'pythonpath':os.environ.get('PYTHONPATH'),'flags':str(sys.flags)}}),flush=True)\nassert Path(importlib.util.find_spec('pontius').origin).resolve()==(Path.cwd()/'src/pontius/__init__.py').resolve()\nsys.argv=[target]\nif kind=='design':\n    namespace=runpy.run_path(target,run_name='engineer_focused_design')\n    suite=unittest.defaultTestLoader.loadTestsFromTestCase(namespace['DesignReviewTests'])\n    result=unittest.TextTestRunner(verbosity=2).run(suite)\n    raise SystemExit(not result.wasSuccessful())\nrunpy.run_path(target,run_name='__main__')\n'''
command=[str(exe),'-B','-P','-c',wrapper,str(exe),version,kind,str(target)]
setup={'candidate':C,'generator_overlay_sha256':h(overlay),'snapshot':str(snap),'temp':str(temp),'before':before,'command':command,'environment':env(temp,snap),'probe_sha256':digest,'control_sha256':h(P(__file__).read_bytes())}
out(checks/(label+'-setup.json'),setup)
result=subprocess.run(command,cwd=snap,env=env(temp,snap),capture_output=True)
raw=(result.stdout+result.stderr).replace(b'\r\n',b'\n');log=checks/(label+'.txt');write(log,raw)
after={path:h((snap/path).read_bytes()) for path in before};dirty=git(snap,temp,'status','--porcelain','--untracked-files=all').decode()
receipt={**setup,'exit':result.returncode,'log':str(log),'log_sha256':h(raw),'after':after,'dirty_after':dirty,'identity_before_imports':json.loads(result.stdout.splitlines()[0])}
out(checks/(label+'-receipt.json'),receipt)
req(before==after,'snapshot mutation');req(dirty.strip()=='M tools/generate_test_inventory.py','unexpected dirty '+dirty)
print(json.dumps({'label':label,'exit':result.returncode,'log':str(log),'overlay_sha256':h(overlay),'tail':raw.decode(errors='replace')[-5000:]},indent=2))
