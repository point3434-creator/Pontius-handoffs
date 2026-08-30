# Cold B initial inventory - v0a-i01-ab/r001

Recorded before opening coverage.md. Reviewer Codex cold B, 2026-08-30.
Candidate 256bcf5b1e721c70216f4d8937166cbb9c25a7ce; manifest SHA-256
7a4cbf46c9eb34693d605ae43a0b9048b709d65f9c3fed40610c5c1b5ae3b384.
Base c74b80628a89938ca585ef3240b5c267a7174d0f.

Requirements: ADR-0485 failure vocabulary/containment and preserved delivered
records; ADR-0484 brief criteria 5, 6, 8; r006 disposition R6-01 and R6-02.
Current CLAUDE.md and workflow.md apply. No other reviews or implementer
self-report were opened. The predecessor disposition's corrected absolute
locator is D:/Pontius-handoffs/v0a-i01-impl/r006/disposition.md.

Independent invariants

1. A genuine clock-source invalid/reversed occurrence is retained exactly once.
   A later refusal to sample that same dead witness is not a new occurrence,
   and must not retry the source or change the original type.
2. A fresh body-origin clock exception is a distinct occurrence. Two independent
   causes with the same code retain multiplicity rather than enum deduplication.
3. Failure causes follow actual occurrence order: interval-entry clock fault,
   any subsequent body failure, interval-exit fault, publication failure,
   publication-exit fault, finalization fault, subject to reachability once
   the witness is dead. A body-caught witness fault remains observable before
   a later mismatch or escaping body error.
4. Normal and hostile exception presentation/metadata must not prevent the real
   host returning its failed completion receipt. The adapter must neither call
   user rendering nor misclassify fake __class__; actual ancestry determines
   invalid/reversed clock types.
5. Accepted actions and full retained decisions survive every later fault.
   Failed host receipts cannot become passed via successful cleanup/publication.
6. Required checks cross ReplayHost.run, its public settlement_oracle, public
   witness callable, and real create-new trace writer. Public runtime observations
   may inspect results but must not fabricate internal state or marker ownership.

Related-path discovery from frozen source (before coverage claim)

- clock.py: MonotonicWitness.__call__, failure and owns_failure; source exception,
  invalid exact value, reversal, original identity, later refusal, last sample.
- runtime.py: _OwnedInterval entry/body/exit for owned_bookkeeping and
  owned_publication. _retain_witness_failure, _retain_error, record, classify,
  _record_closure_failure, measurable, closure_failures, finalize_accounting.
- runtime dispatch and failure release: ActionClockLedger creation and transition
  start; _HandFailure retention before _release_boundary; _clock_reject and
  _reject; public accepted_delivery_count and accounting. These share the journal
  and therefore are related regression paths, though broader policy/event fixes
  are excluded from the round.
- replay.py: settlement runtime.settle, independent oracle call, oracle field
  access/comparison/conservation checks; body wrapper transfer and settlement
  clearing. TraceBuilder.close and real write_trace within publication wrapper;
  handled TraceWriteError/OSError notes; final ledger closure; final primary and
  complete secondary tuple assembled after all closures.
- Sealed action_clock ledger owns interval timing and has state refusals. Such
  refusal after dead witness must not invent a fresh clock cause. New nesting
  support is excluded. Existing model/trace define returned values, not new
  schema or accounting acceptance scope.
- tests/test_v0a_replay.py contains closure, compound schedule, conservation,
  body ownership and adapter regression groups. Their existence is not evidence;
  independent schedules must record actual invoked fault events and compare the
  entire returned cause tuple, action identity and containment.

Planned evidence and limits

Verify exact frozen manifest blobs, parent/tree/ref and a fresh D-local detached
clone. Run actual CPython 3.11.15 first then 3.14.6, identities asserted before
imports, -B -P, exact cwd and src PYTHONPATH, scrubbed env, absolute Git.
Focused replay/hand/trace/contract-fault suites plus independent fixture A/B
public-oracle and actual writer schedules. Cover source exception/invalid/reversal,
entry/body/exit, caught/uncaught dead-witness samples, normal/hostile body errors,
independent equal codes and post-delivery preservation. Higher-order schedules
must state actual reached faults; impossible repeat-source failures stay excluded.
No broad suite, source edits, experiment owner, optional dependency, GPU, private
mutation, fabricated OperationFailed or unsupported nested interval contract.
