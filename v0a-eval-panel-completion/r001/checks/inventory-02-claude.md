# Reviewer 02 inventory: v0a-eval-panel-completion/r001

Written BEFORE opening coverage.md, operating-boundary.md or checks/. Derived only from
handoff.md, candidate.json, manifest.sha256, brief.md, supporting-files.json, the inputs/
copies and raw frozen blobs read with `git cat-file blob 449a2a3c...:<path>`.

Candidate 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13, sole parent
beb84be566aa28029284bd35c526d33cd27af369, tree 09d78e4ede52a9093fc7941270d497a7362706dc,
manifest f58d6ed822787f0766c23ee63540ddc999784ad11d03dc103a1cbf80f68c0194 (recomputed).

## A. Requirements this checkpoint must meet

Sources: brief.md mechanisms 1-8; accepted brief criteria 4-9; accepted design sections
4-6; resource decision (H=1081, 600 s / 2048 MiB solve envelope, board 2c 7d 9h Js Qc);
controller addendum 2 (3,000 production-line hard ceiling, 1,200/600 working figures);
workflow checklist v1. Tier C lens: teacher identity, exported membership and retained
outcome interpretation must not manufacture agreement from missingness, defaults or
failures.

R1  Phase admission (mech. 1; design 1, 6). Each of solve/export/agreement is its own
    immutable plan; declared-full plans bind the retained capacity/preflight bytes and the
    controller decision by hash; export/agreement also bind producer result, teacher bytes
    and (agreement) wire bytes. No phase continues into another. test-subset plans are
    labeled, cannot claim H=1081, cannot carry retained prerequisites. Missing mandatory
    inputs refuse, never default.
R2  Solve (mech. 2; design 3). One hero at a time in frozen permutation order, H a prefix
    of the permutation; each completed row and untraced cost retained; first exact tie with
    nonzero per-deal returns gets the singleton reference (build_reference, forced values,
    best_response, validate_reference); a failed reference stops the phase; tie-absence may
    only be claimed over a completed census.
R3  Teacher bytes and export (mech. 3; criteria 4; design 1-2, 4). Canonical ASCII JSON
    binds fixed game/opponent law, prefix, board, full permutation, H and ordered rows.
    Export consumes immutable bytes without solving, is byte-identical on repeat, encodes
    through encode_blueprint with source_id t1:<sha256(teacher)>, decodes and compares the
    complete key/action map, and checks actual wire size against the 1,048,576 cap.
    Teacher, canonical-source and wire identities stay distinct.
R4  Membership (mech. 4; criteria 4-5; design 4). Exhaustive over the 1,081-hand root
    universe through PreparedBlueprint.action_for and BlueprintProvider.propose with real
    DecisionObservation values; every h in H hits with the teacher action; every complement
    key defaults (table_hit False, CHECK, blueprint_default). Provider labels never stand in
    for v1 selection_reason.
R5  Witness bank (mech. 5; criteria 6; design 4). Scan the frozen finite seed/index bank in
    declared order with the unchanged deal_for_hand; reject only board collisions among all
    twelve private cards; keep the first witness per required h with all six hands intact;
    retain unused draws and collisions; missing witnesses fail coverage; no late seeds, no
    replaced cards, no post-play selection; the estimate is planning only.
R6  Host reuse and ownership (mech. 6; criteria 9; design 6). Worker cwd equals the
    inherited run root, PONTIUS_RUN_CONTEXT set before Session.prepare, each Session runs
    prepare and launches its real child; child stdout retained as a complete frame stream;
    one parent result and one journal line per invocation, including failure; no per-hand
    verification files.
R7  Outcome then agreement (mech. 7; criteria 5, 7; design 5). Read nested
    hands[*].result; any outer/nested failure, non-completed status, non-null failure cause,
    truncated capture, nonzero child exit, absent settlement, malformed base64/frames,
    duplicate keys, nonfinite numbers, missing terminal closure, incomplete hand_result or
    failed event_result is an unusable outcome with a retained cause. Completed hands get
    chips and chip eligibility separately from agreement. Blueprint agreement requires
    exactly one controlled river record; replay the applied history and reconcile
    event/action indices, state hashes, visible-card hash, blueprint digest, selected action
    and reason against an independent PreparedBlueprint.action_for; compare the action to
    the frozen teacher; pre-river reasons must be passive_default; a prefix-diverged
    completed baseline stays chip-eligible and is never forced through the river gate.
