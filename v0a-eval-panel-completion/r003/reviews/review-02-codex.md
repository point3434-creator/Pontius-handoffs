# Cold review 02 - Codex

Defect verdict: CLEAN.
Design verdict: SOUND for the bounded raw-frame correction.
No required correction survives this independent review.

Candidate: 7ca821802c949b047becf6599d603b3b63d51fa7
Parent: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Tree: 3d2fe79d2af20125e322dd4a668335e789810863
Ref: refs/heads/review/v0a-eval-panel-completion/r003
Manifest SHA-256: 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd
Packet: D:/Pontius-handoffs/v0a-eval-panel-completion/r003/

All source locations below refer to that candidate's raw Git blobs unless explicitly parented.
This is a static cold review with executed read-only identity utilities. It is not a new test run,
retained measurement, adoption decision, or assertion that every conceivable malformed input ran.

## Cold-input qualification and output discipline

I inspected inherited context before substantive review and read handoff.md first. No candidate
history, lane findings, verdicts, prior review conclusions or candidate test results were inherited.
No memory file, reviews directory, sibling scratch, other packet directory, progress, INDEX or
readiness file was opened. No other active reviewer's conclusions were received or inspected.

The inherited developer text did contain an injected MEMORY_SUMMARY v1. This is memory-derived
context, distinct from ordinary repository or tool instructions. It described six-max 100bb
preferences, offline training, exact ties/folded-player factors, immutable training milestones and
measured strength. It mentioned unrelated pilot/bucket scaling baseline-000 at 258.87 iterations/s,
ADR-0507 baseline-watch preparation/authorization, six-max architecture under 30 seconds, and
six-dealt contested-card evaluator stability/research ZIP. It also listed unrelated prior workspace
paths/dates and per-command Git safe.directory advice. None mentioned eval-panel-completion,
its r001/r002/r003 candidates, findings, verdicts or tests. I did not use this material as
review evidence. This exposure is disclosed so the coordinator can assess qualification.

The initial inventory was written and hashed before opening coverage.md or any checks/ file:
D:/Pontius/tmp/eval-completion-r003-review-02-74ab610d/inventory-02-codex.md
SHA-256: 8ded6e13365a5f42982f862b04dc02660db6e29842f3f77536ecb8c3eed10d6c
The inventory remains unchanged. The expressly allowed checks/parent-disposition.md was read only
after sealing; its prior-review paraphrases were permitted deferred evidence, not initial priming.

I read the generic code-verification skill for evidence grading. The using-superpowers skill
explicitly excludes dispatched subagents. One mistaken read of a nonexistent skill path failed
without exposing content. Initial mandated Python startup was denied by the sandbox; approved
escalated calls then ran read-only standard-library/Git utilities with that exact interpreter.
No automatic approval review rejected an action. No project code, tests, hooks or retained phase
executed. No source, packet, ledger, ref or other review output was written. No utility scratch
files were created. The only created files are this report and the sealed inventory in my exclusive
scratch directory. The directory itself was created for those two authorized outputs.

## Executed identity and evidence checks

Read-only Git rev-parse, show, diff-tree, diff, grep and cat-file established the exact ref,
sole parent, tree and two changed paths: eval_agreement.py and test_eval_protocol.py.
Standard-library subprocess/hashlib/json/pathlib utilities used only:
C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe -B -P -
Its reported version was CPython 3.14.6. Git resolved to C:/Program Files/Git/cmd/git.exe;
subsequent utilities used that absolute executable, with per-command safe.directory settings.

Candidate and parent manifests were regenerated from raw blobs, sorting complete digest/path/LF
rows bytewise. Both exactly match the supplied files. Parent manifest SHA-256 is
6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5, covering the parent's exact
three-file delta. All 51 dependency hashes and their named packet copies matched. All 32 supporting
file hashes matched after deferred admission. Brief, supporting-list and coverage hashes match
handoff.md; coverage is 27cfa20b93cabeacbf0d36e91a2448bac2da1f4f45b435e8918fc4fd5cc6a659.

