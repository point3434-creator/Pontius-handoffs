# Coverage claim: v0a-eval-panel-code/r003 (FIX round)

Deferred input. Reviewers: do not open this until your initial invariant and
related-path inventory are recorded, per the cold-review request.

## Category and method

Every path from an admitted plan to the single retained run record, plus every
failure and interruption that can occur on it. Members were enumerated by
following the data — plan bytes → parse → validate → worker launch → request
transport → phase work → stage events → parent assembly → cleanup → boundary
retention → result and journal writers — through the candidate and the frozen
base surfaces it calls, and by re-deriving each r001 finding's scenario against
the corrected code. Finding IDs are cross-references, not the organizing axis.

## Path, stage by stage

| Stage | Governing surface | Assertion in r002 | Falsifying observation |
|---|---|---|---|
| Plan bytes | `parse_plan` | 1..262,144 bytes; `parse_constant` refuses NaN/Infinity tokens; a recursive finiteness walk refuses `1e999` → `inf` anywhere | An admitted plan containing a nonfinite float or a constant token; a plan over the bound reaching the worker |
| Plan schema | `validate_plan` (schema v2) | Closed key set per phase; `runtime.python` equals the executing interpreter; `stacks == 4`; `prefix` equals `prefix_document()`; `hand_count`/`hand_universe_sha256` equal the replayed universe; `permutation` equals the seeded strength-blind order exactly; `resource.seconds` finite positive non-bool; `memory_mib` exact int in `1..2²⁰`; preflight `coverage ∈ {declared-full, test-subset}`, `declared-full` needs ≥4 development hands and ≥1 control; seed/index bank fields refused (phase-specific reading stated in the module docstring) | Any unknown or missing member accepted; a reordered, duplicated or truncated permutation accepted; a bool or `inf` seconds accepted; a subset passing as `declared-full` |
| Declared root | `require_declared_root`, `bet_action` | River, seat 2 to act, live seats (1, 2), pot 4, live stacks 2, starting stacks all 4, legal `(CHECK, RAISE)` with bounds exactly `[2, 2]`; the bet is the constant `raise_to(2)` | `s = 3` (`raise_to(1)`) or `s = 6` reaching `hand_totals`, `build_reference` or the tool |
| Capacity | `capacity_probe`, `retain_boundaries` | Binary search on wire bytes; boundary encodings returned as bytes, shipped base64, written into the run directory as `capacity-boundary-<k>.blueprint.json`, bound by path/length/digest | A digest retained without its bytes; a size measured on canonical bytes |
| Production | `hand_totals` | Two kernel-settled lines, integer totals, CHECK on tie, work counts | A private payoff formula; a second hero hand's game |
| Reference | `build_reference`, `forced_value`, `reference_best_response` | 990 raw-1.0 deals; one hero root `(CHECK, raise_to(2))`; CALL at every villain key; forced lines end at integer terminals ≤ 4 with no chance node; explicit villain policy; separate forced and best-response calls | Default uniform villain; a non-integer or oversize terminal; a changed domain inheriting the bound |
| Lattice rule | `lattice_integer`, `validate_reference` | Exact dyadic rationals; unique `J`; `J == production`; production maximizes; response within bound; map is exactly the hero key; non-tie exact action equality; tie → production CHECK, either label recorded | Any of the arithmetic fixtures in `test_eval_bridge.py` passing when it should fail, or vice versa |
| Request transport | `supervise.send` thread | Initial request written on a daemon thread; the watchdog loop starts regardless | The supervisor blocked in `stdin.write` past the deadline |
| Ownership | `supervise` | `assigned` tracked; unassigned suspended process killed; every cleanup step guarded; pipes closed; `job.close()` in nested `finally`; `cleanup_verified` false on any leftover | A live process after a failed `assign`; an exception in cleanup skipping `job.close()`; an unclosed pipe |
| Stage events | `preflight_hand`, `supervise.drain` | One event per completed stage with cache before/after and cost; parent assembles hands; `missing_stages` labeled; incomplete hands fail the phase | A kill after production losing the production measurement |
| Nonfinite output | `json_safe` | Nonfinite floats become `{"nonfinite": repr}` before any writer | `finish_run` raising `allow_nan` |
| Run record | `main` | `begin_run` once; all work in `try`; `KeyboardInterrupt` and `Exception` both recorded; `finish_run` in `finally` with `output_directory` set when the directory exists | Two journal rows, or zero after admission |

## Findings cross-reference

r001 A (R01 I-01 / R02 I-01) → Ownership, Run record. B (R01 I-02 / R02 I-02)
→ Plan bytes, Plan schema, Nonfinite output. C (R01 I-03) → Request transport.
D (R01 I-04 / R02 I-04) → Plan schema. E (R01 I-05 / R02 I-03) → Declared root.
F (R01 I-06) → Capacity. G (R02 I-05) → Stage events. H (R01 I-07) → the
exercised cases below.

## Exercised cases (executed, receipts in `checks/`)

Bridge suite (11): declared root and prefix document; `s = 3` and `s = 6`
refused by `require_declared_root`, `bet_action`, `hand_totals`,
`build_reference`; universes and keys; placeholder conservativeness and
monotonicity; boundary bytes returned and decodable, all-fit and one-row cases;
royal tie totals with work counts; development identity `J_bet = 2·J_check`;
the sealed singleton reference on the royal tie **and on `As Ad`** (nonzero,
`agree`, validated totals equal production); changed-domain refusal; signed
cancellation both signs and smallest lattice gap both signs **through
`validate_reference`**, false tie, changed total, wrong action, extra key, NaN.

Tool suite (11): parse refusals (size, `1e999`, `NaN`, `Infinity`); schema
refusals (22 wrong or missing members including reordered/duplicated/truncated
permutation, bool and zero seconds, fractional and oversize memory, bank field,
wrong runtime, `s = 3`, `s = 6`, wrong prefix, wrong universe digest, subset
posing as full); in-process capacity with boundary bytes; in-process preflight
emitting exactly the seven stages then `hand_completed`; exhausted budget;
`json_safe`; **the real supervisor** running a real capacity worker under the
`Job` to completion; **a real assignment refusal** through the real launcher
observing process death, retained `containment_failed`, and verified cleanup;
**a real budget kill** during reference work retaining the completed production
stage and labeling the missing ones; **`main` through the real `finish_run`**
in a disposable git repository for a completed run and for a `1e999` plan, each
yielding exactly one journal row, the latter starting no worker.

## Limits

No retained measurement; the development diagnostic in r001 is not repeated.
No export or agreement code. The pipe-fill stall (finding C) is corrected by
construction and not reproduced by a test. Whole-slice budget projected
1,000–1,100 production lines pending the controller's number.

## r002 withdrawal

r002 (`e398f833`) froze the same production code; its focused receipt failed only
because the `OwnershipTests` fixture invoked `git` by bare name under the scrubbed
environment. r003 corrects the fixture and nothing else; see
`inputs/r002-withdrawal.md`.
