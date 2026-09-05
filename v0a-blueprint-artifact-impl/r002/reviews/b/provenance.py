"""Read-only remaining receipt provenance and frozen hygiene checks."""
from pathlib import Path
import ast
import hashlib
import json
import subprocess

root = Path('D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001')
packet = root / 'packets/r002'
repo = root / 'authoring'
prior = '6fb7f840d31d946e6b5dcb45faf82939dafd46ec'
def blob(path):
    return subprocess.run(['C:/Program Files/Git/cmd/git.exe', '-C', str(repo),
                           'cat-file', 'blob', prior + ':' + path],
                          capture_output=True, check=True).stdout
for name in ('correction-codec-red-r001-311', 'correction-boundary-red-r001-311'):
    records = json.loads((root / 'run-records' / (name + '.json')).read_text())
    for path in ('src/pontius/blueprint_artifact/codec.py',
                 'tools/check_stabilization_boundaries.py'):
        assert (Path(records[-1]['snapshot']) / path).read_bytes() == blob(path)
print('Both behavioral RED snapshots: production codec and checker exactly r001')
for name in ('correction-boundary-green-floor-r001-311',
             'correction-boundary-green-native-r001-314',
             'correction-inventory-focused-floor-r001-311',
             'correction-inventory-focused-native-r001-314',
             'correction-registration-check-floor-r001-311',
             'correction-registration-check-native-r001-314'):
    records = json.loads((root / 'run-records' / (name + '.json')).read_text())
    snap = Path(records[-1]['snapshot'])
    mismatches = [p for row in (packet / 'manifest.sha256').read_text().splitlines()
                  for _, p in [row.split('  ', 1)]
                  if (snap / p).read_bytes() != (packet / 'files' / p).read_bytes()]
    assert mismatches == ['tests/test_blueprint_artifact.py'], (name, mismatches)
    old_lines = (snap / mismatches[0]).read_text().splitlines()
    new_lines = (packet / 'files' / mismatches[0]).read_text().splitlines()
    def cases(lines):
        tree = ast.parse('\n'.join(lines))
        return {node.name: ast.dump(node, include_attributes=False)
                for node in tree.body if isinstance(node, ast.ClassDef)
                and node.name == 'BlueprintArtifactTests'}
    assert cases(new_lines) == cases(old_lines)
print('All six 11/12 receipt snapshots: only main codec test differs; test class AST identical')
for path in packet.joinpath('files').rglob('*.py'):
    if path.parts[-1] not in ('codec.py', '__init__.py', 'test_blueprint_artifact.py',
                            'test_blueprint_artifact_boundary.py'):
        continue
    raw = path.read_bytes()
    assert b'\r' not in raw and not raw.startswith(b'\xef\xbb\xbf')
    assert not any(line.rstrip() != line for line in raw.splitlines())
    print(path.name, 'max_width', max(map(len, raw.decode().splitlines())))
for name in ('fix-review-b-targeted-311', 'fix-review-b-targeted-314',
             'fix-review-b-targeted-native-314'):
    path = root / 'run-records' / (name + '.json')
    print(path.name, hashlib.sha256(path.read_bytes()).hexdigest())
for path in sorted((packet / 'reviews/b').glob('*')):
    if path.is_file():
        print(path.name, hashlib.sha256(path.read_bytes()).hexdigest())
