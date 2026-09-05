Reviewer B — v0a-hand-adapter-design/r003 — commit 02e24f143b8df4b2f03e8a94c58ab57905a8b2b6 — manifest f730799182d3f3eda2d9efa273048b2eaf28ceeb4274ea7525df95426ca679b1 — PASS: Spec PASS; Quality PASS; C/I/M 0/0/0; CLEAN; Design SOUND.

## Findings

No required corrections.

The prior C1 replacement-object finding is closed. The design now requires `--no-replace-objects` on every initial and final Git identity/object operation after environment scrubbing, covering HEAD, commit/tree inspection, base comparison, inventories, blob reads, and revalidation. It also forbids archive, checkout-normalized, or caller-supplied replacement views as raw identity oracles.

The required future public-boundary control is adequate: with HEAD still naming original commit O, a replacement commit or source blob supplies changed adapter/scenario bytes and the checkout is materialized from that substituted view. The CLI must refuse before host construction, trace creation, or success output. A replacement ref with no raw-byte mismatch is correctly outside the refusal predicate; the protected fact is executed-byte identity, not mere ref presence.

Concrete prior failure scenario now prevented: if `refs/replace/O` points to R containing a modified adapter while HEAD still prints O, raw `ls-tree` and `cat-file` operations inspect O rather than R. Checkout comparison therefore detects the R-derived bytes and refuses instead of reporting O as their source.

## Initial invariant and affected-path inventory

Recorded before opening `coverage.md`, the protected invariant was:

- Raw scenario and blueprint bytes must be read once, separately hashed, strictly decoded, and retained independently from their derived semantic identities.
- Literal scenario cards must emerge from `Fixture.deal()` unchanged despite its seed-derived suit permutation.
- Opponent hands, future board cards, fixture schedule, and expectations remain host-side and never enter blueprint selection.
- Acceptance is conjunctive: real host completion, exact persisted-byte equality and receipt hash, independent legal replay, declared action and settlement expectations, source revalidation, then one success line.
- Every failure remains nonzero, prints no success line, performs no retry or cleanup of published bytes, and cannot be replaced by a later successful phase.
- Reported source commit and manifest must describe the raw committed blobs whose matching checkout bytes execute.
- Registration may admit only the named host-side origins and tests, with no analyzer repair or capability grant.

The independently identified affected paths were the three frozen documents; proposed `pontius.hand_scenario/{__init__,codec}.py` and `tools/v0a_hand_adapter.py`; four declared fixtures and three test suites; existing `holdem_cards.py`, `immutable_blueprint.py`, blueprint codec, `v0a/{model,runtime,replay,trace}.py`, and the sealed rehearsal driver; plus the six registration files. The affected execution paths are decode/adaptation, source preflight/import binding, host construction and single invocation, trace publication/readback, independent replay and expectation projection, final source revalidation, stdout/exit refusal, and repository boundary/inventory/profile/CI enforcement.

The deferred coverage claim’s SHA-256 recomputes to `051adc62d56fd25a3795a0b76b257abfd2ba1f11a5031fd25025d7d78a356e3d`. Its discovery, affected identity operations, archive/normalization exclusions, public-CLI controls, limits, and falsifier cover the independently identified C1 category. Its narrower statement that no schema, host, policy, or trace change belongs to this FIX is accurate. Future implementation controls remain prescribed and unexecuted.

## Base-contract compatibility

The design matches the actual sealed interfaces:

- `Fixture.deal()` maps each original `cdhs` suit through `suit_mapping(permutation_for_label(seed_label))`. Applying its inverse to file literals before constructing the fixture therefore yields the original literal cards. The required complete-deal comparison, including unordered private pairs and ordered board cards, detects an incorrect inversion.
- `ReplayHost` retains the fixture and complete deal, while `HandRuntime` receives the immutable blueprint only. Host events disclose only the controlled private pair and street-by-street public reveals. `BlueprintDecisionKey.from_state()` accepts only `OneSeatCardState`, public betting state, and the exact legal decision.
- The existing blueprint codec admits complete non-executable keys and actions. Raw artifact SHA-256, decoded blueprint digest, and trace-bound blueprint identity remain distinct.
- `verify_successful_trace()` reparses persisted bytes, reconstructs its own betting/card state, performs blueprint lookup independently, checks the complete fixture schedule, and judges pots, payouts, and final stacks through the chip-depth oracle. The proposed additional persisted decision projection closes the declared action/reason expectation.
- `VerifiedTrace` exposes accepted payouts, final stacks, pots, semantic digest, and run ID; parsed and independently verified decision rows can supply actions and hit/fallback counts without trusting an unchecked host object.
- The raise-to-6 fold case is arithmetically consistent: the unmatched four chips are returned, leaving a five-chip pot and seat 3 at 203. The showdown case likewise yields a 12-chip pot, seat 0’s three kings, and final stacks `(210,198,198,198,198,198)`.

