# Prosecutor report - Claude: v0a-eval-panel-completion/r002 (FIX, Tier C)

Role: prosecutor. This pass tries to break the candidate by mutation and reports which attacks
the frozen source refuses. It issues no defect verdict of its own; the design opinion below is
the prosecutor's reading, offered for the cold reviewers and the finalizer.

Candidate: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Parent (sole): 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13
Tree: c531d0b93520cd69704aa14842cea32d5b31ca51
Ref: refs/heads/review/v0a-eval-panel-completion/r002-verified
Manifest SHA-256: 6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5
Scratch: D:/Pontius/tmp/eval-completion-r002-prosecutor-068a8070/
Sealed inventory: inventory-prosecutor-claude.md, SHA-256
ab3ed87a121bc7395a17fbfbed34778685dd06d42c1f41c24c82f79cc85872ef (written and hashed before
coverage.md or any checks/ file was opened; rehashed unchanged at the end of this pass).

Outcome in one line: 73 consumed members of the retained envelopes were attacked under
absence, wrong JSON type, equal-but-not-it values, default/conversion fill and (for v2) the
public validator; no attack reached 'hit', chip_eligible, agreement_eligible or a complete
schedule from a report that a completed real host attempt could not have produced. Four
advisory observations survive; none is a product defect on the frozen surface.

## 1. Identity results (from Git objects, not the packet)

- Ref resolves to the candidate; the commit has exactly one parent, 449a2a3c; tree c531d0b9.
- diff-tree --no-renames parent..candidate: M src/pontius/eval_agreement.py, M tests/cases.json,
  A tests/test_eval_protocol.py; no other path differs (whole-tree filter returns empty).
- Manifest recomputed as "<sha256>  <path>\n" rows over raw cat-file blob bytes, whole rows
  sorted bytewise, LF after every row: byte-identical to manifest.sha256; digest equals the
  handoff and candidate.json value above.
- Parent manifest anchor recomputed over beb84be5..449a2a3c: byte-identical to
  inputs/parent-manifest.sha256, digest f58d6ed822787f0766c23ee63540ddc999784ad11d03dc103a1cbf
  80f68c0194 (line-wrapped here only).
- brief.md, supporting-files.json and coverage.md hash to the handoff's stated digests; all 35
  supporting-files.json entries and all 51 inputs/dependencies.json pins (blob at the stated
  commit in D:/Pontius or D:/Pontius-handoffs, plus the packet copy) match.
- Preparatory refs, read as raw Git identity only: r002-red 64526c1a has sole parent 449a2a3c
  and changes only tests/cases.json and tests/test_eval_protocol.py (production blobs equal
  r001); checks/red-test.py is byte-equal to 64526c1a:tests/test_eval_protocol.py
  (cc43c867...). r002 85e59e8f and r002-green-initial f2cdf32e have sole parent 449a2a3c and
  the same three-path delta; 85e59e8f carries the identical eval_agreement.py blob (8329de1e)
  and differs from the candidate by one test line (the dealer-index fix coverage.md describes).

## 2. Attack surface and method

Every member the classifier consumes was enumerated from the frozen producers (event adapter,
runtime v1/v2 record producers, host WireConsumer, Session report) and the frozen consumer
(eval_agreement.py). For each member the frozen bytes were traced under (a) absence, (b) wrong
JSON type, (c) a value that compares equal to the required one but is not it (False/0, 1.0/1,
True/1), (d) dataclass default or conversion instead of a check, and (e) for v2 records the
public validator. Tracing is static from raw blobs; no project code was executed. The full
table is section 3 of the sealed inventory; it is reproduced in condensed form here.

Legend: EX excluded (Unusable/KeyError/TypeError caught at eval_agreement.py L308, chips
None, chip_eligible False); DIS disagreement (chip-eligible, never hit); CRASH uncaught
exception (fail-closed, no credit). Line numbers are raw frozen candidate lines.

### 3. Attack table (member | required by producer/host | refusing line | a | b | c | d)

Session report (tools/v0a_table_session.py L183-190, L356-361)
- version, session_id: str equality/prefix, L123-124 | EX | EX | n/a | n/a
- status 'completed', stop_reason None: L290-291 | EX | EX | False is not None EX | n/a
- failure_reason None, secondary_failures list []: L92-94 | EX | EX | False/'' EX | n/a
- requested_hands, completed_hands exact 1: L292-293 via L45 | EX | EX | True/1.0 EX | n/a
- hands list len 1: L294 | EX | EX | n/a | n/a
- source_commit, blueprint_artifact_sha256, blueprint_sha256: chain L131-132, shape L141-146,
  digest L162 | EX | EX | n/a | n/a
