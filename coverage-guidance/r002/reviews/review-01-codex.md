# Independent review: coverage-guidance/r002

Reviewer: Codex, independent cold-context Tier-A documentation review.
Issued: 2026-08-30.
Verdict: CLEAN - r001 I1 closed; no required correction remains in scope.

Candidate commit: 81fb6cf6491b7ae87ca2a2a3ccd0a7103c4cfed3
Manifest SHA-256: 2c9903843b765143f2f2a33c4c3e0233ff0ca9c907faae9462f12b2577e56fdc
Ref: refs/heads/review/coverage-guidance/r002
Base: d1ed3cbda6107d61ea8e77133871720af04970cd
Tree: 33dc90fc78bb8ec62f07c7afed82f6b4b2a4851e
Prior candidate: d07b11e874955121487351a20104dec5176f9cb3
Prior manifest: dd4dcf342e86556db151871fb1e5292ff0cd0f68e8160f969c9ff5f90bdd5c6b

## Required findings

None. Important finding I1 from the allowed r001 review is closed.
Confidence: high for the documented closure paths; no runtime claim is made.

Stage 1 now directs coverage-only corrections to Stage 4. Stage 4 explicitly
allows the independent check to pass on the rejected implementation and requires
neither an invented product failure nor a production edit. Demonstrated defects
still require deterministic RED against the rejected candidate before production
edits and integrated GREEN afterward. A coverage check that exposes a defect
transfers that defect to this ordinary path. Frozen workflow lines 61-65 and
191-197 therefore resolve the two unconditional obligations identified in I1.

## Requirement and scenario walkthrough

- Demonstrated defect: the A-then-B contract loses B. Reproduce the failure on
  the rejected candidate, fix production behavior, then obtain integrated GREEN.
  Lines 191-193 retain that obligation. Pass.
- Missing check, correct behavior: the rejected implementation preserves A and B,
  but the suite checks only A. Establish the gap, add the independent A/B check,
  and record its passing result. Lines 193-196 explicitly permit closure without
  a failing product test or production change. Pass.
- Unsound prior evidence: an implementation-derived oracle or structural helper
  assertion cannot establish the real contract. Replace that evidence with an
  independent behavioral check; lines 230-238 remain binding. Its actual result
  selects the evidence-only or demonstrated-defect path. Pass.
- Newly exposed defect: if the new A/B check fails because B is lost, lines
  196-197 require ordinary RED/GREEN for the defect. Coverage terminology cannot
  exempt the product correction. Pass.
- Unresolved coverage: a missing, inconclusive, or unsound check does not close
  the unmet acceptance requirement. Lines 161-166 and 222-238 still prevent CLEAN
  while a required correction remains unresolved. Pass.
- Advisory concern: a design preference does not become a blocking coverage
  finding. The acceptance requirement and concrete unverified scenario threshold
  in lines 222-229, and the advisory distinction in 183-187, are unchanged. Pass.
- Existing gates: identity, immutable rounds, frozen fix scope, independent
  review, severity, residual escalation, real-boundary evidence, isolated
  verification, and per-commit authorization remain unchanged. The exact prior
  candidate diff changes only the two opening paragraphs. Closure does not
  authorize acceptance, integration, a replacement, or a commit. Pass.

Specification verdict: Pass for FIX I1 only.
Engineering-quality verdict: Pass; the narrow rule is coherent and proportionate.

## Independent inventory and deferred claim

Before opening coverage.md, recorded the eight-path inventory in
checks/review-01-codex-initial-inventory.md, SHA-256:
b42fd8759a35c75283613faf4007e5e77ca603c669ae471007d4fe02727101a0.
It was derived from the frozen workflow, applicable authorities, requirements,
and allowed r001 I1, not the author's coverage claim.

Then read coverage.md and independently verified its supplied SHA-256:
b293a9260ff3556f1384fe943414332e46ddc40d55db6d6a5f019c43e190da4a.
The claim's defect, passing-evidence, newly exposed defect, and advisory cases
match the inventory. The independent pass additionally checked unsound evidence,
unresolved checks, residual/replacement rules, and the unchanged gates. The
claim's concise scope does not exclude those obligations or assert exhaustive
runtime coverage. No missed closure path creates a required correction.

## Consistency and advisory wording

No operative instruction found requires product RED merely to close the
coverage-only scenario whose independent check already passes. The implementer
role summary at lines 28-29 and the brief's RED-target placeholder at line 426
are general descriptions, read with the explicit Stage 1/Stage 4 rule. The
replacement paragraph at lines 259-262 governs a chosen replacement; it does not
require a replacement for evidence-only closure. The broad-suite GREEN gate
concerns verification scope and never supplies a product-RED requirement.

Optional advice only: the role summary could say 'required verification evidence'
or point to Stage 4 to avoid leaving its generic RED/GREEN wording to context.
This is not a required correction or an acceptance gate. No extra design verdict,
rewrite, dependency, or review pass is recommended.

## Fresh verification evidence

Environment: Windows PowerShell, repository D:/Pontius. All Git invocations used
C:/Program Files/Git/cmd/git.exe; no PATH lookup or safe.directory change.

- rev-parse refs/heads/review/coverage-guidance/r002 returned the stated commit.
- show -s --format=%H%n%P%n%T confirmed the stated commit, parent, and tree.
- diff-tree --no-renames --no-commit-id --name-status -r from the stated base
  to candidate returned exactly M docs/workflow.md.
- diff --no-ext-diff --no-renames from prior candidate to candidate showed only
  Stage 1 and Stage 4 opening-paragraph changes. diff --stat: one file,
  10 insertions and 4 deletions.
- cat-file blob read stored candidate bytes through redirected raw stdout.
  Independently computed blob SHA-256:
  51ca0741ebe4ed0289525642967deabbf4c422ba830c7fd781d3ad2b1119d39b.
- Reconstructed the one whole-row-sorted manifest using that blob hash, two
  spaces, docs/workflow.md, and LF. It equals manifest.sha256 byte for byte;
  both independently hash to the manifest digest bound above.
- diff --check from the prior candidate to candidate exited 0. The raw workflow
  blob contains no CR, UTF-8 BOM, trailing whitespace, or lines over 100 columns.
- Read the complete frozen workflow and exact diff; inspected frozen CLAUDE.md,
  workflow-amendment-2026-08-30.md, and PROJECT.md's evidence/dissent authority.
  A frozen-source search for RED, GREEN, Each finding, Every binding,
  coverage-only, CLEAN, and advisory located the related obligations above.

All verification commands completed with exit 0. No runtime suite was run:
this authorized light pass is a document-consistency review, not a runtime fix.

## Limits and disposition

Known: the frozen wording supplies coherent closure paths and preserves the
existing gates. Opposing consideration: the unchanged role shorthand is less
specific than the operative closure rule; it does not defeat that explicit rule.
Largest unknown: the adequacy of future behavioral checks, which this document
cannot prove. Cheapest falsifying check: identify an operative instruction that
requires a product failure for the passing-evidence scenario. That would defeat
this consistency verdict; the complete workflow walkthrough found none.

Recommend accepting the I1 correction for review purposes only. This is not a
claim of final acceptance or authorization to commit.

No mutable workflow bytes, before/after narratives, implementer discussion,
other reviewer inputs, pending design-verdict edits, or separate task inputs were
used. The initial status query only observed pre-existing working changes, which
were preserved. No production imports, tests, source changes, issued-input edits,
commits, pushes, or integration were performed. Unchanged freeze scripts and
unrelated procedures were not separately audited.
