"""Verify the frozen add-only population correction; no payload execution."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

H = Path(r'D:\Pontius-handoffs')
T = H / 'v0a-i01-c-authority'
COMMIT = '2393d9b3680426f5a3169ddb19e7b542ce68531d'
MANIFEST = '3ca45c9839ae6f7101d6405607260d766a18ed6ab260886c65a92bffb1a2471d'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
def blob(name):
    raw = subprocess.run([r'C:\Program Files\Git\cmd\git.exe', '-C', str(H),
                          'cat-file', 'blob', COMMIT + ':v0a-i01-c-authority/' + name],
                         capture_output=True, check=True, timeout=60).stdout
    assert raw == (T / name).read_bytes()
    return raw

assert sys.version_info[:3] == (3, 11, 15)
manifest = blob('rewrite-r2-population-v2-manifest.sha256')
assert sha(manifest) == MANIFEST
assert manifest.splitlines(keepends=True) == sorted(manifest.splitlines(keepends=True))
for row in manifest.decode().splitlines():
    wanted, name = row.split('  ', 1)
    assert sha(blob(name)) == wanted
old_raw = blob('tests-checks/rewrite-r2-identity-population-v1.json')
new_raw = blob('tests-checks/rewrite-r2-identity-population-v2.json')
original_raw = blob('rewrite-early-population-v1.json')
assert sha(old_raw) == '30295f39daafcf265103cd78f3de50393c9111633ca3d5f8515e3f77c9a1197a'
assert sha(new_raw) == '8ab800c1361ca53f4f294bd32e308ecb7061e031b60d32dc74d7fdf52cc5ce3b'
assert sha(original_raw) == '3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce'
old, new, original = map(json.loads, (old_raw, new_raw, original_raw))
restored = new['envelopes'].pop('name_environment_public')
assert restored == original['envelopes']['name_environment_public']
assert new == old
assert (json.dumps(new, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode() == old_raw
new['envelopes']['name_environment_public'] = restored
assert len(new['cases']) == 12
for identifier, case in new['cases'].items():
    assert case['envelope_ref'] in new['envelopes']
unchanged = original['gates']['A']['ordered_case_ids'] + ['helper65', 'generator70']
for identifier in unchanged:
    assert new['cases'][identifier] == original['cases'][identifier]
    envelope = new['cases'][identifier]['envelope_ref']
    assert new['envelopes'][envelope] == original['envelopes'][envelope]
report = {'pass': True, 'kind': 'static population correction closure only',
          'commit': COMMIT, 'manifest_sha256': MANIFEST,
          'population_sha256': sha(new_raw), 'only_semantic_delta': '/envelopes/name_environment_public',
          'inverse_raw_bytes_exact': True, 'resolved_case_count': 12,
          'unchanged_original_descriptors_and_resolved_envelopes': unchanged,
          'runtime': list(sys.version_info[:3]), 'payload_executed': False,
          'verifier_sha256': sha(Path(__file__).read_bytes())}
target = T / 'coordinator-rewrite-r2-population-v2-verification.json'
with target.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'pass': True, 'sha256': sha(target.read_bytes())}))
