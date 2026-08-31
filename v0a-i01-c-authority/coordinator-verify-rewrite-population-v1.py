"""Read-only population/custody checks; no source imports, Models or tests."""
from pathlib import Path
import collections
import hashlib
import json
import subprocess

T = Path(r'D:\Pontius-handoffs\v0a-i01-c-authority')
GIT = r'C:\Program Files\Git\cmd\git.exe'
h = lambda raw: hashlib.sha256(raw).hexdigest()
canonical = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
path = T / 'rewrite-early-population-v1.json'
raw = path.read_bytes()
assert h(raw) == '3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce'
manifest = json.loads(raw)
assert manifest['execution_authorized'] is False
sources = {}
for name, item in manifest['inputs'].items():
    input_path = Path(item['path'])
    assert input_path.resolve().is_relative_to(T.resolve())
    data = input_path.read_bytes()
    assert len(data) == item['bytes'] and h(data) == item['sha256']
    sources[name] = data
module = manifest['original_test_module']
assert module['commit'] == '29c02f6fbd5eb0b7ddc9e816ef28f570b9839358'
assert module['relative_path'] == 'tests/test_inventory_and_profiles.py'
def git(*args):
    return subprocess.run([GIT, '-c', 'core.fsmonitor=false', '-C', r'D:\Pontius', *args],
        check=True, capture_output=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW).stdout
assert git('rev-parse', module['commit'] + ':' + module['relative_path']).decode().strip() == module['blob_oid']
original = git('cat-file', 'blob', module['blob_oid'])
assert len(original) == module['bytes'] and h(original) == module['sha256']
sources['original_test_module'] = original

def pointer(value, pointer):
    for key in pointer.split('/')[1:]:
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value

case_count = 0
for name, item in manifest['cases'].items():
    if 'pack_ref' not in item:
        continue
    pack = json.loads(sources[item['pack_ref']])
    case = pointer(pack, item['case_json_pointer'])
    assert case['id'] == name and case['classification'] == item['classification']
    assert h(canonical(case)) == item['case_record_canonical_sha256']
    expected = {k: case[k] for k in item['expected_data_keys']}
    assert h(canonical(expected)) == item['expected_data_canonical_sha256']
    for role in ('source', 'model'):
        record = item[role]
        data = pointer(pack, record['json_pointer']).encode()
        assert h(data) == record['sha256'] and len(data) == record['bytes']
    assert item['model_projection_count'] == len(case.get('witnesses', [case.get('expected')]))
    case_count += 1

spans = 0
def walk(value):
    global spans
    if isinstance(value, dict):
        if {'source_ref', 'start_line', 'end_line', 'source_span_sha256'} <= value.keys():
            data = b''.join(sources[value['source_ref']].splitlines(keepends=True)[value['start_line']-1:value['end_line']])
            assert h(data) == value['source_span_sha256'] and len(data) == value['source_span_bytes']
            spans += 1
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)
walk(manifest)
for name in ('helper65', 'generator70'):
    item = manifest['cases'][name]
    assert item['oracle']['work_cap_error_is_substitute'] is False
    receipt = item['historical_fixture_receipt']
    assert h(Path(receipt['path']).read_bytes()) == receipt['sha256']
for gate_name, gate in manifest['gates'].items():
    ids = gate['ordered_case_ids']
    assert len(ids) == len(set(ids)) == gate['public_analysis_count']
    assert dict(collections.Counter(manifest['cases'][i]['classification'] for i in ids)) == gate['classifications']
    assert sum(manifest['cases'][i]['model_projection_count'] for i in ids) == gate['independent_model_projections']
assert len(manifest['gates']['A']['ordered_case_ids']) == 6
assert len(manifest['gates']['B']['ordered_case_ids']) == len(manifest['cases']) == 12
assert manifest['gates']['B']['engineering_continuation_work_maximum'] == 196608
assert manifest['original_caps']['MAXIMUM_ANALYSIS_WORK_UNITS'] == 262144
report = {'kind': 'static population/custody verification only', 'manifest_sha256': h(raw),
          'whole_inputs_rehashed': len(sources), 'existing_case_records_rechecked': case_count,
          'original_source_spans_rehashed': spans, 'GateA': 6, 'GateB': 12,
          'source_or_models_executed': False, 'AST_correspondence_independently_repeated': False,
          'limitations': 'No controller, operation-accounting or replacement-candidate approval; no runtime result.'}
outputs = {'coordinator-verify-rewrite-population-v1.py': Path(__file__).read_bytes(),
           'coordinator-rewrite-population-verification-v1.json': (json.dumps(report, indent=2, sort_keys=True) + '\n').encode()}
assert not any((T / n).exists() for n in outputs)
for name, data in outputs.items():
    with (T / name).open('xb') as stream:
        stream.write(data)
print(json.dumps(report))
