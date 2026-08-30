import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from dataclasses import replace

from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.model import FailureCode
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost, verify_successful_trace
from pontius.v0a.runtime import HandRuntime
import pontius.v0a.trace as tr

COMMIT = 'ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1'
MANIFEST = 'c234b4271bd665e869689fb5d976e629703b678faeb3f55532a3615edc98b189'
BASE = '52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8'
STEP = 125_000_000
class Clock:
    def __init__(self):
        self.now = 1_000_000
        self.fail_next = False
        self.reads = self.raises = 0
    def __call__(self):
        self.reads += 1
        if self.fail_next:
            self.raises += 1
            self.fail_next = False
            return True
        return self.now

def make_host(fixture, clock, suffix):
    policy = ImmutableBlueprintActionSource(source_id='cold-b-reference')
    host = ReplayHost(fixture, run_id=PROTOCOL_ID + '-correctness-cold-b-' + suffix,
        blueprint=policy, clock=clock, source_commit=COMMIT, source_manifest_sha256=MANIFEST)
    return host, policy

def observed_run(callback, host, **kwargs):
    old = sys.getprofile()
    sys.setprofile(callback)
    try:
        return host.run(**kwargs)
    finally:
        sys.setprofile(old)

for fixture in (FIXTURE_A, FIXTURE_B):
    with tempfile.TemporaryDirectory(prefix='codex-b-measured-') as temporary:
        root = Path(temporary)
        parent = root / 'parent'
        parent.mkdir()
        target = parent / 'trace.jsonl'
        clock = Clock()
        host, policy = make_host(fixture, clock, fixture.name)
        expected = dict(preparation=0, post_terminal=0, publication=0)
        samples, foreign = [], []
        def observe(frame, event, arg):
            if event != 'call':
                return
            code = frame.f_code
            terminal = False
            relevant = False
            if code is tr.canonical_json.__code__:
                payload = frame.f_locals['payload']
                terminal = type(payload) is dict and payload.get('record_type') == 'terminal'
                relevant = True
            elif code is tr.TraceWriter.append.__code__:
                content = frame.f_locals['content']
                terminal = b'"record_type":"terminal"' in content
                relevant = True
            elif code is tr._open_native.__code__:
                relevant = True
            elif code is tr._NativeHandle.close.__code__:
                terminal = True
                relevant = True
            if relevant:
                category = 'publication' if terminal else ('post_terminal' if host.runtime.betting_terminal else 'preparation')
                clock.now += STEP
                expected[category] += STEP
            if code is ReplayHost._events.__code__ and target.exists():
                rows = [json.loads(line) for line in target.read_bytes().splitlines()]
                decisions = [row for row in rows if row['record_type'] == 'decision']
                assert len(decisions) == len(host.mailbox.accepted)
                assert not any(row['record_type'] == 'terminal' for row in rows)
                samples.append(len(decisions))
                if not foreign:
                    child = "import pathlib, sys; p=pathlib.Path(sys.argv[1]); blocked=[]\nfor mode in ('ab','wb'):\n try:\n  with p.open(mode) as f: f.write(b'foreign')\n except PermissionError:\n  blocked.append(mode)\nassert blocked == ['ab','wb'], blocked\nprint('foreign writes denied')"
                    result = subprocess.run([sys.executable, '-B', '-P', '-c', child, str(target)],
                        cwd=Path.cwd(), env=dict(os.environ), capture_output=True, text=True)
                    assert result.returncode == 0, (result.stdout, result.stderr)
                    foreign.append(result.stdout.strip())
                    try:
                        parent.rename(root / 'moved')
                    except PermissionError:
                        pass
                    else:
                        raise AssertionError('owned parent was renamed')
        outcome = observed_run(observe, host, destination=target, run_root=root)
        terminal = tr.parse_trace(outcome.trace).terminal
        assert outcome.receipt.passed, outcome.receipt
        assert target.read_bytes() == outcome.trace
        assert outcome.receipt.trace_sha256 == hashlib.sha256(target.read_bytes()).hexdigest()
        actual = dict(preparation=terminal['preparation_compute_seconds'],
                      post_terminal=terminal['post_terminal_compute_seconds'],
                      publication=outcome.receipt.terminal_publication_compute_seconds)
        assert actual == {key: value / 1_000_000_000 for key, value in expected.items()}, (actual, expected)
        assert all(decision.timing.elapsed_ns == 0 for decision in outcome.decisions)
        assert len(outcome.decisions) == fixture.expected_controlled_actions
        assert samples and foreign
        verify_successful_trace(target.read_bytes(), fixture=fixture, blueprint=policy,
            source_commit=COMMIT, source_manifest_sha256=MANIFEST,
            expected_mode='correctness', expected_clock_kind='deterministic_test')
        parent.rename(root / 'released')
        print(json.dumps(dict(case='measured_native_' + fixture.name, categories=actual,
              incremental_observations=len(samples), decisions=len(outcome.decisions),
              foreign=foreign, released=True)), flush=True)

