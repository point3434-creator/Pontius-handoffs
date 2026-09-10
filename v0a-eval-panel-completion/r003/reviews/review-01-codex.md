# Cold review 01 - Codex - completion r003

Defect verdict: CLEAN.
Design verdict: SOUND for the authorized raw-frame admission correction.
No required finding survives independent source review and deferred-evidence reconciliation.
This is a static cold review with verified supplied execution records, not a reviewer test run.

Candidate: 7ca821802c949b047becf6599d603b3b63d51fa7
Parent: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Tree: 3d2fe79d2af20125e322dd4a668335e789810863
Ref: refs/heads/review/v0a-eval-panel-completion/r003
Manifest: 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd

Scope and qualification disclosure

The exact delta is src/pontius/eval_agreement.py and tests/test_eval_protocol.py.
All source locations below refer to raw blobs at the candidate unless another SHA is named.
No worktree source was used as evidence. The handoff was read before other review input.

Inherited developer context exposed a memory summary, distinct from repository instructions:
- User preferences for rigorous six-max NLHE/Pontius research, exactness, reproducibility,
  general-purpose 100 bb six-max play, offline training, exact ties and folded-card factors.
- Prior training notes for the fa55 Pontius/pluribus-lite work: baseline-000, two dated
  training/bucket scripts, Fisher-Yates equivalence, 258.87 iterations/s with four workers,
  durable milestones, no established strength improvement, and shared-update nondeterminism.
- ADR-0507 baseline-watch governance: baseline-rules-v1, a prepared but unlaunched three-hand
  proposal, freeze/independent-review/authorization sequencing, and a reserved run identity.
- Architecture research in a separate research workspace: Pluribus, ReBeL, Deep CFR, ESCHER,
  offline blueprint plus neural approximation and depth-limited solving, with multiplayer
  guarantee limitations. Numerical six-dealt evaluator notes mention Z5, output-aware
  treewidth/Hessians, ownership splits, cancellation, precision_probe.py, package_checks.py,
  and a verified research ZIP; a planned PDF had not materialized in that earlier delivery.
- General operational advice included per-command safe.directory in D:/Pontius, avoiding
  retained-output scans, and separating feasibility, throughput, persistence, and strength.

Those summaries supplied no completion r003/r002 candidate history, findings, or verdicts.
They were not used for substantive review. No memory file was opened, searched, or cited.
Ordinary inherited instructions also described tools, runtime, workspace permissions, skills,
review behavior and user preferences. The using-superpowers skill exempts dispatched agents;
code-verification and its evidence matrix were read for process. No other reviewer conclusion
was received. Cold qualification under the injected-summary disclosure is for finalization.

One accidental read targeted a nonexistent skill path and returned no contents. The required
Python executable initially failed to launch under the sandbox; the identical read-only
utility then succeeded with reviewed escalation. This was an environment failure, not a test.
No auto-review rejection remained. No project code, tests, hooks, solver, host, or session was
executed by this reviewer. Utilities used only the specified Python 3.14 executable, PowerShell,
and absolute read-only Git commands. No utility scratch files were created.

Independent inventory was written and hashed before coverage.md or any checks/ was opened:
D:/Pontius/tmp/eval-completion-r003-review-01-9cf26a71/inventory-01-codex.md
SHA-256: 49f1aacda69b8139571497cf4e89f5550d71e13f8e54a0911142d86ae6a523a5
Only after sealing did I read the expressly permitted parent disposition and repair plan.
No reviews/ directory, other packet, transcript, ledger, readiness file, or sibling scratch
was inspected. Dependency verification read only the raw objects named by dependencies.json,
including the explicitly pinned handoffs repository blobs; no adjacent packet was opened.

Executed utility evidence

Read-only subprocess.check_output calls used C:/Program Files/Git/cmd/git.exe with per-command
safe.directory. Commands were rev-parse, show -s --format=%P/%T, diff-tree --name-only,
diff --no-ext-diff, and cat-file blob. Standard-library hashlib/json/pathlib utilities:
- Verified ref, sole parent, tree, and exact two-file delta.
- Rebuilt candidate SHA-256 digest/path/LF rows from raw blobs, sorted full rows bytewise;
  exact manifest bytes and announced manifest digest match.
- Rebuilt the supplied parent three-file manifest from raw parent blobs. Parent's sole parent
  is 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13; the delta includes tests/cases.json.
