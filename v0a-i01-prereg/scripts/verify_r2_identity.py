"""Read-only verification of the frozen pair and returned review binding."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path('D:/Pontius-worktrees/codex-v0a-increment-1-preregistration')
REPORT = Path('D:/Pontius-worktrees/v0a-increment-1-preregistration-review')
GIT = 'C:/Program Files/Git/cmd/git.exe'
identity = json.loads((REPORT / 'r2-candidate.json').read_text(encoding='utf-8'))

def git(*args):
    return subprocess.run([GIT, '-C', str(ROOT), *args], check=True,
                          capture_output=True).stdout

candidate = identity['candidate']
assert git('rev-parse', identity['ref']).decode().strip() == candidate
assert git('rev-parse', candidate + '^').decode().strip() == identity['base']
paths = git('diff-tree', '-r', '--no-commit-id', '--no-renames', '--name-only',
            candidate + '^', candidate).decode().splitlines()
assert sorted(paths) == sorted(identity['paths'])
rows = []
for path in sorted(paths):
    blob = git('cat-file', 'blob', candidate + ':' + path)
    assert b'\r' not in blob and not blob.startswith(b'\xef\xbb\xbf')
    rows.append(hashlib.sha256(blob).hexdigest() + '  ' + path + '\n')
manifest = ''.join(rows).encode()
assert manifest == (REPORT / 'r2-manifest.txt').read_bytes()
assert hashlib.sha256(manifest).hexdigest() == identity['manifest_sha256']
review_bytes = (REPORT / 'r2-review-claude.md').read_bytes()
review = review_bytes.decode('utf-8')
assert candidate in review and identity['manifest_sha256'] in review
ledger = (REPORT / 'progress.md').read_text(encoding='utf-8').splitlines()
matches = [line for line in ledger if '| claude/cold_review_c |' in line]
assert len(matches) == 1
assert candidate in matches[0] and identity['manifest_sha256'] in matches[0]
workflow = git('cat-file', 'blob', identity['base'] + ':docs/workflow.md')
assert hashlib.sha256(workflow).hexdigest() == '2ea6b7c849ec4d991ae68fcc9b069b6892b51c5831f5d21a424a709fec05b7bf'
print(json.dumps(dict(candidate=candidate, manifest_sha256=identity['manifest_sha256'],
                     scope=paths, review_sha256=hashlib.sha256(review_bytes).hexdigest(),
                     review_binding_verified=True, single_ledger_entry=True,
                     sealed_workflow_verified=True)))
