# Class composition findings and bounded repair proposal v1

Engineering diagnosis and design proposal only. NOT a cold review, acceptance result, source patch, test authorization, or storage-port regression attribution. No production source, old cases, expectations, control, cap, or public API was changed. This turn read retained results and source, parsed JSON/AST using stdlib only, and wrote this create-only T note; it imported/executed no Pontius analyzer, source fixture, oracle, or payload.

The primary normal-path defect is a missing destination capture for a write-only nonlocal setter. It is not, in these traces, an already-updated cell hidden behind a stale outer projection. Class completion refresh remains a separate post-capture repair obligation. The explicit-raise class loop also continues into unreachable statements. A coherent repair must cover capture destinations, precise rebinding, and all class exits; refreshing the normal class end alone cannot repair this category.

## Evidence identity and limits

All source lines below refer to retained `T/engineer-generator-v19.py`, SHA256 `3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1`. T is `D:/Pontius-handoffs/v0a-i01-c-authority`. The production worktree remains v20 SHA256 `e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679`; no write there was authorized or performed. Static AST comparisons show v19/v20 equality for `_callable_free_names`, `_with_callable_authority`, `_helper_effect_shape`, and `_helper_local_namespace_effects`. The executed evidence is specifically v19, so these are newly demonstrated defects already present before the name-storage port, not proof of a new v20 regression.

Root ran reviewed control v2 SHA256 `5dd1e6692f82d096a976ca248b45e313a93a97922331186e2cf3e462c2c37717` with mechanism probe SHA256 `4e2e0cb1f472a6cf7f0c38bd699f4fc54c084db29e5f903305e88f1358dbe83e`. Each scope ran on Python 3.11.15 then 3.14.6 in a fresh r010 clone, commit `29c02f6fbd5eb0b7ddc9e816ef28f570b9839358`. All four receipts report intact infrastructure, 1761 tracked files unchanged during the child, no oracle/analyzer errors, and semantic exit 1. Root independently rehashed the snapshots in `coordinator-class-mechanism-verification-v1.json`, SHA256 `529fe91786c2b4f699d5476d0d0f6cf6e60594f464c23e01d7475bddcd06f6ee`.

Receipt files are under `T/tests-checks/`, prefix `class-composition-`, suffix `-v19-mechanism01-{slot}-receipt.json`:

| Scope / slot | Receipt SHA256 | Corresponding .txt log SHA256 |
|---|---|---|
| original-class2 / 311 | 9c26c08e8fab39c11e0c49ccd952274b0a31eb98899b51d2bd3f419cf9ad0f32 | e33010b37137e38bc7eb969501ffe2c66c08921a9f165fd5f38d3e572f6f501a |
| original-class2 / 314 | b8429565b8179962c00e3207c6669d294ceb678bf255b9f09250d1cb26e31314 | 2235228af384caf4f4f8538ea23df3d586493a01bd1ae1b93ffaed096aa86e7c |
| scalar-class6 / 311 | 9c86569d53b6664bf5a6f1912607255c253412dac70d2bd74bfb1dda454b6be9 | 778b795f2e5bb48dfa24dad28929f87e641dc31f2280e1c7df2a7b67da1593d5 |
| scalar-class6 / 314 | 97ff9ac31ad8a1eb3f75f3dcde461e1c2ff392ed1d705481cd5e9b45f156ff2d | 840a93ae339f77f52b3487f843a5a99d2e8cb883394351bb97e08ee330e5cc1c |

I rehashed these bytes, parsed each log, selected all `class_adoption_mechanism` objects in event order, recursively removed ONLY the `budget_units` key, and compared complete objects across slots. All 60 original events and all 196 scalar events match. Canonical JSON (`sort_keys=True`, separators comma/colon) normalized-event SHA256 values are `9dcd5718c7c87a3cd1055315e28aa0966ea1adfbefb200f6164d283c0c0aa0ce` and `6532a6518e589140cd8e011934329ce1eb69f19d6ed80090a4739d6b41c0a872`. No private numeric identity equality is an oracle. There are zero `recursive_review.entry` events in every log.

Frozen original pack remains SHA256 `faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709`; scalar extension remains SHA256 `50e88cedf77f902012237ccd88700c911fa8f3681c8dada380cca6c3142659ac`. Sensitive fixtures were parsed/reviewed only. Independent harmless models supplied the expected traces. No expectation is weakened.

## Public outcomes and directly observed mechanisms

Both slots agree:

| Case | Frozen public expectation | Actual public result |
|---|---|---|
| class-adoption-unsafe | refuse | clean row `[-m, outer]`; no blocker: FAIL |
| class-adoption-safe | clean `[-m, outer]` | refused: FAIL |
| scalar-class-normal-unsafe | refuse | clean row `[-m, outer]`; no blocker: FAIL |
| scalar-class-normal-safe | clean `[-m, outer]` | refused: FAIL |
| scalar-class-change-then-raise-unsafe | refuse | refused: passes output check, not mechanism proof |
| scalar-class-change-then-raise-safe | clean `[-m, outer]` | refused: FAIL |
| scalar-class-raise-before-change-unsafe | refuse | refused: passes output check, not mechanism proof |
| scalar-class-raise-before-change-safe | clean `[-m, outer]` | refused: FAIL |

1. **Lost write destination, normal path.** In both normal scalar cases the reader captures `armed`, but `change(value): nonlocal armed; armed = value` records `captures=[]`. At class entry the outer cell has the initial scalar. Class bindings are reset. The setter's call environment consequently has no `armed` cell. The assignment changes its private projection to the requested opposite scalar, while the reader's captured cell remains unchanged. Class completion returns the original outer projection AND original cell. `_call_environment(read)` hydrates that same unchanged cell, so the unsafe initial False is treated as harmless and the safe initial True as harmful. In each normal case event 19 is setter environment, 21 assignment.after, 23 class.after, and 28 reader environment. This disproves the earlier primary updated-cell/stale-projection hypothesis in `engineer-class-composition-static-mechanism-v1.md`; it does not delete that immutable note.

2. **Protected rebind guard is an additional seam.** The original owner pair shows the same empty setter capture and absent destination cells. In the safe ReviewTests-to-None case, assignment.after event 21 also records `helper namespace binding change is dynamically unresolved` at source line 14, propagated to caller line 17. Class completion still exposes the original ReviewTests cell. Separate call-snapshot namespace-effect refusal and post-call rebound poisoning exist in source; repairing only capture or only the assignment guard is insufficient. Rebinding a precise lexical cell is not itself mutation of the previously referenced class object or its other aliases. The original clean expectation remains intact.

3. **Direct class raise fails to terminate its item loop.** In raise-before-change cases, enabled events 17/18 are direct Raise before/after; events 19 through 26 then analyze the unreachable setter and assignment. Event 27 is class.after. In both exceptional schedules, the later reader snapshot (event 28) contains divergent `armed` AND `module`; the outer module should remain literal `outer`, whereas class-local `module` is `inner`. Reader hydration preserves the divergence. The two unsafe refusals therefore cannot certify correct exception analysis.

The logs did not instrument throw-state recording, handler joins, or every namespace transfer. Thus the exact number/order of contamination edges is not asserted. Source identifies a concrete route: `_record_throw_state` 16323-16335 copies its supplied name map; generic class flow 22171-22179 goes through `_flow_expression_statement` 21613-21630, which collects exceptions while calling the legacy class loop. Calls at 19686-19692 and helper must-raise propagation 18489-18496 can publish a class map into that collector. The outer Try handler starts from the exceptional map at 22062-22064 and later coalesces with normals. A class-map exception must be projected back into the enclosing namespace before that join. Direct Raise currently takes legacy 22539-22542, not real successor handling 21672-21740.

## Capture construction inventory and scope obligations

`_callable_free_names` 17593-17610 uses a full recursive `_metered_ast_walk` (7856-7865), selecting ONLY `ast.Name(ctx=Load)` not in the containing function's local-name set. `_with_callable_authority` 17634-17648 resolves those names to enclosing cells and writes the callable authority record's cells. Static AST enumeration finds five constructor callers, all sharing this selection:

| Site | Construction path |
|---|---|
| 17771 | retained implicit callable fallback |
| 18048 | synthetic function for construction-expression obligations |
| 18078 | descriptor/method construction obligations |
| 19177 | lambda callable construction |
| 22852 | local FunctionDef / AsyncFunctionDef installation, including local generator metadata paths |

No second independent authority-record cell-capture constructor was found. Deferred generator factories retain definitions/defaults; they are not an alternative destination-capture algorithm. `_helper_effect_shape` 17878-17898 has another Load walk, but already detects declared Name Store/Del as effects: deciding that effects exist does not supply the missing destination. `_helper_local_namespace_effects` 23372-23378 uses `_MeteredHelperBindings`, and provides existing scope-aware declaration/binding infrastructure rather than a new raw all-Store predicate.

