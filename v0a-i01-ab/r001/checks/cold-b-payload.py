import sys
expected = tuple(map(int, sys.argv[1].split('.')))
assert sys.implementation.name == 'cpython', sys.implementation.name
assert sys.version_info[:3] == expected, sys.version
assert sys.flags.safe_path and sys.dont_write_bytecode
import json, os, pathlib, runpy
root = pathlib.Path(sys.argv[2]).resolve()
target = pathlib.Path(sys.argv[3]).resolve()
assert pathlib.Path.cwd().resolve() == root
assert os.environ['PYTHONPATH'] == str(root / 'src')
assert os.environ['PONTIUS_GIT'] == r'C:\Program Files\Git\cmd\git.exe'
assert not any(k in os.environ for k in ('PATH', 'PYTHONHOME', 'VIRTUAL_ENV', 'GIT_DIR', 'GIT_WORK_TREE'))
print(json.dumps({'identity_before_payload':True,'version':sys.version,'executable':sys.executable,'cwd':str(root),'argv':sys.argv,'env':dict(os.environ)}), flush=True)
import pontius.v0a.clock as clock_module
import pontius.v0a.runtime as runtime_module
import pontius.v0a.replay as replay_module
for module in (clock_module, runtime_module, replay_module):
    assert pathlib.Path(module.__file__).resolve().is_relative_to(root / 'src')
print(json.dumps({'resolved_payloads':[m.__file__ for m in (clock_module,runtime_module,replay_module)]}), flush=True)
sys.argv = [str(target), *sys.argv[4:]]
runpy.run_path(str(target), run_name='__main__')
