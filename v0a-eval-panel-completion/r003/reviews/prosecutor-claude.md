# Prosecutor report: v0a-eval-panel-completion r003

Role: prosecutor (mutation attack; no verdict issued). Reviewer: Claude, cold packet path only.
Candidate ref refs/heads/review/v0a-eval-panel-completion/r003 at commit
7ca821802c949b047becf6599d603b3b63d51fa7,
sole parent 430ad75de79cec13d66ff3dc4981dd3770a371b7, tree 3d2fe79d2af20125e322dd4a668335e789810863,
manifest 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd. Every finding below
binds to that commit and manifest. Line numbers: C = src/pontius/eval_agreement.py at the candidate,
H = tools/v0a_table_host.py at the candidate (unchanged), M = src/pontius/v0a/model.py.

## 1. Identity results (from Git objects; reviewer arithmetic, not a test receipt)

- Ref resolves to 7ca82180; one parent 430ad75d; tree matches candidate.json.
- Exactly two changed paths against the parent: src/pontius/eval_agreement.py (8329de1e ->
  5122fd5b) and tests/test_eval_protocol.py (059adac1 -> 5c53a450).
- Manifest recomputed as "<sha256>  <path>\n" rows over raw blobs, sorted bytewise: byte-identical
  to manifest.sha256; its digest equals the stated 1f48c97a...57fd.
- inputs/parent-manifest.sha256 recomputed at 430ad75d over its three-path delta from 449a2a3c:
  byte-identical; file digest 6e36bb41... as listed.
- supporting-files.json (c1a9c980...), brief.md (4d65b2aa...), coverage.md (27cfa20b..., hashed
  before opening, opened only after the inventory hash) and all 32 checks/ digests match.
- All 51 dependency pins verified at the base each states, including the packet copies.
- RED commit named in checks/red-journal.jsonl, 81a5aaf5, is refs/heads/check/.../r003-red:
  parent 430ad75d, single delta tests/test_eval_protocol.py 059adac1 -> 5c53a450, i.e. exactly
  the candidate's test blob on the parent source. refs/heads/check/.../r003-focused = 7ca82180.

## 2. Standard applied

Host-equivalence of admission: any child stdout byte sequence the unchanged host would refuse
(framing, sizes, CR/BOM, UTF-8, depth, integer digits, duplicates, field sets and field rules)
must be excluded before chip_eligible, agreement_eligible, hit or schedule completion. Crediting
such a capture is an Important candidate regardless of whether the credited values change.
Tier C lens: missingness, defaults, conversions and failures must not become successful credit.

## 3. Inventory reference

D:/Pontius/tmp/eval-completion-r003-prosecutor-3354fe13/inventory-prosecutor-claude.md
SHA-256 d3cd01f78c187394a8f394ca78489379980203b67f27f233f29ec875ef455b5e (14943 bytes), written
and hashed before coverage.md or any checks/ file was opened.

## 4. Attack table A: raw bytes the classifier decodes (frames_for 183-191, decode_frame 120-151)

Column "host": would the unchanged host accept these bytes (H read_stream 512-537, decode_json
52-90, read 662-664, complete 912)? Column "C": classifier outcome and refusing line.

