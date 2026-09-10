# Review 02 (claude): v0a-eval-panel-completion/r003 — Tier C FIX cold review

Verdict: CLEAN. Design verdict: SOUND.
Candidate 7ca821802c949b047becf6599d603b3b63d51fa7, sole parent
430ad75de79cec13d66ff3dc4981dd3770a371b7, tree 3d2fe79d2af20125e322dd4a668335e789810863,
manifest 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd. Every finding
below binds to this commit and manifest. Reviewer role: review-02, top-down from the
requirements; inventory recorded and hashed before any deferred input was opened.

Inventory: D:/Pontius/tmp/eval-completion-r003-review-02-669b2ff0/inventory-02-claude.md
SHA-256 be34b6dffdee17eb9bb426aedf689e4d9d7c0b45bd43cf6278c5a0b87e7acd85 (17573 bytes).

## 1. Identity (recomputed from Git objects, not from packet claims)

- refs/heads/review/v0a-eval-panel-completion/r003 -> 7ca82180; commit has exactly one
  parent 430ad75d; tree 3d2fe79d matches candidate.json.
- diff-tree parent..candidate with rename detection disabled: exactly two modified paths,
  src/pontius/eval_agreement.py (blob 8329de1e -> 5122fd5b) and tests/test_eval_protocol.py
  (059adac1 -> 5c53a450). Recomputed rows "<sha256>  <path>\n" over the raw blobs, sorted
  as whole byte strings, are byte-identical to manifest.sha256; the digest of that file
  is 1f48c97a..., equal to candidate.json and handoff.md.
- Parent manifest (inputs/parent-manifest.sha256) recomputed over the three-file delta
  449a2a3c..430ad75d: byte-identical, digest 6e36bb41... as pinned.
- All 51 dependency pins in inputs/dependencies.json reproduce from the blob at the stated
  commit (README.md and docs/workflow.md at b6f8b08f; the accepted brief/design at
  beb84be5; three handoffs-repository rows at 2943f935 hashed only, without displaying,
  and byte-equal to the inputs/ copies; 44 rows at the candidate). brief.md,
  supporting-files.json and coverage.md digests match handoff.md.
- RED receipt commit 81a5aaf5 (refs/heads/check/v0a-eval-panel-completion/r003-red) is a
  sole child of the parent that changes only tests/test_eval_protocol.py to blob 5c53a450,
  the candidate's test blob; its classifier blob is the parent's 8329de1e.
  refs/heads/check/.../r003-focused points at the candidate commit itself.

## 2. Standard applied

Host-equivalence of admission: any retained byte sequence that tools/v0a_table_host.py at
the candidate (read_stream lines 512-537, decode_json 52-90, WireConsumer.read 662-680)
would refuse must be excluded before chip or hit credit. I compared every admission
predicate byte level first, then parsed level, against my own enumeration (inventory
sections 5-6), and only then against coverage.md and the receipts. Tier C lens: teacher
identity, exported membership and retained-outcome interpretation must not manufacture
agreement from missingness, defaults or failures.

## 3. Byte-level admission: classifier versus host (own enumeration, frozen bytes)

frames_for (eval_agreement.py 183-187) decodes strict base64, requires
0 < len <= 2,097,152 and a final LF, splits on byte 10 only and calls decode_frame on
line + b'\n'. decode_frame (120-151) requires bytes, 0 < len <= 16384 including the LF,
no byte 13, no EF BB BF prefix, byte-scanned bracket depth <= 8 outside quoted text with
escape handling, strict UTF-8, json.loads with unique keys, 640-digit integers after
lstrip('-'), rejected constants and finite floats; RecursionError becomes
wire:json_recursion. Every predicate is the host's, in the same order, with one
deliberate stricter case (float overflow such as 1e9999: host accepts inf, classifier
excludes), which brief.md line 12 requires. Result of the comparison:

- empty capture, capture over 2 MiB, trailing bytes without LF, CR anywhere, CRLF, BOM
  prefix, frames of 16385 bytes, depth 9, 641-digit integers, duplicate keys,
  NaN/Infinity, invalid UTF-8, non-object frames, concatenated values, extra frames
  after session_result, missing closure: refused by both.