R8  Counters (criteria 6; design 5). Scheduled, observed, missing, completed, agreement
    eligible, hits, disagreements, unsupported, excluded reconcile exactly; one final
    disposition per attempt; pre-river defaults never count as hits; final acceptance needs
    complete required coverage, no disagreement, no unresolved excluded attempt.
R9  Negative controls (mech. 8; criteria 8; design 4-5). Real host: proper-subset off-pool
    default, in-pool CHECK hit distinguished from default by retained reason, changed stack
    zero hits, reason relabeling detected. Test artifacts keep their own identities; their
    coverage never transfers to the production artifact.
R10 Budget and hygiene. Whole-slice production/test totals disclosed against 1,200/600 with
    the 3,000 hard ceiling; changed files LF-only, BOM-free, <=100 columns, no trailing
    whitespace; exact-type discipline on evidence paths; Python 3.14.6 only.
R11 Unchanged surfaces. Host, session, dealer, codec, evaluation, betting, cards, trace,
    execution, status generation unchanged (dependencies.json entries equal the parent).

## B. Producer / caller / consumer paths per computed value

Frozen locations are file:line in the candidate blobs.

V1  Teacher bytes. Producer: completion.solve (completion.py:189-226) builds rows with
    bridge.hand_totals (eval_bridge.py:210-236) and serializes with bridge.teacher_bytes
    (:311-332) -> _teacher_validate (:252-308) -> _teacher_json (:239-241). Consumers:
    bridge.teacher_actions (:335-343) via completion.teacher_input (:229-255) in export and
    agreement; completion.complete (:376-436) recomputes bytes from teacher_hand rows for
    the solve phase; complete() also re-reads the teacher artifact for every phase.
    Meaning: hands == permutation[:k]; action strings "check"/"raise-to-2" from
    BettingAction.__str__ (no_limit_betting.py:65-68); actions dict maps hand name ->
    BettingAction. bet_total must equal 2*check_total (:288-290) which is the s=4 law.
V2  Wire artifact. Producer: bridge.export_teacher (:363-382) from _teacher_entries
    (:346-360) using root_key (:145-150) and encode_blueprint. Consumers: bridge.
    validate_membership (:385-421); completion.export (:258-273) repeat-compare and emit;
    completion.agreement (:314-373) re-exports and requires byte equality with the bound
    input wire; completion.play (:282-311) writes it as host-blueprint.json for the real
    Session and passes decode_blueprint(wire) to classify; host WireConsumer.ready
    (v0a_table_host.py:729-734) binds ready.blueprint_sha256 to decode(raw).digest.
V3  Membership report. Producer validate_membership; consumer completion.export requires
    passed; completion.complete requires the single membership observation passed.
    Meaning: passed = exact entries AND zero disagreements over all 1,081 hands.
V4  Witness scan. Producer completion.witnesses (:149-180) over v0a_seeded_deals.
    deal_for_hand (:58-65, sorted two-card lists, seat order (index+1+offset)%6).
    Consumers: agreement requires scan['complete']; scan['selected'][name] feeds play;
    the witness is echoed in attempt_scheduled and host_attempt and compared by
    accounting (:439-463). hand_name over the dealer's sorted list equals the universe
    naming (combinations over ascending DECK).
V5  Session report. Producer tools/v0a_table_session.Session.run (:317-361) with
    play_hand (:233-315) and the real child through host.ChildConnection/WireConsumer.
    Consumer eval_agreement.classify (:223-309). Identity strings: session prefix
    'pontius-v0a-table-session-v1-correctness-' (session.py:15-16); hand session_id
    'pontius-v0a-table-host-v1-correctness-<suffix>' (:241); child id
    protocol+'-correctness-table-'+suffix (:237-238). classify.bind_identity (:69-88)
    expects exactly these.
V6  Decision record (v1). Producer pontius.v0a.runtime._decision_record
    (runtime.py:1286-1307): selection_reason TABLE_HIT/PASSIVE_DEFAULT from the child's
    own PreparedBlueprint lookup; host WireConsumer.decision (host.py:796-815) validates
    shape and expected hashes but NOT selection_reason. Consumer classify: shape via
    DecisionRecord (eval_agreement.py:145-151, reason overridden for shape only), then
    field equality with replay (:274), selected action vs replay and vs independent lookup
    (:276-281), digest and reason vs independent lookup (:282-284), river collection
    (:285-288).
