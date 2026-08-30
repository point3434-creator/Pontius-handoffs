# Cold documentation review: review-guidance/r001

Reviewer: Codex, independent cold reviewer (`/root/workflow_commit_cold`).
Issued: 2026-08-30. Tier A; one bounded documentation pass.

Candidate: e6e525bd51c4cd4e455b90522fc5a975f0b598ea
Manifest SHA-256: 8e60c05ff6f7959ab3db46e24495e738259a24569f34fc643f94680ff3ab89ab
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 611ef5171cf60b14cd124dc3e4b3e2995d785811
Ref: refs/heads/review/review-guidance/r001
Scope: the frozen `docs/workflow.md` blob and its base diff only.

Verdict: **NOT CLEAN**. Two Important corrections remain.
Specification: FAIL. Engineering quality: FAIL (contradictory procedural requirements).
Design verdict: **SOUND**. Separating binding outcomes from advisory techniques fits the
contract. The defects below are conflicting policy clauses, not a reason to replace this
workflow's overall structure.

## Required corrections

### RG-01 - Important: optional assessment becomes a mandatory policy

Confidence: high. Location: `docs/workflow.md:181-205`, especially 181-183 and 201-205.

The handoff requires structural refactor/rewrite assessment to remain optional and says
implementation preferences cannot become hidden gates. The candidate instead requires a
design verdict in every review, explicitly says this cannot be skipped, and makes redesign
the default after any WRONG SHAPE verdict, with a mandatory written justification to patch.
The adjacent statement that design findings remain advisory until controller adoption does
not remove those unconditional requirements.

Concrete failure scenario: a compliant candidate receives a defect-CLEAN review and an
advisory WRONG SHAPE recommendation. The controller has not adopted the recommendation and
no second residual exists. Lines 198-199 say that recommendation cannot block the candidate
on its own, but lines 201-205 require a redesign disposition or a written reason to continue
patching solely because the reviewer expressed that preference. Even without such a
recommendation, an ordinary review cannot omit the assessment under lines 181-183. This
changes the optional assessment promised by the acceptance map into a mandatory obligation.

Required outcome: keep assessment and implementation choices optional within the authorized
scope. Remove the unconditional design-verdict/default-redesign obligations, or obtain a
new explicit controller brief that adopts them before reviewing a replacement candidate.
Preserve the separately adopted second-residual isolation and root-cause requirements.

Verification: walk a compliant defect-CLEAN candidate with no design advice, and then one
with unadopted design advice and no second residual. Both must remain eligible for the
existing gates without a mandatory design classification or rewrite/patch justification.

### RG-02 - Important: advisory findings still trigger binding correction gates

Confidence: high. Location: `docs/workflow.md:191-210` and `docs/workflow.md:424-435`.

The new text says design findings need no reproduction and do not block a candidate on
their own (191-199). Stage 3 now correctly limits CLEAN to unresolved required corrections
(156-158). However, Stage 4 still requires deterministic RED for "Each finding" (209-210),
and the cold-review template still permits CLEAN only if "no finding survives verification"
(426-427). The template also requires a concrete failure scenario for every Important
finding (424-425), while design findings are only forbidden from being Critical (198).

Concrete failure scenario: a reviewer using the required template reports no behavioral
defect and one supported, unadopted advisory design finding. Stage 3 allows CLEAN, but the
template disallows it while that finding survives. If a fix round is opened for it, Stage 4
requires a RED reproduction despite the express no-reproduction rule. The same review can
therefore pass or block solely according to which mandatory passage its reader follows.
This gives advisory implementation preferences a hidden gate and makes the rules incoherent.

Required outcome: use one consistent distinction between required behavioral corrections
and advisory design findings in Stage 4 and the template. Apply defect reproduction and
CLEAN gating only to the required corrections; an advisory finding must not activate them.
An independently demonstrated behavioral defect must retain its existing RED/GREEN duties.

Verification: trace an advisory-only review through Stage 3, the cold-review template,
Stage 4, and Stage 5. All must permit the same CLEAN result without demanding a defect
reproduction for advice. Trace a required behavioral correction through the same passages;
it must still prevent CLEAN until resolved and retain the RED/GREEN requirement.

## Acceptance and evidence

- Cause/hypothesis, invariant, technique, public-boundary verification: PASS at 160-179.
  The technique examples are explicitly optional and do not authorize reviewer fixes.
- Optional structural assessment and no hidden advice gates: FAIL under RG-01 and RG-02.
- Evidence-based, bounded replacement guidance: PASS at 236-248. It names the boundary,
  preserved behavior, verification and transition risks, restricts cold reviewers to their
  inputs, and does not itself authorize a rewrite.
- Cold independence, immutable inputs, separate new surface, second-residual isolation,
  acceptance ordering and per-candidate commit authority: their explicit rules remain
  present at 13-23, 214-248, 250-264 and 330-355. RG-02 prevents a clean coherence verdict.
- No implementation integration, experiment, or rewrite authorization: PASS at 178-179
  and 248, read together with the handoff's explicit exclusions.

Fresh checks used `C:/Program Files/Git/cmd/git.exe` against `D:/Pontius`:

- `rev-parse` of the review ref, candidate tree and parent: matched the bound identities.
- `diff-tree -r --no-renames --no-commit-id --name-status <base> <candidate>`:
  exit 0; exactly `M docs/workflow.md`.
- Complete `show <candidate>:docs/workflow.md`, captured as raw stdout bytes: exit 0.
  Blob length: 23,635 bytes; SHA-256:
  `46fd7af39c330cea8086d49a5d92a14fc7874ed781b2269084f8b1f9c947f3b7`.
- Rebuilt the canonical `<blob-sha><two spaces>docs/workflow.md<LF>` manifest row.
  It byte-matched `manifest.sha256`; its SHA-256 matched the full bound manifest above.
- Strict UTF-8 decode, LF-only, no BOM, final LF, no lines over 100 columns and no
  trailing whitespace: PASS across all 438 lines.
- `diff --check <base> <candidate> -- docs/workflow.md`: exit 0, no output.
- `diff --no-ext-diff --unified=10 <base> <candidate> -- docs/workflow.md`: exit 0;
  reviewed the complete diff and frozen document against the handoff and root CLAUDE.md.

One partial display command piped `git show` into `Select-Object -First 149`, which closed
its pipe early and returned nonzero after printing the requested lines. A full capture
followed by local slicing exited 0; independent raw-blob capture also exited 0. This was
a display-command issue, not a candidate failure, and is not counted as a passing check.

No prior reviews, implementer transcripts or narratives were consulted. The unrelated
working changes were not reviewed. No source edits, commits, pushes, code tests or broad
suite were performed. Tests are inapplicable under this documentation-only handoff;
no runtime correctness claim is made. The review does not itself authorize integration.
