# Cold review 01 - Codex - v0a-eval-panel-code/r003

Verdict: NOT CLEAN. Design verdict: STRAINED.
Two Important findings survive frozen-source verification. No Critical findings.
Specification: FAIL. Engineering quality: FAIL at admission and cleanup boundaries.
Confidence in both findings: high, by source control flow; no candidate execution performed.

Candidate commit: 7004285d883995de98161dafd766b18d7862cd46
Manifest SHA-256: 12e9ceddd6e366f2a5f4e9ebd1d6de2a8327a7ddbb732cf082f0906d544eab73
Ref: refs/heads/review/v0a-eval-panel-code/r003
Base/sole parent: f647a7989394f084875a040b20c41891168163ed
Tree: 850b111d83aa2755363eca1db25de454b8a0b4b4
Date: 2026-09-09. Reviewer: Codex, independent cold pass 01.
All locations below refer to blobs at the candidate commit, unless explicitly labeled BASE.
Every finding in this report binds to the full commit and manifest pair above.

## Important findings, severity ordered

### I-01 - A cleanup exception still skips pipe closure and retained event draining

Location: tools/v0a_eval_panel.py:335-363, especially 338-347 and 354-358.
Related paths: tools/v0a_table_host.py:430-447; tool main at 434-448.
Contract: handoff ownership item 1; implementation brief criteria 3 and 9;
completed stage observations must survive subsequent failure, and all owned resources must
receive their cleanup attempts. This is a residual of accepted r001 category A, with a
consequence also on category G retention.

Concrete failing schedule: the assigned worker emits a production event, the stdout reader
queues it, and the watchdog leaves its loop before that event is drained. During cleanup,
the real Job.active query at line 338 raises HostRefusal("cleanup_failed") because its native
query failed. That method explicitly raises on a failed QueryInformationJobObject call.
Control jumps to line 354. The fallback only polls and kills the process. It does not wait,
join the readers/sender, close any of the three pipes, or drain queued events. The nested
finally does attempt Job.close, but closing a Job does not close Popen's parent pipe objects
or convert the queue into report observations. A report can therefore lose an already
emitted completed stage and return with unclosed pipes and no reaping verification.

The same skipped suffix occurs if terminate, wait, a join, or an earlier stream.close raises.
If the fallback poll/kill itself raises, supervise can escape without returning its report;
main then retains its original empty report rather than the already assembled observations.
These are control-flow consequences of the frozen source, not claims that the snapshot run
observed these schedules.

Assignment refusal itself is corrected: assigned stays false, the suspended process is
killed, and the supplied real-launcher test verifies that ordinary rollback path. Job.close
is now protected by a nested finally. The remaining defect is that all other cleanup actions
still share one try block, despite the coverage claim that every step has its own guard.

Smallest correction: make termination/reaping, each pipe close, thread completion and final
event draining independent bounded cleanup attempts, retaining each failure while ensuring
later attempts run. Preserve the report even if fallback termination fails. Keep Job.close
in unconditional final cleanup. Do not alter the sealed Job owner to repair this caller.
Verification: through the real launcher, control one cleanup query/operation failure after a
stage is independently observed, then assert process exit, each pipe closure attempt, retained
stage data, failed cleanup status and the original cause. Include a fallback failure schedule
that cannot discard the report. No such fault schedule is in the supplied 22 cases.

### I-02 - Cardinality alone lets an incomplete sample become declared-full evidence

Location: tools/v0a_eval_panel.py:120-134, especially 131-134.
Related paths: run_plan at 213-229; hand assembly at 288-298; estimate at 390-406;
main at 439-444; tests/test_eval_panel_tool.py:76-103.
Contract: implementation brief at BASE, lines 80-82 and 101-109: the four named development
hands on the declared board and royal-spade/2c 3d control must be measured. Handoff admission
item 2 explicitly forbids a test subset passing as declared-full. This is a residual of
accepted r001 category D.

Concrete input: take the frozen plan-preflight.json and replace development_hands with four
copies of ["As", "Ad"], retaining coverage="declared-full", the correct board, identities,
permutation, runtime, resource limits and the existing royal control. All admission predicates
pass: the hand list has length four, every element has two cards, and there is one control.
No check requires Kh Kd, Td 8d or 3c 4d, uniqueness, or the declared sample membership.

