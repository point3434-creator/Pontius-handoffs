# Prosecutor inventory (sealed before deferred inputs): v0a-eval-panel-completion/r002

Candidate 430ad75de79cec13d66ff3dc4981dd3770a371b7, parent
449a2a3c1fa1f5a7f5f04adca32e499faaf81e13, manifest
6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5. Role: prosecutor.
All line numbers are raw frozen blob lines at the candidate unless a file is named.
EA = src/pontius/eval_agreement.py; HOST = tools/v0a_table_host.py; SESS =
tools/v0a_table_session.py; ADP = tools/v0a_event_adapter.py; MODEL =
src/pontius/v0a/model.py; PCODEC = src/pontius/decision_provider/codec.py; TRACE =
src/pontius/v0a/trace.py; RT = src/pontius/v0a/runtime.py; TOOL =
tools/v0a_eval_panel_completion.py.

## 1. Obligations (completion brief, accepted brief 5-7, design 5, r002 brief)

O1 Outcome eligibility precedes agreement eligibility; they are separate values.
O2 Missing/malformed protocol receives neither chip nor hit credit; nullable failures,
   malformed frames, truncation, missing settlement, incomplete closure are exclusions
   with causes.
O3 Raw schema admission happens before any typed constructor can normalize or default.
O4 Exactly one controlled river record on a successful blueprint hand; zero/duplicate
   never hit. Replayed key/state cross-checked; table_hit cross-checked against the v1
   reason; selected_action compared to the frozen teacher; in-pool default and wrong
   action are disagreements; off-pool default is unsupported.
O5 Well-formed v1 unknown/relabelled reasons remain chip-eligible disagreements; a
   completed prefix-diverged baseline hand remains chip-eligible (unsupported).
O6 Changed stack/prefix yields zero hits; CHECK hit differs from default by reason.
O7 Counters: scheduled, observed, missing, completed, agreement-eligible, hits,
   disagreements, unsupported, excluded; one disposition per attempt; missing visible.
O8 Only the three named paths changed; every other blob equals the parent.
O9 Slice A production stays below 3000 lines (hard ceiling).

## 2. Producer -> consumer paths

P1 Child frames: ADP PipeOutput.frame L188-192 (ready L226-231, action L199-201,
   event_result L243-247, hand_result L278-285, session_result L296-299); v1 decision
   payload TRACE.decision_payload L216-237 from RT._decision_record L1286-1306; v2
   decision payload PCODEC.decision_payload L23-41 from RT._provider_record L1172-1191.
P2 Host consumes frames HOST.WireConsumer.read L662-680 (decode_json L52-90: exact
   ints, floats allowed, no constants, unique keys, <=16384 bytes, no CR/BOM), validates
   decisions L760-815, hand_result/session_result L886-913, retains raw child stdout
   bytes ChildConnection.read_stream L512-537, base64 into the report L986-989.
P3 Session wraps one host Table per hand SESS.play_hand L233-315: hand result dict
   L240-251, entry L252-253 (ordinal, button, starting_stacks, result), completion
   L315; outer report SESS L183-190, L327-361.
P4 TOOL.play L282-311 builds the schedule from the witness, runs Session, calls
   EA.classify with blueprint=decode_blueprint(wire), teacher_actions, board,
   private_hands from the witness, stacks. TOOL.agreement L345-373 requires 'hit' on
   every primary, three controls, EA.summarize on primaries. TOOL.complete L402-416 and
   TOOL.accounting L439-463 re-derive from observations.
P5 EA.classify L273-361 -> frames_for L149-218 (bind_identity L120-146,
   admitted_decision L53-87, clean L90-95) -> replay L221-270 -> agreement L311-361.

## 3. Nested schema and attack table

Columns: member | required (producer/host) | classifier check (EA line) | (a) absent |
(b) wrong JSON type | (c) equal-but-not-it (False/0, 1.0/1, True/1) | (d) default or
conversion | outcome. "EX" = excluded (Unusable/KeyError/TypeError caught at L308),
"DIS" = disagreement, "CRASH" = uncaught exception (fail-closed, no credit).

### 3.1 Session report (SESS L183-190, L356-361)
version | str 'pontius-v0a-table-session-result-vN' | L123 == | a KeyError EX | b EX
session_id | str, prefix | L124 type str + startswith | a EX | b EX
status | 'completed' | L290 | a EX | b EX (str ==)
stop_reason | None | L291 is None | a EX | b EX | c: False is not None -> EX
failure_reason | None | L94 via clean L289 | a KeyError L93 EX | b EX | c False/'' EX
secondary_failures | list [] | L94 type list and == [] | a KeyError L92 EX | b tuple EX
requested_hands, completed_hands | int 1 | L292-293 exact_integer | a EX | b EX |
   c True -> type bool refused L45 EX; 1.0 refused EX
