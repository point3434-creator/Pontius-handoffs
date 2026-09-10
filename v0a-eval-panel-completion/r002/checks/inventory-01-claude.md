# Inventory 01 (Claude, review-01): v0a-eval-panel-completion/r002

Sealed before coverage.md or any checks/ file was opened. Built bottom-up from the
frozen candidate 430ad75de79cec13d66ff3dc4981dd3770a371b7 (manifest
6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5), read with
`git cat-file blob`, and from handoff.md, brief.md, candidate.json, manifest.sha256,
supporting-files.json and every inputs/ file.

## 1. Identity (verified from Git objects, reviewer arithmetic)

- ref refs/heads/review/v0a-eval-panel-completion/r002-verified -> 430ad75d; tree
  c531d0b93520cd69704aa14842cea32d5b31ca51; sole parent 449a2a3c (whose parent is
  beb84be5, the base named in completion-brief.md).
- diff-tree parent..candidate: M src/pontius/eval_agreement.py, M tests/cases.json,
  A tests/test_eval_protocol.py. Nothing else.
- Manifest recomputed over raw blob bytes, rows "<sha256>  <path>\n" sorted bytewise:
  byte-identical to manifest.sha256; SHA-256 of that file equals candidate.json
  manifest_sha256 and handoff.md.
- Parent manifest (inputs/parent-manifest.sha256, 8 rows) recomputed at 449a2a3c
  against beb84be5: byte-identical; file digest f58d6ed8... matches supporting-files.
- All 35 supporting-files digests match; all 51 dependencies.json pins match the
  blob at the stated commit and repository (D:/Pontius and D:/Pontius-handoffs).
  Every dependency pinned at 430ad75d other than the two modified paths is
  byte-identical to the parent blob (confirmed), so "all other source is exactly
  the rejected parent" holds for the pinned set.
- Observation: sibling refs review/v0a-eval-panel-completion/{r002, r002-red,
  r002-green-initial} exist and point at other commits; not opened.

## 2. Obligations in scope for this FIX round

From brief.md (r002 FIX), completion-brief.md mechanisms 7-8 and accepted design
section 5, restricted to the changed surface (classifier + its tests):

O1 Missing or malformed protocol cannot receive chip credit or hit credit:
   any absent member, wrong type, coerced value (bool for int, float for int,
   string for list), default-supplied field or failure marker on the retained
   path yields classification 'excluded', chip_eligible False, chips None.
O2 Raw schema admission precedes typed construction: no dataclass constructor
   may normalize (tuple('') == ()) or default (PreparationUseRecord defaults)
   a wire member before its exact presence/type/value is checked.
O3 Exact successful metadata: ready.evidentiary is False; interrupted_response_count
   is exact int 0; requested/completed hands, ordinal, button, action indices,
   seats and starting stacks are exact ints; decision timing completed with no
   cutoff/deadline; delivery accepted (v2).
O4 Well-formed v1 unknown or relabelled selection_reason strings remain
   chip-eligible disagreements, never defaults and never hits.
O5 A completed baseline (v2) hand that diverges from the prefix retains chips and
   is 'unsupported', never excluded by the exactly-one-river predicate.
O6 Compatibility: real-host CHECK hit is 'hit'; off-pool default is 'unsupported'
   with chips; changed-stack prefix yields zero observed table hits and no hit;
   retained failures (session or hand failed, transport failure) are 'excluded'.
O7 Both protocol versions: v1 DecisionRecord shape (16 members, no
   delivery_status) and v2 ProviderDecisionRecord shape (27 members) are each
   admitted exactly under their own protocol; identity of the v2 provider and
   config digest is bound across ready/hand/report/record.
O8 Tier C: a hit requires (a) completed, settled, untruncated capture; (b) exactly
   one controlled river decision; (c) independently replayed key equal to the
   declared s=4 root key; (d) replayed PreparedBlueprint lookup table_hit True;
   (e) retained selection_reason equal to the replayed reason; (f) selected action
   equal to applied action, to the replayed lookup action and to the frozen
   teacher action; (g) every retained decision's replayed state digests equal.
O9 Scope: only eval_agreement.py, test_eval_protocol.py, cases.json change; no
   solver/export arithmetic, host/session, codec, ownership or timing change.
O10 Whole Slice A production < 3000 lines (hard ceiling); working figures
   1200/600 disclosed; hygiene LF-only, BOM-free, <= 100 columns, no trailing
   whitespace on changed files.
O11 Tests are registered only through tests/cases.json; the new suite must
   exercise real Session captures (v1 and v2) as anchors, not only fixtures.

## 3. Producer / consumer paths

