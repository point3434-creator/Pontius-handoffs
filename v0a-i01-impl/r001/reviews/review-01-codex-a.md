# Independent cold review A - v0a-i01-impl/r001

Reviewer: Codex, independent agent /root/slice_a_cold_a
Date: 2026-08-30
Tier: C
Verdict: NOT CLEAN - six Important material findings
Specification axis: FAIL
Engineering-correctness axis: FAIL
Confidence: high for the reproduced failures below
Finalizer: Claude; this review grants no integration or commit authority.

## Frozen identity and scope

Ref: refs/heads/review/v0a-i01-impl/r001
Commit: 2d059f90fb6cec27e4090ad0432c68759a760960
Manifest SHA-256:
fc090d962a914b41dec932f21a6c8421499191ccac9dca40363a078cbba95b0c
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 7672cad16e0624db73e38095cf3d70d74144b8da

Every finding below binds to this commit/manifest pair. Source locations are
line numbers in the frozen Git blobs, not mutable checkout files.

Known: independent absolute-Git reads confirmed the ref, tree, parent, and
exactly five additions: src/pontius/v0a/{__init__,model,clock,runtime}.py and
tests/test_v0a_hand_replay.py. I independently recomputed SHA-256 for every
changed blob through raw Git stdout bytes, sorted complete digest/path/LF
rows using ordinal ordering, and reproduced the manifest above. No working
implementation bytes were used. The base and candidate preserve the sealed
dependencies and governance inputs.

Cold inputs were the packet handoff/candidate identity, frozen CLAUDE.md,
workflow and amendment, ADR-0485, the brief, relevant charter/architecture
sections, and the sealed interfaces. I did not read the implementer's
self-report, plan narrative, other review reports, or implementer transcripts.
The coordinator supplied fresh diagnostic code and raw execution outputs for
scenarios raised during this independent review; those receipts were inspected
directly, not accepted as another reviewer's verdict.

Trace serialization, replay, the explicit-deal host, independent settlement
oracle, terminal accounting/receipt, boundary classification, inventory, and
CI are deferred slices B/C. Their absence is not a finding here.

## Material findings

### A-01 - Important / high impact: reveal work precedes the response wall

Frozen locations: runtime.py:285-315, especially 307-315; related opponent
validation at 249-274. Requirement: ADR-0485:199-213 and brief criterion 2
place the outer boundary first at host dispatch, before validation and visible
card construction.

Reproduced on both interpreters: after a legal preflop round with controlled
seat 1, inject 16,000,000,000 ns into the real OneSeatCardState.advance_to
operation while delegating to its unchanged implementation. Dispatch the legal
flop event (20,21,22). Arrival is 1,000 ns, but the recorded wall starts at
16,000,001,000 ns. The outcome is decided, elapsed_ns=0, and
deadline_crossed=false. The real mailbox contains the new accepted action.

The runtime has spent more than the entire wall processing the triggering
event while reporting a timely action. The ordinary legal transition and
real mailbox run; the diagnostic changes elapsed time, not their semantics.
The existing late-start test covers hand initialization with a ticking clock
and does not cover this reveal path.

Smallest correction: establish the outer transition boundary at dispatch
before any event validation or visible-state work, carry that boundary through
the handlers, and classify/close the complete interval through the public
ledger APIs. Do not move or reconstruct the start after transition work.

Evidence keys: reveal_work_before_wall in both v3 probe logs.

### A-02 - Important / high impact: policy input is neither immutable nor bound

Frozen locations: runtime.py:60-98, 151-159, 483-489, 650-665.
Requirement: ADR-0485:103-109 and 168-180; brief criteria 3-4. Selection must
receive an immutable blueprint only, bind its canonical digest at hand
initialization, and implement the exact table-hit/passive-miss split.

Reproduced on both interpreters: a replaceable source delegates to a genuine
ImmutableBlueprintActionSource when the hand starts, then delegates to a
different source before the first controlled action. The runtime accepts the
action and records the replacement digest, without rejecting the changed
policy. Initial digest:
b189570fcb7ea6779bc6aaa4b51fb6819d473cc0ecc890a3681ca1ed1b2aa33e
Recorded replacement digest:
c7910df470560f8d3b79363107a311708b2d5bbdc6bcf42b73c9aeb10db6d060

A second direct probe supplies the currently accepted duck-typed source shape:
digest equals a genuine empty table's digest; action_for returns a correctly
keyed BlueprintSelection with raise_to(6), table_hit=False, and that digest.
The real runtime and mailbox accept the raise and label it passive_default.
A miss in this context must call; it cannot raise.

These probes intentionally use malformed/custom source objects, not a claim
that the sealed immutable class mutates spontaneously. The defect is that the
public runtime explicitly accepts those objects and does not enforce its
source contract. Source inspection further establishes that arbitrary source
objects/closures can carry dealer or future data directly into action_for;
this is ordinary argument data flow, not malicious Python introspection.
The probes establish source substitution and fabricated policy output, not a
completed hidden-deal host isolation test.

