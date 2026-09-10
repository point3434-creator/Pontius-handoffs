# Independent cold review — reviewer 01 (Codex)

Verdict: **NOT CLEAN**.
Specification verdict: **NOT CLEAN for the complete execution packet**. The concrete solve
plan satisfies the frozen admission predicates and the controller's resource decision;
the invocation does not enforce the specified one-shot and failure-retention contract.
Engineering-quality verdict: **NOT SOUND for retained invocation as packaged**.
Findings: **0 Critical, 5 Important, 1 Minor**.

Packet: D:/Pontius-handoffs/v0a-eval-panel-completion/solve-run-20260910/
Source: 1c7067448106cfa2aca3d57be879842d72293c61.
Review identity checks completed 2026-09-10T03:09:48Z; report written afterward.
Scope: the complete solve packet, including admission, identities, one-shot execution,
interruption, retention, repetition, rehearsal consistency, campaign sequence and claims.
This is one reviewer of the user's expressly requested two reviews, not their coordinator.
The current request overrides the packet's ordinary one-review count and output locations.
No source repair or packet modification was performed. This report grants no invocation.

## Independence, read order and sealed inventory

**CONTEXT_PROBE_NONE** was stated before opening any packet or source. Inherited context
contained the current request, generic tools/environment/safety instructions and the supplied
AGENTS.md joke instruction. No memory summaries, prior project history, candidate verdicts
or findings were injected. There was no basis for CONTEXT_ABORT at that initial probe.

I followed the prescribed sequence:

1. handoff.md, then identity.json.
2. plans/solve.json against frozen validate_plan and completion validate, then their source
   admission, solve, supervision, completion and retention dependencies through Git blobs.
3. invoke.sh. Then wrote and sealed the independent inventory, before opening step 4.
4. rehearsal/receipt.json; raw solve captures, retained-files and invocation log;
   rehearsal/chain-receipt.json.
5. authorization-request.md, then campaign-note.md.
6. Frozen implementation brief/design, including sections 1 and 3 and step 7; prerequisite
   resource-decision.md, identity.json and measured-report.md. Then completed the required
   adoption, manifest, frozen journal, capacity-plan and read-only checkout identity checks.
   Additional frozen source reads resolved line references and later-phase control flow.

Sealed artifact:
D:/Pontius/tmp/solve-plan-cold-20260910/reviewer-01/inventory-01-codex.md

SHA-256:
`e70a8fd36d9bd6b87d756a5234ae58c76589663ab726248a98cb37f7067b8c20`

The inventory was not edited after its first hash. It recorded the empty-log/start-append,
unchecked shell writes, rehearsal/override and stale-journal boundary questions before any
rehearsal receipt or capture was opened. Findings below were resolved against the remaining
required inputs, not adopted from another review.

No delegation or reviewer communication occurred. No memory, sibling scratch, reviews
directory, progress.md, INDEX.md, conversation history, prior verdict report,
ready-for-claude.md or disposition was opened. No launch logs were read. References to such
files inside allowed documents were not followed. candidate.json was not an allowed input
and was not opened. Only the two requested artifacts were written in exclusive scratch.

## Findings

### I-01 — Important: authorization consumption is not atomic

Location: invoke.sh:32, invoke.sh:43, invoke.sh:50–57.
Contract: authorization-request.md:34–42; handoff.md's one-shot semantics requirement.

The nonempty-log check occurs well before the start append and launch, with no exclusive
claim. Two simultaneous invocations can both observe an empty log and the same old run
census, both finish the preconditions, then both append a start and launch. The run-directory
check does not close that interval: schedule both callers past line 43 before either child
creates its UUID directory. Both commands then run on the same authorized source and plan.

Consequences: one authorization can produce two retained solves; both processes redirect
stdout/stderr to the same filenames, so captures can be truncated or overwritten, and their
journal-tail and retained-file collection can interleave. This is a control-flow
counterexample without changing any source, plan or authorization bytes. It does not require
an intentionally bypassed check. The successful single-caller rehearsal cannot establish
exclusion between callers.

