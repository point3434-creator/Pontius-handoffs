# Independent cold review B - v0a-i01-impl/r001, Slice A

Reviewer: Codex cold reviewer B (/root/slice_a_cold_b), 2026-08-30.
Role: review only; Claude remains finalizer.

**Verdict: FAIL / NOT CLEAN.** Seven material findings survive direct
verification. Specification and engineering-correctness verdicts both FAIL.
The existing 36 tests pass on both supported interpreters; passing them does
not establish the missing boundary/error behaviors below.

Identity independently verified:
- Ref: refs/heads/review/v0a-i01-impl/r001
- Commit: 2d059f90fb6cec27e4090ad0432c68759a760960
- Base: b357d333fc2393b7fc7dcf31f30c86616208c817
- Tree: 7672cad16e0624db73e38095cf3d70d74144b8da
- Manifest: fc090d962a914b41dec932f21a6c8421499191ccac9dca40363a078cbba95b0c

This reviewer read the whole five-file slice from frozen Git blobs, its tests,
ADR-0485, brief, frozen workflow, repository guidance, and relevant unchanged
dependencies. No working implementation, implementer self-report/plan narrative,
other review, or conversation transcript entered the cold pass. The coordinator
ran diagnostic schedules after this reviewer identified scenarios; this reviewer
independently assessed their source and raw results. All scenarios below
reproduce identically in fresh 3.11.15 and 3.14.6 snapshots.

Source locations mean candidate blob lines. Runtime is
src/pontius/v0a/runtime.py; model is src/pontius/v0a/model.py; clock is
src/pontius/v0a/clock.py.

## Material findings

### B1 - Important / High: visible-card construction precedes the response wall

**Location:** runtime 307-315; also opponent validation at 250-273.
**Confidence:** high, reproduced.

ADR-0485 requires the outer boundary to start first at dispatch, before input
validation or visible-card construction. The reveal handler executes
OneSeatCardState.advance_to before starting its outer boundary.

In reveal_work_before_wall, a legal flop reveal arrives at clock 1000 after a
completed preflop with controlled seat 1. A delay wrapper advances the clock by
16,000,000,000 ns and executes the real advance_to. The real runtime/mailbox
deliver, returning decided, wall_start_ns=16000001000, elapsed_ns=0,
deadline_crossed=false. A response beyond the 15-second wall is reported timely.
The wrapper adds time around real production work; it does not replace a ledger
or legal transition.

**Correction:** establish the outer ingress boundary before all validation/card
work and classify that entire interval once the actor is known. Preserve the
separate terminal-verification treatment. Tests 579-612 only exercise initial
hand-start/lookup timing and miss this reveal path.

### B2 - Important / High: clock failures escape dispatch or lose a valid start

**Location:** runtime 219-220, 235-236, 273, 314, 351-361; clock 49-53.
**Confidence:** high, reproduced.

Outer construction and several boundary reads are outside clock-failure
handling. The V2 setup catch explicitly passes wall_start_ns=None despite a
successful outer start. Ordinary witness-source exceptions are re-raised raw.

Four direct schedules establish the consequences:
- invalid_initial_clock: a Boolean first sample escapes as ClockInvalidError.
- invalid_later_boundary_clock: a Boolean sample on the next valid opponent
  boundary likewise escapes, instead of returning a failure outcome.
- third_read_clock_failure: valid samples 1001/1002 establish the outer start;
  invalid sample three returns clock_invalid with timing_present=false.
- clock_source_exception: an OSError from the supplied source escapes as OSError.

ADR-0485 requires typed failure outcomes and retained interrupted timing after
an established input/response boundary. **Correction:** contain every dispatch
clock read, retain established start/prefix evidence, map ordinary source faults
to typed clock failure, and never query a broken witness to repair it.

### B3 - Important / High: arbitrary sources bypass immutable blueprint authority

**Location:** runtime 151-159, 74-98, 650-665.
**Confidence:** high, reproduced.

The constructor accepts any action_for/digest object, never binds its initial
canonical digest, and selection checks returned class/action legality without
establishing that key, hit/miss, digest, and action came from the hand's immutable
authority.

