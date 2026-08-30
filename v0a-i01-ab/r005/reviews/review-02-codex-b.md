# Independent cold review B - v0a-i01-ab/r005

Reviewer: Codex cold B. Date: 2026-08-30. Tier C FIX.
Defect verdict: **NOT CLEAN** (two Important required corrections).
Design verdict: **STRAINED** (advisory; detailed below).
Specification result: **FAIL**. Engineering-quality result: **PARTIAL**.

Bound candidate identity:

- Ref: `refs/heads/review/v0a-i01-ab/r005`
- Commit: `6cdf7b00dac653a9a295bbb86cdc3b5782317491`
- Manifest SHA256: `83798245d9feac931479478e81c850ac4de277a2903a7523f5745320738cd21f`
- Base: `c6adbcaa048988361d2388970eaca772711b797b`
- Tree: `89ae2190fa69c6974750ae032a7afec3ca106f18`

The accepting legal checker rejects every invalid successful-trace probe exercised.
The independent tied-pot correction also passes a complete real host/checker control.
The remaining findings concern the separately promised strict parser: it still admits
schema-invalid event values and internally contradictory failed terminal records.
Neither finding is represented as a successful legal-replay bypass.

## Required corrections

### B-01 - Important: failed-terminal consistency is conditional on passed=true

Confidence: high; reproduced on CPython 3.11.15 and 3.14.6.
Location: frozen `src/pontius/v0a/trace.py:900-926`, especially the guard at line 910.
Contract: ADR-0485 failure vocabulary and trace schema; R2-05 terminal consistency;
R2-06 strict admission. An interrupted response forces complete=false, passed=false,
and accounting_complete=false. Failed/incomplete hands carry no settlement. The
terminal retains the primary typed reason rather than erasing or replacing it.

Concrete real-path reproduction: run `ReplayHost(FIXTURE_A)` with an ordinary real
`ActionMailbox`. Its wrapper calls the real mailbox first, receives the real receipt,
then arms the monotonic witness to return bool on the next read. The host produces
one known accepted action, matching interrupted decision/failure rows, and a terminal
with interrupted_response_count=1, reason=clock_invalid, complete=false, passed=false,
accounting_complete=false, and settlement=null. The unmodified failed trace parses.

Starting from that real trace, independently recompute both hashes after each mutation:

1. Set terminal complete=true and accounting_complete=true while retaining the
   interrupted response, null category totals, and passed=false.
2. Set terminal failure_reason=null, or separately replace it with invalid_event.
3. Supply the successful A control's settlement on this incomplete failed hand.

`parse_trace` accepts all four mutations on both interpreters. The cause is visible:
the terminal-record consistency checks are guarded by `if terminal["passed"]`.
The parser checks decision/failure pairing but does not extend the required terminal
implications to failed traces. The legal checker rejects these prefixes because
passed remains false; that contains legal acceptance but does not satisfy strict
failed-record admission or make their accounting/cause/settlement metadata trustworthy.
This is a trace-reader finding, not a claim about the separately owned publication
or runtime accounting correction.

Required outcome and verification: reject contradictory failed terminals with typed
TraceInvalidError. Enforce interrupted/unknown-delivery implications, unsuccessful
settlement nullability, accounting completeness versus available measurements, and
terminal primary-reason consistency across the admitted record stream. Keep valid
failed prefixes inspectable and preserve completed timing/known delivered actions.
Run real accepted-interruption, nondelivery/unknown-delivery, and late-completed
controls; independently rebind both hashes for each terminal mutation. No particular
implementation technique is required.

Evidence: `checks/cold-b-probe.py`, observations
`honest_accepted_interruption`, `interrupted_claims_complete_accounting`,
`interrupted_erases_primary_reason`, `interrupted_replaces_primary_reason`, and
`failed_prefix_carries_settlement`; both `cold-b-*-probe.log` and receipt files.

