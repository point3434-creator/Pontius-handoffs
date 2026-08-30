# v0a-i01-impl/r004 disposition

Coordinator: Codex /root, 2026-08-30.
Finalizer: Claude, the first drafter.
NOT CLEAN: one residual contract (R3-02), with two Important failure mechanisms.
Design verdict: STRAINED. Recommend a bounded runtime/host cause-flow refactor.
No implementation integration or broad-suite advancement from this candidate.

## Frozen identity and scope

Ref: refs/heads/review/v0a-i01-impl/r004
Candidate: 0207430a37e1e5b31c8da8da7aa57da1bc5c88ee
Manifest SHA-256: ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: c5cf6cc281d2800727029737fd4ee05bd20ebbd3

The ref, parent, tree, ten frozen blobs and manifest verify. Only runtime.py,
replay.py and test_v0a_replay.py differ from r003. FIX scope remains R3-02
host typed closure causes, occurrence ordering, no source resampling and
delivery-record preservation. R3-01 policy authority and deferred
R2-04/05/06/09/10 are not reopened. The separately frozen value-boundary audit
does not expand this round.

## R4-01 — First trace-write cause is demoted

Important / Medium, high confidence. Attribution: both independent cold
reviewers and coordinator C-01.
Frozen replay.py:432-448, with receipt construction at :603-619.

A real write to an existing destination correctly refuses. With no earlier
failure, the receipt is passed=false but primary=null and
secondary=[trace_write_failed]. If a clock fault then occurs during publication
exit or finalization, the later clock code becomes primary and the earlier write
failure remains secondary. This occurs on both required interpreters without
writer monkeypatching or private state manipulation.

The handoff asked for an interpretation ruling. ADR-0485:269-280 defines
secondary codes as later failures and requires host publication and finalization
for success. A write failure cannot replace an earlier cause; it is itself the
first cause when no earlier failure exists. The successful betting outcome does
not make subsequent host completion failures category-exempt. No ADR amendment
is needed to establish this reading.

Required outcome: first observed typed host cause is primary regardless of
category; exactly the later causes remain secondary, in order. Keep the
opposing clock-before-write control, which already behaves correctly.

## R4-02 — Rejected-event abort drops its later clock cause

Important / Medium, high confidence. Attribution: cold A R4-A-02, independently
reproduced afterward by the coordinator in its immutable addendum.
Frozen runtime.py:424-441; host ingestion at replay.py:451-460.

An ordinary public fixture variant changes the first scripted opponent from
seat 4 to seat 5. The real runtime raises event_order after one valid controlled
action. A clock fault at observation 16 occurs while the real outer
abort_transition_boundary closes that rejected input. The receipt retains
event_order but has no secondary code; runtime.closure_failures is also empty.
Raising and boolean samples lose clock_invalid; a reversed sample loses
clock_reversed. The real accepted action and its decision survive.

Aborted transition closure is within ADR-0485:246-251, and the later typed cause
must be retained under :269-280. This is not a new event-validation or accounting
formula finding.

Required outcome: event_order remains primary; actual abort-close clock failure
is secondary. Retain its type without another source sample or lost delivery.
Merely adding the missing catch to the existing closure list is insufficient:
draining that list before the returned dispatch failure would put the later
cleanup cause ahead of the input failure that caused it.

## Improvements verified, without overstating coverage

The five advertised terminal closure seams now retain typed clock causes, and
the no-success/no-source-resampling protections survive. Both actual slots
pass 113 focused tests: hand replay 35, trace 25, replay 31, contract faults 22.

Coordinator: 628 clock-fault schedules per interpreter across A and B, covering
raising/invalid samples at every read and reversals after the first read. None
loses a primary, escapes, resamples the failed source or loses a delivery count.
Six real writer-refusal schedules expose R4-01. A separate 56-fault wrong-turn
matrix plus one control exposes R4-02 and retains the later-publication controls.

Cold A: 641 diagnostic cases per slot, including a 630-schedule clock sweep;
six expected contract mismatches across these two mechanisms. A supplemental
30 closure schedules plus two controls compares complete decision/envelope
values, not just counts, and passes. Earlier probe defects are preserved and
explicitly excluded; v3 is its completed diagnostic.

Cold B independently verifies the focused suites, clock sweep and real
writer/clock ordering; its dedicated first-cause RED fails on both versions.
These overlapping counts are not summed as unique coverage. A reversal at the
first observation has no previous sample and exercises invalidity instead;
the coordinator explicitly omits that position from its reversal count.

