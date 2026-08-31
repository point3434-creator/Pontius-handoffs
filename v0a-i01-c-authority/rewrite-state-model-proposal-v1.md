# C core replacement: authoritative state proposal v1

2026-08-31. Engineering design only, not implementation, an issued candidate,
cold review, or runtime evidence. Prepared for the coordinator's chosen partial
replacement. No production/test edits, new fixtures, analyzed-source imports, or
payload execution were performed. v31 remains unfinished, held scratch.

## Decision and preservation

Supersede Stage0's choice to retain legacy abstract values as an independent
semantic representation plus a separate authority payload. Keep Stage0's
behavioral requirements. Replace the live state/effect core, not merely its map
backend. Preserve parser/discovery, accepted A/B, argument binding, capability
schema/digest, exception partitions, all five limits, boundary/CI checks and the
native writer. Reusable scalar/descriptor logic remains only after its interface
cannot carry a second copy of live object contents or closure state.

The smaller patch alternative preserves the demonstrated synchronization burden.
A whole-generator rewrite would disturb unrelated working boundaries. This
proposal replaces the authority-bearing value model and its evaluator seams;
it does not add a general Python interpreter or general class heap precision.

## One canonical model

Use immutable ProgramFacts plus one State per execution successor. ProgramFacts
contains scope classifications, source ordering, callable templates, binding
rules and existing descriptor/provenance facts; share it across activations.
Do not reconstruct all ambient names at helper entry.

A Value is an immutable atom, an ObjectRef, or an ordered choice of Values.
Atoms cover the existing exact primitive/symbol semantics, including ordinary
imported/module reads. Unbound and unresolved alternatives are explicit. Exact
scalar type distinctions remain unchanged. No Value embeds a second mutable
collection, copied closure contents, or independent helper-authority payload.

State has typed frames, lexical cells and object records. These are parts of
one state, not mutually repairing stores:

| Component | Canonical contents |
| --- | --- |
| Function frame | Scope identity and local/captured binding destinations. Each activation allocates its own lexical cells; a callee receives only its callable's captures plus its own parameters/locals. |
| Cell | Current bound/unbound/maybe-bound Value. A cell's lexical ownership comes from activation allocation, never from an arbitrary store entry or a nonmissing value. |
| Callable record | Template, definition-time defaults, captured cell identities, bound receiver and existing invocation support facts. Capture completeness and lexical write proof are separate. |
| Collection record | Current exact sequence/mapping contents, or explicitly opaque contents with retained possibilities; mutation/progress facts where the existing generator policy needs them. Every alias refers to this record. |
| Class execution frame | Separate class namespace slots plus an enclosing nonclass lexical frame reference. Class slots do not confer lexical-cell ownership. |
| Completed class record | Stable owner identity and existing admitted member/descriptor facts, with named member dependencies and read-only base-owner links. Keeping a dependency does not grant positive general member, MRO, metaclass or descriptor precision. Immutable descriptor syntax can be shared; current member/override choices come only from this state. |
| Deferred record | Existing generator/factory plan, captured frame/cells, captured first iterator, progress/remaining/closed facts and explicit unsupported effects. It is an object even when presently harmless. |
| Opaque object/result record | Retained alternatives or contents whose exact shape is unavailable. Edges distinguish possible object alternatives, contained elements, captures, named members and bases. Loss of shape never means loss of dependency. |

Represented classes receive their owner identity on normal construction, before
aliases escape, including initially empty classes. Known classes available only
as unresolved module/prepass symbols retain explicit class origin without
inventing alias identities. Their obligation-bearing namespace stores take the
frozen conservative refusal boundary; ordinary scalar stores and global reads
retain their old behavior. No blanket refusal for represented dormant storage.