- capture of exactly 2,097,152 bytes and frames of exactly 16384 bytes: admitted by both.
- \v, \f, \x1c, \x1d, \x1e, \x85, U+2028, U+2029 (the parent's splitlines separators):
  no longer separators; the bytes stay inside one frame and the frame fails JSON or the
  CR rule exactly as in the host.
- No byte predicate exists that the classifier admits and the host refuses. Host queue
  depth, deadlines and thread timing are not byte predicates and are not reproducible
  from a capture; that limit is stated, not a gap.

Parent finding I-01 is therefore closed completely, not only for the four executed
examples: the correction replaced the normalizing text path with the host's own physical
framing and bounded parser at one boundary, before any schema construction. Parent
Minor (RecursionError escaping the exclusion path) is closed at the same boundary.

## 4. Parsed-level admission and successful-credit paths

Exact field sets per frame kind mirror the host's WIRE_FIELDS (v2 ready adds provider and
config_sha256); protocol and session_id are bound across every frame and to the hand and
outer report identities; v1 decisions require the exact 16-field set, exact preparation
absence, exact TimingRecord fields with COMPLETED status, the 15 s and 2e-9 bounds, and
a DecisionRecord construction that enforces ascii id, digest shapes and SPINE_REASONS;
v2 decisions pass validate_decision plus provider identity binding and accepted delivery;
hand_result and session_result require complete/completed, accounted, evidentiary False,
finite seconds, no failure causes, and the settlement is compared as sorted JSON text to
both the retained hand settlement and the kernel replay. A hit additionally requires the
replayed hero decision count, replayed fields, action equality with both the applied
action and the lookup, blueprint digest and reason agreement, exactly one river record
whose lookup key equals the declared root key, a teacher entry, a true table hit and the
teacher action. I found no path by which a missing member, a default, a failed or
interrupted record, or a host-refused frame reaches 'hit'.

## 5. Findings (severity ordered)

F-01 Minor (design-consistent; non-blocking; outside the r003 fix scope).
Host semantic refusals remain chip-eligible agreement failures.
Location: src/pontius/eval_agreement.py 344-348 (chip_eligible set before the agreement
loop), 353-375 (replayed_state_mismatch, controlled_decision_count, river_decision_count
graded as causes). Host authority: tools/v0a_table_host.py 815 (state_mismatch), 825-830
and 679 (expects-action ordering).
Requirement: brief.md line 10 (host-invalid frames get no chip credit) read together with
inputs/accepted-design.md section 5, which assigns the replayed key/reason cross-check and
zero/duplicate river records to agreement while keeping outcome eligibility separate.
Scenario: a v1 capture whose river decision carries state_before_sha256 of 64 zeros
(tests/test_eval_agreement.py 214-216) would be refused by WireConsumer.decision with
state_mismatch and the hand would never complete; classify returns chip_eligible True,
chips -2, classification 'disagreement'. The same holds for a removed river action frame
(host: expects 'action', reads event_result, refuses) which the classifier grades
'agreement:river_decision_count:0' with chips retained (test 283-306 asserts that).
Falsifying observation: summarize over such a result reports completed=1.
Why not Important: these are not byte-level or field-rule admission predicates; they are
the host's cross-check against its live table, which the accepted design deliberately
reproduces at the agreement stage so that a policy's settled chips are not deleted by an
agreement diagnostic; brief.md line 13 preserves reason-only disagreements; the parent
disposition accepted the decision-admission structure. No hit is reachable this way.
Smallest correction, if the controller adopts strict parsed-level host equivalence: move
the replayed-field equalities (hand_id, event_index, action_index, street_action_index,
seat, street, state hashes, visible hash, blueprint digest) and the record-count check
from the agreement loop into frames_for/admitted_decision as exclusions, leaving only
reason, action and teacher comparisons at agreement. That is a design change requiring
its own candidate; it is not a residual of I-01.

F-02 Advisory (carried from the parent, unchanged bytes). strategy is compared only
against 'blueprint-v1' (line 349) and is not bound to the capture's protocol version; a
v1 capture classified with any other strategy string becomes chip-eligible 'unsupported'.
A v2 capture under 'blueprint-v1' cannot hit (v2 reasons and the absent blueprint_sha256
force causes). Parent disposition accepted this as a Slice B attribution limit; the frozen
caller (tools/v0a_eval_panel_completion.py play, line 302) fixes 'blueprint-v1'.

F-03 Advisory (carried). summarize.complete (409-411) ignores 'unsupported'; readers
(agreement 347-366, complete 409-415) require every primary attempt to be 'hit', so the
generic summary is outcome resolution, not primary acceptance. Preserve that reading.

F-04 Advisory, coverage only (not a product defect). The real-capture matrix models
read_stream with a local host_accepts helper (split on LF, 2 MiB) and calls the real
decode_json; the 2 MiB cap is exercised only by a stream that also breaks the per-frame
bound (coverage.md says so). Members of my inventory not exercised through classify: a
capture of exactly 2,097,152 bytes, a BOM inside a non-first frame, a whitespace-only or
empty frame in the middle of a real capture, a nested duplicate key. All are covered by
the same decode_frame code path the direct oracle test compares to decode_json, so I do
not treat them as an unverified failure scenario.

Verified limits, no finding: ready.source_manifest_sha256 is shape-checked only because
the session does not retain the manifest (comment at line 174); the classifier is stricter
than the host on non-finite floats; unknown v1 selection_reason strings are admitted and
become disagreements by explicit brief authority.

## 6. Design verdict: SOUND

