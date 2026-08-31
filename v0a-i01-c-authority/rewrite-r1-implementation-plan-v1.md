# R1 Canonical Analyzer Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. One source writer; the coordinator owns setup, source approval and every payload dispatch. Checkboxes record future work, not work already executed.

**Goal:** Run the fixed six Gate A public analyses through one canonical object/cell/frame engine, retaining the frozen classifications and public evidence schema.

**Architecture:** Replace the live path from module construction through unittest entry, local helper execution and terminal sink observations. Immutable scope facts are shared; successor states own canonical records and preserve ordered alternatives. Existing scalar policy/receipt helpers receive only terminal detached evidence.

**Tech Stack:** CPython 3.11-compatible stdlib, AST data, dataclasses, ordinary owned dictionaries and tuples inside tools/generate_test_inventory.py. No new module, package, dependency, Mapping adapter or persistent-tree backend.

**Spec:** Frozen H commit fc7870b6f5e4c77c2efce8339377d13daeeb1bb4 in D:/Pontius-handoffs; design manifest 18fdd632f5eeb3f414ac9e5160b9b276ef9dca0830f60ae13ca1f774b78dd55f. Binding files: rewrite-design-v1.md, rewrite-scope-clarification-v1.md and rewrite-early-population-v1.json. Their current bytes were compared to the H blobs before writing this plan.

## Global constraints

- Plan only now. Candidate source authoring starts only after root approves this plan and the exact r010 RED evidence. This document grants no payload or commit authority.
- Sole candidate file: D:/Pontius-worktrees/codex-v0a-i01-c-core-v1/tools/generate_test_inventory.py. Root prepared branch codex/v0a-i01-c-core-v1 from clean r010 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358. No v25/v30 overlay; held v31 is not an input.
- Retained baseline T/rewrite-r1-base-generator.py SHA256 29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692; r010 manifest 8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb.
- T means D:/Pontius-handoffs/v0a-i01-c-authority. Root owns test/controller/generated-file writes. This plan changes no test, expectation, inventory, profile, other production path or main checkout.
- First attempt stops at 2500 added-plus-deleted implementation lines relative to r010, before further expansion. Report pure deletions separately; they do not buy extra lines. No reformatting to hide size.
- Keep _AnalysisBudget.__init__/consume, all five caps, binder signature algorithm, public API/schema, terminal receipt/capability policy, boundary/CI and native publication code unchanged. Caps remain work262144, helper64, child4, container4096, cardinality2147483647.
- Gate A records all epochs under those caps. Gate B's adopted196608 engineering ceiling is a later continuation test, not an R1 admission rule.
- Sensitive fixture source remains AST-only. Root runs reviewed controls in fresh D-local r010 snapshots: actual3.11.15 first, then identical bytes on3.14.6, source/controller pins, scrubbed environment/Git, full before/after custody. No source writer executes payloads.
- No fixture IDs, source hashes, known line numbers, expected argv strings or pack classifications drive analyzer behavior. Unsupported reached syntax explicitly refuses; no fallback to the old engine. Intermediate R1 is not integration-ready.

## Fixed test contract and RED requirement

Gate A is six public analyses and eight independent harmless Model projections, using the manifest's two exact public envelopes, no larger original test envelope or child probe:

| Case | Required result | R1 mechanism exercised |
| --- | --- | --- |
| shared-list-consumed | Explicit blocker | Two formals share one list; append captured-default callable; read through the other alias; invoke it. |
| shared-list-dormant | Clean, exact argv [-m,fixed] | Same store without executing the stored callable. |
| class-adoption-unsafe | Explicit blocker | None -> class owner through a nonlocal setter in a class body; subsequent closure reads the current cell. |
| class-adoption-safe | Clean, exact argv [-m,outer] | Owner -> None; class-local module=inner cannot leak; readonly reader must not be blanket refused. |
| hidden-cell-joined-reached | Explicit blocker | Returned reader/setter references, one activation cell and unknown choice. |
| hidden-cell-joined-dormant | Explicit refusal permitted; otherwise exact clean [-m,fixed] | Same references/branch effects with the reader dormant. |

