# R2-E1 source-hook audit v1

Audit type: independent static engineering audit of the held checkpoint-2 source against the governing E1 repair design. This memo records implementation hooks and post-implementation proof obligations; it is not a candidate admission, runtime result, or cold-review verdict.

## Bound pair

- Held source: `D:\Pontius-worktrees\codex-v0a-i01-c-core-v1\tools\generate_test_inventory.py`
- Held source SHA-256: `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`
- Governing design: `D:\Pontius-handoffs\v0a-i01-c-authority\rewrite-r2-e1-repair-design-codex-a-v3.md`
- Governing design SHA-256: `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`

All line anchors below refer to the held source bytes. The source and design hashes were independently rechecked before this memo was created.

## Verdict

The design matches the held source architecture. I found no unexpected design/source mismatch, missing current execution path, or additional current builtin-environment consumer beyond the design-v3 inventory.

The source is not yet compliant: it has no retained builtin proof, no implicit class/import gate, and no classified proof-gated explicit fallback table. Those are the expected E1 implementation changes, not newly discovered defects in the design.

## Exact record and construction census

### `_CFunction`

The immutable slotted record is declared at baseline lines 9147-9153 with five fields: template, defaults, captures, descriptor kind, and body kind. There is exactly one `_CFunction(...)` allocation in the complete file, at 10768-10769 in `_c_construct_function`.

That single producer serves both `FunctionDef` and `AsyncFunctionDef` through `_c_statement` 10592-10593 and `_c_construct_function` 10695-10773. The required `builtin_fallback_proved: bool` field therefore belongs on this record with no default, and the sole allocation must always supply it.

### `_CFrame`

The immutable slotted record is declared at baseline lines 9137-9144 with six fields. There are exactly three `_CFrame(...)` construction sites in the complete file:

1. Class-body frame at 10806.
2. Ordinary function invocation frame at 10941.
3. Initial module frame at 11389.

No handler, branch, try body, snapshot, fork, join, call observation, or review path constructs another frame. Handlers and branches reuse their supplied frame. Checkpoint 3 has not yet introduced a generator frame.

Every current constructor must supply a required `builtin_fallback_proved: bool` value with no default:

- class body: the cached pre-base class-body creation proof;
- function invocation: the selected `_CFunction` record's retained proof;
- initial module: literal `True`.

### Function invocation convergence

`_c_call` calls the sole `_c_invoke` at 10841. Direct function references and bound methods converge in `_c_invoke`; `_CBound` is unwrapped at the corrected baseline anchor 10891-10895. The only function-body execution is the `_c_statements` call using the local frame at 10968.

Entry calls, helper calls, bound methods, recursion, aliases, and historical function references therefore share the frame constructor at 10941. Projection belongs there, from the selected `record.builtin_fallback_proved`. It must not copy the caller frame's proof and must not recompute from current module membership. Class bodies and module bodies bypass `_c_invoke`, which is why their two frame sites require independent providers.

Existing immutable object-table references preserve a `_CFunction` field through aliasing, binding, containers, state forks, snapshots, and ordered outcome joins. No `_CState`, `_CView`, namespace, cell/object table, outcome, trace, or call-observation field is required.

## Creation authority helper

The current implementation needs one creation helper with the exact semantic rule:

1. Read the current module namespace through `frame.module` and the supplied exact successor state.
2. Test exact membership with `"__builtins__" in namespace.members`.
3. If the member is present, return `False` without interpreting its value.
4. If absent, return the executing frame's retained proof.

The helper must not use `_c_name_route`, class/local lookup, `.get()` value truth, a reserved-name rule, or a monotonic poison field. Local and class-local spellings are irrelevant because the tested owner is always `frame.module`.

There are exactly two current creation-helper call sites after the repair:

- ordinary/async function creation;
- class-body function-like creation.

Future checkpoint-3 generator creation will be a separately reviewed third carrier; it is not part of this E1 source change.

## Exact timing and authority projection

### Ordinary and async functions

`_c_construct_function` evaluates admitted decorator/default expressions through `_c_eval_many` at 10736. Every normal successor is represented by `prior.state`. Captures and defaults are then materialized, and the sole record allocation occurs at 10768-10769.

The creation helper must be called with `prior.state` and the current executing `frame` after all admitted decorator/default effects and before `_CFunction` allocation. The result is retained on that exact record. A false result is historical metadata, not a reason to refuse a dormant function definition.

### Class statements

The current `_c_construct_class` performs its existing unsupported-header refusal at 10779-10780 and begins base evaluation at 10783. The compliant order for every otherwise admitted class is:

