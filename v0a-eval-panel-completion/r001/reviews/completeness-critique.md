# Completeness critique — v0a-eval-panel-completion/r001 (not a cold pass)

Author: Opus 5 agent dispatched by the coordinator after cold reviews 01 and 02 returned.
Candidate: 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13.

**This is not an independent cold review and must not be counted as a Tier C pass.** It
was given both cold reviewers' inventory summaries and the titles of their Minor/Advisory
items (no reports, no verdicts), and asked what both had missed, with the brief's Tier C
question put to it directly. It checked its suspicions against the frozen blobs, ran no
project code, opened no reviews/, other packet, ledger or scratch directory, and wrote
nothing. Its text below is reflowed to 100 columns without changing any word.

---

**Completeness critique — candidate 449a2a3c (r001), from frozen bytes only**

Method: read all eight changed blobs plus frozen consumers (v0a_table_session.py, v0a_table_host.py,
v0a_event_adapter.py run_session, v0a_seeded_deals.py, execution.py, immutable_blueprint.py,
blueprint_artifact/codec.py, blueprint_preparation/lookup.py,
decision_provider/{model,providers,codec}.py, holdem_cards.py, v0a/model.py, no_limit_betting.py
excerpts). No reviews/, checks/, progress, INDEX or tmp opened. No project code run.

**1. Tier C path check (missingness / default / failure -> hit, completed, or full-coverage): none
found.**
Enumerated every precondition for `classification == 'hit'` in
src/pontius/eval_agreement.py:259-308: fresh `PreparedBlueprint.action_for` on the kernel-replayed
state must hit (276-278), the retained v1 `selection_reason` must equal that fresh result (282-284),
`selected == replayed applied action == fresh lookup action` (279-281), exactly one river record
(289-290), `selection.key == root_key(replay_root(), ...)` at the fixed s=4 root (293-294), teacher
entry present (296), and zero accumulated causes (302). Because `agreement()` enforces `wire ==
export_teacher(raw)` (tools/v0a_eval_panel_completion.py:320-322), wire keys are exactly H's keys,
so hit implies h in H. Off-pool default reaches only 'unsupported' (296-299); in-pool default is
`teacher_disagreement` (300-301); any failure/malformation returns at 256-258 with
`chip_eligible=False`. Missing attempts: `summarize` forces `complete=False` on `missing` (320-326);
parent `complete()` requires count+3 scheduled and observed with ordinals 0..count+2, hand labels ==
H, and every primary 'hit' (405-411). Test-subset cannot claim full pool: `count < HERO_COUNT` (138)
and `coverage` is compared by `complete()` (383-384). Membership `passed` needs `exact` (source_id
`t1:<sha>`, entry count, full key/action map) and zero provider disagreements
(eval_bridge.py:391-392, 418).

**2. Unexamined by both inventories; checked and found correct**
- Strategy kwarg vs wire protocol (eval_agreement.py:223-224, 264-266). `classify` never binds
  `strategy` to the frames' protocol version. Checked whether a v2 stream classified as blueprint-v1
  could become a hit: it cannot. v2 records carry `selection_reason` in SELECTION_REASONS
  (`provider_selected`...; decision_provider/model.py) and have `fallback_blueprint_sha256`, no
  `blueprint_sha256`, so line 282-284 always adds a cause -> 'disagreement'. `play()` hard-codes
  'blueprint-v1' for both Session and classify (completion.py:301-302, 307-309). Latent API hazard
  only (misclassified as disagreement rather than unsupported).
- Replay event numbering vs host (eval_agreement.py:183-186, 205-211 vs v0a_table_host.py:274-302).
  The inner loop's unconditional `event_index += 1` per street advance cannot double count with the
  trailing `+= showdown`, because `apply_action` already sets SHOWDOWN when a river round completes
  (no_limit_betting.py:528-529) and `advance_street` at river keeps `street` (588-611); all-in
  run-outs go through the trailing loop's street-change-conditional increment, matching the host's
  street_revealed x3 + showdown_result.
- Real-host prefix realization (completion.py:292-296). With button 0 and opponents
  `['fold_to_bet','passive',None,'fold_to_bet'x3]`, `select_opponent` (host:213-225) yields seats
  3,4,5,0 fold (cannot check), seat 1 call then check, bot passive default CHECK pre-river: exactly
  PREFIX (eval_bridge.py:58-63). Villain 'passive' calls a river bet, so BET teacher rows settle at
  showdown.