| #   | mutation of a valid capture        | host                     | C outcome (line)           |
|-----|------------------------------------|--------------------------|----------------------------|
| A1  | every LF -> CRLF                   | refuse H68 (CR)          | excluded C124              |
| A2  | first LF -> lone CR                | refuse H68; frames merge | excluded C124              |
| A3  | first LF -> U+0085 (C2 85)         | refuse H86 Extra data    | excluded C147 ValueError   |
| A4  | first LF -> U+2028 or U+2029       | refuse H86               | excluded C147              |
| A5  | first LF -> U+000B or U+000C       | refuse H86 (not JSON ws) | excluded C147              |
| A6  | first LF -> U+001C, 1D or 1E       | refuse H86               | excluded C147              |
| A7  | leading EF BB BF on first frame    | refuse H69               | excluded C124              |
| A8  | EF BB BF at start of frame 2       | refuse H69               | excluded C124 (per frame)  |
| A9  | 0xFF prepended; ED A0 80 in string | refuse H86 decode        | excluded C147 (Unicode-    |
|     |                                    |                          | DecodeError is ValueError) |
| A10 | ready frame padded to 16384 w/ LF  | accept H532 (<=16384)    | admitted C122; same        |
|     |                                    |                          | classification             |
| A11 | ready frame padded to 16385 w/ LF  | refuse H532/H535         | excluded C122              |
| A12 | capture exactly 2097152 bytes      | accept H523-526          | admitted C185              |
| A13 | capture 2097153 bytes              | truncated H526-527       | excluded C185              |
| A14 | drop final LF                      | refuse H520 pending      | excluded C186              |
| A15 | empty capture                      | refuse H664 (None)       | excluded C185              |
| A16 | inserted empty frame (bare LF)     | refuse H86 Expecting     | excluded C147              |
| A17 | nesting depth 9 outside strings    | refuse H83               | excluded C138              |
| A18 | 2000 nested brackets               | refuse H83 before parse  | excluded C138 (no          |
|     |                                    |                          | RecursionError reachable)  |
| A19 | integer token 641 digits (+/-)     | refuse H54               | excluded C143              |
| A20 | NaN / Infinity / -Infinity         | refuse H57-58            | excluded C111              |
| A21 | 1e400 (float overflow)             | ACCEPT as inf H87 float  | excluded C116 (stricter)   |
| A22 | duplicate member key               | refuse H63               | excluded C105              |
| A23 | two JSON values in one frame       | refuse H86 Extra data    | excluded C147              |
| A24 | extra frame after session_result   | refuse H912              | excluded C189-191          |
| A25 | duplicate session_result frame     | refuse H912              | excluded C190 (frames[-2]) |
| A26 | empty object frame before ready    | refuse H666/H679         | excluded C190 KeyError     |
| A27 | NUL byte inside a string           | refuse H86 strict        | excluded C147              |
| A28 | U+2028 inside a JSON string        | accept both              | admitted; identical        |
| A29 | leading spaces/tab before brace    | accept both (json ws)    | admitted; identical        |

All A-rows are host-equivalent except A21, where the classifier is stricter. No host-accepted
stream can contain an infinite float: every wire float member is finite-checked by the host
(H641-642 finite_seconds at 891-892, 906-910; M378-381 through TimingRecord at H699; codec
_validate_timing for v2). So A21 over-excludes nothing the host would complete.

## 5. Attack table B: every consumed member, cases (a) absent, (b) wrong type, (c) equal-but-not-it,
## (d) default/conversion, (e) v2 public validator

Outcome key: EXCL = excluded before credit (line); AGR = chip_eligible=True, agreement-stage
disagreement; CREDIT = chip_eligible=True with no diagnostic. Host column from H unless stated.

Session report / hand entry / hand result (Session envelopes; not host frames, but the outer gate)
- version, session_id, status, stop_reason, failure_reason, secondary_failures, requested_hands,
  completed_hands, hands, ordinal, button, starting_stacks, status, capture_truncated,
  child_exit_code, applied_actions, settlement, identity fields: (a) KeyError -> EXCL C341;
  (b)/(c) requested_hands/completed_hands/ordinal/button/starting_stacks/child_exit_code/
  interrupted counters use exact_integer or `type is int` (C325-335, 255-258, 269-270) so True,
  1.0, "1" -> EXCL; capture_truncated `is False` C334 (0 -> EXCL); settlement compared by
  json.dumps sort_keys (C247-250, 300-302) so 4.0/true vs 4 -> EXCL; applied_actions rows
  exact fields C264, origin C273, order C269-271, legality via kernel C275 (ValueError -> EXCL).
- session_id charset/length ([A-Za-z0-9_-]{1,40}, session.py 205; adapter 321): not checked;
  a consistent triple of ids with a space is admitted (carried advisory, parent F-04/C4 class).
