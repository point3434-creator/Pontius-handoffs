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
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.no_limit_betting import raise_to
from pontius.v0a.model import ActionMailbox, HandStartedEvent
from pontius.v0a.runtime import HandRuntime
from pontius.v0a.replay import FIXTURE_A
import pontius.v0a.runtime as runtime_module
assert Path(runtime_module.__file__).resolve() == Path(snapshot, 'src/pontius/v0a/runtime.py').resolve()
class Clock:
    def __init__(self): self.now = 0
    def __call__(self):
        self.now += 1000
        return self.now
class ReboundDelegate:
    def __init__(self, source):
        self.source = source
        self.digest = source.digest
        self.entries = source.entries
    def action_for(self, **kwargs):
        selected = self.source.action_for(**kwargs)
        return replace(selected, action=raise_to(6), table_hit=True)
source = ImmutableBlueprintActionSource(source_id='cold-b-empty-anchor')
fixture = FIXTURE_A
start = HandStartedEvent(hand_id='blueprint-binding', event_index=0, button=fixture.button,
                        controlled_seat=fixture.controlled_seat,
                        starting_stacks=fixture.starting_stacks,
                        small_blind=fixture.small_blind, big_blind=fixture.big_blind,
                        private_cards=tuple(fixture.deal().hand(fixture.controlled_seat)))
mailbox = ActionMailbox()
runtime = HandRuntime(blueprint=ReboundDelegate(source), mailbox=mailbox, clock=Clock())
outcome = runtime.dispatch(start)
print(json.dumps({'probe': 'delegated_false_hit_under_empty_canonical_anchor',
                  'anchor_entries': len(source.entries), 'anchor_digest': source.digest,
                  'mailbox_accepted': len(mailbox.accepted), 'outcome': asdict(outcome)}))
assert outcome.status == 'decided' and outcome.decision.selected_action.kind == 'raise'
assert outcome.decision.blueprint_sha256 == source.digest
assert len(source.entries) == 0
