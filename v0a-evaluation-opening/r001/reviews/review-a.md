# Independent Tier C review A — paired evaluation source opening r001

Issuer: Codex /root/evaluation_review_a. Date: 2026-09-07.
Round: NEW-SURFACE. Read-only design/source-opening review; no implementation review claim.
Candidate: 96aad82a482a0f37b13490df1bf03c1c74a860ca.
Manifest SHA-256: 6f388fbcc7c7bff9d99ba69fcac5287ad9e30e72d20bc1d1e02fe76ee8a06129.
Base: e043f81ecec3ac16128720b42c3312bb41a4ed67.
Tree: 17140a92f66c1b10bd11f266b093a7c3076f7711.

Specification: NOT CLEAN. Engineering quality: NOT CLEAN. Defect verdict: NOT CLEAN.
C/I/M required findings: 0/2/0. Confidence: high for A-I1; medium-high for A-I2.
Design verdict: STRAINED (advisory design assessment, separately stated below).

## Required findings

### A-I1 — The exact summary schema cannot preserve action failure causes separately

Location: source-contract.md:217-240; design.md:131-132; accepted
 tools/v0a_table_host.py:727-734, 921-929; tools/v0a_table_session.py:337-367.

Known from source: the host validates an event_result failure record and then raises
HostRefusal('child_failed'). The session retains that host cause in both the hand and
session failure lists. The original action-level FailureRecord.code is available in
retained child_stdout_base64, not in those outer lists. Examples in the accepted model
include delivery_rejected, delivery_ambiguous, clock_reversed and trace_write_failed.

Concrete scenario: a schema/identity-valid failed event carries delivery_rejected,
with no work-cutoff/deadline flags. Host and session report child_failed. The proposed
observer parses the valid prefix but its exact trial-summary field set provides only
failure_reason, hand_failure_codes, session_failure_codes and capture_deficiencies.
There is no action failure field. Emitting only child_failed loses the requested
failure distinction; putting delivery_rejected in hand/session lists misstates its
scope; calling a valid event failure a capture deficiency misstates the observation.
The same issue applies when decision and failure carry the same action cause.

Violated requirement: design.md explicitly requires separate trial status,
hand/session causes, action failures and transport/capture deficiencies. The exact
output schema must be able to represent that behavior. Retained raw bytes are useful
opposing evidence, but do not make the promised clear summary express the distinction.

Required correction: freeze a separate versioned action-failure observation field,
its exact schema, identity/deduplication rules and incomplete-prefix standing. Preserve
unknown/missing coverage, and distinguish raw observed failures from host acceptance.
Alternatively obtain an explicit narrowed reporting requirement and align every
normative document; silently dropping the requirement during implementation is invalid.

Required verification: finite independent report/frame controls with a non-timing
failure such as delivery_rejected show child_failed retained at hand/session scope
and the underlying action cause separately. Cover decision/failure duplication,
missing/invalid failure rows and unverified prefixes; no paired score follows. The
check must fail when the observer drops, scope-folds or double-counts the cause.

### A-I2 — The completion record's own failed or late publication lacks a safe state

Location: source-contract.md:188-195; design.md:103-106; PROJECT.md retained
canonical-publication rule (data and completion-seal phases).

Known specification: result JSON is create-new, flushed, reread and compared under
the deadline. Then completion.json is create-new with status=completed,
deadline_met=true and a result hash/size. The stated consumer predicate requires
both files, their bytes/hash binding and an all-complete result. The completion
record's own flush/readback/post-publication deadline outcome is not specified.
The broader prose forbids late success but does not resolve this terminal state.

Concrete scenario (prospective failure analysis, not executed): all trials and the
result write/readback finish before D. The completion record is serialized with
completed_elapsed_ns < D and deadline_met=true. Its write or close blocks until
D+epsilon (or all bytes reach disk but flush/close raises). A complete, parseable
completion.json remains beside the correctly hashed all-complete result. The stated
two-file consumer predicate accepts them, even if the runner subsequently returns
failure. Create-new/no-rewrite prevents repairing that marker in place. CLI failure
alone does not protect a later consumer.

Violated requirement: complete standing must cover successful publication under the
shared deadline, and a partial/late publication must remain incomplete. PROJECT also
requires the completion-seal phase, not only data, to be checked. The acknowledgement
that OS calls may block limits wall-time promises; it does not grant late success.

Required correction: specify the completion phase and the consumer acceptance state
through write, flush/close, readback, source/deadline checks and ambiguous/late failure.
A complete-looking marker left by an unsuccessful seal must not be consumable. Define
how an incomplete/failed publication guard or equivalent retained state enforces this;
do not simply add another unchecked success marker or rely on the process exit code.

Required verification: deterministic seam controls through real files delay the
completion write/close beyond D and inject failure after marker bytes are present.
The public consumer predicate must reject those roots, with no overwrite or retry;
a normal fully checked publication passes. Include interrupted/partial completion,
and distinguish precomputed timestamp assertions from observed completed publication.

## Independent identity and scope evidence

