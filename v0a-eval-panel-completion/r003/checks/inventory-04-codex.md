# Independent cold inventory 04 - Codex

Context probe: CONTEXT_PROBE_NONE, stated before any packet or source was opened.
No inherited memory summary, project history, candidate verdict or finding was present.
Only generic instructions, the user's review request and environment were inherited.
This inventory precedes coverage.md and every checks/ input. It is sealed without them.

Candidate: 7ca821802c949b047becf6599d603b3b63d51fa7
Parent: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Tree: 3d2fe79d2af20125e322dd4a668335e789810863
Manifest: 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd

## Authority and scope

Read handoff first, then candidate, manifest, brief, supporting list and named inputs.
The current brief and r003 authorization bound this FIX to raw-frame admission and
protocol tests. Accepted brief/design and completion brief supply the wider invariant.
Pinned README/workflow supersede older dual-runtime language: Python 3.14.6 only.
The user's independent Codex assignment overrides the packet's Claude role wording.
No execution, adoption, broad tests, retained phase or fourth round is authorized.

Verified ref, sole parent, tree and exact two modified paths using frozen Git objects.
Rebuilt both manifests by SHA-256 of raw blobs, ordinal sorting full ASCII digest/path
rows with LF. Candidate manifest matches. Parent's three-file delta is against
449a2a3c1fa1f5a7f5f04adca32e499faaf81e13 and matches its supplied manifest:
6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5.
Every dependencies.json pin matches its raw blob, including explicit evidence-repository
pins; only their named blobs were accessed, never the other packet directories.
Initial supporting inputs, brief and supporting-list hashes match.
No worktree source, memory, reviews, ledger, history, index or launch log was read.
Commit metadata and the required parent delta were read solely for identity verification.

## Top-down contractual requirements and implementation map

All source locations below refer to the candidate, not worktree line numbers.

R1. Host-invalid physical framing or JSON must produce no chips and no agreement.
    eval_agreement.frames_for:183-251 calls decode_frame before replay or credit.
    classify:318-348 initializes excluded/no chips and credits only after its try gate.
R2. LF is the physical separator. Reject unfinished frames, raw CR/CRLF, BOM and invalid
    UTF-8; Unicode/control splitlines separators cannot create independent messages.
    frames_for:184-187 splits bytes on LF; decode_frame:122-149 validates each frame.
    Host oracle: v0a_table_host.read_stream:512-537 and decode_json:52-90.
R3. Retained stdout <=2097152 bytes; every LF-inclusive frame <=16384 bytes.
    frames_for:185 and decode_frame:122; host stream capture and pending limits agree.
    Boundaries include exact cap, cap+1, final terminator, trailing bytes and blank frames.
R4. JSON depth <=8 outside quoted strings, integer tokens <=640 digits excluding minus,
    no duplicate members or nonstandard constants; decoding/parser failures exclude.
    decode_frame:125-151, unique_object:102-107, reject_constant:110-111.
    Challenge escaped quotes/backslashes, arrays/objects, sign, duplicate decoded keys,
    invalid UTF-8, multiple JSON roots, scalar roots and recursion.
R5. Preserve the existing finite-number rule, stricter than host float parsing.
    finite_float:114-117 refuses overflow-to-infinity; json constants also refuse.
    Host floats=True uses float and is not itself a finite-float reference.
R6. Nested outcomes and failures precede agreement. Missing/extra attempts, nullable
    failures, truncation, failed exit, incomplete hand/closure and unsettled outcomes
    exclude with causes. classify:321-343; clean:90-95; frames_for:236-250.
R7. Wire identities, exact shapes, ordered event/action pairs, v1 model and v2 codec
    contracts must hold before credit. frames_for:189-235, bind_identity:154-180,
    admitted_decision:53-87. No normalization/default can hide a missing wire field.
    Unknown string selection reasons deliberately remain agreement disagreements.
R8. Replay the applied history through the kernel; reconcile actual card settlement.
    replay:254-303 checks wrapper stacks/button, action types/order/origin, terminal,
    payouts/stacks/pots, final event count and showdown rank source.
R9. Outcome and agreement are separate. Valid prefix-diverged v2 baseline keeps chips.
    classify:345-351 returns baseline unsupported before the blueprint river predicate.
    Blueprint CHECK hit, raise hit, off-pool default and reason disagreement stay distinct.
R10. Successful agreement requires exactly one controlled river at the declared key,
     selected action equal to replay/lookup/teacher, and correct retained reason.
     classify:352-393; PreparedBlueprint.action_for; eval_bridge.root_key/replay_root.
     Pre-river defaults are checks, not agreement hits. Wrong root cannot be a hit.
R11. Each scheduled attempt has one disposition; missing/excluded/disagreement remains
     visible. summarize:397-411 supplies counts; unsupported is not itself failure.
     Therefore callers must bind the required population rather than trust complete alone.
