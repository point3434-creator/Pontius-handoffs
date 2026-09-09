# Reviewer 01 inventory: v0a-eval-panel-completion/r001

Written BEFORE opening coverage.md, operating-boundary.md or checks/.
Candidate 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13, parent
beb84be566aa28029284bd35c526d33cd27af369, manifest
f58d6ed822787f0766c23ee63540ddc999784ad11d03dc103a1cbf80f68c0194.
Derived from the frozen blobs (bottom-up), the frozen consumers they call, the accepted
brief/design under inputs/, and this checkpoint's brief.md.

## A. Requirements this checkpoint must meet (governing text)

R1  Phase admission is explicit and immutable: solve/export/agreement each need their own
    complete plan; a full run binds the retained capacity/preflight bytes and the controller
    decision; export/agreement also bind their producer result and teacher/wire bytes; no
    phase continues implicitly; test subsets are labeled and cannot claim a full population
    (brief.md mech 1; design s1, s6 step 4-7).
R2  Solve runs one hero at a time in the frozen pool order, retains each completed row and
    its untraced cost, inspects the first exact tie with nonzero per-deal returns against the
    singleton reference, and claims tie absence only over a completed census (brief mech 2;
    design s3).
R3  Canonical teacher bytes bind the fixed game/opponent law, permutation/H and ordered
    action/value rows; export consumes them without solving; repeat encoding is byte-identical;
    decode and compare exact complete keys/actions; check the actual wire size; keep teacher,
    canonical-codec and wire identities distinct (brief mech 3; design s1, s2, s4; accepted
    brief crit 4).
R4  Exhaustive root membership through PreparedBlueprint and the public
    BlueprintProvider.propose boundary with real DecisionObservation values, separate from
    host observations; every complement key defaults; provider labels never stand in for the
    v1 selection_reason (brief mech 4; design s4; accepted brief crit 5).
R5  Witness scan of a frozen finite seed/index bank in declared order using the unchanged
    deal_for_hand; reject only board collisions among all twelve private cards; keep first
    witnesses; retain unused draws and collisions; missing witnesses fail coverage; no late
    seeds, replaced cards or post-play selection; witness draws are never a chip population
    (brief mech 5; design s4; accepted brief crit 6).
R6  Reuse the existing worker run context and Session.prepare per one-hand session at the
    inherited root (PONTIUS_RUN_CONTEXT set before preparation; cwd equals the run root);
    child stdout is a complete retained frame stream; one parent records one result and one
    journal line per invocation including failed/partial attempts; no per-hand admission or
    verification files (brief mech 6; design s6; accepted brief crit 9).
R7  Outcome eligibility precedes agreement eligibility: read the nested hands[*].result;
    nullable failures, malformed frames, truncation, missing settlement, incomplete
    terminal/closure are exclusions with retained causes; replay the applied history;
    reconcile real keys/reasons/actions; exactly one controlled river decision for agreement;
    a completed prefix-diverged baseline stays chip-eligible (brief mech 7; design s5;
    accepted brief crit 5, 7).
R8  Real-host negative controls: proper-subset off-pool default, a CHECK hit distinguished
    from a default by its retained reason, changed stack/prefix yields zero hits, reason
    relabeling is detected; test artifact identity never transfers to the production artifact
    (brief mech 8; design s4, s5; accepted brief crit 8).
R9  Counters reconcile scheduled, completed, missing, agreement-eligible, hits, disagreements,
    unsupported and excluded; one final disposition per scheduled attempt; pre-river defaults
    are never hits; acceptance needs complete required coverage, no disagreement and no
    unresolved excluded attempt (design s5; accepted brief crit 6).
R10 Tier C lens: teacher identity, exported membership and retained-outcome interpretation
    must not manufacture successful agreement from missingness, defaults or failures.
