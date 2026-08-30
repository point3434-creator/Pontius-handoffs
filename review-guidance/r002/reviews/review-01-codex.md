# Follow-up documentation review: review-guidance/r002

Reviewer: Codex, independent reviewer (`/root/workflow_commit_cold`).
Issued: 2026-08-30. Tier A; one bounded FIX-round follow-up.

Candidate: b4dc05c6199c74e7c7afd45a60fbcea1a900cc8a
Manifest SHA-256: 3faad06f06dfd1c472aed30dde6dd359f5588e37b6c5a3491f6048a37d518130
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 8b1b9c5aff92900bb254c33a94128c4747329ddb
Ref: refs/heads/review/review-guidance/r002
Scope: frozen `docs/workflow.md`, its base diff, and closure of my r001 findings.

Verdict: **CLEAN**. No required correction remains in the reviewed scope.
Specification: PASS. Engineering quality: PASS for this documentation change.

## Prior finding closure

- **RG-01: CLOSED.** The r001 mandatory design-verdict/default-redesign section and its
  associated template requirements are absent. The retained guidance is offered where
  useful (160-179, 402-405). A compliant review need not emit a design classification.
  Lines 210-222 require evidence for a structural recommendation and explicitly state
  that recurrence is not an automatic rewrite and that the guidance authorizes none.
  The separately adopted second-residual isolation/root-cause rule remains at 199-206.

- **RG-02: CLOSED by scope isolation.** r002 no longer introduces the r001 category of
  advisory design findings that simultaneously carried finding status and a reproduction
  exemption. Required corrections and verification remain binding; separately marked
  implementation advice is advisory and cannot become an acceptance gate (156-177).
  The template reinforces that distinction at 402-405. Its retained finding/CLEAN rule
  and Stage 4's RED/GREEN rule govern required corrections, not a separate advice section.
  No reproduction-exempt finding category or mandatory design output remains to contradict
  them. An advisory-only review can be CLEAN; an unresolved required behavioral correction
  still prevents CLEAN and keeps its RED/GREEN duties.

The earlier r001 verdict remains unchanged and bound to its earlier candidate. This report
assesses only r002; it neither adopts nor rejects the excluded concurrent policy proposal.
No design-verdict category is imported from the excluded material.

## Scoped acceptance

- **Actionable guidance: PASS.** Lines 164-169 distinguish demonstrated cause from a
  hypothesis, require a falsifying check, connect technique to the protected invariant,
  and call for verification through the real public boundary and related in-scope paths.
- **Binding outcomes versus advice: PASS.** Lines 156-177 distinguish required corrections
  from optional implementation choices. Example techniques are not a mandatory catalogue
  or grounds to add dependencies. Guidance grants no reviewer implementation authority.
- **Patch/refactor/replacement assessment: PASS.** Lines 210-222 require a supported shared
  cause, a concrete reason another patch retains the weakness, the replacement boundary,
  preserved behavior, verification plan and transition risks. They do not authorize a
  rewrite or make one automatic after a residual count.
- **Existing safeguards: PASS.** Cold inputs and independence remain at 13-23 and 151-179;
  only the coordinator uses residual history beyond reviewer inputs (212-213). Fix scope,
  new-surface separation and second-residual isolation remain at 188-222. Required
  RED/GREEN, immutable candidates/reports, acceptance order and per-candidate controller
  commit authority remain at 183-184, 219-238 and 304-329.
- **Scope isolation: PASS.** The candidate changes only `docs/workflow.md` relative to its
  base. The r001-to-r002 delta removes only the excluded section and its template changes.
  CLAUDE.md interpreter notes are absent from the changed-path set. Mutable working bytes
  were not used as this candidate, and this reviewer did not edit or discard them.

## Fresh verification

All Git commands used `C:/Program Files/Git/cmd/git.exe` with repository `D:/Pontius`.

- `rev-parse` for the r002 ref, parent and tree: exit 0; all match the identities above.
- `diff-tree -r --no-renames --no-commit-id --name-status <base> <candidate>`:
  exit 0; exactly `M docs/workflow.md`.
- Complete `show <candidate>:docs/workflow.md`, captured as raw stdout bytes: exit 0.
  Length: 21,734 bytes. Blob SHA-256:
  `571ad5367c6446e081fcf91b45df26538a4e2db04afb6fd4c88a65d6127eedc3`.
- Reconstructed the canonical `<blob-sha><two spaces>docs/workflow.md<LF>` row. It exactly
  matches `manifest.sha256`; the reconstructed and file SHA-256 both match the bound
  manifest above. This computation uses frozen bytes, not the working file.
- Independently reconstructed r002 from frozen r001 by removing the mandatory design
  section and its associated template additions, restoring the original output line.
  The resulting bytes exactly match r002 and the blob SHA above; no other bytes differ.
- Strict UTF-8, LF-only, no BOM, final LF, no trailing whitespace and maximum 97 columns:
  PASS over all 408 lines. `diff --check <base> <candidate> -- docs/workflow.md`:
  exit 0, no output.
- Complete frozen-document read, base diff and r001-to-r002 diff: each Git read exited 0.
  The scoped review used r002's handoff, candidate and manifest, applicable root CLAUDE.md
  already read for this review, and my own r001 findings as the permitted FIX targets.

No material finding or residual remains in this documentation review. No source edits,
commits, pushes, code tests, broad suite or experiments were performed. The handoff makes
code tests inapplicable to this documentation scope; no runtime correctness claim is made.
The finalizer retains responsibility for preserving excluded working changes, integrating
only the reviewed candidate bytes, and satisfying the existing authorization/commit gates.
