# Review 01 (Claude, cold, Tier C FIX): v0a-eval-panel-completion/r003

Candidate 7ca821802c949b047becf6599d603b3b63d51fa7 on
refs/heads/review/v0a-eval-panel-completion/r003, sole parent
430ad75de79cec13d66ff3dc4981dd3770a371b7, tree 3d2fe79d2af20125e322dd4a668335e789810863,
manifest 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd.
Findings bind to that commit/manifest pair.

Defect verdict: CLEAN. Design verdict: SOUND.

## 1. Identity (recomputed from Git objects, not from packet claims)

- ref -> commit: rev-parse of the review ref returns 7ca82180...; commit object has
  exactly one parent, 430ad75d..., tree 3d2fe79d... (matches candidate.json).
- Delta (diff-tree --no-renames parent..candidate): exactly two modified paths,
  src/pontius/eval_agreement.py and tests/test_eval_protocol.py. The dispatch prompt
  said "three changed blobs"; the handoff's "exact two-file delta" is what Git shows.
- Manifest: rows "<sha256>  <path>\n" over raw blobs, whole-row bytewise sort, LF
  after each row; recomputed bytes are identical to manifest.sha256 and its SHA-256
  is 1f48c97a...d57fd, equal to candidate.json and handoff.md.
- Parent anchor: recomputed three-row manifest at 430ad75d (eval_agreement.py,
  tests/cases.json, tests/test_eval_protocol.py) is byte-identical to
  inputs/parent-manifest.sha256; digest 6e36bb41...04cd5.
- Dependency pins: all 51 rows in inputs/dependencies.json verified by cat-file at
  the stated commit (D:/Pontius at b6f8b08f, beb84be5, 7ca82180; D:/Pontius-handoffs
  at 2943f935); packet copies under inputs/ match their pinned digests. The
  supporting-files list (32 entries), brief.md and coverage.md digests match
  handoff.md; coverage.md was hashed but not read until the inventory was written.
- RED anchor (from checks/red-receipt.json): commit 81a5aaf5... is a child of the
  parent whose only change is tests/test_eval_protocol.py at blob 5c53a450..., the
  same blob as the candidate's test file; its eval_agreement.py blob equals the
  parent's (8329de1e...). The focused receipt names the candidate commit itself.

## 2. Inventory reference

D:/Pontius/tmp/eval-completion-r003-review-01-5330cb47/inventory-01-claude.md
SHA-256 71c08a4d849c78d59032c51422fb6860cb448394a9bdccbd433a313a6e873fb3
(190 lines, LF, no BOM), written before coverage.md or any checks/ file was opened.

## 3. Standard applied

Host-equivalence of admission: every byte sequence the unchanged
tools/v0a_table_host.py would refuse (ChildConnection.read_stream lines 512-537,
WireConsumer.read 662-680, decode_json 52-90, plus the exact-member and closure
rules of WireConsumer) must be excluded by classify() before chip or hit credit.
A host-refused capture that keeps credit is Important regardless of whether the
credited action, chips or counts change. I compared every predicate byte level
first, then parsed level, for both protocol versions.

## 4. Byte-level comparison (host oracle vs frozen classifier)

