import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

snapshot = Path(r'D:\Pontius-review-cold-a-r002')
commit = '18c965d1f3445c253a6333c4d10899c1dcac0cc6'
expected_exe, expected_version, output_path = sys.argv[1:]
assert os.path.normcase(sys.executable) == os.path.normcase(expected_exe)
assert sys.implementation.name == 'cpython'
assert '.'.join(map(str, sys.version_info[:3])) == expected_version
assert Path.cwd() == snapshot
assert os.environ['PYTHONPATH'] == str(snapshot / 'src')
assert os.environ['PONTIUS_GIT'] == r'C:\Program Files\Git\cmd\git.exe'
assert sys.flags.safe_path and sys.dont_write_bytecode
identity = {'executable': sys.executable, 'implementation': sys.implementation.name,
            'version': sys.version, 'cwd': str(Path.cwd()),
            'PYTHONPATH': os.environ['PYTHONPATH'], 'PONTIUS_GIT': os.environ['PONTIUS_GIT'],
            'safe_path': sys.flags.safe_path, 'dont_write_bytecode': sys.dont_write_bytecode}
print(json.dumps({'before_payload_import': identity}), flush=True)
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.replay import ReplayHost, FIXTURE_A, PROTOCOL_ID
from pontius.v0a import replay, trace, runtime, model, clock
for module in (replay, trace, runtime, model, clock):
    path = Path(module.__file__)
    assert path.is_relative_to(snapshot / 'src')
    rel = path.relative_to(snapshot).as_posix()
    blob = subprocess.run([os.environ['PONTIUS_GIT'], '-C', str(snapshot), 'cat-file',
                           'blob', commit + ':' + rel], capture_output=True, check=True).stdout
    assert path.read_bytes() == blob

class Clock:
    def __init__(self, fail_at=None):
        self.ns = 1000
        self.calls = 0
        self.fail_at = fail_at
    def __call__(self):
        self.calls += 1
        if self.calls == self.fail_at:
            raise OSError('cold-a injected clock source fault')
        self.ns += 1000
        return self.ns

def host(c, suffix='baseline', **kwargs):
    return ReplayHost(FIXTURE_A, run_id=f'{PROTOCOL_ID}-correctness-cold-a-{suffix}',
                      blueprint=ImmutableBlueprintActionSource(), clock=c, **kwargs)

results = []
baseline_clock = Clock()
baseline_host = host(baseline_clock)
baseline = baseline_host.run()
assert baseline.receipt.passed
baseline_rows = [json.loads(line) for line in baseline.trace.splitlines()]
decision_index = next(i for i, row in enumerate(baseline_rows) if row['record_type']=='decision')
projection_keys = ('hand_id event_index action_index street_action_index seat street '
                   'state_before_sha256 state_after_sha256 visible_cards_sha256 '
                   'blueprint_sha256 selected_action selection_reason spine_reason '
                   'preparation_use').split()
def encode(rows, semantic=False, allow_nan=False):
    if semantic:
        projection = {
            'events': [r['event'] for r in rows if r['record_type']=='event'],
            'decisions': [{k:r[k] for k in projection_keys} for r in rows
                          if r['record_type']=='decision'],
            'settlement': rows[-1]['settlement']}
        rows[-1]['semantic_sha256'] = hashlib.sha256(
            json.dumps(projection, separators=(',', ':'), sort_keys=True).encode()).hexdigest()
    encoded = [json.dumps(row, separators=(',', ':'), sort_keys=True,
                          allow_nan=allow_nan).encode()+b'\n' for row in rows]
    rows[-1]['trace_prefix_sha256'] = hashlib.sha256(b''.join(encoded[:-1])).hexdigest()
    encoded[-1] = json.dumps(rows[-1], separators=(',', ':'), sort_keys=True,
                            allow_nan=allow_nan).encode()+b'\n'
    return b''.join(encoded)

def parser_probe(name, mutate, semantic=False, allow_nan=False):
    rows = copy.deepcopy(baseline_rows)
    mutate(rows)
    data = encode(rows, semantic, allow_nan)
    try:
        parsed = trace.parse_trace(data)
        equal = parsed.terminal['semantic_sha256'] == trace.parsed_semantic_sha256(parsed)
        results.append({'probe':name, 'parser':'accepted', 'passed':parsed.terminal['passed'],
                        'semantic_digest_matches':equal})
    except Exception as error:
        results.append({'probe':name, 'parser':'rejected', 'exception':type(error).__name__,
                        'message':str(error)})
parser_probe('foreign_semantic_digest', lambda r:r[-1].update(semantic_sha256='f'*64))
parser_probe('illegal_first_check_rebound',
             lambda r:r[decision_index]['selected_action'].update(kind='check'), True)
