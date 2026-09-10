# Prosecutor inventory: v0a-eval-panel-completion r003 (written before deferred inputs)

Role: prosecutor. Candidate 7ca821802c949b047becf6599d603b3b63d51fa7, sole parent
430ad75de79cec13d66ff3dc4981dd3770a371b7, manifest
1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd. Everything below is
derived from the frozen blobs at the candidate commit (git cat-file), the packet's initial
inputs, and stdlib-only probes labeled reviewer arithmetic. coverage.md and checks/ were
NOT opened before this file was written and hashed.

## 1. Identity verified from Git objects (reviewer arithmetic)

- refs/heads/review/v0a-eval-panel-completion/r003 -> 7ca82180; commit tree
  3d2fe79d2af20125e322dd4a668335e789810863; exactly one parent 430ad75d.
- diff-tree parent..candidate: exactly two modified paths, src/pontius/eval_agreement.py
  (8329de1e -> 5122fd5b) and tests/test_eval_protocol.py (059adac1 -> 5c53a450).
- Recomputed manifest rows ("<sha256>  <path>\n", sorted bytewise) equal manifest.sha256
  byte for byte; digest of that file equals the stated 1f48c97a...57fd.
- inputs/parent-manifest.sha256 recomputed at 430ad75d over its three-file delta from
  449a2a3c (eval_agreement.py, tests/cases.json, tests/test_eval_protocol.py added):
  byte-identical, file digest 6e36bb41... as listed.
- supporting-files.json digest c1a9c980..., brief.md 4d65b2aa..., coverage.md digest
  27cfa20b... (hashed only, not opened). All 51 dependency pins in inputs/dependencies.json
  verified at the base each states, including the packet copies under inputs/.

## 2. Obligations the classifier must meet (from brief.md, accepted design s.5, s.7)

O1 Host-equivalence of admission: any child stdout byte sequence the unchanged host would
   refuse (framing, sizes, CR/BOM, UTF-8, depth, integer digits, duplicates, field sets,
   field rules) is excluded before chip_eligible, agreement_eligible, hit, or schedule
   completion. The frozen host oracle is tools/v0a_table_host.py read_stream (512-537),
   decode_json (52-90), WireConsumer.read/action/timing/decision/closure_fields/settlement/
   complete (662-913).
O2 Outcome eligibility precedes agreement eligibility; they are separate values.
O3 Missing records, defaults, conversions and failures never become successful credit
   (Tier C): teacher identity, exported membership, retained-outcome interpretation.
O4 Existing finite-number restriction remains in force (classifier stricter than host).
O5 Valid v1 CHECK hits, off-pool defaults, reason-only disagreements and completed v2
   baseline divergence keep their previous outcomes and settled chips.
O6 Exactly one controlled river decision for a hit; pre-river reasons passive_default.
O7 summarize: one disposition per observed attempt; missing stays visible.

## 3. Producer / consumer paths

Producer of the retained bytes: tools/v0a_event_adapter.py PipeOutput.frame (188-192,
json.dumps sort_keys compact allow_nan=False + LF, UTF-8) -> child stdout -> host
ChildConnection.read_stream (capture cap 2097152 stdout / 65536 stderr, frame split on
byte 10, frame <= 16384 incl. LF, partial < 16384, EOF with pending -> protocol_invalid)
-> WireConsumer.read -> decode_json -> field rules -> Table/kernel. Session
(tools/v0a_table_session.py play_hand 233-315) wraps the host per hand into
hands[i].result with child_stdout_base64 = b64encode(connection.stdout).
Consumer under review: src/pontius/eval_agreement.py classify (306-394) ->
frames_for (183-251) -> decode_frame (120-151) -> admitted_decision (53-87) -> replay
(254-303) -> agreement stage (344-393); summarize (397-411).
Caller: tools/v0a_eval_panel_completion.py play (282-311) passes strategy='blueprint-v1',
stacks, caller-owned board/private_hands/teacher_actions; agreement (314-373) and
accounting (439-463) consume classification and summarize.

## 4. Nested schemas the classifier consumes, with the host-required type/value

