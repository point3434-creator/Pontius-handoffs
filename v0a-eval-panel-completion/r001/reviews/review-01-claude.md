# Cold review 01 (Claude): v0a-eval-panel-completion/r001

Verdict: CLEAN. Design verdict: SOUND.
Round kind: NEW-SURFACE, Tier C. Reviewer 01, bottom-up from the frozen blobs.
Candidate 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13, parent
beb84be566aa28029284bd35c526d33cd27af369, tree 09d78e4ede52a9093fc7941270d497a7362706dc,
manifest f58d6ed822787f0766c23ee63540ddc999784ad11d03dc103a1cbf80f68c0194.
Every finding below binds to that commit and manifest. Line numbers cite the frozen blob
(`git cat-file blob <commit>:<path>`), never the working tree.

## 1. Identity results (from Git objects, not packet claims)

- refs/heads/review/v0a-eval-panel-completion/r001 -> 449a2a3c...; `rev-list --parents`
  shows exactly one parent, beb84be5...; `rev-parse 449a2a3c^{tree}` = 09d78e4e...;
  commit message "Freeze eval panel bridge completion r001". All match candidate.json.
- `diff-tree -r --no-renames` parent..candidate lists exactly eight paths: A
  src/pontius/eval_agreement.py, M src/pontius/eval_bridge.py, M tests/cases.json, A
  tests/test_eval_agreement.py, A tests/test_eval_completion_tool.py, A
  tests/test_eval_export.py, M tools/v0a_eval_panel.py, A tools/v0a_eval_panel_completion.py.
  No deletions, no typechanges.
- Manifest recomputed as `<sha256>  <path>\n` rows over raw blob bytes, whole rows sorted
  bytewise: byte-identical to manifest.sha256; digest f58d6ed8..., equal to the stated one.
- supporting-files.json self-digest 3041c7fb... matches handoff.md; all 27 pinned files
  (8 inputs, 19 checks) verified. brief.md 1822e87a..., coverage.md 95578e84...,
  operating-boundary.md cfb1a43f... match the handoff.
- inputs/dependencies.json: all 42 rows verified at their stated commits (README and
  workflow at b6f8b08f in D:/Pontius; accepted brief/design at beb84be5; three handoff
  inputs at 2943f935 in D:/Pontius-handoffs; 35 source/test/config/fixture blobs at the
  candidate). Every packet copy matches its pinned blob. It is a direct inventory of the
  modules the changed code imports or launches plus the run-record owners and pinned
  config, not a transitive closure (package `__init__` files and second-level imports are
  absent). Treated as such.

## 2. Inventory reference

D:/Pontius/tmp/eval-completion-r001-review-01-6392f503/inventory-01-claude.md
SHA-256 290949bacfaf50c43021bcf1f4a233245beba349dd3aaa25b8192e9d739783e9
(written and hashed before coverage.md, operating-boundary.md or any checks/ file was
opened; 12 requirements, producer/caller/consumer paths for every computed value, nine
failure-case groups, five items deferred to the receipts).

## 3. Findings, severity-ordered

No Critical or Important finding survived verification. Each candidate path by which a
missing record, a default or a failure could become a table hit was traced and closed by
frozen code; see section 4. The items below are Minor evidence/reconciliation gaps and
Advisory notes; none is a required correction.

