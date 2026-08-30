# Cold Tier-C review 01 - Codex A - v0a-i01-impl/r002

Verdict: NOT CLEAN. Specification: FAIL. Engineering quality: FAIL.
Confidence: high for A1-A4; high for the observed link-following behavior in A5,
medium for its unexecuted race consequence. Five Important findings remain.
Claude is the finalizer. No source correction is implemented by this review.

Candidate identity:

- Ref: refs/heads/review/v0a-i01-impl/r002
- Commit: 18c965d1f3445c253a6333c4d10899c1dcac0cc6
- Base: b357d333fc2393b7fc7dcf31f30c86616208c817
- Tree: 35f00349a7538cffc02f8e81f71913251be200be
- Manifest: 4cfd14ac7bfdb22e052bb9f625610657c01aafa07182acf58d19367a8816cb18

Every finding below binds to that commit/manifest pair. All source locations
are line numbers in that frozen commit, not mutable checkout locations.

## Material findings

### A1 - Important/P1 - Host closure can falsely pass or lose its failure receipt

Locations: src/pontius/v0a/replay.py:496-552;
src/pontius/v0a/runtime.py:254-276,293-303.
Requirement: ADR-0485:265-284, especially success requiring the measured final
publication interval and outer finalization, retaining the primary typed cause,
and returning a receipt even when a complete terminal preceded a later failure.

Concrete scenario and executed evidence: run real FIXTURE_A with the ordinary
immutable blueprint and an injected monotonic source that raises OSError on
its 138th read, the final outer-finalization observation. On both actual
CPython 3.11.15 and 3.14.6, all four actions were accepted; the returned receipt
has passed=true, accounting_complete=true, failure_reason=null, and no secondary
failures, while runtime.accounting().complete is false. The finalizer swallows
the clock failure, and ReplayHost uses the pre-finalization totals and passed
value when constructing the receipt.

The same real path fails to return any receipt when the source fails on read
137 (final publication interval closure): ClockInvalidError escapes after all
four actions were accepted. A failure on read 1 instead escapes as RuntimeError
('publication measurement requires a started hand'), losing the already typed
clock failure to unconditional terminal-publication setup. No mailbox, ledger,
or settlement double was used in these probes.

Evidence: checks/cold-a-py311-probes-v2.json and
checks/cold-a-py314-probes-v2.json, probes first_clock,
publication_close_clock, and finalization_clock.

Correction direction: make host closure an explicit failure-preserving path.
Return whether finalization completed; build the receipt from the final result,
not pre-publication totals. Catch typed start/stop/finalization faults at the
host boundary, preserve known delivered actions and the first cause, record
later failures separately, leave unobserved fields null, and never attempt to
repair or query a known-broken clock. Host success must require all closure steps.

### A2 - Important/P1 - Pre-terminal trace work disappears from accounting

Locations: src/pontius/v0a/replay.py:395-410,412-429,496-511;
src/pontius/v0a/trace.py:326-341.
Requirement: ADR-0485:240-267 requires post-delivery trace work to be measured as
uncredited preparation or post-terminal bookkeeping, including every preceding
trace-row write through the terminal's pre-publication cut.

Concrete scenario and executed evidence: wrap canonical_json with a deterministic
one-second clock advance, then call its original implementation for every real
serialization in ReplayHost.run. No production path is replaced. FIXTURE_A makes
31 calls after host construction: 29 event/decision rows, one semantic object,
and the final terminal. The injected run still passes. Both terminal totals are
unchanged from the no-delay run: preparation=0.000061 seconds and
post_terminal=0.000002 seconds. All four response durations are unchanged too.
Only the final terminal call appears in publication_seconds=1.000001. The other
30 seconds vanish from all reported categories, on both supported interpreters.

Inspection explains the result: add_event/add_decision/add_failure and semantic
projection hashing run outside runtime.bookkeeping(). The ledger does not
implicitly charge the gap between completed dispatches and the next boundary.

Evidence: both cold-a-*-probes-v2.json receipts, probe
real_serialization_one_second_each. The wrapper advances the injected witness
source and calls the unchanged serializer; this is real host/serializer execution,
not a helper-state assertion.

Correction direction: measure every post-dispatch row construction/serialization
and semantic-hash operation in the proper public outer preparation interval.
Close and classify those intervals before the pre-publication totals are read;
retain only terminal construction/serialization/write in the final receipt's
separate interval. Propagate any measurement failure through A1's host outcome.

### A3 - Important/P1 - No independent semantic replay or complete binding check

Locations: src/pontius/v0a/trace.py:583-746,749-794;
src/pontius/v0a/replay.py:383-561;
tests/test_v0a_trace.py:364-372; tests/test_v0a_replay.py:207-223.
Requirement: ADR-0485:370-391 requires a separately written checker that replays
legal transitions, compares selected actions/payouts, independently validates
source/configuration/policy identities, rejects wrong counts/digests, and checks
recorded timing against its walls. Brief criterion 7 requires independent replay.

