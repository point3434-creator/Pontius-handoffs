"""Targeted independent frozen-r002 review probe; snapshot execution only."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
from dataclasses import replace
import pontius.blueprint_artifact.codec as codec
from pontius.immutable_blueprint import BlueprintActionEntry, ImmutableBlueprintActionSource

root = Path.cwd()
packet = Path('D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/packets/r002')
assert 'snapshots' in root.parts
assert Path(codec.__file__).resolve() == root / 'src/pontius/blueprint_artifact/codec.py'
for row in (packet / 'manifest.sha256').read_text().splitlines():
    digest, path = row.split('  ', 1)
    assert hashlib.sha256((root / path).read_bytes()).hexdigest() == digest, path
assert sys.get_int_max_str_digits() == 640
raw = (root / 'tests/fixtures/blueprint_artifact/history_control.json').read_bytes()
source = codec.decode_blueprint(raw)
entry = source.entries[0]
count = 0
def refused(fn, value):
    global count
    try:
        fn(value)
    except codec.BlueprintArtifactError:
        count += 1
    else:
        raise AssertionError('Expected typed refusal')
def clone(value, omit=None, **changes):
    result = object.__new__(type(value))
    for name in value.__slots__:
        if name != omit:
            object.__setattr__(result, name, changes.get(name, getattr(value, name)))
    return result
def with_key(key):
    return clone(source, entries=(clone(entry, key=key),))
def with_action(action):
    return clone(source, entries=(clone(entry, action=action),))
for obj, wrap in ((source, lambda x: x),
                  (entry, lambda x: clone(source, entries=(entry, x))),
                  (entry.key, with_key), (entry.action, with_action)):
    for slot in obj.__slots__:
        refused(codec.encode_blueprint, wrap(clone(obj, omit=slot)))
print('Every required source/entry/key/action slot omission refused:', count)

markers = []
class ForeignInt(int):
    def __str__(self):
        markers.append('str'); raise AssertionError('foreign str')
    def __eq__(self, other):
        markers.append('eq'); raise AssertionError('foreign eq')
    def __hash__(self):
        markers.append('hash'); raise AssertionError('foreign hash')
class ForeignStr(str):
    def strip(self, *args):
        markers.append('strip'); raise AssertionError('foreign strip')
class ForeignTuple(tuple):
    def __iter__(self):
        markers.append('iter'); raise AssertionError('foreign iter')
for value in (with_key(clone(entry.key, small_blind=ForeignInt(1))),
              with_key(clone(entry.key, stacks=(ForeignInt(2),) * 6)),
              with_key(clone(entry.key, public_history=(
                  ('preflop', 0, ForeignStr('fold'), None, 0, False, None, 0),))),
              with_key(clone(entry.key, acted_at_bet=(ForeignInt(0),) * 6)),
              with_key(clone(entry.key, private_hand=ForeignTuple((0, 1)))),
              clone(source, source_id=ForeignStr('source')),
              clone(source, entries=ForeignTuple((entry,)))):
    refused(codec.encode_blueprint, value)
assert not markers

maximum = 10**640 - 1
doc = json.loads(raw)
numeric_paths = [('entries', 0, 'key', field) for field in
                 ('big_blind', 'last_full_raise_size')]
numeric_paths += [('entries', 0, 'key', field, 0) for field in
                  ('starting_stacks', 'stacks', 'total_contributions',
                   'street_contributions', 'acted_at_bet')]
numeric_paths += [('entries', 0, 'key', 'public_history', row, col)
                 for row, col in ((2, 4), (3, 3), (3, 4), (3, 7))]
for path in numeric_paths:
    for number, accepted in ((maximum, True), (10**640, False)):
        altered = json.loads(raw)
        target = altered
        for component in path[:-1]:
            target = target[component]
        target[path[-1]] = 'NUMERIC_TOKEN'
        wire = json.dumps(altered).encode().replace(
            b'"NUMERIC_TOKEN"', b'9' * 640 if accepted else b'1' + b'0' * 640)
        key = entry.key
        tail = path[3:]
        if tail[0] == 'public_history':
            rows = list(key.public_history)
            row = list(rows[tail[1]])
            row[tail[2]] = number
            rows[tail[1]] = tuple(row)
            key = clone(key, public_history=tuple(rows))
        elif len(tail) == 2:
            values = list(getattr(key, tail[0]))
            values[tail[1]] = number
            key = clone(key, **{tail[0]: tuple(values)})
        else:
            key = clone(key, **{tail[0]: number})
        exact = with_key(key)
        if accepted:
            admitted = codec.decode_blueprint(wire)
            assert admitted == exact, path
            assert codec.decode_blueprint(codec.encode_blueprint(exact)).digest == exact.digest
        else:
            refused(codec.decode_blueprint, wire)
            refused(codec.encode_blueprint, exact)
print('Additional numeric paths closed at min640:', len(numeric_paths))

for label in ('\U0001f680', 'e\u0301', '\u00e9', '\x00x'):
    exact = ImmutableBlueprintActionSource(label)
    literal = json.dumps({'version': 'pontius-v0a-blueprint-artifact-v1',
                          'source_id': label, 'entries': []}, ensure_ascii=False).encode()
    escaped = json.dumps({'version': 'pontius-v0a-blueprint-artifact-v1',
                          'source_id': label, 'entries': []}, ensure_ascii=True).encode()
    assert codec.decode_blueprint(literal).digest == codec.decode_blueprint(escaped).digest
    assert codec.decode_blueprint(codec.encode_blueprint(exact)).source_id == label
for payload in (b'\xef\xbb\xbf' + raw, raw + b'false', b'"\xed\xa0\x80"'):
    refused(codec.decode_blueprint, payload)
alias = raw.replace(b'"source_id":', b'"source_id":"x","source_\\u0069d":')
refused(codec.decode_blueprint, alias)
print('Nested foreign hooks untouched; Unicode/no-normalization and parser aliases PASS')

spec = importlib.util.spec_from_file_location('review_b_gate', root / 'tools/check_stabilization_boundaries.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
checker.check_repository(root)
for relative in ('src/pontius/blueprint_artifact.py',
                 'src/pontius/blueprint_artifact/nested/__init__.py'):
    target = root / relative
    assert not target.exists()
    created_parent = not target.parent.exists()
    target.parent.mkdir(exist_ok=True)
    try:
        target.write_bytes(b'"""Owned review negative fixture."""\n')
        try:
            checker.check_repository(root)
        except checker.BoundaryError as error:
            assert 'unclassified stabilization origin' in str(error)
        else:
            raise AssertionError('Undeclared path accepted: ' + relative)
    finally:
        target.unlink()
        if created_parent:
            target.parent.rmdir()
print('Actual public gate positive, flat and nested-origin negatives PASS')
print('Targeted probe PASS; typed refusal checks:', count)
