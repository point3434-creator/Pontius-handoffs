"""Independent public-parser checks; no candidate test helper supplies an oracle."""
import copy
import itertools
import json
from hashlib import sha256
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name('codex-b-identity.py')))
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.model import ActionMailbox
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost
from pontius.v0a.replay import verify_successful_trace
from pontius.v0a.trace import TraceInvalidError, parse_trace

COMMIT = '52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8'
MANIFEST = '7e1575b18c7a9cf0c74bd956a54e899aad670349d198d7863ae1f67463583d7a'
COUNTS = {}
POLICY = ImmutableBlueprintActionSource('codex-b-independent-policy')

class Source:
    def __init__(self, failure_at=None, fault='invalid'):
        self.now = 100_000
        self.calls = 0
        self.failure_at = failure_at
        self.fault = fault
        self.dead = False
    def __call__(self):
        self.calls += 1
        if self.dead or self.calls == self.failure_at:
            if self.fault == 'exception':
                raise RuntimeError('independent source failure')
            if self.fault == 'reversed':
                return self.now - 1 if self.calls > 1 else -1
            return False
        self.now += 10_000
        return self.now

def host(fixture=FIXTURE_A, kind='success', source=None):
    source = source or Source()
    real = ActionMailbox()
    class Adapter:
        def deliver(self, value):
            if kind == 'rejected':
                return real.deliver(None)
            receipt = real.deliver(value)
            if kind == 'interrupted':
                source.dead = True
            if kind == 'unknown':
                raise RuntimeError('independent lost acknowledgement')
            if kind == 'late':
                source.now += 16_000_000_000
            return receipt
    outcome = ReplayHost(fixture, run_id=PROTOCOL_ID + '-correctness-codex-b-' + kind,
                         blueprint=POLICY, clock=source, mailbox=Adapter(),
                         source_commit=COMMIT, source_manifest_sha256=MANIFEST).run()
    return outcome, real, source

