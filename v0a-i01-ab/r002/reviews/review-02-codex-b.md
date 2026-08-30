# Cold review B - v0a-i01-ab/r002

Reviewer: Codex /root/ab_r002_cold_b, 2026-08-30.
Tier C, independent cold policy-authority FIX review. No source changes.

**Defect verdict: NOT CLEAN - one Important direct-helper refusal defect.**
**Design verdict: SOUND.** Exact admission into an owned immutable graph fits
this authority contract. The remaining finding is a validation-order/exception
boundary defect, not another demonstrated policy-identity substitution. A small
bounded correction is appropriate; no sealed-kernel rewrite is recommended.

## Frozen identity and independence

- Candidate: `2f4287f68a83fac4225a05a91daffdb3f2977a43`.
- Ref: `refs/heads/review/v0a-i01-ab/r002`.
- Base: `256bcf5b1e721c70216f4d8937166cbb9c25a7ce`.
- Tree: `7d1383a1a7b2cf05442e4ef4fe8a9189708b2263`.
- Manifest SHA-256:
  `55f7ebf8827c79a6d6c70b1bf26508d87527b8c7113d2458fb4c3dfb5fed0957`.

Ref, parent, tree, all four stored-blob rows, whole-row ordering, manifest file
bytes and its SHA-256 independently verify. Only runtime.py, replay.py and the
two declared tests differ from the parent. Changed blobs are LF-only/BOM-free;
Git diff whitespace checking passes. Sealed source/action_for is unchanged.

I read only the handoff's allowed cold inputs, current process/checklist,
frozen source/tests and permitted outcome dispositions. I recorded
[my independent inventory](../checks/codex-b-initial-inventory.md) before opening
coverage.md, whose SHA-256 independently matches
`35edf1f2b309f0bc017f6831631efaead86d0cf3b8f6cf1fe9db6a753b102b12`.
No implementer conversation, plan, self-report, root-cause narrative, referenced
implementer receipt, or another review was read. Coverage was compared as a
claim, not adopted as evidence.

## B-01 - Important: malformed exact context escapes its typed refusal

Confidence: high; independently reproduced on CPython 3.11.15 and 3.14.6.
Frozen location: `src/pontius/v0a/runtime.py:88-89`, `:152-157`.

ADR-0485's blueprint-outcome contract requires an invalid decision context to
terminate with a typed failure. The handoff explicitly includes the direct
four-input helper in this round's closure. That helper currently leaks an
unclassified `RecursionError` from an ordinarily constructed context:

```python
cards = OneSeatCardState.preflop(controlled_seat=3, private_hand=(0, 13))
betting = NoLimitBettingState.six_max_100bb(button=0)
decision = betting.legal_decision()
source = ImmutableBlueprintActionSource("cold-b-depth-control")
value = 200
for _ in range(600):
    value = (value,)
bad = dataclasses.replace(decision, stack=value)
select_blueprint_action(source, cards, betting, bad)
# Observed: RecursionError. Required: InvalidDecisionContextError.
```

`LegalBettingDecision` is an exact frozen dataclass with no field validator.
Its normal constructor accepts this value; the probe uses no private writes,
constructor bypass, subclass, source monkeypatch, recursion-limit change or
callback. The candidate recursively copies the supplied decision before
comparing it with the legal decision derived from betting. Its generic copier
traverses arbitrary exact tuple structure in an integer field, exhausts Python
recursion, and the exception set at line 156 does not normalize that failure.

The same independent reproduction covers `action_kinds` and `raise_bounds`.
Depth-one wrong shapes yield `InvalidDecisionContextError`; depth 600 yields
`RecursionError` for each field on both required interpreters. This is a
concrete missed context-shape member, not merely absence of a test. A direct
helper caller catching the documented context/blueprint failures instead sees
an unexpected exception. No selection is returned and no false policy identity
or runtime action was demonstrated; the impact is bounded to malformed direct
helper inputs and truthful typed refusal.

Required outcome: malformed context shapes must be refused through
`InvalidDecisionContextError` before selection, without arbitrary recursive
traversal escaping the public helper. Cover all three reproduced fields plus
normal legal contexts and nested subtype refusals on both actual interpreters.
Preserve owned policy authority, sealed lookup, and the existing outcome split.
Do not introduce an invented operational depth budget to disguise a field that
is already structurally invalid. This is not a claim about valid large tables
or valid long public histories.

Evidence: [minimal reproduction](../checks/codex-b-context-depth-repro.py),
[3.11 receipt](../checks/codex-b-311-codex-b-context-depth-repro.json), and
[3.14 receipt](../checks/codex-b-314-codex-b-context-depth-repro.json). Their zero
exits confirm the documented observations; they are not passing verdicts.

