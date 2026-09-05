# Reviewer B: independent whole-candidate Tier C technical review

Spec FAIL. Quality FAIL. C/I/M 0/2/0. Verdict: REQUIRED CORRECTIONS.
Design verdict: SOUND. The small, explicit byte adapter and shared admission traversal fit the
adopted contract. The findings are bounded omissions in refusal handling and exact origin
classification; neither requires a new serializer, runtime changes, or analyzer redesign.

Issuer: independent Codex reviewer B, 2026-09-05. Review kind: NEW-SURFACE, whole candidate.
Commit: `6fb7f840d31d946e6b5dcb45faf82939dafd46ec`.
Base: `c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`.
Tree: `6f8e17c12da42ad901c90bc764fc39958cca5854`.
Manifest: `26b8fb178aecaf3dccf038ee2e108dc4ce913f7f07baff10cff5efbe11011aee`.

## Required findings

### B01 — Important: malformed exact records escape the common typed refusal

High confidence; reproduced on CPython 3.11.15 and 3.14.6 at the minimum decimal limit.
Locations: `codec.py` record-field access in `_admit`, `_key`, and `_action`, and the exception
translation at `encode_blueprint` lines 270–280.

Concrete input: `encode_blueprint(object.__new__(ImmutableBlueprintActionSource))` raises
`AttributeError` for missing `source_id`, rather than `BlueprintArtifactError`. A complete exact
source whose entries contain an uninitialized exact `BlueprintActionEntry`, an entry containing
an uninitialized exact `BlueprintDecisionKey`, and an entry containing an uninitialized exact
`BettingAction` produce the same escape at `key`, `street`, and `kind`, respectively. All four
were independently executed against the frozen codec. These are malformed exact value graphs,
not subclasses or hostile monkey-patching of installed modules.

The adopted Boundary and public API contract requires a common typed refusal for the fixed exact
graph; acceptance item 6 explicitly includes malformed exact graphs. A caller catching the
documented admission error instead receives an unexpected exception and cannot handle rejection
uniformly. No partial bytes are produced, so this is an error-contract failure, not silent policy
acceptance. Current malformed-graph tests populate every slot and therefore miss this category.

Required outcome: absent required fields at every admitted record level must become a useful
`BlueprintArtifactError` without traversing foreign objects or invoking formatting hooks.
Required verification: public encoder negatives for missing fields on source, entry, key and
action, including a valid entry before an incomplete entry; retain existing foreign-hook and
numeric-before-formatting controls. Do not broaden to catching `BaseException` or resource errors.
Advisory implementation choice: translate missing-field access at the admission boundary or
validate required exact-record slots explicitly. The concrete technique is not a new gate.

Evidence: `review-b-falsifiers-v2-311.json` and `review-b-falsifiers-native2-314.json` under the
task's `run-records/`; both probe processes exit 0 after recording four expected-contract failures.
The exit means the diagnostic completed, not that the codec contract passed.

### B02 — Important: undeclared flat module is admitted as the new family

High confidence from source analysis and an independently executed source-map falsifier.
Locations: `tools/check_stabilization_boundaries.py`, `enforce_legacy_edges` new family exemption
and `enforce_origin_classification` lines 213–233.

Concrete state: add a regular, import-free `src/pontius/blueprint_artifact.py` alongside the two
declared package files. The new origin predicate checks only the slash-terminated directory
prefix, so this path is never compared with `BLUEPRINT_ARTIFACT_ORIGIN_PATHS`. The legacy graph
rule explicitly classifies module `pontius.blueprint_artifact` as permitted. The baseline scanner
names the package initializer `pontius.blueprint_artifact.__init__`, so it does not reject the flat
module as a duplicate. An import-free file also passes all import/SCC rules.

The independent probe supplied exactly that additional path in memory and called the same seven
content predicates used by `check_repository`, with the real frozen source/tool bytes and parsed,
authenticated baseline. All seven accepted. The paired in-package `blueprint_artifact/extra.py`
negative was refused. No source file was written. This is direct evidence for the content-rule
hole; a filesystem mutation through the complete public gate was deliberately not executed in
this read-only review. The remaining public-gate checks validate regular file identity and
snapshot stability and contain no additional allowed-origin predicate.

ADR-0490 and the adopted exact registration exception authorize only the inert initializer and
codec, require other origins in the family to be rejected, and prohibit opening new flat source.
The wrong outcome is a CLEAN boundary result for an undeclared additional source origin. This
does not claim that the current candidate already contains the extra file or that any capability
has been granted.

