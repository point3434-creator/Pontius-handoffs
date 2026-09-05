Reviewer A — v0a-hand-adapter-design/r003 — commit 02e24f143b8df4b2f03e8a94c58ab57905a8b2b6 — manifest f730799182d3f3eda2d9efa273048b2eaf28ceeb4274ea7525df95426ca679b1 — CLEAN; Spec PASS; Quality PASS; C/I/M 0/0/0; Design SOUND.

## Findings

No Critical, Important, or Minor findings. No required correction remains unresolved.

The prior C1 source-identity defect is closed at design level. Every initial and final Git identity/object operation must now use `--no-replace-objects` after environment scrubbing, including HEAD, commit/tree, base comparison, inventory, blob reads, and revalidation. The required public control reproduces the relevant failure scenario: HEAD retains original commit O, a replacement object supplies modified adapter or scenario bytes, and the checkout contains those substituted bytes. Raw-object comparison must refuse before host construction, trace creation, or success output. The design correctly does not reject an irrelevant replacement ref when the executed bytes still match raw O.

This is design acceptance only. The future CLI and its replacement-object controls are unimplemented and unexecuted.

## Independent invariant and affected-path inventory

Before opening `coverage.md`, I recorded these protected invariants:

- Literal scenario cards must survive `literal → inverse suit transform → Fixture.deal` unchanged, with private pairs compared unordered and board order preserved.
- Scenario, blueprint, filesystem, and source inputs must be admitted exactly and entirely before host or trace construction.
- The complete deal, opposing private cards, and future board remain confined to the host-side scenario/ReplayHost and independent reader. Runtime and blueprint selection receive only the controlled hand and revealed board.
- Successful output is conjunctive: real host receipt, exact persisted-byte/hash equality, independent legal replay, declared action/reason/pot/payout agreement, raw source revalidation, and only then stdout.
- Published prefixes survive every later failure; no failed phase can become success through a later check.
- Ground truth is the author-declared action/chip arithmetic plus the sealed independent legal/settlement reader, not runtime output or a regenerated golden.
- Raw source identity must describe the committed blobs whose matching bytes execute, unaffected by Git replacement objects, archive attributes, or checkout normalization.

The affected surface is the three new production paths, three new tests, four fixtures, and six pinned registration files. Relevant preserved contracts include `river.py`, `holdem_cards.py`, `immutable_blueprint.py`, the blueprint codec, `v0a/{model,runtime,replay,trace}.py`, and the old rehearsal driver, plus their card, artifact, replay, trace, fault, driver, inventory, and boundary tests.

After that inventory, I opened the deferred claim. Its SHA-256 reproduced as `051adc62d56fd25a3795a0b76b257abfd2ba1f11a5031fd25025d7d78a356e3d`. Its discovery, affected Git operations, required CLI falsifier, and stated limits match the prior C1 and my inventory. Its “no schema, host, policy or trace change” boundary is correct for this fix; I nevertheless reviewed those unchanged portions substantively as required.

## Contract assessment

Literal-card handling is compatible with the base contracts. `Fixture.deal` maps source suits through the seed-derived permutation, so rewriting literal suits through its inverse restores the intended cards. The mandatory complete-deal comparison detects a reversed or otherwise incorrect transform. The proposed all-24-permutation controls use fixed external numeric expectations rather than the new conversion as its own oracle.

The declared raise-case ground truth is correct under the actual rank-major `cdhs` encoding: controlled seat 3 holds `2c/5c`, yielding key `(0,12)`, while the historical fixture’s unadapted seed permutation yielded `(1,13)`. A raise to 6 followed by folds from seats 4, 5, 0, 1, and 2 returns the uncalled excess and produces the declared 5-chip pot, payouts, and final stacks. The showdown case also checks out: seat 0’s kings make three kings on the declared board, winning the six-way 12-chip pot with the stated final stacks.