The hidden pair permits refusal of optional effective tuple-result precision.
Passing it alone does not prove precise joined-cell execution. R1 will implement
ordinary tuple return and branch alternatives because they fit the canonical
path, without strengthening either expectation. The receiver's absent
self.choice fact is unknown under admitted unittest entry, not a proved
AttributeError or a closed-instance absence.

Root first runs the unchanged r010 bytes for these exact six/eight, retains each
result and all budgets, and approves the baseline. Do not assert all six are RED:
previous v19 or v23 receipts are not r010 evidence. Infrastructure failure is not
semantic RED. The source writer then receives an approved exact baseline receipt
and a source GO; neither is presumed by this plan.

## Concrete internal contracts

All new names use the _C prefix except the public-path _process_review_rows
replacement. dataclasses holding semantic records use eq=False; comparisons and
ordered unions use explicit, charged scalar/reference keys, avoiding recursive
implicit record equality.

The implementation types are:

| Type | Fields and representation |
| --- | --- |
| _CAtom | kind: literal/symbol/unknown/unbound; data: immutable exact scalar or qualified symbol string; reason: optional string. Never stores AST-based live values. |
| _CRef | object_id:int. Object IDs are allocated by one _CArena for the entire public analysis. |
| _CChoice | alternatives:tuple[_CAtom or _CRef,...], flattened, ordered and explicitly deduplicated. Missing/unbound alternatives cannot be dropped. |
| _CCellRef | activation_id:int, name:str. Only a function activation's declared local allocation creates these. |
| _CScope | node, path, kind, ordered local names, parameter names, globals, nonlocals, ordered free routes, child scopes, direct call/store source sites. Immutable syntax/classification only. |
| _CCapture | kind:cell/module/unresolved; cell:_CCellRef or None; module_ref:_CRef or None; name:str; reason:str or None. |
| _CFrame | scope, activation_id or None, captures:dict[str,_CCapture], module_ref, class_namespace or None, enclosing_nonclass frame or None. No copied ambient values. |
| _CCellBank | declared scope identity, values:dict[name,_CValue], write_token. Storage ownership token is not lexical proof. |
| _CFunction | template:_CScope, defaults:tuple[name,_CValue], captures:tuple[name,_CCellRef or unresolved/module route], descriptor kind:ordinary/staticmethod, body kind:plain/unsupported-deferred. |
| _CBound | function:_CRef, receiver:_CValue. Attribute binding allocates this record rather than changing the shared function. |
| _CNativeMethod | receiver:_CRef, operation:str; holds the already-selected receiver. |
| _CSequence | kind:list/tuple, elements:tuple[_CValue,...]. Mutating a list replaces its current record; no value contains old embedded list contents. |
| _CNamespace | kind:module/class, members:dict[name,_CValue], class/module origin. Member dictionaries are owned record contents, never mutated behind a retained view. |
| _CInstance | class_ref:_CRef, open_entry:bool. R1 unittest instances are open; absent ordinary receiver facts yield unknown. |
| _CEnvironment | inherited:bool, additions:tuple[str,str], removals:tuple[str,...], unresolved_reason. Bounded abstract policy; never reads os.environ. |
| _CState | cell_banks and objects as two typed COW tables, write_token, version. Frames are explicit parameters, not name projections. |
| _CView | Read-only cell/object table references and version; no budget/resolver object. Created by revoking the current write token. |
| _CIssue | source node/path, reason and typed category; every reached issue remains attached to its outcome. |
| _CTrace | kind:empty/event/sequence/alternative; children:tuple[_CTrace,...]; event:call/sink/issue observation or None. Immutable and acyclic. |
| _COutcome | state, result, control(normal/return/raise/refused), exception_tag, explicit, excluded_handlers, issues, trace:_CTrace. |
| _CCallObservation | source call, selected callable/bound receiver, evaluated argument/default references, entry frame/view, tagged result/effects. |
| _CSinkObservation | Original source attribution plus fully detached exact scalar/container evidence, helper context and branch occurrence key. No live references. |
| _CArena / _CContext | Arena owns only the monotonic identity source. Context owns program facts, the existing budget, item/path/helper context and call stack. Forks never copy the allocator. |

