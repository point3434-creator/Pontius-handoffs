import importlib.util, json, os, pathlib, runpy, stat, sys
version, rootarg, target, *args = sys.argv[1:]
root=pathlib.Path(rootarg).resolve()
expected={'3.11.15':r'D:\Pontius-tools\py311\Scripts\python.exe','3.14.6':r'D:\Pontius\.venv\Scripts\python.exe'}[version]
assert '.'.join(map(str,sys.version_info[:3]))==version,sys.version
assert pathlib.Path(sys.executable).resolve()==pathlib.Path(expected).resolve(),sys.executable
assert sys.flags.safe_path and sys.dont_write_bytecode
assert pathlib.Path.cwd().resolve()==root
assert os.environ['PYTHONPATH']==str(root/'src')
assert pathlib.Path(os.environ['TEMP']).drive.upper()=='D:'
git=pathlib.Path(os.environ['PONTIUS_GIT']); info=git.lstat()
assert git.is_absolute() and stat.S_ISREG(info.st_mode) and not(info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
assert pathlib.Path(importlib.util.find_spec('pontius').origin).resolve()==root/'src'/'pontius'/'__init__.py'
print(json.dumps({'python':sys.executable,'full_version':sys.version,'cwd':str(root),'argv':sys.argv,'env':dict(os.environ),'pontius_origin':importlib.util.find_spec('pontius').origin}),flush=True)
sys.argv=[target,*args]
exitcode=0
try: runpy.run_path(target,run_name='__main__')
except SystemExit as e: exitcode=e.code
origins={}
for name,module in list(sys.modules.items()):
    if name=='pontius' or name.startswith('pontius.v0a'):
        value=getattr(module,'__file__',None)
        if value:
            resolved=pathlib.Path(value).resolve()
            assert resolved.is_relative_to(root/'src'),(name,value)
            origins[name]=str(resolved)
print(json.dumps({'payload_exit':exitcode,'verified_payload_origins':origins}),flush=True)
raise SystemExit(exitcode)