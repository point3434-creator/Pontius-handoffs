"""Independent cold A runner; stdlib only until environment is verified."""
import hashlib
import json
import os
from pathlib import Path
import platform
import runpy
import subprocess
import sys

PACKET = Path(r'D:\Pontius-handoffs\v0a-i01-ab\r003')
SNAPSHOT = Path(r'D:\pontius-snapshots\v0a-i01-ab-r003-cold-a-20260830')
GIT = r'C:\Program Files\Git\cmd\git.exe'
COMMIT = '30df7bce8da51715e6f1d7576892dd689421c516'
BASE = '2f4287f68a83fac4225a05a91daffdb3f2977a43'
MANIFEST = '21d9686c9918d9d0648fd98edf35219dfb5e0b4dc1dcfe5e4f28171b7d94e513'
phase, expected = sys.argv[1:3]
assert platform.python_implementation() == 'CPython'
assert platform.python_version() == expected, sys.version
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert Path.cwd().resolve() == SNAPSHOT.resolve()
assert os.environ['PYTHONPATH'] == str(SNAPSHOT / 'src')
assert os.environ['PONTIUS_GIT'] == GIT
allowed = {'SYSTEMROOT', 'WINDIR', 'COMSPEC', 'TEMP', 'TMP', 'PYTHONPATH',
           'PYTHONNOUSERSITE', 'PYTHONDONTWRITEBYTECODE', 'PONTIUS_GIT'}
assert set(os.environ) <= allowed, set(os.environ) - allowed
metadata = {'implementation': platform.python_implementation(), 'version': sys.version,
            'executable': sys.executable, 'cwd': str(Path.cwd()),
            'safe_path': sys.flags.safe_path, 'dont_write_bytecode': sys.dont_write_bytecode,
            'environment': dict(os.environ), 'snapshot_commit': COMMIT}
print(json.dumps({'environment_verified': metadata}), flush=True)

def git(*args):
    return subprocess.run([GIT, '-C', str(SNAPSHOT), *args], check=True,
                          capture_output=True).stdout

def receipt(name, data):
    path = PACKET / 'checks' / name
    with path.open('x', encoding='utf-8', newline='\n') as output:
        output.write(json.dumps(data, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'receipt': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}))

if phase == 'identity':
    candidate = json.loads((PACKET / 'candidate.json').read_bytes())
    assert git('rev-parse', candidate['ref']).decode().strip() == COMMIT
    assert git('rev-parse', COMMIT + '^').decode().strip() == BASE
    assert git('rev-parse', COMMIT + '^{tree}').decode().strip() == candidate['tree']
    items = git('diff-tree', '-r', '--no-renames', '-z', '--no-commit-id',
                '--name-status', BASE, COMMIT).decode().split('\0')
    blobs = []
    rows = []
    for pos in range(0, len(items) - 1, 2):
        status, path = items[pos:pos + 2]
        raw = git('cat-file', 'blob', COMMIT + ':' + path)
        digest = hashlib.sha256(raw).hexdigest()
        rows.append(f'{digest}  {path}\n')
        blobs.append({'path': path, 'status': status, 'sha256': digest,
                      'lf_only': b'\r' not in raw, 'bom_free': not raw.startswith(b'\xef\xbb\xbf'),
                      'overlong_lines': [i for i, line in enumerate(raw.decode().splitlines(), 1)
                                         if len(line) > 100],
                      'checkout_equals_blob': (SNAPSHOT / path).read_bytes() == raw})
    row_bytes = ''.join(sorted(rows)).encode()
    assert row_bytes == (PACKET / 'manifest.sha256').read_bytes()
    assert hashlib.sha256(row_bytes).hexdigest() == MANIFEST == candidate['manifest_sha256']
    assert {b['path'] for b in blobs} == {'src/pontius/v0a/runtime.py',
                                        'tests/test_v0a_hand_replay.py'}
    assert all(b['lf_only'] and b['bom_free'] and b['checkout_equals_blob'] for b in blobs)
    whitespace = git('diff', '--check', BASE, COMMIT).decode()
    assert not git('status', '--porcelain')
    receipt('cold-a-identity.json', {'metadata': metadata, 'candidate': candidate,
             'blobs': blobs, 'manifest_verified': True, 'diff_check': whitespace})
elif phase == 'payload':
    import pontius.v0a.runtime as runtime
    assert Path(runtime.__file__).resolve() == SNAPSHOT / 'src/pontius/v0a/runtime.py'
    print(json.dumps({'payload_origin': runtime.__file__}), flush=True)
    payload = sys.argv[3]
    sys.argv = [payload, *sys.argv[4:]]
    runpy.run_path(payload, run_name='__main__')
elif phase in ('focused', 'probe'):
    targets = ([str(SNAPSHOT / 'tests' / name) for name in (
        'test_v0a_hand_replay.py', 'test_v0a_contract_faults.py',
        'test_v0a_replay.py', 'test_v0a_trace.py')] if phase == 'focused' else
        [str(PACKET / 'checks/cold-a-context-probe.py')])
    runs = []
    for target in targets:
        command = [sys.executable, '-B', '-P', __file__, 'payload', expected, target]
        result = subprocess.run(command, cwd=SNAPSHOT, env=dict(os.environ),
                                capture_output=True, text=True, timeout=90)
        runs.append({'command': command, 'exit': result.returncode,
                     'stdout': result.stdout, 'stderr': result.stderr})
        print(json.dumps({'target': target, 'exit': result.returncode,
                          'stderr_tail': result.stderr[-1500:], 'stdout_tail': result.stdout[-1000:]}),
              flush=True)
    receipt('cold-a-' + expected.replace('.', '') + '-' + phase + '.json',
            {'metadata': metadata, 'runs': runs})
    assert all(run['exit'] == 0 for run in runs)
else:
    raise AssertionError(phase)