_CValue is _CAtom | _CRef | _CChoice. Object records form a closed union of the
record types above. An unsupported operation cannot discard a reference into a
harmless unknown: return an explicit refused outcome and retain the originating
state/issues. R1 does not implement generator resumption; callable construction
can retain an unsupported body without executing it, while invocation outside
the declared subset refuses.

Canonical operation signatures (the context always supplies an existing budget):

```python
_c_program(parsed: Mapping[str, ast.Module],
           certificate_budgets: Mapping[str, _AnalysisBudget]) -> _CProgram
_c_read_name(ctx: _CContext, state: _CState, frame: _CFrame,
             name: str, site: ast.AST) -> tuple[_COutcome, ...]
_c_read_member(ctx: _CContext, state: _CState, receiver: _CValue,
               member: str, site: ast.AST) -> tuple[_COutcome, ...]
_c_read_element(ctx: _CContext, state: _CState, receiver: _CValue,
                index: _CValue, site: ast.AST) -> tuple[_COutcome, ...]
_c_store(ctx: _CContext, state: _CState, frame: _CFrame,
         target: ast.expr, value: _CValue) -> tuple[_COutcome, ...]
_c_delete(ctx: _CContext, state: _CState, frame: _CFrame,
          target: ast.expr) -> tuple[_COutcome, ...]
_c_construct_function(ctx: _CContext, state: _CState, frame: _CFrame,
                      template: _CScope) -> tuple[_COutcome, ...]
_c_call(ctx: _CContext, state: _CState, frame: _CFrame,
        call: ast.Call, selected: _CValue,
        arguments: tuple[_CValue, ...],
        keywords: tuple[tuple[str, _CValue], ...]) -> tuple[_COutcome, ...]
_c_eval(ctx: _CContext, state: _CState, frame: _CFrame,
        expression: ast.expr) -> tuple[_COutcome, ...]
_c_statements(ctx: _CContext, initial: _COutcome, frame: _CFrame,
              statements: Sequence[ast.stmt]) -> tuple[_COutcome, ...]
_c_fork(ctx: _CContext, state: _CState) -> _CState
_c_snapshot(ctx: _CContext, state: _CState) -> _CView
_c_join(ctx: _CContext,
        alternatives: Iterable[_COutcome]) -> tuple[_COutcome, ...]
_c_emit_sink(ctx: _CContext,
             observed: _CSinkObservation) -> tuple[dict[str, object] | None,
                                                   str | None]
```

_CProgram contains modules:dict[path,_CScope], scopes:dict[AST identity,_CScope],
signatures:dict[AST identity,_ReviewFunction] and source_sites keyed by scope.
These are immutable module/scope facts and template-only binder descriptors. It contains no current class member
claim, helper-return value or resolved live callable cache.

### State ownership, alternatives and time

Use ordinary dictionaries with an internal table wrapper carrying data and a
write_token; it implements no Mapping compatibility API. Fork/snapshot shares
the table pointers and revokes the writer's token. Before mutation, copy a shared
outer table and, for a cell write, the affected activation bank. Charge every
copied entry. Unique token ownership permits subsequent in-place table/bank
updates; immutable object records are replaced. Do not copy all ambient names
at function entry. Object-table detachment can still be expensive: measure it,
do not hide it or add a backend in R1.

R1 join is the ordered tuple of tagged successor states. It does not create a
generic merged heap or flatten state/result pairs. Subsequent statements execute
on each normal successor; return/raise/refused successors bypass later statements.
Coalesce only the same outcome object or a fully proved identical representation,
not equal-looking values. Charge tuple creation/reference visits. No new path cap
or budget reset; existing work/cardinality limits bound expansion. Root accepted
this limited exact-path representation for R1; it proves no wider correlation
contract.

Arena allocation is monotonic across all branches and factory calls. A branch
copy cannot reuse another activation's cell identity. Old callable aliases retain
their capture references, and an empty/currently irrelevant cell remains live.

