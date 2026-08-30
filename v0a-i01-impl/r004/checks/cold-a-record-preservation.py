import sys
EXPECTED = {
    '311': (r'D:\Pontius-tools\py311\Scripts\python.exe', (3, 11, 15, 'final', 0), '3.11.15 (main, Jul 23 2026, 14:42:43) [MSC v.1944 64 bit (AMD64)]'),
    '314': (r'D:\Pontius\.venv\Scripts\python.exe', (3, 14, 6, 'final', 0), '3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)]'),
}
slot = sys.argv[1]
exe, version_info, full_version = EXPECTED[slot]
assert sys.executable.casefold() == exe.casefold(), sys.executable
assert sys.implementation.name == 'cpython', sys.implementation
assert tuple(sys.version_info) == version_info, tuple(sys.version_info)
assert sys.version == full_version, sys.version
assert sys.flags.dont_write_bytecode == 1 and sys.flags.safe_path is True
# Identity assertions above precede all repository imports.
import os, json, hashlib, subprocess
from pathlib import Path
from dataclasses import replace, asdict
SNAP = Path(r'D:/pontius-snapshots/v0a-r004-cold-a-4ea61c5d8d494d66a1951cf78a019ee3/harness')
PACKET = Path(r'D:/Pontius-handoffs/v0a-i01-impl/r004')
COMMIT = '0207430a37e1e5b31c8da8da7aa57da1bc5c88ee'
MANIFEST = 'ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef'
assert Path.cwd() == SNAP
assert Path(os.environ['PYTHONPATH']) == SNAP / 'src'
assert os.environ['PONTIUS_GIT'] == r'C:/Program Files/Git/cmd/git.exe'
allowed_env = {'SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP', 'PATH', 'PYTHONPATH', 'PONTIUS_GIT', 'PYTHONNOUSERSITE', 'PYTHONDONTWRITEBYTECODE'}
assert set(os.environ).issubset(allowed_env), sorted(set(os.environ) - allowed_env)
git = os.environ['PONTIUS_GIT']
def gr(*args):
    return subprocess.run([git, '-C', str(SNAP), *args], check=True, capture_output=True).stdout
assert gr('rev-parse', 'HEAD').decode().strip() == COMMIT
assert gr('status', '--porcelain') == b''
candidate = json.loads((PACKET / 'candidate.json').read_text())
assert candidate['commit'] == COMMIT and candidate['manifest_sha256'] == MANIFEST
assert gr('rev-parse', COMMIT + '^').decode().strip() == candidate['base']
assert gr('rev-parse', COMMIT + '^{tree}').decode().strip() == candidate['tree']
fields = gr('diff-tree', '-r', '-z', '--no-renames', '--no-commit-id', '--name-status', COMMIT + '^', COMMIT).split(b'\0')
rows = []
for i in range(0, len(fields) - 1, 2):
    status, rawpath = fields[i:i + 2]
    path = rawpath.decode()
    digest = '0' * 64 if status == b'D' else hashlib.sha256(gr('cat-file', 'blob', COMMIT + ':' + path)).hexdigest()
    rows.append(f'{digest}  {path}\n')
manifest_bytes = ''.join(sorted(rows)).encode()
assert manifest_bytes == (PACKET / 'manifest.sha256').read_bytes()
assert hashlib.sha256(manifest_bytes).hexdigest() == MANIFEST
for path in ('docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md', 'docs/briefs/v0a-increment-1-brief.md'):
    assert gr('cat-file', 'blob', COMMIT + ':' + path) == gr('cat-file', 'blob', candidate['base'] + ':' + path)
print(json.dumps({'identity': {'executable':sys.executable, 'implementation':sys.implementation.name, 'version':sys.version, 'cwd':str(Path.cwd()), 'flags':'-B -P', 'environment':dict(os.environ), 'commit':COMMIT, 'tree':candidate['tree'], 'base':candidate['base'], 'manifest_sha256':MANIFEST, 'manifest_rows':len(rows)}}), flush=True)
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.clock import ClockReversedError, MonotonicWitness
from pontius.v0a.model import FailureCode
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost, chip_depth_settlement
for name, module in sorted(sys.modules.items()):
    if name.startswith('pontius') and getattr(module, '__file__', None):
        assert Path(module.__file__).resolve().is_relative_to(SNAP / 'src'), (name, module.__file__)
