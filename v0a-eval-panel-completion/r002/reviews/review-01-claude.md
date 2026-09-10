# Cold review 01 - Claude

Verdict: CLEAN
Design verdict: SOUND
Round: v0a-eval-panel-completion/r002, FIX, Tier C
Candidate: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Parent: 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13
Tree: c531d0b93520cd69704aa14842cea32d5b31ca51
Ref: refs/heads/review/v0a-eval-panel-completion/r002-verified
Manifest SHA-256: 6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5
Inventory: D:/Pontius/tmp/eval-completion-r002-review-01-ac0a701c/inventory-01-claude.md
Inventory SHA-256: af8323913bd1acc9fd77c8d987b90079292584189e8b2d7af1f00a15eefe03b6

## 1. Identity (verified from Git objects, reviewer arithmetic, not a test receipt)

- The ref resolves to 430ad75d; `cat-file -p` shows tree c531d0b9 and exactly one parent,
  449a2a3c, whose own parent is beb84be5 (the base named by completion-brief.md).
- `diff-tree parent..candidate`: M src/pontius/eval_agreement.py, M tests/cases.json,
  A tests/test_eval_protocol.py; nothing else. Numstat +80/-28, +2/-1, +137/0.
- Manifest recomputed over raw `cat-file blob` bytes as "<sha256>  <path>\n" rows sorted
  bytewise: byte-identical to manifest.sha256; its SHA-256 equals candidate.json
  manifest_sha256 and the handoff line.
- Parent anchor: inputs/parent-manifest.sha256 recomputed at 449a2a3c against beb84be5
  is byte-identical; its digest f58d6ed8... matches supporting-files.json.
- brief.md, supporting-files.json and coverage.md digests match the handoff; all 35
  supporting-file digests match; all 51 dependencies.json pins match the blob at the
  stated commit in the stated repository. Every dependency pinned at 430ad75d other than
  the two modified paths is byte-identical to the parent blob, so "all other source is
  exactly the rejected parent" holds for the pinned set.
- Receipt refs (identity only, contents not read as source): 64526c1a (r002-red) has sole
  parent 449a2a3c and changes only tests/cases.json and tests/test_eval_protocol.py; its
  four Slice A production blobs equal the parent's; its test blob hashes to
  cc43c867..., the digest of checks/red-test.py; its cases.json equals the candidate's.
  85e59e8f (r002, the setup-error run) has sole parent 449a2a3c and the same three
  changed paths as the candidate. Sibling ref r002-green-initial was not examined.

## 2. Findings (severity-ordered)

No Critical or Important finding survived verification. The Tier C invariant holds on
every path I traced: a 'hit' requires a completed, settled, untruncated capture, exactly
one controlled river record, the independently replayed key equal to the declared s=4
root key, a replayed PreparedBlueprint table hit, the retained selection_reason equal to
the replayed reason, and the selected action equal to the applied action, the replayed
lookup action and the frozen teacher action. Missing members raise KeyError/Unusable,
wrong types fail `type(x) is T`, coerced values (True/1.0 for 1, '' for []) fail the new
exact predicates, and no dataclass with defaults or normalization (PreparationUseRecord,
tuple(), HandAction, TimingRecord, DecisionRecord) sees a wire object before its member
set and values are checked. Both protocol versions are admitted only under their own
shapes; a v2 capture can never produce 'hit' (no blueprint_sha256 member, provider
labels never equal 'table_hit'/'passive_default').

### F-01 Minor: frame splitting is broader than the host's LF framing

