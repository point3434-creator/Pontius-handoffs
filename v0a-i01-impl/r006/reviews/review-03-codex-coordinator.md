# r006 coordinator verification

Codex /root, 2026-08-30. Additional verification and reconciliation, not a cold
pass. NOT CLEAN; three Important mechanisms in one R2-03 contract.
Design verdict: STRAINED at the new owned-operation exception protocol.

Candidate: c74b80628a89938ca585ef3240b5c267a7174d0f
Manifest SHA-256: 2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f
Ref: refs/heads/review/v0a-i01-impl/r006
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: a22414541973b76ddd1efa1ca8fc41f51b7a4065

## R6-C01: a marker's type is still substituted for retained-cause evidence

Important / Medium; high confidence. runtime.py:56-57, :412-413 and :425-426;
replay.py:526-529 and :582-583.

A public oracle callback raises the exported OperationFailed without any
current-host journal entry. Both owners simply rethrow it and the host assumes
the body cause is already retained. On A/B, the receipt fails but has primary
null, secondary [], and accounting_complete=true. Four/two real delivered
actions remain. Required: an unrecorded body failure must be retained with its
typed operation cause, before cleanup, not disappear because of its class.

A real foreign HandRuntime.owned_bookkeeping operation produces the same
marker after recording its ValueError in that other runtime's journal. Passing
that exception out of the oracle still leaves this host's journal empty. This
supports the ownership distinction; arbitrary cross-runtime nesting is not
claimed as a newly supported measurement feature or a separate blocking
contract. The minimal unowned-marker case needs no nested ledger and no private
state access.

With a later actual cleanup clock fault, that later fault becomes the only
reported cause. The initiating settlement failure remains lost. This is the
same R2-03 invariant, not a new value-admission or policy finding.

Evidence: coordinator-*-ownership-probe.txt, modes unowned_marker and
foreign_owner; coordinator-*-builtin-error-probe.txt additionally compares the
full mailbox envelope mapping and complete returned decisions with healthy
controls. Both comparisons pass for the unowned-marker cases.

Required outcome: validate retention for the current operation/journal before
suppressing an error as already recorded. Do not deduplicate by exception class,
code membership or nonempty journal. Genuine repeated same-code failures must
remain distinct. A verifiable owner/occurrence record is advisory design
guidance; exact representation is not prescribed.

## R6-C02: exception normalization invokes fallible caller-defined behavior

Important / Medium; high confidence. runtime.py:389-396, :414-416, :427-429.

The new catch path invokes isinstance(error, Clock...) and str(error) before
emitting its signal. Both can run code supplied by the exception object.

1. A public oracle raises a built-in ValueError(BadMessage()), where the
   argument's __str__ raises TypeError. The new str(error) call raises while
   translating the original failure. TypeError escapes ReplayHost.run, so there
   is no completion receipt. The original settlement_mismatch was recorded,
   and four/two delivered envelopes remain exactly equal to healthy controls.
2. An ordinary Exception subclass with a raising __class__ property fails in
   classify's isinstance at runtime.py:392. It escapes with no recorded cause.
   The separate classification-trace capture pins the actual stack.
3. If that property's value instead impersonates ClockReversedError, an
   ordinary non-clock exception is recorded as clock_reversed while the
   monotonic source remains healthy. Its actual type MRO is
   MisleadingException -> Exception -> BaseException -> object.

These are real public oracle exceptions through the changed production
handlers. No helper replacement, method monkeypatch, journal mutation or
standalone invalid-object acceptance argument is used. The default oracle
does not generate these injected errors; this is the host's declared generic
body-exception containment boundary.

Required outcome: a caught body error must not cause a new escape or invented
type during classification/transport. Preserve the original typed cause and
finish fail-closed host reporting. Diagnostic formatting is optional, and must
not control correctness.

Engineering guidance: keep the failure adapter free of callbacks into arbitrary
exception objects. Inspect actual exception types using trusted type metadata;
use fixed transport text or a separate guarded diagnostic channel. Inspect the
whole propagation route, including context-manager exception translation, before
claiming that changing a single str call closes the class. Test the real host,
not classify() alone. Both owned helpers contain the duplicated conversion;
a correction should share one implementation rather than fix one copy.

## R6-C03: a dead-witness refusal is counted as another genuine clock fault