hands | list len 1 | L294 | a EX | b EX
source_commit, blueprint_artifact_sha256, blueprint_sha256 | str equal to ready and hand
   | L131-132 chain; shape L141-146; digest L162 | a EX | b EX (str != non-str)
provider, config_sha256 (v2 only) | equal chain | L133-139 | a EX | b EX
input_sha256, next_button, carried_stacks | not consumed | none | no effect
extra members | not refused (no exact set on the outer report) | advisory only

### 3.2 Hand entry (SESS L252-253)
ordinal | int 1 | L297 exact_integer | a EX | b EX | c True/1.0 EX
button | int 0 | L222 exact_integer | a EX | b EX | c False/0.0 EX
starting_stacks | list of six ints == stacks | L223-224 | a EX | b EX | c True/4.0 EX
result | dict | L299 clean -> L91 | a EX | b EX

### 3.3 Hand result (SESS L240-251, L315)
version, session_id | derived strings | L127-128 | a EX | b EX
status | 'completed' | L300 | a EX | b EX
failure_reason, secondary_failures | None, [] | L299 -> L92-94 | a EX | b EX | c EX
source_commit, blueprint_artifact_sha256, blueprint_sha256 | chain/digest | L131-132,
   L162-163 | a EX | b EX
applied_actions | list of exact rows | L229, L231 exact_fields | a EX | b EX
  .index | int == position | L236 | a EX(L231) | b EX | c False/0.0 EX
  .seat | int == acting seat | L237 | a EX | b EX | c EX
  .street | str == state street | L238 | a EX | b EX
  .origin | 'bot'/'opponent' | L240 | a EX | b EX
  .action | {kind, raise_to} exact | L241 parsed_action -> HandAction | a EX | b EX |
     c raise_to True -> _require_exact_int refuses bool EX; 2.0 EX
settlement | dict equal to terminal and to kernel replay | L214-217, L267-269 | a EX |
   b EX (json text differs) | c False vs 0 -> 'false' vs '0' EX; 1.0 vs 1 EX
child_exit_code | int 0 | L301-302 | a EX | b EX | c False EX
child_stdout_base64 | base64 str | L150 validate=True | a EX | b TypeError EX
capture_truncated | False | L301 is False | a EX | b EX | c 0 is not False EX
child_stderr_base64, input_sha256 | not consumed | none | no effect (advisory: the
   host input identity is not bound by the classifier; hero hand and board are bound
   through visible_cards_sha256 at every controlled decision, villain/folder hands only
   through settlement replay)
provider, config_sha256 (v2) | chain | L135-136 | a EX | b EX

### 3.4 Frame stream (ADP L188-192; HOST decode L52-90)
base64 | valid | L150 | invalid -> binascii.Error EX
raw | nonempty, ends LF | L151 | EX
lines | strict JSON, unique keys, finite floats, no constants | L152-154 | EX
frames | >= 3 dicts | L155 | EX
frames[0]/[-2]/[-1] types | ready/hand_result/session_result | L157-158 | EX
every frame member set | exact WIRE_FIELDS (+provider, config_sha256 on v2 ready) |
   L166-172 | any absent/extra member -> EX
protocol, session_id | shared by every frame | L173-174 | EX
Leniency (advisory, not credit): L154 uses str.splitlines (universal newlines), so a
capture with CR LF, or with U+001E/U+0085/U+2028 between objects, is framed where HOST
L68 and ADP L95 would refuse; no per-frame 16384 limit. Content checks still apply.

### 3.5 Ready frame (ADP L226-231; HOST L729-737)
protocol | one of two | L160 | EX
session_id | nonempty str == derived | L161, L129 | EX
source_commit | 40 hex == hand == report | L131, L144-146 | EX
source_manifest_sha256 | 64 hex; v2 == record | L144-146, L58 | EX
blueprint_artifact_sha256 | 64 hex chain | L131, L144-146 | EX
blueprint_sha256 | == PreparedBlueprint.digest | L162 | EX
evidentiary | False | L164 is False (NEW) | a EX (member set) | b/c True, None, 'false',
   0 -> EX
provider (v2) | 'baseline-rules-v1' | L134 (NEW) | EX
config_sha256 (v2) | 64 hex, == hand == report == record | L135-139, L58 (NEW) | EX

### 3.6 Action frame (ADP L199-201; HOST L826-831)
hand_id | == record.hand_id == identity | L197, L195 | b EX
action_index | int >= 1, == record | L179 (NEW), L197 | a EX | b EX | c True/1.0 EX
seat | int 0..5, == record | L180 (NEW), L197 | c EX
street | == record.street (validated label) | L197-198 | b EX
action | exact {kind, raise_to}, == record.selected_action | L182 (NEW), L199 | c EX
ordering | action then decided event_result; no unpaired action | L178, L192, L202 | EX