The repair design must account for the following bounded lexical category. Rows beyond the observed setter are static obligations, not executed new failures or blanket promises of newly supported syntax:

| Form / boundary | Required interpretation and current risk |
|---|---|
| Own-scope declared nonlocal Store | Capture the actual enclosing function destination even with no read. Includes assignment/destructuring and other valid binding forms, not just `x = value`. This is directly demonstrated. |
| Declared nonlocal Del | `ast.Del` is omitted by Load selection. `_delete_target` 21124-21151 must publish the unbound marker to the captured destination, with correct lookup/exception behavior. |
| Declared nonlocal AugAssign | Name target has Store context although evaluation reads it at 22472, then writes through 22518. Capture is needed even without another explicit Load; existing conservative arithmetic/protocol behavior must not be widened accidentally. |
| Read-only and read/write nonlocal | A Load may make the current capture succeed. Preserve this route, including alternatives; it must not regress while write-only support is repaired. A coincidental inherited caller binding is not proof of the correct captured destination. |
| Globals | A declaration alone, write-only Store/Del, and AugAssign need defining-module resolution distinct from lexical nonlocal. `_registered_helper_environment` 17918-17934 deliberately seeds defining-module globals and filters caller locals. Do not capture a same-spelled caller local or class attribute. Missing/unrepresented module provenance remains a conservative case. |
| Nested functions and closure forwarding | A grandparent destination used only by a nested write-only setter may have to pass through an intermediate closure even when that intermediate body neither loads nor declares the name. Unioning only the current function's declarations is insufficient. Conversely, descendant parameters/locals and their Loads are not globals of the outer function. |
| Function definitions inside class compounds | Class loop 23016-23018 sets the enclosing override only when the immediate item is FunctionDef/AsyncFunctionDef. A method under If/Try currently enters without that override. A class frame must retain its enclosing nonclass environment across compound statements and nested classes; methods must skip class attribute bindings when resolving free lexical cells. |
| Direct class declarations | Class-local Store/Del differs from explicit class-body global/nonlocal. The present class reset 23003 has no corresponding class-specific lexical declaration routing; default `_statements` traversal treats declaration nodes as inert children. Do not apply function-only `_lexical_binding_scope` to ClassDef (it accesses `.args`). Any supported direct declaration path needs an explicit frame destination. |
| Comprehensions / lambda / defaults | Comprehension target scopes must not become enclosing captures; the outermost iterable and defaults are evaluated in the surrounding scope at their actual time. Nested function decorators/defaults are eager metadata, nested bodies deferred. A default retaining a value is distinct from a closure retaining a live destination. Preserve lambda/comprehension and generator boundaries rather than recursively collecting every Name. |
| Distinct activations / sibling closures | Capture ownership follows the lexical activation, not source definition identity or the current caller's name map. A class-cleared map exposed this bug; escaped or separately invoked helpers must not accidentally update unrelated caller cells. Preserve shared cells between siblings and separate cells between activations. |

Reuse and extend the existing scope-aware visitors/contracts (`_ExceptionBindingVisitor` 9700-9797, `_lexical_binding_scope` 9800-9833, `_MeteredHelperBindings` and eager metadata visitors). They are building blocks, not a claim that their current traversal is a complete free-variable algorithm. `_lexical_binding_scope` intentionally excludes nested function/class bodies while visiting eager metadata; `_callable_free_names` currently does not preserve those boundaries. Keep every traversal explicitly metered and bounded; no new unmetered whole-tree pass or raised work cap is proposed.

## Bounded repair requirements, not a patch

A. **Represent invocation destinations before writing.** Establish scope-correct captured destinations and hydrate the invocation projection from their cells before argument/local setup, preserving defaults and caller evaluation order. Reuse the authority ownership model and missing-store checks; do not manufacture a global capture from an unrelated ambient projection. Missing retained refs reachable through legitimate adoption remain relevant; fabricated future numeric IDs are outside the public parsed-source contract.

B. **Separate precise binding writes from unresolved namespace effects.** The same represented-destination decision must govern `_assign` 20764-20770, `_delete_target` 21124-21130, call-snapshot refusal 16179-16182, and helper-completion rebound processing 18475-18483. A merely present `bindings[name]` is insufficient proof: the invoked callable's lexical destination and retained store must justify it. Preserve unresolved/global/dynamic namespace guards where that proof is absent. Preserve strong writes for one destination and weak writes for alternative cells (14130-14134); no blanket strong write and no removal of object-mutation refusals. Do not overwrite a successfully updated represented cell with `helper namespace binding was changed` after completion. Rebinding/deleting the lexical name must leave independently retained old object aliases and bound methods valid unless their objects were actually mutated.

