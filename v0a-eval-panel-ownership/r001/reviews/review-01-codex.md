# Cold review 01: eval-panel ownership r001

Reviewer: Codex. Date: 2026-09-09. Independent cold pass; no implementation role.
Candidate: 182d14e213c6f0b7d7578e429f81d051a9e59707
Manifest SHA-256: 438d192a26e39b216cca33099c79f6f607de8e2ec1ca1749d44a50434bc7f6f6
Base: 0bc19bcaad5c6660468094772216cac2dc27a651
Tree: 81f2e97805bcaf9e93a05b98ecc4277e1c2dd32c
Ref: refs/heads/review/v0a-eval-panel-ownership/r001

Verdict: NOT CLEAN. Specification: FAIL. Engineering quality: FAIL on cleanup state.
Design verdict: STRAINED. One Important finding and one Minor finding; no Critical findings.

The supplied RED/GREEN evidence supports the three targeted repairs. However, a late
console interrupt can still leave cleanup_verified true alongside a recorded cleanup
interruption. Native Job acquisition also occurs before the release protection begins.

This review covers cleanup, caller-owned observations and boundary publication only.
The sample-role contract is a separate dependent candidate, not an unaddressed finding
in this scope. This verdict does not certify that separate contract or design steps 4-7.

## I-01: late SIGINT leaves a true cleanup certificate beside an interrupted outcome

Severity: Important (bounded evidence-contract failure). Confidence: high, static proof.
This schedule was not executed by this reviewer; no runtime reproduction is claimed.

Frozen locations, all at the candidate above:

- tools/v0a_eval_panel.py:275-277, the installed handler changes status and cleanup only.
- tools/v0a_eval_panel.py:448-450, cleanup_verified becomes true after successful cleanup.
- tools/v0a_eval_panel.py:282-284, that handler remains installed during context exit.
- tools/v0a_eval_panel.py:451-456, subsequent code never invalidates the certificate for
  an already interrupted status.
- tools/v0a_eval_panel.py:552-568 and src/pontius/execution.py:140-156 retain that report.

Concrete counterexample:

1. Run the valid capacity fixture through main, with the real worker and successful native
   cleanup. Resource observations and all cleanup outcomes are successful.
2. Lines 448-450 assign cleanup_verified = True.
3. Deliver one SIGINT while the context manager executes its finally block, immediately
   before restoring the previous handler at line 284. The current handler is still the
   function at lines 275-277. It sets status = interrupted and records
   cleanup["console interrupt"] = interrupted, but leaves cleanup_verified = True.
4. The restored context exits normally. The conditional at line 451 only handles completed
   status, so it cannot correct this state. Main retains an interrupted result with a true
   cleanup certificate and a recorded cleanup interruption.

This is one ordinary console-interrupt timing, not a failed storage device, an externally
killed parent or a simultaneous-fault assumption. All resources may actually be released;
the defect is the contradictory certificate under the explicitly declared contract.
Coverage invariant 1 requires that a recorded cleanup failure/interruption cannot coexist
with a true certificate. The deferred disposition likewise requires monotonic invalidation.

The new test at tests/test_eval_panel_tool.py:416-450 interrupts after native Job.close,
before the certificate assignment. The existing interrupted-wait test at 251-262 also acts
before it. Neither reaches this later transition, so their GREEN results do not refute it.

Required correction: make interruption and certificate validity one coherent state
transition. A newly recorded cleanup interruption must invalidate any prior certificate,
and a certificate assignment must not overwrite an interruption arriving during its own
finalization. Preserve the single owner and the existing release behavior.

Required verification outcome: in a disposable CPython 3.14.6 run, keep the real worker,
releases, main and result/journal writers. Trigger the installed SIGINT handler immediately
after certification and before handler restoration. Observe one interrupted result and one
journal row, retained observations, and cleanup_verified false whenever cleanup records an
interruption. Also challenge the assignment boundary; an earlier false value alone does not
prove a later assignment cannot restore true. No project or test change was made here.

## M-01: the successful Job acquisition is outside the cleanup owner

Severity: Minor. Confidence: high, static proof; no execution claimed.
Locations: tools/v0a_eval_panel.py:315-324, 374-375 and 434-447;
tools/v0a_table_host.py:326-446, all at the frozen candidate.

After host.Job returns successfully at line 316, deliver KeyboardInterrupt at line 317
before queue allocation. No worker exists yet. The cleanup try/finally and interrupt
handler have not been entered. Main catches the interrupt, but no path calls job.close.
Job owns an integer native handle, has no destructor, and only explicit close consumes it.
The native job handle therefore survives until process exit. The report has no cleanup
outcome for it because report initialization also occurs after acquisition.

This violates the packet workflow's ownership-timing rule: each handle must have a release
owner before another fallible step. Coverage says its discovery traces Job acquisition
through release, yet its protected region starts later. The impact is bounded: this
schedule creates no orphan worker, and process exit releases the otherwise leaked handle.
That limited reach is why this is Minor rather than another Important finding.

Correction direction: initialize ownership/report state before acquisition, and protect
successful acquisition through release in the same lifetime. Keep Job itself unchanged.
Verification: after a real Job is returned but before any worker launch, interrupt the
caller and independently observe exactly one native close, no child, and one interrupted
result/journal row. Do not fabricate a successful close or retry a consumed numeric handle.

## Design assessment

STRAINED applies to the remaining cleanup boundary, not the whole bridge. Attaching stage
records directly to observations and registering intended publication identity before
rename are useful reductions in duplicate state. The remaining cleanup boolean is still
an independent cached projection while the SIGINT handler can mutate its inputs afterward.
Acquisition and protected cleanup also have different lifetime boundaries.

