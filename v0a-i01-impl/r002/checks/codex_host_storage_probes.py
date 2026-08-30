"""Coordinator diagnostics for frozen r002; no candidate mutations."""
import sys, json, os
identity = dict(executable=sys.executable, implementation=sys.implementation.name,
                full_version=sys.version, version=list(sys.version_info[:3]))
assert identity['implementation'] == 'cpython'
assert '.'.join(map(str, identity['version'][:2])) == sys.argv[1]
assert os.path.normcase(sys.executable) == os.path.normcase(sys.argv[2])
print(json.dumps({'identity_before_payload_import': identity}), flush=True)
from pathlib import Path
from unittest.mock import patch
import subprocess, uuid
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.replay import ReplayHost, FIXTURE_A, PROTOCOL_ID
from pontius.v0a.trace import TraceBuilder, parse_trace, write_trace
import pontius.v0a.trace as trace_module
assert Path(trace_module.__file__).resolve() == Path.cwd() / 'src/pontius/v0a/trace.py'

class Clock:
    def __init__(self): self.now = 1000
    def __call__(self):
        value = self.now
        self.now += 1000
        return value

def host(clock, suffix):
    return ReplayHost(FIXTURE_A, run_id=f'{PROTOCOL_ID}-correctness-coordinator-{suffix}',
                      blueprint=ImmutableBlueprintActionSource(source_id='review-empty'),
                      clock=clock)

baseline_clock = Clock()
baseline = host(baseline_clock, 'baseline').run()
baseline_terminal = parse_trace(baseline.trace).terminal
slow_clock = Clock()
real_add_decision = TraceBuilder.add_decision
calls = []
def slow_add_decision(builder, decision):
    slow_clock.now += 2_000_000_000
    calls.append(decision.action_index)
    return real_add_decision(builder, decision)
with patch.object(TraceBuilder, 'add_decision', slow_add_decision):
    delayed = host(slow_clock, 'slow-serialization').run()
delayed_terminal = parse_trace(delayed.trace).terminal
print(json.dumps({'probe':'serialization_accounting','injected_ns':2_000_000_000*len(calls),
    'baseline_preparation_seconds':baseline_terminal['preparation_compute_seconds'],
    'delayed_preparation_seconds':delayed_terminal['preparation_compute_seconds'],
    'baseline_post_terminal_seconds':baseline_terminal['post_terminal_compute_seconds'],
    'delayed_post_terminal_seconds':delayed_terminal['post_terminal_compute_seconds'],
    'clock_final_delta_ns':slow_clock.now-baseline_clock.now,
    'passed':delayed.receipt.passed, 'accounting_complete':delayed.receipt.accounting_complete}), flush=True)

area = Path(os.environ['TEMP']) / ('coordinator-storage-' + uuid.uuid4().hex)
area.mkdir()
root = area / 'incremental'; root.mkdir()
destination = root / 'trace.jsonl'
file_observations = []
def observe_add_decision(builder, decision):
    answer = real_add_decision(builder, decision)
    file_observations.append({'action_index':decision.action_index,
                              'destination_exists_after_serialization':destination.exists()})
    return answer
with patch.object(TraceBuilder, 'add_decision', observe_add_decision):
    outcome = host(Clock(), 'incremental').run(destination=destination, run_root=root)
print(json.dumps({'probe':'incremental_publication','observations':file_observations,
    'exists_after_run':destination.exists(),'passed':outcome.receipt.passed}), flush=True)

# Real Windows junction replacement between lexical path validation and os.open.
# All affected paths are unique fixtures underneath this diagnostic's temp area.
race_root = area / 'race-root'; race_root.mkdir()
slot = race_root / 'slot'; slot.mkdir()
parked = race_root / 'parked'
outside = area / 'outside'; outside.mkdir()
target = slot / 'escaped.jsonl'
real_open = os.open
race_applied = False
powershell = Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
def ps_quote(value): return "'" + str(value).replace("'", "''") + "'"
def race_open(path, flags, *args, **kwargs):
    global race_applied
    if Path(path) == target and not race_applied:
        race_applied = True
        slot.rename(parked)
        command = 'New-Item -ItemType Junction -Path ' + ps_quote(slot) + ' -Value ' + ps_quote(outside) + ' -ErrorAction Stop | Out-Null'
        result = subprocess.run([str(powershell), '-NoProfile', '-NonInteractive', '-Command', command], capture_output=True, text=True, env=os.environ.copy())
        if result.returncode: raise RuntimeError('junction setup failed: ' + result.stderr)
    return real_open(path, flags, *args, **kwargs)
try:
    with patch.object(os, 'open', race_open):
        returned_digest = write_trace(b'review-only\n', target, run_root=race_root)
    result = {'returned_digest':returned_digest,'exception':None}
except Exception as error:
    result = {'exception':type(error).__name__,'message':str(error)}
result.update(probe='writer_parent_junction_race',race_applied=race_applied,
    escaped_file_exists=(outside/'escaped.jsonl').exists(),
    escaped_bytes=((outside/'escaped.jsonl').read_text() if (outside/'escaped.jsonl').exists() else None),
    run_root=str(race_root),fixture_area=str(area))
print(json.dumps(result),flush=True)
