# Cold-A initial invariant and related-path inventory — v0a-i01-ab/r001

Recorded before opening coverage.md. Inputs: frozen source and tests are permitted, but
tests and deferred coverage have not yet been used to choose expectations. Current
CLAUDE.md/workflow.md, frozen ADR-0485 and ADR-0484 brief, and the corrected absolute
r006 disposition supply requirements. No self-report, transcript, or other cold
reviewer material was read.

Candidate: 256bcf5b1e721c70216f4d8937166cbb9c25a7ce
Manifest: 7a4cbf46c9eb34693d605ae43a0b9048b709d65f9c3fed40610c5c1b5ae3b384
Base: c74b80628a89938ca585ef3240b5c267a7174d0f
Snapshot: checks/cold-a-snapshot (fresh local clone, detached; no overlay)

## Independent contract

1. The host's receipt cause sequence must equal actual distinct typed failure
   occurrences in chronological order. A source fault is one occurrence even if
   later code samples the permanently failed witness. Independent errors with equal
   codes are multiple occurrences. Catching a source fault inside a body does not
   erase it; later ordinary/clock body failures and cleanup/writer faults survive.
2. Measurement entry, body, exit and finalization are separate possible failure
   points. The failure that initiates cleanup precedes cleanup's later failure.
   Reporting never creates success or retries a failed source.
3. The public host returns a failed completion receipt after owned operation errors
   regardless of hostile exception message/class/traceback representation. Actual
   exception ancestry, not metadata impersonation, determines typed classification.
4. Every accepted action remains accepted and is represented by its full decision
   in the returned outcome. Later body, clock, cleanup and publication failures
   cannot erase accepted envelopes or delivery counts. No extra event is admitted
   after a terminal failure.
5. Failed/unclosed measurement reports incomplete accounting; trace-publication
   failure preserves the original cause and no completed-trace claim is invented.
   Existing action decisions/timings remain intact.
6. Exact candidate identity comes from whole-row-byte-sorted blob SHA-256 manifest,
   not checkout hashes. Acceptance payloads run in fresh D-local snapshot, actual
   CPython 3.11.15 before 3.14.6, -B -P, snapshot cwd/src PYTHONPATH, scrubbed env,
   absolute PONTIUS_GIT. No optional/GPU/broad/experiment paths are authorized.

## Related paths discovered independently

Discovery method: trace each changed failure producer forward to receipt and each
receipt producer backward to source/dispatch/operation, then inspect all catch and
journal sites in runtime.py and replay.py. Scope is R2-03 across the whole boundary.

- clock.MonotonicWitness.__call__: normal exact sample; invalid/reversed/source
  exception; permanent failure and refusal; failure/owns_failure observation.
- runtime._OwnedInterval.__enter__/__exit__: measurable and unmeasurable entry,
  preparation entry refusal, escaped and locally caught body failure, public
  stop_preparation_work, bookkeeper/publication duration sinks, trusted propagation.
- runtime._retain_witness_failure / record / _retain_error / classify /
  _record_closure_failure: occurrence retention and classification, no enum dedup.
- runtime.dispatch/_clock_reject/_clock_hand_failure/_from_failure and
  _release_boundary: first transition/wall read, clock wrapping in handlers,
  rejected event's abort cleanup, accepted-delivery clock closure and partial timing.
- runtime.finalize_accounting, accounting, measurable, closure_failures: final
  witness drain/ledger refusal and receipt inspection. Repeated observations must
  not duplicate occurrences.
- replay.ReplayHost.run: event loop; all-in runout and showdown dispatch;
  owned settlement plus real settlement oracle; mismatch note versus thrown body;
  owned terminal builder/write; expected write refusal versus escaping exception;
  finalization; complete receipt assembly.
- Sealed consumer seams action_clock / legal_decision_spine_v2 / preparation_bank:
  shared witness samples and public closure semantics only, no modification.
- trace.TraceBuilder.close/write_trace and model action/receipt/failure values:
  real artifact/value boundary under late failure. Trace schema/verifier/accounting
  redesign and policy authority are outside this review's correction scope.

## Planned behavioral evidence and limits

Run all four existing focused v0a suites. Independently exercise both complete-hand
fixtures using the real ReplayHost and ledgers, public injected clock, oracle and
mailbox seams, and real writer destination refusal. Observe actual source-failure
and body/writer occurrences externally, assert the whole receipt list, and compare
full decisions and accepted envelopes with fault-free controls. Target fresh versus
dead witness, caught versus escaped source errors, ordinary and hostile exception
representation, body-before-cleanup, equal-code multiplicity and compound schedules.
Exercise single source-fault locations throughout whole hand execution, plus event
rejection with cleanup faults where reachable. Distinguish reached injection from
unreachable schedule members; do not count hypothetical faults.

No fabricated OperationFailed, private state mutation, nested unsupported preparation
intervals or cross-runtime marker propagation is a gate. No conclusion yet; any
coverage claim remains to be compared with this inventory after this file is written.