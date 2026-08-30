import hashlib, json, os, pathlib, subprocess, sys
SNAPSHOT=pathlib.Path('D:/Pontius-review-snapshots/cold-a-v0a-i01-ab-r005-20260830')
CHECKS=pathlib.Path('D:/Pontius-handoffs/v0a-i01-ab/r005/checks')
GIT='C:/Program Files/Git/cmd/git.exe'
COMMIT='6cdf7b00dac653a9a295bbb86cdc3b5782317491'
ENV={k:os.environ[k] for k in ('SYSTEMROOT','WINDIR','COMSPEC','TEMP','TMP') if k in os.environ}
ENV.update(PYTHONPATH=str(SNAPSHOT/'src'), PYTHONNOUSERSITE='1', PONTIUS_GIT=GIT)
def git(*args):
    return subprocess.run([GIT,'-c',f'safe.directory={SNAPSHOT.as_posix()}','-C',str(SNAPSHOT),*args],env=ENV,cwd=SNAPSHOT,check=True,capture_output=True).stdout
fields=git('diff-tree','--no-renames','-r','-z','--no-commit-id','--name-status',COMMIT+'^',COMMIT).decode().split('\0')
rows=[]
for i in range(0,len(fields)-1,2):
    status,path=fields[i:i+2]
    digest='0'*64 if status=='D' else hashlib.sha256(git('cat-file','blob',f'{COMMIT}:{path}')).hexdigest()
    rows.append(f'{digest}  {path}\n')
manifest=''.join(sorted(rows)).encode()
assert manifest==(CHECKS.parent/'manifest.sha256').read_bytes()
assert hashlib.sha256(manifest).hexdigest()=='83798245d9feac931479478e81c850ac4de277a2903a7523f5745320738cd21f'
identity={'commit':git('rev-parse','HEAD').decode().strip(),'parent':git('rev-parse','HEAD^').decode().strip(),'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'manifest_sha256':hashlib.sha256(manifest).hexdigest(),'rows':rows,'diff_check_exit':subprocess.run([GIT,'-C',str(SNAPSHOT),'diff','--check',COMMIT+'^',COMMIT],env=ENV,cwd=SNAPSHOT,capture_output=True).returncode,'snapshot':str(SNAPSHOT)}
(CHECKS/'cold-a-identity.json').write_text(json.dumps(identity,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(identity),flush=True)
for slot,python,version in [('311','D:/Pontius-tools/py311/Scripts/python.exe','3.11.15'),('314','D:/Pontius/.venv/Scripts/python.exe','3.14.6')]:
    receipts=[]
    payloads=sys.argv[1:] or ['tests/test_v0a_trace.py','tests/test_v0a_replay.py']
    for payload in payloads:
        prelude='import sys,os,json,platform; print(json.dumps(dict(executable=sys.executable,implementation=platform.python_implementation(),version=platform.python_version(),cwd=os.getcwd(),path=sys.path,flags=str(sys.flags),environment=dict(os.environ))),flush=True); assert platform.python_version()=='+repr(version)+'; assert sys.flags.dont_write_bytecode and sys.flags.safe_path; import pontius.v0a.trace,pontius.v0a.replay; print(json.dumps(dict(trace=pontius.v0a.trace.__file__,replay=pontius.v0a.replay.__file__)),flush=True); import runpy; runpy.run_path('+repr(str(SNAPSHOT/payload) if not pathlib.Path(payload).is_absolute() else payload)+',run_name="__main__")'
        command=[python,'-B','-P','-c',prelude]
        result=subprocess.run(command,env=ENV,cwd=SNAPSHOT,capture_output=True,text=True)
        stem=pathlib.Path(payload).stem.replace('cold-a-','')
        log=CHECKS/f'cold-a-{slot}-{stem}.txt'
        log.write_text(result.stdout+result.stderr,encoding='utf-8',newline='\n')
        receipt={'command':command,'environment':ENV,'cwd':str(SNAPSHOT),'exit':result.returncode,'log':str(log),'sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
        receipts.append(receipt)
        print(json.dumps({'slot':slot,'payload':payload,'exit':result.returncode,'log':str(log),'output_tail':(result.stdout+result.stderr)[-1800:]}),flush=True)
    name='focused' if not sys.argv[1:] else 'probes'
    (CHECKS/f'cold-a-{slot}-{name}-receipt.json').write_text(json.dumps(receipts,indent=2)+'\n',encoding='utf-8',newline='\n')
