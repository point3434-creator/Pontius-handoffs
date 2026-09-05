Codex, fresh independent Tier A reviewer — v0a-hand-adapter-open/r001 — commit 36c31477d87028aeec31339d28ccc089ffcaa31d — manifest 83814f33a6f7f64b99da7bedfaaa81e61712c083d8f0ecf55a79f0f9a22f142c — Spec PASS; Quality PASS; C/I/M 0/0/0; CLEAN; Design SOUND.

## Findings

No Critical, Important, or Minor findings. No required correction remains.

The candidate faithfully incorporates the accepted r003 design under ADR-0490’s Tier A precedent. It does not introduce a substantive design change, expand implementation scope, transfer acceptance, or grant operating authority.

## Raw identity and scope

Using raw Git objects with `--no-replace-objects`:

- Candidate commit rehashes to `36c31477d87028aeec31339d28ccc089ffcaa31d`.
- Its sole parent is the specified base,
  `7a387e995e3b37232d2379332927247a4d49c64e`.
- Its tree rehashes to `67d0e61c2cce8cba2c6e2ff759c24f432d50ac04`.
- `refs/heads/review/v0a-hand-adapter-open/r001` resolves to the candidate.
- No replacement refs are present.
- The delta is exactly five regular `100644` paths: one modification and four additions.

Raw file SHA-256 identities are:

- `STATUS.md`:
  `2d6d89f27c70b1062a28e6a5df44774b07ff99be4e1dc9870492440ebe995ad3`
- `docs/architecture/v0a-hand-adapter-r002/brief.md`:
  `f33da4160da7aa8b7caa8c99b15ff9456b257e970eb0c99efd349fc817ff06b9`
- `docs/architecture/v0a-hand-adapter-r002/design.md`:
  `fbe4d15e03ae06567a4a0a795e23976fa29aa48f50da024c36f5beccb175e63a`
- `docs/architecture/v0a-hand-adapter-r002/source-opening-draft.md`:
  `4e62f00b05c3401905d04d57e04db27fb1ea5f5a28286f3bd979736970ac41da`
- `docs/decisions/ADR-0493-open-the-one-hand-file-adapter-source-round.md`:
  `ed3aae9437c5402ceaba14ccac71228a5051d634e8ea4205dcb271a0c15709bd`

Digest-first whole-row sorting, two spaces, POSIX paths and LF row terminators reproduce manifest SHA-256
`83814f33a6f7f64b99da7bedfaaa81e61712c083d8f0ecf55a79f0f9a22f142c`
exactly.

## Accepted-design incorporation

The anchor commit independently rehashes to
`02e24f143b8df4b2f03e8a94c58ab57905a8b2b6`, with the same sole parent as this candidate, tree
`bd1cd2f83612aacac9d1de1c8e0afd673a86579c`, and reconstructed manifest
`f730799182d3f3eda2d9efa273048b2eaf28ceeb4274ea7525df95426ca679b1`.

All three candidate design-document blobs have the same Git blob IDs and raw bytes as that anchor. The r002 document path and edition names are retained deliberately while r003 remains the reviewed snapshot identity.

The two permitted original review reports hash exactly as ADR-0493 states:

- Review A:
  `ed499e3b4764aa1f8d7afe4a206f965f8f870cc67e409aae50c45c3e1f5e5765`
- Review B:
  `0320d1f877a0567013bd0c9a992be68bcc5a300c505d8b114cb99d3694190e99`

Both bind the exact anchor commit and manifest and report CLEAN, Spec PASS, Quality PASS, C/I/M 0/0/0, Design SOUND. In particular, both accept the corrected design-level requirement that every initial and final Git identity/object operation use raw object mode, including the prospective real-CLI replacement-commit and replacement-blob refusal controls.

ADR-0493 preserves the reviewed contract:

