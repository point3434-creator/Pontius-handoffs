# Independent cold review B: v0a-i01-impl/r005

Verdict: FAIL. Design: STRAINED. Confidence: high for the reproduced behavior. R2-03 remains open: the changed settlement exception handling still reverses an initiating host exception and a cleanup clock fault, and its new special clock-exception catch can discard a real typed cause. This is not a verdict on deferred contracts or a demand to expand this FIX round.

Reviewer: Codex B, independent of implementation and other r005 reviews. Date: 2026-08-30.

## Binding and method

- Candidate: `a8582e6d6b53b55415dab79c4a54e252d00b74ad`.
- Manifest: `e9b0baf12e258d66a92169d38137cbf2f42317158b6515ac377f745bbc52093a`.
- Base: `b357d333fc2393b7fc7dcf31f30c86616208c817`.
- Tree: `5d373871b27bed5ef026150b816d684a588b75c3`.
- Exclusive execution snapshot: `D:\pontius-snapshots\v0a-r005-cold-b-e6ac13a682804562a53621e8fab883e1\harness`.

The pair was independently recomputed from all ten changed Git blobs with rename detection disabled and whole-row byte sorting, and compared with the literal manifest file bytes. Ref, tree, ADR-0485, brief, representative sealed kernels, and legacy dependency baseline were also checked. A final repeat confirmed the same identity after execution. The checkout uses CRLF; snapshot bytes compare with the stored blobs after comparison-only CRLF-to-LF conversion. No snapshot or source bytes were normalized or edited.

Before reading handoff.md or its coverage claim, I derived and issued `checks/cold-b-initial-inventory.md`, SHA-256 `15ea3ab6df64f0a5f43a563fa8fe4cea731d585040d86a28ca6f6d3c5e151908`, from candidate metadata, frozen ADR-0485/brief, and code. I then read the handoff and its named root-cause note. I did not read other r005 reviewers or coordinator probes. The frozen workflow governs this review; the primary checkout's uncommitted workflow refinements do not impose additional packet gates.

Scope: R2-03 host failure containment and typed cause occurrence order. Excluded: policy-authority/value admission and deferred R2-04/05/06/09/10. The comparison against r004 (`0207430a37e1e5b31c8da8da7aa57da1bc5c88ee`) confirms the required findings below are in the changed settlement handling, not discoveries used to reopen untouched fixture or trace validation contracts.

## Required findings

### R5-B01 — High: settlement-body exception becomes secondary to its own cleanup fault

Location: `src/pontius/v0a/replay.py:496-532`, especially the `except Exception` at line 527 and `note(SETTLEMENT_MISMATCH)` at line 531; context cleanup at `src/pontius/v0a/runtime.py:342-348`.

Requirement: ADR-0485 says to terminate on the first failure and retain the primary cause. The FIX's stated contract requires the true occurrence order across host and runtime, including initiating failure before cleanup.

Reproduced on CPython 3.11.15 and 3.14.6 through the real `ReplayHost.run`, real hand A, real betting settlement, and real outer ledger. The public settlement-oracle callback records its own `ValueError` occurrence, arms the supplied clock to fail on its next call, then raises. The bookkeeping context's exit performs that next clock call. This uses no ledger subclass, private observation hook, hand-edited runtime state, or guessed clock-call index.

Observed versus returned:

| Source fault on cleanup | Independent occurrence log | Receipt primary then secondary |
| --- | --- | --- |
| invalid value | settlement_mismatch, clock_invalid | clock_invalid, settlement_mismatch |
| reversal | settlement_mismatch, clock_reversed | clock_reversed, settlement_mismatch |
| source OSError | settlement_mismatch, clock_invalid | clock_invalid, settlement_mismatch |

The handler that classifies the body exception is outside the measurement context, so cleanup has already journalled its later fault when that handler runs. Returning a semantic mismatch normally instead of raising is an opposing control: both invalid and reversed cleanup cases then preserve the correct order. This isolates exception unwinding as the defect.

Consequence: the host misidentifies the cause that failed the hand, so its evidence misattributes an oracle/settlement failure to subsequent infrastructure cleanup. All four accepted actions are retained; the receipts correctly fail with incomplete accounting, and the underlying failed source is never queried again. Those guards limit damage but do not satisfy the cause-order contract.

Smallest remediation direction: the owner of the fallible settlement body must classify and retain its initiating cause before leaving the measurement context and before cleanup can append. Do not rank codes afterward or reconstruct chronology from exception collection order.

### R5-B02 — Medium: the new clock-exception catch assumes a cause was already retained

