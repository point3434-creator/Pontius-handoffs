"""One two-caller rehearsal in the declared detached snapshot; never retained mode."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

PK = Path('D:/Pontius-handoffs/v0a-eval-panel-completion/export-run-20260910-r001')
SNAP = Path('D:/Pontius-worktrees/eval-panel-export-rehearsal-20260910')
RETAINED = Path('D:/Pontius-worktrees/eval-panel-export-20260910')
GIT = 'C:/Program Files/Git/cmd/git.exe'
BASH = 'C:/Program Files/Git/bin/bash.exe'
SOURCE = '1c7067448106cfa2aca3d57be879842d72293c61'
assert sys.version_info[:3] == (3, 14, 6)
assert SNAP.resolve() != RETAINED.resolve()
assert not (PK / 'authorization.md').exists() and not (PK / 'invocations').exists()
assert not (PK / 'rehearsal').exists()
git = [GIT, '-c', f'safe.directory={SNAP.as_posix()}', '-C', str(SNAP)]
assert subprocess.check_output(git + ['rev-parse', 'HEAD']).decode().strip() == SOURCE
assert subprocess.run(git + ['symbolic-ref', '-q', 'HEAD'], capture_output=True).returncode == 1
env = dict(os.environ)
for key in ('BASH_ENV', 'ENV', 'REHEARSAL', 'REHEARSAL_PK', 'EXPORT_ROOT'):
    env.pop(key, None)
env.update(REHEARSAL='1', EXPORT_ROOT=SNAP.as_posix())
checks = PK / 'checks'; checks.mkdir(exist_ok=True)
command = [BASH, '--noprofile', '--norc', str(PK / 'invoke.sh')]
rows_before = len((SNAP / 'execution_journal.jsonl').read_bytes().splitlines())
started = time.time()
with (checks / 'race-caller-a.txt').open('xb') as a, (checks / 'race-caller-b.txt').open('xb') as b:
    first = subprocess.Popen(command, stdout=a, stderr=subprocess.STDOUT, env=env)
    second = subprocess.Popen(command, stdout=b, stderr=subprocess.STDOUT, env=env)
    statuses = [first.wait(timeout=650), second.wait(timeout=650)]
elapsed = time.time() - started
captures = list((PK / 'rehearsal').rglob('export-stdout.json'))
observed = dict(statuses=statuses, stdout_pathnames=len(captures), wall_seconds=elapsed,
                command=command, environment=dict(REHEARSAL='1', EXPORT_ROOT=SNAP.as_posix()))
(checks / 'race-observed.json').write_text(json.dumps(observed, indent=2) + '\n', newline='\n')
assert sorted(statuses) == [0, 97], observed
assert len(captures) == 1, observed
row = json.loads((PK / 'rehearsal/export-journal-row.jsonl').read_bytes())
result_path = SNAP / row['output']
raw = result_path.read_bytes()
assert hashlib.sha256(raw).hexdigest() == row['output_sha256']
result = json.loads(raw)
assert result['phase'] == 'export' and result['status'] == 'completed'
assert all(result[key] is True for key in ('phase_complete', 'cleanup_verified'))
assert row['source_verified'] is True and row['source_commit'] == SOURCE
assert len((SNAP / 'execution_journal.jsonl').read_bytes().splitlines()) == rows_before + 1
assert not (PK / 'invocations').exists()
for name in ('result.json', 'runtimes.json', 'teacher.json', 'blueprint.json'):
    (PK / 'rehearsal' / name).write_bytes((result_path.parent / name).read_bytes())
print(json.dumps(dict(statuses=statuses, wall_seconds=elapsed, result=str(result_path),
                     fields=list(result), observations=result['observations'][:2])))
