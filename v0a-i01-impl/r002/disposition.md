# v0a-i01-impl/r002 disposition and next-round brief

Coordinator: Codex /root, 2026-08-30.
Finalizer: Claude, the first drafter for this implementation checkpoint.

**NOT CLEAN: ten consolidated Important findings. No integration authorized.**

Identity binding:

- candidate `18c965d1f3445c253a6333c4d10899c1dcac0cc6`;
- ref `refs/heads/review/v0a-i01-impl/r002`;
- manifest SHA-256 `4cfd14ac7bfdb22e052bb9f625610657c01aafa07182acf58d19367a8816cb18`;
- base `b357d333fc2393b7fc7dcf31f30c86616208c817`;
- tree `35f00349a7538cffc02f8e81f71913251be200be`.

The coordinator independently recomputed the ten frozen blob rows and their
whole-row-sorted LF manifest, including the manifest file's own SHA-256. Ref,
parent and tree agree. Both paths declared unchanged from r001 have empty
Git diffs. Review covers the declared Slice A fix round plus Slice B; absent
Slice C admission, boundary-policy and CI work is not a finding here.

## Outcome and evidence

All four existing focused suites pass independently on actual CPython 3.11.15
and 3.14.6: 36 hand replay, 25 trace, 20 replay host, 18 contract faults,
**99 per interpreter**. Disposable snapshots, asserted interpreter identity
before imports, exact snapshot PYTHONPATH, scrubbed environments and absolute
Git were used. Required NumPy comes from the unchanged package baseline;
CuPy/Torch were not imported. Git diff whitespace checks pass.

The new adversarial controls expose behavior outside those passing examples.
They are ordinary correctness diagnostics, not experiments or timing evidence.
The diagnostic processes' zero exits mean observations completed, not that
r002 passed. All candidate source and test bytes remain unchanged.

The two fresh cold reviewers did not receive the coordinator's or each other's
findings as inputs. Their independent reports are:

- [Cold reviewer A](reviews/review-01-codex-a.md);
- [Cold reviewer B](reviews/review-02-codex-b.md).

The additional, non-cold coordinator pass is
[host accounting and storage](reviews/review-03-codex-coordinator.md).
Each reviewer issues their own task-ledger line; this disposition combines
contracts rather than counting duplicated observations as separate bugs.

## Findings accepted for correction

### R2-01: The immutable blueprint authority is still substitutable

Origin: cold reviewer B's blueprint-binding probe; residual r001 F3.
Frozen locations: `runtime.py:168-175`, `:801-815`.

An ordinary delegate around a real empty immutable source returns the real
selection with `action=raise_to(6)` and `table_hit=True`. It retains the empty
source's canonical digest and correct decision key. The public runtime
constructor admits it and a real mailbox accepts the raise. The resulting
record claims a table hit under a policy with zero entries. Neither
monkeypatching nor malicious introspection is needed.

Accept as Important. Digest/key equality is necessary but does not establish
that the object answering is the bound immutable policy. The unchanged source
class is not being accused of mutation; the open callable boundary is the gap.

Required direction: accept the actual immutable policy authority at the
production boundary, not an arbitrary object that reports its digest. Bind it
once and preserve the unchanged action_for behavior. Keep fault injection
outside the production policy-input shape. Do not add a second full-table
rehash per decision to compensate for admitting an unrestricted delegate.
GREEN must reject the reproduced false-hit delegate before any action, while
real hit/miss/illegal-entry cases and hidden-card isolation still work.

### R2-02: An established outer violation is still lost on a later clock fault

Origin: cold reviewer B; residual r001 F7.
Frozen locations: `runtime.py:579-601`, `:888-911`.

A real outer finish_transition_boundary snapshot returns deadline_crossed=true
and no decision-work time remaining. The next clock sample fails. Interrupted
timing reports null cutoff and deadline flags even though the valid outer
snapshot already established them. The prior fixes preserve later checkpoints
but omit this earlier one.

Accept as Important. Capture established truths from every relevant valid
public outer snapshot before another fallible observation. Do not query a
failed clock to reconstruct them; retain null only for unknown facts. GREEN
must exercise this real transition path as well as the existing ready-to-emit
and post-acceptance interruption cases.