### M-01 Minor (evidence limit): full-pool prerequisite digests are not verifiable cold
- Location: tools/v0a_eval_panel_completion.py:18-22 (`PREREQUISITES`), 112-132.
- Requirement: brief.md mechanism 1 ("Full runs bind the actual retained capacity/preflight
  bytes and controller decision"); handoff: verify from frozen source and allowed inputs.
- Observation: the `decision` digest equals inputs/resource-decision.md (037a0de1...,
  verified). The `capacity` (29f532a9...) and `preflight` (8a17325e...) digests match no
  blob in the frozen tree (14 files under experiments/results/runs, none matching) and no
  line in the frozen execution_journal.jsonl; checks/admission-receipt.json names files
  under D:/Pontius-worktrees/eval-panel-prerequisite-20260909, outside the allowed inputs.
- Why not a defect: a wrong or absent file refuses admission (digest mismatch, phase,
  permutation digest and sample_complete predicates at lines 119-132), and export
  re-measures the actual wire against the cap (eval_bridge.py:371); no false success path.
- Smallest correction (packet, not source): when the solve plan is frozen, pin the two
  retained result files (bytes or an allowed-input digest plus their journal lines) so a
  cold reviewer can confirm the constants bind runs a89932e7 and 7ce5ab4f.

### M-02 Minor (reconciliation gap): primary attempts' wire identity is not reconciled
- Location: tools/v0a_eval_panel_completion.py:403-416 (`complete`), 439-463
  (`accounting`); identity available at 310-311 (`blueprint_wire_sha256`) and in
  `session['blueprint_artifact_sha256']` (tools/v0a_table_session.py:215).
- Requirement: design s1/s4 "keep distinct identities ... encoded wire artifact";
  accepted brief crit 8 "test artifact identity ... never transfer to the production
  artifact".
- Observation: `agreement()` plays primaries with the plan-bound wire by construction
  (line 346), but the parent-side reconciliation never checks that each primary's retained
  `blueprint_wire_sha256`/`blueprint_artifact_sha256` equals
  `plan['inputs']['blueprint']['sha256']`, nor that the three controls carry the control
  artifact digests. classify does bind the canonical digest (eval_agreement.py:104-105),
  so a hit cannot be attributed to a different policy; only the wire-byte identity is
  unreconciled.
- Smallest correction: in `complete()` require the primaries' retained wire digest to equal
  the bound blueprint digest and the controls' to equal the emitted control artifacts.

### M-03 Minor (preference): `summarize.complete` tolerates `unsupported`
- Location: src/pontius/eval_agreement.py:326; consumer at
  tools/v0a_eval_panel_completion.py:459 (`accounting()['primary']`).
- Requirement: design s5 "final acceptance requires complete required coverage".
- Observation: `complete = not (missing or disagreement or excluded)`. For the production
  primary set an in-pool default is a `teacher_disagreement` (line 300-301) and the worker
  stops at the first non-hit (line 347), so a completed run cannot reach this. In a failed
  run whose last observed primary was `unsupported` and nothing is missing,
  `agreement_accounting.primary.complete` reads True while `phase_complete` is False.
- Smallest correction: derive the accounting flag from `hits == scheduled` (or pass the
  required-hit semantics into `summarize`) so the sub-field cannot read True without hits.

### A-01 Advisory (missing test): v2 frame path unexercised
- src/pontius/eval_agreement.py:111-112, 152-155 and `bind_identity` v2 naming (70-79)
  handle baseline (protocol v2) captures, but every fixture in tests/test_eval_agreement.py
  uses protocol v1 and v1 ids even with `baseline=True` (line 32-34, 110-117). The Slice B
  chip-eligibility interface for real baseline sessions is therefore untested here. Not a
  Slice A requirement; noted for the Slice B checkpoint.

### A-02 Advisory (design): three loaded copies of tools/v0a_table_host.py per worker
- `load_tool('v0a_table_host')` (completion.py:30-44, used at 59), `load_host()`
  (v0a_eval_panel.py:82-89) and `Admission` (v0a_table_session.py:41-61, alias
  pontius_v0a_table_session_host) each execute the same file under a different module
  name. Exception classes (`HostRefusal`) are distinct per copy. Harmless today because
  `bound_bytes` catches nothing by class; a future `except host.HostRefusal` would miss
  refusals from another copy. One shared loader would remove the hazard.

### A-03 Advisory (limit): agreement result growth
- Every witness draw is emitted (completion.py:172-173) and repeated inside the
  `witness_scan` report (`draws`, line 176); every attempt retains the complete session
  report including `child_stdout_base64` (line 341-342). `validate_bank` admits up to
  65,536 x 16 draws. `finish_run` has no size guard; `bound_bytes` limits a later consumer
  to 16 MiB. Plan the bank size with this in mind; not a defect for this checkpoint.

### A-04 Advisory (receipt provenance)
- checks/hygiene.json names an executable from a different worktree venv
  (eval-timing-check-r002-broad) and checks/hygiene.py rewrote CRLF-normalized bytes into
  the worktree before the freeze. The counts (production 2008, tests 1781) were reproduced
  independently from the frozen blobs (section 6), so the receipt's numbers stand.

### A-05 Advisory (failure path)
- `accounting()` can raise (completion.py:447-458) from inside `supervise`
  (v0a_eval_panel.py:521) after cleanup; main records the failure but skips `retain()`,
  leaving control artifacts as base64 inside observations. Fail-safe and retained; a
  try/except that records the accounting refusal in the report would keep retention.

## 4. Verified invariants (bottom-up), with the paths that establish them

- Teacher identity: `teacher_bytes` (eval_bridge.py:311-332) emits canonical ASCII JSON
  only after `_teacher_validate` (252-308): exact field set, fixed domain, canonical board,
  full 1081-hand permutation, nonempty exact prefix H, ordered rows, exact ints, denominator
  990, bet == 2*check, CHECK-first maximizing action, consistent optional counts/work.
  `teacher_actions` (335-343) refuses non-bytes and any non-canonical re-serialization
  (duplicate keys, whitespace, NaN, spelling). source_id = 't1:' + sha256(raw) (369),
  canonical codec identity = decoded.digest (380), wire identity = sha256(wire) (380).
- Export without solving: `export_teacher` (363-382) only encodes supplied rows; wire size
  is checked against the cap before decode (371); decoded source_id, entry count and the
  exact key->action map are required equal (373-378). Repeat byte-equality is enforced by
  the caller (completion.py:262-264). Test patches `hand_totals` to assert no recomputation.
- Membership: `validate_membership` (385-421) walks all 1081 root hands through
  `PreparedBlueprint.action_for` and the public `BlueprintProvider.propose` with real
  `DecisionObservation` values; complement must default with reason `blueprint_default`;
  `passed` requires exact entries and zero disagreements. Provider labels are used only
  here; the v1 `selection_reason` is checked separately in classify.
- Witnesses: `witnesses` (completion.py:149-180) scans the admitted bank in declared
  order via the unchanged `deal_for_hand` (sorted two-card hands, 12 distinct cards),
  rejects only board collisions across all twelve cards, keeps the first witness per
  required hand, retains unused draws and collisions, and reports `complete` only when the
  selected set equals the required set; `agreement()` refuses otherwise (328).
- Session reuse: `play` (282-311) requires cwd == inherited root == ROOT, builds a fresh
  `Session` per attempt (real `prepare`, real child), and never journals: `Session.run`
  does not call `finish_run`; `begin_run(inherited=...)` (execution.py:40-44) does no scan
  and `finish_run` returns for inherited contexts (124-125); the child adapter inherits
  the same context. One journal row per invocation comes only from main (669).
- Outcome gate: `classify` (eval_agreement.py:223-258) reads `hands[0]['result']`, needs
  outer/nested cleanliness and completion, no truncation, exit 0, strict NDJSON with
  duplicate-key/NaN/1e9999 refusal (51-66, 94-96), fixed ready/hand_result/session_result
  positions, identity binding across ready/hand/report (69-88), exact frame field sets,
  action/event pairing with contiguous indices, no failed event, timing completed within
  limits, v1 DecisionRecord shape, terminal/closure accounted, and settlement equality
  terminal vs hand vs kernel replay (169-172, 217-219). Any failure -> `excluded`,
  chip_eligible False, chips None, cause retained.
- Replay: `replay` (176-220) re-applies `applied_actions` through
  `NoLimitBettingState` from the declared initial state, checks order/origin, records the
  expected per-decision fields including state_before/after and visible-cards digests
  (which bind the caller-supplied hero hand to the child's record), counts events exactly
  as the host does (street advance, opponent action, one showdown_result; confirmed
  against tools/v0a_table_host.py:241-302 and no_limit_betting.py:588-613), and settles
  with the kernel.
- Agreement gate: chips come from the kernel (`net_returns[2]`); classification starts as
  `unsupported`; baseline strategy stays chip-eligible and unsupported (264-266); record
  count, replayed fields, own lookup (`prepared.action_for`) vs record action, reason and
  blueprint digest, passive pre-river reasons, exactly one river record, river key ==
  declared s=4 root key, teacher present, table hit, action equal and no other cause are
  all required for `hit` (267-309). Off-pool default at the root -> unsupported; hit outside
  teacher pool or declared root -> disagreement; relabeled CHECK hit/default -> disagreement.
- Orchestration: admission (`validate`, 97-146) is exact-member, phase-specific, refuses
  test subsets with prerequisites or count 1081, and requires the fixed envelope for a
  full solve; each phase is a separate invocation with its own bound plan; the worker
  re-validates; `complete` (376-436) and `accounting` (439-463) reconcile census rows,
  tie reference, artifacts (bytes, size, digest, recomputed teacher), scheduled versus
  observed attempts with ordinal/hand/label/witness equality; controls are excluded from
  the primary summary (367-368); `retain` (466-487) binds identity before rename and
  reconciles an interrupted publication.

## 5. Coverage comparison (inventory versus coverage.md)

- All fifteen coverage items map onto inventory sections B/C; none claims more than the
  frozen code establishes. Item 11's showdown-count correction is corroborated by the
  retained real-host RED log and by my own host/kernel event trace. Item 12's stated limit
  (ready source-manifest SHA checked for format only) matches eval_agreement.py:82-88.
- Not stated in coverage.md: the untested v2 frame path (A-01), the unreconciled wire-byte
  identity of primaries (M-02), the accounting `complete` semantics (M-03) and the result
  size growth (A-03). None is an unmet acceptance requirement; they are gaps in the claim,
  not product defects.
- Coverage's evidence section correctly disclaims the export/accounting RED outputs that
  exist only in tool history; that is a receipts limitation, disclosed, not a defect.

## 6. Receipts assessment (implementer evidence, not reproduced)

- focused-receipt.json: candidate 449a2a3c..., snapshot worktree, CPython 3.14.6, scrubbed
  environment (SystemRoot, TEMP, TMP, PONTIUS_GIT, PYTHONDONTWRITEBYTECODE), `-B -P -W
  error::ResourceWarning`, pytest with unraisable warnings as errors, `-k` over the five
  suites; exit 0. focused-stdout: 5 passed, 44 deselected. focused-journal: one row,
  source_commit = candidate, source_verified true, 78 cases, 0 skipped, output_sha256
  48e4d157... = the pinned focused-result.json digest. focused-result.json lists 11 + 29
  + 8 + 21 + 9 tests, all OK, including the real-host and three-phase CLI tests.
- snapshot.ps1 creates a detached worktree, `uv sync --locked --offline`, asserts 3.14.6,
  clears the environment; consistent with the receipt. freeze.ps1 is create-only.
- classifier-red*.txt: availability RED (module absent, 11 failures) and four dirty-source
  boundary REDs (False failure_reason, missing ready field, swapped ready commit, boolean
  payouts each yielding `hit`) plus the real-host event-count RED (`excluded` instead of
  `hit`). Labeled as dirty observations; the frozen suites assert the corrected behavior.
- admission-check.py / admission-receipt.json: read-only admission of a declared-full
  solve plan, refusing changed count/envelope/seed; the prerequisite files are outside my
  inputs (M-01). No phase was invoked.
- scope-check.json: eval_bridge existing functions unchanged; tools entry changed only in
  validate_plan/run_plan/supervise/main; protected blobs unchanged. Agrees with my diffs.
- hygiene.json: ruff clean; counts agree with section 7. Provenance note in A-04.
- Absent: raw REDs for teacher/export availability and the accounting orphan case
  (disclosed as tool-history only). Missing receipts, not evidence of a defect.

## 7. Line counts, budget and hygiene (reviewer arithmetic from raw frozen bytes)

- Changed blobs: eval_agreement.py 326, eval_bridge.py 521 (+189/-1), cases.json 51
  (+4/-1), test_eval_agreement.py 383, test_eval_completion_tool.py 297,
  test_eval_export.py 153, v0a_eval_panel.py 674 (+44/-3), v0a_eval_panel_completion.py
  487. Checkpoint delta 1883 insertions, 5 deletions.
- Whole Slice A surface: production 2008 raw lines (1794 non-blank) over eval_bridge,
  eval_agreement, v0a_eval_panel, v0a_eval_panel_completion; tests 1781 raw (1590
  non-blank) over the five suites. Matches hygiene.json (2008 / 1781). Above the 1,200 /
  600 working figures, below the 3,000 production hard ceiling; addendum 2 and the
  correction authorization make this a disclosure, not a return to the controller.
- All eight changed blobs: LF-only, BOM-free, no CR bytes, no line over 100 columns, no
  trailing whitespace, ASCII only, final newline present.
- Exactness: `type(...) is int/float/str/dict/list` discipline is used on every evidence
  path I traced (eval_agreement.py:40-48, 86-87, 123, 249-250, 314; completion.py:48-54,
  83-93, 109). Cosmetic only: a double blank line inside a class at
  tests/test_eval_agreement.py:248-249.

## 8. Design verdict: SOUND

The shape fits the contract: one classifier owns outcome-then-agreement interpretation
with every exclusion carrying a cause; export is a pure function of immutable teacher
bytes; membership and host agreement are separate reports; admission is exact-member and
phase-specific; reconciliation lives in the parent. The findings are ordinary evidence and
reconciliation gaps, not symptoms the shape invites. Two strains worth naming without
changing the verdict: reconciliation semantics are spread over four predicates (worker
`require`, `summarize`, `complete`, `accounting`) whose notions of "complete" differ
(M-03), and the host module is loaded three times per worker (A-02).

## 9. Verified boundaries and limits

- Verified: identity, eight-path scope, manifest, all pins, dependency inventory at its
  stated bases; the frozen consumers read at the candidate (host, session, adapter entry,
  dealer, execution, cards, betting, key/codec, provider, lookup, model).
- Not verifiable from allowed inputs: the two retained prerequisite result files behind
  the hard-coded digests (M-01); the runtime behavior of the v2 protocol path (A-01).
- Not established by this checkpoint (and not claimed): any retained solve, export or
  agreement result, tie census, full-H host coverage, poker strength or Slice B estimand.

## 10. Prohibitions statement

- Opened: handoff.md, candidate.json, manifest.sha256, brief.md, supporting-files.json,
  every inputs/ file, raw frozen blobs via `git cat-file`/`diff-tree`/`diff`/`ls-tree`/
  `rev-parse`/`rev-list` (read-only), then, after the inventory was written and hashed,
  coverage.md, operating-boundary.md and every checks/ file.
- Not opened: reviews/ (any packet), progress.md, INDEX.md, any disposition/readiness/
  adoption file, any other round or task directory, any worktree, any other reviewer's
  scratch directory, any transcript. No project code, tests, tools, owners, uv/pip or hooks
  were run; utility scripting used only CPython 3.14.6 at the named path plus git
  read-only commands. No file under D:/Pontius or D:/Pontius-handoffs was modified other
  than the two files in my scratch directory, created exclusively.
- Exposure to disclose: one `ls -la checks/` listing was issued while surveying the packet
  before the inventory existed; it surfaced file names and sizes only, no contents. The
  harness system prompt carried an auto-memory index whose one-line summaries mention the
  eval-panel lane's earlier rounds (r001-r003 states); those memory files were not opened
  and nothing from them entered this review's inventory or findings.
