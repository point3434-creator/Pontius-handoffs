"""Read-only integration preservation checks against frozen Git blobs."""
import json,os,subprocess,tomllib
from pathlib import Path
root=Path.cwd(); git=os.environ['PONTIUS_GIT']
base='d1ed3cbda6107d61ea8e77133871720af04970cd'
fixbase='00db06624ab25f10cd181badccf92c87a78f17ee'
commit='8d240db477b8c141e6142e055dbfbedc75c6a2f8'
def raw(ref,path):
    return subprocess.run([git,'-C',str(root),'cat-file','blob',ref+':'+path],check=True,capture_output=True).stdout
old=json.loads(raw(base,'tests/test-inventory.json')); new=json.loads(raw(commit,'tests/test-inventory.json')); before=json.loads(raw(fixbase,'tests/test-inventory.json'))
byid=lambda doc:{r['stable_id']:r for r in doc['entries']}
a,b,c=byid(old),byid(new),byid(before)
assert a.keys()<=b.keys() and all(a[k]==b[k] for k in a)
assert c.keys()<=b.keys() and all(c[k]==b[k] for k in c)
suites=('test_v0a_boundaries.py','test_v0a_hand_replay.py','test_v0a_trace.py','test_v0a_replay.py','test_v0a_contract_faults.py')
counts={f:sum(row['relative_path']=='tests/'+f for row in b.values()) for f in suites}
assert all(counts.values())
assert raw(fixbase,'tests/test-profiles.toml')==raw(commit,'tests/test-profiles.toml')
ci_old=raw(base,'.github/workflows/ci.yml').decode(); ci=raw(commit,'.github/workflows/ci.yml').decode()
oldlines=ci_old.splitlines(); newlines=iter(ci.splitlines())
assert all(any(candidate==line for candidate in newlines) for line in oldlines)
for f in suites:
    matching=[block for block in ci.split('      - name: ') if ('tests\\'+f) in block]
    assert len(matching)==1 and 'if: ${{ !cancelled() }}' in matching[0] and 'continue-on-error' not in matching[0]
blob=subprocess.run([git,'-C',str(root),'rev-parse',commit+':docs/architecture/dependency-baseline.toml'],capture_output=True,check=True).stdout.decode().strip()
assert blob=='5fe6ee47f3380b65887b528efef05b72c8e6ac0a'
print(json.dumps({'main_existing_entries_unchanged':len(a),'main_additions':len(b.keys()-a.keys()),'fix_existing_entries_unchanged':len(c),'fix_additions':sorted(b.keys()-c.keys()),'v0a_suite_counts':counts,'profiles_unchanged_vs_fix':True,'ci_prior_lines_retained':True,'ci_all_five_reachable_hard_gates':True,'baseline_blob':blob}),flush=True)