R11 Placement/scope: extend eval_bridge.py, add eval_agreement.py, extend v0a_eval_panel.py
    with dispatch into tools/v0a_eval_panel_completion.py (not a second entry), three new
    suites registered only in tests/cases.json; host/session/dealer/codec/evaluation/betting/
    cards/trace unchanged; Python 3.14.6 only; no retained solve/export/agreement authorized.
R12 Budget/hygiene: whole-slice count disclosed against 1,200/600 working figures under a
    3,000-production-line hard ceiling; LF-only, BOM-free, <=100 columns, no trailing
    whitespace; exactness (type is int / is bool) on evidence paths.

## B. Producer / caller / consumer paths for every computed value

Teacher bytes and identities (eval_bridge.py)
- hand_totals(root, board, hero) [r003, unchanged] -> row dict {hand, check_total, bet_total,
  denominator, action, bet, wins, losses, ties, work}; producer: completion.solve() per hero
  in permutation order.
- teacher_bytes(board, permutation, rows) -> canonical ASCII JSON; validates board tuple,
  permutation tuples, rows dicts, then _teacher_validate. Consumers: completion.solve()
  (artifact 'teacher.json'), completion.complete() (recomputes and compares bytes),
  tests.
- teacher_actions(raw) -> (board, hands, actions); requires bytes, canonical re-serialization
  equality (refuses dup keys, whitespace, NaN), _teacher_validate. Consumers:
  completion.teacher_input(), completion.complete(), _teacher_entries().
- _teacher_validate: exact field set, domain equality (version/prefix/root/opponent),
  canonical board names, full-universe permutation (1081 distinct), H = nonempty exact
  prefix, rows in order, exact ints, denominator 990, |check|<=1980 even, bet == 2*check,
  action maximizes with CHECK on tie, optional outcome counts consistent, optional work.
- Identities: teacher_sha256 = sha256(raw); source_id = 't1:' + teacher_sha256 (67 ASCII);
  source_sha256 = decoded.digest (canonical codec identity); wire_sha256 = sha256(wire).

Export (eval_bridge.py)
- _teacher_entries(raw) -> (board, hands, actions, root, entries): replays root, requires
  declared root, traverses CHECK / bet->CALL / bet->FOLD terminals, builds one
  BlueprintActionEntry per h via root_key.
- export_teacher(raw, cap) -> (wire, report): cap exact int in (0, ARTIFACT_CAP]; encodes,
  refuses len(wire) > cap, decodes, requires source_id, entry count and exact key->action map
  equality. Consumers: completion.export() (twice, byte-equality), completion.agreement()
  (re-derives expected wire and requires wire == expected), tests.
- validate_membership(raw, wire) -> report over all 1081 hands: prepared.action_for and
  BlueprintProvider.propose(DecisionObservation) per hand; passed = exact entries and zero
  disagreements; rows retained. Consumer: completion.export(), complete().

Witness selection (completion.witnesses)
- Inputs: board ints, required names, bank {seed_start, seed_count, indices,
  holdout_seed_start, holdout_seed_count, sizing_rationale}; validate_bank (disjoint ranges,
  indices unique ascending 0..15, counts 1..65536).
- For offset in range(seed_count), for index in indices: deal_for_hand(seed, index) (sorted
  two-card hands, 12 distinct cards); status collision | witness (first for a required hand)
  | unused; every draw emitted via progress; returns selected, draws, counts, missing,
  complete, planning estimate. Consumer: completion.agreement() requires complete.

Host attempts (completion.play / agreement)
- play(): requires cwd == context root == ROOT; directory inside ROOT; builds a one-hand
  schedule (button 0, seat 2 controlled, stacks, blinds 1/2, opponents fold_to_bet x4 and
  passive at seat 1, witness private hands, board runout); writes host-input.json and
  host-blueprint.json; Session(args).run() with strategy blueprint-v1, reviewed_commit =
  context commit, development False; classify(result, ...). Session.prepare admits
  Path.cwd(); Source -> begin_run(inherited=PONTIUS_RUN_CONTEXT) does no filesystem
  verification; Session.run never calls finish_run (main only); child adapter also inherits
  and never journals.
