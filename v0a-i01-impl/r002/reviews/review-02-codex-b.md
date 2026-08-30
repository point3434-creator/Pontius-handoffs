# Cold Tier-C review 02 - Codex B

Verdict: **NOT CLEAN**. Specification: **FAIL**. Engineering correctness: **FAIL**.
Confidence: high. Nine Important findings survive fresh bounded verification.
No Critical finding is asserted.

Candidate: `refs/heads/review/v0a-i01-impl/r002`
Commit: `18c965d1f3445c253a6333c4d10899c1dcac0cc6`
Base: `b357d333fc2393b7fc7dcf31f30c86616208c817`
Tree: `35f00349a7538cffc02f8e81f71913251be200be`
Manifest: `4cfd14ac7bfdb22e052bb9f625610657c01aafa07182acf58d19367a8816cb18`
Reviewer: Codex B, independently dispatched cold reviewer, 2026-08-30.

Every source location below refers to this frozen commit, not mutable working bytes.
Inputs: CLAUDE.md, workflow/checklist, frozen ADR-0485 and brief, and approved r002
handoff/candidate/manifest. No other review, prior findings, implementer self-report, or
chat transcript was read. Coordinator supplied objective suite receipts and snapshots.

## Important findings

### B1 - Finalization failure still returns a successful completion receipt

Severity: Important / P1. Confidence: high; reproduced on both interpreters.
Locations: `src/pontius/v0a/runtime.py:293-303`;
`src/pontius/v0a/replay.py:496-502,538-550`.
Requirement: ADR-0485 requires outer finalization for host success and forbids success
when later reporting fails.

Run real fixture A normally, but make the witness source raise OSError on observation
138, the final outer finalization observation in the deterministic baseline. Runtime
catches the normalized clock failure and marks accounting incomplete. Host still uses
`totals` and `passed` captured before finalization: its receipt has `passed=true`,
`accounting_complete=true`, no primary/secondary failure, and a trace digest. The public
`runtime.accounting()` then reports incomplete/null totals.

Evidence: `finalize_clock_failure` in both `cold-b-*-diagnostics-v3.txt` receipts.
Correction: propagate finalization's typed result and derive final receipt flags after
publication closure and finalization; preserve primary and subsequent failures.

### B2 - Clock failures escape the host instead of retaining its outcome

Severity: Important / P1. Confidence: high; reproduced on both interpreters.
Locations: `src/pontius/v0a/replay.py:395-405,472-489,509-538`;
`src/pontius/v0a/runtime.py:253-276`.
Requirement: ADR-0485 requires a returned host receipt, retained delivered decisions,
honest null measurements where closure is impossible, and terminal reporting only with
a valid clock and honestly closed active intervals.

Three real schedules lose the required ReplayOutcome:

- Failure on clock call 1 is typed by dispatch, but unconditional publication raises
  `RuntimeError: publication measurement requires a started hand`.
- After real ActionMailbox acceptance, arm failure at `finish_action`. Dispatch retains
  a known delivered decision, but publication raises
  `RuntimeError: on-clock work cannot be labeled as preparation`. The mailbox contains
  action 1 while no receipt or retained decision is returned to the caller.
- Failure at observation 137, closing publication after four actions, escapes as
  ClockInvalidError after the terminal was constructed, with no receipt.

Evidence: `initial_clock_failure`, `clock_failure_after_real_acceptance`, and
`publication_close_clock_failure` in both v3 receipts. The mailbox wrapper calls real
acceptance before arming the clock; it does not substitute an acceptance result.
Correction: contain typed failures through settlement/publication/finalization, skip
impossible closure, preserve the first cause, and return retained records with failed,
incomplete receipt fields instead of losing the outcome during reporting.

### B3 - A delegate can emit a false hit under an empty policy's digest

Severity: Important / P1. Confidence: high; reproduced without production monkeypatching.
Locations: `src/pontius/v0a/runtime.py:63-101,168-175,397-426,801-815`.
Requirement: ADR-0485 permits the immutable blueprint as policy input, binds its canonical
identity at initialization, and requires unchanged `action_for` semantics. A miss must
be passive. Arbitrary callbacks and hidden-data carriers are excluded inputs.

Wrap a real empty ImmutableBlueprintActionSource in a plain object exposing its genuine
digest and empty entries. Delegate to real `action_for`, then return
`replace(selection, action=raise_to(6), table_hit=True)`. No introspection, sealed-class
edit, monkeypatch, or digest forgery is needed. Runtime accepts the object, emits raise
to 6, and records a table hit under the empty table's canonical digest.

Evidence: `delegated_false_hit_under_empty_canonical_anchor` in both
`cold-b-*-blueprint-binding.txt` receipts: zero entries, one accepted raise, matching
anchor digest, and no failure. An honest delegate reporting a changed digest is caught;
that check does not prove the supplied object is immutable or that a claimed hit exists.
This is a public-input contract breach, not the excluded malicious-introspection threat.
Correction: enforce a canonical immutable source at the production boundary and invoke
the trusted unchanged lookup. Tests must not require admission of arbitrary policy
objects. A second full-policy rehash per action is not needed.