Capture callee before arguments, evaluate each argument once in order, then bind
and read closure contents against the resulting state. Defaults retain the
reference captured at construction, not a copied object. Native methods retain
their originally observed receiver; later operands cannot replace it by a fresh
name lookup. Tuple unpacking snapshots outer element references before target
stores. Historical views are never patched or used to hydrate the current state.
A call observation retains control/value/post-view/issues summaries, not a whole
outcome that recursively contains that observation's own trace.

## Task 1: State primitives and the operation ledger

**File:** candidate generator only. **Budget:** approximately360 implementation lines.

- [ ] Add the types above and explicit allocation/table helpers beside the analyzer support region. Keep _AnalysisBudget and cap definitions byte/AST unchanged.
- [ ] Implement scalar/reference comparison keys with exact types; ordered choices preserve unknown/unbound. Do not compare nested records using dataclass equality.
- [ ] Implement arena allocation, fork, snapshot, table detachment, cell read/write and object record replacement. Every charge precedes publication of the resulting semantic mutation.
- [ ] Add the static new-work ledger to the eventual handoff, mapping each helper to the charges below. No instrumentation-only counter is substituted for _AnalysisBudget.consume.
- [ ] Root inspects state ownership and allocator invariants before their use in evaluator code; this is a source checkpoint, not a primitive payload.

## Task 2: Stable scope facts and lexical destinations

**File:** candidate generator only. **Budget:** approximately330 lines.

- [ ] Implement one metered scope traversal using the existing lexical-classification rules. Direct scope loads/stores exclude nested bodies; nested defaults/decorators are visited in their evaluating scope.
- [ ] Compute child free routes bottom-up. Forward free/nonlocal needs through functions, subtract the current function's declared locals/globals correctly, and preserve current-scope global barriers. Class children use the enclosing nonclass routes rather than class locals.
- [ ] At function activation allocate a bank containing every declared local (initially unbound), fill parameters with the selected values, and install only the callable's captured destinations. Never inherit unrelated caller bindings.
- [ ] Resolve local, capture, class-slot and module routes explicitly. Missing lexical destinations remain unresolved. Ordinary module symbols retain existing read behavior; global writes outside supported precision refuse.
- [ ] Class deletion uses class slots, not lexical cells. Function nonlocal writes require an actual captured cell; cell-table membership alone supplies no proof.
- [ ] Carry the frozen comprehension clarification in coverage: R1 refuses reached comprehension execution; later migration must give comprehension targets their own implicit frame, first iterable in the surrounding frame, and free lookup skipping class locals.

## Task 3: Finite source-order evaluator and tagged control

**File:** candidate generator only. **Budget:** approximately560 lines.

- [ ] Implement Constant, Name, Attribute, List/Tuple, the inherited-environment Dict shape, integer Subscript, Call, and the needed exact None identity/boolean conditions. General unsupported expressions return a typed refusal at the reached node.
- [ ] Implement Assign (including tuple unpack), Expr, Return, Pass, FunctionDef, ClassDef, Nonlocal/Global declaration routing, Delete through the same destination API, If and supported known call failures. Unsupported loops/Try/TryStar/comprehensions/async/child-program execution refuse rather than enter the old resolver.
- [ ] Unknown unittest receiver attributes such as self.choice split feasible boolean successors; do not infer lookup failure from an absent receiver fact. Literal false blocks do not evaluate their bodies.
- [ ] Every sequence operation pairs its result with the successor that produced it. Earlier argument/default effects survive later call failure. A known call to None produces the known TypeError successor; analysis-unsupported refusal is a distinct control value, not an invented Python exception.
- [ ] Read list contents through the current object record after operand effects. append updates that record once. Assigning the same list to two formals passes one reference. Merely storing a callable does not inspect/execute its body.
- [ ] Preserve candidate-independent source-site and outcome evidence. Sequential effects count in sequence; branches are alternatives, not repeated execution. The trace representation keeps this distinction for emission.

R1's deferred coverage is ordinary callable creation/storage versus invocation.
There is no promised generator/comprehension completion, explicit handler/finally,
cross-file helper or multiple-factory coverage from Gate A.

## Task 4: Construction, calls and class/entry frames

