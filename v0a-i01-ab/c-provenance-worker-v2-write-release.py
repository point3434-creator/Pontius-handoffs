import ast, hashlib, json, re, subprocess
from pathlib import Path
root=Path(r'D:\Pontius-handoffs\v0a-i01-ab')
work=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance')
git=r'C:\Program Files\Git\cmd\git.exe'
base='00db06624ab25f10cd181badccf92c87a78f17ee'
owned=('tools/generate_test_inventory.py','tests/test_inventory_and_profiles.py')
def git_run(*args):
    return subprocess.run([git,'-C',str(work),*args],capture_output=True,check=True)
def digest(raw): return hashlib.sha256(raw).hexdigest()
def save(name,raw):
    with (root/name).open('xb') as stream: stream.write(raw)
sha={path:digest((work/path).read_bytes()) for path in owned}
receipts=[]
for slot in ('311','314'):
    path=root/f'c-provenance-v2-green01-{slot}-receipt.json'
    receipt=json.loads(path.read_text())
    assert receipt['exit']==0 and receipt['overlay_sha256']==sha
    log=Path(receipt['log']).read_bytes()
    assert digest(log)==receipt['sha256']
    results=[json.loads(line) for line in log.decode().splitlines() if line.startswith('{')]
    summary=next(result for result in results if 'tests_run' in result)
    assert summary=={'tests_run':36,'failures':0,'errors':0,'skipped':0}
    elapsed=re.search(r'Ran 36 tests in ([0-9.]+)s',log.decode()).group(1)
    receipts.append({'receipt':path.name,'receipt_sha256':digest(path.read_bytes()),
                     'slot':slot,'summary':summary,'elapsed_seconds':elapsed,
                     'log_sha256':digest(log),'command':receipt['command']})
old=git_run('show',base+':'+owned[1]).stdout.decode('utf-8')
new=(work/owned[1]).read_text(encoding='utf-8')
def methods(text):
    return {(node.name,member.name):ast.dump(member,include_attributes=False)
            for node in ast.parse(text).body if isinstance(node,ast.ClassDef)
            for member in node.body if isinstance(member,(ast.FunctionDef,ast.AsyncFunctionDef))}
prior,current=methods(old),methods(new)
assert all(current.get(key)==value for key,value in prior.items())
status=git_run('status','--porcelain').stdout.decode()
assert {line[3:] for line in status.splitlines()}==set(owned),status
check=git_run('diff','--check')
patch=git_run('diff','--binary',base,'--',*owned).stdout
save('c-provenance-worker-v2-final-owned.patch',patch)
validation={'base':base,'owned_sha256':sha,'git_status':status,'diff_check_exit':check.returncode,
            'existing_class_methods_ast_identical':len(prior),'removed_or_changed_existing_methods':0,
            'new_class_methods':sorted('::'.join(key) for key in current.keys()-prior.keys()),
            'green':receipts,'patch_sha256':digest(patch),
            'line_endings':{path:{'bom':(work/path).read_bytes().startswith(b'\xef\xbb\xbf'),
                                  'crlf_count':(work/path).read_bytes().count(b'\r\n')}
                            for path in owned}}
