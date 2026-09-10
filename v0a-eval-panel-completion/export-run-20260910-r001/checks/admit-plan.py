import hashlib
import importlib.util
import json
from pathlib import Path
import sys

assert sys.version_info[:3] == (3, 14, 6)
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'src'))
spec = importlib.util.spec_from_file_location('export_admission_entry', root / 'tools/v0a_eval_panel.py')
entry = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = entry
spec.loader.exec_module(entry)
raw = (root / 'plans/export.json').read_bytes()
plan = json.loads(raw)
entry.validate_plan(plan)
completion = entry.load_completion()
teacher, board, hands, actions = completion.teacher_input(plan)
print(json.dumps(dict(python=sys.version, root=str(root), admitted=True,
                     teacher_input_validated=True, hands=len(hands),
                     teacher_sha256=hashlib.sha256(teacher).hexdigest(),
                     plan_sha256=hashlib.sha256(raw).hexdigest())))
