# Independent invariant inventory — export-run-20260910-r001, reviewer 01 (Claude)

Sealed 2026-09-10T06:15Z, before opening `checks/`, `rehearsal/`, `coverage.md`,
`authorization-request.md` or `next-phase.md`. Derived from the packet's step 1-3 inputs,
the frozen Git blobs at `1c7067448106cfa2aca3d57be879842d72293c61`, and read-only
inspection of the two execution checkouts. Not revised after sealing.

## Context disclosure, stated before any finding

This session drafted the four solve packets and the campaign note that prescribes what the
export phase must bind, and it has read both ledgers repeatedly during that work. It has no
exposure to the drafter's reasoning for this candidate, and no review of it exists. This is
therefore an independent review of Codex's candidate but not a cold pass in the project's
sense. The prohibition on opening `reviews/`, ledgers and memory indexes during this pass is
observed from here on; ledger exposure predates the pass and is disclosed rather than cured.

## Identity established independently

- Manifest recomputed over raw bytes, whole-row byte order, LF: 47 members, digest
  `9965a225729a5896818127c013122f62fb3ae323889fde8ab16ea35e3e43eb17`, byte-identical to the
  stored `manifest.sha256` and equal to `candidate.json`.
- `plans/export.json` `c55f26f6…`, `invoke.sh` `c70c9dea…`, `journal_attribution.py`
  `a20e760a…`. The helper is byte-identical to the solve packet's helper.
- All eight `inputs/` copies are byte-identical to their real sources: the retained solve
  teacher `c3ffab40…`, result `e6db93c0…`, runtimes `12af22dd…` and journal row
  `ab668990…`; the three prerequisites `29f532a9…`, `8a17325e…`, `037a0de1…`; and the r004
  wrapper `160cfcec…`.
- `governing/brief.md` and `governing/design.md` are byte-identical to the frozen blobs at
  the source commit.
- Retained execution checkout `D:/Pontius-worktrees/eval-panel-export-20260910`, branch
  `codex/eval-panel-export`, HEAD equal to the adopted commit, source scope clean with only
  an untracked `plans/`, `plans/export.json` equal to the pinned digest, 59 journal rows,
  seven on-disk run directories equal to the seven tracked at HEAD, venv CPython 3.14.6 with
  NumPy 2.5.2. A separate detached rehearsal worktree exists and is not the retained root.

## Invariants to be checked

**I-01 admission.** The plan satisfies every frozen predicate in entry `validate_plan` and
completion `validate`: key set with no `witness_bank`, declared root, prefix, universe digest
and count, seeded permutation, `declared-full` with `pool_count` equal to `HERO_COUNT`, the
three prerequisite digests equal to the frozen `PREREQUISITES` constants, the capacity
result's permutation digest equal to the re-derived order, preflight `sample_complete`, and
`inputs` exactly `{teacher, producer_result}` each binding an absolute path and a digest.
*Status: evaluated independently against the bytes, 35 of 35 predicates pass.*

**I-02 envelope authority.** The completion validator constrains `resource` to 600 s /
2048 MiB only when `phase == 'solve'`. For export the validator accepts any positive
seconds and any `memory_mib` in 1..1048576, so the recorded resource decision does not
extend to this phase and the proposed envelope requires its own controller approval. The
packet must request it rather than assume it.

**I-03 producer binding.** `teacher_input` must reject anything but the completed retained
solve: status completed, phase `solve`, `cleanup_verified` and `phase_complete` true,
coverage equality, `pool_count` equality, exact `prerequisites` dict equality, permutation
digest re-derivation, and a produced `teacher.json` artifact row whose digest equals the
plan's teacher digest with `retention == "complete"`.
*Status: evaluated independently against the retained bytes, all hold.*

**I-04 export semantics.** `export_teacher` sets `source_id` to `t1:` plus the teacher
digest, refuses a wire above the 1,048,576-byte cap, and requires the decoded artifact to
reproduce the complete key and action map. The phase additionally requires a second encode
to be byte-identical, `validate_membership` to pass, and both `teacher.json` and
`blueprint.json` to be retained. `complete` re-checks one passing membership row, exactly
those two artifact names, and each artifact's declared bytes and digest.

**I-05 membership scope.** `validate_membership` walks the whole 1,081-hand universe through
`PreparedBlueprint.action_for` and the public `BlueprintProvider.propose`, comparing key,
`table_hit`, action, reason and decision digest. Its own `scope` field is
`exhaustive_library_provider_root`. Because the pool is the entire universe, `unsupported`
must be 0 and `hits` 1,081; no off-pool complement exists on this board, and nothing here
may be presented as host agreement or teacher strength.

**I-06 wrapper bindings.** Every changed constant must be internally consistent: retained
root, packet root, plan path and digest, capture filenames, phase labels in both records,
the argument passed to the adopted tool, and the helper pin. The new pre-claim guard must
check both retained solve inputs before any claim is taken.

**I-07 one-shot and evidence.** Mode refusal before the branch consumes the value; retained
mode refuses any set root or packet override; rehearsal requires an explicit, non-retained,
detached root; the claim is an atomic `mkdir` taken after the read-only preconditions and
before any record or launch; claim and start records are checked and a failure stops without
a launch; captures use `noclobber`; the journal row is attached only when exactly one new
row binds this checkout's result file; exit precedence returns a nonzero child status first,
then 99 for a zero-status child with incomplete evidence, then 0.

**I-08 check honesty.** Each executed case must assert what its name claims, the runner must
fail when a case fails, and any mutant or injected fault must be labeled and bound. A
passing label is not evidence; assertions are to be recomputed from the raw captures.

**I-09 rehearsal separation.** The rehearsal must run in a disposable detached checkout that
is not the retained root, must be labeled as not evidence, and its receipt's numbers must
follow from its own log, captures and attributed row.

**I-10 claims and residuals.** No teacher-strength, host-agreement or transfer claim may be
made. The agreement phase must remain unauthorized and must depend on the retained export
bytes rather than the rehearsal's. Operator duties and coverage limits must be explicit.

## Open questions carried into the deferred inputs

1. Does the packet request a new envelope for export, with a measured basis, rather than
   inheriting the solve decision?
2. Is the rehearsal's blueprint wire size under the cap, and is the retained wire expected
   to be identical or merely equivalent?
3. Do the executed checks cover the new pre-claim input guard and the stricter override
   refusal introduced in this wrapper?
4. Is the retained export's blueprint, not the rehearsal's, named as the agreement phase's
   input?
