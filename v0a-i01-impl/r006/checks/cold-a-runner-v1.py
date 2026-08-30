import sys
expected_executable, expected_version, mode = sys.argv[1:4]
print('executable=' + sys.executable, flush=True)
print('implementation=' + sys.implementation.name, flush=True)
print('full_version=' + sys.version, flush=True)
assert sys.executable.lower().replace('/', '\\') == expected_executable.lower().replace('/', '\\')
assert sys.implementation.name == 'cpython'
assert '.'.join(map(str, sys.version_info[:3])) == expected_version
assert sys.version_info.releaselevel == 'final' and sys.version_info.serial == 0
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
SNAPSHOT = Path(r'D:\pontius-snapshots\v0a-r006-cold-a-98fee7dce06d4fcca2da4475c550b928\harness')
PACKET = Path(r'D:\Pontius-handoffs\v0a-i01-impl\r006')
GIT = r'C:\Program Files\Git\cmd\git.exe'
assert Path.cwd() == SNAPSHOT
assert os.environ['PYTHONPATH'] == str(SNAPSHOT / 'src')
assert os.environ['PONTIUS_GIT'] == GIT
assert not any(k.startswith('GIT_') for k in os.environ)
assert not any(k.startswith('PYTHON') and k not in {'PYTHONPATH', 'PYTHONDONTWRITEBYTECODE', 'PYTHONNOUSERSITE'} for k in os.environ)
print('cwd=' + str(Path.cwd()))
print('environment=' + json.dumps(dict(os.environ), sort_keys=True))
print('sys_path=' + json.dumps(sys.path))
def git(*args):
    return subprocess.run([GIT, *args], check=True, capture_output=True).stdout
if mode == 'manifest':
    candidate = json.loads((PACKET / 'candidate.json').read_text(encoding='utf-8'))
    commit = candidate['commit']
    assert commit == 'c74b80628a89938ca585ef3240b5c267a7174d0f'
    assert git('rev-parse', 'HEAD').decode().strip() == commit
    assert git('rev-parse', commit + '^').decode().strip() == candidate['base']
    assert git('rev-parse', commit + '^{tree}').decode().strip() == candidate['tree']
    status = git('status', '--porcelain=v1')
    assert status == b'', status
    fields = git('diff-tree', '-r', '-z', '--no-commit-id', '--no-renames', '--name-status', commit + '^', commit).decode('utf-8').split('\0')
    rows = []
    for index in range(0, len(fields) - 1, 2):
        change, path = fields[index:index + 2]
        if not change:
            continue
        if change == 'D':
            digest = '0' * 64
        else:
            blob = git('cat-file', 'blob', f'{commit}:{path}')
            digest = hashlib.sha256(blob).hexdigest()
            checkout = (SNAPSHOT / path).read_bytes()
            assert checkout.replace(b'\r\n', b'\n') == blob.replace(b'\r\n', b'\n'), path
        rows.append(f'{digest}  {path}\n'.encode('utf-8'))
    manifest = b''.join(sorted(rows))
    assert hashlib.sha256(manifest).hexdigest() == candidate['manifest_sha256']
    assert manifest == (PACKET / 'manifest.sha256').read_bytes()
    print('manifest_sha256=' + hashlib.sha256(manifest).hexdigest())
    print('rows=' + str(len(rows)))
    print('delta_r005=' + git('diff', '--no-renames', '--name-status', 'a8582e6d6b53b55415dab79c4a54e252d00b74ad', commit).decode().strip())
    print('VERIFIED: blob identity, parent, tree, clean snapshot, in-memory normalized checkout equality')
elif mode == 'suite':
    import pontius.v0a.replay as replay
    import pontius.v0a.runtime as runtime
    for module in (replay, runtime):
        assert Path(module.__file__).resolve().is_relative_to(SNAPSHOT / 'src')
        print('module=' + module.__name__ + ':' + module.__file__)
    test = sys.argv[4]
    assert test in {'test_v0a_replay.py', 'test_v0a_hand_replay.py', 'test_v0a_trace.py', 'test_v0a_contract_faults.py'}
    sys.argv = [str(SNAPSHOT / 'tests' / test)]
    runpy.run_path(sys.argv[0], run_name='__main__')
else:
    raise AssertionError(mode)
