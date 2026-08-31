from pathlib import Path
import hashlib

root = Path(r'D:\Pontius')
source = root / 'codex-c-core-rewrite-brief-draft.md'
raw = source.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '9926f7dfb78ccc910c8b6f8a9f36177f6f6a4e052ef3956f4e5c0f2ee350fca8'
text = raw.decode('utf-8')
remove = [
'''The binder's signature-matching algorithm can remain; its state-bearing input
and result transport must use the new model. The replacement also includes the
helper-entry/prepass and recursive _review_body bridges that currently rebuild
executable inputs from name/default/argument projections. Keeping those bridges
unchanged would preserve a second execution model even with a new resolver.
''',
'''The selected callee identity is captured first; each argument is selected in its
own evaluation order; live cells and mutable referents are read at the actual
invocation/consumption point. Final sink evidence is fixed at its own source
point. An observation is never reconstructed by re-executing the helper body.
''',
'''Gate A is exactly shared-list-consumed, shared-list-dormant,
class-adoption-unsafe, class-adoption-safe, hidden-cell-joined-reached, and
hidden-cell-joined-dormant from the frozen composition/environment packs. Keep
their two required-clean, three required-refusal, and one permitted-refusal
classifications. Gate A does not claim deep-generator support.
''',
]
for value in remove:
    assert text.count(value) == 1
    text = text.replace(value, '', 1)
replacements = [
('''Any reused primitive keeps its old requirements; standalone prototype-specific
tests and counter identities retain their evidence but do not force a new API.
No existing production behavioral test is removed or weakened under that rule.
''', '''Any reused primitive keeps its old requirements; retired implementation-specific
tests and counter identities retain their evidence but do not force a new API.
'''),
('''models, and unchanged expected outcomes before dispatch. Gate B reruns Gate A
and adds helper65, generator70, scale-n8-s4-d0-normal, scale-n64-s4-d0-normal,
scale-n8-s4-d2-exceptional, and scale-n64-s4-d2-exceptional: twelve existing cases.
''', '''models, and unchanged expected outcomes before dispatch.
'''),
('''196608-unit ceiling (75% of the existing 262144 cap) is adopted for Gate B as an
engineering continuation criterion, leaving 65536 units of reserve. Its
sufficiency is unproved; it is not a new runtime admission cap or a speedup
claim. Gate A records all budgets/headroom under the unchanged cap without
requiring Gate B's depth machinery. Match all original budget scopes by their
creation owner/stage, never select only historical failing epoch numbers. Count
every actual request through refusal; invent no charge for a noncharging check.
''', '''196608-unit ceiling (75% of the existing 262144 cap) reserves engineering headroom
for the rest of the migration. Its sufficiency is unproved; it is not a new
runtime admission cap. It must be dispositioned and frozen before a fitness run,
not selected after looking at the result.
'''),
]
for new, old in replacements:
    assert text.count(new) == 1
    text = text.replace(new, old, 1)
original = text.encode('utf-8')
assert hashlib.sha256(original).hexdigest() == '18ff3c1d6b228474a321d93f8be4498c717f5af2244be62855cfb5e50ec24acb'
out = root / 'codex-c-core-rewrite-reviewed-draft-v0.md'
with out.open('xb') as handle:
    handle.write(original)
print(hashlib.sha256(out.read_bytes()).hexdigest())
