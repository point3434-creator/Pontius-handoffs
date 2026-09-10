# Independent cold review 04 - Codex

Defect verdict: CLEAN.
Design verdict: SOUND.
Required findings: none.

Candidate: 7ca821802c949b047becf6599d603b3b63d51fa7
Manifest SHA-256: 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd
Parent: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Tree: 3d2fe79d2af20125e322dd4a668335e789810863
Packet: D:/Pontius-handoffs/v0a-eval-panel-completion/r003/
Reviewer scratch: D:/Pontius/tmp/eval-completion-r003-cli-04-72ad817e

This is one independent static cold pass of the authorized two-file raw-admission FIX.
No required correction remains on the reviewed contract. This verdict does not establish
full-H agreement, authorize broad tests by itself, or authorize adoption or a retained phase.

## Context and input-order disclosure

CONTEXT_PROBE_NONE was stated before the first packet/source read. The inherited context
contained generic tool/safety/workflow instructions, environment and this review assignment;
it contained no memory summary, project history, candidate verdict or substantive finding.
No memory facility, other reviewer output, reviews directory, sibling scratch, coordinator
launch log, progress/index/readiness file, worktree source or project history was accessed.

Read handoff.md first, then candidate.json, manifest.sha256, brief.md, supporting-files.json,
the named inputs and frozen source. Independently inventoried 15 requirement groups, raw
boundaries, producers, consumers and possible successful-credit paths. Wrote and hashed
inventory-04-codex.md before opening or hashing coverage.md or any checks/ input.

Inventory SHA-256, sealed before deferred input:
924ebb2c8da26352778b5e237555b9aa357b9941636b80b9a41fa2ba44186caf

Only afterward read the deferred coverage/checks, including the explicitly permitted parent
disposition, repair plan and diagnostic copies. The parent disposition contains prior
verdicts and finding summaries; that is the sole such exposure and occurred after sealing.
It was used to reconcile closure, not to construct the initial inventory. References inside
those copies to earlier packets/reviews were not followed. The old diagnostic's external
capture was not opened. Named dependency blobs in the evidence repository were read only
to verify their explicit pins; their containing packet directories were not accessed.

The user's Codex assignment and exclusive output path override the handoff's Claude/reviews
placement wording. No other output-policy deviation occurred. PowerShell/.NET and absolute
read-only Git were the only utilities. No Python or project code executed. No tests, hooks,
Git mutations, publication, packet/source/ledger edits or delegation occurred. No utility
files were created. One read-only grep initially failed because of argument quoting and
was corrected; no required check was blocked by permissions. Large tool outputs were
occasionally truncated; targeted reads and structured extraction recovered material evidence.

## Identity, scope and evidence integrity

Verified the review ref resolves to the candidate, its sole parent is the named base, and
its tree matches candidate.json. The exact delta is two modified regular source/test paths:

- src/pontius/eval_agreement.py: +37/-4, SHA-256
  9187fd8d667776902962c943e1d4e282771f7120f519a9ed4f2e6724b4d3f008
- tests/test_eval_protocol.py: +81/-0, SHA-256
  4ddab49405e1b4111c975c4b64b5168e0883fd60ada06f4c2f7236c34c28cdd3

Recomputed the manifest from raw Git blobs, sorting whole digest/two-space/path/LF ASCII
rows bytewise, and matched its exact file digest. Also reconstructed the parent's three-file
manifest against its sole parent 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13:
6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5.
The parent delta contains eval_agreement.py, test_eval_protocol.py and tests/cases.json.

All 51 dependency pins match raw blobs at their named commits. Candidate identity and all
dependency pins were additionally checked with Git replacement objects disabled. No source
bytes were substituted from a checkout. All 32 supporting-file hashes match; the brief,
supporting-list and deferred coverage hashes match the handoff. The dependencies are direct
semantic pins, not a claim of complete transitive closure.

Whole-slice raw-blob counts match scope.json: 2093 production and 1999 test lines across the
four production and six test files. Production is 907 lines below the 3000 hard ceiling.
Both 1200/600 working figures are exceeded and explicitly disclosed; those figures are not
new authority gates. Frozen reference searches found no additional eval-bridge caller in
the searched src/tools/tests and experiment Python paths. The ten counted files are LF,
without trailing whitespace or lines over 100 columns; changed files have no BOM.
Host/session/codec/kernel/solver/export/ownership code and test registration are unchanged.

