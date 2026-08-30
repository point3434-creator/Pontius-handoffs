import hashlib, json, os, pathlib, platform, subprocess, sys
root=pathlib.Path.cwd()
commit='c6adbcaa048988361d2388970eaca772711b797b'
base='30df7bce8da51715e6f1d7576892dd689421c516'
expected='a810c89b7342fb1bcb4f1498fdcf53cd11a589b70424c7da48f6619a45da67cb'
git=os.environ['PONTIUS_GIT']
assert platform.python_implementation()=='CPython'
assert platform.python_version()==os.environ['COLD_B_EXPECTED_VERSION']
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert os.environ['PYTHONPATH']==str(root/'src')
assert os.path.isabs(git) and pathlib.Path(git).is_file()
assert not pathlib.Path(git).stat().st_file_attributes & 0x400
assert os.environ['PATH']==''
def run(*args):
 return subprocess.run([git,'-C',str(root),*args],check=True,capture_output=True).stdout
assert run('rev-parse','HEAD').strip().decode()==commit
assert run('rev-parse',commit+'^').strip().decode()==base
assert run('rev-parse',commit+'^{tree}').strip().decode()=='1b6edef1e943483e0a83ec33f1bcc61348ada166'
f=run('diff-tree','-r','-z','--no-renames','--no-commit-id','--name-status',base,commit).decode().split('\0')
rows=[]
for i in range(0,len(f)-1,2):
 status,path=f[i],f[i+1]
 blob=run('cat-file','blob',f'{commit}:{path}') if status!='D' else None
 digest=hashlib.sha256(blob).hexdigest() if blob is not None else '0'*64
 rows.append(f'{digest}  {path}\n')
 assert (root/path).read_bytes()==blob, path
manifest=''.join(sorted(rows)).encode()
assert hashlib.sha256(manifest).hexdigest()==expected
packet=pathlib.Path('D:/Pontius-handoffs/v0a-i01-ab/r004')
assert (packet/'manifest.sha256').read_bytes()==manifest
assert run('status','--porcelain=v1')==b''
print(json.dumps({'implementation':platform.python_implementation(),'version':platform.python_version(),'executable':sys.executable,'cwd':str(root),'sys_path':sys.path,'flags':{'B':sys.flags.dont_write_bytecode,'P':sys.flags.safe_path},'commit':commit,'base':base,'manifest':expected,'rows':rows,'clean':True},indent=2))