### B4 - The trace reader establishes neither legal replay nor semantic identity

Severity: Important / P1. Confidence: high; reproduced on both interpreters.
Locations: `src/pontius/v0a/trace.py:583-746,749-794`;
`src/pontius/v0a/replay.py:383-561`.
Requirement: ADR-0485 requires a separately written checker of legal transitions,
actions/payouts, source/context bindings, semantic digest, ordering and terminal facts.

Change fixture A's first decision to raise-to-1, illegal facing the 2-chip big blind,
leaving the recorded before/after states unchanged. Recompute prefix and semantic
hashes. `parse_trace` accepts it with `terminal.passed=true`. Even replacing only the
semantic digest with 64 zeroes is accepted. The exported semantic helper hashes supplied
projections; neither new module supplies the required independent transition/policy
checker. A self-consistent digest of false rows has no semantic judge.

Evidence: `illegal_decision_with_all_digests_rebound` accepts the illegal action with
matching hashes; `semantic_digest_not_checked` accepts a semantic mismatch, on both slots.
Correction: add the preregistered independent replay boundary, bind trusted inputs, and
compare reconstructed transitions, policy choices, settlement, counts, failure/timing
facts and both digests before accepting a trace.

### B5 - Strict parsing admits malformed nested events and non-finite timing

Severity: Important / P1. Confidence: high; reproduced on both interpreters.
Locations: `src/pontius/v0a/trace.py:472-518,598-608,645-652,714-717`.
Requirement: ADR-0485 rejects unknown/missing fields, wrong exact types, bad enums and
non-finite numbers throughout the schema, including nested variants.

Add `extra=true` and set `event_index=true` inside a real event, rehash the prefix, and
parse. The unknown field and boolean index are accepted: only outer event-row keys and
the nested schema string are checked. Separately put JSON NaN into completed timing's
`response_compute_seconds`; default JSON loading accepts it and `value < 0.0` does not
reject it. The passed terminal remains accepted and the semantic digest still matches
because timing is outside the projection.

Evidence: `invalid_event_schema_accepted` and `nan_timing_accepted` in both v3 receipts.
Correction: exhaustively validate nested event variants; reject non-finite JSON constants
and require finiteness for every measurement, independently of B4's semantic checks.

### B6 - Decision serialization disappears from reported compute totals

Severity: Important / P1. Confidence: high; reproduced on both interpreters.
Locations: `src/pontius/v0a/replay.py:395-410,412-429,496-527`;
`src/pontius/v0a/trace.py:326-342`.
Requirement: ADR-0485 charges post-delivery trace work as preparation or post-terminal
bookkeeping, with preceding row work complete at the cut. Terminal publication is separate.

Wrap real TraceBuilder.add_decision and add one second of deterministic clock cost per
serialized decision. Fixture A still emits four actions and passes. The clock advances
four extra seconds but all totals equal baseline: preparation 0.000061, post-terminal
0.000002, publication 0.000001 seconds. Serializers execute between dispatches without
an outer bookkeeping interval.

Evidence: `unmeasured_decision_serialization` and its delta in both v3 receipts. The real
serializer executes; the wrapper adds cost and replaces no ledger or result.
Correction: measure each post-delivery row construction/serialization/write in a public
outer interval before the next dispatch, classify by terminal state at entry, and close
all preceding rows before the terminal cut. Keep terminal publication separate.

### B7 - Settlement comparison ignores final stacks and eligible seats

Severity: Important / P1. Confidence: high; reproduced on both interpreters.
Locations: `src/pontius/v0a/replay.py:214-265,472-494`.
Requirement: brief criterion 1 and ADR-0485 require exact conservation and independent
validation of published payouts, final stacks and ordered pots including eligible seats.

Let real fixture-A settlement finish, then corrupt only its returned final stacks to six
zeroes. The unchanged host comparison passes and publishes them, losing all 1,200 chips.
Separately replace the pot's eligible seats with `(0,)`; it still passes while payout
awards 12 chips to seat 3. Real payouts, pot amounts and the independent oracle remain
unchanged. Host compares only payouts and pot amounts, discarding eligibility and the
independently derivable final stacks.

Evidence: `oracle_omits_final_stacks` and `oracle_omits_pot_seats` in both v3 receipts.
These corrupt the real settlement return at the production comparison, rather than
substituting a judge. They prove a verifier gap, not a newly alleged sealed-kernel defect.
Correction: compare every settlement field, including ordered eligible sets and each
`start - contribution + payout`, with exact conservation. Oracle injection itself is
not the established defect.

### B8 - Established outer transition cutoff/deadline flags are discarded

Severity: Important / P2. Confidence: high; reproduced on both interpreters.
Locations: `src/pontius/v0a/runtime.py:579-598,622-625,888-917`.
Requirement: ADR-0485 interrupted timing retains truths from any earlier valid outer
snapshot; null is allowed only where a flag was not established.

Add 15,000,000,001 ns before real OUTER finish_transition_boundary sampling. Its public
snapshot has `deadline_crossed=true`, `work_remaining_seconds=0.0`. Fail the next witness
call in V2 decision opening. Dispatch retains valid start/last observation but records
both flags null. `_finish_boundary` discards the action snapshot; only the later ready
checkpoint populates the remembered flags.