Raw line counts reproduce checks/scope.json: 2093 production and 1999 test lines for the stated
whole-slice files. This is below the 3000 production ceiling, above the disclosed 1200/600 working
figures. Candidate source and tests are LF-only, BOM-free, without trailing whitespace or lines
over 100 columns. The inventory satisfies the same hygiene. Final report hygiene is checked below
by the coordinator-facing utility output, after this file is written.

RED candidate 81a5aaf5670c9f495cc03dbb26796699a11cffa1 has the declared parent and only the protocol
suite delta. Its protocol test blob equals the final candidate; its classifier blob equals the
parent. Supplied RED result: two unittest cases, zero skips, 27 failure labels and zero errors.
Those comprise 26 malformed-capture exclusions and one missing-helper assertion; the latter is
not a separate behavioral counterexample. RED result digest matches its supplied journal.

Supplied focused receipt and journal bind this candidate, Python 3.14.6, scrubbed environment,
-B -P, warning gates and the parameterized harness. They report six suites, 80 unittest cases,
zero skips, pytest exit 0 and source_verified=true. Result digest matches the journal:
906fe72e7ee8c2229e0b50ea5ec46040819a0f2312fa116864fb821d0a863633.
I inspected the harness, unchanged registration and snapshot script as raw text. Receipt contents
are supplied execution evidence; I independently executed their hash/consistency checks, not the
reported suites or the snapshot script. No snapshot or shared-scratch directory was inspected.

## Top-down obligation assessment

1. Failure before credit. accepted-design.md:219-230, accepted-brief criterion 7 and
   completion-brief mechanism 7 require unusable retained frames to exclude the attempt.
   eval_agreement.py:183-188 now enforces decoded capture size and final LF and splits only
   physical byte LF. Every frame goes through decode_frame before schema or settlement replay.
   classify:329-343 contains that path inside its exclusion handler; chip credit starts at 345.
   Invalid UTF-8, syntax, duplicates and numeric refusals are ValueError-family failures; the
   decoder translates parser RecursionError into Unusable. Neither success update runs first.
   Falsifier: a retained CRLF/oversized/unfinished capture reaches chip_eligible=True. No such
   route remains in the inspected code; actual-capture tests assert exclusion and chips=None.

2. Exact raw host contract. r003 brief identifies tools/v0a_table_host.py:52-90 and 512-536 as
   JSON/physical-frame authorities. eval_agreement.py:120-151 matches the host's 16384-byte
   LF-inclusive frame limit, CR/BOM refusal, quote/escape-aware depth 8 and 640 signless integer
   digits. Base64 capture size is bounded at 2097152. Empty physical frames fail JSON parsing.
   The finite_float/reject_constant hooks preserve the expressly stricter finite-number rule.
   Non-LF Unicode separators no longer create records; raw UTF-8 decoding remains strict.
   Falsifier: host-rejected raw framing/JSON survives into semantic admission, or legal padding
   at exactly 16384 bytes changes a valid classification. Inspection and supplied cases agree.

3. Preserve valid outcomes. accepted-design.md:232-243 and r003 brief preserve CHECK hits,
   off-pool defaults, reason-only disagreements and completed v2 prefix divergence with chips.
   Raw parsing never normalizes a reason or action. admitted_decision:53-87, replay:254-303 and
   post-admission agreement:344-393 have unchanged bytes. Exact field sets precede constructors;
   v2 uses validate_decision, v1 retains unknown string reasons for later disagreement. Baseline
   return follows replay/settlement and precedes the exactly-one-river agreement restriction.
   Actual CHECK and premium preflop-raise v2 controls are explicit in test_eval_protocol.py:61-73.
   Exact-frame-limit variants compare the entire classification dictionary to the control.
   Existing real controls in test_eval_completion_tool.py preserve off-pool, changed-stack and
   relabeled-reason chips. Fixture tests separately assert fixed -2 CHECK and -4 all-in chips.
   Falsifier: legal raw spelling changes these outcomes or a reason disagreement erases chips.

