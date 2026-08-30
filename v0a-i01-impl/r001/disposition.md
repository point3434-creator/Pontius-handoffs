# Slice A r001 review disposition and fix-round brief

Coordinator: Codex /root. Date: 2026-08-30.
Finalizer: Claude, the first drafter at this checkpoint.
Outcome: NOT CLEAN; return Slice A for a bounded correctness fix round.

Candidate: 2d059f90fb6cec27e4090ad0432c68759a760960
Manifest SHA-256: fc090d962a914b41dec932f21a6c8421499191ccac9dca40363a078cbba95b0c
Ref: refs/heads/review/v0a-i01-impl/r001
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 7672cad16e0624db73e38095cf3d70d74144b8da

## Scope and independence

The coordinator read the implementer's informal self-report, so this document is
an evidence-backed consolidation, not a third cold review. Two fresh reviewers
received the frozen identity, five-file scope, accepted contract and checklist,
without that report or one another's findings. Their attributed reports and own
ledger entries are retained in reviews/. Claude retains finalization; no source
edit, source seal, ceremonial commit, integration, or experiment is authorized by
this review. R001 remains immutable. Changed candidate bytes require r002.

Trace/replay/explicit-deal host, the independent settlement oracle, final terminal
accounting, origin classification, inventory and CI are declared slices B/C.
Their absence is not used as a finding against Slice A.

## What the evidence establishes

Both final v3 runs used fresh disposable, detached D:-local snapshots of the frozen
commit, with no alternates/hardlinks, a scrubbed environment, absolute Git,
python -B -P and the exact snapshot PYTHONPATH. The child executable, CPython
implementation and full version were asserted and recorded before Pontius import.
Module paths resolve inside the snapshot. Candidate bytes and snapshot status
remain unchanged. The whole-row-sorted blob manifest reproduces exactly.

- CPython 3.11.15: the existing 36 tests pass, exit 0.
- CPython 3.14.6: the existing 36 tests pass, exit 0.
- Eleven diagnostic schedules complete on each interpreter and expose the same
  contract violations. Their exit 0 means the diagnostic completed, not that the
  candidate met its contract. Expected-vs-observed failures are detailed below.
- NumPy is a declared required dependency. No CuPy or Torch scientific import was
  observed. This is scoped CPU verification, not a broad profile or CI verdict.

Final receipts: checks/codex-py311-v3-verification.json and
checks/codex-py314-v3-verification.json, with *-identity.json, *-suite.txt and
*-probes.txt alongside. The v1/v2 reviewer-runner limitations and the corrected
v3 pre-import provenance are recorded in checks/codex-verification-setup-note.md;
prior helpers/diagnostic outputs remain intact. No old result is relabeled.

## Accepted findings, ordered for the fix round

### F1 — Start the response boundary before event work (Important)

Frozen runtime.py:189-220, 249-275, 285-315. ADR-0485 requires the outer
start_transition_boundary at dispatch entry, before validation and visible-card
construction. The reveal handler calls the real OneSeatCardState.advance_to first.
With an injected 16,000,000,000 ns delay around that real method, a valid flop reveal
that makes seat 1 act returns decided, elapsed_ns=0 and deadline_crossed=false.
The event arrives at 1000; the recorded wall starts at 16000001000.

Correction: establish the outer ledger before event processing, acquire a single
boundary at event entry, then validate/transition/classify that interval. Apply the
same rule to hand start, opponent actions and reveals. Preserve the special rule
that a dead/broken hand accepts no new input and never queries a broken witness.
Regression: delay actual pre-decision adapter work on each decision-producing event
path; require that its duration affects the ledger and cutoff/deadline outcome.
The current late-start test covers a narrower hand-start read sequence and misses
this real reveal path; do not pin a replacement test only to private read counts.

### F2 — Make showdown completion irreversible (Important)

Frozen runtime.py:329-381, especially 379-381. An accepted showdown never closes
further input. A second correctly indexed showdown_result replaces _strengths.
The real passive six-seat hand settles its 12-chip pot to seat 5, then accepts a
second strength vector and settles the same pot to seat 0. hand_complete was
already true before the second event.

Correction: represent awaiting-showdown versus completed explicitly. Accept the
strength vector exactly once, disable policy before accepting it, reject every
later event, and preserve the first accepted settlement facts. Regression: replay
a real hand through showdown; attempt a second vector and other post-completion
events; assert typed event_order and no rewritten strengths/payouts.

### F3 — Bind an actual immutable blueprint and validate its selection (Important)

Frozen runtime.py:60-98, 151-159 and 660. Construction only tests for action_for and
digest attributes; it never saves a canonical initialization digest. A delegating
source can switch immutable policies after hand start, and the next record simply
adopts the replacement digest. A second probe supplies an empty-policy digest yet
returns a legal raise with table_hit=False: the runtime delivers it and labels it
passive_default. Legality alone does not prove blueprint provenance or outcome.

Correction: admit the intended immutable source through a narrow validated boundary,
bind its canonical digest once, and validate returned source/key/outcome bindings
before delivery. Reject mismatches with the existing typed vocabulary. Production
selection must not admit arbitrary host/future-aware callbacks through the source
argument; preserve fault-injection seams without broadening that production input.
Keep the sealed action_for API unchanged. Regression: same-hand source replacement,
foreign key/digest, fabricated table-hit/miss action, and input-boundary controls.
These probes use supplied source objects accepted by today's public constructor;
they do not claim that a frozen ImmutableBlueprintActionSource mutates itself.

### F4 — Contain clock faults and retain established timing (Important)