**File:** candidate generator only. **Budget:** approximately480 lines.

- [ ] Construct functions from their templates, evaluating defaults and supported decorator expressions in source order. R1 admits ordinary functions and the existing staticmethod case; custom descriptor/decorator effects explicitly refuse. Bodies are not executed at construction.
- [ ] Call the same _bind_helper_arguments algorithm at r01023210 with proven_bound explicitly True or False, supplied by the selected canonical callable/bound record. Its output AST identities select already evaluated argument values or captured defaults by parameter. Never evaluate those AST nodes again or run _helper_is_bound on spelling.
- [ ] Preserve binder rejection semantics: unsupported signature/call shape refuses before body execution; definite fixed-signature argument errors are failed calls, not successful unknown results. Arguments have already had their proper effects.
- [ ] Invoke local/helper bodies once under a new activation/frame, sharing the caller's existing body budget. Pair return values with their current states; retained cell banks survive activation return when referenced.
- [ ] Allocate a class namespace for body execution, separate from enclosing function cells. Module-level unittest.TestCase construction and ordinary nested classes use canonical class records; supported method/staticmethod bindings install in order.
- [ ] On normal class completion install its owner reference; on raised/refused completion do not install it or evaluate later body statements. Both routes retain outer cell/object effects and discard class-local bindings.
- [ ] Bind the selected unittest method through the canonical class. Its open receiver supports ordinary unknown attributes; supported class member choices come from the current class record. Preserve entry-signature admission without _unittest_receiver_attributes running the old resolver.
- [ ] Attribute stores to a proved protected helper/class member update the current canonical record and emit the typed reached namespace-write issue. This happens on invocation, not while constructing the mutator. A safe nonlocal cell write is not automatically such a namespace issue.

## Task 5: Replace the full public execution path and emit detached rows

**File:** candidate generator only. **Budget:** approximately380 lines, leaving390 lines of the2500 attempt budget for necessary glue and review corrections.

- [ ] Preserve derive_design_review and pure parsing/inventory-selection rules. Rename the existing _process_review_rows implementation as an explicitly unreachable legacy body and install the canonical implementation under the original name. No conditional dispatch to the legacy body. Keep the old core as uncalled migration residue only; R3 removes it.
- [ ] Use the canonical module construction pass instead of _definition_time_protocol_resolver, _module_protected_namespace_mutations and live _definition_time_blockers execution. Import-time calls use the same core and unowned import-time refusal policy. Imports are symbol facts, never actual Python imports.
- [ ] Build immutable scope/template facts instead of current-value _review_function_registry certificates. Preserve duplicate-definition and unsupported entry checks; constructor/member decisions are current state, not the registry.
- [ ] Replace entry preflight's resolver execution, _source_ordered_helper_return, _source_ordered_review_flow and all recursive _review_body execution on this path. Module/fixture/probe/test entries unsupported by the R1 syntax subset get explicit owned blockers, not old-engine output.
- [ ] Create a call observation at each actual invocation and final sink observation at the sink source point. Reporting never reexecutes a helper or reconstructs entry values from names/default AST.
- [ ] Implement source-site dispositions from independent scope facts plus canonical outcomes: row, blocker, proved unreachable or proved nonsensitive. Every reached sensitive site must be present in the static site set; undisposed feasible sites produce an explicit blocker/error, never silent omission. Do not reuse a preclassifier's live name state.
- [ ] For an exact admitted subprocess observation, reject any argv containing -c with the R1 unsupported-child blocker BEFORE calling the existing process policy. Convert only detached exact literals plus canonical sys.executable spelling to an emission AST; pass empty live assignments and an explicitly captured environment triple. An empty _ExecutionScopeVisitor may supply the unused parameter, but it never visits a body. Pass the existing body budget explicitly.
- [ ] Reuse _process_definition only along its verified non-child branch. Unknown argv/env/cwd/callable evidence refuses before conversion. No ObjectRef, cell, frame, FlowValue or old alias projection crosses this boundary. The returned dictionary is used only for final rows; it never returns to evaluation.
- [ ] Reuse _review_blocker, _capability_id, _normalise_review_rows, scalar sorting and derive_design_review receipt/census/digest code. Preserve source/helper attribution and deny_all.
- [ ] Aggregate identical branch-alternative sink occurrences with maximum feasible count; sequential occurrences add. A call occurrence key is its source/helper invocation path, not a newly allocated object ID. Conflicting alternative subprocess definitions explicitly refuse under the existing representability policy. Do not sum two alternative paths into two runtime calls.
- [ ] Produce an exact static call-edge inventory proving the public path cannot reach _SourceOrderedResolver, _review_body, live helper-return/preflight, or _process_definition's child branch. Record any unconverted private caller as unreachable from the new entry, not as converted source.

