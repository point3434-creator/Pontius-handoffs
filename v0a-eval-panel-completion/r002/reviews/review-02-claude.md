# Cold review 02 - Claude

Defect verdict: CLEAN
Design verdict: SOUND
Round: v0a-eval-panel-completion/r002, FIX, Tier C
Candidate: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Parent: 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13
Tree: c531d0b93520cd69704aa14842cea32d5b31ca51
Ref: refs/heads/review/v0a-eval-panel-completion/r002-verified
Manifest SHA-256: 6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5
Inventory: D:/Pontius/tmp/eval-completion-r002-review-02-2c219e21/inventory-02-claude.md
Inventory SHA-256: fb8c8c8a8db96179739d39a917aa87930e4b868391276fdd285058b587a124d1

## 1. Identity results (from Git objects, not packet claims)

- refs/heads/review/v0a-eval-panel-completion/r002-verified resolves to 430ad75d; the
  commit object has exactly one parent, 449a2a3c, and tree c531d0b9; all three equal
  candidate.json.
- diff-tree 449a2a3c..430ad75d with rename detection off yields exactly three paths:
  M src/pontius/eval_agreement.py, M tests/cases.json, A tests/test_eval_protocol.py.
- Manifest recomputed as "<sha256>  <path>\n" rows over raw cat-file blob bytes, rows sorted
  bytewise as whole rows, LF after every row: byte-identical to manifest.sha256; its SHA-256
  is 6e36bb41...04cd5, equal to candidate.json and handoff.md.
- Parent anchor: the same recipe over 449a2a3c against its sole parent beb84be5 (eight
  paths) is byte-identical to inputs/parent-manifest.sha256 and hashes to f58d6ed8...e194.
- All 51 rows of inputs/dependencies.json verified at the stated repository and commit; the
  seven packet copies match their pins byte-for-byte. Every pinned path outside the three
  changed paths resolves to the same blob at the parent and the candidate, so the host,
  session, dealer, event adapter, provider codec, v0a model/runtime/trace, kernel and cards
  surfaces are unchanged (brief R1).
- brief.md, supporting-files.json, every inputs/ file, coverage.md (384bcc6b...934e1) and
  every checks/ file hash to the values pinned in handoff.md and supporting-files.json.
- Receipt refs: r002-red 64526c1a has sole parent 449a2a3c and changes only tests/cases.json
  and tests/test_eval_protocol.py; checks/red-test.py equals that blob (cc43c867...c6fc).
  r002 85e59e8f carries the candidate's exact eval_agreement.py blob (8329de1e) and differs
  from the candidate only in the dealer-index line of the test, matching coverage.md's
  setup-error account.

## 2. Findings (severity-ordered)

No Critical or Important finding survived verification. The material category accepted at
r001 (review 03 R03-01 and review 04 F1: incomplete raw retained-schema admission before
credit) is closed completely on this candidate, not only for the named examples; section 4
walks every member. The items below are Minor or advisory and do not block.

### F02-01 - Minor: declared strategy is not bound to the retained protocol version

Location: src/pontius/eval_agreement.py:273-274 (strategy parameter), 316-318 (early
baseline return), 149-165 (protocol admitted from the ready frame only).
Requirement: design section 5 keeps outcome and agreement eligibility separate but reads
the actual retained envelope; brief R3 credits chips to a valid completed baseline
divergence. The retained ready frame carries the protocol version, and the session tool
binds v2 to baseline-rules-v1 (tools/v0a_table_session.py:179-190, 237).
Scenario: call classify(report, strategy='baseline-rules-v1', ...) with an unmodified
completed blueprint-v1 capture (protocol v1, a table-hit river record). The classifier
returns chip_eligible=True, classification='unsupported', cause
agreement:baseline_outside_declared_root, attributing a blueprint host hand to the
baseline policy. The converse (v2 capture with strategy='blueprint-v1') can never reach
'hit': bind_identity forces provider baseline-rules-v1 and the v2 record lacks
blueprint_sha256 and a v1 reason, so every record disagrees.
Falsifying observation: no predicate compares protocol.endswith('v2') with the strategy
label; nothing else in the completion tool does either (play fixes strategy to
blueprint-v1 and the v1 host). Unreachable through tools/v0a_eval_panel_completion.py
in Slice A; reachable only by a caller that mislabels, which is the Slice B interface.
Smallest correction: in classify, require (protocol == v2 interface) == (strategy ==
'baseline-rules-v1') before chip credit, with an excluded cause on mismatch. Confidence
high (static, complete path). Not a Tier C manufacture of agreement.

### F02-02 - Advisory: frame splitting is more lenient than the host's LF-only framing