The one-shot boundary needs a successful exclusive claim before execution and a consumed
state that survives interruption; this packet has neither an atomic claim nor an external
exclusive-launch mechanism bound as a precondition. No concurrency experiment was run.

### I-02 — Important: rehearsal mode bypasses authorization on the retained checkout

Location: invoke.sh:10–11, invoke.sh:22–33, invoke.sh:55–57.
Contract: authorization-request.md:13–14,34–42; identity.json invocation/checkout binding.

REHEARSAL=1 skips both authorization presence and the consumed-log check. It does not require
a disposable SOLVE_ROOT: the default remains the permanent retained execution checkout.
Thus with REHEARSAL=1 and no root override, the present checkout satisfies the remaining
identity checks and can execute a full solve without authorization.md. The child receives
no rehearsal/development flag; it invokes the ordinary retained run writer and appends the
real checkout journal. Only the wrapper's output destination and log label change.

SOLVE_ROOT and SOLVE_PK are also accepted in ordinary retained mode without comparison to
the bound checkout/packet. A different matching checkout or output packet is accepted, and
mkdir/redirections use those paths before child-environment scrubbing. Therefore the script
also does not enforce the promised write destinations. These are supported environment
branches in the reviewed script, not a proposal to edit it or invoke the Python tool directly.

Consequences: an inherited rehearsal flag can spend a retained full-pool run before approval;
caller overrides can redirect execution/records outside the declared binding. Restricting
rehearsal to an explicitly distinct disposable destination and enforcing the retained roots
must be part of the executable boundary. I did not exercise any of these launch paths.

### I-03 — Important: failed start-record and evidence writes do not stop execution

Location: invoke.sh:8,26–27,50–57,60–63,67–76.
Contract: authorization-request.md:36–38,76–77; brief.md:110–112,141–144 at the frozen source.

The script sets only `-u`. mkdir, the start-log append, journal capture, end-log append and
retained-file output are unchecked. A concrete pre-launch state is an existing writable OUT
with an empty, unwritable LOG: `! -s` passes, appending the start record fails, and the script
continues to launch the solve. That loses the durable consumed marker and its start identity.
A failed mkdir likewise does not stop at that operation.

After execution, capture/hash failures do not change rc. `sha256sum | cut` can yield empty
output after a hash-read failure; the wrapper still formats an end record, continues through
retained-file collection and exits with the child's rc. A successful child plus failed end
or retained-file write therefore exits 0 with incomplete evidence. Fixed redirections also
have no protection against overwriting existing captures whose LOG is empty.

Consequences: execution can begin without its required record, and a wrapper success does
not certify the required capture set. This is separate from I-01: even one caller and no
race fail when a required filesystem operation fails. Explicitly checked record creation
and evidence finalization are required; a generic assertion that failures retain everything
is not implemented. No write-failure simulation was performed.

### I-04 — Important: an early child failure is bound to the previous journal row

Location: invoke.sh:46,60–63,74; tools/v0a_eval_panel.py:630–633,668 at 1c706744;
src/pontius/execution.py:37–104,122–162 at 1c706744.
Contract: authorization-request.md:36–38; brief.md:141–144.

The wrapper always copies `tail -1 execution_journal.jsonl` as solve-journal-row.jsonl. It
prints the before/after row counts but does not compare them, verify a newly appended row,
or reconcile the row's result with the started attempt. The frozen entry calls begin_run
before entering its report-owning try/finally. A transient Git/source-verification failure
there, or interruption before finish_run appends, leaves no new row. The wrapper then copies
and hashes the existing last row as the current solve's journal capture.

Consequences: a failed or ambiguous invocation can retain another invocation's successful
journal identity instead of an explicit missing-current-outcome record. The nonzero child
exit is still captured in ordinary failure cases; this finding does not assert that it is
changed to zero. It is a false binding of the journal evidence and an unmet promise of one
fresh failed/incomplete result per invocation. The normal rehearsal only exercises a path
where a new journal row exists.

