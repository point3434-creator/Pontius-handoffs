"""Codex A independent r006 public-boundary checks; no production edits."""
import copy
import hashlib
import itertools
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import unittest

SNAPSHOT = Path(r"D:\Pontius-review-codex-a-r006-6c3f4d")
PACKET = Path(r"D:\Pontius-handoffs\v0a-i01-ab\r006")
COMMIT = "52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8"
BASE = "6cdf7b00dac653a9a295bbb86cdc3b5782317491"
MANIFEST = "7e1575b18c7a9cf0c74bd956a54e899aad670349d198d7863ae1f67463583d7a"
GIT = r"C:\Program Files\Git\cmd\git.exe"
assert tuple(sys.version_info[:3]) == tuple(map(int, sys.argv[1].split('.')))
assert Path(sys.executable) == Path(sys.argv[2])
assert Path.cwd() == SNAPSHOT
assert os.environ['PYTHONPATH'] == str(SNAPSHOT / 'src')
assert os.environ['PONTIUS_GIT'] == GIT
assert sys.flags.dont_write_bytecode and sys.flags.safe_path and sys.flags.no_user_site
assert 'PATH' not in os.environ
CLEAN_ENV = dict(os.environ)
assert stat.S_ISREG(Path(GIT).stat().st_mode)
assert not Path(GIT).lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT

def git(*args):
    return subprocess.run([GIT, '-C', str(SNAPSHOT), *args], check=True,
                          capture_output=True, env=CLEAN_ENV).stdout

assert git('rev-parse', 'HEAD').decode().strip() == COMMIT
assert git('rev-parse', COMMIT + '^').decode().strip() == BASE
assert git('rev-parse', COMMIT + '^{tree}').decode().strip() == (
    '8f5e35e5c266d8a8fa4c63e96550a4e9ef894216')
fields = git('diff-tree', '--no-renames', '-r', '-z', '--no-commit-id',
             '--name-status', BASE, COMMIT).decode().split('\0')
rows = []
paths = []
for index in range(0, len(fields) - 1, 2):
    status, path = fields[index:index + 2]
    paths.append(path)
    data = git('cat-file', 'blob', COMMIT + ':' + path)
    assert not data.startswith(b'\xef\xbb\xbf') and b'\r' not in data
    assert all(line.rstrip() == line for line in data.splitlines())
    digest = hashlib.sha256(data).hexdigest() if status != 'D' else '0' * 64
    rows.append(f'{digest}  {path}\n'.encode())
    assert (SNAPSHOT / path).read_bytes() == data
assert set(paths) == {'src/pontius/v0a/trace.py', 'tests/test_v0a_trace.py'}
manifest_bytes = b''.join(sorted(rows))
assert hashlib.sha256(manifest_bytes).hexdigest() == MANIFEST
assert manifest_bytes == (PACKET / 'manifest.sha256').read_bytes()
assert hashlib.sha256((PACKET / 'coverage.md').read_bytes()).hexdigest() == (
    '8316fc9dc13bac5b66142f73ffc992b537f009736bde77694eb9eec7b0a6ee46')

import pontius.v0a.trace as trace
import pontius.v0a.model as model
import pontius.v0a.replay as replay
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.clock import MonotonicWitness, ClockInvalidError, ClockReversedError
for module in (trace, model, replay):
    assert Path(module.__file__).resolve().is_relative_to(SNAPSHOT / 'src')
print(json.dumps({'kind': 'identity', 'executable': sys.executable,
                  'version': sys.version, 'cwd': str(Path.cwd()),
                  'flags': str(sys.flags), 'launch_environment': CLEAN_ENV, 'post_import_environment': dict(os.environ),
                  'git': GIT, 'commit': COMMIT, 'manifest': MANIFEST,
                  'modules': {m.__name__: m.__file__ for m in (trace, model, replay)},
                  'blob_rows': manifest_bytes.decode()}, sort_keys=True), flush=True)

# This projection is transcribed from ADR0485's field list, not a production helper.
PROJECTION = ('hand_id event_index action_index street_action_index seat street '
              'state_before_sha256 state_after_sha256 visible_cards_sha256 '
              'blueprint_sha256 selected_action selection_reason spine_reason '
              'preparation_use').split()
def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')
def encode(rows):
    rows = copy.deepcopy(rows)
    semantic = {'events': [r['event'] for r in rows if r['record_type'] == 'event'],
                'decisions': [{k: r[k] for k in PROJECTION} for r in rows
                              if r['record_type'] == 'decision'],
                'settlement': rows[-1]['settlement']}
    rows[-1]['semantic_sha256'] = hashlib.sha256(canonical(semantic)).hexdigest()
    prefix = b''.join(canonical(r) + b'\n' for r in rows[:-1])
    rows[-1]['trace_prefix_sha256'] = hashlib.sha256(prefix).hexdigest()
    return prefix + canonical(rows[-1]) + b'\n'

