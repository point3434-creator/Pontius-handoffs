# r001 independent cold Tier A metadata review A

Issuer: Codex agent /root/seal_metadata_review. Date: 2026-09-06.
Task: v0a-decision-provider-seal/r001. Finalizer: root implementer.
Scope: incorporation metadata only, under the ADR-0503 integration precedent.

Candidate: 68c3fd24702a575ec5f9468c70f209e127f7f688.
Manifest SHA-256: c1fb04e1599c56033e80b3273dcb718f0fb1ec7613fb728d3761c0bd9123569c.
Tree: 1e5d9491a979ad59938b0b1b35146a574bf9badf.
Base: fc99ab1a02649b82ba3bc21e5db79cb9c6e25829.
Source candidate: 4d567797e4b3945ea3ff6c75613c56c05bc0b75a.
Source manifest SHA-256: 7d273ea40ca8b3c251ad029a8ab8ca423312703661b3c14a3bf01a375fece58b.
Source tree: 95deb812dd8f5cad79b3973a2c35346fabbfd0ad.

## Verdict and required findings

CLEAN for the independent metadata-review stage. Specification: CLEAN.
Engineering quality: CLEAN. Design: SOUND. Required findings: Critical 0,
Important 0, Minor 0. No required correction remains in this review scope.

This verdict binds only to the full candidate and manifest pair above. It is not
final executable acceptance, a source-seal activation, commit/push approval, or
permission to run poker. Fresh exact-metadata-candidate status --check and all
12 status tests on actual CPython 3.11.15 first and 3.14.6 second remain pending,
followed by the controller's explicit authorization of the exact decision commit.

Design is SOUND because this is the established bounded incorporation pattern:
reviewed source blobs stay identical; the new decision records their acceptance
and limitations; generated STATUS projects that decision. The metadata adds no
provider behavior, source exception, acceptance substitution or invocation grant.

## Independence and inputs

I did not author this candidate, inspect an author conversation transcript, or
consume another metadata review. I read the handoff, candidate/manifest and
incorporation record; frozen CLAUDE.md and docs/workflow.md; frozen ADR-0503,
ADR-0505 and its adopted source contract; the entire new ADR-0506 and the STATUS
delta. The supplied r002 source reviews, registration records and acceptance
receipts were used to check the metadata's factual claims and bindings.

Source semantics were not re-reviewed and no repository tests or analyzer were
executed. Frozen source identity and scope were inspected through Git blobs and
trees in the supplied authoring object store, with per-command safe.directory.
Read-only Python scripts used only standard-library hashing, JSON, path and Git
subprocess inspection; they imported no Pontius code.

## Independent identity, scope and incorporation evidence

I recomputed both changed-path manifests from raw frozen Git blobs. Changes were
enumerated against each candidate's parent with rename detection disabled; each
SHA-256 row used two spaces, a POSIX path and LF, and complete rows were sorted
before hashing. The integration manifest bytes equal the supplied manifest file,
and both recomputed digests equal the identities stated above. rev-parse confirms
the frozen integration ref, both trees and both candidates' stated base parent.

The integration has exactly 25 changed paths. The accepted source has exactly 23,
all byte-identical when extracted from the integration candidate. Its population
matches the source contract exactly: 12 existing-file exceptions and 11 additions
(five provider modules, four test suites and two fixtures). The only source-to-
integration changes are:

- STATUS.md.
- docs/decisions/ADR-0506-source-seal-the-selectable-decision-provider.md.

Tree comparison against source-contract B, e205cd8cd6f46a50db8b2d0cb1f39366da0f2767,
independently confirms 1,825 unchanged older blobs. B has 1,838 paths; the other
13 are the twelve explicit source exceptions plus generated STATUS. There is no
unexplained modification to an older path. This also preserves the named old
model, trace, clock, spine, kernel, evaluator, seeded generator and historical
rehearsal driver/bindings.

Raw diff accounting independently confirms the ADR's 890 production added/removed
lines, 1,185 new-suite lines and 142 manual registration added/removed lines.
The two raw fixture blobs total 4,712 bytes. These agree with the reviewed source
reports and are within ADR-0505's ceilings. Generated inventory/profile data is
excluded consistently with the adopted contract.

Both metadata blobs are LF-only, BOM-free and have no trailing whitespace.
ADR-0506's maximum line width is 97. STATUS retains the established generator's
long Markdown table/link lines; this is generated layout, not a new prose rule.

## Factual claims and evidence bindings

The following referenced artifacts were independently hashed and matched the
full SHA-256 values in ADR-0506:

| Artifact | Verified SHA-256 |
| --- | --- |
| r002 source review A | 7265f4d8e092abe52f2348cccb1e8e1f34e71cdff1e662f8ddc920c56350bbd9 |
| r002 source review B | 0bed213f9c8a7d7219cc99466a21d0a9771f3969c192a6976ddb023622961f1b |
| Final source acceptance summary | 05f0390a50346209d14a6fef1e23b1d89889396104edd3461d4171bedfbca491 |
| Registration evidence | 7f85fdc51c00283079be7cb1596f04b871a1b1b842fbf9a67c8d6efe59f03584 |
| Complete census comparison | 84f7bb92d6ffaabd060dd8c29025ae52a3922981a3b4f8f3f48af9bf2d6ad49a |
| Complete analyzer report | 56d1392a4dda104c829f3a33ef5edbc07af5588b97dbb7335375d3e7ae63f07f |
| Complete raw analyzer detail | 574739ae96a2d29a3e57aba2eaa7d77fcbba2452032f52bab5dd8762cdff3e7c |

The source reports identify the stated independent issuers, bind to the accepted
source pair and each give CLEAN/CLEAN, C/I/M 0/0/0 and SOUND. Their permanent local
handoff copies are byte-identical. The original r001 reports remain present and
NOT CLEAN. Their standing is not silently upgraded by the new decision.

All 52 selected source receipt files match their indexed hashes. For each slot,
the ordered 26-command list exactly matches the frozen source contract. Every
receipt binds preflight and payload to the accepted source candidate and its
individual snapshot, records exact_candidate=true, records -B -P, and has exit 0.
The preflight output identifies actual 3.11.15 or 3.14.6. The selected unit-test
outputs report the indexed counts and OK, summing to 483 per interpreter and
966 total; the summary orders the floor slot first. The four new suites report
9, 18, 12 and 3 tests respectively. These are retained source results, not fresh
metadata test results supplied by this reviewer.

The retained failed floor host-suite receipt and both unchanged-baseline Git-path
diagnostics also match their indexed hashes. The original full suite records
37 tests and one failure comparing Windows backslashes with forward slashes for
the same absolute Git path. The baseline reproduces that exact assertion failure;
the corrected-spelling baseline diagnostic passes. The final selected floor
receipt is separate. The metadata accurately preserves the failed attempt.

The actual candidate-review.json and analysis-details.json artifacts, not their
path-reporting stdout, are byte-identical across interpreter slots and reproduce
the two analyzer hashes above. The full comparison reports 2,999 old inventory
entries, 436 old payloads/order, 141 expanded rows, 646 blockers, 388 analyzed sites,
4,269 helper edges and 591 decoys preserved. It accounts for exactly 42 new IDs,
32 blockers, 19 analyzed sites, 60 helper edges and one decoy, with no new expanded
rows. These match the ADR's factual census summary and the supplied source reviews.
The registration captures are correctly development observations; only the final
52 selected receipts are treated here as exact-source-candidate acceptance.

## Authority, STATUS and residual limits

ADR-0506 expressly conditions effect on its separately authorized exact decision
commit. Source tests and review refs do not activate the seal. It incorporates only
the bound source population and the two metadata paths, closes the twelve current
exceptions with their accepted versions, and grants no standing mutation right.
It preserves engine ownership of admission, legal application, continuous timing,
fallback and delivery, and describes the fixed baseline without strength claims.

The Tier A metadata procedure matches ADR-0503: independent light review, exact
incorporation, then unchanged status --check and all twelve status tests on both
actual supported interpreters in fresh exact-candidate snapshots. It replaces no
Tier C review or source gate. Exact controller commit authorization remains later.

STATUS's current-decision paragraphs match ADR-0506; its active-next and blocker
text match that decision's front-door fields. Latest process/latest ADR point to
0506, the decision count advances to 506, and the existing research, runtime and
revoked-authority references remain intact. The displayed new ADR-header digest
and complete generated freshness will be exercised by the pending metadata gates;
this review does not claim to have run the generator.

The next boundary is selection of a separately bounded baseline demonstration.
No demonstration population, new poker invocation, operating/research run, arbitrary
policy or neural loader, training, self-play, league, tuning, cleanup or ref retirement
is opened. Older consumed demonstrations and owners remain closed. The continuing
ADR-0307 and operating/research prerequisites are expressly retained.

Inspection commands and independent hash/count audits completed successfully.
A preliminary interpreter-path probe used py311/python.exe and found no file;
inspection continued with the documented py311/Scripts/python.exe. An overbroad
filename listing encountered access-denied disposable directories; all referenced
artifacts were then read directly. Neither produced acceptance evidence or an
unresolved review gap. No test, analyzer, demonstration, production edit, cleanup,
commit, push, remote publication or child-agent launch was performed.
