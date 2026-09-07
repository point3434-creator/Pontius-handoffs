"""Adopt only the exact ADR-0513 candidate authorized by the current user."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('blueprint_design_admin', HERE/'admin.py')
admin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admin)
MAIN = Path('D:/Pontius')
PACKET = admin.PACKETS/'r001'
CANDIDATE = 'ddf652d00e68a84e1eef03d5bd4df37c5a022b79'
MANIFEST = 'e68bf5eb2bf2338c9217717a960d79a5624abdb62b09c0914609fa6a3fc35aa4'
ORIGIN = 'https://github.com/point3434-creator/Pontius.git'
TITLE = 'Open the immutable blueprint preparation source round'


def head(repo):
    return admin.git('rev-parse', 'HEAD', cwd=repo).decode().strip()


def remote():
    rows = admin.git('ls-remote', '--exit-code', 'origin', 'refs/heads/master').decode().splitlines()
    assert len(rows) == 1 and rows[0].split()[1] == 'refs/heads/master'
    return rows[0].split()[0]


frozen = json.loads((PACKET/'candidate.json').read_bytes())
assert frozen['commit'] == CANDIDATE and frozen['manifest_sha256'] == MANIFEST
assert head(admin.WORK) == head(MAIN) == admin.BASE
assert admin.git('branch', '--show-current').decode().strip() == 'codex/blueprint-preparation'
assert admin.git('branch', '--show-current', cwd=MAIN).decode().strip() == 'master'
assert not admin.git('status', '--porcelain', '--untracked-files=no', cwd=MAIN)
assert not admin.git('diff', '--cached', '--name-only')
for flag in ([], ['--push']):
    assert admin.git('remote', 'get-url', *flag, 'origin').decode().strip() == ORIGIN
assert remote() == admin.BASE
changed = admin.git('diff', '--name-only', admin.BASE, CANDIDATE).decode().splitlines()
assert set(changed) == set(admin.PATHS)
rows = []
for path in changed:
    raw = admin.git('show', CANDIDATE+':'+path)
    assert raw == (admin.WORK/path).read_bytes() == (PACKET/'blobs'/path).read_bytes()
    rows.append((hashlib.sha256(raw).hexdigest()+'  '+path+'\n').encode())
manifest = b''.join(sorted(rows))
assert manifest == (PACKET/'manifest.sha256').read_bytes()
assert hashlib.sha256(manifest).hexdigest() == MANIFEST
qualification = json.loads((PACKET/'qualification.json').read_bytes())
assert qualification['candidate'] == frozen
for review in qualification['reviews']:
    assert review['defect'] == 'CLEAN' and review['design'] == 'SOUND'
    assert hashlib.sha256(Path(review['path']).read_bytes()).hexdigest() == review['sha256']
for slot in ('311', '314'):
    checks = PACKET/'checks'/slot
    complete = json.loads((checks/'completion.json').read_bytes())
    assert complete['candidate'] == frozen and complete['all_gates_passed']
    for gate in ('runtime', 'status-check', 'status-tests'):
        assert json.loads((checks/(gate+'-receipt.json')).read_bytes())['exit_code'] == 0
    raw = (checks/'status-tests-stderr.bin').read_bytes()
    assert b'Ran 12 tests in ' in raw and b'OK' in raw and b'skipped=' not in raw
adoption = admin.ROOT/'adoption'
adoption.mkdir()
with (adoption/'adopt_authorized.py').open('xb') as out:
    out.write(Path(__file__).read_bytes())
admin.write(adoption/'authorization.json', dict(
    user_message='Commit and push then next',
    approval_question='Do you approve committing and pushing this exact ADR-0513 candidate, '
        'publishing its review packet to the private Pontius-handoffs repository, '
        'and proceeding with the scoped implementation?',
    candidate=frozen, decision='ADR-0513',
    packet_destination='https://github.com/point3434-creator/Pontius-handoffs',
    recorded_utc=datetime.now(timezone.utc).isoformat()))
for path in changed:
    oid = admin.git('rev-parse', CANDIDATE+':'+path).decode().strip()
    admin.git('update-index', '--add', '--cacheinfo', '100644', oid, path)
assert admin.git('write-tree').decode().strip() == frozen['tree']
admin.git('diff', '--cached', '--check')
output = admin.git('commit', '-m', TITLE)
commit = head(admin.WORK)
assert admin.git('rev-parse', commit+'^{tree}').decode().strip() == frozen['tree']
assert admin.git('rev-parse', commit+'^').decode().strip() == admin.BASE
admin.write(adoption/'commit.json', dict(commit=commit, tree=frozen['tree'],
    title=TITLE, output=output.decode(), recorded_utc=datetime.now(timezone.utc).isoformat()))
print(output.decode(), flush=True)
admin.git('push', 'origin', 'HEAD:refs/heads/master')
assert remote() == commit
admin.git('-c', 'core.autocrlf=false', 'merge', '--ff-only', commit, cwd=MAIN)
assert head(MAIN) == commit
for path in changed:
    expected = admin.git('show', commit+':'+path)
    assert (admin.WORK/path).read_bytes() == (MAIN/path).read_bytes() == expected
assert not admin.git('status', '--porcelain', '--untracked-files=no')
assert not admin.git('status', '--porcelain', '--untracked-files=no', cwd=MAIN)
result = dict(status='COMMITTED_AND_PUSHED', commit=commit, tree=frozen['tree'],
    parent=admin.BASE, approved_candidate=CANDIDATE, origin=ORIGIN,
    remote_branch='master', remote_verified=True, primary_fast_forwarded=True,
    recorded_utc=datetime.now(timezone.utc).isoformat())
admin.write(adoption/'result.json', result)
print(json.dumps(result), flush=True)