- child_stderr_base64: never read. Host stderr cap 65536 -> truncated -> transport_failed
  (H513, 525-527, 624-625). See P-04.
- input_sha256 (schedule bytes): never read; the caller's deal/board are trusted (carried
  advisory; visible_cards_sha256 AGR and settlement replay EXCL bind them partially).

ready frame (C190-207, bind_identity 154-180; H667-670, 729-737)
- type/protocol/session_id/field set: (a)(b) EXCL C190, 193-194, 201-207; protocol other than
  the two literals EXCL C193.
- source_commit, blueprint_artifact_sha256, blueprint_sha256: (a)(b)(c) EXCL C165-166, 175-180,
  195-196 (equality to hand/report/digest plus 40/64 lowercase hex shape).
- source_manifest_sha256: shape only C175-180. Host compares to child_manifest H732. The
  session envelopes do not retain it (C174 comment). Carried identity limit (parent F-04).
- evidentiary: True/None/"false"/0 -> EXCL C197 (`is False`). Host `is False` H734. Equivalent.
- v2 provider/config_sha256: EXCL C168-173, 203-205.

action frame (C210-217, 230-232; H826-831, 842)
- fields: EXCL C205. hand_id: EXCL C228/C230. action: exact fields C49, HandAction validity
  M141-147 (kind not in kinds, raise_to on non-raise, raise_to bool/0/float) -> EXCL C215;
  action != record.selected_action -> EXCL C232.
- action_index: (b)(c) bool/float/0 -> EXCL C212. Value != bot_index+1 (H828): only AGR C359
  through the record. See P-02.
- seat: (b)(c) EXCL C213. Value != 2 (H829): AGR C359. See P-02.
- street: type/value only through record equality C230 + DecisionRecord M469; value != current
  street (H830): AGR C359/370-375. See P-02.
- placement: action while none expected (H679/825): AGR C353/359. See P-02.
- two actions before an event_result: EXCL C211; action after last event_result: EXCL C235.

event_result frame (C218-234; H844-860)
- fields EXCL C205; event_index (b)(c) EXCL C219, non-sequential EXCL C219, count vs replay
  EXCL C338; status not in accepted/decided (incl. 'failed') EXCL C221; failure non-null EXCL
  C221; decision present iff decided EXCL C224; decided iff preceded by action EXCL C225.

v1 decision record (16 members; C55-87, 228-232; H796-815)
- field set (a): EXCL C66. hand_id: EXCL C228 + M464. event_index: EXCL C228 + M465.
- action_index/street_action_index/seat/street: (b)(c) EXCL via DecisionRecord M466-469 at
  C84; values vs host expected (H815 state_mismatch): AGR C359 only. See P-02.
- state_before_sha256/state_after_sha256/visible_cards_sha256/blueprint_sha256: shape EXCL
  M470-476; value vs host expected (H815): AGR C359/C367. See P-02.
- selected_action: EXCL C49-50/C85 shape; == frame action EXCL C232; vs applied history and
  lookup AGR C365 (design-intended disagreement).
- selection_reason: (b) non-str -> EXCL C73. (d) ANY string is admitted, DecisionRecord is
  constructed with PASSIVE_DEFAULT substituted C87; legal-label mismatch AGR C367-369. Host
  constructs SelectionReason(value) H809 inside try 806-812 -> protocol_invalid for anything
  but 'table_hit'/'passive_default' (M60-62). See P-01.
- spine_reason: not in SPINE_REASONS -> EXCL C84 via M481. Host H810 same.
- timing: field set EXCL C74; status not 'completed' EXCL C78; interruption_reason non-null on
  completed EXCL M406 at C77; wall_start/last/emission/elapsed bool/float/negative EXCL M401-415;
  elapsed != emission-wall_start EXCL M414; seconds int/NaN/inf/negative EXCL M378-381;
  work_cutoff/deadline 0/1/None EXCL M421; True EXCL C78; elapsed > 15e9 EXCL C79; sum off by
  > 2e-9 EXCL C81-82. Host H689-706 equivalent (TimingRecord + same two predicates).
