# Cold A initial bounded inventory

Recorded 2026-08-30 before reading r005 handoff.md, implementer coverage claims, receipts, or any reviewer output.

Candidate requested: a8582e6d6b53b55415dab79c4a54e252d00b74ad. Manifest requested: e9b0baf12e258d66a92169d38137cbf2f42317158b6515ac377f745bbc52093a. Base: b357d333fc2393b7fc7dcf31f30c86616208c817. These were read from candidate.json and manifest.sha256; independent Git-blob recomputation is next.

Read as primary inputs: frozen ADR-0485 (especially lines 221-280, 328-352, 395-441), increment-one brief, frozen workflow, CLAUDE.md, and complete runtime.py/clock.py plus host run/fixture and trace publication source. Current uncommitted workflow refinement is excluded. This inventory concerns R2-03 host/runtime failure containment and typed occurrence order only; policy authority, value-boundary auditing and deferred R2-04/05/06/09/10 are excluded.

## Required invariant map

- First detected fault must remain primary. Each independently occurring later typed fault must appear in occurrence order in secondary_failures, including repeated equal codes. A known dead witness's later refusal is an echo, not a fresh cause.
- Input/blueprint refusal emits no action; delivery failure is not retried; unknown acceptance stays unknown. Already acknowledged delivery retains its full decision and interrupted timing after clock closure failure.
- Cleanup/reporting faults cannot make the hand successful, erase earlier causes, fabricate timing/accounting, or query a known-broken witness.
- Host run must contain supported host failure channels and return typed unsuccessful completion. Required vocabulary is the 15 frozen FailureCode spellings, not invented cleanup/error categories.

## Bounded channels and exits derived before handoff

| Channel | Production entry and exit | Independent checks planned |
| --- | --- | --- |
| Witness source | MonotonicWitness.__call__: ordinary exception, invalid sample, reversed sample; failed witness refuses later use | Public callable faults through host; primary code fidelity, source called once after failure, no echo secondary |
| Dispatch pre-transition | dispatch admission, ActionClockLedger construction/start, event rejection | Typed refusal, no delivered action, failed hand, later cleanup order |
| Transition/process cleanup | process raises _HandFailure; dispatch records before _release_boundary/abort | Invalid order or clock cause followed by abort failure; first-before-cleanup and reversal not rewritten as invalid |
| Controlled decision | legal context, lookup/validation, snapshot, V2 emission, publish | Retained reason and no safe retry; scope restricted to failure propagation, not policy/value audit |
| Mailbox | public mailbox.deliver rejection, exception/ambiguous acknowledgement, accepted receipt | Real mailbox acceptance before injected post-delivery clock fault; full action/context record retained |
| Bookkeeping entry/body/exit | bookkeeping start_preparation_work, host settlement/oracle body, stop_preparation_work finally | Entry clock failure; body ordinary exception; body failure plus later exit clock fault; ensure occurrence order reflects body before finally |
| Settlement verification | run's runtime.settle and public settlement_oracle callback; mismatch branch; except ClockInvalid/Reversed; except Exception | Ordinary host exception containment, mismatch+cleanup, exceptions carrying clock vocabulary, distinguish body fault from cleanup echo |
| Publication entry/body/exit | publication_interval, builder.close, public write_trace, stop_preparation_work | Entry failure before write failure, write failure before exit failure, clean terminal cannot make failing receipt pass; public destination failure rather than private tampering |
| Finalization | finalize_accounting after publication; live failure vs dead skip | Final fault after known primary; no retry of dead source; null/false accounting remains honest |
| Host event generation/report construction | public fixture/script -> _events event construction, accepted/failed row creation, semantic/terminal construction | Inspect reachable ordinary exception exits and distinguish malformed fixture/public reporting failure from out-of-scope value-boundary audit |
| Host completion aggregation | journal[0] primary and journal[1:] secondary | Verify journal agrees with real occurrence order, equal-code multiplicity, no synthetic deduplication or recovery success |

Initial source risks to verify, not yet findings: settlement exception handling occurs outside the bookkeeping context and therefore after its finally cleanup; ClockInvalid/ClockReversed caught around settlement are assumed already journalled although the public oracle can raise them; trace publication catches only OSError subclasses. Establish real public paths and exact outputs before any verdict.

Planned evidence: verify full commit/manifest pair from Git blobs; record clean snapshot before/after; actual CPython 3.11.15 first and 3.14.6 second, -B -P, snapshot cwd, cleared whitelist environment, snapshot/src only PYTHONPATH and absolute PONTIUS_GIT. Diagnostic scripts and receipts are create-only cold-a-* under this packet checks directory; no source/test/config changes, broad suites, GPU, experiments, installations, commits, other reviewers, or Claude contact.