R12. Real host witnesses, immutable teacher/wire identity, full H and complement accounting
     remain inherited requirements. completion.teacher_input:229-255, agreement:314-373,
     witnesses:149-180 enforce admitted population and first collision-free witnesses.
     Proper-subset controls and real-host subsets cannot certify full-H execution.
R13. Actual public provider enumeration is separate from real-host observation.
     Accepted design sections 4-5 and completion brief items 3-5 remain constraints.
     Solver/export arithmetic and provider/host/session contracts are unchanged by FIX.
R14. One parent owns admission/result/journal; worker reuses run context and real Session.
     completion.play:282-311 binds cwd/context; Session.run/prepare supplies producer.
     eval_panel.main:618-670 calls finish_run; execution:122-162 writes result and journal;
     status_generation:14-79 validates/renders run metadata without reclassifying outcomes.
R15. Scope, evidence and acceptance authority must remain precise: exactly two changed
     files, unchanged registration/dependencies, <=3000 whole-slice production lines,
     disclosed working figures, independent RED before edit and integrated focused GREEN.
     Two qualifying cold passes precede broad verification; no runtime result is inferred
     from a cold static pass. Coverage claims must distinguish fixtures and host controls.

## Raw inputs, producers and every discovered consumer

The Session producer retains stdout from ChildConnection.read_stream, applies actions
through WireConsumer/Table, finalizes cleanup, then places the hand in hands[*].result.
Session:240-315 retains capture/exit/failures; :317 onward settles outer completion.
WireConsumer.read:662-680 combines physical framing with host JSON/schema admission.
Raw stdout is base64 in a structured report; classifier caller supplies immutable blueprint,
teacher, board, actual private hands, stacks and strategy. These are distinct trust inputs.

Production chain:
Session.run -> completion.play -> classify -> returned host_attempt.classification.
agreement:345-348 demands hit for each primary. Off-pool, CHECK and changed-stack controls
have separate predicates at :362-366. summarize contributes agreement_summary at :367-373.
completion.complete:376-436 checks primary hits, schedule counts, controls and artifacts.
completion.accounting:439-463 binds schedule order/witnesses and reconciles missing outcomes.
eval_panel.supervise:519-528 computes phase_complete/accounting and changes success to failure.
eval_panel.main retains observations and artifacts, then execution.finish_run writes one
result and journal record. status_generation displays the parent status/summary; it does
not independently reconstruct host validity. No other production caller was found by
frozen Git grep across src, tools and tests.

Test consumers:
test_eval_agreement calls classify/summarize on explicitly constructed envelopes.
test_eval_completion_tool calls real play and classify, including post-send refusal and
reason-only mutation; later orchestration tests consume completion/accounting observations.
test_eval_protocol calls classify on real v1/v2 controls and altered retained streams,
plus direct decode_frame comparisons with host.decode_json.
tests/cases.json registers the existing protocol suite; test_pontius is the harness.
A Git grep invocation first failed from argument quoting; corrected read-only invocation
completed. This was a utility error, not a product check or permission limitation.

## Potential successful-credit and acceptance paths to challenge

- Parser accepts altered separators, padding, depth, huge tokens, duplicates or encoding
  that host framing rejects: malformed capture can otherwise reach chip and hit credit.
- Tests reject an oversized capture only because its first frame is oversized. That does
  not independently discriminate the aggregate-capture gate.
- A host_accepts helper that repeats LF/capture predicates is not an executed read_stream
  oracle. Check what actual producer behavior the deferred evidence establishes.
- Exact frame/depth/digit boundary positives must remain accepted; rejection-only checks
  can hide over-restriction. Escaped Unicode inside strings differs from a separator.
- Raw valid JSON need not be a valid frame object or valid protocol sequence. Decoder
  equality alone cannot prove full classifier behavior or all successful-credit consumers.
- Constructor normalization, equal bool/int/float values, absent fields, identity mismatch,
  event pairing and settlement mismatch must not manufacture a successful decoded record.
- Agreement-only discrepancies should not erase completed chips. Baseline preservation
  requires an actual completed v2 divergence, not just passing a baseline strategy flag.
- summarized complete permits unsupported; primary worker and parent acceptance predicates
  must still demand declared-pool hits, not merely a complete observed count.
- RED must fail for behavioral contract assertions against parent production with new
  tests, not only absence of a newly named helper. GREEN must bind integrated bytes.
- Receipts and source/plan hashes identify evidence, but do not turn implementer-authored
  cases into an independent oracle or a full population/OS-boundary proof.

## Seal and limits

This inventory was derived without opening coverage.md or any checks/ file.
Hash this exact LF, UTF-8 without BOM file before deferred inputs, and do not revise it.
The review is static: no Python, project imports, tests, hooks or source execution.
Utilities are PowerShell/.NET and read-only absolute-path Git. No utility files retained.
Only inventory-04-codex.md and review-04-codex.md may be written in exclusive scratch.
