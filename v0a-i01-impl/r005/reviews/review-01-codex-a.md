# v0a-i01-impl/r005 - Codex cold review A

Verdict: FINDINGS. Specification: FAIL. Engineering quality for this bounded
failure contract: FAIL. Design: STRAINED. Two Important findings remain.

Candidate: a8582e6d6b53b55415dab79c4a54e252d00b74ad
Manifest SHA-256: e9b0baf12e258d66a92169d38137cbf2f42317158b6515ac377f745bbc52093a
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 5d373871b27bed5ef026150b816d684a588b75c3
Reviewer: Codex cold A. Date: 2026-08-30. Tier C, FIX R2-03 only.

## Findings

### R5-A01 - Important: a settlement exception is ordered after its cleanup fault

Severity: Important / Medium (P2). Confidence: high, reproduced on both required
interpreters. Location: src/pontius/v0a/replay.py:497-531, especially the
`except Exception` at 527; runtime.py:341-348 performs the intervening cleanup.

The public `settlement_oracle` callback raises `ZeroDivisionError` after four
real controlled actions have been delivered. Immediately before raising, the
callback arms the injected clock to fail on the next observation. Thus the
oracle exception occurs first and the real outer ledger's
`stop_preparation_work()` fails later during context-manager exit. No runtime,
ledger, trace builder, test, or configuration object is patched.

Expected receipt codes, in occurrence order:

- Invalid source: primary `settlement_mismatch`, secondary `[clock_invalid]`.
- Reversed source: primary `settlement_mismatch`, secondary `[clock_reversed]`.

Actual on CPython 3.11.15 and 3.14.6:

- Invalid source: primary `clock_invalid`, secondary `[settlement_mismatch]`.
- Reversed source: primary `clock_reversed`, secondary `[settlement_mismatch]`.

The generic host exception is journalled only after `with runtime.bookkeeping()`
unwinds. Its finally block has already journalled the later clock failure. This
is the same first-cause inversion the round is intended to eliminate, now on the
host body-exception path rather than dispatch rejection. The receipt stays
unsuccessful, and all four delivered decisions remain available; the defect is
the authoritative failure identity and occurrence order, not an action loss or
false success.

Requirement: ADR-0485:271-279 and 437-441 preserve the first typed cause and order
later failures. The r005 R2-03 contract explicitly includes host-side settlement
exceptions, and its G1 tests use this same public callback seam.

Fresh evidence: probes `oracle_body_before_cleanup_invalid` and
`oracle_body_before_cleanup_reversed` in both cold-a-receipt-*.json files. Their
independent `observed` lists are `[settlement_mismatch, clock_*]`; `reported`
lists are reversed. The callback and source are in checks/cold-a-verify-v2.py.

Required outcome: retain the settlement failure as primary and the subsequent
actual clock code as the first secondary, for both clock kinds; preserve the
existing delivered records and unsuccessful outcome. A returned mismatch and a
raised settlement exception must obey the same occurrence-order contract.

Nonbinding implementation guidance: capture and journal a body exception before
leaving the measured body, so finally cleanup cannot run ahead of that capture.
This does not require replacing the append-only journal or selecting a specific
exception/container design.

### R5-A02 - Important: a genuine clock cause inside host settlement is discarded

Severity: Important / Medium (P2). Confidence: high, reproduced on both required
interpreters. Location: src/pontius/v0a/replay.py:524-526, with
runtime.py:299-300 and 344-348 controlling the cleanup echo.

Pass one public `MonotonicWitness` to `ReplayHost(clock=...)`. Its source is the
ordinary deterministic callable supported by ADR-0485. In the public
`settlement_oracle` callback, arm that source and invoke that same witness.
It genuinely raises `ClockInvalidError` or `ClockReversedError` inside `run()`;
this is not an exception fabricated by changing runtime private state.

Minimal invocation using the two public-path helpers in the issued diagnostic:

```python
observed = []
source = Clock(observed)
witness = MonotonicWitness(source)
def clocked_oracle(**kwargs):
    source.arm = "reversed"  # use "invalid" for the other frozen code
    witness()
    return chip_depth_settlement(**kwargs)
host = make_host("clock-in-oracle", clock=witness, oracle=clocked_oracle)
outcome = host.run()
```

`Clock` is a callable with a public `arm` test control; it records the actual
source failure and returns a reversed integer or raises `OSError` as appropriate.
`make_host` uses FIXTURE_A and the real immutable empty blueprint. Both helpers
are entirely outside production code in checks/cold-a-verify-v2.py. No monkeypatch
or private-field access is involved in these diagnostic probes.

Expected:

- Invalid source: primary `clock_invalid`, secondary `[]`.
- Reversed source: primary `clock_reversed`, secondary `[]`.

Actual for both: `failure_reason=null`, `secondary_failures=[]`. The independent
observer contains exactly the appropriate `clock_*` code. `passed=false` and
`accounting_complete=false`, but the terminal even has `complete=true` because
its completeness calculation sees an empty journal. Four acknowledged decisions
remain retained.

The first failure occurs in the host body, before any runtime closure seam owns
it. The subsequent cleanup sees an already-failed witness and suppresses its
own echo, which is appropriate for that echo. Then the host's typed-clock catch
silently assumes the original failure was already journalled. Neither layer
records the genuine cause. Liveness establishes that a read is an echo; it does
not establish that another layer has retained the original cause.

Requirement: ADR-0485:337-352 and 405-441 require the actual typed failure and
honest failed completion. The R2-03 category is every runtime/host failure reaching
the receipt with its true type and position. The explicit public oracle injection
is part of the host API and is already used by the candidate's acceptance tests.
This is failure propagation, not a policy-authority or value-boundary finding.

Fresh evidence: `shared_public_witness_in_oracle_invalid` and
`shared_public_witness_in_oracle_reversed` in both cold-a-receipt-*.json files.
`observed` is `[clock_invalid]` / `[clock_reversed]`; `reported` is `[]`.

Required outcome: retain the genuine code exactly once, with no later synthetic
`clock_invalid` echo replacing or duplicating `clock_reversed`. Do not emit an
unnamed failure or successful/complete terminal on this clock-broken path.

Nonbinding implementation guidance: make ownership of a caught typed exception
explicit instead of assuming an exception class proves prior journal entry. The
particular representation is not prescribed; repeated independently occurring
same-code faults must still remain distinct.

## Identity, independence, and scope

I read candidate.json, manifest.sha256, frozen ADR-0485, the frozen brief and
workflow, and the source first. I issued checks/cold-a-initial-inventory.md before
reading handoff.md or its coverage claim. I did not read another reviewer report,
implementer receipts/root-cause narrative, or contact Claude. The handoff itself
was read only after that inventory was on disk.

Both successful diagnostic launches independently resolved the owner ref and
verified its commit, parent, tree, complete changed-path set (rename detection
explicitly disabled), every changed Git blob, the whole-row-byte-sorted LF
manifest, and the manifest file's actual SHA-256. They also matched the snapshot
HEAD and blobs, verified the frozen ADR/brief/workflow bytes, and checked the
snapshot working content allowing only Git checkout CRLF conversion in memory.
No source byte was normalized or written.

The snapshot is exclusively:
D:/pontius-snapshots/v0a-r005-cold-a-96aa34d9536845ddaddc4b1dfbb9615e/harness

Snapshot `git status --porcelain=v1 --untracked-files=all` was empty before and
after each successful launch. Git was invoked only via
C:/Program Files/Git/cmd/git.exe. Owner-Git reads and packet writes used scoped
escalations; no safe.directory changes were made.

The current uncommitted workflow refinement does not gate this frozen submission.
Absence of a separate coverage.md is not a finding. Policy authority,
value-boundary auditing, R2-04/05/06/09/10, broad acceptance, experiments, GPU,
source seals, ceremonial commits and integration are outside this verdict.

## Coverage claim compared with the initial inventory

The initial independent inventory specifically included bookkeeping
entry/body/exit, body exception before finally cleanup, and host clock exceptions
whose origin may differ from closure echoes. The handoff's twelve closure seams
and named three-channel pair generation missed these exceptional body exits.

The candidate's G1 test raises several ordinary host exception classes with a
steady clock; it cannot expose a later cleanup failure. Its mismatch-before-clock
control returns a mismatching value, and therefore calls `note()` inside the body.
That is a different exit path from a body exception caught outside the context.

The conservation test is useful evidence for actual ledger clock faults, but its
observer subclasses the sealed ledger's private `_read_clock` and the comparison
filters the receipt down to clock codes. That filter cannot detect host/clock
relative-order inversion (R5-A01). Its observed domain does not include a genuine
public witness call originating in the host body (R5-A02). Thus its green result
does not establish the handoff's larger all-channel conservation claim, and the
claim is falsified by the two public schedules above.

## Requirement-to-evidence map