The wrapper must distinguish no new row, one matching new row and unexpected additional
rows while preserving the attempt's original start/captures. No early-failure invocation
or interruption was executed during this review.

### I-05 — Important: aggregate manifest identity uses the wrong ordering rule

Location: handoff.md:5–8,35; manifest.sha256:1–12.

All twelve member digests match the raw files. The published aggregate
`a283396997e87cde60ffe00ae5c1e5413fe27a77eca559a360a20570ffe5abfe`
is the SHA-256 of the existing 1,076-byte LF manifest in filename order. The handoff explicitly
requires whole-row byte sort (`LC_ALL=C`), not filename sort. Sorting the complete
`digest + two spaces + path` rows and appending one LF per row produces:

`d82f86718bbe04627f3d48f212ffd97546a3cbc73cbb477a45017e8fc8a417cb`

Independent Python byte sorting and .NET ordinal ASCII sorting produced the same different
aggregate. The raw manifest already uses LF, so this is not a CRLF-normalization ambiguity.
For example, the current first row starts 61057f..., while the campaign-note row starts
0dc1dc... and must precede it in the mandated whole-row order.

Consequence: the declared packet identity cannot be reproduced with its governing algorithm.
No member-content tampering is alleged. Correcting the manifest/identity specification and
issuing a consistent freeze is needed before treating this packet as that identified freeze.

### M-01 — Minor: agreement memory claim overstates what the receipt establishes

Location: campaign-note.md:67–76; rehearsal/chain-receipt.json:239–244,250–288.
Source: tools/v0a_eval_panel_completion.py:149–180,324–342 and
 tools/v0a_eval_panel.py:383–406,433–441 at 1c706744.

The note says memory/result size scale with the bank, not H, and asserts a 98,304-draw bank
would exceed 2,048 MiB. The four-hand, 65,536-draw receipt establishes only one observation:
1,560.2 MiB Job peak and 20,128,357 result bytes. The source supports growth from retaining
individual draws plus their scan report, but also retains each host Session result in the
worker's results list and emits it into parent observations. Host outcomes therefore grow
with H as well. Parent-held duplicate draws do not by themselves establish the worker Job
peak; the parent is outside the job it creates.

A simple multiplication of the whole 1,560.2-MiB peak by 1.5 would give 2,340.3 MiB, but a
fixed-baseline model using 787.5 MiB gives 1,946.55 MiB. Neither model is a justified forecast:
one receipt does not separate fixed runtime/host cost, per-draw cost and per-hand retention.
The exact source also launches real host children during agreement, another distinction
from solve/export. I make no claim that 98,304 draws will fit.

Consequence: the stated numeric exceedance and independence from H are unsupported planning
claims. Qualify the inference and measure the full-pool agreement under its later plan, as
the note already proposes. Minor here because no agreement envelope or invocation is
requested, and the current solve envelope is unchanged.

## Independent evidence and complete-packet assessment

### Frozen source and execution identity

Read-only Git checks established:

- HEAD: 1c7067448106cfa2aca3d57be879842d72293c61.
- Tree: 3d2fe79d2af20125e322dd4a668335e789810863.
- Execution branch: claude/eval-panel-solve.
- Adopted parent: beb84be566aa28029284bd35c526d33cd27af369.
- Reviewed candidate 7ca821802c949b047becf6599d603b3b63d51fa7 resolves to the same tree.
- Read-only origin ls-remote returned the exact adopted commit for
  refs/heads/codex/eval-panel-completion-adopted.
- Status before and after review: only `?? plans/`.
- Exactly the seven old run-directory names listed in identity.json occur on disk and in
  the adopted tree; no extra run directory was present. authorization.md and invocations/
  were absent at inspection.

I independently compared 892 source-scope files to frozen Git blobs using the normalization
rules read in execution.py, without importing it. There were no mismatches or extra indexed/
untracked nonignored scope files. The independent raw-source digest was
`bac14bea3e9a4e4c8c120556311447262d7775de54e39ef121c02bb2c59eb204`, matching identity.json
and the rehearsal journal. Worktree source bytes were read only for this expressly requested
identity comparison; all behavioral source inspection used Git blobs, never substituted
worktree code. Read-only Git commands used the specified executable; status used
--no-optional-locks. No Git mutation, checkout mutation, tests or project execution occurred.

