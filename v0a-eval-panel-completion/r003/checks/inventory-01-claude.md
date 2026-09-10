# Inventory 01 (Claude, review-01): v0a-eval-panel-completion/r003

Written BEFORE opening coverage.md or any checks/ file. Derived only from
handoff.md, candidate.json, manifest.sha256, brief.md, supporting-files.json,
inputs/ and raw frozen Git blobs at 7ca821802c949b047becf6599d603b3b63d51fa7.

Candidate 7ca821802c949b047becf6599d603b3b63d51fa7, sole parent
430ad75de79cec13d66ff3dc4981dd3770a371b7, tree 3d2fe79d2af20125e322dd4a668335e789810863,
manifest 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd (two rows:
src/pontius/eval_agreement.py, tests/test_eval_protocol.py).

## 1. Governing obligations (from brief.md, accepted brief/design, completion brief)

O1  Host-equivalence of admission: any retained child_stdout byte sequence that the
    unchanged host (tools/v0a_table_host.py: ChildConnection.read_stream framing and
    WireConsumer.read -> decode_json(code='protocol_invalid', digits=640, floats=True))
    would refuse must be excluded by classify() before any chip or hit credit.
O2  Scope of this FIX: physical LF framing, capture/frame byte bounds, CR/BOM, JSON
    depth and integer-digit limits, duplicate keys, decoding/parser failures. The
    classifier's finite-number restriction stays (stricter than host floats=True).
O3  Unchanged outcomes: valid v1 CHECK hits, off-pool defaults, reason-only
    disagreements, completed v2 baseline divergence keep prior classification/chips.
O4  Two separate gates (design s5): outcome/chip eligibility first (session, hand,
    frames complete and host-valid, settlement replayed), agreement second; an
    agreement failure must not remove chips; failures/defaults/missingness never
    become a hit.
O5  Exactly two files changed; no host/session/codec/model change; Python 3.14.6 only;
    whole-slice production ceiling 3000 lines; LF/BOM-free/<=100 cols/no trailing ws.
O6  Tier C lens: teacher identity, exported membership, retained-outcome
    interpretation cannot manufacture agreement from missingness/defaults/failures.

## 2. Producer -> consumer paths of the retained capture

P1  tools/v0a_event_adapter.py PipeOutput.frame(): json.dumps(sort_keys, compact,
    allow_nan=False) + '\n', UTF-8, one os.write per frame to the child's stdout.
    Frame kinds: ready, action, event_result, hand_result, session_result.
P2  tools/v0a_table_host.py ChildConnection.read_stream(stdout=True): 4096-byte
    chunks; capture cap 2097152 bytes total (over -> truncated, transport_failed);
    frames split on byte 0x0A inclusive; frame size (incl. LF) <= 16384; residual
    after each chunk < 16384; at EOF residual must be empty. Frames queue depth 8.
P3  WireConsumer.read(): raw is bytes and ends with LF; decode_json: bytes,
    0 < len <= 16384, no 0x0D anywhere, no leading EF BB BF, bracket depth <= 8
    counted outside strings with backslash escapes, strict UTF-8, json.loads with
    parse_int digits <= 640, parse_float=float (non-finite accepted), NaN/Infinity
    rejected, duplicate keys rejected, ValueError/TypeError/RecursionError -> refuse.
    Then: dict, type str in WIRE_FIELDS, exact member set (+provider config_sha256
    for v2 ready), protocol == expected, session_id == child_id.
P4  Sequence: ready; per host event: [action if bot to act] event_result;
    hand_result; session_result; then receive() must return EOF (None).
P5  tools/v0a_table_session.py play_hand(): host runs IN PROCESS (Admission execs
    the host module); hand result retains child_exit_code, child_stdout_base64 =
    b64(connection.stdout), child_stderr_base64, capture_truncated; status completed
    only if no failures, exit 0, not truncated, settlement provisional.
P6  tools/v0a_eval_panel_completion.py play(): Session(args).run() -> classify(result,
    blueprint=decode_blueprint(wire), teacher_actions, board, private_hands, stacks).
    agreement(): 'hit' required for every primary; controls off-pool/check-hit/
    changed-stack; summarize() over primaries only.
P7  src/pontius/eval_agreement.py classify(): clean(session) -> hands[0].result ->
    frames_for() (byte + frame admission) -> replay() (kernel settlement) -> chips;
    then agreement over decoded decision records (blueprint-v1 only).

## 3. Byte-level admission schema the classifier must enforce (host oracle)

B1  hand.child_stdout_base64: str, strict base64 (validate=True). Host: bytes come
    straight from the pipe, so any non-alphabet char is a fabrication -> exclude.
