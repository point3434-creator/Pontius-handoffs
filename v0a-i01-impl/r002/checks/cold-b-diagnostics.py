import sys
import platform
import os
import json
import hashlib
import subprocess
from pathlib import Path

expected_executable, expected_version, snapshot = sys.argv[1:4]
assert Path(sys.executable).resolve() == Path(expected_executable).resolve()
assert platform.python_implementation() == 'CPython'
assert platform.python_version() == expected_version
assert Path.cwd().resolve() == Path(snapshot).resolve()
assert Path(os.environ['PYTHONPATH']).resolve() == Path(snapshot, 'src').resolve()
git = Path(os.environ['PONTIUS_GIT'])
assert git.is_absolute() and git.is_file() and not git.is_symlink()
identity = {'executable': sys.executable, 'implementation': platform.python_implementation(),
            'full_version': sys.version, 'cwd': str(Path.cwd()),
            'PYTHONPATH': os.environ['PYTHONPATH'], 'PONTIUS_GIT': str(git),
            'argv': sys.argv, 'env_keys': sorted(os.environ)}
print(json.dumps({'identity_before_payload_import': identity}), flush=True)
commit = '18c965d1f3445c253a6333c4d10899c1dcac0cc6'
base = 'b357d333fc2393b7fc7dcf31f30c86616208c817'
packet = Path('D:/Pontius-handoffs/v0a-i01-impl/r002')
def gitrun(*args):
    return subprocess.check_output([str(git), '-C', snapshot, *args])
assert gitrun('rev-parse', 'HEAD').decode().strip() == commit
raw = gitrun('diff-tree', '-r', '-z', '--no-commit-id', '--name-status', base, commit)
fields = raw.decode('utf-8').split('\0')
rows = []
for index in range(0, len(fields)-1, 2):
    status, path = fields[index:index+2]
    blob = gitrun('cat-file', 'blob', commit + ':' + path)
    digest = hashlib.sha256(blob).hexdigest()
    assert Path(snapshot, path).read_bytes() == blob
    rows.append((digest + '  ' + path + '\n').encode())
manifest = b''.join(sorted(rows))
assert manifest == (packet / 'manifest.sha256').read_bytes()
manifest_digest = hashlib.sha256(manifest).hexdigest()
assert manifest_digest == '4cfd14ac7bfdb22e052bb9f625610657c01aafa07182acf58d19367a8816cb18'
print(json.dumps({'independent_blob_manifest': manifest_digest, 'rows': len(rows)}), flush=True)

from dataclasses import asdict, replace
from unittest.mock import patch
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.action_clock import ActionClockLedger
from pontius.v0a.clock import MonotonicWitness
from pontius.v0a.model import ActionMailbox, HandStartedEvent, PotRecord
from pontius.v0a.runtime import HandRuntime
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost
from pontius.v0a.trace import parse_trace, parsed_semantic_sha256, canonical_json
import pontius.v0a.runtime as runtime_module
assert Path(runtime_module.__file__).resolve() == Path(snapshot, 'src/pontius/v0a/runtime.py').resolve()

class Clock:
    def __init__(self, fail_at=None):
        self.calls = 0
        self.now = 0
        self.fail_at = fail_at
        self.fail_next = False
    def __call__(self):
        self.calls += 1
        if self.calls == self.fail_at or self.fail_next:
            self.fail_next = False
            raise OSError('injected source failure')
        self.now += 1000
        return self.now

def host_for(name, clock, fixture=FIXTURE_A):
    return ReplayHost(fixture, run_id=f'{PROTOCOL_ID}-correctness-cold-b-{name}',
                      blueprint=ImmutableBlueprintActionSource(source_id='cold-b'), clock=clock,
                      source_commit=commit, source_manifest_sha256=manifest_digest)

def run_observed(name, host):
    try:
        result = host.run()
        receipt = asdict(result.receipt)
        receipt['runtime_accounting_after'] = asdict(host.runtime.accounting())
        receipt['mailbox_accepted_count'] = len(host.mailbox.accepted)
        receipt['trace_terminal'] = parse_trace(result.trace).terminal
        print(json.dumps({'probe': name, 'returned': receipt}), flush=True)
        return result
    except BaseException as error:
        print(json.dumps({'probe': name, 'escaped': type(error).__name__, 'message': str(error),
                          'mailbox_accepted_count': len(host.mailbox.accepted),
                          'runtime_accounting_after': asdict(host.runtime.accounting())}), flush=True)
        return None