- preparation_use: field set EXCL C68; producer_status EXCL C69; artifact_sha256s non-list or
  non-empty EXCL C70; credited_seconds True/0.0/1 EXCL C71 (exact_integer). Host H801-805 same.
  (d) tuple conversion C86 happens after the list == [] check; no default fills a missing member.
- failure_reason: non-null EXCL C55 (clean). Host H813.

v2 decision record (27 members; C56-64, 74-82; codec validate_decision 44-137; H760-795)
- (e) validate_decision is the public provider validator and runs at C57 before any credit;
  (a)(b) of every member and every label/consistency rule there -> EXCL (TraceInvalidError and
  ValueError are caught at C341). provider/config_sha256/source_manifest_sha256 vs ready and
  fallback_blueprint_sha256 vs ready.blueprint_sha256 EXCL C58-61; delivery_status != accepted
  EXCL C62; delivered != applied != selected EXCL C63-64; timing as v1 EXCL C74-82.
- NOT checked: action_index, street_action_index, seat, street, state_before_sha256,
  state_after_sha256, visible_cards_sha256, decision_sha256, fallback_action, fallback_reason,
  proposal action legality, applied/selected legality against the replayed state. Host refuses
  each: H764-767 apply fallback then selected to the context state (ValueError ->
  protocol_invalid), H770 expected-field equality (state_mismatch), H772-781 proposal
  validity, H782-785 state_after. Classifier returns 'unsupported' with chip_eligible=True and
  causes ['agreement:baseline_outside_declared_root'] (C349-351). See P-03.

hand_result frame (C236-250, 339; H886-901)
- failure_reason/secondary_failures EXCL C237; accounting_complete `is True` C238 (1 -> EXCL);
  evidentiary `is False` C238; complete `is True` C240; interrupted_response_count exact 0 C241
  (False/0.0 -> EXCL); preparation/post_terminal seconds `type is float` finite >= 0 C242-243
  (0 int -> EXCL; -0.0 admitted by both, H642 same); rank_source vs replayed showdown EXCL
  C339-340; settlement mismatch with outer EXCL C247-250, with replay EXCL C300-302.

session_result frame (C236-246; H902-912)
- status 'failed' EXCL C244; accounting_scope EXCL C245; terminal_publication_compute_seconds
  None/int/NaN EXCL C246; accounting_complete/evidentiary EXCL C238; failure fields EXCL C237.

Caller inputs (not wire): board unsorted EXCL C315; private_hands overlapping board/duplicate
cards -> SixSeatHoldemDeal ValueError, raised OUTSIDE the try (C316) -> propagates to the caller
rather than returning an excluded result (unchanged since parent; caller-owned exact values).
strategy is never cross-checked against ready.protocol (carried advisory F02-01/F-03): v2 frames
under 'blueprint-v1' can reach at most 'disagreement' because v2 records carry no
blueprint_sha256 member (C367).

## 6. Candidate findings (severity-ordered)

### P-01 Important (medium confidence) - unknown v1 selection_reason is host-refused but credited

