# Disposition: v0a-eval-panel-design/r002

Finalizer: the round's drafter (Claude). Date: 2026-09-08. Both cold reviews
returned **NOT CLEAN / STRAINED** with two converging Important findings, both
residuals of the r001 categories: the host oracle was corrected at the label
level but not at the enclosing failure envelope, and the population was
corrected at acquisition but not at post-play selection. Both verified against
the frozen base blobs before acceptance.

Outcome: **r002 is not adopted.** Both findings and all advisory items are
accepted; corrections are frozen as `v0a-eval-panel-design/r003` (FIX round).
No ruling is reversed or refined further.

## Findings

| Finding | Disposition | Correction in r003 |
|---|---|---|
| R002-R01-01 / R02-01 — v1 `DecisionRecord` has no `delivery_status`; a rejected or ambiguous publication raises `_HandFailure` before any decision record exists, and the dispatch outcome is `status='failed', decision=None, failure=FailureRecord(...)`. Mechanism 5's record-only mapping cannot classify that cell, and a constructed record with a delivery field would contradict the frozen schema. | **Accepted.** Verified at `runtime.py:1233–1265` (`_publish` raises with `delivery_status` REJECTED/UNKNOWN and no decision), `runtime.py:1345–1365` (`_from_failure`), `v0a/model.py` (`DecisionRecord` fields vs `FailureRecord.delivery_status`), and the host's `event_result` / `hand_result` field sets. | Mechanism 5 becomes an **outcome classifier with failure precedence** over the real envelopes: the session hand entry (`status`, `failure_reason`), the host `hand_result` (`complete`, `settlement`, `interrupted_response_count`, `accounting_complete`, `failure_reason`), and the per-event `event_result` (`status ∈ {accepted, decided, failed}`, nullable `decision`, nullable `failure` with `code`, `delivery_status`, nullable `timing`). Only a completed, settled hand proceeds to river-decision classification by `selection_reason` and `selected_action`. Planned schedules use the frozen payload shapes: pre-publication failure with no decision, accepted delivery then timing failure, host/transport failure with no ordinary decision, and a successful v1 payload. |
| R002-R01-02 / R02-02 — whole-unit deletion targets `E[D \| all cells survived]`, not the declared `E[D]`; nothing makes survival independent of `D`, and `baseline-rules-v1`'s premium preflop raises make prefix divergence card-dependent by construction. | **Accepted.** The reviewers' schedule — a cutoff that fires exactly when the hero would bet — is admissible in the frozen runtime and is a valid counterexample to the inference rule. | Two changes. **Prefix divergence is no longer an exclusion** for chip comparisons: the hand completes, its settlement is the deployed policy's outcome, and deleting such units would filter the population by the cards. It remains a label, and excludes only from the Slice A agreement enumeration. **Cutoff/failure remains the only exclusion, with a stated inferential consequence:** a board with zero exclusions keeps its full-population claim; a board with any exclusion — and any pooled result containing it — has that claim **withheld and reported inconclusive**, with counts, survivors' statistics, and Manski worst-case bounds (each missing unit at `−4s` and `+4s`) over the planned denominator. Meeting the floor with survivors does not restore the claim; re-running the excluded units to completion does. No survivor-population estimand is adopted. |

## Advisory items

Adopted: `src/pontius/v0a/trace.py` and `src/pontius/legal_decision_spine_v2.py`
added to the dependency inventory with their base blobs — the trace omission is
exactly why the delivery-field error escaped the r002 "exhaustive" check; the
normalization is written as equations in mechanism 9 (unit total `2·m_P,B`,
unit difference `2·(m_A,B − m_C,B)`, fixed `1/4` board weights on both
empirical and exact quantities); the variance-based tightening clause is
removed — the Hoeffding floor on planned units stands alone, with the
per-board formula and `α` split written out.

Not adopted: none.

## Coverage-claim critique, accepted

Both reviewers noted that organizing `coverage.md` around prior finding IDs
made its discovery method textual-survivor checking, narrower than the design's
own category (every path from teacher to recorded outcome, plus every
exclusion). r003's `coverage.md` is reorganized by **path**, not by finding:
acquisition → composition → session → event → decision → settlement →
pairing → exclusion → inference, with a falsifier per stage, and the finding
IDs as cross-references only.

## What r003 is not

No implementation, run, ceremonial commit, or sealed-surface change. The
corrected specification returns for a third cold review at Tier C. This will
be the lane's third design round; the brief's budget of two review rounds per
slice was written for implementation slices, and the controller should say
whether it also bounds the specification rounds.
