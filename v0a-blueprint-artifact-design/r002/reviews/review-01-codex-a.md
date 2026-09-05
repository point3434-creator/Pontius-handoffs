# Cold design review A — v0a-blueprint-artifact-design/r002

Reviewer: Codex, independent cold Review A  
Date: 2026-09-05  
Round kind: Tier C FIX design review  
Candidate: `a552f6f34efe10155a702fd09a03bcc70802a369`  
Base and sole parent: `7ee314b443e10896e87a2e194f24eddda31ff77d`  
Tree: `14b71ec9dc6bc6db20393008dde9f25db13a95c5`  
Manifest SHA-256:  
`67abe320f73b8edfab60a93511f31eac62d0fac0279cdef712acda91fcf7aced`

## Verdict

- Specification: **PASS**
- Engineering quality: **PASS**
- Required-correction verdict: **CLEAN**
- Counts: **Critical 0 / Important 0 / Minor 0**
- Design verdict: **SOUND**

No required correction remains. The r002 documents close all three authorized
r001 Review B corrections and retain the brief's full bounded design and source-opening
contract. The additive byte codec is the right shape: it owns representation admission,
reuses the existing immutable key/action and digest contracts, and hands an admitted exact
source to the unchanged runtime and replay boundaries. The six registration exceptions are
explicit, base-blob-bound, zero-grant, and do not reopen the parked analyzer.

## Required findings

None.

There is no Critical, Important, or Minor requirement failure to reproduce or correct.
The absence of executed feature tests is expected: this is a design/source-opening review,
the codec does not exist, and the candidate neither authorizes nor claims execution.

## Initial invariant and related-path inventory

I recorded this inventory before opening the deferred `coverage.md`.

### Initial invariant

The codec must be a total, symmetric admission boundary over exactly its declared
source/value graph. Wire-to-source and source-to-wire must enforce the same numeric and
Unicode domains. Every successful encode must decode with identical complete keys/actions
and the unchanged policy digest. Refusal must be typed and atomic. The codec must not
duplicate runtime legality or key-reachability semantics, and raw-artifact identity must
remain distinct from canonical policy identity.

The source-opening side must authorize only a narrow additive package and the exact
registration work needed to scan, inventory, and run it. It must neither edit the sealed
runtime/kernel behavior nor grant analyzer, process, network, GPU, owner, rehearsal, or
operational authority.

### Initial related-path inventory

- Proposed surface: `src/pontius/blueprint_artifact/{__init__,codec}.py`, the two named
  test files, and the two named literal JSON fixtures.
- Existing value and identity contracts: `src/pontius/immutable_blueprint.py` and
  `src/pontius/no_limit_betting.py`.
- Real consumers: `src/pontius/v0a/runtime.py`, `replay.py`, `trace.py`, and `model.py`.
- Registration boundary: only `tools/check_stabilization_boundaries.py`,
  `tools/generate_test_inventory.py`, `tests/test_inventory_and_profiles.py`,
  `tests/test-inventory.json`, `tests/test-profiles.toml`, and `.github/workflows/ci.yml`.
- Governing requirements: the portable-artifact brief under ADR-0489; ADR-0485 key/action,
  digest, runtime/replay, source-seal, and registration boundaries; ADR-0486's parked,
  known-unsound, zero-grant analyzer disposition; and ADR-0487's sealed library surface.

### Initial falsifiers

- A value admitted in one direction fails the other direction or the existing digest path.
- A wire representation loses, aliases, or substitutes a complete key or action.
- The runtime/replay expected result is derived from the codec rather than an independent
  declared action and settlement oracle.
- A registration delta widens permissions, changes inference logic, or escapes the six
  exact exceptions.
- A capacity or operational gate is adopted without authority and provenance.

## Deferred coverage comparison

I opened frozen `coverage.md` only after making the inventory above.

- **Category:** matches. It identifies codec closure across export, import, and unchanged
  policy identity; explicit scalar portability; and removal of the unrelated byte ceiling.
- **Discovery:** matches. It follows source ID plus every key/action/history field through
  constructors, canonical bytes, digest, both codec APIs, and the real consumers. It does
  not claim a whole-runtime or analyzer audit.
- **Controls:** match and are independent. Numeric boundary cases span raw JSON, exact
  source graphs, digest, encode, and re-decode. Unicode cases cover both lone surrogate
  directions and valid astral preservation. The above-former-limit case proves removal of
  the old compatibility gate without being presented as an operational benchmark.
- **Limits:** match. Reachability, policy quality, hostile module mutation, arbitrary
  resource safety, and analyzer soundness remain excluded. The six registration exceptions
  and line/fixture budgets remain unchanged.
- **Falsifiers:** are sufficient for the correction category. Failure at the documented
  minimum digit setting, encoder/decoder Unicode asymmetry, or any surviving byte ceiling
  would directly disprove the respective closure claim.

No missed related member or unsound discovery method remains within this FIX scope.

