"""Correct packet ordering without changing the frozen source commit."""
import hashlib
import json
from pathlib import Path
import subprocess

OLD = Path('D:/Pontius-handoffs/v0a-i01-prereg/r004')
NEW = OLD.parent / 'r005'
GIT = 'C:/Program Files/Git/cmd/git.exe'
ROOT = 'D:/Pontius'
meta = json.loads((OLD / 'candidate.json').read_text(encoding='utf-8'))
previous_digest = meta['manifest_sha256']
previous_ref = meta['ref']
for name in ('candidate.json', 'handoff.md', 'manifest.sha256'):
    if (NEW / name).exists():
        raise RuntimeError('new packet file already exists: ' + name)

def git(*args):
    return subprocess.run([GIT, '-C', ROOT, *args], check=True,
                          capture_output=True).stdout

paths = git('diff-tree', '-r', '--no-commit-id', '--no-renames', '--name-only',
            meta['base'], meta['commit']).decode().splitlines()
rows = []
for path in paths:
    blob = git('cat-file', 'blob', meta['commit'] + ':' + path)
    rows.append(hashlib.sha256(blob).hexdigest() + '  ' + path + '\n')
manifest = ''.join(sorted(rows)).encode()
digest = hashlib.sha256(manifest).hexdigest()
if digest != 'd972987187b78a2ac5fdb6dbaa74cd7b23e1ce7fdd3a73fae5ed96a0f532da17':
    raise RuntimeError('manifest differs from independently established canonical identity')
meta.update(round='r005', ref='refs/heads/review/v0a-i01-prereg/r005', manifest_sha256=digest)
assert git('rev-parse', meta['commit'] + '^{tree}').decode().strip() == meta['tree']
git('update-ref', meta['ref'], meta['commit'], '0' * 40)
handoff = (OLD / 'handoff.md').read_text(encoding='utf-8')
handoff = handoff.replace('v0a-i01-prereg/r004', 'v0a-i01-prereg/r005')
handoff = handoff.replace(previous_ref, meta['ref']).replace(previous_digest, digest)
for name, raw in [('manifest.sha256', manifest),
                  ('candidate.json', (json.dumps(meta, indent=2) + '\n').encode()),
                  ('handoff.md', handoff.encode())]:
    with (NEW / name).open('xb') as target:
        target.write(raw)
print(json.dumps(meta))