Location: `src/pontius/v0a/replay.py:524-526`, interacting with `src/pontius/v0a/runtime.py:299-300,344-348`.

Requirement: R2-03 requires actual clock failures inside host work to reach the outcome with their true typed cause. A failed receipt with a missing cause is not equivalent to typed containment.

Reproduced on both interpreters: pass a real `MonotonicWitness` as the host clock. During the public oracle callback, arm the actual clock source and invoke that shared witness. An invalid value raises `ClockInvalidError`; a reversed value raises `ClockReversedError`. The witness is now dead before bookkeeping cleanup begins. The cleanup echo is suppressed, as intended, but the new host catch also suppresses the original exception on the assumption in its comment that a seam already journalled it.

For each case the independent observation log contains exactly its actual typed clock failure. The receipt has `failure_reason=None` and `secondary_failures=()`, with `passed=False` and `accounting_complete=False`. Four earlier accepted actions survive, and the source-call log confirms no calls after the failure.

This is a bounded injected-oracle scenario using the public constructor seam and a real witness. The default chip-depth oracle does not itself sample a clock; I do not claim this occurs on that default no-fault path. It nevertheless directly exercises the newly added host clock-exception branch and falsifies its unconditional already-recorded assumption.

Smallest remediation direction: make responsibility for retaining the original host exception explicit. Suppressing a repeated dead-witness read must not also suppress an original body exception that has never been recorded; retain the original type without manufacturing a second event.

## Comparison with the implementation's coverage claim

The independent inventory included settlement entry/body/exit separately, plus cross-channel exception-unwinding schedules, before seeing the claim. The claimed sweep of twelve closing seams is useful but insufficient: classifying the body exception outside the context creates an ordering gap that enumerating stop/abort/finalize sites cannot detect.

`R2_03ConservationTests` is useful evidence for conservation of ledger-observed clock failures on its two schedules. It is independent of the runtime journal's storage, but it is not a general observer of all causes:

- `tests/test_v0a_replay.py:852` instruments the sealed ledger's private `_read_clock` and reads `_clock_ns.failed`, so it is coupled to that observer implementation and liveness convention.
- The reported projection at line 896 filters to clock codes. A settlement cause can move across a clock cause without changing that projection at all; R5-B01 is such a counterexample.
- Host body failures and a witness sampled within host work are not in the sweep's observer population. R5-B02 is outside that population while still inside the changed host exception branch.
- The G1 test samples several ordinary oracle exception classes but only requires an unsuccessful receipt and some nonnull cause. It does not combine that exception with failing context exit, nor require its occurrence order.

This critique does not invalidate the passing conservation test. It narrows what the evidence establishes and explains why all 37 existing replay tests can be green while this FIX remains incorrect. A direct call to `runtime.record` twice also tests append mechanics rather than two independently occurring production failures; it is not sufficient proof of real fault conservation by itself.

## Requirement-to-evidence summary

| Requirement or risk | Evidence | Result |
| --- | --- | --- |
| Frozen commit/manifest and tested source binding | Blob-derived identity checks on 3.11 and 3.14; final repeat | PASS, with documented checkout line-ending translation |
| First cause before cleanup | Three exception-then-source-fault schedules, both runtimes | FAIL: R5-B01 |
| Original typed host clock cause retained, without echo duplication | Real witness fault inside oracle, invalid and reversed | FAIL: R5-B02 |
| Genuine accepted action survives post-acknowledgement clock failure | Real ActionMailbox, invalid/reversed next observation; full decision and matching failure timing checked | PASS for the two exercised schedules |
| No further source reads after a failed witness | Independent source call log in all armed-source schedules | PASS for the exercised schedules |
| Normal controls remain functional | Literal frozen payouts/counts for A and B; chip conservation | PASS |
| Ordinary semantic mismatch followed by cleanup failure | Independent wrong oracle result, invalid/reversed cleanup | PASS; opposing evidence to R5-B01 |
| Existing focused replay regression suite | 37 tests per interpreter, zero errors/failures/skips | PASS, insufficient to close R2-03 |
| Whole host/trace/fixture behavior | Not the bounded FIX's acceptance claim in this review | Not admitted as a new gate |

## Reproduced observations excluded from required FIX findings

The independent probes also found three escaping exceptions after real deliveries: an embedded-NUL destination reaches the production writer and raises ValueError after four actions; a declared ScriptedAction with kind `dance` raises during production event construction after one action; an injected terminal-builder OSError escapes after four actions. The first two use real production paths without method patching; the last is explicitly a bounded `TraceBuilder.close` fault injection.

