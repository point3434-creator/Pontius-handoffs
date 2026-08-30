import sys
from pathlib import Path
import json
import os
import platform
import hashlib
import subprocess
import runpy

exe, version, snapshot, target = sys.argv[1:5]
root = Path(snapshot)
expected = tuple(map(int, version.split('.')))
assert Path(sys.executable).is_absolute()
assert os.path.normcase(os.path.abspath(sys.executable)) == os.path.normcase(os.path.abspath(exe)), (sys.executable, exe)
assert tuple(sys.version_info[:3]) == expected, (sys.version, expected)
assert platform.python_implementation() == 'CPython'
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert Path.cwd() == root, (Path.cwd(), root)
assert os.environ['PYTHONPATH'] == str(root / 'src')
git = os.environ['PONTIUS_GIT']
assert git == r'C:\Program Files\Git\cmd\git.exe' and Path(git).is_file()
print(json.dumps({'identity': {'executable': sys.executable, 'version': sys.version, 'implementation': platform.python_implementation(), 'cwd': str(root), 'pythonpath': os.environ['PYTHONPATH'], 'git': git, 'safe_path': sys.flags.safe_path, 'dont_write_bytecode': sys.flags.dont_write_bytecode, 'environment_keys': sorted(os.environ)}}), flush=True)

if target == 'identity':
    commit = '0207430a37e1e5b31c8da8da7aa57da1bc5c88ee'
    def command(repo, *args):
        return subprocess.run([git, '-C', str(repo), *args], capture_output=True, check=True).stdout
    assert command(root, 'rev-parse', 'HEAD').decode().strip() == commit
    assert command(root, 'status', '--short', '--untracked-files=all') == b''
    assert command(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == 'c5cf6cc281d2800727029737fd4ee05bd20ebbd3'
    ref_value = command(Path(r'D:\Pontius'), 'rev-parse', 'refs/heads/review/v0a-i01-impl/r004').decode().strip()
    assert ref_value == commit, ref_value
    fields = command(root, 'diff-tree', '-r', '-z', '--no-commit-id', '--no-renames', '--name-status', commit + '^', commit).decode('utf-8', 'surrogateescape').split('\0')
    rows=[]
    for i in range(0, len(fields)-1, 2):
        status, path = fields[i], fields[i+1]
        digest = '0'*64 if status[0] == 'D' else hashlib.sha256(command(root, 'cat-file', 'blob', commit+':'+path)).hexdigest()
        rows.append(f'{digest}  {path}\n')
    manifest = ''.join(sorted(rows)).encode('utf-8')
    expected_digest='ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef'
    assert hashlib.sha256(manifest).hexdigest() == expected_digest
    assert manifest == Path(r'D:\Pontius-handoffs\v0a-i01-impl\r004\manifest.sha256').read_bytes()
    print(json.dumps({'frozen_pair': {'ref': 'refs/heads/review/v0a-i01-impl/r004', 'commit': commit, 'manifest_sha256': expected_digest, 'rows': len(rows), 'clean': True}}), flush=True)
else:
    import pontius.v0a.runtime as runtime
    import pontius.v0a.replay as replay
    assert Path(runtime.__file__).resolve() == (root/'src/pontius/v0a/runtime.py').resolve()
    assert Path(replay.__file__).resolve() == (root/'src/pontius/v0a/replay.py').resolve()
    print(json.dumps({'payload': target, 'runtime': runtime.__file__, 'replay': replay.__file__}), flush=True)
    sys.argv = [target]
    runpy.run_path(target, run_name='__main__')
