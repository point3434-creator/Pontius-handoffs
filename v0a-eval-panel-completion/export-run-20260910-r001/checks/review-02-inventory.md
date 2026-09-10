# Sealed independent invariant inventory — export-run-20260910-r001 (cold pass, Claude)

Written and hashed BEFORE opening `checks/`, `rehearsal/`, `coverage.md`,
`authorization-request.md` or `next-phase.md`, per handoff read contract step 4.
Not revised after sealing.

Scratch: `D:/Pontius/tmp/export-r001-cold`.
Context probe: CONTEXT_PROBE_NONE (no memory index, transcript, verdict, disposition or
addendum text was present in the system prompt or any system-reminder; only a git-status
block, user e-mail, tool/skill listings and environment notes).

## A. Inputs read before sealing

Packet (manifest-listed unless noted): `handoff.md` (wrapper), `identity.json`,
`candidate.json` (wrapper), `manifest.sha256` (wrapper), `invoke.sh`,
`journal_attribution.py`, `plans/export.json`, `governing/brief.md`, `governing/design.md`,
`inputs/*` (all ten files).
Frozen Git at `1c7067448106cfa2aca3d57be879842d72293c61`:
`tools/v0a_eval_panel.py`, `tools/v0a_eval_panel_completion.py`, `src/pontius/execution.py`,
`src/pontius/eval_bridge.py`, `src/pontius/holdem_cards.py` (constants), `src/pontius/river.py`
(constants and `format_card`), `src/pontius/blueprint_artifact/codec.py` (header only),
`tools/v0a_table_host.py` (`OwnedInput` only), plus `ls-tree`/`cat-file` over the source scope.
No project module was imported; every re-derivation below is plain CPython 3.14.6 stdlib.

## B. Identity — established, not assumed

- I1. Manifest recomputation over raw bytes, rows `<sha256>  <relpath>`, whole-row byte
  sort, LF separators **and a trailing LF**, excluding `handoff.md`, `candidate.json`,
  `manifest.sha256`: 47 members, digest
  `9965a225729a5896818127c013122f62fb3ae323889fde8ab16ea35e3e43eb17`. Matches
  `candidate.json.manifest_sha256` and `manifest_members`. The manifest FILE is byte-identical
  to that canonical blob (its own sha256 equals the manifest digest); no CRLF; already sorted.
  Without the trailing LF the digest would be `3f4a32e5...`, so the trailing LF is load-bearing
  and the packet's rule statement is exact.
- I2. Every non-manifest artefact in the directory (`reviews/`, `finalization/`,
  `disposition.md`, `finalizer-addendum.md`, `authorization-template.txt`,
  `checks/review-01-inventory.md`) is OUTSIDE the 47 members; excluding them left the
  digest exact, which independently confirms the freeze boundary without opening them.
- I3. `1c7067448106cfa2aca3d57be879842d72293c61` is a commit in `D:/Pontius`; its tree is
  `3d2fe79d2af20125e322dd4a668335e789810863`, equal to `identity.json.source_tree` and
  `candidate.json.tree`.
