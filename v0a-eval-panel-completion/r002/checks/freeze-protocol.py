import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path('D:/Pontius-worktrees/codex-eval-panel-completion-r002')
stage = Path('D:/Pontius/tmp/eval-completion')
label = sys.argv[1]
git = 'C:/Program Files/Git/cmd/git.exe'
parent = '449a2a3c1fa1f5a7f5f04adca32e499faaf81e13'
paths = ['tests/cases.json', 'tests/test_eval_protocol.py']
if label != 'r002-red':
    paths += ['src/pontius/eval_agreement.py']

def run(*args, env=None, data=None):
    return subprocess.run([git, '-C', str(root), *args], check=True, input=data,
                          stdout=subprocess.PIPE, env=env).stdout

with tempfile.TemporaryDirectory() as temporary:
    env = dict(os.environ, GIT_INDEX_FILE=str(Path(temporary) / 'index'))
    run('read-tree', parent, env=env)
    for path in paths:
        raw = (root / path).read_bytes()
        assert b'\r' not in raw and max(map(len, raw.splitlines())) <= 100, path
        blob = run('hash-object', '-w', '--stdin', data=raw).strip().decode()
        run('update-index', '--add', '--cacheinfo', '100644', blob, path, env=env)
    tree = run('write-tree', env=env).strip().decode()
    commit = run('commit-tree', tree, '-p', parent, '-m',
                 'Freeze completion protocol ' + label).strip().decode()
run('update-ref', 'refs/heads/review/v0a-eval-panel-completion/' + label, commit, '0' * 40)
(stage / (label + '-commit.txt')).write_text(commit + '\n', encoding='utf-8', newline='\n')
print(json.dumps(dict(candidate=commit, parent=parent, tree=tree, paths=paths)))