Required outcome: reject the flat family module as well as undeclared package descendants while
retaining the two exact accepted paths. Required verification: add the flat-file negative through
the real public gate in a disposable snapshot, retain the accepted package, undeclared descendant,
forbidden-import, legacy-import and exact driver-origin controls. Advisory implementation choice:
match the explicit flat-path handling already present for `src/pontius/v0a.py`.

Evidence: `run-records/review-b-boundary-falsifier-311.json`, exit 0; diagnostic output explicitly
states acceptance by all seven content predicates and paired sibling refusal.

## Requirement-to-evidence assessment

| Requirement | Evidence and result |
| --- | --- |
| Frozen identity and scope | Independently read all 12 changed Git blobs, checked each packet copy, rebuilt digest-first LF manifest rows, matched manifest bytes/digest and tree. Six registration base blob pins match the adopted proposal; both exact amendment SHA-256 values match. PASS. |
| Fixed API, inert package and imports | Two public byte operations and typed error; initializer is a docstring. Codec directly imports only `__future__`, `json` and the two authorized value modules. Frozen diff contains no runtime, driver, analyzer inference, dependency, or legacy module edit. PASS. |
| Complete key/action schema | Read all codec and test bytes against the adopted 17-field key, action, root and entry schemas. Closed objects, tuple/list distinction, enum conversion, card/state shape, history widths/nullability and delegated action-record semantics are present. No second poker reachability validator. PASS for populated graphs; B01 covers absent fields. |
| Independent full-key and byte oracle | Primary literal raise fixture is compared with separately constructed complete expected values and independently authored canonical bytes. Reviewer additionally constructed the entire postflop history key, including every eight-field row and action, and verified equality on both slots. PASS for these controls; not exhaustive proof of all reachable keys. |
| Determinism and identity | Full canonical key bytes sort entries; compact sorted ASCII JSON plus one LF; unchanged source digest format. Candidate controls cover entry permutation, empty policy, raw file bytes, and round trip. Source reading confirms every field is emitted. PASS. |
| Real runtime hit/miss/illegal hit | Candidate directly dispatches `HandStartedEvent` through `HandRuntime`, checks table-hit raise-to-6 and one delivery, nonmatching passive call, and illegal raise-to-1000 with INVALID_BLUEPRINT_ENTRY/no delivery. Fresh frozen suite receipts: seven tests PASS in both slots, normal and min640. PASS. |
| Complete hand and independent reader | Real `ReplayHost.run`, five prescribed opponent folds, one controlled delivery, five-chip payout, and independently stated final stacks; `verify_successful_trace` receives separately constructed expected policy. No helper replaces the runtime/reader. Fresh frozen suite covers actual execution. PASS. |
| Numeric and Unicode closure | Exact scalar checks precede construction/hash formatting; token hook rejects more than 640 digits. Fresh suite covers max/overflow, source surrogates, escaped astral pair and above-former-one-MiB ID. Reviewer checks seven scalar/vector chip families at max/overflow through public encode/decode/digest on both slots at min640. PASS for checked cases; no capacity guarantee. |
| Bad input, duplicate and partial admission | Candidate controls cover malformed UTF-8, trailing data, nesting, duplicate names at root/key/action, duplicate semantic private-card aliases, good-first/bad-second input, scalar and tuple failures. Shared closed-schema/type predicates also inspected. Decoder constructs only after all entry validation. Encoder malformed absent slots FAIL B01. |
| Exact source boundary | Existing real public-gate controls and receipts pass for current package, driver, forbidden imports and in-package siblings. Flat family origin content checks FAIL B02. |
| Precise driver extension | Diff adds exactly existing driver origin and three origin-specific internal edges. Driver and its existing behavioral tests are unchanged. No driver CI step. PASS. |
| Inventory/profile registration and zero grants | Parsed generated JSON/TOML against base blobs: all 2,828 old inventory rows unchanged, exactly 23 new rows (7 codec, 4 boundary, 12 driver); all old payloads/settings preserved, three added payloads and current-profile memberships, zero capability-binding digests. PASS. |
| Census and unchanged writer | Manual diff confines generator change to three registrations. Permitted diagnostic shows nine new driver helper sites, 18 blockers and base decoy fingerprint reproduced by source-coordinate substitution. Final focused census and writer --check receipts have zero exits on both slots. These establish registration, not parked analyzer soundness. PASS within that limited claim. |
| Budgets and hygiene | Independently measured 281 source lines, 299 new test lines, 1,699 fixture bytes, 96 manual added+removed registration lines. Frozen diff --check passes; new Python files are LF and at most 99 columns. Fixture canonical JSON intentionally has a long single line. PASS. |

