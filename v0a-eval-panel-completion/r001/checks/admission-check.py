"""Read-only admission of the adopted full-pool decision; never invoke a phase."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

assert sys.version_info[:3] == (3, 14, 6)
root = Path('D:/Pontius-worktrees/eval-completion-check-r001')
stage = Path('D:/Pontius/tmp/eval-completion')
sys.path.insert(0, str(root / 'src'))
spec = importlib.util.spec_from_file_location('completion_admission_only',
                                             root / 'tools/v0a_eval_panel.py')
entry = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = entry
spec.loader.exec_module(entry)
plan = json.loads((root / 'tests/fixtures/eval_panel/plan-capacity.json').read_bytes())
plan.update(version='pontius-eval-panel-completion-plan-v1', phase='solve',
            coverage='declared-full', pool_count=1081, inputs={})
run_root = Path('D:/Pontius-worktrees/eval-panel-prerequisite-20260909/experiments/results/runs')
paths = dict(capacity=run_root / 'a89932e7730e47b8b26b3dafad4f0c41/result.json',
             preflight=run_root / '7ce5ab4fb1304abfa592e780d675d9b7/result.json',
             decision=Path('D:/Pontius-handoffs/v0a-eval-panel-completion/'
                           'prerequisite-run-20260909/resource-decision.md'))
plan['prerequisites'] = {name: dict(path=str(path),
    sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for name, path in paths.items()}
admitted = entry.validate_plan(plan)
assert admitted.document == plan
rejected = []
for field, value in [('pool_count', 1080), ('resource', dict(seconds=601, memory_mib=2048)),
                     ('pool_seed', '0' * 64)]:
    changed = dict(plan, **{field: value})
    try:
        entry.validate_plan(changed)
    except ValueError:
        rejected.append(field)
assert len(rejected) == 3
receipt = dict(check='admission_only_no_phase_invoked', source=stage.joinpath(
    'r001-commit.txt').read_text().strip(), python=sys.version, pool_count=1081,
    resource=plan['resource'], prerequisites=plan['prerequisites'],
    admitted=True, rejected_changed_fields=rejected)
(stage / 'admission-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n',
                                            encoding='utf-8', newline='\n')
print(json.dumps(receipt))
