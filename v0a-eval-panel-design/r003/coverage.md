# Coverage claim: v0a-eval-panel-design/r003 (FIX round)

Deferred input. Reviewers: do not open this until your initial invariant and
related-path inventory are recorded, per the cold-review request.

## Category and method

The r002 reviewers faulted r002's coverage for being organized by prior
finding ID, which made its discovery method textual-survivor checking rather
than the design's own category. This claim is therefore organized by **path**:
every stage from a frozen teacher to a recorded chip result, plus every
exclusion and every inferential step after it. Each stage names the frozen
surface that governs it, what the design now asserts there, and the
observation that would falsify the assertion. Finding IDs appear only as
cross-references. Discovery method: follow the data — deal bytes, session
document, child frames, host validation, retained hand result, pairing,
exclusion, inference — through the frozen base sources listed at the end,
reading each serializer and validator rather than each label.

## Path, stage by stage

| Stage | Governing frozen surface | Assertion in r003 | Falsifying observation |
|---|---|---|---|
| Teacher | `legal_river_continuation`, `evaluation.best_response`, `no_limit_betting._raise_bounds` | T1 per hero hand by exact enumeration over 990 villains; sealed singleton-hero game as ground truth; `s = 4` gives one all-in bet size and one hero node, derived statically; partition valid only for fixed villain | A hero information set at `s = 4` other than the root; a hand whose per-hand action differs from singleton `best_response`; any statement extending the partition to T2 |
| Export | codec, `immutable_blueprint` | Entries exactly at hero root keys for `h ∈ H`; wire-byte capacity measured with `check`/`null` placeholder before solving and rechecked after | Unsupported set ≠ complement of `H`; capacity measured on canonical bytes; placeholder shorter than a real row shape |
| Acquisition | `v0a_seeded_deals.deal_for_hand`, `holdem_cards.SixSeatHoldemDeal` | Private cards from the sealed dealer; board declared and ascending; rejection on private/board collision only; villain uniform over 990 after marginalizing folders | Any rejection keyed on `H` membership; board order differing between export and composition; a conditional-on-folders villain law |
| Composition | `table_host.TableInput`, `table_session.Schedule/play_hand` | One hand per session (button rotates and stacks carry within a session); button 0, controlled seat 2, `(s,)*6`, opponents `fold_to_bet`×4 / `passive` seat 1 | A multi-hand session; a prefix that does not reach the checked-to root on every deal |
| Child frames | `v0a/runtime` (`_publish`, `_from_failure`), `v0a/trace`, `v0a_event_adapter` | `event_result` with `status ∈ {accepted, decided, failed}`, independently nullable `decision` and `failure`; a rejected/ambiguous publication raises before any decision exists; `DecisionRecord` has no delivery field, `FailureRecord` does | A design predicate reading delivery status off a decision record; a schedule that assumes every failure carries a decision |
| Host validation | `table_host.WireConsumer.exchange/decision/failure/complete` | v1 mode: record fields validated against host state digests and the applied action; timing completed with no cutoff; no independent lookup; failed events and incomplete hands raise `child_failed` | A claim that the v1 host recomputes the lookup; a claim that `selection_reason` is host-verified |
| Retention | `table_session.play_hand`, `table_host.ChildConnection.read_stream` | Hand entry carries `status`, `failure_reason`, `settlement`, `applied_actions`, and `child_stdout_base64` with `capture_truncated` (2,097,152-byte cap); the frame stream is where the river `DecisionRecord` is read post-hoc | A river `selection_reason` read from anywhere the session does not retain; truncation not treated as exclusion |
| Classifier | design mechanism 5 | Failure precedence: hand entry → completed and settled → exactly one river record → hit / disagreement / unsupported; independent `action_for` cross-check of `selection_reason`; check-hand hit/default separated by reason | A hand classified by its decision before its outcome; a failed hand needing a decision record; a check-hand whose hit status is inferred from the applied action |
| Provider boundary | `decision_provider.providers.BlueprintProvider.propose` | Driven directly with constructed observations; proves provider behavior only | Runtime behavior inferred from provider-boundary results or vice versa |
| Settlement | `no_limit_betting.settle`, `table_host.settlement`, `legal_river_continuation.returns` | Hero net chips = final stack − starting stack = kernel `net_returns`; exact per-orientation value `m_P,B` from per-hand enumeration | Disagreement to the chip between enumeration, sealed evaluator, and host on a small pool |
| Pairing | design mechanism 7 | Matched unit = unordered pair on its board, both orientations, all policies; off-pool hero cell is a retained `passive_default` observation of the deployed policy | Any both-in-`H` requirement; a swap dropped for pool membership |
| Divergence | `decision_provider.providers.BaselineProvider` (premium preflop raises) | Prefix divergence is a **label**, retained in chip comparisons, excluded only from agreement | A diverged unit deleted from a chip comparison (card-dependent selection) |
| Exclusion | design mechanisms 7 and 9 | Cutoff/failure is the only exclusion; it removes the whole unit across policies and orientations | A partially excluded unit; an exclusion keyed on anything but the outcome classifier |
| Inference | design mechanism 9 | Equal-weight fixed strata over four declared boards; unit in `[−4s, 4s]`; Hoeffding floor on planned units with `α` split; zero exclusions → full-population claim; any exclusion → claim withheld, survivors reported as conditional, Manski bounds over planned denominator; normalization `2·m_P,B` and `2·(m_A,B − m_C,B)`; fixed `1/4` weights on empirical and exact quantities | A full-population claim on a board with exclusions; a floor met with survivors treated as restoring the claim; a survivor estimand adopted without a ruling; a factor of two between per-cell and per-unit quantities; a variance-based loosening of the floor |
| Recording | `pontius.execution.begin_run/finish_run` | One journal line per panel run; sessions are cells | A journal line per session |

