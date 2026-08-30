# Independent cold inventory B, recorded before deferred coverage

Candidate: 52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8
Manifest: 7e1575b18c7a9cf0c74bd956a54e899aad670349d198d7863ae1f67463583d7a
Base: 6cdf7b00dac653a9a295bbb86cdc3b5782317491
Scope: trace.py and test_v0a_trace.py, and only directly related frozen contracts.

Cold inputs consulted: handoff, candidate, manifest rows, current CLAUDE.md and
workflow.md, r005/disposition.md, frozen ADR0485/ADR0484 and increment-one brief,
frozen trace.py, model.py event admission, test names, and runtime/replay call-site
searches. No coverage, implementer narrative, sibling checks, or peer review read.

## Invariants and planned direct evidence

1. Interrupted response or unknown delivery implies complete=false, passed=false,
   accounting_complete=false across every terminal variant, including unknown with
   null timing. Exercise all eight flag assignments over honest failure controls.
2. Unsuccessful/incomplete terminal settlement is null. Failed terminal retains a
   non-null primary typed cause; completed accounting has both finite category
   totals. Changing reason, adding settlement or deleting required totals must
   refuse with TraceInvalidError even after both digests are independently rebound.
3. First cause preservation is constrained by actual information on the wire.
   A source/witness failure may precede an adapter refusal; no invented source/body
   chronology may reject an honest compound failure. Exercise failure before wall,
   after wall start, rejected input, accepted/rejected/ambiguous delivery, prefailed
   witness, late completed response, and post-terminal publication separation.
4. Counts and known-delivery pairing remain exact: unique interrupted identities,
   contiguous events/actions, paired decision/failure timing/action/reason, valid
   completed timing/accounting and SHA256 projection/prefix bindings.
5. Every event uses exact common fields: schema, kind, ASCII hand ID, exact index.
   Start: exact seat/stacks/blinds domains, six stacks, ascending distinct private
   cards 0..51; opponent: street/seat/action keys and raise domain; reveal: 3/1/1
   distinct cards in reveal order (unsorted boards allowed); showdown: six ranks,
   exact integer/nonempty integer tuples/null and comparable nonnull rank domains.
6. Schema construction is pure; event constructor admission must not execute
   policy, legal replay, host capabilities, or deserialize arbitrary objects.
   Parsing rejects malformed wire values with a typed error while legal replay is
   a separate boundary. Cross-record semantic illegality alone is not this fix.
7. Preserve successful real A/B hand traces, honest failed prefixes and sealed
   source bytes. The known ReplayHost premature schedule/null reason producer issue
   is excluded. No broad/GPU/install/capability/lifecycle execution is authorized.

## Related path inventory

- trace.py: _EVENT_COMMON/_EVENT_VARIANTS, _validate_event, primitive/action/timing/
  settlement validators, _validate_terminal_consistency, parse_trace ordering/counts/
  pairs, semantic projection and TraceBuilder terminal serialization.
- model.py: HandAction and four event constructors; admit_event exact copied graph;
  TimingRecord, FailureRecord, FailureCode and outcome types as value contracts.
- runtime.py: event ingress, failed response preservation, delivery status and
  accounting snapshot (read-only related contract, unchanged in this round).
- replay.py: ReplayHost terminal fields/primary source journal and real A/B fixtures;
  verify_successful_trace remains an unchanged independent acceptance boundary.
- tests/test_v0a_trace.py: canonical/schema/write tests; terminal admission and
  constructor tests to inspect against these independent expected outcomes.
- tests/test_v0a_model.py: focused existing event-value preservation suite if present.

Evidence strategy: fresh D-local candidate clone; assert actual 3.11.15 executable
first and 3.14.6 second, -B -P, snapshot cwd/src PYTHONPATH, scrubbed environment and
absolute regular non-reparse Git. Recompute whole-row-sorted manifest from blobs.
Run changed trace suite, related model suite, and bounded independent public-parser
mutation checks with independent digest calculation. No implementation changes.
