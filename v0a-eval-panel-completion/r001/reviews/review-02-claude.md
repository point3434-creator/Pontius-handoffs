# Cold review 02 (Claude, top-down): v0a-eval-panel-completion/r001

Verdict: CLEAN. Design verdict: SOUND.

Binds to candidate 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13 and manifest
f58d6ed822787f0766c23ee63540ddc999784ad11d03dc103a1cbf80f68c0194. NEW-SURFACE, Tier C,
accepted design section 6 steps 4-7. Reviewer 02 worked top-down from brief.md mechanisms
1-8, accepted brief criteria 4-9, accepted design sections 4-6 and the resource decision.

## 1. Identity (verified from Git objects, not packet claims)

- refs/heads/review/v0a-eval-panel-completion/r001 -> 449a2a3c...; commit object has
  exactly one parent, beb84be566aa28029284bd35c526d33cd27af369; tree
  09d78e4ede52a9093fc7941270d497a7362706dc; all three equal candidate.json.
- diff-tree parent..candidate (no renames): exactly eight paths, A src/pontius/
  eval_agreement.py, M src/pontius/eval_bridge.py, M tests/cases.json,
  A tests/test_eval_agreement.py, A tests/test_eval_completion_tool.py,
  A tests/test_eval_export.py, M tools/v0a_eval_panel.py,
  A tools/v0a_eval_panel_completion.py.
- Manifest recomputed as "<sha256>  <path>\n" rows over raw cat-file blobs, whole rows
  sorted bytewise: bytes identical to manifest.sha256; digest f58d6ed8... equals the
  file's own SHA-256, candidate.json and handoff.md.
- supporting-files.json (SHA-256 3041c7fb...) pins 27 files; all 27 recomputed digests
  match. brief.md, coverage.md and operating-boundary.md match the handoff digests.
- inputs/dependencies.json: 43 entries; every (repository, commit, path) blob digest
  matches, and every packet copy matches its pin. It is a direct inventory, not a closure:
  36 candidate-commit entries of which 35 are byte-identical to the parent blob and the
  only changed member is tests/cases.json, itself in the manifest. Governing documents
  are pinned at b6f8b08f (README, docs/workflow.md), beb84be5 (accepted brief/design) and
  handoffs commit 2943f935 (resource decision, addendum 2, correction authorization).

## 2. Inventory reference

D:/Pontius/tmp/eval-completion-r001-review-02-d0c7b90f/inventory-02-claude.md
SHA-256 d27bf264c12253cbd3fea131861305b487a3018143a665ab38e3bf13e8e05781, written and
hashed before coverage.md, operating-boundary.md or checks/ were opened.

## 3. Method

Read every changed blob in full and the frozen consumers they touch at the candidate:
tools/v0a_table_session.py, tools/v0a_table_host.py (OwnedInput, Table, select_opponent,
WireConsumer), tools/v0a_seeded_deals.py, src/pontius/v0a/model.py, v0a/runtime.py
(selection reason emission), blueprint_preparation/lookup.py, decision_provider/model.py
and providers.py, immutable_blueprint.py, blueprint_artifact/codec.py, holdem_cards.py,
no_limit_betting.py, execution.py, tests/test_pontius.py and the plan-capacity fixture.
For each obligation I located the code, traced every value to every reader, and asked
what happens on hostile, malformed or incomplete input. No project code was executed.

## 4. Findings (severity-ordered)

No Critical or Important finding survived verification. The following are Minor
coverage/receipt items and advisories; none is a demonstrated product defect.

### F-01 Minor (coverage, provenance) - retained prerequisite digests are not cold-verifiable