No normal first-fault route for the bare ledger RuntimeError was established,
so no fabricated private-ledger state is used to invent a third finding.
Cold A distinguishes zero underlying-source resamples from existing wider
dispatch cleanup attempts to call the already-failed witness, which refuses
before invoking its source. This is not a blanket claim that every path avoids
calling the witness object.

Cold B's pre-publication terminal-row observation is retained in its report
as a non-counted note for the already deferred trace/accounting work. The final
host receipt retains those particular bookkeeping causes. This disposition
does not relabel a deferred surface as a third R3-02 defect.

## Design recommendation and the next round

The design assessments differ and are preserved: cold B calls the queue/cursor
shape SOUND and treats its found precedence defect as local; cold A and the
coordinator call the cause plumbing STRAINED. The coordinator adopts STRAINED
because R4-02 additionally demonstrates that host receipt order cannot recover
the original runtime-failure/cleanup order. This is a reasoned reconciliation,
not an invented unanimous design verdict. All issued defect verdicts are NOT CLEAN.

STRAINED describes the failure plumbing, not betting, timing or settlement.
The runtime's initiating failures, cleanup failures and host failures travel
through separate channels. Their collection/receipt time is not necessarily
their occurrence time. Category-priority projection then discards chronology
that was already available. Both reproduced mechanisms point to this shared
weakness.

Recommend a bounded refactor: make an operation retain its initiating cause
before cleanup, append actual cleanup causes once, and transfer the ordered
sequence explicitly to the host. The host appends its own subsequent causes
and derives first/rest without type ranking. An immutable ordered batch or a
single owner can implement this; the exact representation is advisory.

Preserve sealed ledgers/spine, timing ownership, death guards, delivered
envelopes and records, successful fixture behavior and existing failure codes.
Transition risks are duplicate causes, wrong order across the runtime/host
boundary, synthetic errors from re-querying dead clocks, and accidentally
dropping a decision during failure transfer.

GREEN must cover real compound schedules, not only one fault on an otherwise
valid hand: rejected input then abort fault; clock then mismatch and the
reverse; write-only, write then publication/finalization fault and the reverse;
repeated actual codes without accidental deduplication; and complete record
preservation. Keep no-fault controls and real public producers/consumers.

A whole-host rewrite would unnecessarily disturb the working event, delivery
and timing paths. Another isolated catch or one-line split patch would leave
the cross-channel ordering problem. The bounded cause-flow replacement is the
proportionate intervention supported by the evidence.

### Contract-based residual history

R2-03 was the original host-failure contract. r003/R3-02 was its first residual;
r004 leaves the same contract open a second time. These are two mechanisms of
one contract, not two independent second-residual triggers.

The adopted workflow requires a written root-cause note explaining why the
r003 and r004 attempts missed before another fix is attempted, and a candidate
containing only this contract. r004 already supplies isolation; preserve it.
The note should address the difference between single-fault happy-path
enumeration and compound failure/cleanup paths, and the unsupported
reporting-priority interpretation. This review supplies diagnosis, not a claim
that the implementer's pre-fix note already exists.

The explicit handoff request for a design verdict is satisfied. The bounded
refactor recommendation also explains why we are not recommending wholesale
replacement after recurrence; it does not depend on adopting unrelated pending
workflow edits. New policy work and new value-admission work stay separate.
Claude retains finalization after the next candidate clears review and gates.

## Records and publication

Independent reports:
- reviews/review-01-codex-a.md — SHA-256 2e9bfcb423a07061b0bb929ed60743e4e545dd6a2fb7fb4836e11897946d2d9d
- reviews/review-02-codex-b.md — SHA-256 f71d6f9244f3e18b9ef483041d7b2d4341845fe1d5e03505285ad3962371f1f2

Coordinator's issued additional pass and later reconciliation:
- reviews/review-03-codex-coordinator.md
- reviews/review-04-codex-coordinator-addendum.md

Each issuer appends their own bound task-ledger verdict; this is the one program
disposition for the round. Reports remain immutable. The addendum explicitly
qualifies earlier engineering advice instead of silently rewriting it.

Actual CPython3.11.15 ran first, then3.14.6, using permanent executable slots,
fresh disposable snapshots, -B -P, snapshot cwd/src PYTHONPATH, scrubbed child
environments and absolute Git. Identity was recorded/asserted before payload
imports. Source snapshots stayed clean; implementation and existing concurrent
CLAUDE.md/workflow.md changes are untouched. No GPU, broad suite, installation,
experiment, source commit or performance/acceptance claim was made.

checks/.gitattributes preserves the exact bytes of newly issued raw console
captures and receipt JSON where Windows produced CRLF. Manifest and governance
markdown keep the repository LF convention. Publication verification checks
every newly staged r004 blob against its issued working bytes.
