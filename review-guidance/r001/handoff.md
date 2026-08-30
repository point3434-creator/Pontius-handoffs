# Review-guidance r001: documentation-only review
Round kind: NEW-SURFACE. Tier A. Finalizer: Codex.
Candidate: e6e525bd51c4cd4e455b90522fc5a975f0b598ea
Ref: refs/heads/review/review-guidance/r001
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 611ef5171cf60b14cd124dc3e4b3e2995d785811
Manifest SHA-256: 8e60c05ff6f7959ab3db46e24495e738259a24569f34fc643f94680ff3ab89ab

Scope: docs/workflow.md only. No runtime or test changes. CLAUDE.md's pending
interpreter guidance and .tmp.driveupload/ are excluded from this candidate.

Controller request: future reviews should include useful engineering/coding
techniques and consider replacing a slice when local debugging is not converging.
The controller authorized committing this documentation update if ready.

Acceptance:
- Concrete advice links supported cause or hypothesis, invariant, technique
  and verification; implementation preferences cannot become hidden gates.
- Structural refactor/rewrite assessment is evidence-based, scoped and optional.
- Existing independent cold review, immutable inputs, residual escalation,
  RED/GREEN, acceptance and commit-authority requirements remain intact.
- Include the already adopted pending residual-based workflow rule because
  the new rewrite guidance depends on it. New surface stays separate.
- No rewrite, implementation integration or experiment is authorized here.

Read only frozen blob plus base diff and applicable primary process rules.
Do not read prior reviews or implementer narratives. One light independent
documentation pass is sufficient. Return a bound report in reviews/ and append
one own verdict in ../progress.md when given the exclusive ledger slot.
Checks: frozen identity, exact changed-path set, LF/no BOM, <=100 columns,
no trailing whitespace, coherent rules. No code tests or broad suite required
for this document-only scope; no runtime correctness claim is made.