## Verified authority closure and coverage comparison

| Requirement / independent risk | Fresh evidence | Result |
| --- | --- | --- |
| Outer digest/canonical/lookup and class-pretender substitution | Real runtime, direct helper and ReplayHost admissions; hook counters | Pass |
| Nested policy field authority, including nonempty history | Generated field walk; 339 boundary rejections per interpreter, zero caller hooks | Pass |
| Context top types, history, records, containers and scalar subtypes | 66 direct-helper rejections per interpreter, zero caller hooks | Pass |
| Legal-decision numeric aliases | Seven independent float/bool alias refusals per interpreter | Pass |
| Honest hit, miss and illegal matching entry | Real mailbox runtime cases and direct helper; focused preserved cases | Pass |
| Owned identity and no second per-action table rehash | Real profiling of both full fixture hosts | Pass |
| Initial identity remains measured | First real canonicalization delayed 16 seconds; exact elapsed retained | Pass |
| Structurally malformed exact direct-helper graph | Three depth-600 cases on both interpreters | Fail, B-01 |

The generated walk distinguished three constructor-normalized container cases
from boundary-tested cases; those three are not counted as admission refusals.
It used normally constructed values and truthful hooks, then cleared hook
observations immediately before the production boundary. This challenges the
category rather than only repeating the frozen test names.

For fixture A, profiling observed one admission, four sealed lookups and six
source canonicalizations: header, initial measured binding, and one per lookup.
Fixture B observed one admission, two lookups and four canonicalizations.
Every observed source lookup/hash used the same owned source, never the caller's
source. Header and every decision digest agreed. Injecting sixteen seconds in
the first digest operation produced exactly 16,000,000,000 elapsed nanoseconds
and action_deadline_exceeded; the known late delivery remained retained as the
contract requires. These are deterministic correctness diagnostics, not measured
performance results or operating-budget provenance.

The deferred coverage claim matches the discovered entrances and nested-hook
members. Its finite subtype/alias evidence does not cover B-01's malformed exact
shape traversal. No arbitrary metaclass or private-mutation attack is needed
for that gap. Historical R2-01/R3-01 identity substitution was not reproduced
against this candidate; B-01 should not be mislabeled as another such residual.

## Execution and limitations

Fresh clone outside the packet repository:
`D:\pontius-snapshots\v0a-i01-ab-r002-cold-b-20260830`.
Each payload asserted actual interpreter identity before application imports,
`-B -P`, snapshot cwd, exact snapshot/src PYTHONPATH and snapshot module origin.
The environment was scrubbed; Git was the absolute
`C:\Program Files\Git\cmd\git.exe`. No CuPy/Torch import was observed.

Runs were CPython 3.11.15 at `D:\Pontius-tools\py311\Scripts\python.exe`
first, then CPython 3.14.6 at `D:\Pontius\.venv\Scripts\python.exe`.
Each passed 39 hand-replay, 22 contract-fault, 45 replay-host and 25 trace tests:
**131 focused tests per interpreter**. Commands, environments, origins, exits
and output are retained in [3.11 focused](../checks/codex-b-311-focused.json)
and [3.14 focused](../checks/codex-b-314-focused.json) receipts. Independent
probe results are in the corresponding `codex-b-*-codex-b-policy-probe-v2.json`
receipts, with [the source](../checks/codex-b-policy-probe-v2.py).

The first retained probe version failed its own incorrect assertion that an
already late action could not be delivered. That was a diagnostic expectation
error: the contract retains late accepted delivery. Version 2 instead checks
measured elapsed time and typed deadline failure, records actual delivery, and
passes on both slots. The original failed script/receipt is retained and is
not used as product-defect evidence.

No source/test edits, broad suites, GPU/dependency work, lifecycle invocation,
trace-acceptance expansion, publication/accounting work, evidence commit,
integration, or ref retirement was performed. This review does not establish
operating bounds, exhaustive hostile-input resilience, or Slice C acceptance.

## Advisory engineering guidance

Keep exact source admission and owned reconstruction. For the direct decision
input, use the known legal-decision shape to reject structurally impossible
fields before recursively copying them. A comparison against the independently
derived exact legal decision can bound traversal by the expected schema rather
than caller-provided nesting, provided exact type checks precede attribute or
equality use. Alternatively use a schema-directed copier. Those techniques are
advisory choices; B-01's typed public outcome and preservation criteria are the
binding requirements. A whole-runtime or sealed-blueprint redesign is unwarranted
by the evidence from this review.

The report is issued append-only. Its owner will append the single task-ledger
verdict after the coordinator grants the serialized append slot.
