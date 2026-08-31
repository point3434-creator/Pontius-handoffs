"""Prepare an isolated R1 worktree; no candidate or test execution."""
from pathlib import Path
import hashlib
import json
import subprocess

P = Path(r'D:\Pontius')
H = Path(r'D:\Pontius-handoffs')
T = H / 'v0a-i01-c-authority'
W = Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-core-v1')
OLD = Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1')
BASE = '29c02f6fbd5eb0b7ddc9e816ef28f570b9839358'
DESIGN = 'fc7870b6f5e4c77c2efce8339377d13daeeb1bb4'
BRANCH = 'codex/v0a-i01-c-core-v1'
GIT = r'C:\Program Files\Git\cmd\git.exe'
h = lambda raw: hashlib.sha256(raw).hexdigest()
def git(repo, *args, check=True):
    return subprocess.run([GIT, '-c', 'core.fsmonitor=false', '-c', 'core.autocrlf=false', '-C', str(repo), *args],
        check=check, capture_output=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
assert git(P, 'rev-parse', 'HEAD').stdout.decode().strip() == 'd1ed3cbda6107d61ea8e77133871720af04970cd'
user = {'CLAUDE.md': 'af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76',
        'docs/workflow.md': 'd9de38ede87fb619b3045a60ee7fab137ae23ba3b580c0a6d6b3ca14e567a170'}
assert all(h((P / n).read_bytes()) == pin for n, pin in user.items())
assert git(H, 'rev-parse', DESIGN + '^{commit}').stdout.decode().strip() == DESIGN
manifest = (T / 'rewrite-design-manifest-v2.sha256').read_bytes()
assert h(manifest) == '18fdd632f5eeb3f414ac9e5160b9b276ef9dca0830f60ae13ca1f774b78dd55f'
assert git(H, 'show', DESIGN + ':v0a-i01-c-authority/rewrite-design-manifest-v2.sha256').stdout == manifest
design_pins = {}
for line in manifest.decode().splitlines():
    pin, name = line.split('  ', 1)
    assert h((T / name).read_bytes()) == pin
    assert h(git(H, 'show', DESIGN + ':v0a-i01-c-authority/' + name).stdout) == pin
    design_pins[name] = pin
baseline = json.loads((T / 'coordinator-preservation-baseline-v2.json').read_bytes())['paths']
old_pins = dict(baseline)
old_pins['tools/generate_test_inventory.py'] = 'e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679'
old_pins['tests/test_inventory_and_profiles.py'] = '06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd'
assert all(h((OLD / n).read_bytes()) == pin for n, pin in old_pins.items())
assert not W.exists()
assert git(P, 'show-ref', '--verify', '--quiet', 'refs/heads/' + BRANCH, check=False).returncode == 1
assert not (T / 'rewrite-r1-base-generator.py').exists()
assert not (T / 'coordinator-rewrite-r1-setup-v1.json').exists()
result = git(P, 'worktree', 'add', '-b', BRANCH, str(W), BASE)
assert git(W, 'rev-parse', 'HEAD').stdout.decode().strip() == BASE
assert not git(W, 'status', '--porcelain', '--untracked-files=all').stdout
assert all(h((W / n).read_bytes()) == pin for n, pin in baseline.items())
assert all(h((OLD / n).read_bytes()) == pin for n, pin in old_pins.items())
assert all(h((P / n).read_bytes()) == pin for n, pin in user.items())
base_source = (W / 'tools/generate_test_inventory.py').read_bytes()
with (T / 'rewrite-r1-base-generator.py').open('xb') as stream:
    stream.write(base_source)
report = {'kind': 'isolated engineering worktree setup; no payload', 'worktree': str(W),
          'branch': BRANCH, 'base': BASE, 'design_commit': DESIGN,
          'design_manifest_sha256': h(manifest), 'design_pins': design_pins,
          'base_paths': baseline, 'old_worktree_preserved': old_pins, 'main_user_files': user,
          'baseline_generator_sha256': h(base_source), 'payload_executed': False,
          'candidate_source_modified': False}
for name, raw in {'coordinator-rewrite-r1-setup-v1.json': (json.dumps(report, indent=2, sort_keys=True) + '\n').encode(),
                  'coordinator-prepare-rewrite-r1-v1.py': Path(__file__).read_bytes()}.items():
    with (T / name).open('xb') as stream:
        stream.write(raw)
print(json.dumps({'worktree': str(W), 'base': BASE, 'preserved_paths': len(baseline),
                  'baseline_source_sha256': h(base_source), 'payload_executed': False}))