parser_probe('foreign_header_policy', lambda r:r[0].update(blueprint_sha256='f'*64))
parser_probe('zero_delivered_count', lambda r:r[-1].update(decision_count=0))
def late_false(rows):
    t=rows[decision_index]['timing']; start=t['wall_start_ns']
    t.update(emission_observed_ns=start+16000000000,last_valid_observation_ns=start+16000000000,
             elapsed_ns=16000000000,response_compute_seconds=0.0,
             response_uninstrumented_seconds=16.0,work_cutoff_crossed=False,deadline_crossed=False)
parser_probe('late_action_with_false_deadline',late_false)
parser_probe('null_decision_timing', lambda r:r[decision_index].update(timing=None))
parser_probe('bool_record_index', lambda r:r[0].update(record_index=False))
parser_probe('unknown_event_timestamp',lambda r:r[1]['event'].update(timestamp_ns=123),True)
parser_probe('missing_hand_start_button',lambda r:r[1]['event'].pop('button'),True)
parser_probe('invalid_spine_enum',lambda r:r[decision_index].update(spine_reason='not-a-v2-reason'),True)
parser_probe('invalid_source_commit',lambda r:r[0].update(source_commit=[]))
parser_probe('out_of_range_seat',lambda r:r[decision_index].update(seat=6),True)
parser_probe('nan_response_seconds',lambda r:r[decision_index]['timing'].update(
             response_compute_seconds=float('nan')),allow_nan=True)
parser_probe('infinite_terminal_total',lambda r:r[-1].update(
             preparation_compute_seconds=float('inf')),allow_nan=True)

for name, fail_at in [('first_clock',1),('publication_close_clock',baseline_clock.calls-1),
                       ('finalization_clock',baseline_clock.calls)]:
    c=Clock(fail_at)
    h=host(c,name)
    try:
        outcome=h.run()
        results.append({'probe':name,'returned_receipt':True,'fail_at':fail_at,
                        'source_calls':c.calls,'receipt_passed':outcome.receipt.passed,
                        'receipt_accounting_complete':outcome.receipt.accounting_complete,
                        'runtime_accounting_complete':h.runtime.accounting().complete,
                        'failure_reason':outcome.receipt.failure_reason,
                        'secondary_failures':outcome.receipt.secondary_failures,
                        'accepted_actions':len(h.mailbox.accepted)})
    except Exception as error:
        results.append({'probe':name,'returned_receipt':False,'fail_at':fail_at,
                        'source_calls':c.calls,'exception':type(error).__name__,'message':str(error),
                        'accepted_actions':len(h.mailbox.accepted)})

slow_clock=Clock()
slow_host=host(slow_clock,'slow-trace')
original_json=trace.canonical_json
serialization_calls=[]
def delayed_json(payload):
    serialization_calls.append(payload.get('record_type','semantic') if isinstance(payload,dict)
                               else type(payload).__name__)
    slow_clock.ns += 1000000000
    return original_json(payload)
trace.canonical_json=delayed_json
try:
    slow=slow_host.run()
finally:
    trace.canonical_json=original_json
slow_parsed=trace.parse_trace(slow.trace)
base_parsed=trace.parse_trace(baseline.trace)
results.append({'probe':'real_serialization_one_second_each','passed':slow.receipt.passed,
                'serialization_calls':serialization_calls,
                'delay_seconds':len(serialization_calls),
                'base_preparation':base_parsed.terminal['preparation_compute_seconds'],
                'slow_preparation':slow_parsed.terminal['preparation_compute_seconds'],
                'base_post_terminal':base_parsed.terminal['post_terminal_compute_seconds'],
                'slow_post_terminal':slow_parsed.terminal['post_terminal_compute_seconds'],
                'publication_seconds':slow.receipt.terminal_publication_compute_seconds,
                'base_response_ns':[d.timing.elapsed_ns for d in baseline.decisions],
                'slow_response_ns':[d.timing.elapsed_ns for d in slow.decisions]})

mismatch=host(Clock(),'mode',mode='rehearsal').run()
results.append({'probe':'correctness_run_id_rehearsal_mode','passed':mismatch.receipt.passed,
                'mode':trace.parse_trace(mismatch.trace).header['mode'],
                'run_id':mismatch.receipt.run_id})
report={'identity':identity,'candidate':commit,'modules':{m.__name__:m.__file__ for m in
        (replay,trace,runtime,model,clock)}, 'baseline_source_clock_calls':baseline_clock.calls,
        'results':results,'optional_imports':[n for n in sys.modules if n.split('.')[0] in
        ('cupy','torch')]}
with open(output_path,'x',encoding='utf-8',newline='\n') as handle:
    json.dump(report,handle,indent=2,allow_nan=False)
    handle.write('\n')
print(json.dumps(report,indent=2,allow_nan=False))