# Cold review — export-run-20260910-r001 (independent pass, Claude)

**Verdict: CLEAN**
**Specification judgment: SOUND.** **Engineering judgment: SOUND.** **Design verdict: SOUND.**

Reviewer: Claude, cold and independent. Drafter: Codex. No author verdict was supplied and
none was sought. Nothing in this report authorizes an invocation, publication, commit or push.

- Sealed inventory: `D:/Pontius/tmp/export-r001-cold/inventory-02-claude.md`,
  sha256 `e62d1f04e0cf2834e608a04ef45473d65701ebeb109fedebc76f165479608875`, 25533 bytes.
  Written and hashed before `checks/`, `rehearsal/`, `coverage.md`,
  `authorization-request.md` and `next-phase.md` were opened; not revised afterwards.
- Scratch (exclusive, all writes): `D:/Pontius/tmp/export-r001-cold`.
- Context probe: **CONTEXT_PROBE_NONE**.

Filename deviation, stated up front: the packet's `handoff.md` asks for
`reviews/review-01-claude.md` and `checks/review-01-inventory.md`. My commissioning
instructions forbid opening or writing inside `reviews/`, state that slot 01 is already
occupied by an earlier report that must not be overwritten, and direct both outputs to
`D:/Pontius/tmp/export-r001-cold` as `inventory-02-claude.md` and `review-02-claude.md`.
I followed the commissioning instructions. The packet owner may copy these files wherever
the packet convention requires; I have not written into the packet.

---

## 1. Identity — established from the bytes

| Claim | Independent result |
|---|---|
| 47-member manifest `9965a225…` | **Reproduced.** Rows `"<sha256>  <relpath>"`, whole-row byte sort, LF joins **and a trailing LF**; `handoff.md`, `candidate.json`, `manifest.sha256` excluded. 47 rows, digest exact. |
| Manifest file integrity | The file is byte-identical to that canonical blob (its own sha256 equals the manifest digest); no CRLF; already in sorted order. |
| Freeze boundary | `reviews/`, `finalization/`, `disposition.md`, `finalizer-addendum.md`, `authorization-template.txt`, `checks/review-01-inventory.md` are outside the 47 members. Excluding them left the digest exact, which confirms the boundary **without opening any of them**. |
| Source commit / tree | `1c706744…` is a commit; tree `3d2fe79d…` matches `identity.json.source_tree` and `candidate.json.tree`. `refs/heads/codex/eval-panel-completion-adopted` resolves to `1c706744…`. |
| `governing/{brief,design}.md` | `git hash-object` gives `1c26704c…` / `fda51e07…`, equal to the commit's `docs/architecture/v0a-eval-panel-impl-r001/{brief,design}.md` blobs. Exact frozen blobs. |
| `inputs/source-scope-blobs.json` | **Reproduced.** 892 entries, all mode `100644` blobs; every `git_blob`, `bytes` and raw-byte `sha256` matches `git ls-tree` / `cat-file` at the adopted commit; declared `count` and `tree` correct. |
| `checks/invoke-from-solve-r004.diff` | **Reproduced.** My own `diff -u inputs/solve-wrapper-r004.sh invoke.sh` is byte-identical to the packet's diff body. |
| Executed slice digests | **Reproduced from `invoke.sh` itself:** `producer_guard` `95ac5b97…` and `exit_tail` `b86dd771…` (`focused-checks.json`); the harness-error receipt's `68fd2195…` reproduces under the faulty extraction; the race-gate `slice_sha256` `39c86b6f…` reproduces from `checks/rehearse.py`. |
| Execution checkout | `D:/Pontius-worktrees/eval-panel-export-20260910` HEAD = `1c706744…`, branch `codex/eval-panel-export`, `plans/export.json` hashes to `c55f26f6…`, source scope clean, 7 on-disk run dirs = 7 tracked, `.venv/Scripts/python.exe` present, journal 59 rows, no `authorization.md`, no `invocations/`. Every wrapper precondition is currently satisfiable except the deliberate authorization gate. |
| Rehearsal snapshot | `D:/Pontius-worktrees/eval-panel-export-rehearsal-20260910` is detached at `1c706744…` and is not the retained checkout. |