Producers of the bytes the classifier reads (all frozen, unchanged):
- tools/v0a_event_adapter.py PipeOutput.frame: child stdout frames
  ready / action / event_result / hand_result / session_result, each
  json.dumps(sort_keys, compact, allow_nan=False, ensure_ascii) + LF.
  decision payload: trace.decision_payload (v1) or provider_codec.decision_payload
  (v2, validated by validate_decision before emission).
- src/pontius/v0a/runtime.py _decision_record / _provider_record: v1 record with
  selection_reason from BlueprintSelection.table_hit; v2 record with provider labels.
- tools/v0a_table_host.py Table.apply: hand['applied_actions'] rows
  {index, seat, street, action{kind, raise_to}, origin}; WireConsumer validates
  every frame at capture time (exact_object per kind, DecisionRecord typed check
  for v1, validate_decision + state_mismatch for v2); ChildConnection captures
  stdout (cap 2 MiB, truncated flag), exit code.
- tools/v0a_table_session.py Session.play_hand/run: outer report
  (version result-v1/v2, session_id, status, stop_reason, failure_reason,
  secondary_failures, source_commit, input_sha256, blueprint_artifact_sha256,
  blueprint_sha256, requested_hands, completed_hands, next_button,
  carried_stacks, hands[{ordinal, button, starting_stacks, result}], v2: provider,
  config_sha256); nested hand result (version hand-result-v1/v2, session_id,
  status, failure_reason, secondary_failures, input_sha256, blueprint_*,
  source_commit, applied_actions, settlement, child_exit_code,
  child_stdout_base64, child_stderr_base64, capture_truncated, v2: provider,
  config_sha256). Only a hand with no failures becomes status 'completed' with a
  settlement; otherwise the entry keeps status 'failed' and causes.
Consumers of the classifier:
- tools/v0a_eval_panel_completion.py play(): classify(result, blueprint=
  decode_blueprint(wire), teacher_actions=actions, board, private_hands, stacks);
  strategy defaults to 'blueprint-v1' (Session strategy is blueprint-v1 there).
  agreement(): requires 'hit' for every primary; controls off-pool 'unsupported'
  + chip_eligible, check-hit 'hit', changed-stack chip_eligible + 0 observed hits.
  accounting()/complete(): summarize(primary classifications, len(names)).
- tests/test_eval_agreement.py (constructed fixtures), tests/test_eval_completion_tool.py
  (real host controls + relabel), tests/test_eval_protocol.py (new: real v1/v2
  captures + schema mutations).
- Harness: tests/test_pontius.py imports each cases.json name via importlib.

## 4. Nested schemas consumed by the classifier (required type and value)

Notation: exact = `type(x) is T`; == = equality against an already-validated value.

Caller inputs (outside the try; errors propagate to the caller):
- blueprint: ImmutableBlueprintActionSource (PreparedBlueprint refuses others).
- board: exact tuple, ascending; private_hands: six 2-tuples (SixSeatHoldemDeal).
- teacher_actions: mapping hand_name -> BettingAction; stacks: int (default 4);
  strategy: str (default 'blueprint-v1').

Outer session report (dict required by clean):
- failure_reason: is None. secondary_failures: exact list, == [].
- status: == 'completed'. stop_reason: is None.
- requested_hands, completed_hands: exact int == 1. hands: exact list, len 1.
- version: == 'pontius-v0a-table-session-result-' + v (v from ready.protocol).
- session_id: exact str, startswith 'pontius-v0a-table-session-<v>-correctness-'.
- source_commit, blueprint_artifact_sha256, blueprint_sha256: == ready's values.
- v2 only: provider, config_sha256: == ready's values.
- Not read: input_sha256, next_button, carried_stacks; extra members tolerated.

hands[0] entry (subscripted; non-dict fails by TypeError/KeyError):
- ordinal: exact int == 1. button: exact int == 0.
- starting_stacks: exact list, len 6, every element exact int == stacks.
- result: the nested hand (dict required by clean).

Nested hand result:
- failure_reason: is None. secondary_failures: exact list == [].
- status: == 'completed'. capture_truncated: is False.
- child_exit_code: exact int == 0.
- child_stdout_base64: base64 (validate=True), decodes to nonempty bytes ending LF,
  UTF-8, one JSON object per line (unique keys, finite floats, no constants).
- settlement: not None; json.dumps(sort_keys) equal to hand_result.settlement and
  to the kernel replay settlement {payouts[6], final_stacks[6], pots[{amount,
  seats}]} (json equality separates 0 / false / 0.0).