A bounded adjustment in the tool can put acquisition, interruption state and terminal
certificate validity under one owner. Preserve real suspended launch, independent release
attempts, bounded stream closure, caller-owned observations and existing result writers.
The tradeoff is careful transition-order testing; a general lifecycle framework or bridge
rewrite is not justified. Another guard before final cleanup would leave I-01 intact.

## Independent inventory and deferred coverage comparison

The initial inventory was created before opening coverage.md, checks/,
inputs/prior-disposition.md or inputs/repair-plan.md. Its immutable staging name is
`eval-ownership-r001-review-01-inventory.md`, SHA-256:
11b633049b45d943d23626603d041df4d77ca5f542fe2b18e315e5325a6a4ee9

Discovery followed the complete changed tool and test diff, then resource, observation
and publication ownership into frozen Job, execution and status-generation consumers.
No implementer transcript, other conversation, sibling output or prior review report was
read. The specifically permitted deferred disposition was read after the inventory.

| Requirement/risk | Evidence and outcome |
| --- | --- |
| Final release affects certificate | Real post-close failure RED/GREEN supports repair |
| Any cleanup interruption invalidates | Interrupted-wait covered; I-01 survives |
| Job acquisition owns release | Source lifetime trace exposes M-01 |
| Suspended assignment failure | Existing real supervisor control kills unassigned worker |
| Drained observations survive unwind | Real post-close interruption RED/GREEN supports repair |
| Partial stages remain explicit | Existing budget control and in-place stage fields |
| Stream close is bounded | New real pipe backpressure control; pending cleanup fails |
| Rename has prior identity | Real rename-then-interrupt RED/GREEN supports repair |
| Failed write keeps pending bytes | Existing second-write/retry control and source trace |
| One result and journal per tested run | Real clone tests compare count and result-byte hash |
| Exact identity and scope | Fresh Git/.NET byte checks pass |

Coverage identifies the right main paths and supplies behavioral rather than merely
structural tests. Its limits on simultaneous faults, dead storage and externally killed
parents are reasonable. They do not exclude the single late-SIGINT schedule in I-01.
Publication reconciliation preserves the registered intended identity and recoverable
encoding if a later read cannot complete. No additional publication defect is established.
No false cleanup certification is inferred merely because a daemon closer remains pending;
the timeout is recorded and prevents certification for that tested path.

## Identity and evidence verification

All source inspection used frozen Git objects. Read-only Git used safe.directory=D:/Pontius;
byte verification additionally used --no-replace-objects. No working-tree source was read.
There is no tracked AGENTS.md in the frozen candidate tree. Applicable instructions came
from the packet workflow, governing brief/design and the verification skill.

Fresh PowerShell/.NET verification, exit 0:

- Ref resolves to the stated commit; sole parent and tree match candidate.json.
- Candidate differs from BASE only in tests/test_eval_panel_tool.py and
  tools/v0a_eval_panel.py: 146 test additions; 149 tool additions and 76 deletions.
- Recomputed each changed blob's SHA-256, sorted whole hash/path rows ordinally, encoded
  exact LF rows, and compared manifest bytes and its recorded SHA-256. All match.
- All 16 handoff input/check pins and the deferred coverage SHA-256 match packet bytes.
- All 34 dependencies.json blob pins match its original base
  f647a7989394f084875a040b20c41891168163ed, not the immediate candidate parent.
  These historical pins establish provenance; they are not claimed as current-file hashes.
- Changed source files are LF-only, BOM-free, have no trailing whitespace and fit 100 columns.
- RED cf47853df2c17723a162792db6910021652d2f20 has the rejected BASE as sole parent and
  changes only the test file, with 115 additions. Production remains the rejected source.

Read-only commands were git show, ls-tree, diff and rev-parse, plus PowerShell Get-Content,
Get-ChildItem and .NET process/byte/hash utilities. No candidate, test, owner or Python code
was run. One initial read targeted a nonexistent skill path and failed without reading data;
the actual applicable skill was then read. The first draft inventory failed its in-memory
column check; it was corrected before its only create-only file write.

Supplied execution evidence, read and hash-verified rather than rerun:

- Both receipts name CPython 3.14.6 and disposable snapshot-local interpreters with
  -B -P -W error::ResourceWarning, scrubbed environment keys and PONTIUS_GIT.
- Command: pytest -p no:cacheprovider -q tests/test_pontius.py
  -k "eval_bridge or eval_panel_tool".
- RED: exit 1, 30 unittest cases, zero skipped. Stdout identifies exactly three assertion
  failures: final-release certificate, lost drained stages and unbound renamed artifact.
  There are no unittest errors; both pytest wrapper and journal retain failure.
- GREEN: exit 0, 31 unittest cases, zero skipped; stdout reports two pytest wrapper tests
  passed, 44 deselected. Frozen harness inspection explains the wrapper/case distinction.
- Both journal copies name the corresponding frozen source and source_verified true.
  Result hashes are supplied journal assertions; their external retained result files were
  not opened because the packet was the sole substantive input.
- Both stderr files are empty. Coverage reports Ruff success, but no separate Ruff command
  receipt is pinned here; it is not elevated to independent executable evidence.

No new runtime RED reproduction is part of this review's evidence. The failure verdict
rests on explicit frozen-state counterexamples; supplied GREEN establishes only its tested
schedules. Deterministic new regressions and fresh focused receipts are required for a fix.
No broad suites, retained capacity/preflight run, full-pool solve, integration, source edit,
owner invocation or Python utility execution was performed or authorized by this review.