Notation: H = what the unchanged host requires (line refs in v0a_table_host.py);
C = what the classifier checks (line refs in eval_agreement.py); level = EXCL (excluded
before chip credit), AGR (agreement-stage only: chip_eligible=True, disagreement),
NONE (not checked).

### 4.1 Session report (outer, from Session.run)
- version: C 157 == 'pontius-v0a-table-session-result-'+v (EXCL). Not a host frame.
- session_id: C 158 str startswith prefix; suffix binds hand/ready ids (EXCL). Charset
  regex [A-Za-z0-9_-]{1,40} (session 205) NOT checked by C.
- status == 'completed', stop_reason is None (323-324, EXCL).
- failure_reason None, secondary_failures == [] (clean 322, EXCL).
- requested_hands, completed_hands exact int 1 (325-326, EXCL); hands list len 1 (327).
- source_commit, blueprint_artifact_sha256, blueprint_sha256 (+provider, config_sha256 v2)
  equal to ready/hand (165-170, EXCL).

### 4.2 Hand entry hands[0]
- ordinal exact 1 (330, EXCL); button exact 0 (255); starting_stacks list of six exact
  ints == stacks (256-257, EXCL); result dict (clean 332).

### 4.3 Hand result hands[0].result
- status == 'completed' (333); failure_reason None; secondary_failures == [] (332).
- capture_truncated is False; child_exit_code exact int 0 (334-335). H: Session 299-301.
- child_stdout_base64: b64decode validate=True; 0 < len <= 2097152; endswith LF
  (184-186). H: read_stream cap 2097152 (513, 523-527), pending empty at EOF (520).
- child_stderr_base64: NOT read by C. H: stderr cap 65536 -> truncated -> transport_failed
  (513, 525-527, 624-625).
- applied_actions: list of {index, seat, street, action{kind,raise_to}, origin} replayed
  through the kernel (262-287). H: produced by Table.apply (265-266).
- settlement: not None; dumps-equal to terminal.settlement and to replay (247-250,
  300-302). H: settlement (873-884) structure + == table.settlement().
- version, session_id, source_commit, blueprint_artifact_sha256, blueprint_sha256
  (+provider, config_sha256): bound in bind_identity (154-180).
- input_sha256: NOT read by C (the caller's deal/board are trusted, cross-bound only via
  visible_cards_sha256 at AGR and settlement replay at EXCL).

### 4.4 Frame stream (raw bytes) - byte level
Per frame f = line + b'\n':
- bytes, 0 < len <= 16384, endswith LF (C 122-123; H 68, 532, 664).
- no b'\r' anywhere, no leading EF BB BF (C 124; H 68-69).
- bracket depth outside strings <= 8 (C 125-140; H 70-85, identical scanner).
- UTF-8 strict decode (C 147; H 86). Non-UTF-8 -> ValueError both.
- json.loads: duplicate keys refused (unique_object / pairs), parse_constant refused,
  parse_int digits <= 640 (both), parse_float: H float (inf admitted), C finite only.
- RecursionError: both refuse (unreachable under depth 8).
- Empty frame b'\n': both refuse (JSONDecodeError). Trailing bytes without LF: H 520
  protocol_invalid, C 186. Empty capture: H 664 (None), C 185.
- Separators: only byte 10 splits in both (bytes.split vs read_stream index(10)). CR, VT,
  FF, FS/GS/RS, NEL, LS, PS outside strings -> JSON error in both; CR refused by byte
  check in both. Inside strings: control bytes < 0x20 refused (strict), NEL/LS/PS
  admitted by both (stdlib probe).
- Extra frames after session_result: H 912 (receive must be None); C 189-191 shape.

### 4.5 ready frame (frames[0])
- protocol in {v1,v2 names} and == every frame (C 193, 206; H 670). session_id nonempty
  str, == every frame and derived child id (C 194, 163; H 670).
- fields exactly protocol session_id type source_commit source_manifest_sha256
  blueprint_artifact_sha256 blueprint_sha256 evidentiary (+provider config_sha256 v2)
  (C 199-205; H 667-669).
