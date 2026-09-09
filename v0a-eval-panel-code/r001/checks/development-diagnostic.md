# Development diagnostic — NOT EVIDENCE

Run by the drafter on 2026-09-09 in the working tree before the freeze, in
process, without a run plan, without a journal line, and without resource
containment. It exists so the reviewers and the controller can see the shape of
the numbers the authorized run would produce. It authorizes nothing and is not
a receipt for criteria 1–3, which require the tool's supervised, journaled run.

Interpreter: the repository's `.venv` (CPython 3.14.6, numpy 2.5.2).
Board: `2c 7d 9h Js Qc`; stacks 4; control board `Ts Js Qs Ks As`.

## Capacity (design §2)

| Field | Value |
|---|---|
| cap | 1,048,576 |
| hands_total | 1,081 |
| largest_fitting | **1,081** (all fit; no overflow point within the domain) |
| bytes_at_largest | 1,012,625 (≈ 936.7 bytes per row; 35,951 bytes of headroom, 3.4%) |
| placeholder | `check`/`null` rows, `source_id` `t1:` + 64 zeros |
| probe elapsed | 8.0 s (11 encodings, binary search over the nested prefix family) |
| permutation sha256 | `344e7eeb06d72b97…` (seed in `tests/fixtures/eval_panel/plan-capacity.json`) |

Consequence if reproduced under authorization: `H` is the entire universe on
this board, and the format-fit kill criterion does not fire.

## Per-hand preflight (design §3)

| hand | label | J_check | J_bet | action | production s | ref build s | forced s | best_response s | class |
|---|---|---:|---:|---|---:|---:|---:|---:|---|
| As Ad | development | 1,430 | 2,860 | raise-to 2 | 0.33 (cold) | 6.28 | 7.44 | 10.17 | agree |
| Kh Kd | development | 1,438 | 2,876 | raise-to 2 | 0.10 | 6.85 | 7.51 | 9.94 | agree |
| Td 8d | development | 1,914 | 3,828 | raise-to 2 | 0.06 | 6.59 | 7.61 | 10.30 | agree |
| 3c 4d | development | −1,962 | −3,924 | check | 0.07 | 6.57 | 7.34 | 10.21 | agree |
| 2c 3d | control (royal) | 0 | 0 | check | 0.35 | 6.84 | 7.64 | 10.13 | tie |

Root replay: 1.1 ms. `J_bet = 2·J_check` on every hand (the fixed-CALL
identity). The royal control is an exact `(0, 0)` tie; the reference selected
CHECK, so the classification is `tie` rather than
`tie_reference_broke_differently`.

Estimate, production only, labeled as such: 1,081 hands × 0.06–0.35 s ≈
**1.1–5.9 minutes**, mean 2.5 minutes. The first hand is cold (empty
seven-card rank cache); later hands share cached villain ranks. The sealed
reference costs ≈ 24 s per hand and is sample-only by design; it is not
extrapolated.

## Limits

Traced allocation peaks were 0–3.6 MB per hand; no platform (job) peak was
observed because the diagnostic ran in process. Cold/warm labeling here is by
position only; the authorized run records the ranker cache state before and
after each phase. Nothing here is a capacity, cost, agreement, or strength
result.
