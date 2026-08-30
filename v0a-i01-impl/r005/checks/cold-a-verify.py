import sys
import platform
from pathlib import Path
import os
import json
import hashlib
import subprocess
import runpy
import unittest
import io
from dataclasses import asdict, replace

SNAPSHOT = Path(r'D:\pontius-snapshots\v0a-r005-cold-a-96aa34d9536845ddaddc4b1dfbb9615e\harness')
PACKET = Path(r'D:\Pontius-handoffs\v0a-i01-impl\r005')
OWNER = Path(r'D:\Pontius')
COMMIT = 'a8582e6d6b53b55415dab79c4a54e252d00b74ad'
BASE = 'b357d333fc2393b7fc7dcf31f30c86616208c817'
MANIFEST = 'e9b0baf12e258d66a92169d38137cbf2f42317158b6515ac377f745bbc52093a'
GIT = r'C:\Program Files\Git\cmd\git.exe'
expected_exe, expected_version = sys.argv[1:3]
assert platform.python_implementation() == 'CPython'
assert platform.python_version() == expected_version
assert Path(sys.executable).resolve() == Path(expected_exe).resolve()
assert sys.flags.dont_write_bytecode == 1 and sys.flags.safe_path
assert Path.cwd() == SNAPSHOT
assert os.environ['PYTHONPATH'] == str(SNAPSHOT / 'src')
assert os.environ['PONTIUS_GIT'] == GIT
assert set(os.environ) <= {'SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP', 'PYTHONPATH', 'PONTIUS_GIT', 'PYTHONIOENCODING', 'PYTHONUTF8', 'LC_CTYPE'}
result = {'identity_before_payload_imports': {'executable': sys.executable, 'full_version': sys.version, 'implementation': platform.python_implementation(), 'cwd': str(Path.cwd()), 'flags': str(sys.flags), 'environment': dict(os.environ)}}

def git(repo, *args):
    call = subprocess.run([GIT, '-C', str(repo), *args], capture_output=True, check=True)
    return call.stdout

before = git(SNAPSHOT, 'status', '--porcelain=v1', '--untracked-files=all')
assert before == b'', before
candidate = json.loads((PACKET / 'candidate.json').read_bytes())
assert candidate['commit'] == COMMIT and candidate['base'] == BASE and candidate['manifest_sha256'] == MANIFEST
assert git(OWNER, 'rev-parse', candidate['ref']).decode().strip() == COMMIT
assert git(OWNER, 'rev-parse', COMMIT + '^').decode().strip() == BASE
assert git(OWNER, 'rev-parse', COMMIT + '^{tree}').decode().strip() == candidate['tree']
assert git(SNAPSHOT, 'rev-parse', 'HEAD').decode().strip() == COMMIT
changed = git(OWNER, 'diff-tree', '-r', '-z', '--no-renames', '--no-commit-id', '--name-status', BASE, COMMIT).split(b'\0')
rows = []
blobs = []
for index in range(0, len(changed)-1, 2):
    status, raw_path = changed[index:index+2]
    rel = raw_path.decode('utf-8')
    blob = b'' if status == b'D' else git(OWNER, 'cat-file', 'blob', COMMIT + ':' + rel)
    digest = '0'*64 if status == b'D' else hashlib.sha256(blob).hexdigest()
    rows.append((digest + '  ' + rel + '\n').encode())
    if status != b'D':
        assert git(SNAPSHOT, 'cat-file', 'blob', COMMIT + ':' + rel) == blob
        assert (SNAPSHOT / rel).read_bytes() == blob
    blobs.append({'path': rel, 'status': status.decode(), 'sha256': digest})