In blueprint_identity_swap, a nonacting initialized hand accepts a delegating
source wrapping immutable source A; replacing its delegate with immutable B
before the first decision succeeds and records B's different digest.
In fabricated_passive_default, an accepted source claims an empty immutable
blueprint's digest but returns legal raise_to(6) with table_hit=False. The real
mailbox receives the raise, recorded as passive_default under the empty digest.

This violates both fixed blueprint identity and the frozen miss rule:
check, else call, else fold. **Correction:** restrict/validate the source to the
permitted immutable authority, bind its canonical identity at initialization,
and validate selection against the exact key/authority before emission.
Refusing unsupported arbitrary wrappers is a valid correction; this finding
does not claim that the unchanged ImmutableBlueprintActionSource mutates.

### B4 - Important / High: another showdown result changes a completed hand

**Location:** runtime 329-381, especially 336-342 and 378-380.
**Confidence:** high, reproduced.

The handler rejects terminal FOLD but lets terminal SHOWDOWN accept another
strength vector and increment the event index; no consumed-result guard exists.

In repeated_showdown, a legal passive six-seat hand accepts strengths
(1,2,3,4,5,6), settles, then accepts the next-index result (6,5,4,3,2,1).
hand_complete was already true. Real kernel payouts change from
(0,0,0,0,0,12) to (12,0,0,0,0,0).

ADR-0485 rejects events after completion. **Correction:** consume showdown
results once, reject later inputs, and retain the first accepted settlement
authority. This is implemented event-order behavior, not missing deferred
terminal accounting/oracle work. The current test at 870-909 ends after one
showdown and misses the mutation.

### B5 - Important / High: delivery clock exception falsely reports no attempt

**Location:** runtime 539-553, especially 547-548; helper 698-704.
**Confidence:** high, reproduced.

A ClockInvalidError/ClockReversedError from mailbox.deliver uses a helper whose
delivery_status defaults to not_attempted, unlike the ordinary exception branch
which correctly preserves uncertainty.

In clock_exception_after_acceptance, the supplied mailbox calls the real
ActionMailbox.deliver, then raises ClockInvalidError before returning its
acknowledgement. The real mailbox contains one action, but the failure says
clock_invalid/not_attempted and delivered_action is null.

The runtime attempted publication and lacks a returned receipt: its knowledge
is unknown, not known acceptance and not nondelivery. ADR-0485 prohibits losing
that uncertainty. **Correction:** classify all exceptions after delivery entry
by actual acknowledgement knowledge regardless of exception class, preserving
clock failure information and prohibiting retry.

### B6 - Important / Medium: a normal return is accepted without acknowledgement

**Location:** runtime 539-558, especially 540.
**Confidence:** high, reproduced; malformed supplied-component boundary.

The return value of mailbox.deliver is discarded, so neither exact receipt type
nor hand/action identity is checked before completed timing and a decision are
reported.

In missing_delivery_acknowledgement, the constructor accepts a supplied mailbox
whose deliver returns None and accepts nothing. Dispatch returns decided with
completed timing. This does not allege a defect in built-in ActionMailbox; the
runtime admits the malformed component and claims delivery without its required
receipt.

**Correction:** require an unambiguous correctly bound DeliveryReceipt before
claiming known acceptance; fail closed without retry if acknowledgement is
missing or malformed. ADR-0485 places synchronous acknowledgement at the
delivery boundary.

### B7 - Important / Medium: interruption discards previously established limits

**Location:** runtime 516-521, 559-565, 675-695; discarded boundary snapshot 413-420.
**Confidence:** high, reproduced.

The ready checkpoint establishes a cutoff flag, but _interrupted_timing always
writes both flags as null when a later observation fails.

In established_cutoff_lost, real immutable lookup completes after
14,000,000,001 ns of injected decision work. The real mailbox accepts, returns
its receipt, then poisons the next sample. The full interrupted decision
correctly retains accepted delivery, but work_cutoff_crossed is null although
the ready snapshot had established true.

ADR-0485 permits null only for an unestablished interrupted flag.
**Correction:** retain monotonic true flags from valid outer observations
before/after blueprint work and at readiness, and reuse them without retrying
a broken clock. Test 779-801 has no prior cutoff crossing and cannot expose
this loss.

## Nonblocking observations and test limits

- Model 107-110 validates schema_version by equality without exact str;
  model 440 accepts any nonempty ASCII spine_reason rather than V2's enum
  spelling. These are source-inspection guard observations, not executed
  parser defects, and add no blocking finding here. Trace parsing is deferred.
