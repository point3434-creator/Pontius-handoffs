# Publication host implementation handoff

2026-08-30, Codex non-cold worker. Unfrozen and uncommitted.
Worktree D:\Pontius-worktrees\codex-v0a-i01-publication, base policy r003
30df7bce8da51715e6f1d7576892dd689421c516. Adopted plans:
publication-plan-draft.md and publication-plan-amendment-01.md.

Worker scope is runtime.py, replay.py and test_v0a_replay.py only. Parent owns
trace.py native TraceWriter/take_pending and test_v0a_trace.py. No C edit, new
module/test filename, sealed change, ledger, cold report, freeze or integration.
The attached worker patch excludes the two parent-owned files. Final tests include
their exact native-writer overlay, recorded in both interpreter receipts.

## Behavior

- HandRuntime.begin_host_accounting initializes the outer public ledger without
  binding policy or private/betting state. Direct runtime dispatch initialization
  remains unchanged. Header construction/configuration/hash work is deferred from
  ReplayHost.__init__ into measured run work; declared fixture/deal setup stays pre-run.
- Required owned-bookkeeping entry stops ordinary behavior before a failed interval
  can acquire input, serialize or proceed to dispatch. Iterator advancement and
  exhaustion, all-in/showdown event construction, row serialization/assembly/writes,
  settlement/oracle, and semantic hashing run in real public intervals. Classification
  uses actual betting-terminal-at-entry. Semantics finish before terminal totals are read.
- One feed path retains outcome records before serialization. Each required batch,
  including header and the first outcome, is drained to the owned writer before next
  input. Writer creation is lazy at that first flush. First storage failure stops input,
  keeps already accepted deliveries and incomplete bytes, and forbids later append/finish.
- A failed required post-delivery entry uses a separate optional in-memory failure-report
  path to retain the accepted decision. It never acquires more input or publishes
  unmeasured rows. Accounting/digest success is refused. The old optional owned-operation
  semantics remain available for honest failure reporting.
- Final terminal construction, prefix/full hashing, byte assembly, terminal append,
  writer finish/flush/close, and their failures are inside final owned publication.
  Finalization follows. Receipt success requires clean publication and finalization.
- Owned cleanup runs after recording the body cause and before its closing clock read.
  TraceWriter.close_errors is drained in occurrence order. If finish already raised its
  first close error as the body cause, only that identical occurrence is skipped; equal
  codes on distinct close errors remain distinct. Cleanup and final callbacks never
  repeat an owned close attempt or replay a previously reported close occurrence.

## Fresh validation

All payloads ran only in fresh disposable D-local snapshots using the existing runner,
asserted exact CPython executable/full version, -B/-P, explicit cwd/src PYTHONPATH and
scrubbed environment. Receipts preserve hashes and immutable logs before/after execution.

- publication-checks/red-host-final-311-receipt.json: frozen r003 plus test overlays;
  seven incremental host tests fail genuinely, and the parent's four native lifetime
  tests produce five assertion failures. No production overlay is in this RED.
- publication-checks/host-final-311-receipt.json: actual3.11.15,144 tests pass.
- publication-checks/host-final-314-receipt.json: actual3.14.6,144 tests pass.
  Each lane:40 hand +29 trace/native +53 replay +22 fault contracts. Both tested the same
  five overlay hashes; the worker-owned three files still match those receipts.
- Worker-scope git diff --check passes.

The seven new host tests use actual public operations, profile observers and real paths:
required entry gates iterator; iterator/exhaustion cost enters totals; actual serializer
and semantic cost enters totals without contaminating response time; a failed post-
delivery entry retains the accepted decision without further input/file publication;
clock loss after the first append leaves an incomplete prefix, stops input and releases
its native owner; rows exist before next dispatch while the parent remains pinned;
and a real pre-existing destination stops A after one accepted action without overwrite.

Existing conservation sweeps pass over all dynamically observed clock reads in both clean
and rejected-input hands. Earlier-end publication expectations were changed from A4/B2
accepted actions to A1/B0 at first write failure. Required settlement entry now prevents
an oracle body after entry failure, with no invented body cause. A separate real public-
runtime optional interval test preserves the former source/dead-witness/distinct-body
conservation property. No fixture constants or hand/fault test files were changed.

Earlier draft receipts remain honest: host-draft-v2 exposed the expected old publication
and optional-entry assertions; host-draft-v3 exposed a new test's wrong status spelling
(accepted versus decided). They are not final verification evidence.

## Review and integration limits

No native writer helper doubles were introduced. Native lifetime tests belong to parent;
this worker exercised their current four-test suite in both final lanes. Multiple native
close-error draining is source-inspected; no injected native-close-error evidence is
claimed. No exhaustive fault, cross-platform, performance, rehearsal, source-seal or
production authority claim follows from these correctness runs.

Root must review and layer policy/value/trace/publication successors without copying whole
files over concurrent work. Replay host hunks and trace checker additions share replay.py;
the two test classes added near main also require a careful merge. Final combined focused
verification and fresh cold review remain required before a frozen source candidate.

## Exact worker hashes

- `src/pontius/v0a/runtime.py`: `619efc71eae7f1768c8e63922d81f40a6ba2359632401991a91c0ccba4b88e71`
- `src/pontius/v0a/replay.py`: `18aded14503774a89097de6efec847ec16afba908d9def35dbbf9ad84e689f0e`
- `tests/test_v0a_replay.py`: `ebe1673d64867d4ec7fd6a4502dbc7456375660f0d97f6230a675441f53471e6`

Worker patch SHA256: `ec18632da01b5e2ee1b146bc0bcb2c5db79aab35f50bd59e3a6d3f122437d956`.

```text
src/pontius/v0a/replay.py  | 391 ++++++++++++++++++++++++++-------------------
 src/pontius/v0a/runtime.py |  57 ++++++-
 tests/test_v0a_replay.py   | 306 ++++++++++++++++++++++++++++++-----
 3 files changed, 538 insertions(+), 216 deletions(-)
```
