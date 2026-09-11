import hashlib, json, pathlib, shutil, subprocess, zipfile

S = pathlib.Path(__file__).resolve().parent
P = pathlib.Path('D:/Pontius-handoffs/v0a-blueprint-lookup-performance/r001')
I = json.loads((P/'identity.json').read_bytes())
G = ['C:/Program Files/Git/cmd/git.exe', '-c', 'safe.directory='+I['checkout'], '-C', I['checkout']]
rows = []
with zipfile.ZipFile(P/'base-src.zip') as z:
    for name in z.namelist():
        if name.endswith('/'): continue
        assert z.read(name) == subprocess.check_output(G+['cat-file','blob', I['base_commit']+':'+name]), name
        rows.append(name)
shutil.copytree(S/'base', S/'candidate')
paths = subprocess.check_output(G+['ls-tree','-r','--name-only',I['base_commit'],'--','tests/','tools/','pyproject.toml']).decode().splitlines()
for name in paths:
    out=S/'candidate'/name
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(subprocess.check_output(G+['cat-file','blob',I['base_commit']+':'+name]))
for name, expected in I['overrides'].items():
    raw=(P/'source'/name).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==expected
    out=S/'candidate'/name
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(raw)
receipt=json.loads((P/'checks/affected-pytest-receipt.json').read_bytes())
modules=[r['module'] for r in receipt['suites']]
(S/'suite-modules.json').write_text(json.dumps(modules,indent=2)+'\n')
print(json.dumps({'raw_git_blob_matches':len(rows),'overrides':I['overrides'],'modules':modules},indent=2))