With enough finite time to finish these valid singleton calculations, the worker performs
As Ad four times and the control once. The parent keys hands by label/board/hand, so each As Ad
repetition overwrites the previous stages in the same record. It can return completed with
coverage declared-full, only one development record, and full_pool_estimate.kind="estimate"
with sample=1. The retained production cost is the last, warmed repetition while the estimate
assumption says the first sampled hand is cold. Three mandatory hands were never evaluated.
The existing test rejects a one-element list, so it cannot detect this admitted counterexample.

The control is also bound only by count and object keys. Replacing the required royal-board
control with another valid board/hand passes admission, as does a consistently rebound
non-development board. These are related members of the same missing semantic admission rule.

Smallest correction: validate declared-full against the actual required development board,
canonical distinct hand membership, and exact required control identities before launch.
Keep arbitrary subsets explicitly labeled test-subset. If extra/repeated measurements are
intended, assign occurrence identities and reconcile completed required members rather than
merging repetitions by hand; otherwise reject duplicates. Require the required completed
sample before issuing a full-sample estimate, and derive cache assumptions from retained data.
Verification: count-preserving duplicate and substitution plans must refuse before a worker
exists; the valid full plan must still pass. Exercise duplicate handling and required-member
reconciliation through parent report assembly, not solely by asserting list lengths.

## Design verdict

STRAINED. The root replay, per-hand kernel enumeration, singleton reference and exact lattice
comparison are appropriately narrow and readable. The new tool still carries two authorities
for sample meaning (plan counts and merged observations), and the supervisor copies the
workload pattern without making cleanup independently exhaustive. The surviving defects are
concrete evidence of those stresses. A bounded correction to admission and the caller's
cleanup/report assembly is preferable to replacing the arithmetic or reopening sealed code.
A shared general orchestration framework is not required to close these findings.

## Identity and cold-review discipline

I first read the handoff, required verification skill, pinned workflow/rulings/dependency list,
and frozen implementation brief/design. I recorded my own invariant/related-path inventory
before opening coverage.md, checks/, or inputs/prior-disposition.md. I subsequently read that
permitted disposition and compared its categories against my inventory. I read no prior-round
review, sibling reviewer output, implementer transcript or conversation context.

The original pre-deferred inventory remains unchanged at:
D:/Pontius/tmp/eval-code-r003-review-01-inventory.md
SHA-256: 4453a8c2aded55e9594991e159e9b8b3d585185952dbb2599ef91187d8dbc931
It had 13 table rows of 101-108 columns. With coordinator authorization, I preserved it and
created a separate formatting-only publication copy, converting its table to wrapping bullets.
No invariant, related path, requirement or coverage claim was added, removed or altered.
Publication inventory:
D:/Pontius/tmp/eval-code-r003-review-01-inventory-reflowed.md
SHA-256: 41eed096e8878bad1a911e5467f88f4023fd283e5ae77d897bef0e461c6d5d3a

Independent Git reads resolved the stated ref to the stated commit, sole parent and tree.
The changed scope is exactly the seven handoff paths. SHA-256 of each frozen changed blob,
whole-row ordinal byte ordering of the ASCII hash/path rows, two spaces before the POSIX path,
and LF after every row reproduce manifest.sha256 byte-for-byte and its declared digest.
All 34 direct dependency blob pins match BASE. All input and check digests explicitly pinned
in the handoff, including coverage.md and prior-disposition.md, match their stored bytes.
No ref fetch was needed and no Git mutation was performed.

The packet also contains a later, unpinned controller-rulings-addendum-2.md. Its observed hash:
0b708f7619c25167a51d55f8af00baa3cedc3e8a85e0a80511c18bd178e93dfa
I treated its quoted budget ruling as additional controller input, not as part of the frozen
manifest or as an implementation correctness receipt.

## Independent inventory compared with supplied coverage

- Identity, scope and text hygiene: independently verified from Git bytes. No sealed path
  changed. Both suites are added to cases.json; no existing registration was removed.
- Admission: closed phase key sets, exact ordered permutation and universe binding, finite
  seconds/non-bool checks, exact memory checks, parse constants and 1e999 refusal are present.
  The count-only full-sample rule misses inventory members identified in I-02. Arbitrary
  control/hand strings are also parsed later in the worker rather than fully at admission.
