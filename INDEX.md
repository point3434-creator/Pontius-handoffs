# Pontius handoffs

Navigation only. A candidate's full commit and manifest SHA-256 bind its identity.
Private origin: https://github.com/point3434-creator/Pontius-handoffs.git.
Packet commits use the installed post-commit push hook; remote identity must
still be checked after each publication rather than inferred from hook success.

| Task | Round | Packet | State |
| --- | --- | --- | --- |
| workflow-proportionality | r001 | [Adoption](workflow-proportionality/r001/adoption-result.md) | ADOPTED ADR-0492, 7a387e9; three prospective workflow amendments |
| v0a-blueprint-artifact-impl | r001 | [Packet](v0a-blueprint-artifact-impl/r001/handoff.md) | Rejected; retained |
| v0a-blueprint-artifact-impl | r002 | [Packet](v0a-blueprint-artifact-impl/r002/handoff.md) | Incorporated with fixture r002 under ADR-0491, 53773cb |
| windows-handle-fixture | r001 | [Packet](windows-handle-fixture/r001/handoff.md) | Minor formatting rejection; retained |
| windows-handle-fixture | r002 | [Acceptance](windows-handle-fixture/r002/acceptance.md) | ADOPTED ADR-0491, 53773cb; 38 acceptance commands passed |
| v0a-blueprint-artifact-seal | r001 | [Packet](v0a-blueprint-artifact-seal/r001/handoff.md) | STATUS CRLF rejection; retained |
| v0a-blueprint-artifact-seal | r002 | [Adoption](v0a-blueprint-artifact-seal/r002/adoption-result.md) | ADOPTED 53773cb; exact source seal pushed; no operating authority |
| v0a-blueprint-artifact-open | r001 | [Packet][blueprint-open-r001] | ADOPTED c4af7f6 |
| v0a-blueprint-artifact-design | r001 | [Packet][blueprint-r001] | NOT CLEAN; retained |
| v0a-blueprint-artifact-design | r002 | [Packet][blueprint-r002] | Adopted ADR-0490 |
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

## One-hand file adapter

- [Design r001](v0a-hand-adapter-design/r001/disposition.md): retained NOT CLEAN.
- [Design r002](v0a-hand-adapter-design/r002/disposition.md): audit failed; no review.
- [Design r003](v0a-hand-adapter-design/r003/disposition.md): two CLEAN/SOUND reviews.
- [Source opening r001](v0a-hand-adapter-open/r001/disposition.md): CLEAN/SOUND;
  [adopted as abe5595](v0a-hand-adapter-open/r001/adoption-result.md).
- [Publication map](v0a-hand-adapter-design/publication-map.md): original-path mappings.
- [Publication complete](v0a-hand-adapter-open/r001/publication-result.md):
  four archive refs and all retained packets verified on the private remotes.

## Paired local evaluation

- [Source opening r002](v0a-evaluation-opening/r002/handoff.md): adopted ADR-0508,34616938; r001 retained unchanged.
- [Source progress](v0a-evaluation-source/progress.md): scoped checkpoints and whole-source review/acceptance; source seal and evaluation remain pending.

- [Paired evaluation source-seal metadata r001](v0a-evaluation-seal/r001/handoff.md): exact source incorporation; decision commit and remote upload pending.

## Bounded reads in paired evaluation v2

- [Review and qualification packet](v0a-evaluation-bounded-reads/publication.md):
  r001-r004 retained after adoption of ADR-0512 as 363c9fb. Original review types,
  verdicts and qualification wording are preserved; measurement evidence remains
  at its retained paths.

## Immutable blueprint preparation design

- [Design r001](v0a-blueprint-preparation-design/r001/publication.md): ADR-0513
  adopted as c9a8aa9; two CLEAN/SOUND reviews and floor-first status receipts.
  Remote publication follows the user's explicit packet authorization; original
  pre-authorization records remain unchanged.

## Immutable blueprint preparation source and seal

- [Source r001/r002](v0a-blueprint-preparation-source/r002/disposition.md): retained reviews, mechanical closure and complete source qualification.
- [Source-seal metadata r001/r002](v0a-blueprint-preparation-seal/r002/publication.md): ADR-0514 adopted as 7242891b; exact approval, review, checks and dispositions.

## Evaluation panel Slice A implementation design

- [Slice A r001](v0a-eval-panel-impl/r001/handoff.md): Codex draft; cold reviews pending.

- [Slice A r002](v0a-eval-panel-impl/r002/handoff.md): FIX; two cold reviews pending.

## Evaluation panel Slice A first source checkpoint

- [Code r001](v0a-eval-panel-code/r001/handoff.md): Claude draft; NOT CLEAN under two Codex reviews, all accepted.
- [Code r002](v0a-eval-panel-code/r002/disposition.md): withdrawn by the drafter before review (test-fixture receipt failure).
- [Code r003](v0a-eval-panel-code/r003/handoff.md): FIX of r001; NOT CLEAN under two Codex reviews, all three accepted in disposition.md.
- [Code r004](v0a-eval-panel-code/r004/handoff.md): FIX of r003 (0bc19bca); NOT CLEAN under two Codex reviews; second residual on cleanup and sample contracts — separate candidates by Codex next, root-cause note in disposition.md.

- [Evaluation panel ownership correction r001](v0a-eval-panel-ownership/r001/handoff.md): separate contract candidate; focused verification complete; cold review pending.

- [Evaluation panel sample r001](v0a-eval-panel-sample/r001/handoff.md): one CLEAN/SOUND
  Codex pass and Claude cold review 02 CLEAN/SOUND; 33 focused cases pass; published with controller approval.
- [Evaluation panel ownership r002](v0a-eval-panel-ownership/r002/handoff.md): final combined
  source, one CLEAN/SOUND Codex pass and Claude cold review 02 CLEAN/SOUND (two Minors); 35 focused cases pass; published with controller approval.
  [Ownership r001 disposition](v0a-eval-panel-ownership/r001/disposition.md) retains the rejected round.

- [Evaluation panel verification correction r001](v0a-eval-panel-verification/r001/disposition.md):
  two independent CLEAN/SOUND reviews; focused and post-review broad gates pass;
  local packet only, source adoption and public publication pending.

- [Timing finalizer ruling I-01](v0a-eval-panel-ownership/r002/finalizer-ruling-01.md):
  Important confirmed; d8d291cc and descendant 9fce4bf are NOT CLEAN for the intended
  cost-preflight decision. Earlier bounded reviews and passing receipts remain recorded.

- [Timing correction r001](v0a-eval-panel-timing/r001/handoff.md):
  withdrawn before review; original failed cutoff-fixture receipt retained.
- [Timing correction r002](v0a-eval-panel-timing/r002/disposition.md):
  two cold CLEAN/SOUND passes; focused and post-review broad gates pass;
  I-01 resolved on a40e29ca only; local packet, adoption/publication pending.
  [Historical closure ruling](v0a-eval-panel-ownership/r002/finalizer-ruling-02.md)
  preserves the original I-01 ruling on earlier source.

- [Timing r002 adoption](v0a-eval-panel-timing/r002/adoption-result.md):
  adopted locally as beb84be on codex/eval-panel-timing, exact reviewed tree;
  remote publication pending destination approval; review refs retained.

- [Timing r002 publication](v0a-eval-panel-timing/r002/publication-result.md):
  source adoption and handoff packets pushed and remote hashes verified;
  four candidate archives published; review refs retained pending deletion approval.

- [Timing review-ref retirement](v0a-eval-panel-timing/r002/retirement-result.md):
  authorized cleanup complete; all four candidates remain in verified remote archives.