These observations concern unchanged writer-validation, fixture/admission, and broader publication surfaces. They limit the handoff's literal phrase that every possible failure anywhere in `run()` is contained, but they are not added as required fixes, not assigned new deferred-contract gates, and not needed for this FAIL verdict. Their retained probe expectations describe the broad hypothesis being challenged, not new normative classification decisions for this FIX.

## Execution and retained evidence

Every Python process used `-B -P`, snapshot cwd, exact snapshot `PYTHONPATH`, a cleared child environment with only Windows necessities and explicit Python settings, and absolute `PONTIUS_GIT=C:\Program Files\Git\cmd\git.exe`. Exact executable, CPython implementation, and full patch version were asserted and printed before importing the payload. Product module resolution was asserted to the assigned snapshot.

Actual runtime order was 3.11 first, then 3.14:

| Executable | Existing replay tests | Independent observation cases |
| --- | --- | --- |
| `D:\Pontius-tools\py311\Scripts\python.exe`, CPython 3.11.15 | 37 PASS, no skips | 14 captured: 6 satisfied controls and 8 broad counterexample schedules |
| `D:\Pontius\.venv\Scripts\python.exe`, CPython 3.14.6 | 37 PASS, no skips | Same 14 captured, same contract outcomes |

The eight counterexample schedules are three instances of R5-B01, two of R5-B02, and three explicitly excluded observations above. The adversarial capture's exit 0 means observation completed, not that the candidate passed. It intentionally records all case results rather than aborting at the first violated invariant.

Reproduction uses `checks/cold-b-launch.ps1` with explicit `-Exe`, `-Version`, `-Payload`, and a fresh create-only `-Receipt`. Payloads: `cold-b-identity-v2.py`, `cold-b-focused.py`, and `cold-b-adversarial-v2.py`. Exact argv, cwd, environment, exit, stdout, and stderr are retained in the matching `*-311.json` and `*-314.json` receipts. `cold-b-final-identity-314.json` records the final identity check. `checks/cold-b-evidence.sha256` binds the scripts, initial inventory, and all issued receipts preceding this report.

Two review-harness problems are transparently retained: the initial identity probe rejected CRLF checkout bytes versus LF blobs, then a new v2 probe correctly separated manifest identity from checkout translation; the first adversarial capture completed twelve cases before a reviewer KeyError from indexing the mailbox mapping as a list, then a separately named v2 corrected only that probe access and reran all fourteen cases. Original scripts/receipts were not overwritten or normalized. All cold-b files were checked as BOM-free UTF-8/LF before this report was issued.

## Engineering judgment, advice, and limits

Specification verdict: FAIL for the bounded R2-03 contract. Engineering verdict: STRAINED, not WRONG SHAPE. A single append-only cause journal is a suitable representation, and the accepted-action/no-success/dead-source protections hold in these checks. The strained part is ownership of when a cause becomes recorded: some layers assume another layer has already done it, while exception unwinding can execute cleanup before the host classifier. Renaming the list or changing its transport alone will not repair that ordering.

Concrete nonbinding engineering advice: write the settlement body and its cleanup as one explicit error-ownership operation; keep one clear point that records the original body failure before cleanup; distinguish an already-recorded echo from an original exception by provenance rather than assuming every clock-shaped exception has an entry. Test a returned semantic mismatch and a raised exception under the same independent phase-triggered cleanup faults. Use a combined observer of host events and source failures for cross-channel order; keep the existing ledger conservation sweep as supplementary evidence. This does not require adopting a particular batching API or widening the production change surface.

Opposing evidence is substantial: 37 existing tests pass on each interpreter, no-fault A/B controls produce exact expected payouts and deliveries, ordinary mismatch ordering is correct, accepted records survive post-ack clock faults, and failed sources are not called again. None contradicts the specific unwinding and unjournalled-body exceptions reproduced here.

Largest unknown: unexercised compound host failure schedules beyond this bounded sample. Cheapest falsifying check for R5-B01 is the public-oracle ValueError followed by the phase-armed next source call; the retained probe already performs it on both required interpreters. Kill criterion for accepting this FIX: any genuine cause still absent, mis-typed, or placed after its own later cleanup cause in the changed R2-03 paths.

No source/test/configuration edits, broad suite, GPU/optional dependency work, experiments, installations, source seal, commit, push, safe.directory changes, or contact with Claude were performed. No performance, operational authority, or whole-increment acceptance claim is made. Recommendation: keep R2-03 open and return the two changed-path findings for bounded correction under the existing review/circuit-breaker process.
