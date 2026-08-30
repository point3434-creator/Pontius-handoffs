import json, os, pathlib, platform, runpy, subprocess, sys
root=pathlib.Path.cwd()
assert platform.python_implementation()=='CPython'
assert platform.python_version()==os.environ['COLD_B_EXPECTED_VERSION']
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert os.environ['PYTHONPATH']==str(root/'src') and os.environ['PATH']==''
print(json.dumps({'implementation':platform.python_implementation(),'version':platform.python_version(),
 'executable':sys.executable,'cwd':str(root),'B':sys.flags.dont_write_bytecode,
 'P':sys.flags.safe_path,'PYTHONPATH':os.environ['PYTHONPATH'],'git':os.environ['PONTIUS_GIT']}),flush=True)
try:
 runpy.run_path(str(root/'tests/test_v0a_hand_replay.py'),run_name='__main__')
finally:
 origins={name:mod.__file__ for name,mod in sys.modules.items()
          if name.startswith('pontius') and getattr(mod,'__file__',None)}
 assert all(pathlib.Path(path).is_relative_to(root/'src') for path in origins.values())
 clean=subprocess.run([os.environ['PONTIUS_GIT'],'-C',str(root),'status','--porcelain=v1'],
                      check=True,capture_output=True).stdout
 assert clean==b'',clean
 print(json.dumps({'origins':origins,'snapshot_clean':True}),flush=True)
