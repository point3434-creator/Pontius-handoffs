# Cold review 04 - Codex

Defect verdict: NOT CLEAN
Design verdict: STRAINED
Round: v0a-eval-panel-completion/r001, NEW-SURFACE, Tier C
Candidate: 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13
Manifest SHA-256: f58d6ed822787f0766c23ee63540ddc999784ad11d03dc103a1cbf80f68c0194
Parent: beb84be566aa28029284bd35c526d33cd27af369
Tree: 09d78e4ede52a9093fc7941270d497a7362706dc
Ref: refs/heads/review/v0a-eval-panel-completion/r001

## Independence, input order and verification method

I received the assignment and general runtime/tool guidance. No unsolicited prior review, verdict,
disposition, readiness file, implementation conversation or memory content was supplied. The
explicitly allowed governing inputs contain historical references and quotations; I did not follow
their references into other packets or histories. The coordinator later requested a progress
update and supplied no substantive review information.

I read handoff.md first, then the initial candidate, manifest, brief, supporting-file list and
named inputs. The initial bulk display was truncated; targeted reads completed the governing text.
I inspected raw frozen Git blobs, never worktree source. Before opening coverage.md,
operating-boundary.md or checks/, I exclusively wrote inventory-04-codex.md and hashed it:

3cf975037f8ef800e1c529ca1dab137cfc8b7ce79383853ebf0ee4f79189d94b

The inventory was rehashed unchanged at final verification. Only that inventory and this report
were written in the assigned exclusive directory. No source, packet, Git ref, ledger or index was
modified. No forbidden reviews, sibling scratch, progress/readiness files or other packets were
opened.

The first handoff read used PowerShell. All Python utilities used the handoff's absolute CPython
3.14 executable, with read-only Git and data/AST parsing. Sandbox launch access required
escalation; no global safe.directory change was made. No project import, test, solver, export or
host execution was performed. Findings below are static counterexamples proved by tracing the
frozen branches; they are not new executed reproductions.

## Important finding F1 - Retained protocol admission manufactures missing fields

Primary frozen location: src/pontius/eval_agreement.py:145-155.
Related consumer: src/pontius/eval_agreement.py:251-266 and 295-303.
Authoritative producer validation: tools/v0a_table_host.py:796-815.
Default source: src/pontius/v0a/model.py:360-374.
Related v2 authority: src/pontius/decision_provider/codec.py:44-137.

Governing requirement: brief mechanism 7 excludes malformed frames before outcome/agreement
eligibility; accepted design section 5 requires complete retained envelopes and failure before
agreement. The Tier C invariant explicitly disallows successful agreement manufactured from
missingness or defaults. The unchanged host requires the exact preparation_use fields at lines
801-805.

Reachable input scenario: take an otherwise valid completed blueprint-v1 CHECK-hit Session report,
remove only credited_seconds from one decision's preparation_use object in child_stdout_base64,
and retain the re-encoded complete NDJSON stream. Keep action, reason, settlement, timing,
identities and applied history unchanged. The classifier is explicitly the retained-envelope
admission boundary, and its tests already exercise this kind of post-capture field mutation.

Static falsifying observation: frames_for checks top-level frame fields but not the
preparation_use member set. At lines 146-150 it copies the object, converts artifact_sha256s to a
tuple, and passes the incomplete object to PreparationUseRecord. That dataclass supplies
credited_seconds=0. Its validation passes, DecisionRecord construction passes, and the original
missing member is never checked later. Replay and teacher/reason checks are unchanged, so classify
reaches classification='hit', chip_eligible=True and agreement_eligible=True at lines 260 and
294-303. The required outcome is exclusion with a malformed-capture cause. The same argument
applies when producer_status is omitted: the dataclass supplies producer_absent.

This is anchored to a real producer shape. The pinned checks/classifier-red-real-host.txt contains
a completed actual Session/hand and 20 complete frames, with a CHECK river record whose
preparation_use contains artifact_sha256s=[], credited_seconds=0 and
producer_status='producer_absent'. I parsed that diagnostic as data only. Its old classifier
failure is implementation history evidence, not a fresh reproduction or the verdict's authority.
The unchanged frozen host independently requires all three members; it would reject either
omission.

Related affected paths discovered from the same schema boundary:

- artifact_sha256s='' is converted to the empty tuple by line 147 and passes, even though the
actual v1 host requires a list. Thus the problem includes type normalization as well as omitted
defaults.
- The v2 branch at lines 152-155 only checks delivery status and equality of
selected/applied/delivered actions after the common timing checks. It never calls the existing
validate_decision schema validator. Removing provider_outcome or preparation_use from an otherwise
successful v2 baseline decision is therefore invisible to frames_for. The baseline exit at lines
264-266 returns chip_eligible=True without later schema validation. The actual v2 host calls
provider_codec.validate_decision at tools/v0a_table_host.py:761-769, which rejects such a record.
- terminal.interrupted_response_count=False satisfies the comparison to zero at line 163, while
the actual host requires an exact integer at tools/v0a_table_host.py:890. ready.evidentiary is
also not checked against False, unlike host ready at lines 729-737. These are further members of
the same incomplete retained-schema admission category, not independent findings.