Location: src/pontius/eval_agreement.py:152-154 (`raw.decode('utf-8').splitlines()`).
Requirement: design section 5, "inspect the child_stdout_base64 stream as complete framed
messages"; the host frames on b'\n' only (tools/v0a_table_host.py:530-535) and refuses
CR (host decode_json:68).
Scenario: a constructed capture whose physical line is `{...ready...}\u2028{...}\n`
(U+2028 inside a line) is one frame to the host and two frames to the classifier, since
str.splitlines also splits on \u2028, \u2029, \x85, \x1c-\x1e, \x0b, \x0c and \r.
Falsifying observation: the classifier can only turn one frame into several that must
each pass the full member-set, identity, pairing and replay checks, so it cannot admit
a stream the host would have accepted as something else, and it cannot manufacture
credit; it can accept a stream the host would have refused as protocol_invalid. Real
captures are ASCII produced by json.dumps (all control and non-ASCII characters
escaped), so no retained capture reaches this divergence.
Correction: split the raw bytes on b'\n' (after requiring no b'\r') before decoding.

### F-02 Minor: RecursionError is outside the exclusion boundary

Location: src/pontius/eval_agreement.py:152-154 and the except tuple at 308.
Requirement: brief mechanism 7 and design section 5 make a malformed capture an
excluded observation with a retained cause.
Scenario: a constructed capture whose ready frame is a JSON array nested a few thousand
levels deep. json.loads raises RecursionError, which is not ValueError/TypeError/
KeyError/IndexError/binascii.Error, so classify raises instead of returning 'excluded'.
Falsifying observation: the caller (completion.play/attempt) propagates the exception,
the phase fails and nothing is credited; the host bounds depth to 8 (decode_json:81-83)
and a completed hand implies every frame passed that bound, so no retained capture
reaches this path. Constructed-fixture only.
Correction: add RecursionError to the caught tuple, or bound depth as the host does.

### F-03 Advisory: declared strategy is not bound to the capture's protocol

Location: src/pontius/eval_agreement.py:273-274, 316-318.
The `strategy` argument selects the early 'unsupported' return, while the protocol
version comes from the ready frame. A v1 blueprint capture passed with
strategy='baseline-rules-v1' is chip-eligible 'unsupported' with cause
baseline_outside_declared_root; a v2 capture passed with 'blueprint-v1' is a
'disagreement'. Neither direction can produce a hit, and completion.play always passes
the default, so this is a labeling concern for any future Slice B consumer, not a
Slice A defect. The result dict carries no protocol/strategy member.
Advisory correction: require `protocol.endswith('v2') == (strategy == 'baseline-rules-v1')`
or record the observed protocol in the result.

### F-04 Advisory: outer envelopes are not exact-membership checked

Location: src/pontius/eval_agreement.py:289-302 and replay:222-225.
Frames are checked for exact member sets; the session report, hands[0] entry and nested
hand result are not. Every member the classifier reads is validated (exact ints, `is`
checks, equality to validated ready values, json equality of settlements), so unknown
extra members cannot influence credit and missing members exclude. Two cheap
hardenings consistent with the "one raw admission boundary" direction: exact member
tables for the three envelopes, and recomputing hand['input_sha256'] from the caller's
deal/board/stacks/opponents through the Session's encode() to bind the exact host input
to the retained envelope (today the deal is bound through visible_cards_sha256 and the
showdown settlement only).

### F-05 Advisory: summarize().complete ignores 'unsupported' primaries

Location: src/pontius/eval_agreement.py:378 (unchanged from the parent).
`complete` is false only for missing, disagreement or excluded; an 'unsupported'
primary would pass. completion.complete/agreement independently require every primary
to be 'hit', and an in-pool hand cannot be 'unsupported' under a matching teacher, so
no acceptance path is affected. Out of this FIX round's scope; noted for the next
surface.

### F-06 Advisory (packet hygiene): review namespace holds several r002 refs

refs/heads/review/v0a-eval-panel-completion/{r002, r002-red, r002-green-initial,
r002-verified} exist; the flat r002 ref points at the setup-error commit 85e59e8f, not
the candidate. Identity binds by commit+manifest so this packet is unambiguous, and
coverage.md discloses the preparatory refs, but the workflow names rounds r<NNN> and
treats round refs as immutable; a later packet could bind r002 to the wrong bytes.
Retirement under the packet rules should archive or delete the preparatory refs.

## 3. Reconciliation with the parent findings, coverage.md and the receipts

