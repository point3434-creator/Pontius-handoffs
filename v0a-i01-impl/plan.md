# v0a-i01-impl — implementation plan (first draft)

Drafter and finalizer: Claude (first draft at this checkpoint; roles
alternate next checkpoint). Cold reviewer: Codex. Date: 2026-08-30.
Controller authorization remains per commit.

Governance: ADR-0485 (the frozen contract), the ADR-0484 brief at
`docs/briefs/v0a-increment-1-brief.md`, docs/workflow.md (checklist v1,
Tier C), `docs/workflow-amendment-2026-08-30.md`. This plan adds no
authority: no rehearsal, production, or authorized-mode identity is created
during implementation; correctness runs use only
`pontius-v0a-hand-replay-v1-correctness-<unique-id>`.

Base: master `b357d33` (post ADR-0485 and workflow reconciliation).
Worktree: `D:/Pontius-worktrees/v0a-increment-1`, branch `v0a/increment-1`.
No test ever runs from the primary checkout; focused GREEN evidence comes
from fresh disposable D:-local snapshots (`-B -P`, snapshot `PYTHONPATH`,
scrubbed environment, absolute `PONTIUS_GIT`), dual-interpreter
(CPython 3.11 and 3.14) at every freeze.

## Slices (coherent contracts with their tests, per ADR-0485)

- **Slice A — hand core**: `src/pontius/v0a/__init__.py`, `model.py`
  (frozen event/action-envelope/receipt/record/outcome values and exact
  validation), `clock.py` (monotonic witness; outer-ledger adapter),
  `runtime.py` (visible-state transitions, blueprint outcomes, ready-to-emit
  checkpoint, mailbox delivery, interrupted timing), plus their tests.
- **Slice B — record and replay**: `trace.py` (canonical JSON, digests,
  parsing rejections, semantic projection), `replay.py` (explicit-deal host,
  fixtures A/B with the seed-bound suit permutations, settlement oracle,
  terminal accounting and host completion receipt), plus their tests.
- **Slice C — admission and gates** (mechanical): v0a origin classification
  and import policy in the boundary checker with focused boundary tests;
  `STABILIZATION_TEST_FILES` declaration; inventory/profile regeneration and
  honest census refresh; CI clone-safe gate. The legacy dependency baseline
  is never regenerated (byte-pin test included).

One review candidate per slice pair as size dictates: if A+B together stay
under ~3,000 changed lines they freeze as one round with named slices;
otherwise A freezes first. C rides with the final round. Rounds are
`review/v0a-i01-impl/r<NNN>` with packets here.

## Build order — deterministic RED before source, per contract

1. `model.py` events: RED for every rejection in the ADR's event table —
   boolean-as-integer, duplicate/overlapping cards, wrong seat/street/hand,
   repeated or skipped indices, premature reveals, events after completion,
   clock timestamps in events.
2. `clock.py`: RED for late-started walls (detectable), reversal rejection,
   invalid witness values, retained-sample identity — the recorded
   `(emission_observed_ns - wall_start_ns)/1_000_000_000` must equal the
   closing snapshot's elapsed seconds exactly.
3. `runtime.py` blueprint outcomes: separate REDs for miss→passive-default,
   legal hit, illegal matching entry (typed failure, no emission), invalid
   decision context; hidden-card isolation both ways — distinct hidden
   completions of one visible prefix must yield identical decisions, and
   data-flow controls reject host/complete-deal/mailbox reachability from
   selection.
4. Emission boundary: REDs at both cutoff edges and both deadline edges
   (±1 ns via deterministic witness), delay injection at the adapter
   boundaries including between the ready-to-emit checkpoint and mailbox
   acceptance; duplicate delivery; ambiguous delivery → `unknown`, never
   retried; clock failure before delivery and immediately after real
   acceptance (interrupted timing variant, null-not-false flags).
5. `trace.py`: REDs for duplicate/unknown/missing keys, wrong exact types,
   digest mismatches, truncated traces, semantic tampering, write failure
   after delivery (action stands; typed outcome; input stops).
6. `replay.py`: settlement mismatch against the independent chip-depth
   recomputation (side pots, ties, odd chips); semantic-byte equality across
   distinct run IDs; terminal accounting — pre-publication cut, separate
   `terminal_publication_compute_seconds`, publication-clock failure rejects
   host success despite a complete terminal row.
7. Slice C boundary/inventory/CI REDs: unclassified-module rejection,
   baseline byte-pin, census honesty.

Focused GREEN follows each RED cluster; the freeze carries the full focused
snapshot evidence on both interpreters. Fixtures A and B come from ADR-0287
as explicit chance outcomes with independent expected payouts; no historical
owner is invoked.

## Acceptance

The ten brief criteria against ADR-0485's acceptance map, verified in the
implementation self-report with commands, exits, counts, and hashes; then
freeze, two independent cold Tier-C reviews, controller authorization naming
the round, ceremonial commit by the finalizer, ref retirement, ledger lines.

## Forbidden

Everything in ADR-0485's kill criteria: no hidden data to policy paths, no
sealed-kernel or baseline edits, no invalid-blueprint recovery-as-passivity,
no V2-internal-stop-as-delivery, no erased late emissions, no ambiguous-
delivery retries, no fabricated credits, no GPU/optional dependencies, no
namespace widening, no operation without the later measured closure.