manifest_bytes = b''.join(sorted(rows))
assert manifest_bytes == (PACKET / 'manifest.sha256').read_bytes()
assert hashlib.sha256(manifest_bytes).hexdigest() == MANIFEST
result['identity'] = {'commit': COMMIT, 'base': BASE, 'tree': candidate['tree'], 'manifest_sha256': MANIFEST, 'changed_blobs': blobs, 'snapshot_before': before.decode()}
for rel in ['docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md', 'docs/briefs/v0a-increment-1-brief.md', 'docs/workflow.md']:
    blob = git(OWNER, 'cat-file', 'blob', COMMIT + ':' + rel)
    assert (SNAPSHOT / rel).read_bytes() == blob
result['frozen_governance_verified'] = True
print(json.dumps({'stage':'identity_verified', 'version':platform.python_version(), 'manifest':MANIFEST}), flush=True)

# Every payload import follows the assertions above.
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.clock import MonotonicWitness, ClockInvalidError, ClockReversedError
from pontius.v0a.model import ActionMailbox, MailboxRejectionError, FailureCode
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost, chip_depth_settlement
import pontius.v0a.runtime as runtime_module
import pontius.v0a.replay as replay_module
assert Path(runtime_module.__file__).resolve() == SNAPSHOT / 'src/pontius/v0a/runtime.py'
assert Path(replay_module.__file__).resolve() == SNAPSHOT / 'src/pontius/v0a/replay.py'
result['payload_origins'] = [runtime_module.__file__, replay_module.__file__]

class Clock:
    def __init__(self, observed=None):
        self.now = 10000
        self.reads = 0
        self.arm = None
        self.observed = [] if observed is None else observed
    def __call__(self):
        self.reads += 1
        fault, self.arm = self.arm, None
        if fault:
            self.observed.append('clock_' + fault)
            if fault == 'reversed':
                return self.now - 5000
            raise OSError('cold-A clock source fault')
        self.now += 1000
        return self.now

def make_host(label, clock=None, oracle=chip_depth_settlement, mailbox=None, fixture=FIXTURE_A):
    return ReplayHost(fixture, run_id=f'{PROTOCOL_ID}-correctness-cold-a-{label}', blueprint=ImmutableBlueprintActionSource(source_id='cold-a-empty'), clock=Clock() if clock is None else clock, settlement_oracle=oracle, mailbox=mailbox)

def summarize(host, outcome, observed=None):
    r = outcome.receipt
    codes = ([] if r.failure_reason is None else [r.failure_reason.value]) + [x.value for x in r.secondary_failures]
    return {'observed': observed, 'reported': codes, 'receipt': asdict(r), 'decisions': len(outcome.decisions), 'accepted': host.runtime.accepted_delivery_count, 'failures': [asdict(f) for f in outcome.failures], 'decision_timing': [asdict(d.timing) for d in outcome.decisions], 'terminal': json.loads(outcome.trace.splitlines()[-1])}

probes = []
for kind in ['invalid', 'reversed']:
    observed = []
    clock = Clock(observed)
    def exploding(**kwargs):
        observed.append('settlement_mismatch')
        clock.arm = kind
        raise ZeroDivisionError('cold-A oracle body failed before cleanup')
    host = make_host('body-before-cleanup-' + kind, clock=clock, oracle=exploding)
    outcome = host.run()
    probe = summarize(host, outcome, observed)
    probe['name'] = 'oracle_body_before_cleanup_' + kind
    probe['source_reads_after_fault'] = clock.reads
    probe['expected'] = ['settlement_mismatch', 'clock_' + kind]
    probe['contract_pass'] = probe['reported'] == probe['expected']
    probes.append(probe)

for kind in ['invalid', 'reversed']:
    observed = []
    source = Clock(observed)
    witness = MonotonicWitness(source)
    def clocked_oracle(**kwargs):
        source.arm = kind
        witness()
        return chip_depth_settlement(**kwargs)
    host = make_host('clock-in-oracle-' + kind, clock=witness, oracle=clocked_oracle)
    outcome = host.run()
    probe = summarize(host, outcome, observed)
    probe['name'] = 'shared_public_witness_in_oracle_' + kind
    probe['expected'] = ['clock_' + kind]
    probe['contract_pass'] = probe['reported'] == probe['expected']
    probes.append(probe)