The shape is now one raw-admission boundary that mirrors the host's physical framing and
bounded parser, followed by typed record admission, kernel replay, then agreement. The
parent's STRAINED verdict named exactly the missing raw boundary; it is present. The
residual strain is that decode_frame duplicates decode_json rather than sharing it (the
host is a tool, not an importable module, and the brief forbids changing it); the direct
oracle test in tests/test_eval_protocol.py 185-214 is what keeps the copies aligned and
must be kept whenever either side changes.

## 7. Reconciliation with coverage.md and the parent round

coverage.md's five boundaries match my inventory sections 2, 5 and 6 one for one. Its
category statement (raw input normalized or admitted under weaker bounds before the typed
validator) is the invariant I recorded. Its exercised cases equal the frozen test bytes:
nine separators, CRLF, frame at and over limit, BOM, invalid UTF-8, unfinished, capture
over limit, integer over limit on two real captures (v1 CHECK hit, v2 premium divergence),
plus 7 accepted and 14 refused direct oracle frames and the stricter 1e9999 case. The
parent disposition's four executed mutations (CRLF, U+001E, U+2028, oversized ready frame)
all appear in the RED failure list and pass GREEN. Coverage claims nothing about full-H,
timing or natural corruption, which is correct. My only additions are the F-04 members.

## 8. Receipts assessment (implementer evidence, assessed, not reproduced)

- RED: snapshot of 81a5aaf5, CPython 3.14.6, -B -P -W error::ResourceWarning, scrubbed
  environment (SystemRoot, TEMP, TMP, PONTIUS_GIT, PYTHONDONTWRITEBYTECODE), pytest exit 1,
  2 unittest cases, 27 failures = 26 real-capture exclusion subtests (13 variants x 2
  strategies) + 1 missing-seam assertion, 0 errors, 0 skips, source_verified true; journal
  output digest 401da4bd... equals checks/red-result.json. The 13 failing variants are
  exactly those the parent normalized; BOM, invalid UTF-8 and unfinished were already
  excluded on the parent, so their absence from RED is consistent.
- GREEN: snapshot of 7ca82180 (the candidate), same interpreter and environment, six
  suites, 80 unittest cases, 0 skipped, exit 0, source_verified true; journal output
  digest 906fe72e... equals checks/focused-result.json. freeze-r003.py and snapshot.ps1
  document create-only refs, a temporary index, uv sync --locked --offline and an explicit
  3.14.6 assertion. Broad suites were not run, as the workflow requires before two passes.
- Parent finalizer diagnostic (377c5e08...) executed at 430ad75d with source_verified
  true; its four host-rejected, classifier-hit observations are the defect this round
  fixes.

## 9. Line counts, budget and hygiene (raw frozen bytes; reviewer arithmetic)

- src/pontius/eval_agreement.py: 411 lines (parent 378), +37/-4; tests/test_eval_protocol.py:
  218 lines (parent 137), +81/-0. Both blobs: LF only, no CR, no BOM, final LF, all lines
  <= 100 columns, no trailing whitespace, ASCII, no tabs.
- Whole Slice A surface at the candidate: production 2093 (eval_bridge 521,
  eval_agreement 411, v0a_eval_panel 674, v0a_eval_panel_completion 487); tests 1999.
  checks/scope.json matches exactly. Production is above the 1200 working figure and at
  70% of the 3000 hard ceiling; per the controller's clarification the working figure
  alone does not return the slice.

## 10. Prohibitions and exposure statement

- Read only the allowed initial inputs, then coverage.md and the checks/ files named in
  supporting-files.json, in that order. Did not open reviews/, any other packet, progress
  or INDEX files, transcripts, or any other scratch directory.
- Harness-surfaced exposure, disclosed: `ls -la` of the packet listed the reviews/
  directory name and three files under checks/ that supporting-files.json does not name
  (inventory-01-codex.md, inventory-02-codex.md, retained-reviews-01-02.json); none was
  opened. `git for-each-ref` printed sibling ref names for r001/r002; names only. The
  system reminder showed the working tree's branch and five commit titles; no candidate
  content. Large tool outputs were persisted by the harness under
  C:/Users/point/.claude/projects/... and read back from there.
- No project code was executed; no tests, tools, imports, uv or hooks. Git use was
  read-only (rev-parse, cat-file, diff-tree, diff, for-each-ref). Nothing under
  D:/Pontius or D:/Pontius-handoffs was written or modified.
- Utility scratch files (reviewer arithmetic, not test receipts), all in my scratch
  directory D:/Pontius/tmp/eval-completion-r003-review-02-669b2ff0/: identity_check.py,
  hygiene.py, check_report.py. Interpreter:
  C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe (3.14.6).
- Output policy: this report and the inventory are LF-only, BOM-free, <= 100 columns,
  no trailing whitespace. No deviation to disclose.
