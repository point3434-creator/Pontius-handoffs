# Increment-one preregistration r2 — cold review C (Claude)

Issuer: Claude Fable 5, controller-side reviewer (cold_review_c). Date: 2026-08-30.
Role: independent whole-candidate review per r2-handoff.md. I did not author
either candidate, did not read r1/r2 reviewer findings before forming this
verdict, and reviewed git blobs only — no mutable working files.

## Binding

- Candidate: `119411fda2376d61d9ff310bada71f25aa64de70`
  (ref `refs/heads/review/v0a-increment-1-prereg-r2`, tree `c7630b5a84b4…`)
- Manifest SHA-256: `da3c4ad5290a49f9d6e600b61e3190047ca6221394a4fc4ad06e40af727d799c`
  — independently recomputed from `diff-tree`/`cat-file` blob bytes per the
  docs/workflow.md convention; byte-exact match, two rows, scope exactly
  `STATUS.md` (M) and
  `docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md` (A).
- Parent verified as mainline HEAD `ca0b2e41bbf5d9fc1649de20379299331de6591a`;
  primary checkout clean at that commit.
- Declared pins verified against base: Brief-Blob `8ef19c83…` and
  Legacy-Baseline-Blob `5fe6ee47…` both match `git rev-parse` at the base
  commit exactly.
- Hygiene: both candidate blobs are LF-only, no BOM, no trailing whitespace,
  final newline present.

## Verification performed

**Mechanical.** From my own fresh disposable snapshot (`--no-hardlinks`,
`core.autocrlf=false`, detached at the candidate, scrubbed environment,
snapshot `PYTHONPATH`, absolute `PONTIUS_GIT`, `python -B -P`, CPython
3.14.6 dev slot): `python -m pontius.status_generation --check` reports
"STATUS.md is current" (exit 0) and `tests/test_status_generation.py` passes
12/12 — the candidate STATUS.md is the generator's honest projection of the
ADR set including ADR-0485, and the machine-checked continuity directives
hold. This independently confirms the issuer's dual-interpreter receipts on
the mechanical claim (the 3.11 receipt remains theirs; I did not repeat it).

**Sealed-API conformance.** Every surface the contract names exists at the
base commit with the claimed semantics:

- `ActionClockLedger` (`src/pontius/action_clock.py:145`) accepts an injected
  `clock_ns` witness callable; `start_transition_boundary()` (line 401)
  returns a boundary value whose `started_ns` is public — the runtime never
  needs a sealed private field; `finish_transition_boundary(...)` (line 443)
  takes `starts_controlled_action` and `controlled_action_public_state_sha256`
  and backdates the response wall to event arrival inside the sealed ledger;
  `finish_action()` (line 539) closes on exactly one clock observation, so a
  witness that retains its last returned sample yields precisely the
  nanosecond the closing snapshot used.
- Elapsed arithmetic (line 240–243) is `(observed - started) /
  1_000_000_000` in float division of the same two integers the runtime
  holds, so the ADR's required exact equality between
  `(emission_observed_ns - wall_start_ns)/1_000_000_000` and the snapshot's
  elapsed seconds is reproducible without a second clock. `deadline_crossed`
  is strict `elapsed > 15.0` (line 263) — consistent with the ADR's
  ">15,000,000,000 ns is a violation; exactly the boundary is as the ledger
  interprets it". Constants are 15.0/1.0 (lines 23–24), so the 14,000 ms
  work cutoff equals wall minus reserve. Snapshot exposes
  `response_compute_seconds` / `response_uninstrumented_seconds` /
  preparation totals under exactly the names the timing/terminal records use.
  Post-delivery trace writes can legally charge as ledger preparation
  intervals (`start_preparation_work` is valid between actions), matching
  "uncredited preparation or post-terminal bookkeeping".