Scope resolution is explicit. Function global declarations are barriers to
forwarding an older lexical cell. Nested callable free/nonlocal analysis uses
scope-aware infrastructure, including intermediate factories. Method bodies
skip class locals. Class reads distinguish a local slot's bound/maybe-unbound
state from enclosing/module fallback; deletion reveals fallback, and joins retain
both feasible routes. No value-identity heuristic or unioned shadow-name set.
Direct class global writes retain the required conservative policy; proved
nonlocal destinations use current lexical cells.

Constructing a later method imports ownership, not old cell contents. Class
namespace/frame identity persists through If/Try/finally. All outward exits keep
outer object/cell effects and caller observations while discarding class-local
bindings. Only normal completion installs the completed class. Preserve existing
explicit/call-raised successor partitions; do not promise correlation already
merged by the current helper completion rules.

## Small explicit API

These are semantic operations, not a required public Python interface. Each
operation receives the existing operation budget and returns tagged outcomes
carrying state, result and accumulated issues.

| Operation | Obligation |
| --- | --- |
| read(state, frame-or-value, selector) | Resolve a name, cell, element or member through the current state. A missing managed record is unresolved, never an unmanaged exact fallback. |
| write/delete(state, destination, value) | Update the one record. Strong writes require a single proved destination; alternate/missing destinations retain weak effects and uncertainty. Extract before removal. |
| construct(state, template, evaluated_inputs) | Allocate the callable/collection/class/deferred object and capture the required references. Evaluate defaults/headers/decorators in their admitted source order; do not execute a body merely to retain it. |
| call/consume/escape(state, selected_value, operation, arguments) | Apply the existing binder and operation policy, then return effects/results/issues. These are distinct operations over the same records, not one flattened sensitivity walk. |
| fork/snapshot(state) | Isolate successor writes; preserve immutable historical evidence. No implicit name-map materialization. |
| join(ordered_tagged_successors) | Merge changed execution facts, object alternatives and cell bindings with missing/unbound evidence intact; preserve exit/exception tags and observable order. |

A native operation reports whether its exact update actually completed; admission
is not completion. One update changes shape and retained dependencies together.
There is no later exact-value recovery from an old record. Native containers
retain both ordinary and marked generators, not just currently sensitive ones.

Immediate iteration of a known tuple/list consumes that container, not a
generator stored as an element. Extraction and yielded elements retain their
references; items/popitem have their actual pair nesting. Captures and named
base links are not immediate iterator alternatives. Unknown escape applies the
existing conservative policy separately. Reached unsupported issues travel in
outcomes through helper completion, syntax iteration, joins and exception paths;
they cannot disappear because a caller ignores the expression's value.

Class member selection follows the requested name and current owner/base records.
Unrelated names stay unrelated. No new shadow/MRO precision is implied; unsupported
selection retains may-alternatives or an explicit reached refusal. Instance
writes do not follow class-base links. Class __dict__/vars projections are not
invented mutable write owners; extracted values still retain their own identity.

Class comprehension headers/first iterables use the class frame; implicit bodies
and targets use the enclosing nonclass frame with current cells. Deferred class
generators retain that distinction, including later consumption in another
helper. Creation, __iter__, unstarted close, invalid arity and proved-empty
nonexecution keep their existing semantics. A mutable iterator's former emptiness
is not permanent proof after mutation. Unsupported deferred precision refuses
when required by the frozen reached contract, not simply at construction.

All new graph work has typed edge dispatch, ordered deduplication and cycle
visits that distinguish object identity and edge role. Ordinary callable
retention remains separate from deferred execution. Do not reintroduce a generic
helper_obligations payload under a new name.

## Time, evidence and analysis modes

Capture the callee reference before argument evaluation, but read its live
closure cells at invocation. Read a previously captured mutable receiver against
the then-current state after relevant operand/protocol effects; never reevaluate
its source expression to find a replacement receiver. Unpacking/star expansion
captures element references at its own language phase; later stores do not
retroactively change already extracted values.

