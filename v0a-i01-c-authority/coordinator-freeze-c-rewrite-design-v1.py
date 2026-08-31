"""Retain design-only inputs; preserve all source and prior navigation bytes."""
from pathlib import Path
import hashlib
import json

P = Path(r'D:\Pontius')
T = Path(r'D:\Pontius-handoffs\v0a-i01-c-authority')
W = Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1')
h = lambda raw: hashlib.sha256(raw).hexdigest()
copies = {
    'rewrite-stage0-v1.md': ('codex-c-core-rewrite-stage0-draft.md', '8c84baa92400716efee2d4dd23eeafefa88a794125bafd4cc97432572ca7e077'),
    'rewrite-design-v1.md': ('codex-c-core-rewrite-brief-draft.md', '701552c177840e4c5c0dd9c5985776256af5b31e7e997067dd662638a67c3ca8'),
    'rewrite-design-reviewed-draft-v0.md': ('codex-c-core-rewrite-reviewed-draft-v0.md', '18ff3c1d6b228474a321d93f8be4498c717f5af2244be62855cfb5e50ec24acb'),
    'coordinator-retain-rewrite-draft-v0.py': ('codex-retain-rewrite-draft-v0.py', None),
}
inputs = {
    'stage0-design.md': '78bebca5279bf81e30181787f962d40c73826259d0bb3ffb1c7804804c1211e8',
    'rewrite-state-model-proposal-v1.md': 'dfbff5aef7e49ba2f70e39919feff18bafad3313131771a3184b60f30e60bead',
    'rewrite-cost-and-fitness-proposal-v1.md': '9b5c4a3cf7d187f47a2f1dc9e01f239279d42c74aaf56208fad39a801f164c76',
    'rewrite-cost-and-fitness-clarification-v2.md': '75c98159a96c33f5f9072c572beae567494ac16fa831c94058c6706be1e22c80',
    'rewrite-design-engineering-review-codex-a-v1.md': '40eeb140b1cd7bc312883368df3a97127bf1f727b0b197f4751a98bb3fdf3979',
    'coordinator-v30-design-verification-v1.json': 'ed57b0fa44fda469f2291268682774bda02e82f5bc13dc9bbfca9d807c2acbf1',
    'tests-checks/depth-budget-v5-harness-engineering-review-codex-a-v1.md': 'd2d4439356937b3a393c55cd100c60fb5c79572c4fbf05abf798d781150932e3',
    'strategy-hold-v31-v1/custody-receipt-v1.json': '3c1d733f247078b6c9f5fc6b356eacca8bf14d3a6cb922374c4f350db60fa161',
}
assert all(h((T / name).read_bytes()) == pin for name, pin in inputs.items())
baseline = json.loads((T / 'coordinator-preservation-baseline-v2.json').read_bytes())['paths']
baseline['tools/generate_test_inventory.py'] = 'e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679'
baseline['tests/test_inventory_and_profiles.py'] = '06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd'
assert len(baseline) == 17 and all(h((W / n).read_bytes()) == pin for n, pin in baseline.items())
user_files = {'CLAUDE.md': 'af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76',
              'docs/workflow.md': 'd9de38ede87fb619b3045a60ee7fab137ae23ba3b580c0a6d6b3ca14e567a170'}
assert all(h((P / n).read_bytes()) == pin for n, pin in user_files.items())
contents = {}
for target, (source, pin) in copies.items():
    raw = (P / source).read_bytes()
    assert pin is None or h(raw) == pin
    contents[target] = raw
contents['coordinator-freeze-c-rewrite-design-v1.py'] = Path(__file__).read_bytes()
disposition = '''# C replacement: design review disposition v1

Engineering only. The reviewed draft was SHA18ff3c1d6b228474a321d93f8be4498c717f5af2244be62855cfb5e50ec24acb.
Its exact bytes are retained as rewrite-design-reviewed-draft-v0.md after an exact
inverse of the recorded later edit reproduced that hash. The reviewer read a
mutable draft; this is not a frozen implementation review or a cold pass. Do not
apply its report to later bytes as though it reviewed them.

The coordinator accepts all six design findings. rewrite-design-v1.md addresses:
1. Executable-entry inventory: resolver, call snapshots, helper-return/prepass,
   unittest preflight and recursive review bridges. Binder rules can remain;
   executable live-value transport cannot.
2. Full call observation: selected callee/receiver, argument/default references,
   call-entry state version, and result/effects. A default selects a reference,
   not frozen mutable contents; closure reads remain live until invocation.
3. R1 includes required minimal successor/state-result pairing and exceptions.
   R2 extends control/deferred behavior; it cannot supply a missing R1 obligation.
4. Explicit class shadow/fallback, lexical destinations, outermost comprehension
   iterable versus implicit body scope, and state-owned current members.
5. Typed retention/element/capture/deferred edges and reached outcome issues,
   without confusing container traversal with executing a contained generator.
6. The early test uses the entire public path and all actual budget scopes;
   required name enumeration is separate from avoidable value reconstruction.

The state proposal and cost v1/v2 are adopted as design input subject to the
coordinator design. Root adopts the196608 Gate B reserve before any replacement
result, while retaining the262144 production cap. Gate A uses the cap and records
headroom. This is a continuation choice, not empirically established sufficiency.
No representation-specific prototype interface is added to product requirements.

Replacement implementation, detailed operation accounting, controller review and
payload execution have not occurred. Category/coverage planning and a concrete R1
implementation plan precede production edits. All failed candidates, tests,
expectations and held diagnostics remain intact. Existing engineering sessions
cannot count as the future two mutually blind cold reviewers.
'''.encode()
contents['rewrite-design-disposition-v1.md'] = disposition
manifest_names = sorted(set(contents) | set(inputs))
manifest = ''.join(f'{h(contents[n]) if n in contents else inputs[n]}  {n}\n' for n in manifest_names).encode()
contents['rewrite-design-manifest-v1.sha256'] = manifest
receipt = {'kind': 'design-only; no implementation/cold/runtime claim',
           'inputs': inputs, 'outputs': {n: h(raw) for n, raw in contents.items()},
           'preserved_W_paths': baseline, 'main_user_owned_paths': user_files,
           'rewrite_source_changed': False, 'payload_executed': False,
           'held': ['unfinished v31 scratch', 'v5 generator70 diagnostic'],
           'runtime_work_cap': 262144, 'gate_B_continuation_reserve_ceiling': 196608}
contents['coordinator-rewrite-design-freeze-v1.json'] = (json.dumps(receipt, indent=2, sort_keys=True) + '\n').encode()
assert not any((T / n).exists() for n in contents)
for name, raw in contents.items():
    with (T / name).open('xb') as stream:
        stream.write(raw)
assert all(h((T / n).read_bytes()) == h(raw) for n, raw in contents.items())
print(json.dumps({'outputs': {n: h(raw) for n, raw in contents.items()}, 'source_changed': False}))