The .venv pyvenv.cfg records CPython 3.14.6, the specified base Python home, uv 0.12.1 and
include-system-site-packages=false. Windows executable metadata reports Python 3.14.6;
installed NumPy metadata says 2.5.2. This verifies current metadata, not the historical
execution of the stated uv sync command. I did not launch the project's .venv interpreter.

### Plan admission and prerequisites

The 12,365-byte packet plan and checkout copy are byte-identical, SHA-256
`c1a6af606cc80841d61b5824913c8a1b6c896988ae4c578127c1dfc08b4f8982`.
An independent standard-library parser rejected duplicate/nonfinite JSON during checking;
these bytes have no such ambiguity. Exact solve key set, version, phase, declared-full
coverage, runtime, integer stack/counts, fixed board, prefix, empty inputs and resource
600 seconds / 2048 MiB meet the frozen predicates. No export/agreement is admitted by this
solve plan. The plan is within the 262,144-byte limit.

From ascending rank-major `23456789TJQKA` / `cdhs` cards, independently enumerating C(47,2)
compatible pairs yields 1,081 hands. Python 3.14.6 standard-library seeded shuffle of those
pairs exactly equals every entry of the plan permutation. Recomputed digests:

- Universe: 18953f113d65c6e25111ac9c2441942e4145051e169261fecd0ed0b9e5be41ed.
- Permutation: 344e7eeb06d72b97313f470880b8d169c4674e83bb440de827fa6fb87d97648a.

Board, prefix, seed, universe digest and full permutation equal the frozen retained-capacity
plan at beb84be5:tests/fixtures/eval_panel/plan-capacity.json, digest
6ad3e205058de941a695e04a966cb966d255369b0f910cfcee25a3426636bae1.
Its identity agrees with the retained capacity result, not only the current packet claims.

All three absolute prerequisites match the frozen constants, are below OwnedInput's size
limit and have no reparse-point path component at inspection:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| Capacity result | 2,789 | 29f532a900289c3e7b274646a7fc7332ff1a0aa9e6d74c332319668783d89e53 |
| Preflight result | 20,722 | 8a17325eaa07e0f8774dcb7bc2050a3ae233cf47bebfc63a6b59574031fb742f |
| Resource decision | 1,256 | 037a0de1b8605dc182cdc99ef0ef146e8c5ab08f73d984e4497e5a7a94afe2cf |

The capacity/preflight results are completed with cleanup_verified=true, have the correct
phase and permutation identity, and preflight has sample_complete=true. The five preflight
units have passed comparisons, including the zero royal-board control. Frozen journal rows
60 and 61 at 642858d65bdf5256f47c1f8197c2726ac30ed699 bind these exact result hashes and
paths, source beb84be5, source_verified=true, and source digest 43ee826f...; the local
claude/eval-panel-prerequisite branch resolves to that journal commit. The recorded capacity
selects all 1,081 hands, 1,012,625 bytes, and no next failing prefix within the domain.
The required resource decision explicitly chooses that H and 600 s / 2048 MiB, while
withholding invocation authority. The current plan respects that distinction.

### Control flow, interruption and retention boundaries

Frozen control flow supports the normal single-phase execution: admission in the parent,
worker launch suspended inside a finite-memory Job, resume after assignment, caller-owned
drained observations, separate bounded cleanup attempts, and final phase reconciliation.
Worker failure, exhausted budget, errors, missing required observations or unverified cleanup
cannot produce a completed status through the normal supervise path. Completion dispatch
returns after solve and cannot silently export or run agreement.

Solve checks its deadline before each hero, the first required tie-reference stage and
teacher publication. It uses 990 compatible villain hands per hero, exact kernel-settled
integer totals, and CHECK on equality. Completion reconciles the exact seeded hand order,
tie reference if needed, canonical teacher reconstruction and artifact digest. Normal
retention publishes a partial file, reconciles intended bytes in finally and retains the
recoverable encoding until publication is confirmed. These mechanisms are appropriate for
the declared teacher consistency question; they are not evidence of teacher strength.