- applied_actions: exact list; each row exact members {index, seat, street,
  action, origin}; index exact int == position; seat exact int == acting seat;
  street == replayed street; origin == 'bot' iff seat 2; action exact members
  {kind, raise_to} admitted by HandAction (kind in fold/check/call/raise;
  raise_to exact int >= 1 iff raise, else None); kernel apply_action legal.
- version: == 'pontius-v0a-table-session-hand-result-<v>'; session_id: ==
  'pontius-v0a-table-host-<v>-correctness-<outer suffix>-h01'.
- source_commit, blueprint_artifact_sha256, blueprint_sha256 (== ready's);
  blueprint_sha256 == PreparedBlueprint(blueprint).digest; v2: provider,
  config_sha256 == ready's. Not read: input_sha256, child_stderr_base64.

Frames (every frame exact dict; >= 3 frames; frames[0] ready, frames[-2]
hand_result, frames[-1] session_result; every frame exact member set =
{protocol, session_id, type} + WIRE_FIELDS[type] (+ provider, config_sha256 on a
v2 ready); every frame protocol == ready.protocol and session_id == ready.session_id):
- ready: protocol in {v1, v2 interface names}; session_id exact nonempty str ==
  protocol + '-correctness-table-<suffix>-h01'; source_commit 40 lowercase hex;
  source_manifest_sha256 64 hex; blueprint_artifact_sha256 64 hex;
  blueprint_sha256 == prepared digest; evidentiary is False; v2: provider ==
  'baseline-rules-v1', config_sha256 64 hex.
- action (must be immediately followed by a decided event_result): hand_id ==
  record.hand_id (== identity); action_index exact int >= 1 == record's; seat exact
  int 0..5 == record's; street == record's; action exact {kind, raise_to}
  HandAction-valid and == record.selected_action.
- event_result: event_index exact int == running count; status in {'accepted',
  'decided'}; failure is None; decision is None iff status 'accepted' iff no
  pending action; count == replayed final event index + 1.
- decision v1 (protocol v1): exact 16 members = DecisionRecord fields:
  hand_id ascii nonempty == identity; event_index exact int >= 0 == row's;
  action_index exact >= 1; street_action_index exact >= 1; seat exact 0..5;
  street in names; state_before_sha256, state_after_sha256, visible_cards_sha256,
  blueprint_sha256 64 lowercase hex; selected_action exact HandAction shape;
  selection_reason exact str (any content; compared later); spine_reason in
  ActionSelectionReasonV2 values; timing (below); preparation_use exact 3
  members {producer_status == 'producer_absent', artifact_sha256s exact list ==
  [], credited_seconds exact int == 0}; failure_reason is None.
- decision v2 (protocol v2): validate_decision exact 27 members; schema_version
  'pontius-provider-decision-v1'; provider == ready.provider; config_sha256 ==
  ready's; source_manifest_sha256 == ready's; fallback_blueprint_sha256 ==
  ready.blueprint_sha256; delivery_status == 'accepted'; delivered_action ==
  applied_action == selected_action; failure_reason None; preparation absent;
  labels in fixed sets and mutually consistent; timing (below).
- timing (both): exact 10 members = TimingRecord fields; status ==
  'completed'; interruption_reason None; wall_start_ns, last_valid_observation_ns,
  emission_observed_ns, elapsed_ns exact ints with elapsed == emission - start,
  last == emission; response_compute_seconds, response_uninstrumented_seconds
  exact finite floats >= 0 summing to elapsed_ns/1e9 within 2e-9;
  work_cutoff_crossed, deadline_crossed exact bool False; elapsed_ns <= 15e9.
- hand_result: complete is True; settlement (see above); rank_source ==
  'host_supplied' iff replay reached showdown else 'not_required'; evidentiary
  is False; preparation_compute_seconds, post_terminal_compute_seconds exact
  finite float >= 0; interrupted_response_count exact int == 0;
  accounting_complete is True; failure_reason None; secondary_failures exact [].
- session_result: status == 'completed'; terminal_publication_compute_seconds
  exact finite float >= 0; accounting_complete is True; failure_reason None;
  secondary_failures exact []; accounting_scope ==
  'runtime_begin_to_final_publication'; evidentiary is False.

Agreement path (after chip eligibility; blueprint-v1 only):
- records (decisions in event order) count == replayed bot actions, else cause.
- per record vs replay: event_index, action_index, street_action_index, seat,
  street, state_before_sha256, state_after_sha256, visible_cards_sha256 all ==.
- selected == replayed applied action == PreparedBlueprint.action_for(...).action.
- record.blueprint_sha256 == prepared digest; record.selection_reason ==
  'table_hit' iff replayed table_hit else 'passive_default'.
- pre-river records: selection_reason must be 'passive_default'.
- exactly one river record; its replayed key == root_key(replay_root(), board,
  hero) (stacks 4 declared); teacher present and table_hit and selected ==
  teacher and no other cause -> 'hit'; teacher absent and default -> 'unsupported';
  teacher absent and table_hit -> disagreement; key differs and table_hit ->
  disagreement; any cause -> 'disagreement'.

## 5. Failure cases and expected disposition

E1 outer/nested status != completed, non-null failure_reason, non-empty or
   non-list secondary_failures, missing stop_reason/ordinal/result -> excluded.
E2 requested/completed hands or ordinal as True/1.0/'1' -> excluded (exact int).
E3 capture_truncated True/0/None, child_exit_code False/0.0/None -> excluded.
E4 child_stdout_base64 invalid base64, non-UTF-8, no trailing LF, < 3 frames,
   non-object frame, duplicate keys, NaN/Infinity/1e9999, unexpected frame type,
   wrong member set, missing terminal closure, hand_result.complete False,
   unaccounted or late failure, session_result failed -> excluded.
E5 ready.evidentiary True/None/'false'; identity shape (40/64 hex) wrong;
   ready/hand/report identity fields differ; child session id mismatch ->
   excluded.
E6 event_result failed/decision-status inconsistency/unpaired or duplicate
   action/event_index gap; action frame counters bool/float; action shape
   missing raise_to; action != record.selected_action -> excluded.
E7 v1 decision missing any of 16 members or preparation members; preparation
   '' or [x] or credited 0.0/False; selection_reason non-str; timing missing
   members, interrupted, cutoff/deadline flags, elapsed > 15e9, sum mismatch;
   digests malformed; spine_reason unknown -> excluded.
E8 v2 decision missing members; delivery not accepted; delivered != applied !=
   selected; provider/config/manifest not equal to ready; failure non-null ->
   excluded.
E9 applied_actions non-list, row missing/extra members, index/seat bool/float,
   out-of-turn action, illegal kernel action, non-terminal end, settlement
   mismatch (also payout False vs 0), starting_stacks True/4.0/len != 6 ->
   excluded.
E10 v1 selection_reason unknown string or relabelled either direction, pre-river
   non-passive reason, wrong teacher action, tampered state digest, wrong
   blueprint digest, zero/duplicate river decision, in-pool default -> chip
   eligible, 'disagreement' (never 'hit').
E11 changed stack prefix (stacks=6 on both sides) -> chip eligible, 'unsupported',
   observed_table_hits 0; off-pool default -> 'unsupported'; CHECK table hit ->
   'hit'; raise table hit -> 'hit'.
E12 baseline v2 completed hand (fold, all-in, or prefix-diverged raise) ->
   chip eligible, 'unsupported', agreement_eligible False.
E13 summarize: observed > scheduled or unknown classification -> ValueError;
   missing attempts keep complete False.

## 6. Invariants to verify on every path

I1 Every wire member that influences chips or agreement is exact-typed before
   any comparison; equality to a validated value is acceptable in place of a
   direct type check.
I2 No constructor with defaults or normalization sees raw wire input before its
   member set and values are checked (PreparationUseRecord, tuple(), HandAction,
   TimingRecord, DecisionRecord).
I3 The exception boundary of classify catches every exception class malformed
   input can raise inside the try (ValueError incl. JSONDecodeError/
   UnicodeDecodeError/Unusable/TraceInvalidError, TypeError, KeyError,
   IndexError, binascii.Error); anything else would crash rather than exclude.
I4 A 'hit' cannot arise from a default (reason relabel is caught both ways), from
   a missing record (count and river checks), from a failure (excluded first) or
   from a caller-supplied teacher without a table hit.
I5 chip_eligible is only set after settlement replay equality and complete
   closure; chips are the kernel's net return for seat 2.
I6 Protocol v1 and v2 branches are selected by ready.protocol and each admits
   only its own record shape; a v2 capture can never produce 'hit'.
I7 Line budget and hygiene from raw frozen bytes.

## 7. Limits noted before the deferred inputs

- The classifier cannot verify blueprint_artifact_sha256 or source identity
  against external truth; admission owns those (documented in source).
- Outer report/hand/entry envelopes are not exact-membership checked; every
  member read is validated, extra members are tolerated.
- The declared strategy argument is a caller input and is not cross-checked
  against ready.protocol.
- Frames are split with str.splitlines (broader than the host's LF framing) and
  json depth is unbounded (RecursionError not in the caught set); real completed
  captures are ASCII, LF-framed and depth-limited by the host.