## 2. Acceptance question 1 — solve, census, teacher, prerequisites, identity, envelope

**Answered yes, from independent re-derivation, not from labels.**

Working only from `RANKS`/`SUITS`/`DECK` in the frozen source and CPython 3.14.6 stdlib, I
re-derived the entire plan surface: the board `2c 7d 9h Js Qc` → `(0,21,30,39,40)`, ascending
and distinct; the hero universe C(47,2) = **1081** = `hand_count` = `pool_count` =
`HERO_COUNT`; `hand_universe_sha256` = `18953f11…`; and
`random.Random(int(pool_seed,16)).shuffle(...)` producing a permutation **byte-identical to
the plan's 1081-name list**, digest `344e7eeb…`. The `prefix` equals
`eval_bridge.prefix_document()` exactly; `stacks` = 4; `runtime` = 3.14.6. The member set is
exactly the export shape (15 keys, no `witness_bank`), and `inputs` is exactly
`{teacher, producer_result}`.

The teacher bytes are canonical (`json.dumps(sort_keys, separators, ensure_ascii,
allow_nan=False)` round-trips byte-identically), `hands == permutation` (full census, not a
proper prefix), and **all 1081 rows independently satisfy every `_teacher_validate` domain
rule** I recomputed by hand: `denominator == 990`, `|check_total| <= 1980`, `check_total`
even, `bet_total == 2*check_total`, `wins+losses+ties == 990`,
`check_total == 2*(wins-losses)`, `work == {990, 1980, 991}`, and
`action == "raise-to-2"` iff `bet_total > check_total`. Distribution 545 / 536, with **zero**
rows where `check_total == bet_total` — which is exactly why `nonzero_tie` is
`absent_in_completed_pool` and why zero `nonzero_tie_reference` observations is the correct
outcome under `completion.complete`, not a missing check.

The producer result carries `status=completed`, `phase=solve`, `coverage=declared-full`,
`cleanup_verified=true`, `phase_complete=true`, `errors=[]`, all twelve cleanup entries `ok`,
`worker_exit_code=0`, `permutation_sha256=344e7eeb…` (= my derived digest), 1083 observations
with row hands in plan-permutation order, and one `teacher.json` artifact row at
`c3ffab40…` with `retention=complete` and no residual base64 — precisely the predicates
`completion.teacher_input` re-checks at run time. Prerequisite capacity and preflight results
both complete, `cleanup_verified`, with the same permutation digest and
`sample_complete=true` on preflight; all three prerequisite digests equal the constants frozen
in `v0a_eval_panel_completion.PREREQUISITES`.

**Envelope — the point I looked hardest at.** `completion.validate` pins
`resource == {600, 2048}` **only when `phase == 'solve'`**. For `export` the numbers are
code-unconstrained, and `inputs/prerequisite-decision.md` scopes the controller's adoption to
"the full-pool T1 solve", adding that solve, export and agreement "each still need their own
bound plan and one-shot authorization". The packet gets this right in every place it appears:
`identity.proposed_resource` = "new export proposal; not inherited solve authorization";
`authorization-request.md` §"Separate resource proposal" says the values "require their own
approval here" and that "the earlier solve authorization supplies no export authority", and
labels the 15 s / 11.265 s / 787.8 MiB rehearsal figures as "one observation, not a runtime
guarantee". No inheritance is claimed anywhere.

## 3. Acceptance question 2 — wrapper binding consistency

I diffed the predecessor wrapper myself before sealing my inventory. The change set is exactly
the phase rename, the root/packet/plan constants, the four new producer constants with their
exit-80 guard, the `SOLVE_ROOT` → `EXPORT_ROOT` rename with a **strengthened** refusal, and
the six record-name changes. Every binding is consistent:

- `ADOPTED` = the commit in `identity.json`, `candidate.json`, the plan's source and the
  producer journal row's `source_commit`.
- `RETAINED_ROOT` = `identity.execution_checkout`, distinct from the solve worktree that holds
  the producer inputs. `PK` = this packet; `authorization_file` = `$PK/authorization.md`.
- `PLAN_SHA` = `c55f26f6…` = the packet plan copy = the checkout copy, **and the argument
  passed to the tool is `"$ROOT/plans/export.json"` — the same file the precondition hashes.**
  No packet copy is handed to the tool, and there is no second plan path.
- `identity.json.command` reproduces the wrapper's launch line token for token, including
  `-B -P -W error::ResourceWarning`, `run`, `--reviewed-commit "$ADOPTED"` and the plan path.
- `ATTRIBUTE_SHA` = the packet's own `journal_attribution.py`.
- The exit-80 producer guard sits **above** `mkdir "$OUT/claim.d"`, so both digests are
  checked strictly before the claim is spent, as `identity.invocation.input_guard` asserts.
- Capture paths: the six pre-existence names, the two redirections and the two digest reads
  all use the same `export-*` names under `$OUT`.

## 4. Acceptance question 3 — refusals, claim, records, attribution, exit precedence

**Sound. I found no supported failure that can look successful.**

- Mode: unset `REHEARSAL` → retained; any set value must be exactly `0` or `1`; empty is
  refused (84). Retained mode refuses any *set* `EXPORT_ROOT`/`REHEARSAL_PK` via `${VAR+x}`,
  so an explicitly empty value is now refused too — a genuine strengthening over r004's
  `${VAR:-}`. Rehearsal mode requires an explicit root, an existing directory, a canonical
  path different from the retained checkout, and a detached HEAD.
- Claim: `mkdir "$OUT/claim.d"` is atomic; the script contains no `rm`/`rmdir`, so a claim is
  never removed; both record writes are checked with `|| exit 98`, and the start record is
  re-read with `grep -q`. `set -o noclobber` is armed around the redirections, so a
  pre-existing capture file aborts the redirection and the child never starts.
- Interpreter: `"$PY" -I -B -c "…assert…"`. `-I` implies `-E`, so a hostile `PYTHONOPTIMIZE`
  cannot strip the assert. This is a real check, not a cosmetic one.
- Evidence: `EVIDENCE` starts `complete` and is only ever cleared. I walked every write and
  capture on the post-launch path: a failed attribution, a failed digest, a failed
  retained-file listing, a failed end-record append and a missing capture each clear it.
- Attribution: the helper refuses a missing row (`ABSENT`/3), an extra row (`EXTRA`/4), a row
  that does not name the adopted commit, an absent/non-string `output`, a missing output file,
  a digest mismatch and — when present — a `runtimes_sha256` mismatch. It never substitutes an
  older row. I also checked the `wc -l` / split-count seam: a journal whose final row lacks a
  trailing newline makes the two counts disagree, and that disagreement can only produce
  `EXTRA` (evidence incomplete), never a false `BOUND`.
- Exit precedence: nonzero child status first (with `EVIDENCE INCOMPLETE` still printed),
  then 99 for incomplete evidence, then 0. The frozen tool returns 0 only when
  `report["status"] == "completed"`, which `supervise` downgrades to `failed` on any error, on
  unverified cleanup (`resource_state_verified` **and** every `cleanup[*] == "ok"`), or on any
  incomplete observation. `begin_run` independently re-verifies the whole source scope against
  the reviewed commit and raises without `--development`. `main` always creates the run
  directory and `runtimes.json` before reading the plan, and `finish_run` writes exactly one
  result and one journal row **including on failure** — so criterion 9 holds and the
  retained-file listing can never be silently empty on a launched child.

## 5. Acceptance question 4 — do the executed assertions reject false outcomes?

**Yes, and the receipts are accurately labeled.**