Location: C72-73 (`type(record['selection_reason']) is str`), C87 (constructed with
SelectionReason.PASSIVE_DEFAULT), C345 (chip_eligible=True), C367-369 (disagreement only).
Host oracle: H809 `SelectionReason(value['selection_reason'])` inside try H806-812 raises
ValueError -> HostRefusal('protocol_invalid'); enum members are exactly 'table_hit' and
'passive_default' (M60-62). The hand fails; status 'failed', settlement None (H992-995).
Mutated bytes: in the decided v1 event_result frame replace `"selection_reason":"table_hit"`
by `"selection_reason":"table_hit "` (or "TABLE_HIT", "", "blueprint_hit"); re-encode base64;
keep the outer envelope as captured.
Falsifying observation (static trace): frames_for admits the record (C73 str), DecisionRecord
is constructed with the substituted default (C87), classify sets chip_eligible=True, chips=<the
settled value>, agreement_eligible=True when the river key matches (C379), classification
'disagreement' with cause 'agreement:lookup_reason_or_identity_mismatch'; summarize counts
completed=1 and agreement_eligible=1. The host would never complete this hand.
Conflict of authorities, stated honestly: brief.md ("reason-only disagreements ... retain their
previous outcomes and settled chips"), checks/parent-disposition.md ("Preserve v1 unknown string
reason disagreements") and checks/parent-repair-plan.md step 3 ("Preserve the accepted
reason-label exception at the later agreement layer") direct exactly this behaviour. Under this
round's host-equivalence standard it is nonetheless a host-refused capture receiving chip and
agreement-eligibility credit. This needs an explicit ruling rather than silent carriage: either
re-ratify the carve-out against the host standard, or apply the smallest correction.
Smallest correction: at admission require `record['selection_reason'] in
tuple(SelectionReason)` (construct `SelectionReason(value)` as the host does) and keep the
existing agreement-layer cross-check for the two legal labels.

### P-02 Important (medium confidence) - v1 host state_mismatch / action-placement rules are
### re-derived only at the agreement layer, after chip credit

Location: C359 (`replayed['fields']` equality), C367 (blueprint_sha256), C353 (record count),
C212-214/230 (action frame shape and record equality only); credit at C345.
Host oracle: H815 `require(all(value[k] == v ...), 'state_mismatch')` over hand_id,
event_index, action_index, street_action_index, seat, street, state_before_sha256,
visible_cards_sha256, blueprint_sha256, selected_action, state_after_sha256 (H832-843);
H826-830 action frame action_index == bot_index+1, seat == controlled seat, street == current
street; H679/H825 an action frame is read only when the table expects one.
Mutated bytes (each alone, in the decided v1 river event_result frame and, where paired, the
preceding action frame so that C230 still holds): `"street_action_index":1` -> `:2`;
`"state_before_sha256":"<64 hex>"` -> 64 zeros; same for state_after_sha256,
visible_cards_sha256, blueprint_sha256; `"action_index":1` -> `:2` in both frames;
`"seat":2` -> `:3` in both frames.
Falsifying observation (static trace): DecisionRecord accepts each (shape only, M466-476);
chip_eligible=True and chips credited (C345); agreement_eligible=True whenever the replayed
river key matches (C379 uses the replay, not the record); classification 'disagreement'
(C359 -> 'agreement:replayed_state_mismatch' or C367 -> 'lookup_reason_or_identity_mismatch').
summarize: completed=1, agreement_eligible=1, disagreements=1, complete=False.
Design note: accepted-design s.5 describes hash/state cross-checks and duplicate river records
as agreement diagnostics, so this is a standard-versus-design tension, not a regression of
r003; the changed bytes do not touch it. Under the host-equivalence standard it is still
chip and agreement-eligibility credit for a capture the host refuses with state_mismatch or
protocol_invalid.
Smallest correction: in frames_for, after replay is available (or by moving the replay
before the agreement stage), require record field equality with the replayed expected
fields for the host's expected set and the action-frame placement, raising Unusable
('wire:state_mismatch'); keep selected_action-vs-teacher and table_hit-vs-reason as the
agreement-layer observations the design wants.

### P-03 Important (medium-high confidence) - v2 records skip every host state/legality rule
### and receive chip credit with no diagnostic

Location: C56-64 (v2 branch checks only identity, delivery and timing), C349-351 (returns
'unsupported', chip_eligible=True, no cause), summarize C411 (unsupported does not block
complete=True).
Host oracle: H761-785: apply fallback_action and selected_action to the context state
(illegal -> protocol_invalid), equality with provider_expected (H748-758: hand_id, event_index,
action_index, street_action_index, seat, street, state_before_sha256, visible_cards_sha256,
decision_sha256, source_manifest_sha256, provider, config_sha256, fallback_blueprint_sha256,
fallback_action, fallback_reason, selected_action, applied_action) -> state_mismatch; proposal
validity vs provider_outcome H772-781; state_after_sha256 H782-785.
Mutated bytes (each alone, in a decided v2 event_result frame of the actual baseline capture):
`"fallback_reason":"passive_default"` -> `"table_hit"`; `"state_before_sha256"` -> 64 zeros;
`"street_action_index":1` -> `:7`; for an origin 'provider' record `"fallback_action":
{"kind":"check","raise_to":null}` -> `{"kind":"fold","raise_to":null}` (validate_decision
still passes: selected == proposal action, C94-96 of the codec); `"decision_sha256"` and
`"proposal":{"decision_sha256":...}` both -> 64 zeros.
Falsifying observation (static trace): validate_decision accepts each (labels and internal
consistency only); C58-64 pass; classify returns chip_eligible=True, chips credited,
classification 'unsupported', causes ['agreement:baseline_outside_declared_root'];
summarize reports completed=1, unsupported=1, complete=True. The host would refuse every one
(state_mismatch or protocol_invalid) and the hand would not complete.
Scope note: the frozen Slice A worker never plays v2 (play() fixes 'blueprint-v1'); the only
v2 consumer is the r003 test. The design names v2 chips as a Slice B interface, which is
exactly where this credit path will be consumed.
Smallest correction: for v2 records, replay the controlled decision through PreparedBlueprint
(fallback_action/fallback_reason), require the host's provider_expected equalities that the
retained envelope can reproduce (indices, seat, street, state hashes, visible-cards hash,
fallback identity/action/reason, applied == selected, state_after), and apply
selected_action legality through the kernel replay before chip_eligible.

### P-04 Important by the stated standard (medium confidence) - the host's 65536-byte stderr cap
### is not mirrored

Location: C183-187 read only child_stdout_base64; child_stderr_base64 is never decoded or
bounded; C334 relies on the envelope's capture_truncated flag.
Host oracle: H513 `cap = 65536` for stderr; H523-527 any chunk beyond it sets truncated and
raises transport_failed; H624-625 re-adds the failure at finish; the hand fails.
Mutated bytes: hand['child_stderr_base64'] = base64 of 65537 bytes (e.g. 'x'*65537),
capture_truncated left False, everything else the actual capture.
Falsifying observation (static trace): classification unchanged ('hit' for the CHECK
control), chip_eligible=True, complete=True. The unchanged host marks such a child truncated
and refuses.
Parity argument: r003 added the 2097152 stdout bound (C185) for exactly this reason; the
stderr bound is the same read_stream mechanism and the same retained flag. brief.md names
"retained stdout/frame byte bounds", so the coordinator may judge stderr outside r003's
scope; it remains a host size limit the classifier does not enforce.
Smallest correction: `require(len(b64decode(hand['child_stderr_base64'], validate=True))
<= 65536, 'wire:stderr_capture_size')` beside C185.

### Carried advisories (disposed in the parent; restated only so they are not lost)

- P-05 Advisory: session/child identity charset and length (session.py 205, adapter 321,
  H943) are not checked; consistent but out-of-regex ids are admitted (parent F-04/C4 class).
- P-06 Advisory: summarize.complete ignores 'unsupported' (C411); the frozen worker requires
  every primary to be 'hit' (completion tool 347, 409-410), so this is outcome resolution only.
- P-07 Advisory: strategy is not bound to ready.protocol (parent F02-01/F-03); no hit is
  reachable from the mismatch, but the label is caller-asserted.
- P-08 Advisory: source_manifest_sha256 is shape-checked only (C175-180); admission owns it.
- P-09 Advisory: SixSeatHoldemDeal construction at C316 is outside the try; an invalid
  caller deal raises instead of returning an excluded result. Caller-owned values; no credit.

## 7. Closed members (attacks the frozen source refuses correctly, with the refusing line)

Byte level: A1-A9, A11, A13-A20, A22-A27 above (C122, 124, 138, 143, 105, 111, 116, 147,
185, 186, 189-191). Parsed level: ready evidentiary (C197), protocol/type/field sets (C193,
201, 205), identity equality and hex shapes (C165-180, 195-196), event_index type/order/count
(C219, 338), status/failure (C221), decision/action pairing (C211, 224-225, 235), action frame
counters (C212-213) and action shape (C49, M141-147 via C215), frame action vs record (C232),
v1 record field set (C66), preparation fields/values (C68-71, exact_integer refuses True/0.0),
timing fields/status/flags/ints/seconds/elapsed/sum (C74-82, M401-422), spine_reason (C84,
M481), decision hashes/indices shape (M464-476), failure_reason (C55), v2 validate_decision
(C57), v2 identity/delivery (C58-64), hand_result closure and counters (C237-243, exact
`is True`/`is False`/exact 0/float), rank_source (C339), settlement equality (C247-250,
300-302), session_result (C244-246), outer session/hand/entry gates (C322-335, 255-258,
262-275, 292), replay illegal action (C275 kernel ValueError), board order (C315). Every (c)
attack (False/0, True/1, 1.0/1) on an integer or boolean member is refused: the classifier
uses exact_integer, `type is int/float/bool` (through the dataclasses) or `is True/False`, and
compares settlements by json.dumps, which distinguishes 1, 1.0 and true.

## 8. Reconciliation with coverage.md, the receipts and the parent findings

- Parent I-01 (framing): closed completely at the byte level, not only for the four
  finalizer examples. decode_frame reproduces decode_json predicate for predicate (size incl.
  LF, CR, BOM, depth <= 8 with the same quoted/escaped scanner, 640 signless digits, duplicate
  keys, constants, strict UTF-8, RecursionError), frames_for splits only on byte 10 and
  enforces the 2097152 capture bound and final LF. My independent A-table found no separator,
  size, depth, encoding, duplicate or closure case where the host refuses and the classifier
  credits. The only divergence is the deliberate stricter finite-float rule (A21), which
  cannot over-exclude a host-completed hand.
- Parent F-02 (RecursionError escaping exclusion): closed at C150-151 and C138.
- coverage.md's five-stage category matches my inventory sections 4.4-4.7. Its stated limits
  are accurate: the 2 MiB test variant also exceeds the per-frame bound; the decoder oracle
  test exercises the helper directly; no natural corrupted capture is claimed.
- Coverage gaps (not product defects by themselves): no real-capture mutation for an inserted
  empty frame, an extra frame after session_result, a NUL byte, depth 9 inside a real
  capture, or a stderr over the cap; the decoder-level tests cover empty/depth. P-01..P-03
  are parsed-level classes outside r003's declared scope and are not exercised by any test.
- The parent finalizer's four executed mutations (CRLF, U+001E, U+2028, oversized ready
  frame) appear verbatim in the r003 matrix (CRLF, separator_30, separator_8232,
  frame_over_limit); RED shows them failing on the parent source and GREEN passing on 7ca82180.

