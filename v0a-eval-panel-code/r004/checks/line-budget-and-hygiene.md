# Line budget and text hygiene — v0a-eval-panel-code/r004

Counted on the frozen blobs at `0bc19bca` (`git show`, raw lines and lines with
a non-whitespace character).

| File | Raw lines | Non-blank |
|---|---:|---:|
| `src/pontius/eval_bridge.py` | 333 | 283 |
| `tools/v0a_eval_panel.py` | 501 | 448 |
| **production, this checkpoint** | **834** | **731** |
| `tests/test_eval_bridge.py` | 198 | 171 |
| `tests/test_eval_panel_tool.py` | 358 | 310 |
| **tests, this checkpoint** | **556** | **481** |

Excluded as data: `tests/cases.json` and the two plan fixtures (unchanged
since r003).

**Against the budget.** The controller's ruling in
`inputs/controller-rulings-addendum-2.md` sets a hard ceiling of 3,000
production lines for the whole slice; the drafter's working figure is 1,200
production / 600 test. This checkpoint is 834 / 556 (+42 / +128 over r003):
identity admission and the declared sample (+26), independent cleanup attempts
(+9 net), staged boundary retention (+8), estimate membership (+7); tests add
five cases and extend two for the three accepted findings. Bridge completion
(design steps 4–7) is still to come; the whole-slice projection is now
**1,050–1,150 production lines**, inside the working figure and far from the
ceiling. The test side will exceed 600 at completion; that is flagged for the
controller now rather than at the next freeze.

## Hygiene (checklist v1 item 10)

Over the seven frozen paths: 0 lines over 100 columns, 0 CR bytes, 0 trailing
whitespace, no BOM. Both suites pass with `-W error::ResourceWarning`.
