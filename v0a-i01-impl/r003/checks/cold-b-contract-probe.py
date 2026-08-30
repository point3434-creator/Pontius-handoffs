from __future__ import annotations
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import traceback

ROOT = pathlib.Path(r'D:\pontius-snapshots\v0a-i01-r003-f7c260aed2044b2280e1cedd64516064\harness')
PACKET = pathlib.Path(r'D:\Pontius-handoffs\v0a-i01-impl\r003')
COMMIT = '47d08d8c1556d776358e15811e3e98b859fd6a8b'
MANIFEST = 'cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a'
EXPECT = {
    '311': (r'D:\Pontius-tools\py311\Scripts\python.exe', (3, 11, 15)),
    '314': (r'D:\Pontius\.venv\Scripts\python.exe', (3, 14, 6)),
}[sys.argv[1]]
identity = {'executable': sys.executable, 'implementation': sys.implementation.name,
            'full_version': sys.version, 'version': list(sys.version_info[:3]),
            'cwd': os.getcwd(), 'PYTHONPATH': os.environ.get('PYTHONPATH'),
            'environment_keys': sorted(os.environ), 'dont_write_bytecode': sys.dont_write_bytecode,
            'safe_path': sys.flags.safe_path}
assert os.path.normcase(sys.executable) == os.path.normcase(EXPECT[0]), identity
assert sys.implementation.name == 'cpython' and sys.version_info[:3] == EXPECT[1], identity
assert pathlib.Path.cwd() == ROOT and pathlib.Path(os.environ['PYTHONPATH']) == ROOT / 'src'
assert sys.dont_write_bytecode and sys.flags.safe_path
assert os.environ['PONTIUS_GIT'] == r'C:\Program Files\Git\cmd\git.exe'
assert not any(key.startswith('pontius') for key in sys.modules)
print(json.dumps({'identity_before_payload_import': identity}), flush=True)