Location: src/pontius/eval_agreement.py:152-154 (str.splitlines on the decoded stream).
The host frames on b'\n' only and refuses CR (tools/v0a_table_host.py:68, 530-535).
str.splitlines also splits on CR, VT, FF, FS, GS, RS, NEL, LS and PS. Every such
divergence fails closed (fragments do not parse, or a '\r\n' line is accepted where the
host would have refused), so no success can be manufactured. Advisory: split the raw
bytes on b'\n' and refuse b'\r', matching the producer.

### F02-03 - Advisory: caller inputs are trusted without shape checks

Location: src/pontius/eval_agreement.py:273-283. stacks is not required to be an exact
int and teacher_actions values are not required to be BettingAction. A non-action
teacher value yields teacher_disagreement (fail closed); a float stacks value reaches
NoLimitBettingState.new_hand and exact_integer(v, stacks), which accepts int 4 == 4.0.
These are in-process caller values from the completion tool, not retained protocol.
Advisory: exact-type both at entry.

### F02-04 - Advisory: summarize.complete does not require hits or forbid unsupported

Location: src/pontius/eval_agreement.py:378. complete is true when nothing is missing,
disagreeing or excluded, so an all-unsupported primary schedule would read complete.
The tool-level gates close this (completion.agreement:347, completion.complete:409-411
require every primary attempt to be 'hit'), so the run cannot succeed. Pre-existing at
r001 and outside the fix scope; noted so a later consumer does not treat complete as
acceptance on its own.

## 3. Design verdict: SOUND

The corrected shape now has an explicit raw-admission stage (admitted_decision,
exact_fields, exact_integer, parsed_action) that validates the received object before any
constructor can normalize or default, reuses the public v2 validate_decision boundary and
the v1 model field sets, and only then hands the raw dict to replay and agreement. That
removes the structural cause the parent round named: typed constructors standing in for
validation. The residual duplication is small and pinned by a real-capture test: the
WIRE_FIELDS literal and the identity prefixes are copied from the sealed host, and the
timing tolerance predicate mirrors host lines 703-706. If a later round finds drift there,
the change that stops it is to derive frame field sets from one shared constant; today no
defect follows from the duplication.

## 4. Reconciliation with the parent findings and coverage.md

Parent category (R03-01, F1) members, each traced at the candidate:

- ready.evidentiary ignored -> line 164 requires `is False` (RED: True/None/'false').
- interrupted_response_count coerced -> line 208 exact_integer 0.
- requested_hands, completed_hands, ordinal coerced -> lines 292-297 exact_integer 1.
- preparation_use defaults (credited_seconds, producer_status) and artifact_sha256s ''
  normalized -> lines 68-71 exact member set, producer_absent, exact list == [], exact 0,
  all before PreparationUseRecord is built at line 86.
- v2 admitted by suffix plus three delivery fields -> line 57 validate_decision (exact 27
  keys, labels, ints, digests, timing, preparation) plus lines 58-64 binding provider,
  config_sha256, source_manifest_sha256 and fallback_blueprint_sha256 to the ready frame and
  delivery accepted with delivered == applied == selected.

Beyond the named examples, the same exactness is applied at every other consumed integer
or boolean I inventoried: button and the six starting stacks (222-225), applied-action
index and seat (236-237), action-frame action_index and seat (179-181), action objects at
all three sites (49-50, 182, 241), the v1 decision and timing member sets (66, 74),
child_exit_code (301-302), event_index (186), and v2 provider/config identities across
ready, hand and outer report (133-139). I found no remaining member of the category that
could enter chip or hit credit by coercion, omission or default. The relabel/unknown-reason
behaviour required by R3 is preserved: selection_reason must be a str (73) and is compared,
never replaced (330-336). CHECK hits, off-pool defaults, changed-stack zero hits and
retained failures keep their prior classifications (R4), and a valid v2 baseline retains
kernel-settled chips (R3).

coverage.md claims 1-7 match my inventory sections 3-5. Claim 6's real v2 premium witness
and claim 2's identity binding are the two members the parent tests could not reach; both
are now exercised against actual captures. Claim 7 (six affected suites) matches the six
registered names. Claims about RED (50 mutations, 49 failures, the v1 artifact_sha256s case
already excluded at r001) reproduce from red-result.json. Limits that coverage states and I
confirm: the mutation matrix is not byte-identical between RED and GREEN (GREEN adds
missing_action, stack_type, missing_timing and provider_binding cases); no full-H claim.

Coverage members I inventoried that the tests do not exercise, none a product defect:
non-str selection_reason (None/bool) as an exclusion; the strategy/protocol coupling
(F02-01); a real host all-in-before-river baseline capture (the event-count replay for that
line is checked only by the constructed 'allin' fixture, and I verified from the kernel at
no_limit_betting.py:588-640 and the host at v0a_table_host.py:274-302 that the numbering
agrees); CR/LF leniency (F02-02). Missing coverage here is not evidence of a defect.

