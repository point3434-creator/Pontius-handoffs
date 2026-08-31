import hashlib, json, os, re, stat, subprocess, sys, uuid
from pathlib import Path
ROOT = Path(r'D:\Pontius-handoffs\v0a-i01-ab')
ROUND = ROOT / 'r009'
CHECKS = ROUND / 'checks'
REPO = Path(r'D:\Pontius')
GIT = Path(r'C:\Program Files\Git\cmd\git.exe')
COMMIT = '8d240db477b8c141e6142e055dbfbedc75c6a2f8'
BASE = 'd1ed3cbda6107d61ea8e77133871720af04970cd'
FIXBASE = '00db06624ab25f10cd181badccf92c87a78f17ee'
ABBASE = 'ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1'
MANIFEST = '4f91aa7ce728c3eff6a7ad30a7c131985d5b86b615875df978d30ac39386aa51'
META = ROOT / 'cold-r009-a-snapshot.json'
SLOTS = {'311': (r'D:\Pontius-tools\py311\Scripts\python.exe','3.11.15'), '314': (r'D:\Pontius\.venv\Scripts\python.exe','3.14.6')}
def require(ok, reason):
    if not ok: raise RuntimeError(reason)
def checked(p, directory=False):
    p = Path(p)
    require(p.is_absolute() and '..' not in p.parts, 'unsafe path')
    for q in (p,*p.parents):
        require(not (q.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT), 'reparse path '+str(q))
    require(p.is_dir() if directory else p.is_file(), 'path kind '+str(p))
    return p
def sha(b): return hashlib.sha256(b).hexdigest()
def create(p, data):
    with p.open('x', encoding='utf-8', newline='\n') as f: f.write(data)
