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
    decision_rows = [row for row in trace_rows if row['kind'] == 'decision']
    assert len(decision_rows) == len(host.mailbox.accepted), ('accepted/trace-decision loss', case_counter)
    if source.failed:
        assert not outcome.receipt.passed, ('fault admitted as success', case_counter)
        assert outcome.receipt.failure_reason is not None or outcome.receipt.secondary_failures, ('unexplained source fault', case_counter)
        assert source.calls == source.observations[-1]['read'], ('resampled', case_counter)
    return host, outcome, witness

counts = {}
for fixture in (FIXTURE_A, FIXTURE_B):
    source = Source(collect=True)
    host, normal, _ = run(fixture, source)
    assert normal.receipt.passed
    counts[fixture.name] = source.calls
    print(json.dumps({'baseline':fixture.name, 'observations':source.calls, 'closure_seams':source.observations[-5:]}), flush=True)
    for kind in ('invalid', 'reversed', 'source'):
        for read in range(1, source.calls + 1):
            clock = Source(fail_at=read, kind=kind)
            host, outcome, witness = run(fixture, clock)
            expected = 'clock_reversed' if kind == 'reversed' else 'clock_invalid'
            assert codes(outcome.receipt) == (expected, []), (fixture.name, read, kind, codes(outcome.receipt))
            if read > source.calls - 5:
                assert len(outcome.decisions) == fixture.expected_controlled_actions
            results.append({'fixture':fixture.name, 'read':read, 'kind':kind, 'codes':codes(outcome.receipt), 'source_calls':clock.calls, 'failed_witness_calls':witness.calls_after_failed, 'deliveries':len(host.mailbox.accepted)})
print(json.dumps({'sweep_runs':len(results), 'all_clock_faults_typed':True, 'source_resample_count':0, 'sweep_failed_witness_calls':sum(x['failed_witness_calls'] for x in results), 'all_known_deliveries_retained':True}), flush=True)

def wrong_oracle(**kwargs):
    result = chip_depth_settlement(**kwargs)
    return replace(result, final_stacks=tuple(v + 1 for v in result.final_stacks))

write_root = PACKET / 'checks' / ('cold-a-write-root-' + slot)
write_root.mkdir()
destination = write_root / 'already-exists.jsonl'
with destination.open('xb') as handle:
    handle.write(b'independent pre-existing destination\n')
original_bytes = destination.read_bytes()
# Production writer encounters a real existing destination; no writer double.
scenarios = [
    ('write_only', Source(), False, True, ('trace_write_failed', [])),
    ('write_before_publication_stop_clock', Source(fail_at=counts[FIXTURE_A.name]-1), False, True, ('trace_write_failed', ['clock_invalid'])),
    ('write_before_finalization_clock', Source(fail_at=counts[FIXTURE_A.name]), False, True, ('trace_write_failed', ['clock_invalid'])),
    ('clock_before_mismatch_before_write', Source(fail_at=counts[FIXTURE_A.name]-4), True, True, ('clock_invalid', ['settlement_mismatch', 'trace_write_failed'])),
    ('mismatch_before_bookkeeping_stop_clock_before_write', Source(fail_at=counts[FIXTURE_A.name]-3), True, True, ('settlement_mismatch', ['clock_invalid', 'trace_write_failed'])),
    ('publication_entry_clock_before_write', Source(fail_at=counts[FIXTURE_A.name]-2), False, True, ('clock_invalid', ['trace_write_failed'])),
]
for name, clock, mismatch, writing, expected in scenarios:
    kwargs = {'oracle': wrong_oracle} if mismatch else {}
    if writing:
        kwargs.update(destination=destination, run_root=write_root)
    host, outcome, witness = run(FIXTURE_A, clock, **kwargs)
    observed = codes(outcome.receipt)
    row = {'case':name, 'expected':expected, 'observed':observed, 'receipt':asdict(outcome.receipt), 'fault_observations':clock.observations, 'deliveries':len(host.mailbox.accepted), 'decisions':len(outcome.decisions), 'failed_witness_calls':witness.calls_after_failed}
    print(json.dumps(row), flush=True)
    assert destination.read_bytes() == original_bytes
    assert len(outcome.decisions) == FIXTURE_A.expected_controlled_actions
    if observed != expected:
        violations.append(row)

# A rejected public event closes its real transition boundary. Test later
# clock failure there; no ledger double or source modification is involved.
bad_fixture = replace(FIXTURE_A, name='cold-a-wrong-actor', script=(replace(FIXTURE_A.script[0], seat=5), *FIXTURE_A.script[1:]))
for kind in ('invalid', 'reversed', 'source'):
    clock = Source(fail_seam='_release_boundary', kind=kind)
    host, outcome, witness = run(bad_fixture, clock)
    expected = ('event_order', ['clock_reversed' if kind == 'reversed' else 'clock_invalid'])
    observed = codes(outcome.receipt)
    row = {'case':'rejected_event_then_boundary_closure_'+kind, 'expected':expected, 'observed':observed, 'receipt':asdict(outcome.receipt), 'fault_observations':clock.observations, 'deliveries':len(host.mailbox.accepted), 'decisions':len(outcome.decisions), 'retained_closure_codes':[v.value for v in host.runtime.closure_failures]}
    print(json.dumps(row), flush=True)
    if observed != expected:
        violations.append(row)
assert gr('status', '--porcelain') == b''
print(json.dumps({'summary':{'cases':case_counter, 'sweep':len(results), 'contract_mismatches':len(violations), 'snapshot_clean':True}}), flush=True)
raise SystemExit(1 if violations else 0)