- Exactly three production paths, three test suites and four JSON fixtures are opened prospectively.
- The six registration exceptions remain confined to their stated registration, generated-data and direct-CPU-CI deltas.
- The 500-production-line, 400-test-line, four-fixture/16-KiB and 100-manual-registration-line budgets are unchanged.
- One initial implementation round and at most one bounded correction remain the stop rule.
- The complete acceptance map remains binding, including all 24 literal-card permutations, independently declared action and settlement expectations, real loaded-policy hands, persisted-byte verification, raw source identity and replacement-object controls, strict input admission, failure retention and the real repository boundary gate.
- Floor-first verification remains CPython 3.11.15 followed by 3.14.6, with the reviewed post-CLEAN direct CPU population.
- Sealed runtime, blueprint codec, immutable blueprint, driver, existing tests outside registration scope and historical evidence remain outside the opening.

All six prospective base pins reproduce at the current base:

- `ccf41b8e145d4463b6dd13aa224df54440d87c4d`
- `7f7f9cf16553bcc36f2e5015c782bb203baebd68`
- `75fdc9bf532958bf5d0300488dc828a5d3a1d66a`
- `e36ac6213decc0e3dc9cc9f38559fcf9fa5bed6c`
- `685a65c9cd8c0a8c7a347c94832cbc0370a6fd1a`
- `1c5278605fdfde8c75a2b31ea4a06251ca88c975`

ADR-0486’s zero-grant disposition is preserved: registration does not establish analyzer soundness or capability approval. Analyzer repair, Gate 13, H32, campaign and compiled work remain parked.

## Authority and STATUS

No additional authority is created by this review candidate. ADR-0493 says its decision takes effect only at a separately authorized adoption commit; the frozen review commit, copied proposals and generated STATUS do not activate implementation. `Invocation-Authority` remains `none`, source acceptance remains open, and operating, research and rehearsal execution remain closed.

STATUS accurately reflects ADR-0493’s front door:

- Research: ADR-0280
- Process/current decision: ADR-0493
- Runtime contract: ADR-0307
- Revoked: ADR-0281, ADR-0468, ADR-0472 and ADR-0475
- Active next: bounded adapter implementation, with no operating run
- Blockers: adapter source acceptance and operating/research gates remain open

The status generator and its test retain their base blobs
`ad661536f8a964fc7ac40f3e3791ff96fd8c1fc4`
and
`ef7fdd78bf6399085644eaad312dadfee52c1afe`.
The four supplied receipts record successful snapshot-local import preflights, `-B -P`, exact CPython 3.11.15 then 3.14.6, `STATUS.md is current`, and 12/12 status tests passing on each interpreter. The four corresponding snapshots are detached at the base and contain exactly the five candidate overlay paths; those paths, the unchanged generator and its test match their expected raw SHA-256 bytes.

## Hygiene and design assessment

All five candidate blobs are strict UTF-8, BOM-free, CR-free, trailing-whitespace-free and end in exactly one LF. The newly authored ADR and copied documents have maximum line lengths of 98, 85, 94 and 84 columns. STATUS retains the unchanged generator’s long ledger-row layout. `git diff --check` is clean.

Design SOUND. The metadata cleanly separates the adopted host-side value adapter and CLI boundary from sealed poker/runtime semantics, preserves the independently reviewed acceptance conjunction, and uses the established faithful-incorporation shape without laundering new scope or authority.

## Limits

This was a read-only Tier A metadata-incorporation review. I read the frozen candidate blobs, named base rules and directly relevant authority, the three r003 anchor blobs, the two permitted original design reviews, the four focused receipts and their corresponding snapshot bytes. I did not repeat the full Tier C design review, review implementation code, run project tests or hands, import project code, invoke an owner, inspect controller transcripts or unlisted reviews, modify files/index/HEAD/refs, install anything, use the network or spawn agents. The receipt assessment is limited to the fields recorded in those receipts and the presently available snapshot state. No adoption, source acceptance/seal, runtime result, implementation acceptance or invocation authority is claimed.