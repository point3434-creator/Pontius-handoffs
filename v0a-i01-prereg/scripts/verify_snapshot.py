"""Disposable documentation checks only; imports no experiment owner."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

REPORT = Path('D:/Pontius-worktrees/v0a-increment-1-preregistration-review')
GIT = Path('C:/Program Files/Git/cmd/git.exe')
candidate, python_arg, expected, label = sys.argv[1:]
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
git('-C', str(harness), '-c', 'core.autocrlf=false', '-c', 'core.eol=lf',
    'checkout', '--detach', candidate)
if (harness / '.git/objects/info/alternates').exists():
    raise RuntimeError('object alternates are forbidden')
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
if changed:
    raise RuntimeError('verification snapshot changed: ' + changed)
outcome = {'candidate': candidate, 'snapshot': str(harness), 'interpreter': identity,
           'git_executable_sha256': hashlib.sha256(GIT.read_bytes()).hexdigest(),
           'results': results, 'snapshot_clean': True,
           'scope': 'complete status-generation suite plus four clone-safe documentation selectors; no broad scientific suites'}
(REPORT / (label + '-verification.json')).write_text(json.dumps(outcome, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps({'identity': identity, 'snapshot': str(harness), 'all_passed': all(row['exit'] == 0 for row in results)}), flush=True)
raise SystemExit(0 if all(row['exit'] == 0 for row in results) else 1)