Frozen runtime.py:219-220, 235-236, 273, 314, 351 and error-path closers;
clock.py:49-53. Invalid clock values on the initial or later boundary escape as
ClockInvalidError. An OSError from the supplied clock escapes unchanged. Failure
on the third hand-start clock read returns a typed failure but timing=None, despite
a valid outer boundary having already established the start.

Correction: make acquisition and all closing/abort observations part of the typed
failure boundary. Normalize ordinary source-read failures, retain the first cause,
keep the witness permanently failed, and pass every valid established start into
the interrupted record. Do not repair/requery a failed witness. Regression: faults
at construction/entry, V2 transition, boundary finish and abort, including before
and after start establishment. This is a runtime defect, not an interpreter issue.

### F5 — Preserve delivery ambiguity for clock exceptions too (Important)

Frozen runtime.py:547-548. A supplied mailbox calls the real ActionMailbox.deliver,
then raises ClockInvalidError before returning its receipt. The real mailbox has
accepted one action, but the failure says delivery_status=not_attempted.

Correction: once the delivery call begins, exception class cannot establish that
publication never happened. Without an unambiguous rejection or valid receipt,
retain unknown and never retry. Do not infer accepted from the diagnostic mailbox
registry: the runtime did not receive that acknowledgement. Regression: exceptions
of several classes on either side of real mailbox acceptance, including clock errors.

### F6 — Validate the acknowledgement before claiming delivery (Important)

Frozen runtime.py:540. The return value of deliver is discarded. A malformed
supplied mailbox returns None without accepting anything; runtime reports decided.
The real ActionMailbox normally returns the proper receipt, so this probe establishes
missing admission/acknowledgement validation, not a defect in that concrete mailbox.

Correction: require an exact receipt bound to the emitted hand/action identity before
claiming acceptance. Wrong/absent acknowledgements fail closed with honest uncertainty
about publication, not success or retry. Regression: matching receipt, missing receipt,
wrong hand/action, and malformed return, each through the same publication boundary.

### F7 — Keep already established violations on interrupted timing (Important)

Frozen runtime.py:521 and 675-695. Decision work advances the witness by
14,000,000,001 ns, so the valid ready snapshot establishes cutoff=true. A real
mailbox accepts, then poisons the closing clock. The retained decision correctly
has interrupted timing and accepted delivery, but work_cutoff_crossed is reset to
null. That erases a measurement already established by the authoritative ledger.

Correction: retain observed cutoff/deadline truths for the response. Carry true
into interrupted records; use null only where no valid observation established
that flag. Preserve measurements without another read of the failed clock.
Regression: known-cutoff and known-deadline prefixes followed by failures at
pre-delivery, delivery and post-acknowledgement boundaries.

## How to make the next version simpler and faster to validate

Do this as one coherent Slice A fix round before adding B/C. Centralize entry timing
and delivery outcome handling; explicit state transitions should make completion,
publication attempt, acknowledgement and clock interruption hard to confuse. This
reduces duplicated exceptional paths and gives the tests a small, clear matrix.

Capture the canonical blueprint binding once and compare returned identity values;
avoid adding a second full-policy rehash per decision merely for validation. The
sealed action_for implementation already performs canonical hashing. Its table scan
and hashing may deserve later measurement at a declared realistic policy size, but
this review establishes no runtime bottleneck or speedup. Keep performance changes
compatible with the unchanged API and the measured-budget/source-seal sequence.

The controlled-seat guard is not a blocker. Its removal is an observationally
equivalent mutation when the wrong-actor guard yields the same event_order result.
Keep the explicit rule if it improves readability; do not manufacture a private
state or helper-double test merely to kill an equivalent mutant. Removing the empty
_next_event_index_after_decision method and unused locals is optional cleanup, not
performance evidence or a reason to reopen a clean round.

Follow the existing RED/GREEN rule: turn each concrete failure above into an
independent public-boundary regression against r001, preserve that RED receipt,
make the smallest source correction, then run the complete focused suite on actual
3.11 and 3.14. Freeze r002 and request fresh reviews. Both required cold passes and
all applicable gates must clear before Claude finalizes and requests the controller's
specific commit authorization. R001 was never a source seal or an experiment result.

## Final reviewer reconciliation

Both issued reports are NOT CLEAN, bound to the same candidate/manifest above.
Review A groups the two delivery issues together; review B separates them. The
seven-item coordinator list decomposes the same substantive findings; it does
not represent a disagreement or an additional cold-review verdict.

| Coordinator item | Review A | Review B |
| --- | --- | --- |
| F1 ingress wall | A-01 | B1 |
| F2 terminal showdown | A-03 | B4 |
| F3 blueprint authority | A-02 | B3 |
| F4 clock failure/start | A-05 | B2 |
| F5 delivery ambiguity | A-04 | B5 |
| F6 delivery acknowledgement | A-04 | B6 |
| F7 retained timing flags | A-06 | B7 |

Issued report digests:
- reviews/review-01-codex-a.md:
  2633f8b64eae391aff0edcdcf7cdc5fb22b3261ca9a34947c85a37b2e9e9c558
- reviews/review-02-codex-b.md:
  56064683adc1d7fa3074206b9d70c79c40c57551da806501a5bf9910ab9fa235

The coordinator read both reports, verified their bytes and issuer-written ledger
entries, and accepted the substantive findings. Review B's schema/spine-label
observations remain nonblocking follow-up for model/parser coverage. No issued
findings or frozen input bytes were rewritten. The original implementer receipt
has CRLF working bytes and LF Git blob bytes; Git reports no content change. It
was left untouched, and its line-ending conversion is not a candidate finding.
