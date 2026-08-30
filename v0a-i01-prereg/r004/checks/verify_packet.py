"""Verify packet identity against frozen Git blobs; no source execution."""
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parent.parent
GIT = 'C:/Program Files/Git/cmd/git.exe'
ROOT = 'D:/Pontius'
meta = json.loads((PACKET / 'candidate.json').read_text(encoding='utf-8'))
expected = {'schema_version', 'task_id', 'round', 'ref', 'commit', 'base',
            'tree', 'manifest_sha256', 'date'}
assert set(meta) == expected
assert meta['schema_version'] == 'pontius-handoff-candidate-v1'
assert meta['task_id'] == 'v0a-i01-prereg' and meta['round'] == 'r004'

def git(*args):
    return subprocess.run([GIT, '-C', ROOT, *args], check=True,
                          capture_output=True).stdout

commit = meta['commit']
assert git('rev-parse', meta['ref']).decode().strip() == commit
assert git('rev-parse', commit + '^').decode().strip() == meta['base']
assert git('rev-parse', commit + '^{tree}').decode().strip() == meta['tree']
paths = git('diff-tree', '-r', '--no-commit-id', '--no-renames', '--name-only',
            meta['base'], commit).decode().splitlines()
assert sorted(paths) == sorted(['STATUS.md', 'docs/workflow-amendment-2026-08-30.md',
    'docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md'])
rows = []
for path in sorted(paths):
    raw = git('cat-file', 'blob', commit + ':' + path)
    assert b'\r' not in raw and not raw.startswith(b'\xef\xbb\xbf')
    rows.append(hashlib.sha256(raw).hexdigest() + '  ' + path + '\n')
manifest = ''.join(rows).encode()
assert (PACKET / 'manifest.sha256').read_bytes() == manifest
assert hashlib.sha256(manifest).hexdigest() == meta['manifest_sha256']
handoff = (PACKET / 'handoff.md').read_text(encoding='utf-8')
assert commit in handoff and meta['manifest_sha256'] in handoff
inputs = {}
for name in ('workflow.md', 'controller-rulings.md'):
    raw = (PACKET / 'inputs' / name).read_bytes()
    inputs[name] = hashlib.sha256(raw).hexdigest()
    assert inputs[name] in handoff
checks = []
for name in ('r004-py311-verification.json', 'r004-py314-verification.json'):
    check = json.loads((PACKET / 'checks' / name).read_text(encoding='utf-8'))
    assert check['candidate'] == commit and check['snapshot_clean']
    assert all(result['exit'] == 0 for result in check['results'])
    checks.append(dict(version=check['interpreter']['version'], all_exit_zero=True))
print(json.dumps(dict(candidate=commit, manifest_sha256=meta['manifest_sha256'],
                     inputs=inputs, checks=checks, packet_identity_verified=True)))