| Host predicate (frozen location)                 | Classifier (frozen location)           |
|--------------------------------------------------|----------------------------------------|
| stdout capture <= 2097152 total, else truncated  | frames_for:185  0 < len <= 2097152     |
| (read_stream:513,523-527)                        |                                        |
| residual empty at EOF (read_stream:520)          | frames_for:186 endswith LF             |
| split on byte 0x0A only (read_stream:530-534)    | frames_for:187 raw.split(b'\n')[:-1]   |
| frame incl. LF <= 16384 (read_stream:532,535)    | decode_frame:122 0 < len <= 16384      |
| bytes, no 0x0D, no EF BB BF (decode_json:68-69)  | decode_frame:122-124                   |
| depth <= 8 outside strings, escapes (70-85)      | decode_frame:125-140 (same scan)       |
| strict UTF-8 + json.loads (86)                   | decode_frame:147                       |
| parse_int digits <= 640 signless (53-55)         | decode_frame:142-144                   |
| constants rejected (57-58,87)                    | reject_constant (parse_constant)       |
| duplicate keys rejected (60-65,88)               | unique_object (object_pairs_hook)      |
| floats accepted incl. non-finite (87)            | finite_float: stricter, refuses        |
| ValueError/TypeError/RecursionError -> refuse    | Unusable/ValueError; RecursionError    |
| (89-90)                                          | -> Unusable; classify catches 341      |
| EOF required after session_result (complete:912) | frames[-1] must be session_result      |

Every host refusal at this level maps to an exclusion. The one asymmetry is in the
allowed direction: a non-finite float (e.g. 1e9999) is refused by the classifier and
accepted by the host; brief.md keeps that restriction, and the adapter writes with
allow_nan=False, so no real capture is affected. Both the splitlines() normalization
and the unbounded parse of the parent are gone; frame decoding precedes every schema
check and no normalization survives.

Parsed level (frame members, enums, closure, ordering): WIRE_FIELDS and the v2 ready
extension are identical to the host's; type/enum rules for ready, action,
event_result, decision (v1 DecisionRecord path, v2 validate_decision path), timing,
preparation_use, hand_result and session_result match WireConsumer, with the one
deliberate exception the brief preserves (v1 selection_reason is any str; unknown
labels become disagreements). Ordering (action immediately before decided, no
duplicates, no unpaired action, contiguous event_index, count bound to replay) and
closure (complete, accounting, zero interruptions, rank_source, settlement replayed
through the kernel and compared as canonical JSON) match. Exception discipline:
every refusal on a reachable input surfaces as ValueError/TypeError/KeyError/
IndexError/binascii.Error (over-long action lists reach acting_seat None and fail
exact_integer before any kernel assertion). I found no successful-credit path from
missingness, defaults or failures in the changed or unchanged code.

## 5. Findings (severity-ordered)

### F-01 Minor: host `state_mismatch` predicates are agreement-only (v1) or absent (v2)