The worker budget is not an end-to-end wall limit: initial source admission, parent checks,
result serialization and retention are outside it. finish_run writes result, appends journal
and regenerates STATUS sequentially, so abrupt termination or I/O failure can leave partial
record state. It does not provide an atomic three-file transaction. The wrapper's one-shot
and ambiguity handling must accommodate that actual boundary; I-01 through I-04 explain
where it fails to do so. No claim is made that forced process termination can guarantee an
end timestamp or completed artifact; such absence must remain explicit and consume the run.

### Rehearsal consistency

The raw captures substantiate the normal solve receipt:

| Check | Independently recomputed observation |
| --- | --- |
| Raw stdout | 527,287 bytes; e4a77d2a3face936ec0b892a46968c5fcc61ea54fa6c16909e3ec1fd81b816c0 |
| LF-normalized stdout | 527,286 bytes; 02bb208ee1dbf619c09bf21aa9b55200d243d6029bd6ced8156f20c035771ece |
| Stderr | 0 bytes; e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| Captured journal row | 765 bytes; d1d8ff72ea87d2c349d4cc2700fc22ab382e32036158cc7ef36b882259dea712 |
| Observations | 1,081 teacher hands + one artifact + one solve summary = 1,083 |
| Ordered census | All 1,081 unique hands, exactly equal to the plan permutation |
| Actions | 545 raise-to-2; 536 check |
| Exact ties | 0; thus no nonzero-return tie reference required for this completed census |
| Production body time | min 0.0131278 s; mean 0.0143095 s; max 0.0659511 s; sum 15.4685849 s |
| Worker time | 16.0230708 s |
| Worker Job peak | 825,425,920 bytes = 787.1875 MiB |
| Journal duration | 18.8813197 s |
| Log wall/exit | 19 s from 02:45:43Z to 02:46:02Z; recorded exit 0 |

Every captured teacher row has denominator 990, consistent outcome counts and totals, and
the required maximizing action. Independently constructing the canonical teacher document
from those rows yields 241,587 bytes and SHA-256
`c3ffab403eb7e939857cc31b0f21b255cefdffd8b0d26d078b703c1fe956b3e3`.
This matches the artifact observation and retained-files capture. LF-normalized stdout
matches the recorded result digest. The capture reports phase_complete, resource-state and
cleanup verification true, all twelve cleanup entries ok, no errors and worker exit 0;
the journal reports source_verified=true with the identified source digest.

These are consistency checks of the executed record and reconstruction from its rows, not
a new solve or independent poker-value oracle. The removed snapshot, raw runtimes.json and
original teacher/result files could not be inspected. Runtime digest eec89296... is bound
by the journal and retained-files capture but its original bytes are absent. The chain's raw
export/agreement captures are explicitly outside this allowed packet; I did not access the
coordinator scratch mentioned in chain-receipt.json:6. Its costs/digests remain receipt
assertions, not independently re-hashed original chain artifacts.

### Campaign sequence, arithmetic and claim limits

The proposed sequence matches frozen teacher_input: export binds retained solve teacher and
producer result; agreement binds retained export teacher, blueprint and producer result.
The producer must be completed, phase_complete and cleanup_verified, with matching coverage,
pool, prerequisites, permutation and retained artifact identities. Agreement requires the
bound blueprint to equal deterministic export of its bound teacher. Export verifies repeated
bytes, wire cap, exact decoded key/action equality and the exhaustive provider boundary.
For a full pool the real complement is empty; the off-pool host case uses a test-only proper
subset. These are separate identities, consistent with the governing design.

The agreement witness scan rejects a draw if any of the twelve private cards collides with
the board, scans every declared seed/index pair, and requires actual complete coverage before
scheduling hosts. The bank ranges/indices are finite, unique and disjoint from holdout. With
H=1,081 it schedules 1,081 primary sessions plus three controls, 1,084 attempts, and reconciles
scheduled/observed outcomes. The classifier reads nested retained results and actual frames,
requires completed outcomes, replays settlement and lookup/reasons, and keeps chip eligibility
separate from agreement. No witness scan, deal generation or host execution was performed.

