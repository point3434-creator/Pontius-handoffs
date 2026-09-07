# Adversarial source review: selectable decision provider

Tier C. Round kind FIX. Finalizer Codex (root implementer).
Candidate ref: refs/heads/review/v0a-decision-provider-implementation/r002
Commit: 4d567797e4b3945ea3ff6c75613c56c05bc0b75a
Base: fc99ab1a02649b82ba3bc21e5db79cb9c6e25829
Tree: 95deb812dd8f5cad79b3973a2c35346fabbfd0ad
Manifest SHA-256: 7d273ea40ca8b3c251ad029a8ab8ca423312703661b3c14a3bf01a375fece58b
Repository containing the immutable ref:
D:/Pontius/tmp/v0a-decision-provider-implementation-r001/authoring
Published packet: D:/Pontius-handoffs/v0a-decision-provider-implementation/r002

Scope is exactly the 23 paths in manifest.sha256, including generated registration.
Named review slices: provider values/rules/selection; runtime/codec timing and failure;
source-admitted adapter/host/session transport; registration and cross-slice integrity.
Both reviewers independently assess every slice and all cross-boundary invariants.
Recompute the complete changed-path manifest from frozen Git blobs using whole-row
byte sorting and LF. Read source from the frozen commit, never mutable author files.

Permitted cold inputs are this handoff, candidate.json, manifest.sha256, source.diff,
review.diff, files/, source-audit.json, focused-evidence.json, registration-census.json,
and these unchanged
requirements/dependencies from the candidate tree:
CLAUDE.md; docs/workflow.md (checklist v1); docs/architecture/v0a-decision-provider-r001/
brief.md, design.md, source-contract.md; docs/superpowers/plans/2026-09-06-decision-provider.md;
docs/decisions/ADR-0505-open-the-selectable-decision-provider-source-round.md.
Follow dependency code where needed to verify these contracts. Do not read other
reviewer reports, authoring transcripts, task progress or implementer explanations.
The focused-evidence table names development receipts, not final acceptance.
Final named acceptance gates have not run and must follow both CLEAN source reviews.

FIX deferred input: coverage.md, SHA-256 ff080e16d41d0e31d78c08bd13329d7d4dc4dd1f7f94b3be41906ec20c6d872e.
Do not open it until your initial invariant and related-path inventory from the
requirements and frozen source is recorded. Then compare its category, discovery
method, members, exercised cases, limits and falsifier against your independent
inventory. Anchor is19227191696052837770ab68492705ffad60a87d; correction.diff
contains the exact cumulative delta from that anchor. Both full-scope reviews are
fresh and independent; no earlier review verdict is transferred to the new bytes.

User ruling: additional routine within-scope correction rounds are permitted without
asking solely to exceed the original one-correction count. All source/file/line bounds,
review independence, sealed history and per-decision commit authority remain binding.

Assess exact public API and wire schemas; private-data separation; legal rule order;
provider and source identity; immutable ownership; continuous-clock precedence;
ordinary fallback versus fatal engine faults; actual application and delivery state;
every writer/consumer pair; legacy v1 equivalence; literal independent expectations;
real child/source/pipe controls; complete analyzer accounting and old capability grants;
source scope and proportionality. Do not rerun baseline rules as a strength oracle.

Write an attributed report with separate specification and quality verdicts, severity
counts, concrete inputs/state-to-wrong-outcome for each Critical/Important finding,
required correction and verification, and required Design SOUND/STRAINED/WRONG SHAPE
verdict. CLEAN requires no surviving required finding. Do not implement corrections.
Record the manifest+commit in the report and one verdict line in the task ledger.
Each reviewer writes only its assigned reviews/review-a.md or reviews/review-b.md.

Read-only review and static checks are sufficient where conclusive. Any focused
reproduction must use a fresh D-local exact-candidate snapshot, actual 3.11.15 first,
-B -P, scrubbed environment, snapshot cwd/src and absolute PONTIUS_GIT. Coordinate
reproduction names through root; never run a payload from the primary checkout.
No broad suite, demo, random population, live play, training, source edit, cleanup,
primary commit or push is authorized by this review request. Do not spawn subagents.
