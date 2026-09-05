# Independent cold design review A — v0a-blueprint-artifact-design/r001

## Review identity and outcome

- Candidate: `336b8660f2f0b33fbeaa40d02cfc97c041ae6e1a`
- Base: `7ee314b443e10896e87a2e194f24eddda31ff77d`
- Tree: `f796e812640f56ec6e21ca88f5c63ff91982b976`
- Ref: `refs/heads/review/v0a-blueprint-artifact-design/r001`
- Manifest SHA-256: `404d81333837358c2c4d5d60e1702039a13c276dbe14979684033aa23b82024a`
- Scope: exactly the frozen blobs
  `docs/architecture/v0a-blueprint-artifact-r001/design.md` and
  `docs/architecture/v0a-blueprint-artifact-r001/source-opening-draft.md`
- Defect verdict: **CLEAN**
- Specification: **PASS**
- Engineering quality: **PASS**
- Severity counts: **Critical 0 / Important 0 / Minor 0**
- Design verdict: **SOUND**

No required correction survives verification.

## Findings

None.

## Design verdict

**SOUND.** The proposed shape is a closed, byte-level adapter around the existing
immutable policy value contract. It reconstructs the complete keys that the existing
digest-only policy representation cannot reconstruct, then hands the unchanged source
type to the already sealed runtime. It does not add executable artifact behavior,
duplicate state-specific legality, expose future/opponent-private data, or require a
runtime modification. The separate raw-artifact and policy identities are explicit,
and the real runtime plus independent replay reader remain the behavioral authorities.

The source-opening draft is similarly bounded: it names two source files, two test
files, two small fixtures, and six exact existing registration files; pins the six
existing files to their base blobs; limits each permitted delta; preserves the original
six-file `pontius.v0a` population and all legacy edges/hard gates; and treats the known
analyzer as registration-only with zero capability grants. That is the narrow exception
shape required by the brief and ADR-0486, not an analyzer repair or a general sealed-byte
waiver.

## Requirement-to-evidence assessment

| Requirement or material risk | Frozen-design evidence | Independent contract evidence | Result |
| --- | --- | --- | --- |
| Portable, non-executable data reconstructs an existing immutable source | `design.md:33-59`, `61-123` defines two byte operations, a closed JSON schema, exact values, and no I/O/dispatch/import target | `src/pontius/immutable_blueprint.py:27-251`, `254-263`, `305-375` exposes the complete key, entry, source, canonical policy identity, and lookup contract described by the design | PASS |
| Complete field coverage without future or opponent-private data | `design.md:82-123` accounts for the key version plus every one of the 16 stored key fields, all eight history positions, and the action pair; it explicitly excludes whole deals, future boards, and opponent hands | `BlueprintDecisionKey` fields and canonical payload at `src/pontius/immutable_blueprint.py:27-45`, `222-247` match the proposed 17-member wire key; card visibility is enforced by `src/pontius/holdem_cards.py:133-155` | PASS |
| Exact rejection and no partial admission | `design.md:42-48`, `63-80`, `100-118`, `146-157`, `186-194` requires exact public input/value types, duplicate/unknown/missing/type/version/value rejection, pre-return validation, typed refusal, and failure without partial policy/bytes | Existing constructors validate cards, key state, history/action values, duplicate semantic keys, and source identity at `src/pontius/no_limit_betting.py:19-168` and `src/pontius/immutable_blueprint.py:104-220`, `259-263`, `312-321` | PASS |
| Deterministic export and identity relationship | `design.md:125-150` sorts by full key canonical bytes, fixes JSON encoding and final LF, distinguishes `SHA256(raw)` from the existing policy digest, and requires re-encodability under the proposed ceiling | Existing key/source canonicalization and digest definitions are `src/pontius/immutable_blueprint.py:222-251`, `323-346`; the proposed artifact retains full keys rather than misusing the digest-only source representation | PASS |
| Nonempty loaded hit reaches the real consumer and differs from passive default | `design.md:167-181` declares the fixture-independent key/action oracle, TABLE_HIT, raise-to-6, one real delivery, exact fold-terminal pot/payout/final stacks, and independent-reader comparison | `src/pontius/v0a/runtime.py:141-179`, `858-960`, `1100-1135` uses the exact admitted source, records hit/miss, and delivers through the real spine/mailbox; the established neighboring control at `tests/test_v0a_hand_replay.py:485-539` confirms the applicable seam and typed illegal-hit behavior | PASS |
| Complete-hand outcome is independently read, not self-round-tripped | `design.md:176-181` requires `ReplayHost` completion and `verify_successful_trace` with a separately constructed expected policy | `src/pontius/v0a/replay.py:318-424`, `729-892` shows the host uses `HandRuntime`, while the reader independently reconstructs state, calls the sealed lookup directly, verifies rows, and judges settlement by chip depth | PASS |
| Miss and illegal hit remain sealed runtime responsibilities | `design.md:29-31`, `182-185` explicitly separates representability from live legality and requires passive miss plus `INVALID_BLUEPRINT_ENTRY` with no delivery | Runtime maps an illegal matching entry before emission at `src/pontius/v0a/runtime.py:882-939`; source lookup preserves passive default at `src/pontius/immutable_blueprint.py:348-375` | PASS |
| Acceptance oracles and negative population are independent and field-complete | `design.md:159-210` requires handwritten fixtures, separately constructed expected values/canonical bytes, every field, all action labels, postflop/history/null cases, corruption families, real public operations, runtime/replay, floor-first execution, and unchanged broader walls | The plan uses the real public runtime and independent reader rather than helper doubles. No yet-unimplemented test execution is claimed | PASS |
| New namespace and import boundary are narrow and enforceable | `design.md:35-59`, `195-197`; `source-opening-draft.md:30-51` fixes the two-module family, inert initializer, exact direct imports, undeclared-sibling rejection, legacy-origin negative control, and preservation of the six-file v0a set | Current public boundary gate has explicit exact-family classification/import-policy/public-check seams at `tools/check_stabilization_boundaries.py:145-176`, `204-225`, `253-317`, `476-527`; the proposed change fits those seams without baseline regeneration | PASS |
| Registration is additive, zero-grant, and CI-preserving | `source-opening-draft.md:43-73`, `89-118` limits the generator/test/inventory/profile/CI changes, requires mechanical deltas, retains zero binding hashes and all hard gates, and stops on unrelated changes | Current registrations and gates are visible at `tools/generate_test_inventory.py:156-186`, `tests/test_inventory_and_profiles.py:206-236`, `tests/test-profiles.toml:9-10`, and `.github/workflows/ci.yml:78-126` | PASS |
| Scope, budget, stop rule, and claims remain bounded | `design.md:212-248`; `source-opening-draft.md:89-123` keeps analyzer repair, runtime/kernel edits, operation, owners, rehearsal, source seal, measurements, and publication outside this decision; it declares line/fixture/round bounds and controller return conditions | This matches the brief, ADR-0486's registration-only decision, ADR-0487's source immutability, and ADR-0489's engineering-only opening | PASS |