- Domain and arithmetic: s=3 and s=6 are refused at teacher/reference/tool entries; the bet is
  constant raise_to(2). Kernel settlement supplies integer totals with CHECK on exact ties.
  The reference builds a singleton hero game with 990 raw-1.0 distinct villain deals, explicit
  CALL policy and separate forced-action and best-response calls. Frozen evaluator/control
  flow supports the claimed domain-specific lattice bound; no arithmetic defect found.
- Capacity: keys come from the real replay and key builder; actual codec wire bytes drive the
  prefix search. Boundary bytes are returned, base64 transported and written with path,
  length and digest on the successful retention path. No solver runs in capacity.
- Stage retention: the real budget-kill case covers ordinary cleanup after production. The
  event assembly preserves completed stages and marks missing stages. Cleanup faults remain
  outside that test and violate retention as described in I-01.
- Ownership: actual assignment refusal, capacity completion and a finite budget kill exercise
  the real launcher and Job. They do not exercise cleanup-query, wait, close or fallback
  failures. The category claim of separately guarded steps is contradicted by source.
- Request transport: the initial send runs on a daemon thread, allowing the watchdog to run
  while stdin fills. The supplied coverage explicitly admits no pipe-fill test. Static
  correction of the synchronous stall is established; its real-boundary regression coverage
  remains incomplete, and sender/pipe cleanup is subject to I-01.
- Run record: main now places work after admission inside try/finally, catches interruption,
  sets the run directory before writing runtime/plan outputs, normalizes nonfinite report
  values and calls finish_run once. The two owner tests use the real result/journal writers
  in disposable repositories while replacing supervise; separate tests cover the launcher.
  They establish successful/refused-plan ownership at those seams, not a complete real-worker
  main invocation, interruption, directory-write failure, or cleanup-fault retention.
- Export/agreement/full-pool mechanisms are absent as required for steps 1-3. The bank fields
  are explicitly refused for these phases; later agreement admission remains deferred.

The inventory method and supplied data-path method substantially agree. The discrepancies are
specific missing members, not a claim that every untested path is defective. Separate residual
coverage gaps include an actual pipe-fill schedule, cleanup faults, an interrupted main, and
parent-side boundary-file round-trip assertions. These gaps are not additional product findings.

## Executed evidence and commands

No project code, tests, solver, host, owners or measurements were executed by this reviewer.
Only Git object reads, packet text reads, mechanical hash/census operations and create-only
review-output writes were performed. Production/test source and lifecycle state were unchanged.
Read-only command families: git show, ls-tree, rev-parse, diff-tree and diff, all using
-c safe.directory=D:/Pontius; PowerShell/.NET raw-byte SHA-256 and text hygiene checks.
The candidate source was read from Git objects, not the dirty working tree.

The pinned supplied receipt records this disposable-snapshot command:
python -B -P -W error::ResourceWarning -m pytest -p no:cacheprovider -q tests/test_pontius.py
with -k "eval_bridge or eval_panel_tool"; CPython 3.14.6 and a snapshot-local dev environment.
The receipt says env -i with SystemRoot, TEMP, TMP, PONTIUS_GIT and PYTHONDONTWRITEBYTECODE;
Git is C:/Program Files/Git/mingw64/bin/git.exe. Pytest: exit 0, two harness parameters passed,
44 deselected, 66.17 seconds. The pinned journal states 22 unittest cases, zero skipped,
source_verified=true, and source_commit equal to this candidate. The reviewed tests include
real sealed checks for the royal tie and nonzero As Ad, plus independent arithmetic fixtures.
These are supplied executed results verified by packet hashes, not a new reviewer rerun.
They do not falsify the two source-derived schedules above.

Independent raw-byte census agrees with the receipt: bridge 333 lines, tool 459, tests 198 and
230: 792 production and 428 test lines. All seven changed paths are LF-only, BOM-free, have no
trailing whitespace and have no line over 100 columns. Fixture data are excluded from budget.

## Budget and disposition limits

The 1,000-1,100 production-line completion projection is a planning estimate, not a measurement.
The original brief's 600/400 budget was raised by controller statements; the later addendum
records working figures of 1,200/600 and interprets the controller's concern near 3,000 as a
ceiling. Exact governance of that number is a controller decision, not a source defect or a
reason to compress the code. This checkpoint's counts and its remaining work must stay visible.

NOT CLEAN means this pass does not clear the candidate for subsequent gates. Required work is
I-01 and I-02, followed by appropriate bounded evidence and a fresh immutable correction round.
No source correction, retained experiment, full-pool solve, ceremonial commit or integration
is implemented or authorized by this review.