- agreement(): teacher_input; wire bound and equal to export_teacher(raw); witness scan;
  per primary hand attempt(...) requires classification 'hit'; three controls on names[0]:
  off-pool (wire minus first key), check-hit (single CHECK row), changed-stack (stacks 6);
  summarize(primaries); agreement_summary observation.
- Retained: attempt_scheduled and host_attempt observations (full session report incl.
  child_stdout_base64), witness_draw per draw, witness_scan, artifacts for control wires.

Retained-outcome classification (eval_agreement.classify)
- Outcome gate (try block): session clean/completed/stop_reason None/1 of 1 hands/ordinal 1;
  nested result clean/completed/not truncated/child exit 0; frames_for: base64 strict,
  trailing LF, one JSON object per line with dup-key/NaN/inf refusal, >=3 frames,
  ready/hand_result/session_result at fixed positions, protocol v1|v2, blueprint digest equals
  caller's decoded wire, session/hand/child identity binding, exact field sets per frame,
  action/event_result pairing, event_index continuity, accepted|decided only, decision
  cleanliness, timing completed within limits, v1 DecisionRecord shape, terminal/closure
  clean and accounted, settlement equality terminal vs hand; replay(): button 0, stacks,
  kernel replay of applied_actions with origin and order checks, expected per-hero-decision
  fields incl. state_before/after and visible-cards digests, terminal reached, showdown
  strengths from caller deal, kernel settlement equals hand settlement; event count equals
  replayed final event + 1; rank_source consistent. Any failure -> excluded with cause,
  chip_eligible False, chips None.
- Agreement gate: chip_eligible True, chips = kernel net_returns[2], classification starts
  'unsupported'; non-blueprint strategy -> unsupported with baseline cause; record count vs
  expected; per record field equality, own lookup (prepared.action_for) vs record action,
  reason and blueprint digest; pre-river must be passive_default; exactly one river record;
  agreement_eligible = river key == declared s=4 root key; teacher present and table_hit and
  action equal and no causes -> 'hit'; else disagreement/unsupported with causes.
- summarize(results, scheduled): counts per classification, missing = scheduled - observed,
  complete = no missing, no disagreement, no excluded (unsupported tolerated).

Orchestration/reconciliation (tools entry + helper)
- validate_plan dispatch on version completion-plan-v1 -> completion.validate(plan, entry):
  exact member set per phase; common keys validated as a v2 capacity plan (runtime, board,
  stacks 4, prefix, universe digest, seed, permutation, resource); coverage; pool_count;
  declared-full: count 1081, development board, three prerequisites bound to hard-coded
  digests (capacity/preflight results must be completed + cleanup_verified + right phase,
  capacity permutation digest equals plan seed order, preflight sample_complete; decision
  digest 037a0de1...), solve resource exactly 600 s / 2048 MiB; test-subset: no
  prerequisites, count < 1081; inputs keys per phase, bound shape; witness_bank validated.
- run_plan -> completion.run -> solve/export/agreement with emit/deadline/measure.
- supervise -> completion.complete(observations, plan) -> phase_complete;
  completion.accounting for agreement; status forced failed when phase incomplete.
- main -> retain_boundaries then completion.retain (artifact publication with .partial
  staging, identity re-read, retention state) -> finish_run writes result.json + one journal
  row + STATUS.md; children never journal.
- teacher_input (export/agreement): teacher bytes bound; hands == plan permutation prefix;
  board == plan board; document permutation == plan permutation; producer result bound,
  completed, right phase, cleanup_verified, phase_complete, same coverage, same pool_count
  and prerequisites, same permutation digest; artifact rows bound with retention complete.

## C. Failure cases the code must handle (expected disposition)

F1  Plan with wrong phase, extra/missing member, witness_bank on non-agreement, coverage
    label invalid, pool_count 0/bool/>1081, test-subset with prerequisites or count 1081,
    declared-full with wrong board or missing/mismatched prerequisites, wrong solve envelope,
    inputs missing/extra/relative path/bad digest -> refusal before any work.