class Clock:
    def __init__(self):
        self.now = 100_000
        self.fault = None
    def __call__(self):
        if self.fault == 'invalid':
            return False
        if self.fault == 'reversed':
            return self.now - 1
        self.now += 10_000
        return self.now

def real_case(kind='success', fixture=None):
    clock = Clock()
    real_mailbox = model.ActionMailbox()
    class Mailbox:
        def deliver(self, envelope):
            if kind == 'rejected':
                return real_mailbox.deliver(None)
            receipt = real_mailbox.deliver(envelope)
            if kind == 'unknown':
                raise RuntimeError('lost real mailbox acknowledgement')
            if kind == 'interrupted':
                clock.fault = 'invalid'
            if kind == 'late':
                clock.now += 16_000_000_000
            return receipt
    if kind == 'no_start':
        clock.fault = 'invalid'
    def bad_oracle(**kwargs):
        raise ValueError('oracle body fault')
    kwargs = {'settlement_oracle': bad_oracle} if kind == 'settlement' else {}
    policy = ImmutableBlueprintActionSource('independent-codex-a-policy')
    host = replay.ReplayHost(fixture or replay.FIXTURE_A,
                            run_id=replay.PROTOCOL_ID + '-correctness-codex-a-' + kind,
                            blueprint=policy, clock=clock, mailbox=Mailbox(), **kwargs)
    outcome = host.run()
    return outcome, real_mailbox, policy