The one-way terminal AST is evidence serialization only. The allowed boundary
does not permit reconstructing executable helper inputs as literal AST.

## Required legacy seam inventory

All anchors are r010, not v25:

| Existing entry | R1 replacement |
| --- | --- |
| _process_review_rows25677; module setup25739-25776 | Canonical orchestration, ProgramFacts and module construction. |
| _definition_time_protocol_resolver25023; _definition_time_blockers25095 | Same canonical evaluator in module/unowned context. |
| _review_function_registry22851/certificate budget22860 | Immutable scope/template facts; no live binding certification. |
| _unittest_receiver_attributes25461; preflight25491/25936 | Canonical open receiver and scope/descriptor admission; keep preflight budget. |
| _ReviewFlow12338; _snapshot_call15747 | _CCallObservation and tagged traces, no live value/alias maps. |
| _review_body24106/recursive24629,24764 | _c_call and _c_statements once, same body budget. |
| helper-return22501; source-flow22544 | No semantic bridge/call from the new path. |
| _bind_helper_arguments23210 | Same signature algorithm, reference selection and existing-budget metering only. |
| _merge_states20656; expression15953; statement20927/20977 | COW fork/view plus ordered tagged outcome join. |
| _process_definition23584 | Terminal non-child policy only; all live/child paths excluded. |
| normalize25177; sort25977-26007; derive26165 | Pure output policy/schema retained. |

## Operation-accounting map

The existing budget class is the sole production meter. No optional budget
fallback on a new operation, side epoch for a recursive helper, reset, refund or
cost discount. Context is replaced only when entering an original owner/stage.

| Original owner/stage | R1 placement |
| --- | --- |
| Per-source definition protocol budget25031 | Canonical eager module/class construction and reached definition expressions. |
| Per-source certificate budget22860 | Metered static scope/free-route/template construction. Share resulting facts; charge actual creation once, not repeated nonexistent work. |
| Per-selected-method preflight budget25943 | Canonical signature/descriptor/open-receiver entry checks. No body execution just to discover receiver names. |
| Per direct body/probe/fixture budget24130 | Its canonical activation and all nested helper calls, argument binding, state changes, observations and terminal policy. |
| Resolver/source-flow fallback13895/22584; sink23599; bounds8232/8409 | New path always passes its owner budget; no fallback budget is created. Reused pure routines receive it explicitly. Root traces creation owners, not old ordinal epoch numbers. |

Retired redundant old walks are not executed for artificial charge parity.
Their actual semantic replacement work is charged in the matching stage. Any
necessary ownership consolidation must be disclosed to root; this plan does not
authorize silently splitting work into more epochs.

Charge before the corresponding allocation/copy/visit:

- AST/scope/capture/site traversal: consume1 per visited node/edge/name; result
  allocation and retained references are additionally charged. No unmetered
  repeated raw AST walk for capture proof.
- New arena identity/record/frame/outcome/view/table: consume1 per allocation;
  consume1 per retained field/element reference actually installed.
- Name/cell/object/member lookup or mutation: consume1 per table operation.
  Copying n dictionary entries charges n visits plus n installed references and
  the table allocation; cell-bank detachment charges that bank separately.
- Tuple/choice/native contents: container(n) for the existing size rule and
  element installation, plus actual read/compare/union visits. No duplicate
  charge for the same installation under two ledger categories.
- Fork/snapshot: charge fixed new view/state/reference work and token rotation;
  do not enumerate values. Later COW detachment pays the actual copy.