Required correction: validate the original parsed v1/v2 records and every relevant nested object's
exact required fields/types before conversions or dataclass defaults can fill them. Preserve the
intended distinction: a well-formed reason-only relabel remains an agreement disagreement with
eligible chips; a malformed record must be excluded before chips or hits are counted. V2 baseline
support must enforce its actual existing provider-record contract while allowing completed prefix
divergence to retain chips.

Required verification: demonstrate the omitted credited_seconds/producer_status and wrong
artifact_sha256s-type cases fail against the frozen candidate through classify, then pass after
correction as exclusions. Cover missing required v2 provider/preparation members and malformed
terminal integer/ready fields. Keep an unmodified real blueprint-v1 CHECK-hit capture passing,
keep the real reason-only mutation disagreeing, and exercise an actual valid baseline-rules-v1/v2
completed prefix-diverged capture as chip-eligible. Expected malformed outcomes must come from the
unchanged host/protocol schemas, not new classifier bookkeeping.

Current coverage gap: tests/test_eval_agreement.py:250-262 checks a missing entire preparation_use
object, not missing/defaultable nested members. The baseline fixtures at lines 23-37 and tests at
225-231 and 335-339 still produce protocol v1 even when the caller requests baseline-rules-v1.
Thus they cannot exercise the actual v2 admission branch. The real host test at
tests/test_eval_completion_tool.py:100-173 uses blueprint-v1 throughout. The declared coverage
honestly labels baseline fixtures; it does not close this malformed-v2 path.

## Design assessment

STRAINED is localized to retained protocol validation. The broader phase/teacher/export/witness
architecture fits the accepted task. The classifier maintains a second, partly handwritten
interpretation of existing host schemas: top-level key checks, semantic dataclass reconstruction
for v1, and only a delivery subset for v2. F1 demonstrates the drift this shape invites. It
conflates a convenient in-memory constructor with validation of the exact received bytes.

Advisory technique: keep framing, raw-schema admission, outcome replay and agreement comparison as
explicit stages. Reuse the existing public v2 validate_decision boundary; for v1, add a narrow
exact parsed-schema check aligned with the frozen host before constructing typed values. Avoid
changing the host or broadening into a new protocol framework. This costs a bounded
classifier/test correction and adds no runtime owner or phase. No whole-bridge rewrite is
recommended, and this design advice creates no independent gate beyond F1's required behavioral
correction.

## Reconciliation with deferred coverage and receipts

The initial inventory covered all brief mechanisms, including producer/result identity, every
phase transition, provider versus host claims, seed/deal consumers, outcome/agreement separation
and execution/status ownership. Deferred coverage largely matches those boundaries. Its claim 11
of strict retained frames is too broad in view of F1; claim 13's baseline fixtures do not
establish actual v2 behavior. Claims about complete host capture apply to returned attempts; I did
not execute a hard kill during an active Session to establish partial-capture retention.

The packet's focused evidence is consistent and properly limited: five registered suites, 78
unittest cases, zero skips, pytest exit zero, Python 3.14.6, candidate-matching journal
source_commit and source_verified=true. The copied focused-result bytes independently match the
journal output_sha256. ResourceWarning and pytest unraisable warnings were configured as errors.
These are implementer checks, not this reviewer's execution or broad/adoption clearance.

The provenance note explicitly lacks raw initial teacher/export availability RED and accounting
RED receipts. I did not invent those receipts or read tool history to recover them. The retained
RED diagnostics identify dirty implementation observations, not a frozen rejected candidate. This
provenance limit is separate from the concrete product defect above.

I independently verified the exact ref, sole parent, tree and eight-path delta. Raw cat-file
SHA-256 rows sorted as whole digest/path byte strings with LF endings reproduce the pinned
manifest; a final check used --no-replace-objects. All pinned D:/Pontius dependency blobs match.
All named initial supporting copies, deferred coverage/boundary and listed checks match their
supplied hashes. External historical resource-document source repositories were not opened; the
allowed packet copies were checked instead.

Whole Slice A raw source counts independently reproduce 2008 production lines and 1781 test lines.
Production is below the 3000 hard ceiling, above the 1200 working figure by 808; tests exceed the
600 working figure by 1181. The clarification does not make this working-figure overage a new
approval blocker. Candidate delta is 1883 added and 5 removed lines across the eight authorized
paths. The nine Slice A production/test Python files satisfy LF-only, BOM-free, at most 100
columns and no trailing whitespace. Test registration adds precisely the three new suites.

## Verified boundaries and practical limits

Static tracing supports the explicit phase dispatch and immutable plan snapshot, measured
full-pool prerequisites, one-hero-at-a-time solver, canonical teacher serialization, actual codec
wire-size/key/action checks, complete provider/complement enumeration, finite first-witness
selection with intact private hands, and parent schedule/result reconciliation. Session.run
invokes prepare; inherited cwd/context feed Admission/Source; Session.run itself does not call the
CLI journal writer. Parent finish_run writes the result and status_generation appends its journal
row. Protected existing host/session/dealer/codec/kernel files are outside the exact changed-path
delta.

I did not independently execute numerical reference checks or public host/provider tests. The
reviewer verified source/receipt contracts, not full-population behavior or resource adequacy. No
retained full-H solve, nonzero-tie census, export, agreement, holdout, paired chip estimate,
calibration or strength result follows from this report. Exact source gates, controller adoption
and separately bound one-shot phase authorizations remain necessary. The unresolved Important
finding makes this candidate NOT CLEAN.