- provider, config_sha256 (v2): L133-139 | EX | EX | n/a | n/a
- input_sha256, next_button, carried_stacks: not consumed; extra members not refused (adv.)

Hand entry (session L252-253)
- ordinal exact 1: L297 | EX | EX | True/1.0 EX | n/a
- button exact 0: L222 | EX | EX | False/0.0 EX | n/a
- starting_stacks six exact ints == stacks: L223-224 | EX | EX | True/4.0 EX | n/a
- result dict: L299 -> L91 | EX | EX | n/a | n/a

Hand result (session L240-251, L315)
- version, session_id derived: L127-128 | EX | EX
- status 'completed': L300 | EX | EX
- failure_reason, secondary_failures: L299 -> L92-94 | EX | EX | EX
- identities: L131-132, L162-163 | EX | EX
- applied_actions list, exact row members {index, seat, street, action, origin}: L229, L231
  | EX | EX; .index/.seat exact ints L236-237 (False/0.0 EX); .street/.origin str L238, L240;
  .action exact {kind, raise_to} via HandAction L241 (raise_to True/2.0 EX)
- settlement: not None, json == terminal L214-217, json == kernel replay L267-269 | EX | EX |
  false vs 0, 1.0 vs 1 differ as JSON text EX
- child_exit_code int 0: L301-302 | EX | EX | False EX
- child_stdout_base64: L150 validate=True | EX | TypeError EX
- capture_truncated is False: L301 | EX | EX | 0 EX
- child_stderr_base64, input_sha256: not consumed (adv. C4)
- provider, config_sha256 (v2): L135-136 | EX | EX

Frame stream (adapter L188-192; host decode L52-90)
- base64/raw/LF: L150-151 | EX; strict JSON, unique keys, finite floats, no constants:
  L152-154 | EX; >= 3 dicts L155; ready/hand_result/session_result at 0/-2/-1 L157-158;
  exact member set per frame (plus provider, config_sha256 on v2 ready) L166-172 | any
  absent or extra member EX; shared protocol/session_id L173-174 | EX
- leniency (adv. C3): L154 str.splitlines universal newlines; no 16384 limit; CR accepted

Ready frame (adapter L226-231; host L729-737)
- protocol L160; session_id L161, L129; source_commit 40 hex L131, L144-146;
  source_manifest_sha256 64 hex L144-146 (v2 == record L58); blueprint_artifact_sha256 L131,
  L144-146; blueprint_sha256 == PreparedBlueprint.digest L162 | all EX
- evidentiary is False: L164 (new) | absent EX (member set) | True/None/'false'/0 EX
- provider 'baseline-rules-v1' L134 (new); config_sha256 64 hex, chain L135-139 (new) | EX

Action frame (adapter L199-201; host L826-831)
- hand_id == record == identity L197, L195 | EX; action_index int >= 1 L179 (new) and ==
  record L197 | True/1.0 EX; seat int 0..5 L180 (new) | EX; street == validated record street
  L197-198 | EX; action exact object L182 (new) and == record selected_action L199 | EX;
  pairing/ordering L178, L192, L202 | EX

event_result frame (adapter L243-247; host L845-860)
- event_index int == running count L186-187 | EX | EX | True/0.0 EX; status/decision pairing
  L188, L191 | EX; decision None or dict L190-194 | EX; failure None L188 | EX

v1 decision record (runtime L1286-1306; trace L216-237; host L796-815)
- exact 16 members L66 | absent/extra EX
- hand_id, event_index, action_index, street_action_index, seat, street, four digests,
  spine_reason: DecisionRecord L84-87 after raw checks (model.py L464-482) | wrong type or
  bool-for-int EX; replay equality L326 | wrong value DIS
- selected_action exact object L85; == action frame L199; BettingAction == applied action and
  == replayed lookup L331-333 | EX / DIS
- selection_reason: str only L73 (by design); raw value compared at L335, L339 | None/1 EX |
  unknown or relabelled DIS. The constant substituted at L87 (case d) never reaches L335/L339.
- timing exact 10 members L74; TimingStatus(...) L76; TimingRecord L77 (exact ints, exact
  floats, exact bools, interruption None); completed/no flags/<= 15 s L78-80; sum L81-82 |
  any absent/typed/equal-but-not-it member EX (0 for 0.0 EX, 0 for False EX, True for 1 EX)
