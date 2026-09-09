"""Capture the final external review; no experiment or runtime invocation."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time

REPORT = Path('D:/Pontius-worktrees/v0a-increment-1-preregistration-review')
ROOT = Path('D:/pontius-snapshots/v0a-prereg-r2-py311-59b9ff051a7e4526ab924cde29ec1dce/harness')
EXE = Path('C:/Users/point/AppData/Local/Programs/coderabbit/coderabbit.exe')
GIT = 'C:/Program Files/Git/cmd/git.exe'
CANDIDATE = '119411fda2376d61d9ff310bada71f25aa64de70'
BASE = 'ca0b2e41bbf5d9fc1649de20379299331de6591a'
MANIFEST = 'da3c4ad5290a49f9d6e600b61e3190047ca6221394a4fc4ad06e40af727d799c'

def git(*args):
    return subprocess.run([GIT, '-C', str(ROOT), *args], check=True,
                          capture_output=True).stdout.decode().strip()

if git('rev-parse', 'HEAD') != CANDIDATE or git('status', '--porcelain'):
    raise RuntimeError('review snapshot is not the clean frozen candidate')
argv = [str(EXE), 'review', '--agent', '--committed', '--base-commit', BASE,
        '-c', 'CLAUDE.md', 'docs/workflow.md', 'docs/briefs/v0a-increment-1-brief.md']
start = time.monotonic()
started_at = datetime.now(timezone.utc).isoformat()
with (REPORT / 'r2-coderabbit.ndjson').open('x', encoding='utf-8', newline='\n') as log:
    proc = subprocess.Popen(argv, cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                            errors='replace')
    for line in proc.stdout:
        log.write(line)
        log.flush()
        print(line, end='', flush=True)
    code = proc.wait()
receipt = dict(candidate=CANDIDATE, base=BASE, manifest_sha256=MANIFEST,
               cwd=str(ROOT), argv=argv, executable_sha256=hashlib.sha256(EXE.read_bytes()).hexdigest(),
               started_at=started_at, elapsed_seconds=time.monotonic() - start,
               exit_code=code, final_head=git('rev-parse', 'HEAD'),
               final_status=git('status', '--porcelain'))
(REPORT / 'r2-coderabbit-receipt.json').write_text(
    json.dumps(receipt, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps(receipt), flush=True)
raise SystemExit(code)