for kind in ['invalid', 'reversed']:
    observed = []
    clock = Clock(observed)
    real = ActionMailbox()
    class AcceptedThenFault:
        def deliver(self, envelope):
            receipt = real.deliver(envelope)
            observed.append('accepted')
            clock.arm = kind
            return receipt
    host = make_host('accepted-clock-' + kind, clock=clock, mailbox=AcceptedThenFault())
    outcome = host.run()
    probe = summarize(host, outcome, observed)
    probe['name'] = 'acknowledged_delivery_then_' + kind
    probe['expected'] = ['clock_' + kind]
    probe['contract_pass'] = (probe['reported'] == probe['expected'] and len(outcome.decisions) == 1 and host.runtime.accepted_delivery_count == 1 and outcome.decisions[0].timing.emission_observed_ns is None and outcome.decisions[0].timing == outcome.failures[0].timing)
    probes.append(probe)

host = make_host('real-write-refusal')
outcome = host.run(destination=PACKET / 'checks/cold-a-verify.py', run_root=PACKET / 'checks')
probe = summarize(host, outcome)
probe['name'] = 'real_existing_destination_refusal'
probe['expected'] = ['trace_write_failed']
probe['contract_pass'] = probe['reported'] == probe['expected'] and not outcome.receipt.passed and len(outcome.decisions) == 4
probes.append(probe)

for kind in ['invalid', 'reversed']:
    observed = []
    clock = Clock(observed)
    def mismatching_oracle(**kwargs):
        oracle = chip_depth_settlement(**kwargs)
        observed.append('settlement_mismatch')
        clock.arm = kind
        return replace(oracle, final_stacks=(0,)*6)
    host = make_host('mismatch-before-cleanup-' + kind, clock=clock, oracle=mismatching_oracle)
    outcome = host.run(destination=PACKET / 'checks/cold-a-verify.py', run_root=PACKET / 'checks')
    observed.append('trace_write_failed')
    probe = summarize(host, outcome, observed)
    probe['name'] = 'detected_mismatch_cleanup_write_' + kind
    probe['expected'] = ['settlement_mismatch', 'clock_' + kind, 'trace_write_failed']
    probe['contract_pass'] = probe['reported'] == probe['expected']
    probes.append(probe)
result['probes'] = probes
print(json.dumps({'stage':'probes', 'version':platform.python_version(), 'results':[{k:p[k] for k in ['name','observed','reported','expected','contract_pass']} for p in probes]}), flush=True)

module = runpy.run_path(str(SNAPSHOT / 'tests/test_v0a_replay.py'), run_name='cold_a_frozen_replay_tests')
classes = ['R2_03HostClosureTests', 'R3_02TypedClosureCauseTests', 'R2_03CompoundScheduleTests', 'R2_03ConservationTests', 'FixtureReplayTests', 'TraceAndAccountingTests']
suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(module[name]) for name in classes)
stream = io.StringIO()
tests = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
result['existing_tests'] = {'classes': classes, 'tests_run': tests.testsRun, 'failures': len(tests.failures), 'errors': len(tests.errors), 'passed': tests.wasSuccessful(), 'output': stream.getvalue()}
assert tests.wasSuccessful(), stream.getvalue()
after = git(SNAPSHOT, 'status', '--porcelain=v1', '--untracked-files=all')
assert after == before == b''
result['snapshot_after'] = after.decode()
result['overall'] = 'FAIL' if any(not p['contract_pass'] for p in probes) else 'PASS'
output = PACKET / ('checks/cold-a-receipt-' + expected_version + '.json')
with output.open('x', encoding='utf-8', newline='\n') as handle:
    json.dump(result, handle, indent=2, ensure_ascii=True)
    handle.write('\n')
print(json.dumps({'stage':'complete', 'receipt':str(output), 'existing_tests':tests.testsRun, 'overall':result['overall'], 'source_clean':True}), flush=True)