## Closure of the authorized r001 corrections

### 1. Ungrounded artifact-byte ceiling — closed

- **Locations:** `design.md:174-181`; `source-opening-draft.md:109-116`.
- **Prior unmet requirement:** r001 imposed a 1,048,576-byte compatibility gate without a
  declared policy population, worst-case size derivation, or approved provenance.
- **r002 outcome:** the codec has no artifact-byte, entry-count, or source-ID-length ceiling.
  The text explicitly removes rather than renames the guessed gate and disclaims hard
  capacity, memory, time, and availability guarantees.
- **Consequence prevented:** a schema-valid policy is no longer made non-portable merely
  because its bytes cross the arbitrary former threshold.
- **Verification:** `design.md:237-240` requires a valid empty policy whose canonical bytes
  exceed the former one-MiB threshold to round-trip. The expected outcome is admission in
  both directions; no one-byte-over refusal remains because no byte limit remains.

This satisfies the authorized choice to remove the optional ceiling. No replacement guessed
budget appears in either corrected document.

### 2. Numeric portability across decode, encode, and digest — closed

- **Locations:** `design.md:74-89`, `design.md:228-234`, and
  `source-opening-draft.md:109-116`.
- **Prior unmet requirement:** unbounded decimal integers could satisfy the written schema
  yet fail CPython JSON decoding, encoding, or the existing canonical digest under an
  ambient integer-conversion setting.
- **r002 outcome:** every integer field has the uniform additional range
  `0 <= value < 10**640`, with all narrower semantic ranges retained. Decode rejects a JSON
  integer token longer than 640 decimal digits before conversion. Encode checks the exact
  integer value before formatting, key canonicalization, or policy hashing. Neither path
  changes or derives behavior from process-global settings.
- **Existing-path fit:** `src/pontius/immutable_blueprint.py:222-251` serializes every full
  key through canonical decimal JSON; `:323-346` serializes the source identity using key
  digests and action values. The selected domain covers both conversions rather than adding
  a codec-only workaround or second digest format.
- **Consequence prevented:** a schema-admitted policy no longer fails differently across
  supported interpreters or scrubbed startup configurations merely because one integer is
  too wide for decimal conversion.
- **Verification:** independently authored `10**640 - 1` data must survive
  decode -> unchanged `source.digest` -> encode -> decode; `10**640` and longer tokens must
  receive the common typed refusal. The focused codec suite must also start with
  `-X int_max_str_digits=640` on CPython 3.11.15 and 3.14.6.

The Python 3.11 and 3.14 built-in-type documentation states that 640 digits is the lowest
configurable nonzero threshold and that both decimal text-to-int and int-to-decimal text
conversions are limited. The JSON documentation confirms that `parse_int` receives the raw
integer token string, providing the declared pre-conversion seam:

- <https://docs.python.org/3.11/library/stdtypes.html#integer-string-conversion-length-limitation>
- <https://docs.python.org/3.14/library/stdtypes.html#integer-string-conversion-length-limitation>
- <https://docs.python.org/3.11/library/json.html#json.load>
- <https://docs.python.org/3.14/library/json.html#json.load>

### 3. Encoder closure over the decoder's Unicode domain — closed

- **Locations:** `design.md:42-52`, `design.md:91-96`, `design.md:235-237`, and
  `source-opening-draft.md:109-116`.
- **Prior unmet requirement:** the existing source constructor accepts a nonblank `str`
  containing a surrogate code point, while r001 decode rejected such a value and encode's
  domain did not say whether it rejected it.
- **r002 outcome:** an existing source becomes codec-admitted only after the codec's own
  checks. Both directions require Unicode scalar-value strings. Encode rejects any high or
  low surrogate in `source_id` before hashing/output; decode checks after JSON escape
  processing. Valid astral characters are preserved without normalization or replacement.
- **Consequence prevented:** no successful public encode can produce bytes the public
  decoder must reject, and implementers cannot choose contradictory widening or narrowing.
- **Verification:** both operations refuse lone high and low surrogates with
  `BlueprintArtifactError`; valid escaped pairs and literal astral source IDs preserve the
  string and policy identity; every successful encoding must re-decode to the same digest.

The Python JSON documentation independently confirms that the standard library accepts and
emits unpaired surrogate code points by default. The explicit codec check is therefore a
real required boundary, not a redundant assumption:

- <https://docs.python.org/3.11/library/json.html#character-encodings>
- <https://docs.python.org/3.14/library/json.html#character-encodings>

## Full corrected design and source-opening contract

The correction did not weaken or omit the original bounded requirements:

| Requirement | Frozen contract and direct evidence | Result |
| --- | --- | --- |
| Exact byte API and atomic typed refusal | `design.md:33-63` | PASS |
| Closed, full-key, non-executable schema | `design.md:65-150`; exact 17 key members match `immutable_blueprint.py:27-251` | PASS |
| Deterministic encoding and separate raw/policy identities | `design.md:152-181`; existing policy bytes/digest at `immutable_blueprint.py:323-346` | PASS |
| Independent codec oracle, not self-round-trip alone | `design.md:187-202` | PASS |
| Real controlled action and no helper double | `design.md:203-207`; `HandRuntime` owns/adopts the source at `runtime.py:325-369` | PASS |
| Complete-hand replay and independent reader | `design.md:208-214`; `ReplayHost` and `verify_successful_trace` at `replay.py:318-424,729-778` | PASS |
| Miss and illegal-hit behavior remain runtime-owned | `design.md:215-219`; ADR-0485 blueprint outcome contract | PASS |
| Floor-first supported interpreter checks | `design.md:242-251` | PASS |
| New-path and proportionality bounds | `design.md:187-192,254-280`; `source-opening-draft.md:30-41` | PASS |
| Six exact, zero-grant registration exceptions | `source-opening-draft.md:43-73` | PASS |
| Registration exception bound to current base blobs | `source-opening-draft.md:75-87`; all six object IDs independently reproduced | PASS |
| No analyzer repair, owner, operation, rehearsal, source seal, or commit authority | `source-opening-draft.md:89-126` | PASS |

The controlled-action example is internally consistent: button 0 places blinds at seats 1
and 2, controlled seat 3 raises to 6, and seats 4, 5, 0, 1, and 2 fold. Returning the four
uncalled chips leaves contributions 0/1/2/2/0/0, a five-chip pot, payout
`(0, 0, 0, 5, 0, 0)`, and final stacks `(200, 199, 198, 203, 200, 200)`. This supplies an
independent non-passive action and settlement oracle before implementation.

The source-opening draft also matches the actual base registration shape. The boundary
checker currently recognizes only the sealed `pontius.v0a` additive family, applies its
import policy through the public gate, rejects legacy outgoing-edge drift, and calls the
policy from that gate. The draft requires a separate exact artifact family, forbids legacy
imports into it, preserves existing SCC/edge/v0a controls, and adds no exemption from
scanning. The inventory, mirrored expectation, generated inventory/profile, and release-slot
CI changes are each limited to the two new test paths and mechanically derived identities.

## Identity and exactness verification

The local freeze-snapshot object database resolved the published ref to the candidate above.
The commit has exactly one parent, the stated base, and the stated tree. A rename-disabled
diff against that parent contains exactly these three additions and no other path:

```text
A  docs/architecture/v0a-blueprint-artifact-r002/coverage.md
A  docs/architecture/v0a-blueprint-artifact-r002/design.md
A  docs/architecture/v0a-blueprint-artifact-r002/source-opening-draft.md
```

Raw blob bytes read from Git—not checkout files and not decoded PowerShell hashing—produced:

```text
d83bfd196dc8fe9b632858a83abba77a7dc9d8ae9e3247ea1d1fed82de80b2e3  coverage.md
5403709d2ee8cc6b0cbacd7775ca7cf71f07f1eecba5e5902286a2387de1b96d  design.md
346aa8c36c59d970bd1ae71ecdf86d64ccbe78c996f955e526f581b061c96808  source-opening-draft.md
```

Sorting complete manifest rows as whole digest-first byte strings, with two spaces before
each POSIX path and one final LF, reproduced manifest SHA-256
`67abe320f73b8edfab60a93511f31eac62d0fac0279cdef712acda91fcf7aced`.

The three frozen blobs are strict UTF-8, LF-only, BOM-free, final-LF terminated, have no
trailing whitespace, and have no line longer than 100 characters. The six base Git blob
object IDs printed in `source-opening-draft.md:75-87` also reproduce exactly from the stated
base commit.

The permitted prior report was read only through its `Required corrections` section after
its bytes reproduced SHA-256
`44a4523a86bb647f1aed7e48b9366bd93e63ec219ae3cb3049926e6760165706`.

## Advisory implementation choices

No additional advisory preference is needed for design acceptance. The future implementer
may centralize the scalar-domain checks to reduce drift, but that technique is non-binding;
the binding outcomes are the symmetric public behaviors and independent controls already
stated in the design.

## Independence and limits

This review used the frozen handoff, candidate metadata, manifest rows, raw candidate/base
Git blobs, the governing brief/ADR/workflow inputs, the permitted r001 Review B Required
corrections section, and the cited official CPython documentation. I did not read the other
current review, prior Review A, coordination/disposition/ledger material, controller thread,
or implementation narratives.

I did not import project payloads, execute tests, prototypes, generators, owners, runtime
code, or feature code; install dependencies; modify Git/source state; publish to the network;
or use subagents. The only review-artifact write was this report; the issuer's separately
directed post-issuance workflow action is one append-only verdict line in `progress.md`.
The review is a static design and source-opening judgment. It does not claim an
implementation, runtime result, source seal, capacity guarantee, policy quality result,
rehearsal, or operational authority.