### R2-03: Host clock failures can escape, or become a successful receipt

Origin: both cold reviewers; new host integration defect, related to r001 F4.
Frozen locations: `runtime.py:228-302`; `replay.py:496-557`.

Independent schedules reproduce three host-level failures:

- An initial source failure becomes RuntimeError from publication without a
  started ledger, replacing the typed runtime outcome.
- A source failure immediately after real mailbox acceptance, or while closing
  terminal publication, escapes ReplayHost.run without its retained outcome.
- Failure at finalization is swallowed by finalize_accounting; the host uses
  pre-finalization totals and returns passed=true/accounting_complete=true
  while runtime.accounting().complete is false.

Accept as one Important host-lifecycle finding with multiple required RED
cases. Contain clock failures across bookkeeping, publication and finalization;
preserve the first cause, accepted actions and in-memory records; never retry
the failed witness. Derive host success only after all required closure steps.
An already written terminal row must not manufacture successful host completion
when publication or finalization measurement failed. An unmeasurable operation
must remain explicitly unmeasured, not repaired with invented zeros.

### R2-04: Non-response serialization and semantic work is not accounted

Origin: both cold reviewers and coordinator C-01.
Frozen locations: `replay.py:395-428`, `:496-507`.

The coordinator adds two seconds at each real decision serializer: eight
seconds disappear while complete preparation and post-terminal totals are
unchanged. Cold A independently adds one second to each real canonical JSON
operation: thirty pre-publication seconds disappear, with only the final
terminal serialization's extra second reflected in its separate receipt.
Cold B independently reproduces the omission with four decision seconds.

Accept as Important. Measure event/decision/failure serialization, required
row writes, semantic computation and other pre-cut host work through public
bookkeeping intervals. Charge each exactly once by terminal state at entry,
and form complete ordered totals through the declared cut. Keep this work
outside subsequent response walls. Preserve separate terminal publication
measurement and fail closed if any necessary interval cannot be closed.

### R2-05: There is no accepting independent legal replay verifier

Origin: both cold reviewers.
Frozen locations: `trace.py:590-749`, `:752-791`; `replay.py:496-557`.

The available reader accepts an illegal first CHECK (or raise-to=1), even when
both prefix and semantic digests have been recomputed to bind that illegal
trace. It also accepts a foreign header policy, a false delivered-action count,
a 16-second completed response claiming no deadline crossing, and null timing
on a successful decision. A mismatched semantic digest is returned rather than
rejected. The replay host reruns a fixture; it is not a checker of the supplied
trace's legal transitions and pinned input identities.

Accept as Important. A hashing helper cannot establish semantic correctness.
Provide an explicit accepting checker that validates the supplied trace against
its bound source/configuration/policy, replays legal transitions and selection,
checks state/card identities and settlement, and validates timing and terminal
consistency. Rebinding hashes must never legalize invalid semantics. Keep a
structural parser separate if useful, but do not expose structural parsing as
successful replay. Valid failed prefixes remain failures, even with valid
semantic digests.

### R2-06: The strict schema reader accepts invalid types and values

Origin: both cold reviewers.
Frozen locations: `trace.py:480-521`, `:590-749`.

Direct parser probes accept false as record index zero; unknown/missing event
keys (including an injected timestamp); invalid spine_reason; source_commit
as an array; seat 6; NaN response seconds; and Infinity in a terminal total.
These are structural defects independent of legal replay. JSON's permissive
number parsing and comparisons such as value < 0 do not reject NaN.

Accept as Important. Validate every variant's exact key set and every field's
exact type, allowed range/enum and finiteness, including nested events and
failures. Reject noncanonical/nonfinite input as required and ensure malformed
input yields typed trace refusal. Extend field-level negative coverage using
valid real traces and rebound digests, so a prefix mismatch does not mask the
rule under test. Keep this distinct from R2-05's behavioral verification.

### R2-07: The independent settlement comparison omits output fields

Origin: cold reviewer B.
Frozen location: `replay.py:467-494`.