Parent category (03 R03-01, 04 F1, accepted as one Important): incomplete raw
retained-schema admission before typed construction. Members named there: ready
.evidentiary; interrupted_response_count; requested_hands/completed_hands/ordinal
equality coercion; v2 records admitted without validate_decision; preparation_use
members defaulted by PreparationUseRecord; artifact_sha256s normalized by tuple().

Closure check against my inventory (section 4), member by member:
- ready.evidentiary is False (frames_for:164). Closed.
- interrupted_response_count exact int 0 (frames_for:208). Closed.
- requested_hands, completed_hands, ordinal exact int 1 (classify:292-297). Closed.
- v2: validate_decision on the parsed record, then provider/config/source_manifest and
  fallback_blueprint identity bound to the ready frame, then delivery accepted with
  delivered == applied == selected (admitted_decision:56-64); ready/hand/report
  provider and config equality plus a 64-hex config digest (bind_identity:133-139).
  Closed, including the baseline early-exit concern: admission precedes chip credit.
- v1: exact 16-member DecisionRecord set, exact 3-member preparation set with
  producer_absent, exact empty list and exact int 0, selection_reason exact str,
  exact 10-member timing set, HandAction shape, all before any constructor
  (admitted_decision:65-87). Closed. tuple() normalization is gone.
- Beyond the named examples, the same category was closed for the other consumed
  members I enumerated: entry.button and starting_stacks (exact ints, len 6), the
  applied_actions list and each row's member set, index and seat (exact), each action
  object's shape, the action frame's action_index/seat types and action shape, and
  secondary_failures' list type. I found no remaining consumed wire member that is
  compared by equality without an exact type check or without equality to an already
  validated value. The correction closes the category, not only the examples.

coverage.md claims 1-7 correspond to inventory obligations O1-O8 and O11. Claim 5
(unknown reasons observed, not replaced) matches admitted_decision:72-73 and
classify:334-336. Claim 6 (finite deterministic premium witness, real baseline raises
preflop) matches test_eval_protocol.py:26-33 and 67-70. Claim 7 (six affected suites)
matches the focused receipt. The claimed falsifiers are the right ones. Coverage limits
I add: the new suite asserts exclusion for a sample of members (ready flag, eight
integer counters as bool/float, three preparation members, '' artifacts, three action
shapes, two stack types, three timing members, four v2 members, three v2 identity
bindings). Members consumed but not mutated there - selection_reason non-string,
spine_reason, digest shapes, evidentiary/accounting_complete on the terminal frames,
capture_truncated and child_exit_code types, status strings, event_index type, timing
flag/elapsed semantics, settlement element types - are either exercised by the parent's
retained test_eval_agreement.py cases or pass by construction through `is`/exact-type
predicates and the typed models I traced. Missing coverage there is not a product
defect; F-01/F-02 above are the only uncovered paths with an observable difference, and
neither is reachable from a retained capture.

Receipts (implementer evidence, assessed not reproduced):
- RED: r002-red at 64526c1a, verified above as a test-only child of the rejected parent
  with the parent's production blobs; 1 unittest case, 49 of 50 subtests failed the
  exclusion assertion, 0 errors, pytest exit 1, CPython 3.14.6, source_verified true.
  The one passing subtest (missing v1 artifact_sha256s) was already excluded by the
  parent's KeyError, which matches my reading of the parent blob. Deterministic RED
  against the frozen rejected candidate: satisfied.
- Setup error: r002 at 85e59e8f failed on a test bug (dealer index 16 outside 0..15),
  retained honestly; the candidate's test scans index % 16 over 32 seeds.
- GREEN: focused isolated snapshot at 430ad75d, detached worktree, `uv sync --locked
  --offline`, interpreter asserted 3.14.6, scrubbed environment (SystemRoot, TEMP, TMP,
  PONTIUS_GIT absolute, PYTHONDONTWRITEBYTECODE), -B -P, ResourceWarning and unraisable
  warnings as errors, `-o pythonpath=. src tests`; six suites, 79 unittest cases, 0
  skipped, pytest exit 0; journal source_commit is the candidate, source_verified true;
  the journal's output_sha256 equals the SHA-256 of checks/focused-result.json
  (a1318803...) and the supporting-files pin. Consistent and properly limited.