A call observation records the selected callee/bound receiver, evaluated argument
and default references, the call-entry snapshot and tagged result/effects. Recursive public-row review uses this
observation and the same core. It must not rebuild an environment from an old
name projection, replay the helper to obtain a second effect interpretation, or
rehydrate history from the final state. Reporting projections are one-way,
detached outputs; they never re-enter execution.

Definition/prepass modes share ProgramFacts and the typed semantics, not a
second disabled authority representation. Merely discovering a body does not
execute it. Existing definition-expression analysis runs in its proper isolated
state and commits only justified effects. Cached static facts are safe to share;
a live result cache must identify its relevant state dependencies or be removed.
The external helper-return/prepass and unittest preflight entries cannot remain
an alternate engine. Existing _bind_helper_arguments signature rules may stay,
but their runtime transport is canonical references, not reconstructed aliases,
AST literals or copied caller projections.

## Concrete replacement seams

Anchors below are source-text references in frozen v25, not a decision to adopt
v25 as the implementation base. The coordinator's brief chooses a new r010-based
isolated candidate. The replacement includes state-bearing portions of these
seams, not every unrelated statement in their containing functions.

| Existing seam (v25 line) | Replace/remove |
| --- | --- |
| _FlowValue 9019; _DeferredResultCarrier 9041; _AuthorityRecord 14023; _AuthorityState 14150 | Replace duplicated value/record/carrier authority with canonical Value/record variants. Retire record.value reconciliation. |
| _transfer_authority 14223; _ExecutionState 14913; _fork_values 15497 | Remove generic MutableMapping compatibility, raw hydration/adoption and payload transfer repair; use typed frame/state operations. |
| _captured_call_environment 15212; _ClassFrame 15254; _call_environment 15951; _refresh_bound_projection 15955 | Replace copied captures/projection refresh with explicit binding destinations and current-state reads. |
| deferred/element/member walkers 15513, 15624, 15695, 15795; _with_callable_authority 19333 | Replace duplicated retention/recovery walks with typed record access and operation-specific traversal. |
| _snapshot_call 17846; _evaluate 20361; _evaluate_value 20790; _assign 22746 | Route all converted reads, stores, call phases and observations through the core; immutable literal helpers may remain. |
| _current_exact_collection_value 15895; collection/native seams 19895-20099 | Remove stale shape fallback and native admission/result reconciliation; exact native operations return their canonical result/effect once. |
| _merge_states 23261; auxiliary state 23344-23382; class/control paths 23610-24720 | Successors own frames, objects, cells and issues together; no independent class/callable auxiliary state to reconcile. |
| helper-return 25299; source flow 25342; _review_body 26904, recursive bridge 27448 | Replace live FlowValue bridge and second-state body review; retain compatible row-building/classification logic on canonical observations. |
| derive_design_review 28967 | Preserve the public API and evidence schema; wire the selected analysis entirely through the new core. |

The final region has no live legacy-state adapter. During development, a declared
syntax subset may refuse unsupported analysis, but the whole selected public
analysis uses one engine. No fixture-keyed dispatch, mid-analysis fallback, or
combining the old engine's rows with the new engine's effects. Such intermediate
refusals are not permission to weaken any final required-clean case.

## First useful vertical path and cost gate

Gate A is six existing public analyses, not an isolated data-structure prototype:

- storage-composition-cases-v1.json: shared-list-consumed (refuse),
  shared-list-dormant (clean), class-adoption-unsafe (refuse),
  class-adoption-safe (clean).
- name-environment-cases-v1.json: hidden-cell-joined-reached (refuse),
  hidden-cell-joined-dormant (permitted-refusal).

The path is derive_design_review -> source-order evaluation -> real helper
binding/activation -> shared list or lexical cell mutation -> branch/class
successor -> later alias/closure call -> public row/blocker emission. Implement
ordinary local helper construction/calls/returns, tuple transfer/unpacking,
list append/index, live nonlocal cells, the existing small branch/None condition,
class namespace separation and protected-owner effects along that path. This
tests canonical state, not merely whether six fixtures can be recognized.
It does not wait for deep generator resumption or claim that six cases close C.