- I4. `governing/brief.md` and `governing/design.md` are byte-exact frozen blobs:
  `git hash-object` gives `1c26704c387b5894cab5be12ae9843a4c41b32ca` and
  `fda51e07d045eba1a087b1dd392aa273e87865b4`, equal to the commit's
  `docs/architecture/v0a-eval-panel-impl-r001/{brief,design}.md` blob ids. (They are NOT the
  parent-lane `v0a-eval-panel-r001` documents; the packet's wording "exact source-commit
  blobs" is true of the impl-r001 pair.)
- I5. `inputs/source-scope-blobs.json` reproduces exactly: 892 entries over
  `src tools tests .github pyproject.toml uv.lock .gitattributes`, all mode 100644 blobs,
  every `git_blob`, `bytes` and raw-byte `sha256` identical to `git ls-tree` / `cat-file`
  output at the adopted commit; declared `count` and `tree` correct.
- I6. Digest self-consistency of all bindings: `plans/export.json` = `c55f26f6...` (12838 B) =
  `identity.plan.sha256` = `candidate.plan_sha256` = wrapper `PLAN_SHA`; `invoke.sh` =
  `c70c9dea...`; `journal_attribution.py` = `a20e760a...` = wrapper `ATTRIBUTE_SHA`;
  `inputs/solve-wrapper-r004.sh` = `160cfcec...` = `candidate.predecessor_wrapper_sha256`.

## C. Plan invariants re-derived independently (stdlib only)

Deck model taken from frozen source: `DECK = range(52)`, `card = rank_index*4 + suit_index`,
`RANKS="23456789TJQKA"`, `SUITS="cdhs"`.

- P1. Board `["2c","7d","9h","Js","Qc"]` maps to ints `(0,21,30,39,40)`, strictly ascending,
  five distinct cards; equals `DEVELOPMENT_BOARD`, which `completion.validate` requires for
  `declared-full`.
- P2. Hero universe = C(47,2) = **1081** = `plan.hand_count` = `plan.pool_count` =
  `eval_bridge.HERO_COUNT`. Full census, not a prefix.
- P3. `hand_universe_sha256` recomputed as `sha256(json.dumps(sorted(names)))` =
  `18953f113d65c6e25111ac9c2441942e4145051e169261fecd0ed0b9e5be41ed` = plan value.
- P4. `permutation` recomputed as `random.Random(int(pool_seed,16)).shuffle(list(universe))`
  is **byte-identical to the plan's 1081-name list**; all names distinct. Its digest
  `sha256(json.dumps(names))` =
  `344e7eeb06d72b97313f470880b8d169c4674e83bb440de827fa6fb87d97648a`.
- P5. `prefix` equals `eval_bridge.prefix_document()`:
  `[[3,fold],[4,fold],[5,fold],[0,fold],[1,call],[2,check],null,[1,check],[2,check],null,[1,check],[2,check],null,[1,check]]`.
  `stacks` = 4 = `DECLARED_STACK`. `runtime` = `{"python":"3.14.6"}`.
- P6. Plan member set is exactly `COMMON_KEYS + {coverage, pool_count, prerequisites, inputs}`
  (15 keys), i.e. the export shape; **no `witness_bank`** (that member is admitted only for
  `agreement`). `version` = `pontius-eval-panel-completion-plan-v1`, `phase` = `export`,
  `coverage` = `declared-full`.
- P7. `inputs` = exactly `{teacher, producer_result}` — the set `completion.validate` requires
  for `export` (`solve` takes none; `agreement` adds `blueprint`).
- P8. **Envelope.** `resource` = `{seconds:600, memory_mib:2048}`. `completion.validate`
  constrains the envelope against the controller decision **only when `phase == 'solve'`**
  (frozen `v0a_eval_panel_completion.py`, the `if phase == 'solve'` branch inside the
  `declared-full` block). For `export` these numbers are therefore code-unconstrained and MUST
  be carried as a new proposal requiring the controller's separate approval.
  `inputs/prerequisite-decision.md` says so in terms: it adopts the envelope "for the
  full-pool T1 solve" and states that the full-pool solve, export and agreement runs each
  still need their own bound plan and one-shot authorization. Falsifier: any packet text that
  treats the 600 s / 2048 MiB export envelope as already authorized, or that cites the
  resource decision as authority for the export launch.

## D. Prerequisite invariants

- Q1. Frozen `PREREQUISITES` digests in the completion module are exactly capacity
  `29f532a9...`, preflight `8a17325e...`, decision `037a0de1...`; the plan's three
  `prerequisites` bindings carry those digests with absolute paths, and the copies in
  `inputs/` hash to the same values.
- Q2. Capacity result (`inputs/prerequisite-capacity.json`): `status=completed`,
  `phase=capacity`, `cleanup_verified=true`, `errors=[]`,
  `permutation_sha256 = 344e7eeb...` — **equal to my independently derived P4 digest**, which
  is what `completion.validate` recomputes. Probe: `all_fit=true`, `largest_fitting=1081`,
  `bytes_at_largest=1012625`, `bytes_at_next=null`, `cap=1048576`, `one_row_failure=false`,
  placeholder `t1:` + 64 zeros. Boundary artifact for 1081 retained,
  `boundary_retention=complete`.
- Q3. Preflight result: `status=completed`, `phase=preflight`, `coverage=declared-full`,
  `cleanup_verified=true`, `sample_complete=true`, `errors=[]`, same permutation digest.
  `full_pool_estimate` = 15.79 / 31.14 / 71.38 s over H, sample 4, `untraced-body-v1`.
- Q4. The decision document records the envelope's measured basis (peak worker Job about
  0.8 GiB; at least 8x time and about 2.5x memory headroom) on source `beb84be5...`, not on
  the adopted commit. The prerequisites are pinned by digest, not by source identity; nothing
  in the frozen code requires the prerequisite runs to have been produced at `1c706744...`.