The refusal sequence is properly ordered. Inputs and source are admitted before host construction; the host runs exactly once; persisted bytes must equal both returned bytes and receipt hash; independent replay and scenario expectations follow; source revalidation precedes stdout. Any late failure retains the trace or prefix and cannot issue success.

## Registration scope and proportionality

All six proposed registration files are genuinely implicated:

1. The boundary checker must classify the two new package files and tool, add the exact host-side imports, permit only the adapter’s incoming blueprint/scenario edges, and preserve v0a complete-deal and SCC restrictions.
2. The inventory generator needs the three test registrations.
3. Its inventory/profile test mirrors those registrations and derived census expectations.
4. Inventory JSON is generated output.
5. Profiles TOML is generated output and must retain zero capability binding.
6. CI needs direct floor-job CPU steps for the three suites.

This is proportionate to the existing hard-gate structure. The source-opening proposal forbids analyzer inference changes, extra origins, weakened old assertions, unrelated census drift, capability grants, and CI demotion. A new boundary suite can exercise the changed checker without editing the sealed existing boundary tests.

Observation only: the 500-production-line and 400-test-line budgets are tight for raw Git preflight plus the adversarial CLI matrix. The explicit stop rule correctly requires reassessment rather than omitted controls or compressed scope.

## Independently recomputed identity and hygiene

Raw-object mode reproduced:

- Ref: `refs/heads/review/v0a-hand-adapter-design/r003` → candidate commit.
- Commit rehash: `02e24f143b8df4b2f03e8a94c58ab57905a8b2b6`.
- Parent and merge base: `7a387e995e3b37232d2379332927247a4d49c64e`.
- Tree: `bd1cd2f83612aacac9d1de1c8e0afd673a86579c`.
- Scope: exactly three regular `100644` additions, with rename detection unnecessary.
- `brief.md`: SHA-256 `f33da4160da7aa8b7caa8c99b15ff9456b257e970eb0c99efd349fc817ff06b9`.
- `design.md`: SHA-256 `fbe4d15e03ae06567a4a0a795e23976fa29aa48f50da024c36f5beccb175e63a`.
- `source-opening-draft.md`: SHA-256 `4e62f00b05c3401905d04d57e04db27fb1ea5f5a28286f3bd979736970ac41da`.
- Whole-row byte sorting, two spaces, POSIX paths, and LF rows reproduce the supplied manifest exactly.

For each document, the r002 blob equals the r003 blob plus exactly one additional terminal LF: sizes changed `4820→4819`, `19701→19700`, and `6417→6416`. No wording, path, or other byte changed. The r003 blobs remain UTF-8, BOM-free, LF-only, terminal-LF-terminated, without trailing whitespace; maximum line lengths are 85, 94, and 84. `diff-tree --check` is clean.

All six raw base blob pins reproduce exactly:

- `ccf41b8e145d4463b6dd13aa224df54440d87c4d`
- `7f7f9cf16553bcc36f2e5015c782bb203baebd68`
- `75fdc9bf532958bf5d0300488dc828a5d3a1d66a`
- `e36ac6213decc0e3dc9cc9f38559fcf9fa5bed6c`
- `685a65c9cd8c0a8c7a347c94832cbc0370a6fd1a`
- `1c5278605fdfde8c75a2b31ea4a06251ca88c975`

The object repository’s HEAD remains at the base; no replacement refs exist. Mutable untracked copies of the r001 and r002 document sets are present but were not reviewed or used for identity.

## Limits

This was a read-only design/source-opening review. I inspected the three frozen blobs, governing contracts, prior permitted C1 report, deferred claim, actual source interfaces, registration machinery, and directly relevant test contracts. I did not import project code, run tests or hands, invoke owners, modify files/index/HEAD/refs, inspect sibling reports or controller transcripts, install dependencies, use the network, or claim implementation, source-seal, runtime, or adoption acceptance.