def git(*args):
    return subprocess.run([os.environ['PONTIUS_GIT'], '-C', str(ROOT), *args],
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

assert git('rev-parse', 'HEAD').decode().strip() == COMMIT
fields = git('diff-tree', '-r', '-z', '--no-renames', '--no-commit-id', '--name-status',
             COMMIT + '^', COMMIT).split(b'\0')
rows = []
for index in range(0, len(fields) - 1, 2):
    status, name = fields[index:index + 2]
    digest = ('0' * 64).encode() if status == b'D' else hashlib.sha256(
        git('cat-file', 'blob', COMMIT + ':' + name.decode())).hexdigest().encode()
    rows.append(digest + b'  ' + name + b'\n')
manifest_bytes = b''.join(sorted(rows))
assert manifest_bytes == (PACKET / 'manifest.sha256').read_bytes()
assert hashlib.sha256(manifest_bytes).hexdigest() == MANIFEST
assert not git('status', '--porcelain')
print(json.dumps({'independent_manifest': MANIFEST, 'whole_row_byte_sort': True,
                  'blob_rows': len(rows), 'snapshot_pristine': True}), flush=True)

from pontius.immutable_blueprint import (ImmutableBlueprintActionSource,
    BlueprintDecisionKey, BlueprintActionEntry)
from pontius.holdem_cards import OneSeatCardState
from pontius.no_limit_betting import NoLimitBettingState, raise_to
from pontius.v0a.replay import ReplayHost, FIXTURE_A, ActionMailbox, PROTOCOL_ID
from pontius.v0a.runtime import HandRuntime
from pontius.v0a.model import HandStartedEvent
import pontius.v0a.runtime as runtime_module
assert pathlib.Path(runtime_module.__file__) == ROOT / 'src/pontius/v0a/runtime.py'
assert not any(name in sys.modules for name in ('cupy', 'torch'))
print(json.dumps({'runtime_import': runtime_module.__file__, 'no_cupy_or_torch': True}), flush=True)

class Clock:
    def __init__(self, failure_at=None, kind='invalid', capture=False):
        self.reads = 0
        self.failure_at = failure_at
        self.kind = kind
        self.capture = capture
        self.stacks = []
    def __call__(self):
        self.reads += 1
        if self.capture:
            self.stacks.append([f'{pathlib.Path(f.filename).name}:{f.lineno}:{f.name}'
                                for f in traceback.extract_stack()[-6:-1]])
        if self.reads == self.failure_at:
            if self.kind == 'reversed':
                return 0
            raise ValueError('deterministic cold-b clock fault')
        return self.reads * 1000000

def host_run(clock, name):
    host = ReplayHost(FIXTURE_A,
        run_id=f'{PROTOCOL_ID}-correctness-cold-b-{name}',
        blueprint=ImmutableBlueprintActionSource('cold-b-empty'), clock=clock)
    outcome = host.run()
    terminal = json.loads(outcome.trace.splitlines()[-1])
    return {
        'read_count': clock.reads, 'passed': outcome.receipt.passed,
        'reason': outcome.receipt.failure_reason,
        'secondary': list(outcome.receipt.secondary_failures),
        'accounting_complete': outcome.receipt.accounting_complete,
        'publication_seconds': outcome.receipt.terminal_publication_compute_seconds,
        'delivery_count': host.runtime.accepted_delivery_count,
        'mailbox_accepted': len(host.mailbox.accepted),
        'terminal_decision_count': terminal['decision_count'],
        'terminal_passed': terminal['passed'],
        'terminal_reason': terminal['failure_reason'],
        'failure_codes': [record.code for record in outcome.failures],
    }

baseline_clock = Clock(capture=True)
baseline = host_run(baseline_clock, 'baseline')
print(json.dumps({'baseline': baseline}), flush=True)
observations = []
for index in range(1, baseline_clock.reads + 1):
    clock = Clock(index)
    try:
        record = host_run(clock, str(index))
    except BaseException as exc:
        record = {'escaped': type(exc).__name__, 'detail': str(exc), 'read_count': clock.reads}
    record.update(failure_at=index, baseline_stack=baseline_clock.stacks[index - 1])
    observations.append(record)
print(json.dumps({'clock_fault_sweep': observations}), flush=True)
late_reverse = []
for index in range(baseline_clock.reads - 4, baseline_clock.reads + 1):
    clock = Clock(index, 'reversed')
    record = host_run(clock, f'reverse-{index}')
    record['failure_at'] = index
    late_reverse.append(record)
print(json.dumps({'late_reverse': late_reverse}), flush=True)

# A permitted subclass lies through the canonical identity method, while the
# sealed action_for still sees the nonempty entries. No introspection or patching.
fixture = FIXTURE_A
honest = ImmutableBlueprintActionSource('cold-b-empty')
state = NoLimitBettingState.new_hand(button=fixture.button,
    starting_stacks=fixture.starting_stacks, small_blind=fixture.small_blind,
    big_blind=fixture.big_blind)
cards = OneSeatCardState.preflop(controlled_seat=fixture.controlled_seat,
    private_hand=tuple(fixture.deal().hand(fixture.controlled_seat)))
key = BlueprintDecisionKey.from_state(cards=cards, betting=state, decision=state.legal_decision())
class CanonicalOverride(ImmutableBlueprintActionSource):
    def canonical_bytes(self):
        return honest.canonical_bytes()
source = CanonicalOverride(source_id=honest.source_id,
    entries=(BlueprintActionEntry(key=key, action=raise_to(6)),))
mailbox = ActionMailbox()
runtime = HandRuntime(blueprint=source, mailbox=mailbox, clock=Clock())
event = HandStartedEvent(hand_id='cold-b-policy', event_index=0, button=fixture.button,
    controlled_seat=fixture.controlled_seat, starting_stacks=fixture.starting_stacks,
    small_blind=fixture.small_blind, big_blind=fixture.big_blind, private_cards=cards.private_hand)
outcome = runtime.dispatch(event)
print(json.dumps({'canonical_subclass': {
    'reported_digest': source.digest, 'bound_empty_digest': honest.digest,
    'sealed_canonical_digest': hashlib.sha256(ImmutableBlueprintActionSource.canonical_bytes(source)).hexdigest(),
    'status': outcome.status, 'decision': {'action': outcome.decision.selected_action.kind,
        'raise_to': outcome.decision.selected_action.raise_to,
        'reason': outcome.decision.selection_reason,
        'blueprint_sha256': outcome.decision.blueprint_sha256},
    'mailbox_accepted': len(mailbox.accepted)}}), flush=True)
assert not git('status', '--porcelain')