F2  Solve: deadline before a hero or before publication -> ValueError, partial teacher_hand
    rows retained, no artifact; first nonzero tie failing the reference -> stop; teacher
    bytes that fail validation -> stop; complete() false on missing/duplicated rows, wrong
    summary count, tie reference absent/extra/failed, artifact bytes not equal to
    recomputed teacher bytes.
F3  Export: teacher not canonical / changed domain / wrong board / wrong prefix / wrong
    order; producer result not completed/wrong phase/coverage/pool/prerequisites/permutation;
    teacher artifact row not bound or not retained; wire over cap; decode mismatch; repeat
    not byte-identical; membership disagreement or inexact entries -> stop.
F4  Agreement: blueprint bytes differ from deterministic export; bank incomplete -> stop
    with scan retained; deadline mid-scan or before an attempt -> stop with draws/attempts
    retained; any primary not 'hit' -> stop with that attempt retained; control outcomes not
    as expected -> stop; orphan/out-of-order/mismatched attempts -> accounting refusal.
F5  Classification: outer or nested failure_reason (None only, '' and False excluded),
    missing nested result, status not completed, stop_reason set, extra/missing hands,
    capture_truncated, nonzero/absent child exit, invalid base64, no trailing LF, empty or
    non-object frames, duplicate JSON keys, NaN/Infinity/1e9999, missing closure frames,
    wrong protocol/session ids, identity field mismatch or malformed sha, wrong frame field
    sets (v1 delivery_status), duplicate/unpaired action frames, event index gap, failed
    event_result, decided without decision, timing not completed or inconsistent, decision
    failure_reason non-null, hand incomplete/unaccounted/late failure, closure not
    completed, settlement missing or mismatched (terminal vs hand vs kernel replay),
    replay order/origin/initial-state drift, non-terminal history, event count mismatch,
    wrong rank_source -> excluded (chip_eligible False).
F6  Agreement-level: record count mismatch, replayed-field mismatch (state hashes, visible
    cards, indices), selected action differing from applied or from own lookup, wrong
    blueprint digest or selection_reason (including relabeled CHECK hit/default and unknown
    reasons), non-passive pre-river reason, zero or duplicate river records, table hit
    outside declared root or outside teacher pool, teacher disagreement -> disagreement;
    off-pool default at the declared root -> unsupported; changed stack -> unsupported with
    zero observed hits; baseline strategy -> unsupported but chip-eligible.
F7  Reconciliation: summarize refuses more results than scheduled and unknown labels;
    missing attempts stay visible; accounting refuses outcomes without a schedule or with
    the wrong hand/label/witness; complete() refuses missing summary, wrong coverage, wrong
    artifact set, artifact base64/size/digest mismatch.
F8  Publication: interrupted rename -> retention stays pending with base64 kept, or
    complete with bytes re-read and verified; unexpected artifact name refused.
F9  Interruption/kill of the worker: parent status interrupted/budget_exhausted/failed,
    observations already drained retained, phase_complete False, one journal row.

## D. Items to check against deferred inputs

D1  Whether the two hard-coded capacity/preflight prerequisite digests are tied to retained
    runs a89932e7 / 7ce5ab4f (not derivable from frozen tree or journal).
D2  Whether the focused receipts ran the three new suites plus test_eval_bridge and
    test_eval_panel_tool under the snapshot procedure on CPython 3.14.6 with scrubbed env.
D3  Whether the v2 (baseline) frame path in frames_for is exercised anywhere (the
    agreement fixtures use protocol v1 even for baseline=True).
D4  Whether RED receipts demonstrate each new behavioral boundary (identities, frames,
    failure types, settlement types, real host, admission).
D5  Whole-slice line totals as counted by the implementer versus my raw/nonblank counts
    (production 2008 raw / 1794 nonblank; tests 1781 raw / 1590 nonblank).
