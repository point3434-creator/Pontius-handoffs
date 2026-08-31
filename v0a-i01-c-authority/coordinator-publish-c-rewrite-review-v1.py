"""Retain final design review, fixed population and append-only scope clarification."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess

H = Path(r'D:\Pontius-handoffs')
T = H / 'v0a-i01-c-authority'
GIT = r'C:\Program Files\Git\cmd\git.exe'
EXPECTED = '135470ade797dbe2001208a7b6ff3fd4dbb6c5fd'
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

assert git('rev-parse', 'HEAD').decode().strip() == EXPECTED
assert not git('diff', '--cached', '--name-only', '-z')
old_manifest = read(T / 'rewrite-design-manifest-v1.sha256')
assert h(old_manifest) == '51cf85d387ac0b64c59603cd04fc758dcfa936cac839d016673b02fe9f7a6267'
pins = {line.split('  ', 1)[1]: line.split('  ', 1)[0] for line in old_manifest.decode().splitlines()}
pins.update({
    'rewrite-design-manifest-v1.sha256': h(old_manifest),
    'rewrite-design-engineering-rereview-codex-a-v2.md': 'aead9e1ca2f5fa6a79b7c52aaea05455ad2d6f153dded352e17050968d80d3ab',
    'rewrite-scope-clarification-v1.md': '2e699aaf3b520539eca38233b1a758cbdefcdf67fea86aaa54a7699f926ea8c1',
    'rewrite-early-population-v1.json': '3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce',
})
for name in ('coordinator-rewrite-population-verification-v1.json', 'coordinator-verify-rewrite-population-v1.py'):
    pins[name] = h(read(T / name))
assert all(h(read(T / n)) == pin for n, pin in pins.items())
old_current = read(T / 'CURRENT.md')
assert h(old_current) == '75a2bf310a737d3fa74623b851fd2660da61cfac718a97055450577ebf25bfba'
appendix = '''
## Final design review and exact early population

The [bounded rereview](rewrite-design-engineering-rereview-codex-a-v2.md) verified
the frozen design pair and found all six concerns addressed. Its comprehension
wording clarification is retained in [the scope addendum](rewrite-scope-clarification-v1.md):
implicit comprehension locals belong to their own frame; free-name lookup skips
the class namespace. Read that addendum with the v1 design; issued bytes are unchanged.

[The early population](rewrite-early-population-v1.json) binds exactly Gate A6 and
Gate B12 to the original cases and depth assertions. [Static verification](coordinator-rewrite-population-verification-v1.json)
rehashes12 whole inputs,10 source/Model case records and36 original source spans.
No payload ran. These are design checks, not implementation or performance results.
The combined [design manifest v2](rewrite-design-manifest-v2.sha256) includes the
clarification, rereview and population. Category/API implementation planning,
operation accounting and a reviewed controller still precede production edits/runs.
[Navigation before this addendum](coordinator-navigation-v16-before-v17.md).
'''.encode()
new_current = old_current + appendix
manifest = ''.join(f'{pin}  {name}\n' for name, pin in sorted(pins.items())).encode()
created = {
    'rewrite-design-manifest-v2.sha256': manifest,
    'coordinator-navigation-v16-before-v17.md': old_current,
    'coordinator-publish-c-rewrite-review-v1.py': Path(__file__).read_bytes(),
    'coordinator-navigation-v17.json': (json.dumps({'kind': 'navigation-only', 'before_sha256': h(old_current),
        'after_sha256': h(new_current), 'design_manifest_v2_sha256': h(manifest),
        'source_changed': False, 'payload_executed': False}, indent=2, sort_keys=True) + '\n').encode(),
}
report_path = T / 'coordinator-c-rewrite-review-publication01.json'
assert not report_path.exists() and not any((T / name).exists() for name in created)
extra = 'coordinator-c-rewrite-decision-publication01.json'
extra_raw = read(T / extra)
for name, raw in created.items():
    with (T / name).open('xb') as stream:
        stream.write(raw)
(T / 'CURRENT.md').write_bytes(new_current)
local = {n: read(T / n) for n in pins}
local.update(created)
local['CURRENT.md'] = new_current
local[extra] = extra_raw
contents = {'v0a-i01-c-authority/' + n: raw for n, raw in local.items()}
attributes = H / '.gitattributes'
before = read(attributes)
assert git('show', 'HEAD:.gitattributes') == before
rules = [f'{n} -text' for n, raw in contents.items() if b'\r\n' in raw and f'{n} -text' not in before.decode().splitlines()]
if rules:
    attributes.write_bytes(before + ('\n# Preserve issued C design rereview and population bytes.\n' + '\n'.join(rules) + '\n').encode())
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
git('commit', '-m', 'Retain C rewrite design review and scope clarification')
commit = git('rev-parse', 'HEAD').decode().strip()
for name, raw in contents.items():
    assert git('cat-file', 'blob', commit + ':' + name) == raw and read(H / name) == raw
remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()
if not remote or remote[0] != commit:
    git('push', 'origin', 'HEAD:refs/heads/main')
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()
assert remote[0] == commit
report = {'kind': 'design-only; no Pontius source integration', 'previous_commit': EXPECTED,
          'commit': commit, 'remote_main_verified': True, 'design_manifest_v2_sha256': h(manifest),
          'published_sha256': {n: h(raw) for n, raw in contents.items()},
          'changed_paths': sorted(changed), 'all_git_blobs_match_issued_bytes': True}
with report_path.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'commit': commit, 'manifest_sha256': h(manifest), 'changed_paths': len(changed),
                  'remote_verified': True, 'current_sha256': h(new_current)}))
