# Inventory 03 - finalization layer of export-run-20260910-r001

Reviewer: Claude, independent third pass, 2026-09-10. Drafter of the packet: Codex.
This is NOT a verdict-blind cold pass and is not described as one. The subject of this pass
is the packet's own review-and-disposition record, so review verdicts and findings were read
deliberately. Independence rests on carrying no prior context about this project and no
relationship to the authors of any file here.

Context probe: CONTEXT_PROBE_NONE. No memory index, memory file, conversation transcript or
summary of prior work appeared in the system prompt or in any system-reminder. The only
contextual material was a git-status block, the user's e-mail address, tool and skill
listings, MCP server notes and environment notes, all excluded by the stated rule.

Scratch (exclusive, all writes): `D:/Pontius/tmp/export-r001-final-review`.
Not opened: any `progress.md`, `D:/Pontius-handoffs/INDEX.md`, any memory index or memory
file, any conversation transcript, any unrelated scratch.
Execution discipline: no project invocation; no wrapper, check-script or `invoke.sh` run in
any mode, including `finalization-02/reconstructed-red-invoke.sh`; no solve, export or
agreement; no worktree mutation; no commit; no push. Git was used read-only
(`cat-file -t`, `rev-parse`). All re-derivations are plain CPython 3.14.6 stdlib
(`hashlib`, `json`, `pathlib`), plus `diff` and `sha256sum` for cross-checks.
Interpreter observed: `3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944]`.

---

## 1. Frozen manifest - recomputed, not accepted

- `manifest.sha256` hashes to
  `9965a225729a5896818127c013122f62fb3ae323889fde8ab16ea35e3e43eb17`.
- 4327 bytes, 47 rows, trailing LF present, no CRLF, already in whole-row byte-sorted order.
- All 47 member digests recomputed from current bytes: 0 mismatches, 0 missing.
- Excluded from the manifest: `handoff.md`, `candidate.json`, `manifest.sha256` - exactly
  the `manifest_rule` stated in `identity.json`.
- `1c7067448106cfa2aca3d57be879842d72293c61` is a real commit; `git rev-parse` on its tree
  gives `3d2fe79d2af20125e322dd4a668335e789810863`, equal to `identity.json.source_tree`.

## 2. Files in the packet but outside the frozen manifest (23)

Digests recomputed from current bytes. Paths under `finalization-02/` and `finalization/`
are shown relative to those directories.

Packet root:

```
5b8f500dd6cae70be85db3df8fd9e864565bc48444d51b43e3e433294462a4fa  authorization-template-02
0f6bb94c6cc3e3d719b4d970368ad9c15b0da8bc4f56113714d4b91fcaa8f37d  authorization-template.txt
b62a4348afe07231e2f955ddbfb4478bb1bc50c11fdef716bc91bd66823c1d0d  candidate.json
82eade57db087fd6b70d3a9f7e3b3564f440f9bce621d027c92533966649e93a  disposition-02.md
c86fcdc743468fac976e13b35014d979599f05cdc392d7b259c229f0e4434fcd  disposition.md
9d5f71ef45b8d170ce03aa38a8441a125146c295ad385591e17fc36f55417106  finalizer-addendum-02.md
db16f1eb25f714241a8d599c52a4eada28fe672f596158dfa83889858985e444  finalizer-addendum.md
7ddc69a044aa2344f5aef45411f0cc666a57c4c287c45e4a79d7d599ede49a18  handoff.md
9965a225729a5896818127c013122f62fb3ae323889fde8ab16ea35e3e43eb17  manifest.sha256
```

`checks/` and `reviews/`:

```
2aca0a33263630121239389899cd0aaedb75b277150091b851b20079801f5197  review-01-inventory.md
e62d1f04e0cf2834e608a04ef45473d65701ebeb109fedebc76f165479608875  review-02-inventory.md
bd28eadde16cd5d6f522351b9c4054e7e3f79db83cbb0ba87e0fa8e26f77cf2d  review-01-claude.md
125c4e18522067d355f5aa51e0ebc73d18ddb0ffdf2d3acca6d38ca6caeadddd  review-02-claude.md
e25d5619cf837a936b22ab3e7ad3d1e872cc7beac9c9495ecb23b1f7d4784e6b  review-02-dispatch-note
```

`finalization/` then `finalization-02/`:

```
923d2e96f6995b459211ab6aee006b985ab0d829126d249b96518f44d5db9ba7  evidence.json
963f75a82ffd588ffb2ff9bac2aa0bcef0c530c76d6a41408be6e36233d6fd34  manifest.sha256
a463c9b374da3587231f2a333a596575ab38ff452cb94680301f578b53cfd36c  preservation.json
8f2fc244df0f4b7bc357bf6c39570fb3232ea54a15fae79f4c6597e30bf09467  evidence.json
3cb08ed6f5ec20bf2ea9cc48fec4368f45c46bdc2b78834902598e668974f71c  manifest.sha256
84c63ebd76076dfdccc05694735db336e1ea54c445b9bdbaf8d32953dd44550f  preservation.json
ddb54461f1c1f6c19198255e61ac0958d280aa6c1b6fae0acc3860d2cd8e2a49  received-review.json
8edd61520f838de99afde315a19065e3e1c5e0d08c63fa9975673af97a3a43b6  reconstructed-red-invoke.sh
9ab1210130e8c2d25c729f379bd4f88034bbb92210d7935790a79611bac95dbc  red-to-frozen.diff
```

47 + 23 = 70 files; that is every regular file under the packet root.


## 3. Finalization layer 01 - internal consistency

`finalization/manifest.sha256` names 5 members. All 5 recomputed digests match:
`authorization-template.txt`, `disposition.md`, `finalizer-addendum.md`,
`finalization/evidence.json`, `finalization/preservation.json`. Rows are byte-sorted; the
manifest excludes itself.

`finalization/evidence.json` assertions, each recomputed:

- `original_manifest_sha256` = `9965a225...`, `original_member_count` 47 - both reproduce.
- `review_sha256` `bd28eadd...` = `reviews/review-01-claude.md`; `inventory_sha256`
  `2aca0a33...` = `checks/review-01-inventory.md`. Both match.
- `original_verdict` "NOT CLEAN", 0 Critical / 0 Important / 2 Minor - matches the literal
  header line of `reviews/review-01-claude.md:3`.
- `current_loser` `checks/race-caller-b.txt` `7978887c...` - matches; its single line is
  `PRECONDITION an invocation was already started (claim.d exists)`.
- `predecessor_loser` at `.../solve-run-20260910-r004/checks/race-caller-b.txt`
  `266af844...` - matches (280 bytes). Its text is `PRECONDITIONS ok ...`, then
  `mkdir: cannot create directory ... : File exists`, then the claim-refused message.
  The recorded refusal label "mkdir after PRECONDITIONS ok" is accurate.
- `claim_block`: slicing from `mkdir -p "$OUT"` up to (excluding) `START=$(now)` gives
  346 bytes and `dbcbcb73b3a5e9435acd36a3c67d0775764cb9891a9ce25ab9a5e4d59fe325d4` in
  BOTH `invoke.sh` and `inputs/solve-wrapper-r004.sh`. `byte_identical: true` is correct.

## 4. Finalization layer 02 - internal consistency

`finalization-02/manifest.sha256` names 10 members; all 10 recomputed digests match, rows
are byte-sorted, the manifest excludes itself. The 10 are the two review-02 artifacts, the
addendum, template, disposition, and the five other files in `finalization-02/`.

`finalization-02/evidence.json` assertions, each recomputed:

- `review_sha256` `125c4e18...` = `reviews/review-02-claude.md` (32228 bytes). Match.
- `inventory_sha256` `e62d1f04...` = `checks/review-02-inventory.md` (25533 bytes). Match.
  These are the same two digests the review's own header declares for its scratch outputs.
- `original_manifest_sha256` / `original_manifest_members` - reproduce (section 1).
- `red_expected_sha256` = `red_reconstructed_sha256` =
  `8edd61520f838de99afde315a19065e3e1c5e0d08c63fa9975673af97a3a43b6`, `red_bytes` 9447.
  The file on disk is 9447 bytes and hashes to exactly that. Match.
- `changed_source`, `changed_wrapper`, `changed_plan` all false - consistent with section 5.
- `current_corrections`: all 5 digests recomputed and matching.

`finalization-02/preservation.json` lists 59 pre-existing files. All 59 recomputed digests
match current bytes; 0 mismatches, 0 missing. The 59 are the 47 manifest members plus
`handoff.md`, `candidate.json`, `manifest.sha256`, `reviews/review-01-claude.md`,
`checks/review-01-inventory.md`, `reviews/review-02-dispatch-note-claude.md`,
`disposition.md`, `finalizer-addendum.md`, `authorization-template.txt` and the three
files of `finalization/`. `all_preexisting_bytes_preserved: true` is therefore true.

## 5. Reconstructed RED wrapper - derived independently

Slice definitions taken from `checks/focused-checks.py:53-55` and `:100`, replicated in my
own stdlib code; the script itself was never executed.