Location: tools/v0a_eval_panel_completion.py:18-22 (PREREQUISITES) and :115-132.
Requirement: brief mechanism 1 and design section 1, "full runs bind the actual retained
capacity/preflight bytes and controller decision". Observation: the decision constant
equals the pinned inputs/resource-decision.md digest, but the capacity and preflight
constants (29f532a9..., 8a17325e...) match no blob in the candidate tree and no row of the
frozen execution_journal.jsonl (/experiments/results/runs/ is gitignored; the frozen
journal ends 2026-09-08). Only checks/admission-receipt.json, an implementer receipt,
binds them to result.json files under D:/Pontius-worktrees/eval-panel-prerequisite-
20260909 (the a89932e7/7ce5ab4f runs the resource decision names). validate() also
does not check the preflight result's coverage or the capacity result's pool_seed, so
the constants alone carry "declared-full". Scenario: if a constant named some other
completed result, a declared-full plan would still admit with the wrong measured basis;
if mistyped, no full plan admits (fail-closed). Neither can be excluded from the allowed
inputs. Smallest correction: record the two result digests with their journal rows and
source identity in a pinned governing input of the next packet (or a resource-decision
addendum), and optionally require result['coverage'] == 'declared-full' and
result['plan']['pool_seed'] == plan['pool_seed'] in validate(). Confidence high that it
is unverifiable cold; missing coverage alone is not a product defect.

### F-02 Minor (receipts) - three RED observations are not retained

checks/implementation-evidence.md states that the teacher/export availability RED, the
canonical board-name RED and the accounting orphan/ordinal/hand RED exist only in tool
history. brief.md requires demonstrating RED at each new behavioral boundary. The final
frozen tests exercise those boundaries (test_eval_export.py:34-36, :72-76;
test_eval_completion_tool.py:279-293) and the focused receipt is GREEN, so no product
defect follows; the export availability RED is trivially reproducible against the parent
commit, which lacks the functions. Advisory: retain such receipts in the next round.

### F-03 Advisory (label overlap) - baseline completed hands share the 'unsupported' label

src/pontius/eval_agreement.py:264-266 classifies any strategy != 'blueprint-v1' as
'unsupported' with cause agreement:baseline_outside_declared_root, the same label that
:296-305 gives off-pool defaults; summarize (:316-326) counts them together. Slice A
schedules only blueprint-v1 attempts, so no count is affected here, and chip eligibility
is preserved as the design requires. Before Slice B consumes this classifier, a distinct
label or counter would keep baseline hands out of the off-pool default count.

### F-04 Advisory - completion phases emit no 'ready' event

tools/v0a_eval_panel.py:282-284 returns before the 'ready' emit at :288-289, so
solve/export/agreement results lack the worker's sys.version/executable record that
capacity/preflight results carry. runtime.python is still validated inside the worker
(:147-150 via completion validate :104-106) and runtimes.json records the parent
interpreter that launched the worker, so identity is bound; the result is merely less
self-describing. Suggest emitting the same 'ready' event for completion phases.

### F-05 Advisory - per-attempt host input files are overwritten

tools/v0a_eval_panel_completion.py:297-300 writes host-input.json and host-blueprint.json
at fixed names for every attempt; only the last attempt's files survive on disk.
Each retained session report carries input_sha256, blueprint_artifact_sha256, the
witness and the frame stream, and coverage.md item 9 acknowledges the reuse, so identity
is preserved. Per-ordinal names would add on-disk retention at no contract cost.

### F-06 Advisory (process) - the hygiene check mutates the worktree

checks/hygiene.py rewrites changed files with normalized line endings as a side effect
of a check. The frozen blob digests equal hygiene.json's rows, so the receipt describes
the candidate; a check should nevertheless not modify the bytes it certifies.

### F-07 Advisory (limit) - full-H agreement result size

witnesses() emits one witness_draw observation per draw (:172-173) and the witness_scan
report repeats the draws list (:176-177); each host_attempt embeds the whole session
report with base64 child stdout. A full-H run can produce a result of tens of MB. No
later phase reads the agreement result through the 16 MiB OwnedInput, so no functional
effect; noted as an operating limit for the later plan.

## 5. Tier C trace: no path manufactures a hit

