# Cold review A - v0a-i01-ab/r003

Reviewer: Codex /root/ab_r003_cold_a, 2026-08-30.
Tier C, independent narrow typed-refusal FIX review. No source changes.

**Defect verdict: CLEAN. Required corrections: none.**
**Specification verdict: PASS within the declared r003 scope.**
**Engineering-quality verdict: PASS; design verdict: SOUND.**

The correction closes r002 B-01 at the public helper. A malformed exact decision
is compared against the kernel-derived decision before its caller-chosen graph
can be copied. Exact type checks precede equality or descent, and the admitted
selector passes the derived decision to the unchanged sealed lookup. This is a
small correction at the appropriate boundary, not a new policy algorithm or an
arbitrary operational depth budget. No material defect or blocking coverage gap
was found in this round's scope.

## Frozen identity and cold-input discipline

- Ref: `refs/heads/review/v0a-i01-ab/r003`.
- Commit: `30df7bce8da51715e6f1d7576892dd689421c516`.
- Base: `2f4287f68a83fac4225a05a91daffdb3f2977a43`.
- Tree: `fbf234bfffcdb51113b3b137a36afa3460bc94b5`.
- Manifest SHA-256:
  `21d9686c9918d9d0648fd98edf35219dfb5e0b4dc1dcfe5e4f28171b7d94e513`.

Ref, parent, tree, both stored blob hashes, whole-row manifest ordering, row-file
bytes and manifest digest independently verify. Only `src/pontius/v0a/runtime.py`
and `tests/test_v0a_hand_replay.py` differ from the parent. Both blobs are LF-only,
BOM-free, at most 100 columns, and pass `git diff --check`. Snapshot checkout
bytes equal those blobs. The sealed betting/card/blueprint kernels are unchanged.
See [identity receipt](../checks/cold-a-identity.json).

The [initial independent inventory](../checks/cold-a-initial-inventory.md), SHA-256
`c7502d1e6d39f0368793a5824331a2a69f68c00f4b45d44e3915603420c2d23b`, was written
before opening deferred coverage. Coverage independently hashes to
`369dcc88458e71b4d2ef5b5407c1bf2b2728f8e1779f35c0053d234e95f6104c`.
I compared it as a claim; I did not open the implementer's linked receipts.

Permitted inputs were the handoff/candidate/manifest, frozen source/tests,
ADR-0485/ADR-0484 and their brief, current CLAUDE.md/workflow checklist, and
r002's required disposition/B-01. Transparency: while retrieving B-01 I opened
its named predecessor report in full, also exposing its prior closure/advice
sections. I informed the coordinator, who expressly allowed continuation because
this was the authorized predecessor report. No implementer transcript, plan,
self-report or other r003 review/inventory was read. Current-round source and
execution evidence were independently assessed.

## Required behavioral outcomes and fresh evidence

| Required outcome / risk | Evidence | Result |
| --- | --- | --- |
| Malformed exact decisions and RaiseBounds fail typed before selection | 441 independently generated public-helper cases per interpreter; exact exception type, zero actual lookup entries | Pass |
| Refusal depends on legal shape rather than caller nesting depth | Depth-2500 tuple in all decision/bounds fields, same-width action-kind tuple containing deep child, shallow wrong shapes | Pass |
| Exactness does not invoke caller hooks | int/tuple/string subtypes, decision/bounds subtypes, class-property pretender; equality/iteration/attribute counters | Pass: zero hooks |
| Honest legal hit and passive miss remain available | Five contexts: ordinary raise, no-raise call, short all-in-only raise, nonempty history, check | Pass |
| Illegal matching entry retains its own typed outcome | Direct helper with illegal raise; real runtime outcome regression suite | Pass |
| Owned policy and visible context remain lookup authority | Public helper profile observes actual sealed action_for call, independently checks copied source/cards/betting/decision and source digest | Pass |
| Runtime/host admissions and mailbox outcomes are preserved | Existing hand, contract-fault and replay suites through real public paths | Pass |
| Four-input surface and sealed lookup remain unchanged | Signature assertions, frozen diff and existing regression tests | Pass |
| Genuine supported interpreters with isolated execution | Actual CPython 3.11.15 first, then 3.14.6; asserted environment and module origins | Pass |

The diagnostic uses ordinary constructors and `dataclasses.replace`, with no
source edits, monkeypatched production methods, private writes, recursion-limit
changes, helper doubles, or malformed-value rendering. Its 441 cases cover every
one of the nine LegalBettingDecision fields and all five RaiseBounds fields
across the five contexts. Variants include foreign objects, enum/string aliases,
float/int and bool/int aliases, wrong exact values, optional-bound mismatches,
container subclasses, wrong container kinds, and malformed nested tuple members.
Each refusal is checked before `ImmutableBlueprintActionSource.action_for` is
entered. Profiling observes the real function; it does not replace that function.

