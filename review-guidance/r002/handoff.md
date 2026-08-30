# Review-guidance r002: scope-isolated documentation correction
Round kind: FIX. Tier A. Finalizer: Codex.
Candidate: b4dc05c6199c74e7c7afd45a60fbcea1a900cc8a
Ref: refs/heads/review/review-guidance/r002
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 8b1b9c5aff92900bb254c33a94128c4747329ddb
Manifest SHA-256: 3faad06f06dfd1c472aed30dde6dd359f5588e37b6c5a3491f6048a37d518130

Scope: docs/workflow.md only. The corrected candidate excludes the concurrent
Design verdict (required) section and its associated mandatory template edits
present in r001. It restores the reviewed document's final LF. The concurrent
edits were absent from the reviewed draft and intended commit; all remain
byte-identical in the primary working file. Never use that mutable file as
this candidate. A reconstruction hash proves the original reviewed bytes.

Acceptance:
- Review advice connects cause or hypothesis, technique, invariant and verification.
- Required outcomes remain binding; advisory design choices introduce no hidden gate.
- Evidence can justify a bounded refactor/rewrite recommendation; rewriting is not
  an automatic consequence of a design label or residual count.
- Existing scope, residual escalation, cold review and acceptance gates remain.
- Include the already adopted residual-rule update on which this guidance depends.
- Exclude the separate CLAUDE.md interpreter notes and concurrent design-verdict
  edits without changing or discarding either from the working tree.

User authorized committing the reviewed documentation when ready. This is scope
isolation of that commit, not rejection or implementation of the external addition.
No runtime/implementation integration, broad suite or experiment is authorized.

Read frozen blob/base diff and applicable process rules. Return one light review,
bound to this pair. Prior r001 findings may be used as this FIX round's targets.
No code tests needed: exact-path/identity and documentation checks are sufficient.
Create reviews/review-01-codex.md and append your own verdict to ../progress.md.