Smallest correction: admit only the specified immutable source/value closure,
bind and validate its canonical digest at hand initialization, and reject
mismatched source/key/hit/action bindings before emission. Keep fault/delay
injection outside the production policy object's accepted data surface.
A correctly shaped BlueprintSelection is not enough to authenticate a lookup.

Evidence keys: blueprint_identity_swap and fabricated_passive_default.

### A-03 - Important / high impact: completed showdown accepts replacement results

Frozen locations: runtime.py:329-381, especially 342-379.
Requirement: ADR-0485:138-157 rejects events after completion and provides
one terminal settlement path.

Reproduced on both interpreters: run a legal passive six-seat hand through
river, submit showdown strengths (1,2,3,4,5,6), and settle. hand_complete is
true and the payout vector is (0,0,0,0,0,12). Submit another showdown result
with the next contiguous event index and strengths (6,5,4,3,2,1). It is
accepted and settle now returns (12,0,0,0,0,0).

The terminal state bypasses the nonterminal guard and the handler overwrites
_strengths. This is an event/state defect in the delivered hand core, not a
request to implement the deferred independent settlement oracle. The kernel
is unchanged; the accepted terminal input is mutable through a second event.

Smallest correction: make showdown-result acceptance a one-time transition
and refuse further host events after that completion, without replacing the
previous terminal strengths or settlement state.

Evidence key: repeated_showdown.

### A-04 - Important / high impact: mailbox acknowledgement is not validated

Frozen locations: runtime.py:538-558 and 698-704; model.py:287-316.
Requirement: ADR-0485:219-226 and 410-427 requires known synchronous
acceptance, distinguishes ambiguous publication, and forbids retry.

Reproduced on both interpreters: an admitted mailbox object's deliver method
returns None without accepting anything. The runtime ignores its return
value and produces a successful decided outcome with completed timing.
Separately, a wrapper calls the real ActionMailbox.deliver, then raises
ClockInvalidError before returning the receipt. The real mailbox has one
acceptance, but the failure reports delivery_status=not_attempted and no
delivered action.

The first schedule is a malformed/injected mailbox, not a claim that the
provided ActionMailbox silently loses actions. The second exercises real
acceptance under a failure schedule. An exception without acknowledgement
cannot prove acceptance, but it also cannot establish not_attempted. This
finding concerns receipt and delivery-state handling, not storage durability.

Smallest correction: require an exact matching acknowledgement for known
acceptance, treat absent/mismatched acknowledgement as ambiguous failure,
and classify exceptions from an attempted delivery conservatively regardless
of their exception class unless rejection before acceptance is established.
Never retry. Preserve known accepted actions only where acceptance is known.

Evidence keys: missing_delivery_acknowledgement and
clock_exception_after_acceptance.

### A-05 - Important / medium impact: clock failures escape or erase a valid start

Frozen locations: runtime.py:219-236, 271-280, 312-321; clock.py:46-56.
Requirement: ADR-0485:337-350 and 403-435 requires typed terminal failures,
retained valid interrupted starts, and no repair of a failed clock.

Reproduced on both interpreters:
- An invalid first clock value escapes dispatch as ClockInvalidError.
- An invalid next opponent-boundary read also escapes as ClockInvalidError.
- A clock callable raising OSError escapes as OSError.
- An invalid third read of initial dispatch follows a valid outer boundary
  start, but returns clock_invalid with timing absent.

The outer construction/start calls precede the handler try blocks. The
witness poisons itself but rethrows arbitrary source exceptions without the
typed vocabulary. The initial handler explicitly passes wall_start_ns=None
when V2 construction fails after the outer start, losing an observed response
prefix. These paths cannot supply the required complete typed failure record.

Smallest correction: cover all clock observations at ingress and transition
closure with typed failure handling; translate clock-source failure to the
clock vocabulary; carry a start only when its observation succeeded and
retain that exact start in interrupted timing. Mark the runtime terminal and
do not query a known-broken clock to fill missing values.

Evidence keys: invalid_initial_clock, invalid_later_boundary_clock,
clock_source_exception, and third_read_clock_failure.

### A-06 - Important / medium impact: interrupted timing forgets proven cutoff

Frozen locations: runtime.py:516-521, 559-565, 675-696.
Requirement: ADR-0485:337-354 retains true cutoff/deadline flags established
by a valid outer snapshot even when the closing measurement is interrupted.

Reproduced on both interpreters: perform 14,000,000,001 ns of decision work,
then accept the action through the real mailbox and poison the next clock
read. The ready snapshot has already established the cutoff crossing. The
returned full decision and failure correctly retain known delivery and
interrupted timing, but work_cutoff_crossed is null. _interrupted_timing
always sets both flags null, discarding the established observation.

The hand still fails, so this is a bounded evidence-fidelity defect rather
than a successful late-hand claim. It nevertheless violates the frozen
timing variant and erases a known violation from the record.

Smallest correction: retain the true flags established by prior valid outer
snapshots and pass them into interrupted timing; leave only unestablished
flags null. Do not read the failed witness again.

Evidence key: established_cutoff_lost.

## Nonblocking ruling and test-quality limits