## Fresh checks, receipts and limitations

I used the code-verification skill to separate specification, quality, independent invariants and
execution evidence. Read-only source and registration analysis preceded targeted falsifiers.
No implementation narrative outside the four permitted evidence sections, reviewer reports,
implementation chats, or controller ledger was read. No subagent, source/index/ref change, fix,
commit, push, cleanup, dependency installation, operating run or broad acceptance run occurred.

Every probe used the inspected `run-snapshot.ps1`, explicitly overlaid `packets/r001/files`, ran
with `-B -P`, scrubbed environment, absolute `PONTIUS_GIT`, snapshot cwd/src and exact slot identity.
The codec probe separately checked its resolved module path and raw blob hash before use.

Executed commands were helper invocations with `-PythonArgs` pointing to this review's `probe.py`
or `boundary_probe.py` and these run parameters:

| RunName / slot | Extra startup setting | Outcome |
| --- | --- | --- |
| review-b-falsifiers / 311 | MinimumDigits | Exit 1 in reviewer structural comparison: current profile's nested membership list was handled as an unchanged whole object. Identity/inventory checks passed before this probe defect; codec was not reached. |
| review-b-falsifiers-v2 / 311 | MinimumDigits | Exit 0. All identity/registration and targeted positive checks pass; four missing-slot refusal failures observed. |
| review-b-falsifiers-v2 / 314 | MinimumDigits | Identity launch exit 101: native interpreter access denied by sandbox before payload. Retained. |
| review-b-falsifiers-native / 314 | MinimumDigits, native escalation | Identity succeeds; probe exit 1 at read-only authoring Git invocation (exit 128). Codec not reached. |
| review-b-falsifiers-native2 / 314 | MinimumDigits, native escalation | Exit 0 after exact per-command Git safe.directory selection; same four missing-slot failures and all positive/identity/registration checks reproduced. No Git configuration mutation. |
| review-b-boundary-falsifier / 311 | Normal | Exit 0; undeclared flat path accepted by content rules, in-package sibling rejected. |

The retained final `probe.py` differs from the successful floor probe only by the exact per-command
Git safe.directory option needed for the native account; codec checks were unchanged. The first
probe's nested-profile comparison was corrected before either successful codec probe.

Probe SHA-256 values:

- `probe.py`: `b7def7d80c9310b0ad07233d55b58b3d72f9eb725bb25a894dab0fcd8b21a0c5`.
- `boundary_probe.py`: `3c6119de453c46e29fe66e71a164d4d791e2dc7f3c76292b51af146d28f8fb72`.

Key receipt SHA-256 values:

- `review-b-falsifiers-v2-311.json`: `8b8a3e48e00894571dc9be861e94909770a931a521449f884165807ad0dc58d8`.
- `review-b-falsifiers-native2-314.json`: `e74d1e82af2bd22da37260c6ffe30e1fd1b67a2135897571feb8b07b7acf549b`.
- `review-b-boundary-falsifier-311.json`: `6b13b477475d93475e900948ddbb6aa149209644180a911d4e36b03424bc214a`.

Additionally inspected raw receipts: `frozen-codec-{normal,min}-{311,314}.json` (each 7 PASS),
`boundary-shape-fix-floor-r001-311.json` and `boundary-shape-final-native-r001-314.json` (each
4 PASS), `registration-stable-final-{floor-r001-311,native-r001-314}.json` (zero exits), and
`inventory-focused-{floor-r002-311,native-r001-314}.json` (each 2 PASS). The older fingerprint
attribution diagnostic exits 1 on then-unupdated coordinates; its printed base/candidate/hybrid
fingerprints and nine helper rows are diagnostic evidence, not a passing suite claim.

Coverage is finite: no all-input formal proof, arbitrary resource guarantee, boundary race claim,
policy strength, analyzer soundness, source-seal, publication, or operating authority follows.
Broad acceptance is intentionally pending both CLEAN reviews and cannot proceed on this verdict.