- source_commit: H == source.commit (731); C == hand == report, 40 hex (165-166, 175-180).
- source_manifest_sha256: H == child_manifest (732); C shape only (64 hex) - NOT bound
  (comment 174: admission owns that comparison).
- blueprint_artifact_sha256: H == artifact hash (733); C == hand == report, 64 hex.
- blueprint_sha256: H == policy hash (734); C == blueprint.digest and == hand/report.
- evidentiary: H is False (734); C is False (197).
- v2 provider == identity.provider (736); C == 'baseline-rules-v1' == hand == report (168-170).
- v2 config_sha256 == identity.config (737); C == hand == report, 64 hex (169-173).

### 4.6 action frame
- fields protocol session_id type hand_id action_index seat street action (C 205; H 669).
- action_index: H integer >= 1 AND == bot_index+1 (826-828); C int >= 1 (212) EXCL,
  equality to replay only via record at 359 (AGR).
- seat: H integer 0..5 AND == controlled_seat (826-829); C int 0..5 EXCL, == 2 AGR.
- hand_id: H == child_id (827); C == record.hand_id == identity (228, 230) EXCL.
- street: H == current street (830); C == record.street (230) EXCL, == replay AGR.
- action: H HandAction(**) then apply_bot legality (831, 842); C parsed_action (215) EXCL,
  == record.selected_action (232) EXCL, == applied history AGR (365).
- Order: H action only when expects_action (822-825, 679); C action must be followed by a
  decided event_result (211, 225, 235) EXCL; placement vs replay AGR (353, 359).

### 4.7 event_result frame
- fields protocol session_id type event_index status decision failure (C 205; H 669).
- event_index: H integer and == table.event_index (845); C int == len(events) (219),
  total == replay final_event+1 (338). EXCL.
- status: H str in accepted/decided/failed (846-847), failed -> child_failed; C in
  accepted/decided (221) EXCL.
- failure: H None (855); C None (221) EXCL.
- decision: H None iff accepted (857-859); C 224-225 EXCL.

### 4.8 v1 decision record (16 members, DecisionRecord)
- exact 16 fields (C 66; H 796-799). hand_id ascii nonempty == identity (C 228 + model
  464; H 815). event_index == event_result index (C 228; H 815).
- action_index >= 1 (model 466), street_action_index >= 1 (467), seat 0..5 (468), street
  in names (469): shape EXCL; H equality to expected (815) -> C AGR only (359).
- state_before_sha256, state_after_sha256, visible_cards_sha256, blueprint_sha256: shape
  64 hex (model 470-476) EXCL; H equality (815) -> C AGR (359, 367).
- selected_action: exact {kind, raise_to}, HandAction validity (C 49-50, 85); == frame
  action (232) EXCL; H expected (838).
- selection_reason: H SelectionReason(value) -> only 'table_hit' or 'passive_default'
  (809-812, protocol_invalid otherwise); C type str only (73), constructed with
  PASSIVE_DEFAULT substituted (87); legal-label mismatch AGR (367-369). ANY OTHER STRING
  IS HOST-REFUSED BUT C-ADMITTED.
- spine_reason: in SPINE_REASONS (model 481) both EXCL.
- timing: 10 exact fields; TimingRecord validation (C 74-77; H 689-701): status
  'completed' (C 78; H 813-814), interruption_reason None (model 406), wall_start/last/
  emission exact ints, elapsed == emission - wall_start, seconds exact finite floats >= 0,
  flags exact bool; work_cutoff/deadline False; elapsed <= 15e9; sum within 2e-9 (C 78-82;
  H 702-706). EXCL. Note C uses `not flag` but TimingRecord already forces bool.
- preparation_use: exact 3 fields; producer_status 'producer_absent'; artifact_sha256s
  list == []; credited_seconds exact int 0 (C 67-71; H 801-805). EXCL.
- failure_reason: None (clean 55; H 813). EXCL.

