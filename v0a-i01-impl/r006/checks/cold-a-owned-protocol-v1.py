import sys
expected_executable, expected_version = sys.argv[1:3]
print('executable=' + sys.executable, flush=True)
print('implementation=' + sys.implementation.name, flush=True)
print('full_version=' + sys.version, flush=True)
assert sys.executable.lower().replace('/', '\\') == expected_executable.lower().replace('/', '\\')
assert sys.implementation.name == 'cpython'
assert '.'.join(map(str, sys.version_info[:3])) == expected_version
assert sys.version_info.releaselevel == 'final' and sys.version_info.serial == 0
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import traceback
import types
SNAPSHOT = Path(r'D:\pontius-snapshots\v0a-r006-cold-a-98fee7dce06d4fcca2da4475c550b928\harness')
GIT = r'C:\Program Files\Git\cmd\git.exe'
BASE = 'a8582e6d6b53b55415dab79c4a54e252d00b74ad'
CURRENT = 'c74b80628a89938ca585ef3240b5c267a7174d0f'
assert Path.cwd() == SNAPSHOT
assert os.environ['PYTHONPATH'] == str(SNAPSHOT / 'src')
assert os.environ['PONTIUS_GIT'] == GIT
print('environment=' + json.dumps(dict(os.environ), sort_keys=True))
def blob(commit, name):
    return subprocess.run([GIT, 'cat-file', 'blob', commit + ':src/pontius/v0a/' + name + '.py'], check=True, capture_output=True).stdout
for name in ('__init__', 'clock', 'model', 'trace'):
    assert blob(BASE, name) == blob(CURRENT, name)
    assert (SNAPSHOT / 'src' / 'pontius' / 'v0a' / (name + '.py')).read_bytes().replace(b'\r\n', b'\n') == blob(CURRENT, name)
# A read-only counterfactual, not an r005 acceptance run: load exact r005
# runtime/replay blobs under a separate package, with unchanged siblings.
# No production, test or configuration file is written or edited.
import pontius
from pontius.holdem_cards import SixSeatHoldemDeal
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
prefix = 'pontius.cold_a_r005_v0a'
package = types.ModuleType(prefix)
package.__path__ = [str(SNAPSHOT / 'src' / 'pontius' / 'v0a')]
package.__package__ = prefix
sys.modules[prefix] = package
for name in ('runtime', 'replay'):
    source = blob(BASE, name)
    full_name = prefix + '.' + name
    module = types.ModuleType(full_name)
    module.__package__ = prefix
    module.__file__ = 'git:' + BASE + ':src/pontius/v0a/' + name + '.py'
    sys.modules[full_name] = module
    exec(compile(source, module.__file__, 'exec'), module.__dict__)
    print('baseline_blob=' + name + ':' + hashlib.sha256(source).hexdigest())

class ClockSource:
    def __init__(self):
        self.now = 1_000
    def __call__(self):
        value = self.now
        self.now += 1_000
        return value

observations = []
for label, prefix in (('r005-blob-counterfactual', 'pontius.cold_a_r005_v0a'), ('r006-candidate', 'pontius.v0a')):
    replay = importlib.import_module(prefix + '.replay')
    for hostile_message in (False, True):
        rendering = []
        class Message:
            def __str__(self):
                rendering.append('attempt')
                raise RuntimeError('secondary exception while rendering original error')
        body_error = ValueError(Message() if hostile_message else 'ordinary body failure')
        host = replay.ReplayHost(replay.FIXTURE_A,
            run_id=replay.PROTOCOL_ID + '-correctness-cold-a-owned-protocol',
            blueprint=ImmutableBlueprintActionSource(source_id='cold-a-owned-protocol'),
            clock=ClockSource())
        evaluations = [0]
        def schedule(frame, event, arg):
            if event == 'call' and frame.f_code is SixSeatHoldemDeal.showdown_strengths.__code__:
                evaluations[0] += 1
                if evaluations[0] == 2:
                    raise body_error
            return schedule
        outcome = None
        escaped = None
        stack = []
        try:
            sys.settrace(schedule)
            outcome = host.run()
        except BaseException as error:
            escaped = type(error).__name__
            stack = traceback.format_tb(error.__traceback__)
        finally:
            sys.settrace(None)
        observation = {'candidate': label, 'hostile_message': hostile_message,
            'rendering_attempts': len(rendering), 'evaluations': evaluations[0],
            'escaped_type': escaped, 'accepted_actions': len(host.mailbox.accepted),
            'journal': host.runtime.closure_failures,
            'receipt': None if outcome is None else {'passed': outcome.receipt.passed,
                'primary': outcome.receipt.failure_reason, 'secondary': outcome.receipt.secondary_failures},
            'traceback': stack}
        observations.append(observation)
        print(json.dumps(observation, sort_keys=True), flush=True)
        assert evaluations[0] == 2 and len(host.mailbox.accepted) == 4
        if label == 'r006-candidate' and hostile_message:
            assert escaped == 'RuntimeError' and outcome is None and len(rendering) == 1
            assert tuple(host.runtime.closure_failures) == ('settlement_mismatch',)
        else:
            assert escaped is None and outcome.receipt.failure_reason == 'settlement_mismatch'
            assert not outcome.receipt.passed and len(rendering) == 0
print('REGRESSION CONFIRMED: r005 contains both body errors; r006 contains ordinary error but leaks the formatting error')