4. Producers and consumers. Raw host stdout is retained by table_session's hand-result producer,
   then Session.run supplies completion.play:282-311. This is the only production classify call
   found in frozen source/tools. Inputs bind artifact, teacher, board, hands and stacks outside
   raw admission. frames_for calls decode_frame for every physical line; there is no bypass.
   Completion.agreement:345-348 requires each primary to be a hit. complete:402-416 rechecks
   primary and control outcomes; accounting:439-463 reconciles scheduled and observed attempts.
   summarize:397-411 counts excluded and missing outcomes separately. A generic unsupported
   outcome can be resolved without being a hit, but these consumers independently require every
   primary to hit. Falsifier: a malformed/excluded attempt makes the primary campaign complete.
   No newly reachable path was found. This is a source-backed scope statement, not an exhaustive
   audit of every unchanged solver, exporter or possible future caller.

## Oracle and coverage challenge

The independent inventory and deferred coverage agree on the missing raw-input category. The
parent disposition's framing residual is closed by byte-preserving LF splitting and bounded
admission. Its parser-recursion observation is closed structurally by the depth bound and local
RecursionError conversion. No parent verdict was adopted as proof of this candidate.

The protocol suite first obtains actual Session captures. It confirms a v1 hit and an actual v2
baseline preflop raise before mutations. Mutating only child_stdout_base64 holds envelope,
actions and settlement fixed, making the exclusion requirement discriminating: downstream replay
cannot detect a framing defect by itself. Rejection assertions require excluded, false chip
eligibility, absent chips and a retained cause. They do not directly assert agreement_eligible
for every rejection, but the inspected exclusion path returns its initial false value unchanged.

The test host_accepts wrapper calls the unchanged host decoder and implements physical LF and
capture bounds itself. It does not execute ChildConnection.read_stream for each mutation. I
checked its complete-buffer language against read_stream: LF-inclusive size and unfinished
suffix behavior agree for the supplied finite byte streams. This is adequate for raw admission
but does not establish concurrent I/O, read chunk timing, process containment or natural corruption.
The true decoder is an independent existing authority, not the candidate's expected-value helper.

Direct decoder tests pair 640/641 integer digits, depth 8/9 and frame sizes 16384/16385. They cover
negative over-limit integers, signed zero, finite exponent notation, quoted braces and escaped
quotes, duplicate keys, constants, BOM, CR, invalid UTF-8 and extra JSON documents. The finite
exponent-overflow refusal is deliberately stronger than host.decode_json; the test labels this.
The direct Unicode positive is serialized with json.dumps default escaping, so it establishes
escaped Unicode acceptance, not a separately executed raw non-ASCII UTF-8 positive. Raw decoding
supports that path statically; the packet is not an exhaustive JSON-language equivalence proof.

The over-capture test also violates per-frame size. It proves exclusion of that supplied stream,
not isolated execution of the capture-only predicate or acceptance at exactly 2 MiB. This limit
is accurately disclosed in coverage.md. No normal completed four-chip hand is asserted to reach
that size. The depth-2000 fixture is refused by pre-scan, so it does not demonstrate organic entry
into the RecursionError handler. The handler's correctness is static evidence, and no injected
parser-recursion execution is claimed. Neither limit leaves a demonstrated successful-credit
path or warrants inventing a blocking defect.

The supplied six-suite focused result includes retained fixture and actual-host checks; those
roles stay distinct. The new raw cases are subtests inside two unittest cases. No matrix count
is inflated into additional independent runs. Positive controls and invariant-derived exclusions
avoid an always-reject implementation passing the suite.

## Design and remaining boundaries

SOUND: a small raw decoder and one call site place the lost invariant before decoded-record
validation. The correction is 37 added/4 removed production lines plus 81 test lines. It avoids
changing the sealed producer, codec, game or execution owner. Replacing the whole classifier is
not justified by this packet. Maintaining host-equivalent predicates in the library creates a
future synchronization obligation; the frozen dependency pins and host-oracle cases make that
obligation explicit. A host framing contract change must revisit both the adapter and its tests.

The parent-disposed strategy attribution, external identity binding, unused outer fields and
generic summary interpretation remain interface limits for future callers, not new r003 findings.
Current production play fixes blueprint-v1 and passes the bound deal/artifact values. This review
makes no Slice B attribution guarantee, full-H host claim, teacher-strength claim or timing claim.

No required findings remain. CLEAN is the defect verdict for these frozen bytes under the stated
scope and evidence limits. Two qualifying cold passes still precede broad testing; exact adoption
and each retained phase require their separately authorized next steps. This report grants none.
