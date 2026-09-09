"""Local documentation-review helper; never an experiment owner."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path('D:/Pontius-worktrees/codex-v0a-increment-1-preregistration')
REPORT = Path('D:/Pontius-worktrees/v0a-increment-1-preregistration-review')
GIT = 'C:/Program Files/Git/cmd/git.exe'
PATHS = ['STATUS.md', 'docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md',
         'docs/workflow-amendment-2026-08-30.md']
if sys.argv[1:] != ['r3']:
    raise RuntimeError('this helper admits only the fresh r3 freeze')
REF = 'refs/heads/review/v0a-increment-1-prereg-' + sys.argv[1]
env = os.environ.copy()
for field, variables in [('user.name', ('GIT_AUTHOR_NAME', 'GIT_COMMITTER_NAME')),
                         ('user.email', ('GIT_AUTHOR_EMAIL', 'GIT_COMMITTER_EMAIL'))]:
    identity = subprocess.run([GIT, '-C', str(ROOT), 'config', '--get', field],
                              check=True, capture_output=True).stdout.decode().strip()
    if not identity:
        raise RuntimeError('configured Git identity is absent')
    for variable in variables:
        env[variable] = identity
index = REPORT / ('index-' + os.urandom(8).hex())
env['GIT_INDEX_FILE'] = str(index)
env['GIT_CONFIG_NOSYSTEM'] = '1'
env['GIT_CONFIG_GLOBAL'] = 'NUL'
env['GIT_NO_REPLACE_OBJECTS'] = '1'

def git(*args):
    result = subprocess.run([GIT, '-C', str(ROOT), *args], env=env, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace'))
    return result.stdout

try:
    base = git('rev-parse', 'HEAD').decode().strip()
    if base != 'ca0b2e41bbf5d9fc1649de20379299331de6591a':
        raise RuntimeError('unexpected base')
    git('read-tree', base)
    git('add', '--', *PATHS)
    tree = git('write-tree').decode().strip()
    candidate = git('commit-tree', tree, '-p', base, '-m', 'Review candidate ' + REF + ' (frozen, not a decision commit)').decode().strip()
    git('update-ref', REF, candidate, '0' * 40)
    changed = git('diff-tree', '--no-commit-id', '--name-only', '-r', candidate).decode().splitlines()
    if sorted(changed) != sorted(PATHS):
        raise RuntimeError('candidate scope differs')
    rows = []
    for path in sorted(PATHS):
        raw = git('cat-file', 'blob', candidate + ':' + path)
        if b'\r' in raw or raw.startswith(b'\xef\xbb\xbf') or not raw.endswith(b'\n'):
            raise RuntimeError('noncanonical document: ' + path)
        rows.append(hashlib.sha256(raw).hexdigest() + '  ' + path + '\n')
    manifest = ''.join(rows)
    result = {'base': base, 'ref': REF, 'candidate': candidate, 'tree': tree,
              'manifest_sha256': hashlib.sha256(manifest.encode()).hexdigest(),
              'paths': PATHS, 'remote_publication': 'not_performed'}
    (REPORT / (sys.argv[1] + '-manifest.txt')).write_text(manifest, encoding='ascii', newline='\n')
    (REPORT / (sys.argv[1] + '-candidate.json')).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(result))
finally:
    index.unlink(missing_ok=True)
