"""Read-only independent frozen identity, scope and evidence audit."""
import hashlib
import json
from pathlib import Path
import subprocess
import tomllib
from collections import Counter

ROOT = Path('D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001')
PACKET = ROOT / 'packets/r002'
REPO = ROOT / 'authoring'
GIT = 'C:/Program Files/Git/cmd/git.exe'
BASE = 'c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98'
COMMIT = '5e56e4454f7b8ccb360d3e36245abc33318349bb'
PRIOR = '6fb7f840d31d946e6b5dcb45faf82939dafd46ec'
MANIFEST = '6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5'
def git(*args):
    return subprocess.run([GIT, '-c', f'safe.directory={REPO.as_posix()}',
                           '-C', str(REPO), *args], capture_output=True, check=True).stdout
def blob(commit, path):
    return git('cat-file', 'blob', f'{commit}:{path}')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
assert git('rev-parse', 'refs/heads/review/v0a-blueprint-artifact-impl/r002').strip().decode() == COMMIT
assert git('rev-parse', COMMIT + '^').strip().decode() == BASE
assert git('rev-parse', COMMIT + '^{tree}').strip().decode() == 'dc18ed133504fe6c7677b494bcefba311cc73704'
paths = git('diff', '--no-renames', '--name-only', BASE, COMMIT).decode().splitlines()
assert len(paths) == 12
rows = []
for path in paths:
    raw = blob(COMMIT, path)
    assert raw == (PACKET / 'files' / path).read_bytes(), path
    rows.append(f'{sha(raw)}  {path}\n')
manifest = ''.join(sorted(rows)).encode()
assert manifest == (PACKET / 'manifest.sha256').read_bytes()
assert sha(manifest) == MANIFEST
fix_paths = git('diff', '--no-renames', '--name-only', PRIOR, COMMIT).decode().splitlines()
assert set(fix_paths) == {'src/pontius/blueprint_artifact/codec.py',
                        'tests/test_blueprint_artifact.py',
                        'tests/test_blueprint_artifact_boundary.py',
                        'tools/check_stabilization_boundaries.py'}
for name, digest in {
    'inputs/driver-amendment-authorization.md': '0d5cd53eb456a47a0ff346034fdfad173c77a39e37b030c99205c4913eeb2af7',
    'inputs/inventory-amendment-authorization.md': '666d89a6708c9d749265d816d063857432be42d754b6e76ad2dbafff6ba98ea3',
    'coverage.md': 'ad3a47e26c2c8ff8a2d9b63422996d27e338f4041019c84235bfc4ffb1c20417',
}.items():
    assert sha((PACKET / name).read_bytes()) == digest
pins = {
    'tools/check_stabilization_boundaries.py': 'c3f739f001fd70d5326bc7ec4609f483e1ba5525',
    'tools/generate_test_inventory.py': 'da0fb1efd0f38747ad90f91aea572789ace7e0aa',
    'tests/test_inventory_and_profiles.py': '45c65de9cde1506db8ad900d624ec69fce5b9893',
    'tests/test-inventory.json': 'd655d205053c13da2634e8a22b36c58b72ee340b',
    'tests/test-profiles.toml': 'ada2c73eb0834fe9822b84e5d31b2ffdfb78b4a6',
    '.github/workflows/ci.yml': '0585dcd6191dbe97b4f00f3866cc5da9798b4c51',
}
for path, pin in pins.items():
    assert git('rev-parse', f'{BASE}:{path}').strip().decode() == pin
git('diff', '--check', BASE, COMMIT)
source_lines = sum(len(blob(COMMIT, p).splitlines()) for p in paths if p.startswith('src/'))
test_lines = sum(len(blob(COMMIT, p).splitlines()) for p in paths if p.startswith('tests/test_blueprint'))
fixture_bytes = sum(len(blob(COMMIT, p)) for p in paths if '/fixtures/' in p)
manual = sum(int(a) + int(b) for a, b, p in
             (r.split('\t') for r in git('diff', '--numstat', BASE, COMMIT).decode().splitlines())
             if p in pins and p not in ('tests/test-inventory.json', 'tests/test-profiles.toml'))
assert (source_lines, test_lines, fixture_bytes, manual) == (290, 300, 1699, 97)
old, new = [json.loads(blob(c, 'tests/test-inventory.json')) for c in (BASE, COMMIT)]
old_rows = {r['stable_id']: r for r in old['entries']}
new_rows = {r['stable_id']: r for r in new['entries']}
assert len(old_rows) == 2828
assert all(new_rows[k] == v for k, v in old_rows.items())
added = [v for k, v in new_rows.items() if k not in old_rows]
assert Counter(v['relative_path'] for v in added) == {
    'tests/test_blueprint_artifact.py': 7, 'tests/test_blueprint_artifact_boundary.py': 4,
    'tests/test_v0a_rehearsal_driver.py': 12}
assert all(v['assignment']['profile_name'] == 'current' for v in added)
old, new = [tomllib.loads(blob(c, 'tests/test-profiles.toml').decode()) for c in (BASE, COMMIT)]
for key in old:
    if key not in ('payload', 'profile', 'stabilization_test_files'):
        assert old[key] == new[key], key
for key, identity in [('payload', 'payload_id'), ('profile', 'name')]:
    old_map = {r[identity]: r for r in old[key]}
    new_map = {r[identity]: r for r in new[key]}
    for name, row in old_map.items():
        if key == 'profile' and name == 'current':
            assert {k: v for k, v in row.items() if k != 'payload_ids'} == {
                k: v for k, v in new_map[name].items() if k != 'payload_ids'}
            assert set(row['payload_ids']) <= set(new_map[name]['payload_ids'])
        else:
            assert new_map[name] == row, name
assert new['capability_bindings_sha256'] == new['spec_capabilities_sha256'] == '0' * 64
print('Identity, 12 overlay blobs, four FIX paths, pins, budgets and 2828 preserved rows PASS')
print('Budgets:', source_lines, test_lines, fixture_bytes, manual)
families = ('correction-final-codec-', 'correction-boundary-green-',
            'correction-inventory-focused-', 'correction-registration-check-',
            'correction-registration-write-final-', 'correction-codec-red-r001-',
            'correction-boundary-red-r001-')
for path in sorted((ROOT / 'run-records').glob('*.json')):
    if not path.name.startswith(families):
        continue
    records = json.loads(path.read_text(encoding='utf-8-sig'))
    records = records if isinstance(records, list) else [records]
    last = records[-1]
    matches = sum((Path(last['snapshot']) / p).read_bytes() == blob(COMMIT, p) for p in paths)
    print(path.name, 'exits', [r['exit_code'] for r in records], 'matching_blobs', matches,
          'argv', last['argv'], 'output', last['stdout'][-500:], last['stderr'][-800:])
    print('receipt_sha256', sha(path.read_bytes()))