## 9. Receipts assessment (implementer evidence assessed, not reproduced)

- RED: refs/heads/check/.../r003-red = 81a5aaf5 verified as parent + the candidate's exact test
  blob (section 1). red-journal: source_verified true, 3.14.6, pytest exit 1, "2 unittest
  cases; 0 skipped". red-stdout lists 27 failures = 13 framing variants x 2 strategies (26) +
  test_raw_decoder_matches_frozen_host_boundaries (missing seam), matching coverage.md.
  Schema-mutation subtests do not fail on the parent, consistent with the parent disposition
  that member/coercion cases were already closed.
- GREEN: focused-receipt/result bind candidate 7ca82180, snapshot worktree, .venv 3.14.6,
  exit 0, scrubbed environment (SystemRoot, TEMP, TMP, PONTIUS_GIT, PYTHONDONTWRITEBYTECODE),
  -B -P -W error::ResourceWarning, -p no:cacheprovider; six suites 11+29+8+21+9+2 = 80 cases,
  0 skipped; journal source_verified true, source_commit 7ca82180. focused-stderr and
  red-stderr are empty (e3b0c442...).
- freeze-r003.py builds the tree from the worktree files with CR/column/trailing-space
  assertions and create-only update-ref (old value 0*40); snapshot.ps1 refuses an existing
  snapshot, syncs --locked --offline, asserts the interpreter version with -I, clears the
  environment. Both are utilities, not sealed producers; they were not executed by me.
