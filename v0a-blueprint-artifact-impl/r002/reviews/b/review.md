# Independent Tier C FIX review B

Spec PASS. Quality PASS. C/I/M 0/0/0. Defect verdict: CLEAN.
Design verdict: SOUND. Explicit exact-graph admission shared by the two byte
operations fits this bounded adapter. The correction translates missing slots
at checked reads after exact-type admission and closes the omitted family path.
It does not add a serializer framework, duplicate poker validator or runtime
coupling. No remaining required correction or design finding was demonstrated.

Issuer: fresh independent Codex review B, 2026-09-05.
Task: v0a-blueprint-artifact-impl/r002, sole bounded FIX round.
Commit: `5e56e4454f7b8ccb360d3e36245abc33318349bb`.
Manifest SHA-256: `6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5`.
Base: `c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`.
Tree: `dc18ed133504fe6c7677b494bcefba311cc73704`.
Ref: `refs/heads/review/v0a-blueprint-artifact-impl/r002`.

## Independence and governing contract

I used the code-verification skill to separate specification, engineering
quality, independent invariants and executable evidence. I read the base
CLAUDE.md and workflow checklist/FIX/cold-input rules, ADR-0490 and all three
adopted architecture documents, then both exact controller extensions and the
frozen implementation/tests. I recorded `initial-inventory.md` before opening
the deferred r002 `coverage.md`. Only then did I read the permitted r001 reports
as binding correction requirements. I did not read current sibling reports,
implementation reports/transcripts or the controller ledger, or delegate work.

ADR-0490 activates the otherwise prospective design. The two extensions add
only the existing driver's exact origin/three edges and its unchanged test-suite
registration. No analyzer repair or capability grant follows. All task payloads
were launched by the inspected snapshot helper with the explicit r002 overlay.

## Closure of prior required findings

| Prior finding | Actual correction and verification | Result |
| --- | --- | --- |
| A Important 1 / B02: flat family module admitted | The origin predicate now explicitly rejects `src/pontius/blueprint_artifact.py`; the registered boundary test exercises the real public gate. My fresh probe called `check_repository` on the accepted frozen snapshot and on both flat-module and nested-package negatives on 3.11.15 and 3.14.6. Both negatives raised the expected unclassified-origin error. | Closed |
| B01: absent slots escape typed refusal | `_slot` translates only AttributeError from fixed record-field reads, after the record's exact type has been checked. Registered tests cover incomplete source, entry, key and action, including a valid first entry. My probe independently omitted each of all 22 slots across the four record classes; every public encode call raised BlueprintArtifactError on both slots. | Closed |
| A Important 2: durable independent acceptance missing | Frozen tests now compare the complete postflop/history graph with separately constructed expected values, assert all four artifact action labels, reject action-object missing/extra members, and exercise scalar/vector/history/action max and overflow through raw input and independently constructed exact graphs. The explicit lazy digest assertion traverses unchanged policy identity. Four permitted final codec receipts execute these exact frozen assertions on both interpreters, normal and min640. | Closed |

Both historical behavioral RED snapshots were independently checked: their codec
and checker raw bytes exactly match rejected r001. Their nonzero payload exits
show the AttributeError and absent public-gate refusal, respectively. The new
coverage-only assertions are not presented as defects that needed production
changes. The FIX changes exactly four files: codec.py, both new tests and the
boundary checker. No additional correction round or source edit was performed.

## Requirement and risk assessment

