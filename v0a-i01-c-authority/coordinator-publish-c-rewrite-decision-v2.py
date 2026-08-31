"""Publish released design and held-engineering artifacts, never main source."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess

H = Path(r'D:\Pontius-handoffs')
T = H / 'v0a-i01-c-authority'
GIT = r'C:\Program Files\Git\cmd\git.exe'
EXPECTED = '8e3db78f995f131463693708939d1b2c62ab3213'
COPY = T / 'coordinator-publish-c-rewrite-decision-v2.py'
OUT = T / 'coordinator-c-rewrite-decision-publication01.json'
h = lambda raw: hashlib.sha256(raw).hexdigest()

def read(path):
    assert path.is_absolute() and '..' not in path.parts
    for ancestor in (path, *path.parents):
        assert not getattr(ancestor.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path.read_bytes()

def git(*args):
    return subprocess.run([GIT, '-c', 'core.fsmonitor=false', '-c', 'core.autocrlf=false', '-C', str(H), *args],
        check=True, capture_output=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW).stdout

pins = {
    'CURRENT.md': '75a2bf310a737d3fa74623b851fd2660da61cfac718a97055450577ebf25bfba',
    'coordinator-rewrite-design-freeze-v1.json': '6e269ff4539a3c609c0ff2023263513c6611792a95fa5409216c58b98edf7c86',
    'coordinator-v30-design-verification-v1.json': 'ed57b0fa44fda469f2291268682774bda02e82f5bc13dc9bbfca9d807c2acbf1',
    'coordinator-v30-storage-inspection-v1.json': '169bfc18b9943d10f2433729e1f2c37cc6684f1146be0aa4ededb135dfefed9f',
    'engineer-generator-v30-storage-static-v1.json': '14506755969039902f8c951d111991b806f814e185face0372367579a4ff3f29',
    'engineer-depth-budget-probe-v5.py': 'd64afd0f9adca93d9ac4c28b4124f2954b8a8d1e56a36848fbd7b8b111920758',
    'tests-depth-budget-control-v5.py': '0fbec7b5419f134cbc837b6f41e87f2557b2cc70ff5f9fec499482e948c22725',
    'engineer-semantic-storage-composition-plan-codex-a-v1.md': '382849e96ec1e454da3725365f1d9f1772dc6c34053af6f35d1ac0b9403d0c6e',
}
additional = [
    'coordinator-storage-semantic-checkpoint-publication01.json',
    'coordinator-navigation-v15-before-v16.md', 'coordinator-navigation-v16.json',
    'coordinator-update-authority-navigation-v16.py',
    'coordinator-inspect-v30-storage-v1.py', 'coordinator-verify-v30-design-v1.py',
    'coordinator-publish-c-rewrite-decision-v1.py',
    'engineer-v30-generator70-diagnostic-plan-v1.md',
    'tests-depth-budget-control-v5-from-v4.diff',
]
assert not COPY.exists() and not OUT.exists()
assert git('rev-parse', 'HEAD').decode().strip() == EXPECTED
assert not git('diff', '--cached', '--name-only', '-z')
assert all(h(read(T / name)) == pin for name, pin in pins.items())
freeze = json.loads(read(T / 'coordinator-rewrite-design-freeze-v1.json'))
pins.update(freeze['inputs'])
pins.update(freeze['outputs'])
pins.update(json.loads(read(T / 'engineer-generator-v30-storage-static-v1.json'))['artifacts'])
receipt_name = 'tests-checks/focused-v2-v30-first01-design-311-receipt.json'
pins[receipt_name] = 'ae46f1f92f9f7de5e554f5cc1f51694a4bd69d6856acce12e099389319a6391d'
receipt = json.loads(read(T / receipt_name))
assert receipt['stage'] == 'finished' and not receipt['timed_out']
for item in [*receipt['outputs'].values(), *receipt['inputs_before'].values()]:
    path = Path(item['path'])
    if path.is_relative_to(T):
        pins[path.relative_to(T).as_posix()] = item['sha256']
# These families were explicitly released, or are immutable held scratch.
# Active population-manifest authoring is intentionally not included here.
for pattern in ('engineer-generator-v30-storage*', 'engineer-depth-budget-v5-*', 'engineer-depth-budget-probe-v5-from-v4.diff'):
    additional += [p.relative_to(T).as_posix() for p in T.glob(pattern) if p.is_file()]
additional += [p.relative_to(T).as_posix() for p in (T / 'strategy-hold-v31-v1').iterdir() if p.is_file()]
assert all(h(read(T / name)) == pin for name, pin in pins.items())
files = {T / n for n in (*pins, *additional)}
assert all(p.resolve().is_relative_to(T.resolve()) for p in files)
contents = {p.relative_to(H).as_posix(): read(p) for p in sorted(files)}
with COPY.open('xb') as handle:
    handle.write(Path(__file__).read_bytes())
contents[COPY.relative_to(H).as_posix()] = read(COPY)
attributes = H / '.gitattributes'
before = read(attributes)
assert git('show', 'HEAD:.gitattributes') == before
rules = [f'{name} -text' for name, raw in contents.items()
         if b'\r\n' in raw and f'{name} -text' not in before.decode().splitlines()]
if rules:
    assert before.endswith(b'\n')
    attributes.write_bytes(before + ('\n# Retain issued C rewrite decision and held inputs byte-exact.\n' + '\n'.join(rules) + '\n').encode())
    contents['.gitattributes'] = read(attributes)
changed = {}
for name, raw in contents.items():
    prior = subprocess.run([GIT, '-C', str(H), 'show', 'HEAD:' + name], capture_output=True,
                           timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
    if prior.returncode or prior.stdout != raw:
        changed[name] = raw
assert changed
git('add', '--', *sorted(changed))
staged = set(git('diff', '--cached', '--name-only', '-z').decode().rstrip('\0').split('\0'))
assert staged == set(changed)
for name, raw in changed.items():
    assert git('cat-file', 'blob', ':' + name) == raw
git('commit', '-m', 'Record the partial C core replacement decision')
commit = git('rev-parse', 'HEAD').decode().strip()
for name, raw in contents.items():
    assert git('cat-file', 'blob', commit + ':' + name) == raw and read(H / name) == raw
remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()
if not remote or remote[0] != commit:
    git('push', 'origin', 'HEAD:refs/heads/main')
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()
assert remote[0] == commit
report = {'kind': 'design and held engineering evidence; no main integration',
          'previous_commit': EXPECTED, 'commit': commit, 'remote_main_verified': True,
          'manifest_sha256': pins['rewrite-design-manifest-v1.sha256'],
          'published_sha256': {n: h(raw) for n, raw in contents.items()},
          'changed_paths': sorted(changed), 'new_crlf_exceptions': rules,
          'all_blobs_match_issued_bytes': True}
with OUT.open('x', encoding='utf-8', newline='\n') as handle:
    json.dump(report, handle, indent=2)
    handle.write('\n')
print(json.dumps({'commit': commit, 'changed_paths': len(changed), 'remote_verified': True,
                  'manifest_sha256': report['manifest_sha256']}))
