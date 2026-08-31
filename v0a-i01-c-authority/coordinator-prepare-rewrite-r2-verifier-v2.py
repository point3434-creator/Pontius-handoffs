"""Create-only data verifier correction; no candidate or Model execution."""
from pathlib import Path
import ast
import hashlib
import json

P = Path(r'D:\Pontius')
T = Path(r'D:\Pontius-handoffs\v0a-i01-c-authority')
raw = (P / 'codex-verify-rewrite-r2-baseline-v1.py').read_bytes()
assert hashlib.sha256(raw).hexdigest() == '22def22c092c8c8b499303974691b2b877bc45c75a2665d23618764cb7edbad9'
text = raw.decode()
changes = {
    "pop['gates']['B']['ordered_case_ids']": "pop['gates']['B_identity']['ordered_case_ids']",
    "'-311-verification-v1.json'": "'-311-verification-v2.json'",
    "outputs = {key: read(entry['path']) for key, entry in r['outputs'].items()}": '''copies = {
    'probe.py': 'probe', 'control.py': 'control', 'plan.md': 'plan', 'observer-map.json': 'observer_map',
    'retained-source.py': 'overlay', 'population.json': 'population', 'depth-provenance.py': 'depth_provenance',
    'storage-composition-cases-v1.json': 'storage', 'name-environment-cases-v1.json': 'name_environment',
    'rewrite-r2-identity-cases-v1.json': 'identity', 'prior-population.json': 'prior_population',
    'identity-coverage.json': 'coverage', 'observer-spec.md': 'spec', 'authoring-disposition.md': 'authorization',
    'plan-addendum.md': 'addendum', 'source-model.diff': 'source_model_diff'}
check(set(copies) | {'run.json'} == payload_names, 'complete runtime-copy closure')
for name, key in copies.items():
    check(read(snapshot / PAYLOAD / name) == read(r['input_paths'][key]), 'runtime copy equals verified input: ' + name)
check(digest(read(snapshot / 'tools/generate_test_inventory.py')) == SOURCE
      and digest(read(snapshot / PAYLOAD / 'retained-source.py')) == SOURCE
      and r['input_hashes_before']['overlay'] == r['input_hashes_before']['core_watch'] == SOURCE,
      'actual executable and retained source equal held R1')
run_config = json.loads(read(snapshot / PAYLOAD / 'run.json'))
check(all(key in r and r[key] == value for key, value in run_config.items()), 'run config equals verified receipt context')
outputs = {key: read(entry['path']) for key, entry in r['outputs'].items()}''',
    "check(digest(pack_raw) == r['pack_sha256'][scope], 'pack pin')": '''population_key = 'tests-checks/' + filename
    population_pin = (pop['new_inputs'][population_key] if scope == 'identity'
                      else pop['original_inputs_unchanged'][population_key]['sha256'])
    check(digest(pack_raw) == r['pack_sha256'][scope] == population_pin, 'population-bound pack pin')''',
    "fixture = None if depth else packs[scope][name]": '''fixture = None if depth else packs[scope][name]
    if fixture is not None:
        record_raw = json.dumps(fixture, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
        check(digest(record_raw) == desc['case_record_canonical_sha256']
              and digest(fixture['source'].encode()) == desc['source']['sha256']
              and digest(fixture['oracle_source'].encode()) == desc['model']['sha256'], 'selected frozen record/source/Model')''',
}
for before, after in changes.items():
    assert text.count(before) == 1, before
    text = text.replace(before, after)
ast.parse(text)
out = P / 'codex-verify-rewrite-r2-baseline-v2.py'
with out.open('x', encoding='utf-8', newline='\n') as stream:
    stream.write(text)
print(json.dumps({'path': str(out), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
                  'changes': len(changes), 'AST_valid': True, 'payload_imported': False}))