| Contract | Independent evidence and assessment |
| --- | --- |
| Frozen identity | Recomputed ref, parent, tree, all 12 Git-blob SHA-256 values, whole-row digest-first sorted LF manifest, packet manifest bytes and all 12 overlay copies. Both amendment pins and deferred claim pin match. PASS. |
| Exact graph and typed refusal | Source checks every fixed record before slot access and every nested scalar/tuple before constructors, equality, hash or serialization. Rebuilt key/action/source values use existing validators. All-slot probe, nested int/string/tuple subclasses with untouched hooks, and registered malformed/populated/foreign cases pass. No broad BaseException/resource catch. PASS. |
| Closed schema | Exact root/entry/key/action members, duplicate decoded object names, full 17-member key, array widths, exact integer/bool/null and labels, private-card canonicalization, ordered board/pending/history and delegated BettingActionRecord semantics were inspected against source. Registered corruption cases plus fresh escaped-name duplicate, BOM, malformed UTF-8 and trailing-data negatives pass. PASS within finite coverage. |
| Numeric closure | Registered independent scalar/vector/history/action controls and final four-slot receipts pass. My min640 probe additionally exercises 11 named numeric paths: big blind, last full raise, starting stacks, stacks, total/street contributions, acted-at-bet, history call chips, raise amount, raise chips and returned chips. Each accepts 10**640-1 through decode/digest/encode/decode and refuses 10**640 through raw tokens and exact-source encode. PASS. |
| Unicode and capacity domain | Source refuses surrogate code points symmetrically before hashing; parser handles escaped valid pairs. Registered tests cover high/low/Python-pair refusal and the above-former-one-MiB empty policy. Fresh checks compare escaped and literal astral/combining/precomposed/control-containing IDs and retain exact strings without normalization. PASS; no resource or capacity guarantee. |
| Full keys, canonical bytes and identity | Literal canonical raise fixture remains an independent byte oracle; full raise/history expected graphs are separate from the codec. Sorting uses full key canonical bytes, objects are sorted/compact ASCII JSON plus one LF, and existing source.digest is unchanged. Equivalent entry permutations, empty policy and temporary file bytes remain tested. PASS. |
| Actual runtime | Registered test dispatches the real HandRuntime: matching raise-to-6/TABLE_HIT and one mailbox delivery; nonmatching passive call and one delivery; raise-to-1000 gives INVALID_BLUEPRINT_ENTRY/NOT_ATTEMPTED and zero deliveries. Exact frozen final-codec receipts execute it successfully on both supported slots in both settings. PASS. |
| Full hand and independent reader | Registered ReplayHost control uses the declared five folds, one controlled action, five-chip payout and final stacks `(200,199,198,203,200,200)`. It requires passed receipt and invokes verify_successful_trace with separately constructed expected policy. The unchanged host/reader remain real production consumers. Same exact frozen receipts pass. PASS. |
| Source boundaries and driver amendment | Actual fresh gate accepts frozen source and refuses flat/nested extra origins; registered boundary receipts retain sibling, forbidden codec import, legacy ingress, driver sibling, extra driver edge and other-origin allowance negatives. Exact driver path and three targets remain conditional on that origin. Existing six-file v0a and runtime/driver/test behavior bytes are outside the diff. PASS. |
| Registration and budgets | Six authorized base blob pins match; generator changes only three path registrations. Independently parsed generated JSON/TOML: all 2,828 prior inventory rows unchanged, exact 7 codec + 4 boundary + 12 driver additions, old payloads/profiles/settings preserved apart from current membership, zero capability-binding/spec hashes. Final writer receipt uses all 12 frozen blobs. Source 290/300 lines; new tests 300/300; fixtures 1,699/8,192 bytes; manual registration added+removed 97/100. PASS. |
| Hygiene | Fresh frozen diff --check exits 0. New Python files are LF-only, BOM-free, no trailing whitespace, maximum width 99. Canonical JSON fixture is intentionally a single line. PASS. |

The independent initial inventory and deferred claim agree on the three
correction categories, but I challenged the claimed representatives using all
record slots, additional nullable/history/vector integer fields, nested foreign
types and a deeper package origin. These checks did not falsify the claim. The
claim explicitly excludes exhaustive scalar combinations, arbitrary object
mutation, resource safety and whole-hand reachability; I retain those limits.

The r001-to-r002 test diff preserves the hit/miss/illegal-hit delivery assertions,
replay settlement and independent reader, canonical fixture, empty/large policy,
foreign record hooks, schema corruptions and driver boundaries. Partial history
assertions were replaced by stronger full-graph equality. Permutation preparation
now uses independently built exact entries; public export permutation equality
remains asserted. Removed subTest wrappers affect failure localization, not the
required acceptance outcomes. No missing binding acceptance control was found.

## Fresh execution and receipt provenance

Reviewer-owned metadata commands (read-only; no task payload imports):

- `D:/Pontius-tools/py311/Scripts/python.exe -B -P .../reviews/b/metadata.py`
  exited 0: identity, scope, pins, budgets, preserved registrations, receipt
  exits and snapshot blob comparisons described above.
- `git diff --check <base> <candidate>` exited 0.
- `...python.exe -B -P .../reviews/b/provenance.py` final execution exited 0:
  r001 RED production identities, earlier receipt differences and hygiene.

