# Independent inventory 02 - Codex

Candidate: 7ca821802c949b047becf6599d603b3b63d51fa7
Parent: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Manifest: 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd

Written before opening coverage.md or any checks/ file.

## Independence and authority

Inherited context contained general Pontius memory guidance, with no substantive candidate
history, findings or verdicts. That guidance was not used as evidence. No memory file was read.
The dispatched review request, current user instructions and packet handoff are the task inputs.
Initial packet inputs and frozen Git blobs are the only project evidence read so far.
The generic code-verification skill was read; using-superpowers says subagents ignore that skill.
One failed read of a nonexistent skill path exposed nothing. Mandated Python startup was denied
in the sandbox; an approved escalation then ran read-only standard-library hashing/Git utilities.
No project code or tests executed. No other reviewer conclusions were received.

## Independently derived obligations

1. accepted-brief criteria 5 and 7, accepted-design outcome classification, and completion-brief
   mechanism 7 require failure-first admission. Missing outcome, failed delivery, child failure,
   truncated or malformed capture, missing closure and unsettled hands get neither chip nor
   agreement credit. A complete baseline with a divergent prefix must retain settled chips.
2. r003 brief fixes the physical host read_stream and decode_json contracts as framing/JSON
   oracles. Raw capture cap is 2097152 bytes; each LF-inclusive frame is at most 16384 bytes.
   Every physical frame terminates in LF. CR and initial UTF-8 BOM are rejected. Internal LF,
   Unicode line separators, tabs, escaped controls and trailing spaces need distinct treatment.
3. JSON nesting is bounded by 8 outside quoted/escaped strings; integer tokens are at most
   640 digits excluding minus. Duplicate keys at every depth and invalid UTF-8/syntax fail.
   Nonfinite constants and exponent overflow must fail under the retained finite-number rule.
   Negative zero, exponent forms, empty containers and valid whitespace must use real parsing.
4. No decoding or parser failure may escape classification and manufacture a successful result.
   Examine malformed base64, all JSON top-level types, wrong record field types and malformed
   nesting. Admission must not rely on a constructor silently defaulting missing raw fields.
5. Later-stage model/codec contracts continue to validate exact field sets, exact integer/bool
   types, timing, identities, accepted delivery, paired actions and event ordering. Do not turn
   unknown string reasons into malformed transport; they remain agreement disagreements.
6. Replay applied actions using supplied immutable deal/stacks; require a real terminal state,
   exact kernel settlement and host rank-source/event reconciliation. Agreement additionally
   requires one controlled river decision, exact key/action/reason and teacher membership.
7. Preserve valid in-pool CHECK hits, off-pool defaults, reason-only disagreements and actual v2
   baseline divergence. Byte-identical semantics with legal alternative JSON spellings must
   not lose settled chips. Host acceptance alone does not establish agreement correctness.
8. Accepted-brief criteria 6 and 9 require explicit missingness and one result owner. A malformed
   attempt must not count as a primary hit, completed attempt or complete successful campaign.
9. Scope is exactly classifier and protocol tests; host/session/codec/solver and registration
   remain frozen. Whole-slice production ceiling is 3000; 1200/600 are disclosed working figures.
   The review authorizes no project execution, adoption, retained phase, source edits or ref writes.

## Producers, consumers and successful-credit paths

- Frozen tools/v0a_table_host.py: Connection.read_stream emits physical LF frames and retains
  stdout bytes; decode_json governs bounded JSON. Child capture and settlement enter hand results.
- tools/v0a_table_session.py produces the outer single-hand envelope and its hands[*].result.
- tools/v0a_eval_panel_completion.py: play passes Session.run output, decoded artifact, immutable
  teacher map, board and private hands to eval_agreement.classify. agreement requires primary
  classification hit, inspects off-pool/check/changed-stack controls, then summarizes.
- eval_agreement.classify calls frames_for before replay and before chip_eligible=True.
  frames_for decodes base64, splits physical LF and calls decode_frame on every frame; later
  fields/identity/admitted_decision gates precede replay. There is one chip-success update.
- Baseline early return occurs after chip admission. Blueprint agreement subsequently compares
  replayed states, prepared lookup, action/reason, root membership and teacher. Only one branch
  assigns hit. summarize counts dispositions and includes absent scheduled attempts as missing.
- Completion accounting consumes classifier dictionaries in retained observations. Completion
  summary and primary loop must not conceal excluded/disagreeing results or unobserved hands.
- Search of frozen source/tools/tests found one production classify call in completion.play;
  summarize production consumers are completion.agreement and completion.accounting.

## Independent challenges to apply before accepting supplied checks

- Paired exact/plus-one frame, capture, nesting and integer boundaries; test negative and positive
  numeric spellings, escaped quotes/brackets, actual versus escaped CR/BOM/control separators.
- Preserve a valid completed host result while changing only its raw stdout framing, to show
  invalid bytes cannot retain chips merely because the decoded records would be unchanged.
- Compare both host reader and host decoder, not json.loads alone. A decoder accepts pretty
  internal LF in a complete JSON document while the streaming reader splits it physically.
- Assert both chip_eligible=False and agreement_eligible=False for rejections, plus excluded,
  chips=None and a retained cause. Avoid only asserting not-hit or matching private error text.
- Positive cases must reach valid v1 CHECK-hit and actual v2 divergent-baseline outcomes. A fake
  envelope only establishes classifier behavior; source utilities do not execute project paths.
- Check parser exception handling independently and distinguish injected failures from organic
  inputs. A parser mock tests propagation only; it does not prove real parser-limit behavior.
- Inspect registration and fixture construction, source isolation and receipts after sealing.
  Derive expected outcomes from frozen host/model/kernel authorities rather than test helpers.

## Executed identity facts

Read-only Git and standard-library hashes verified ref, sole parent and tree
3d2fe79d2af20125e322dd4a668335e789810863. Exact two-file candidate manifest matches.
Parent raw three-file delta regenerates parent-manifest SHA-256
6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5.
All 51 dependency pins and 12 initial supporting-file hashes match, including packet copies.
Brief and supporting-file list hashes match handoff. Deferred files have not been opened.
These are executed utility facts; behavioral observations above are static source reasoning.
Only this inventory file has been written in the exclusive scratch directory.