## Top-down contract assessment

Frozen locations below are at the candidate unless explicitly labeled otherwise. The sealed
inventory contains the full initial R1-R15 requirement enumeration and consumer map.

1. Raw admission before credit, physical LF and byte bounds (R1-R3).
   eval_agreement.py:183-187 decodes retained base64, bounds stdout at 2097152 bytes,
   requires final LF and splits bytes only on LF. Every resulting LF-inclusive frame
   passes decode_frame:120-151 before record construction or replay.
   Host read_stream at tools/v0a_table_host.py:512-537 captures the same maximum, rejects
   unfinished pending bytes, and imposes a 16384-byte LF-inclusive frame maximum.
   The classifier checks 0 < frame length <=16384 and final LF at :122-123.
   Alternative Unicode/control separators cannot create new physical messages.
   At most they remain within a frame for JSON decoding to reject or accept as string data.
   CR anywhere and a leading UTF-8 BOM are refused before decoding, matching the host.
   A blank physical line and trailing extra JSON fail before successful credit.

2. JSON acceptance and refusal (R4-R5).
   decode_frame:125-144 matches the frozen host's quote/escape-aware depth scan and
   640-digit signless integer-token rule. Both use UTF-8 decode, json.loads and duplicate
   object-member checks. The classifier rejects nonstandard constants and additionally
   rejects finite-syntax floats that overflow to infinity, preserving the prior restriction.
   Depth, frame length and integer checks happen before expensive semantic admission.
   RecursionError from JSON parsing becomes Unusable, a ValueError subtype, and reaches
   classify's excluded return at :341-343. Syntax/UTF-8/type/base64 failures also reach it.
   No normalization or relaxed JSON entry point bypasses this path in a discovered caller.

3. Received records, retained outcome and settlement (R6-R8).
   classify:321-340 validates the outer single-hand outcome and nested result before
   frames_for. Exact fields, identity, ordered event/action pairs, completed timing,
   preparation absence and v1/v2 model/codec checks remain in :53-87 and :189-250.
   replay:254-303 reconstructs public history through NoLimitBettingState, checks action
   order/origin and terminal state, and recomputes settlement from the supplied actual deal.
   Event count and rank source are checked before :345 first makes chip_eligible true.
   The change touches neither these later predicates nor chip arithmetic.
   Trusted caller input validation is distinct from validation of received wire values.

4. Separate chip and agreement outcomes (R9-R10).
   A completed v2 baseline returns unsupported with replayed chips at :349-351 before
   blueprint exactly-one-river checks. This preserves actual early prefix divergence.
   Blueprint comparison at :352-393 checks replayed state/action, PreparedBlueprint lookup,
   retained reason, exact declared root and teacher action. CHECK equality alone is
   insufficient: a relabeled hit/default remains disagreement. Unknown string reasons
   intentionally reach that agreement diagnosis instead of becoming successful defaults.
   Off-pool defaults remain unsupported. Pre-river records are checked, not counted as
   separate agreement observations. Raw refusal happens earlier for both strategies.

5. Population, all acceptance consumers and ownership (R11-R14).
   The sole discovered production classify caller is completion.play:307-311, after real
   Session.run, with caller-bound wire, teacher, board, private hands and stacks.
   completion.agreement:345-348 demands hit for every primary. It validates off-pool,
   CHECK-hit and changed-stack controls separately at :362-366, then emits the summary.
   summarize:397-411 counts one disposition and keeps missing/disagreement/excluded visible.
   Its complete flag can be true for unsupported outcomes. It is therefore insufficient
   as primary acceptance alone, but the actual worker and parent do not use it that way.
   completion.complete:403-416 independently requires each primary classification be hit
   and checks controls/counts; accounting:439-463 checks admitted ordering/witness binding.
   eval_panel.py:519-528 uses phase_complete/accounting and downgrades failed completion.
   Its main:649-668 retains outputs and calls execution.finish_run:122-162 once.
   The latter persists result status/summary and journal identity; status_generation:14-79
   validates/displays that metadata without reinterpreting chip or agreement eligibility.
   No other direct caller or independent success sink was found in the frozen searches.

   The unchanged export boundary in eval_bridge.py:363-421 binds teacher/wire identities,
   complete decoded key/action membership and separate actual BlueprintProvider.propose
   checks over the root universe. completion.teacher_input:229-255 binds producer/plan
   inputs; witnesses:149-180 preserves first compatible draws and explicit missing hands.
   These prevent a subset/control artifact from supplying full-H acceptance. Their source
   connections were traced; this FIX review does not re-certify all solver mathematics.

