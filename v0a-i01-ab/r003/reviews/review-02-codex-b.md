# Cold review B - v0a-i01-ab/r003

Reviewer: Codex /root/ab_r003_cold_b, 2026-08-30.
Tier C FIX, independent narrow direct-context typed-refusal review.

**Defect verdict: CLEAN. No required correction remains in this scope.**
**Specification verdict: PASS. Engineering-quality verdict: PASS.**
**Design verdict: SOUND.** Comparing the supplied exact decision against the
finite kernel-derived schema before selection fits the contract and closes
the demonstrated cause. Owned policy admission and unchanged sealed lookup
remain appropriate; no redesign or operational depth budget is needed.

## Identity and independence

Candidate: `30df7bce8da51715e6f1d7576892dd689421c516`.
Ref: `refs/heads/review/v0a-i01-ab/r003`.
Parent: `2f4287f68a83fac4225a05a91daffdb3f2977a43`.
Tree: `fbf234bfffcdb51113b3b137a36afa3460bc94b5`.
Manifest: `21d9686c9918d9d0648fd98edf35219dfb5e0b4dc1dcfe5e4f28171b7d94e513`.

I independently recomputed both stored-blob hashes and the whole-row-sorted,
LF-only manifest, verified its exact file bytes, and verified ref/parent/tree.
Only runtime.py and test_v0a_hand_replay.py differ from the parent: 43 added
and 6 removed lines. Changed blobs have no BOM, CR, trailing whitespace or
lines over 100 columns; git diff --check passes. Sealed immutable_blueprint.py,
no_limit_betting.py and replay.py are byte-identical to the parent.

The [initial inventory](../checks/cold-b-initial-inventory.md) was recorded
before coverage.md was opened. Its SHA-256 is
`085271f5c87da2ab7d4538f382d8f21bb7549400d8a4813606d5cc79ea0433d7`.
Coverage independently hashes to the declared
`369dcc88458e71b4d2ef5b5407c1bf2b2728f8e1779f35c0053d234e95f6104c`.

Inputs were the frozen source/tests, ADR-0485/0484 brief requirements, current
CLAUDE/workflow, r002 disposition and predecessor review. Transparency: the
predecessor review read returned its entire text, including prior-round
material beyond B-01. This was disclosed to the coordinator before proceeding.
No implementer transcript, plan, self-report or r003 peer review/inventory was
read. No referenced implementer receipt was read. The deferred coverage claim
was compared with independent inventory and execution, not treated as evidence.

## Required findings

None. The r002 B-01 public-helper refusal outcome is closed by fresh evidence
on both supported interpreters. This verdict is limited to the r003 FIX scope.

## Requirement-to-evidence results

| Required behavior / risk | Independent evidence | Result |
| --- | --- | --- |
| Exact malformed decision and RaiseBounds fields refuse before lookup | 422 generated public-helper cases per interpreter, all with exact InvalidDecisionContextError, zero sealed lookups and zero caller hooks | Pass |
| Caller depth must not dictate validation traversal | 78 depth-2000 cases across every field and same-width action_kinds members; source inspection of runtime.py:151-158 | Pass |
| Same-type semantic disagreement and exact-type aliases refuse | Different integer/enum/bounds values; bool/float aliases; list/map/tuple shape; nested int/tuple/bounds subtypes | Pass |
| Valid contexts remain valid | Raise-enabled, raise-disabled, short all-in-only, nonempty-history and check contexts | Pass |
| Honest outcome split and owned authority remain | Five controls per state: hit, miss, unrelated-key miss, illegal match and source-subtype refusal; real sealed lookup observed without replacing it | Pass |
| Four-input public surface and sealed kernel remain unchanged | Signature assertion, stored-blob comparison and existing runtime checks | Pass |
| Focused integration on actual Python floor then development slot | 40 hand, 22 contract-fault, 45 replay and 25 trace tests on each interpreter | Pass |