Reproduced by absolute native Git, --no-replace-objects/--no-optional-locks,
read-only rev-parse/diff-tree --no-renames/cat-file. Raw stdout bytes were hashed with
.NET SHA-256 without checkout newline conversion. Whole digest-first rows reproduce
the manifest above, equal to manifest.sha256's own raw hash. Candidate ref, parent
and tree match. The diff has exactly the six declared documentation paths:

- design.md: 1a0cf5fcddf3f33c392b19849c2af39c8c74c871f5fcfd04006a32e2d6dce8e4
- implementation plan: 2c2c064d464559b5ccc53cea3d073d5a8ad94bb0d32eeb3fe69f13a952575ee8
- STATUS.md: 4254976215f5c4f22c66ddc5077263038f84a53ad27dc9a22cd577fc8baa9bc5
- source-contract.md: 47ce8747e7cc0c0a46f22fe710a9d6da63856ebb05a4f42ee19314c6cee33cdd
- ADR-0508: 632b79d4124bf8426fd2466a7ba64f00ccbbff68489c387766cb270016c2a09a
- brief.md: 6b59aae1c94780eb7ca54c2e2cc0d5a780eb7858247af89cd8912299cd8905c8

All nine raw B blob IDs reproduced and remain identical at the candidate:

- tools/check_stabilization_boundaries.py: 9cc2ae8d8e82ccc77648ade4eb79ae9c34c88a9f
- tools/generate_test_inventory.py: 2ac1413b0f89fa848f1ee5df0814b58dcbfa15b8
- tests/test-inventory.json: c28445aa4b77a98cfd706672d955be4570b98a15
- tests/test-profiles.toml: 4469bf813b2e97116667c206784a7bc212f6eef5
- tests/test_inventory_and_profiles.py: e71a24322878361fb2feb44437d9210cff79c89e
- .github/workflows/ci.yml: 3d873a2f75ff1b155bf3533583eddf971eb7790a
- tools/v0a_seeded_deals.py: 2963004e38c6e66f76ae9ce3bd474063eee870fe
- tools/v0a_table_session.py: a5e058260fa56e29f06e38074d59dc55f420c5ee
- tools/v0a_table_host.py: 6ec8a162b053158203663c48e82314b10750f962

Prior final-disposition.json raw SHA-256 independently reproduced:
2f9d99f1aaca32252680a80b80e9b7a0ef1ad6d51b9482af0b42d849b1382c5f.
Initial sandbox Git read refused ownership; rerun used command-local safe.directory
for this exact authoring repo, with no configuration mutation. No other failed check.

## Requirement assessment and design judgment

Known from the reviewed proposal: d/l/r ordering fixes a maximum 96 pairs/192 trials;
button depends on d, not rotation; unchanged physical private pairs plus six controlled
seats cover all positions. Both arms share exact input, stacks reset to 200, and arm
order alternates prospectively. Arithmetic uses planned-pair denominators, null global
aggregate on any incomplete trial, and no profitability source gate. This shape avoids
policy-dependent dropout and survivor bias. Accepted generator/session source supports
the specified one-hand conversion, strategy versions and identifier lengths.

The explicit source closure, distinct host child manifest, inert raw helper loading,
public subprocess and host.Job reuse preserve useful existing boundaries. Source
permissions are exactly six pinned registration exceptions; old source remains sealed.
Overflow, descendants, unknown launch/exit and cleanup failure have finite named
controls. No test has been run in this review, so these are proposed obligations,
not verified executable properties.

Advisory design finding: STRAINED. The two-tool wrapper is a reasonable architecture,
but its hand-copied versioned observation/schema surface and publication state machine
are substantial within 1,200 production lines. A-I1 is concrete evidence that metric
requirements and exact field enumeration already drifted; A-I2 shows a terminal-state
gap. Before implementation, use one compact metric-to-source/output/unknown-state map
and one publication transition table in the existing contract. Cost is a small document
correction, not a new framework. Preserve the line ceiling; split or narrow the design
through the controller if faithful decoding/resource handling cannot fit. Duplicating
full poker validation or adding generic assurance infrastructure would be disproportionate.
This design judgment is advisory and is not itself a blocking behavioral finding.

Authority assessment: the proposal is explicitly inert until exact adoption; finite
correctness vectors after adoption do not authorize evaluation. Source seal and actual
population remain separate decisions. ADR-0505/0506/0507 and the retained prior hash
support the consumed-demo boundary. No authority-expansion defect found.

Largest unknown: executable reducer and native/publication behavior do not exist in
this candidate. Cheapest falsifying controls are the two finite scenarios above after
an adopted corrected opening. Kill criterion: inability to express honest failure and
publication standing inside the fixed scope/budget requires redesign/reauthorization.
Recommendation: preserve this candidate, make a bounded documentation correction,
freeze a new round, and obtain the required fresh reviews before adoption.

Inputs: full CLAUDE.md, workflow/checklist, PROJECT evidence rules, six frozen proposal
files, accepted source/schema contracts and ADR-0505/0506/0507. No author transcripts,
other reviewer reports, mapping-agent material or coordinator commentary were read.
No generator/poker imports, CLI help, tests, inventory/census, benchmark, cards, seed
creation, implementation edits, Git mutation or evaluation execution occurred.