6. Scope, runtime, evidence and authorization (R15).
   Exact two-file scope and line totals pass. Pinned workflow/README supersede the older
   dual-runtime requirement. RED/GREEN evidence is assessed below. This independent pass
   is only one Tier C pass; it neither counts nor inspects another reviewer's work.
   The authorized stopping/adoption/retained-phase restrictions remain in force.

## Independence and scope of RED/GREEN evidence

RED receipt binds 81a5aaf5670c9f495cc03dbb26796699a11cffa1. Verified that its sole parent
is r002 and its entire delta is test_eval_protocol.py. The RED test hash exactly matches
the final candidate, while its eval_agreement hash matches parent production:
c2383c54fb5959326612546d6a28fe7d9ba7e092907afb06bc64905a986abd83.

The retained RED result reports two unittest cases, no errors/skips and 27 failures:
26 real-capture exclusion assertions plus absence of the new decoder seam. The missing
helper is a structural failure and is not an additional product counterexample. Each of
the 13 behavioral mutations fails under v1 and v2: nine separator substitutions, CRLF,
overlong frame, oversized capture and overlong integer token. RED output shows v1 still
credited hit/chips=-2, and actual premium-diverged v2 still credited unsupported/chips=-4.
Thus RED is not merely a missing-symbol check and does not replace real v2 with a label.

The new test creates actual Session controls at test_eval_protocol.py:43-71. It requires
baseline preflop bot raising and a v2 envelope. Retained-byte mutations occur afterward,
without replacing successful transport, settlement or cleanup. Their reachability is the
public retained-envelope classifier boundary; they do not claim natural child corruption.

The GREEN receipt binds the exact candidate and reports exit 0, CPython 3.14.6, -B -P,
ResourceWarning escalation, explicit snapshot import paths and a scrubbed environment.
The six suite totals reconcile: bridge 11, panel tool 29, export 8, agreement 21,
completion tool 9, protocol 2; 80 unittest cases, zero skips. Pytest reports six selected
suite entries, not 80 pytest cases. The journal's result hashes match the supplied results.
The snapshot script and unchanged test harness explain the reported source_verified=true
and one result/journal record. This review did not execute that script or inspect snapshots.

The journal timestamps place RED before the candidate commit/Green receipt. This supports
the documented sequence; receipts and Git timestamps cannot independently prove exactly
when an implementer's local edit occurred. The reported source_verified and actual snapshot
source_sha256 values are execution evidence from the supplied run, not measurements made
by this review. Dependency/raw-blob hashes were independently recomputed here.

The copied parent diagnostic supplies corroborating four-case rejection evidence and its
own result/journal hash binding. It reused an earlier capture rather than launching a host.
Its original capture path is outside allowed inputs and was not opened; I do not claim
independent reproduction of that capture's provenance. The new RED's actual controls and
frozen test-only delta are the stronger evidence for this candidate's correction.

## Nonblocking evidence observations and acceptance-language limits

These are limits/advisory observations, not required findings or new acceptance gates.

E1. Aggregate capture-bound discrimination is limited.
Frozen location: test_eval_protocol.py:163; host_accepts:140-149.
The oversized fixture prepends 2097152 spaces, so it also violates the per-frame limit.
Deleting only the aggregate guard could leave this regression green because another guard
rejects it. The test helper itself copies the total-size predicate rather than exercising
ChildConnection.read_stream. Coverage explicitly acknowledges the overlap. Static inspection
establishes the required guard and its pre-parser location at eval_agreement.py:185; no
remaining successful-credit counterexample was found. Do not describe this fixture as
isolated verification of the 2 MiB guard or a natural completed hand at that size.
A discriminating guard check would use individually valid LF frames crossing the aggregate
cap and independently observe refusal before JSON/schema work, without fabricating a
successful hand. A valid exact-cap positive would need a justified protocol population.

