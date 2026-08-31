"""Publish only the issued R1 plan, harness and static preparation artifacts."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess

H = Path(r'D:\Pontius-handoffs')
T = H / 'v0a-i01-c-authority'
GIT = r'C:\Program Files\Git\cmd\git.exe'
EXPECTED = 'fc7870b6f5e4c77c2efce8339377d13daeeb1bb4'
h = lambda raw: hashlib.sha256(raw).hexdigest()
def read(p):
    assert p.is_absolute() and '..' not in p.parts
    for a in (p, *p.parents):
        assert not getattr(a.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert p.is_file()
    return p.read_bytes()
def git(*args):
    return subprocess.run([GIT, '-c', 'core.fsmonitor=false', '-c', 'core.autocrlf=false', '-C', str(H), *args],
        check=True, capture_output=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW).stdout
assert git('rev-parse', 'HEAD').decode().strip() == EXPECTED
assert not git('diff', '--cached', '--name-only', '-z')
proof = read(T / 'coordinator-rewrite-r1-static-v1.json')
assert h(proof) == 'af9cf8d47f293b3cba43e81cc9f19acef5104741d84891d82e88e4beb19dfa6f'
pins = json.loads(proof)['inputs']
for name in ('coordinator-rewrite-r1-static-v1.json', 'rewrite-r1-plan-disposition-v1.md',
             'coordinator-review-rewrite-r1-v1.py', 'coordinator-review-rewrite-r1-v2.py',
             'coordinator-prepare-rewrite-r1-v1.py', 'coordinator-rewrite-r1-setup-v1.json',
             'tests-checks/rewrite-r1-author-v1.py', 'tests-checks/rewrite-r1-control-v1-from-original-ten.diff',
             'tests-checks/rewrite-r1-probe-v1-from-original-ten.diff', 'rewrite-design-manifest-v2.sha256'):
    pins[name] = h(read(T / name))
local = {name: read(T / name) for name in pins}
assert all(h(raw) == pins[name] for name, raw in local.items())
old_current = read(T / 'CURRENT.md')
assert h(old_current) == '410cf06cbe47f4c551eaa43cccfc9aafe2d34842a93ebce730a991b9226f5523'
appendix = '''
## R1 implementation preparation

The controller said to proceed. The isolated r010 worktree is prepared; the
[concrete plan](rewrite-r1-implementation-plan-v1.md) and [coordinator disposition](rewrite-r1-plan-disposition-v1.md)
define the sole source writer, public-path replacement, accounting and2500-line
first-attempt boundary. [Static checks](coordinator-rewrite-r1-static-v1.json)
confirm the six original public cases/eight Models and preserved harness helpers.
[The preparation manifest](rewrite-r1-preparation-manifest-v1.sha256) freezes
the exact plan/harness/baseline inputs. Independent harness review and root
baseline dispatch still precede source GO. No replacement source or payload
has been executed at this entry; it does not imply implementation acceptance.
See [R1 progress](rewrite-r1-progress.md); [prior navigation](coordinator-navigation-v17-before-v18.md).
'''.encode()
old_progress = read(T / 'rewrite-r1-progress.md')
new_progress = old_progress + b'\nPlan and Gate A harness are now issued; root static review completed. Independent\nharness disposition and actual baseline remain before source GO. See the preparation manifest.\n'
manifest = ''.join(f'{pin}  {name}\n' for name, pin in sorted(pins.items())).encode()
created = {'rewrite-r1-preparation-manifest-v1.sha256': manifest,
           'coordinator-navigation-v17-before-v18.md': old_current,
           'coordinator-rewrite-r1-progress-v1-before-v2.md': old_progress,
           'coordinator-publish-rewrite-r1-plan-v1.py': Path(__file__).read_bytes()}
report_path = T / 'coordinator-rewrite-r1-plan-publication01.json'
assert not report_path.exists() and not any((T / name).exists() for name in created)
for name, raw in created.items():
    with (T / name).open('xb') as stream:
        stream.write(raw)
(T / 'CURRENT.md').write_bytes(old_current + appendix)
(T / 'rewrite-r1-progress.md').write_bytes(new_progress)
local.update(created)
local.update({'CURRENT.md': old_current + appendix, 'rewrite-r1-progress.md': new_progress,
              'coordinator-c-rewrite-review-publication01.json': read(T / 'coordinator-c-rewrite-review-publication01.json')})
contents = {'v0a-i01-c-authority/' + n: raw for n, raw in local.items()}
attributes = H / '.gitattributes'
before = read(attributes)
assert git('show', 'HEAD:.gitattributes') == before
rules = [f'{n} -text' for n, raw in contents.items() if b'\r\n' in raw and f'{n} -text' not in before.decode().splitlines()]
if rules:
    attributes.write_bytes(before + ('\n# Preserve issued R1 plan and harness bytes.\n' + '\n'.join(rules) + '\n').encode())
    contents['.gitattributes'] = read(attributes)
changed = {}
for name, raw in contents.items():
    previous = subprocess.run([GIT, '-C', str(H), 'show', 'HEAD:' + name], capture_output=True,
        timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
    if previous.returncode or previous.stdout != raw:
        changed[name] = raw
git('add', '--', *sorted(changed))
assert set(git('diff', '--cached', '--name-only', '-z').decode().rstrip('\0').split('\0')) == set(changed)
for name, raw in changed.items():
    assert git('cat-file', 'blob', ':' + name) == raw
git('commit', '-m', 'Retain R1 implementation plan and fixed Gate A harness')
commit = git('rev-parse', 'HEAD').decode().strip()
for name, raw in contents.items():
    assert git('cat-file', 'blob', commit + ':' + name) == raw and read(H / name) == raw
remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()
if not remote or remote[0] != commit:
    git('push', 'origin', 'HEAD:refs/heads/main')
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()
assert remote[0] == commit
report = {'kind': 'routine handoff publication, no Pontius integration or payload', 'previous_commit': EXPECTED,
          'commit': commit, 'manifest_sha256': h(manifest), 'remote_main_verified': True,
          'published_sha256': {n: h(raw) for n, raw in contents.items()}, 'changed_paths': sorted(changed)}
with report_path.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'commit': commit, 'manifest_sha256': h(manifest), 'remote_verified': True,
                  'changed_paths': len(changed)}))
