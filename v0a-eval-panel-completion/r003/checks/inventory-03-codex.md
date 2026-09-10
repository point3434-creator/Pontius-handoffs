# Independent inventory 03 - Codex

Status: sealed before coverage.md or any checks/ input was opened.
Context probe: CONTEXT_PROBE_NONE, issued before opening handoff.md.
No injected memory, project history, candidate verdict or finding was present.
Only generic instructions and this review request preceded the probe.
No delegation. Scratch is exclusively the user-named directory.

Candidate: 7ca821802c949b047becf6599d603b3b63d51fa7
Parent: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Tree: 3d2fe79d2af20125e322dd4a668335e789810863
Manifest: 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd

## Independent requirements

The r003 brief makes frozen host read_stream/decode_json the raw framing/JSON oracle.
Later decoded record, model, codec and kernel contracts remain separate authorities.
The classifier retains its stricter finite-number restriction.
Malformed physical captures must earn no chips, root hit or completion credit.
Do not turn reason-only disagreements into lost settled chips.
Preserve v1 CHECK hits, off-pool defaults and completed v2 prefix divergence.
Missingness, failed delivery, accepted-then-failed decisions, truncation and absent
terminal/closure/settlement must remain exclusions with visible causes.
Root membership, teacher action, lookup reason and applied history must agree for a hit.
No exactly-one-river rule may become a universal baseline chip gate.
Summary counts must reconcile schedules, observations, missing, completed and dispositions.
Host subset observations do not certify the entire 1,081-hand population.
The whole Slice A production ceiling is 3,000 lines; 1,200/600 are working figures.
No host/session/codec edits, changed arithmetic, timing or ownership contract is authorized.

## Frozen raw acceptance language, derived first

Source: tools/v0a_table_host.py at the candidate, lines 52-90 and 512-537.

1. Child stdout is bytes read in chunks of up to 4,096. Retained stdout cap is
   2,097,152 bytes; an overflow marks truncation and transport failure.
   Stderr has its own 65,536-byte capture bound; transport success is retained upstream.
2. Only byte 0x0A ends a physical stdout frame. The emitted frame includes that LF.
   Its size must be at most 16,384 bytes. A pending fragment must be shorter than
   16,384 and must be empty at EOF. The reader then enqueues the EOF sentinel.
3. The host also has an eight-slot frame queue and real transport/deadline/cleanup
   checks. Capture bytes alone cannot reconstruct scheduling; retained outcomes own that.
4. WireConsumer.read requires bytes ending in LF, then decode_json with digits=640,
   floats=True. A raw JSON input must be nonempty, at most 16,384 bytes, contain
   no physical CR anywhere, and not start with the UTF-8 BOM.
5. The byte scanner counts unquoted square/curly nesting, maximum eight.
   Quote state honors backslash escapes. Brackets within strings do not add depth.
   This is an admission bound; json.loads still owns valid JSON grammar.
6. Decode strictly as UTF-8, then Python JSON with unique decoded object keys.
   Duplicate spellings that decode to the same key are duplicates at any level.
   Integer tokens allow at most 640 characters after stripping a leading minus.
   Decimal/exponent tokens use float; NaN/Infinity constants are refused.
   JSON syntax, UTF-8, type/value and recursion failures become HostRefusal.
7. Host raw float conversion can produce infinity for exponent overflow.
   The classifier's explicit finite restriction is intentionally narrower.
8. Blank LF frames, CRLF, bare CR, pretty JSON spanning physical lines and Unicode
   line separators used instead of LF cannot be normalized into valid host frames.
   UTF-8 Unicode inside a JSON string is a different case and is not a line delimiter.

This derivation preceded inspection of eval_agreement.py and the candidate source delta.

## Producers and transformations

- v0a_event_adapter.py:188-202 serializes full JSON objects with allow_nan=False,
  adds LF, UTF-8 encodes and writes full frame bytes. Runtime/trace/provider payloads
  supply ready, actions, event decisions, terminal and closure values.