## E. Producer (retained solve) invariants

- R1. `inputs/solve-result.json` = `e6db93c0...` = plan `inputs.producer_result.sha256`;
  `inputs/solve-teacher.json` = `c3ffab40...` = plan `inputs.teacher.sha256`. Both equal the
  wrapper's `PRODUCER_SHA` / `TEACHER_SHA` and `inputs/external-pins.json`.
- R2. Result fields: `status=completed`, `phase=solve`, `coverage=declared-full`,
  `cleanup_verified=true`, `phase_complete=true`, `errors=[]`, all twelve `cleanup` entries
  `ok`, `resource_state_verified=true`, `worker_exit_code=0`,
  `permutation_sha256=344e7eeb...`, `plan.pool_count=1081`, `plan.prerequisites` **identical
  to this plan's `prerequisites`**, `plan.board` and `plan.pool_seed` identical,
  `plan.resource={600,2048}`, `plan.runtime={"python":"3.14.6"}`, `plan.inputs={}` (solve
  takes none). These are exactly the predicates `completion.teacher_input` re-checks at run
  time.
- R3. Observations: 1081 `teacher_hand` + 1 `artifact` + 1 `solve_summary` = 1083. Row hands,
  in order, equal `plan.permutation[:1081]`. `solve_summary`: `complete=true`,
  `completed_hands=1081`, `coverage=declared-full`, `nonzero_tie=absent_in_completed_pool`,
  `teacher_sha256=c3ffab40...`.
- R4. The single artifact row is `teacher.json`, `bytes=241587`, `sha256=c3ffab40...`,
  `retention=complete`, `path=teacher.json`, and carries **no** `artifact_base64` (deleted by
  `completion.retain`). That is precisely what `teacher_input` demands
  (`row.sha256 == plan.inputs.teacher.sha256 and row.retention == 'complete'`).
- R5. Teacher bytes independently validated: the canonical
  `json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=True, allow_nan=False)`
  round trip is byte-identical to the file, so `teacher_actions`' canonicality equality will
  hold; members are exactly `{version, prefix, root, opponent, board, permutation, hands,
  rows}`; `permutation` equals the plan permutation (1081, distinct); `hands == permutation`
  (full census, not a proper prefix); `rows` is 1081 long. Every row passes the frozen
  `_teacher_validate` domain rules recomputed by hand: `denominator == 990`,
  `abs(check_total) <= 1980`, `check_total` even, `bet_total == 2*check_total`,
  `wins+losses+ties == 990`, `check_total == 2*(wins-losses)`,
  `work == {villain_hands:990, settlements:1980, ranker_calls:991}`, and
  `action == "raise-to-2"` iff `bet_total > check_total` else `"check"`, `bet ==
  "raise-to-2"`. Distribution: 545 `raise-to-2`, 536 `check`, and **0 rows with
  `check_total == bet_total`** — no exact tie exists in the completed census, which is why
  `nonzero_tie` is `absent_in_completed_pool` and why zero `nonzero_tie_reference` rows is
  the correct outcome under `completion.complete`.