def dump(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

# Literal ADR0485 projection fields. No production digest/projection function used.
PROJECTION = ('hand_id', 'event_index', 'action_index', 'street_action_index', 'seat',
              'street', 'state_before_sha256', 'state_after_sha256', 'visible_cards_sha256',
              'blueprint_sha256', 'selected_action', 'selection_reason', 'spine_reason',
              'preparation_use')
def bind(rows):
    semantic = {'events':[row['event'] for row in rows if row['record_type']=='event'],
                'decisions':[{key:row[key] for key in PROJECTION}
                             for row in rows if row['record_type']=='decision'],
                'settlement':rows[-1]['settlement']}
    rows[-1]['semantic_sha256'] = sha256(dump(semantic)).hexdigest()
    prefix = b''.join(dump(row) + b'\n' for row in rows[:-1])
    rows[-1]['trace_prefix_sha256'] = sha256(prefix).hexdigest()
    return prefix + dump(rows[-1]) + b'\n'

def rows_for(content):
    return [json.loads(row) for row in content.splitlines()]

def expect(rows, accepted, category):
    content = bind(rows)
    try:
        parsed = parse_trace(content)
    except TraceInvalidError:
        assert not accepted, (category, 'honest expected prefix refused')
    else:
        assert accepted, (category, 'invalid mutation accepted')
        assert parsed.terminal['trace_prefix_sha256'] == sha256(
            b''.join(content.splitlines(keepends=True)[:-1])).hexdigest()
    COUNTS[category] = COUNTS.get(category, 0) + 1

outcomes = {}
for kind in ('success', 'interrupted', 'unknown', 'rejected', 'late', 'no_start'):
    outcome, mailbox, source = host(kind=kind, source=Source(1) if kind=='no_start' else None)
    outcomes[kind] = rows_for(outcome.trace)
    parsed = parse_trace(outcome.trace)
    assert parsed.terminal['passed'] == (kind=='success')
    assert len(mailbox.accepted) == {'success':4, 'interrupted':1, 'unknown':1,
                                    'rejected':0, 'late':1, 'no_start':0}[kind]
    expect(copy.deepcopy(outcomes[kind]), True, 'honest_outcomes')

for fixture in (FIXTURE_A, FIXTURE_B):
    outcome, _, _ = host(fixture)
    assert outcome.receipt.passed
    verified = verify_successful_trace(outcome.trace, fixture=fixture, blueprint=POLICY,
                source_commit=COMMIT, source_manifest_sha256=MANIFEST,
                expected_mode='correctness', expected_clock_kind='deterministic_test')
    assert verified is not None
    COUNTS['real_successful_legal_controls'] = COUNTS.get('real_successful_legal_controls',0)+1

for kind, original in outcomes.items():
    for complete, passed, accounting in itertools.product((False, True), repeat=3):
        rows = copy.deepcopy(original)
        rows[-1].update(complete=complete, passed=passed, accounting_complete=accounting,
                        preparation_compute_seconds=0.0, post_terminal_compute_seconds=0.0)
        if kind == 'success':
            accepted = complete and passed and accounting
        elif kind in ('interrupted', 'unknown', 'rejected'):
            accepted = not (complete or passed or accounting)
        else:
            accepted = not passed
        expect(rows, accepted, 'terminal_flag_matrix')

for kind in ('interrupted', 'unknown', 'rejected', 'late', 'no_start'):
    for field in ('event_count', 'decision_count', 'interrupted_response_count'):
        rows = copy.deepcopy(outcomes[kind])
        rows[-1][field] += 1
        expect(rows, False, 'terminal_count_mismatch')
    for field, value in (('failure_reason', None), ('failure_reason', 'invalid_event'),
                         ('settlement', outcomes['success'][-1]['settlement'])):
        rows = copy.deepcopy(outcomes[kind])
        rows[-1][field] = value
        expect(rows, False, 'terminal_reason_settlement')
    for accounting, prep, post in itertools.product((False, True), (None,0.0), (None,0.0)):
        rows = copy.deepcopy(outcomes[kind])
        rows[-1].update(accounting_complete=accounting, preparation_compute_seconds=prep,
                        post_terminal_compute_seconds=post)
        accepted = not accounting or (kind in ('late','no_start') and
                                      prep is not None and post is not None)
        expect(rows, accepted, 'terminal_totals_matrix')

# Exhaust the finite distinct private-card pair ordering domain at the public wire boundary.
# Altered cards may not match the fixture; this is explicitly schema admission, not legal replay.
for low, high in itertools.combinations(range(52), 2):
    for pair, accepted in (([low,high],True), ([high,low],False)):
        rows = copy.deepcopy(outcomes['success'])
        rows[1]['event']['private_cards'] = pair
        expect(rows, accepted, 'private_pair_domain')
for card in range(52):
    rows = copy.deepcopy(outcomes['success'])
    rows[1]['event']['private_cards'] = [card,card]
    expect(rows, False, 'duplicate_private_cards')
for permutation in itertools.permutations([51,0,23]):
    rows = copy.deepcopy(outcomes['success'])
    event = next(row['event'] for row in rows if row['record_type']=='event' and
                 row['event']['kind']=='street_revealed')
    event['cards'] = list(permutation)
    expect(rows, True, 'board_reveal_order')

# Independently fault every observed clock source read on the all-in/side-pot control B.
# Existing changed tests sweep passive A and rejected-input A; this adds a distinct real path.
_, _, baseline = host(FIXTURE_B)
for fault in ('invalid','reversed','exception'):
    for position in range(1, baseline.calls+1):
        source = Source(position, fault)
        outcome, _, observed = host(FIXTURE_B, source=source)
        assert observed.calls == position, (fault, position, observed.calls)
        assert not outcome.receipt.passed, (fault, position, 'false host success')
        parse_trace(outcome.trace)
        COUNTS['all_in_clock_failure_sweep'] = COUNTS.get('all_in_clock_failure_sweep',0)+1

print(json.dumps({'independent_public_checks':COUNTS,
                  'all_in_observed_clock_reads':baseline.calls,
                  'total_cases':sum(COUNTS.values()),'result':'PASS'}, sort_keys=True))