Location: src/pontius/eval_agreement.py classify():344-348 (chip credit) versus
359-369 (record/replay comparison, blueprint-v1 only); host authority
tools/v0a_table_host.py:770,815 (`state_mismatch`) and 832-843 (expected fields).
Requirement: accepted-design.md s5 ("Successful transport is taken only from retained
host envelopes"; record cross-checks are agreement predicates); brief.md O1 for byte
and protocol admission.
Scenario (reachable through the public classify boundary, both versions): take the
real check-control capture; change the river decision's state_before_sha256 to 64
zeros, or its blueprint_sha256 to another valid digest, or its action_index to 2.
Host: WireConsumer.decision refuses with state_mismatch, the hand fails, no
settlement. Classifier: frames_for admits (shape valid), replay settles, result is
chip_eligible=True, chips=-2, classification='disagreement' (v1) or 'unsupported'
(v2, where no record/replay comparison exists at all). No hit is possible on this
path (any mismatch appends a cause), so agreement counts are unaffected.
Falsifier: a host-refused record keeps chip credit, contradicting the strictest
reading of host equivalence at the chip gate.
Why Minor, not Important: the accepted design routes record-content anomalies to the
agreement layer with chips retained (s5, and the parent disposition's "reason-only"
and duplicate-record rulings); brief.md scopes this FIX to physical framing and
JSON/parser admission and preserves "existing decoded-record ... contracts at their
later stages"; the host itself codes this class as state_mismatch, distinct from
protocol_invalid. Changing it alters the settled chip contract for Slice B and
therefore needs a controller decision, not a silent r004 edit.
Smallest correction if host parity at the chip gate is wanted: inside the classify
try block, after replay(), require for every decision record (both protocols) that
event_index, action_index, street_action_index, seat, street, state_before_sha256,
state_after_sha256 and visible_cards_sha256 equal the replayed expected fields and
that blueprint_sha256 equals the artifact digest; keep the reason-label exception.
Existing tests only assert "not hit" for the tampered-hash case, so they survive.
Confidence: high on the mechanism; medium on severity (it is a design boundary).

### F-02 Advisory (design): the admission oracle is duplicated by construction

decode_frame reproduces decode_json and frames_for reproduces read_stream because
src/pontius must not import tools/ and the host is sealed. The parent defect was
exactly a divergence of such a copy. The candidate pins parity with
test_raw_decoder_matches_frozen_host_boundaries against the real host module and
with real-capture mutations through classify, so drift is caught at the listed
points only. Alternative: relocate the shared frame/JSON admission (constants
16384, 2097152, depth 8, digits 640, CR/BOM rule) into one src module the host also
imports. Cost: a host edit, i.e. a separate Tier C scope; not for this FIX.

### F-03 Advisory (coverage): limits of the new tests

1. capture_over_limit prepends 2097152 spaces, so the first frame also exceeds
   16384; the 2097152/2097153 boundary with valid frames is not isolated
   (coverage.md discloses this). The check at frames_for:185 is trivially readable.
2. host_accepts in test_eval_protocol.py:140-149 is a model of read_stream (LF split,
   per-frame decode_json), not the real reader; the model matches my reading of
   read_stream:512-535. The direct oracle test uses the real decode_json.
3. The RecursionError branch (decode_frame:150-151) is unreachable behind the depth
   guard; the 2000-deep case exercises the guard, not the handler. Harmless.
4. Refused variants assert `causes` non-empty but not the cause label, so the
   integer_over_limit case is refused for the digit reason only by construction
   (equal shifts keep elapsed_ns consistent). Acceptable.

### F-04 Advisory (limits): host predicates the classifier cannot mirror

ready.source_manifest_sha256 equality (not retained in the session envelope; shape
only, stated at eval_agreement.py:174); v2 config_sha256 is checked for shape and
cross-envelope equality, not recomputed via make_provider; session-id charset
regexes and hand.input_sha256 are session-level admissions; queue-depth and deadline
refusals are not byte-determined. stderr overflow is covered indirectly: the host
sets the same `truncated` flag for both streams (read_stream:526) and the classifier
requires capture_truncated is False (classify:334).

## 6. Design verdict: SOUND

The shape now matches the contract: one explicit raw-frame boundary with the host's
exact predicates, applied before any schema construction and before chip credit,
followed by the unchanged typed admission, kernel replay and separate agreement
gate. The parent's STRAINED verdict named the missing byte boundary; that boundary
exists and is oracle-tested. The residual duplication (F-02) is forced by the
layering and is advisory.

## 7. Reconciliation with coverage.md and the parent round

- Category: coverage.md's category (raw normalization/weak bounds before the
  received-record validator) is the same category as my inventory O1/B1-B11. Its
  five boundaries correspond to my B2-B3, B4-B7/B9, B8-B9, S1-S12 and F1.
- Parent I-01 (Important, framing): closed completely, not only for the four named
  examples. All of CRLF, RS, LS, PS, NEL, VT, FF, FS, GS, oversized frame, oversized
  capture, BOM, invalid UTF-8, missing final LF, digits, depth, duplicates and
  constants now fail closed; my own byte-level comparison (section 4) finds no
  remaining host-refused-but-credited byte sequence.
- Parent F-02 (Minor, RecursionError escape): closed; the depth guard and the
  explicit handler both route to an excluded cause.
- Parent advisories (strategy attribution, outer unused members, caller typing,
  summarize.complete meaning, ref retirement): no changed bytes; unchanged status.