| Quantity | My computation |
|---|---|
| sha256(`finalization-02/reconstructed-red-invoke.sh`) | `8edd6152...` |
| `checks/red-before-guard.json`.`source_sha256` | `8edd6152...` - equal |
| Reconstruction guard slice | empty string, sha256 `e3b0c442...` |
| Receipt `slices_sha256.producer_guard` | `e3b0c442...` - equal, and equal to sha256("") |
| Reconstruction `exit_tail` slice | 259 chars, `b86dd771...` |
| Receipt `slices_sha256.exit_tail` | `b86dd771...` - equal |
| Frozen `invoke.sh` `exit_tail` slice | `b86dd771...` - identical to the reconstruction |
| Frozen `invoke.sh` guard slice | 161 chars, `95ac5b97...` |
| `checks/focused-checks.json` (GREEN) guard slice | `95ac5b97...` - equal |

Difference derived by me with `diff -u`, not read from the packet: `invoke.sh` minus
lines 44-47 (`TEACHER`, `TEACHER_SHA`, `PRODUCER`, `PRODUCER_SHA`) and minus lines 85-88
(the fenced producer-guard block) yields exactly the reconstruction, 10196 -> 9447 bytes.
My diff is textually identical to `finalization-02/red-to-frozen.diff` apart from the
`---`/`+++` header lines. Control computations:

```
remove guard block only        -> d4e4b50a66232cbd81bdb775a634be70e1f4c45238e2676a14d946c5fd5c90df
remove four constants only     -> 110d870f81c9c73d707a70a18b0a16a2f25cbea8bd807bc05af661f900f55971
remove both (reconstruction)   -> 8edd61520f838de99afde315a19065e3e1c5e0d08c63fa9975673af97a3a43b6
```

The `d4e4b50a...` value independently confirms the figure review 02 reported for a
guard-only deletion.

## 6. Review artifacts - labels as they stand

- `reviews/review-01-claude.md:3`: "Verdict: NOT CLEAN. Findings: 0 Critical, 0 Important,
  2 Minor." Findings M-01 (approval wording) and M-02 (race window).
- `reviews/review-02-claude.md:3-4`: "Verdict: CLEAN", specification / engineering /
  design judgments all SOUND. Findings M1, M2, M3, M4 (Minor) and A1 (Advisory).
- Both files hash to the values recorded in both finalization layers, so neither verdict
  label can have been rewritten, softened or replaced.
- `finalization-02/received-review.json` records verdict CLEAN, design SOUND, the reviewer's
  scratch paths, both digests, and all five findings with id, severity, title, location,
  requirement, scenario, falsifying observation, correction and confidence. Compared
  against the report text for all five: severities, ids, titles, locations and correction
  wording agree. No finding is omitted, renamed or re-graded.

## 7. Authority state, observed directly

- `.../export-run-20260910-r001/authorization.md` does not exist.
- `.../export-run-20260910-r001/invocations/` does not exist.
- Both authorization templates are labelled suggested wording only.
- `identity.json.status` still reads "prepared and rehearsed; awaiting Claude review and
  controller authorization; not invoked".

## 8. Supporting facts recomputed for the correction claims

- `checks/race-gate-controls.json`: 9 cases, 0 failures - the addendum's "nine race-gate
  controls" is accurate.
- `checks/focused-checks.json` (GREEN): 31 cases, 0 failures, `source_sha256` = frozen
  `invoke.sh`. `checks/red-before-guard.json` (RED): 31 cases, 3 failures, all three being
  `producer-*` mismatch/missing cases returning 0 where 80 was expected.
- `rehearsal/result.json` membership observation: `universe_count` 1081, `hits` 1081,
  `unsupported` 0, `disagreements` 0; all 1081 rows are `classification: hit`,
  `in_pool: true`, `provider_reason: blueprint_hit`. No `blueprint_default` row exists.
- `journal_attribution.py` contains exactly the four refusal branches the addendum names:
  `MISMATCH unparsable-row` (:37), `MISMATCH output-missing` (:44),
  `MISMATCH output-file-missing` (:48), `MISMATCH runtimes_sha256` (:57).
- `invoke.sh` line facts used later: `set -u -o pipefail` at :29; atomic claim at :109;
  claim record at :111-113; start record at :114-116; the launch line that expands
  `${SystemRoot:-$SYSTEMROOT}`, `$TEMP` and `$TMP` at :122. No guard on those three
  variables exists anywhere above :122.

This inventory was written and hashed before any judgement in review-03-claude.md was
formed. Nothing in it authorizes an invocation, publication, commit or push.
