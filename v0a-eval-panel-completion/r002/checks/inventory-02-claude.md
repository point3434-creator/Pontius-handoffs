# Inventory 02 (Claude, reviewer 02): v0a-eval-panel-completion/r002

Candidate 430ad75de79cec13d66ff3dc4981dd3770a371b7, sole parent
449a2a3c1fa1f5a7f5f04adca32e499faaf81e13, tree c531d0b93520cd69704aa14842cea32d5b31ca51,
manifest 6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5.
Written from requirements and raw frozen Git source only, before coverage.md or any
checks/ file was opened. Line numbers cite 430ad75d:<path>.

## 1. Requirement sources and obligations (top-down)

R1 r002 brief: changed surface is exactly eval_agreement.py, test_eval_protocol.py,
   cases.json; everything else byte-identical to 449a2a3c.
R2 r002 brief: missing/malformed protocol receives neither chip nor hit credit.
R3 r002 brief: well-formed v1 unknown/relabelled selection reasons stay chip-eligible
   disagreements; valid completed baseline (v2) divergence keeps chips.
R4 r002 brief: compatibility keeps CHECK hits, off-pool defaults, retained failures.
R5 r002 brief: correction limited to raw schema admission before typed construction
   and exact successful metadata; no solver/export/host/session/codec/ownership/timing
   change. Whole Slice A production below 3000 lines.
R6 Completion brief item 7: outcome eligibility precedes agreement eligibility;
   nullable failures, malformed frames, truncation, missing settlement are excluded;
   replay applied history; reconcile real keys/reasons/actions; keep prefix-diverged
   baseline chips.
R7 Completion brief items 4/8, accepted brief 5, 7, 8, design 5: exactly one controlled
   river record for agreement; cross-check table_hit against the v1 reason; wrong action
   or in-pool default is disagreement; off-pool default is unsupported; non-passive
   pre-river reason is disagreement; changed stack/prefix yields zero hits; relabelled
   CHECK hit/default is detected by the reason cross-check; provider labels never stand
   in for v1 selection_reason.
R8 Design 5 counters: scheduled, missing, completed, agreement-eligible, hits,
   disagreements, unsupported, excluded; exactly one disposition per attempt; final
   acceptance needs complete coverage, no disagreement, no unresolved exclusion.
R9 Tier C invariant (accepted brief, completion brief): every reported agreement is
   attributable to a completed real host decision, the declared teacher and the exact
   exported key; missingness, defaults and failures never become hits.
R10 Workflow checklist 10/11: exactness (type(x) is int / is bool) in evidence paths;
    LF, no BOM, at most 100 columns, no trailing whitespace; identity recomputed from
    frozen blobs.
R11 Design 6 and brief: tests registered only through tests/cases.json; constructed
    envelope fixtures test the classifier only; real host controls establish interfaces.

## 2. Producer -> consumer paths of every value the classifier reports

Producers of the retained report (all unchanged at 449a2a3c, verified byte-identical):
- tools/v0a_event_adapter.py PipeOutput.frame (188-192): child frames ready, action,
  event_result, hand_result, session_result; v1 decisions via
  pontius.v0a.trace.decision_payload (216-236), v2 via decision_provider.codec
  decision_payload (23-41).
- tools/v0a_table_host.py ChildConnection.read_stream (512-537) captures child stdout
  (2 MiB cap, truncated flag); WireConsumer (645-913) validates frames live.
- tools/v0a_table_session.py Session.play_hand (233-315) builds the hand entry
  (ordinal, button, starting_stacks, result); Session.run (317-361) the outer report.
- tools/v0a_eval_panel_completion.py play (282-311) runs one Session and calls
  eval_agreement.classify with blueprint=decode_blueprint(wire), teacher_actions,
  board and private_hands from the witness, stacks; strategy defaults to blueprint-v1.

Consumers of the classify result:
- completion.agreement (345-366): primary attempts require classification 'hit';
  off-pool control requires chip_eligible and 'unsupported'; check-hit requires 'hit';
  changed-stack requires chip_eligible and observed_table_hits == 0.
- completion.complete (403-416): the same predicates over JSON-roundtripped
  observations.
- completion.accounting (439-463) and eval_agreement.summarize (364-378): counts by
  classification, chip_eligible, agreement_eligible; complete means no missing, no
  disagreement, no excluded.
- tools/v0a_eval_panel.py worker (518-528): phase_complete and agreement_accounting
  enter the run result; status is forced to failed when phase_complete is false.
- tests: test_eval_agreement.py, test_eval_completion_tool.py, test_eval_protocol.py.

Result members: chip_eligible (bool), chips (int or None), agreement_eligible (bool),
classification in {hit, disagreement, unsupported, excluded}, causes (list of str),
river_hand (str), observed_table_hits (int or None), river_records (int or None).

## 3. Nested schema the classifier consumes (member: required type/value; where)