Retain the controlled-seat opponent-event guard at runtime.py:262-267 as
defense in depth. Removing it yields the same externally visible event_order
through the wrong-actor guard; mutation survival does not establish missing
behavior. The explanation at tests/test_v0a_hand_replay.py:396-400 identifies
that equivalence. This is not a material finding and does not require a fix.

No performance claim or performance blocker is issued. The existing suite
does cover ordinary hits, passive defaults, illegal hits, ordering checks,
fresh repeated-action walls, reserve/deadline edges, real duplicate mailbox
acceptance, and accepted-then-clock-failure record retention. Its four-input
signature/source-string check is not proof that the accepted source object
cannot carry hidden data. Its context-breaking source double does not by
itself prove validation of a malformed real decision context. The existing
green results therefore do not refute the reproduced boundary failures.

## Evidence and execution record

Final direct evidence is in checks/ within this packet:
- codex_verify_slice_v3.py
- codex_adversarial_probes_v3.py
- codex-py311-v3-identity.json and codex-py314-v3-identity.json
- codex-py311-v3-verification.json and codex-py314-v3-verification.json
- codex-py311-v3-suite.txt and codex-py314-v3-suite.txt
- codex-py311-v3-probes.txt and codex-py314-v3-probes.txt

The coordinator executed these runs; I inspected the driver, probe source,
identity receipts, verification receipts, complete diagnostic outputs, and
suite conclusions before issuing this verdict. Each interpreter executed:
its recorded absolute executable, -B -P tests/test_v0a_hand_replay.py -v;
then the same executable with -B -P and the absolute v3 diagnostic script.
Full exact argv and snapshot cwd are retained in the verification receipts.

Observed: CPython 3.11.15 and CPython 3.14.6 each ran all 36 existing tests
successfully, exit 0, reported duration 0.012 s. Each diagnostic script also
exited 0 because it records outcomes; that exit is not a contract pass.
The failure outcomes listed above reproduce on both interpreters.

The v3 driver records and asserts sys.executable, sys.implementation.name,
and full sys.version before any runtime import. It uses fresh D:-local
detached snapshots of the frozen candidate, no hardlinks/alternates, a
scrubbed child environment, exact snapshot PYTHONPATH, -B -P, and absolute
C:/Program Files/Git/cmd/git.exe as PONTIUS_GIT. It asserts candidate identity,
snapshot module resolution, clean status, and final changed-file byte hashes.
Import checks observe required NumPy and no CuPy/Torch import.

An earlier coordinator setup incorrectly banned required NumPy and stopped
before tests; the retained setup note classifies this as a harness error.
V2 lacked the full before-import interpreter identity receipt; v3 corrects
that with fresh snapshots. These are reviewer-harness corrections, not source
changes, and neither earlier attempt is relabeled as acceptance evidence.

My own initial read-only manifest-script launch through the workspace venv
was denied before Python execution. I then recomputed the manifest using
raw .NET process-output streams from absolute Git. No test payload was run
from the primary checkout. Only this report and my attributed ledger line
were written by this reviewer, after the coordinator granted the serialized
writer slot. No production/test bytes, refs, commits, or lifecycle identities
were created or modified.

## Requirement-to-evidence disposition

| Requirement/risk | Evidence | Result |
| --- | --- | --- |
| Frozen identity and additive scope | Independent blob manifest/diff | Pass |
| Event order and completed-state stability | Normal tests; repeated showdown | Fail A-03 |
| Immutable policy/digest and miss semantics | Source swap; fabricated miss | Fail A-02 |
| Complete ingress response wall | Real reveal operation with delay | Fail A-01 |
| Typed clock interruption and start retention | Initial/later/third/source faults | Fail A-05 |
| Delivery acknowledgement and ambiguity | No ACK; real acceptance then fault | Fail A-04 |
| Interrupted known flags | Late work then post-ACK fault | Fail A-06 |
| Ordinary action/context record values | Existing tests and source inspection | Partial |
| Genuine CPU interpreter slots | Fresh v3 identities/imports and 36 tests | Pass for scope |
| Deferred B/C contracts | Explicit handoff exclusion | Not assessed |

Opposing evidence: all 36 existing tests pass on both required interpreters,
normal kernel integration and provided mailbox behavior work in those cases,
and no sealed dependency is changed. That evidence does not exercise the
failing schedules above.

Largest remaining unknown: integration with the deferred trace/host/accounting
slices. No end-to-end source seal, independent settlement, replay campaign,
timing result, strategy result, or full increment acceptance is claimed.

Cheapest falsifying checks are the named v3 scenarios against a newly frozen
correction, followed by the focused suite. Their expected corrections are:
charge the full reveal interval; refuse substituted/fabricated sources;
reject a second showdown; retain typed clock failure/start evidence; refuse
unacknowledged delivery; and retain proven interrupted flags.

Kill criterion and recommendation: this round cannot receive CLEAN while any
of A-01 through A-06 survives. Fix only in a new authorized implementation
round, retain this candidate/report unchanged, and repeat independent review.
Do not spend broad acceptance gates or infer commit authorization from this
focused review.
