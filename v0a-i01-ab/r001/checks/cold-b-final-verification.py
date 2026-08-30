import sys
assert sys.implementation.name == 'cpython' and sys.version_info[:3] == (3,11,15)
import collections, hashlib, json, os, pathlib, subprocess
checks=pathlib.Path(r'D:\Pontius-handoffs\v0a-i01-ab\r001\checks')
packet=checks.parent
identity=json.loads((checks/'cold-b-identity.json').read_text())
root=pathlib.Path(identity['snapshot']).resolve()
GIT=r'C:\Program Files\Git\cmd\git.exe'
env={k:os.environ[k] for k in ('SYSTEMROOT','WINDIR','COMSPEC','TEMP','TMP') if k in os.environ}
def git(*args):
    return subprocess.run([GIT,'-C',str(root),*args],capture_output=True,check=True,env=env).stdout
assert git('rev-parse','HEAD').decode().strip()==identity['candidate']['commit']
assert git('status','--porcelain')==b''
manifest=(packet/'manifest.sha256').read_bytes()
assert hashlib.sha256(manifest).hexdigest()==identity['candidate']['manifest_sha256']
for row in manifest.decode().splitlines():
    digest,path=row.split('  ',1)
    blob=git('cat-file','blob',identity['candidate']['commit']+':'+path)
    assert hashlib.sha256(blob).hexdigest()==digest
    assert (root/path).read_bytes()==blob
assert hashlib.sha256((packet/'coverage.md').read_bytes()).hexdigest()=='e74a65f6ad1d33816b36bc69d7ba6936d61a078b3b6dc429e81ae901ec633b9f'
summary={}
for slot in ('311','314'):
    focused=json.loads((checks/('cold-b-v2-focused-'+slot+'.json')).read_text())
    assert all(row['exit']==0 for row in focused['results'])
    diagnostic=json.loads((checks/('cold-b-v3-diagnostic-'+slot+'.json')).read_text())
    assert all(row['exit']==0 for row in diagnostic['results'])
    schedule=json.loads((checks/('cold-b-independent-v2-'+slot+'.json')).read_text())
    assert schedule['failed']==0 and schedule['cases']==1964
    categories=collections.Counter(row['label'].split('/')[0] for row in schedule['rows'])
    summary[slot]={'focused_exit':0,'focused_suites':4,'independent_cases':1964,'categories':dict(categories)}
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(checks.glob('cold-b-*')) if p.is_file()}
result={'candidate':identity['candidate'],'snapshot':str(root),'status':'clean','source_blob_equality':True,'coverage_sha256':'e74a65f6ad1d33816b36bc69d7ba6936d61a078b3b6dc429e81ae901ec633b9f','summary':summary,'sha256':hashes}
with (checks/'cold-b-final-verification.json').open('x',encoding='utf-8',newline='\n') as f:
    json.dump(result,f,indent=2); f.write('\n')
print(json.dumps(result,indent=2))