### B-02 - Important: private-card order is missing from strict event admission

Confidence: high; reproduced on CPython 3.11.15 and 3.14.6.
Location: frozen `src/pontius/v0a/trace.py:660`, `_validate_cards` at lines 625-633.
Contract: ADR-0485 explicitly requires an ascending private pair; R2-06 requires the
complete nested schema. The unchanged `HandStartedEvent` value contract rejects a
nonascending pair, so this is an established schema invariant, not a new restriction.

Concrete reproduction: take a real successful A trace, reverse its private pair from
[32,45] to [45,32], then independently rebind the semantic and prefix digests.
`parse_trace` accepts the result. Constructing the corresponding exact
`HandStartedEvent` rejects it with `private cards must be two distinct ascending cards`.
The parser only checks two in-range distinct cards; it never checks their order.
The legal checker later rejects the mismatch against the supplied fixture. This is
therefore bounded to strict parsing, but the claimed complete event schema remains
unclosed and the two admission boundaries disagree on the same serialized value.

Required outcome and verification: typed parser refusal for descending private pairs,
while ascending pairs remain valid and board reveal order remains order-sensitive
rather than being sorted. Exercise the real serialized hand-start row, recompute both
hashes, and include ascending, descending, duplicate, bool, and out-of-range controls.

Evidence: `checks/cold-b-probe.py`, `descending_private_pair` in both probe logs,
including the value-model rejection and legal-checker refusal.

## Design verdict and advisory engineering guidance

**STRAINED.** The independent accepting walk is a suitable design: it owns legal/card
state, binds external expectations, directly calls the sealed policy lookup, and does
not rerun the host or runtime selector. No replacement of that walk is recommended.
The parser's shape is weaker. Separate hand-written event checks duplicate value
invariants, while cross-row rules accumulate in a success-only post-pass. B-02 shows
actual divergence between the duplicate validators; B-01 shows the one-sided terminal
logic omitting required failure implications. Those observed mechanisms support this
design verdict without any inferred history of earlier rounds.

Advisory alternative: keep raw canonical/key/type admission separate, then use one
explicit source for event value invariants and a compact terminal-state implication
check covering success, interrupted, unknown-delivery, and ordinary failure forms.
Validating decoded exact events through the existing value constructors, or a shared
pure value validator, can prevent schema drift. A table-driven terminal check can
make all implications visible. This is bounded trace validation and focused test work;
it need not rewrite replay, change sealed kernels, or enter publication/accounting
scope. The binding outcomes are B-01/B-02; this implementation advice adds no gate.

Advisory hygiene: stored changed blobs are LF-only, BOM-free, and have no trailing
whitespace. Eleven added lines exceed the repository's 100-column convention; the
identity receipt lists all long lines, including four pre-existing test lines. This
is not the basis of the NOT CLEAN verdict.

## Independent inventory and deferred-claim comparison

Initial inputs were limited to handoff/candidate/manifest, current CLAUDE.md and
workflow.md, the frozen ADR-0485 and ADR-0484 brief, permitted R2-05/R2-06 requirements,
and frozen source/tests. No implementer transcript/plan/self-report or current peer
review was read. The independent inventory was written before opening coverage.md:

- `checks/cold-b-inventory.md`
- SHA256 `dc0387c8391ef0cc86552ff17ffe1aa3dc77dc0d5724ca772457fc8a5c0f3885`

Deferred coverage SHA256 independently matched
`007168c11b2554994ec24b1b6c821e17636f85b75257a84258c1304ac68c53d7`.
Its external-binding/legal-walk and oracle claims have direct supporting evidence.
Its nested-schema completeness claim misses the ascending private-pair member.
Its focus on successful-terminal consistency omits the failed-terminal implications
already named in the independent inventory and required by ADR-0485. These are
reproduced behavioral defects, not findings based only on missing tests. The deferred
implementer GREEN/RED counts were not used as reviewer execution evidence.