Concrete scenario and executed evidence: start with the real successful FIXTURE_A
trace, replace its first controlled CALL with CHECK while the controlled seat
owes the big blind, and correctly recompute both prefix and semantic hashes.
parse_trace accepts it as passed=true, and parsed_semantic_sha256 agrees with
the recorded digest on both interpreters. The unchanged state-after digest and
payouts still describe the CALL. This is a legal-transition failure that a
self-consistent hash cannot detect.

Independent probes also pass when the header blueprint digest disagrees with all
decision policy digests, terminal decision_count is zero despite four deliveries,
or the first completed response lasts 16 seconds with deadline_crossed=false
and a successful terminal. A foreign terminal semantic digest is accepted by
parse_trace without even recomputing it. Null decision timing is accepted on a
successful trace. Source inspection finds only a parser and a function hashing
the supplied projection, with no legal-replay entry point or expected-source,
configuration, or blueprint argument; the host reruns its own production runtime.
The existing digest test intentionally observes inequality after parse succeeds.

Evidence: both cold-a-*-probes-v2.json receipts, probes
illegal_first_check_rebound, foreign_header_policy, zero_delivered_count,
late_action_with_false_deadline, foreign_semantic_digest, null_decision_timing.

Correction direction: add the independent trace validator required by the frozen
contract and make a validated success require it. Bind expected external source,
configuration, and policy inputs; replay accepted events and controlled actions;
verify each context/state digest and settlement, contiguous action/event indices,
exact counts, timing/failure consistency, and both hashes. Hash recomputation
alone must not be presented as successful replay.

### A4 - Important/P2 - Strict parser admits malformed and non-finite records

Locations: src/pontius/v0a/trace.py:478-502,599-620,630-719.
Requirement: ADR-0485:288-325 and the exact event schema require exact types,
finite numbers, exact event keys, valid source identity, six-seat ranges, and
the V2 spine-reason enum.

Concrete scenario and executed evidence: independently mutate a valid real host
trace, rebinding its prefix and semantic hashes where applicable. The parser
accepts every one of these on both interpreters: header record_index=false;
an event with timestamp_ns (an explicitly forbidden event field); a hand-start
event missing button; spine_reason='not-a-v2-reason'; source_commit=[]; decision
seat=6; response_compute_seconds=NaN; and terminal preparation total=Infinity.
Each parsed terminal still says passed=true. These are structural defects
independent of the missing legal replay in A3.

Inspection: json.loads has no non-finite refusal; floating validation checks
only exact float and negativity; record-index comparison uses equality, allowing
False==0; event variant keys/values are never validated; source_commit and
spine_reason are never checked; decision seat has no upper bound.

Evidence: both cold-a-*-probes-v2.json receipts, probes bool_record_index,
unknown_event_timestamp, missing_hand_start_button, invalid_spine_enum,
invalid_source_commit, out_of_range_seat, nan_response_seconds, and
infinite_terminal_total.

Correction direction: validate every decoded field against one exhaustive schema,
including exact record indices, event variants, ID/digest syntax, seat ranges,
required decision timing, V2 enums, and finite numbers. Reuse frozen-model
validation where suitable, translating malformed-data failures into
TraceInvalidError. Add field-complete negative controls rather than relying on
prefix-hash rejection to exercise each rule.

### A5 - Important/P2 - Writer resolves through links before inspecting them

Location: src/pontius/v0a/trace.py:391-403.
Requirement: ADR-0485:393-401 requires create-new writes under the explicit run
root, rejecting unsafe links and path escape without overwrite. The function's
own published contract says it never follows links.

Concrete scenario and executed evidence: in the disposable snapshot, create
cold-a-filesystem/alias as a Windows junction to cold-a-filesystem/real. Pass
alias/through-link.jsonl to the real write_trace with cold-a-filesystem as root.
On actual CPython 3.14.6 the write succeeds through the junction and creates the
file in real. The receipt records alias.is_junction()=true and the created bytes.
The link has already been erased from the pathname by resolve() when is_symlink()
is checked; ancestors and the caller's root are not inspected for reparses.

Inference, not executed: mutable parent directories can also be replaced after
resolve()/containment checks and before os.open, so O_EXCL alone does not prove
that the final open stayed under the authorized root. The executed demonstration
establishes link following; it does not claim a race or out-of-root write occurred.

Evidence: checks/cold-a-filesystem.py and checks/cold-a-filesystem.json.

Correction direction: fail closed on reparse/link components of the supplied
root/destination ancestry before resolution loses their identity, and bind the
actual create-new operation to the checked destination/root. Verify this on the
Windows path, including a real link substitution schedule, without introducing
a generalized governance transaction engine.

