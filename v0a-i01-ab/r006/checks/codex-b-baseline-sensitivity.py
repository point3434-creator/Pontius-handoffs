import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

expected_executable, expected_version = sys.argv[1:3]
snapshot = Path(r'D:\Pontius-review-snapshots\codex-b-v0a-i01-ab-r005-base-c5e378a6')
assert tuple(sys.version_info[:3]) == tuple(map(int, expected_version.split('.')))
assert os.path.normcase(sys.executable) == os.path.normcase(expected_executable)
assert Path.cwd() == snapshot
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert os.environ['PYTHONPATH'] == str(snapshot/'src')
git = Path(os.environ['PONTIUS_GIT'])
assert str(git) == r'C:\Program Files\Git\cmd\git.exe'
info = git.lstat()
assert stat.S_ISREG(info.st_mode) and not info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
assert set(os.environ) <= {'SYSTEMROOT','WINDIR','COMSPEC','TEMP','TMP','PYTHONPATH','PONTIUS_GIT','PYTHONNOUSERSITE'}
def run(*args):
    return subprocess.run([str(git),'-c','safe.directory='+str(snapshot),'-C',str(snapshot),
                           *args], check=True,capture_output=True).stdout
base = '6cdf7b00dac653a9a295bbb86cdc3b5782317491'
assert run('rev-parse','HEAD').strip().decode() == base
assert run('status','--porcelain') == b''

from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.model import ActionMailbox
from pontius.v0a.replay import FIXTURE_A, PROTOCOL_ID, ReplayHost
import pontius.v0a.trace as trace
assert Path(trace.__file__) == snapshot/'src/pontius/v0a/trace.py'
class Clock:
    def __init__(self):
        self.now = 100_000
        self.invalid = False
    def __call__(self):
        if self.invalid:
            return False
        self.now += 10_000
        return self.now

def rows(kind):
    source = Clock()
    mailbox = ActionMailbox()
    class Adapter:
        def deliver(self, envelope):
            receipt = mailbox.deliver(envelope)
            if kind=='interrupted':
                source.invalid = True
            elif kind=='late':
                source.now += 16_000_000_000
            return receipt
    outcome = ReplayHost(FIXTURE_A, run_id=PROTOCOL_ID+'-correctness-codex-b-base-'+kind,
                blueprint=ImmutableBlueprintActionSource('codex-b-base'),clock=source,
                mailbox=Adapter()).run()
    trace.parse_trace(outcome.trace)
    return [json.loads(row) for row in outcome.trace.splitlines()]

def dump(value):
    return json.dumps(value, sort_keys=True,separators=(',',':'),allow_nan=False).encode()
keys = ('hand_id','event_index','action_index','street_action_index','seat','street',
        'state_before_sha256','state_after_sha256','visible_cards_sha256','blueprint_sha256',
        'selected_action','selection_reason','spine_reason','preparation_use')
def bind(values):
    payload = {'events':[row['event'] for row in values if row['record_type']=='event'],
               'decisions':[{key:row[key] for key in keys}
                            for row in values if row['record_type']=='decision'],
               'settlement':values[-1]['settlement']}
    values[-1]['semantic_sha256']=hashlib.sha256(dump(payload)).hexdigest()
    prefix=b''.join(dump(row)+b'\n' for row in values[:-1])
    values[-1]['trace_prefix_sha256']=hashlib.sha256(prefix).hexdigest()
    return prefix+dump(values[-1])+b'\n'

success, interrupted, late = rows('success'), rows('interrupted'), rows('late')
cases=[]
mutated=copy.deepcopy(interrupted)
mutated[-1].update(complete=True,accounting_complete=True,
                  preparation_compute_seconds=0.0,post_terminal_compute_seconds=0.0)
cases.append(('interrupted_claims_complete',mutated))
mutated=copy.deepcopy(late)
mutated[-1]['settlement']=success[-1]['settlement']
cases.append(('failed_settlement',mutated))
mutated=copy.deepcopy(late)
mutated[-1].update(accounting_complete=True,preparation_compute_seconds=None)
cases.append(('missing_complete_total',mutated))
for label, reason in (('erased_primary',None),('replaced_primary','invalid_event')):
    mutated=copy.deepcopy(late)
    mutated[-1]['failure_reason']=reason
    cases.append((label,mutated))
mutated=copy.deepcopy(success)
mutated[1]['event']['private_cards'].reverse()
cases.append(('descending_private_cards',mutated))
for label, values in cases:
    trace.parse_trace(bind(values))
print(json.dumps({'base':base,'executable':sys.executable,'version':sys.version,
                  'cwd':str(snapshot),'module':trace.__file__,
                  'baseline_admits_invalid_cases':[label for label,_ in cases],
                  'count':len(cases),'result':'EXPECTED_BASE_DEFECTS_REPRODUCED'},indent=2))
