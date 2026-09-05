# Independent design review B: v0a-blueprint-artifact-design/r002

- Reviewer: Codex, independent cold Review B
- Candidate: `a552f6f34efe10155a702fd09a03bcc70802a369`
- Base: `7ee314b443e10896e87a2e194f24eddda31ff77d`
- Tree: `14b71ec9dc6bc6db20393008dde9f25db13a95c5`
- Manifest SHA-256:
  `67abe320f73b8edfab60a93511f31eac62d0fac0279cdef712acda91fcf7aced`

## Pre-coverage independent invariant and related-path inventory

Recorded before opening the deferred `coverage.md`. This inventory derives only
from the brief, the permitted r001 Required corrections, the bounded base
workflow/ADR contracts, and frozen r002 `design.md` plus
`source-opening-draft.md`.

### Initial invariants

1. **Closed bidirectional admission domain.** `decode_blueprint` must admit only
   exact bytes containing one complete strict-UTF-8 JSON value in the closed v1
   schema, and `encode_blueprint` must admit only the corresponding exact fixed
   source/record/value graph. Both directions must apply the same exact-type,
   integer and Unicode-scalar domains and must fail atomically with
   `BlueprintArtifactError`; every successful encode must be decodable.
2. **Numeric portability through every direction and identity path.** Every JSON
   integer token must be bounded before conversion, every decoded and source-side
   integer must satisfy the same `0 <= value < 10**640` outer domain plus its
   narrower field constraint, and accepted values must survive
   `decode -> source.digest -> encode -> decode` on supported CPython 3.11 and
   3.14 without dependence on mutable process-global decimal-conversion settings.
3. **Lossless policy reconstruction and independent identities.** Full decision
   keys and exact actions—not key hashes alone—must reconstruct the existing
   immutable source without changing its existing policy digest. Raw-artifact
   SHA-256 remains a distinct byte identity; formatting or entry order may alter
   the raw hash without altering policy identity. Canonical encoding is unique for
   a codec-admitted source/permutation and ends in exactly one LF.
4. **Schema completeness, privacy and semantic ownership.** The artifact carries
   every field required by `BlueprintDecisionKey` and `BettingActionRecord`,
   rejects duplicates/unknowns/missing fields/wrong exact types and malformed
   nullable relationships, preserves order except existing private-hand
   canonicalization, and excludes whole-deal/future-board/opponent-private/runtime
   or executable data. The codec performs representation validation while the
   sealed betting/key constructors retain their existing poker semantics.
5. **Real-consumer behavior stays sealed.** A loaded matching entry must select
   the independently declared non-passive action through `HandRuntime`; a miss
   retains passive fallback; an illegal matching action retains typed
   `INVALID_BLUEPRINT_ENTRY` with no delivery; and `ReplayHost` plus its
   independent reader must establish the declared complete-hand settlement.
   The codec must not add dispatch, clock, trace, replay, I/O or execution
   authority.
6. **No guessed operational/capacity gate.** V1 must not impose an ungrounded
   artifact-byte, entry-count or source-ID-length ceiling. The numeric bound is a
   documented cross-version conversion-compatibility rule, not a bankroll,
   runtime, memory or availability budget. Later operational quotas require their
   own named consumer and grounded decision.
7. **Bounded additive source and registration opening.** The only new paths are
   the inert package initializer, codec, two tests and two tiny independent
   fixtures. Only the six named registration/CI files may receive their narrowly
   described deltas; base drift, generator incompatibility, unexplained census
   movement, any capability grant, analyzer repair, parent re-export, legacy
   origin import, host/runtime back-import or change to the six sealed `v0a`
   modules must stop the round.
8. **Independent acceptance evidence.** Tests must use handwritten/canonical
   byte oracles and independently constructed keys/actions/settlement, not merely
   self-round-trip or historical/rehearsal output. They must cover the schema
   categories, partial-admission failure, source-side malformed graphs, numeric
   and surrogate boundaries, the former one-MiB non-ceiling, real source-boundary
   gates and both supported interpreter slots (floor first, including startup at
   `-X int_max_str_digits=640`). No absent feature execution is required at this
   design-only stage.