The host compares payouts and pot amounts but ignores final_stacks and each
pot's eligible seats. Wrapping the real settlement output to change only all
six final stacks to zero, or only all pot seats to (0,), still yields a passing
host receipt and terminal. The real independent oracle remains unchanged.

Accept as Important. Compare the full settlement contract against independent
expectations: payouts, final stacks, pot amounts, eligibility and order, with
chip conservation. Preserve the default real oracle. The settlement_oracle
injection parameter is not itself rejected: substituting a wrong judge can
validly exercise the production comparison, provided the authority used in
any eventual sealed run is bound by that run's closure. Do not solve this
coverage gap by making the oracle call production settlement.

### R2-08: A known delivered late action is omitted from decision_count

Origin: cold reviewer B.
Frozen location: `replay.py:517-522`.

A real mailbox accepts one action and its acknowledgement is delayed sixteen
seconds. Runtime retains the decision with action_deadline_exceeded and the
host correctly fails the hand, but its terminal says decision_count=0 because
it counts only records whose failure_reason is null. Delivery happened;
response success is not the counting predicate.

Accept as Important. Count known accepted deliveries, including late and
interrupted delivered decisions, exactly once. Do not count ambiguous delivery
as proven acceptance or nondelivery. Reader checks must enforce equality with
the records and failure/delivery bindings rather than merely an upper bound.
GREEN must retain one decision and count one real accepted late delivery.

### R2-09: Required row writes are deferred until the whole hand finishes

Origin: coordinator C-02.
Frozen locations: `replay.py:395-428`, `:510-539`; `trace.py:325-342`.

With a real destination supplied, that file is absent after all four decision
serializations in fixture A. It appears only during final terminal publication.
No storage failure can therefore stop input at the first required post-delivery
write boundary. All later events and actions have already executed by then.

Accept as Important, separate from the missing measurement in R2-04. Implement
incremental publication of the required rows before dispatching the next event,
with create-new destination ownership and fail-closed write handling. Preserve
accepted actions and incomplete files without accepting them as successful
traces. The final terminal row and its publication interval remain separate.
A failure at the first post-delivery write must prevent a second action.

### R2-10: The writer's run-root check is not bound to file creation

Origin: coordinator C-03; related cold-A junction observation.
Frozen location: `trace.py:386-410`, specifically path validation at 391-402
and path-based creation at 403.

After real path validation but before os.open, a diagnostic renames the checked
parent and creates a Windows junction in its old name to a directory outside
the run root. The real writer opens and writes through that junction, then
returns a success digest. Both interpreters reproduce. All paths in the
reproduction are inside a unique disposable fixture area; no user data or
pre-existing file is overwritten.

Accept as Important. The stable directory authority checked must be the one
used to create the file. Refuse unsafe replacement/reparse paths before data
is written using a suitable directory-bound primitive or equivalent verified
protocol. O_EXCL alone binds only the leaf's nonexistence. Keep the fix limited
to this trace writer; no general governance transaction engine is requested.

## Prior-round status and scope decisions

The eighteen new regression tests are green on both interpreters, and the
original thirty-six Slice A tests remain green. This establishes those cases,
not blanket closure of all original contracts. In particular, r001 F3 and F7
still have demonstrated gaps (R2-01 and R2-02). Host-level clock integration adds
R2-03 beyond the runtime-focused F4 cases. Do not mark all F1-F7 closed solely
from the current regression count. No repeated-showdown settlement rewrite or
original missing-acknowledgement defect was reproduced in these controls.

Keep the controlled-seat guard: no new material finding was established against
it. Preserve sealed kernels and the legacy dependency baseline. The optional
oracle injection seam is acceptable as discussed above. Mode/run-identity
consistency remains a future owner-closure requirement; observed mismatches
should be recorded, but this round does not authorize or implement that owner.
Absence of measured write limits is a closure obligation, not permission to
invent numbers during this fix round.

The coordinator report's approximate source spans are clarified here without
editing the issued report: C-01's normal decision serializer is replay.py:410
(and feed:428); accounting cut/semantic computation is :496-507. C-02's builder
append methods are trace.py:325-342 and actual publication is replay.py:531.
C-03's validated-to-open gap is trace.py:391-403, not the narrower earlier
span. These are location corrections only; findings, scenarios and verdict
are unchanged.