The five positive controls separately exercise an independently copied but equal
legal decision, legal hit and passive miss. Each miss reaches a lookup receiver
that is an exact owned source, not the caller source, with copied card and betting
records and a different decision object. Returned policy digests match the honest
sources. Existing public runtime/host regression tests supplement these helper
checks; no helper double is offered as proof of runtime ownership or delivery.

Source: [independent context probe](../checks/cold-a-context-probe.py).
Results: [3.11 probe](../checks/cold-a-31115-probe.json) and
[3.14 probe](../checks/cold-a-3146-probe.json).

## Predecessor sensitivity and coverage assessment

A second fresh disposable clone at the r002 base independently reproduces all
23 deep malformed decision/bounds schedules on actual CPython 3.11.15. Each yields
`RecursionError`; the corresponding public cases against r003 yield exactly
`InvalidDecisionContextError`. The baseline diagnostic exits zero only because
it confirms those expected historical failures; it is not a passing predecessor
verdict. See [baseline probe](../checks/cold-a-baseline-probe.py) and
[baseline receipt](../checks/cold-a-baseline-31115.json).

The frozen new test executes all nine fields with raises enabled and disabled,
and all five bounds fields when present. It supplies valid-context controls and
runs as part of the 40-test hand suite. The independent probe adds shape members
not supplied by that single deep-field loop, including same-width nested
`action_kinds`, exact numeric aliases, hook-bearing subtypes and all-in/check
contexts. No counterexample to the bounded refusal claim was found.

The source-admission `RecursionError` normalization is defensive containment.
Like the coverage claim, this review does not claim an independently reproduced
ordinary source-admission recursion defect. Nor does it establish unbounded
resource safety for tables or histories. The demonstrated B-01 correction is
schema-directed and does not impose a numeric depth ceiling on valid inputs.

## Execution and retained diagnostics

Candidate snapshot:
`D:\pontius-snapshots\v0a-i01-ab-r003-cold-a-20260830`.
Baseline snapshot:
`D:\pontius-snapshots\v0a-i01-ab-r003-cold-a-base-20260830`.
Both are fresh detached D-local clones outside the packet and finish clean.

Each payload verifies CPython implementation/full version before application
imports, `-B -P`, snapshot cwd, exact snapshot/src PYTHONPATH, scrubbed environment,
and snapshot runtime-module origin. Git is bound to the absolute regular executable
`C:\Program Files\Git\cmd\git.exe`; no PATH resolution or global Git safety change.
No CuPy/Torch import was observed in the independent probes.

Each interpreter passed **132 focused tests**: 40 hand replay, 22 contract faults,
45 replay host and 25 trace. Each then passed the **441-case independent probe**.
Commands, environments, stdout/stderr and exits are retained in
[3.11 focused](../checks/cold-a-31115-focused.json),
[3.14 focused](../checks/cold-a-3146-focused.json), and the probe receipts above.
The runner is [cold-a-runner-v2.py](../checks/cold-a-runner-v2.py).

The first runner attempt failed before product payload import because it looked
for the clone's candidate under refs/heads rather than refs/remotes/origin.
Its original script and [setup-failure receipt](../checks/cold-a-runner-v1-failure.json)
remain unchanged. Version 2 fixes that diagnostic-only ref lookup. Separately,
post-run Git status under the default sandbox account reported different snapshot
ownership; status was successfully rechecked under the creator account without
changing safe.directory. These are tooling/access observations, not product failures.
The [final integrity index](../checks/cold-a-final-integrity.json) records clean
snapshot heads, verified receipt counts and SHA-256 hashes of every prior artifact.

## Advisory implementation guidance - nonbinding

Keep schema-derived decision admission and the owned immutable policy boundary.
If these tests are later expanded, retaining a same-width malformed action-kind
member and a caller-hook counter would guard the validation order more directly
than a scalar deep-tuple example alone. This is optional test advice, not a
required correction, operating gate or requested source change. A policy/runtime
redesign is not justified by this narrow corrected defect.

## Limits and disposition boundary

No value-ingress, trace-acceptance, publication/accounting, or Slice C correction
was reviewed or implemented. Existing trace tests were regression checks only.
No broad suite, GPU/dependency installation, experiment/rehearsal/owner invocation,
source commit, merge, push, integration, or ref retirement was performed. This is
not full A/B acceptance, an operating-budget result, or an authority to publish.
There are no unresolved required outcomes in r003's declared fix scope.

This report is issued append-only. The reviewer will append one task-ledger
verdict only after the coordinator grants the serialized append slot.