- v0a_table_host.py:662-680 consumes raw frames, exact kind/fields/identity and order.
  Later action/timing/decision/terminal validation supplies the decoded host boundary.
- v0a_table_session.py:233-315 retains the real connection's stdout via base64 and
  preserves failures, child exit and truncation. Completed hand status is committed only
  after protocol completion and successful cleanup, with a provisional settlement.
  run:317-361 wraps that outcome, carries stacks and commits session completion.
- v0a_eval_panel_completion.py:282-311 uses the actual Session.run result and passes
  frozen blueprint/teacher, board and private hands to classify. It returns both the
  session and the classification, retaining the raw capture inside the session.
- eval_agreement.py:183-187 strictly decodes base64, bounds the decoded capture,
  requires terminal LF and splits only on physical LF before decode_frame.
- decode_frame:120-151 validates size/termination, CR/BOM, quoted byte depth and
  integer tokens before JSON decoding. unique_object and finite_float retain their
  existing duplicate and finite-number checks. RecursionError becomes Unusable.
- JSON strings, numeric spellings and escaped keys normalize only after raw admission.
  Constructors are reached only after the decoded field/type checks.
- frames_for:188-251 binds ready/terminal/closure placement, exact per-kind fields,
  protocol/session/source/blueprint identities and contiguous event indices.
  Each action must pair with a decision; failures and incomplete accounting exclude.
- admitted_decision:53-87 uses exact v1 dataclass fields before model construction.
  It checks exact absent preparation and raw reason string, then substitutes only the
  enum for model validation; the original reason remains for agreement comparison.
  v2 uses decision_provider.codec.validate_decision and accepted delivery equality.
- v0a/model.py:386-488 checks exact counters, valid actions, timing subtraction,
  finite seconds, boolean flags and identities. Provider codec:44-137 also validates
  proposal/selection/application/delivery consistency and calls trace timing checks.
- replay:254-303 rebuilds kernel state from applied history, validates ordered actors
  and origins, obtains real cards, requires terminal state and recomputes settlement.
  no_limit_betting.py:696-751 calculates integer payouts/net returns and conservation.
- PreparedBlueprint.action_for:51-69 computes the complete key, resolves lookup or
  passive fallback, checks legality and returns the table_hit boolean.
  eval_bridge.py:79-97,145-150 independently replays the declared root and builds keys.
  Teacher/export/membership routines at 335-421 bind canonical teacher and exact
  codec key/action membership; their provider counts are library counts, not host counts.

## Every located successful-credit consumer

Frozen source searches were limited to src/, tools/ and tests/, never retained records.

- classify:318-343 initializes all credit false/null and catches malformed retained
  inputs before publication. Raw failures therefore have classification excluded,
  no chips, no agreement eligibility and no observed hit count.
- classify:344-348 first publishes chip eligibility, replayed chips, observed reason
  hit count and river-record count only after outcome/frame/replay gates.
- classify:349-351 preserves completed baseline chips and returns unsupported.
  It intentionally does not apply the blueprint root predicate to baseline chips.
- classify:352-393 reconciles decision count, state/cards, applied and selected action,
  lookup identity/reason, passive pre-river behavior and exactly one river.
  Root-key equality grants agreement eligibility; only an in-pool matching teacher
  with a genuine lookup hit and no causes grants classification hit.
  A reason-only problem is disagreement while completed chips remain available.
- summarize:397-411 counts dispositions, chips as completed, agreement eligibility and
  missing attempts. complete requires no missing, disagreement or excluded attempts.
  Unsupported can complete this generic summary; primary agreement adds a hit gate.
- completion.agreement:345-373 requires each primary classification to be hit.
  It separately requires off-pool unsupported/chips, CHECK hit and changed-stack
  chips with zero observed hits. It then emits the primary summary.
- completion.complete:376-436 verifies one complete phase summary, scheduled/observed
  counts and ordinals, primary hand names/hits, the three controls and artifact identities.