baseline_clock = Clock()
baseline_host = host_for('baseline', baseline_clock)
baseline = run_observed('baseline', baseline_host)
assert baseline is not None and baseline.receipt.passed
print(json.dumps({'baseline_clock_calls': baseline_clock.calls}), flush=True)
finalize_failure = run_observed('finalize_clock_failure', host_for('finalize', Clock(baseline_clock.calls)))
assert finalize_failure is not None and finalize_failure.receipt.passed
publication_failure = run_observed('publication_close_clock_failure',
                                  host_for('publication', Clock(baseline_clock.calls-1)))
assert publication_failure is None
first_failure = run_observed('initial_clock_failure', host_for('initial', Clock(1)))
assert first_failure is None

clock = Clock()
post_delivery_host = host_for('post-delivery', clock)
real_deliver = ActionMailbox.deliver
def accept_then_arm(self, envelope):
    receipt = real_deliver(self, envelope)
    clock.fail_next = True
    return receipt
with patch.object(ActionMailbox, 'deliver', accept_then_arm):
    post_delivery = run_observed('clock_failure_after_real_acceptance', post_delivery_host)
assert post_delivery is None and len(post_delivery_host.mailbox.accepted) == 1

real_settle = HandRuntime.settle
for kind in ('final_stacks', 'pot_seats'):
    def corrupt_settlement(self, kind=kind):
        settled = real_settle(self)
        if kind == 'final_stacks':
            return replace(settled, final_stacks=(0,)*6)
        return replace(settled, pots=tuple(PotRecord(amount=p.amount, seats=(0,)) for p in settled.pots))
    with patch.object(HandRuntime, 'settle', corrupt_settlement):
        corrupted = run_observed('oracle_omits_' + kind, host_for('oracle-' + kind, Clock()))
    assert corrupted is not None and corrupted.receipt.passed

# Real transition snapshot establishes flags; fault the next witness source call.
clock = Clock()
mailbox = ActionMailbox()
runtime = HandRuntime(blueprint=ImmutableBlueprintActionSource(source_id='cold-b'),
                      mailbox=mailbox, clock=clock)
real_finish = ActionClockLedger.finish_transition_boundary
observed = []
def finish_and_arm(self, boundary, **kwargs):
    if kwargs.get('starts_controlled_action'):
        clock.now += 15_000_000_001
    result = real_finish(self, boundary, **kwargs)
    if kwargs.get('starts_controlled_action'):
        observed.append({'deadline_crossed': result.deadline_crossed,
                         'work_remaining_seconds': result.work_remaining_seconds})
        clock.fail_next = True
    return result
fixture = FIXTURE_A
start = HandStartedEvent(hand_id='flags', event_index=0, button=fixture.button,
                        controlled_seat=fixture.controlled_seat,
                        starting_stacks=fixture.starting_stacks,
                        small_blind=fixture.small_blind, big_blind=fixture.big_blind,
                        private_cards=tuple(fixture.deal().hand(fixture.controlled_seat)))
with patch.object(ActionClockLedger, 'finish_transition_boundary', finish_and_arm):
    flagged = runtime.dispatch(start)
print(json.dumps({'probe': 'established_transition_flags', 'snapshots': observed,
                  'outcome': asdict(flagged)}), flush=True)
assert observed[0]['deadline_crossed'] is True
assert flagged.failure.timing.deadline_crossed is None

# Rehashing edited bytes does not repair illegal semantics or schema.
base_rows = [json.loads(row) for row in baseline.trace.splitlines()]
def edited_probe(name, mutate):
    rows = json.loads(json.dumps(base_rows))
    mutate(rows)
    prefix = b''.join((canonical_json(row)+'\n').encode() for row in rows[:-1])
    rows[-1]['trace_prefix_sha256'] = hashlib.sha256(prefix).hexdigest()
    content = prefix + (canonical_json(rows[-1])+'\n').encode()
    try:
        parsed = parse_trace(content)
        print(json.dumps({'probe': name, 'parser_accepted': True,
                          'terminal_passed': parsed.terminal['passed'],
                          'semantic_digest_matches': parsed_semantic_sha256(parsed) == parsed.terminal['semantic_sha256']}), flush=True)
    except BaseException as error:
        print(json.dumps({'probe': name, 'parser_accepted': False,
                          'error': type(error).__name__, 'message': str(error)}), flush=True)

edited_probe('semantic_digest_not_checked', lambda r: r[-1].update(semantic_sha256='0'*64))
edited_probe('illegal_decision_accepted', lambda r: next(x for x in r if x['record_type']=='decision').update(selected_action={'kind':'raise','raise_to':1}))
edited_probe('invalid_event_schema_accepted', lambda r: next(x for x in r if x['record_type']=='event')['event'].update(extra=True, event_index=True))
edited_probe('nan_timing_accepted', lambda r: next(x for x in r if x['record_type']=='decision')['timing'].update(response_compute_seconds=float('nan')))
