# Addendum to cold review 01 — Claude — v0a-eval-panel-impl/r001

Issued 2026-09-08, after the second cold review was delivered. This is a new
record supplementing `review-01-claude.md`; it does not alter that report's
verdict or findings. It sharpens the derivation of I-01 because the second
review reached CLEAN on the same passage, and the finalizer's disposition
should have the strongest form of the argument in front of it.

Binding: candidate `e39d3b93695bfc601d051e8e71f334eef4d10d19`, manifest
`4f16c97f50734f06cc6bcd5286a87d355aaf4f8589f8796de1e33a8c5b47c405`.

## The residual is not random between the two actions — it is exactly doubled

`evaluation.py:257-263` computes, for the hero's single information set,

    action_values[a] = sum(reach * continuation_value(state.apply_action(a))
                           for state, reach in entry.states)

over the **same** `entry.states` list, in the **same** order, for both actions.
With `p = fl(1/990)` as each state's reach (`river.py:203-229`), the CHECK
terms are `fl(p·c_i)` with `c_i ∈ {+2, 0, −2}` and the bet terms are
`fl(p·b_i)` with `b_i = 2·c_i ∈ {+4, 0, −4}` — the bet term is the CHECK term
scaled by 2 (the villain's CALL has probability exactly `1.0` and FOLD exactly
`0.0`, so the bet branch contributes `1.0 × (±4)` exactly). Multiplication by a
power of two is exact in binary floating point, and it commutes exactly with
every rounding in the accumulation, whatever the summation algorithm. Hence

    S_bet = 2 · S_check     exactly, on every interpreter.

On an exact production tie (`w = l`), the true value of both sums is zero.
`max(entry.actions, key=action_values.__getitem__)` returns CHECK only if
`S_check ≥ S_bet`, i.e. only if the computed residual `S_check ≤ 0`. If the
residual is positive, the reference selects `raise_to(2)`, production selects
CHECK, and the candidate's "compare its selected action exactly" fails
criterion 2. The outcome is decided by the sign of a rounding residual.

## The residual is interpreter-dependent

CPython 3.12 changed the built-in `sum()` to Neumaier compensated summation
for floats (gh-100425, "What's New in Python 3.12"). The project mandates
Python 3.11.15 before 3.14.6. On 3.11 the accumulation is naive left-to-right
and partial sums such as `fl(3·2p)` round; on 3.14 the compensation usually,
but not provably always, returns exactly `0.0` for a cancelling sequence. The
same hero hand can therefore pass the reference on 3.14 and fail it on 3.11.
An acceptance predicate whose result depends on the interpreter's summation
algorithm is a specification defect independent of how often a tie hand occurs.

## Why the second review's reading does not close this

The second review endorses "an action disagreement remains a stop, not a tie
invented with epsilon." I agree with that sentence as written: a genuine
disagreement must stop, and no epsilon may manufacture a tie. I-01 is the
converse case, which that sentence does not address — a genuine tie that the
reference misreports as a disagreement. The candidate's own text contemplates
ties ("CHECK first on exact equality"; the royal-spade `2c 3d` control) but
supplies no rule for comparing an exact integer tie against a float reference.
The royal-spade control cannot expose it because every term there is exactly
`0.0`; only a non-degenerate tie (`w = l > 0`) can.

## Smallest correction, restated

When production totals are exactly equal, the reference passes if
`|S_check − S_bet| ≤ allowance` — equivalently, since `S_bet = 2·S_check`,
`|S_check| ≤ allowance` — regardless of which
action it selected, and the case is recorded as a tie. Otherwise require exact
action equality and value agreement within the allowance. The allowance is
derivable from the reference's own accumulation of 990 terms of magnitude
`≤ 4/990`. No sealed module changes.

## Limits

This is arithmetic on frozen source, not an executed test. I have not
enumerated whether a `w = l > 0` hand exists on `2c 7d 9h Js Qc`; the defect
is in the predicate, and the candidate's reference sample is meant to extend
to "a declared sample" of `H`. No other part of my review changes.
