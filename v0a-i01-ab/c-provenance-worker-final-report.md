# C helper-provenance engineering release

Frozen base: 00db06624ab25f10cd181badccf92c87a78f17ee. Worktree: D:\Pontius-worktrees\codex-v0a-i01-c-provenance.
Scope: only tools/generate_test_inventory.py and tests/test_inventory_and_profiles.py.
Stage0 and its append-only clarification govern this bounded implementation.

The helper expansion boundary now requires a flow-carried exact callable identity
and descriptor binding mode. Registry spelling only discovers candidates for refusal.
Both attempted/unbound callee lookup and renamed helper alias loss retain explicit
blockers. Receiver/class values follow lexical and comprehension flow; local closure
cells use invocation state, installed local callables retain definition-time defaults,
and arguments bind from their evaluated values. Callable capture precedes argument
side effects. Parameters override unrelated helper seeds.

A finite member certificate uses metered lexical binding counts and shared member
mutation names across the parsed corpus. Each module retains the existing262144
work-unit cap; no cap is raised and no traversal silently truncates. Namespace-effect
metadata is gathered in that traversal; exact callable candidates have an indexed
lookup, and global seeds use referenced names. This does not implement an object heap.

Conservative explicit refusals include unproved descriptor/member replacement,
reflective namespace operations, callable __code__/__defaults__/__kwdefaults__ access,
class lookup mutation, wildcard/import rebinding, called global/nonlocal helper effects,
and escaping known owner/callable identities directly or inside modeled containers.
Stores of those identities into unsupported namespaces also refuse. Whole-corpus
member-name invalidation can reject an unrelated same-named member; it is deliberately
conservative. Module-qualified/dynamic construction and nonliteral class/object defaults
are not newly certified. Existing supported safe imports, ordinary/static/class binding,
reversed receiver names, positional-only/default parameters and lexical capture controls
remain green. No general-Python-completeness claim is made.

Tests use public derive_design_review plus independent pure return projections. Sensitive
subprocess fixture strings are inspected only and never launched. Seven new methods
cover lexical targets/parameters/deletions, all four comprehension forms, original member
stability, callee/alias capture and local admission, argument/default/callable mutation,
import/alias/cross-file mutation, and unsupported effects/opaque escapes. Nine existing
binding, helper, source-order and decorator methods are retained in the final matrix.

RED evidence:
- red02, actual3.11.15, frozen r008 generator: four methods,49 failing subcases,0 errors/skips.
- red03, actual3.11.15: definition-time defaults and callable defaults mutation,3 failures.
- red05, actual3.11.15: renamed/imported alias loss and called mutator escape,3 failures.
- red06, actual3.11.15: global/nonlocal effects and __class__ mutation,3 failures.
- red07, actual3.11.15: opaque escape through a tuple,1 failure.
- red01 is retained but includes initial projection expectation errors; red02 corrects
  those with generator still unchanged. red04 is retained; red05 expands its subtest scope.

Final GREEN: green01 on actual3.11.15 FIRST (16 tests,2.197s), then actual3.14.6
(identical16 tests,5.382s). Both exit0,0 failures,0 errors,0 skips. Each prepared runner
invocation made a fresh r008 D-local clone with exactly these two overlays, asserted
actual interpreter and module origins, used -B -P, scrubbed environment, D-local TEMP,
snapshot cwd/src PYTHONPATH and absolute Git, and verified overlay hashes after execution.

Exact runner form (outer launcher3.11; child slot asserted by runner):
D:\Pontius-tools\py311\Scripts\python.exe -B -P D:\Pontius-handoffs\v0a-i01-ab\c-provenance-run.py green01 <311|314> <targets below>

Targets:
- DesignReviewTests.test_helper_provenance_scoped_binding_losses_remain_blocked
- DesignReviewTests.test_helper_provenance_comprehension_scope_is_source_ordered
- DesignReviewTests.test_helper_provenance_original_members_require_stability
- DesignReviewTests.test_helper_provenance_callee_capture_and_local_admission
- DesignReviewTests.test_helper_provenance_values_defaults_and_callable_mutation
- DesignReviewTests.test_helper_provenance_alias_loss_and_cross_file_mutation_refuse
- DesignReviewTests.test_helper_provenance_unsupported_effects_and_escapes_refuse
- DesignReviewTests.test_descriptor_defaults_preserve_real_python_argument_binding
- DesignReviewTests.test_unknown_receiver_context_blocks_and_lexical_capture_is_preserved
- DesignReviewTests.test_receiver_descriptor_not_parameter_spelling_controls_binding
- DesignReviewTests.test_invalid_static_helper_arguments_remain_blocked
- DesignReviewTests.test_unproven_helper_descriptor_provenance_remains_blocked
- DesignReviewTests.test_helper_registry_and_argument_binding_fail_closed
- DesignReviewTests.test_registered_probe_and_cross_file_helpers_are_exactly_resolved
- DesignReviewTests.test_source_order_bounds_exception_environments_and_decorators_are_exact
- DesignReviewTests.test_round4_decorator_definition_point_red_contracts_are_independent

Every exact executed child command/environment, snapshot path, log hash and overlay hash
is retained in c-provenance-worker-final-validation.json and individual receipt files.

Final owned SHA256:
- tools/generate_test_inventory.py: d94a8e8c420c2ffccab6b2572e55e365cf0c0cba138027edbd9bdb3fb8ed7185
- tests/test_inventory_and_profiles.py: 4ee87074428c61b1b5d20998526c504806ea1f19c6c829e20471322a005220df
Patch SHA256: 46dd0fbe0be42f5b2ef63cd93be10c8c6855bdbd3b0c9a03a6be54f7ee3db6f2

Final git diff --check passed. Diff scope is exactly the two owned paths (+702/-29);
no A/B or other C bytes, generated inventory/census expectations, sealed pins, capability
state, main checkout, Git refs, ledger or cold-review files were changed.

Root still owns real-corpus generation/derivation and its performance/budget result,
census refresh, full affected integration checks, the next freeze and two cold reviews.
Tiny-fixture GREEN does not establish corpus-budget GREEN or finalization authority.
The owned files are released stable for root integration.
