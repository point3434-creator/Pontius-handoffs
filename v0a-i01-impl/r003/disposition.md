# v0a-i01-impl/r003 disposition

Coordinator: Codex /root, 2026-08-30.
Finalizer: Claude, the first drafter for this implementation checkpoint.

**NOT CLEAN: two Important residual contracts. Three scoped fixes close.
No integration or broad-suite advancement from this candidate.**

## Frozen identity and review scope

- Ref: refs/heads/review/v0a-i01-impl/r003
- Candidate: 47d08d8c1556d776358e15811e3e98b859fd6a8b
- Manifest SHA-256:
  cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a
- Base: b357d333fc2393b7fc7dcf31f30c86616208c817
- Tree: 35a6667ca3785e750324b3c93103a8994a6d7d6a

Ref, parent, tree, all ten frozen blobs and the byte-exact manifest verify.
This is the declared FIX round, slice 1: R2-01, R2-02, R2-03, R2-07 and
R2-08. The five other r002 contracts remain deferred, not rediscovered here.

The current primary CLAUDE.md and docs/workflow.md amendments govern process,
including permanent Python 3.11 tooling and contract-based residual counts.
Frozen ADR-0485, the brief and the handoff govern behavior. No current source
file or chat transcript substitutes for this frozen pair.

There is one nonblocking packet typo: the handoff's heading says four paths
changed and six unchanged from r002. Git and its own table show five changed
and five unchanged. The correct manifest and actual scope are unambiguous;
the issued handoff is preserved without rewriting it.

## Contract disposition

| Contract | Outcome | Residual history |
| --- | --- | --- |
| R2-01 policy authority | OPEN: subclass identity remains substitutable | Second residual |
| R2-02 established outer flags | CLOSED in this slice | Prior residual closed |
| R2-03 host failure closure | OPEN: typed cause and ordering are lost | First residual |
| R2-07 complete settlement comparison | CLOSED in this slice | First fix closes |
| R2-08 acknowledged delivery count | CLOSED in this slice | First fix closes |

CLOSED records review of these contracts on this candidate, not approval to
integrate the whole candidate or permission to drop regression coverage.

## R3-01: Policy identity remains substitutable

Maps to R2-01 and original r001 F3. Important; high confidence.
Attribution: cold A A-01 and cold B B1, independently reproduced.

Frozen locations: runtime.py:178, :94, :462 and :867; unchanged
immutable_blueprint.py:345 and :374 show the remaining virtual identity reads.

The constructor accepts subclasses through isinstance. Calling the base
action_for implementation blocks its direct override, but that method still
reads self.digest, which can call an overridden canonical_bytes method.

Both cold reviewers normally constructed a source with a real legal raise
entry, overriding only canonical identity to report an honest empty table.
A real HandRuntime and ActionMailbox then emitted/accepted the raise,
recording table_hit under the empty policy's digest. Cold A also reproduced
the same result by overriding only the digest property. This needs no private
mutation, monkeypatching, introspection or forged selection.

The failure is authority, not hash width or a mutated sealed table. The
ordinary accepted object's identity hooks still control what the runtime
believes it bound.

Required correction direction: close the entire policy admission/selection
boundary, including identity dependencies. Exact sealed-type admission at
both public boundaries is the smallest option. If subclass support is truly
required, normalize into an exact validated immutable source and use that
source consistently. Preserve the sealed dependency and avoid adding a
second full-table rehash per action.

GREEN must reject both digest and canonical_bytes substitutions before any
action while preserving real hit/miss/illegal-entry behavior and the earlier
delegate/action_for-override protections.

### Required next-step isolation

The history is one contract: r001 F3, residual R2-01 in r002, and residual
R2-01 again in r003. Under current docs/workflow.md:177-181, this is the
second residual. Before another fix, give this contract its own candidate
and a written root-cause note explaining why the r002 and r003 attempts
missed. The note must address the complete trusted-data/identity boundary,
not only the newest override example.

This is the current contract-based rule, not the superseded round counter.
It applies to policy authority; it does not halt unrelated closed contracts
or merge the already declared correction slices.

## R3-02: Host closure loses the first and later typed clock causes

Maps to R2-03. Important; high confidence. Attribution: cold A A-02,
cold B B2 and coordinator C-01.

