"""Coordinator static review and plan disposition; does not import or execute payloads."""
from pathlib import Path
import ast
import hashlib
import json

T = Path(r'D:\Pontius-handoffs\v0a-i01-c-authority')
C = T / 'tests-checks'
PINS = {
    'rewrite-r1-implementation-plan-v1.md': '18f8124432880016d6dd0690ed4d3b582b8e202c5bdda21ae48a65efa0ae521d',
    'rewrite-r1-category-review-v1.md': 'f04eedf4de32550cb3d4e02e310eeed85f5963ba4621ea7de430b8cae125522a',
    'rewrite-r1-base-generator.py': '29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692',
    'rewrite-early-population-v1.json': '3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce',
    'tests-checks/rewrite-r1-probe-v1.py': 'c0672ac61fa19b5dd3d46fc6c0dbbdaae4565c610e7e658619c738559fb27395',
    'tests-checks/rewrite-r1-control-v1.py': '9310da3cecabaae0127fb6562a15b388355f722c35dcd5abbd2b039fd0f4d48c',
    'tests-checks/rewrite-r1-plan-v1.md': '8cec0f3af002f04b20c82dee62d29f0601a87047249ab2dfcde5a164ca73826d',
    'tests-checks/rewrite-r1-observer-map-v1.json': 'af8df00ceb6b02bb5730eee56754ce78badcab6102ce861d726eed704522bfbd',
    'tests-checks/rewrite-r1-static-v1.json': '49414e161aca661bc6c3c302564b5982759ca5ec23618b71dd0cba19568ada97',
    'tests-checks/rewrite-r1-handoff-v1.md': 'cdea6c9dcd3cb91755223178e9114b026edc5625849d641a2d58dbcedd5756d6',
    'tests-checks/original-composition-ten-probe-v1.py': 'e2564b1d1d61c0a92e449f80eb5118eb72141b3fabd9022cf2b2881d1c56927e',
    'tests-checks/original-composition-ten-control-v1.py': '20f196243e078ef542628b6a400ab2266443c1b1d918327ee14004f98e564bb4',
    'tests-checks/name-environment-probe-v1.py': '94a91ff970aa0df12c4334d72a2476ca5d58a4b76aa3a412c5440e93411806b4',
    'tests-checks/storage-composition-cases-v1.json': 'faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709',
    'tests-checks/name-environment-cases-v1.json': 'd07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c',
}
h = lambda raw: hashlib.sha256(raw).hexdigest()
inputs = {name: (T / name).read_bytes() for name in PINS}
assert all(h(raw) == PINS[name] for name, raw in inputs.items())
trees = {name: ast.parse(raw.decode('utf-8')) for name, raw in inputs.items() if name.endswith('.py')}
def function(file, name):
    found = [n for n in trees['tests-checks/' + file].body if type(n) is ast.FunctionDef and n.name == name]
    assert len(found) == 1
    return found[0]
def same(left_file, left, right_file, right, rename=False):
    a, b = function(left_file, left), function(right_file, right)
    if rename:
        a.name = b.name
    assert ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False), (left, right)
    return True
preserved = {}
preserved['storage_public'] = same('rewrite-r1-probe-v1.py', 'storage_public_review',
    'original-composition-ten-probe-v1.py', 'public_review', True)
preserved['storage_Model'] = same('rewrite-r1-probe-v1.py', 'storage_oracle',
    'original-composition-ten-probe-v1.py', 'storage_oracle')
for name in ('public_review', 'project_oracles'):
    preserved['name_' + name] = same('rewrite-r1-probe-v1.py', name, 'name-environment-probe-v1.py', name)
for name in ('checked', 'create', 'write_json', 'environment', 'git', 'file_hashes'):
    preserved['controller_' + name] = same('rewrite-r1-control-v1.py', name,
        'original-composition-ten-control-v1.py', name)
for name in ('load_cases', 'public_verdict', 'validate_budget_metrics'):
    preserved['probe_control_' + name] = same('rewrite-r1-control-v1.py', name, 'rewrite-r1-probe-v1.py', name)
