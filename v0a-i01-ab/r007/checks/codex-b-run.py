import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

SNAPSHOT = Path(r'D:\Pontius-tmp\codex-b-r007-01a05090\snapshot')
CHECKS = Path(r'D:\Pontius-handoffs\v0a-i01-ab\r007\checks')
TEMP = SNAPSHOT.parent / 'temp'
GIT = r'C:\Program Files\Git\cmd\git.exe'
COMMIT = 'ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1'
BASE = '52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8'
MANIFEST = 'c234b4271bd665e869689fb5d976e629703b678faeb3f55532a3615edc98b189'
version, mode, label = sys.argv[1:4]
python = { '3.11.15': r'D:\Pontius-tools\py311\Scripts\python.exe',
           '3.14.6': r'D:\Pontius\.venv\Scripts\python.exe' }[version]
env = {key: os.environ[key] for key in ('SystemRoot', 'WINDIR', 'COMSPEC') if key in os.environ}
env.update(TEMP=str(TEMP), TMP=str(TEMP), PYTHONPATH=str(SNAPSHOT / 'src'),
           PYTHONNOUSERSITE='1', PONTIUS_GIT=GIT)
guard = '''import sys, os, platform, pathlib, json
expected_version, expected_python, expected_root = %r, %r, %r
assert platform.python_implementation() == 'CPython'
assert platform.python_version() == expected_version, sys.version
assert os.path.normcase(sys.executable) == os.path.normcase(expected_python), sys.executable
assert pathlib.Path.cwd() == pathlib.Path(expected_root)
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert os.environ['PYTHONPATH'] == str(pathlib.Path(expected_root) / 'src')
print(json.dumps({'python': sys.executable, 'version': sys.version, 'implementation': platform.python_implementation(), 'cwd': str(pathlib.Path.cwd()), 'flags': {'B': sys.flags.dont_write_bytecode, 'P': sys.flags.safe_path}, 'environment': dict(os.environ)}, sort_keys=True), flush=True)
''' % (version, python, str(SNAPSHOT))
origins = '''import importlib
for module_name in ('pontius.v0a.runtime', 'pontius.v0a.replay', 'pontius.v0a.trace', 'pontius.v0a.clock', 'pontius.v0a.model', 'pontius.action_clock', 'pontius.preparation_bank', 'pontius.legal_decision_spine_v2', 'pontius.no_limit_betting', 'pontius.holdem_cards', 'pontius.immutable_blueprint', 'pontius.river'):
    module = importlib.import_module(module_name)
    expected = pathlib.Path(expected_root) / 'src' / (module_name.replace('.', '/') + '.py')
    assert pathlib.Path(module.__file__) == expected, (module_name, module.__file__, expected)
    print('ORIGIN', module_name, module.__file__, flush=True)
'''
if mode == 'manifest':
    body = '''import hashlib, subprocess
GIT, COMMIT, BASE, MANIFEST, CHECKS = %r, %r, %r, %r, %r
def git(*args):
    return subprocess.run([GIT, '-C', expected_root, *args], capture_output=True, check=True).stdout
assert git('rev-parse', 'HEAD').decode().strip() == COMMIT
assert git('rev-parse', COMMIT + '^').decode().strip() == BASE
assert git('rev-parse', COMMIT + '^{tree}').decode().strip() == '7f8e429d60434ec5979a4ffa0eead94dfb1d9b35'
fields = git('diff-tree', '-r', '-z', '--no-renames', '--no-commit-id', '--name-status', BASE, COMMIT).split(b'\\0')
rows = []
for i in range(0, len(fields)-1, 2):
    status, path = fields[i], fields[i+1]
    digest = '0' * 64 if status == b'D' else hashlib.sha256(git('cat-file', 'blob', COMMIT + ':' + path.decode())).hexdigest()
    rows.append(digest.encode() + b'  ' + path + b'\\n')
manifest_bytes = b''.join(sorted(rows))
actual = hashlib.sha256(manifest_bytes).hexdigest()
assert actual == MANIFEST, actual
packet = pathlib.Path(CHECKS).parent / 'manifest.sha256'
assert packet.read_bytes() == manifest_bytes
print(manifest_bytes.decode(), end='')
print('MANIFEST', actual)
''' % (GIT, COMMIT, BASE, MANIFEST, str(CHECKS))
    targets = [('manifest', guard + body)]
elif mode == 'tests':
    targets = []
    for target in ('tests/test_v0a_replay.py', 'tests/test_v0a_trace.py'):
        body = "import runpy\nsys.argv = [%r, '-v']\nrunpy.run_path(%r, run_name='__main__')\n" % (target, str(SNAPSHOT / target))
        targets.append((Path(target).stem, guard + origins + body))
elif mode == 'probe':
    target = CHECKS / ('codex-b-' + label + '.py')
    body = "import runpy\nsys.argv = [%r]\nrunpy.run_path(%r, run_name='__main__')\n" % (str(target), str(target))
    targets = [(label, guard + origins + body)]
else:
    raise ValueError(mode)
records = []
for target, code in targets:
    argv = [python, '-B', '-P', '-c', code]
    result = subprocess.run(argv, cwd=SNAPSHOT, env=env, capture_output=True, text=True, encoding='utf-8')
    out = CHECKS / ('codex-b-' + label + '-' + version.replace('.', '') + '-' + target + '.txt')
    with out.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(result.stdout)
        stream.write(result.stderr)
    record = dict(target=target, argv=argv, cwd=str(SNAPSHOT), environment=env, exit=result.returncode,
                  output=str(out), output_sha256=hashlib.sha256(out.read_bytes()).hexdigest())
    records.append(record)
    print(json.dumps({key: record[key] for key in ('target', 'exit', 'output', 'output_sha256')}), flush=True)
    print((result.stdout + result.stderr)[-2500:], flush=True)
receipt = CHECKS / ('codex-b-' + label + '-' + version.replace('.', '') + '.json')
with receipt.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(dict(candidate=COMMIT, manifest_sha256=MANIFEST, checks=records), stream, indent=2)
    stream.write('\n')
raise SystemExit(any(record['exit'] for record in records))