- preparation_use exact 3 members L68; producer_status L69; artifact_sha256s list == [] L70
  (''/() EX); credited_seconds exact 0 L71 (False/0.0 EX); conversion at L86 runs after
- failure_reason None L55 -> L94 | EX

v2 decision record (runtime L1172-1191; provider codec L23-41; host L761-795)
- validate_decision L57 (new): exact 27 members, labels, exact ints (trace L659-667), digests,
  actions, proposal/outcome/reason/origin/delivery consistency, timing exact keys and
  _validate_timing, preparation exact, failure/timing consistency | any a/b/c member EX
- provider, config_sha256, source_manifest_sha256 == ready L58-59; fallback_blueprint_sha256
  == ready.blueprint_sha256 L60; delivery accepted and delivered == applied == selected
  L62-64; timing re-check L74-82; failure_reason None L55 | EX
- not constructed as ProviderDecisionRecord; the public validator is the boundary (case e)
- under a mislabelled strategy='blueprint-v1' a v2 record lacks 'blueprint_sha256' -> L334
  cause -> DIS, never hit

hand_result frame (adapter L278-285; host L886-901)
- complete is True L207 (1 EX); settlement json == hand L214-217; rank_source L306-307;
  evidentiary is False L205; two compute seconds exact finite float >= 0 L98-99, L209-210
  (0 int EX); interrupted_response_count exact 0 L208 (new; False/0.0 EX);
  accounting_complete is True L205 (1 EX); failure_reason/secondary L204 -> L92-95 | EX

session_result frame (adapter L296-299; host L902-911)
- status 'completed' L211; terminal_publication_compute_seconds exact float L213 (None/int
  EX); accounting_complete/evidentiary L205; failure members L204; accounting_scope L212 | EX

Settlement (host L873-884; kernel no_limit_betting L696-752)
- payouts, final_stacks, pots: bound only by JSON-text equality with the kernel replay and
  with the terminal frame; chips come from replayed net_returns[2] L270, never from the
  report; false/0, 1.0/1, extra members and order all differ as text | EX

Caller inputs (completion tool L307-309)
- blueprint exact source L281 (CRASH otherwise); teacher_actions .get L348 (None -> no hit;
  non-BettingAction -> DIS); board sorted tuple L282 and deal distinctness L283 (CRASH before
  the try); private_hands: hero bound by visible_cards_sha256 at every controlled decision
  L326, villain/folders by settlement replay only; stacks: entry L222-224, declared root
  always at 4 (L345; eval_bridge L79) so stacks != 4 never agreement_eligible; strategy not
  cross-checked against ready.protocol (adv. C1)

Agreement branch (L311-361) and summarize (L364-378)
- record/expected count L320-321; per-index replayed fields L326 (event_index, action_index,
  street_action_index, seat, street, state_before/after digests, visible digest - the spine
  digest covers the full public history, stacks and contributions); selected action L331-333;
  blueprint identity and reason L334-336; pre-river passive L339-340; exactly one river
  L341-342; declared root L345-346; teacher L348-355; hit outside root L356-357 | all DIS
- summarize: scheduled exact int >= 0 and >= observed L366-367 (bool -> ValueError raised);
  classification label L370; complete L378 admits 'unsupported' (adv. C2); counters L374-375

## 4. Candidates (severity-ordered; all advisory, none binds a required correction)

C1 Advisory - strategy is not bound to the retained protocol version.
   Location: eval_agreement.py L273-274, L316-318; L121, L160.
   Requirement: design section 5, separate outcome and agreement eligibility; brief 7.
   Scenario: an unmodified real blueprint-v1 CHECK capture (protocol
   pontius-v0a-event-interface-v1) classified with strategy='baseline-rules-v1' returns
   chip_eligible True, chips from replay, classification 'unsupported', causes
   ['agreement:baseline_outside_declared_root'].
   Falsifying observation: nothing at L121-L174 or L316 compares strategy with the ready
   protocol, so a blueprint hand's chips can be attributed to the baseline arm by a caller
   label alone. Never a hit; the frozen caller (completion tool L307-309) always passes the
   default, so the frozen surface cannot reach it.
   Smallest correction: require (protocol endswith 'v1') == (strategy == 'blueprint-v1') in
   classify, or make strategy derive from the ready protocol. Confidence high (mechanism),
   product impact none on the frozen callers.

