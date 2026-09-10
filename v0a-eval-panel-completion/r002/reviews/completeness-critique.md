# Completeness critique - Claude (r002 FIX, candidate 430ad75d)

Candidate 430ad75de79cec13d66ff3dc4981dd3770a371b7, parent 449a2a3c. Delta verified as
exactly src/pontius/eval_agreement.py (+80/-28), tests/cases.json (+2/-1) and the new
tests/test_eval_protocol.py (+137). Every claim below was checked against raw frozen blobs
(git cat-file) of the classifier, v0a/model.py, v0a/trace.py, decision_provider/{codec,model,
providers}.py, no_limit_betting.py, holdem_cards.py, immutable_blueprint.py,
legal_decision_spine_v2.py, tools/v0a_{event_adapter,table_host,table_session,
eval_panel,eval_panel_completion}.py and the three eval test suites. Read-only Git; utility
interpreter used only for stdlib semantics and hygiene counts. No project code executed.

Verdict on the question "what did all of them miss": no material defect survives. The items
below are branches, members and consumers that no inventory names, each checked and found
correct, plus three small inaccuracies in the prosecutor's closure claims.

## 1. Unmentioned areas checked and found correct

### 1.1 Code after the exclusion boundary (L311-361) has no wire-reachable raise
No inventory examines what can raise outside the try at L288-310. Traced every call:
- `prepared.action_for(...)` L328: `BlueprintDecisionKey.from_state` raises only when card
  street != state street or the actor is not seat 2; replay builds `cards` from
  `before.street` and only appends rows whose acting seat is 2 (L243-247), so neither holds.
  `require_legal_blueprint_action` (immutable_blueprint L286-302) can raise only for a
  caller blueprint entry whose action is illegal at its own key; the key embeds the full
  LegalBettingDecision, so lookup context equals construction context. Caller input only.
- `HandAction(**record['selected_action'])` L331: already admitted at L86 (v1) or codec L62
  (v2). `root_key(replay_root(), board, deal.hand(2))` L345: caller-bound board/deal.
  `teacher_actions.get` L348: caller mapping.
Kernel `AssertionError`s (settle L719/L731/L743, side_pots, apply_action raise commit) are
internal conservation invariants unreachable from applied-history input. RecursionError from
`json.loads` is the already-noted F-02 and is a phase crash, never credit.

### 1.2 The baseline early return skips every record-to-replay binding
L316-318 returns 'unsupported' before L320-340. For a v2 capture the decision records are
therefore bound only to each other (L195-199), to the ready frame (L58-61) and to the event
count (L305): seat (0..5 at L180), action_index sequence, street, state digests and
selected-vs-applied action are never compared with `applied_actions`. The unchanged host
binds all of them (host L770 state_mismatch, L826-830). Consequence checked: chips are
`settled.net_returns[2]` from applied_actions and caller stacks (L263-270), cross-checked
against terminal and hand settlement (L214-217, L267-269); records cannot move chips. A v2
record can never reach 'hit' under any strategy: its `selection_reason` is a provider label
(codec L67) and it has no `blueprint_sha256`, so L334-336 always adds a cause. For the
blueprint path the same mismatches are agreement-level 'disagreement' with chips retained
(L320-327), so the asymmetry is consistent with design section 5 (outcome eligibility
precedes agreement). Unexamined by all three inventories; correct, not a defect.

### 1.3 v2 provider outcome semantics under chip credit
`validate_decision` admits completed decisions with `provider_outcome` in ('error',
'invalid', 'abstained') and `selection_origin='blueprint_fallback'` (codec L79-96,
L124-134); L78 excludes only cutoff/deadline cases. Such a capture is chip-credited
'unsupported' exactly like a genuine baseline decision; `observed_table_hits` stays 0 even
when `fallback_reason=='table_hit'` because L313 counts only `selection_reason`. The host
accepts the same records (host L786-794). Nobody named provider_outcome, selection_origin,
fallback_reason or proposal beyond "27 keys validated". Correct for Slice A (design 5 makes
baseline an interface constraint only); a Slice B consumer must re-read frames to learn
whether the provider actually decided. Not a defect.

### 1.4 config_sha256 is bound internally, never to the provider's own digest
L134-139 bind ready/hand/report/record config digests to each other and to 64-hex shape.
`BaselineProvider` (providers.py L50-57) derives config_sha256 from a constant dict, so the
expected value is computable, yet the classifier never computes it. No hit or chip
consequence (1.2). Reviewer 01's external-binding limit covers artifact/source identity but
did not name this member. Correct as a limit.

