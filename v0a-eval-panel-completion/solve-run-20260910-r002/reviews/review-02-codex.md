# Independent cold review 02 — Codex

**Verdict: NOT CLEAN — one Minor exit-contract documentation discrepancy.**
**Findings: 0 Critical, 0 Important, 1 Minor.** No material reachable operational failure
was established for this candidate's documented, exclusively owned invocation path.

**Specification verdict:** the concrete solve plan, bindings, resource envelope, reservation,
record checks and attribution satisfy the operational obligations reviewed below. The
unqualified exit-99 promise does not describe the implementation (M-01).
**Engineering-quality verdict:** SOUND for the proposed retained solve under the stated
operator-ownership assumptions; fault coverage and failure-record guarantees have the limits
below. This review supplies no invocation or publication authorization.

Packet-relative citations refer to
`D:/Pontius-handoffs/v0a-eval-panel-completion/solve-run-20260910-r002/`.
Source citations refer exclusively to frozen Git blobs at
`1c7067448106cfa2aca3d57be879842d72293c61`, not behavioral worktree reads.

## Immutable inventory and independence

CONTEXT_PROBE_NONE was stated before opening any packet/source. No memory summary, project
history, candidate verdict or finding was injected. I was the sole reviewer; no delegation
or reviewer contact occurred.

Inventory: `D:/Pontius/tmp/solve-r002-cold-20260910/reviewer-02/inventory-02-codex-cold.md`

SHA-256: `90180d2de9e15a5896037e70733b7bc3136c19b46b7ea5a790fb3e628b11574f`

It was written and hashed after steps 1–3, before any step-4 input, and never revised.
Manifest names were read early to enforce the allowlist; member verification waited until
after the ordered content reads. Step 6 was opened only after the seal and independent
candidate/control-flow inspection and calculations. Exposure is disclosed below.

## Finding

**M-01 — Minor: the blanket exit-99 contract omits child-failure precedence.**

Locations: `authorization-request.md:31`; `invoke.sh:15–18` and `invoke.sh:140–141`.
The authorization binding says anything short of complete evidence exits 99. The executable
first returns any nonzero child status at line 140, and reaches the evidence/99 decision only
when the child returned zero.

Concrete reachability: after preconditions and the successful start append, a transient Git
read failure in `begin_run` can terminate the Python entry before its report-owning
try/finally (`tools/v0a_eval_panel.py:630–633`). No journal row appears. The helper reports
ABSENT/3 (`journal_attribution.py:27–29`); the wrapper sets evidence incomplete at line 117,
records the end state at lines 134–136, then returns the child's status (ordinarily 1), not
99. A failed child plus a later evidence-write failure has the same precedence. This is a
static reachable trace; I did not execute a fault.

Governing obligation: handoff step 2 makes the predicates/exit codes part of the invocation
binding, and acceptance question 1 requires faithful recording of incomplete evidence.
Consequence: an operator or future caller classifying incomplete evidence solely by the
promised exit 99 can misclassify this outcome. The existing checks do not test this compound
failure. No such automated production consumer was supplied, so I do not claim an observed
misclassification or a material launch-safety failure. The command remains nonzero, the
claim stays consumed, and the end record identifies incomplete evidence when writable.

Correct the prose to say that nonzero child status takes precedence, with exit 99 reserved
for a zero-status child whose evidence is incomplete; alternatively change and verify the
exit policy. No repair was performed. This Minor does not reopen the prior unchecked-write
finding: the unsafe successful-exit path is closed.

## Acceptance and closure/evidence matrix