C2 Advisory - summarize.complete counts 'unsupported' attempts as complete.
   Location: L378. Scenario: a primary attempt whose witness replays outside the declared
   root without a table hit (e.g. entry starting_stacks [6]*6 with stacks=6) classifies
   'unsupported'; summarize over such results reports complete=True with hits=0. The frozen
   caller refuses before summarize (completion tool L347-348) and re-checks hits in
   complete() L409-410, so the tool cannot report success on it. Smallest correction: fold
   counts['unsupported'] into the complete predicate or document that complete means
   "every attempt resolved", not "every scheduled hand hit". Unchanged from the parent.

C3 Advisory - framing leniency relative to the host and adapter.
   Location: L152-154 (str.splitlines). The host requires LF-only frames without CR or BOM
   and at most 16384 bytes (host L52-90, L530-535); the classifier frames on universal
   newlines and has no size limit. A constructed capture with CR LF endings, or with U+001E
   between two objects on one line, is framed where the host would have refused. Every
   content, identity, settlement and pairing check still applies, so this yields no credit
   the proper-line form could not; it is a fidelity gap, not a credit path. Smallest
   correction: split on b'\n' only and refuse b'\r'. Unchanged from the parent.

C4 Advisory - host input and wire identities are not bound by the classifier.
   Location: hand result input_sha256 and blueprint_artifact_sha256 are not compared with the
   caller's schedule bytes or sha256(wire); only the canonical blueprint digest (L162-163) and
   the hero's visible-card digest at each controlled decision (L326) bind the deal and
   policy. Villain/folder hands are bound only through settlement replay (L262-269). The
   completion tool records blueprint_wire_sha256 beside the classification (L311) and the
   agreement phase requires wire == deterministic export (L321-322), so the production run
   binds them outside the classifier. Smallest correction: accept an optional expected
   input_sha256/wire digest pair and require equality. Unchanged from the parent.

Coverage observations (not defects): the new test does not mutate v1 timing members by type
(flags 0 for False, seconds 0 for 0.0), hand_result/session_result seconds or booleans by
type, child_exit_code False, or the equal-but-not-it settlement payloads beyond
test_eval_agreement's payouts False case; all of these are closed statically by the lines
named above (TimingRecord model.py L377-422; L98-99; L205-213; L301-302; L214-217). The v1
seat bool case on the action frame (L180) cannot be exercised with an equal value because
the controlled seat is 2; the test retargets to an applied_actions row (replay L237), which
is the only reachable equal-valued site.

## 5. Closed members (attacks the frozen source refuses, with the refusing line)

ready.evidentiary True/None/'false'/0 -> L164; ready.provider/config_sha256 absent or wrong
-> L166-172, L134-139; ready digest shapes -> L141-146; ready.blueprint_sha256 -> L162;
report/hand identity chains -> L123-132; requested_hands/completed_hands/ordinal True or 1.0
-> L292-297 via L45; button False/0.0 -> L222; starting_stacks True/4.0 -> L223-224;
applied_actions row members absent -> L231; index/seat False/0.0 -> L236-237; street/origin
-> L238, L240; action raise_to True/2.0 or missing member -> L241 via L49-50 and model.py
L141-147; settlement False/1.0 or extra member -> L214-217, L267-269; child_exit_code False
-> L301-302; capture_truncated 0 -> L301; stdout non-str or bad base64 -> L150 (L308);
frame member absent/extra -> L166-172; duplicate JSON key -> L102-106; NaN/Infinity/1e9999
-> L110-117; action frame action_index/seat bool or float -> L179-181; action object missing
raise_to -> L182; event_index bool -> L186-187; event failure not None -> L188; decision
without action or action without decision -> L191-192, L202; v1 record member absent (any of
16) -> L66; preparation member absent -> L68; producer_status wrong -> L69; artifact_sha256s
'' or () -> L70; credited_seconds False/0.0 -> L71; selection_reason None/int -> L73;
timing member absent -> L74; timing status other/True/1 -> L76; timing ints bool/float,
seconds int, flags int, interruption str -> L77 (model.py L399-422); elapsed > 15 s, flags
True -> L78-80; seconds sum -> L81-82; hand_id/indices/seat/street/digests/spine_reason
malformed -> L84-87 (model.py L464-482); v2 member absent (schema_version, provider,
provider_outcome, preparation_use, any of 27) -> L57 (codec.py L46); v2 labels/ints/digests/
timing/preparation malformed -> L57 (codec.py L47-136); v2 provider/config/manifest mismatch
-> L58-59; v2 fallback digest -> L60; v2 delivery not accepted or delivered != applied !=
selected -> L62-64; hand_result complete 1, accounting_complete 1, evidentiary other ->
L205-207; interrupted_response_count False/0.0 -> L208; compute seconds int -> L209-210;
session_result status/scope/seconds -> L211-213; settlement missing -> L214; wire event count
vs replay -> L305; rank_source -> L306-307; record count -> L320-321; replayed field mismatch
(any of eight) -> L326; selected action mismatch -> L331-333; blueprint digest or reason
mismatch (unknown label, relabel) -> L334-336; nonpassive pre-river -> L339-340; zero or two
river records -> L341-342; changed stack root -> L345-346, L356-357; off-pool hit -> L350-351;
in-pool default or wrong teacher action -> L352-353; summarize scheduled bool/negative/less
than observed -> L366-367; unknown classification -> L370.