### 4.9 v2 decision record (ProviderDecisionRecord, 27 members)
- validate_decision (public codec 44-137) applied by both (C 57; H 763). EXCL.
- provider, config_sha256, source_manifest_sha256 == ready; fallback_blueprint_sha256 ==
  ready.blueprint_sha256 (C 58-61); H provider_expected equality (770).
- delivery_status 'accepted', delivered == applied == selected (C 62-64; H 788-791).
- timing as 4.8 (C 74-82; H 787-789).
- NOT checked by C: action_index, street_action_index, seat, street, state_before_sha256,
  state_after_sha256, visible_cards_sha256, decision_sha256, fallback_action,
  fallback_reason vs replayed lookup, proposal validity/legality (H 764-785 apply
  fallback and selected to the context state; H 770 state_mismatch on any expected
  mismatch; H 780 proposal validity). For v2 C returns 'unsupported' with
  chip_eligible=True and no diagnostic (349-351).

### 4.10 hand_result frame (terminal)
- fields as WIRE_FIELDS (C 205; H 669). failure_reason None, secondary_failures == []
  (C 237; H 889, 897-898). accounting_complete is True, evidentiary is False (C 238-239;
  H 863, 897). complete is True (C 240; H 890, 894). interrupted_response_count exact 0
  (C 241; H 890, 897). preparation/post_terminal seconds finite float >= 0 (C 242-243;
  H 891-892). rank_source == 'host_supplied' iff showdown (C 339; H 893, 899). settlement
  dumps-equal to outer (C 247-250) and replay (300-302); H 873-884.

### 4.11 session_result frame (closing)
- failure_reason None, secondary == [] (C 237; H 903, 911); accounting_complete is True,
  evidentiary is False (C 238; H 863, 910); status == 'completed' (C 244; H 904, 908);
  accounting_scope literal (C 245; H 905); terminal_publication_compute_seconds finite
  float >= 0 (C 246; H 906-910). EOF after (H 912; C 189-191).

### 4.12 Timing (TimingRecord) - covered in 4.8. preparation_use - 4.8.
### 4.13 Settlement {payouts[6], final_stacks[6], pots[{amount, seats}]} - 4.3/4.10.

## 5. Failure cases and credit paths (potential successful-credit paths to attack)

F1 Byte-level: CRLF, lone CR, NEL/LS/PS/VT/FF/FS/GS/RS separators, BOM, non-UTF-8,
   frame 16385, capture 2097153, depth 9, 641-digit int, NaN/Infinity/1e400, duplicate
   key, trailing bytes, empty frame, empty capture, extra frames.
F2 Parsed-level host field rules whose violation is AGR not EXCL (v1): action frame
   action_index/seat/street, record action_index/street_action_index/seat/street/hashes/
   blueprint_sha256, selection_reason unknown label.
F3 v2: any provider_expected field or proposal/fallback legality mismatch -> C
   chip_eligible=True, no diagnostic.
F4 stderr over 65536 with capture_truncated=False.
F5 Identity charset outside the session/adapter regex.
F6 strategy argument not cross-checked against ready.protocol; v2 frames under
   strategy='blueprint-v1' can only reach 'disagreement' (no blueprint_sha256 key).
F7 summarize: 'unsupported' does not block complete; caller compensates (347, 413).
F8 (c)-type: False/0, True/1, 1.0/1 at every integer or boolean member (see 4.x: all
   integer members use exact_integer/type checks; booleans use `is`; settlement uses
   json.dumps equality which distinguishes 1/1.0/true).
F9 (d)-type: SelectionReason.PASSIVE_DEFAULT substitution (87); PreparationUseRecord tuple
   conversion after list check; TimingStatus conversion; DecisionRecord has no defaults.
F10 (e)-type: v2 validate_decision is the public validator (57).

## 6. Line counts and hygiene from raw frozen bytes (reviewer arithmetic)
- eval_agreement.py candidate: 21402 bytes, 411 lines (371 non-blank); parent 378 lines.
- test_eval_protocol.py candidate: 13127 bytes, 218 lines (208 non-blank); parent 137.
- Both blobs: LF-only, no CR, no BOM, no tab, no line > 100 columns, no trailing
  whitespace, final LF present.