| Requirement/risk | Fresh evidence | Result |
| --- | --- | --- |
| Frozen ref/base/tree/blob manifest and four-file scope | Independent Git blob hashing | Pass |
| Raw canonical and nested schema admission | 34 trace tests + independent mutations | Fail: B-02 |
| Timing/failure/count consistency | Real accepted interruption + terminal mutations | Fail: B-01 |
| Source/config/policy and legal action acceptance | 53 replay tests + rebound probes | Pass within tested scope |
| Chance, selection, fold/all-in controls | Existing focused suite through real boundaries | Pass |
| Independent folded-depth tied settlement | New complete tied-board host/checker control | Pass |
| No host/selector rerun during verification | Real profile observation | Pass |
| Host completion/publication, broad population | Deliberately outside review execution | Not claimed |

For the new oracle control, legal public actions establish contributions
(0,1,2,15,15,5), with only seats 3/4 live. Both cover every contributed depth, so
sum(contributions)=38 is one eligible award. A royal-flush board makes both winners
equal independently of their private cards. The real host and accepting checker
produce pot ((38,(3,4)),), payouts (0,0,0,19,19,0), and final stacks
(20,19,18,24,24,15). No production side_pots/settle result supplies that expectation.
A profile observer sees no ReplayHost.run, HandRuntime.dispatch, or runtime selection
wrapper call while the accepting checker runs.

## Execution and receipts

Disposable detached snapshot, outside packet and primary checkout:
`D:/Pontius-review-snapshots/v0a-i01-ab-r005-cold-b-6a4792407cb04db0bb71d7435cc981c2`

Execution used actual `D:/Pontius-tools/py311/Scripts/python.exe` 3.11.15 first,
then actual `D:/Pontius/.venv/Scripts/python.exe` 3.14.6. Every payload used -B -P,
snapshot-root cwd, snapshot/src PYTHONPATH, PYTHONNOUSERSITE, and a whitelisted
SYSTEMROOT/WINDIR/TEMP/TMP environment with no PATH. PONTIUS_GIT was the absolute
`C:/Program Files/Git/cmd/git.exe`; tool paths were regular/non-reparse. Preflight
proved interpreter versions, flags, and trace/replay/model/runtime module origins.

Commands for each interpreter, in the above order:

- `<python> -B -P <snapshot>/tests/test_v0a_trace.py`: exit 0, 34 tests.
- `<python> -B -P <snapshot>/tests/test_v0a_replay.py`: exit 0, 53 tests.
- `<python> -B -P <packet>/checks/cold-b-probe.py`: exit 0, independent assertions
  confirm the passing controls and reproduce both required findings.

This is 87 existing focused tests per interpreter; no broad/GPU suite was run.
Probe exit 0 means the declared observations were reproduced, not a CLEAN candidate.
One incidental probe label `boolean_record_index` actually mutates source_commit to
an array; its receipt is treated only as that source-type rejection. The existing
focused suite separately exercises a bool record index.

Receipts: `checks/cold-b-identity.json`, `cold-b-311-suite-receipt.json`,
`cold-b-314-suite-receipt.json`, `cold-b-311-probe-receipt.json`,
`cold-b-314-probe-receipt.json`, and `cold-b-final-status.json`; accompanying logs
retain exact stdout/stderr. The runner scripts retain commands and environment setup.
Manifest recomputation matched the stored whole-row-sorted bytes exactly. Ref, parent,
and tree matched the pinned identities; only the four declared files differ.

Final snapshot git status was empty. A read-only sandbox status call first refused
ownership; repeating it under the snapshot owner's scoped execution succeeded.
No safe.directory/global Git configuration change was made. No source/test/config
edits, dependency installs, primary-checkout test payloads, lifecycle/owner launches,
ceremonial commits, pushes, or publication/accounting/Slice C corrections were made.
The verdict earns no broad-suite, integration, source-seal, or invocation claim.
