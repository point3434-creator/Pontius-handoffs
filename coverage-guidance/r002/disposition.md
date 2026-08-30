# coverage-guidance/r002 disposition

Coordinator: Codex /root, 2026-08-30. CLEAN for the prospective documentation
refinement; r001 I1 closed. Finalizer: Claude. Source remains uncommitted.

Candidate 81fb6cf6491b7ae87ca2a2a3ccd0a7103c4cfed3
Manifest 2c9903843b765143f2f2a33c4c3e0233ff0ca9c907faae9462f12b2577e56fdc
Ref refs/heads/review/coverage-guidance/r002
Tree 33dc90fc78bb8ec62f07c7afed82f6b4b2a4851e

Independent report: reviews/review-01-codex.md, SHA-256
475f0eb537a1fae5d3974775c5541d6abf9c852be270b743be8b93614918626c.

## Result

The working docs/workflow.md and its embedded brief/review templates now:
- Require a concise pre-fix category, discovery method, members, limits and
  falsifier, finalized separately in the frozen coverage.md.
- Give reviewers an independent discovery pass before reading that claim and
  share responsibility for finding sibling cases.
- Separate behavioral acceptance checks from supporting structural guards;
  fault schedules must show real occurrence, order and reachability.
- Distinguish demonstrated behavioral defects (RED then GREEN) from missing or
  unsound evidence (independent evidence closure, even when the new check passes).

No new ADR, approval stage, exhaustive-proof obligation or retrospective gate.
The already-frozen implementation r005 is not rejected for lacking coverage.md.

The reviewer independently inventoried closure paths before the deferred claim.
Its walkthrough found no remaining contradiction. The generic role shorthand
could be polished later; this advisory is not a blocking defect and was not
used to open another round.

Coordinator checks independently verified blob/manifest identity, exact
two-paragraph r001-to-r002 correction, LF/no BOM, working diff --check, unchanged
source HEAD/index and preserved CLAUDE.md. Freeze verification preserves the
separate pending design-verdict blocks byte-for-byte; they are excluded from
this candidate. See checks/coordinator-verification.json and
checks/freeze-verification.json. No runtime tests are appropriate for this
wording-only review; none were run for this task.

## Commit boundary

This completes the requested document refinement and review, not ceremonial
integration. No new per-commit authorization was requested or inferred.
The primary working workflow also contains previously pending design language;
do not commit the whole working file as though those extra bytes were reviewed
here. Use the exact frozen pair or separately reviewed authorized scope at
finalization. CLAUDE.md and .tmp.driveupload/ are unrelated and preserved.

Source review refs were routinely pushed, and packet records may be routinely
committed/pushed under packet rule 6. Those actions do not commit the primary
working documentation or accept an implementation.