def jsoncreate(p, value): create(p,json.dumps(value,indent=2)+'\n')
def env(temp,snapshot=None):
    windows=checked(os.environ['SYSTEMROOT'],True)
    e={'SYSTEMROOT':str(windows),'WINDIR':str(windows),'COMSPEC':str(windows/'System32/cmd.exe'),'PATH':str(windows/'System32'),'TEMP':str(temp),'TMP':str(temp),'PONTIUS_GIT':str(GIT),'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'NUL','GIT_CONFIG_SYSTEM':'NUL','GIT_ATTR_NOSYSTEM':'1','PYTHONNOUSERSITE':'1'}
    if snapshot: e['PYTHONPATH']=str(snapshot/'src')
    return e
def git(repo,temp,*args):
    checked(GIT)
    c=[str(GIT),'-c','core.autocrlf=false','-c','core.hooksPath=NUL','-c','init.templateDir=','-c','core.attributesFile=NUL','-c','core.fsmonitor=false','-C',str(repo),*args]
    return subprocess.run(c,cwd=repo,env=env(temp),capture_output=True,check=True).stdout
def paths_changed(repo,temp,base,commit):
    return git(repo,temp,'diff','--name-only','--no-renames','-z',base,commit).decode().strip('\0').split('\0')
def blob(repo,temp,commit,p): return git(repo,temp,'cat-file','blob',commit+':'+p)
def prepare():
    require(not META.exists(),'already prepared')
    parent=Path(r'D:\pontius-snapshots')/('cold-r009-a-'+uuid.uuid4().hex)
    parent.mkdir(); temp=parent/'temp'; temp.mkdir(); snap=parent/'harness'
    git(parent,temp,'clone','--shared','--no-checkout',str(REPO),str(snap))
    git(snap,temp,'checkout','--detach',COMMIT)
    require(git(snap,temp,'rev-parse','HEAD').decode().strip()==COMMIT,'wrong HEAD')
    require(git(snap,temp,'rev-parse',COMMIT+'^').decode().strip()==BASE,'wrong parent')
    require(git(snap,temp,'rev-parse','refs/remotes/origin/review/v0a-i01-ab/r009').decode().strip()==COMMIT,'wrong ref')
    paths=paths_changed(snap,temp,BASE,COMMIT)
    hashes={p:sha(blob(snap,temp,COMMIT,p)) for p in paths}
    raw=''.join(sorted(h+'  '+p+'\n' for p,h in hashes.items())).encode()
    require(sha(raw)==MANIFEST and raw==(ROUND/'manifest.sha256').read_bytes(),'manifest mismatch')
    require(len(paths)==17,'wrong full manifest paths')
    delta=paths_changed(snap,temp,FIXBASE,COMMIT)
    require(set(delta)=={'tests/test-inventory.json','tests/test_inventory_and_profiles.py','tools/generate_test_inventory.py'},'FIX scope')
    preserved=[p for p in paths if p.startswith('src/pontius/v0a/') or (p.startswith('tests/test_v0a_') and p!='tests/test_v0a_boundaries.py')]
    require(len(preserved)==10,'wrong preservation set')
    require(all(blob(snap,temp,ABBASE,p)==blob(snap,temp,COMMIT,p) for p in preserved),'A/B differs')
    require(all(sha((snap/p).read_bytes())==h for p,h in hashes.items()),'checkout differs from blobs')
    pins={'acceptance.md':'81970ee7f14b028800e498b42be607060cefd34e5f7395e80af6ce9ecb96bf54','protocol-interpretation.md':'529fece988fad57871d165b0347ca655eb51a8101462668cd5bb84e5e476a69a','inputs/CLAUDE.md':'af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76','inputs/workflow.md':'d9de38ede87fb619b3045a60ee7fab137ae23ba3b580c0a6d6b3ca14e567a170'}
    require(all(sha((ROUND/p).read_bytes())==h for p,h in pins.items()),'input pin mismatch')
    require(sha((ROOT/'snapshot-run-abc-v2.py').read_bytes())=='62bf07eb88845dfc30c3820aeb8c899ccfbe8111d811192485e2826a5ecfc20c','infrastructure pin mismatch')
    data={'candidate':COMMIT,'base':BASE,'manifest_sha256':MANIFEST,'snapshot':str(snap),'temporary':str(temp),'source_sha256':hashes,'fix_delta':delta,'AB_preserved':preserved,'input_sha256':pins}
    jsoncreate(META,data); jsoncreate(CHECKS/'codex-a-identity.json',data)
    print(json.dumps(data,indent=2))
WRAPPER = r'''import sys,runpy,json,importlib.util
from pathlib import Path
exe,version,target,*args=sys.argv[1:]
assert sys.implementation.name=='cpython'
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert '.'.join(map(str,sys.version_info[:3]))==version
assert sys.flags.safe_path and sys.dont_write_bytecode and not sys.flags.optimize
print(json.dumps({'identity_before_payload_import':{'executable':sys.executable,'version':sys.version,'version_info':list(sys.version_info[:3])}}),flush=True)
assert Path(importlib.util.find_spec('pontius').origin).resolve()==(Path.cwd()/'src/pontius/__init__.py').resolve()
sys.argv=[target,*args]
runpy.run_path(target,run_name='__main__')
'''
def run(slot,label,target,*args):
    require(re.fullmatch('[a-z0-9-]+',label) is not None,'label')
    require(slot in SLOTS,'slot')
    setup=json.loads(META.read_bytes()); snap=checked(setup['snapshot'],True); temp=checked(setup['temporary'],True)
    before={p:sha((snap/p).read_bytes()) for p in setup['source_sha256']}
    require(before==setup['source_sha256'],'source differs before run')
    require(git(snap,temp,'rev-parse','HEAD').decode().strip()==COMMIT,'HEAD changed')
    targetpath=Path(target)
    require(target in {'tools/generate_test_inventory.py','tests/test_inventory_and_profiles.py','tests/test_v0a_boundaries.py','tests/test_v0a_hand_replay.py','tests/test_v0a_trace.py','tests/test_v0a_replay.py','tests/test_v0a_contract_faults.py'} or (targetpath.parent==CHECKS and targetpath.name.startswith('codex-a-probe-')),'target not focused/assigned')
    if slot=='314':
        require((CHECKS/('codex-a-'+label+'-311-receipt.json')).exists(),'floor must run first for target')
    exe,version=SLOTS[slot]; checked(exe)
    command=[exe,'-B','-P','-c',WRAPPER,exe,version,target,*args]
    result=subprocess.run(command,cwd=snap,env=env(temp,snap),capture_output=True,timeout=240)
    logfile=CHECKS/('codex-a-'+label+'-'+slot+'.txt'); create(logfile,(result.stdout+result.stderr).decode('utf-8',errors='replace').replace('\r\n','\n'))
    after={p:sha((snap/p).read_bytes()) for p in before}
    require(before==after,'source mutated')
    jsoncreate(CHECKS/('codex-a-'+label+'-'+slot+'-receipt.json'),{'candidate':COMMIT,'manifest_sha256':MANIFEST,'command':command,'environment':env(temp,snap),'exit':result.returncode,'log_sha256':sha(logfile.read_bytes()),'source_unchanged':True,'snapshot':str(snap),'control_executable':sys.executable,'control_version':sys.version})
    print(json.dumps({'exit':result.returncode,'log':str(logfile),'stdout':result.stdout.decode(errors='replace')[-8000:],'stderr':result.stderr.decode(errors='replace')[-12000:]}))
    return result.returncode
if __name__=='__main__':
    require(sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode,'control flags')
    require(Path(sys.executable).resolve()==Path(SLOTS['311'][0]).resolve(),'control exe')
    require(sys.version_info[:3]==(3,11,15),'control version')
    if sys.argv[1]=='prepare': prepare()
    elif sys.argv[1]=='run': sys.exit(run(*sys.argv[2:]))
    else: raise RuntimeError('mode')