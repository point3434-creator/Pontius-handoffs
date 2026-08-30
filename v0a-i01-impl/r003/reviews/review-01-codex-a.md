# Cold Tier-C review: v0a-i01-impl/r003, pass A

Verdict: NOT CLEAN. Two Important findings survive direct verification.
Specification: FAIL. Engineering correctness within slice 1: FAIL.
Reviewer: Codex cold-a. Date: 2026-08-30. Finalizer: Claude.

## Candidate binding and scope

- Ref: refs/heads/review/v0a-i01-impl/r003
- Commit: 47d08d8c1556d776358e15811e3e98b859fd6a8b
- Base: b357d333fc2393b7fc7dcf31f30c86616208c817
- Tree: 35a6667ca3785e750324b3c93103a8994a6d7d6a
- Manifest SHA-256:
  cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a

This is a FIX-round review of slice 1 only: R2-01, R2-02, R2-03, R2-07,
and R2-08. All source locations below refer to this commit, including unchanged
sealed dependencies. The current uncommitted CLAUDE.md and docs/workflow.md
amendments govern review mechanics and residual tracking. Frozen ADR-0485,
docs/briefs/v0a-increment-1-brief.md, and the packet's explicit contracts govern
behavior. No implementation transcript, self-report, previous review,
disposition, or other reviewer's findings was read.

Both findings below are residuals against contracts named in this FIX handoff.
Historical attempt counts and any repeat-residual consequence belong to the
coordinator; this cold review did not inspect that history.

## A-01 - Important: policy subclasses can still falsify the bound table identity

Confidence: high; reproduced through the real HandRuntime and ActionMailbox on
CPython 3.11.15 and 3.14.6. Contract: R2-01 policy authority.

Frozen locations:

- src/pontius/v0a/runtime.py:178 admits subclasses through isinstance.
- src/pontius/v0a/runtime.py:94 pins action_for but retains its virtual reads.
- src/pontius/v0a/runtime.py:462 binds the policy's overridable digest property.
- src/pontius/v0a/runtime.py:867 compares two values reported by that same policy.
- src/pontius/immutable_blueprint.py:345 dispatches to self.canonical_bytes().
- src/pontius/immutable_blueprint.py:374 returns self.digest from sealed lookup.

ADR-0485:170 requires binding the immutable blueprint by its canonical digest.
The handoff explicitly admits a lying subclass only on the premise that its
substitution cannot defeat sealed policy authority. Calling the base
implementation of action_for does not pin the digest or canonical_bytes calls
made from that implementation.

Concrete reproduction, retained in checks/cold-a-diagnostics.py:88-125:

1. Construct the normal initial six-seat state: button 0, controlled seat 3,
   stacks (200,)*6, blinds 1/2, private cards (0,13).
2. Construct an honest empty ImmutableBlueprintActionSource with source_id
   cold-a-bound-empty. Its legal answer in that state is the passive call.
3. Normally construct a subclass with that same source_id and one real
   BlueprintActionEntry for raise_to(6) at the exact current key. Override
   only its digest property to return the honest empty source's digest.
4. Dispatch a real HandStartedEvent through HandRuntime into a real mailbox.
   Admission succeeds, the runtime returns decided/table_hit/raise-to-6, and
   the real mailbox accepts once. No typed failure is returned.
5. Repeat with only canonical_bytes overridden to return the empty source's
   canonical bytes. The same substitution succeeds.

The honest empty policy and both substituted sources are recorded as:

    07237ffb917edaaabb67942ed451d262a41a33179bfa4a84e0ebe0e12e253364

The actual table bytes produced by the sealed canonical implementation for
both raise-entry sources hash to:

    24b7fc5d3f251adc62bc1439d0283b7b8e0eb66919a21c3c2bf6d13eb066709e

Thus a real emitted raise is attributed to a different immutable table whose
answer is call. This probe uses ordinary subclass construction and public
method overrides: no private mutation, malicious introspection, patched
production method, counterfeit selection, or replacement mailbox is involved.
The existing subclass regression tests only override action_for, so they do
not cover the surviving virtual identity hooks.

Smallest correction: establish trusted policy values at admission and selection,
including canonical identity, instead of accepting arbitrary subclass behavior.
At minimum reject these subclasses at both public boundaries. If subclass inputs
must remain supported, normalize their admitted data into an exact validated
immutable source and bind/use that source consistently. Do not change sealed
immutable_blueprint.py. Add a focused regression for both identity-hook variants
in a subsequent authorized fix candidate.

## A-02 - Important: host clock failure closure discards the typed cause

Confidence: high; reproduced on both required interpreters. Contract: R2-03
host failure closure, specifically the frozen completion receipt contract.

Frozen locations:

- src/pontius/v0a/runtime.py:288 and :298 discard bookkeeping clock exceptions.
- src/pontius/v0a/runtime.py:321 and :331 discard publication clock exceptions.
- src/pontius/v0a/runtime.py:364 discards finalization clock exceptions.
- src/pontius/v0a/replay.py:571-585 builds the final receipt without those causes.

ADR-0485:265-284 requires the host completion receipt to retain the primary typed
cause and to preserve later typed failures in secondary_failures. These catch
blocks only mark the ledger dead and accounting incomplete; the clock_invalid
or clock_reversed cause never reaches either receipt field.

Concrete real-host reproduction in checks/cold-a-host-causes.py:

Run FIXTURE_A with the ordinary empty immutable source and an exact integer
clock returning 1000, 2000, ... nanoseconds. Make exactly one scheduled source
read either raise ValueError or return zero, thereby producing clock_invalid
or clock_reversed through the actual MonotonicWitness. No host/runtime/ledger
method is replaced. The following five stages each reproduce the loss:

| Read | Real operation at failure | Runtime location |
| --- | --- | --- |
| 134 | Settlement bookkeeping start | runtime.py:287 |
| 135 | Settlement bookkeeping stop | runtime.py:297 |
| 136 | Terminal publication start | runtime.py:320 |
| 137 | Terminal publication stop | runtime.py:330 |
| 138 | Outer finalization | runtime.py:363 |

Every result has passed=false and accounting_complete=false, but also
failure_reason=null, secondary_failures=(), and zero FailureRecord objects.
The source is not retried. The complete fault sweep independently reproduces
this absence at reads 68-72 of FIXTURE_B as well. This loses the first cause
on an otherwise valid hand and makes invalid and reversed clocks
indistinguishable to the required host reporting channel.

The new guards do close the original escape/success paths for these schedules;
the surviving finding concerns the typed failure outcome, not aggregate compute
duration accuracy or trace publication mechanics. It therefore remains inside
R2-03 and does not reopen deferred R2-04/R2-09 accounting work.

Smallest correction: retain typed clock failures at the runtime accounting seams
and expose them to ReplayHost. Merge them in occurrence order into the host's
primary/secondary failure state before returning the receipt, without replacing
an earlier primary cause and without reading a failed clock again. Verify the
real host at all five stages for clock_invalid and clock_reversed.

## Requirement-to-evidence summary

| Contract | Evidence | Result |
| --- | --- | --- |
| R2-01 immutable authority | Real subclass/table/digest probes | FAIL, A-01 |
| R2-02 established outer flags | 156 jump-then-fault schedules per interpreter | No finding |
| R2-03 host failure closure | Every read of both fixtures; ten cause probes | FAIL, A-02 |
| R2-07 full settlement | Full tuple comparison and existing real-host oracles | No finding |
| R2-08 known delivery count | Ack counter plus late real-mailbox host regression | No finding |

For R2-02, the diagnostic observes the real inherited outer-ledger methods'
returned snapshots; it does not substitute their timing or computations. Every
established boundary/ready cutoff and deadline remains true through subsequent
interruption. It covers both 14-second-plus-1ns and 16-second delays across the
single-decision read schedule. No closing emission snapshot is misclassified as
decision work. The existing boundary and post-delivery tests were also inspected.

For R2-03, all 138 baseline clock positions of FIXTURE_A and all 72 of FIXTURE_B
were faulted independently on each interpreter. All returned unsuccessful,
incompletely accounted receipts without an escaping ordinary clock exception
or a subsequent source read. This supports closure, but does not erase A-02.

For R2-07, replay.py:514-520 compares payouts, final stacks, contribution-depth
ordered pots including eligible seats, and chip conservation. The existing
real-host test at tests/test_v0a_replay.py:195 independently changes only final
stacks or pot seats and requires settlement_mismatch. For R2-08,
runtime.py:902-913 increments only after a matching acknowledgement;
replay.py:553 uses that count. The real-mailbox late-ack regression at
tests/test_v0a_replay.py:442 verifies terminal decision_count=1 despite failure.

## Execution and identity receipts

Exclusive disposable source snapshot used for all cold-a payload execution:

    D:/pontius-snapshots/v0a-i01-r003-59e5f7bbb8d7441d9d3f501900991e54/harness

Each diagnostic ran on the floor first, then 3.14, using these argument shapes:

    <absolute-python> -B -P <packet>/checks/cold-a-diagnostics.py <snapshot> <slot>
    <absolute-python> -B -P <packet>/checks/cold-a-host-causes.py <snapshot> <slot>

Slots were 311 then 314, with exact executables:

- D:/Pontius-tools/py311/Scripts/python.exe, CPython 3.11.15
- D:/Pontius/.venv/Scripts/python.exe, CPython 3.14.6

Before any pontius import, each process recorded and asserted exact executable,
CPython implementation, full sys.version string, cwd, -B/-P flags, PYTHONPATH,
and absolute PONTIUS_GIT. The cleared child environment contained only SYSTEMROOT,
WINDIR, TEMP, TMP, PYTHONPATH=<snapshot>/src, and
PONTIUS_GIT=C:/Program Files/Git/cmd/git.exe. No PATH lookup was available.
Runtime import provenance was asserted under this snapshot. All four diagnostic
processes exited 0, meaning their stated assertions reproduced/verified as
expected; it does not mean the candidate passed review.

Create-only receipts:

- checks/cold-a-py311-diagnostics.jsonl
- checks/cold-a-py314-diagnostics.jsonl
- checks/cold-a-py311-host-causes.txt
- checks/cold-a-py314-host-causes.txt

The coordinator's fresh objective receipts were read, not any implementer
self-report: checks/codex-py311-verification.json and
checks/codex-py314-verification.json. They record all four focused suites GREEN,
107 tests per interpreter; replay test log tails also independently show 25/25
with exit 0. These green suites do not cover the two surviving scenarios fully.

Manifest identity was independently recomputed from the frozen commit's blobs,
with rename detection disabled and ten complete row byte strings sorted
lexicographically. The computed bytes exactly equal manifest.sha256 and hash to
the bound digest above. Snapshot HEAD and parent were asserted, and git status
was pristine before and after each diagnostic. No candidate byte was changed.

## Limits and exclusions

No trace parsing/acceptance, publication-storage, aggregate accounting, boundary
admission, CI, or other deferred slice is adjudicated here. No broad suite,
experiment owner, GPU, source/test/configuration edit, commit, push, or candidate
mutation was performed. Diagnostic scripts and receipts were created only under
r003/checks/cold-a-*. This report is create-only and LF-only. The issuer will
append exactly one bound verdict line when given the exclusive task-ledger slot.
