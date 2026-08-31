import ast, subprocess, sys
from pathlib import Path
source=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tests\test_inventory_and_profiles.py')
cls=next(node for node in ast.parse(source.read_text(encoding='utf-8')).body if isinstance(node,ast.ClassDef) and node.name=='DesignReviewTests')
names=['DesignReviewTests.'+node.name for node in cls.body if isinstance(node,ast.FunctionDef) and node.name.startswith('test_')]
print('Explicit analyzer methods:',len(names),*names,sep='\n',flush=True)
raise SystemExit(subprocess.run([r'D:\Pontius-tools\py311\Scripts\python.exe','-B','-P',r'D:\Pontius-handoffs\v0a-i01-ab\c-provenance-run.py',*sys.argv[1:],*names]).returncode)