C. **Execute class bodies with successor semantics in an explicit namespace frame.** A frame carries separate class locals, enclosing nonclass lexical/global destination context, and the outer continuation. Integrate existing `_flow_statements` / `_flow_statement_value` semantics instead of teaching the per-item `_statements` loop one special Raise rule. Preserve supported source order for decorators, bases, keywords, method defaults, class assignments and protocol checks. Class-body If/Match/loops/Try/handlers/else/finally must retain the frame and proper successor kind. Keep existing unsupported-protocol/TryStar refusals; this proposal does not expand their contract.

D. **Project every outward class successor, not just normal completion.** Carry live object/cell effects into the enclosing authority; rebuild/refresh only enclosing bound-name projection from adopted cells, with raw hydration semantics rather than replaying semantic assignments. Keep outer bindings and class locals separate. Successful completion can install the class name; body/construction failure must retain the preexisting/unbound outer class-name binding and no class-local leakage. Effects before a direct raise or a known call-raised exit survive an outer handler; statements after that exit do not run. For a raise caught within the class, execution resumes in the class frame; only later exit translates outward. Preserve exception tags/excluded handlers and finalbody effects. Header-time failures already occur in outer evaluation; avoid replaying or losing their effects. Nested class exits translate one frame at a time.

Class normal adoption at 23025-23026 only forks authority, unlike helper completion 18459-18472, which preserves caller observed/results and refreshes bound projections. Once destination capture is repaired, class-end projection freshness becomes a real invariant to establish even though it was not the first cause in current traces. Caller observation/result ownership must be handled deliberately for class frames; do not blindly adopt callee/class stack observations or assume copying the helper code is automatically sufficient.

E. **Audit recursive review entry against captured call state.** Live helper effects use `_call_environment` 14437-14455. Recursive local-helper review at 25325-25329 instead filters the ambient `source_flow.values_by_call` projection into a new state with inherited authority. Review must receive the callable's captured destination values from the correct retained call snapshot, consistently with live effects, while respecting arguments/defaults and local-name initialization. Current logs contain no recursive-review entries; this is a static integration obligation and possible post-repair consequence, not the demonstrated primary cause. Do not apply an unreviewed hydration helper that consumes budget twice, mutates captured cells while copying, or imports unrelated caller namespace.

These requirements apply to authority-enabled semantic execution while preserving the intentionally limited helper-disabled prepass. Class method skip behavior at 23006-23014 must remain bounded and must not rescan every dormant body. No change to modes, caps, public outputs, probe APIs, old scopes, or storage-cursor representation is authorized by this proposal.

## Evidence to freeze before implementation beyond current cases

The retained eight cases already fix public expectations for normal toggles, effects before direct raise, unreachable setters after direct raise, and protected-owner rebinding. Their two unsafe exceptional passes are not enough; the safe counterparts are essential. Preserve all original/shared-list and other frozen scopes.

Before expanding the repair to unobserved paths, select a finite public-output coverage extension with independent harmless traces, reviewed before execution. Small discriminating families are:

- A helper called in a class body that changes a captured scalar and then raises a known builtin exception, caught outside; opposite initial/final polarity distinguishes preserved effects from blanket refusal. A no-change-before-raise counterpart distinguishes execution order. This exercises call-raised exit, currently only a static route.
- A class-internal branch and a class-internal Try/handler/finally with a scalar change, plus a reader method defined under the compound statement. Require the supported clean `[-m, outer]` or refusal and no `inner` namespace leakage. Do not assert private allocation order.
- Write-only nonlocal deletion and read/write controls, a forwarded grandparent destination, and a same-spelled caller-local/defining-global distinction. Freeze only behavior already admitted by the contract; for AugAssign preserve existing allowed refusal if arithmetic remains unsupported, while requiring correct destination/side-effect behavior where observable.
- A recursive helper body that actually emits the public row and reads a changed captured scalar, so the recursive hydration boundary is exercised rather than inferred from these zero-entry traces.

These are candidate coverage obligations, not authored or executed cases and not permission for broad/owner runs. Resolve scope and supported expected outcomes first. Static proof can discharge a boundary where no public difference is possible; private object/cell numbering or harmless extra allocation alone is not a product failure. Implementation review should demand one coherent capture-and-class-frame argument, then the unchanged finite floors and approved targeted extensions, rather than patches to each observed refusal line.