- **GREEN**: the real rehearsal, in the detached snapshot, two callers, statuses `[0, 97]`,
  one capture, journal 59 → 60, `BOUND`. The result carries `phase=export`,
  `coverage=declared-full`, `status=completed`, `phase_complete=true`,
  `cleanup_verified=true`, `resource_state_verified=true`, `worker_exit_code=0`, `errors=[]`,
  `permutation_sha256=344e7eeb…`, `full_pool_estimate=null`, and exactly two artifact rows
  both `retention=complete` with the base64 stripped. Every one of these matched the
  predictions I sealed before opening `rehearsal/`.
- **RED**: `red-before-guard.json` records a wrapper whose `producer_guard` slice digest is
  `e3b0c442…` — the SHA-256 of the empty string, i.e. **the guard was demonstrably absent** —
  and the three producer-mismatch cases returned `0` instead of `80`. The `exit_tail` digest
  is identical to the real wrapper's and the other 28 cases match the GREEN receipt
  case-for-case, so the mutation is localized and the guard is proven load-bearing.
- **Harness error**: `harness-extraction-error.json` carries the *real* wrapper digest
  `c70c9dea…` but a different `producer_guard` slice digest `68fd2195…`. I recomputed that
  digest from the frozen `invoke.sh` under the faulty extraction and it matches exactly: the
  section heading's dashes became Bash code. The signature that this is a harness fault and
  not a product defect is that `producer-bound` — the *positive* case — also failed with a
  bash syntax error, exit 2. Retained, disclosed in `coverage.md`, and correctly labeled.
- **Executed source slices**: both digests reproduce from `invoke.sh`; the race-gate slice
  digest reproduces from `checks/rehearse.py`. Nothing is asserted about a slice I could not
  regenerate.
- **Two-caller rehearsal**: real, not simulated — two `subprocess.Popen` calls on the frozen
  wrapper against a detached snapshot, with a nine-case control set proving the acceptance
  predicate itself rejects `[1,97]`, `[99,97]`, `[0,0]`, `[97,97]`, 0 captures and 2 captures.
  (See Finding M1 for a precision point about which gate actually fired.)
- **The diff is sufficient**: I regenerated it byte-for-byte.

## 6. Acceptance question 5 — do the substantive claims follow from raw captures?

I recomputed every one of them rather than reading the summary.

- **Byte cap — the strongest independent check in this review.** Before opening
  `rehearsal/`, I predicted the exported wire size from first principles: the capacity probe
  measured 1 012 625 bytes for 1081 conservative CHECK/null rows; in the frozen codec
  `"check"`+`null` costs exactly three bytes more than `"raise"`+`2`; the teacher has 545
  `raise-to-2` rows; therefore `1 012 625 − 3 × 545 = 1 010 990`. The rehearsal's
  `blueprint.json` is **1 010 990 bytes**, and the raw wire contains exactly 536
  `"kind":"check","raise_to":null` and 545 `"kind":"raise","raise_to":2` occurrences.
  `cap` is the full 1 048 576 host cap, not a narrower declared bound. ~3.6 % headroom.
- **Membership.** From the raw `membership` observation's 1081 rows, not the summary: 1081
  distinct hands, every row `classification=hit`, every `table_hit` true, every
  `provider_reason` = `blueprint_hit`, and prepared/provider actions agree pairwise
  (545 `raise-to-2`, 536 `check`). `exact_entries` true, `disagreements` 0,
  `universe_count == hands_count == 1081`.
- **Blueprint independently reconciled to the teacher.** I decoded `blueprint.json` myself:
  1081 entries, key set equal to the teacher's hand set, **zero action mismatches** against
  the teacher rows, `source_id` = `t1:` + sha256(teacher) verified by recomputation, and the
  key's root state (`stacks [4,2,2,4,4,4]`, `total_contributions [0,2,2,0,0,0]`,
  `folded` seats 0/3/4/5, `pending_seats [2]`, street `river`, board `[0,21,30,39,40]`)
  is the declared s=4 river root.
