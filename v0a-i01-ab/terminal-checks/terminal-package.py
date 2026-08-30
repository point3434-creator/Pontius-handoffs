import ast,hashlib,json,os,subprocess
from pathlib import Path
root=Path('D:/Pontius-handoffs/v0a-i01-ab')
work=Path('D:/Pontius-worktrees/codex-v0a-i01-terminal')
base='6cdf7b00dac653a9a295bbb86cdc3b5782317491'
paths=('src/pontius/v0a/trace.py','tests/test_v0a_trace.py')
git='C:/Program Files/Git/cmd/git.exe'
env={key:os.environ[key] for key in ('SYSTEMROOT','WINDIR','COMSPEC','TEMP','TMP') if key in os.environ}
def run(where,*args):
    return subprocess.run([git,'-c','safe.directory='+str(where),'-C',str(where),*args],
                          env=env,capture_output=True,check=True).stdout
assert run(work,'rev-parse','HEAD').decode().strip()==base
assert set(run(work,'diff','--name-only',base).decode().splitlines())==set(paths)
assert not run(work,'ls-files','--others','--exclude-standard').strip()
run(work,'diff','--check')
file_hashes={}
for path in paths:
    raw=(work/path).read_bytes()
    assert b'\r' not in raw and not raw.startswith(b'\xef\xbb\xbf')
    ast.parse(raw,filename=path)
    added=run(work,'diff','--unified=0',base,'--',path).decode().splitlines()
    assert not [line for line in added if line.startswith('+') and not line.startswith('+++')
                and len(line[1:])>100]
    file_hashes[path]=hashlib.sha256(raw).hexdigest()
for label,slot in (('green04-final','311'),('green05-final','314')):
    receipt=json.loads((root/'terminal-checks'/f'{label}-{slot}-receipt.json').read_text())
    assert receipt['executed_file_sha256']==file_hashes
    assert all(row['exit']==0 for row in receipt['results'])
    for row in receipt['results']:
        assert hashlib.sha256(Path(row['log']).read_bytes()).hexdigest()==row['sha256']