- Verified all 51 dependency pins and packet-copy byte equality where a copy is declared.
- Verified brief, supporting-file list, all 32 listed supporting files, and deferred coverage.
- Verified RED 81a5aaf5670c9f495cc03dbb26796699a11cffa1 is a test-only child of the rejected
  parent, with final-candidate-identical protocol tests and unchanged parent production bytes.
- Verified focused/RED journal output hashes against the supplied result bytes.
- Recomputed all scope.json line totals: 2093 production and 1999 test lines. Production is
  below the governing 3000 ceiling. The older 1200/600 figures remain disclosed working figures.
- Verified changed raw source and sealed inventory: LF, no BOM/trailing whitespace, <=100 columns.

All successful utilities exited 0. These facts establish byte relationships and record
consistency; they do not independently reproduce project execution or measured performance.

Bottom-up boundary assessment

The producer writes JSON plus LF as UTF-8 with allow_nan=False in
 tools/v0a_event_adapter.py:188-192. Session retains stdout bytes via base64 at
 tools/v0a_table_session.py:289-301. There is no text-line normalization in that retention.

Frozen tools/v0a_table_host.py:512-537 is the physical-stream oracle. It caps stdout at
2097152 bytes, frames only on LF, includes the LF in the <=16384-byte frame bound, and refuses
unfinished EOF. tools/v0a_table_host.py:52-90 and :662-665 then reject CR, leading UTF-8 BOM,
JSON depth above eight outside quoted/escaped text, integer tokens over 640 signless digits,
duplicate decoded keys, nonstandard constants, invalid UTF-8 and invalid JSON.

src/pontius/eval_agreement.py:120-152 repeats the relevant bounded JSON admission; :183-188
first verifies retained capture size/termination and splits only on physical LF. Every chunk
passed to decode_frame has exactly its terminating LF. A direct helper call can contain JSON
whitespace LF internally, just as host decode_json can; the production caller, like the host
stream reader, owns physical splitting. This is not a production acceptance bypass.

Adversarial false-success searches:
- CRLF/raw CR cannot reach decoded records. Replacing LF with control/Unicode separators
  no longer manufactures separate JSON objects; the physical frame remains joined and fails.
- Padding a valid frame above 16384 bytes cannot be normalized away before admission.
  Equality is inclusive, including LF. An exact-cap terminated capture is not size-refused;
  capture overflow is refused before frames are decoded.
- Quoted brackets and escaped quotes cannot accidentally change lexical depth tracking.
  UTF-8 multibyte continuation bytes cannot impersonate ASCII quotes/brackets/backslashes.
- Invalid UTF-8, duplicate decoded keys, constants, malformed/multiple JSON values and integer
  overflow in digit count cannot normalize into valid records. Both integer signs use the
  host's token predicate. Finite float parsing intentionally rejects exponent overflow even
  though raw host JSON parsing may yield infinity; that is the preserved explicit restriction.
- json.loads recursion is translated to Unusable; UnicodeDecodeError/JSONDecodeError and
  other ValueError/TypeError paths are caught by classify at :341-343. Depth refusal happens
  before deep well-formed arrays reach the parser. No raw parser escape granting credit found.

All raw refusal paths precede the first chip_eligible=True update at :345. Later schema and
identity checks remain in frames_for and admitted_decision. V1 checks exact received members
before constructors and preserves the reason-string exception; v2 uses the existing public
validate_decision codec plus provider/delivery checks. Shared TimingRecord is constructed
before completed/budget/accounting checks. Kernel replay binds legal applied actions and
settlement at :258-303; no decoded raw-invalid stream can reach that credit boundary.

False-exclusion searches included exact-limit frames, ordinary JSON spaces/tabs, quoted
brackets/escapes, Unicode within strings, negative zero, bounded integers and finite exponent
forms. The new checks preserve the host's raw acceptance language subject to the declared
finite-number restriction. Existing model/codec validation remains unchanged. Reason-only
mismatch therefore reaches disagreement with chips preserved; actual baseline divergence
returns after chip eligibility at :349-351, before the blueprint-only river count at :374.

Consumer analysis distinguishes eligibility from successful campaign acceptance.
summarize at :397-411 retains missing/excluded/disagreement counts. Unsupported outcomes can
make its generic complete flag true, but tools/v0a_eval_panel_completion.py:345-348 requires
all primary classifications to be hits. Parent completion at :403-416 rechecks primary hits
and controls; accounting at :439-463 reconciles scheduled witnesses and missing outcomes.
No changed raw-refusal result can become a hit/completed primary through those consumers.