Important / Medium; high confidence. runtime.py:337-344 and :414-416.
Discovered independently by cold B, then reproduced by the coordinator.

Fail the actual shared witness at bookkeeping entry: A read 134 / B read 68.
The entry seam records the real clock failure, marks the witness dead, then
yields to the body. The public oracle samples that same witness; it refuses
without calling the underlying source again. owned_bookkeeping nevertheless
classifies that refusal as another clock_invalid cause.

Expected one cause. Actual:
- Invalid value/source exception: [clock_invalid, clock_invalid].
- Reversal: [clock_reversed, clock_invalid].

The independent source observer records only one actual fault. All six schedules
(A/B times invalid/reversed/source exception) reproduce on both interpreters;
source reads stop at the failed entry and prior delivered actions survive.

Required: retain each genuine cause exactly once and distinguish an already
failed witness's synthetic refusal from a new body-origin clock fault. The
passing r005 body-origin counterexample must remain covered: blanket suppression
of all body clock errors would reintroduce R5-02. Blanket same-code deduplication
would also violate the contract. Evidence:
coordinator-*-entry-echo-probe.txt and matching receipts.

## Progress, test quality and bounds

The old R5-01 body-before-cleanup and R5-02 direct-witness cause are fixed.
All 123 focused tests pass per actual interpreter: hand replay 35, trace 25,
replay 41, contract faults 22. Coordinator also repeats:
- 628 single-clock-fault schedules over A/B plus healthy controls.
- 56 rejected-event clock schedules plus a control.
- Six real occupied-destination writer schedules.
- 56 ordinary body-exception entry/exit/writer combinations plus two controls:
  all expected complete cause sequences match.
- Six direct-witness body faults plus two controls: all match.
- Thirty ownership observations and supplemental built-in-message,
  classification and entry-echo probes described above.

These overlapping checks are not summed as independent coverage. Diagnostic
exit 0 means capture completed, not candidate acceptance. Ownership observations
do not contain a matches field; absence of that field is not a passing oracle.
Same-runtime nested interval behavior is retained as an explicitly unadjudicated
observation, since the sealed ledger does not promise nested preparation
intervals. No nesting/accounting gate is added.

The new AST test rejects direct raw-interval attribute spellings in replay.py;
it does not prove semantic ownership or make underscore methods inaccessible.
Treat it as a useful lint-style guard. The body tests mainly assert membership;
complete sequence equality with independent actual-source events is necessary
to expose the duplicate-echo mechanism. Keep the ledger conservation sweep as
supporting evidence; its filtered clock population cannot validate all body
exception normalization or retention provenance.

## Evidence and design disposition

All scripts/captures/receipts are under checks/coordinator-*. Each receipt
records exact argv, environment, exits and capture SHA-256. Captures were LF
normalized before first issuance/hash, never rewritten afterward. The
classification-trace files add stack attribution rather than replacing earlier
observations. checks/codex-snapshots.json binds the full blob manifest and
disposable clone.

Exact CPython3.11.15 ran first, then3.14.6. Executable, CPython implementation,
full version and safe/no-bytecode flags were asserted before production imports;
each child used snapshot cwd, exact snapshot/src PYTHONPATH, scrubbed environment
and absolute Git. Snapshot stayed clean. Source HEAD/index and existing working
documentation edits were preserved.

The journal and placement of body handling inside cleanup boundaries are useful
improvements. The exception adapter still represents provenance as a nominal
marker or an exception class, and performs fallible interpretation while trying
to establish the failure result. A bounded redesign of that adapter is supported;
replacing the betting loop, hand representation, sealed ledgers or entire slice
is not. Separate (a) whether a genuine occurrence has already been retained by
this owner from (b) the transport used to exit the body; transport must not
invent, hide or execute an occurrence.

This is the fourth residual of R2-03. The handoff records a controller condition
to change implementers if the contract remains open. This review neither assigns
a fifth attempt to the current author nor begins implementation. The coordinator
disposition must carry that condition forward; the working contract's needs
are not a judgment of the author's worth or of all previous progress.

No policy, deferred trace/accounting or separate value-boundary contract is
reopened. No broad/GPU suite, experiment, source change, source commit,
integration, performance claim or increment acceptance was performed.
