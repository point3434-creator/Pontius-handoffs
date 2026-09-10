# Inventory 02 (claude): v0a-eval-panel-completion/r003, written before deferred inputs

Candidate 7ca821802c949b047becf6599d603b3b63d51fa7, parent
430ad75de79cec13d66ff3dc4981dd3770a371b7, manifest
1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd. Built from handoff.md,
brief.md, inputs/ and raw frozen blobs only. coverage.md and checks/ were not opened.

## 1. Governing requirements this round must satisfy

- R1 Host-equivalence of raw admission (brief r003): any capture the frozen host would
  refuse on physical framing or JSON (read_stream, decode_json) is excluded before any
  chip or agreement credit. Oracle: tools/v0a_table_host.py at the candidate.
- R2 Preserved outcomes (brief r003): valid v1 CHECK hits, off-pool defaults, reason-only
  disagreements and completed v2 baseline divergence keep their prior classification and
  settled chips.
- R3 Finite-number restriction remains (classifier stricter than host on floats).
- R4 Tier C invariant (accepted brief, completion brief): no hit from missingness,
  defaults or failures; every hit attributable to a completed real host decision, the
  declared teacher and the exact exported key.
- R5 Design section 5: outcome eligibility precedes agreement; the two are separate
  values; nested hands[*].result is read, not the wrapper; malformed base64/frames,
  missing closure, incomplete hand_result, failed event_result are unusable; exactly one
  controlled river record; replayed key/reason cross-check; unknown reasons are explicit
  disagreements; completed prefix-diverged baseline stays chip-eligible.
- R6 Scope: only src/pontius/eval_agreement.py and tests/test_eval_protocol.py change;
  host/session/codec/solver unchanged; 3000 production-line ceiling, 1200/600 working.
- R7 Hygiene: LF-only, BOM-free, <=100 columns, no trailing whitespace; exact-type
  discipline (type(x) is int / is bool) on evidence paths.

## 2. Producer chain of the retained capture (frozen at the candidate)

1. tools/v0a_event_adapter.py PipeOutput.frame writes one frame per line:
   json.dumps(sort_keys, compact, allow_nan=False) + '\n', UTF-8, to the child stdout.
   Frame kinds: ready, action, event_result, hand_result, session_result.
2. tools/v0a_table_host.py ChildConnection.read_stream (lines 512-537): stdout cap
   2,097,152 bytes; a chunk exceeding the cap sets truncated and transport_failed; frames
   split at byte 10 only; each frame (including LF) must be <= 16384 bytes; a pending
   partial of >= 16384 bytes is protocol_invalid; at EOF pending must be empty, then a
   None sentinel is queued. stderr cap 65536 with the same truncated flag.
3. WireConsumer.read (662-680): raw is bytes ending in LF; decode_json(raw,
   digits=640, floats=True): 0 < len <= 16384, no CR byte anywhere, no UTF-8 BOM prefix,
   byte-level bracket depth <= 8 outside quoted strings, strict UTF-8 decode, json.loads
   with parse_int digit cap 640 (after lstrip('-')), parse_float=float (so 1e9999 is
   accepted as inf by the host), parse_constant rejected, duplicate keys rejected; any
   ValueError/TypeError/RecursionError is a refusal. Then type is dict, type is str and in
   WIRE_FIELDS, exact field set (v2 ready adds provider, config_sha256), protocol and
   session_id equal the host's child identity.
4. Lockstep order: ready; per event [action if hero acts] + event_result; hand_result;
   session_result; then the None sentinel (EOF). Anything else is a refusal.
5. Field rules per frame: action (integer action_index>=1, seat 0..5, hand_id, index ==
   bot_index+1, seat == controlled, street == table street, HandAction); event_result
   (event_index == table index, status in accepted/decided/failed, failed -> child_failed,
   decision iff decided); v1 decision (exact 16 fields, HandAction, TimingRecord with
   FailureCode conversion, preparation exact absence, DecisionRecord construction which
   requires SelectionReason and SPINE_REASONS membership and 64-hex digests,
   failure_reason None, COMPLETED timing, equality with expected hand_id/event_index/
   action_index/street_action_index/seat/street/state_before/visible/blueprint/
   selected_action/state_after -> otherwise state_mismatch); v2 decision
   (validate_decision, legal fallback and selected action on the live state, expected
   provider fields, state_after, timing, delivery accepted); hand_result (closure_fields,
   complete bool, settlement equal to Table.settlement(), rank_source matches showdown,
   no failures); session_result (completed, scope, finite duration, no failures).