- `LegalDecisionSpineV2` (`src/pontius/legal_decision_spine_v2.py:98`)
  accepts `action_clock=`/`clock_ns=` injection ("one witness for both
  ledgers" is implementable); `emit_controlled_action(*, candidate,
  fallback)` (line 340) matches the `candidate=None` + validated-fallback
  usage, and with `candidate=None` the spine's reason is deterministically
  `no_candidate` on successful runs — the semantic projection stays
  timing-free. `public_betting_state_sha256` exists (line 28);
  `ActionSelectionReasonV2` spellings (line 73) ground "unchanged V2 enum
  spelling".
- `ImmutableBlueprintActionSource.action_for(*, cards, betting, decision)`
  (`src/pontius/immutable_blueprint.py:348`) takes exactly the four inputs
  the ADR permits policy selection; `digest` is the canonical SHA-256;
  `passive_blueprint_action` (line 274) is check → call → fold verbatim;
  `require_legal_blueprint_action` raises on an illegal entry, grounding the
  typed-failure split.
- `BettingAction` (`src/pontius/no_limit_betting.py:51`) is kind +
  `raise_to`, docstring "raises name the total street contribution" — the
  ADR's raise-to semantics match the sealed kernel exactly; positive-int and
  null-otherwise constraints already enforced kernel-side. `SidePot`,
  payouts with odd-chip distribution and in-kernel conservation, and
  contribution-layer ordering ground the settlement object and "tied pots
  and odd chips" controls.
- `OneSeatCardState` (`src/pontius/holdem_cards.py:134`) carries controlled
  seat, private hand, street, board with overlap/count validation;
  `SixSeatHoldemDeal` (line 67) is the host-side complete-deal type;
  `river.py` is the public evaluator reserved to `replay`.
- ADR-0287 defines Fixture A (passive four-street showdown) and Fixture B
  (multiway all-in side-pot runout) with expected payouts, as reused;
  ADR-0290 exists as the explicit-deal loop. Suit-permutation seed variants
  are sound: consistent whole-deal suit renaming is a poker isomorphism, so
  ranks, actions, and payouts are preserved; the mod-24 lexicographic
  derivation is total and unambiguous.

**Contract review.** The candidate covers all five bullets of the brief's
"Contracts the preregistration must freeze": event types/ordering with the
showdown crossing isolated behind permanently-disabled policy selection;
identifiers, exact raise-to, and per-record source/policy/state bindings;
ledger-derived timing with no second clock (verified above); typed failures
including trace-write-after-emission with the delivered action standing and
durability honestly unestablished when the independent reporting path also
fails; and the replay round-trip split (exact semantic bytes across distinct
run IDs; timing validated structurally against recorded walls). The
interrupted-timing variant and the run-ID-free semantic projection (the two
r1 topics named in the preparation report) are specified honestly — null
rather than fabricated measurements, flags true only when established by a
valid earlier snapshot. ADR-0484 conformance holds: blueprint outcome split
verbatim (miss → passive; illegal entry/invalid context → typed failure, no
emission; stale is not a category), input boundary, frozen record fields,
no h32/GPU/resolver, steering and CI-growth rules untouched. Front-door
metadata is complete and correct (Research ADR-0280, Process self, Contract
ADR-0307, Revoked list verbatim); the change boundary matches the brief's
may-change list; kill criteria and claims boundary are sharp; no number is
invented where ADR-0482 demands measured provenance.

## Findings

No Critical or Important finding survives verification. Non-material notes:

- **N1 (note).** Work-cutoff enforcement is check-bracketed (outer-ledger
  inspection before and after blueprint work) rather than continuous over
  the emit/delivery path; the ADR discloses this ("no noncooperative-worker
  cancellation"), pins the flag's meaning to those checks, and the full
  interval remains visible in `elapsed_ns` with the deadline check at
  emission. Implementation tests should still inject delay between the
  after-work check and mailbox acceptance to exercise that sliver — the
  brief's adapter delay-injection requirement already demands this.
- **N2 (note).** The event/visible-card schema key `private_cards` is a
  v0a-defined name; the sealed `OneSeatCardState` attribute is
  `private_hand`. Provenance naming only — the contract defines its own JSON
  schema — but the implementer should not expect attribute-name identity.
- **N3 (note).** `run_id` charset/length is not pinned beyond the general
  nonempty-ASCII ID rule; it is excluded from the semantic projection, so
  evidence identity cannot depend on it. Pin exact validation at source seal.
- **N4 (note).** The terminal's `post_terminal_compute_seconds` must be
  measured by the witness after outer-ledger finalization (the sealed ledger
  refuses post-finalize charging); the ADR's "post-terminal bookkeeping"
  wording permits this, and the shared witness keeps it a single clock.

## Controller decision points (not defects)

1. **Bootstrap-sequencing clarification.** The candidate resolves the
   ADR-0482 circularity (budgets need rehearsal provenance; rehearsal needs
   sealed source; source needs preregistration) by the five-step ladder,
   deviating from the brief's "binding numbers set at preregistration" in
   the protocol-conservative direction: nothing is invented, the inherited
   15,000/1,000 ms walls are not relaxed, the two-death stand-down binds
   now, the lane budget binds at the measured closure and counts every owner
   without reset, and step 4's absence is an unconditional no-invocation
   gate. The ADR states this requires the controller's approval with the
   decision itself; accepting ADR-0485 constitutes that adoption.
2. **CodeRabbit.** The external review remains unrun because launching it
   transmits private repository content to the external service; that
   permission is the controller's to grant, and no workaround was attempted.

## Verdict

**CLEAN** at candidate `119411fd` / manifest `da3c4ad5…`. No material
specification finding. The candidate is fit for the controller's adoption
ruling, the pending external-review permission decision, and — on the
controller's explicit word — the ceremonial commit
"Preregister the blueprint-only v0a hand contract".
