"""Adopted public validators and teacher_input, using local mutated input documents."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

assert sys.version_info[:3] == (3, 14, 6)
root, packet = map(Path, sys.argv[1:3])
sys.path.insert(0, str(root / 'src'))
spec = importlib.util.spec_from_file_location('export_control_entry', root/'tools/v0a_eval_panel.py')
entry = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = entry
spec.loader.exec_module(entry)
completion = entry.load_completion()
plan = json.loads((packet/'plans/export.json').read_bytes())
producer = json.loads(Path(plan['inputs']['producer_result']['path']).read_bytes())
rows = []
with tempfile.TemporaryDirectory(prefix='export-input-controls-') as tmp:
    for field, bad in [('status','failed'), ('phase','export'), ('coverage','test-subset'),
                       ('cleanup_verified',False), ('phase_complete',False), ('artifact',None)]:
        changed = copy.deepcopy(producer)
        if field == 'artifact':
            artifact = next(r for r in changed['observations'] if r.get('kind') == 'artifact')
            artifact['sha256'] = '0'*64
        else:
            changed[field] = bad
        path = Path(tmp) / (field+'.json')
        raw = json.dumps(changed).encode(); path.write_bytes(raw)
        candidate = copy.deepcopy(plan)
        candidate['inputs']['producer_result'] = dict(path=path.as_posix(),
                                                      sha256=hashlib.sha256(raw).hexdigest())
        try:
            completion.teacher_input(candidate)
            refused = False; reason = ''
        except ValueError as error:
            refused = True; reason = str(error)
        rows.append(dict(case='producer-'+field, refused=refused, reason=reason))
    for key in ('teacher','producer_result'):
        candidate = copy.deepcopy(plan); del candidate['inputs'][key]
        try:
            entry.validate_plan(candidate)
            refused=False; reason=''
        except ValueError as error:
            refused=True; reason=str(error)
        rows.append(dict(case='missing-'+key, refused=refused, reason=reason))
assert all(row['refused'] for row in rows), rows
print(json.dumps(dict(cases=len(rows), failures=0, results=rows, python=sys.version)))