The closed scenario schema applies exact integer/bool separation, strict card syntax and uniqueness, duplicate/unknown/missing-field refusal, integer-token and aggregate bounds, and immutable fixture construction before host creation. Legal schedule errors are appropriately left to the real host and independent reader rather than duplicated or repaired in the decoder.

Full-deal separation is sound. `pontius.hand_scenario` is explicitly host-side; it may construct and validate a `Fixture`, but the runtime and immutable blueprint retain their existing one-seat interfaces. The proposed boundary changes narrowly permit the scenario-to-replay edge while requiring negative controls for runtime imports, undeclared siblings, extra tools, and incoming blueprint-artifact edges.

Reader semantics are used correctly. `verify_successful_trace` independently rebuilds betting/card state, checks the complete event schedule, repeats policy lookup, recomputes showdown and chip-depth settlement, and returns verified payouts, final stacks, pots, semantic identity, and run ID. Only after that acceptance does `parse_trace` supply the action/hit/fallback projection checked against the scenario’s independently declared rows. Summary values therefore come from accepted persisted bytes, not unchecked host objects or expectations.

The six registration exceptions fit the actual base checker/inventory/CI structure. The scenario family and adapter require new origin/import classifications; the three suites require inventory/profile registration and direct floor-job steps. No dependency-baseline regeneration or analyzer repair is necessary. ADR-0486’s zero-grant treatment remains intact.

## Identity and hygiene

Raw-object recomputation produced:

- Commit: `02e24f143b8df4b2f03e8a94c58ab57905a8b2b6`
- Sole parent: `7a387e995e3b37232d2379332927247a4d49c64e`
- Tree: `bd1cd2f83612aacac9d1de1c8e0afd673a86579c`
- Ref: `refs/heads/review/v0a-hand-adapter-design/r003`
- Scope: exactly the three specified additions, all regular mode `100644`
- `brief.md`: `f33da4160da7aa8b7caa8c99b15ff9456b257e970eb0c99efd349fc817ff06b9`
- `design.md`: `fbe4d15e03ae06567a4a0a795e23976fa29aa48f50da024c36f5beccb175e63a`
- `source-opening-draft.md`: `4e62f00b05c3401905d04d57e04db27fb1ea5f5a28286f3bd979736970ac41da`
- Whole-row-sorted LF manifest: `f730799182d3f3eda2d9efa273048b2eaf28ceeb4274ea7525df95426ca679b1`

Each r003 blob equals its r002 counterpart with exactly one final extra LF removed. All three r003 documents still end in one LF. The total delta is exactly three bytes; r002’s manifest independently reproduced as `f2c8c9f8c292585623b06a7f623e6b31f6202199f66c82afd78d765bfcab1b1a`.

All six declared base blob pins reproduce exactly. The frozen documents are UTF-8, BOM-free, CR-free, trailing-whitespace-free, and at most 94 bytes per line. `git diff --check` passes. No replacement refs were present.

The object checkout remains detached at the base with no tracked modification and six untracked mutable document copies under the r001/r002 directories. Those copies were not used as review inputs and do not affect the frozen candidate.

## Design verdict and observation

Design SOUND. The scenario codec remains a value adapter; the CLI owns the source/file/acceptance boundary; the sealed host and reader retain poker semantics. The prior defect required a localized raw-Git correction, not architectural restructuring.

Non-blocking observation: the 400-line combined test budget is tight for the mandated schema matrix, 24 suit permutations, real CLI/source-replacement cases, failure seams, and boundary controls. The written stop rule correctly requires reassessment rather than omitted or compressed coverage if that budget proves insufficient.

## Limits

This was a read-only design review. I inspected all three frozen blobs, the permitted prior finding, deferred coverage claim, governing contracts, actual base sources, registration machinery, and directly relevant tests. I did not import project code, execute tests or hands, invoke an owner, modify files/index/HEAD/refs, inspect current sibling reports or controller transcripts, install anything, spawn agents, or use the network. No implementation acceptance, source seal, adoption, runtime result, or invocation authority is claimed.