"""Create-only terminal-parser focused receipts from fresh D-local snapshots."""
import hashlib
import json
import os
import stat
import subprocess
import sys
import uuid
from pathlib import Path

GIT = 'C:/Program Files/Git/cmd/git.exe'
ROOT = Path('D:/Pontius-handoffs/v0a-i01-ab')
WORK = Path('D:/Pontius-worktrees/codex-v0a-i01-terminal')
BASE = '6cdf7b00dac653a9a295bbb86cdc3b5782317491'
PATHS = ('src/pontius/v0a/trace.py', 'tests/test_v0a_trace.py')
label, slot, scope = sys.argv[1:]
assert slot in ('311', '314') and scope in ('baseline', 'regressions', 'full')
exe, version = (('D:/Pontius-tools/py311/Scripts/python.exe', '3.11.15')
                if slot == '311' else ('D:/Pontius/.venv/Scripts/python.exe', '3.14.6'))
assert Path(GIT).is_file() and not (Path(GIT).stat().st_file_attributes
                                  & stat.FILE_ATTRIBUTE_REPARSE_POINT)
base_env = {key: os.environ[key] for key in ('SYSTEMROOT', 'WINDIR', 'COMSPEC', 'TEMP', 'TMP')
            if key in os.environ}
def git(where, *args):
    return subprocess.run([GIT, '-c', 'safe.directory=' + str(where), '-C', str(where), *args],
                          env=base_env, capture_output=True, check=True).stdout
assert git(WORK, 'rev-parse', 'HEAD').decode().strip() == BASE
changed = git(WORK, 'diff', '--name-only', BASE).decode().splitlines()
assert set(changed) <= set(PATHS), changed
assert not git(WORK, 'ls-files', '--others', '--exclude-standard').strip()
checks = ROOT / 'terminal-checks'
checks.mkdir(exist_ok=True)
receipt_path = checks / (label + '-' + slot + '-receipt.json')
assert not receipt_path.exists()
snapshot = Path('D:/pontius-snapshots') / ('ab-terminal-' + label + '-' + uuid.uuid4().hex) / 'harness'
snapshot.parent.mkdir()
subprocess.run([GIT, 'clone', '--shared', '--no-checkout', 'D:/Pontius', str(snapshot)],
               env=base_env, capture_output=True, check=True)
git(snapshot, 'checkout', '--detach', BASE)
assert git(snapshot, 'rev-parse', 'HEAD').decode().strip() == BASE
paths = (() if scope == 'baseline' else ('tests/test_v0a_trace.py',)
         if label.startswith('red') else PATHS)
for name in paths:
    (snapshot / name).write_bytes((WORK / name).read_bytes())
hashes = {name: hashlib.sha256((snapshot / name).read_bytes()).hexdigest() for name in PATHS}
env = dict(base_env, PYTHONPATH=str(snapshot / 'src'), PYTHONNOUSERSITE='1', PONTIUS_GIT=GIT)
wrapper = '''import json,os,platform,runpy,sys
from pathlib import Path
exe,version,snapshot,target,*tests=sys.argv[1:]
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert platform.python_version()==version and sys.implementation.name=='cpython'
assert sys.flags.safe_path and sys.flags.dont_write_bytecode and sys.flags.no_user_site
assert Path.cwd()==Path(snapshot) and os.environ['PYTHONPATH']==str(Path(snapshot)/'src')
print(json.dumps({'identity_before_payload_import':dict(executable=sys.executable,
    version=sys.version,cwd=os.getcwd(),flags=str(sys.flags))}),flush=True)
import pontius.v0a.trace as trace
assert Path(trace.__file__).resolve()==Path(snapshot,'src/pontius/v0a/trace.py').resolve()
print(json.dumps({'trace_module':trace.__file__}),flush=True)
sys.argv=[target,*tests]
runpy.run_path(target,run_name='__main__')
'''
suites = (('test_v0a_trace.py', ['TerminalAdmissionTests', 'EventConstructorAdmissionTests']),) \
         if scope == 'regressions' else tuple((name, []) for name in (
             'test_v0a_hand_replay.py', 'test_v0a_trace.py',
             'test_v0a_replay.py', 'test_v0a_contract_faults.py'))
receipt = dict(label=label,slot=slot,scope=scope,base=BASE,snapshot=str(snapshot),
               worktree=str(WORK),allowed_paths=PATHS,overlaid_paths=paths,
               executed_file_sha256=hashes,environment=env,results=[])
for name, tests in suites:
    command=[exe,'-B','-P','-c',wrapper,exe,version,str(snapshot),'tests/'+name,*tests]
    result=subprocess.run(command,cwd=snapshot,env=env,capture_output=True)
    data=(result.stdout+result.stderr).replace(b'\r\n',b'\n')
    log=checks/(label+'-'+slot+'-'+Path(name).stem+'.txt')
    with log.open('xb') as file:file.write(data)
    receipt['results'].append(dict(command=command,exit=result.returncode,log=str(log),
                                  sha256=hashlib.sha256(data).hexdigest()))
    print(name,'exit',result.returncode,data.decode(errors='replace')[-1300:],flush=True)
assert all(hashlib.sha256((snapshot/name).read_bytes()).hexdigest()==digest
           for name,digest in hashes.items())
receipt['executed_bytes_unchanged']=True
with receipt_path.open('x',encoding='utf-8',newline='\n') as file:
    json.dump(receipt,file,indent=2);file.write('\n')
print('receipt',receipt_path,flush=True)
raise SystemExit(any(item['exit'] for item in receipt['results']))