save('c-provenance-worker-v2-final-validation.json',(json.dumps(validation,indent=2)+'\n').encode())
report=f'''# C provenance integration correction: worker release v2

Released two files from `{work}` against r008 `{base}`. No further edits pending.
This is an engineering handoff, not a cold review or full-corpus acceptance claim.

## Changes and preserved contracts

Callable/class/module/receiver identity is orthogonal metadata: legacy qualified values,
callable summaries, protected returns and exception transfer remain intact. Proof is met
separately at merges; captured defaults merge by parameter without choosing an arbitrary
branch. Ordinary failed lookup retains the existing exception/census path. Exact harmless
local callables retain their non-sensitive disposition; missing source snapshots are not
turned into invented completed calls.

Source-point arguments, defaults and callee capture remain preserved. Parameters in the
production proof path overwrite unrelated seeds; explicit inputs to the legacy resolver
without a helper registry retain its original contract. Source-point nonlocal captures
survive initialization, and declarations alone do not imply namespace mutation.

Known module exports and standard unittest skip/skipIf/skipUnless class decoration regain
proof through their bindings. Deferred unrelated bodies and immutable code reads do not
poison a module. Actual source-ordered member changes invalidate owner/member identity;
imported initialization changes bind to the resolved owner/member. Unknown reachable
initialization effects and unproved owner escapes produce typed refusals. Existing fresh
unrelated namespaces and protected external-module mutation semantics remain unchanged.

All {len(prior)} pre-existing class methods in the test file are AST-identical to r008;
none was removed or weakened. Only the new annotation/deletion controls were clarified:
proved non-completion may have zero helper rows without an invented unresolved blocker.
The opposing caught-NameError tests require exactly the handler's subprocess projection.
The checks execute only pure return projections of new sensitive fixtures, never their
subprocess bodies. Metered binding traversal is iterative and keeps the existing limits.

## Evidence

Existing RED: root's `abc-checks/provenance-inventory-precheck01-311.txt`, 99 tests,
39 failures and 5 errors on released d94a8e8c source. New precision RED before source edits:
`c-provenance-v2-red01-311-receipt.json`, 2 methods /8 failures /0 errors. The imported
initialization control then exposed one required residual in
`c-provenance-v2-red02-311-receipt.json` (2 methods /1 failure /0 errors); its unrelated
member positive stayed clean. The additional local default-replacement control already
refused and is coverage evidence rather than an invented product RED.

Final commands (the append-only runner derives and passes every method name from the AST):

```powershell
& 'D:\\Pontius-tools\\py311\\Scripts\\python.exe' -B -P 'D:\\Pontius-handoffs\\v0a-i01-ab\\c-provenance-worker-v2-run-all.py' v2-green01 311
& 'D:\\Pontius-tools\\py311\\Scripts\\python.exe' -B -P 'D:\\Pontius-handoffs\\v0a-i01-ab\\c-provenance-worker-v2-run-all.py' v2-green01 314
```

| Slot | Result | Duration | Receipt |
| --- | --- | --- | --- |
| actual3.11.15, first | 36/36;0 failures/errors/skips;exit0 | {receipts[0]['elapsed_seconds']}s | {receipts[0]['receipt']} |
| actual3.14.6 | 36/36;0 failures/errors/skips;exit0 | {receipts[1]['elapsed_seconds']}s | {receipts[1]['receipt']} |

Both receipts contain identical source overlay hashes, full explicit target names,
interpreter/origin assertions, fresh r008 D-local snapshots, -B/-P, scrubbed environments,
snapshot cwd/src PYTHONPATH, D-local TEMP/TMP and absolute PONTIUS_GIT. Intermediate
v2-probe01 through v2-probe07 receipts are retained, including failures and the initial
misplaced delete hook and recursive-visitor error; final evidence supersedes no file.

## Scope and remaining verification

Git status contains only the two owned paths; diff --check exits0. Source/test bytes are
LF with no BOM. Main, A/B, other C, generated pair, expectations, sealed baseline and
capabilities, Git refs, ledgers and review reports were not changed by this worker.
Root also supplied `abc-provenance-v2-existing-test-preservation.json` independently.

No general Python object heap or dynamic descriptor inference is claimed. Unknown/stacked
decorators, ambiguous callable identity, reflective mutation and owner escapes without a
finite read-only proof remain conservatively refused. Known helpers that forward an owner,
store it, or invoke an unproved owner method can therefore gain explicit blockers. Initial
member mutation attribution is conservative across captured modules for the same resolved
owner; unrelated member spellings and deferred bodies do not invalidate other owners.

Root owns full combined generation, helper-edge/capability-row census preservation and
full affected suites before freeze. No corpus count is refreshed or claimed here, and these
focused runs authorize no guarded profile, GPU/capability execution, approval, source freeze,
commit or publication.

## Released identity

- generator SHA256 `{sha[owned[0]]}`
- test SHA256 `{sha[owned[1]]}`
- patch SHA256 `{digest(patch)}`
- patch: `c-provenance-worker-v2-final-owned.patch`
- machine-readable validation: `c-provenance-worker-v2-final-validation.json`
'''
save('c-provenance-worker-v2-final-report.md',report.encode('utf-8'))
artifacts=['c-provenance-worker-v2-final-owned.patch','c-provenance-worker-v2-final-validation.json','c-provenance-worker-v2-final-report.md']
hashes={'owned':sha,'artifacts':{name:digest((root/name).read_bytes()) for name in artifacts}}
save('c-provenance-worker-v2-final-hashes.json',(json.dumps(hashes,indent=2)+'\n').encode())
print(json.dumps({'released':sha,'patch_sha256':digest(patch),'methods_preserved':len(prior),'git_status':status,'green':[(r['slot'],r['summary'],r['elapsed_seconds']) for r in receipts]},indent=2))