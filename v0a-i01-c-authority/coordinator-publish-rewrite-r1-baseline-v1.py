"""Routine handoff publication of the retained Gate A baseline and disposition."""
from pathlib import Path
import hashlib
import json
import subprocess

H = Path(r'D:\Pontius-handoffs')
T = H / 'v0a-i01-c-authority'
GIT = r'C:\Program Files\Git\cmd\git.exe'
EXPECTED = 'f6d9d79e5b9820bffa946193983e193d896575d4'
h = lambda raw: hashlib.sha256(raw).hexdigest()
def git(*args):
    return subprocess.run([GIT, '-c', 'core.fsmonitor=false', '-c', 'core.autocrlf=false', '-C', str(H), *args],
        check=True, capture_output=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW).stdout
assert git('rev-parse', 'HEAD').decode().strip() == EXPECTED
assert not git('diff', '--cached', '--name-only', '-z')
pins = {
    'tests-checks/rewrite-r1-harness-engineering-review-codex-a-v1.md': '6b7b53e8c910c081e8ad42217a992b539db69f45d005a80ee7595df6d1b19db7',
    'rewrite-r1-baseline-disposition-v1.md': '0259ec8773dd28217fd6d2a53fc60dc468e910fb4d6871b128aaa3d6c563af6c',
    'coordinator-rewrite-r1-r1-base01-311-verification-v1.json': '954ee9a908033e0c43d8c7588837e3588398174f3a9e67c034469fa11fe6bc80',
    'tests-checks/rewrite-r1-gate-a-r1-base01-311-receipt.json': 'a9bddbae63bf96bfa85a853ada42e0dde8a9f4a27c785a8f4c08c38ce33c8529',
    'rewrite-r1-preparation-manifest-v1.sha256': 'ee8e0c23a53ed9aee251d9551b8319d248523585b7010ca628543df2d765d4d3',
}
receipt = json.loads((T / 'tests-checks/rewrite-r1-gate-a-r1-base01-311-receipt.json').read_bytes())
for info in receipt['outputs'].values():
    p = Path(info['path'])
    assert p.parent == T / 'tests-checks'
    pins[p.relative_to(T).as_posix()] = info['sha256']
for name in ('coordinator-verify-rewrite-r1-result-v1.py', 'coordinator-retain-rewrite-r1-baseline-v1.py',
             'coordinator-rewrite-r1-progress-v2-before-v3.md', 'coordinator-rewrite-r1-plan-publication01.json'):
    pins[name] = h((T / name).read_bytes())
local = {name: (T / name).read_bytes() for name in pins}
assert all(h(raw) == pins[name] for name, raw in local.items())
manifest = ''.join(f'{pin}  {name}\n' for name, pin in sorted(pins.items())).encode()
created = {'rewrite-r1-baseline-manifest-v1.sha256': manifest,
           'coordinator-publish-rewrite-r1-baseline-v1.py': Path(__file__).read_bytes()}
report_path = T / 'coordinator-rewrite-r1-baseline-publication01.json'
assert not report_path.exists() and not any((T / name).exists() for name in created)
for name, raw in created.items():
    with (T / name).open('xb') as stream:
        stream.write(raw)
local.update(created)
local['rewrite-r1-progress.md'] = (T / 'rewrite-r1-progress.md').read_bytes()
contents = {'v0a-i01-c-authority/' + name: raw for name, raw in local.items()}
attributes = H / '.gitattributes'
before = attributes.read_bytes()
assert git('show', 'HEAD:.gitattributes') == before
rules = [f'{n} -text' for n, raw in contents.items() if b'\r\n' in raw and f'{n} -text' not in before.decode().splitlines()]
if rules:
    attributes.write_bytes(before + ('\n# Preserve issued R1 baseline receipt bytes.\n' + '\n'.join(rules) + '\n').encode())
    contents['.gitattributes'] = attributes.read_bytes()
changed = {}
for name, raw in contents.items():
    p = subprocess.run([GIT, '-C', str(H), 'show', 'HEAD:' + name], capture_output=True, timeout=60)
    if p.returncode or p.stdout != raw:
        changed[name] = raw
git('add', '--', *sorted(changed))
assert set(git('diff', '--cached', '--name-only', '-z').decode().rstrip('\0').split('\0')) == set(changed)
for name, raw in changed.items():
    assert git('cat-file', 'blob', ':' + name) == raw
git('commit', '-m', 'Retain R1 class-cell baseline and bounded implementation start')
commit = git('rev-parse', 'HEAD').decode().strip()
for name, raw in contents.items():
    assert git('cat-file', 'blob', commit + ':' + name) == raw and (H / name).read_bytes() == raw
remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()
if not remote or remote[0] != commit:
    git('push', 'origin', 'HEAD:refs/heads/main')
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()
assert remote[0] == commit
report = {'kind': 'routine handoff only; no Pontius integration', 'previous_commit': EXPECTED,
    'commit': commit, 'manifest_sha256': h(manifest), 'remote_verified': True,
    'changed_paths': sorted(changed), 'published_sha256': {n: h(raw) for n, raw in contents.items()}}
with report_path.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'commit': commit, 'manifest_sha256': h(manifest), 'remote_verified': True}))
