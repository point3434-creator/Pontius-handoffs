# Cold review B independent inventory (before deferred coverage)

Candidate: 6cdf7b00dac653a9a295bbb86cdc3b5782317491
Manifest: 83798245d9feac931479478e81c850ac4de277a2903a7523f5745320738cd21f
Base: c6adbcaa048988361d2388970eaca772711b797b
Inputs: handoff/candidate/manifest; current CLAUDE.md and workflow.md; frozen
ADR-0485 and ADR-0484 brief; R2-05/R2-06 required outcomes; frozen source/tests.
No coverage.md, implementer narrative, or current peer review read at this point.

Independent requirement/path inventory:

1. Packet integrity: exact ref/parent/tree; four changed paths; manifest whole-row
   lexical ordering and SHA256 directly from stored Git blobs; no sealed dependency edits.
2. Raw admission: bytes, UTF8/BOM/LF, canonical JSON, duplicate keys, nonfinite and
   huge/deep input; all failures typed TraceInvalidError.
3. Every nested schema: common row fields, event variant key sets, exact int/bool,
   ASCII identifiers, digest widths/spellings, enums, seats/cards/stacks/blinds,
   ascending private pair, distinct cards, action variant, rank-domain shapes,
   preparation absence, timing variants, failures, settlement/pot shapes.
4. Structural cross-row consistency: header/hand/policy bindings, contiguous rows,
   accepted events and delivered actions, matching accepted failure/decision pairs,
   unique interrupted counts, ordered response intervals; successful and failed
   terminal flags, reasons, accounting and settlement must agree with row content.
5. Cryptographic binding is necessary but insufficient: exact preceding LF bytes
   and independent semantic projection; all semantic mutations rebind both digests.
6. Accepting replay external expectations: source commit+manifest, configuration,
   policy, mode/clock/run identity; immutable exact fixture/policy values; reject
   behavior-supplying subtypes without executing caller metadata.
7. Replay real boundaries: initial blind state/cards, controlled-turn ordering,
   full opponent schedule, chance reveals, independent blueprint action_for,
   before/after/card identities, table hit versus passive miss, repeated actions,
   fold terminal, river showdown ranks, final schedule/action counts.
8. Settlement oracle: derive eligible depth groups independently, merge folded-only
   levels before tied division, clockwise odd chips, conservation, complete pots,
   payouts and final stacks. Explicit (0,1,2,15,15,5) folded 0/1/2/5 => one 38-chip
   pot for (3,4), equal winners => (0,0,0,19,19,0), plus real host/replay control.
9. Timing: complete exact ns subtraction/partition and deadlines, honest interrupted
   fields/flags, failure cause, no successful null timing; emission reserve may
   legitimately finish between 14s and 15s. Trace does not prove host completion.
10. Review tests' independence: real host traces and real checker; external literal
    expectations or independent calculations, not production pot assembly; negative
    controls must not be masked by stale hashes or an earlier unrelated rejection.

Execution plan: fresh detached D-local snapshot outside packet; real CPython
3.11.15 first, then 3.14.6; -B -P, snapshot cwd/src PYTHONPATH, scrubbed environment,
absolute Git; only changed trace/replay suites plus bounded reviewer probes. No
source edits, broad/GPU/dependency installs, owners, commits, or host publication claim.
