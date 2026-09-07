"""Review B finite real-consumer controls; reads only the exact snapshot cwd."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import sys

repo = Path.cwd()
assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.safe_path and sys.dont_write_bytecode
assert Path(os.environ['PYTHONPATH']).resolve() == repo / 'src'
assert Path(os.environ['PONTIUS_GIT']).is_absolute()
spec = importlib.util.spec_from_file_location(
    'review_b_frozen_transport_tests', repo / 'tests/test_decision_provider_transport.py')
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
control = module.ProviderTransportTests()
process = control.invoke(repo)
rows = [json.loads(row) for row in process.stdout.splitlines()][:3]
assert len(rows) == 3 and rows[2]['status'] == 'decided', (process.stdout, process.stderr)
print('snapshot', str(repo))
print('source_commit', rows[0]['source_commit'])
print('real_child_prefix', json.dumps(rows, sort_keys=True, separators=(',', ':')))

def exchange(label, frames):
    host, table, consumer = control.consumer(frames, rows[0])
    try:
        consumer.ready()
        consumer.exchange(table.start_event())
    except host.HostRefusal as error:
        result = dict(case=label, accepted=False, refusal=error.code,
                      applied_actions=table.applied_actions)
    else:
        result = dict(case=label, accepted=True, applied_actions=table.applied_actions)
    print(json.dumps(result, sort_keys=True))
    return result['accepted']

assert exchange('positive_exact_child_record', rows)
broken = copy.deepcopy(rows)
broken[2]['decision']['fallback_action'] = dict(kind='fold', raise_to=None)
broken[2]['decision']['fallback_reason'] = 'table_hit'
wrong_fallback = exchange('empty_blueprint_claims_fold_table_hit', broken)

from pontius.decision_provider.codec import validate_decision
assert Path(sys.modules['pontius.decision_provider.codec'].__file__).resolve() == (
    repo / 'src/pontius/decision_provider/codec.py')
record = copy.deepcopy(rows[2]['decision'])
start = record['timing']['wall_start_ns']
record['timing'].update(last_valid_observation_ns=start+14_000_000_000,
    emission_observed_ns=start+14_000_000_000, elapsed_ns=14_000_000_000,
    response_compute_seconds=0.0, response_uninstrumented_seconds=14.0,
    work_cutoff_crossed=True, deadline_crossed=False)
record['failure_reason'] = 'work_cutoff_exceeded'
try:
    validate_decision(record)
except (ValueError, TypeError):
    wrong_cutoff = False
else:
    wrong_cutoff = True
print(json.dumps(dict(case='provider_selected_despite_pre_emission_cutoff',
    accepted=wrong_cutoff, record=record), sort_keys=True))
assert not wrong_fallback and not wrong_cutoff, 'Required negative controls were accepted'
