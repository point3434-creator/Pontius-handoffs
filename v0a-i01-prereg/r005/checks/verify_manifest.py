"""Check row ordering before validating declared identity against frozen blobs."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

packet = Path(sys.argv[1]).resolve(strict=True)
meta = json.loads((packet / 'candidate.json').read_text(encoding='utf-8'))
assert set(meta) == {'schema_version', 'task_id', 'round', 'ref', 'commit',
                     'base', 'tree', 'manifest_sha256', 'date'}
assert meta['schema_version'] == 'pontius-handoff-candidate-v1'
raw = (packet / 'manifest.sha256').read_bytes()
assert raw.endswith(b'\n') and b'\r' not in raw
lines = raw.splitlines(keepends=True)
assert lines == sorted(lines), 'manifest complete rows are not lexicographically sorted'
assert len(lines) == len(set(lines)), 'duplicate manifest row'

def git(*args):
    return subprocess.run(['C:/Program Files/Git/cmd/git.exe', '-C', 'D:/Pontius', *args],
                          check=True, capture_output=True).stdout

actual = {}
for line in lines:
    digest, path = line[:-1].decode().split('  ', 1)
    assert path not in actual
    assert hashlib.sha256(git('cat-file', 'blob', meta['commit'] + ':' + path)).hexdigest() == digest
    actual[path] = digest
expected_paths = git('diff-tree', '-r', '--no-commit-id', '--no-renames', '--name-only',
                     meta['base'], meta['commit']).decode().splitlines()
assert set(actual) == set(expected_paths)
assert git('rev-parse', meta['ref']).decode().strip() == meta['commit']
assert git('rev-parse', meta['commit'] + '^').decode().strip() == meta['base']
assert git('rev-parse', meta['commit'] + '^{tree}').decode().strip() == meta['tree']
assert hashlib.sha256(raw).hexdigest() == meta['manifest_sha256']
handoff = (packet / 'handoff.md').read_text(encoding='utf-8')
assert meta['commit'] in handoff and meta['manifest_sha256'] in handoff
for name in ('workflow.md', 'controller-rulings.md'):
    assert hashlib.sha256((packet / 'inputs' / name).read_bytes()).hexdigest() in handoff
print(json.dumps(dict(packet=str(packet), candidate=meta['commit'],
                     manifest_sha256=meta['manifest_sha256'], complete_rows_sorted=True,
                     exact_blob_scope_verified=True)))
