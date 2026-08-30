# Independent review: coverage-guidance/r001

Reviewer: Codex, independent cold-context Tier-A documentation review.
Issued: 2026-08-30.
Verdict: FINDINGS - one Important required correction; not CLEAN.

Candidate commit: d07b11e874955121487351a20104dec5176f9cb3
Manifest SHA-256: dd4dcf342e86556db151871fb1e5292ff0cd0f68e8160f969c9ff5f90bdd5c6b
Ref: refs/heads/review/coverage-guidance/r001
Base: d1ed3cbda6107d61ea8e77133871720af04970cd
Tree: 382e757476f8b9f6b1dd441a73852d53ae25f183

## Required finding

### I1 - Give coverage-only findings a coherent closure rule

Severity: Important (bounded process correctness). Confidence: high in the
textual ambiguity; the consequence below is a prospective scenario, not an
observed failed round.

Location: frozen docs/workflow.md:220-223, interacting with lines 190-191.

The new rule permits a blocking coverage finding that names an unmet acceptance
requirement and a concrete *unverified* failure scenario, without demonstrating
a product defect. Stage 4 still says that each finding requires a deterministic
RED reproduction against the rejected candidate before the production edit,
followed by integrated GREEN. It does not distinguish a missing-evidence finding
from a demonstrated behavioral failure.

Concrete scenario: acceptance requires a real-boundary compound-fault check for
causes A then B. The product already preserves both causes correctly, but the
candidate only tests A. The reviewer appropriately raises a coverage finding.
Adding the missing independent A/B check passes on the rejected implementation;
there is no product failure to reproduce and no production edit to make. A
literal application of the unchanged "each finding" rule leaves this valid
coverage correction without a compliant closure path, or encourages a contrived
RED test. This undermines the intended distinction between coverage concerns
and product defects and can impose avoidable work.

Required outcome: explicitly define acceptable closure evidence for coverage-only
findings, while retaining deterministic RED/GREEN for demonstrated behavioral
defects. For example, establish the missing or unsound coverage directly, then
supply the independent behavioral check and its result; a pre-fix GREEN result
must be valid when the defect was missing evidence. No production edit or
additional approval stage should be implied. The exact wording is advisory.

Verification criterion: a document walkthrough must give coherent outcomes for
both (a) a demonstrated product failure requiring RED/GREEN and (b) an unmet
coverage requirement whose newly added behavioral check passes on the rejected
product. Advisory coverage/design concerns must remain non-blocking.

## Requirement and consistency assessment

| Requirement / risk | Frozen evidence | Result |
| --- | --- | --- |
| Small claim before fixing; update and freeze members, method, cases, limits and falsifier | Lines 206-215, 421-422 | Pass |
| Independent inventory before author claim; unprimed initial inputs | Lines 153-159, 208-209, 433-439 | Pass |
| Shared discovery; coverage graded separately from product defects | Lines 216-223 | Intent satisfied; closure ambiguity I1 remains |
| Independent behavioral oracles and honest fault reachability/order | Lines 224-232, 448-452 | Pass |
| Packet and templates consistent with unchanged review rules | Lines 316, 421-422, 432-452 | Partial: I1 interacts with Stage 4 |
| No extra approval, dependency, broad suite or exhaustive proof obligation | Lines 156-157, 213-214; bounded diff | No explicit new gate; I1 can create unintended burden |

Specification verdict: partial; one material process clarification required.
Engineering-quality verdict: otherwise proportionate and coherent. The change
makes reviewer discovery shared work and requires real behavioral expectations
without prescribing an implementation or demanding exhaustive combinations.
No additional design gate or broader rewrite is recommended.

## Verification evidence

All Git commands used C:/Program Files/Git/cmd/git.exe in D:/Pontius.

- rev-parse resolved the supplied ref to the exact candidate commit.
- show --no-patch confirmed the exact parent and tree stated above.
- diff-tree --no-commit-id --name-status -r confirmed exactly one modified path:
  docs/workflow.md. The base-to-candidate delta is 49 additions and 2 deletions.
- cat-file blob read the stored candidate bytes directly. SHA-256:
  2f22a1467359a2b03954f556ba8c6e1369192b9bc3b02acd278aab611f99e7e2.
- Reconstructed the manifest from that hash and the one changed path as the exact
  UTF-8, LF-terminated row. It equals manifest.sha256 byte-for-byte and hashes to
  dd4dcf342e86556db151871fb1e5292ff0cd0f68e8160f969c9ff5f90bdd5c6b.
- diff --check for the exact base/candidate pair exited 0. The frozen workflow
  blob contains no CR bytes and no UTF-8 BOM.
- Read the complete frozen workflow and its base diff, with frozen CLAUDE.md and
  the workflow amendment only for applicable authority and consistency.

## Scope and limits

This is one light review of the prospective docs/workflow.md refinement. It is
not runtime verification or proof that future coverage declarations are correct.
No tests or Python imports were run; no code tests are needed for this document
review. No mutable workflow file, edit-boundary narratives, implementation
conversation, other reviewer inputs, or pending design-verdict edits were used.
The status check merely observed existing working changes, which were preserved.
Unchanged freeze scripts and unrelated procedures were not separately audited.
No source, issued packet inputs, or other reports were edited. No commit, push,
or integration was performed. This report grants no ceremonial-commit authority.