The [independent probe](../checks/cold-b-probe-v2.py) invokes the real public
select_blueprint_action with ordinarily constructed dataclasses and replace().
It neither edits production classes nor substitutes the selected function.
A profiler observes real action_for entry and input identities. All malformed
cases terminate before that function is entered. Every valid or illegal-match
lookup uses a source, cards, betting state and decision distinct from caller
objects; the expected hit/miss action, typed illegal-entry error and canonical
source identity are retained. Hook-bearing subtypes invoke no caller hook.
No private mutation, constructor bypass or recursion-limit change was used.

The identical probe against a separate fresh predecessor snapshot yields
**78 RecursionError failures per interpreter**, all depth cases, and all
25 controls pass. The candidate yields **422/422 malformed refusals and
25/25 controls**. Thus the diagnostic distinguishes the original defect;
its predecessor exits are deliberately RED, not successful candidate evidence.

The candidate's added field walk covers all nine LegalBettingDecision fields
in raising and nonraising states, and all five present RaiseBounds fields.
My independent inventory additionally challenged nested same-width action
members, exact aliases, short all-in-only states and valid outcome controls.
No missed required member was demonstrated. RecursionError normalization in
source admission is defensive containment; an ordinary source-admission
recursion defect was not independently established or fabricated.

## Execution and receipts

Fresh candidate clone outside the packet:
`D:\pontius-snapshots\v0a-i01-ab-r003-cold-b-20260830`.
Fresh predecessor clone:
`D:\pontius-snapshots\v0a-i01-ab-r003-cold-b-base-20260830`.
Both were cloned locally with --no-hardlinks --no-checkout and checked out
at their exact detached commits. No source overlay or source edit occurred.

Execution used actual CPython **3.11.15** at
`D:\Pontius-tools\py311\Scripts\python.exe` first, then actual **3.14.6** at
`D:\Pontius\.venv\Scripts\python.exe`. The retained runner launches each
payload with -B -P, snapshot cwd, exact snapshot/src PYTHONPATH, no PATH,
a scrubbed environment and absolute `C:\Program Files\Git\cmd\git.exe`.
Every payload asserts version, flags, commit and runtime module origin before
execution. Candidate runs report no CuPy/Torch import. Both snapshots remain
clean under the same user that created and executed them.

- Candidate category receipts: [3.11](../checks/cold-b-311-probe-v2.json),
  [3.14](../checks/cold-b-314-probe-v2.json), exit 0 each.
- Predecessor receipts: [3.11](../checks/cold-b-311-baseline-probe-v2.json),
  [3.14](../checks/cold-b-314-baseline-probe-v2.json), exit 1 each, the expected
  78 product failures and no control failure.
- Identity receipts: [3.11](../checks/cold-b-311-identity-v2.json),
  [3.14](../checks/cold-b-314-identity-v2.json), exit 0 each.
- Focused receipts are `cold-b-{311,314}-suite-test_v0a_{hand_replay,
  contract_faults,replay,trace}.json`: all eight exit 0, **132 tests per slot**.
- [Final integrity receipt](../checks/cold-b-final-integrity.json) and
  [artifact hashes](../checks/cold-b-artifact-hashes.sha256) bind the retained
  inventory, diagnostic sources, runners and receipts. No test timing is an
  operating-budget measurement.

The first identity diagnostic expected a local branch ref in the clone;
Git correctly stored that cloned branch under refs/remotes/origin. Its
nonzero receipt is retained. Version 2 corrects only that diagnostic ref
spelling and verifies the original source ref separately. This was a harness
error, not a product defect. A later read-only git-status attempt from the
sandbox account encountered Git's ownership guard; the final cleanliness
check ran as the original snapshot owner. No safe.directory setting changed.

## Separate advisory guidance and limits

Optional test maintenance: retain same-width nested action_kinds and short
all-in-only controls in the permanent field-category suite if that suite is
extended later. They protect useful schema partitions already passing in this
independent probe; this is not a required correction or a new gate.

No exhaustive hostile-Python/resource-exhaustion claim is made. No broad
suite, GPU/dependency run, lifecycle invocation, source seal, operating-bound
measurement, value/trace/publication correction, Slice C acceptance, evidence
commit, integration or ref retirement occurred. Passing this narrow FIX does
not establish full A/B acceptance or authorize a ceremonial commit.

This report is issued append-only. Its author will append exactly one task
ledger verdict after the coordinator grants the serialized append slot.