1. Preserve the existing unsupported decorator/keyword/type-parameter boundary.
2. Gate the implicit `LOAD_BUILD_CLASS` consumer using only the executing frame proof.
3. If that gate succeeds, compute and cache the class-body creation proof from the same incoming pre-base state and executing frame.
4. Evaluate bases through the existing ordered `_c_eval_many` path.
5. Pass the cached pre-base scalar to every class-body `_CFrame` created for a normal base successor.
6. Execute the body and retain the existing class-name installation order.

The gate and the creation helper are distinct. A proved module frame may have a currently present modeled `__builtins__` member: its implicit `__build_class__` gate must still pass because the executing frame already captured the ordinary environment, while the newly created class-body proof must be `False`. Using current module membership as the implicit gate would mask the required outer-class behavior and is a design violation.

The helper result must be computed outside and before the base-outcome loop. Recomputing inside the loop would allow base effects to rewrite class-body history. Methods later reached inside the class body continue through `_c_construct_function` and compute independently from their reached state and the class frame's cached proof.

### Function calls

After `_c_invoke` resolves a direct or bound `_CFunction`, validates the body, module, and arguments, its local frame at 10941 must receive `record.builtin_fallback_proved`. No live function body may receive a default, the caller's bit, or a newly computed module result.

Refused deferred functions, cross-module calls, and invalid calls do not enter a live function body and need not construct a frame.

### Initial module execution

Every module execution uses the single constructor site at 11389. It supplies literal `True`, representing the ordinary builtin environment captured by initial module execution. The modeled module namespace intentionally begins without an implicit `__builtins__` source member; explicit source writes and deletes subsequently affect creation-helper membership while leaving the existing module frame proof unchanged.

## Explicit builtin fallback hook

The sole current explicit canonical builtin fallback is `_c_read_name` at 9961-9967. It is reached only after ordinary lexical/class/module routing, and only when a module member is absent. `_CExceptionType(...)` has exactly one producer in the complete file, at 9965.

Replace the two inline spelling sets with one immutable classified table containing exactly:

- `ValueError`, `TypeError`, `KeyError`, `IndexError` -> exception producer;
- `staticmethod`, `__import__` -> symbol producer.

The required order is:

1. Ordinary lexical/class/module binding lookup.
2. For an absent module name, classified-table lookup.
3. Only for a matched table entry, read and gate the executing frame proof.
4. Only after a true proof, select the classified producer kind and construct the existing value.

An unmatched absent name must retain the existing unresolved/`NameError` behavior. An implementation that checks the frame proof for every absent module name would blanket-refuse unrelated unresolved names. A real lexical, class, or module binding wins before this table, even when its spelling is one of the six names.

The explicit gate reads only the executing frame proof. It must not re-run the creation helper. The sole `_CExceptionType(...)` producer must remain behind the exception-kind branch, and the two symbol producers must remain behind the symbol-kind branch. Checkpoint 3 must extend this same table with `range` and `sum`; E1 must not implement those producers early.

## Implicit builtin consumer hooks

The current admitted implicit inventory is complete:

- each admitted `ClassDef` consumes captured `__build_class__`;
- each `Import` alias consumes captured `__import__`;
- each admitted nonrelative, nonstar `ImportFrom` statement consumes captured `__import__` once.

These paths must share one central implicit frame-proof predicate/gate. It reads only `frame.builtin_fallback_proved`; it takes no authority from module membership, an explicit `__build_class__`/`__import__` binding, or `_c_read_name`.

### Import branch refactor

The held source combines `Import` and `ImportFrom` at 10565-10591 and currently loops per alias for both. The repair must preserve the existing symbol and store effects while distinguishing opcode frequency:

- `Import`: gate inside the alias loop for each normal predecessor, before computing the qualified symbol, constructing `_CAtom`, or calling `_c_store_name`. Earlier completed aliases retain their ordered effects if a later real import operation refuses.
- admitted `ImportFrom`: retain the existing relative/star refusal boundary, then gate once for the statement before creating or binding any imported alias. A multi-name from-import must not gate once per alias.

Because `_c_statement` is called separately for each normal incoming predecessor, a single statement-level `ImportFrom` source gate has the required runtime frequency. A false class/import gate returns the existing conservative refused outcome and performs no base, body, class-name, symbol, alias, or binding effect.

## Work-accounting hooks

All additions remain on the existing `_AnalysisBudget`. The following aggregate constructor changes are the minimum retained-field deltas:

- `_CFunction` at 10767: current `consume(6)` for allocation plus five fields becomes allocation plus six fields, normally `consume(7)`.
- class `_CFrame` at 10805: current `consume(7)` becomes allocation plus seven fields, normally `consume(8)`.
- invocation `_CFrame` at 10940: current `consume(7)` becomes allocation plus seven fields, normally `consume(8)`, and the new read of `record.builtin_fallback_proved` must also be explicitly accounted unless an adjacent charge explicitly owns that read.
- module aggregate at 11388: current `consume(10)` includes the initial frame's six-field aggregate and becomes `consume(11)` when the frame retains the seventh field.

Creation-helper accounting must include:

- the namespace/object read already performed through `_c_namespace`/`_c_object_read`;
- exact module-membership work;
- the executing-frame proof read only on the absent-member branch.

Explicit fallback accounting must include:

- a classified-table lookup for every absent module name;
- the matched frame-proof read/decision only for a table match;
- the producer-kind decision only after a true proof;
- the existing value, object, refusal, outcome, issue, and trace work separately.

Implicit accounting must include:

- the class frame-proof decision before any class-body creation or base work;
- the separate class creation-helper operations;
- one import frame-proof decision per real `Import` alias;
- one import frame-proof decision per admitted `ImportFrom` statement.

A false gate must not charge skipped base, body, class installation, symbol construction, alias binding, or producer-kind work. Carrying the cached class proof as a plain local scalar needs no fabricated persistent-storage charge; any actual tuple, record, or reference introduced to carry it must be charged.

No caps, reserves, epochs, exception behavior, or budget type change follows from this repair. The successor must report its exact raw `SequenceMatcher(autojunk=False)` delta against the held source and add it to the existing R2 cumulative 360/1500 count.

## Post-implementation static invariants

Before any runtime dispatch, a source reviewer should establish all of the following directly:

1. `_CFunction` and `_CFrame` each have one required `builtin_fallback_proved: bool` field with no default.
2. The constructor census remains exactly one `_CFunction(...)` and three `_CFrame(...)` calls.
3. The four frame/function providers are exactly: ordinary creation-helper result, cached pre-base class result, selected function-record proof, and module literal `True`.
4. The current creation-helper call census is exactly two; both use the exact reached state and executing frame.
5. The creation helper uses exact module-member presence and never class/local lookup, value truth, a name route, or a poison bit.
6. The implicit gate has exactly three current source call sites: class, per-alias `Import`, and per-statement `ImportFrom`.
7. The implicit predicate reads only the executing frame proof. It has no state/current-module predicate and does not call `_c_read_name`.
8. The class implicit gate and class-body creation helper both dominate base evaluation; the helper result is outside the base loop and supplies every class frame.
9. A false class gate dominates base evaluation, namespace creation, body execution, and class-name installation.
10. Each `Import` gate dominates its qualified-name calculation, symbol production, and store. The single admitted `ImportFrom` gate dominates every alias, with no duplicate per-alias proof read.
11. Relative/star from-imports preserve their existing unsupported boundary and gain no execution claim.
12. The immutable explicit fallback table contains exactly the six current names and two classified kinds.
13. The table lookup occurs only after an absent ordinary module binding; unmatched names do not read the frame proof.
14. The sole `_CExceptionType(...)` construction and both explicit symbol producers are reachable only through the matched, proved table branch.
15. A real explicit binding wins for explicit name lookup but cannot satisfy an implicit class/import gate.
16. False provenance alone does not refuse dormant function or class-contained definitions; refusal occurs only at a reached explicit or implicit builtin consumer.
17. Function invocation never reads current module membership or caller proof to establish callee authority.
18. No new `_CState`, `_CView`, namespace, outcome, issue, trace, call-observation, or parallel authority-map field exists.
19. Every new helper call, read, membership test, comparison/branch, allocation, retained field, issue, outcome, trace, and installed reference has source-site accounting; skipped work is not charged.
20. The baseline binder, protected set, caps, public envelopes, original case bytes, and retained source/watch invariants remain unchanged outside the authorized E1 surface.

## Audit limits and actions not performed

This is static source/design evidence only. It does not establish fixture correctness, pre-fix RED, implementation correctness, work-cap fitness, interpreter parity, or candidate acceptance.

No repository source, design, handoff, input, harness, test, Model, manifest, snapshot, or generated artifact was imported, executed, or edited during this audit. No analyzer, test suite, payload, or Model was run. This memo is the only file created by the audit-recording step; `D:\Pontius-handoffs` and the held source were not touched.