Fresh behavioral command: `run-snapshot.ps1` with `-MinimumDigits`,
`-Overlay D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/packets/r002/files`
and `-PythonArgs D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/packets/r002/reviews/b/probe.py`.

| RunName / slot | Result |
| --- | --- |
| fix-review-b-targeted / 311 | Identity exit 0, payload exit 0. CPython 3.11.15, -B -P -X int_max_str_digits=640. All 12 snapshot blob identities checked before probe; 22 slot omissions, 11 numeric paths, nested hooks/parser/Unicode and three public-gate checks pass. 55 typed refusals observed. |
| fix-review-b-targeted / 314 | Interpreter identity launch exit 101, sandbox access denied before payload. Environment limitation, not candidate failure. Receipt retained. |
| fix-review-b-targeted-native / 314 | Authorized native launch: identity exit 0, payload exit 0. Exact CPython 3.14.6 and same flags/overlay/probe. Same complete targeted result. |

No broad suite or duplicate full codec/boundary population was rerun. The probe
checks its module path and all 12 frozen file hashes before behavior. Public gate
negative files were confined to disposable snapshots and restored/removed in
finally blocks. No primary or authoring payload execution occurred.

I inspected raw receipts, not filename-derived success claims:

- Four `correction-final-codec-*` receipts: seven tests each, exit 0, normal and
  min640 on both exact slots. Independently matched all 12 snapshot blobs to r002.
- Two `correction-boundary-green-*`: four tests each, exit 0. Both have 11/12
  matching blobs; the only differing file is the unexecuted main codec test.
- Two `correction-inventory-focused-*`: two registration/discovery tests each,
  exit 0; two `correction-registration-check-*`: writer --check exit 0.
  Each has the same sole differing main codec test file.
- `correction-registration-write-final-r001-311`: exit 0 and all 12 snapshot
  blobs exactly r002, including generated outputs.
- Two `correction-*-red-r001-311`: identity 0 / payload 1, with old production
  bytes independently matched to r001 as stated above.

Earlier 11/12 snapshots must not be called byte-identical r002 suites. My
comparison found helper/layout differences in the main codec test (import
wrapping, fixture assignment consolidation, DELETE sentinel to Ellipsis, and
StepClock initialization). Its entire BlueprintArtifactTests AST is identical
across all six earlier snapshots and frozen r002; the explicit digest assertion
is already present in those snapshots. This differs from a preliminary
description attributing the mismatch solely to adding that assertion. The final
four codec receipts and final writer receipt provide exact-frozen provenance.

An initial reviewer provenance check assumed that preliminary description and
failed its line-deletion comparison after the RED-production verification. I
inspected the actual diff and corrected the metadata check to compare the test
class AST and identify the sole differing path. This was a reviewer audit-script
assumption, not a failed candidate test. The behavioral probe did not change.
Authoring working bytes and correction-final2 receipts were not used as evidence.

## Evidence digests and remaining limits

Reviewer files:

- initial-inventory.md: `cc754c2bc476250a49616612c12071ed56df82685e8acd692130b57422add07d`.
- metadata.py: `db276454ac051e3e6417db08da856a388af428ece515b900625499fd7fa82d9d`.
- probe.py: `47d3a861cf41a31717c42ca310a4c76f4b25b716be6b2eb7bd1f42efe7714254`.
- provenance.py: `44c7784eab1c0f3809bb14292781992acb5762305f253e6cced6e09727f0cba5`.

Fresh receipts under task-root/run-records/:

- fix-review-b-targeted-311.json: `9fe1b89497a86ec8a2005d33dbbec1d186dfccd130ccbf715d0c357fe887f380`.
- fix-review-b-targeted-314.json: `4f43a7bad395c828d0195b51645ca52036ff84650ed2e21d9b0b0ed9215c10db`.
- fix-review-b-targeted-native-314.json: `2530d06fda76c02bbecb7db6f39428ca3bc37f74f7a2a9133dce4b7814ec99ac`.

This is bounded technical review of a local frozen, unadopted candidate. The broad
post-CLEAN union remains pending both reviewers; this report is not its result.
No operating/rehearsal/scientific run, owner, optional dependency installation,
network, publication, source seal, commit, push or analyzer-soundness claim is
included. Finite probes do not prove every reachable key, every malformed input,
filesystem races, hostile installed-module mutation, arbitrary resource bounds,
strategy strength or performance. All required prior findings are closed within
the adopted codec contract; none of these limits creates new operating authority.
