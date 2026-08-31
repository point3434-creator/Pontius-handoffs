"""Independently rehash a completed Gate A receipt; no candidate/Model import."""
from pathlib import Path
import hashlib
import json
import sys
import subprocess

T = Path(r'D:\Pontius-handoffs\v0a-i01-c-authority')
C = T / 'tests-checks'
GIT = r'C:\Program Files\Git\cmd\git.exe'
h = lambda raw: hashlib.sha256(raw).hexdigest()
assert len(sys.argv) == 4
label, slot, receipt_sha = sys.argv[1:]
assert slot in ('311', '314') and label.replace('-', '').isalnum()
receipt_path = C / ('rewrite-r1-gate-a-' + label + '-' + slot + '-receipt.json')
raw = receipt_path.read_bytes()
assert h(raw) == receipt_sha
r = json.loads(raw)
assert r['label'] == label and r['slot'] == slot
assert r['completed'] is True and r['integrity_ok'] is True and r['payload_started'] is True
assert 'error' not in r and 'cleanup_error' not in r
assert r['before'] == r['after'] and r['input_hashes_before'] == r['input_hashes_after']
assert r['control_sha256'] == '9310da3cecabaae0127fb6562a15b388355f722c35dcd5abbd2b039fd0f4d48c'
assert r['probe_sha256'] == 'c0672ac61fa19b5dd3d46fc6c0dbbdaae4565c610e7e658619c738559fb27395'
assert r['population_sha256'] == '3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce'
snapshot = Path(r['snapshot'])
assert snapshot.parent.parent == Path(r'D:\pontius-snapshots') and snapshot.name == 'snapshot'
for name, pin in r['before'].items():
    rel = Path(name)
    assert not rel.is_absolute() and '..' not in rel.parts
    assert h((snapshot / rel).read_bytes()) == pin, name
manifest = (snapshot / '.rewrite-r1-gate-a/manifest.json').read_bytes()
assert h(manifest) == r['manifest_sha256'] == r['manifest_after_sha256']
assert json.loads(manifest) == r['before']
for name, pin in r['input_hashes_before'].items():
    assert h(Path(r['input_paths'][name]).read_bytes()) == pin, name
outputs = {key: Path(value['path']).read_bytes() for key, value in r['outputs'].items()}
assert all(h(outputs[key]) == value['sha256'] for key, value in r['outputs'].items())
assert outputs['log'] == outputs['stdout'] + b'\nCONTROL STDERR\n' + outputs['stderr']
setup = json.loads(outputs['setup'])
assert all(r[k] == v for k, v in setup.items())
assert outputs['stdout'].endswith(b'\n') and b'\r' not in outputs['stdout']
records = [json.loads(line) for line in outputs['stdout'].splitlines()]
assert len(records) == 8
identity = records[0]['identity_before_imports']
assert identity == r['identity'] and identity['version_info'] == ([3, 11, 15] if slot == '311' else [3, 14, 6])
assert identity['generator_sha256'] == r['generator_sha256'] and identity['environment'] == setup['environment']
summary = records[-1]
assert summary == r['summary'] and summary['completed'] is True
assert summary['case_count'] == summary['analyzed_cases'] == 6 and summary['projections'] == 8
assert summary['oracle_errors'] == summary['analyzer_errors'] == summary['accounting_errors'] == []
assert summary['original_methods_restored'] is True
pop = json.loads((T / 'rewrite-early-population-v1.json').read_bytes())
assert [x['rewrite_gate_a_case'] for x in records[1:-1]] == pop['gates']['A']['ordered_case_ids']
case_rows = []
failures = []
for case in records[1:-1]:
    name = case['rewrite_gate_a_case']
    assert case['source_sha256'] == pop['cases'][name]['source']['sha256']
    assert case['oracle_sha256'] == pop['cases'][name]['model']['sha256']
    assert case['oracle_actuals'] == case['expected_projections'] and case['oracle_passed'] is True
    assert case['analyzer_error'] is None and case['accounting_error'] is None
    blockers, argv = case['blockers'], case['argv']
    category = case['classification']
    passed = bool(blockers) if category == 'refuse' else (
        bool(blockers) or argv == case['required_argv'] if category == 'permitted-refusal'
        else not blockers and argv == case['required_argv'])
    assert case['semantic_passed'] is passed
    if not passed:
        failures.append(name)
    m = case['budget_metrics']
    assert len(m['epochs']) == m['epoch_count'] == m['initialization_attempts']
    assert not m['initialization_errors'] and m['unscoped_events'] == 0
    for e in m['epochs']:
        assert e['initial_work'] + e['requested_units'] == e['last_observed_work']
        assert e['consume_calls'] == e['completed_consume_calls'] + e['exceptional_consume_calls']
        assert sum(v['units'] for v in e['origins'].values()) == e['requested_units']
        assert sum(e['phase_units'].values()) == e['requested_units']
    case_rows.append({'id': name, 'classification': category, 'passed': passed, 'argv': argv,
        'blockers': blockers, 'budget_epochs': m['epoch_count'],
        'maximum_epoch_work': m['maximum_epoch_observed_work'],
        'total_requested_units': m['requested_units_across_epochs']})
assert failures == summary['semantic_failures']
assert r['exit'] == int(bool(failures)) and r['process_returncode'] == r['exit']
assert r['success'] is (not failures) and r['semantic_ok'] is (not failures) and r['accounting_ok'] is True
command = [GIT, '-c', 'core.fsmonitor=false', '-c', 'core.autocrlf=false', '-C', str(snapshot)]
head = subprocess.run(command + ['rev-parse', 'HEAD'], capture_output=True, check=True, timeout=60).stdout.decode().strip()
assert head == r['base'] == '29c02f6fbd5eb0b7ddc9e816ef28f570b9839358'
report = {'kind': 'coordinator fresh receipt/custody verification; no analyzer execution',
    'receipt': str(receipt_path), 'receipt_sha256': receipt_sha, 'slot': slot,
    'source_sha256': r['generator_sha256'], 'snapshot_manifest_sha256': r['manifest_sha256'],
    'snapshot_files_rehashed': len(r['before']), 'original_inputs_rehashed': len(r['input_paths']),
    'outputs_rehashed': len(outputs), 'actual_version': identity['version_info'],
    'completed': True, 'integrity_ok': True, 'accounting_ok': True, 'semantic_failures': failures,
    'cases': case_rows, 'script_sha256': h(Path(__file__).read_bytes())}
out = T / ('coordinator-rewrite-r1-' + label + '-' + slot + '-verification-v1.json')
with out.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'verification': str(out), 'sha256': h(out.read_bytes()), 'cases': case_rows}))