### 3.7 event_result frame (ADP L243-247; HOST L845-860)
event_index | int == running count | L186-187 | a EX | b EX | c EX
status | 'accepted'/'decided'; decided iff decision | L188, L191 | EX
decision | None or dict | L190-194 | non-dict -> clean L91 EX
failure | None | L188 | EX

### 3.8 v1 decision record (RT L1286-1306; TRACE L216-237; HOST L796-815)
member set | exactly DecisionRecord fields (16) | L66 | a/extra EX
hand_id | ascii nonempty str; == identity | MODEL L464 via L84; L195 | b EX
event_index | exact int >= 0; == frame; == replay | MODEL L465; L195; L326 | c True EX
action_index | exact int >= 1; == action frame; == replay | MODEL L466; L197; L326 | c EX
street_action_index | exact int >= 1; == replay | MODEL L467; L326 | c EX
seat | exact int 0..5; == replay (2) | MODEL L468; L326 | c EX
street | label; == replay; river test | MODEL L469; L326; L337 | b EX
state_before_sha256, state_after_sha256, visible_cards_sha256 | 64 hex; == replay |
   MODEL L470-476; L326 | b EX; wrong value DIS
blueprint_sha256 | 64 hex; == prepared.digest | MODEL L476; L334 | wrong value DIS
selected_action | exact {kind, raise_to}; == action frame; BettingAction == applied
   action == replayed lookup | L85 parsed_action; L199; L331-333 | c EX; wrong DIS
selection_reason | str only (by design) | L73; compared raw at L335, L339 | a EX (L66) |
   b None/1 EX | unknown label DIS | relabel DIS. Constructor at L87 substitutes
   PASSIVE_DEFAULT (case d) but the raw value drives L335/L339, so no hit from it.
spine_reason | in SPINE_REASONS | MODEL L481 via L84 | EX
timing | exact 10 members | L74 | a/extra EX
  .status | 'completed' | L76 TimingStatus(...), L78 | other label/True/1 -> ValueError EX
  .interruption_reason | None | MODEL L406 | str -> EX
  .wall_start_ns, .last_valid_observation_ns, .emission_observed_ns, .elapsed_ns |
     exact ints, elapsed == emission - start | MODEL L401-415 | c True/1.0 EX
  .response_compute_seconds, .response_uninstrumented_seconds | exact float >= 0 finite,
     sum within 2e-9 of elapsed/1e9 | MODEL L377-382, L416-419; L81-82 | c 0 (int) EX
  .work_cutoff_crossed, .deadline_crossed | exact bool False | MODEL L420-422; L78-79 |
     c 0 -> type bool refused EX
preparation_use | exact 3 members | L68 | a/extra EX
  .producer_status | 'producer_absent' | L69 | EX
  .artifact_sha256s | list [] | L70 | () or '' -> type list refused EX; ['x'] EX
  .credited_seconds | exact 0 | L71 | c False/0.0 EX. Conversion to () at L86 happens
     after the raw checks (case d closed).
failure_reason | None | L55 -> L94 | a EX | b EX | c False EX
typed construction | DecisionRecord(**...) L84-87 only after every raw check (O3)

### 3.9 v2 decision record (RT L1172-1191; PCODEC L23-41; HOST L761-795)
validator | public validate_decision | L57 (NEW; case e closed) | exact 27 members
   (PCODEC L46); labels; exact ints (TRACE L659-667 refuses bool); digests; actions;
   proposal/outcome/reason/origin/delivery consistency; timing exact keys and
   _validate_timing (exact bool flags, exact ints, exact float seconds, partition,
   deadline flag == elapsed > 15e9); preparation exact list []/int 0; failure/timing
   consistency. Any absent member, wrong type or equal-but-not-it value -> ValueError EX.
provider, config_sha256, source_manifest_sha256 | == ready | L58-59 | EX
fallback_blueprint_sha256 | == ready.blueprint_sha256 | L60 | EX
delivery_status | 'accepted'; delivered == applied == selected | L62-64 | EX
timing | re-checked completed/no flags/<= 15 s/sum | L74-82 | EX
failure_reason | None | L55 | EX
street, selection_reason | used only by counters L313-315 under baseline strategy;
   under a mislabelled strategy='blueprint-v1' the missing 'blueprint_sha256' member
   makes L334 a cause -> DIS, never hit.