- Discovery method: coverage.md's read_stream -> decode_json -> WireConsumer ->
  frames_for -> admitted_decision -> replay path matches mine. Its exclusions
  (exponent overflow stricter; 2 MiB bound is a resource guard) are accurate.
- Not covered by coverage.md and not required by it: F-01 (parsed-level
  state_mismatch class), which is outside the authorized scope; F-03 items.
  Missing coverage here is not a product defect.

## 8. Receipts assessment (implementer evidence, not reproduced)

- RED (checks/red-*): candidate 81a5aaf5 verified from Git as parent + final test
  bytes. 2 unittest cases, 27 failures, 0 errors, 0 skipped, pytest exit 1; the 26
  real-capture failures are exactly the 13 host-refused variants x 2 strategies I
  expected (BOM, invalid UTF-8 and unfinished already failed closed on the parent);
  the 27th is the missing decode_frame seam. source_verified=true at 81a5aaf5.
- Focused GREEN (checks/focused-*): candidate 7ca82180, six suites, 80 unittest
  cases, 0 skipped, exit 0, source_verified=true, Python 3.14.6, scrubbed
  environment with absolute PONTIUS_GIT, -B -P and warnings as errors per
  snapshot.ps1. Journal output digest equals focused-result.json's pinned digest.
- Parent finalizer framing diagnostic: runs on the parent commit with an existing
  real check-control capture; baseline hit, four host-refused mutations credited.
  It establishes the parent defect and the oracle; it is not evidence for r003.
- Limits: the focused run is the changed-suite scope only; broad suites are not
  claimed. Receipts are trusted as implementer evidence; I ran no project code.

## 9. Line counts and hygiene (raw frozen bytes)

- Changed blobs: eval_agreement.py 411 lines, test_eval_protocol.py 218 lines;
  both LF-only, BOM-free, max column 100, no trailing whitespace, final LF.
- Delta versus parent: eval_agreement.py +37/-4 (378 -> 411), test +81 (137 -> 218).
- Whole slice at the candidate: production 2093 (eval_bridge 521, eval_agreement
  411, v0a_eval_panel 674, v0a_eval_panel_completion 487); tests 1999. These equal
  checks/scope.json. Under the 3000 ceiling; above the 1200/600 working figures,
  which the addendum says is disclosure, not a return trigger.
- Registration: tests/cases.json unchanged and already lists test_eval_protocol.

## 10. Verified boundaries and evidence limits

Verified by reading frozen bytes: byte-level parity table (section 4); frame order
and closure; settlement replay; exception discipline; v1/v2 identity binding;
outcome/agreement separation; RED/GREEN identities. Not verified: runtime behaviour
(no execution), broad suites, the read_stream chunk/queue timing behaviour (not
byte-determined), and any full-H, strength or campaign claim (none is made).

## 11. Prohibitions and exposure statement

- Did not open reviews/ anywhere, progress.md, INDEX.md, other rounds, other task
  directories, transcripts or any scratch directory; did not list D:/Pontius/tmp
  (created my directory exclusively with os.mkdir).
- Dependency-pin verification read Git blobs of D:/Pontius-handoffs at 2943f935 for
  three pinned paths that live in other packets, purely to compare digests with the
  byte-identical inputs/ copies; no content beyond the allowed copies was displayed.
- Read-only Git only (rev-parse, cat-file, diff-tree, diff, ls-tree, for-each-ref),
  including the check/...r003-red and r003-focused refs named by the receipts.
- No project code executed; utility scripting only with CPython 3.14.6 via stdin
  (reviewer arithmetic, not a test receipt). One heredoc failed to parse and wrote
  nothing. No utility scratch files were created; the harness persisted large tool
  outputs under C:/Users/point/.claude/projects/... on its own.
- Exposure: the session start showed git status/recent commit titles of D:/Pontius
  (identity context only). No inherited findings, verdicts or memory content.
- Deliverables written: inventory-01-claude.md and review-01-claude.md only.
