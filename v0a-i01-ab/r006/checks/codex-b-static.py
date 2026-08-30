import ast
import json
from pathlib import Path
import runpy
context = runpy.run_path(str(Path(__file__).with_name('codex-b-identity.py')))
run, commit = context['run'], context['commit']
assert run('diff','--check',commit+'^',commit) == b''
added=[]
for row in run('diff','--no-ext-diff','--no-renames','--unified=0',commit+'^',commit).splitlines():
    if row.startswith(b'+') and not row.startswith(b'+++'):
        added.append(row[1:])
assert not [row for row in added if len(row)>100]
preexisting=[]
for path in ('src/pontius/v0a/trace.py','tests/test_v0a_trace.py'):
    current=run('cat-file','blob',commit+':'+path)
    previous=run('cat-file','blob',commit+'^:'+path)
    ast.parse(current,filename=path)
    old_long={line for line in previous.splitlines() if len(line)>100}
    current_long={line for line in current.splitlines() if len(line)>100}
    assert current_long <= old_long
    preexisting.append({'path':path,'existing_over100_line_count':len(current_long)})
assert run('status','--porcelain') == b''
print(json.dumps({'result':'PASS','added_lines_checked':len(added),
 'added_lines_over100':0,'syntax':'both changed files parsed',
 'preexisting_long_lines_unchanged':preexisting,'snapshot_status':'clean'},sort_keys=True))
