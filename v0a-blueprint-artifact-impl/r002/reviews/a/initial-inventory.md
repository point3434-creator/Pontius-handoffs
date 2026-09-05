# Initial invariant and related-path inventory — independent review A

Recorded before opening the r002 implementation FIX `coverage.md` or either
prior r001 review. Derived independently from the frozen requirements and Git
blobs at candidate `5e56e4454f7b8ccb360d3e36245abc33318349bb`.

## Identity, scope and authorization invariants

- Authority is ADR-0490 plus the two exact controller extensions whose checked
  SHA-256 values are `0d5cd53eb456a47a0ff346034fdfad173c77a39e37b030c99205c4913eeb2af7`
  and `666d89a6708c9d749265d816d063857432be42d754b6e76ad2dbafff6ba98ea3`.
- Candidate identity must be ref commit
  `5e56e4454f7b8ccb360d3e36245abc33318349bb`, parent/base
  `c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`, tree
  `dc18ed133504fe6c7677b494bcefba311cc73704`, and manifest SHA-256
  `6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5`,
  recomputed from frozen blobs under whole-row lexical sorting.
- The base-relative candidate surface is exactly twelve authorized paths. The
  r001-to-r002 correction surface is exactly `codec.py`, the two new codec test
  files, and the boundary checker. No driver/runtime/analyzer edits, grants,
  source seal, operating authority, or extra file population is permitted.
- Bounds: initializer plus codec at most 300 physical lines; the two new test
  files at most 300 combined; two fixtures at most 8192 bytes combined; at most
  100 manual added-plus-removed registration lines excluding generated files.
- Changed governance/code blobs must be LF-only, BOM-free, without trailing
  whitespace, and Python lines must satisfy the repository's 100-column rule.

## Codec and schema invariants

- Public API is only exact-bytes `decode_blueprint`, exact-source
  `encode_blueprint`, and typed `BlueprintArtifactError`; package initializer is
  inert. Codec direct imports are only `__future__`, `json`,
  `pontius.immutable_blueprint`, and `pontius.no_limit_betting`.
- Decode admits strict UTF-8 JSON without BOM; it rejects malformed/trailing
  material, duplicate decoded member names at every depth, floats/nonfinite
  constants, unsupported versions, and missing/unknown fields before returning
  any policy.
- The root/entry/key/action graph is closed and exact. The key carries all 17
  declared fields and history rows carry all eight ordered fields. Wire arrays
  become tuples. Existing constructors remain the semantic authority for card
  uniqueness/overlap and street board width, blind ordering, tuple widths,
  pending-seat uniqueness, action legality/shape, and history constraints.
- Exact type discipline is symmetric: booleans never satisfy integers;
  subclasses and malformed exact source/entry/key/action graphs are refused.
  Partially initialized exact slotted records at each traversed level must yield
  `BlueprintArtifactError`, not leak `AttributeError` or invoke foreign hooks.
- Every integer route (scalar key field, vector member, nullable integer,
  history field, and action amount) shares `0 <= value < 10**640`, subject to
  its narrower sign/range. Decode checks at most 640 decimal digits before
  conversion; encode rejects `10**640` before decimal formatting, key hashing,
  or source hashing. Behavior must be independent of ambient decimal conversion
  configuration and close under the supported minimum setting of 640.
- Every admitted string is a Unicode scalar-value string after JSON escape
  processing. Lone high/low surrogates are refused in both directions; escaped
  valid pairs and literal astral source IDs preserve the same string, without
  normalization, trimming, or replacement. Source ID remains nonblank.
- Private-card ordering is the sole normalization. Duplicate semantic keys are
  refused after that canonicalization, even when actions agree.
- Encoding contains full keys; entries sort by full key canonical bytes; object
  keys are sorted with compact separators, ASCII escaping, UTF-8/ASCII output,
  and exactly one final LF. Equivalent entry permutations encode identically.
  Independently authored canonical bytes and full field values must be the
  oracle, not self-round-trip alone.
- Raw artifact SHA-256 and existing policy digest remain distinct. Every
  successfully encoded codec-admitted source decodes to the same exact source
  and policy digest. Digest closure at the numeric maximum is material.
