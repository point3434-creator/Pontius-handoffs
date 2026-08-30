"""Read-only publication audit of r002 identity, reviews and receipts."""
import hashlib, json, os, subprocess
from pathlib import Path
packet=Path('D:/Pontius-handoffs/v0a-i01-impl/r002')
repo=Path('D:/Pontius'); git='C:/Program Files/Git/cmd/git.exe'
meta=json.loads((packet/'candidate.json').read_bytes())
assert set(meta)=={'schema_version','task_id','round','ref','commit','base','tree','manifest_sha256','date'}
assert meta['commit']=='18c965d1f3445c253a6333c4d10899c1dcac0cc6'
assert meta['manifest_sha256']=='4cfd14ac7bfdb22e052bb9f625610657c01aafa07182acf58d19367a8816cb18'
env={key:os.environ[key] for key in ('SystemRoot','WINDIR','ComSpec','TEMP','TMP') if key in os.environ}
env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='NUL',GIT_NO_REPLACE_OBJECTS='1',GIT_LITERAL_PATHSPECS='1')
def g(at,*args):
    return subprocess.check_output([git,'-C',str(at),*args],env=env)
assert g(repo,'rev-parse',meta['ref']).decode().strip()==meta['commit']
assert g(repo,'rev-parse',meta['commit']+'^').decode().strip()==meta['base']
assert g(repo,'rev-parse',meta['commit']+'^{tree}').decode().strip()==meta['tree']
paths=g(repo,'diff-tree','-r','--no-commit-id','--no-renames','--name-only',meta['base'],meta['commit']).decode().splitlines()
rows=sorted(hashlib.sha256(g(repo,'cat-file','blob',meta['commit']+':'+p)).hexdigest()+'  '+p+'\n' for p in paths)
manifest=''.join(rows).encode()
assert manifest==(packet/'manifest.sha256').read_bytes()
assert hashlib.sha256(manifest).hexdigest()==meta['manifest_sha256']
assert len(paths)==10
for path in ('src/pontius/v0a/__init__.py','tests/test_v0a_hand_replay.py'):
    assert not g(repo,'diff','2d059f90fb6cec27e4090ad0432c68759a760960',meta['commit'],'--',path)
reports={}
for name in ('review-01-codex-a.md','review-02-codex-b.md','review-03-codex-coordinator.md'):
    data=(packet/'reviews'/name).read_bytes()
    assert b'\r' not in data and not data.startswith(b'\xef\xbb\xbf')
    assert meta['commit'].encode() in data and meta['manifest_sha256'].encode() in data
    assert b'NOT CLEAN' in data
    reports[name]=hashlib.sha256(data).hexdigest()
assert reports['review-02-codex-b.md']=='5a6f6fe73aaf3c9cddca718658d21fb40e78fa1c37d4edcfd9a9bbf22fb1b6d0'
slots=[]
for label,version in [('codex-py311',[3,11,15]),('codex-py314',[3,14,6])]:
    receipt=json.loads((packet/'checks'/f'{label}-verification.json').read_bytes())
    assert receipt['candidate']==meta['commit'] and receipt['manifest_sha256']==meta['manifest_sha256']
    assert receipt['identity']['version']==version
    assert all(result['exit']==0 for result in receipt['results']) and len(receipt['results'])==4
    for result,count in zip(receipt['results'],[36,25,20,18]):
        log=Path(result['log']).read_text()
        assert f'Ran {count} tests' in log and '\nOK\n' in log
    snap=Path(receipt['snapshot'])
    for row in rows:
        digest,path=row.rstrip('\n').split('  ',1)
        assert hashlib.sha256((snap/path).read_bytes()).hexdigest()==digest
    assert not g(snap,'status','--porcelain')
    slots.append({'version':version,'tests':99,'snapshot_source_pristine':True})
ledger=(packet.parent/'progress.md').read_text()
for marker in ('Codex coordinator /root (additional pass, not cold)','Codex A','Codex B'):
    matched=[line for line in ledger.splitlines() if marker in line and meta['commit'] in line]
    assert len(matched)==1,(marker,matched)
program=(packet.parents[1]/'progress.md').read_text()
assert sum('v0a-i01-impl/r002 |' in line for line in program.splitlines())==1
assert 'ten consolidated Important findings' in (packet/'disposition.md').read_text()
result={'candidate':meta['commit'],'manifest_sha256':meta['manifest_sha256'],'changed_paths':10,
        'report_sha256':reports,'slots':slots,'task_verdicts_once_per_issuer':True,
        'program_dispositions':1,'primary_head':g(repo,'rev-parse','HEAD').decode().strip(),
        'primary_status':g(repo,'status','--porcelain').decode().splitlines(),
        'scope':'Review publication only; no implementation integration'}
with (packet/'checks/codex-publication-audit.json').open('x',encoding='utf-8',newline='\n') as file:
    json.dump(result,file,indent=2); file.write('\n')
print(json.dumps(result))
