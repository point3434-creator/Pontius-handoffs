# Independent pre-coverage inventory

Recorded before opening coverage.md, implementation evidence, or any peer review.
This is a cold review of candidate 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.
The independently reconstructed whole-row-sorted blob manifest hashes to
8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb.

## Surface and source authority

The initial packet hashes match the handoff. Frozen ADR-0485, ADR-0484 and the
revised brief define the integration contract; pinned current CLAUDE/workflow
and acceptance.md narrow this FIX and execution policy. No mutable checkout
source, prior reports, peer reports, or implementation narrative is an input.

The 17 manifest paths are:

- .github/workflows/ci.yml
- src/pontius/v0a/__init__.py
- src/pontius/v0a/clock.py
- src/pontius/v0a/model.py
- src/pontius/v0a/replay.py
- src/pontius/v0a/runtime.py
- src/pontius/v0a/trace.py
- tests/test-inventory.json
- tests/test-profiles.toml
- tests/test_inventory_and_profiles.py
- tests/test_v0a_boundaries.py
- tests/test_v0a_contract_faults.py
- tests/test_v0a_hand_replay.py
- tests/test_v0a_replay.py
- tests/test_v0a_trace.py
- tools/check_stabilization_boundaries.py
- tools/generate_test_inventory.py

The actual FIX changes only generator, inventory contract tests and ordinary
generated inventory. Six modules plus four A/B suites independently match
ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1. CI, boundary checker and boundary tests
match 00db06624ab25f10cd181badccf92c87a78f17ee. The profile file is unchanged by
the FIX. The legacy dependency-baseline blob remains
5fe6ee47f3380b65887b528efef05b72c8e6ac0a. Clone metadata records these comparisons.

## Requirement / risk to evidence map

1. Exact candidate and preserved contract: reconstruct Git blob rows, verify
   refs/tree and 13 preservation comparisons; hash tracked clone files before
   and after every payload. No candidate edits or governance writes.
2. Static source-point callable identity: inspect _ReviewFunction registry,
   _HelperProvenance/_FlowValue, source-ordered resolver, binding and review-body
   expansion. Name rebind must not erase a retained alias. Missing proof cannot
   become an execution/nonexecution assertion.
3. Python binding semantics: positional-only receiver, defaulted receiver,
   static/class methods, keywords, bad arity, decorated callable identity.
   Preserve callee-before-argument evaluation and precise lookup exceptions.
4. Effective inputs: authority can exist only in a default, closure, receiver,
   returned callback, container or imported helper. Captured defaults use the
   definition point; closure free names use the applicable call-time cells.
   Unrelated reads must not determine whether a mutation is refused.
5. Effective outputs and reached effects: helper-member store/delete, setattr,
   opaque forwarding, callbacks and implicit protocol invocation must preserve
   authority or refuse. Literal sink argv does not justify unknown provenance.
6. Construction and scheduling: defaults and decorators obey source/class order;
   relevant unresolved annotations may refuse portably but deferred annotations
   must not be reported executed. Generator/coroutine creation, dormant storage,
   supported consumption, escape and proved nonexecution are distinct.
7. Finite analysis: metered walks, bounded depth and cardinality; unsupported
   reflection/heap shapes produce blockers. Sensitive fixture source is parsed
   only. Independent runtime oracles must contain harmless effects only.
8. Discovery and integration: five v0a test suites admitted; old inventory
   assignments/profile capability grants unchanged; --check passes without
   mutation. Relevant generated census only changes mechanically.
9. v0a boundary: exactly six origins, replay-only river/complete-deal access,
   absolute/relative/alias/deferred/wildcard/malformed cases; legacy edges and SCC
   policy preserved. Existing hard gates remain, five additions use !cancelled().
10. Execution: real CPython 3.11.15 first then 3.14.6; full identity before
    imports, -B -P, clone cwd/src PYTHONPATH, scrubbed environment, D-local temp,
    absolute validated Git. Only focused checks, never the 17-target wall here.

## Independently selected verification

Inspect the affected DesignReviewTests before trusting them. Run the inventory
suite, generated --check and focused boundary checks on both interpreters.
Add outside-snapshot adversarial public derive_design_review inputs selected
from points 2-6, emphasizing retained aliases, defaults/late cells, opaque
container escape, magic protocol callbacks, and dormant versus consumed async
work. Obtain expected Python ordering only with separately authored harmless
runtime controls; never execute the sensitive source supplied to the analyzer.

The analyzer is a bounded trusted-source classifier, not a general interpreter
or malicious-Python sandbox. Explicit refusal can be correct for unsupported
shapes, while lawful literal/bare-type/readonly/dormant controls must remain
lawful. Coverage is not claimed exhaustive. Required corrections, defect verdict
and design assessment remain separate from implementation advice.