| Requirement / risk | Evidence | Result |
| --- | --- | --- |
| Frozen commit + manifest identity | Owner Git blob recomputation and byte comparison, both receipts | PASS |
| Actual CPU floor before development slot | 3.11.15 first, then 3.14.6; executable/full version/implementation asserted and recorded before payload imports | PASS |
| Initiating failure before later cleanup | Oracle body exception followed by real ledger clock fault, both types | FAIL R5-A01 |
| Genuine typed cause, echo not a replacement | Shared public witness in host settlement, both types | FAIL R5-A02 |
| Known accepted delivery survives closure fault | Real ActionMailbox acceptance then next clock failure; one full decision, matching interrupted failure timing, null emission observation | PASS for both types |
| Write refusal after delivered action remains typed | Existing destination under explicit packet run root, actual write_trace path | PASS; trace_write_failed primary, no overwrite, four decisions retained |
| Mismatch then cleanup then writing has exact order | Mismatching public oracle result, next clock fault, existing destination | PASS for both types: settlement_mismatch, clock_*, trace_write_failed |
| Existing rejection/closure/clock conservation guards | 30 selected frozen tests per interpreter, including full R2_03ConservationTests | PASS within their demonstrated domain |
| Journal does not deduplicate equal code values | Append-only source inspection and existing direct record test | Limited evidence; not promoted to a new real-path multiplicity claim |
| No recovery success or fabricated per-action timing | All nine diagnostics, retained decisions and receipt fields | PASS for tested controls, with the unnamed/complete terminal defect described in R5-A02 |

## Fresh commands and results

The checked-in production/test files were never changed. Diagnostic scripts and
receipts are create-only files under this packet's checks directory.

Executed via the issued checks/cold-a-launch.ps1:

```powershell
& 'D:\Pontius-handoffs\v0a-i01-impl\r005\checks\cold-a-launch.ps1' -Interpreter 'D:\Pontius-tools\py311\Scripts\python.exe' -Version '3.11.15' -Label '3.11.15-v2'
& 'D:\Pontius-handoffs\v0a-i01-impl\r005\checks\cold-a-launch.ps1' -Interpreter 'D:\Pontius\.venv\Scripts\python.exe' -Version '3.14.6' -Label '3.14.6-v2'
```

The launcher clears the child environment and whitelists only SYSTEMROOT, WINDIR,
TEMP, TMP, PYTHONPATH (exclusive snapshot/src), PONTIUS_GIT (absolute Git),
PYTHONIOENCODING and PYTHONUTF8. It invokes the diagnostic with `-B -P`, snapshot
cwd and no shell lookup. Every payload import origin is checked against snapshot
src. No dependency installation occurred.

- CPython 3.11.15: 3.11.15 (main, Jul 23 2026, 14:42:43)
  [MSC v.1944 64 bit (AMD64)]. Launcher exit 0; 30 existing tests passed;
  nine diagnostic schedules completed, four violated the contract.
- CPython 3.14.6: 3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10)
  [MSC v.1944 64 bit (AMD64)]. Same exit, counts, and four violations.
- Existing classes: R2_03HostClosureTests, R3_02TypedClosureCauseTests,
  R2_03CompoundScheduleTests, R2_03ConservationTests, FixtureReplayTests,
  TraceAndAccountingTests. Their complete names/output are in the JSON receipts.
- Diagnostic exit 0 means collection and frozen tests completed; each JSON
  explicitly records `overall=FAIL`. It is not a passing implementation verdict.

Receipts: checks/cold-a-receipt-3.11.15.json,
checks/cold-a-receipt-3.14.6.json, checks/cold-a-launch-3.11.15-v2.txt,
checks/cold-a-launch-3.14.6-v2.txt. The source is checks/cold-a-verify-v2.py and
the initial inventory is checks/cold-a-initial-inventory.md.

Harness correction retained transparently: the original cold-a-verify.py asserted
raw checkout bytes equal Git blobs and exited 1 before payload imports. An initial
launcher did not redirect its output; the unchanged retry captured that precise
assertion in cold-a-launch-3.11.15-attempt2.txt. No implementation test ran in those
attempts. The create-only v2 diagnostic verifies checkout CRLF conversion in memory
while retaining the authoritative blob-based manifest check. No issued file was
rewritten, no source conversion occurred, and no candidate failure was retried to
green. The successful 3.11 slot preceded the first 3.14 payload execution.

## Design assessment and release boundary

STRAINED: one append-only, occurrence-ordered journal is a suitable structure.
However, producer ownership is not closed: a host body can unwind before its
cause is captured, and a typed catch assumes another seam already captured it.
Liveness alone does not provide that ownership guarantee. These are concrete
failure-flow defects in the chosen implementation; the evidence does not require
a wholesale replacement of the journal architecture.

The required outcomes above are binding findings; implementation sketches are
guidance only. This review does not authorize a source change, a broader scope,
another round, broad suites, invocation, a seal, commit, or push. I performed no
source/test/configuration edits and no broad-suite, GPU or experiment execution.