patch=run(work,'diff','--binary','--full-index',base,'--',*paths)
patch_path=root/'terminal-implementation.patch'
with patch_path.open('xb') as file:file.write(patch)
baseline=json.loads((root/'terminal-checks'/'baseline01-311-receipt.json').read_text())
base_snapshot=Path(baseline['snapshot'])
assert not run(base_snapshot,'status','--porcelain').strip()
run(base_snapshot,'apply','--check',str(patch_path))
report='''# Terminal follow-up implementation handoff

2026-08-30. Implementer ab_terminal_impl. This is an implementation report, not a
cold review or freeze. Branch codex/v0a-i01-terminal remains uncommitted at
D:/Pontius-worktrees/codex-v0a-i01-terminal, based on immutable r005 commit
6cdf7b00dac653a9a295bbb86cdc3b5782317491.

Only src/pontius/v0a/trace.py and tests/test_v0a_trace.py changed. No replay,
runtime, model, native writer, sealed kernel, publication or Slice C edits.
The producer contradiction separately reported by the coordinator (all proper
A script prefixes exhausting with failed terminal/reason null) is not repaired
or accepted here; the coordinator owns that replay correction.

## Implemented outcomes

T-02: Exact raw/key admission remains in the reader. Its four known pure event
constructors plus nested exact HandAction now supply primitive/card/order
validation. Constructor TypeError/ValueError becomes TraceInvalidError. Reader
context still owns contiguous stream position, unique initial start, stacks at
least the big blind, and one comparable showdown rank domain. Public reveal order
is preserved. Signed ranks, unequal-length same-domain tuples, and all-null ranks
remain structurally admissible; legal replay separately decides their legality.

T-01: One compact terminal helper runs unconditionally after values, counts,
timing and decision/failure pairing. Interrupted/unknown delivery forces all three
flags false. Unsuccessful/incomplete settlement is null. A failed hand retains a
reason. Complete accounting requires both finite category totals. An incomplete
aggregate may retain either completed category. Success retains the existing
complete/accounted/settled/timely/no-failure requirements.

Primary compatibility follows the Stage0 amendment: first-row code normally
agrees with terminal reason; an interrupted adapter failure can follow an earlier
terminal clock_invalid/clock_reversed; a prefailed reversed witness can record
clock_invalid with null timing. Arbitrary nonclock replacement is rejected.
No failure row is fabricated for host-only closure failure. The current schema
cannot reconstruct hidden source/body chronology or prove category values equal
measured work. These checks validate recorded implications only.

## Evidence

- Baseline: actual 3.11.15, 154 focused tests (45/34/53/22), all pass.
- RED02: unchanged r005 production plus new tests, actual 3.11.15, 14 test methods,
  73 intended missing-refusal failures. Every failure was TraceInvalidError not
  raised. RED01 retained one additional unsupported test expectation about
  preparation availability; it was removed before production edits. No expected
  behavior was derived from the new helper. Both receipts remain retained.
- Final 3.11.15 first: green04-final-311, 168 tests (45/48/53/22), all exit0.
- Final 3.14.6 second: green05-final-314, same 168 tests, all exit0.
- Each final trace suite includes 72 combinations (nine real outcome variants x
  eight complete/passed/accounting flags), independently rebound cause,
  settlement and category-total controls, all four wire event-constructor
  domains, ascending private and unsorted board positives.
- Real paths: accepted then interrupted, accepted then lost acknowledgement,
  genuinely rejected malformed input at the real ActionMailbox with zero real
  acceptances, delivered-late completed timing, no-start, rejected event order,
  malformed event, host-only settlement, and create-new writer refusal. The
  latter keeps its valid pre-publication trace distinct from failed host receipt.
- Clock sweep: every observed read on normal A (138) and rejected-input A (19),
  each under bool-invalid, reversed/invalid-first-read, and raised-exception
  sources: 471 schedules per final interpreter. Twelve cleanup-primary controls
  preserve event_order and reject replacing it with a clock cause. This is the
  observed schedule, not an exhaustive claim over possible future paths.
- Six actual source-before-adapter combinations preserve clock cause through
  acknowledgement, unknown exception, or genuine rejected nondelivery; prefailed
  witnesses and both opposing source/settlement-error orders also parse with
  their actual cause distinction.

Runner: run-terminal-focused.py. Receipts and full logs: terminal-checks/.
Every payload uses a fresh D-local clone/detach at the exact base with only the
owned overlay, -B -P, snapshot cwd, exact snapshot/src PYTHONPATH, scrubbed
allowlisted environment, PYTHONNOUSERSITE=1, and absolute validated Git. It asserts
executable/full version/flags and trace module origin before the test payload.
Final executed file hashes equal the delivered files; all log hashes rechecked.

Patch applies cleanly with git apply --check to the clean baseline snapshot.
Final diff --check passes; changed files are LF-only/BOM-free, syntax parses, and
no added line exceeds100 columns. Scope is exactly two tracked modified files,
no untracked paths. Git emitted its existing core.autocrlf warning about a future
checkout conversion; no global configuration was changed.

## Handoff limits

No broad tests, optional dependency/GPU work, source commit, freeze, ledger write,
ceremonial commit, push, integration or cold-review verdict. Coordinator owns
integrated verification, r006 freeze and two new independent cold contexts.
'''
report_path=root/'terminal-implementation-report.md'
with report_path.open('x',encoding='utf-8',newline='\n') as file:file.write(report)
artifacts=(patch_path,report_path,root/'run-terminal-focused.py',
           root/'terminal-plan-execution.md',
           root/'terminal-checks'/'red02-311-receipt.json',
           root/'terminal-checks'/'green04-final-311-receipt.json',
           root/'terminal-checks'/'green05-final-314-receipt.json')
receipt=dict(base=base,worktree=str(work),files_sha256=file_hashes,
             artifacts_sha256={str(path):hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in artifacts},
             patch_check_base_snapshot=str(base_snapshot),patch_check_exit=0,
             diff_check_exit=0,only_allowed_files_changed=True,no_untracked=True,
             final_test_bytes_match=True,final_log_hashes_verified=True,
             added_lines_at_most100=True,lf_bom_and_syntax_checks=True)
receipt_path=root/'terminal-checks'/'terminal-final-hashes.json'
with receipt_path.open('x',encoding='utf-8',newline='\n') as file:
    json.dump(receipt,file,indent=2);file.write('\n')
print(json.dumps(receipt,indent=2))
