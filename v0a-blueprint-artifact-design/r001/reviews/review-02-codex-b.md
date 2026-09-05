# Independent cold design review B — v0a-blueprint-artifact-design/r001

Candidate: `336b8660f2f0b33fbeaa40d02cfc97c041ae6e1a`

Base: `7ee314b443e10896e87a2e194f24eddda31ff77d`

Tree: `f796e812640f56ec6e21ca88f5c63ff91982b976`

Manifest SHA-256: `404d81333837358c2c4d5d60e1702039a13c276dbe14979684033aa23b82024a`

Round: Tier C, NEW-SURFACE, design/source-opening only

## Verdict

**NOT CLEAN — Spec FAIL — Quality FAIL**

**Critical: 0 — Important: 3 — Minor: 0**

**Design verdict: SOUND.** The closed, byte-oriented JSON adapter into the existing
immutable policy, with the sealed runtime and independent replay reader left as real
consumers, is the right shape. The required corrections close underspecified scalar and
capacity domains; they do not require a different architecture, runtime changes, analyzer
repair, or a generic serialization framework.

## Required corrections

### Important 1 — The format ceiling is an ungrounded hard compatibility gate

- **Location:** `docs/architecture/v0a-blueprint-artifact-r001/design.md:146-151`;
  reinforced by `source-opening-draft.md:110-112`.
- **Confidence:** High.
- **Unmet contract:** The design freezes `1,048,576` bytes as the receive and canonical
  encoding ceiling but supplies no intended policy population, worst-case structural
  calculation, existing artifact observation, or other provenance showing that the value
  admits the portable policies this surface is meant to carry. Calling it a “format
  choice” does not change its observable gate: schema-valid content above it is refused.
  This conflicts with the base review checklist's measured-budget rule
  (`docs/workflow.md:496`) and the still-binding ADR-0485 prohibition on filling a size
  limit with a guessed value (`ADR-0485...md:476-477`).
- **Concrete consequence:** A legitimate policy can consist entirely of valid complete
  keys and actions yet become permanently non-portable solely because its canonical JSON
  is 1,048,577 bytes. Nothing in the brief establishes that roughly this capacity is
  sufficient, so implementation acceptance could seal an arbitrarily truncated product
  domain while all proposed small-fixture tests pass.
- **Required correction:** Either remove the v1 byte ceiling from this design, or ground
  the selected ceiling in an explicit required maximum policy population and an
  independent worst-case canonical-size calculation (or other controller-approved
  provenance). Keep the raw and canonical checks if a grounded ceiling remains.
- **Verification criterion:** Before source opening, a reviewer can reproduce the stated
  bound from the declared consumer capacity and the closed schema without using the codec
  under test, and boundary cases at exactly the limit and one byte over are assigned
  unambiguous expected outcomes for both decode and encode.

### Important 2 — The integer grammar is wider than the supported decoders can promise

- **Location:** `docs/architecture/v0a-blueprint-artifact-r001/design.md:63-68`,
  `:92-98`, `:105-118`, and `:146-156`.
- **Confidence:** High.
- **Unmet contract:** Every chip-valued wire field is specified as an otherwise unbounded
  positive or nonnegative JSON integer, up to the byte ceiling. On the supported CPython
  3.11/3.14 family, ordinary `json` integer decoding and integer-to-decimal encoding are
  subject to the interpreter's decimal-digit conversion limit, which is configurable
  independently of this schema. The proposed import surface provides no stated custom
  numeric grammar and the design supplies no exact digit/value ceiling. Consequently a
  value can satisfy every written wire rule and the byte ceiling but be refused before
  the existing validators, with behavior depending on interpreter configuration.
- **Concrete consequence:** Put a several-thousand-digit positive value in
  `starting_stacks` (and consistent chip fields) while keeping the artifact below the
  proposed one-MiB limit. It is valid under the written schema, but a default or
  more-restrictive interpreter conversion ceiling can raise during JSON parsing; an exact
  source containing the same permitted integer can likewise fail canonical export. The
  codec would report a schema-valid artifact as malformed and portability across the two
  supported slots or scrubbed environments would be accidental.
- **Required correction:** Close the numeric domain independently of ambient CPython
  configuration: specify an exact decimal-digit/value maximum for every integer family
  and enforce it symmetrically before conversion/encoding, or specify a bounded custom
  integer conversion whose accepted domain is the written schema. The bound must also be
  compatible with the existing policy-digest path, which serializes these integers.
- **Verification criterion:** Independent raw JSON cases at the chosen numeric boundary
  and immediately outside it have identical typed outcomes on CPython 3.11.15 and 3.14.6;
  encode applies the same boundary to exact source graphs; and an accepted value survives
  `decode -> source.digest -> encode -> decode` without reliance on process-global digit
  settings.

### Important 3 — The exporter domain is not closed over the decoder's Unicode domain

- **Location:** `docs/architecture/v0a-blueprint-artifact-r001/design.md:42-48`,
  `:63-74`, and `:127-149`.
- **Confidence:** High.
- **Unmet contract:** Decode expressly refuses strings containing unpaired surrogates,
  while encode is described as accepting an exact source and permitted exact scalar
  graph, and export/import is said to preserve its key/action values and policy digest.
  The existing `ImmutableBlueprintActionSource` validator accepts a nonblank exact `str`
  source ID containing an unpaired surrogate. ASCII JSON escaping can serialize that
  value as `\ud800`, producing bytes the proposed decoder must reject. The design never
  states the corresponding encode-side scalar-value refusal or narrows “admitted source”
  to the codec's Unicode-scalar domain.