- Join/trace aggregation: charge each visited successor/event/key comparison,
  each resulting retained reference, and actual cardinality arithmetic using the
  unchanged checked helpers. No deep implicit equality.
- Binding: propose optional analysis_budget keyword plumbing in the existing
  matcher, mandatory from the new core. Insert consume calls for existing
  formal/actual/default visits and existing list/set/dict/tuple construction;
  preserve every matching branch and selected result. Removing only metering
  statements/parameter must reproduce the r010 algorithm AST. Old private
  callers may retain their original default, but the new path cannot omit the
  budget. Root approval of this plan must explicitly include this mechanical
  metering delta; no copied matcher or invented flat matching charge.
- Sink conversion: charge each value/element read, detached literal/AST/metadata
  allocation and copied environment/reference, then retain _process_definition's
  own existing consume. No hidden preprocessing.
- Failure: keep every actual request through refusal, including the request that
  exceeds a cap. A noncharging depth check acquires no fabricated charge.

Before source issuance, the ledger names the concrete helper and charge sites;
the controller reports every budget's initial/requested/final values, maximum,
sum and owner/stage. R1 does not claim COW is fast. Gate B may reject this physical
representation before broad migration.

## Minimal approval, RED and GREEN sequence

- [ ] Root inspects this plan, category review and frozen inputs; disposition
  binder metering-only plumbing, terminal-only reuse and budget owners before source edits.
- [ ] Root dispatches the reviewed fixed Gate A controller against exact retained
  r010 on3.11.15 then matching3.14.6. Preserve all six analyses/eight Models,
  fixed labels, raw failures and all budget epochs. Record actual case-level RED
  and preexisting passes; do not relabel a permitted refusal.
- [ ] On explicit source GO, execute Tasks1-5 in the prepared clean worktree.
  After each task, inspect only source/static deltas; no author payload.
- [ ] Stop before2500 changed lines. Retain immutable candidate bytes, exact
  r010 diff, public-entry/read/write/call/return/census category map, new-work
  ledger, static allowed-node preservation and the unchanged-test/cap/native-writer and normalized binder-algorithm
  checks. Root inspects the whole source before dispatch.
- [ ] Root runs the same Gate A population/controller conditions on that exact
  candidate floor first then dev. All Models must complete with fixed traces;
  no analyzer/infrastructure error is a semantic pass. Required-clean outputs
  must be exact and blocker-free; unsafe cases need explicit blockers.
- [ ] Compare source-bound case records and all budget owners to RED. Separate
  semantic result, control completeness and cost. A green hidden pair does not
  establish precise joined execution, and a blocker does not prove the sensitive
  body actually ran. No result-driven expectation changes.
- [ ] On failure, retain the exact attempt and diagnose from its source/evidence;
  no quiet candidate replacement or gate weakening. Gate A success permits only
  the next root-reviewed R2 plan/Gate B work, not broad corpus or release claims.

No new tests, witness families, commands against a source checkout, or ceremonial
commit are steps in this plan. Root owns the fully pinned controller invocation.

## Pins and engineering limitations

- rewrite-design-v1.md:701552c177840e4c5c0dd9c5985776256af5b31e7e997067dd662638a67c3ca8.
- rewrite-scope-clarification-v1.md:2e699aaf3b520539eca38233b1a758cbdefcdf67fea86aaa54a7699f926ea8c1.
- rewrite-early-population-v1.json:3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce; this pins every source/Model/expected record and envelope.
- rewrite-r1-category-review-v1.md:f04eedf4de32550cb3d4e02e310eeed85f5963ba4621ea7de430b8cae125522a.
- storage-composition pack:faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709.
- name-environment pack:d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c.

This plan was prepared from static source and metadata, including the complete
r010 public entry/binder/process policy seams. No baseline or candidate payload
was run by this author. Fixed52, matrix192/212, accepted A/B, full design/corpus
and later exception/comprehension/child contracts remain later binding gates.
The physical COW cost, implementation fit within2500 lines and real Gate A
behavior remain unproved until the prescribed evidence exists.
