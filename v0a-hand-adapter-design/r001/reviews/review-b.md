Reviewer B — v0a-hand-adapter-design/r001 — commit 21474e3d5b105c1709205df1eb5543417abb5a0a — manifest ce327c6982338c148d26d4d73cad978ad05b49596520449337d2cc9cb9be0bc9 — FAIL: Spec FAIL; Quality FAIL; C/I/M 1/0/0; unresolved correction; Design SOUND.

## Required finding

**C1 — Git replacement objects can falsify the reported source commit and blob identities.**

The design requires the Git child environment to scrub all `GIT_*` variables, then resolves HEAD and reads inventories/blobs from that commit. It does not require `GIT_NO_REPLACE_OBJECTS=1`, Git’s `--no-replace-objects` option, or an equivalent raw-object operation.

Concrete failure scenario: let HEAD resolve to commit `O`, while `refs/replace/O` names commit `R` whose tree contains modified `tools/v0a_hand_adapter.py` or `pontius.hand_scenario` bytes. Materialize the checkout from `R`. `git rev-parse HEAD` still reports `O`, while ordinary `cat-file`, `ls-tree`, archive, and revision-path reads of `O` can transparently use `R`. The checkout therefore agrees with the substituted Git view, the altered adapter executes, and the trace/summary reports `source_commit=O`. This contradicts the design’s claims that identity comes from the actual resolved commit, that the new source equals that commit’s raw blobs, and that revalidation prevents source drift. Scrubbing `GIT_NO_REPLACE_OBJECTS` if the caller supplied it makes the failure more direct.

This is Critical because source identity is a Tier-C protected invariant and the failure can admit different executable bytes under an asserted 40-hex commit, not merely reject a valid checkout. The current review repository has no replacement refs, so the frozen proposal’s own identity is unaffected; the defect is in the prospective mechanism.

Required correction:

- Every initial and final Git identity/object operation must explicitly bypass replacement objects, either with `--no-replace-objects` in the Git command or by restoring exact `GIT_NO_REPLACE_OBJECTS=1` after the environment scrub. This must cover HEAD resolution, commit/tree inspection, base comparisons, inventories, and blob reads.
- A disposable-repository public-CLI control must create a replacement commit with changed adapter or scenario-code bytes while HEAD retains the original object name and the checkout matches the replacement. The adapter must refuse before host construction, trace creation, or success output.
- Revalidation must use the same raw-object mode.

Using both the command option and a controlled Git environment would be reasonable implementation advice, but only the raw-object outcome and public-boundary refusal are required.

## Design and contract assessment

**Design SOUND.** The defect is localized to source preflight and does not require changing the decoder/host/reader architecture. The overall dependency direction is appropriate:

- The scenario codec remains a host-side value adapter.
- Literal suits are correctly inverted before `Fixture.deal`; the subsequent complete-deal comparison catches an incorrect transform.
- Only the controlled private cards and revealed board reach immutable blueprint lookup.
- Raw scenario and artifact identities remain distinct from the decoded blueprint digest.
- Host receipt, persisted-byte equality/hash, independent legal replay, declared action comparison, source revalidation, and final stdout form a proper conjunctive acceptance path.
- Post-publication failures retain the trace and cannot be converted into success.
- The base verifier exposes verified payouts, final stacks, pots, semantic identity, and run ID; validated parsed decisions provide the promised action/hit/fallback projection without relying on an unchecked host object.

The proposed registration surface is compatible with the actual boundary checker. The two new package origins and one tool can be classified narrowly; exact direct-import checks can admit the host-side scenario edge and the adapter’s blueprint/replay/trace edges while preserving legacy edges, SCC checks, complete-deal restrictions, and the old driver exception. The three inventory registrations remain zero-grant mechanical changes under ADR-0486. The six registration files are therefore proportionate to the actual hard gates and generated census machinery.

Observation: the 500-production-line and 400-test-line limits are tight for the required source preflight and adversarial CLI matrix. The written stop rule correctly requires reassessment rather than compressed or omitted controls if those limits cannot be met.

## Independently recomputed identity

Raw candidate commit content re-hashed to `21474e3d5b105c1709205df1eb5543417abb5a0a`.

- Parent: `7a387e995e3b37232d2379332927247a4d49c64e`
- Tree: `be02e38610dee1a819a7686f044aee56899ba785`
- Scope: exactly three additions, with no rename detection:
  - `brief.md`: raw SHA-256 `042a2f345ae3bc6d979ef43c738be4656a9b9a7afcd49625589b48b5d04c1a9d`
  - `design.md`: raw SHA-256 `917c112d49daf461b477b5c066e1e6799b697af24e7e5ed1489089fd7d5178e6`
  - `source-opening-draft.md`: raw SHA-256 `4e62f00b05c3401905d04d57e04db27fb1ea5f5a28286f3bd979736970ac41da`
- Whole-row byte sorting with two spaces and LF recomputes manifest `ce327c6982338c148d26d4d73cad978ad05b49596520449337d2cc9cb9be0bc9`.

All six proposed base registration pins reproduce exactly:

- `ccf41b8e145d4463b6dd13aa224df54440d87c4d` — boundary checker
- `7f7f9cf16553bcc36f2e5015c782bb203baebd68` — inventory generator
- `75fdc9bf532958bf5d0300488dc828a5d3a1d66a` — inventory/profile tests
- `e36ac6213decc0e3dc9cc9f38559fcf9fa5bed6c` — inventory JSON
- `685a65c9cd8c0a8c7a347c94832cbc0370a6fd1a` — profiles TOML
- `1c5278605fdfde8c75a2b31ea4a06251ca88c975` — CI workflow

Frozen-document hygiene passes: regular `100644` blobs, UTF-8 without BOM, LF-only with final LF, no trailing whitespace, and no line over 100 columns. Raw connectivity checks passed and the candidate ref resolves correctly. The object repository’s HEAD remains at the base and has untracked working copies of exactly the three documents; those mutable copies were not reviewed.

## Limits

This was a read-only design/source-opening review. I inspected the three frozen blobs, governing base contracts, actual runtime/replay/trace/codec/card sources, registration files, and directly relevant tests. I did not import project code, execute tests or hands, invoke owners, modify files/refs/index/HEAD, inspect sibling reports or controller transcripts, install anything, or use the network. No implementation or runtime acceptance is claimed.