Outer session report (classify 289-297, bind_identity 120-146):
- failure_reason: None (clean); secondary_failures: exact list equal to [] (clean 94).
- status == 'completed'; stop_reason is None (290-291).
- requested_hands: exact int 1; completed_hands: exact int 1 (292-293).
- hands: exact list of length 1 (294); hands[0].ordinal: exact int 1 (297).
- version == 'pontius-v0a-table-session-result-vN'; session_id: str starting with
  'pontius-v0a-table-session-vN-correctness-' (123-125).
- source_commit, blueprint_artifact_sha256, blueprint_sha256 equal to ready's
  (131-132); v2 also provider and config_sha256 equal to ready's (135-136).
- Not inspected: input_sha256, next_button, carried_stacks, extra keys.

Hand entry hands[0] (replay 222-225): button exact int 0; starting_stacks exact list
of six exact ints equal to stacks; result: dict (clean).

Nested hand result (classify 298-302, frames_for, replay):
- failure_reason None; secondary_failures exact []; status == 'completed'.
- capture_truncated is False; child_exit_code exact int 0 (301-302).
- child_stdout_base64: strict base64, nonempty, LF-terminated (150-151).
- blueprint_sha256 == PreparedBlueprint(blueprint).digest (162-163).
- version, session_id, source_commit, blueprint_artifact_sha256 per bind_identity;
  v2 provider and config_sha256 (127-136).
- settlement: not None; JSON-canonical equal to terminal.settlement (214-217) and to
  the kernel settlement replayed from applied_actions and the caller's deal (267-269).
- applied_actions: exact list; each row exact fields {index, seat, street, action,
  origin}; index exact int equal to position; seat exact int equal to the kernel's
  acting seat; street equal to the kernel street name; origin 'bot' iff seat 2; action
  exact {kind, raise_to} admitted by HandAction (229-241); an illegal action raises in
  the kernel.
- Not inspected: input_sha256, child_stderr_base64.

Frame stream (frames_for 150-174): each line JSON with unique keys, no NaN/Infinity,
finite floats; every frame a dict; at least three frames; frames[0].type 'ready',
frames[-2] 'hand_result', frames[-1] 'session_result'; every frame has exactly
protocol, session_id, type plus WIRE_FIELDS[type] (v2 ready adds provider and
config_sha256); all frames share a protocol in {v1, v2 event interface} and the
nonempty str session_id.

ready: source_commit hex40, source_manifest_sha256 hex64, blueprint_artifact_sha256
hex64 (141-146); blueprint_sha256 == digest (162); evidentiary is False (164);
session_id == protocol + '-correctness-table-' + suffix (129); v2: provider ==
'baseline-rules-v1', config_sha256 hex64 (134-139).

action frame: action_index exact int >= 1; seat exact int 0..5 (179-181); action exact
{kind, raise_to} via HandAction (182); hand_id and street only by equality with the
paired decision (197-199); exactly one pending action per decided event (178, 192,
202).

event_result frame: event_index exact int equal to the running count (186-187); status
in {accepted, decided}; failure is None (188-189); decision None iff accepted (191);
decision present iff an action frame is pending (192).

v1 decision (admitted_decision 66-87): exact field set equal to the 16 DecisionRecord
fields; failure_reason None; preparation_use exact {producer_status ==
'producer_absent', artifact_sha256s exact list equal to [], credited_seconds exact int
0}; selection_reason exact str (any value); timing exact 10-member TimingRecord field
set; TimingStatus valid; TimingRecord construction: status COMPLETED,
interruption_reason None, wall_start_ns, last_valid_observation_ns,
emission_observed_ns, elapsed_ns exact ints with exact subtraction, seconds exact
finite nonnegative floats, flags exact bools; classifier adds not cutoff, not
deadline, elapsed <= 15e9, compute plus uninstrumented within 2e-9 of elapsed/1e9;
DecisionRecord construction (selection_reason overridden to PASSIVE_DEFAULT): hand_id
nonempty ASCII, event_index exact int >= 0, action_index and street_action_index
exact int >= 1, seat 0..5, street name, four hex64 digests, selected_action
HandAction, spine_reason in SPINE_REASONS. Then event_index equals the frame's,
hand_id equals session_id (195-196); hand_id, action_index, seat, street and action
equal the pending action frame (197-199).

v2 decision: decision_provider.codec.validate_decision (44-137): exact 27 keys,
labels, exact ints, digests, actions, proposal/outcome/reason/origin consistency,
timing via trace._validate_timing, preparation absence, failure/timing consistency;
classifier adds provider, config_sha256, source_manifest_sha256 equal to ready's and
fallback_blueprint_sha256 equal to ready.blueprint_sha256 (58-61), delivery accepted
with delivered == applied == selected (62-64), timing as for v1 (74-82).