- R6. `inputs/solve-journal-row.jsonl` is one row: `source_commit=1c706744...`,
  `source_verified=true`,
  `output=experiments/results/runs/ded0fe697fbe424aa40ffd5320940d4b/result.json`,
  `output_sha256=e6db93c0...` (matches R1), `runtimes_sha256=12af22dd...` (matches
  `inputs/solve-runtimes.json`), `status=completed`. `solve-runtimes.json` names CPython
  3.14.6 and the solve worktree venv. This is the shape `journal_attribution.py` demands.
- R7. `identity.json.producer.journal_commit` / `journal_branch` (`0872ba84...`,
  `claude/eval-panel-solve`) are *ownership* claims about the producing checkout, not
  verifiable from this packet's frozen bytes; they must be presented as a disclosed
  assumption, not as a checked fact.

## F. Wrapper invariants (`invoke.sh` versus the frozen tool)

I diffed `inputs/solve-wrapper-r004.sh` against `invoke.sh` myself before sealing. The changed
set is: header wording; `RETAINED_ROOT` to `eval-panel-export-20260910`; `PK` to
`export-run-20260910-r001`; `PLAN_SHA` to `c55f26f6...`; four new
`TEACHER`/`TEACHER_SHA`/`PRODUCER`/`PRODUCER_SHA` constants and the new exit-80 guard;
`SOLVE_ROOT` to `EXPORT_ROOT` including a **strengthened** retained-mode refusal
(`${VAR+x}` instead of r004's `${VAR:-}`, so an explicitly empty value is now refused);
`plans/solve.json` to `plans/export.json`; the six `solve-*` record names to `export-*`;
`"phase":"solve"` to `"phase":"export"` in both journal-log records; three echo strings.
Required bindings, each of which I will test against the packet's own artefacts:

- W1. `ADOPTED` = `1c7067448106cfa2aca3d57be879842d72293c61` (equals identity, candidate, plan
  source and the producer journal row's `source_commit`).
- W2. `RETAINED_ROOT` = `D:/Pontius-worktrees/eval-panel-export-20260910` = the
  `execution_checkout` in `identity.json`; distinct from the solve worktree that holds the
  producer inputs; `PK` = this packet.
- W3. `PLAN_SHA` = `c55f26f6...` and the launched argument is `"$ROOT/plans/export.json"` —
  the SAME file the precondition hashes (`sha plans/export.json` after `cd "$ROOT"`). No
  second path; no packet copy is passed to the tool. `--reviewed-commit "$ADOPTED"`.
- W4. `ATTRIBUTE_SHA` = `a20e760a...` = the packet's own `journal_attribution.py` (exit 82).
- W5. The prerequisite triple is checked as one predicate (exit 93); the producer pair is
  checked as one predicate (exit 80), and the exit-80 block sits **above**
  `mkdir "$OUT/claim.d"`, that is strictly before claim acquisition, as
  `identity.invocation.input_guard` asserts.
- W6. Mode and root refusals: `REHEARSAL` unset becomes `0`; when set it must be exactly `0`
  or `1` (empty gives exit 84). Retained mode refuses any *set* `EXPORT_ROOT` or
  `REHEARSAL_PK` (exit 88) and requires `$PK/authorization.md` (exit 89). Rehearsal mode
  requires a non-empty `EXPORT_ROOT` (87), an existing directory (90), a path whose `pwd -P`
  differs from the retained checkout (86) and a **detached** HEAD (85, `symbolic-ref -q HEAD`
  must fail).
- W7. Preconditions, each with its own code: HEAD equals ADOPTED (91), plan hash (92),
  prerequisites (93), attribution helper (82), producer inputs (80), interpreter exactly
  3.14.6 via `"$PY" -I -B -c "...assert..."` (94) — `-I` implies `-E`, so a hostile
  `PYTHONOPTIMIZE` cannot strip that assert; on-disk run dirs equal tracked run dirs (95);
  `git status --short` clean over
  `src tools tests pyproject.toml uv.lock .gitattributes .github` (96); none of the six record
  names already present (97); journal readable (81).
- W8. Claim: `mkdir "$OUT/claim.d"` is the atomic gate; failure gives 97 with a message that
  does not distinguish "already claimed" from "unwritable" (the script says so). The claim
  record and start record writes are checked (`|| exit 98`), and the start record is re-read
  with `grep -q '"event":"start"'`. The script contains no `rm`/`rmdir`: a claim is never
  removed.
- W9. Launch: exactly one `env -i` invocation with `SystemRoot`, `TEMP`, `TMP`, `PONTIUS_GIT`
  set to the absolute Git and `PYTHONDONTWRITEBYTECODE=1`; `-B -P -W error::ResourceWarning`;
  `PONTIUS_RUN_CONTEXT` is deliberately NOT inherited
  (`identity.child_environment.inherited_run_context = false`), so the tool performs its own
  `begin_run` source scan. `set -o noclobber` is armed around the redirections, so a
  pre-existing capture file makes the redirection fail and the child never starts.
- W10. Evidence: stdout/stderr existence; `wc -l` after; helper run under `-I -B` with
  `(journal, ROWS_BEFORE, ADOPTED, ROOT, out)`; `BOUND` required in field 1 AND `ATTR_RC==0`;
  digests of both captures; a row digest only when `BOUND`, else the literal `absent`;
  `retained-files.txt` listing `sha  bytes  path` for every file in every run directory NOT in
  `TRACKED_RUNS`; the end record appended. Every one of these can only *clear* `EVIDENCE`.
- W11. Exit precedence, textually: `rc != 0` gives `exit "$rc"` (printing `EVIDENCE
  INCOMPLETE` first when applicable); otherwise `EVIDENCE != complete` gives `exit 99`;
  otherwise `exit 0`. Required property: **no path prints DONE and exits 0 with incomplete
  evidence.**
- W12. Attribution helper semantics required: exactly one new row (else `ABSENT`/3 or
  `EXTRA`/4), row `source_commit == ADOPTED`, `output` a non-empty `str`, `root/output` an
  existing file whose sha256 equals `output_sha256`, and — when the row carries
  `runtimes_sha256` — a sibling `runtimes.json` matching it. Only then is the row copied to
  `<out>` with LF and `BOUND` printed. No older row may be substituted. Note for testing:
  `wc -l` counts newlines while the helper counts split rows, so a journal whose final row
  lacks a trailing newline would make the two disagree; that disagreement can only produce
  `EXTRA` (evidence incomplete), never a false `BOUND`.

## G. Tool-path invariants the packet's evidence must satisfy

From frozen `tools/v0a_eval_panel.py`, `tools/v0a_eval_panel_completion.py`,
`src/pontius/eval_bridge.py` and `src/pontius/execution.py`:

- T1. `main` always creates a fresh `experiments/results/runs/<uuid4hex>` and writes
  `runtimes.json` before reading the plan, so a launched child always leaves at least one new
  run directory for `retained-files.txt` to list; `finish_run` writes `result.json` into it
  and appends exactly one journal row **including on failure**. Exit is `0` iff
  `report["status"] == "completed"`.
- T2. `begin_run(ROOT, reviewed_commit=ADOPTED, allow_working_tree=False)` re-verifies the
  whole source scope against the reviewed commit's blobs (CRLF-normalised for text suffixes)
  and raises unless equal — a second, in-process check independent of the wrapper's
  `git status`. `--development` is not passed.
- T3. `completion.validate` for `declared-full` + `export` requires: the member set of P6; a
  `capacity`-shaped re-validation of the common members; `pool_count == HERO_COUNT` and the
  declared board; the three prerequisite digests equal to the frozen constants, each read
  through `OwnedInput` (stat identity plus size bound) and re-hashed; capacity result
  `status`/`cleanup_verified`/`phase` plus **a permutation digest recomputed from the plan's
  own board and seed**; preflight `sample_complete is True`; inputs exactly `{teacher,
  producer_result}`, each an absolute path with a 64-hex digest.
- T4. `completion.teacher_input` re-reads and re-hashes both producer inputs at run time;
  requires the teacher's canonical serialization, its board and its first `pool_count` hands
  to equal the plan's, its full `permutation` to equal the plan's, and the producer result to
  be `status=completed, phase=solve, cleanup_verified=True, phase_complete=True,
  coverage == plan.coverage`, with the producer's own `pool_count` and `prerequisites` equal
  to this plan's and its `permutation_sha256` recomputed. The teacher must appear as a
  `retention=complete` artifact row of that producer result. Failure of any of these raises a
  `ValueError` inside the worker, which emits `event:"failed"`, populates `errors`, forces
  status `failed` and exits 1.
- T5. `completion.export` must, in order: bind the teacher; encode once under `measure`;
  encode a **second** time and require byte equality; emit `export_encoding`; run
  `validate_membership` and require `passed`; emit both artifacts; emit `export_summary`. Two
  budget checks bracket the work.
- T6. `eval_bridge.export_teacher` refuses a `cap` outside `(0, 1048576]`, builds one entry per
  hand from `BlueprintDecisionKey.from_state` on the replayed root (after traversing the legal
  shape to prove the singleton hero decision), sets `source_id = "t1:" + sha256(teacher
  bytes)`, refuses `len(wire) > cap`, and re-decodes to require an identical `source_id`,
  entry count and key-to-action map. The report's `cap` is therefore the full 1048576 host
  cap, not a narrower declared bound.
- T7. `eval_bridge.validate_membership` enumerates **all 1081 board-compatible hero hands**
  (not just H), checking `PreparedBlueprint.action_for` key/`table_hit`/action AND a real
  `BlueprintProvider.propose` with a constructed `DecisionObservation` (reason
  `blueprint_hit`/`blueprint_default`, action, and the `decision_sha256` echo). Its `scope` is
  the literal string `exhaustive_library_provider_root`. With H equal to the whole universe,
  `hits` must be 1081 and `unsupported` 0, so **this run exercises no off-pool default at
  all**: brief criterion 4's complement claim and criterion 8's off-pool control are NOT
  established by this phase. Falsifier for the packet: any text reading `membership.passed` as
  host agreement, as complement coverage, or as evidence about teacher strength.
- T8. `completion.complete(observations, plan)` for `export` requires exactly one
  `export_summary` with `complete is True` and matching coverage, exactly one `membership` row
  with `report.passed is True`, and exactly the artifact set `{teacher.json, blueprint.json}`
  with base64-to-bytes length and digest agreement and the teacher's hands equal to
  `permutation[:pool_count]`. It is computed **before** `completion.retain` strips
  `artifact_base64`.
- T9. `supervise` downgrades `completed` to `failed` if `errors` is non-empty, if
  `cleanup_verified` is false (which requires `resource_state_verified` — job active count 0,
  worker exit code observed, no live I/O thread, all three streams closed — **and** every
  `cleanup[*] == "ok"`), or if any observation row is incomplete. `budget_exhausted` and
  `interrupted` are distinct non-`completed` statuses.
- T10. `completion.retain` re-checks each artifact's bytes against its declared identity,
  writes `<name>.partial` with `open('xb')` (refusing an existing staging file), `os.replace`s
  it, and only then sets `retention='complete'` and deletes the base64. A retained artifact can
  never be labelled complete without the bytes being on disk and re-read.
- T11. The Job memory limit applies to the **worker** process' job object
  (`supervise(..., memory_bytes)` to `host.Job(memory_limit=...)`); the parent's own memory is
  not bounded, and `peak_job_memory_bytes` is a worker-Job figure. `identity.proposed_resource`
  says exactly this (`worker_job_only: true`, `parent_memory_measured: false`); any packet
  claim of a 2048 MiB total bound would be false.

## H. Quantitative predictions I will test against the deferred receipts

- X1. **Predicted export wire size.** The capacity probe measured 1012625 bytes for 1081
  conservative CHECK/null rows. In the frozen codec an action is encoded as
  `{"kind":...,"raise_to":...}`; `"check"` with `null` costs exactly three bytes more than
  `"raise"` with `2`, and the placeholder `source_id` has the same fixed width as a real `t1:`
  digest. The teacher has 545 `raise-to-2` rows, so the exported blueprint wire must be
  **1012625 - 3*545 = 1010990 bytes**, that is `wire_bytes == 1010990` with `cap == 1048576`
  and roughly 3.6 % headroom. A rehearsal receipt reporting a materially different
  `wire_bytes` (or a `cap` other than 1048576) falsifies either the capacity measurement or
  the export path.
- X2. `export_encoding.report.teacher_sha256` must be `c3ffab40...`; `source_id` must be
  `t1:c3ffab403eb7e939857cc31b0f21b255cefdffd8b0d26d078b703c1fe956b3e3`;
  `hands_count == 1081`; `keys_equal` and `actions_equal` true.
- X3. `membership.report` must show `universe_count == 1081`, `hands_count == 1081`,
  `hits == 1081`, `unsupported == 0`, `disagreements == 0`, `exact_entries == true`,
  `scope == "exhaustive_library_provider_root"`, and a `wire_sha256` equal to the
  `blueprint.json` artifact digest.
- X4. A GREEN rehearsal result must carry `phase=export`, `coverage=declared-full`,
  `status=completed`, `phase_complete=true`, `cleanup_verified=true`,
  `resource_state_verified=true`, `worker_exit_code=0`, `errors=[]`,
  `permutation_sha256=344e7eeb...`, `full_pool_estimate=null`, and exactly two artifact rows
  (`teacher.json` with digest `c3ffab40...` and `blueprint.json`), both `retention=complete`
  and both stripped of `artifact_base64`.
- X5. The re-published `rehearsal/teacher.json` must be byte-identical to
  `inputs/solve-teacher.json` (`c3ffab40...`) — the manifest already shows the same digest for
  both, which is the "copied teacher identity" claim; the export must not recompute a teacher.
- X6. Rehearsal wall time must fit inside the proposed 600 s and the worker Job peak inside
  2048 MiB, and the packet must NOT present a rehearsal figure as authority for the envelope.
- X7. `rehearsal/export-stderr.txt` hashes to `e3b0c442...`, the SHA-256 of the empty string,
  so the child produced no stderr; any claim of a captured stderr diagnostic on the GREEN path
  would contradict that.

## I. Falsifiers I will look for in the deferred material

- F1. A RED receipt that is only a label: the removed or edited predicate must be identifiable
  and the observed exit code and message must match the wrapper's own table (80, 82, 84-97,
  98, 99).
- F2. A "harness error" receipt that is really a product failure, or the reverse.
- F3. A two-caller rehearsal that does not actually race the `mkdir` claim, or that shows the
  claim being removed, or that runs against the retained root.
- F4. Any executed source slice whose digest does not reproduce from `invoke.sh` or the frozen
  blobs by my own recomputation.
- F5. Any claim about membership, byte cap, repeated encoding, copied teacher, cleanup or
  resources that rests on a summary label rather than on the raw capture, or that generalises
  the direct-provider scope into host agreement, complement coverage or teacher strength.
- F6. Any statement that the controller's resource decision, the r004 solve authorization, or
  a rehearsal authorizes this export invocation.
- F7. Any residual operator duty (exclusive checkout, journal ownership, authorization
  authenticity, abandoned-claim resolution, output preservation) that the packet asserts as
  verified rather than as an assumption.
