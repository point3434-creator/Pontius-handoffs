import hashlib, json, os, pathlib, stat, subprocess, sys, uuid
assert sys.version_info[:3] == (3,11,15), sys.version
assert pathlib.Path(sys.executable).resolve() == pathlib.Path(r'D:\Pontius-tools\py311\Scripts\python.exe').resolve(), sys.executable
assert sys.flags.safe_path and sys.dont_write_bytecode
GIT = pathlib.Path(r'C:\Program Files\Git\cmd\git.exe')
s = GIT.lstat()
assert GIT.is_absolute() and stat.S_ISREG(s.st_mode) and not (s.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
packet = pathlib.Path(r'D:\Pontius-handoffs\v0a-i01-ab\r008')
checks = packet / 'checks'
checks.mkdir(exist_ok=True)
root = pathlib.Path(r'D:\Pontius-review-snapshots') / ('codex-a-r008-' + uuid.uuid4().hex)
root.mkdir(parents=True)
tmp = root / 'temp'
tmp.mkdir()
env = {key: os.environ[key] for key in ('SystemRoot','WINDIR','COMSPEC') if key in os.environ}
env.update(TEMP=str(tmp), TMP=str(tmp), PONTIUS_GIT=str(GIT), PYTHONDONTWRITEBYTECODE='1', PYTHONSAFEPATH='1', GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
def git(*args):
    r = subprocess.run([str(GIT), *args], cwd=root, env=env, capture_output=True, check=True)
    return r.stdout
candidate='00db06624ab25f10cd181badccf92c87a78f17ee'
base='d1ed3cbda6107d61ea8e77133871720af04970cd'
snapshot = root/'snapshot'
git('-c','core.autocrlf=false','clone','--no-hardlinks','--no-checkout','--quiet',r'D:\Pontius',str(snapshot))
git('-C',str(snapshot),'-c','core.autocrlf=false','checkout','--detach','--quiet',candidate)
assert git('-C',str(snapshot),'rev-parse','HEAD').decode().strip() == candidate
assert git('-C',str(snapshot),'rev-parse',candidate+'^').decode().strip() == base
paths=git('-C',str(snapshot),'diff','--name-only','--no-renames','-z',base,candidate).decode().split('\0')[:-1]
rows=[]
for path in paths:
    raw=git('-C',str(snapshot),'cat-file','blob',candidate+':'+path)
    rows.append(hashlib.sha256(raw).hexdigest()+'  '+path+'\n')
manifest=''.join(sorted(rows)).encode()
assert manifest == (packet/'manifest.sha256').read_bytes()
assert hashlib.sha256(manifest).hexdigest() == '1e5814b2c04a0065586d8fa73f89edc1ffb0eae4830bea8c893630172d5798f2'
assert hashlib.sha256((packet/'acceptance.md').read_bytes()).hexdigest() == '19457c5653e25555d362a50e7e366599542812d38098fb7f5e614060b4bdda62'
ab=[p for p in paths if p.startswith('src/pontius/v0a/') or (p.startswith('tests/test_v0a_') and not p.endswith('boundaries.py'))]
assert len(ab)==10
for path in ab:
    assert git('-C',str(snapshot),'cat-file','blob',candidate+':'+path)==git('-C',str(snapshot),'cat-file','blob','ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1:'+path),path
assert git('-C',str(snapshot),'rev-parse','HEAD:docs/architecture/dependency-baseline.toml').decode().strip()=='5fe6ee47f3380b65887b528efef05b72c8e6ac0a'
assert not git('-C',str(snapshot),'status','--porcelain','--untracked-files=all')
receipt={'candidate':candidate,'base':base,'manifest_sha256':hashlib.sha256(manifest).hexdigest(),'paths':paths,'ab_equal_r007':ab,'snapshot':str(snapshot),'temp':str(tmp),'interpreter':sys.executable,'version':sys.version,'git':str(GIT),'scrubbed_environment':env,'acceptance_sha256':hashlib.sha256((packet/'acceptance.md').read_bytes()).hexdigest()}
with (checks/'codex-a-02-identity.json').open('x',encoding='utf-8',newline='\n') as f: json.dump(receipt,f,indent=2); f.write('\n')
print(json.dumps(receipt,indent=2))