- Exceptions outside classify's try (270-305). `prepared.action_for` / `to_betting_action` cannot
  raise for v1 records already validated at 148-151; a hit key is state-identical so the table
    action
  is legal. If anything did raise it propagates to the worker's 'failed' with `attempt_scheduled`
    but
  no `host_attempt` -> `missing_outcomes=1`, never success.
- `str.splitlines()` at eval_agreement.py:96 splits on more boundaries than the host's `\n` framing
  (host:530-535); any divergence produces a json.loads failure -> excluded. Fail-closed, cannot
    merge
  or synthesize frames.
- Journal count: nested Session and grandchild adapter never write because inherited contexts return
  early in `finish_run` (execution.py:124-125); `Source` passes `inherited=os.environ[CONTEXT_ENV]`
  (host:148-150) and `begin_run` re-stamps `inherited=True` (execution.py:44) even though
  `child_context` strips it. One journal row per invocation holds.
- `PREREQUISITES['decision']` (completion.py:21) is verifiable from allowed inputs:
  sha256(inputs/resource-decision.md) = 037a0de1... matches, and dependencies.json pins the same
    hash
  at handoffs 2943f935. Reviewer 01 M-01 ("full-pool prerequisite digests not verifiable")
  overreaches; only capacity/preflight (F-01) are cold-unverifiable.

**3. Reconciliation gaps neither reviewer named (no defect; each closed elsewhere or unreachable).
Advisory.**
- Export `complete()` (completion.py:398-401, 417-435) never cross-binds
  `membership.report.wire_sha256`/`teacher_sha256` (or `export_encoding.report`) to the retained
  blueprint.json/teacher.json digests; blueprint.json is only self-consistent. Closed downstream:
  agreement re-derives `wire == export_teacher(raw)` (320-322) and `teacher_input` binds the
  producer's retained artifact SHAs (249-254). Two equality checks in `complete()` would make the
  export result self-certifying.
- Agreement `complete()`/`accounting()` (403-416, 441-463) reconcile worker-emitted `hand` labels
  and witness dicts but never check `result.classification.river_hand == hand` (river_hand is
    derived
  at eval_agreement.py:234-237 from the retained private_hands), nor `attempt_scheduled.witness ==
  witness_scan.report.selected[hand]`, nor that exactly one `witness_scan` with `complete=True`
  exists. The worker guarantees all three (324-328, 337), so no false-coverage path exists in the
  frozen bytes; the "every h has a real dealt witness" claim is currently trusted from worker labels
  rather than re-derived by the parent.
- Preflight prerequisite (completion.py:131-132) is admitted on `sample_complete` alone; capacity
  gets a permutation binding (127-130), preflight gets no board/coverage/permutation binding. Safe
  only because the SHA is pinned to one retained file.
- Admission `validate()` (143-145) shape-checks `inputs` bindings but does not read or hash the
  bytes; SHA enforcement happens in the worker (`teacher_input`/`bound_bytes`). A wrong input SHA
  therefore becomes a failed supervised run with a journal row rather than an admission refusal.
  Coverage item 2 wording ("each input binds absolute path and SHA-256") implies admission-time
  binding.
- `retain()` (466-487): two artifact rows sharing a name would both be marked 'complete' while the
  file holds the second's bytes. Unreachable: `complete()` requires the exact name set (417-421) and
  the worker emits each name once; status would be failed regardless.
- Early stop at the first non-hit primary (346-348): remaining H hands are never attempted; the run
  fails with `missing_pool_hands` listing them. Fail-closed, but one transport flake aborts a full-H
  campaign and a retry needs a new plan/grant under operating-boundary.md.
- Malformed prerequisite JSON in `validate()` (123-132) raises KeyError/TypeError, not ValueError;
  main/worker catch `Exception` -> failed. Contract-only (test `assertRaises(ValueError)` style),
  fail-closed.

**4. Values computed but consumed by nobody in code** (informational, none affects a gate):
`witnesses.planning` estimate (174-180), `witness_scan.counts`,
`agreement_summary.action_categories`/`host_complement` (371-373), `export_encoding.report`,
per-attempt `cost`, `classification.river_hand`/`river_records`, `full_pool_estimate=None` for
completion phases (v0a_eval_panel.py:657-659). `observed_table_hits` and `chip_eligible` are the
only classification fields the parent gates on for controls (413-416).

**Verdict for the completeness question:** both inventories jointly cover the material surface; the
items above are either confirmations or advisory reconciliation gaps. No new Critical/Important
finding. I did not find any path by which missingness, a default, or a failure becomes a hit, a
completed count, or a full-coverage claim in the frozen bytes.