class IndependentChecks(unittest.TestCase):
    def assert_refused(self, rows):
        with self.assertRaises(trace.TraceInvalidError):
            trace.parse_trace(encode(rows))
    def test_real_positive_and_failure_prefixes(self):
        expected = {'success': (4, None), 'late': (1, 'action_deadline_exceeded'),
                    'interrupted': (1, 'clock_invalid'),
                    'unknown': (1, 'delivery_ambiguous'),
                    'rejected': (0, 'delivery_rejected'), 'no_start': (0, 'clock_invalid'),
                    'settlement': (4, 'settlement_mismatch')}
        for kind, (accepted, reason) in expected.items():
            with self.subTest(kind=kind):
                out, mailbox, _ = real_case(kind)
                parsed = trace.parse_trace(out.trace)
                self.assertEqual(len(mailbox.accepted), accepted)
                self.assertEqual(parsed.terminal['failure_reason'], reason)
                self.assertEqual(parsed.terminal['passed'], kind == 'success')
                if kind in ('interrupted', 'unknown', 'rejected'):
                    self.assertEqual(tuple(parsed.terminal[k] for k in
                                           ('complete', 'passed', 'accounting_complete')),
                                     (False, False, False))
    def test_bound_a_and_b_still_verify(self):
        for fixture in (replay.FIXTURE_A, replay.FIXTURE_B):
            out, _, policy = real_case(fixture=fixture)
            self.assertTrue(out.receipt.passed)
            replay.verify_successful_trace(out.trace, fixture=fixture, blueprint=policy,
                                           source_commit='0' * 40,
                                           source_manifest_sha256='0' * 64, expected_mode='correctness',
                                           expected_clock_kind='deterministic_test')
    def test_interrupted_and_unknown_flag_lattice(self):
        for kind in ('interrupted', 'unknown', 'rejected'):
            original = [json.loads(row) for row in real_case(kind)[0].trace.splitlines()]
            for flags in itertools.product((False, True), repeat=3):
                rows = copy.deepcopy(original)
                rows[-1].update(zip(('complete', 'passed', 'accounting_complete'), flags))
                rows[-1].update(preparation_compute_seconds=0.0,
                                post_terminal_compute_seconds=0.0)
                with self.subTest(kind=kind, flags=flags):
                    if any(flags):
                        self.assert_refused(rows)
                    else:
                        trace.parse_trace(encode(rows))
    def test_failed_settlement_reason_and_totals(self):
        successful = [json.loads(row) for row in real_case()[0].trace.splitlines()]
        for kind in ('late', 'interrupted', 'unknown', 'rejected', 'no_start', 'settlement'):
            original = [json.loads(row) for row in real_case(kind)[0].trace.splitlines()]
            for key, value in (('settlement', successful[-1]['settlement']),
                               ('failure_reason', None)):
                rows = copy.deepcopy(original)
                rows[-1][key] = value
                self.assert_refused(rows)
            if kind != 'settlement':
                rows = copy.deepcopy(original)
                rows[-1]['failure_reason'] = 'source_binding_mismatch'
                self.assert_refused(rows)
        for kind in ('late', 'settlement'):
            original = [json.loads(row) for row in real_case(kind)[0].trace.splitlines()]
            for prep, post in itertools.product((None, 0.0), repeat=2):
                rows = copy.deepcopy(original)
                rows[-1].update(accounting_complete=True,
                                preparation_compute_seconds=prep,
                                post_terminal_compute_seconds=post)
                if prep is None or post is None:
                    self.assert_refused(rows)
                else:
                    trace.parse_trace(encode(rows))
                rows[-1]['accounting_complete'] = False
                trace.parse_trace(encode(rows))
    def test_private_order_and_wire_value_domains(self):
        original = [json.loads(row) for row in real_case()[0].trace.splitlines()]
        values = {'private_cards': ([51, 0], [1, 1], [False, 2], [0, 52]),
                  'button': (True, -1, 6, 0.0), 'event_index': (False, 1, -1, 0.0),
                  'hand_id': (None, '', '\u00e9'), 'small_blind': (0, True, 2),
                  'starting_stacks': ([1]*6, [True]*6, [2]*5)}
        for field, domain in values.items():
            for value in domain:
                rows = copy.deepcopy(original)
                rows[1]['event'][field] = value
                with self.subTest(field=field, value=value):
                    self.assert_refused(rows)
        rows = copy.deepcopy(original)
        rows[1]['event']['private_cards'] = [0, 51]
        trace.parse_trace(encode(rows))
        rows = copy.deepcopy(original)
        reveal = next(r['event'] for r in rows if r['record_type'] == 'event'
                      and r['event']['kind'] == 'street_revealed')
        reveal['cards'] = [51, 1, 0]
        parsed = trace.parse_trace(encode(rows))
        self.assertEqual(next(e['cards'] for e in parsed.events
                              if e['kind'] == 'street_revealed'), (51, 1, 0))
    def test_real_source_before_adapter_compounds(self):
        for source_fault, finish in itertools.product(('invalid', 'reversed'),
                                                      ('ack', 'unknown', 'rejected')):
            source = Clock()
            witness = MonotonicWitness(source)
            mailbox = model.ActionMailbox()
            observed = []
            class Adapter:
                def deliver(self, envelope):
                    receipt = mailbox.deliver(envelope) if finish != 'rejected' else None
                    source.fault = source_fault
                    try:
                        witness()
                    except (ClockInvalidError, ClockReversedError):
                        observed.append('source_' + source_fault)
                    if finish == 'unknown':
                        observed.append('adapter_exception')
                        raise ValueError('later adapter failure')
                    if finish == 'rejected':
                        observed.append('adapter_rejection')
                        return mailbox.deliver(None)
                    return receipt
            out = replay.ReplayHost(replay.FIXTURE_A, blueprint=
                    ImmutableBlueprintActionSource('independent-compound'), clock=witness,
                    mailbox=Adapter(), run_id=replay.PROTOCOL_ID +
                    '-correctness-codex-a-compound-' + source_fault + '-' + finish).run()
            with self.subTest(source_fault=source_fault, finish=finish):
                parsed = trace.parse_trace(out.trace)
                self.assertEqual(parsed.terminal['failure_reason'], 'clock_' + source_fault)
                self.assertEqual(len(mailbox.accepted), 0 if finish == 'rejected' else 1)
                self.assertEqual(observed[0], 'source_' + source_fault)
                if finish != 'ack':
                    self.assertEqual(len(observed), 2)

if __name__ == '__main__':
    suite_result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(IndependentChecks))
    statuses = []
    for name in ('test_v0a_trace.py', 'test_v0a_hand_replay.py',
                 'test_v0a_replay.py', 'test_v0a_contract_faults.py'):
        command = [sys.executable, '-B', '-P', str(SNAPSHOT / 'tests' / name)]
        result = subprocess.run(command, cwd=SNAPSHOT, env=CLEAN_ENV,
                                capture_output=True, text=True)
        statuses.append(result.returncode)
        print(json.dumps({'kind': 'suite', 'command': command, 'exit': result.returncode,
                          'environment': CLEAN_ENV, 'stdout': result.stdout, 'stderr': result.stderr}), flush=True)
    print(json.dumps({'kind': 'summary', 'independent_tests': suite_result.testsRun,
                      'failures': len(suite_result.failures), 'errors': len(suite_result.errors),
                      'suite_exits': statuses}), flush=True)
    sys.exit(0 if suite_result.wasSuccessful() and all(s == 0 for s in statuses) else 1)
