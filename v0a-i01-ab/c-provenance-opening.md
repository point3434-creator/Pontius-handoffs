# r008 helper-provenance repair opening

The first independent integration reviewer reported valid public derivation that
approves one literal subprocess capability without blockers for an impossible
receiver or class qualifier. Examples: a comprehension target shadows self with
None; a local assignment shadows the helper class with None; a helper parameter
shadows that class name. Pure Python projection validation is being finalized by
the reviewer. r008 is frozen and will not be edited or used for broader gates.

Category to close: helper identity/binding authority at the actual call scope,
including ordinary receivers and qualified helper class/module names. The current
registry fallback can recover a historical name despite newer source-flow state.
Reusing the enclosing-local exception visitor also intentionally omits comprehension
targets, which is insufficient proof for calls inside the comprehension scope.

Systematic discovery must cover all binding forms and evaluation scopes, direct
and local/cross-file helper resolution, nested/default/decorator expression contexts,
class/module qualifier and member writes, deletion and conflicting branches. Use
existing source-ordered state where possible; no independent heuristic name allowlist
may override lost provenance. Unproved cases refuse even with fixed argv.

Only tools/generate_test_inventory.py and tests/test_inventory_and_profiles.py may
change during the repair. Ordinary generated inventory/profile pair and mechanical
census expectation refresh follow once source is GREEN. All ten accepted A/B paths
and the remaining C boundary/CI files stay byte-exact. Worktree:
D:/Pontius-worktrees/codex-v0a-i01-c-provenance at r00800db06624ab25f10cd181badccf92c87a78f17ee.

No production edit before the category/discovery design is reviewed at Stage0.
Real public derivation fixtures with independent pure Python return projections
supply RED; no sensitive source subprocess is executed. GREEN is both exact slots,
new negative/positive scope matrix, existing binding/flow methods, then the complete
affected combined suites and generator checks. A changed byte requires a new frozen
round and two fresh cold contexts. No approval, baseline, sealed kernel, optional/GPU,
guarded profile, source seal, rehearsal or final main commit authority is added.
