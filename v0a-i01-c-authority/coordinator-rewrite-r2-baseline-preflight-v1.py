"""Static custody preflight for one R1 baseline; no payload import or execution."""
from pathlib import Path
import ast
import hashlib
import json
import subprocess

H = Path(r'D:\Pontius-handoffs')
T = H / 'v0a-i01-c-authority'
W = Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-core-v1')
GIT = r'C:\Program Files\Git\cmd\git.exe'
REF = '1ffb59efd95c4a41b87b92de8fd56f26801ff918'
MANIFEST = 'dcb016d9f4eb27d33d55ecba0d0a00ff87de1dccc76a90f095dc7230ac29a61d'
h = lambda raw: hashlib.sha256(raw).hexdigest()

def blob(name):
    return subprocess.run([GIT, '-C', str(H), 'show', REF + ':v0a-i01-c-authority/' + name],
                          capture_output=True, check=True, timeout=60).stdout

manifest = blob('rewrite-r2-identity-harness-v2-manifest.sha256')
assert h(manifest) == MANIFEST
pins = {}
for line in manifest.decode().splitlines():
    pin, name = line.split('  ', 1)
    raw = blob(name)
    assert raw == (T / name).read_bytes() and h(raw) == pin
    pins[name] = pin
assert len(pins) == 10
source = 'c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f'
assert h((T / 'rewrite-r1-task5-source-v2.py').read_bytes()) == source
assert h((W / 'tools/generate_test_inventory.py').read_bytes()) == source
setup = json.loads((T / 'coordinator-rewrite-r1-setup-v1.json').read_bytes())
protected = {name: pin for name, pin in setup['base_paths'].items() if name != 'tools/generate_test_inventory.py'}
assert len(protected) == 16
assert all(h((W / name).read_bytes()) == pin for name, pin in protected.items())
assert h(Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1\tools\generate_test_inventory.py').read_bytes()) == 'e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679'
probe = (T / 'tests-checks/rewrite-r2-identity-probe-v2.py').read_bytes()
control = (T / 'tests-checks/rewrite-r2-identity-control-v2.py').read_bytes()
pt, ct = ast.parse(probe), ast.parse(control)
def segment(raw, tree, name):
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name]
    assert len(nodes) == 1
    return ast.get_source_segment(raw.decode(), nodes[0])
same = ('load_cases', 'public_verdict', 'validate_budget_metrics', 'reserve_violations',
        'validate_identity_inputs', 'validate_mechanism', 'validate_lifecycle')
assert all(segment(probe, pt, name) == segment(control, ct, name) for name in same)
old = (T / 'tests-checks/rewrite-r2-identity-probe-v1.py').read_bytes()
ot = ast.parse(old)
preserved = [n.name for n in ot.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name != 'main']
assert len(preserved) == 25
assert all(segment(old, ot, name) == segment(probe, pt, name) for name in preserved)
run_nodes = [n for n in ast.walk(ct) if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == 'run' for t in n.targets)]
assert len(run_nodes) == 1 and isinstance(run_nodes[0].value, ast.Dict)
run_keys = [ast.literal_eval(k) for k in run_nodes[0].value.keys]
assert len(run_keys) == len(set(run_keys)) == 21
assert not list((T / 'tests-checks').glob('rewrite-r2-identity-v2-r2-base01-311-*'))
assert not list((T / 'tests-checks').glob('rewrite-r2-identity-v2-r2-base01-311.*'))
report = {'kind': 'root static baseline preflight; no payload imported or executed', 'harness_ref': REF,
          'manifest_sha256': MANIFEST, 'harness_pins': pins, 'source_sha256': source,
          'protected16': protected, 'unchanged_probe_definitions': preserved,
          'shared_replay_definitions': list(same), 'run_config_keys': run_keys,
          'label_available': 'r2-base01', 'slot': '311',
          'script_sha256': h(Path(__file__).read_bytes())}
out = T / 'coordinator-rewrite-r2-baseline-preflight-v1.json'
with out.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'preflight': str(out), 'sha256': h(out.read_bytes()), 'protected': len(protected),
                  'preserved_definitions': len(preserved), 'no_payload': True}))
