# Independent inventory 01 - Codex

Candidate: 7ca821802c949b047becf6599d603b3b63d51fa7
Parent: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Manifest: 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd

Written before opening coverage.md or any checks/ file. No deferred contents used.

Context and procedure

Inherited context contains generic Pontius memory summaries about earlier training,
architecture, and baseline-watch governance. It contains no substantive completion candidate
history, findings, or verdicts. Those summaries were not used; no memory files were opened.
The initial task explicitly requests this cold review. No other reviewer conclusions received.
The handoff was read first. Verification skill instructions were read for process only.
One accidental read targeted a nonexistent skill path and returned no contents. One Python
utility launch was denied by the sandbox; the identical read-only utility succeeded with
reviewed escalation. No project code, tests, hooks, or imports have executed.

Executed identity facts

The frozen ref, sole parent, tree, and exact two-file delta verify. SHA-256 rows were rebuilt
from raw Git blobs and sorted bytewise as full digest/path/LF rows. They exactly match the
candidate manifest and its announced digest. The supplied parent manifest matches its raw
three-file delta from 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13. All 51 dependency pins and
all named initial input hashes verify, including dependency packet-copy byte equality.
The brief and supporting-file-list hashes verify. Deferred files have not been hashed yet.

Independent requirements

- Host-invalid physical framing or JSON must receive neither chips nor agreement credit.
- Frozen host read_stream/decode_json govern transport language; model/codec/kernel govern
  their later stages. The classifier's stricter finite-number rule remains intentional.
- Failure and missing settlement precede agreement. Every attempt has one disposition.
- Valid CHECK hits, off-pool defaults, reason-only disagreements, and completed v2 baseline
  divergence preserve their outcomes and settled chips. River multiplicity is agreement-only.
- Exactly the classifier and protocol tests may change. Host, session, codec, provider,
  solver, timing, ownership, and test registration stay sealed. Production ceiling is 3000.
- No new retained measurement, broad test execution, adoption, ref write, or source edit.

Producer and raw acceptance boundary

Frozen tools/v0a_event_adapter.py:188-192 writes compact JSON with allow_nan=False plus LF
as UTF-8 bytes. Session retains ChildConnection.stdout through base64 unchanged.
Frozen tools/v0a_table_host.py:512-537 reads physical LF-delimited frames, counts LF toward
16384 bytes, requires an empty pending buffer at EOF, and caps captured stdout at 2097152.
Overflow marks capture truncated and transport failure. A partial 16384-byte frame fails.
WireConsumer.read at 662-680 requires bytes ending LF and applies decode_json with digits=640
and floats=True. decode_json at 52-90 forbids raw CR and leading UTF-8 BOM, bounds nesting
at eight outside quoted strings with escape tracking, rejects duplicate decoded object keys
and nonstandard constants, decodes strict UTF-8, and caps integer token digits excluding '-'.
JSON grammar rejects blank records, non-JSON controls, trailing garbage, malformed escapes,
invalid nesting, and multiple values. CR escaped inside strings is not raw CR. Physical LF
inside a string splits a frame; escaped LF does not. JSON string contents may include raw
UTF-8 Unicode line separators without creating physical frames.

Transformations and gates to trace

1. Completed outer session and nested outcome, exact counts, failure nullity, child exit 0,
   untruncated capture -> strict base64 -> retained byte bound -> physical LF splitting.
2. Per-frame byte/depth/token/JSON admission -> exact frame fields and protocol/session/source
   identities -> ready/action/event/terminal/closing order -> pending action pairing.
3. V1 exact decision/preparation fields and model validation; unknown string reasons remain
   explicit later disagreements. V2 public codec checks proposals, fallback, delivery and
   identity. Shared TimingRecord must be completed, finite, internally consistent, in budget.
4. Terminal and closure accounting/causes/settlement -> kernel replay of applied history with
   exact indices, seats, origins, legal actions, terminal state, cards, settlement and events.
5. Chips are granted only after steps 1-4. Baseline bypasses blueprint-only river agreement.
6. Blueprint agreement replays record state hashes, lookup action/key/reason, pre-river defaults,
   exact river multiplicity, and frozen teacher membership/action. A CHECK default is not a hit.
7. summarize counts missing/excluded/disagreement separately. Completion tooling requires each
   primary hit and named controls; accounting consumes classifications and preserves attempts.

Independent adversarial cases to reconcile with deferred evidence

- 16383/16384/16385-byte physical frames including LF; exact/over stdout cap; partial EOF;
  CRLF, raw CR, BOM at start/later in frame; leading/trailing legal JSON space/tab.
- Empty frames, blank lines, malformed/trailing JSON, two values, invalid UTF-8, base64 errors,
  embedded raw versus escaped LF, vertical tab/form feed, raw versus escaped U+0085/U+2028/U+2029.
- Depth eight versus nine, quoted bracket storms, odd/even escaped quotes and backslashes,
  duplicate decoded keys including escape spellings, both signs of 640/641 integer digits,
  very deep parser input, NaN/Infinity, exponent overflow and otherwise finite exponent forms.
- Refused raw text that normalizes to valid records must still be excluded. Conversely,
  host-valid spelling variations that decode identically must retain classifications/chips.
- Nested decision/action/preparation/terminal mutations, bool/int lookalikes, nullability,
  contradictory delivery/timing/failure, identity mismatch, duplicate/extra/missing frames.
- Trace settlement and eligibility separately: successful malformed captures cannot gain
  summary/phase credit; benign reason relabeling and true v2 divergence cannot lose chips.
- Search public classifier exceptions for parser/model failures escaping as crashes instead
  of exclusions. Verify valid-domain constructors cannot introduce a false exclusion.
- Keep raw parser parity distinct from later semantic constraints and permitted reason
  disagreement. Test oracles should reference the real frozen host, not a copied decoder.

Evidence limits and next step

This inventory is source reasoning, not executed project behavior. Only read-only Git, file
reads and standard-library hashing ran. Next, hash/read deferred coverage and checks, inspect
frozen protocol tests, reconcile claimed members and independence, and seek both false success
and false exclusion before issuing separate defect and design verdicts. Only this inventory
and the final report are written in this exclusive scratch; no utility scratch files exist.