6. Host main/session play_hand retain: child_exit_code, child_stdout_base64 =
   b64encode(connection.stdout), child_stderr_base64, capture_truncated =
   connection.truncated, applied_actions (Table.applied_actions), settlement (only when
   provisional and no failures), status 'completed' only then.
7. tools/v0a_table_session.py wraps: hands[i] = {ordinal, button, starting_stacks,
   result}; result.version 'pontius-v0a-table-session-hand-result-v1|v2';
   result.session_id 'pontius-v0a-table-host-<ver>-correctness-<suffix>-hNN'; outer report
   version 'pontius-v0a-table-session-result-v1|v2', status completed only if all hands
   completed. Session.run() returns the Python dict; the completion tool classifies that
   dict in-process (tools/v0a_eval_panel_completion.py play, line 305-309), so the outer
   report is never re-parsed from JSON by the classifier path.

## 3. Consumer: src/pontius/eval_agreement.py classify (frozen, 411 lines)

Order: clean(session) -> completed/stop_reason None -> requested==completed==1, one hand
-> ordinal 1 -> clean(outcome) -> status completed -> capture_truncated is False and
child_exit_code exact 0 -> frames_for -> replay -> event count -> rank_source. Any
ValueError/TypeError/KeyError/IndexError/binascii.Error -> excluded, chip_eligible False,
chips None, causes [str(error)]. Then chip_eligible True, chips = kernel net_returns[2],
classification 'unsupported', observed_table_hits, river_records; strategy other than
'blueprint-v1' -> unsupported with cause; else agreement loop.

### 3.1 Nested schema the classifier requires (member: type and value)

Outer session report (dict):
- version: str == 'pontius-v0a-table-session-result-' + ver, ver from ready.protocol[-2:]
- session_id: str, startswith 'pontius-v0a-table-session-<ver>-correctness-'
- status: == 'completed'; stop_reason: is None
- failure_reason: is None; secondary_failures: type list and == []
- requested_hands, completed_hands: type int (not bool) and == 1
- hands: type list, len 1
- source_commit, blueprint_artifact_sha256, blueprint_sha256: == ready == hand result
- v2 only: provider == 'baseline-rules-v1' (via ready), config_sha256 64 lowercase hex,
  equal across ready/hand/report
- not read: input_sha256, next_button, carried_stacks, child_stderr_base64

hands[0] entry (dict): ordinal int == 1; button int == 0; starting_stacks list len 6 of
int == stacks (default 4); result dict.

hands[0].result (dict):
- version == 'pontius-v0a-table-session-hand-result-<ver>'
- session_id == 'pontius-v0a-table-host-<ver>-correctness-' + outer suffix + '-h01'
- status == 'completed'; failure_reason is None; secondary_failures list == []
- capture_truncated is False; child_exit_code type int == 0
- child_stdout_base64: str/bytes, strict base64 -> raw bytes, 0 < len <= 2,097,152,
  endswith b'\n'
- settlement: not None; json.dumps(sort_keys) equal to hand_result.settlement and to the
  kernel settlement dict(payouts=list6, final_stacks=list6, pots=[{amount, seats}])
- applied_actions: type list; each row dict with exactly {index, seat, street, action,
  origin}; index int == position; seat int == kernel acting seat; street == kernel
  street value; origin 'bot' iff seat == 2; action dict exactly {kind, raise_to} that
  HandAction accepts and the kernel applies; replay must reach a terminal state
- source_commit, blueprint_artifact_sha256, blueprint_sha256 (and v2 provider,
  config_sha256): equal to ready and outer report

Capture bytes -> frames (each frame = line + b'\n'): type bytes; 0 < len <= 16384;
no byte 13; no EF BB BF prefix; bracket depth <= 8 outside strings; strict UTF-8; one
JSON value; object keys unique; integer tokens <= 640 digits; floats finite (stricter
than host); NaN/Infinity/-Infinity rejected; RecursionError -> wire:json_recursion.

Frame list: len >= 3, every row type dict; frames[0].type == 'ready';
frames[-2].type == 'hand_result'; frames[-1].type == 'session_result'; every row has
exactly {protocol, session_id, type} + WIRE_FIELDS[type] (+ provider, config_sha256 on a
v2 ready); every row.protocol == ready.protocol which is one of the two interface names;
every row.session_id == ready.session_id, a nonempty str equal to
protocol + '-correctness-table-' + suffix.