- No broad-suite, retained solve/export/agreement, calibration or strength claim is made
  by these receipts, and none follows from this review.

## 4. Design verdict: SOUND

The parent round's STRAINED verdict named one local cause: partial wire validation mixed
with typed constructors that normalize and default. This candidate introduces the raw
admission step those reviews asked for (exact_fields/exact_integer/parsed_action and
admitted_decision) and runs every constructor only after it; v2 reuses the public
validator; framing, admission, outcome replay and agreement comparison are now distinct
stages in one module, and the outcome/agreement separation for baseline chips is kept.
No finding in this round arises from the shape; F-01..F-05 are ordinary hardening.
Advisory only: extending exact member tables to the three outer envelopes (F-04) would
make the completeness argument mechanical for the next reviewer.

## 5. Line counts and hygiene (raw frozen bytes, reviewer arithmetic)

Whole Slice A production: eval_bridge.py 521, eval_agreement.py 378, v0a_eval_panel.py
674, v0a_eval_panel_completion.py 487 = 2,060 lines; below the 3,000 hard ceiling and
860 above the 1,200 working figure. Tests: test_eval_bridge 198, test_eval_panel_tool
750, test_eval_export 153, test_eval_agreement 383, test_eval_completion_tool 297,
test_eval_protocol 137 = 1,918 lines, 1,318 above the 600 working figure. checks/
scope.json states the same numbers and delta. The controller clarification makes the
working-figure excess disclosable, not a return trigger. All ten files are LF-only,
BOM-free, at most 100 columns, free of trailing whitespace and LF-terminated;
cases.json adds exactly one registration. Only the three declared paths change; host,
session, adapter, codec, kernel, provider, execution and status sources are unchanged.

## 6. Verified boundaries and practical limits

Statically traced from frozen blobs: the child frame producer (event adapter), the v1
and v2 record producers (runtime), the host capture and per-frame admission, the
Session envelope, the completion tool's play/agreement/accounting consumers and the
harness registration. I did not execute any project code, test, host, solver, export or
agreement; findings are static, path-complete traces, not executed reproductions. The
classifier cannot bind blueprint_artifact_sha256 or source_commit to external truth;
admission owns that, as the source states. Real-boundary behaviors (transport, Job
containment, kill during an active Session) are outside this round's changed surface.

## 7. Prohibitions and exposure statement

Inputs opened: handoff.md, candidate.json, manifest.sha256, brief.md,
supporting-files.json, every inputs/ file, and raw frozen blobs via
`git cat-file blob 430ad75d:<path>` (plus the parent's two changed blobs for the diff);
coverage.md and every checks/ file only after the inventory was written and hashed.
Read-only Git only (rev-parse, cat-file, diff-tree, diff, rev-list, for-each-ref).
No reviews/ directory, other packet, progress/INDEX/readiness/disposition file outside
this packet's checks/, transcript, session log, sibling scratch or memory source was
opened. No project code was run or imported; utility scripting used only the mandated
CPython 3.14.6 interpreter. No edit to any file under D:/Pontius or D:/Pontius-handoffs;
the only writes are the two files in my exclusively created scratch directory.
Disclosures: (1) before sealing the inventory I hashed coverage.md's bytes to confirm
the handoff digest without displaying its content; (2) `for-each-ref` listed the
sibling r002* ref names and commits (F-06); (3) the harness-injected session context
contained the D:/Pontius working-tree git status (branch master, two modified files)
and five recent master commit subject lines, none of which contain candidate content,
findings or verdicts; (4) one large Read was persisted by the harness to its own
tool-results file, which I did not treat as an input; (5) checks/prerequisite-audit.json
names parent-packet review file paths and digests, which I did not open. No other
exposure occurred. This verdict grants no broad testing, adoption, publication or
retained execution; it is one of the two qualifying cold passes Tier C requires.
