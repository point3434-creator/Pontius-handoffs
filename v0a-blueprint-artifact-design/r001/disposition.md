# Design review disposition: v0a-blueprint-artifact-design/r001

Issued 2026-09-05. Coordinator disposition, not an independent review or adoption.

Candidate: `336b8660f2f0b33fbeaa40d02cfc97c041ae6e1a`.
Base: `7ee314b443e10896e87a2e194f24eddda31ff77d`.
Manifest SHA-256:
`404d81333837358c2c4d5d60e1702039a13c276dbe14979684033aa23b82024a`.

## Outcome

NOT READY FOR ADOPTION. The two fresh-context, design-unexposed reviewers
independently reviewed the same local frozen Git objects. A returned CLEAN;
B returned three Important required corrections. Both judged the shape SOUND.
One clean report does not override another report's unresolved requirements.

- Review A: CLEAN; Spec PASS; Quality PASS; Critical 0 / Important 0 / Minor 0.
  Report: `review-a.md`, SHA-256
  `3a477ee2e7e8c3003cba114639893a722432aea927a86edd1ae913d6fc851957`.
- Review B: NOT CLEAN; Spec FAIL; Quality FAIL;
  Critical 0 / Important 3 / Minor 0. Report: `review-b.md`, SHA-256
  `44a4523a86bb647f1aed7e48b9366bd93e63ec219ae3cb3049926e6760165706`.

Each issuer wrote its own attributed verdict line in local `progress.md`.
The reports and r001 candidate are retained unchanged. No passing source-opening
verdict, runtime execution, implementation result or publication is inferred.

## Per-finding disposition

### B-I1: format capacity and provenance

Accepted as a required capacity/provenance decision before adoption, not as an
executed codec defect or a claim that every format ceiling is intrinsically wrong.
The brief supplies no maximum required policy population, and r001 supplies no
derivation for the 1,048,576-byte raw/canonical ceiling. The workflow's measured-
budget rule is broad; ADR-0485's cited no-guessed-size language specifically
describes that preregistration. This disposition does not silently extend the ADR
sentence to every future format or claim that operational benchmarking is needed
to choose a format. It does retain the unresolved capacity issue and the need for
an explicit, grounded choice if a ceiling is kept.

Recommendation for a separately authorized correction round: remove this optional
byte ceiling and its acceptance claims. Keep the existing explicit exclusions of
hard memory/time guarantees and hostile resource exhaustion. Do not start policy-
capacity research, invent a different byte number, or weaken typed value admission
merely to settle this small design. A later operational capacity limit is a
separate decision. If the controller retains a v1 ceiling instead, bind its
required population/provenance and raw/canonical boundary outcomes as B requires.

### B-I2: integer portability

Accepted. The schema currently promises unbounded positive/nonnegative chip
integers subject only to byte size. CPython's documented decimal conversion limit
can reject those values during JSON parsing or the unchanged policy digest path.
The source inspection and primary documentation support this finding; no project
payload or behavioral probe was run during this design-only review.

Recommendation: specify the same explicit numeric domain for both directions,
validate raw integer tokens before decimal conversion, and validate exact source
integers before hashing or formatting. A 640-decimal-digit maximum for otherwise
unbounded fields is a possible compatibility-derived bound: CPython documents 640
as its minimum configurable nonzero conversion threshold. Existing narrower seat,
card, sign and enum constraints still apply. This is a proposed design choice,
not an adopted rule. Do not change process-global interpreter settings or the
sealed policy digest implementation. The correction must cover accepted-boundary
and next-value refusals, independent JSON inputs, and successful digest/export/
reimport on both supported slots, including the minimum conversion setting.

Basis: Python's [integer conversion limit documentation][integer-limits] and
[JSON decoder documentation][json-docs].

### B-I3: symmetric Unicode admission

Accepted. At the base, `ImmutableBlueprintActionSource.__post_init__` requires a
nonblank string but does not exclude surrogate code points; its canonical output
uses ASCII JSON escaping. The proposed decoder excludes unpaired surrogates,
while the encoder's corresponding scalar domain is not stated precisely enough.
Python documents that its JSON defaults can preserve such code points. Therefore
the current design permits conflicting encoder interpretations.

Recommendation: explicitly require Unicode scalar-value strings in the encoder
as well as the decoder, with typed refusal before output, and scope the round-trip
claim to codec-admitted sources. Keep valid astral characters/escaped surrogate
pairs as positive controls and lone high/low surrogates as both-direction negative
controls. Every successful export must decode with the same policy digest. Do not
change the sealed source class or relax decoder admission.

Basis: base `src/pontius/immutable_blueprint.py:312` and the
[JSON character-encoding documentation][json-docs].

## Shape, next scope and authority

These are first-contact design findings, not residuals from a failed correction.
No redesign trigger fires. Preserve the additive byte codec, closed schema,
unchanged real runtime/replay consumers, independent behavioral oracles, exact
six-file registration exception, line budgets and parked lanes.

The bounded design commission returns to the controller here. Recommend one
documentation-only FIX round r002 addressing B-I1 through B-I3 and their matching
acceptance text, with a new frozen identity and the normal independent reviews.
Do not revise r001 in place. No r002, source opening, feature/test code, runtime
run, ceremonial decision commit or implementation round is authorized by this
disposition. The future implementation budget has not been consumed or expanded.

## Publication and preserved state

The attempted upload was refused before process execution. See the unchanged
`publication-status.md`. Explicit permission remains pending to upload this
internal design/review packet to `point3434-creator/Pontius` (only its named review
branch) and `point3434-creator/Pontius-handoffs` (coordination packet/navigation).
There was no alternate transport, retry or handoff-repository publication.

Primary master remains `7ee314b443e10896e87a2e194f24eddda31ff77d`; the primary
tracked worktree/index is clean. The candidate contains exactly the two approved
new documentation blobs, and their hashes match the blob-derived manifest.
All source, tests, registration files, CI, sealed records and retained results
remain untouched by this task. Review is complete locally; the remote packet
publication gate and all adoption/source-opening gates remain unsatisfied.

This issued disposition is append-only. Later correction, authorization or
publication is a new record, never a rewrite of this outcome.

[integer-limits]: https://docs.python.org/3.11/library/stdtypes.html
[json-docs]: https://docs.python.org/3.14/library/json.html