V7  Replay. eval_agreement.replay (:176-220) recomputes event indices matching host
    Table.event numbering (host.py:241-302: hand_started 0, each opponent action and
    street reveal +1, showdown +1 when not a fold terminal) and settlement through the
    kernel with the caller's deal; consumer classify requires len(events)==final+1
    (:253) and rank_source (:254-255).
V8  Classification. classify result dict {chip_eligible, chips, agreement_eligible,
    classification in hit/disagreement/unsupported/excluded, causes, river_hand,
    observed_table_hits, river_records}. Consumers: completion.agreement requires 'hit'
    for every primary attempt (:345-348) and specific control outcomes (:362-366);
    completion.complete re-checks all primaries 'hit' and the controls (:403-416);
    eval_agreement.summarize (:312-326) counts by classification; accounting summarizes
    primaries and lists missing pool hands.
V9  Phase completion. Worker emits <phase>_summary with complete=True; parent supervise
    (v0a_eval_panel.py:518-528) sets phase_complete=complete(...) and fails a completed
    status when False; main (:644-659) records phase, coverage, plan, permutation_sha256
    (json.dumps of the name list, identical to bridge.permutation_digest) and calls
    completion.retain (:466-487) to publish artifacts and mark retention complete.
    Consumer teacher_input requires producer status completed, phase, cleanup_verified,
    phase_complete, coverage, pool_count, prerequisites, permutation_sha256 and artifact
    sha256 with retention 'complete'.
V10 Prerequisite binding. completion.validate (:97-146) requires declared-full plans to
    carry capacity/preflight/decision bindings whose sha256 equal the constants at :18-22
    and reads them through host.OwnedInput; decision constant equals the pinned
    inputs/resource-decision.md digest 037a0de1...; the capacity and preflight constants
    (29f532a9..., 8a17325e...) match no blob in the candidate tree and no row of the frozen
    execution_journal.jsonl (/experiments/results/runs/ is gitignored) -- provenance is
    unverifiable from the allowed inputs.

## C. Failure cases to check

F1  Session/hand failure, absent nested result, wrong ordinal, requested/completed != 1.
F2  capture_truncated, nonzero or non-int child_exit_code, settlement None or mismatched
    between hand_result frame, outer result and kernel replay.
F3  Bad base64, no trailing LF, duplicate JSON keys, NaN/Infinity/1e9999, non-dict rows,
    wrong first/last frame types, unexpected frame type, wrong field set, protocol or
    session_id drift, blueprint digest drift, identity string swaps.
F4  event_result failed, decided without action or action without decision, event_index
    gap, duplicate action, decision identity mismatch, timing interrupted or exceeding the
    15 s bound, v1 record with v2 fields, missing preparation_use.
F5  Zero or duplicate river records; nonpassive pre-river reason; unknown reason; in-pool
    default; hit with wrong action; hit outside teacher pool; hit outside declared root;
    changed stack/prefix (key differs) -> zero hits, chip-eligible, unsupported.
F6  Baseline prefix-diverged completed hand -> chip-eligible, not agreement-eligible,
    never forced through the river gate.
F7  Witness bank not covering H; deadline inside the scan; collision draws; duplicate
    controlled hands; overlapping development/holdout ranges.
F8  Solve deadline before publication; reference disagreement on the first nonzero tie;
    tie present but reference absent (or vice versa) in complete().
F9  Export: repeat not byte-identical; wire over cap; decoded map differs; membership
    relabel at the provider boundary; changed or reduced entries.
F10 Plan admission: wrong members, coverage/pool_count mismatch, test-subset with
    prerequisites, declared-full with wrong board/count/envelope, prerequisite digest or
    phase mismatch, capacity permutation drift, preflight sample incomplete.
F11 Agreement accounting: orphan or out-of-order host_attempt, hand/label/witness
    mismatch, missing outcomes, overcount in summarize.
F12 Parent-side: accounting() or complete() raising inside supervise skips retain and the
    permutation digest but cannot produce a 'completed' status; no 'ready' event exists for
    completion phases.
F13 Host input files host-input.json/host-blueprint.json are overwritten per attempt in
    one directory; identity survives only through the retained session report.
F14 Budget: raw whole-slice production 2,008 lines (521+326+674+487), tests 1,781
    (198+750+153+383+297); checkpoint delta +1,046/-4 production, +833 test.
