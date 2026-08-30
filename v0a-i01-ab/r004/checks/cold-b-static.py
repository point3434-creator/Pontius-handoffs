import json, os, pathlib, platform, subprocess, sys
root=pathlib.Path.cwd()
assert platform.python_version()==os.environ['COLD_B_EXPECTED_VERSION']=='3.11.15'
git=os.environ['PONTIUS_GIT']
base='30df7bce8da51715e6f1d7576892dd689421c516'
commit='c6adbcaa048988361d2388970eaca772711b797b'
def run(*args):
 return subprocess.run([git,'-C',str(root),*args],check=True,capture_output=True).stdout
print(run('diff','--no-ext-diff',base,commit,'--','src/pontius/v0a/model.py','src/pontius/v0a/runtime.py').decode())
print('DIFF_CHECK',run('diff','--check',base,commit).decode())
for path in ('src/pontius/v0a/model.py','src/pontius/v0a/runtime.py','tests/test_v0a_hand_replay.py'):
 data=run('cat-file','blob',commit+':'+path)
 old=run('cat-file','blob',base+':'+path)
 lines=data.decode().splitlines()
 oldlong={line for line in old.decode().splitlines() if len(line)>100}
 print(json.dumps({'path':path,'BOM':data.startswith(b'\xef\xbb\xbf'),'CR':b'\r' in data,
                  'trailing_whitespace':[i for i,line in enumerate(lines,1) if line.rstrip()!=line],
                  'new_over_100_columns':[(i,len(line)) for i,line in enumerate(lines,1)
                                          if len(line)>100 and line not in oldlong]}))
print('STATUS',run('status','--porcelain=v1').decode())