- A 'hit' requires (eval_agreement.py:239-255, 289-303): session and nested hand
  completed with null failure causes; capture untruncated and child exit 0; a complete
  NDJSON stream with strict duplicate-key/nonfinite refusal, ready/hand_result/
  session_result closure, exact frame field sets, action/event_result pairing, every
  event_result accepted or decided with null failure, v1 DecisionRecord shape and
  completed timing; identity binding of ready, hand and outer report to the same commit
  and blueprint digest and to the derived session/child ids; kernel replay of the
  applied history reproducing the host settlement and the event count; exactly one
  river record; replayed key equal to the declared s=4 root key; the teacher containing
  the hand; the classifier's own PreparedBlueprint.action_for reporting table_hit; the
  record's selected_action equal to both the replayed action and the teacher; the
  record's blueprint_sha256 and selection_reason equal to the independent lookup; no
  other cause. Missing river record, duplicate, in-pool default, relabeled reason,
  unknown reason, wrong action, off-root hit and tampered state hashes all yield
  disagreement; failures yield excluded with chips null.
- The host's v1 vocabulary is exactly table_hit/passive_default (v0a/model.py:60-62,
  runtime.py:1298-1302); the host verifies state hashes but not selection_reason
  (v0a_table_host.py:796-815), so the classifier's independent lookup is the only reason
  oracle and it is applied (:276-284). Provider labels blueprint_hit/blueprint_default
  are used only in validate_membership (eval_bridge.py:405-409), never for records.
- Coverage of H cannot be inflated: agreement() requires 'hit' for every H hand in
  permutation order (completion.py:345-348); complete() re-checks count+3 scheduled and
  observed ordinals, hand names equal to plan['permutation'][:count], every primary
  'hit' and the three control outcomes (:403-416); accounting() ties each outcome to its
  scheduled ordinal/hand/label/witness and lists missing pool hands (:439-463);
  summarize refuses observed > scheduled (:314-315). Test subsets keep their coverage
  label through summary and complete().
- Teacher and wire identities: teacher bytes are canonical ASCII JSON validated against
  the fixed domain, full permutation, nonempty exact prefix H and the s=4 settlement law
  bet_total == 2*check_total (eval_bridge.py:252-308); export consumes bytes only, is
  compared with a repeated encode, decoded and compared as a complete key/action map,
  and sized against the cap (:363-382, completion.py:262-268); the agreement phase
  re-exports and requires byte equality with the bound wire (:320-322); the child's
  ready.blueprint_sha256 must equal decode(wire).digest in both the host and the
  classifier.
- Witnesses: dealer output is unchanged and sorted; only board collisions among all
  twelve private cards reject; first witness wins; missing coverage fails before any
  host attempt (:328); the bank is part of the immutable admitted plan.
- Ownership: the worker runs with cwd ROOT and PONTIUS_RUN_CONTEXT set (panel :436-441);
  play() re-checks cwd == context root == ROOT before every Session (:288-289);
  Session.prepare -> Admission -> Source uses the inherited context with no rescan;
  Session.run never calls finish_run; the parent writes one result and one journal row.

## 6. Design verdict: SOUND

The shape fits the contract: a pure library classifier with two separate eligibility
values, bridge functions that consume immutable bytes, a helper that only orchestrates
already-reviewed real boundaries (Session, host child, dealer, codec, provider), and the
unchanged supervisor as the single execution entry with parent-side reconciliation.
Strain is limited to ordinary duplication (three separately loaded host module
instances, reconciliation logic split across complete()/accounting()/summarize) and
does not invite the failure class this checkpoint guards against.

## 7. Coverage comparison (inventory vs coverage.md)

Every inventory requirement R1-R11 and failure case F1-F14 maps to a coverage.md item
1-15 or to a frozen test I located. Agreements: item 9 acknowledges my F13 (input file
reuse); item 12 states the manifest-field limit I derived from bind_identity; item 11
matches the real-host event-count RED and the showdown accounting in replay(); item 4
states the tie-absence limit exactly as design section 3 requires. Not addressed by
coverage.md: the provenance of the two prerequisite constants (F-01), the absent 'ready'
event for completion phases (F-04) and the baseline/off-pool label overlap (F-03).
Coverage.md's discovery method (per-boundary map with labeled fixtures versus real
boundaries) is sound; its claim that fixtures never fabricate transport success holds:
the only real-host failure control raises after an actual native send
(test_eval_completion_tool.py:134-140).

## 8. Receipts assessment (implementer evidence, not a cold pass)