### Initial related-path inventory and discovery rationale

- **Frozen contract:**
  `docs/architecture/v0a-blueprint-artifact-r002/design.md`,
  `docs/architecture/v0a-blueprint-artifact-r002/source-opening-draft.md`.
- **Requirements/governance:** `CLAUDE.md`, `docs/workflow.md` Stage 0b/3/4 and
  Review checklist v1, `docs/briefs/v0a-blueprint-artifact-brief.md`, and the
  bounded source/runtime/registration dispositions in ADR-0485, ADR-0486,
  ADR-0487 and ADR-0489.
- **Key/action construction and digest seams:**
  `src/pontius/immutable_blueprint.py` and
  `src/pontius/no_limit_betting.py`; discovered from the proposed codec's only
  internal imports and the brief's existing key/action/policy-digest contract.
- **Real runtime/replay/reader seams:** `src/pontius/v0a/model.py`,
  `src/pontius/v0a/runtime.py`, `src/pontius/v0a/replay.py`,
  `src/pontius/v0a/trace.py`, and `src/pontius/v0a/__init__.py`; discovered from
  the named public consumers, typed outcome, replay and independent-reader
  requirements. Inspection is limited to the directly relevant public contracts,
  not a whole-runtime audit.
- **Existing neighboring behavioral controls:**
  `tests/test_immutable_blueprint.py` and the four directly registered `v0a`
  suites named by the base inventory/CI; discovered from the brief/design's
  explicit reuse requirement. Only the portions needed to validate the proposed
  seams and independent oracles are in scope.
- **Registration and direct-CI seams:**
  `tools/check_stabilization_boundaries.py`,
  `tools/generate_test_inventory.py`,
  `tests/test_inventory_and_profiles.py`, `tests/test-inventory.json`,
  `tests/test-profiles.toml`, and `.github/workflows/ci.yml`; discovered as the
  six exact exceptions. Inspection is limited to whether the proposed deltas are
  feasible and preserve the named boundaries; it excludes a general analyzer or
  test-orchestration audit.
- **Prospective additions:** `src/pontius/blueprint_artifact/__init__.py`,
  `src/pontius/blueprint_artifact/codec.py`,
  `tests/test_blueprint_artifact.py`,
  `tests/test_blueprint_artifact_boundary.py`, and exactly two fixture files
  under `tests/fixtures/blueprint_artifact/`; these do not exist at this design
  stage and are assessed as proposed boundaries only.

## Deferred coverage comparison

After recording the inventory above, I opened frozen `coverage.md` at blob
SHA-256 `d83bfd196dc8fe9b632858a83abba77a7dc9d8ae9e3247ea1d1fed82de80b2e3`.
Its category is coextensive with the independent inventory for this FIX round:
bidirectional portability and policy-identity closure, the explicit scalar
domain, and removal of the ungrounded byte gate. Its discovery method reaches
raw token conversion, exact source graphs, key/history/action construction,
canonical key serialization, policy digest, export/reimport and both public
codec operations. That matches the independent paths; subsequent inspection
also found the transitive card canonicalization in `holdem_cards.py`/`river.py`,
which the claim covers through the existing key constructor rather than by
opening a separate codec dependency.

The future controls cover the numeric boundary and immediately outside it on
both interpreter slots, minimum-setting startup, digest and round-trip closure,
both surrogate directions plus a valid astral case, removal of the former byte
gate, the original schema categories, real consumers and the independent
reader. Limits exclude whole-hand reachability, policy quality, hostile module
mutation and arbitrary resource safety. The three stated falsifiers directly
invalidate the three correction claims. I found no missed member or unsound
discovery method within the authorized correction category.

## Required corrections

None.

All three binding r001 Review B corrections are closed:

1. The ungrounded `1,048,576`-byte compatibility gate is removed rather than
   replaced (`design.md:174-179`; `source-opening-draft.md:110-116`), and a valid
   above-former-limit round-trip control is required (`design.md:237-239`).
2. Numeric portability is closed symmetrically across raw-token conversion,
   exact-source admission, key serialization, existing policy digest and
   export/reimport (`design.md:74-89`, `:227-234`). The maximum accepted value,
   `10**640 - 1`, has 640 decimal digits and remains within the documented
   minimum nonzero CPython conversion limit; `10**640` has 641 digits and is
   refused before conversion. Existing key and source digest paths do perform
   decimal JSON serialization (`immutable_blueprint.py:222-251`, `:323-346`).
3. The exporter is explicitly narrowed to codec-admitted Unicode-scalar source
   IDs and refuses surrogates before hashing or emission (`design.md:42-50`,
   `:91-95`). Decode applies the same post-escape domain, valid escaped pairs
   remain astral scalars, and successful encode is required to decode with the
   same digest (`design.md:170-172`, `:235-236`).

Because no required correction remains, the defect verdict is **CLEAN**.

## Advisory implementation choices

No additional advisory design change is needed. The implementation should keep
the already-selected narrow techniques visible in review: pre-conversion
`parse_int` length validation, duplicate detection from decoded object pairs,
pre-hash exact-graph/scalar validation, and one typed wrapper for ordinary
decode/schema/constructor failures. These are reminders of the accepted design,
not new gates and not permission to add a parser, serializer framework, process
launcher or global interpreter-setting change.

## Requirement-to-evidence assessment

1. **Lossless complete-key artifact — PASS.** `design.md:97-150` matches
   all 17 members in `BlueprintDecisionKey.canonical_bytes()` and its existing
   validators at `immutable_blueprint.py:27-247`; actions/history match
   `no_limit_betting.py:19-168`.
2. **Exact, atomic admission boundary — PASS.** `design.md:33-63`, `:65-95`
   and `:181-185` fix exact inputs/graphs, closed traversal, a common typed
   refusal and an all-or-nothing return.
3. **Deterministic encoding and identities — PASS.** `design.md:152-179`
   separates raw SHA-256 from the unchanged policy digest, sorts full-key
   encodings, fixes JSON options and final LF, and requires digest closure.
4. **Required r001 corrections — PASS.** `design.md:47-50`, `:74-95`,
   `:170-179`, `:227-239`; `source-opening-draft.md:110-116`; and official
   CPython 3.11/3.14 integer and JSON documentation support the closure.
5. **Real existing consumers — PASS.** `design.md:195-213` uses independent
   expectations through `HandRuntime`, no helper double, and complete
   `ReplayHost`/reader behavior. Existing seams confirm exact source admission
   and typed illegal-hit/no-delivery handling (`runtime.py:102-109`, `:127-179`,
   `:882-942`) and independent replay (`replay.py:729-825`).
6. **Schema-derived and independent controls — PASS.** `design.md:187-252`
   covers field/type/shape failures, duplicates, bad-later-entry atomicity,
   canonical bytes, malformed source graphs, scalar boundaries, real source
   gates and both supported slots.
7. **Bounded source opening — PASS.** `source-opening-draft.md:14-41` opens
   only two source files, two test files and two fixtures after separate
   adoption; implementation and source seal remain separate.
8. **Six exact registration exceptions — PASS.**
   `source-opening-draft.md:43-87` binds all six base blobs exactly and
   restricts their deltas. Base inspection confirms every listed object ID and
   that the public boundary/CI/inventory seams can host the narrow additions.
9. **Zero-grant and parked-analyzer boundary — PASS.**
   `source-opening-draft.md:89-122` preserves ADR-0486's registration-only
   rationale, grants no capability and makes generator incompatibility a stop.
10. **Stage 0b design quality — PASS.** The design states goals/observations,
    mechanisms and invariants, error-prone points, rejected alternatives,
    remaining ruling, coverage, project ties, blast radius and explicit
    exclusions (`design.md:13-31`, `:187-290`).

