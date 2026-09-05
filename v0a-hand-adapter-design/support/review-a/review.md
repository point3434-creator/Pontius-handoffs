Codex independent review — v0a-hand-adapter-design/r001 @ 21474e3d5b105c1709205df1eb5543417abb5a0a / manifest ce327c6982338c148d26d4d73cad978ad05b49596520449337d2cc9cb9be0bc9: CLEAN; Spec PASS; Quality PASS; C/I/M 0/0/0; Design SOUND.

## Identity and hygiene

The frozen candidate identity is internally consistent and independently reproduced:

- Raw commit identity recomputes to `21474e3d5b105c1709205df1eb5543417abb5a0a`.
- Sole parent is the declared base `7a387e995e3b37232d2379332927247a4d49c64e`, whose raw identity also recomputes.
- Tree is `be02e38610dee1a819a7686f044aee56899ba785`, also reproduced from its raw Git object.
- The review ref resolves to the candidate.
- Exact delta is three additions only: `brief.md`, `design.md`, and `source-opening-draft.md`.

Frozen blob SHA-256 rows are:

```text
042a2f345ae3bc6d979ef43c738be4656a9b9a7afcd49625589b48b5d04c1a9d  docs/architecture/v0a-hand-adapter-r001/brief.md
4e62f00b05c3401905d04d57e04db27fb1ea5f5a28286f3bd979736970ac41da  docs/architecture/v0a-hand-adapter-r001/source-opening-draft.md
917c112d49daf461b477b5c066e1e6799b697af24e7e5ed1489089fd7d5178e6  docs/architecture/v0a-hand-adapter-r001/design.md
```

Whole-row ordinal sorting with exact LF rows produces the supplied manifest SHA-256. All three blobs are LF-only, final-LF terminated, BOM-free, free of trailing whitespace, and have no line over 100 characters.

All six proposed registration pins match the base exactly:

```text
ccf41b8e145d4463b6dd13aa224df54440d87c4d  tools/check_stabilization_boundaries.py
7f7f9cf16553bcc36f2e5015c782bb203baebd68  tools/generate_test_inventory.py
75fdc9bf532958bf5d0300488dc828a5d3a1d66a  tests/test_inventory_and_profiles.py
e36ac6213decc0e3dc9cc9f38559fcf9fa5bed6c  tests/test-inventory.json
685a65c9cd8c0a8c7a347c94832cbc0370a6fd1a  tests/test-profiles.toml
1c5278605fdfde8c75a2b31ea4a06251ca88c975  .github/workflows/ci.yml
```

The live checkout has an untracked `docs/architecture/v0a-hand-adapter-r001/` directory. It was not used for review and does not affect the frozen candidate, but the live worktree itself is therefore not Git-clean.

## Contract assessment

The literal-card adapter is compatible with the sealed implementation. `Fixture.deal()` maps each template suit through `suit_mapping(permutation_for_label(seed_label))`; rewriting each literal suit through that mapping’s inverse supplies exactly the required preimage. Comparing board cards in order and private pairs canonically/unordered matches `SixSeatHoldemDeal` and `OneSeatCardState`. The acceptance plan’s independent fixed text/numeric controls across all 24 permutations prevents a mutually wrong encode/decode pair from serving as its own oracle.

The declared raise control is consistent with actual betting semantics. A seat-3 raise-to-6 followed by folds returns the unmatched four-chip excess, leaving effective contributions of 2 from seat 3, 1 from the small blind, and 2 from the big blind. Thus pot/payout 5 and final seat-3 stack 203 are correct. The literal controlled hand `2c/5c` yields canonical key `(0,12)` after adaptation, unlike the existing suit-renamed artifact control `(1,13)`.

The showdown declaration is also consistent: six preflop contributions of 2 make a 12-chip pot; seat 0’s `Kh/Kd` with board king wins with three kings, yielding payouts `(12,0,0,0,0,0)` and final stacks `(210,198,198,198,198,198)`.

Input admission is suitably separated from hand execution. Scenario and policy bytes are read, hashed, strictly decoded, and value-owned before `ReplayHost` construction. Duplicate decoded member names, bool/integer aliases, float/nonfinite tokens, BOM/encoding faults, card overlap, width/domain faults, digit-limit violations, and aggregate chip overflow are explicitly covered. Actor order, sizing, script exhaustion and settlement truth correctly remain semantic responsibilities of the real host and reader rather than being duplicated in the decoder.

Full-deal separation remains intact. The new codec is explicitly host-side and constructs a `Fixture`; the unchanged `ReplayHost` alone owns the resulting `SixSeatHoldemDeal` and future schedule. `HandRuntime` continues to receive only controlled private cards, public reveals and betting events. Blueprint keys contain the controlled hand, revealed board and public betting state—never opponent cards or unrevealed board cards. The proposed boundary policy also preserves the six-file v0a population and forbids runtime/policy imports of the new scenario package.

Acceptance is not circular. Host `passed` and accounting state are only the first conjunct. The adapter then requires persisted bytes to equal the returned trace and receipt digest; `verify_successful_trace` independently reparses those bytes, checks source/configuration/policy bindings, reconstructs the legal event schedule, performs the sealed lookup from visible state, and compares settlement against the chip-depth oracle and declared fixture values. A second parse of those same immutable accepted bytes supplies the complete decision projection for comparison with independently authored expected actions and reasons. No header, recomputed hash, host flag, or unchecked outcome alone grants success.

Failure retention and output semantics are clear: no retries, no trace rewriting or cleanup, no success line after a later verification failure, and nonzero status for admission, host, readback, replay, expectation, source-revalidation or output-publication failure.

## Findings and required outcomes

No Critical, Important, or Minor finding survives review. There are no unresolved corrections.

The following are existing mandatory implementation outcomes, not new findings or optional advice:

- Preserve the exact inverse-suit adaptation and independently authored literal-card controls.
- Keep both inputs fully admitted before host construction or trace creation.
- Keep scenario/full-deal objects out of runtime and policy-selection boundaries.
- Exercise hit, miss and illegal matching entries through the real runtime.
- Require the complete host/readback/reader/expectation/source conjunction before emitting success.
- Ensure controlled corruption schedules still execute the real host, real file publication and independent checker, with an external exit/stdout/retained-byte oracle.
- Preserve the exact source additions, six pinned registration exceptions, zero capability grant, floor-first dual-interpreter checks and two Tier C implementation reviews.

These requirements are already stated by the frozen documents; implementation technique within them remains advisory.

## Design verdict and limits

Design SOUND. The shape is a narrow, acyclic host-side decoder plus CLI around the existing host, codec and reader. It does not copy poker/runtime semantics, alter sealed source, invent another trace framework, or confuse design acceptance with execution authority. The stronger source preflight is proportionate to the declared source-bound summary and remains fail-closed.

Confidence: high for design/source compatibility. The largest unknown is necessarily the unimplemented adapter—particularly exact source revalidation and deterministic post-publication fault controls. The cheapest falsification is the prescribed implementation suite through the real CLI boundary. A required sealed-core change, broader package/import grant, failure to preserve literal cards, or inability to make the independent acceptance conjunction fail under deliberate corruption triggers the stated stop rule.

This was static frozen-object design review only. No project code, tests, hand, owner, import, network operation or source-opening action was executed. Coverage remains the declared finite correctness population; it establishes no exhaustive poker coverage, concurrent-writer defense, arbitrary-resource guarantee, operational authority, timing result, policy strength or evidentiary result.