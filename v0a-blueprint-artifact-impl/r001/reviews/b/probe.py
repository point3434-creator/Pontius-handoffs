"""Independent reviewer B read-only identity, registration, and codec falsifiers."""
import hashlib
from collections import Counter
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib

PACKET = Path(__file__).resolve().parents[2]
REPO = PACKET.parents[1] / 'authoring'
COMMIT = '6fb7f840d31d946e6b5dcb45faf82939dafd46ec'
BASE = 'c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98'
def git(*args):
    return subprocess.run([os.environ['PONTIUS_GIT'], '-c', 'safe.directory=' + REPO.as_posix(),
                           '-C', str(REPO), *args],
                          check=True, capture_output=True).stdout
def blob(ref, path):
    return git('cat-file', 'blob', ref + ':' + path)
paths = git('diff-tree', '-r', '--no-renames', '--no-commit-id', '--name-only',
            BASE, COMMIT).decode().splitlines()
rows = []
for path in paths:
    raw = blob(COMMIT, path)
    assert raw == (PACKET / 'files' / path).read_bytes(), path
    rows.append(hashlib.sha256(raw).hexdigest() + '  ' + path + '\n')
manifest = ''.join(sorted(rows)).encode()
assert manifest == (PACKET / 'manifest.sha256').read_bytes()
assert hashlib.sha256(manifest).hexdigest() == '26b8fb178aecaf3dccf038ee2e108dc4ce913f7f07baff10cff5efbe11011aee'
assert git('rev-parse', COMMIT + '^{tree}').decode().strip() == '6f8e17c12da42ad901c90bc764fc39958cca5854'
print('IDENTITY: all', len(rows), 'Git blobs and packet bytes match; manifest and tree verified')
for name, expected in [
    ('driver-amendment-authorization.md', '0d5cd53eb456a47a0ff346034fdfad173c77a39e37b030c99205c4913eeb2af7'),
    ('inventory-amendment-authorization.md', '666d89a6708c9d749265d816d063857432be42d754b6e76ad2dbafff6ba98ea3')]:
    assert hashlib.sha256((PACKET / 'inputs' / name).read_bytes()).hexdigest() == expected
old = json.loads(blob(BASE, 'tests/test-inventory.json'))
new = json.loads(blob(COMMIT, 'tests/test-inventory.json'))
assert all(row in new['entries'] for row in old['entries'])
added = [row for row in new['entries'] if row not in old['entries']]
assert len(old['entries']) == 2828 and len(added) == 23
assert {k: v for k, v in old.items() if k not in ('entries', 'discovery')} == {
    k: v for k, v in new.items() if k not in ('entries', 'discovery')}
counts = Counter(row['relative_path'] for row in added)
assert counts == {'tests/test_blueprint_artifact.py': 7,
                  'tests/test_blueprint_artifact_boundary.py': 4,
                  'tests/test_v0a_rehearsal_driver.py': 12}
assert all(row['assignment']['profile_name'] == 'current' for row in added)
print('INVENTORY: 2828 old rows identical; 23 additions:', dict(counts))
oldp = tomllib.loads(blob(BASE, 'tests/test-profiles.toml').decode())
newp = tomllib.loads(blob(COMMIT, 'tests/test-profiles.toml').decode())
for key in oldp:
    if oldp[key] != newp[key]:
        if key == 'profile':
            assert len(oldp[key]) == len(newp[key])
            for before, after in zip(oldp[key], newp[key]):
                for field in before:
                    if before[field] != after[field]:
                        assert isinstance(before[field], list), field
                        assert all(x in after[field] for x in before[field]), field
                        assert len(after[field]) - len(before[field]) == 3, field
                        print('PROFILE MEMBERS', before.get('name'), field, 'three additions')
                assert before.keys() == after.keys()
            continue
        assert isinstance(oldp[key], list), key
        assert all(item in newp[key] for item in oldp[key]), key
        extra = [item for item in newp[key] if item not in oldp[key]]
        assert len(extra) == 3, key
        print('PROFILE DELTA', key, 'exactly three additions, all old values identical')
