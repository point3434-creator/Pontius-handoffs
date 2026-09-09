# Second addendum to cold review 01 — Claude — v0a-eval-panel-impl/r001

Issued 2026-09-09 at the controller's request, to resolve the reviewer
disagreement on I-01 by measurement rather than ruling. New record; the
verdict of `review-01-claude.md` is unchanged.

Binding: candidate `e39d3b93695bfc601d051e8e71f334eef4d10d19`, manifest
`4f16c97f50734f06cc6bcd5286a87d355aaf4f8589f8796de1e33a8c5b47c405`.

## What was run, and what was not

A standalone script, `checks/i01-tie-residual.py`, with **no project imports**.
It models exactly the accumulation `evaluation.best_response` performs at the
hero's single information set — `sum(reach * value for state, reach in
entry.states)` with `reach = 1.0/990` as produced by
`river._normalized_joint_weights`, CHECK values `±2`/`0`, bet values `±4`/`0`
(the villain's CALL at probability exactly `1.0`), same state order for both
actions — over 2,000 seeded random orderings for four `(w, l)` splits with
`w = l`, i.e. exact production ties. It reports the sign of the CHECK residual
under an explicit naive loop and under the built-in `sum`, and checks
`S_bet == 2 * S_check` exactly. No Pontius module, host, solver, or test was
executed; this is a calculator run on the project's two mandated interpreters.

Receipts: `checks/i01-tie-residual-cpython-3.11.15.txt` and
`checks/i01-tie-residual-cpython-3.14.6.txt` (digests in the ledger line and
the commit message).

## Results

| Interpreter | Accumulation | `w = l = 495` residual `>0 / <0 / ==0` | `S_bet == 2·S_check` exactly |
|---|---|---|---|
| CPython 3.11.15 | explicit naive loop | 901 / 1,009 / 90 | 2,000 / 2,000 |
| CPython 3.11.15 | built-in `sum` | 901 / 1,009 / 90 | 2,000 / 2,000 |
| CPython 3.14.6 | explicit naive loop | 901 / 1,009 / 90 | 2,000 / 2,000 |
| CPython 3.14.6 | built-in `sum` | 0 / 0 / **2,000** | 2,000 / 2,000 |

The other three splits (`300/300`, `100/100`, `450/450`) show the same pattern;
positive residuals occur in 7–45% of orderings on 3.11 depending on how many
ties dilute the sequence, and never under 3.14's `sum`.

## What this establishes

1. `S_bet = 2 · S_check` **exactly**, in every one of 8,000 orderings on both
   interpreters and both accumulation methods — as derived in the first
   addendum. The reference therefore selects the bet on an exact production tie
   if and only if the CHECK residual is positive.
2. On CPython 3.11.15, which the project mandates first, that residual is
   positive in roughly **45%** of state orderings for a balanced tie hand. The
   candidate's "compare its selected action exactly" would then report a
   disagreement against a correct production CHECK, fail criterion 2, and fire
   criterion 3's stop.
3. On CPython 3.14.6 the built-in `sum` (Neumaier, since 3.12) returns exactly
   `0.0` for every tested ordering, so the same hand passes. The acceptance
   predicate as written is **interpreter-dependent** — the concrete form of the
   defect.

What it does not establish: whether a `w = l > 0` hero hand exists on the
development board `2c 7d 9h Js Qc`, or how the sealed evaluator orders
`entry.states` for a real game (the residual's sign depends on order; its
existence does not). Neither affects the finding, which is about the rule.

## Disposition requested

Accept I-01 as Important; correction as stated in the first addendum: on an
exact production tie, the reference passes if `|S_check| ≤ allowance`
regardless of its selected action, recorded as a tie; otherwise exact action
equality and value agreement within the allowance. One sentence in `design.md`
§3; no sealed change.
