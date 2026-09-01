# Cold design review: v0a-i01-freeze-tools-design/r001

Adversarial design review request.

Round kind: NEW-SURFACE. Tier C. Design/specification only.
Finalizer: `codex/finalizer` for this authority-tool checkpoint only.
Required independent reviewers: 2 (`codex-a`, `codex-b`).
Candidate ref: `refs/heads/review/v0a-i01-freeze-tools-design/r001`
Candidate commit: `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e`
Manifest SHA-256: `862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`
Base commit: `d1ed3cbda6107d61ea8e77133871720af04970cd`
Tree: `e8de257880c1a034091034fd17a6c4e2c6a5bfdb`

The commit plus manifest is the candidate identity. Independently verify the
pushed ref, single parent, exact five-path diff, modes, and manifest from frozen
Git blobs. Do not use checked-out candidate files as byte authority. Changed
bytes or changed scope require a new round.

## Candidate scope

- `docs/briefs/v0a-i01-freeze-tools-r001-brief.md`
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md`
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-runtime-boundary.md`
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md`
- `docs/superpowers/specs/2026-09-01-raw-object-workflow-amendment-v4.md`

This is a documentation-only design checkpoint. It contains no utility
implementation or tests and authorizes none. The workflow amendment is itself a
proposal under review; it is not adopted authority and grants no execution.

## Complete cold-input set

- this `handoff.md`, `candidate.json`, and `manifest.sha256`;
- the five frozen candidate blobs and their exact base blobs;
- `inputs/workflow.md`: adopted workflow capture, SHA-256
  `ab5202b170a5fd9c2cf1540aa198d4a82c742cb336134b0f9a8db944fd64f91a`,
  30,942 bytes; and
- `inputs/runtime-closure.json`: direct CPython closure, SHA-256
  `3390ab3d041d432f06754ca94aed348774c421de1c14553a25395c2cab112a3a`,
  413,522 bytes, 2,614 governed files, 63,499,244 governed bytes.

The pinned workflow capture governs this review over the older
`docs/workflow.md` blob inherited from the candidate base. Verify both input
hashes before assessment. Parse the runtime closure read-only; do not start that
runtime. Primary Microsoft, Git, and CPython documentation needed to verify API
semantics claimed by the frozen candidate may be consulted and cited.

No chat transcript, mutable P or H file, earlier v2-v7 draft or review, C
candidate, harness, Model, sensitive case, analyzer, controller artifact, prior
or peer review, `progress.md`, disposition, self-report, or unlisted check is a
cold input. Both reviewers receive the same immutable initial handoff packet
commit. Mutable handoff `main` is never review authority.

## Review contract

First record the governing invariants and a systematic seam inventory. Then
assess whether the five documents form one coherent and implementable design:

- the nonrecursive bootstrap is acyclic and cannot let unreviewed tools establish
  their own authority;
- component and role separation are complete and each entry point receives only
  the authority it needs;
- the launcher binds and holds the complete direct CPython runtime and exact
  child process facts for the stated threat model;
- the Git/GCM route closes executable, environment, config, credential-helper,
  ref, transport, timeout, output, and process-lifetime rerouting seams;
- raw blob/tree/commit/manifest construction avoids checkout, index, filters,
  attributes, and normalization drift;
- local and remote pair transitions distinguish ABSENT, EXACT, PARTIAL,
  DIFFERENT, UNKNOWN, malformed, unavailable, ambiguous, timeout, crash, and
  lost-ack states without rollback, deletion, or accidental authority;
- generated cold-input semantics and utility-review provenance are byte-bound
  without content recursion or self-bootstrap;
- failure residue remains monotonic and recovery relies on fresh state; and
- the tests and rehearsals can falsify every material acceptance claim within
  the stated size budget and trusted-computing-base limits.

Resolve any conflicting or looping requirement by naming the stronger invariant,
the weaker text that must be amended, and the smallest coherent correction. Do
not silently select one interpretation or enlarge permissions or scope.

Every Critical or Important finding must bind to this candidate pair, cite exact
frozen locations, state a concrete state/inputs to wrong-outcome scenario, name
the violated invariant, and give the required outcome and verification criteria.
Separate required corrections from advisory engineering techniques.

Each report states each of these fields exactly once:

- `Reviewer ID`
- `Candidate commit`
- `Manifest SHA-256`
- `Defect verdict`
- `Design verdict`

The defect verdict is `CLEAN` only when no Critical or Important correction
remains. The design verdict is exactly `SOUND`, `STRAINED`, or `WRONG SHAPE`,
with the justification required by the adopted workflow. Issue both even when
no defect survives.

Routine read-only Git inspection and blob-manifest calculation under the adopted
workflow are permitted. Do not implement, edit candidate bytes, execute the
pinned CPython runtime or any candidate artifact, run implementation tests,
mutate a network ref, publish C candidate or packet refs, mutate retained
evidence, or spend an experiment authority.

## Output contract

`codex-a` authors `reviews/review-01-codex-a.md`; `codex-b` authors
`reviews/review-02-codex-b.md`. Neither report is an input to the other review.
After fixing its report bytes, each issuer supplies exactly one append-only
ledger line for `../progress.md` containing date, round, reviewer, both verdicts,
candidate commit, manifest, report path, and report SHA-256. The coordinator
publishes each issuer-authored output through ordinary handoff packet rule 6.