assert oldp.keys() == newp.keys()
assert newp['spec_capabilities_sha256'] == newp['capability_bindings_sha256'] == '0' * 64

from pontius.blueprint_artifact.codec import decode_blueprint, encode_blueprint, BlueprintArtifactError
from pontius.immutable_blueprint import ImmutableBlueprintActionSource, BlueprintActionEntry, BlueprintDecisionKey
from pontius.no_limit_betting import BettingAction, BettingStreet
import pontius.blueprint_artifact.codec as codec
assert Path(codec.__file__).resolve() == Path('src/pontius/blueprint_artifact/codec.py').resolve()
assert hashlib.sha256(Path(codec.__file__).read_bytes()).hexdigest() == hashlib.sha256(blob(COMMIT, 'src/pontius/blueprint_artifact/codec.py')).hexdigest()
print('CODEC RESOLUTION:', codec.__file__, 'digits', sys.get_int_max_str_digits())
raw = Path('tests/fixtures/blueprint_artifact/raise_control.json').read_bytes()
source = decode_blueprint(raw)
def forge(value, **changes):
    result = object.__new__(type(value))
    for name in value.__slots__:
        object.__setattr__(result, name, changes.get(name, getattr(value, name)))
    return result
def wrap_key(key):
    return forge(source, entries=(forge(source.entries[0], key=key),))
failures = []
for cls, wrap in [
    (ImmutableBlueprintActionSource, lambda x: x),
    (BlueprintActionEntry, lambda x: forge(source, entries=(x,))),
    (BlueprintDecisionKey, wrap_key),
    (BettingAction, lambda x: forge(source, entries=(forge(source.entries[0], action=x),)))]:
    try:
        encode_blueprint(wrap(object.__new__(cls)))
    except BlueprintArtifactError:
        print('MISSING SLOTS typed refusal', cls.__name__)
    except Exception as error:
        failures.append((cls.__name__, type(error).__name__, str(error)))
    else:
        failures.append((cls.__name__, 'unexpected acceptance'))
print('MISSING SLOTS CONTRACT FAILURES:', json.dumps(failures))

history = decode_blueprint(Path('tests/fixtures/blueprint_artifact/history_control.json').read_bytes())
expected_history = (('preflop', 0, 'fold', None, 0, False, None, 0),
                    ('preflop', 1, 'check', None, 0, False, None, 0),
                    ('preflop', 2, 'call', None, 2, False, None, 0),
                    ('preflop', 3, 'raise', 6, 6, True, 3, 4))
expected_key = BlueprintDecisionKey(0, (0, 1), (20, 21, 22), 0, 1, 2, BettingStreet.FLOP,
    (200,) * 6, (200,) * 6, (0,) * 6, (0,) * 6, (False,) * 6, (0, 1), 2,
    (None,) * 6, expected_history)
assert history.entries[0].key == expected_key
assert history.entries[0].action.kind.value == 'check' and history.entries[0].action.raise_to is None
print('INDEPENDENT FULL HISTORY KEY: PASS')
for field in ('big_blind', 'last_full_raise_size', 'starting_stacks', 'stacks',
              'total_contributions', 'street_contributions', 'acted_at_bet'):
    for accepted, number in [(True, 10**640 - 1), (False, 10**640)]:
        value = number if field in ('big_blind', 'last_full_raise_size') else (number,) * 6
        candidate = wrap_key(forge(source.entries[0].key, **{field: value}))
        try:
            encoded = encode_blueprint(candidate)
            assert decode_blueprint(encoded).digest == candidate.digest
            assert accepted, field
        except BlueprintArtifactError:
            assert not accepted, field
print('ENCODER NUMERIC FAMILIES: boundary and overflow PASS')
print('PROBE COMPLETE; product-refusal finding count:', len(failures))