Frozen locations: runtime.py:288, :298, :321, :331 and :364 discard caught
clock exceptions; replay.py:571-585 builds the receipt without those causes.

A single invalid or reversed clock observation at bookkeeping entry/exit,
publication entry/exit or finalization returns an unsuccessful, incompletely
accounted receipt with failure_reason=null and secondary_failures=().
The current guards correctly prevent exception escape and false success;
the typed reporting contract remains incomplete.

Cold B additionally reproduced both orderings against the admitted oracle
seam. A bookkeeping clock fault followed by a settlement mismatch reports
the later mismatch as primary, losing the earlier clock_invalid. A mismatch
followed by a publication clock fault preserves the mismatch but drops the
later clock code from secondary_failures.

ADR-0485:269-280 explicitly requires primary cause retention and ordered later
typed failures. This is within R2-03 host closure. Deferred R2-04 concerns
duration accounting, and R2-09 concerns publication progression; neither
defers the host's truthful failure cause.

Required correction direction: retain typed runtime closure failures and
communicate them to the host at each boundary in occurrence order. Preserve
the first cause, append subsequent typed causes, keep dead-clock/no-success
guards and never sample a failed witness again. A final generic fallback
code alone cannot reconstruct the demonstrated ordering.

GREEN must cover invalid and reversed clocks at all five seams; assert
primary and secondary fields, not merely passed=false. Include clock before
another failure and clock after an existing failure, accepted-action
retention, and no further source read. This is R2-03's first residual; it
does not independently trigger the repeated-residual isolation rule.

## Verified progress and evidence

Fresh focused suites pass on actual CPython 3.11.15 first and 3.14.6 second:
35 hand replay, 25 trace, 25 replay host and 22 contract faults,
**107 tests per interpreter**. Versions and executable paths were asserted
before payload imports; runs used disposable clones, -B -P, snapshot cwd,
exact snapshot PYTHONPATH, scrubbed environments and absolute Git.
All candidate source/test bytes remain unchanged.

Two cold reviewers independently verified the frozen manifest and ran their
own bounded probes. They received no other reviewer's findings as inputs.
The coordinator clarified one scope question using the primary ADR's typed
receipt requirement after cold A had already observed cause loss; no
reproduction or other reviewer's finding was supplied.

- [Cold A](reviews/review-01-codex-a.md): both identity-hook variants,
  156 established-flag schedules per interpreter, every observation in
  both fixtures and typed-cause stage probes.
- [Cold B](reviews/review-02-codex-b.md): canonical identity substitution,
  every observation in Fixture A, both cause orderings, conserving
  final-stack and eligibility-only mismatches, and real late delivery.
- [Coordinator, additional non-cold pass](reviews/review-03-codex-coordinator.md):
  628 clock-fault schedules per interpreter across both fixtures,
  successful baselines and two real settlement-output corruption controls.

The coordinator's 1,256 fault schedules show no ordinary exception escape,
false success or lost accepted-decision record. Thirty cases per interpreter
lose the typed cause. Probe exits of zero mean the stated observations were
reproduced; they are not passing candidate verdicts or measured timing evidence.

R2-02 retains established boundary/ready truth across interruption.
R2-07 rejects final-stack-only and pot-eligibility-only differences, including
a stack difference that preserves total chips. R2-08 correctly counts a real
mailbox acceptance even when the sixteen-second acknowledgement fails the
action wall. These fixes are retained as reviewed progress.

## Remaining board and authority

Keep the three planned correction slices separate. Deferred and unchanged:
R2-05/06 trace acceptance; R2-04/09/10 publication and accounting. Slice C
admission, boundary policy and CI remain out of scope. No further product,
research, GPU or architecture requirement is introduced by this review.

Claude retains finalization. Next implementation bytes require a new frozen
ref/manifest pair and review; this report does not authorize source changes,
a ceremonial evidence commit, integration or review-ref retirement. The
existing candidate refs and reports remain immutable.

Only this packet's reviews, diagnostic artifacts, ledgers and navigation are
published through the routine handoff-repository commit/push workflow.
The primary checkout's existing CLAUDE.md/workflow.md edits and user files
are left untouched. Reviewer verdicts are issued by their owners in the
task ledger; this disposition appears once in the program ledger.
