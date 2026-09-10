# Completeness critic: v0a-eval-panel-completion r003

Candidate 7ca821802c949b047becf6599d603b3b63d51fa7
(parent 430ad75de79cec13d66ff3dc4981dd3770a371b7).
Read from raw Git blobs only. Packet inputs read: handoff.md, brief.md, coverage.md, inputs/*,
checks/* (boundary-plan, scope, parent-disposition, gate files, receipts). No reviews/ opened.
Utility scripting: stdlib-only probes with pythoncore-3.14-64 (base64/json/float behavior).
No project code executed. One file written (this one); one generator script in session scratch.

Identity checked: ref refs/heads/review/v0a-eval-panel-completion/r003 -> 7ca82180, one parent,
manifest.sha256 rows equal the raw blob digests (eval_agreement.py 9187fd8d...,
test_eval_protocol.py 4ddab494...). tests/cases.json is blob b1d4254... at BOTH parent and
candidate (unchanged; test_eval_protocol already registered at line 51).
tests/test_eval_protocol.py exists at the parent (blob 059adac) and is modified (+81/-0), not
new. The task text's "changed paths: tests/cases.json" and "(new)" are inaccurate; the handoff's
two-file delta is what the bytes show.

Line references: C = eval_agreement.py, H = tools/v0a_table_host.py,
S = tools/v0a_table_session.py, T = tools/v0a_eval_panel_completion.py,
M = src/pontius/v0a/model.py, K = src/pontius/no_limit_betting.py.

## 1. Byte-level admission: covered; evidence I checked

decode_frame (C120-151) is a transcription of H52-90 with the same predicate order: bytes type,
0 < len <= 16384 incl. LF, no CR, no leading BOM, bracket depth <= 8 outside quoted/escaped text,
640 signless integer digits, duplicate-key hook, constant hook, strict UTF-8 via str.decode, and
RecursionError mapped to a cause. frames_for (C184-187) mirrors H512-535: strict base64, 0 < raw
<= 2097152, final LF, split on 0x0A only, each physical frame fed with its LF. The only asymmetry
is parse_float (C114-117 refuses non-finite; H87 admits inf). I checked that every float member a
completed stream can carry is host-validated finite (H641-642 at H892/907; M377-381 via H689-707;
trace._validate_timing for v2), so the stricter rule cannot exclude a host-completed stream.
Probes: float('1e400') is inf; json '1E5' is float; '-0' is int 0; raw NUL/tab inside strings
refused by json strict mode in both. Nothing at this layer is missing from the four inventories.

## 2. Members, branches and readers no inventory mentions

N-1 Identity-label charset/length is not mirrored (Minor, constructed-only, no semantics).
  S205 admits session ids only as prefix + [A-Za-z0-9_-]{1,40}; H943 {1,48}; adapter {1,64}. The
  child_id the host binds every frame to (H670, H827) is derived from that label, so a stream
  whose session_id/hand_id suffix is outside the charset or longer than 40 is host-unreachable.
  bind_identity (C154-164) checks prefix, structural derivation and equality only. Concrete
  input: take the real v1 CHECK capture and replace suffix "protocol" with "pro/tocol"
  consistently in report.session_id, hand.session_id, every frame session_id, every action
  hand_id and record hand_id. All equality checks pass, M464 _require_ascii_id accepts ASCII "/",
  classify returns hit. Requirement: host-equivalence of admission. Materiality: none for
  actions, chips or keys; the suffix carries no game content, and play() (T304) always supplies
  a regex-valid label. Same class as the parent-accepted external identity limits
  (source_commit/manifest). Non-ASCII suffix variants are refused once any decision record
  exists (M464 / trace _require_text), so they can only reach chip credit on a zero-record hand.
  Not an r003-scope defect; record as an unmirrored predicate for the Slice B interface.

N-2 "Cannot mirror" is overstated for config_sha256 (Advisory, corrects review-01 F-04).
  providers.py:50-57: BaselineProvider identity is canonical_sha256 of a fixed config dict,
  independent of the blueprint, so the v2 config_sha256 the host requires (H736-737) is a
  constant the classifier could compare; C171-173 checks 64-hex shape only. source_commit and
  source_manifest_sha256 are available to play() through the run context (T287, T303) but are
  not passed to classify (C175-180 shape only). Effect is limited to v2 chip credit and identity
  binding; no hit path. Not a defect under the r003 brief; a checkable gap, not an impossible one.

N-3 Reported values with no reader (examined; no credit path).
  play() reports blueprint_wire_sha256 (T311); nothing compares it with
  session.hands[0].result.blueprint_artifact_sha256 (complete T376-436 and accounting T439-463
  do not). The classifier binds the canonical blueprint_sha256 to the caller's decoded blueprint
  (C195-196, C165-166, C367) and only cross-equates the artifact hash (C165-166), so the design's
  wire-vs-canonical distinction (accepted-design section 1) is retained but never reconciled.
  Also unread: hand/report input_sha256, next_button, carried_stacks, child_stderr_base64, and
  result members river_hand, river_records, chips, causes. None can create a hit, chip
  eligibility, a completed count or a coverage claim; complete() reads only classification,
  chip_eligible and observed_table_hits (T409-416).

N-4 Exception paths that escape classify (examined; correct, fail closed).
  Outside the try: C314 PreparedBlueprint TypeError, C315 board-order Unusable, C316 deal
  errors, C361-362 prepared.action_for (require_legal_blueprint_action ValueError,
  immutable_blueprint 286-302), C364 HandAction, C378 root_key. An escape aborts play() with no
  result and no host_attempt observation; accounting() then reports a missing outcome. No
  disposition is manufactured. The prosecutor's "board unsorted refused (C315)" is an exception,
  not an excluded result; same fail-closed effect. Reachability of C361 with a real table is
  closed: the key embeds the legal decision (immutable_blueprint 67-70), so a stored entry legal
  at export is legal at lookup.

N-5 Replay event-count derivation versus the host's event sequence (examined; equivalent).
  No inventory states why C338 is exact. Traced: K522-529 makes a completed river round terminal
  inside apply_action; K588-616 advance on river keeps the street and sets SHOWDOWN; K617-640
  advance to a non-river street yields round_complete when fewer than two seats can act. Host
  next_event (H274-302): FOLD terminal -> no event; river round complete -> at most one advance
  then one showdown_result; otherwise one street_revealed per advance; opponent_action per
  opponent act. Replay: in-loop advances (C265-267) always +1, and a same-street advance cannot
  occur there because any later applied row fails C270 (acting_seat None); post-loop advances
  (C288-291) count only street changes; showdown +1 (C293-294). Bot decision event_index,
  action_index and street_action_index (C281-284) equal H832-838 by construction. So a v1
  record can only satisfy C359 if it is host-consistent; this is the evidence behind P-02 being
  an agreement-layer (not chip-gate) predicate.

N-6 Non-canonical inputs that decode to identical values (examined; correct).
  base64 with non-zero trailing bits ("AB==" -> b"\x00") is admitted by validate=True; identity
  is by decoded bytes, the same bytes the host captured, so no admission difference. Escaped
  lone surrogates ("\ud800") parse in both decoders; every credited str member is bound by
  equality to an ASCII identity or enum membership except v1 selection_reason (P-01) and the
  identity suffix (N-1).

N-7 Exception surface of the try at C341 (examined; closed).
  Every data-dependent access before a credit is guarded so that only ValueError/TypeError/
  KeyError/IndexError/binascii.Error can arise: str checks precede startswith (C158), dict checks
  precede key access (exact_fields), 640-digit ints reach TimingRecord (exact ints) and, for v2,
  _seconds_ns_bounds, whose converted() catches OverflowError; C78 bounds elapsed_ns before C81
  divides. No AttributeError/OverflowError/ZeroDivisionError path found.

## 3. Failure modes declared without checking, now checked

- "No host-completed stream can carry a non-finite float": true (section 1).
- "All (c) attacks refused because exact_integer / dataclass exact types / is True": true, and
  also for the cross-frame equalities: pending[k] == record[k] (C230) could pass 2 == 2.0, but
  both sides are exact-int validated first (C212-213; C85 / M141-147; trace._validate_action).
- "Content checks still apply" is not used as closure anywhere in this report.

## 4. Contested items: my verdicts from the bytes

P-01 Unknown v1 selection_reason: confirmed as described (C73 str only; H806-812 refuses).
  It is a parsed-level host-equivalence deviation, but the governing r003 brief directs that
  "reason-only disagreements retain their previous outcomes" and design section 5 names unknown
  reasons as explicit disagreement observations. Design-sanctioned; outside r003 scope; not a
  candidate defect. Note agreement_eligible can be True for such a record (C379 ignores the
  reason) while classification stays disagreement; that matches the counter's definition.
P-02 v1 state/placement rules only at the agreement layer: confirmed (chip gate C344-348; record
  reconciliation C353-375). Chips come from the host-authoritative applied_actions replay, and
  design section 5 places record reconciliation after outcome eligibility. Pre-existing,
  disposed at r002 ("baseline replay separation"); not an r003 defect. Worth a controller ruling
  on whether chip eligibility must also require host-consistent records.
P-03 v2 records unreconciled: confirmed and stronger than P-02 (no selected_action vs applied
  bot action check either). Same disposition as P-02; a cheap follow-up is comparing each v2
  record's selected_action and event/action indices to the replayed bot rows.
P-04 stderr cap: confirmed (H513 cap 65536 -> truncated -> transport_failed; classifier reads
  only stdout). The FIX itself added the stdout cap (C185) although the same capture_truncated
  flag covers it, so the stderr omission is an asymmetry by the candidate's own logic. No
  consumed bytes; brief scope names stdout. Minor follow-up, not blocking.

## 5. Any path from missingness/default/coercion/failure to credit?

None found beyond the disposed P-01..P-03 class. Traced every assignment to chip_eligible (C345
only, after all wire/replay gates), agreement_eligible (C379 only, key equality), hit (C388,
requires not causes, exactly one river record, declared key, table hit, teacher equality, and
C365/C367-369 tie the record's action and reason to the independent lookup), summarize.completed
(chip_eligible sum), summarize.complete (no missing/disagreement/excluded; unsupported ignored,
carried advisory) and complete() (all primaries hit, controls, artifacts). .get defaults at C346,
C359, C367-372 cannot fire for admitted records (exact_fields / codec _keys guarantee presence).
teacher_actions.get(name) None leads only to unsupported or hit_outside_teacher_pool.

## 6. Packet observations

- coverage.md's RED count (26 + 1 seam) matches red-stdout (failures=27). Focused stdout shows
  6 pytest entries passed.
- checks/review-gate.json says broad "Not yet run" while checks/broad-gate.json records BROAD
  GREEN on 3.14.6; the gate record is stale. The handoff ordering (two Codex cold passes, then
  broad) is consistent, but the stale file should be corrected before adoption.
- Test oracle limits: host_accepts mirrors decode_json plus the capture cap; the exact 2097152
  acceptance boundary has no positive control (only an over-limit case that also overflows a
  frame). Disclosed in coverage.md; not a defect.

## Verdict

No new material defect. New items: N-1 (Minor, unmirrored identity-label regex, constructed
only), N-2 (advisory correction: config digest is mirrorable), N-3/N-4/N-5/N-6/N-7 examined and
correct. Contested P-01..P-04 are real host-equivalence deviations at parsed/envelope level but
are design-sanctioned or pre-disposed and outside the r003 raw-frame scope; P-04 is the one the
candidate's own reasoning most directly implies. Recommendation: CLEAN for the r003 scope, with
N-1, N-2, P-03 and P-04 carried as explicit follow-ups before the classifier becomes the Slice B
interface.