## Identity and static verification

The local freeze-snapshot repository was used for all candidate and base source
inspection; no mutable checkout content was used as candidate evidence.

- Ref `refs/heads/review/v0a-blueprint-artifact-design/r002` resolves to
  `a552f6f34efe10155a702fd09a03bcc70802a369`.
- Its sole parent is `7ee314b443e10896e87a2e194f24eddda31ff77d` and its tree is
  `14b71ec9dc6bc6db20393008dde9f25db13a95c5`.
- The base-to-candidate delta adds exactly the three frozen paths. Recursive
  tree inspection of their directory finds exactly those same three blobs.
- Native byte-stream SHA-256 recomputation over `git cat-file blob` output:
  - `346aa8c36c59d970bd1ae71ecdf86d64ccbe78c996f955e526f581b061c96808`
    — `source-opening-draft.md`
  - `5403709d2ee8cc6b0cbacd7775ca7cf71f07f1eecba5e5902286a2387de1b96d`
    — `design.md`
  - `d83bfd196dc8fe9b632858a83abba77a7dc9d8ae9e3247ea1d1fed82de80b2e3`
    — `coverage.md`
- The supplied rows are in whole-row digest-first byte order, use two spaces
  before POSIX paths and end in a final LF. Hashing those raw manifest bytes
  reproduces
  `67abe320f73b8edfab60a93511f31eac62d0fac0279cdef712acda91fcf7aced`.
- `git diff --check` reports no whitespace error. Raw blob inspection reports
  strict UTF-8, no BOM, no CR bytes, a final LF, no line over 100 characters and
  no trailing whitespace for all three frozen documents.
- The six proposed registration exceptions' base Git object IDs independently
  match `source-opening-draft.md:75-84` exactly.
- The CPython 3.11 and 3.14 Built-in Types documentation states that 640 is the
  lowest configurable nonzero decimal integer/string conversion limit and that
  the restriction covers both base-10 `int(string)` and `str(integer)`. The JSON
  documentation confirms `parse_int` receives each integer token as text and
  that the stock codec otherwise accepts/outputs unpaired surrogates, supporting
  the explicit hook and scalar checks. Sources:
  <https://docs.python.org/3.11/library/stdtypes.html#integer-string-conversion-length-limitation>,
  <https://docs.python.org/3.14/library/stdtypes.html#integer-string-conversion-length-limitation>,
  <https://docs.python.org/3.11/library/json.html>, and
  <https://docs.python.org/3.14/library/json.html>.

## Independence and limits

This was a cold, design-only Review B. I read only the prior r001 Review B
`Required corrections` section; I did not read either current Review A, any
coordination/disposition/ledger file, controller thread, implementation
narrative or the rest of the prior review. The pre-coverage inventory above was
written before `coverage.md` was opened.

I inspected only raw Git blobs from the local freeze snapshot plus the permitted
prior-review section and read-only official CPython documentation. I did not
import project payloads, execute tests, prototypes, generators, owners or
runtime code, install dependencies, change Git/source state, publish to the
network or use subagents. The existing source inspection was bounded to the
key/action/digest, card-construction, runtime/replay/reader, registration and
direct-CI interfaces needed to judge this proposal. This is not a whole-runtime,
whole-core or parked-analyzer audit. No feature implementation exists, so absent
executed feature tests are recorded as the design-stage limit required by the
handoff, not as a defect.

## Verdict

- **Specification: PASS**
- **Engineering quality: PASS**
- **Findings: Critical 0 / Important 0 / Minor 0**
- **Defect verdict: CLEAN**
- **Design verdict: SOUND** — the two-function byte adapter, closed fixed schema,
  unchanged immutable source/consumer interfaces and separately bounded
  registration amendment fit the brief. The corrections are local contract
  closures and do not strain the shape or require reopening the sealed runtime.