## Non-blocking observation

ReplayHost checks that the run ID begins with either allowed prefix, but does
not match that prefix to mode. A correctness-prefixed ID with mode='rehearsal'
returns a successful receipt (both interpreter probes). ADR-0485:481-485 assigns
the mandatory mode/root/identity gate to the future owner, which is not admitted
in this slice, so this review does not add a present-slice blocker for that
future-owner gate. Do not treat the current constructor as proving it.

## Verification and traceability

Inputs read: CLAUDE.md, docs/workflow.md, the frozen ADR-0485 and brief,
packet handoff.md/candidate.json/manifest.sha256, frozen source/tests and their
sealed dependency interfaces. No implementer self-report, prior review,
other reviewer's findings, or chat was read. Only objective fresh test receipts
from the coordinator were accepted after independent inspection was underway.
Slice C's origin policy/inventory/CI admission remains excluded as directed.

| Requirement/risk | Evidence | Result |
| --- | --- | --- |
| Frozen ref/base/tree/blob identity | cold-a-identity.json; 10 exact rows | PASS |
| Frozen line hygiene / no tracked edit | Same receipt; LF, no BOM, <=100 columns | PASS |
| Real host completion after faults | Own dual-interpreter probes | FAIL A1 |
| Pre-publication accounting | Own delayed real serialization probes | FAIL A2 |
| Legal replay / bindings / walls | Own trace-tampering probes plus source | FAIL A3 |
| Exact trace schema | Own independent field mutations | FAIL A4 |
| Link-safe trace destination | Real Windows junction / actual 3.14 | FAIL A5 |
| Run-independent semantic projection | Source and coordinator focused receipts | PASS scoped |
| Independent chip-depth oracle | Separate implementation; fixture receipts | PASS scoped |
| Existing A-fix regression suites | Coordinator fresh focused receipts | PASS scoped |
| Full operational owner / broad suites | Deliberately not invoked | OUT OF SCOPE |

Identity was independently recomputed from frozen Git blobs with absolute
C:/Program Files/Git/cmd/git.exe, rename detection disabled, whole-row byte sort,
and LF rows. The published manifest file is byte-equal to those rows and hashes
to the pinned digest. The two stated unchanged-path hashes also match. A final
snapshot audit rechecked all ten files byte-for-byte and found no tracked diff;
only the review's cold-a-filesystem/ fixture is untracked in the disposable clone.

The clone was freshly created at D:/Pontius-review-cold-a-r002 with --no-hardlinks,
--no-checkout, core.autocrlf=false, then detached at the candidate. Each diagnostic
payload ran with cwd there, -B -P, PYTHONPATH=<snapshot>/src, and a scrubbed
environment containing only SYSTEMROOT/WINDIR/TEMP/TMP/COMSPEC plus explicit
Python flags, empty PATH, and absolute PONTIUS_GIT. Before importing payloads,
it asserted actual executable, CPython implementation, full version tuple,
cwd and import path; the principal probes also verified every imported v0a
module against its frozen blob. No CuPy or Torch import occurred.

Commands and results:

- Actual 3.11.15: python -B -P checks/cold-a-probes-v2.py with explicit expected
  executable/version/output arguments, cwd the disposable clone: exit 0;
  checks/cold-a-py311-probes-v2.json retains all observations.
- Actual 3.14.6: the same bounded payload and invocation discipline: exit 0;
  checks/cold-a-py314-probes-v2.json retains all observations.
- Actual 3.14.6: python -B -P checks/cold-a-filesystem.py under the same scrubbed
  discipline: exit 0; checks/cold-a-filesystem.json retains link evidence.
- Coordinator receipts checks/codex-py311-verification.json and
  checks/codex-py314-verification.json were read as external executed facts:
  four focused suites exit 0 under each actual interpreter (99 tests per slot,
  as reported by the coordinator), with snapshot import provenance. This reviewer
  did not independently rerun those whole suites or rely on their GREEN status
  to excuse the directly reproduced contract failures above.
- Initial checks/cold-a-probes.py failed at diagnostic setup because its blueprint
  constructor omitted source_id. No hand was run in that attempt. The immutable
  original is retained; corrected create-only cold-a-probes-v2.py supplies the
  required source_id and completed both slots. That setup failure is not a
  candidate finding.

No source/test/config, sealed kernel, legacy baseline, lifecycle identity,
primary checkout file, or prior packet artifact was changed. No owner, GPU,
broad suite, commit, push, or ledger mutation was performed by this report.
Ledger append awaits coordinator serialization.

Largest remaining unknown: the full host failure matrix beyond the demonstrated
clock positions and the unexecuted link race. The cheapest falsifying controls
are the retained bounded reproductions against the next immutable candidate;
all findings require deterministic rejection or a truthful failed receipt there.
The present candidate cannot advance through the CLEAN gate or broader acceptance.