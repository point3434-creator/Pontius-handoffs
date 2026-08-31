"""Publish a root-authored explicit handoff release; never stages unrelated paths."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

H = Path(r'D:\Pontius-handoffs')
T = H / 'v0a-i01-c-authority'
GIT = r'C:\Program Files\Git\cmd\git.exe'
h = lambda raw: hashlib.sha256(raw).hexdigest()
def git(*args):
    return subprocess.run([GIT, '-c', 'core.fsmonitor=false', '-c', 'core.autocrlf=false', '-C', str(H), *args],
        capture_output=True, check=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW).stdout
assert len(sys.argv) == 2
release_path = Path(sys.argv[1])
assert release_path.is_absolute() and release_path.parent == Path(r'D:\Pontius')
release_raw = release_path.read_bytes()
release = json.loads(release_raw)
assert git('rev-parse', 'HEAD').decode().strip() == release['expected_head']
assert not git('diff', '--cached', '--name-only', '-z')
tag = release['release_id']
assert tag.replace('-', '').isalnum()
pins = release['pins']
assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in pins)
local = {name: (T / name).read_bytes() for name in pins}
assert all(h(raw) == pins[name] for name, raw in local.items())
manifest = b''.join(sorted((pin + '  ' + name + '\n').encode() for name, pin in pins.items()))
created = {tag + '-manifest.sha256': manifest, tag + '-release.json': release_raw}
report_path = T / (tag + '-publication.json')
assert not report_path.exists() and not any((T / name).exists() for name in created)
for name, raw in created.items():
    with (T / name).open('xb') as stream:
        stream.write(raw)
local.update(created)
contents = {'v0a-i01-c-authority/' + name: raw for name, raw in local.items()}
attributes = H / '.gitattributes'
before = attributes.read_bytes()
assert git('show', 'HEAD:.gitattributes') == before
rules = [f'{n} -text' for n, raw in contents.items() if b'\r\n' in raw and f'{n} -text' not in before.decode().splitlines()]
if rules:
    attributes.write_bytes(before + ('\n# Preserve issued ' + tag + ' bytes.\n' + '\n'.join(rules) + '\n').encode())
    contents['.gitattributes'] = attributes.read_bytes()
changed = {}
for name, raw in contents.items():
    p = subprocess.run([GIT, '-C', str(H), 'show', 'HEAD:' + name], capture_output=True, timeout=60)
    if p.returncode or p.stdout != raw:
        changed[name] = raw
assert changed
git('add', '--', *sorted(changed))
assert set(git('diff', '--cached', '--name-only', '-z').decode().rstrip('\0').split('\0')) == set(changed)
for name, raw in changed.items():
    assert git('cat-file', 'blob', ':' + name) == raw
git('commit', '-m', release['title'])
commit = git('rev-parse', 'HEAD').decode().strip()
for name, raw in contents.items():
    assert git('cat-file', 'blob', commit + ':' + name) == raw and (H / name).read_bytes() == raw
remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()
if not remote or remote[0] != commit:
    git('push', 'origin', 'HEAD:refs/heads/main')
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()
assert remote[0] == commit
report = {'kind': 'routine handoff publication only', 'commit': commit, 'previous_commit': release['expected_head'],
    'manifest_sha256': h(manifest), 'remote_verified': True, 'changed_paths': sorted(changed),
    'published_sha256': {name: h(raw) for name, raw in contents.items()}, 'publisher_sha256': h(Path(__file__).read_bytes())}
with report_path.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'commit': commit, 'manifest_sha256': h(manifest), 'remote_verified': True}))
