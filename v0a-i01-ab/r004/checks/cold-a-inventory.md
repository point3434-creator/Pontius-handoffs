# Cold A independent invariant and related-path inventory

Recorded 2026-08-30 before opening coverage.md, any implementer self-report,
transcript or plan, or any current peer report. Reviewer: Codex cold A.
Candidate: c6adbcaa048988361d2388970eaca772711b797b
Manifest: a810c89b7342fb1bcb4f1498fdcf53cd11a589b70424c7da48f6619a45da67cb

Inputs so far: handoff and candidate identity, current CLAUDE.md and workflow,
required outcomes from value-boundaries/r001/disposition.md, frozen ADR0484,
ADR0485 and brief, frozen model.py and runtime.py admission consumers. No
coverage claim or current implementation/review narrative read.

## Invariants and paths

1. V-01: every public dispatch enters the outer measured transition before
   event admission, and obtains a complete exact immutable value graph before
   mutating spine/cards/indices/completion or emitting. Paths: dispatch ->
   admit_event/_copy_ingress_value -> all four _process_* handlers -> sealed
   spine/card kernels -> _finish_boundary -> optional controlled decision.
   Probe all four ordinary skipped-validator subclasses; exact outer
   OpponentActionEvent with invalid nested HandAction; bool/float aliases,
   invalid schema/index/identifier/card/action/seat/street variants where
   naturally constructible. A constructor refusal alone is not boundary proof.
2. V-01 refusal: malformed input cannot throw while constructing failure
   metadata. Paths: admission -> _HandFailure -> record -> _release_boundary
   -> _from_failure; pre-admission clock failures -> _clock_reject; dead or
   complete -> _reject. Unadmitted identifiers must be null or independently
   validated. Verify no accepted-envelope delta and unchanged public betting
   state, cards, and completion. Terminal failed status itself is permitted.
3. V-01 showdown: admission must own six exact immutable ranks; live seats
   have non-null ranks, folded seats null; compared rank domains are compatible
   before completion/advance. Paths: ShowdownResultEvent -> admission ->
   _process_showdown_result -> state.live_seats -> _strengths -> settle ->
   sealed NoLimitBettingState.settle. Exercise actual legal showdown, mutable
   list/empty vector, wrong live mask, mixed int/tuple ranks, malformed tuple
   member, valid all-int and all-tuple controls; preserve repeated settlements
   and independent expected payouts, including folded-seat and all-in states.
4. V-02: ActionMailbox.deliver validates every envelope field, exact nested
   action, and a valid receipt before inserting (hand_id, action_index).
   Wrong seat/street/action or bool/float keys must leave accepted empty;
   following valid delivery at integer key one must succeed exactly once,
   duplicate refused without delta. Check the returned/retained graph is exact
   and immutable. Public ActionMailbox accepted copy cannot mutate ownership.
5. V-03: genuine forwarded ActionMailbox delivery followed by malformed,
   subclass, bool/float alias, mismatched exact, or missing receipt means typed
   delivery_ambiguous/unknown, one attempt, no automatic or subsequent-dispatch
   retry, real delivery retained and not upgraded to known acceptance.
   Paths: _decide_inner -> _publish -> mailbox.deliver -> admit_receipt ->
   equality only after admission -> _accepted_deliveries -> failure/timing.
   Pair exact valid acknowledgment and known post-delivery clock-failure
   controls with malformed forwarded receipts.
6. Preservation: compare frozen change paths and inspect unaffected sealed
   kernels/spine; run focused frozen tests to retain blueprint authority and
   typed refusals, response clocks/cause order, known delivery semantics,
   all-in/side-pot/settlement controls. Do not count trace/publication or C
   surface findings as this value-only FIX round's residuals.

## Evidence plan

Recompute whole-row-sorted LF manifest from candidate blobs and compare exact
packet rows. Fresh D-local clone outside packet; CPython 3.11.15 first, then
3.14.6; -B -P; snapshot cwd and src PYTHONPATH; explicitly scrubbed process
environment; absolute validated PONTIUS_GIT. Record executable/version/import
origins before payload imports, commands, exits, and snapshot cleanliness.
Run focused existing value/runtime tests plus independently written attributed
public-boundary probes outside snapshot. No source changes, broad suite, GPU,
optional package installation, experimental owner, or integration action.