- **Repeated encoding.** `export()` encodes twice and requires byte equality before emitting
  anything; a difference is a `ValueError` inside the worker, which forces `failed` and exit 1.
- **Copied teacher identity.** `rehearsal/teacher.json` is **byte-identical** to
  `inputs/solve-teacher.json` (I compared the bytes, not the digests). The export republishes
  the solve's teacher; it does not recompute one.
- **Cleanup and resources.** All twelve cleanup attempts `ok`, `resource_state_verified` true,
  peak worker Job 826 081 280 B = 787.8125 MiB (I verified the arithmetic in `receipt.json`),
  worker 11.265 s, wrapper 15 s. `receipt.json` states `"evidence": false` and
  `"parent_memory": "not measured; outside worker Job limit"`, matching the frozen code, where
  the Job limit binds the worker process only.
- **Receipt integrity.** All six file digests and byte counts in `receipt.json` verify against
  the actual files; the `encoding` and `membership` blocks are byte-equal to the corresponding
  result observations; `export-stdout.json` is exactly `result.json` with CRLF translation.
  `export-stderr.txt` is empty (`e3b0c442…`).
- **Scope separation.** The membership scope is the literal
  `exhaustive_library_provider_root`. `coverage.md` says it "is not the host runtime oracle";
  `next-phase.md` says real-host agreement, teacher strength, equilibrium quality and transfer
  "are not established by this export packet"; `authorization-request.md` says agreement "must
  bind future retained export outputs, never rehearsal copies". The distinction is held
  everywhere I checked. (See Finding M2 for one precision point.)

## 7. Acceptance question 6 — remaining duties, coverage limits, withheld authority

Explicit and adequate. `identity.residuals` lists exclusive checkout and journal ownership,
the helper's trust in the adopted producer, operator authentication of the authorization,
preservation/mirroring of outputs and abandoned claims, the worker-Job memory boundary, and
the rehearsal-only status of snapshot artifacts. `authorization-request.md` repeats that
"existence alone does not authenticate a decision" and that the operator resolves ambiguity.
`coverage.md` names its own limits (synthetic slice inputs; no new compound child-failure or
post-launch write-failure test; unmeasured parent memory; the blob inventory is a pin, not a
line-by-line review) and discloses both process faults honestly. `preservation-after.json`
records `retained_export_authorized: false`, `retained_export_invoked: false`,
`committed: false`, `pushed: false`, with all 53 pre-hashes re-matched. Authority is withheld
pending the controller's separate decision.

---

## 8. Findings

No Critical or Important finding survives verification. The four Minor findings and one
Advisory below are precision and disclosure points; none changes the plan's correctness or the
safety of the proposed invocation, and none requires a source or wrapper change.

### M1 (Minor) — the two-caller receipt exercises the pre-claim existence check, not the atomic `mkdir`

- **Location.** `checks/race-caller-b.txt:1`; `checks/rehearse.py:31-41`; `coverage.md:20-22`
  ("Claim at most once … two actual callers, statuses 0/97"); `identity.json`
  `invocation.claim` ("atomic mkdir").
- **Requirement.** Brief criterion 9 and the wrapper's own contract: one authorization can
  never start two exports. The only gate that is safe when two callers pass the pre-check in
  the same instant is `mkdir "$OUT/claim.d"`.
- **Concrete observation.** Caller B's captured output is exactly
  `PRECONDITION an invocation was already started (claim.d exists)`. That string is emitted by
  the pre-claim `for f in claim.d …` existence loop, **not** by the `mkdir` failure branch,
  whose message is `claim refused: an existing claim or an unwritable record directory`. So
  the second caller arrived after `claim.d` already existed and was refused by the earlier,
  non-atomic check. Both branches exit 97, so the receipt cannot distinguish them, and
  `coverage.md`'s Limits paragraph does not mention it.
