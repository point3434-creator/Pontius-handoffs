# C provenance v3: effective callable inputs and effects — Stage 0 addendum

Scope remains only tools/generate_test_inventory.py and tests/test_inventory_and_profiles.py
in the c-provenance worktree, plus append-only worker v3 artifacts. Base for this correction
is released v2 generator a57f76e38bd8e8494ab16fb878e2887854d3f59844fb1e78bd3d50c54f0b4341
and tests af929697b3f6c8ddad823ff16bef63936f5b924cdf16992d8bc93679368ca961. The root's
abc-provenance-v2-owner-probe-311 receipt is existing RED: a local helper's omitted owner
parameter mutates ReviewTests._launch, but its body is skipped as originally nonsensitive.

The violated boundary is the complete effective invocation, not a particular default
syntax. Current escape admission sees only explicitly written arguments, requires a
registry callable, and excludes local marker identities and their captured defaults.
The sensitivity-only local-body shortcut then silently discards an actual namespace effect.

## Binding-path inventory and preservation requirements

1. Explicit inputs: ordinary positional, positional-only, keyword and keyword-only values;
   bound argument values are those already evaluated, with callee capture before arguments.
   Supplied values replace the corresponding default, including a supplied harmless value.
2. Defaults: omitted positional and keyword-only defaults use definition-time values;
   local callable_defaults already retains them. A saved local callable keeps its original
   definition/default values after source-name rebinding. Module/class defaults need a
   conservative definition-context value/proof projection; uncertain defaults stay unknown.
3. Receiver input: ordinary bound methods and classmethods carry the captured receiver as
   an effective first formal. Staticmethods and ordinary unbound class access do not invent
   a receiver. Receiver parameter spelling never determines descriptor semantics.
4. Lexical inputs: free closure cells and globals resolve in their invocation environment;
   local/parameter bindings shadow them. A readonly global/nonlocal declaration is harmless;
   reached assignment/deletion or member mutation is an effect. Dormant nested bodies are
   not executed merely because they mention an owner.
5. Callable paths: registered functions/methods, local definition markers, saved aliases,
   and nested lawful wrappers use the same admission. Lost or merged identity remains a
   typed refusal; raw registry spelling never restores authority.
6. Invalid versus unsupported binding: a proved duplicate/missing/positional-only keyword
   TypeError has no body effects. Preserve existing exception successors and census tables.
   Unsupported argument expansion or unresolved input needed for a namespace effect refuses.
7. Effect order: reached mutation before a raise remains relevant; raise before mutation
   does not mutate. Current-call capability expansion remains tied to entry state. Effects
   invalidate subsequent lookups, without erasing already captured callable entry identity.

## Bounded design

Replace the explicit-argument-only preservation gate with one effective-input builder and
one effect admission path. Resolve a local definition by its existing executable marker,
or a registered definition by exact callable proof. Bind FlowValues once using the existing
value binder's valid/invalid/unsupported distinction; extend its private role/name only if
needed rather than duplicating Python argument binding. Bind the captured receiver and
selected defaults alongside supplied values. Preserve legacy FlowValue kinds/summaries,
meet receiver metadata independently, and never re-read argument ASTs after later effects.

Reuse the existing source-ordered resolver for the narrowly selected callee effect body,
with the effective parameter values and proper free/global environment. This supports lawful
nested self._launch wrappers and existing branch/exception behavior without a second syntax
blacklist or a generic heap. Analyze only when relevant owner identity/potential namespace
inputs are present; dormant generators remain deferred and use their existing consumption
path. Recursive/deep/unproved effect analysis refuses under existing item/work limits.

Propagate only helper namespace/escape refusals and known invalidated owner identities;
ordinary protected-return and exception summaries remain on their original path. Snapshot
the current invocation after argument evaluation, then apply body effects for later calls.
This preserves legitimate capability rows inside a currently invoked fixture helper even
when a body effect needs a blocker, and prevents a subsequent helper lookup from acquiring
stale proof. Unknown callees receiving owner identities remain explicit opaque escapes.
Unknown owner writes to a discovered helper slot refuse, rather than silently assuming a
pure old body; known unrelated fields and scalar overrides remain controls.

This is bounded reuse of existing flow and binding semantics, not a Python object heap,
new runtime execution, module import execution, or capability authority. New scans and
recursive effect work use the same finite analysis budget; no cap is raised or truncated.

## Evidence plan

Before source edits add public derivation and pure-return projection controls for omitted
positional/posonly/kwonly owner defaults, explicit owner inputs, harmless supplied overrides,
free/global/receiver owners, saved default capture versus late closure rebinding, dormant
nested mutators versus invocation, and mutation/raise order. Pair them with readonly/unused
owner defaults and lawful wrappers. Sensitive subprocess fixtures remain inspection-only.
Use the supplied actual3.11 RED plus fresh named RED receipts for new discriminators.

After correction run every current DesignReviewTests method, names extracted from source
AST, through the existing fresh D-local snapshot runner: actual3.11.15 first, then actual
3.14.6 on identical bytes. Preserve all pre-v3 assertions. Root alone owns full generation,
census/expectation changes, full affected suites, review/freeze and release authority.
No main/A-B/other-C/generated/baseline/capability/ref/ledger/review-report changes are allowed.
