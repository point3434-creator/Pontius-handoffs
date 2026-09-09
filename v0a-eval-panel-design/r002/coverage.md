# Coverage claim: v0a-eval-panel-design/r002 (FIX round)

Deferred input. Reviewers: do not open this until your initial invariant and
related-path inventory are recorded, per the cold-review request.

## Category

The r001 findings and advisory items, as recorded in
`../r001/disposition.md`, and the two frozen documents they bind to. This is a
specification fix; no implementation, run, or sealed-surface change exists.
The correction method was: verify each finding against the frozen base blobs
it cites, accept, rewrite the mechanism it binds to, and re-derive every
dependent statement (goals, tests, hazards, barriers, brief criteria).

## Members: finding → correction → how to falsify

| Finding | Where corrected | Falsifying observation |
|---|---|---|
| R01-01 / R02-01 host oracle | design Goals 1–2; mechanism 5; brief criteria 1–2 and Slice A | Any remaining statement that the `blueprint-v1` host emits `blueprint_hit`/`blueprint_default`, or any mapping of a v1 record shape that is neither hit, disagreement, unsupported, nor excluded. |
| R01-02 / R02-02 population | design mechanisms 7, 8; brief criterion 5; rulings refinement note | Any inclusion rule other than collision rejection; any requirement that both hands be in `H`; any expectation computed for T1-restricted-to-hits rather than the deployed policy over the full accepted population. |
| R01-03 estimand | design mechanism 9; brief criterion 6 | An undefined weight, interval, confidence level, or sample-size rule; any claim that more deals reduce uncertainty about boards outside the four; the word "cluster" used to mean a sampled unit. |
| R01-04 / R02-03 quadratic solve | design mechanism 2; capacity paragraph; barriers; brief ground truth | Any residual "exact in seconds" claim; any monolithic full-range `LegalHeadsUpRiverContinuation` as the production T1 or calibration path; a partition argument that does not state why villain-policy fixity makes hero information sets independent, or that extends the partition to T2. |
| R01-05 line length | brief ground-truth paragraph | Any changed-file line over 100 columns. |
| Advisory: `s = 6` node count | design knobs bullet | "roughly four" surviving anywhere. |
| Advisory: direction control | design mechanism 8 | A bare observed sign used as a gate; no declared exact expected gap; zero effect treated as failure. |
| Advisory: random-boards wording | design alternatives | "no artifact can cover" surviving. |
| Advisory: board order | design mechanism 7; Slice A tests | Export or composition left free to differ in board order. |
| Advisory: placeholder bytes | design capacity paragraph | Placeholder rows shorter than the longest real row shape. |
| Advisory: marginalization | design knobs bullet | "regardless of what the folders hold" without the marginalization qualifier. |
| Advisory: dependency inventory | design coverage section; base-blobs closing paragraph; this table below | A dependency the key identity or v1 oracle relies on that is absent from the inventory. |

## Exercised cases

The reviewers' concrete scenarios were re-derived, not merely accepted:
`_provider = None` at `runtime.py` for `blueprint-v1` and `DecisionRecord` with
`SelectionReason.TABLE_HIT`/`PASSIVE_DEFAULT`; `dict(self.game.deals)` at
`legal_river_continuation.py:195,241`; `_raise_bounds` giving `[2, 2]` at
`s = 4`; `best_response` tie handling by first legal-action order; the
106-column line; the unequal-degree small-pool weight example.

## Limits

T2's determinization rule remains open by controller ruling 4 and is not
addressed. No cost has been measured; the design now requires a preflight and
states the operation-count reason, nothing more. The per-hand partition is
argued, not executed. No test exists yet; the Slice A/B test lists are plans.
The design verdict for r002 is the reviewers' to give.

## Dependency inventory pinned at base `b378104c`

Files the key identity and the v1 oracle depend on, beyond the design's own
base-blobs table. The freeze's whole-tree diff is the identity guard; this
table is the semantic inventory the reviewers asked for.

| Path | Git blob at base |
| --- | --- |
| `src/pontius/immutable_blueprint.py` | `0defb13caad0e8e11ef78b8aa85a83667147ac09` |
| `src/pontius/no_limit_betting.py` | `c4adbb0212fbaf144bcb51b14923028f69ea0eea` |
| `src/pontius/holdem_cards.py` | `25c64168ae46c835efce95050ef52cc9ac3734a5` |
| `src/pontius/blueprint_preparation/lookup.py` | `8d70e3014a6d1af2fe53e7ddfb15bbe30f8b2cb1` |
| `src/pontius/v0a/runtime.py` | `57c028eb737e424eb9fc0534b9c238d3eee92569` |
| `src/pontius/v0a/model.py` | `3602989e3a3d5f36c9a0bd5d102797b8e349191d` |
| `src/pontius/decision_provider/model.py` | `6cce376e73594a6836d146cd53022fdb250a04f5` |
| `src/pontius/decision_provider/providers.py` | `c456a6953d32d1d28c4bef587c736b8971a69df4` |
| `src/pontius/decision_provider/selection.py` | `7b1f1eac2b53cca87cdec5e8f8a4ea9f50b63ebb` |
| `src/pontius/decision_provider/codec.py` | `f5795bc1d7f723a569b76732cf195b2ef9d69eaf` |
| `src/pontius/evaluation.py` | `d5fb3b2a3c765febc9b8c5e630943133907434bc` |
| `src/pontius/river.py` | `308279dddb7cad74a7af153fed45e2c92265bd71` |
| `tools/v0a_event_adapter.py` | `3e36eb42450ae328282737aeb20798078ccf16e2` |
| `tools/v0a_table_host.py` | `a6b00ec3886065e7bd31b9f5936b702c92ec023e` |
| `tools/v0a_table_session.py` | `80b934b1c2d5782d0805fa5cae9d8270320107e6` |