# A real native create-new refusal preserves the accepted action and original bytes.
with tempfile.TemporaryDirectory(prefix='codex-b-collision-') as temporary:
    root = Path(temporary)
    target = root / 'existing.jsonl'
    target.write_bytes(b'original\n')
    host, _ = make_host(FIXTURE_A, Clock(), 'existing')
    outcome = host.run(destination=target, run_root=root)
    assert outcome.receipt.failure_reason is FailureCode.TRACE_WRITE_FAILED
    assert not outcome.receipt.passed and outcome.receipt.trace_sha256 is None
    assert len(outcome.decisions) == len(host.mailbox.accepted) == 1
    assert target.read_bytes() == b'original\n'
    target.rename(root / 'released.jsonl')
    print('PASS native_create_refusal retained=1 original_unchanged released=true', flush=True)

# The successful prepublication terminal cannot attest later host finalization.
for seam in ('publication_close', 'finalization'):
    with tempfile.TemporaryDirectory(prefix='codex-b-final-') as temporary:
        root = Path(temporary)
        target = root / 'trace.jsonl'
        clock = Clock()
        host, _ = make_host(FIXTURE_A, clock, seam)
        armed = []
        def fault(frame, event, arg):
            if armed:
                return
            match = ((seam == 'publication_close' and event == 'return'
                      and frame.f_code is tr.TraceWriter.finish.__code__)
                     or (seam == 'finalization' and event == 'call'
                         and frame.f_code is HandRuntime.finalize_accounting.__code__))
            if match:
                armed.append(clock.reads)
                clock.fail_next = True
        outcome = observed_run(fault, host, destination=target, run_root=root)
        assert armed and clock.raises == 1
        terminal = tr.parse_trace(target.read_bytes()).terminal
        assert terminal['passed'] is True and terminal['accounting_complete'] is True
        assert not outcome.receipt.passed and not outcome.receipt.accounting_complete
        assert outcome.receipt.failure_reason is FailureCode.CLOCK_INVALID
        assert outcome.receipt.secondary_failures == ()
        assert len(outcome.decisions) == len(host.mailbox.accepted) == 4
        if seam == 'publication_close':
            assert outcome.receipt.terminal_publication_compute_seconds is None
        else:
            assert outcome.receipt.terminal_publication_compute_seconds == 0.0
        target.rename(root / 'released.jsonl')
        print(json.dumps(dict(case=seam, terminal_passed=terminal['passed'], receipt_passed=outcome.receipt.passed,
              primary=outcome.receipt.failure_reason.value, source_raises=clock.raises,
              publication_seconds=outcome.receipt.terminal_publication_compute_seconds,
              retained=len(outcome.decisions), released=True)), flush=True)

# All proper A schedule prefixes fail with a typed reason, with no decision loss.
for count in range(len(FIXTURE_A.script)):
    fixture = replace(FIXTURE_A, script=FIXTURE_A.script[:count])
    host, _ = make_host(fixture, Clock(), 'prefix-' + str(count))
    outcome = host.run()
    assert not outcome.receipt.passed
    assert outcome.receipt.failure_reason is FailureCode.EVENT_ORDER
    assert len(outcome.decisions) == len(host.mailbox.accepted)
    assert tr.parse_trace(outcome.trace).terminal['failure_reason'] == 'event_order'
print('PASS all_20_nonterminal_prefixes typed=event_order retained_deliveries=true', flush=True)

# Independent structural comparison of frozen parser and legal checker bodies.
def blob(revision, path):
    return subprocess.run([os.environ['PONTIUS_GIT'], 'cat-file', 'blob', revision + ':' + path],
                          capture_output=True, check=True).stdout
for path, first_name in (('src/pontius/v0a/trace.py', '_no_duplicate_keys'),
                         ('src/pontius/v0a/replay.py', '_owned_expected_fixture')):
    def nodes(revision):
        selected, enabled = {}, False
        for node in ast.parse(blob(revision, path)).body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                enabled = enabled or node.name == first_name
                if enabled:
                    selected[node.name] = ast.dump(node, include_attributes=False)
        return selected
    before, after = nodes(BASE), nodes(COMMIT)
    assert before and before == after, path
    print('PASS preserved_AST', path, len(before), flush=True)
print('ALL INDEPENDENT BOUNDARY CHECKS PASSED', flush=True)
