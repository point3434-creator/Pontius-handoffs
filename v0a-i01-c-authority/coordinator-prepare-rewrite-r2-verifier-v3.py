"""Create the baseline verifier's exact harness-v2 adapter; no payload execution."""
from pathlib import Path
import ast
import hashlib
import json

P = Path(r'D:\Pontius')
raw = (P / 'codex-verify-rewrite-r2-baseline-v2.py').read_bytes()
assert hashlib.sha256(raw).hexdigest() == '3af2e99f4e5c16ff8e5116f956f0318d065f1d5a2935c3dc606bdd71d84d6585'
text = raw.decode()
changes = {
    "PAYLOAD = '.rewrite-r2-identity'": "PAYLOAD = '.rewrite-r2-identity-v2'",
    "'rewrite-r2-identity-' + label": "'rewrite-r2-identity-v2-' + label",
    "r['schema'] == 'pontius-rewrite-r2-identity-v1'": "r['schema'] == 'pontius-rewrite-r2-identity-v2'",
    "'-311-verification-v2.json'": "'-311-verification-v3.json'",
    "check(all(key in r and r[key] == value for key, value in run_config.items()), 'run config equals verified receipt context')": '''run_keys = {
    'schema', 'slot', 'generator_sha256', 'probe_sha256', 'pack_sha256', 'plan_sha256',
    'control_sha256', 'overlay_source', 'watch_source', 'watch_sha256', 'population_sha256',
    'observer_map_sha256', 'core_watch_source', 'core_watch_sha256', 'tests_sha256',
    'depth_provenance_sha256', 'continuation_work_maximum', 'adapter', 'adapter_source_sha256',
    'extra_input_sha256', 'reserve_basis'}
check(type(run_config) is dict and set(run_config) == run_keys, 'exact required run config fields')
check(all(key in r and r[key] == value for key, value in run_config.items()), 'run config equals verified receipt context')''',
    "mechanism, verdict = case['mechanism'], case['mechanism_verdict']": '''lifecycle = case['observer_lifecycle']
    check(case['lifecycle_error'] is None and case['lifecycle_verdict'] is True
          and lifecycle['schema'] == 'pontius-r2-observer-lifecycle-v1'
          and lifecycle['acquired'] is True and lifecycle['closed'] is True
          and lifecycle['acquisition_stage'] == 'complete' and lifecycle['complete'] is True
          and lifecycle['budget_methods_restored'] is True and lifecycle['mechanism_methods_restored'] is True
          and lifecycle['errors'] == [], 'clean observer lifecycle')
    lifecycle_hooks = ('_c_state', '_c_fork', '_c_snapshot', '_c_copy_dict', '_c_cell_write',
                       '_c_eval', '_c_statement', '_c_join', '_c_invoke', '_c_call', '_c_sink', '_c_review_outcomes')
    stages = ['budget.construct', 'budget.install', 'budget.begin', 'mechanism.construct',
              'mechanism.install', 'mechanism.restore', 'mechanism.result', 'budget.end', 'budget.restore']
    stages += ['force-hook:' + name for name in lifecycle_hooks]
    stages += ['force-budget:__init__', 'force-budget:consume', 'verify-mechanism', 'verify-budget']
    check(lifecycle['events'] == [{'stage': stage, 'completed': True} for stage in stages], 'all lifecycle stages')
    mechanism, verdict = case['mechanism'], case['mechanism_verdict']''',
    "completed = returned == 10 and depth_errors == 2 and not analyzer_errors": '''check(r['lifecycle_ok'] is True and summary['lifecycle_ok'] is True
      and summary['lifecycle_failures'] == [] and summary['lifecycle_errors'] == [], 'lifecycle summary')
completed = returned == 10 and depth_errors == 2 and not analyzer_errors''',
    "'observation_complete': True, 'completed': completed, 'success': r['success'],":
    "'observation_complete': True, 'completed': completed, 'success': r['success'], 'lifecycle_ok': True,",
}
for before, after in changes.items():
    assert text.count(before) == 1, before
    text = text.replace(before, after)
ast.parse(text)
out = P / 'codex-verify-rewrite-r2-baseline-v3.py'
with out.open('x', encoding='utf-8', newline='\n') as stream:
    stream.write(text)
print(json.dumps({'path': str(out), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
                  'changes': len(changes), 'AST_valid': True, 'payload_imported': False}))