## Recommended next handoff

Do not grow Slice C admission work into this correction candidate. Fix the
known contracts first, with deterministic RED against this immutable r002
before production edits and integrated GREEN afterward on both actual release
slots. Use the diagnostics as failure scenarios, not substitute helper-only
tests or a checklist to special-case.

Keep the next review explicitly sliced with source and contract tests together:

1. Runtime authority and host failure closure: R2-01, R2-02, R2-03, R2-07,
   R2-08. Real immutable policy, real mailbox acceptance, complete host receipts.
2. Trace acceptance: R2-05 and R2-06. Strict parsing plus an independent legal
   checker, with tampering controls that recompute both digests.
3. Trace publication and accounting: R2-04, R2-09, R2-10. Incremental writes,
   actual filesystem fault schedules, full pre-cut accounting, separate
   terminal publication and retained failure outcomes.

These are proposed correction slices, not new experiment authority. Any changed
bytes or scope must receive a fresh numbered frozen packet and manifest before
review. Apply the workflow's three-round circuit breaker if rounds cease to
converge; do not bypass it by relabeling the same unresolved work. No broad
suite, lifecycle launch or ceremonial implementation commit is earned by this
NOT CLEAN result. Claude retains finalization; controller authorization remains
specific to a future reviewed candidate.

## Retention and publication

Reports, diagnostic scripts and receipts live in this packet. The coordinator's
focused check receipts are `checks/codex-py311-verification.json` and
`checks/codex-py314-verification.json`; host/storage observations are the
corresponding `*-host-storage.txt` files. Cold-A's v2 probe receipts and Cold-B's
v3 diagnostic and blueprint-binding receipts carry the independent observations.
Earlier diagnostic script versions are retained for audit, not claimed as
additional successful coverage.

No source/test edits, evidence-repository commits, integration, source seal,
experiment owner execution or review-ref retirement were performed. The primary
checkout's existing `.tmp.driveupload/` remains untouched. r001 and r002 refs
remain immutable and local as declared by their handoffs; this publication does
not assert that those evidence-repository refs were pushed. Packet publication
uses the handoff repository's routine commit/push rule, not evidence ceremony.

## Attributed finding map (publication reconciliation)

| Consolidated contract | Independent / additional findings |
| --- | --- |
| R2-01 immutable policy authority | Cold B B3; residual r001 F3 |
| R2-02 established outer flags | Cold B B8; residual r001 F7 |
| R2-03 truthful host closure | Cold A A1; Cold B B1 and B2 |
| R2-04 complete serialization accounting | Cold A A2; Cold B B6; coordinator C-01 |
| R2-05 independent legal replay | Cold A A3; Cold B B4 |
| R2-06 strict schema validation | Cold A A4; Cold B B5 |
| R2-07 full settlement comparison | Cold B B7 |
| R2-08 count known deliveries | Cold B B9 |
| R2-09 incremental row publication | Coordinator C-02 |
| R2-10 stable writer root | Cold A A5; coordinator C-03 |

All material findings are accepted, with duplicates consolidated as above.
Cold A's unexecuted race inference is not represented as its executed result;
the coordinator independently executed the stronger out-of-root race on both
interpreters. Cold B's final v3 outer-ledger probe, not its earlier ambiguous
v2 probe, supports R2-02. Each reviewer subsequently appended their own verdict
under the serialized ledger slot; report prose written before that append does
not negate the actual ledger entry. No reviewer verdict was written by another
issuer. No additional user authorization or implementation action is implied.

Publication-state note: the final read-only audit observed a concurrent,
uncommitted primary-checkout change to CLAUDE.md documenting the permanent
3.11 tool slot at D:/Pontius-tools/py311 and floor-first CPU development. That
change is not part of this frozen candidate and was not made, staged, reverted
or integrated by this review. Existing receipts truthfully retain the actual
3.11.15 executable used earlier from the preregistration review tool environment;
no interpreter substitution or retroactive relabeling occurred. Future runs
should follow the newly documented permanent tool location. The audit receipt
records the primary's actual final status, including this unrelated change.