- completion.accounting:439-463 binds observed attempts to the declared schedule,
  labels and witnesses, then recomputes primary summary and missing counts.
- v0a_eval_panel.py:519-528 consumes complete/accounting; worker completion is changed
  to failed for incomplete phase, errors, unverified cleanup or incomplete observations.
- execution.finish_run:122-162 persists that report and its status once at the parent;
  inherited children return. status_generation.py:14-78 validates journal fields and
  displays retained status, without independently granting agreement credit.
  Only source definitions were read; no journal, result, STATUS or progress was opened.
- Tests are consumers of classifier outputs, including host controls and constructed
  envelopes. Initial source searches exposed matching test lines, not deferred checks
  or any reviewer output. Full changed-test assessment remains for reconciliation.

## Independent challenge matrix for deferred reconciliation

Physical language: LF versus all other line boundaries; missing final LF; empty and blank
frames; multiple frames; leading/trailing whitespace; CR anywhere; BOM at frame start;
valid UTF-8, invalid UTF-8 and Unicode separators inside versus outside strings.

Bounds: 16,384 inclusive versus 16,385 frame bytes including LF; 2,097,152 inclusive
versus overflow capture; byte counts versus character counts; depth eight versus nine;
quoted/escaped brackets; 640 versus 641 positive and negative integer token digits.

JSON: top-level scalars/arrays, duplicate and escaped-equivalent keys, trailing tokens,
invalid syntax/escapes/control bytes, exponent overflow, constants, negative zero,
finite exponents, parser recursion and exception conversion. Grammar must be challenged
before constructing objects; decoded equality alone is not an acceptance-language oracle.

Decoded and credit paths: nullable failures; unknown/missing/extra fields; booleans
masquerading as integers; malformed actions/preparation/timing; failed events, unpaired
actions, identity changes, incomplete closure/settlement and missing schedules.
Both v1 hit and genuine v2 completed prefix divergence must exercise raw rejection.
Positive variants must preserve the entire classification and settled chips.
Failures must propagate to summary exclusion/incompleteness and primary completion gates.

Potential weaknesses to resolve: any raw predicate mismatch; a successful route that
bypasses frames_for; a decoder exception escaping instead of exclusion; expectations
derived from the candidate parser instead of the host; test normalization erasing the
invalid bytes; an unsupported count being mistaken for a primary hit.
No candidate defect verdict is sealed in this inventory.

## Identity and input-order evidence

Verified ref target, exact candidate tree and sole parent from raw commit metadata.
Candidate delta is exactly eval_agreement.py and test_eval_protocol.py, both modified.
All 51 dependency blob digests match; every named dependency packet copy matches its blob.
Named inputs/ hashes match supporting-files.json.
Brief and supporting-list SHA-256 match handoff.md.
Candidate manifest was regenerated from raw blobs, sorting full digest/path ASCII rows
ordinally (equivalent to bytewise here), LF terminated, and compared byte for byte.
The supplied parent manifest likewise matches its raw three-file delta from parent
449a2a3c1fa1f5a7f5f04adca32e499faaf81e13 to 430ad75de79cec13d66ff3dc4981dd3770a371b7.
Parent manifest SHA-256:
6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5

No coverage.md or checks/ bytes have been accessed, even for hashing.
Pinned earlier authorization/design text was read only through allowed inputs/.
Three named handoff-repository dependency blobs were read only to verify pins/copies;
no other packet navigation or prior review/disposition was performed.
No worktree source, memory, sibling scratch, launch log, history, index, progress,
readiness file, reviewer output or project execution was accessed.
PowerShell/.NET copied Git stdout as raw bytes in memory; no utility files were created.
One malformed read-only Git search failed before returning source; corrected discovery
used explicit frozen blobs. No permission denial or substituted worktree bytes occurred.
The final report will record this file's post-write SHA-256; this inventory stays unchanged.