- **Why it is Minor, not Important.** The atomicity is a property of the code, which I read
  and verified; the receipt's outcome (`[0,97]`, one capture, one new journal row) is correct
  regardless of which gate fired; and no packet text claims the `mkdir` window itself was
  raced. This is an evidence-precision gap, not a defect.
- **Smallest correction.** One sentence in `coverage.md` Limits: the two-caller receipt
  demonstrates single-claim behaviour through the pre-claim existence check; the atomic
  `mkdir` window is argued from the frozen wrapper text and has no receipt.

### M2 (Minor) — the empty complement is not disclosed, so `unsupported: 0` can read as a passed off-pool control

- **Location.** `coverage.md:36-38`; the `membership` observation in `rehearsal/result.json`;
  `governing/brief.md` acceptance criterion 4 ("Unsupported root keys equal the complement of
  H within the declared board") and criterion 8 (off-pool default control).
- **Requirement.** Criterion 4's complement clause and criterion 8's off-pool discrimination.
- **Concrete observation.** With `coverage = declared-full`, H is the entire 1081-hand
  universe, so the complement within the declared board is **empty by construction**.
  `validate_membership` therefore enumerates 1081 hands of which 1081 are in-pool: `hits` 1081,
  `unsupported` 0, and the `blueprint_default` branch is never taken. `coverage.md` reports
  "1,081 hits, no disagreement/unsupported; exact entries" without saying the complement is
  empty, so a reader can take `unsupported: 0` as an exercised off-pool control rather than an
  empty set. Design section 4 assigns the off-pool control to the agreement phase's
  test-only proper-subset artifact, and `completion.complete` only builds
  `control-off-pool.json` for `agreement` — so the deferral is correct, just unstated.
- **Smallest correction.** One sentence in `coverage.md`: for declared-full the complement of
  H is empty, so criterion 4's complement clause is satisfied vacuously here and criterion 8's
  off-pool default control is deferred to agreement.

### M3 (Minor) — the RED wrapper is not retained, so the mutation's scope is not reproducible from packet bytes

- **Location.** `checks/red-before-guard.json` (`source_sha256` `8edd6152…`); packet contains
  no wrapper with that digest.
- **Requirement.** A RED receipt must be identifiable, not merely labelled: a reviewer should
  be able to confirm what was changed.
- **Concrete observation.** I could not reproduce `8edd6152…` from the frozen `invoke.sh` by
  any obvious guard removal (a clean deletion of the guard block gives `d4e4b50a…`), and the
  mutated wrapper is not in the manifest. What *is* reproducible is the receipt's
  `producer_guard` slice digest `e3b0c442…`, which is the SHA-256 of the empty string and
  therefore proves the guard slice was empty; the `exit_tail` digest is identical to the real
  wrapper's; and 28 of 31 cases match the GREEN receipt exactly. The RED is well-evidenced,
  but the claim "only the guard was removed" rests on that circumstantial agreement rather
  than on retained bytes.
- **Smallest correction.** Retain the mutated wrapper (or a diff of it) beside the receipt, or
  state in `coverage.md` that the mutation is bounded by the slice digests and the
  case-by-case comparison rather than by retained bytes.

### M4 (Minor) — four attribution-helper refusal branches are unexercised and undisclosed

- **Location.** `checks/focused-checks.py:81-98`; `journal_attribution.py:33-58`;
  `coverage.md:28-30` and the Limits paragraph at `coverage.md:64-69`.
- **Requirement.** "Recompute meaningful assertions from the bytes; do not accept a passing
  label as evidence" — and the packet's own claim that attribution "binds exact new bytes".
- **Concrete observation.** The six synthetic cases cover `ABSENT`, `EXTRA`,
  `MISMATCH source_commit`, `MISMATCH output_sha256`, `BOUND` and `BOUND` over CRLF. They do
  **not** cover `MISMATCH unparsable-row`, `MISMATCH output-missing` (non-string or empty
  `output`), `MISMATCH output-file-missing`, or `MISMATCH runtimes_sha256`. The last matters
  most in practice: `finish_run` always writes `runtimes_sha256` when an output directory is
  set, so the real retained row will carry it, yet only the *passing* side of that branch is
  ever exercised (by the rehearsal). `coverage.md`'s Limits paragraph names filesystem errors,
  interrupted cleanup and unrelated journal writers, but not these branches.
- **Why it is Minor.** All four branches are conservative refusals: each can only turn a
  would-be `BOUND` into a non-`BOUND`, which the wrapper maps to `EVIDENCE=incomplete`. No
  false success is reachable through them.
- **Smallest correction.** Add the four synthetic cases to `focused-checks.py`, or name them
  in `coverage.md` Limits.

### A1 (Advisory) — a post-claim `set -u` expansion can consume the one-shot claim without launching

- **Location.** `invoke.sh`, the launch block:
  `env -i SystemRoot="${SystemRoot:-$SYSTEMROOT}" TEMP="$TEMP" TMP="$TMP" …`, which executes
  after `mkdir "$OUT/claim.d"` and after both record writes; `authorization-request.md:53-55`
  (operator instructions).
- **Requirement.** The wrapper's own contract that a refusal *before* acquisition consumes
  nothing, and the one-shot nature of the authorization.
- **Concrete scenario.** An operator runs the wrapper from a shell in which `SystemRoot` and
  `SYSTEMROOT` are both absent (or `TEMP`/`TMP` is absent). Under `set -u` the expansion fails,
  bash exits before `env -i` runs, and the result is: claim taken, start record written, no
  child, no end record, no `PHASE`/`DONE` line, exit status 1. The behaviour is fail-closed —
  nothing is falsely reported as successful — but the single authorized attempt is consumed
  and only the controller can resolve the abandoned claim.
- **Why it is Advisory, not a defect.** Both branches are demonstrably satisfied on this
  machine: the r004 solve launched through the same construct, and this packet's rehearsal
  exercised the `$SYSTEMROOT` fallback (Python upper-cases environment keys on Windows, so the
  child bash saw `SYSTEMROOT` rather than `SystemRoot`). Moving the expansion above the claim
  would change the frozen wrapper digest and re-open the whole freeze for a hazard that has
  not occurred.
- **Smallest correction.** Documentation only: list `SystemRoot`/`SYSTEMROOT`, `TEMP` and
  `TMP` as required environment in the operator instructions in `authorization-request.md`.

---

## 9. Separate judgments

**Specification (SOUND).** The plan is the phase design step 7 describes: a bounded export
plan that binds the measured preflight and a chosen resource envelope, on the adopted source,
with no automatic continuation from the solve. It satisfies brief criterion 3 (the full-pool
launch rests on the recorded decision and finite limits, with failure retained), criterion 4
(immutable teacher and pool; repeated export byte-identical; decode through the existing
codec; complete key membership and action equality over H), and criterion 9 (one parent, one
worker, one result, one journal row, no per-hand records). The one place where specification
and code could have drifted — the envelope, which the completion module pins only for `solve`
— is the place the packet handles most carefully: it re-proposes 600 s / 2048 MiB as a new
request and states in three separate documents that the solve authorization confers none.
Scope discipline is maintained: the direct-provider check, real-host agreement and any claim
about teacher strength are held apart, and `next-phase.md` refuses to bind agreement to
snapshot bytes.

**Engineering (SOUND).** `invoke.sh` is a minimal, faithful derivation of a wrapper that has
already survived a retained invocation, with exactly one behavioural strengthening (set-but-
empty override refusal) and one addition (the pre-claim producer guard) — and the addition is
demonstrated RED, GREEN and, honestly, once as a harness fault, with slice digests I
regenerated from the frozen bytes. The refusal, claim, record and exit-precedence logic is
fail-closed at every branch I traced; `EVIDENCE` is monotone downward; the frozen tool's own
status computation cannot report success with errors, unverified cleanup or incomplete
observations. The rehearsal is a real two-caller run on a detached snapshot whose product —
1 010 990 wire bytes — I predicted to the byte from the capacity measurement and the codec
before opening it. I found no path on which a supported failure reports success.

## 10. Coverage and exposure disclosures

- **Context probe: CONTEXT_PROBE_NONE.** No memory index, memory file, conversation
  transcript, review verdict, disposition or addendum text appeared in my system prompt or in
  any system-reminder. The only contextual material was a git-status block (whose most recent
  commit subjects mention an earlier round label), the user's e-mail, tool/skill listings and
  environment notes — all excluded from the probe by the stated rule.
- **Prohibited files: none opened.** I did not read `reviews/` (any file),
  `checks/review-01-inventory.md`, `disposition.md`, `finalizer-addendum.md`,
  `authorization-template.txt`, `finalization/`, any `progress.md`, `INDEX.md`, any memory
  index or file, any conversation transcript, or any unrelated scratch. `ls` listings showed
  some of those names; I opened none of their contents. My manifest recomputation deliberately
  excluded them and still reproduced the digest exactly, which confirmed the freeze boundary
  without reading them.
- **Predecessor material: declined.** Handoff step 6 permits reading r004 and r003
  review/disposition records after independent inspection. I did not open them; my judgment is
  complete from the current packet and the frozen source, and reading predecessor verdict
  language would have cost more than it added. No ledger was opened.
- **Incidental path exposure.** `checks/preservation-before.json` is a manifest member I was
  required to read at step 5. It contains 53 absolute paths with digests, including
  `D:\Pontius-handoffs\INDEX.md` and files under the r004 solve packet
  (`authorization.md`, `handoff.md`, `measured-report.md`, `campaign-note.md`, check and
  invocation records). I saw **path names and SHA-256 values only** — no content — and no
  review, disposition or verdict path appears in that list. This is disclosed for completeness;
  it exposed no finding or verdict language.
- **Execution discipline.** No project invocation, no wrapper or check-script execution, no
  solve, export or agreement, no worktree mutation, no commit, no push. I did not run
  `checks/rehearse.py`, `checks/focused-checks.py`, `checks/admit-plan.py`,
  `checks/input-controls.py` or `invoke.sh` in any mode. Git was used read-only
  (`cat-file`, `ls-tree`, `rev-parse`, `hash-object`, `status`, `symbolic-ref`). Worktree bytes
  were touched only for identity checks. **No project module was imported**: every
  re-derivation — deck, universe, permutation, digests, teacher-row domain rules, blueprint
  decoding, slice digests, manifest — is plain CPython 3.14.6 stdlib. All writes went to
  `D:/Pontius/tmp/export-r001-cold`.
- **What this review does not establish.** I did not execute the export, so the retained
  invocation's outcome is unknown; the rehearsal is one observation on one machine and is not
  a runtime guarantee. I did not verify the producer's journal ownership claims
  (`identity.producer.journal_commit`/`journal_branch`) — they are not checkable from this
  packet's frozen bytes and must remain disclosed assumptions. I did not audit the 892
  source-scope blobs line by line; I verified their identity against the adopted commit. I did
  not evaluate host agreement, teacher strength, equilibrium quality or transfer, none of
  which this packet claims.

## 11. Disposition

**CLEAN.** The plan binds the correct completed retained solve, the full 1081-hand census and
the exact teacher; the wrapper's bindings are internally consistent and its refusal, claim,
record and exit logic is fail-closed; the receipts are accurate and their substantive claims
reproduce from raw bytes; scope separation and residual duties are explicit; and authority is
withheld pending the controller's separate decision on a separately proposed envelope. The
four Minor findings and one Advisory are disclosure and coverage-precision improvements, all
of which can be made in `coverage.md` and `authorization-request.md` without touching the
frozen plan, wrapper, helper or source.

This report authorizes nothing. It is returned for the drafter's disposition.
