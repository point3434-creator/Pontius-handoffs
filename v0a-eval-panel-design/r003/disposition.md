# Disposition: v0a-eval-panel-design/r003

Finalizer: the round's drafter (Claude). Date: 2026-09-08. Both cold reviews
returned **CLEAN / SOUND**: no Critical or Important finding survives
frozen-source verification, and the design's shape is judged appropriate to
the declared game with no further change of shape indicated.

Outcome: **r003 is the accepted specification for the lane.** Per the
workflow's invariant order, the next step is the controller's ceremonial-commit
authorization; nothing here grants it. Candidate identity is unchanged:
`18b7527a3989f7d38830a7881c976385fe9bc4de`, manifest
`2664aca6f857999a4b45036b5cd3c250fbc3d8210b3132510d0e05a57e821975`, base
`b378104c`.

## What the reviews established

Both verified, independently and against frozen blobs: the outcome classifier
matches the real session/host/event envelopes including every failure path the
runtime and host can produce; the retained frame stream and its truncation flag
are sound as the post-hoc source of the river record; the independent
`action_for` cross-check is necessary because the v1 host computes no lookup;
prefix-divergence retention is required by the deployed-policy estimand;
withholding the full-population claim on any exclusion correctly refuses the
survivor substitution; the normalization equations, `[−4s, 4s]` unit range,
Hoeffding floor, and `1/4` strata weights are consistent; the per-hero T1
partition, static `s = 4`, collision-only acquisition, and fixed strata survived
the r002 edits intact; the path-organized coverage claim matches both
reviewers' independent inventories; all 21 blob pins recompute.

## Advisory items, all carried forward

None is a finding; each becomes an obligation of the implementation round.

| Advisory | Disposition |
|---|---|
| The 21-blob inventory is a direct semantic inventory, not a transitive closure. Reviewer 01 named `v0a/clock.py` (`32cdc99e`), `action_clock.py` (`844643c5`), `execution.py` (`c46cd0e8`), `preparation_bank.py` (`75c381fb`); reviewer 02 named `game.py`, `cfr.py`, the prefix test, and the source-admission / execution-status writer paths. | Accepted. The implementation round's coverage record calls the inventory *direct* and extends the pins to these when the corresponding boundaries are exercised. |
| Read `hands[*].result`, not the ordinal/button wrapper, for session outcome fields; the design's "hand entry" denotes that nested result. | Accepted as an implementation constraint. |
| Keep agreement-only river-record diagnostics separate from chip eligibility; the exactly-one-river-record predicate governs Slice A agreement, not chip inclusion. | Accepted; already the design's intent, now stated as a test obligation. |
| `deal_for_hand` supplies hand indices 0–15 per seed; the preregistration must record enough seed/index pairs for the planned floor plus collision rejection, and record each draw even when an unordered pair repeats. | Accepted as a preregistration constraint. |
| Label planned-sample missing-unit bounds separately from population confidence intervals; completion-based restoration must re-run the *original* sampled units under the original plan, never substitute new successful deals. | Accepted; the re-run rule is valid only because the chip outcome is a deterministic function of cards and policy, and the preregistration states that explicitly. |

## Round history

r001 NOT CLEAN (host oracle labels, both-in-`H` filter, quadratic sealed
game, estimand undefined); r002 NOT CLEAN (delivery envelope, survivor
missingness); r003 CLEAN. The controller authorized the third round
explicitly. Six controller rulings of 2026-09-08 stand; two wording refinements
are recorded in the r001 disposition; T2 determinization remains open by
ruling 4 and must be declared in the preregistration before any T2 export.

## Next course, as recommended to the controller

1. Ceremonial commit of the two accepted documents on `codex/v0a-eval-panel`
   (the worktree holds them untracked), then integration to `master` — both
   need the controller's explicit authorization.
2. Per the checkpoint-alternation rule, Codex drafts the next checkpoint:
   the `v0a-eval-panel-impl` brief for Slice A, opening with the two
   measurements the accepted design gates on — the wire-byte capacity probe
   (mechanism 4) and the T1 per-hand cost preflight (mechanism 2). Either can
   fire a kill criterion before any solving; both are cheap and answer more
   than further prose would. Claude reviews.
