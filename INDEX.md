# Pontius handoffs

Navigation only. A candidate's full commit and manifest SHA-256 bind its identity.
Private origin: https://github.com/point3434-creator/Pontius-handoffs.git.
Packet commits use the installed post-commit push hook; remote identity must
still be checked after each publication rather than inferred from hook success.

| Task | Round | Packet | State |
| --- | --- | --- | --- |
| v0a-blueprint-artifact-open | r001 | [Packet][blueprint-open-r001] | CLEAN/SOUND; authorized adoption pending |
| v0a-blueprint-artifact-design | r001 | [Packet][blueprint-r001] | NOT CLEAN; retained |
| v0a-blueprint-artifact-design | r002 | [Packet][blueprint-r002] | CLEAN/SOUND twice; not adopted |
| v0a-i01-prereg | r001 | [Legacy reports](../Pontius-worktrees/v0a-increment-1-preregistration-review/r1-candidate.json) | Rejected; preserved in its original location |
| v0a-i01-prereg | r002 | [Legacy handoff](../Pontius-worktrees/v0a-increment-1-preregistration-review/r2-handoff.md) | Three independent CLEAN reviews; later notes assessed separately |
| v0a-i01-prereg | r003 | [Legacy candidate](../Pontius-worktrees/v0a-increment-1-preregistration-review/r3-candidate.json) | Preserved; a generated-link check failed |
| v0a-i01-prereg | r004 | [Handoff](v0a-i01-prereg/r004/handoff.md) | Rejected: manifest row ordering; source bytes unchanged |
| v0a-i01-prereg | r005 | [Handoff](v0a-i01-prereg/r005/handoff.md) | Integrated and pushed as 111807b; three CLEAN reviews; scoped checks pass on 3.11/3.14; review refs safely retired |
| v0a-i01-impl | r001 | [Handoff](v0a-i01-impl/r001/handoff.md) | Slice A NOT CLEAN; seven consolidated findings; reproduced on 3.11/3.14; fix-round brief in disposition.md; Claude finalizes |
| v0a-i01-impl | r002 | [Disposition](v0a-i01-impl/r002/disposition.md) | NOT CLEAN; ten consolidated Important findings; 99 focused tests pass on actual 3.11/3.14; F3/F7 remain open; Claude finalizes the next reviewed candidate |
| v0a-i01-impl | r003 | [Disposition](v0a-i01-impl/r003/disposition.md) | FIX slice 1 NOT CLEAN; two residuals R2-01/03; R2-02/07/08 closed; second policy residual requires its own candidate and root-cause note |
| v0a-i01-impl | r004 | [Disposition](v0a-i01-impl/r004/disposition.md) | NOT CLEAN: first write cause demoted and abort clock cause lost; second host-cause residual; 113 focused tests pass per interpreter; root-cause note and isolated refactor next |
| v0a-i01-impl | r005 | [Disposition](v0a-i01-impl/r005/disposition.md) | NOT CLEAN: host exception/cleanup order and missing original clock cause; old r004 mechanisms fixed; 119 focused tests pass per interpreter; bounded ownership correction next |
| v0a-i01-impl | r006 | [Disposition](v0a-i01-impl/r006/disposition.md) | NOT CLEAN: dead-witness echo and unsafe exception normalization; old r005 mechanisms fixed; 123 focused tests pass per interpreter; change-of-implementer condition applies |
| v0a-i01-value-boundaries | r001 | [Disposition](v0a-i01-value-boundaries/r001/disposition.md) | NEW-SURFACE audit: three Important admission contracts; V2 ticket route not established; separate from r003/r004 fix scopes |
| v0a-i01-ab | r001 | [Disposition](v0a-i01-ab/r001/disposition.md) | R2-03 CLEAN/SOUND in two independent reviews; 127 focused per interpreter; scoped acceptance only |
| v0a-i01-ab | r002 | [Disposition](v0a-i01-ab/r002/disposition.md) | Policy identity corrected; NOT CLEAN for typed-refusal shape gap, preserved with reviewer severity dissent |
| v0a-i01-ab | r003 | [Disposition](v0a-i01-ab/r003/disposition.md) | Typed-refusal correction CLEAN/SOUND twice; 132 focused plus independent malformed-context campaigns on both interpreters |
| v0a-i01-ab | r004 | [Disposition](v0a-i01-ab/r004/disposition.md) | Value admission CLEAN/SOUND twice; 137 focused plus independent ingress probes on both interpreters |
| v0a-i01-ab | r005 | [Disposition](v0a-i01-ab/r005/disposition.md) | NOT CLEAN/STRAINED: failed-terminal implications and private-pair order; legal checker/oracle controls pass; Codex correcting locally |
| v0a-i01-ab | r006 | [Handoff](v0a-i01-ab/r006/handoff.md) | Parser follow-up CLEAN/SOUND twice;168 focused and independent campaigns on both interpreters |
| v0a-i01-ab | r007 | [Disposition](v0a-i01-ab/r007/disposition.md) | Publication/accounting CLEAN/SOUND twice; real native close failures covered; combined C integration checks running |
| v0a-i01-ab | r008 | [Handoff](v0a-i01-ab/r008/handoff.md) | NOT CLEAN/STRAINED: helper receiver/class qualifier provenance; Codex correcting locally, A/B unchanged |
| coverage-guidance | r001 | [Disposition](coverage-guidance/r001/disposition.md) | NOT CLEAN: coverage-only closure loop; corrected in r002 |
| coverage-guidance | r002 | [Disposition](coverage-guidance/r002/disposition.md) | CLEAN: category/discovery guidance and templates; independent evidence closure; source uncommitted, pending design edits excluded |
| v0a-i01-ab | r009 | [Handoff](v0a-i01-ab/r009/handoff.md) | NOT CLEAN/STRAINED: default/callback provenance loses reached effects; focused GREEN retained; bounded C repair open, A/B unchanged |
| v0a-i01-ab | r010 | [Disposition](v0a-i01-ab/r010/disposition.md) | NOT CLEAN; A: WRONG SHAPE, B: STRAINED. Four Important authority-loss findings; second contract residual. Separate bounded C reassessment next; A/B unchanged, no main integration |
| v0a-i01-c-authority | draft | [Current state](v0a-i01-c-authority/CURRENT.md) | Separate C authority-transfer FIX after r010 second residual; bounded identity/cell-state replacement and independent contract tests in progress; no frozen successor or main integration |
| review-guidance | r001 | [Disposition](review-guidance/r001/disposition.md) | NOT CLEAN; concurrent proposal isolated from intended commit; archived |
| review-guidance | r002 | [Disposition](review-guidance/r002/disposition.md) | CLEAN; exact reviewed workflow committed and pushed as d1ed3cb; concurrent edits preserved; refs archived |
| v0a-i01-freeze-tools-design | r002 | [Disposition](v0a-i01-freeze-tools-design/r002/disposition.md) | NOT CLEAN: codex-a WRONG SHAPE, codex-b STRAINED; three blocking classes; no implementation authority |
| v0a-consolidation | r004 | [Disposition](v0a-consolidation/r004/disposition.md) | Bounded CPU acceptance approved; exact r007 core preserved; inherited fixture caveat retained; source-seal decision pending |
| v0a-i01-seal | r001 | [Disposition](v0a-i01-seal/r001/disposition.md) | CLEAN/SOUND independent metadata review; three files beyond unchanged r004; specific decision-commit authorization pending, seal inactive |

The existing task verdict ledger remains at
[its original location](../Pontius-worktrees/v0a-increment-1-preregistration-review/progress.md).
New-round verdicts are issued in v0a-i01-prereg/progress.md; old verdicts are not
copied or rewritten. Relative legacy links resolve on this D: workstation only;
those packet files are not claimed to be included in this repository's backup.

[Program dispositions](progress.md) contain round outcomes; review verdicts remain
in [the task ledger](v0a-i01-prereg/progress.md).

[Increment-one current state](v0a-i01-impl/CURRENT.md) is a navigation page, not a frozen handoff.

[blueprint-r001]: v0a-blueprint-artifact-design/r001/handoff.md
[blueprint-r002]: v0a-blueprint-artifact-design/r002/handoff.md
[blueprint-open-r001]: v0a-blueprint-artifact-open/r001/handoff.md