ready: source_commit 40 hex; source_manifest_sha256 64 hex (shape only; manifest is
not retained by the session, comparison belongs to admission); blueprint_artifact_sha256
64 hex; blueprint_sha256 == PreparedBlueprint(blueprint).digest; evidentiary is False.

Middle rows frames[1:-2], in order:
- action: hand_id, action_index (int >= 1), seat (int 0..5), street, action
  ({kind, raise_to} HandAction-valid); must be followed by a decided event_result whose
  decision has equal hand_id/action_index/seat/street and selected_action == action; two
  actions in a row -> wire:duplicate_action; trailing unpaired action -> refused
- event_result: event_index int == running count; status in ('accepted', 'decided');
  failure is None; decision None iff accepted; decision present iff an action preceded
- total event_result count == replayed final event index + 1 (showdown event included)

decision v1 (exact DecisionRecord field set, 16 members): hand_id ascii nonempty ==
ready.session_id; event_index int == row.event_index; action_index int >= 1;
street_action_index int >= 1; seat int 0..5; street in STREET_NAMES; state_before_sha256,
state_after_sha256, visible_cards_sha256, blueprint_sha256 64 lowercase hex;
selected_action {kind, raise_to}; selection_reason any str (unknown labels admitted, become
disagreements); spine_reason in SPINE_REASONS; timing (below); preparation_use exactly
{producer_status == 'producer_absent', artifact_sha256s type list == [], credited_seconds
int == 0}; failure_reason is None. Agreement-stage equalities (not exclusions): event_index,
action_index == position+1, street_action_index, seat == 2, street, state hashes and
visible hash from the kernel replay; blueprint_sha256 == prepared.digest; selection_reason
== 'table_hit' iff replayed lookup hit; selected_action == replayed applied action ==
lookup action; pre-river reason must be passive_default.

decision v2: validate_decision (provider codec, full schema and internal consistency);
provider, config_sha256, source_manifest_sha256 == ready's; fallback_blueprint_sha256 ==
ready.blueprint_sha256; delivery_status 'accepted'; delivered == applied == selected;
timing as below; failure_reason None. No replayed-field cross-check (baseline is outside
the declared root: unsupported with cause).

timing (exact TimingRecord field set): status 'completed' (interruption_reason None);
wall_start_ns, last_valid_observation_ns, emission_observed_ns exact int >= 0 with lvo ==
emission; elapsed_ns exact int == emission - wall_start and <= 15,000,000,000;
response_compute_seconds, response_uninstrumented_seconds float, finite, >= 0, sum within
2e-9 of elapsed_ns/1e9; work_cutoff_crossed, deadline_crossed exact bool False.

hand_result: complete is True; settlement JSON-equal to result.settlement; rank_source ==
'host_supplied' if replay reached showdown else 'not_required'; evidentiary is False;
preparation_compute_seconds, post_terminal_compute_seconds float finite >= 0;
interrupted_response_count int == 0; accounting_complete is True; failure_reason None;
secondary_failures list == [].

session_result: status 'completed'; terminal_publication_compute_seconds float finite
>= 0; accounting_complete is True; failure_reason None; secondary_failures list == [];
accounting_scope == 'runtime_begin_to_final_publication'; evidentiary is False.

Caller inputs (not retained data, validated outside the try): blueprint exact
ImmutableBlueprintActionSource; teacher_actions dict name -> BettingAction; board tuple in
ascending order; private_hands six distinct pairs disjoint from the board; stacks int;
strategy str.

### 3.2 Values reported and their readers

chip_eligible (bool), chips (int | None), agreement_eligible (bool), classification in
{hit, disagreement, unsupported, excluded}, causes (deduplicated list[str]), river_hand,
observed_table_hits (int | None), river_records (int | None).
- tools/v0a_eval_panel_completion.py play(): stores the dict as 'classification'.
- agreement(): every primary attempt must be 'hit'; off-pool control chip_eligible and
  'unsupported'; check-hit control 'hit'; changed-stack control chip_eligible and
  observed_table_hits == 0; summarize over primaries emitted as agreement_summary.