### 1.5 Blinds, controlled seat and button are not retained; replay hard-codes them
The session report carries no small_blind/big_blind/controlled_seat. Replay uses 1/2, seat 2
and button 0 (L222, L226, L240, L247). Checked what binds them: button exact 0; seat-2
origin labels; settlement equality. Chips equal `final_stacks[2] - stacks`, and final
stacks are bound to the retained settlement, so no blind configuration can manufacture
chips. Hits are protected by `state_before_sha256`, whose payload includes big_blind and
button (spine L33-36), so a host state under other blinds never matches the replay digest.
Correct; nobody traced it.

### 1.6 Event-count identity against the host's numbering
Traced host Table.event/next_event (host L241-302) against replay L232-235, L244, L255-261:
opponent action +1, street reveal +1, completed river advances to SHOWDOWN with street kept
RIVER (kernel L594-611) so the trailing loop adds 0, then showdown +1; FOLD terminal adds
nothing (host L275-276). A completed-river advance inside the per-row loop (L232-235) would
over-count by one, but the following row then fails L237 (`acting_seat` is None on a
terminal state, kernel L326-327). Correct.

### 1.7 Settlement comparison via json.dumps(sort_keys=True)
Verified with the utility interpreter: 1, 1.0 and true serialize differently; tuple and
list serialize identically (value-equivalent, in-memory only; JSON cannot yield tuples);
NaN serializes as 'NaN' and can never equal kernel output. Correct.

### 1.8 Result members with no production reader
`chips`, `river_hand`, `river_records` and `causes` are consumed only by tests;
`observed_table_hits` by complete()/agreement() for the changed-stack control;
`chip_eligible` and `agreement_eligible` by summarize; `classification` by
agreement()/complete()/accounting()/summarize. The completed count is the chip_eligible
sum (L374), never a chip total. Nothing reads a missing member with a default that could
turn into credit: complete() requires `complete is True`, `coverage == plan['coverage']`,
every primary 'hit', and the three controls (completion L403-416).

### 1.9 Registration, hygiene, totals
tests/test_pontius.py L21/L59-61 loads cases.json and imports each module; the focused
receipt shows test_eval_protocol ran (1 case, 0 skipped) inside 79 total. All three blobs
are LF, BOM-free, at most 100 columns, no trailing whitespace. scope.json totals
(2060/1918) match reviewer 02.

## 2. Inaccuracies in closure claims (no credit consequence)

- Prosecutor "stdout non-str -> L150": `base64.b64decode(bytes, validate=True)` accepts
  bytes (verified), so a bytes-typed `child_stdout_base64` is admitted. Content-equivalent;
  only in-memory reports can carry bytes. Also non-canonical trailing bits ('QR==') decode
  to the same bytes as 'QQ=='; the decoded bytes are what is validated. Not a defect.
- `seconds()` L99 and host finite_seconds both accept -0.0 (verified `-0.0 >= 0`).
  Value-equivalent. Not a defect.
- `exact_integer(value, expected)` type-checks `value` only; a caller `stacks=True` would
  accept starting stack 1. Caller input (reviewer 02 F02-03 territory).

## 3. Test-quality observations (not defects)

- test_eval_protocol.py asserts only `classification == 'excluded'` (L131-133), never the
  cause label, so a mutation excluded for an unintended reason still passes. The RED receipt
  (checks/red-result.json) shows the original 50 mutations accepted by the parent; the final
  file is a strict superset (diffed: only additions). Of the added cases, missing_action,
  missing_timing and stack_type=True were already excluded by the parent's constructors or
  list equality; stack_type=4.0 and provider_binding are genuine regression guards without a
  RED receipt, as coverage.md discloses.
- The premium-witness search (L26-33) and the baseline Session run establish a real
  prefix-diverged v2 capture; the assertion at L69-70 checks the raise actually happened.

## 4. Answer to the credit question

Hit requires, at L320-357 with no cause: record count equals replayed bot decisions, all
eight replayed fields equal, selected == applied == lookup action, blueprint digest and
reason label equal, pre-river reasons passive, exactly one river record, river key equals
the declared s=4 root, teacher present, lookup table_hit, selected == teacher. Every member
read there was admitted with an exact type at L53-87/L179-199 or is a caller input; `.get`
defaults at L313-339 can only add causes. Chips depend only on kernel settlement bound to
two retained copies. Completed counts sum chip_eligible, which is set only after the whole
admission try succeeds (L312). Full coverage requires scan['complete'], each primary 'hit'
before the next attempt (completion L345-348), and complete()'s echo checks. I found no
path by which missingness, a default, a coercion or a failure becomes a hit, chip
eligibility, agreement eligibility, a completed count or a full-coverage claim.

Limits: static tracing only; no host, session or classifier execution; kernel conservation
assertions taken as unreachable from validated input on the strength of their guards.