Independent combinatorics gives collision-free fraction C(47,12)/C(52,12) =
0.2531812725090036 and per-target probability 0.00023421024283904124. Full-pool IID union-bound
planning estimates are 0.00023279358275093317 at 65,536 draws,
1.0802982173046996e-7 at 98,304, and 5.0132148168377026e-11 at 131,072. These support the
rounded bank-sizing figures. The receipt's collision + unused + witness counts total
65,536, and 48,746/65,536 is about 74.38%; its seven host outcomes match four primary hits
plus the named controls. Actual census, not the IID model, remains the acceptance condition.

The export arithmetic is consistent: 1,048,576 - 1,010,990 = 37,586 bytes headroom;
1,012,625 - 1,010,990 = 1,635 = 545 * 3 bytes saved by raise/2 versus CHECK/null rows.
The stated nine minutes for 1,084 host attempts at about 0.5 s is a rough planning estimate.
M-01 concerns the separate unjustified categorical memory extrapolation.

The packet consistently labels its solve/chain rehearsals non-evidence and treats teacher
comparison as diagnostic only. It does not claim retained host agreement or teacher strength.
It explicitly withholds export/agreement authorization and leaves their envelopes to later
packets/controller decisions. The solve envelope has not been reduced because rehearsal was
faster. Those boundaries are correct in the prose; I-02 shows the script does not enforce
its own authorization/rehearsal separation.

## Exposure log and limitations

Required-input exposure, in read order:

- handoff.md and identity.json: adoption/controller approval, assertions of a previously
  reviewed source tree, and drafter statements of rehearsal admission/census/source digest.
  These were present before the inventory seal and disclosed inside it.
- authorization-request.md:12, after the seal: explicit prior-source `CLEAN/SOUND, broad
  GREEN` labels. They were not used as support for my verdict.
- Frozen governing brief/design: references to accepted prior specification/review gates,
  parent specification and disposition paths. No linked disposition or old review opened.
- Prerequisite identity.json: reviewed candidate and disposition path; measured-report.md:98–100
  describes the old timing diagnostic as `I-01`. This is prior-finding exposure inside a
  expressly required governing input. I did not open the old finding/report.
- Required r003/adoption.md: explicit `CLEAN / SOUND`, `GREEN`, prior broad result counts and
  a statement that Claude reconciliation stands. The associated required
  checks/adoption-receipt.json includes exact candidate/adoption identities and a broad
  receipt digest/test assertion. No broad report or reconciliation/disposition was opened.

No such prior material was inherited at the initial context probe. Exposure in these later
required inputs is disclosed, not silently treated as continued verdict blindness.

The specified Python utility initially received OS access denied. An approved escalation
then allowed Python 3.14.6 with -I -B to run only inline standard-library parsing, hashing,
combinatorics and read-only Git utilities; no retained utility script or project import.
Initial sandboxed ls-remote could not connect; an approved read-only escalation returned the
exact remote head. No automatic approval rejection remains unresolved. All frozen Git blob
reads succeeded; none was replaced by worktree source because of permissions.

No project execution, rehearsal, retained solve/export/agreement, invocation-script run,
tests, publication, Git mutation or checkout modification occurred. Failure, concurrency and
interruption findings are static traces, not new measured receipts. Environment metadata
and current identities do not guarantee future state at launch or prove the historical uv
sync command. The absent disposable snapshot and unprovided chain raw captures limit
independent verification as stated above. Only the requested inventory and this report were
written; the coordinator must perform any later packet copy or ledger entry.

Disposition of this review: NOT CLEAN. The valid plan and consistent normal solve capture
do not discharge the one-shot/retention failures or the manifest identity defect. Findings
are reported for the drafter/coordinator; no correction, renewed rehearsal or source repair
was attempted by this reviewer.