- Limits: static verification only on my side; no project code was run. The receipts show
  the test matrix passes; they cannot show host-equivalence beyond the cases enumerated, which
  is why the A-table above was derived from the frozen host bytes rather than from the tests.

## 10. Line counts and hygiene (raw frozen bytes; reviewer arithmetic)

- eval_agreement.py: 21402 bytes, 411 lines (371 non-blank); parent 378 lines; delta +37/-4.
- test_eval_protocol.py: 13127 bytes, 218 lines (208 non-blank); parent 137; delta +81/-0.
- Both blobs LF-only, no CR, no BOM, no tab, no line over 100 columns, no trailing whitespace,
  final LF present. checks/scope.json reports whole-slice production 2093 / test 1999 lines:
  under the 3000 ceiling, over the disclosed 1200/600 working figures.

## 11. Verified boundaries, limits and evidence limits

- Verified from frozen bytes: byte-level host equivalence (A-table), the exact member sets of
  ready/action/event_result/hand_result/session_result, the 16-member v1 record, 10-member
  timing, 3-member preparation, 27-member v2 record, settlement, and the outer envelopes.
- Not verified: runtime behaviour (no execution), host transport timing (queue depth 8,
  60 s/300 s deadlines) which retained bytes cannot expose, OS containment, and anything
  about the sealed kernel/codec beyond the exception surfaces read.
