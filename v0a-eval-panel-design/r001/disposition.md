# Disposition: v0a-eval-panel-design/r001

Finalizer: the round's drafter (Claude), per the checkpoint-alternation rule.
Date: 2026-09-08. Both cold reviews returned **NOT CLEAN / STRAINED**. Their
Important findings converge on the same three defects, independently derived
and cross-checked here against the frozen base blobs before acceptance.

Outcome: **r001 is not adopted.** Every finding below is accepted; corrections
are frozen as `v0a-eval-panel-design/r002` (FIX round). No ruling is reversed;
two are refined in wording, flagged for the controller.

## Findings

| Finding | Disposition | Correction in r002 |
|---|---|---|
| R01-01 / R02-01 — host oracle labels do not exist on the `blueprint-v1` path | **Accepted.** Verified: `v0a/runtime.py` sets `_provider = None` for `blueprint-v1` and emits the ordinary `DecisionRecord` with `SelectionReason.TABLE_HIT` / `PASSIVE_DEFAULT`; `blueprint_hit`/`blueprint_default` are provider proposal reasons the selected mode never produces. | Mechanism 5 and Goals 1–2 now name the v1 record fields (`selection_reason`, `selected_action`, `timing`, `failure_reason`, delivery status) as the host oracle, with an exhaustive mapping to hit / unsupported / disagreement / excluded. A separate direct check drives the `BlueprintProvider` public boundary against the frozen teacher; the design states plainly that the host does not instantiate that class. Cutoff exclusion uses the v1 timing/failure fields. |
| R01-02 / R02-02 — both-in-`H` hand swap contradicts the declared population and breaks calibration | **Accepted.** My own text required both hands in `H` while rejecting only collisions; for a proper subset `H` that is unsatisfiable without an undeclared filter, and the filter distorts hero weights by compatible-degree (reviewers' small-pool examples are correct). | One inclusion law: every valid original and its swap is played whatever the pool; an off-pool hero cell is a `passive_default` observation reported separately, never a rejection. The deployed policy is defined as table-on-`H` plus passive default off-`H`, and the calibration expectation is computed for **that** policy over the full accepted-deal population (hero uniform over 1,081, villain uniform over 990). Whole-unit exclusion is declared. No both-in-`H` filter exists. |
| R01-03 — estimand and interval mechanism undefined for four boards | **Accepted.** | Mechanism 9 rewritten: the target is the mean over the four declared boards with equal weights — fixed strata, conditional on those boards; per-board paired-unit intervals combined as strata; the loss budget in chips per paired unit with the confidence level, and a Hoeffding-style bound from the `2s` outcome range as the pre-registered floor; an explicit statement that more deals reduce within-board uncertainty only. |
| R01-04 / R02-03 — quadratic range validation in the sealed teacher game | **Accepted.** Verified at `legal_river_continuation.py:195,241`: `dict(self.game.deals)` is rebuilt per membership check, so a monolithic full-`H` game costs ≥ `2·N²` row insertions, `N = 1,070,190`. The "exact in seconds" claim is withdrawn. | Mechanism 2 rewritten: T1 and the calibration expectation are computed per hero hand by exact enumeration over that hand's 990 compatible villains using the kernel's settlement, in new caller code; the sealed game with `best_response` remains ground truth and is run on singleton-hero pools as an independent cross-check for a declared sample. The partition is valid because the villain policy is fixed, so hero information sets are independent at `s = 4`; the design says why this does **not** extend to T2. A cost preflight with a stop condition precedes any full-pool solve. |
| R01-05 — 106-column line in `brief.md` | **Accepted.** | Reflowed. |

## Advisory items

Adopted: `s = 6` has three hero decision histories, not "roughly four"; the
direction control is weak dominance with an exact expected gap declared and a
zero effect allowed (royal-flush board as the all-zero control); "no artifact
can cover randomly dealt boards" softened to the capacity argument; board order
declared ascending and applied identically in export and session composition;
capacity placeholder uses `check`/`null` rows (three wire bytes longer than
`raise`/`2`) with a final-artifact recheck; "regardless of what the folders
hold" restated as a marginalization claim; the coverage record names the full
dependency inventory (key constructor, kernel, card view, lookup, runtime,
provider model/codec/selection, event adapter, host, session, evaluator), with
their base blobs pinned in r002's `coverage.md`.

Not adopted: none. The reviewers' scoping caution — that a fixed-board,
card-blind-folder, one-size instrument cannot discriminate bunching or
adaptive-menu improvements outside its target — is already the brief's
forbidden-claims list and is repeated in the design's limits.

## Ruling refinements flagged for the controller

- **Ruling 3.** "Boards are the sampling clusters" is kept as the accepted
  intent but stated in r002 as *fixed strata, conditional on the four declared
  boards*, because with four declared boards there is no board sampling frame
  and "cluster-robust" implies one. Substance unchanged: `k = 4`, per-board and
  pooled, conditional, few-board weakness stated.
- **Rulings 1–2.** The inclusion law above adds no filter beyond collision
  rejection; it removes one the design had implied. It is a clarification,
  not a new selection rule.

## What r002 is not

No implementation, run, ceremonial commit, or sealed-surface change. The
corrected specification returns for a second cold review at Tier C.
