import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(r'D:\Pontius-review-ab-r002-cold-a-20260830')
CHECKS = Path(r'D:\Pontius-handoffs\v0a-i01-ab\r002\checks')
GIT = r'C:\Program Files\Git\cmd\git.exe'
COMMIT = '2f4287f68a83fac4225a05a91daffdb3f2977a43'
BASE = '256bcf5b1e721c70216f4d8937166cbb9c25a7ce'
MANIFEST = '55f7ebf8827c79a6d6c70b1bf26508d87527b8c7113d2458fb4c3dfb5fed0957'

def git(*args):
    return subprocess.run([GIT, '-C', str(ROOT), *args], capture_output=True, check=True).stdout

fields = git('diff-tree', '-r', '-z', '--no-commit-id', '--no-renames',
             '--name-status', COMMIT + '^', COMMIT).decode().split('\0')
rows = []
file_checks = []
for index in range(0, len(fields) - 1, 2):
    status, path = fields[index:index+2]
    blob = git('cat-file', 'blob', COMMIT + ':' + path)
    digest = hashlib.sha256(blob).hexdigest() if status != 'D' else '0' * 64
    rows.append(f'{digest}  {path}\n')
    file_checks.append({'path': path, 'sha256': digest,
                        'checkout_equals_blob': (ROOT / path).read_bytes() == blob,
                        'lf_only': b'\r' not in blob, 'no_bom': not blob.startswith(b'\xef\xbb\xbf'),
                        'long_lines': [i for i, line in enumerate(blob.splitlines(), 1)
                                       if len(line) > 100],
                        'trailing_whitespace': [i for i, line in enumerate(blob.splitlines(), 1)
                                                if line.rstrip() != line]})
row_bytes = ''.join(sorted(rows)).encode()
assert hashlib.sha256(row_bytes).hexdigest() == MANIFEST
assert git('rev-parse', 'HEAD').decode().strip() == COMMIT
assert git('rev-parse', COMMIT + '^').decode().strip() == BASE
assert hashlib.sha256((CHECKS.parent / 'manifest.sha256').read_bytes()).hexdigest() == MANIFEST
assert (CHECKS.parent / 'manifest.sha256').read_bytes() == row_bytes
assert not git('status', '--porcelain')
sealed = ['src/pontius/immutable_blueprint.py', 'src/pontius/no_limit_betting.py',
          'src/pontius/holdem_cards.py', 'src/pontius/legal_decision_spine_v2.py',
          'src/pontius/action_clock.py', 'src/pontius/preparation_bank.py']
identity = {'commit': COMMIT, 'base': BASE,
            'tree': git('rev-parse', COMMIT + '^{tree}').decode().strip(),
            'manifest_sha256': MANIFEST, 'files': file_checks,
            'sealed_unchanged': {path: git('rev-parse', COMMIT + ':' + path) ==
                                git('rev-parse', BASE + ':' + path) for path in sealed}}
identity_path = CHECKS / 'codex-a-identity.json'
if not identity_path.exists():
    identity_path.write_text(json.dumps(identity, indent=2) + '\n', encoding='utf-8')

slot = sys.argv[1]
executable, version = {
    '311': (r'D:\Pontius-tools\py311\Scripts\python.exe', [3, 11, 15]),
    '314': (r'D:\Pontius\.venv\Scripts\python.exe', [3, 14, 6]),
}[slot]
env = {key: os.environ[key] for key in ('SystemRoot', 'WINDIR', 'TEMP', 'TMP', 'COMSPEC')
       if key in os.environ}
env.update({'PYTHONPATH': str(ROOT / 'src'), 'PONTIUS_GIT': GIT,
            'PYTHONNOUSERSITE': '1', 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONSAFEPATH': '1'})
preflight = """import json, os, pathlib, sys
assert list(sys.version_info[:3]) == EXPECTED
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert pathlib.Path.cwd() == pathlib.Path(ROOT)
assert os.environ['PYTHONPATH'] == str(pathlib.Path(ROOT) / 'src')
assert os.environ['PONTIUS_GIT'] == GIT
import pontius.v0a.runtime as runtime
assert pathlib.Path(runtime.__file__) == pathlib.Path(ROOT) / 'src/pontius/v0a/runtime.py'
print(json.dumps({'version': sys.version, 'executable': sys.executable, 'cwd': os.getcwd(),
                  'environment': dict(os.environ), 'runtime': runtime.__file__,
                  'safe_path': sys.flags.safe_path, 'dont_write_bytecode': sys.flags.dont_write_bytecode}))
""".replace('EXPECTED', repr(version)).replace('ROOT', repr(str(ROOT))).replace('GIT', repr(GIT))
# GIT replacement would rewrite the string key; bind constants instead.
preflight = "import os,sys,json,pathlib\n" + f"expected={version!r}; root={str(ROOT)!r}; git={GIT!r}\n" + """assert list(sys.version_info[:3]) == expected
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert pathlib.Path.cwd() == pathlib.Path(root)
assert os.environ['PYTHONPATH'] == str(pathlib.Path(root) / 'src')
assert os.environ['PONTIUS_GIT'] == git
import pontius.v0a.runtime as runtime
assert pathlib.Path(runtime.__file__) == pathlib.Path(root) / 'src/pontius/v0a/runtime.py'
print(json.dumps({'version': sys.version, 'executable': sys.executable, 'cwd': os.getcwd(),
                  'environment': dict(os.environ), 'runtime': runtime.__file__,
                  'safe_path': sys.flags.safe_path, 'dont_write_bytecode': sys.flags.dont_write_bytecode}))
"""
commands = [['-c', preflight]]
commands += [[str(ROOT / 'tests' / name)] for name in (
    'test_v0a_hand_replay.py', 'test_v0a_contract_faults.py',
    'test_v0a_replay.py', 'test_v0a_trace.py')]
probe = CHECKS / 'codex-a-policy-probe.py'
if probe.exists():
    commands.append([str(probe)])
results = []
for payload in commands:
    command = [executable, '-B', '-P', *payload]
    done = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
    result = {'command': command, 'exit': done.returncode, 'stdout': done.stdout, 'stderr': done.stderr}
    results.append(result)
    print(json.dumps({'payload': payload[0], 'exit': done.returncode, 'stdout': done.stdout,
                      'stderr': done.stderr}))
    if payload[0] == '-c' and done.returncode:
        break
receipt = {'identity': identity, 'slot': slot, 'expected_version': version,
           'environment': env, 'cwd': str(ROOT), 'results': results,
           'final_status': git('status', '--porcelain').decode()}
out = CHECKS / f'codex-a-py{slot}-v2-receipt.json'
with out.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(receipt, stream, indent=2)
    stream.write('\n')
raise SystemExit(0 if all(item['exit'] == 0 for item in results) else 1)