- There is no artifact-byte, entry-count, or source-ID-length ceiling. A valid
  empty source whose canonical bytes exceed the former one-MiB limit round-trips;
  this is not a performance/capacity claim.

## Behavioral and boundary invariants

- The handwritten nonempty raise fixture reconstructs the separately declared
  full key/action, and history fixture covers postflop board, nullable history,
  all action labels, and all eight history positions.
- Loaded fixture bytes enter the actual `HandRuntime` public `blueprint=` path.
  The matching entry selects raise-to-6 with TABLE_HIT and one delivery; a miss
  keeps passive call-to-2; matching raise-to-1000 produces typed
  `INVALID_BLUEPRINT_ENTRY`, NOT_ATTEMPTED, and no delivery.
- The complete fold control runs through `ReplayHost`; expected payouts are
  `(0,0,0,5,0,0)` and final stacks `(200,199,198,203,200,200)`. The existing
  independent reader verifies the trace against a separately constructed policy,
  not the decoded object.
- The public repository boundary gate, not just helper calls, must accept the
  real candidate and reject undeclared codec siblings, the top-level alias
  `src/pontius/blueprint_artifact.py`, forbidden codec imports, and legacy origins
  importing the codec. It must keep scanning the family and preserve baseline
  edges, SCC controls, host-only rules, and the six-file v0a population.
- The driver extension classifies only `tools/v0a_rehearsal_driver.py` and only
  its three existing internal edges: `pontius.immutable_blueprint`,
  `pontius.v0a.replay`, and `pontius.v0a.trace`. Undeclared tool siblings and any
  fourth internal edge remain public-gate refusals.
- Registration adds exactly `test_blueprint_artifact.py`,
  `test_blueprint_artifact_boundary.py`, and the unchanged
  `test_v0a_rehearsal_driver.py` to generator/mirror/generated inventory/profile
  population. Stable historical assignments remain; both capability binding
  hashes stay zero. CI adds only direct CPU steps for the two codec suites and no
  driver step. The unchanged writer/check path must reproduce checked-in bytes.
- Consolidation to the exact test-line budget must retain the full adopted
  acceptance controls, including independent canonical bytes, every field/value
  category, full action/history labels, all malformed/duplicate/partial cases,
  runtime hit/miss/illegal behavior, replay/reader, numeric/Unicode closure,
  above-former-ceiling behavior, missing exact slots, and actual public boundary
  negatives.

## Related frozen paths to challenge

- New/changed: `src/pontius/blueprint_artifact/{__init__,codec}.py`, both JSON
  fixtures, both codec test files, `tools/check_stabilization_boundaries.py`,
  `tools/generate_test_inventory.py`, `tests/test_inventory_and_profiles.py`,
  `tests/test-inventory.json`, `tests/test-profiles.toml`, and CI.
- Semantic producers/consumers: `src/pontius/immutable_blueprint.py`,
  `src/pontius/no_limit_betting.py`, `src/pontius/holdem_cards.py`,
  `src/pontius/v0a/{runtime,replay,trace,model}.py`.
- Source gate: `tools/generate_dependency_baseline.py`,
  `docs/architecture/dependency-baseline.toml`, and
  `tests/test_stabilization_boundaries.py`.
- Driver amendment: `tools/v0a_rehearsal_driver.py` and unchanged
  `tests/test_v0a_rehearsal_driver.py`.
- Acceptance preservation: `tests/test_immutable_blueprint.py`, the four
  unchanged v0a suites named by the design, inventory/profile checks, and the
  existing direct CPU hard-gate population; broad execution remains post-CLEAN.

## Planned fresh evidence before verdict

- Recompute Git/ref/tree/parent/blob manifest identities, line/byte/style bounds,
  exact changed surfaces, registration delta, generated-file semantic delta, and
  import graph from frozen bytes.
- Run only targeted isolated-snapshot checks: floor first, then exact 3.14 where
  available; codec test normally and with `-X int_max_str_digits=640`; boundary
  suite/public checker; focused registration/writer check; and reviewer-owned
  probes at real public seams for material gaps not already isolated by a focused
  test. No broad population or primary/authoring payload.