Gate B, before broad migration, reruns A and adds unchanged helper65/generator70
depth outcomes plus scale-n8-s4-d0-normal, scale-n64-s4-d0-normal,
scale-n8-s4-d2-exceptional and scale-n64-s4-d2-exceptional from public24. Use the
actual public analyzer and original budget epochs, not just storage counters.
The cost lane proposes a 196608-unit continuation reserve under the unchanged
262144 cap; it remains a coordinator decision to freeze before execution, not a
new runtime refusal threshold.

Use ordinary owned maps and shared stable metadata initially. A first-write
copy, order materialization, lookup, allocation, comparison, edge visit or failed
attempt remains real charged work. Neither dict+COW nor a custom persistent
backend is presumed efficient. Do not rebuild the whole module projection on
each unchanged fork/join/call. If ownership/partitioning still forces unacceptable
work, stop and reassess before adding a backend. Existing NameVersion/cursor and
primitive schedule counts are historical implementation evidence, not required
replacement APIs.

## Fixed acceptance and remaining risks

All existing labels stay fixed: matrix192/212 is 92 required-refuse, 81
required-clean and 19 permitted-refusal. Semantic52 is 22 clean, 26 refuse and
4 permitted-refusal across the seven frozen packs. Preserve public24, design53,
coordinatorjoin8, weakwrite3, lexical6, A19 and B18 required plus its one excluded
absent-global case (19 raw cases). Preserve existing canonical capability rows,
entry assignments/digests, profiles and later full gates.

Clean means exact expected rows/argv and no blockers. Refuse requires an explicit
public blocker; missing rows alone is not success. Permitted-refusal allows that
blocker, otherwise requires the exact clean output. In particular, forwarded-safe,
joined dormant and selected optional effective-result controls do not become new
mandatory clean promises. Delete/NameError coverage does not grant new clean
erasure recovery. Ordinary globals remain readable; unsupported global writes,
TryStar, mixed-exit correlation and descriptor/metaclass precision are not widened.

The main unresolved design risks are the physical snapshot ownership/copy cost,
the volume of state-bearing evaluator code that must be converted atomically,
preservation of historical versus current operand phases, and carrying opaque
dependencies without accidental execution or new positive precision. Gate A
tests the first semantic cut; Gate B tests cost/depth feasibility. Neither proves
all52, matrix192 or full corpus acceptance. The coordinator draft's bounded
increments and stop/reassess rule agree with this proposal. No faster runtime,
smaller final diff or complete implementation is claimed.

## Sources and custody

Read-only source/metadata inspection, not source execution. Local references:

- stage0-design.md: 78bebca5279bf81e30181787f962d40c73826259d0bb3ffb1c7804804c1211e8.
- tests-release-v4.md: eb571631726ea54a0ccb4bdf3b0b20324754fb7a85e5d6cd447f103862ad82ee;
  tests-scope-addendum-v1.md: 76db37e2edaa05f058e8514d9209c6d5f2f057a8860417a5bf6da39f24602e22.
- engineer-generator-v25-semantic.py (anchors only):
  481098d0be86d27f1664d0705a44a91d50b3a1361280a4e28c82bc366a541853.
- Gate A storage pack:
  faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709;
  name-environment pack:
  d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c.
- Cost gate clarification: rewrite-cost-and-fitness-clarification-v2.md,
  75c98159a96c33f5f9072c572beae567494ac16fa831c94058c6706be1e22c80.
- The seven fixed semantic packs and classifications were read as JSON metadata,
  including the unchanged52 population and its accepted scope notes.
- D:/Pontius/codex-c-core-rewrite-brief-draft.md was read as mutable coordinator
  design. No material architectural contradiction found; this note makes its
  class/deferred roles, temporal evidence boundary and API obligations explicit.

This note supersedes no issued evidence or test expectation. Root owns the
combined design, implementation authorization, future controls and dispatch.