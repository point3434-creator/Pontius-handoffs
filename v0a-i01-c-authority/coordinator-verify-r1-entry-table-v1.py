"""Coordinator AST/hash-only check of the two-runtime unittest source union."""
import ast
import hashlib
import json
from pathlib import Path
import sys

T = Path(r'D:\Pontius-handoffs\v0a-i01-c-authority')
path = T / 'rewrite-r1-unittest-entry-reserved-names-v1.json'
h = lambda raw: hashlib.sha256(raw).hexdigest()
raw = path.read_bytes()
assert h(raw) == '55ed71468da3c480e4805672b2b254e1bff5d6d0cf99a2c36ed0fbcfec202ceb'
assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.safe_path
table = json.loads(raw)
union = set()
reports = []
for source in table['sources']:
    cfg = Path(source['pyvenv_cfg_path']).read_bytes()
    assert h(cfg) == source['pyvenv_cfg_sha256']
    values = dict(line.split(' = ', 1) for line in cfg.decode().splitlines() if ' = ' in line)
    assert values['version_info'] == source['configured_version']
    assert Path(values['home']) / 'Lib' / 'unittest' / 'case.py' == Path(source['source_path'])
    code = Path(source['source_path']).read_bytes()
    assert h(code) == source['source_sha256'] and len(code) == source['source_bytes']
    module = ast.parse(code)
    candidates = [n for n in module.body if isinstance(n, ast.ClassDef) and n.name == 'TestCase']
    assert len(candidates) == 1
    cls = candidates[0]
    assert [cls.lineno, cls.end_lineno] == source['TestCase_lines']
    names, fields = set(), set()
    for member in cls.body:
        if isinstance(member, ast.FunctionDef):
            names.add(member.name)
            fields.update(n.attr for n in ast.walk(member)
                          if isinstance(n, ast.Attribute) and isinstance(n.ctx, (ast.Store, ast.Del))
                          and isinstance(n.value, ast.Name) and n.value.id in ('self', 'cls'))
        elif isinstance(member, ast.Assign):
            assert all(isinstance(n, ast.Name) for n in member.targets)
            names.update(n.id for n in member.targets)
        else:
            assert isinstance(member, ast.Expr) and isinstance(member.value, ast.Constant)
            assert type(member.value.value) is str
    assert sorted(names) == source['class_scope_names']
    assert sorted(fields) == source['lifecycle_storage_names']
    union.update(names | fields)
    reports.append({'slot': source['slot'], 'version': values['version_info'],
                    'source_sha256': h(code), 'class_names': len(names), 'lifecycle_fields': len(fields)})
assert sorted(union) == table['reserved_names'] and len(union) == 111
nondunder = sorted(n for n in union if not (n.startswith('__') and n.endswith('__')))
assert len(nondunder) == 104
report = {'kind': 'coordinator AST-only table verification, no candidate or unittest import',
          'table_sha256': h(raw), 'sources': reports, 'reserved_count': len(union),
          'nondunder_count': len(nondunder), 'passed': True,
          'verifier_sha256': h(Path(__file__).read_bytes())}
out = T / 'coordinator-rewrite-r1-entry-table-verification-v1.json'
with out.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'output': str(out), 'sha256': h(out.read_bytes()), **report}))