## Frozen identity verification

Read-only Git-object inspection established all of the following:

1. The supplied ref resolves to candidate
   `336b8660f2f0b33fbeaa40d02cfc97c041ae6e1a`.
2. The candidate has the single parent
   `7ee314b443e10896e87a2e194f24eddda31ff77d` and tree
   `f796e812640f56ec6e21ca88f5c63ff91982b976`.
3. `git diff-tree -r` from the parent reports exactly the two in-scope added paths.
4. Their Git blob IDs are `c740285ff88406820b4f12ef3a9b4576fbb096ad`
   (`design.md`) and `b636fc4b808e1eb77ca72b0e7df367d2109c14a2`
   (`source-opening-draft.md`).
5. SHA-256 was recomputed over each raw `git cat-file blob` byte stream. Whole-row,
   digest-first ordinal sorting with two spaces and LF produced:
   - `a60015d4edd24c33fb78690998787b657d30272927d8fb99122e0efa03c530bf  docs/architecture/v0a-blueprint-artifact-r001/design.md`
   - `1038ac032e0385587b4cc963b158cff61f9441e2e4f074a9d79c49f115dad760  docs/architecture/v0a-blueprint-artifact-r001/source-opening-draft.md`
6. The SHA-256 of those sorted LF rows is the supplied manifest digest
   `404d81333837358c2c4d5d60e1702039a13c276dbe14979684033aa23b82024a`.
7. Every base blob pin in `source-opening-draft.md:75-84` matches `git ls-tree` at
   the supplied base.
8. Both reviewed blobs are UTF-8-compatible, LF-only, BOM-free, final-LF terminated,
   free of trailing whitespace, and no line exceeds 100 characters.

## Advisory implementation choices (non-binding)

- The 1,048,576-byte canonical/raw ceiling is clearly presented as a prospective
  versioned format choice, not a measured runtime wall, memory guarantee, or operating
  authorization (`design.md:146-151`; `source-opening-draft.md:110-112`). Its adoption
  remains a controller product-scope decision; this review found no conflicting contract.
- The design fixes observable validation, encoding, identity, and boundary behavior but
  intentionally leaves helper factoring and exact implementation structure open. Those
  choices remain advisory provided the 300-line codec bound and all stated public oracles
  are met.

## Inspection limits and independence

This was a cold, independent, design-only review. I read the frozen packet handoff,
candidate metadata and manifest; the two raw candidate blobs; the base `CLAUDE.md`,
applicable workflow sections/checklist, brief, and relevant ADR-0485/0486/0487/0489
boundaries; and bounded base source slices for the key/action values, card visibility,
runtime admission/delivery, replay reader, registration generator, boundary checker,
mirrored registration, profile header, and CI gates.

I did not read another review, a coordination ledger, an implementer transcript, or any
implementation narrative outside the handoff's required inputs. I did not import project
payloads, run tests, owners, prototypes, or runtime behavior; install dependencies; edit
source; mutate Git state; or use remote/network publication. No feature exists yet, so
this report establishes design/contract consistency and implementability, not executed
feature correctness. The pending separately authorized publication step is a logistics
gate, not a design defect.