pop = json.loads(inputs['rewrite-early-population-v1.json'])
ids = pop['gates']['A']['ordered_case_ids']
assert ids == ['shared-list-consumed', 'shared-list-dormant', 'class-adoption-unsafe',
               'class-adoption-safe', 'hidden-cell-joined-reached', 'hidden-cell-joined-dormant']
records = []
for pack_name in ('storage-composition-cases-v1.json', 'name-environment-cases-v1.json'):
    pack = json.loads(inputs['tests-checks/' + pack_name])
    for case in pack['cases']:
        if case['id'] not in ids:
            continue
        bound = pop['cases'][case['id']]
        canonical = json.dumps(case, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
        assert h(canonical) == bound['case_record_canonical_sha256']
        assert h(case['source'].encode()) == bound['source']['sha256']
        assert h(case['oracle_source'].encode()) == bound['model']['sha256']
        assert case['classification'] == bound['classification']
        records.append(case['id'])
assert set(records) == set(ids) and len(records) == 6
report = {'kind': 'coordinator static review; no candidate or Model imported', 'inputs': PINS,
          'preserved_AST': preserved, 'fixed_case_ids': ids, 'public_count': 6, 'Model_count': 8,
          'runtime_executed': False, 'source_edits_authorized_now': False,
          'independent_harness_disposition_still_required_before_dispatch': True}
note = '''# Coordinator R1 plan disposition v1

Plan 18f8124432880016d6dd0690ed4d3b582b8e202c5bdda21ae48a65efa0ae521d
is accepted for the bounded first implementation, subject to the baseline and
source checkpoints below. The frozen design remains the controlling contract.

The coordinator read the full plan, full Gate A probe/controller and category
review. The accompanying static record independently rehashes original inputs,
compares the original public envelopes/Models and unchanged controller custody
helpers by AST, and verifies the six population bindings. No payload ran.
The independent harness engineering disposition must also be accepted before
root dispatch. This is not a cold implementation review or acceptance result.

## Clarifications

1. The plan's baseline sentence mentioning both interpreters is conditional:
   actual3.11.15 runs first. A semantic RED on3.11 is retained and suffices to
   start the fix; it does not unlock3.14. The controller's existing successful
   matching floor requirement stays intact. If all six baseline cases pass,
   record passing characterization honestly and use the already retained wider
   r010 defects as the replacement rationale. Do not alter this population.
2. Binder metering-only plumbing is approved. Add only the optional keyword
   analysis_budget=None and guarded calls to that budget's consume method.
   Removing those validated additions must reproduce the entire r010 binder
   AST. Charge expressions may use only existing values, literals, arithmetic
   and len, with no new semantic helper. The canonical caller must pass its
   existing budget. Signature matching branches/results remain unchanged.
3. One canonical public execution path is required. Terminal non-child
   _process_definition reuse is allowed only after exact canonical evidence
   extraction and explicit -c refusal; no legacy helper-return or resolver
   state can enter the new path. Static facts may be shared, live state may not.
4. Ordered outcome states are acceptable for R1. COW copying and path expansion
   remain charged and unproved for cost. Gate B's fixed depth/scaling population
   and196608 continuation ceiling remain the next engineering checkpoint.
5. The original per-source facts/module, entry preflight and body budget owners
   are retained semantically; redundant legacy passes need not run to fabricate
   charge parity. Recursive calls share the current body budget. Any extra
   owner/split requires an explicit disposition before execution.
6. Source GO follows verified baseline evidence. The sole source writer first
   issues state primitives for root inspection, then proceeds through the plan.
   The first candidate stops before2500 added-plus-deleted implementation lines;
   no scope expansion or size hiding. Tests and other16 r010 paths stay exact.

Only root dispatches reviewed finite controls from fresh D-local snapshots.
Main integration, broad acceptance and the named finalizer remain later gates.
'''
outputs = {'coordinator-rewrite-r1-static-v1.json': (json.dumps(report, indent=2, sort_keys=True) + '\n').encode(),
           'rewrite-r1-plan-disposition-v1.md': note.encode(),
           'coordinator-review-rewrite-r1-v1.py': Path(__file__).read_bytes()}
assert not any((T / name).exists() for name in outputs)
for name, raw in outputs.items():
    with (T / name).open('xb') as stream:
        stream.write(raw)
print(json.dumps({name: h(raw) for name, raw in outputs.items()}))