## 6. Design opinion (prosecutor's reading, not a verdict)

SOUND for the corrected classifier. The r001 category was invited by mixing typed
constructors with validation; the candidate now admits every raw member of the v1 decision,
its preparation and timing, and every counter it consumes, before any constructor runs, and
routes v2 through the public validator. No consumed member remains admitted by default or by
loose equality. Residual strain, advisory: the classifier still hand-mirrors host predicates
(WIRE_FIELDS, integer/float/bool discipline, framing) rather than sharing one table with the
host, which is where C1 and C3 come from; a shared wire-schema module would remove that
duplication at modest cost, but nothing in the frozen bytes requires it now.

## 7. Reconciliation with coverage.md, the parent findings and the disposition

The parent round accepted one Important category (R03-01 and F1): incomplete raw retained
schema admission manufacturing defaults/types before credit. The named examples were
ready.evidentiary, interrupted_response_count False/0.0, requested_hands/completed_hands/
ordinal True/1.0, missing credited_seconds/producer_status, artifact_sha256s '', and v2
records admitted without validate_decision (schema_version, provider, provider_outcome,
preparation_use).

Closure of the named examples: each is refused at L164, L208, L292-297, L69-71, L57 as
listed above, and the RED/GREEN pair exercises exactly those mutations on real v1 and v2
captures (49 exclusion failures on the parent, all passing on the candidate).

Closure of the whole category, beyond the examples: my inventory enumerated every consumed
member (section 3) and found none that is still admitted by a dataclass default, a conversion
before a check, or an untyped equality. The members the parent reviewers did not name -
button, starting_stacks, applied_actions row members and index/seat, action-frame counters
and action object, v1 timing member set and selection_reason type, v2 ready provider/config
binding and record identity binding - are also closed by new lines in this delta (L179-182,
L222-224, L229-231, L236-237, L73-74, L133-139, L58-60). Members already closed in the
parent (closure booleans, seconds, child_exit_code, settlement text equality, exact frame
member sets, duplicate keys, nonfinite numbers) are unchanged. I therefore read the fix as
closing the category, not only the examples.

coverage.md claims 1-7 match the inventory: claim 1 (v1 raw member sets before constructors)
is L66-71, L74, L85-87; claim 2 (v2 public validator and identity binding) is L57-60,
L133-139; claim 3 (ready/terminal exactness) is L164, L208; claim 4 (counts, ordinal, button,
stacks, indices, raw action objects) is L222-224, L236-237, L179-182, L292-297; claim 5
(unknown v1 reasons observed, not replaced) is L73 with L335/L339; claim 6 (real v2 premium
divergence keeps chips) is the test's premium witness search and preflop-raise assertion;
claim 7 (six affected suites) matches the focused receipt selection. Its stated falsifiers are
the right ones. The coverage note is honest that the final matrix is not byte-identical to
the initial RED and about the dealer-index setup error; the receipts confirm both.