## 5. Receipts assessment (implementer evidence, not reproduced)

- focused-receipt.json: candidate 430ad75d, snapshot worktree eval-completion-check-
  r002-verified, venv CPython 3.14.6, -B -P, ResourceWarning and unraisable warnings as
  errors, environment limited to SystemRoot/TEMP/TMP/PONTIUS_GIT/PYTHONDONTWRITEBYTECODE,
  exit 0. focused-journal.jsonl: source_commit 430ad75d, source_verified true, 79 unittest
  cases, 0 skipped, output_sha256 a1318803...d7d7 equal to focused-result.json's bytes.
  Suite counts 11+29+8+21+9+1 = 79 across exactly the six registered names.
- red-receipt.json: candidate 64526c1a (test-only child of r001), exit 1; red-journal names
  it with source_verified true; red-result.json shows one unittest, 49 FAIL subtests, no
  errors; the v1 CHECK control and v2 baseline control passed before the mutations.
- setup-error receipts: candidate 85e59e8f, exit 1, one ERROR from dealer index 16; retained
  honestly as a test setup failure, production bytes identical to the candidate.
- snapshot.ps1 and freeze-protocol.py describe an isolated worktree snapshot with uv
  --locked --offline, interpreter identity assertion and create-only ref update; I did not
  run either. prerequisite-audit.json is a finalizer fact check of r001 artefacts and is
  not evidence for this candidate's behaviour.
- These receipts authorize nothing beyond focused GREEN on this candidate; broad suites,
  adoption and any retained solve/export/agreement remain separately gated.

## 6. Line counts, hygiene, boundaries and limits

- Changed blobs from raw bytes: eval_agreement.py 378 lines (parent 326), test_eval_protocol
  .py 137, cases.json 52; all LF-only, BOM-free, no line over 100 columns, no trailing
  whitespace, ASCII, final LF. scope.json's per-file figures equal mine.
- Whole Slice A from blobs: production 2060 (eval_bridge 521, eval_agreement 378,
  v0a_eval_panel 674, v0a_eval_panel_completion 487); tests 1918. Below the 3000 hard
  ceiling; above the 1200/600 working figures, which the addendum says is disclosure, not a
  return trigger. No dated experiments script exists at the candidate.
- Verified boundaries: three-path delta; unchanged host/session/codec/kernel/model blobs;
  raw admission precedes every typed construction; agreement derives hits only from a
  replayed applied history, the classifier's own lookup, the retained v1 reason and the
  caller's teacher; a v2 capture can never be a hit.
- Practical limits: static review only; no test, host, solver or classifier execution by me;
  no real all-in baseline capture inspected; the classifier trusts in-process caller inputs
  by design; no full-H, tie-census, strength or resource-adequacy claim follows.

## 7. Prohibitions and exposure statement

Order of work: handoff.md, candidate.json, manifest.sha256, brief.md, supporting-files.json
and every inputs/ file; Git identity; frozen source via git cat-file/diff/diff-tree/
rev-parse/rev-list/for-each-ref/ls-tree only; inventory written and hashed; only then
coverage.md and checks/. No reviews/ directory, other packet, progress/INDEX/readiness/
disposition file outside checks/, transcript, session log, sibling scratch or memory
source was opened. No project code was run or imported; no test, tool, uv or hook was
executed. No commit, ref write, worktree operation or edit under D:/Pontius or
D:/Pontius-handoffs occurred. Utility scripting used the mandated CPython 3.14.6 path and
coreutils sha256sum, labelled reviewer arithmetic.

Disclosures: (1) the harness injected a git-status snapshot of the D:/Pontius working tree
(branch master, two modified files, five recent commit titles) and the user's email; it
contained no finding or verdict and I did not read working-tree source. (2) To verify three
dependency pins in the D:/Pontius-handoffs repository at commit 2943f935 I hashed those
blobs with git cat-file without displaying them; they are byte-identical to the allowed
packet copies. (3) for-each-ref listed five review ref names for this task; I inspected
commits 64526c1a, 85e59e8f and f2cdf32e only through read-only Git objects to check the
receipts. (4) Besides the two deliverables, my scratch directory holds identity_check.py,
the manifest/pin utility; the harness also persisted two large tool outputs under its own
tool-results directory. (5) One Bash heredoc failed to parse and wrote nothing; the
inventory was then written with the file tool and normalized to LF before hashing. No
prohibited exposure occurred.

This verdict grants no broad testing, adoption, publication or retained execution; a second
qualifying cold pass, broad snapshot suites and exact per-commit authorization remain due.