- Test 539-554 injects a source ValueError rather than constructing a genuinely
  invalid card/betting/decision context; it proves classification, not complete
  context validation. Runtime visibly calls the unchanged key builder.
- The 36 tests cover basic event rejection, legal hits/misses, repeated-action
  indices, cutoff/deadline edges, and selected delivery failures. They omit the
  materially different schedules above.
- Trace/replay, explicit-deal host, independent settlement oracle, terminal
  accounting, boundary classification, inventory, and CI were explicitly
  deferred B/C. Their absence is not a finding.
- No performance optimization or style preference blocks the candidate.
  No live timing/strength result, hidden-completion replay result, full increment
  completion, or experimental authority is asserted.

## Evidence and traceability

| Requirement/risk | Best evidence | Result |
| --- | --- | --- |
| Frozen identity and permitted five-file scope | Independent raw Git blob hashes, ref/parent/tree, packet manifest | Pass |
| Response includes ingress/card construction | Real advance_to delay through runtime/mailbox | Fail B1 |
| Typed clock failure and valid interrupted prefix | Four clock-fault schedules | Fail B2 |
| Fixed blueprint and passive miss rule | Identity swap and fabricated-passive schedules | Fail B3 |
| No input after completion | Repeat showdown and changed kernel payouts | Fail B4 |
| Honest delivery knowledge/ACK | Real acceptance then exception; absent ACK | Fail B5/B6 |
| Retained known cutoff on interruption | Cutoff then actual ACK and clock poison | Fail B7 |
| Focused suite on actual 3.11/3.14 | 36/36 tests each, exit 0 | Pass for exercised cases |
| Broader/deferred acceptance | Not run/in scope | Not assessed |

This reviewer independently hashed absolute-Git cat-file blob bytes captured
through .NET BaseStream, sorted complete digest-first rows ordinally, concatenated
LF rows, and obtained the manifest above. The separately hashed packet
manifest.sha256 and candidate.json agree. Ref, parent, and tree agree.
All five blobs are LF-only, BOM-free, have no trailing whitespace, and are
at most 100 columns. No working-file hash substituted for a blob.

The authoritative fresh receipts are in this round's checks directory:
codex_verify_slice_v3.py; codex_adversarial_probes_v3.py;
codex-py311-v3-{identity,verification}.json and -{suite,probes}.txt;
codex-py314-v3-{identity,verification}.json and -{suite,probes}.txt.
This reviewer inspected the runner, probe source, both raw outputs, identity
records, snapshot verification records, and suite tails.

Actual environments, asserted before payload import:
- D:/Pontius-worktrees/v0a-increment-1-preregistration-review/venv311/Scripts/python.exe:
  CPython 3.11.15; full version
  3.11.15 (main, Jul 23 2026, 14:42:43) [MSC v.1944 64 bit (AMD64)].
- D:/Pontius/.venv/Scripts/python.exe:
  CPython 3.14.6; full version
  3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)].

Each used a fresh detached D:-local candidate snapshot, -B -P, exact snapshot/src
PYTHONPATH, scrubbed environment, and absolute
C:/Program Files/Git/cmd/git.exe. Runtime imports resolved to those snapshots,
and snapshots/tested bytes remained pristine afterward. NumPy is required and
loaded; recorded imports included no CuPy/Torch. This narrow observation is
not a full optional-dependency audit.

Commands for each actual executable:
- <python> -B -P tests/test_v0a_hand_replay.py -v:
  exit 0; 36 tests, OK, no reported skips.
- <python> -B -P D:/Pontius-handoffs/v0a-i01-impl/r001/checks/codex_adversarial_probes_v3.py:
  exit 0; eleven diagnostic observations emitted. That exit means diagnostics
  ran successfully, not that the observed candidate behavior passed.

Earlier retained coordinator runs contained reviewer-harness limitations:
an initial NumPy prohibition contradicted the declared base dependency, and v2
omitted full pre-import interpreter provenance. Fresh v3 receipts close those
limitations without changing candidate bytes. This reviewer's initial Python
hash-launch attempt was denied before execution; independent .NET byte hashing
then succeeded. No test payload ran from the primary checkout; no production,
test, ref, commit, lifecycle, or evidence bytes were modified by this review.