print(json.dumps({'optional_import_roots':sorted({n.split('.')[0] for n in sys.modules if n.startswith(('cupy', 'torch', 'numpy'))})}), flush=True)
assert not any(n.startswith(('cupy', 'torch')) for n in sys.modules)

class Source:
    def __init__(self, fail_at=None, kind='invalid', fail_seam=None, collect=False):
        self.calls = 0
        self.fail_at = fail_at
        self.kind = kind
        self.fail_seam = fail_seam
        self.collect = collect
        self.failed = False
        self.observations = []
    def __call__(self):
        assert not self.failed, 'source resampled after fault'
        self.calls += 1
        frames = []
        frame = sys._getframe(1)
        while frame:
            if frame.f_code.co_filename.replace('\\', '/').endswith('/v0a/runtime.py'):
                frames.append(frame.f_code.co_name)
            frame = frame.f_back
        fault = self.calls == self.fail_at or (self.fail_seam is not None and self.fail_seam in frames)
        if self.collect or fault:
            self.observations.append({'read':self.calls, 'runtime_frames':frames, 'fault':fault})
        if fault:
            self.failed = True
            if self.kind == 'source':
                raise OSError('independent source failure')
            if self.kind == 'reversed':
                if self.calls == 1:
                    raise ClockReversedError('source explicitly reports reversal')
                return (self.calls - 2) * 1000
            return True
        return self.calls * 1000

class ObservedWitness(MonotonicWitness):
    def __init__(self, source):
        super().__init__(source)
        self.calls_after_failed = 0
    def __call__(self):
        if self.failed:
            self.calls_after_failed += 1
        return super().__call__()

case_counter = 0
violations = []
results = []
def codes(receipt):
    return (None if receipt.failure_reason is None else receipt.failure_reason.value, [v.value for v in receipt.secondary_failures])
def run(fixture, source, **kwargs):
    global case_counter
    case_counter += 1
    oracle = kwargs.pop('oracle', chip_depth_settlement)
    witness = ObservedWitness(source)
    host = ReplayHost(fixture, run_id=f'{PROTOCOL_ID}-correctness-cold-a-{slot}-{case_counter}', blueprint=ImmutableBlueprintActionSource(source_id='cold-a-independent'), clock=witness, settlement_oracle=oracle)
    outcome = host.run(**kwargs)
    assert len(host.mailbox.accepted) == len(outcome.decisions), ('accepted/decision loss', case_counter)
    trace_rows = [json.loads(row) for row in outcome.trace.splitlines()]
    decision_rows = [row for row in trace_rows if row['record_type'] == 'decision']
    assert len(decision_rows) == len(host.mailbox.accepted), ('accepted/trace-decision loss', case_counter)
    if source.failed:
        assert not outcome.receipt.passed, ('fault admitted as success', case_counter)
        assert outcome.receipt.failure_reason is not None or outcome.receipt.secondary_failures, ('unexplained source fault', case_counter)
        assert source.calls == source.observations[-1]['read'], ('resampled', case_counter)
    return host, outcome, witness

verified = 0
for fixture in (FIXTURE_A, FIXTURE_B):
    baseline_clock = Source()
    baseline_host, baseline, _ = run(fixture, baseline_clock)
    assert baseline.receipt.passed
    for position in range(baseline_clock.calls - 4, baseline_clock.calls + 1):
        for kind in ('invalid', 'reversed', 'source'):
            clock = Source(fail_at=position, kind=kind)
            host, outcome, witness = run(fixture, clock)
            assert outcome.decisions == baseline.decisions, ('full delivered record changed', fixture.name, position, kind)
            assert host.mailbox.accepted == baseline_host.mailbox.accepted, ('accepted envelopes changed', fixture.name, position, kind)
            for decision in outcome.decisions:
                envelope = host.mailbox.accepted[(decision.hand_id, decision.action_index)]
                assert (envelope.seat, envelope.street, envelope.action) == (decision.seat, decision.street, decision.selected_action)
            assert witness.calls_after_failed == 0, ('closure queried dead witness', fixture.name, position, kind)
            verified += 1
assert gr('status', '--porcelain') == b''
print(json.dumps({'full_record_preservation': {'closure_schedules':verified, 'interpreter':slot, 'all_decision_fields_equal_to_successful_control':True, 'all_mailbox_envelopes_equal_to_successful_control':True, 'all_record_actions_match_mailbox_actions':True, 'no_dead_witness_calls_at_five_closure_seams':True, 'snapshot_clean':True}}), flush=True)
