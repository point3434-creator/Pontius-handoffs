import hashlib
import json
from pathlib import Path
import subprocess
import sys

assert sys.version_info[:3] == (3, 14, 6)
root = Path('D:/Pontius-worktrees/codex-eval-panel-completion')
stage = Path('D:/Pontius/tmp/eval-completion')
production = ['src/pontius/eval_bridge.py', 'src/pontius/eval_agreement.py',
              'tools/v0a_eval_panel.py', 'tools/v0a_eval_panel_completion.py']
tests = ['tests/test_eval_bridge.py', 'tests/test_eval_panel_tool.py',
         'tests/test_eval_export.py', 'tests/test_eval_agreement.py',
         'tests/test_eval_completion_tool.py']
changed = production + tests[2:] + ['tests/cases.json']
rows = []
for name in production + tests:
    raw = (root / name).read_bytes().replace(b'\r\n', b'\n')
    lines = raw.decode('utf-8').splitlines()
    assert all(len(line) <= 100 and line.rstrip() == line for line in lines), name
    assert not raw.startswith(b'\xef\xbb\xbf'), name
    if name in changed:
        (root / name).write_bytes(raw)
    rows.append(dict(path=name, lines=len(lines), sha256=hashlib.sha256(raw).hexdigest()))
counts = dict(production=sum(r['lines'] for r in rows if r['path'] in production),
              tests=sum(r['lines'] for r in rows if r['path'] in tests))
assert counts['production'] < 3000
lint = subprocess.run([sys.executable, '-B', '-P', '-m', 'ruff', 'check', '--no-cache',
                       *[str(root / p) for p in changed if p.endswith('.py')]],
                      capture_output=True, text=True)
receipt = dict(python=sys.version, executable=sys.executable, rows=rows, counts=counts,
               ceiling_production=3000, working_figures=dict(production=1200, tests=600),
               lint=dict(exit=lint.returncode, stdout=lint.stdout, stderr=lint.stderr))
(stage / 'hygiene.json').write_text(json.dumps(receipt, indent=2) + '\n',
                                  encoding='utf-8', newline='\n')
print(json.dumps(receipt))
sys.exit(lint.returncode)