Advisories C2-C4 are unchanged parent behaviour outside the accepted category and outside
the declared fix scope ("raw schema admission before typed construction and exact successful
metadata"); reporting them here is not a claim that the fix is incomplete. C1 is likewise
outside the category. Missing test coverage for statically closed members is not a product
defect and is not graded as one.

## 8. Receipts assessment (implementer evidence, assessed not reproduced)

- RED: snapshot of 64526c1a (test-only child of r001; production blobs equal r001), CPython
  3.14.6, scrubbed environment (SystemRoot, TEMP, TMP, PONTIUS_GIT, PYTHONDONTWRITEBYTECODE),
  -B -P, ResourceWarning and unraisable warnings as errors, -k test_eval_protocol; exit 1;
  one unittest case, 49 distinct failing subtests (22 blueprint-v1, 27 baseline-rules-v1),
  zero errors; journal source_commit 64526c1a, source_verified true; journal output_sha256
  equals the packet's red-result.json digest (3131a540...). red-test.py equals the frozen RED
  test blob. This is a genuine counterfactual RED against the rejected parent's classifier.
- Setup error: snapshot of 85e59e8f (same production blob as the candidate), exit 1 with one
  unittest error (dealer index 16 outside 0..15) and five suites passed; retained honestly.
- GREEN: snapshot of the candidate 430ad75d, same environment and flags, six suites selected;
  exit 0; 79 unittest cases, 0 skipped (11+29+8+21+9+1); journal source_commit equals the
  candidate, source_verified true; journal output_sha256 equals focused-result.json's digest
  (a1318803...). The freeze script hashes candidate bytes from the implementer worktree with
  a temporary index and a create-only ref; the snapshot script refuses an existing snapshot,
  syncs a locked offline environment and asserts 3.14.6.
- The prerequisite audit is a finalizer fact record about r001; it lists names and digests
  of r001 review files but no content, and it does not bear on this delta.
- Limits: the new suite's baseline control depends on a real Session run inside the test
  (about 144 s per focused run); the receipts do not cover a hard kill during an active
  Session (parent advisory, unchanged) nor any retained solve/export/agreement run.

## 9. Line counts and hygiene (raw frozen bytes)

Changed blobs: eval_agreement.py 378 lines (max 100 cols), cases.json 52, test_eval_protocol
.py 137 (max 100 cols); all LF-only, BOM-free, no trailing whitespace, final LF. Delta
parent..candidate: +80/-28, +2/-1, +137/-0 (numstat). Whole Slice A surface at the candidate:
production 2060 lines (eval_bridge 521, eval_agreement 378, v0a_eval_panel 674,
v0a_eval_panel_completion 487) and tests 1918 (198+750+153+383+297+137); the parent was
2008/1781. Production is below the 3000 hard ceiling and above the 1200/600 working figures
(disclosed in checks/scope.json, which matches this census exactly). All ten counted files
pass the hygiene checks.

## 10. Verified boundaries and practical limits

Verified statically: the three-path delta touches only the classifier and its tests; host,
session, adapter, runtime, codecs, kernel, dealer, bridge and completion tool blobs equal the
parent. The agreement path binds hero hand and board (visible digest), full public history
and stacks (spine digest), applied action, replayed lookup, canonical blueprint digest, v1
reason and teacher action before a hit; chips come only from a kernel replay that matched
both retained settlements. Not verified: any execution; the numeric reference path; full-H
coverage, tie census, strength or resource claims; host transport under kill. This report
authorizes nothing.

## 11. Prohibitions and exposure statement

- Read: handoff.md, candidate.json, manifest.sha256, brief.md, supporting-files.json, every
  inputs/ file, raw frozen Git blobs via cat-file at the candidate and parent; then, only
  after the inventory was sealed, coverage.md and every checks/ file. Git use was read-only
  (rev-parse, rev-list, cat-file, diff-tree, diff, for-each-ref, hash comparisons).
- Not opened: any reviews/ directory, any other packet or round, progress.md, INDEX.md,
  readiness/disposition files outside checks/, any transcript or session log, any other
  scratch directory, D:/Pontius working-tree source.
- Not run: no project code, tests, tools, imports, uv/pip or hooks. Utility scripting used
  C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe (reviewer arithmetic,
  not a test receipt), plus coreutils sha256sum.
- Disclosures: (1) checks/prerequisite-audit.json lists r001 reviews/ file names and digests;
  I read that metadata as data and opened none of the files. (2) `git for-each-ref` showed the
  sibling preparatory refs r002, r002-red and r002-green-initial; I read only their commit
  identity, delta paths and blob ids to verify the receipts' provenance. (3) Large tool
  outputs were persisted by the harness under my own session's tool-results directory and
  re-read from there; no other session's files were touched. (4) The inherited context carried
  general tool, skill and MCP server instructions and this assignment; no candidate narrative,
  prior finding or prior verdict was present. (5) Besides the two named deliverables, my
  scratch directory holds utility scripts (identity.py, seal.py, census.py) and a src/ folder
  of frozen blob dumps used for reading; nothing outside the scratch directory was written.
- No source, packet, ledger, ref or worktree was modified.
