"""Read frozen R2 inputs with stdlib only; never execute a fixture or Model."""
from pathlib import Path
import ast
import hashlib
import json
import subprocess
import sys

H = Path(r'D:\Pontius-handoffs')
T = H / 'v0a-i01-c-authority'
GIT = r'C:\Program Files\Git\cmd\git.exe'
COMMIT = 'aa75536cad0ae54b76b02f9351cd7bc789d7f443'
MANIFEST = '96d1b71a3a08b73d2cf1bb09d3ac06473253b6291addf2fbefc541e3bbe3b41f'
sha = lambda b: hashlib.sha256(b).hexdigest()
canonical = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def blob(relative):
    return subprocess.run([GIT, '-C', str(H), 'cat-file', 'blob',
                           COMMIT + ':v0a-i01-c-authority/' + relative],
                          capture_output=True, check=True, timeout=60).stdout

assert sys.version_info[:3] == (3, 11, 15)
manifest = blob('rewrite-r2-inputs-v1-manifest.sha256')
assert sha(manifest) == MANIFEST
assert manifest.splitlines(keepends=True) == sorted(manifest.splitlines(keepends=True))
pins = {}
for line in manifest.decode().splitlines():
    wanted, relative = line.split('  ', 1)
    raw = blob(relative)
    assert sha(raw) == wanted and (T / relative).read_bytes() == raw
    pins[relative] = wanted

def read(relative, wanted=None):
    raw = blob(relative)
    assert raw == (T / relative).read_bytes()
    if wanted is not None:
        assert sha(raw) == wanted
    pins[relative] = sha(raw)
    return json.loads(raw)

old = read('tests-checks/name-environment-cases-v1.json',
           'd07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c')
old_population = read('rewrite-early-population-v1.json',
                      '3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce')
new = read('tests-checks/rewrite-r2-identity-cases-v1.json')
population = read('tests-checks/rewrite-r2-identity-population-v1.json')
assert len(new['cases']) == new['planned_cases'] == 4
assert new['planned_projections'] == sum(len(c['witnesses']) for c in new['cases']) == 16
assert new['exercised_cases'] == new['exercised_projections'] == 0
assert new['public_envelope']['selector_domain_argument'] is False
old_by_id = {c['id']: c for c in old['cases']}
regions = ('true', 'false', 'none', 'other')
case_checks = []
for case in new['cases']:
    predecessor = old_by_id[case['predecessor']['id']]
    assert case['id'] == 'identity-' + predecessor['id']
    assert case['predecessor']['record_canonical_sha256'] == sha(canonical(predecessor))
    for field, predecessor_pin in (('source', 'source_sha256'), ('oracle_source', 'model_sha256')):
        assert sha(predecessor[field].encode()) == case['predecessor'][predecessor_pin]
        tree = ast.parse(case[field])
        assert not any(isinstance(n, (ast.Eq, ast.NotEq)) for n in ast.walk(tree)
                       if field == 'source')
        # Reverse only the admitted selector latch and the three predicates.
        lines = case[field].splitlines(keepends=True)
        latch = [i for i, line in enumerate(lines) if line.strip() == 'selector = self.choice']
        assert len(latch) == 1
        del lines[latch[0]]
        reversed_source = ''.join(lines)
        for index, singleton in enumerate(('True', 'False', 'None')):
            assert reversed_source.count('selector is ' + singleton) == 1
            reversed_source = reversed_source.replace('selector is ' + singleton,
                                                       'self.choice == ' + str(index))
        if field == 'oracle_source':
            cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
            ctor = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == '__init__')
            ctor_lines = case[field].splitlines(keepends=True)[ctor.lineno - 1:ctor.end_lineno]
            assert reversed_source.count(''.join(ctor_lines)) == 1
            reversed_source = reversed_source.replace(''.join(ctor_lines), '', 1)
        assert reversed_source == predecessor[field], (case['id'], field)
    for field in ('ambient', 'changed', 'successors', 'exit', 'classification', 'unreachable_events'):
        assert case[field] == predecessor[field]
    for index, (actual, previous) in enumerate(zip(case['witnesses'], predecessor['witnesses'], strict=True)):
        expected = dict(previous)
        assert type(expected.pop('choice')) is int and previous['choice'] == index
        expected['region'] = regions[index]
        assert actual == expected
    binding = population['cases'][case['id']]
    assert binding['case_record_canonical_sha256'] == sha(canonical(case))
    case_checks.append({'id': case['id'], 'source_and_Model_inverse_exact': True,
                        'witness_discriminator_only_delta': True})

unchanged = old_population['gates']['A']['ordered_case_ids'] + ['helper65', 'generator70']
assert len(unchanged) == 8
for identifier in unchanged:
    assert population['cases'][identifier] == old_population['cases'][identifier]
assert population['original_caps'] == old_population['original_caps']
assert population['original_test_module'] == old_population['original_test_module']
for envelope in ('storage_composition_public', 'original_design_review'):
    assert population['envelopes'][envelope] == old_population['envelopes'][envelope]
expected_envelope = dict(old_population['envelopes']['name_environment_public'])
expected_envelope['selector_domain_argument'] = False
assert population['envelopes']['identity_name_environment_public'] == expected_envelope
assert population['gates']['A'] == old_population['gates']['A']
gate = population['gates']['B_identity']
assert gate['ordered_case_ids'] == unchanged + [c['id'] for c in new['cases']]
assert gate['public_analysis_count'] == 12 and gate['independent_model_projections'] == 24
assert gate['engineering_continuation_work_maximum'] == 196608
assert gate['production_work_cap_unchanged'] == 262144
assert len(population['remaining_affected_scale_siblings']) == 12
unresolved = {identifier: binding['envelope_ref']
              for identifier, binding in population['cases'].items()
              if binding['envelope_ref'] not in population['envelopes']}
report = {'kind': 'root static input custody and exact-delta verification',
          'commit': COMMIT, 'manifest_sha256': MANIFEST, 'runtime': list(sys.version_info[:3]),
          'pins': pins, 'case_checks': case_checks, 'unchanged_descriptors': unchanged,
          'public_envelope_preserved_no_selector_domain': True,
          'caps_and_original_test_module_preserved': True,
          'source_Model_or_candidate_execution': False,
          'claims_exclude': ['Model outcomes', 'analyzer semantics', 'mechanism coverage', 'work reserve'],
          'unresolved_envelope_refs': unresolved,
          'verifier_sha256': sha(Path(__file__).read_bytes()), 'pass': not unresolved}
destination = T / 'coordinator-rewrite-r2-inputs-verification-v1.json'
with destination.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'pass': report['pass'], 'unresolved_envelope_refs': unresolved,
                  'path': str(destination), 'sha256': sha(destination.read_bytes())}))