- focused-receipt.json/focused-journal.jsonl: candidate 449a2a3c..., snapshot worktree,
  venv Python 3.14.6, -B -P, ResourceWarning and unraisable warnings as errors, scrubbed
  environment (SystemRoot, TEMP, TMP, PONTIUS_GIT, PYTHONDONTWRITEBYTECODE), exit 0,
  78 unittest cases across the five suites, source_verified true; the journal row's
  output_sha256 48e4d157... equals the pinned checks/focused-result.json digest.
- hygiene.json: nine rows whose SHA-256s equal the manifest blobs and dependency pins;
  production 2,008, tests 1,781; ruff clean. The script's rewrite side effect is F-06.
- scope-check.json numstat equals my git diff --numstat; protected blobs unchanged agrees
  with my dependency check (35 of 36 candidate paths identical to the parent).
- admission-receipt.json: read-only admission at the candidate of a declared-full solve
  plan binding the three prerequisites; changed pool_count, resource and pool_seed all
  refused. It is the sole provenance for the two constants (F-01).
- RED transcripts: module-absent RED (11 tests), failure-type, frame-field, identity and
  settlement-type REDs, and the real-host 'wire:event_count' RED on a genuine CHECK
  capture; all labeled dirty-tree, none source-verified, consistent with the fixes in the
  frozen bytes. Three further REDs are unretained (F-02).
- No broad suite, no retained solve/export/agreement, no full-H census exist; the
  receipts establish focused correctness on a two-hand subset only.

## 9. Line counts and hygiene (from raw frozen bytes)

Changed blobs: eval_agreement.py 326, eval_bridge.py 521 (+189/-1), cases.json 51
(+4/-1), test_eval_agreement.py 383, test_eval_completion_tool.py 297,
test_eval_export.py 153, v0a_eval_panel.py 674 (+44/-3), v0a_eval_panel_completion.py
487. All eight are LF-only, BOM-free, end with LF, have no line over 100 columns and no
trailing whitespace. Checkpoint delta: +1,046/-4 production, +833 test lines.
Whole Slice A at the candidate: production 2,008 (521+326+674+487), tests 1,781
(198+750+153+383+297). This exceeds the 1,200/600 working figures and the r003
projection of 1,000-1,100 production lines, and stands at 67% of the 3,000 hard
ceiling recorded in addendum 2 and the correction authorization. Raw line counts here
and in hygiene.json count every line; r003's 792/428 evidently used another method, so
the projection comparison is approximate. Exact-type discipline (type(x) is int/str/
dict/list, is True/is False) is used on the evidence paths I traced.

## 10. Verified boundaries and limits

- Verified: identity, manifest, pins, dependency inventory, hygiene, the frozen source
  semantics traced in section 5, and agreement between the classifier's expectations and
  the unchanged host/session/runtime/dealer at the candidate.
- Not verified and not verifiable from the allowed inputs: the provenance of the two
  prerequisite result digests (F-01); any test outcome (receipts assessed, not
  reproduced); resource adequacy of any full-H phase; the size of a full-H agreement
  result (F-07). No claim about teacher strength, tie census, or host agreement over H
  follows from this review.

## 11. Prohibitions statement

I did not open any reviews/ directory, progress.md, INDEX.md, any disposition, readiness,
adoption, publication or retirement file, any other round or task packet, any
implementer transcript or session log, or any other reviewer's scratch directory. I did
not read source from the working tree of D:/Pontius; all source came from
`git cat-file blob 449a2a3c...:<path>` (and the parent for diffs). Git use was read-only
(rev-parse, cat-file, diff-tree, diff, ls-tree). No project code, tests, tools, uv/pip or
hooks were run; utility scripting used only CPython 3.14.6 at
C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe plus coreutils
sha256sum, labeled reviewer arithmetic, not test receipts. The only files written are
inventory-02-claude.md and review-02-claude.md in my scratch directory
D:/Pontius/tmp/eval-completion-r001-review-02-d0c7b90f (temporary helper scripts and blob
dumps lived in the session scratchpad outside D:/Pontius). Exposure to disclose: an
initial `ls` of the packet listed the file names under checks/ and the existence of
reviews/ before my inventory was written; no contents of either were read then, and the
names were already enumerated in supporting-files.json. No other exposure occurred.