- **Concrete consequence:** An exact existing source with `source_id` containing a
  nonblank unpaired surrogate can either (a) export successfully to an artifact that the
  same public codec refuses, violating codec closure, or (b) be refused by encode despite
  the current public-domain wording. Different implementers can choose opposite behavior
  and still point to the document.
- **Required correction:** Define the encoder's string domain explicitly and symmetrically.
  The narrow correction is to require Unicode scalar-value strings for `source_id`, raise
  `BlueprintArtifactError` before emission for an unpaired surrogate, and qualify the
  round-trip claim as applying to codec-admitted sources. Do not relax the decoder merely
  to preserve a value the wire format intends to exclude.
- **Verification criterion:** Encode and decode both refuse lone high and low surrogates
  with the common typed error; a valid escaped surrogate pair/astral character is accepted
  and preserved; and every successful `encode_blueprint` result is accepted by
  `decode_blueprint` with the same policy digest.

## Advisory implementation techniques (non-binding)

- Keep one explicit field schema/validator table for both directions so numeric and
  Unicode admission cannot drift. This is an implementation technique, not permission to
  add reflection or a generalized schema framework.
- Include independent positive controls for an astral `source_id`, harmless formatting
  variation, and raw-vs-policy identity divergence. They make the two identities and the
  paired-surrogate boundary visible without promoting raw hashing into the codec API.
- In the boundary checker, encode the new origin set as the two exact paths, separately
  assert the initializer's inertness, and preserve the existing legacy-edge and SCC checks.
  This is a concise way to realize the already-required registration contract, not an
  additional required file or permission.

## Requirement-to-evidence summary

| Requirement / risk | Fresh evidence | Result |
| --- | --- | --- |
| Frozen candidate and raw-blob identity | Ref resolution, commit parent/tree, `diff-tree`, exact subtree population, raw `cat-file blob` SHA-256, digest-first whole-row manifest recomputation | PASS |
| Complete key/action field coverage | Compared the 17-member schema and eight-field history atom with `BlueprintDecisionKey.canonical_bytes`, `BlueprintDecisionKey.__post_init__`, `BettingAction`, and `BettingActionRecord` at the base | PASS, subject to numeric-domain correction |
| Admission and rejection shape | Traced exact-source runtime admission and the codec's proposed exact bytes/record/scalar boundary | FAIL: numeric and Unicode domains are not closed |
| Policy and raw identities | Compared proposed full-key export and policy digest claims with the existing digest-only `ImmutableBlueprintActionSource.canonical_bytes` | PASS, subject to Unicode closure correction |
| Real consumer / no helper-double acceptance | Traced `HandRuntime`, `_admit_blueprint`, `_select_admitted_blueprint_action`, `ReplayHost.run`, and `verify_successful_trace`; the proposed expected policy and chip-depth oracle remain independent of decoded bytes | PASS as a design oracle |
| Declared raise/fold control arithmetic | Static transition check: raise-to-6 from seat 3, folds by 4/5/0/1/2, four-chip return, pot 5, payouts `(0,0,0,5,0,0)`, final stacks `(200,199,198,203,200,200)` | PASS as predeclared arithmetic, not runtime evidence |
| Six bounded registration exceptions | Compared the six pinned base blob IDs and inspected the current origin classification, legacy-edge/SCC checks, v0a import policy, test registration, profiles, and CI release-slot population | PASS as a bounded opening design |
| Format ceiling | Compared the proposed ceiling with the brief, workflow checklist, ADR-0485, and source-opening rationale | FAIL: no capacity or measurement provenance |
| Scope / authority boundary | Design and draft preserve sealed runtime/kernel/tests, zero grants, parked analyzer, no owner/run/source seal, and separate future adoption | PASS |

## Identity evidence and inspection limits

The immutable ref resolved to the supplied candidate. Its sole parent is the supplied
base, and its tree is the supplied tree. `git diff-tree --no-renames` showed exactly two
additions, the two paths named by the handoff; `git ls-tree` showed exactly those two files
under the frozen design directory. Raw blob hashes recomputed without checkout conversion:

```text
1038ac032e0385587b4cc963b158cff61f9441e2e4f074a9d79c49f115dad760  docs/architecture/v0a-blueprint-artifact-r001/source-opening-draft.md
a60015d4edd24c33fb78690998787b657d30272927d8fb99122e0efa03c530bf  docs/architecture/v0a-blueprint-artifact-r001/design.md
```

Digest-first whole-row sorting plus final LF recomputed manifest SHA-256
`404d81333837358c2c4d5d60e1702039a13c276dbe14979684033aa23b82024a`.
All six base Git blob IDs in the source-opening draft also resolve exactly.

This was an independent cold, read-only design review beginning from `handoff.md`,
`candidate.json`, and `manifest.sha256`. I inspected only the two frozen review blobs and
directly relevant base requirements/source: `CLAUDE.md`, `docs/workflow.md`, the artifact
brief, ADR-0485/0486/0487/0489, the immutable blueprint/card/betting contracts, the v0a
runtime/replay reader, and the six registration mechanisms. I did not read `review-a.md`,
coordination records, implementation transcripts, or mutable working versions of the
candidate. Per the design-only authorization, I imported no project payload, ran no tests,
owners, prototypes, generators, or applications, installed nothing, changed no Git/source
state, used no network, and made no publication attempt. Therefore this report assesses
contract soundness and proposed evidence design; it is not implementation-readiness or
runtime-pass evidence. Remote-publication logistics are deliberately outside the product
verdict.