- complete(): re-checks all primaries 'hit' and the three controls before success.
- accounting(): summarize over primaries, missing outcomes and missing pool hands.
- summarize(): scheduled, observed, missing, completed (chip_eligible count),
  agreement_eligible count, hits, disagreements, unsupported, excluded, complete = no
  missing, no disagreement, no excluded ('unsupported' does not block; readers compensate
  by requiring every primary to be 'hit').
- tests/test_eval_agreement.py, tests/test_eval_protocol.py assert on these fields.

## 4. Successful-credit paths (what could manufacture a hit or chips)

- P1 'hit' requires: outcome gates all pass; strategy blueprint-v1; record count ==
  replayed hero decisions; no replayed-field mismatch; every selected action equals both
  the replayed applied action and the lookup action; blueprint digest and reason label
  agree with the replayed lookup; exactly one river record; river lookup key == declared
  root key; teacher entry exists; lookup was a table hit; selected == teacher; no cause.
- P2 chips require the outcome gates and a kernel replay whose settlement equals both
  retained settlements.
- P3 Semantic mismatches the host would refuse with state_mismatch or expects-action
  ordering (wrong action_index, seat, street_action_index, state hashes, missing or
  duplicate river record) are graded 'disagreement' with chips retained (design 5 assigns
  the replay cross-check to agreement). Unknown selection_reason is likewise a
  chip-eligible disagreement (brief r003 preserves reason-only disagreements).
- P4 strategy is only compared against 'blueprint-v1'; it is not bound to the
  capture's protocol version.

## 5. Byte-level admission comparison, classifier vs host (my own enumeration)

| Predicate | Host (read_stream/decode_json) | Classifier (frames_for/decode_frame) |
|---|---|---|
| capture empty | consumer read gets None -> refuse | 0 < len -> excluded |
| capture > 2 MiB | truncated + transport_failed | len <= 2097152 and truncated flag |
| trailing bytes without LF | pending at EOF -> protocol_invalid | endswith LF |
| separator | byte 10 only | split(b'\n') only (parent used splitlines) |
| frame > 16384 incl. LF | protocol_invalid | len(line + LF) <= 16384 |
| CR anywhere / CRLF | refuse | refuse |
| BOM prefix | refuse | refuse |
| depth > 8 | refuse (byte scan) | identical byte scan |
| invalid UTF-8 | refuse | strict decode -> ValueError |
| int > 640 digits | refuse | refuse |
| duplicate keys | refuse | refuse |
| NaN/Infinity constants | refuse | refuse |
| float overflow 1e9999 | accept (inf) | refuse (stricter, R3) |
| non-object frame | refuse | refuse (all rows dict) |
| two JSON values in a frame | refuse | refuse |
| frames after session_result | EOF required -> refuse | last must be session_result |
| >8 queued frames, timing | transport/host_limit | not observable from bytes |

## 6. Failure cases to check against coverage and receipts

Byte level: empty capture; capture of exactly 2,097,152 bytes (admitted by both);
capture of 2,097,153 bytes; frame of exactly 16384 (admitted) and 16385 bytes; each of
\r, \v, \f, \x1c, \x1d, \x1e, \x85, U+2028, U+2029 as a line separator; CRLF; BOM at
frame start; BOM inside a later frame; invalid UTF-8 byte; overlong/surrogate UTF-8;
depth 8 vs 9; 640 vs 641 digit integer, negative sign excluded from the count;
duplicate key at top level and nested; NaN/Infinity/-Infinity; 1e9999; blank frame
(b'\n'); whitespace-only frame; non-object top level; concatenated objects; extra
trailing frame after session_result; missing session_result; unpaired action.
Parsed level: every member above with a wrong type, bool where int, float where int,
missing member, extra member, unknown type label, non-str type, protocol/session_id
drift, event_index gap, decision with status accepted, failed event, interrupted timing,
elapsed > 15 s, non-finite seconds, settlement mismatch, rank_source mismatch, changed
stacks, v2 capture under blueprint-v1 strategy, v1 capture under baseline strategy.
Identity: swapped source_commit/artifact/blueprint digests, mismatched suffix chain.

## 7. Evidence limits recorded before deferred inputs

No project code was executed; every claim above is from reading frozen blobs. The
host's queue depth, deadlines and thread timing are not byte predicates and cannot be
reproduced from a capture. The session does not retain the source manifest hash, so
ready.source_manifest_sha256 can only be shape-checked by the classifier.