- Stdlib probes (json.loads whitespace, non-LF separators, 1e400 -> inf, -0, BOM, ED A0 80,
  bytes.split parity) were run with the utility interpreter only; reviewer arithmetic.

## 12. Design observation (prosecutor's view, not a verdict)

At the raw boundary the shape is SOUND: one decode_frame that is textually the host's
decode_json, called on the host's physical partition. Overall the classifier remains
STRAINED in the same way the parent finalizer named: admission is split across three layers
(byte, typed shape, then agreement) and the third layer runs after chip credit, so any host
rule that lives in WireConsumer.decision/exchange rather than decode_json (P-01..P-03) is
re-derived only as a disagreement or not at all. The change that would stop the recurrence
is a single replay-before-credit step: derive the host's expected record for each controlled
decision from the replayed state and require equality before chip_eligible, leaving only
teacher/reason semantics to the agreement layer.

## 13. Prohibitions and exposure statement

- Did not open D:/Pontius-handoffs/v0a-eval-panel-completion/r003/reviews/ or any reviews/
  directory (its name appeared in a directory listing of the packet root; not entered).
- Did not open any other packet, progress.md, INDEX.md, disposition/readiness files outside
  this packet's checks/, any transcript, session log or other reviewer's scratch. Did not list
  D:/Pontius/tmp; created only D:/Pontius/tmp/eval-completion-r003-prosecutor-3354fe13/
  (uuid4 suffix, exclusive mkdir) and wrote exactly two files there: this report and the
  inventory. No other scratch files; all utility scripts ran from stdin.
- Ran no project code, tests, tools, hooks, uv or pip. Git use was read-only: rev-parse,
  cat-file, diff-tree, diff, for-each-ref. No writes under D:/Pontius or D:/Pontius-handoffs.
  Utility work used C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe only.
- Exposure disclosures: (1) `git for-each-ref` output listed names of refs belonging to other
  tasks and rounds (names only, no content read); (2) the harness's inherited context carried
  a git status snapshot (STATUS.md and execution_journal.jsonl modified in the working tree)
  and five recent commit subjects; identity context only, no candidate findings, verdicts or
  lane history; (3) the harness persisted large tool outputs (allowed inputs and frozen blobs)
  to files under C:/Users/point/.claude/projects/... outside my scratch directory; I read only
  those copies of allowed content; (4) coverage.md was hashed before the inventory without
  displaying it and opened only afterwards, together with checks/.
- No output-policy deviation: LF-only, BOM-free, <= 100 columns, no trailing whitespace.
- Working tree source of D:/Pontius was never read; all source came from cat-file at 7ca82180.
