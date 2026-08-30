import ast,hashlib,json,os,subprocess
from pathlib import Path
work=Path('D:/Pontius-worktrees/codex-v0a-i01-terminal')
base='6cdf7b00dac653a9a295bbb86cdc3b5782317491'
paths=('src/pontius/v0a/trace.py','tests/test_v0a_trace.py')
git='C:/Program Files/Git/cmd/git.exe'
env={key:os.environ[key] for key in ('SYSTEMROOT','WINDIR','COMSPEC','TEMP','TMP') if key in os.environ}
def run(*args):
    return subprocess.run([git,'-c','safe.directory='+str(work),'-C',str(work),*args],
                          env=env,capture_output=True,check=True).stdout
assert run('rev-parse','HEAD').decode().strip()==base
assert set(run('diff','--name-only',base).decode().splitlines())==set(paths)
assert not run('ls-files','--others','--exclude-standard').strip()
run('diff','--check')
for path in paths:
    raw=(work/path).read_bytes()
    assert b'\r' not in raw and not raw.startswith(b'\xef\xbb\xbf')
    ast.parse(raw,filename=path)
    added=run('diff','--unified=0',base,'--',path).decode().splitlines()
    long=[line for line in added if line.startswith('+') and not line.startswith('+++')
          and len(line[1:])>100]
    print(json.dumps({'path':path,'sha256':hashlib.sha256(raw).hexdigest(),
                      'lines':len(raw.splitlines()),'added_over100':long}),flush=True)
print(run('status','--short').decode())