hand_result: failure_reason None, secondary_failures []; accounting_complete is True;
evidentiary is False; complete is True; interrupted_response_count exact int 0;
preparation_compute_seconds and post_terminal_compute_seconds exact finite float >= 0;
settlement JSON-equal to hand.settlement; rank_source == 'host_supplied' iff the
replayed terminal is a showdown, else 'not_required' (306-307).

session_result: failure_reason None, secondary_failures []; accounting_complete True;
evidentiary False; status == 'completed'; accounting_scope ==
'runtime_begin_to_final_publication'; terminal_publication_compute_seconds exact
finite float >= 0.

Event-count binding: the number of event_result frames equals the replayed final event
index plus one (305); replay counts opponent actions, street advances and one showdown.

Caller inputs (trusted, in-process): blueprint exact ImmutableBlueprintActionSource;
teacher_actions dict name -> BettingAction; board sorted tuple; private_hands via
SixSeatHoldemDeal (six distinct two-card tuples disjoint from the board); stacks;
strategy label. strategy is not bound to the retained protocol version.

## 4. Agreement derivation (classify 311-361)

records = all decisions in event order; observed_table_hits and river_records count
raw selection_reason and street strings. strategy other than blueprint-v1 gives
unsupported, chip-eligible, cause baseline_outside_declared_root. Otherwise: decision
count must equal the replayed bot-action count; each record's event_index,
action_index, street_action_index, seat, street, state_before/after and
visible_cards digests must equal the independent replay; the selected action must
equal the applied action and the classifier's own PreparedBlueprint.action_for
result; record blueprint_sha256 must equal the prepared digest and selection_reason
must equal the recomputed table_hit/passive_default; pre-river records must be
passive_default; exactly one river record; agreement_eligible iff its key equals
root_key(replay_root(), board, hero) at s=4; hit only when the teacher has the hand,
the lookup is a table hit, the applied action equals the teacher action and no cause
was recorded; otherwise disagreement (in-pool default, wrong action, hit outside pool
or root) or unsupported (off-pool default, changed root without a hit).

## 5. Failure cases (expected classification)

Excluded (chip_eligible False, chips None): outer or nested failure_reason not None or
secondary_failures not []; status not completed; stop_reason set; requested or
completed hands not exact 1; hands not a one-element list; ordinal not exact 1;
result missing or not a dict; capture_truncated not False; child_exit_code not exact
0; base64 invalid; stream not LF-terminated; duplicate JSON keys; NaN, Infinity or
nonfinite floats; frame not a dict; fewer than three frames; wrong terminal or closure
types; unknown protocol; blueprint digest mismatch in ready or hand; ready
evidentiary not False; identity prefix/suffix mismatch across report, hand and ready;
digest shape errors; frame field-set mismatch; mixed protocol or session_id; unknown
frame type; duplicate or unpaired action; non-exact action_index or seat; bad action
object; event_index gap or non-int; failed or unknown event status; non-null failure;
decision/status/pending inconsistency; v1 decision field-set mismatch (including v2
members such as delivery_status); preparation not the exact honest absence; non-str
selection_reason; timing field-set or type errors; interrupted or cutoff/deadline
crossed timing; elapsed over 15 s; seconds not partitioning elapsed; DecisionRecord
type or range failures; v2 validate_decision failures; v2 provider, config, manifest
or fallback digest not bound to ready; v2 delivery not accepted; decision identity or
action mismatch with the action frame; hand_result or session_result unaccounted,
failed, incomplete, evidentiary, wrong scope or status, or non-float seconds;
non-exact interrupted_response_count; settlement missing or JSON-different between
hand, frame and kernel replay; button or starting_stacks not exact; applied_actions
not a list, or a row with wrong fields, order, seat, street, origin or illegal action;
replay not terminal; event count mismatch; rank_source mismatch.

Disagreement (chip-eligible): decision count differs from applied bot actions;
replayed field mismatch; selected action differs from the applied or lookup action;
wrong blueprint digest in a record; selection_reason differs from the recomputed
reason (relabelled hit, in-pool default, unknown label); non-passive pre-river reason;
zero or duplicate river records; table hit outside the teacher pool or the declared
root; teacher disagreement.

Unsupported (chip-eligible): baseline strategy; off-pool passive default at the
declared root; changed stack or prefix without any hit.

Missing (summarize): scheduled minus observed; blocks complete.

## 6. Places the invariant must hold that I will check against coverage

C1 every exact-integer metadata member above; C2 every 'is True' / 'is False'
boolean; C3 v1 decision and preparation field sets; C4 selection_reason type versus
label; C5 v2 record binding to ready and outer identities; C6 action frame counters
and action object; C7 applied_actions row shape; C8 timing field set; C9 settlement
exactness through JSON text; C10 strategy/protocol coupling (not enforced); C11
event-count and showdown numbering for fold, showdown and all-in terminals; C12
splitlines leniency (CR and Unicode separators) versus host LF-only framing; C13
caller-input admission (stacks type, teacher value types); C14 test registration and
hygiene; C15 whole-slice line totals (2060 production, 1918 test, counted from blobs).