B2  0 < len(raw) <= 2097152. Host read_stream cap (exactly 2097152 accepted).
B3  raw ends with 0x0A (host: empty residual at EOF).
B4  Split on 0x0A only (NOT str.splitlines: no CR, VT, FF, FS, GS, RS, NEL, LS, PS).
B5  Each frame incl. LF: 0 < len <= 16384.
B6  No 0x0D anywhere in a frame; no EF BB BF prefix.
B7  Depth of unquoted [ { <= 8 (byte scan with escape handling identical to host).
B8  Strict UTF-8 (surrogates/overlong/invalid -> refuse).
B9  json.loads strict: one value per frame, no control chars in strings, no leading
    zeros, ints <= 640 digits after '-', NaN/Infinity/-Infinity rejected, duplicate
    keys rejected at any nesting, finite floats only (classifier-stricter, allowed).
B10 Every frame a dict; >= 3 frames; frames[0].type == ready, frames[-2].type ==
    hand_result, frames[-1].type == session_result, nothing after (host EOF rule).
B11 Empty frame (b'\n'), whitespace-only frame, top-level array/scalar -> refuse.

## 4. Nested parsed schemas consumed by classify (member: required type/value)

S1 session_report (outer, v1 'pontius-v0a-table-session-result-v1' / v2 '-v2'):
   version str exact; session_id str startswith 'pontius-v0a-table-session-vN-
   correctness-'; status == 'completed'; stop_reason None; failure_reason None;
   secondary_failures list == []; requested_hands exact int 1; completed_hands exact
   int 1; hands list len 1; source_commit == ready == hand; blueprint_artifact_sha256
   == ready == hand; blueprint_sha256 == ready == hand == blueprint.digest;
   v2: provider == 'baseline-rules-v1' (via ready) == hand == report, config_sha256
   64 lowercase hex == ready == hand == report. Not consumed: input_sha256,
   next_button, carried_stacks.
S2 hands[0] entry: ordinal exact int 1; button exact int 0; starting_stacks list len
   6 of exact int == stacks; result dict.
S3 entry.result (hand): version 'pontius-v0a-table-session-hand-result-vN';
   session_id == 'pontius-v0a-table-host-vN-correctness-' + tail + '-h01'; status
   == 'completed'; failure_reason None; secondary_failures []; capture_truncated is
   False; child_exit_code exact int 0; child_stdout_base64 per B1-B11; settlement
   not None and canonical-JSON-equal to hand_result.settlement and to the replayed
   kernel settlement; applied_actions list of rows {index exact int == position,
   seat exact int == acting seat, street == state street, action {kind, raise_to}
   HandAction-valid and kernel-legal, origin 'bot' iff seat 2}. Not consumed:
   input_sha256, child_stderr_base64.
S4 frame common: protocol in {'pontius-v0a-event-interface-v1','-v2'} same on every
   frame; session_id nonempty str same on every frame and == protocol +
   '-correctness-table-' + tail + '-h01'; type in WIRE_FIELDS; member set exact.
S5 ready: source_commit 40 hex; source_manifest_sha256 64 hex (value NOT verifiable
   here; admission owns it); blueprint_artifact_sha256 64 hex; blueprint_sha256 ==
   blueprint.digest; evidentiary is False; v2 adds provider 'baseline-rules-v1',
   config_sha256 64 hex.
S6 action: hand_id == identity (via record equality); action_index exact int >= 1;
   seat exact int 0..5; street == record.street; action {kind,raise_to} valid.
   Must immediately precede a 'decided' event_result; no two in a row; none unpaired.
S7 event_result: event_index exact int == ordinal position (0..); status in
   {accepted, decided}; failure None; decision None iff accepted; decision present
   iff an action frame is pending.
S8 decision v1 (exact 16 members = DecisionRecord fields): hand_id == identity;
   event_index == row.event_index; action_index, street_action_index exact int >= 1;
   seat 0..5; street in STREET_NAMES; state_before/after, visible_cards, blueprint
   sha256 64 hex; selected_action HandAction == action frame's action;
   selection_reason str (ANY label; enum deliberately not enforced -> observable
   disagreement, O3); spine_reason in SPINE_REASONS; failure_reason None;
   preparation_use exact {producer_status 'producer_absent', artifact_sha256s list
   [], credited_seconds exact int 0}; timing exact 10 members: status 'completed',
   interruption_reason None, wall_start_ns/last_valid_observation_ns/
   emission_observed_ns/elapsed_ns exact ints (last == emission, elapsed == emission
   - wall_start, >= 0), response_compute_seconds/response_uninstrumented_seconds
   finite floats >= 0 with |sum - elapsed_ns/1e9| <= 2e-9, work_cutoff_crossed and
   deadline_crossed exact False, elapsed_ns <= 15_000_000_000.
S9 decision v2: validate_decision() member/label/consistency rules; plus provider,
   config_sha256, source_manifest_sha256 == ready; fallback_blueprint_sha256 ==
   ready.blueprint_sha256; delivery_status 'accepted'; delivered == applied ==
   selected; timing as S8. Agreement is never computed for v2 (strategy gate).
S10 hand_result: complete is True; settlement == hand.settlement (canonical JSON);
   rank_source == 'host_supplied' iff replay reaches showdown else 'not_required';
   evidentiary is False; preparation_compute_seconds, post_terminal_compute_seconds
   float finite >= 0; interrupted_response_count exact int 0; accounting_complete is
   True; failure_reason None; secondary_failures [].
S11 session_result: status 'completed'; terminal_publication_compute_seconds float
   finite >= 0; accounting_complete is True; failure_reason None; secondary_failures
   []; accounting_scope 'runtime_begin_to_final_publication'; evidentiary is False.
S12 count binding: number of event_result frames == replayed final event index + 1
   (hand_started, opponent actions, street reveals, showdown_result).

## 5. Host predicates the classifier cannot or does not mirror (limits to state)

L1  ready.source_manifest_sha256 equality with the run manifest (not retained in the
    session envelope; shape only).
L2  v2 provider identity config_sha256 recomputation from the blueprint (shape and
    cross-envelope equality only).
L3  Host 'state_mismatch' equality of record fields with the host's own expected
    values (event/action/street indices, state digests, blueprint digest): the
    classifier applies these only as blueprint-v1 AGREEMENT predicates (disagreement,
    chips kept), never for v2. Design s5 makes record-level anomalies agreement
    failures, so this is a designed divergence, not a byte-admission gap.
L4  Timing/queue refusals (frame queue depth 8, 60 s exchange, 300 s hand deadlines)
    are not byte-determined.
L5  stderr capture cap 65536 (child_stderr_base64 is not consumed).
L6  EVENT_LIMIT/ACTION_LIMIT 256 (unreachable under declared stacks 4/6 replay).
L7  Session id charset/length regexes (session-level input admission).
L8  hand.input_sha256 (not recomputed).

## 6. Failure cases to check on every path (both protocol versions)

F1  Byte-level: each of B1-B11 individually violated with otherwise valid frames;
    boundary values 16384/16385, 2097152/2097153, depth 7/8, digits 640/641, -0,
    NEL/LS/PS/VT/FF/FS/GS/RS separators, CRLF, BOM, invalid UTF-8, missing final LF,
    empty capture, empty frame, two values in one frame, trailing frame after
    session_result, NaN/Infinity, 1e9999 (classifier-stricter).
F2  Absent members (KeyError), wrong types (bool for int, float for int, str for
    bool, None), coerced-equal values (True == 1, 4.0 == 4), extra members.
F3  Ordering: action without decided, decided without action, two actions, unpaired
    trailing action, event_index gaps/duplicates, extra ready/hand_result mid-stream.
F4  Closure: hand_result complete False, accounting_complete False, nonzero
    interrupted_response_count, failure_reason set, secondary_failures nonempty,
    rank_source wrong, settlement mismatch with hand or with kernel; session_result
    status failed, wrong accounting_scope, None duration.
F5  Outer: session status not completed / stop_reason set / failure markers False,
    '' or missing; requested/completed hands != 1; hands empty or 2; ordinal != 1;
    entry without result; result status failed; capture_truncated True; exit != 0.
F6  Replay: button != 0, stacks mismatch/bool/float, action rows out of order, wrong
    seat, illegal action, origin wrong, extra rows after terminal (acting_seat None),
    non-terminal end, settlement mismatch.
F7  Exception discipline: every refusal must surface as ValueError/TypeError/
    KeyError/IndexError/binascii.Error (caught) -- never a crash on a reachable
    input (AttributeError, RecursionError, AssertionError).
F8  Agreement (v1): reason relabels, unknown reason, in-pool default, hit outside
    teacher pool, hit outside declared root, wrong action, zero/duplicate river
    records, nonpassive pre-river, record/replay field mismatch -> never 'hit'.
F9  Credit paths that must not exist: any host-refused capture with chip_eligible
    True or classification != 'excluded' (O1); any 'hit' without table_hit and exact
    teacher action at the declared root key.
