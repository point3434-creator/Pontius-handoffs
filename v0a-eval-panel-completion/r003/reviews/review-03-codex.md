# Independent cold review 03 - Codex

Defect verdict: CLEAN.
Design verdict: SOUND.
Required findings: none. No material r003 residual identified.
This is one independent cold pass, not a disposition for other reviewers or adoption.

Candidate: 7ca821802c949b047becf6599d603b3b63d51fa7
Manifest SHA-256:
1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd
Parent: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Tree: 3d2fe79d2af20125e322dd4a668335e789810863
Packet: D:/Pontius-handoffs/v0a-eval-panel-completion/r003/

All source locations below refer to raw blobs at the candidate unless stated otherwise.
No source citation refers to worktree bytes.

## Context, independence and input order

CONTEXT_PROBE_NONE was stated before opening handoff.md or any source/packet input.
I inspected my inherited conversation context and found no memory summary, project
history, candidate verdict or finding. Generic instructions and the review assignment
were present. No memory system or project history was consulted to perform the probe.

I read handoff.md, the initial identity/manifest/brief/supporting list, named inputs/,
and permitted frozen source. I derived the host raw acceptance language first, then
traced normalization, typed admission, replay and all located credit consumers.
The independent inventory was written and hashed before any coverage.md or checks/
bytes were opened, including for hashing. It remains unchanged after that seal.

Sealed inventory: inventory-03-codex.md
Bytes: 13099
SHA-256:
178e8d8f6502ad649c463c41893bb271c125327c152daf7b4a8782887f7e3eb4

Only after sealing did I open coverage.md and the listed checks, including the explicitly
allowed parent disposition, repair plan and diagnostic copies. That disposition contains
summaries of earlier findings; this was a permitted deferred exposure, not inherited
context or input to my independent inventory. No original reviewer output was opened.
Earlier authorities and their historical references were exposed through named inputs/
only. Three explicitly pinned handoff-repository blobs were read for hash/copy verification;
I did not navigate their packets or follow historical references.

No delegation, project execution, tests, Python invocation, Git mutation, publication,
source/packet/ledger write, memory access or sibling scratch access occurred.
I did not read coordinator launch logs, histories, progress, index or readiness files.
Source searches used frozen Git src/, tools/ and tests/ paths. Initial searches returned
matching test lines, which are allowed source inputs; they returned no deferred checks.

Only the two authorized Markdown files were written in the exclusive scratch.
No utility files were retained or created. Read-only Git stdout was captured as bytes
in memory and hashed with PowerShell/.NET. A malformed read-only Git search failed;
a large inventory write attempt failed without creating the file, and a JavaScript
base64-helper attempt failed before writing. Smaller sequential writes completed the
inventory before its seal. These utility failures caused no substituted source reads,
input-order violation or extra output file. No permission restriction blocked a check.
Output-policy deviations: none.

## Frozen identity and scope verification

- Ref resolves to the candidate; raw commit has the named tree and exactly one parent.
- Exact candidate delta: src/pontius/eval_agreement.py and tests/test_eval_protocol.py.
  Both are modifications; registration and every other tree path are unchanged.
- Regenerated manifest from raw candidate blobs, sorting full lowercase digest/path
  rows bytewise (ordinal ASCII), with two spaces and LF per row. Exact bytes match.
- Independently regenerated the supplied parent manifest from its three-file delta
  against 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13. Exact bytes match.
  Parent manifest SHA-256:
  6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5
- All 51 dependency pins match raw Git blobs. Named dependency copies match those bytes.
  All 32 supporting-file hashes match; initial and deferred portions were checked in order.
  Brief, supporting list and deferred coverage hashes match handoff.md.
- Candidate classifier SHA-256:
  9187fd8d667776902962c943e1d4e282771f7120f519a9ed4f2e6724b4d3f008
  Candidate protocol-test SHA-256:
  4ddab49405e1b4111c975c4b64b5168e0883fd60ada06f4c2f7236c34c28cdd3
- Independently counted 2,093 whole-slice production and 1,999 test lines, matching scope.
  Production remains below 3,000. The 1,200/600 working figures are exceeded and disclosed;
  they are not substituted for the controller's hard ceiling.
- Delta is 37 additions/4 deletions in the classifier and 81 additions/0 deletions in tests.
  Both changed blobs are LF-only, BOM-free, without trailing whitespace or lines over 100.

## Bottom-up acceptance result

