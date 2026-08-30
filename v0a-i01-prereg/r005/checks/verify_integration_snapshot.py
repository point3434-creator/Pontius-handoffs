"""Disposable documentation checks only; imports no experiment owner."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

REPORT = Path('D:/Pontius-handoffs/v0a-i01-prereg/r005/checks')
GIT = Path('C:/Program Files/Git/cmd/git.exe')
candidate, integration_base_arg, expected_tree, python_arg, expected, label = sys.argv[1:]
python = Path(python_arg).resolve(strict=True)
root = Path('D:/pontius-snapshots') / ('v0a-prereg-' + label + '-' + uuid.uuid4().hex)
harness = root / 'harness'
temp = root / 'temp'
temp.mkdir(parents=True, exist_ok=False)
env = {key: os.environ[key] for key in ('SystemRoot', 'WINDIR', 'ComSpec', 'PATHEXT') if key in os.environ}
env.update({'PATH': str(python.parent) + ';' + os.environ['SystemRoot'] + '/System32',
            'TEMP': str(temp), 'TMP': str(temp), 'HOME': str(temp), 'USERPROFILE': str(temp),
            'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': 'NUL',
            'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_LITERAL_PATHSPECS': '1'})

def git(*args):
    result = subprocess.run([str(GIT), *args], env=env, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()

git('-c', 'core.autocrlf=false', '-c', 'core.eol=lf', 'clone', '--local',
    '--no-hardlinks', '--no-checkout', 'D:/Pontius', str(harness))
integration_base = git('-C', str(harness), 'rev-parse', integration_base_arg + '^{commit}')
git('-C', str(harness), '-c', 'core.autocrlf=false', '-c', 'core.eol=lf',
    'checkout', '--detach', integration_base)
if (harness / '.git/objects/info/alternates').exists():
    raise RuntimeError('object alternates are forbidden')
paths = git('-C', str(harness), 'diff-tree', '-r', '--no-commit-id', '--no-renames',
            '--name-only', candidate + '^', candidate).splitlines()
required = ['STATUS.md', 'docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md',
            'docs/workflow-amendment-2026-08-30.md']
if sorted(paths) != sorted(required):
    raise RuntimeError('unexpected candidate overlay scope')
overlay_hashes = {}
for path in paths:
    blob = subprocess.run([str(GIT), '-C', str(harness), 'cat-file', 'blob',
                           candidate + ':' + path], env=env, check=True, capture_output=True).stdout
    (harness / path).write_bytes(blob)
    overlay_hashes[path] = hashlib.sha256(blob).hexdigest()
git('-C', str(harness), 'add', '--', *paths)
if git('-C', str(harness), 'write-tree') != expected_tree:
    raise RuntimeError('overlay differs from clean merge preview tree')
before_status = git('-C', str(harness), 'status', '--porcelain', '--untracked-files=all')
env.update({'PYTHONPATH': str(harness / 'src'), 'PYTHONDONTWRITEBYTECODE': '1',
            'PYTHONSAFEPATH': '1', 'PYTHONNOUSERSITE': '1', 'PYTHONHASHSEED': '0',
            'PYTHONUTF8': '1', 'PONTIUS_GIT': str(GIT)})

def child(args):
    return subprocess.run([str(python), '-B', '-P', *args], cwd=harness,
                          env=env, capture_output=True, text=True)

probe = child(['-c', 'import json,sys,numpy; print(json.dumps(dict(executable=sys.executable,implementation=sys.implementation.name,version=list(sys.version_info[:3]),numpy=numpy.__version__)))'])
if probe.returncode:
    raise RuntimeError(probe.stderr)
identity = json.loads(probe.stdout)
if identity['implementation'] != 'cpython' or '.'.join(map(str, identity['version'][:2])) != expected:
    raise RuntimeError('unexpected interpreter identity: ' + probe.stdout)
if os.path.normcase(identity['executable']) != os.path.normcase(str(python)):
    raise RuntimeError('wrong executable substituted')
commands = [
    ['src/pontius/status_generation.py', '--check'],
    ['tests/test_status_generation.py', '-v'],
    ['tests/test_documentation_integrity.py', '-v',
     'DocumentationIntegrityTests.test_maintained_local_markdown_links_resolve',
     'DocumentationIntegrityTests.test_current_contract_is_visible_in_every_front_door',
     'DocumentationIntegrityTests.test_fifteen_second_wall_is_the_authoritative_action_contract',
     'DocumentationIntegrityTests.test_action_clock_and_preparation_successor_is_visible'],
]
results = []
for number, args in enumerate(commands):
    result = child(args)
    log = REPORT / (label + '-' + str(number) + '.txt')
    log.write_text(result.stdout + result.stderr, encoding='utf-8', newline='\n')
    results.append({'argv': [str(python), '-B', '-P', *args], 'exit': result.returncode,
                    'log': str(log), 'output': (result.stdout + result.stderr)[-1500:]})
    print(json.dumps(results[-1]), flush=True)
changed = git('-C', str(harness), 'status', '--porcelain', '--untracked-files=all')
if changed != before_status or git('-C', str(harness), 'write-tree') != expected_tree:
    raise RuntimeError('verification snapshot changed beyond its bound overlay: ' + changed)
for path, digest in overlay_hashes.items():
    if hashlib.sha256((harness / path).read_bytes()).hexdigest() != digest:
        raise RuntimeError('tested candidate file changed: ' + path)
outcome = {'candidate': candidate, 'integration_base': integration_base,
           'integration_tree': expected_tree, 'overlay_sha256': overlay_hashes,
           'snapshot': str(harness), 'interpreter': identity,
           'git_executable_sha256': hashlib.sha256(GIT.read_bytes()).hexdigest(),
           'results': results, 'snapshot_changes_match_bound_overlay': True,
           'scope': 'complete status-generation suite plus four clone-safe documentation selectors; no broad scientific suites'}
(REPORT / (label + '-verification.json')).write_text(json.dumps(outcome, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps({'identity': identity, 'snapshot': str(harness), 'all_passed': all(row['exit'] == 0 for row in results)}), flush=True)
raise SystemExit(0 if all(row['exit'] == 0 for row in results) else 1)
