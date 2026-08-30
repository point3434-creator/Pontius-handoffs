import sys
assert sys.implementation.name == 'cpython'
assert sys.version_info[:3] == (3, 11, 15), sys.version
import hashlib, json, os, pathlib, stat, subprocess, uuid
GIT = pathlib.Path(r'C:\Program Files\Git\cmd\git.exe')
OWNER = pathlib.Path(r'D:\Pontius')
PACKET = pathlib.Path(r'D:\Pontius-handoffs\v0a-i01-ab\r001')
assert GIT.is_file() and not (GIT.stat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
env = {k: os.environ[k] for k in ('SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP', 'COMSPEC') if k in os.environ}
env.update({'PONTIUS_GIT': str(GIT), 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONNOUSERSITE': '1'})
def git(root, *args):
    return subprocess.run([str(GIT), '-C', str(root), *args], env=env, check=True, capture_output=True).stdout
candidate = json.loads((PACKET / 'candidate.json').read_text())
commit = candidate['commit']
assert git(OWNER, 'rev-parse', candidate['ref']).decode().strip() == commit
assert git(OWNER, 'rev-parse', commit + '^').decode().strip() == candidate['base']
assert git(OWNER, 'rev-parse', commit + '^{tree}').decode().strip() == candidate['tree']
fields = git(OWNER, 'diff-tree', '-r', '-z', '--no-renames', '--no-commit-id', '--name-status', commit + '^', commit).decode().split('\0')
rows = []
for i in range(0, len(fields)-1, 2):
    status, path = fields[i:i+2]
    digest = '0'*64 if status == 'D' else hashlib.sha256(git(OWNER, 'cat-file', 'blob', commit+':'+path)).hexdigest()
    rows.append((digest+'  '+path+'\n').encode())
manifest = b''.join(sorted(rows))
assert manifest == (PACKET/'manifest.sha256').read_bytes()
assert hashlib.sha256(manifest).hexdigest() == candidate['manifest_sha256']
assert len(rows) == 4
snapshot = pathlib.Path(r'D:\Pontius-snapshots') / ('cold-b-ab-r001-' + uuid.uuid4().hex)
snapshot.parent.mkdir(exist_ok=True)
subprocess.run([str(GIT), 'clone', '--local', '--no-hardlinks', '--no-checkout', str(OWNER), str(snapshot)], env=env, check=True, capture_output=True)
git(snapshot, '-c', 'core.autocrlf=false', 'checkout', '--detach', commit)
assert git(snapshot, 'rev-parse', 'HEAD').decode().strip() == commit
assert not git(snapshot, 'status', '--porcelain')
for row in rows:
    digest, path = row.decode().rstrip('\n').split('  ', 1)
    assert hashlib.sha256((snapshot/path).read_bytes()).hexdigest() == digest
receipt = {'candidate':candidate,'snapshot':str(snapshot),'python':sys.version,'executable':sys.executable,'git':str(GIT),'manifest_recomputed':hashlib.sha256(manifest).hexdigest(),'manifest_rows':len(rows),'status':'clean','env':env}
with (PACKET/'checks'/'cold-b-identity.json').open('x', encoding='utf-8', newline='\n') as f:
    json.dump(receipt,f,indent=2); f.write('\n')
print(json.dumps(receipt,indent=2))