The governing raw oracle is tools/v0a_table_host.py:52-90,512-537,662-665.
The reader splits bytes only at LF, includes LF in the 16,384-byte frame bound,
rejects an unfinished EOF fragment and limits retained stdout to 2,097,152 bytes.
Its decoder rejects physical CR, a leading UTF-8 BOM, depth above eight outside quoted
text, more than 640 signless integer-token digits, duplicate decoded object keys,
invalid UTF-8/JSON and nonstandard numeric constants. JSON syntax remains the final
grammar authority after the bounded byte scan. Its float hook is float; the classifier
deliberately retains its narrower rejection of nonfinite exponent results.

Candidate eval_agreement.py:183-187 now applies decoded-capture bounds and final LF,
splits only raw LF and passes complete physical frames to decode_frame:120-151.
That helper matches the frozen byte/depth/integer predicates before UTF-8/JSON parsing.
It preserves unique_object and finite_float, and turns RecursionError into Unusable.
ValueError, Unicode decoding errors, type errors and missing-field failures reach the
existing exclusion return at 341-343. No normalization can erase CRLF, alternate line
separators or oversized frames before this gate.

The helper's trailing-LF predicate alone does not assert there is no earlier LF.
That does not open a credit bypass: its production caller supplies exactly one physical
frame obtained from raw.split(b'\n'). Direct helper parsing is not a separate credit API.
I did not infer physical-stream validity from decoded-object equality.

Positive language also matters. Legal padding to 16,384 bytes is admitted, ordinary
JSON whitespace and equivalent finite numeric spellings are not required to be canonical,
escaped brackets do not add depth, and UTF-8 is decoded strictly rather than normalized
with universal line splitting. The existing finite-float exception is explicit authority,
not an accidental demand to reproduce every raw host float result.

## Transformations and successful-credit paths

The sealed inventory contains the detailed boundary census. The decisive paths are:

1. Producer: v0a_event_adapter.py:188-202 emits UTF-8 JSON plus physical LF through
   full writes. Host WireConsumer validates records and completion. Session:233-315
   retains connection stdout as base64, failure state, exit/truncation and settlement;
   Session.run:317-361 only commits completed outcomes after the successful hand path.
2. Admission: frames_for:188-251 validates frame kinds/fields, identities, ordering,
   paired actions/decisions, nullable failures, terminal accounting and closure.
   admitted_decision:53-87 checks raw decoded shapes before constructors, uses v1
   DecisionRecord/TimingRecord or the frozen v2 decision codec, and preserves the
   intentional v1 reason-label disagreement behavior.
3. Replay: eval_agreement.py:254-303 rebuilds actual applied history through the kernel,
   checks terminal state and recomputes settlement from supplied cards. Settlement
   comparison distinguishes JSON booleans/floats from kernel integer payouts.
4. First chip credit: classify:336-348 follows frame admission and replay. Any raw
   refusal returns the initialized excluded result with no chips, agreement eligibility,
   observed hit count or river count. Baseline return:349-351 is downstream of these gates.
5. Hit credit: classify:352-393 separately compares reconstructed state/cards/actions,
   PreparedBlueprint key/action/table_hit, reason, teacher and exactly one river.
   Only an in-pool teacher match with no causes becomes hit. Reason-only disagreement
   retains settled chips; completed v2 divergence does not face the blueprint river gate.
6. Summary credit: summarize:397-411 counts excluded and missing outcomes and marks them
   incomplete. Its generic complete can include unsupported; primary campaign acceptance
   is stronger and requires every primary result to be hit.
7. Worker/parent completion: completion.agreement:345-373 checks primary hits and all
   three controls. complete:376-436 checks summary, ordinals, names, classifications
   and artifacts. accounting:439-463 binds attempts to schedule/witnesses and computes
   missing counts. v0a_eval_panel.py:519-528 rejects incomplete/error/cleanup outcomes.
8. Retention/display: execution.finish_run:122-162 persists the final parent report and
   status once; inherited children return. status_generation.py:14-78 copies validated
   journal status for display. Neither supplies a bypass around agreement classification.

Export/provider membership at eval_bridge.py:363-421 is a distinct successful-credit
surface. It checks canonical teacher, exact codec keys/actions, actual wire size and
the public provider across the root universe. Those library counts do not certify
host attempts. The completion caller binds teacher/wire/deal inputs before classify.

Thus the repaired raw gate dominates every chip, hit and phase-completion path located
in the frozen Slice A production consumers. This is a source-path conclusion, not a
new execution result or a claim that arbitrary external observations are authenticated.

## Deferred reconciliation and receipt verification

The deferred discovery chain and five boundary categories agree with the independent
inventory. The four parent framing examples are closed by the explicit raw checks:
CRLF by CR refusal; record/Unicode separators by physical LF splitting and JSON refusal;
oversized ready frame by the byte bound. Parent recursion handling is also repaired.

