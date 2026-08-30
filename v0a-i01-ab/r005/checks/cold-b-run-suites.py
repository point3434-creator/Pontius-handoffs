import hashlib, json, os, pathlib, subprocess, sys, time
snapshot = pathlib.Path(sys.argv[1]).resolve()
packet = pathlib.Path('D:/Pontius-handoffs/v0a-i01-ab/r005')
checks = packet / 'checks'
git = 'C:/Program Files/Git/cmd/git.exe'
commit = '6cdf7b00dac653a9a295bbb86cdc3b5782317491'
expected_manifest = '83798245d9feac931479478e81c850ac4de277a2903a7523f5745320738cd21f'
env = {k: os.environ[k] for k in ('SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP') if k in os.environ}
env.update(PONTIUS_GIT=git, PYTHONPATH=str(snapshot / 'src'), PYTHONDONTWRITEBYTECODE='1',
           PYTHONNOUSERSITE='1', PYTHONUTF8='1')
os.environ.clear()
os.environ.update(env)
os.chdir(snapshot)
def run(argv):
    return subprocess.run(argv, cwd=snapshot, env=env, capture_output=True, check=True).stdout
def git_run(*args):
    return run([git, '-C', str(snapshot), *args])
assert git_run('rev-parse', 'HEAD').decode().strip() == commit
fields = git_run('diff-tree', '-r', '-z', '--no-commit-id', '--no-renames', '--name-status',
                 commit + '^', commit).decode().split('\0')
rows = []
hygiene = {}
for i in range(0, len(fields) - 1, 2):
    status, path = fields[i:i+2]
    blob = git_run('cat-file', 'blob', commit + ':' + path)
    digest = hashlib.sha256(blob).hexdigest() if status != 'D' else '0' * 64
    rows.append(f'{digest}  {path}\n')
    lines = blob.decode().splitlines()
    hygiene[path] = {'lf_only': b'\r' not in blob, 'bom_free': not blob.startswith(b'\xef\xbb\xbf'),
                     'trailing_whitespace': [i+1 for i,x in enumerate(lines) if x.rstrip() != x],
                     'over_100_columns': [i+1 for i,x in enumerate(lines) if len(x)>100]}
manifest = ''.join(sorted(rows)).encode()
assert hashlib.sha256(manifest).hexdigest() == expected_manifest
assert manifest == (packet / 'manifest.sha256').read_bytes()
assert git_run('rev-parse', commit + '^').decode().strip() == 'c6adbcaa048988361d2388970eaca772711b797b'
assert git_run('rev-parse', commit + '^{tree}').decode().strip() == '89ae2190fa69c6974750ae032a7afec3ca106f18'
(checks / 'cold-b-identity.json').write_text(json.dumps({'snapshot':str(snapshot), 'commit':commit,
    'manifest_sha256':expected_manifest, 'rows': sorted(rows), 'hygiene':hygiene}, indent=2)+'\n', encoding='utf8')
preflight = '''import json, os, pathlib, platform, sys
from pontius.v0a import trace, replay, model, runtime
root = pathlib.Path.cwd().resolve()
mods = {x.__name__: str(pathlib.Path(x.__file__).resolve()) for x in (trace,replay,model,runtime)}
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert all(pathlib.Path(p).is_relative_to(root / "src") for p in mods.values())
print(json.dumps(dict(version=platform.python_version(), executable=sys.executable, cwd=str(root),
 flags=dict(dont_write_bytecode=sys.flags.dont_write_bytecode,safe_path=sys.flags.safe_path),
 modules=mods, environment=dict(os.environ)), sort_keys=True))
'''
for label, exe, version in [('311','D:/Pontius-tools/py311/Scripts/python.exe','3.11.15'),
                            ('314','D:/Pontius/.venv/Scripts/python.exe','3.14.6')]:
    data = json.loads(run([exe, '-B', '-P', '-c', preflight]))
    assert data['version'] == version, data
    receipt = {'preflight':data, 'commands':[]}
    for rel in ['tests/test_v0a_trace.py','tests/test_v0a_replay.py']:
        argv = [exe, '-B', '-P', str(snapshot/rel)]
        start = time.monotonic()
        p = subprocess.run(argv, cwd=snapshot, env=env, capture_output=True)
        log = checks / ('cold-b-' + label + '-' + pathlib.Path(rel).stem + '.log')
        log.write_bytes(p.stdout + p.stderr)
        item = {'argv':argv,'exit_code':p.returncode, 'seconds':time.monotonic()-start,
                'log':str(log),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
        receipt['commands'].append(item)
        print(json.dumps(item), flush=True)
        print((p.stdout+p.stderr).decode('utf8', 'replace')[-2000:], flush=True)
    (checks / ('cold-b-' + label + '-suite-receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
    assert all(item['exit_code']==0 for item in receipt['commands'])
print('IDENTITY_AND_FOCUSED_SUITES_PASS')