| Question / prior issue | Independent result and evidence | Assessment |
| --- | --- | --- |
| 1. Reservation | `invoke.sh:77–94`: preexisting records refuse; atomic `mkdir claim.d` precedes start and the sole launch. Claim is never removed. C9 loser reaches the failed mkdir. | Prior I-01 closed. |
| 1. Rehearsal/roots | Fixed constants at lines 23–24; retained overrides refuse at 43–47. Rehearsal requires an explicit different physical path and detached HEAD at 49–55. | Prior 01/I-02 and 02/I-03 closed for documented callers. |
| 1. Records | Lines 88–94 check claim/start writes; 97–103 use noclobber; 111–136 propagate capture/hash/list/end-write failures. A zero child cannot yield wrapper zero with those failures. | Prior 01/I-03 and 02/I-02 closed; M-01 qualifies exit numbering. |
| 1. Attribution | Helper lines 24–60 require exactly one additional row, adopted commit, existing result/digest, and runtimes digest when present. No tail substitution. | Prior I-04 closed within the actual producer boundary. |
| 2. Executed checks | Seven expected refusal exits; six helper outcomes; C9 records A=97/B=0 and one capture, with B's result/file list matching rehearsal. | Supported by script and captures, with coverage limits below. |
| 3. Rehearsal | Raw/normalized hashes, row, claim/log, ordered census and reconstructed teacher agree. | Consistent rehearsal; never retained evidence. |
| 4. Residual ownership | Authorization content, persistent claim, exclusive checkout/journal use, stable files and mirroring remain operator responsibilities. | Explicit assumptions, not hidden guarantees. |
| 5. Manifest/campaign | All 26 hashes and whole-row LF reconstruction agree. Memory discussion distinguishes worker Job/parent and growth with bank and H. | Prior manifest and memory findings closed. |
| 6. Forbidden claims | Solve inputs are empty; later phases require bound producers. Request lines 47–49 and campaign lines 91–94 withhold later authority. | No teacher-strength/full-host-agreement proof or later authorization. |

## Identity, admission and actual boundaries

HEAD and remote adopted branch both resolve to `1c7067448106cfa2aca3d57be879842d72293c61`.
The tree is `3d2fe79d2af20125e322dd4a668335e789810863`, also the named completion candidate's
tree. Execution branch is `claude/eval-panel-solve`; status is only `?? plans/`.
All 892 source-scope files match batched frozen blobs after the producer's permitted newline
normalization; the name sets agree. Identity-only raw hashing yields
`bac14bea3e9a4e4c8c120556311447262d7775de54e39ef121c02bb2c59eb204`.
The seven on-disk run names equal the tracked census. Bound path ancestry has no reparse points.

The 26-member manifest reproduces byte-for-byte:
`8acaaa389fc152e4127e98fe879df758fd819961085c717dd5c2601b9d145f1a`.
Both plan copies are 12,365 identical bytes:
`c1a6af606cc80841d61b5824913c8a1b6c896988ae4c578127c1dfc08b4f8982`.
The helper pin agrees. Capacity/preflight/decision bytes match all three frozen constants
(`tools/v0a_eval_panel_completion.py:18–22`); capacity/preflight record completed cleanup,
matching permutation, and preflight sample completion.

Static admission tracing covers entry `validate_plan:131–196` through completion
`validate:97–146` and `OwnedInput` at `tools/v0a_table_host.py:118–136`. Independent stdlib
checks establish the exact 15-member plan, board/prefix/stacks, runtime declaration, empty
inputs, full universe and seeded order. Universe digest is `18953f11…`; permutation is
`344e7eeb…`, with every ordered hand matching. The fixed 600 seconds / 2048 MiB agrees with
resource-decision lines 10–22 and completion lines 133–135. No project validator was executed.

The actual path is wrapper -> entry `main` -> `begin_run` -> fresh UUID directory and
runtimes -> supervisor/worker -> completion solve -> artifact retention -> `finish_run` ->
`append_run` -> wrapper helper. Solve enumerates one hero at a time; bridge
`hand_totals:210–236` calls the ranker and real kernel settlement. Completion lines 386–397
reconcile the ordered census/tie reference. Retention lines 466–487 verifies teacher bytes
before completed publication. Execution lines 128–161 writes a root-contained relative
result, then its digest-bearing row; `status_generation.py:28–35` appends one LF JSON object.
Thus the helper's absent-row branch covers a real early failure without borrowing history.

## Check and rehearsal coverage

C1–C7 captures agree with exits 88/89/87/86/85/97/83. Each refusal predicate precedes launch;
receipt notes say no stdout capture. Their former case directories are outside permitted
inputs, so absence was not independently re-observed. C8 covers ABSENT, EXTRA, wrong commit,
wrong result hash, BOUND and CRLF BOUND; rejected rows are recorded as unwritten. It omits
malformed/nonobject rows, missing files, runtime mismatch and helper write failure. The
harness's `pass` field compares exits (`checks/wrapper-checks.sh:17–19`); capture absence,
row creation and launch count are notes, not additional pass predicates. C7 tests directory
creation failure, not failed start/end appends or postlaunch disk-full conditions.

