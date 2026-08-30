# r005 coordinator verification

Reviewer: Codex /root, 2026-08-30. Additional verification and reconciliation;
not a third cold review. Verdict: NOT CLEAN. Two Important mechanisms remain
within one contract, R2-03. Design verdict: STRAINED at host exception ownership.

Candidate: a8582e6d6b53b55415dab79c4a54e252d00b74ad
Manifest SHA-256: e9b0baf12e258d66a92169d38137cbf2f42317158b6515ac377f745bbc52093a
Ref: refs/heads/review/v0a-i01-impl/r005
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 5d373871b27bed5ef026150b816d684a588b75c3

## R5-C01: host body exception is recorded after cleanup

Important / Medium, high confidence. Frozen replay.py:494-532 and
runtime.py:341-350. ADR-0485:269-280 requires a primary cause plus ordered
later causes; cleanup cannot reorder the initiating failure.

Public reproduction: run fixture A with an ordinary oracle callback that raises
ValueError, and a clock source that faults at observation 135 (bookkeeping
exit). The callback records its occurrence before raising. The source separately
records its own actual fault. Expected [settlement_mismatch, clock_invalid];
actual [clock_invalid, settlement_mismatch]. ZeroDivisionError and reversal
produce the same ordering defect. Fixture B reproduces at observation 69.

The outer except Exception handles the body error only after the with statement
has unwound. During that unwind bookkeeping's finally appends its own clock
failure. A single append-only journal faithfully records append order; it cannot
recover occurrence order when the producer records late.

Required result: record/classify the host body failure before leaving the
measured body; append actual cleanup causes afterward, exactly once. Preserve
clock-before-body, returned-mismatch-before-cleanup, writer ordering, no-resample
and accepted-delivery controls. No sorting or category priority is justified.

Coordinator's ordinary-exception subset: 56 schedules across A/B, ValueError/
ZeroDivisionError, no fault or entry/exit fault, three clock fault kinds and
optional real occupied-destination refusal. Twenty-four exit-fault schedules
violate order on each interpreter. Exception-only and entry-first controls
retain the expected order. A has four accepted actions and four decisions;
B has two of each. All faults are real public callback/source/writer behavior;
no helper replacement, private journal edits or production mutation.

## R5-C02: typed exception is mistaken for already-recorded provenance

Important / Medium, high confidence. Frozen replay.py:524-526 and
runtime.py:344-348, interacting with clock.py:51-70. Same ADR cause-retention
contract. Independently discovered by both cold reviewers; coordinator
subsequently reproduced the stronger real-witness case.

Give ReplayHost a public MonotonicWitness(source). The public settlement oracle
uses that same witness to time its own work. Arm the source to raise OSError,
return True, or reverse before the oracle's witness read. The actual witness
raises clock_invalid or clock_reversed and becomes failed. Cleanup correctly
avoids treating the later dead-witness refusal as a new fault, but the host's
typed catch assumes the original error was already journalled by a ledger seam.
It was not. Receipt: passed=false, failure_reason=null, secondary_failures=[].

Expected exactly the original typed clock cause. This is a genuine source fault
through real public production witness code, not an artificially corrupted ledger
or an unsupported claim based on constructing an invalid standalone object.
Six fault schedules (A/B times three kinds) reproduce on each interpreter.
Two healthy shared-witness controls pass. The failed source is never resampled;
accepted action/decision counts remain four for A and two for B.

Required result: exception type alone must not imply that its occurrence has
already been retained. Assign cause-recording ownership at the actual operation
boundary, before cleanup. Suppress only synthetic repeats, not an unrecorded
origin. Existing ledgers, witness and spine need not be rewritten.

## What is now working

Both previous r004 mechanisms are corrected:
- Real occupied destination: trace_write_failed is primary. At later publication
  exit/finalize clock faults it remains first, with the clock code secondary.
- Wrong-turn event followed by real abort fault at observation 16: event_order
  stays primary, clock_invalid/reversed is secondary, the delivered action stays.

All 119 focused tests pass per actual interpreter: hand replay 35, trace 25,
replay 37, contract faults 22. The coordinator additionally repeated 628
single-clock-fault schedules over A/B, six real writer schedules, and 56
wrong-turn clock schedules plus a control. No single-clock schedule in that
sweep escapes, loses a primary, resamples the failed source or loses a delivery
count. These checks are bounded observations, not whole-product acceptance.

## Engineering assessment and test technique

The journal is a useful improvement and removes the earlier merge/cursor/type
ranking. The remaining defect class is ownership across exceptional context
manager exits: every failure-producing operation must retain its origin before
any cleanup with another failure producer. The next search should cover
context-manager bodies and exception handlers, not only ledger-closing calls.

A bounded completion of this refactor is proportionate. Keep the working
journal and make host operation boundaries explicit. Catch/translate within the
measured body, or use an equivalent explicit outcome protocol that records before
unwind. The mechanism is advisory; occurrence order and genuine origin retention
are required. A whole hand/solver/spine rewrite would disturb unrelated working
contracts without evidence of need.

Build the category matrix over independent dimensions:
returned mismatch versus raised exception; ledger-origin versus direct witness
origin; interval entry, body, exit and finalization; alone versus later real
writer refusal. Record actual occurrence through the public injected source/
oracle, independently of runtime.record. Assert exact receipt first/rest, actual
reachability, no extra source samples and complete delivered records.

The new ledger _read_clock conservation observer checks a useful subset, but
cannot observe a direct witness call in host work and does not establish ordering
against non-clock host causes. Keep it as supporting coverage, not the whole
R2-03 oracle. No separate documentation/coverage requirement is imposed
retroactively on this frozen round.

## Evidence interpretation and limits

checks/coordinator-311-receipt.json and coordinator-314-receipt.json record
commands, environment, child exits and capture hashes. The witness receipts add
the independent reproduction after reviewer discovery. Diagnostic script exit 0
means observations were captured; it does NOT make a contract counterexample
GREEN. Snapshot identity: checks/codex-snapshots.json.

The initial unwind diagnostic also deliberately throws ClockInvalidError and
ClockReversedError from an arbitrary oracle and provisionally labels those as
settlement_mismatch. Those 56 schedules and their provisional expected type are
NOT used to establish required typed behavior or inflate the two findings.
The separate real-witness diagnostic supplies the decisive type evidence.
Of the original 114 observations, the accepted ordinary-exception subset has
24 ordering counterexamples; two default-oracle controls pass. Its aggregate
80 mismatch field must not be quoted as 80 independently adjudicated defects.

Release CPython 3.11.15 ran first, then 3.14.6, with executable/implementation/
full-version asserted and recorded before production imports. Each child used
-B -P, snapshot cwd and exact snapshot/src PYTHONPATH, scrubbed environment and
absolute Git. Root's disposable snapshot stayed clean. All raw coordinator
captures were normalized to LF before first issuance/hashing; issued evidence
was not rewritten.

This is FIX R2-03 only. Policy authority, trace/schema/accounting deferred work
and the separate value-boundary audit are not reopened. No GPU, broad suite,
installation, production edit, ceremonial source commit, integration, performance
claim or increment acceptance occurred.
