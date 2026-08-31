from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import uuid

ROOT = Path(r'D:\Pontius-handoffs\v0a-i01-ab')
WORK = Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-callbacks')
BASE = '8d240db477b8c141e6142e055dbfbedc75c6a2f8'
GIT = r'C:\Program Files\Git\cmd\git.exe'
label, slot, phase, selection = sys.argv[1:]
assert label and all(c.isalnum() or c == '-' for c in label)
assert slot in ('311', '314') and phase in ('red', 'green')
assert selection in ('new', 'all')
assert subprocess.check_output([GIT, '-C', str(WORK), 'rev-parse', 'HEAD']).decode().strip() == BASE
parent = Path(r'D:\pontius-snapshots') / ('c-provenance-v4-' + label + '-' + slot + '-' + uuid.uuid4().hex)
parent.mkdir()
snapshot = parent / 'harness'
temporary = parent / 'temp'
temporary.mkdir()
for arguments in (
    ['-c', 'core.autocrlf=false', 'clone', '--shared', '--no-checkout', r'D:\Pontius', str(snapshot)],
    ['-C', str(snapshot), '-c', 'core.autocrlf=false', 'checkout', '--detach', BASE],
):
    subprocess.run([GIT, *arguments], capture_output=True, check=True)
paths = ('tools/generate_test_inventory.py', 'tests/test_inventory_and_profiles.py')
for path in paths:
    payload = (subprocess.check_output([GIT, '-C', str(WORK), 'show', BASE + ':' + path])
               if phase == 'red' and path == paths[0] else (WORK / path).read_bytes())
    (snapshot / path).write_bytes(payload)
hashes = {path: hashlib.sha256((snapshot / path).read_bytes()).hexdigest() for path in paths}
environment = {key: os.environ[key] for key in ('SYSTEMROOT', 'WINDIR', 'COMSPEC') if key in os.environ}
environment.update(PATH=str(Path(environment['SYSTEMROOT']) / 'System32'),
    TEMP=str(temporary), TMP=str(temporary), PYTHONPATH=str(snapshot / 'src'),
    PONTIUS_GIT=GIT, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='NUL',
    GIT_CONFIG_SYSTEM='NUL', GIT_ATTR_NOSYSTEM='1', PYTHONNOUSERSITE='1')
executable, version = ((r'D:\Pontius-tools\py311\Scripts\python.exe', '3.11.15')
                       if slot == '311' else (r'D:\Pontius\.venv\Scripts\python.exe', '3.14.6'))
payload_path = ROOT / 'c-provenance-v4-debug-payload.py'
command = [executable, '-B', '-P', str(payload_path), version, executable, selection]
result = subprocess.run(command, cwd=snapshot, env=environment, capture_output=True)
after = {path: hashlib.sha256((snapshot / path).read_bytes()).hexdigest() for path in paths}
assert hashes == after
output = (result.stdout + result.stderr).replace(b'\r\n', b'\n')
log = ROOT / ('c-provenance-v4-' + label + '-' + slot + '.txt')
with log.open('xb') as stream:
    stream.write(output)
receipt = dict(base=BASE, phase=phase, worktree=str(WORK), snapshot=str(snapshot),
    temporary=str(temporary), overlay_sha256=hashes, after_sha256=after,
    command=command, environment=environment, exit=result.returncode, log=str(log),
    log_sha256=hashlib.sha256(output).hexdigest(),
    payload_sha256=hashlib.sha256(payload_path.read_bytes()).hexdigest(),
    runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
with (ROOT / ('c-provenance-v4-' + label + '-' + slot + '-receipt.json')).open(
        'x', encoding='utf-8', newline='\n') as stream:
    json.dump(receipt, stream, indent=2)
    stream.write('\n')
print(output.decode(errors='replace')[-12000:], flush=True)
print('exit', result.returncode, 'receipt', log.with_name(log.stem + '-receipt.json'), flush=True)
raise SystemExit(result.returncode)