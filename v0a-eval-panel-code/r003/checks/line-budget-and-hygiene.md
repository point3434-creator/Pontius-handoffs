# Line budget and text hygiene — v0a-eval-panel-code/r003

| File | Raw lines | Non-blank |
|---|---:|---:|
| `src/pontius/eval_bridge.py` | 333 | 283 |
| `tools/v0a_eval_panel.py` | 459 | 412 |
| **production, this checkpoint** | **792** | **695** |
| `tests/test_eval_bridge.py` | 198 | 171 |
| `tests/test_eval_panel_tool.py` | 230 | 193 |
| **tests, this checkpoint** | **428** | **364** |

Excluded as data: `tests/cases.json` (+2 entries) and two plan fixtures, which
now carry the full ordered 1,081-hand permutation (≈11.6 KB each).

**Against the budget.** The controller raised the slice budget on 2026-09-09
("we will raise the budget whats a few lines of code"); the drafter's reading
of 800 production / 500 test is recorded in
`inputs/controller-rulings-addendum.md` and is not yet confirmed. This
checkpoint alone is 792 / 428. The growth from r001 (575 / 264) is the accepted
r001 corrections: the supervisor rebuilt on the workload ownership pattern
(+~90), plan schema v2 with closed key sets and permutation binding (+~40),
per-stage emission and boundary retention (+~50), and real-launcher tests
(+~160). Bridge completion (design steps 4–7) is still to come; a realistic
whole-slice projection is now **1,000–1,100 production lines**. The controller
should set a number before step 4. Nothing was compressed below readability.

## Hygiene (checklist v1 item 10)

Over the seven frozen paths: 0 lines over 100 columns, 0 CR bytes, 0 trailing
whitespace, no BOM. Both suites also pass with `-W error::ResourceWarning`;
the r001 supervisor leaked the worker's three pipe handles and r002 closes them
and includes their closure in `cleanup_verified`.

## Sealed surfaces

Unchanged, by construction of the freeze. The tool still reads one private
attribute of the unchanged ranker (`river._evaluate_seven_cached.cache_info()`)
to label cache state; both r001 reviews judged that read-only use acceptable.

## r002 → r003

The only change from withdrawn r002 is the `OwnershipTests` fixture resolving Git
through `PONTIUS_GIT` or `shutil.which`, as `execution.git()` does, plus its two
imports. Both suites now pass under `env -i` with only `PONTIUS_GIT` set, `-B -P`,
and `-W error::ResourceWarning`, before the freeze.