Coverage reconciliation and supplied execution evidence

The independent inventory covered the same producer -> framing -> parser -> records -> replay
-> classification -> summary/phase chain as deferred coverage.md. I did not use the parent
finding to choose the independent category. Its authorized later disposition identifies the
old normalization/bounds defect; the actual candidate diff closes that earlier boundary.

Frozen tests/test_eval_protocol.py:136-183 mutates actual v1 CHECK and v2 premium-divergence
Session captures, checks the host decoder, and asserts public classify outcomes and causes.
The exact-frame-limit positive compares the whole classification result, preserving chips.
The tests prove premium v2 preflop raising occurred at :68-72 rather than merely relabeling
v1 output. :185-214 compares JSON boundaries with the unchanged host decoder for depth 8/9,
640/641-digit integers, escape tracking, duplicates, encoding, constants and size boundaries.
The shared expected value comes from the real host decoder, not a copied candidate parser.

The independent false-exclusion inspection is broader than the executed positive cases.
In particular, the Unicode helper fixture at :194 uses json.dumps with default ensure_ascii;
it tests an escaped Unicode value, not literal UTF-8 U+2028 bytes inside the JSON string.
Literal Unicode inside strings, escaped duplicate-key spellings, negative 640-digit success,
and all whitespace combinations are statically assessed, not individually executed by these
receipts. This is a nonblocking evidence limit, not proof of a product or acceptance defect.
A literal UTF-8 positive plus an escaped-key duplicate would be useful future regression cases.

The capture-cap negative also violates a per-frame bound. The claim explicitly acknowledges
that overlap and does not present it as isolated cap sensitivity or a naturally occurring
completed four-chip capture. The explicit capture predicate is directly visible at :185;
no unsupported claim of natural 2 MiB completed-hand coverage is needed for this correction.

Preservation coverage also includes frozen tests/test_eval_completion_tool.py:100-171:
real CHECK hit, off-pool default, changed-stack zero hits, real send failure, and a retained
reason relabeling whose chips remain eligible. tests/test_eval_agreement.py:264-322 separately
covers off-pool and unknown reasons; those constructed fixtures remain classifier evidence.

Supplied focused-receipt/result/journal records bind the exact candidate on CPython 3.14.6:
80 unittest cases across six suites, zero skips, pytest exit 0, source_verified=true.
Counts are 11 bridge, 29 panel tool, 8 export, 21 agreement, 9 completion tool, 2 protocol.
RED records bind the test-only child: two cases, zero skips, exit 1 and 27 assertion failures.
The reported 26 raw-capture failures are distinct from the one missing-helper seam assertion.
Frozen source relationships and receipt hashes verify. I inspected snapshot.ps1 and the
freeze utility as text only; no receipt-generating script was executed by this reviewer.

Design verdict and limits

SOUND: the correction installs one explicit byte-admission boundary before already existing
record, settlement, and agreement stages. It removes the lossy normalization responsible for
the supplied parent residual without moving agreement predicates into universal chip gates.
The small duplicated host contract creates a future drift risk, but direct frozen-host tests
and explicit pins make that obligation visible. Extracting a shared parser would require
sealed-producer changes and offers no demonstrated necessary correction for this candidate.
A broader replacement is not justified by the allowed evidence.

There are no required Critical/Important findings, so no required correction or finding
falsifier is asserted. The positive conclusion is falsified by a retained stream admitted
through classify that the frozen physical LF/JSON contract rejects, by a valid preserved
control losing chips solely to the new raw checks, or by a refused result reaching a primary
hit through an actual consumer. The reviewed source and supplied tests support none of these.

This review does not independently attest runtime receipts beyond their verified bindings;
it supplies static project reasoning plus executed utility facts. It does not establish
full-H agreement, strength, timing adequacy, OS containment, or a new retained measurement.
Existing caller policy attribution/outer identity limits remain outside this two-file fix;
no broad universal host-equivalence claim is made for the later decoded semantic contract.
No adoption, broad-suite launch, retained phase, source/packet/ledger/ref write, or push occurred.
Only the sealed inventory and this final report were written in the exclusive assigned scratch.