### 3.10 hand_result frame (ADP L278-285; HOST L886-901)
complete | True | L207 is True | c 1 EX
settlement | json == hand.settlement | L214-217 | EX
rank_source | 'host_supplied' iff showdown | L306-307 | EX
evidentiary | False | L205 | EX
preparation_compute_seconds, post_terminal_compute_seconds | finite float >= 0 |
   L98-99, L209-210 | c 0 (int) EX
interrupted_response_count | exact 0 | L208 (NEW) | c False/0.0 EX
accounting_complete | True | L205 | c 1 EX
failure_reason, secondary_failures | None, [] | L204 -> L92-95 | EX

### 3.11 session_result frame (ADP L296-299; HOST L902-911)
status | 'completed' | L211 | EX
terminal_publication_compute_seconds | finite float >= 0 | L213 | None/int EX
accounting_complete, evidentiary | True, False | L205 | EX
failure_reason, secondary_failures | None, [] | L204 | EX
accounting_scope | 'runtime_begin_to_final_publication' | L212 | EX

### 3.12 Settlement (HOST L873-884; kernel settle no_limit_betting L696-752)
payouts, final_stacks, pots[].amount, pots[].seats | exact ints/lists | bound only by
   json.dumps equality with the kernel replay L267-269 (and terminal L214-217); json
   text distinguishes false/0, 1.0/1, extra members, order; chips = replayed
   net_returns[2] L270, never read from the report.

### 3.13 Caller inputs (TOOL L307-309)
blueprint | exact ImmutableBlueprintActionSource | L281 (lookup L35-36) | CRASH otherwise
teacher_actions | dict name -> BettingAction | L348 .get | None -> no hit; other -> DIS
board | sorted tuple, distinct with hands | L282-283 | CRASH otherwise (before try)
private_hands | six hole cards | L283 | hero bound via visible digest L326
stacks | replay depth | L222-224; declared root always at 4 (L345, bridge L79) |
   stacks != 4 -> selection.key != declared -> never agreement_eligible
strategy | 'blueprint-v1' or other | L316 | not cross-checked against ready.protocol
   (advisory): a v1 blueprint capture classified with strategy='baseline-rules-v1'
   returns chip_eligible True / 'unsupported'.

### 3.14 Agreement branch (L311-361)
records vs expected count | L320-321 cause
per-index replayed fields | L326 cause (event_index, action_index, street_action_index,
   seat, street, three state digests) - binds hero hand, board, full public history
   (spine digest covers history, stacks, contributions)
selected action | == applied action and == replayed lookup | L331-333 cause
blueprint identity and reason | L334-336 cause
pre-river reason | 'passive_default' | L339-340 cause
river count | exactly one | L341-342 cause
declared root | selection.key == root_key(replay_root(), board, hero) | L345-346
teacher | absent + hit -> cause; default or wrong action -> cause; hit only when
   no cause at all | L348-355
outside root + hit | cause | L356-357

### 3.15 summarize (L364-378)
scheduled | exact int >= 0, >= len(results) | L366-367 | bool -> ValueError raised
classification | one of four | L370 | ValueError
complete | no missing, disagreement or excluded | L378 | 'unsupported' counts toward
   complete (advisory): the frozen caller gates every primary on 'hit' (TOOL L347-348,
   L409-410) so the tool cannot report success on it.
completed, agreement_eligible | sum of row values via .get | L374-375 | counters only

## 4. Failure cases and limits

F1 Caught at L308: ValueError (Unusable, JSONDecodeError, TraceInvalidError,
   UnicodeDecodeError), TypeError, KeyError, IndexError, binascii.Error. Not caught:
   AttributeError, RecursionError, AssertionError, OverflowError -> CRASH (fail-closed).
F2 prepared.action_for at L328 runs outside the try: an illegal table action for the
   replayed decision raises ValueError out of classify (fail-closed, caller artifact).
F3 The classifier never verifies the host's acceptance of the frames; it re-parses with
   its own (slightly more lenient) framing, then requires full consistency with the
   retained applied_actions, settlement and identities.
F4 Nothing in the classifier reads the reviewed commit or the manifest; admission owns
   that comparison (comment L140).

## 5. Candidate defects to test against the deferred inputs

C1 (advisory) strategy/protocol not cross-bound (3.13).
C2 (advisory) summarize.complete admits 'unsupported' primaries (3.15).
C3 (advisory) framing leniency relative to HOST/ADP (3.4).
C4 (advisory) hand result input_sha256 and blueprint artifact wire identity are not bound
   by the classifier; canonical digest and visible-card digests are (3.3, 3.5).
No member found whose absence, wrong type, equal-but-not-it value, default or conversion
can yield 'hit', chip_eligible True or agreement_eligible True from a report that a
completed real host attempt could not have produced.