Evidence: `established_transition_flags` in authoritative v3 receipts, restricted to
`self is runtime._outer`. Earlier v2 did not isolate that ledger and is not used here.
Correction: preserve flags from the public transition action snapshot before further
fallible work and retain them monotonically through interruption.

### B9 - A known delivered late action is excluded from terminal decision_count

Severity: Important / P2. Confidence: high; reproduced on both interpreters.
Locations: `src/pontius/v0a/replay.py:397-405,518-520`;
`src/pontius/v0a/trace.py:728-732`.
Requirement: ADR-0485 decision_count counts known delivered actions, including failed,
late or interrupted delivered actions. Failure does not imply nondelivery.

After real mailbox acceptance of fixture A's first action, add 16 seconds before the
acknowledgement returns. The outer snapshot closes, the deadline failure and full decision
are retained, and mailbox contains one action. Host publishes decision_count zero because
it counts records without a failure_reason. Reader's one-sided count check accepts it.

Evidence: `delivered_failure_decision_count` in both v3 receipts.
Correction: count known deliveries independently of success and enforce exact agreement
between terminal counts, delivered decision rows, and failure delivery facts.

## Evidence, coverage and limits

Independent scripts recomputed all ten changed blob hashes using absolute Git, whole-row
byte sorting and LF rows. These bytes equal manifest.sha256 and its pinned hash. Each
snapshot file equals its candidate blob before imports. Both handoff-designated unchanged
digests match. All changed paths are additive; sealed kernels/baseline are unchanged.

Every diagnostic asserts actual executable, CPython, full version, cwd and PYTHONPATH
before payload import, then verifies runtime import origin. The scrubbed environment
contains only Windows basics, snapshot PYTHONPATH and absolute PONTIUS_GIT. Runs used
`-B -P` in the coordinator's fresh D-local disposable snapshots:

- 3.11.15: D:/pontius-snapshots/v0a-i01-r002-c988362507a842839a2e58c1d6907e19/harness
- 3.14.6: D:/pontius-snapshots/v0a-i01-r002-4b9831493f2b4f30acc081e8df5e8654/harness

Create-only checks, each interpreter exiting 0:

- `cold-b-py311-diagnostics-v3.txt`, `cold-b-py314-diagnostics-v3.txt`.
- `cold-b-py311-blueprint-binding.txt`, `cold-b-py314-blueprint-binding.txt`.
- Scripts: `cold-b-diagnostics-v3.py`, `cold-b-blueprint-binding.py`.

Command shape, with exact argv/identity captured in every receipt:
`<actual-python> -B -P <packet-script> <expected-python> <expected-version> <snapshot>`.
Exit 0 means the reproduction assertions held, not that the candidate passed. Earlier
create-only script revisions remain preserved; v3 is this report's diagnostic authority.

Coordinator raw receipts `codex-py311-verification.json` and `codex-py314-verification.json`
report 99 focused tests passing per interpreter. These are coordinated suite evidence,
not suites independently rerun by this reviewer. Existing controls cover normal A/B,
miss/hit examples, completion, acknowledgement, and selected schema/clock faults. The
new accounting test asserts positivity/self-consistency; it does not charge delayed
serialization. Those green tests do not cover the reproduced failures above.

| Requirement or risk | Evidence | Assessment |
| --- | --- | --- |
| Frozen identity / additive scope | Independent blobs and manifest | Established |
| Normal A/B and narrow regression controls | Fresh suite receipts | Pass at tested scope |
| Host completion/failure retention | Real host clock schedules | Fail B1-B2 |
| Immutable policy-only input | Unpatched delegate probe | Fail B3 |
| Semantic replay and strict schema | Rehashed trace mutations | Fail B4-B5 |
| Complete compute accounting | Real serialization delay | Fail B6 |
| Independent settlement fields | Settlement corruption controls | Fail B7 |
| Interrupted flags / delivery counts | Outer snapshot and mailbox | Fail B8-B9 |
| Run-independent projection | Source and distinct-run control | Narrow pass |
| Completion and acknowledgement | Source and focused controls | No extra finding |
| Slice-C inventory/import-policy/CI | Explicit handoff deferral | Out of scope |

Runtime/model/clock have no replay imports; built-in host supplies visible events and
controlled cards only. B3 prevents a general policy-input isolation claim despite that
built-in path. The chip-depth oracle is independent of production pot assembly; B7 concerns
comparison omissions, not the injectable judge parameter alone. Filesystem race/hardening
was inspected but not independently executed in this pass; no pass is asserted there.

No source/test/config edits, commits, owner invocation, GPU work, broad suite, operation
authorization, source seal, research/timing result or strategy result is asserted. No
other review was used to fill evidence gaps. No fixes were implemented.

Recommendation: do not advance r002 to broad acceptance or integration. Preserve r002 and
resolve findings under the next-round and circuit-breaker rules. Claude remains finalizer.
The reviewer's task-ledger verdict awaits the coordinator's serialized write slot; this
report does not authorize a commit or delegate the verdict to a different writer.
