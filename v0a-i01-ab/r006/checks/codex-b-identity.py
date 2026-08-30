import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

snapshot = Path(r"D:\Pontius-review-snapshots\codex-b-v0a-i01-ab-r006-2fddbb63")
packet = Path(r"D:\Pontius-handoffs\v0a-i01-ab\r006")
expected_executable, expected_version = sys.argv[1:3]
assert tuple(sys.version_info[:3]) == tuple(map(int, expected_version.split('.')))
assert os.path.normcase(sys.executable) == os.path.normcase(expected_executable)
assert Path.cwd() == snapshot
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert os.environ['PYTHONPATH'] == str(snapshot / 'src')
git = Path(os.environ['PONTIUS_GIT'])
assert str(git) == r'C:\Program Files\Git\cmd\git.exe'
info = git.lstat()
assert stat.S_ISREG(info.st_mode)
assert not info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
assert set(os.environ) <= {'SYSTEMROOT', 'WINDIR', 'COMSPEC', 'TEMP', 'TMP', 'PYTHONPATH', 'PONTIUS_GIT', 'PYTHONNOUSERSITE'}
def run(*args):
    return subprocess.run([str(git), '-c', 'safe.directory=' + str(snapshot), '-C',
                           str(snapshot), *args], check=True, capture_output=True).stdout
candidate = json.loads((packet / 'candidate.json').read_bytes())
commit = candidate['commit']
assert run('rev-parse', 'HEAD').strip().decode() == commit
assert run('rev-parse', commit + '^').strip().decode() == candidate['base']
assert run('rev-parse', commit + '^{tree}').strip().decode() == candidate['tree']
assert run('status', '--porcelain') == b''
fields = run('diff-tree', '--no-renames', '-r', '-z', '--no-commit-id', '--name-status',
             commit + '^', commit).decode().split('\0')
rows = []
blobs = []
for index in range(0, len(fields)-1, 2):
    status, path = fields[index:index+2]
    blob = run('cat-file', 'blob', f'{commit}:{path}')
    digest = hashlib.sha256(blob).hexdigest()
    rows.append(f'{digest}  {path}\n')
    blobs.append({'path':path, 'status':status, 'sha256':digest, 'cr_bytes':blob.count(b'\r'),
                  'bom':blob.startswith(b'\xef\xbb\xbf'),
                  'over_100_lines':[n for n,line in enumerate(blob.splitlines(),1) if len(line)>100],
                  'trailing_whitespace_lines':[n for n,line in enumerate(blob.splitlines(),1) if line.rstrip()!=line]})
assert {row['path'] for row in blobs} == {'src/pontius/v0a/trace.py', 'tests/test_v0a_trace.py'}
row_bytes = ''.join(sorted(rows)).encode()
manifest = hashlib.sha256(row_bytes).hexdigest()
assert manifest == candidate['manifest_sha256'] == '7e1575b18c7a9cf0c74bd956a54e899aad670349d198d7863ae1f67463583d7a'
assert row_bytes == (packet / 'manifest.sha256').read_bytes()
import pontius.v0a.trace as trace
assert Path(trace.__file__) == snapshot / 'src' / 'pontius' / 'v0a' / 'trace.py'
print(json.dumps({'executable':sys.executable, 'version':sys.version,
 'cwd':str(Path.cwd()), 'flags':{'B':bool(sys.flags.dont_write_bytecode),'P':bool(sys.flags.safe_path)},
 'environment':dict(os.environ),'sys_path':sys.path,'trace_module':trace.__file__,
 'candidate':candidate,'manifest_sha256':manifest,'manifest_rows':rows,'blobs':blobs}, indent=2))
