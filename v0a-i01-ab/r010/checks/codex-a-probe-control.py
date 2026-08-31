import hashlib, json, os, stat, subprocess, sys, uuid
from pathlib import Path
C='29c02f6fbd5eb0b7ddc9e816ef28f570b9839358'
B='d1ed3cbda6107d61ea8e77133871720af04970cd'
G=Path(r'C:\Program Files\Git\cmd\git.exe')
R=Path(r'D:\Pontius-handoffs\v0a-i01-ab\r010')
REPO=Path(r'D:\Pontius')
SLOTS={'311':(r'D:\Pontius-tools\py311\Scripts\python.exe','3.11.15'),'314':(r'D:\Pontius\.venv\Scripts\python.exe','3.14.6')}
def checked(p,directory=False):
    p=Path(p)
    assert p.is_absolute() and '..' not in p.parts
    for a in (p,*p.parents):
        assert not a.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT,a
    assert p.is_dir() if directory else p.is_file()
    return p
assert sys.implementation.name=='cpython' and sys.version_info[:3]==(3,11,15)
assert Path(sys.executable).resolve()==Path(SLOTS['311'][0]).resolve()
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
checked(G)
def env(temp,snap=None):
    win=checked(os.environ['SYSTEMROOT'],True)
    d={'SYSTEMROOT':str(win),'WINDIR':str(win),'COMSPEC':str(win/'System32/cmd.exe'),'PATH':str(win/'System32'),'TEMP':str(temp),'TMP':str(temp),'PONTIUS_GIT':str(G),'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'NUL','GIT_CONFIG_SYSTEM':'NUL','GIT_ATTR_NOSYSTEM':'1','PYTHONNOUSERSITE':'1'}
    if snap:d['PYTHONPATH']=str(snap/'src')
    return d
def gb(repo,temp,*args):
    return subprocess.run([str(G),'-c','core.autocrlf=false','-c','core.hooksPath=NUL','-c','init.templateDir=','-c','core.attributesFile=NUL','-c','core.fsmonitor=false','-C',str(repo),*args],cwd=repo,env=env(temp),capture_output=True,check=True).stdout
def create(p,b):
    with Path(p).open('xb') as f:f.write(b)
def sha(b):return hashlib.sha256(b).hexdigest()
def js(p,obj):create(p,(json.dumps(obj,indent=2)+'\n').encode())
def hashes(snap,paths):return {p:sha((snap/p).read_bytes()) for p in paths}
WRAPPER='''import sys,json,runpy,os,importlib.util
from pathlib import Path
exe,version,target,*args=sys.argv[1:]
assert sys.implementation.name=='cpython'
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert '.'.join(map(str,sys.version_info[:3]))==version
assert sys.flags.safe_path and sys.dont_write_bytecode and not sys.flags.optimize
print(json.dumps({'identity_before_import':{'executable':sys.executable,'implementation':sys.implementation.name,'version':sys.version,'version_info':list(sys.version_info[:3]),'cwd':str(Path.cwd()),'pythonpath':os.environ.get('PYTHONPATH')}}),flush=True)
assert Path(importlib.util.find_spec('pontius.v0a.trace').origin).resolve()==(Path.cwd()/'src/pontius/v0a/trace.py').resolve()
sys.argv=[target,*args]
runpy.run_path(target,run_name='__main__')
'''
mode=sys.argv[1]
meta=R/'checks/codex-a-probe-snapshot.json'
if mode=='init':
    create(R/'checks/codex-a-probe-control.py',Path(__file__).read_bytes())
    parent=Path(r'D:\pontius-snapshots')/('codex-a-r010-probe-'+uuid.uuid4().hex)
    parent.mkdir();temp=parent/'temp';temp.mkdir();snap=parent/'snapshot'
    gb(parent,temp,'clone','--shared','--no-checkout',str(REPO),str(snap))
    gb(snap,temp,'checkout','--detach',C)
    assert gb(snap,temp,'rev-parse','HEAD').decode().strip()==C
    changes=gb(snap,temp,'diff','--no-renames','--name-status','-z',B,C).decode().split('\0')
    rows=[];paths=[]
    for i in range(0,len(changes)-1,2):
        status,p=changes[i:i+2];paths.append(p)
        h='0'*64 if status=='D' else sha(gb(snap,temp,'cat-file','blob',C+':'+p))
        rows.append(h+'  '+p+'\n')
    raw=''.join(sorted(rows)).encode()
    assert sha(raw)=='8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb'
    assert raw==(R/'manifest.sha256').read_bytes()
    create(R/'checks/codex-a-recomputed-manifest.sha256',raw)
    preserved={}
    for p in paths:
        if p.startswith('src/pontius/v0a/') or (p.startswith('tests/test_v0a_') and p!='tests/test_v0a_boundaries.py'):ref='ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1'
        elif p in ('.github/workflows/ci.yml','tools/check_stabilization_boundaries.py','tests/test_v0a_boundaries.py'):ref='00db06624ab25f10cd181badccf92c87a78f17ee'
        else:continue
        assert gb(snap,temp,'cat-file','blob',ref+':'+p)==gb(snap,temp,'cat-file','blob',C+':'+p)
        preserved[p]=ref
    assert len(paths)==17 and len(preserved)==13
    fix=gb(snap,temp,'diff','--name-only','8d240db477b8c141e6142e055dbfbedc75c6a2f8',C).decode().splitlines()
    assert fix==['tests/test-inventory.json','tests/test_inventory_and_profiles.py','tools/generate_test_inventory.py']
    assert gb(snap,temp,'rev-parse',C+':docs/architecture/dependency-baseline.toml').decode().strip()=='5fe6ee47f3380b65887b528efef05b72c8e6ac0a'
    allpaths=gb(snap,temp,'ls-tree','-r','--name-only',C).decode().splitlines();h=hashes(snap,allpaths)
    js(meta,{'candidate':C,'snapshot':str(snap),'temporary':str(temp),'paths':paths,'all_hashes':h,'manifest':sha(raw),'preserved':preserved,'fix_paths':fix,'control_version':sys.version,'control_executable':sys.executable})
    print(json.dumps({'snapshot':str(snap),'meta':str(meta),'meta_sha256':sha(meta.read_bytes()),'manifest':sha(raw),'preserved':len(preserved),'all_paths':len(allpaths)}))
elif mode=='run':
    data=json.loads(meta.read_text());snap=checked(data['snapshot'],True);temp=checked(data['temporary'],True)
    slot,label,target,*args=sys.argv[2:];assert slot in SLOTS and label.startswith('codex-a-')
    assert data['candidate']==C and gb(snap,temp,'rev-parse','HEAD').decode().strip()==C
    before=hashes(snap,data['all_hashes']);assert before==data['all_hashes']
    exe,version=SLOTS[slot];checked(exe)
    cmd=[exe,'-B','-P','-c',WRAPPER,exe,version,target,*args]
    result=subprocess.run(cmd,cwd=snap,env=env(temp,snap),capture_output=True)
    log=R/'checks'/(label+'-'+slot+'.txt');create(log,(result.stdout+result.stderr).replace(b'\r\n',b'\n'))
    after=hashes(snap,data['all_hashes']);assert after==before
    identity=json.loads(result.stdout.splitlines()[0])['identity_before_import']
    assert identity['version_info']==list(map(int,version.split('.')))
    receipt={'candidate':C,'manifest':data['manifest'],'snapshot':str(snap),'command':cmd,'environment':env(temp,snap),'identity':identity,'exit':result.returncode,'log':str(log),'log_sha256':sha(log.read_bytes()),'all_tracked_paths_unchanged':len(after),'control_sha256':sha(Path(__file__).read_bytes())}
    out=R/'checks'/(label+'-'+slot+'-receipt.json');js(out,receipt)
    print(json.dumps({'receipt':str(out),'exit':result.returncode,'log_sha256':receipt['log_sha256']}))
    sys.exit(result.returncode)
else:raise ValueError(mode)
