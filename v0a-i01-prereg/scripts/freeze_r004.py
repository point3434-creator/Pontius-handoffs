"""Freeze and publish only the local r004 coordination packet, never an owner."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('D:/Pontius-worktrees/codex-v0a-increment-1-preregistration')
PACKET = Path('D:/Pontius-handoffs/v0a-i01-prereg/r004')
GIT = 'C:/Program Files/Git/cmd/git.exe'
BASE = 'ca0b2e41bbf5d9fc1649de20379299331de6591a'
REF = 'refs/heads/review/v0a-i01-prereg/r004'
PATHS = ['STATUS.md', 'docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md',
         'docs/workflow-amendment-2026-08-30.md']
for name in ('candidate.json', 'manifest.sha256', 'handoff.md'):
    if (PACKET / name).exists():
        raise RuntimeError('published packet inputs cannot be overwritten: ' + name)

env = os.environ.copy()
for field, variables in [('user.name', ('GIT_AUTHOR_NAME', 'GIT_COMMITTER_NAME')),
                         ('user.email', ('GIT_AUTHOR_EMAIL', 'GIT_COMMITTER_EMAIL'))]:
    value = subprocess.run([GIT, '-C', str(ROOT), 'config', '--get', field],
                           check=True, capture_output=True).stdout.decode().strip()
    if not value:
        raise RuntimeError('configured Git identity is absent')
    for variable in variables:
        env[variable] = value
index = PACKET / 'checks' / ('freeze-index-' + os.urandom(8).hex())
env.update(GIT_INDEX_FILE=str(index), GIT_CONFIG_NOSYSTEM='1',
           GIT_CONFIG_GLOBAL='NUL', GIT_NO_REPLACE_OBJECTS='1')

def git(*args):
    return subprocess.run([GIT, '-C', str(ROOT), *args], env=env, check=True,
                          capture_output=True).stdout

def publish(name, raw):
    with (PACKET / name).open('xb') as out:
        out.write(raw)

try:
    if git('rev-parse', 'HEAD').decode().strip() != BASE:
        raise RuntimeError('worktree base changed')
    git('read-tree', BASE)
    git('add', '--', *PATHS)
    tree = git('write-tree').decode().strip()
    commit = git('commit-tree', tree, '-p', BASE, '-m',
                 'Review candidate ' + REF + ' (frozen, not a decision commit)').decode().strip()
    changed = git('diff-tree', '-r', '--no-commit-id', '--no-renames', '--name-only',
                  BASE, commit).decode().splitlines()
    if sorted(changed) != sorted(PATHS):
        raise RuntimeError('unexpected changed-path scope')
    rows = []
    for path in sorted(PATHS):
        raw = git('cat-file', 'blob', commit + ':' + path)
        if b'\r' in raw or raw.startswith(b'\xef\xbb\xbf') or not raw.endswith(b'\n'):
            raise RuntimeError('noncanonical candidate document: ' + path)
        rows.append(hashlib.sha256(raw).hexdigest() + '  ' + path + '\n')
    manifest = ''.join(rows).encode()
    manifest_sha = hashlib.sha256(manifest).hexdigest()
    workflow_sha = hashlib.sha256((PACKET / 'inputs/workflow.md').read_bytes()).hexdigest()
    rulings_sha = hashlib.sha256((PACKET / 'inputs/controller-rulings.md').read_bytes()).hexdigest()
    git('diff', '--check', BASE, commit)
    git('update-ref', REF, commit, '0' * 40)
    metadata = dict(schema_version='pontius-handoff-candidate-v1', task_id='v0a-i01-prereg',
                    round='r004', ref=REF, commit=commit, base=BASE, tree=tree,
                    manifest_sha256=manifest_sha, date='2026-08-30')
    handoff = f'''# Cold review: v0a-i01-prereg/r004

Candidate ref: `{REF}`
Candidate commit: `{commit}`
Manifest SHA-256: `{manifest_sha}`
Base commit: `{BASE}`
Tree: `{tree}`
Tier: C specification review; no runtime implementation exists in this candidate.

The full commit and manifest bind identity; this path and the index only locate it.
The ref is local in D:/Pontius and its linked worktrees, not yet pushed.
Independently verify the exact candidate/base and blob-derived manifest. Read
candidate Git blobs, not mutable working files. Changed bytes or scope require
a new round. Never invoke a runtime, historical owner, or test from this packet.

## Scope

- STATUS.md
- docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md
- docs/workflow-amendment-2026-08-30.md

## Pinned inputs

At BASE: CLAUDE.md; docs/briefs/v0a-increment-1-brief.md (blob
8ef19c830eb929037c9cdd99e52cb0f0b56ddb28); governing ADRs and public APIs these
documents identify. The original base workflow remains retained; the controller
adopted the newer handoff structure captured in `inputs/workflow.md` at SHA-256
`{workflow_sha}`. Its specific overrides are captured in
`inputs/controller-rulings.md` at SHA-256 `{rulings_sha}` and the candidate amendment.
The adopted workflow capture is review input, not a modification included in this
evidence-repository candidate. The controller owns the separate primary edit.

## Review contract

Review the whole candidate against the brief and checklist v1: exact API feasibility,
action/clock/delivery boundaries, typed failure and replay contracts, public-ledger
accounting, hidden-card isolation, claims limits, and authority. No implementer
transcript, prior findings, disposition, or other reviewer's output is a cold input.
Do not read those files before issuing your independent verdict. No tests/owners or
candidate edits are requested; verification receipts are separate coordinator work.

CLEAN requires that no material finding survive verification. Every Critical or
Important finding binds to this pair, cites exact frozen locations, states a concrete
failing scenario, and gives the smallest correction. Return attributed findings to
your assigned `reviews/review-<NN>-<reviewer>.md`, and coordinate the verdict issuer's
single task-ledger append. A corrected finding/report is a new record, never overwrite.

The controller retired CodeRabbit and authorized the coherent bootstrap sequence;
do not resurrect those approval questions. Specific ceremonial-commit authorization
and any experiment invocation remain separate, ungranted gates.
'''
    publish('candidate.json', (json.dumps(metadata, indent=2) + '\n').encode())
    publish('manifest.sha256', manifest)
    publish('handoff.md', handoff.encode())
    print(json.dumps(metadata))
finally:
    index.unlink(missing_ok=True)