## Findings cross-reference

r001: R01-01/R02-01 host oracle → stages Child frames, Host validation,
Retention, Classifier. R01-02/R02-02 population → Acquisition, Pairing.
R01-03 estimand → Inference. R01-04/R02-03 quadratic → Teacher. r002:
R002-R01-01/R02-01 delivery envelope → Child frames, Retention, Classifier.
R002-R01-02/R02-02 missingness → Divergence, Exclusion, Inference. Advisory
inventory omissions (`v0a/trace`, `legal_decision_spine_v2`) → the table below.

## Exercised derivations

All static, from frozen base blobs: `_provider = None` for `blueprint-v1`;
`DecisionRecord` field set versus `FailureRecord.delivery_status`; `_publish`
raising `_HandFailure` with `REJECTED`/`UNKNOWN` before record construction;
`_from_failure` returning `status='failed', decision=None`; `event_result`
payload with nullable members; the v1 `exchange` expected-dict (state digests,
`blueprint_sha256`, `selected_action`) and `provider_expected` being
provider-mode only; `read_stream` capture and truncation; `hand_result`
`complete`/`settlement` gating; `dict(self.game.deals)` at lines 195 and 241;
`_raise_bounds` giving `[2, 2]` at `s = 4`; `best_response` first-action ties;
`BaselineProvider` premium raises; the reviewers' correlated-cutoff schedule
as a counterexample to survivor inference.

## Limits

No implementation, run, measurement, or test exists. T2's determinization
remains open by ruling 4. The per-hand partition and its cost are argued and
preflight-gated, not executed. The classifier's frame parsing assumes the
retained stream is the child's complete stdout below the cap; the cap and the
flag are frozen host behavior, not new code. This is the lane's third design
round; the disposition asks the controller whether the brief's two-round
budget bounds specification rounds.

## Dependency inventory pinned at base `b378104c`

| Path | Git blob at base |
| --- | --- |
| `tests/cases.json` | `53497f56ab0ac4b05c4dba7ca21e022f5bf62813` |
| `src/pontius/legal_river_continuation.py` | `dc82aa748a195391143a09958e4e0dade827c45b` |
| `src/pontius/blueprint_artifact/codec.py` | `c8a21b91cc4d285ff6e82b1f1b187c4e178bb5ce` |
| `tools/v0a_seeded_deals.py` | `2963004e38c6e66f76ae9ce3bd474063eee870fe` |
| `src/pontius/immutable_blueprint.py` | `0defb13caad0e8e11ef78b8aa85a83667147ac09` |
| `src/pontius/no_limit_betting.py` | `c4adbb0212fbaf144bcb51b14923028f69ea0eea` |
| `src/pontius/holdem_cards.py` | `25c64168ae46c835efce95050ef52cc9ac3734a5` |
| `src/pontius/blueprint_preparation/lookup.py` | `8d70e3014a6d1af2fe53e7ddfb15bbe30f8b2cb1` |
| `src/pontius/v0a/runtime.py` | `57c028eb737e424eb9fc0534b9c238d3eee92569` |
| `src/pontius/v0a/model.py` | `3602989e3a3d5f36c9a0bd5d102797b8e349191d` |
| `src/pontius/v0a/trace.py` | `8440aa0274b642af3e03326813989ff5b3333766` |
| `src/pontius/legal_decision_spine_v2.py` | `824f4938788769be4165dcad04926bf9f2ec22e8` |
| `src/pontius/decision_provider/model.py` | `6cce376e73594a6836d146cd53022fdb250a04f5` |
| `src/pontius/decision_provider/providers.py` | `c456a6953d32d1d28c4bef587c736b8971a69df4` |
| `src/pontius/decision_provider/selection.py` | `7b1f1eac2b53cca87cdec5e8f8a4ea9f50b63ebb` |
| `src/pontius/decision_provider/codec.py` | `f5795bc1d7f723a569b76732cf195b2ef9d69eaf` |
| `src/pontius/evaluation.py` | `d5fb3b2a3c765febc9b8c5e630943133907434bc` |
| `src/pontius/river.py` | `308279dddb7cad74a7af153fed45e2c92265bd71` |
| `tools/v0a_event_adapter.py` | `3e36eb42450ae328282737aeb20798078ccf16e2` |
| `tools/v0a_table_host.py` | `a6b00ec3886065e7bd31b9f5936b702c92ec023e` |
| `tools/v0a_table_session.py` | `80b934b1c2d5782d0805fa5cae9d8270320107e6` |
