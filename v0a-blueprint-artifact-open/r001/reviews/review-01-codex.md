# Independent Tier A metadata review: v0a-blueprint-artifact-open/r001

Reviewer: Codex, fresh independent Tier A metadata seat.
Date: 2026-09-05.
Round kind: NEW-SURFACE, mechanical documentation adoption.
Candidate: `964ae18a64eccc595526525536d0e53e02293b83`.
Base: `7ee314b443e10896e87a2e194f24eddda31ff77d`.
Tree: `5f7d7ec8b289db58dc84ab2e0d5f168254b62dd0`.
Manifest SHA-256:
`a6daf28c7bba5d7c531b39d31ea4f2e09c292339996a73baec0edb5bd523da1b`.

## Verdict

- Specification: **PASS**
- Engineering quality: **PASS**
- Required-correction verdict: **CLEAN**
- Findings: **Critical 0 / Important 0 / Minor 0**
- Shape: **SOUND**

No technical finding survives verification. The candidate faithfully adopts the exact
reviewed r002 design and narrowly bounded source-opening proposal without changing their
bytes or expanding their authority. It is locally technically ready to proceed to the
controller's post-CLEAN acceptance gate.

Publication, post-CLEAN acceptance, per-candidate decision authorization, ceremonial
commit and push remain incomplete. Those are workflow and authority gates, not defects in
this frozen candidate. This review grants none of those permissions.

## Findings

None.

## Frozen identity and population

The local review ref resolves to the named candidate. Its sole parent and tree reproduce
the declared base and tree. The base-to-candidate diff has exactly five paths:

- `STATUS.md`, modified;
- `docs/architecture/v0a-blueprint-artifact-r002/coverage.md`, added;
- `docs/architecture/v0a-blueprint-artifact-r002/design.md`, added;
- `docs/architecture/v0a-blueprint-artifact-r002/source-opening-draft.md`, added; and
- `docs/decisions/ADR-0490-open-the-portable-blueprint-artifact-source-round.md`, added.

There is no source, test, registration, CI, old-brief, prior-ADR, runtime or retained-
evidence change in the candidate. `git diff --check` exits 0. Raw inspection of all five
Git blobs finds strict UTF-8, no BOM or CR bytes, a final LF and no trailing whitespace.
The hand-authored adoption ADR and three copied documents remain within 100 columns.

Independent SHA-256 recomputation over `git cat-file blob` byte streams produced these
whole-row, digest-first manifest rows:

```text
11672166217301e9048de7048a209a11b9e36d4f334c674d5d7efd6d0d4356fc  docs/decisions/ADR-0490-open-the-portable-blueprint-artifact-source-round.md
346aa8c36c59d970bd1ae71ecdf86d64ccbe78c996f955e526f581b061c96808  docs/architecture/v0a-blueprint-artifact-r002/source-opening-draft.md
5403709d2ee8cc6b0cbacd7775ca7cf71f07f1eecba5e5902286a2387de1b96d  docs/architecture/v0a-blueprint-artifact-r002/design.md
96fe0c7a31f6a45d89b39673c631d0b0a506d84602fafc8c32a9984cf78458b3  STATUS.md
d83bfd196dc8fe9b632858a83abba77a7dc9d8ae9e3247ea1d1fed82de80b2e3  docs/architecture/v0a-blueprint-artifact-r002/coverage.md
```

The rows sort as complete byte strings, use two spaces before each POSIX path and end in
LF. Their exact 601 bytes match `manifest.sha256`; both independently hash to the bound
manifest identity. `candidate.json` contains exactly the required nine fields, and each
value matches the candidate, base, tree, manifest, ref, task, round and date inspected.

## Byte-identical reviewed inputs

The three adoption blobs have the same Git blob object IDs as candidate
`a552f6f34efe10155a702fd09a03bcc70802a369` in the original r002 object repository:

- coverage: `39048ade3357672da487227f58d6a231596a791c`;
- design: `b86c7385e496a87a6e77c42f57de8f28a76de7fe`; and
- source-opening draft: `37e3cc4977fa4f18f95bca17724d45fe66160830`.

Their raw SHA-256 values also reproduce ADR-0490's three pins. The r002 Review A, Review B
and append-only Review A format-clarification files independently reproduce the three
report identities printed by ADR-0490. The clarification is represented accurately as a
report-format correction that leaves the candidate, findings and design verdict unchanged.

## Faithful adoption

ADR-0490 adopts the reviewed API, closed schema, symmetric scalar domain, deterministic
encoding, separate raw/policy identities, direct-import boundary and independent acceptance
map. It adopts the proposal's exact new paths, six registration exceptions, evidence limits
and stop rules rather than granting a general sealed-byte or analyzer exception.

The six prospective registration-file blob pins all match the declared base. The ADR keeps
the codec/test, fixture, manual-registration-delta and review-round budgets; requires base
drift and unexplained generated deltas to stop the round; preserves the two Tier C reviews
for future implementation; and retains the complete real-runtime, replay, independent-
reader, refusal, scalar-boundary and source-gate acceptance map.

The copied proposal's draft wording is explicitly dispositioned: copying or reading it does
not activate authority, while an authorized ADR-0490 decision commit would satisfy its
conditional adoption language. The candidate does not treat the copied draft as an active
decision by itself. A working ADR and generated STATUS are also explicitly non-adopting.

No operating, experimental, rehearsal, training, policy-strength, capacity, source-seal,
analyzer-repair, H32, campaign, compiled-lane or Gate 13 authority is broadened. Historic
commits, reviewed candidates, issued reports, source seals, consumed identities, old briefs,
runtime source and retained evidence remain unchanged.

## Generated STATUS and focused evidence

The `STATUS.md` Current decision section is byte-for-text identical to ADR-0490's Decision
section. Its active-next, blocker, process-head, latest-ADR, decision-count and required-
reading changes agree with ADR-0490 metadata and the unchanged generator's rendering rules.
The resulting diff is limited to those mechanically expected front-door and rolling-ledger
updates.

The supplied focused-check receipt records, in floor-first order, the unchanged status
generator's `--check` and all 12 `test_status_generation.py` tests passing on CPython
3.11.15, followed by the same results on CPython 3.14.6, from fresh D-local snapshots with
the required isolation controls. Those are pre-review focused receipts, not adoption.

This reviewer did not rerun tests or project payloads. The controller has prepared but not
executed the fresh post-CLEAN acceptance snapshots. Accordingly, this report does not claim
that Stage 5 acceptance has passed; it establishes the required Tier A CLEAN review that
precedes that gate.

## Publication and authorization boundary

The local ref `refs/heads/review/v0a-blueprint-artifact-open/r001` exists and resolves to the
bound candidate. `publication-hold.md` records that the approval guard rejected the proposed
network publication before execution because explicit egress permission was absent. No
remote publication is claimed or inferred, and this review made no network request or push.

The technical verdict is CLEAN. The review ref and permanent handoff packet still await
publication authority. After the controller's post-CLEAN checks, adoption still requires
explicit authorization for this exact candidate, the ceremonial decision commit and its
push. Pending authority does not alter the zero-finding technical verdict, and the verdict
does not substitute for pending authority.