C9's losing capture ends at the exclusive claim; the winner reports exit zero, 19 seconds,
BOUND and complete evidence. The winning retained-file text equals rehearsal's list.
The log has one start/end and rows 59 -> 60; the original journal is unavailable, so those
counts remain captured observations rather than an independently recounted journal.

Stdout is 527,215 raw CRLF bytes, SHA-256 `83ea709c…`; LF normalization gives 527,214 bytes
and `af86256d…`, exactly the journal's result digest. Stderr is empty; row digest is
`94a2b01c…`. There are 1,081 teacher observations plus artifact and summary, in exact plan
order: 545 raise-to-2, 536 check, zero action-value ties. Outcome totals, denominator 990
and maximizing actions reconcile. Independent canonical serialization of those rows yields
241,587 teacher bytes and
`c3ffab403eb7e939857cc31b0f21b255cefdffd8b0d26d078b703c1fe956b3e3`.
Production min/mean/max/sum are 0.0130929/0.0140868/0.0666608/15.2278551 seconds;
worker time is 15.7722 seconds, Job peak 786.9141 MiB. Receipt rounding agrees.
These calculations do not independently rerank poker hands or remeasure native cleanup.

## Ownership, campaign and limits

The claim is per packet, not a global authorization registry. Abandoned claims, a second
packet/authorization, removal of consumed records, concurrent direct project invocations,
postcheck source/file changes and backup retention require controller/operator ownership.
Authorization is an existence check, not authenticated content validation. Detached HEAD
alone does not prove a selected rehearsal checkout is disposable. Documented mode values
are 0/1; arbitrary flag strings are not validated as JSON before log interpolation.

The helper assumes the producer's JSON object and relative output convention; it is not a
general hostile-journal validator. Absolute/traversing paths or a forged newly appended old
result could defeat stronger attribution claims, but the inspected producer does not emit
those inputs. Another journal writer violates the exclusive-owner assumption. Likewise,
the file list enumerates existing fresh-run files rather than enforcing an independent
required-file schema; successful solve/retention supplies that set. These broader input and
ownership limitations are not demonstrated defects in the current producer/caller path.

Campaign lines 68–81 match the code: witness draws are retained and emitted, scan report
retains them again, and each host Session result is accumulated in worker results and
parent observations. `supervise:433–452` assigns the worker to the measured Job, excluding
its parent; completion `play:305–310` calls real Session.run, whose host launches a real
adapter child. One four-hand receipt (1,560.2 MiB; 20,128,357 result bytes) supplies no larger
memory forecast. Full-pool bank estimates and 37,586-byte wire headroom recompute. Later
phase input bindings at completion 229–255 enforce completed producer identity. Chain raw
captures are unavailable within scope; their execution claims remain receipt-only.

## Exposure and method disclosure

Before sealing, mandatory handoff/identity exposed r001 NOT CLEAN, four Important wrapper
issues, prior passing plan/identity/envelope/census claims, proposed fixes and adoption
approval language. After sealing, authorization-request repeated these; campaign named
prior M-01/M-02; rehearsal stated historical teacher equality. At step 6 I inspected both
r001 reviews' findings/verdicts and evidence summaries, their coordination and disposition:
four Important wrapper defects, manifest grading disagreement (Important versus Minor;
coordinator Minor), and Minor memory wording. Those documents also relay earlier
CLEAN/SOUND/GREEN adoption and prerequisite finding language. These historical claims were
not adopted as my verdict. Governing excerpts mention accepted semantics and resource
approval; they confer no invocation authority. No additional adoption reports were opened.

Current reviews/disposition, unmanifested checks, other scratch/logs, ledgers, INDEX,
memories and conversation history remained closed. All project/checkout operations were
read-only; worktree source bytes were used only for identity hashing. Utilities were
PowerShell/.NET and the exclusively specified CPython 3.14.6 with -I -B. Its initial sandbox
launch was denied; read-only escalation succeeded. No required check remained blocked by
approval review. I did not run the checkout interpreter, verify package installation by
execution, import project code, run any script/test/solve/export/agreement/rehearsal, mutate
Git/source, or publish. Deleted rehearsal runtimes/teacher originals and chain raw captures
were not substituted from elsewhere. Only the two requested exclusive-scratch artifacts
were written; the coordinator retains their bytes and owns ledger work.
