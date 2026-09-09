# Line budget and text hygiene — v0a-eval-panel-code/r001

Counted on the frozen blobs of candidate `b1fdacf157649ca92d1aee3e39b7b0471edbcd5d`.

## Budget (brief: 600 production and 400 test lines for the whole of Slice A)

| File | Raw lines | Non-blank |
|---|---:|---:|
| `src/pontius/eval_bridge.py` | 297 | 254 |
| `tools/v0a_eval_panel.py` | 278 | 248 |
| **production, this checkpoint** | **575** | **502** |
| `tests/test_eval_bridge.py` | 159 | 136 |
| `tests/test_eval_panel_tool.py` | 105 | 88 |
| **tests, this checkpoint** | **264** | **224** |

Excluded as data: `tests/cases.json` (+2 entries), two plan fixtures.

**Stated plainly for the controller:** this first checkpoint alone uses 575 of
the 600 production lines the brief allots to the entire slice. Bridge
completion (design steps 4–5: deterministic export, membership and provider
checks, the outcome/agreement classifier, and the tool's export/agreement
phases) cannot fit in the remaining 25. A realistic projection for the whole
slice is 750–800 production lines. The brief says an over-budget
implementation returns to the controller before freeze; this checkpoint is
within budget on its own, but the slice will not be, and the controller should
rule on the budget before step 4 rather than discover it at the second freeze.
Nothing was compressed below readability to hide this (working rule 8).

## Hygiene (checklist v1 item 10)

Over the seven frozen paths: 0 lines over 100 columns, 0 CR bytes, 0 trailing
whitespace, no BOM. `tests/cases.json` was rewritten by a Windows text-mode
write and normalized to LF before the freeze.

## Sealed surfaces

Unchanged, by construction of the freeze (only seven added or modified paths):
`legal_river_continuation.py`, `evaluation.py`, the codec, `immutable_blueprint.py`,
the kernel, the host, session, adapter, dealer, and `execution.py`. The tool
reads one private attribute of the unchanged ranker
(`river._evaluate_seven_cached.cache_info()`) to label cold and warm phases;
it writes nothing.