E2. Decoder differential evidence has a bounded domain.
Frozen location: test_eval_protocol.py:185-214.
Seven valid and fourteen invalid raw cases compare with the unchanged host decoder.
They exercise exact depth/digit/frame boundaries, quotes/escapes, constants, duplicates,
invalid UTF-8 and JSON syntax; exponent overflow is a classifier-only stricter negative.
The host decoder and classifier share Python's UTF-8/JSON/int/float implementations and
nearly the same scanner algorithm. The oracle is independent of the changed classifier
entry point, not an independent parser implementation or exhaustive acceptance proof.
The actual-capture positive at 16384 bytes compares the entire classification including
chips, which is stronger than decoded-object equality alone.

The Unicode-positive fixture uses json.dumps with default ensure_ascii=True. It exercises
escaped Unicode string content, not literal multibyte U+2028/U+2029 inside a raw JSON string.
The invalid separator fixtures do include literal encoded separators between messages.
Static inspection shows the new byte-split path preserves literal Unicode string content;
there is no corresponding runtime positive receipt here. Adding one would improve symmetry.

host.decode_json alone accepts some non-LF inputs because read_stream/WireConsumer own
framing. decode_frame alone is not a full stream validator either; frames_for guarantees
one physical frame per call. Claims of matching acceptance must therefore compare the
composed framing-plus-decoding paths, and retain the explicit finite-number exception.
They cannot mean that these two helper functions accept every identical arbitrary byte
argument. I found no mismatch on the actual physical-frame domain relevant to credit.

E3. Preservation and wider evidence claims remain narrow.
Unchanged tests cover off-pool defaults, CHECK/raise hits, reason-only disagreements,
kernel settlement, missing outcomes and later acceptance accounting. The focused receipt
does not retain a separate complete positive raw capture for each assertion; execution
details rest on the frozen tests and their logged success. Shared poker kernel/ranker
logic does not independently establish physical poker correctness or teacher strength.
No full-H host census, broad run, timing adequacy, resource containment campaign, complete
transitive dependency proof or Slice B policy-attribution assurance follows from this pass.

## Deferred reconciliation and design judgment

The sealed inventory's principal risks match the deferred category: byte normalization
and weaker raw limits precede otherwise valid parsed records. The former splitlines path
is removed; one explicit bounded raw decoder now sits before both chip and hit credit.
The permitted parent framing finding is closed by the source change and matching behavioral
RED/GREEN cases. Its parser-recursion issue is also closed by pre-parse depth rejection and
the explicit RecursionError translation. No new material residual was established.

The inventory independently identified the aggregate-test overlap, composed-oracle limit,
unsupported-summary interpretation and baseline-preservation boundary. Deferred coverage
discloses the first two limits and the parent disposition discusses the latter boundaries.
I evaluated them against frozen callers instead of accepting the disposition as proof.
A generic summary can resolve unsupported observations; actual primary acceptance still
demands hits. Caller strategy/external identity and unused outer fields remain explicit
interface limits, with no additional successful-credit defect demonstrated in this FIX.

SOUND is appropriate for the authorized boundary. Raw bytes, parsed records, settlement
and agreement now have an explicit order. The local helper closes the demonstrated loss
of raw distinctions without altering sealed producers or broadening into a protocol
framework. Duplication of the frozen host scanner creates a future drift risk; its pins
and direct differential cases make that risk visible. A shared-parser extraction would
change sealed ownership/scope and is not warranted by an unresolved defect in these bytes.

## Deliverables and remaining limits

Only these two files were written in the exclusive scratch directory:
inventory-04-codex.md and review-04-codex.md.
Both use LF, UTF-8 without BOM, no trailing whitespace and at most 100 columns.
The inventory remains byte-identical to its pre-deferred seal. The review hash is supplied
with the final response after writing, avoiding a self-referential hash inside this file.

No permission limitation prevented a required static check. No new execution evidence was
generated. CLEAN means no required correction survived this independent bounded review;
it does not mean every possible stream was executed or that future consumers are verified.
