import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = 'D:/Pontius-worktrees/codex-eval-panel-completion-r003'
stage = Path('D:/Pontius/tmp/eval-completion')
label = sys.argv[1]
parent = '430ad75de79cec13d66ff3dc4981dd3770a371b7'
paths = ['tests/test_eval_protocol.py']
if label != 'r003-red':
    paths.append('src/pontius/eval_agreement.py')

def git(*args, env=None, data=None):
    return subprocess.run(['C:/Program Files/Git/cmd/git.exe', '-C', root, *args],
                          check=True, input=data, stdout=subprocess.PIPE, env=env).stdout

with tempfile.TemporaryDirectory() as temporary:
    env = dict(os.environ, GIT_INDEX_FILE=str(Path(temporary) / 'index'))
    git('read-tree', parent, env=env)
    for name in paths:
        raw = Path(root, name).read_bytes()
        assert b'\r' not in raw
        assert all(len(l) <= 100 and l.rstrip() == l for l in raw.decode().splitlines()), name
        blob = git('hash-object', '-w', '--stdin', data=raw).decode().strip()
        git('update-index', '--add', '--cacheinfo', '100644', blob, name, env=env)
    tree = git('write-tree', env=env).decode().strip()
    commit = git('commit-tree', tree, '-p', parent, '-m',
                 'Snapshot completion framing ' + label).decode().strip()
prefix = 'refs/heads/check/' if label != 'r003' else 'refs/heads/review/'
git('update-ref', prefix + 'v0a-eval-panel-completion/' + label, commit, '0' * 40)
(stage / (label + '-commit.txt')).write_text(commit + '\n', encoding='utf-8', newline='\n')
print(commit)