The test matrix at tests/test_eval_protocol.py:136-183 mutates actual v1 CHECK and v2
premium-diverged Session captures. It checks the frozen host decoder on physical frames
before checking classify, and does not parse/reserialize the framing mutations away.
It tests alternate separators, CRLF, BOM, invalid UTF-8, unfinished capture, frame/capture
overflow and 641-digit timing integers. The exact frame-limit positive compares the
entire classification with the original control, including settled chips.

The direct decoder matrix at 185-214 checks depth 8/9, 640/641 digits, quoted escapes,
size boundaries, duplicate keys, invalid syntax/encoding/constants and finite exponent
acceptance. Exponent overflow has a separate stricter classifier expectation.
Existing actual controls at test_eval_completion_tool.py:125-171 distinguish CHECK hit,
off-pool default, changed-stack zero hits, failed transport and reason relabeling.
Protocol tests:68-72 explicitly require the real v2 premium preflop raise.

RED commit 81a5aaf5670c9f495cc03dbb26796699a11cffa1 has the rejected parent as its sole
parent and changes only tests/test_eval_protocol.py. Its test blob equals the candidate
test blob exactly; its classifier equals the rejected parent's classifier.
The RED receipt/result/journal agree on commit and exit 1. The output records 26
real-capture exclusion assertion failures, plus one missing-decoder assertion, across
two unittest methods, no errors and no skips. The structural missing-helper assertion
is not treated as another behavioral counterexample.

The focused receipt/result/journal agree on candidate, exit 0 and result SHA-256.
They report Python 3.14.6, source_verified=true, six suites and 80 unittest cases:
11 bridge, 29 panel-tool, 8 export, 21 agreement, 9 completion-tool and 2 protocol.
All report OK with zero skips; pytest reports six passed and 44 deselected.
Both stderr copies are empty. Journal result hashes match the actual packet result bytes.
The snapshot script was inspected as text only. Its declared test environment is scrubbed,
uses -B -P, absolute PONTIUS_GIT and fatal resource/unraisable warnings.

These are hash-verified packet receipts, not tests run by this reviewer.
The copied parent diagnostic's four failures are consistent with the parent raw code.
Its referenced r001 capture was not opened, so that old capture provenance was not
independently reconstructed; the candidate's real-capture tests provide newer evidence.

## Evidence limits and design assessment

No required finding survived source verification. No additional material raw-admission
failure scenario was established. The remaining limits do not justify a NOT CLEAN verdict:

- The oversized capture case also violates the frame-size limit. It does not isolate
  the capture guard or prove a natural completed four-chip hand can reach that size.
  This limitation is correctly disclosed in coverage.md. The capture predicate was
  independently inspected; no production bypass was found.
- The Unicode positive at test_eval_protocol.py:194 uses json.dumps with default
  ensure_ascii=True. It proves the escaped JSON form, not a literal multibyte UTF-8
  separator inside a string. Literal acceptance follows from static UTF-8/JSON analysis,
  not that executed positive. Byte-length versus character-length positives, escaped-key
  duplicates and all JSON spellings are not exhaustively tested.
- The deep-input test exercises the depth guard, not an injected internal RecursionError.
  The explicit exception conversion was checked statically. No arbitrary resource-failure
  or parser-environment exhaustion claim is made.
- host_accepts is a physical split plus the actual host decoder, not a rerun of the
  threaded read_stream. Queue occupancy, scheduling, wall clocks, stderr overflow and
  cleanup are not reconstructible from stdout. Retained real-host failure status owns them.
- The parent completion consumer trusts observations from its admitted worker; it does
  not independently rerun classify on every embedded session. The located worker path
  always calls classify. Arbitrarily forged observation dictionaries are outside that trust.
- External source/wire/deal admission, caller strategy attribution and unused outer
  envelope fields remain the existing boundary. This is not a general Slice B identity
  validator or permission to treat summarize.complete as full primary agreement.
- No broad verification, full-H coverage, retained solve/export/agreement, strength,
  performance, calibration, OS-containment or independent poker-rules result was produced.

SOUND applies to this bounded repair. A single explicit raw admission boundary now
precedes the existing typed validation and replay, while chip outcome and root agreement
stay separate. No sealed producer change or general protocol framework is needed.
The host predicates are duplicated locally because the host is frozen; future changes
must keep that relationship explicit and preserve the differential tests. That maintenance
cost does not establish a current structural defect or justify a whole-bridge replacement.

The final delivery supplies this report's SHA-256 after writing, separately from its bytes.
The inventory hash was rechecked unchanged after deferred reconciliation.
