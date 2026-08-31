"""Check the two pre-wiring corrections and original-code preservation without import."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import sys

T = Path(r'D:\Pontius-handoffs\v0a-i01-c-authority')
W = Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-core-v1')
h = lambda raw: hashlib.sha256(raw).hexdigest()
assert len(sys.argv) == 2
pin = sys.argv[1]
base = (T / 'rewrite-r1-base-generator.py').read_bytes()
v1 = (T / 'rewrite-r1-task1-source-v1.py').read_bytes()
v2 = (T / 'rewrite-r1-task1-source-v2.py').read_bytes()
assert h(base) == '29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692'
assert h(v1) == 'ff889b1ee3595d23d2109d15d87f80d8f5c153b3db524aaef3eb53b1797dcab1'
assert h(v2) == pin == h((W / 'tools/generate_test_inventory.py').read_bytes())
start = b'# Canonical C core. R1 Task1 is intentionally not wired to public analysis yet.\n'
end = b'@dataclass(slots=True)\nclass _PreclassifierExceptionalState:'
fragments = []
for raw in (v1, v2):
    a, b = raw.index(start), raw.index(end)
    assert raw[:a] + raw[b:] == base
    fragments.append(ast.parse(raw[a:b].decode()))
expected = copy.deepcopy(fragments[0])
choice = next(n for n in expected.body if isinstance(n, ast.FunctionDef) and n.name == '_c_choice')
empty = next(n for n in choice.body if isinstance(n, ast.If) and isinstance(n.test, ast.UnaryOp)
             and isinstance(n.test.op, ast.Not) and isinstance(n.test.operand, ast.Name) and n.test.operand.id == 'values')
empty.body = ast.parse('ctx.budget.consume()\nraise InventoryError("canonical alternative set is empty")').body
container_index = next(i for i, n in enumerate(choice.body) if isinstance(n, ast.Expr)
    and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute)
    and n.value.func.attr == 'container')
assert isinstance(choice.body[container_index - 1], ast.Expr)
choice.body[container_index - 1], choice.body[container_index] = choice.body[container_index], choice.body[container_index - 1]
assert ast.dump(expected, include_attributes=False) == ast.dump(fragments[1], include_attributes=False)
setup = json.loads((T / 'coordinator-rewrite-r1-setup-v1.json').read_bytes())
preserved = {name: wanted for name, wanted in setup['base_paths'].items() if name != 'tools/generate_test_inventory.py'}
assert all(h((W / name).read_bytes()) == wanted for name, wanted in preserved.items())
report = {'kind': 'root static pre-wiring correction verification; no candidate execution',
    'version': list(sys.version_info[:3]), 'source_sha256': pin, 'original_bytes_exact': True,
    'only_semantic_AST_changes': ['empty choice throws InventoryError after one visit charge',
        'existing container guard precedes additional tuple-copy visit charge'],
    'other16_paths_preserved': preserved, 'public_entry_unwired': True,
    'baseline_semantic_RED_still_open': True, 'script_sha256': h(Path(__file__).read_bytes())}
out = T / 'coordinator-rewrite-r1-task1-v2-verification.json'
with out.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'verification': str(out), 'sha256': h(out.read_bytes()), 'source_sha256': pin}))
