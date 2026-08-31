# R2 baseline R1 natural-hook inventory v1

Engineering input-side inventory, codex/mapping_compatibility, 2026-08-31. Signatures and shapes only; not an evaluator re-audit, adapter approval, cold pass or runtime result.

Bound to H `b1d15de062ac45c351f0254b358ee1e5fc35bdee`, manifest `beb50fab0fe159249de1397529b78a71e2b176b8e3643ea64ccb37dbf1a1c15a`, source `rewrite-r1-task5-source-v2.py` SHA256 `c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f`. Independently verified the frozen source and all 19 manifest-listed blob hashes. All line numbers below refer to this exact source.

## Exact signatures

All arguments are positional-or-keyword except the explicitly keyword-only owned parameter. No listed function has a default argument.

```python
# 10180
_c_eval(ctx: _CContext, state: _CState, frame: _CFrame,
        node: ast.expr) -> tuple[_COutcome, ...]
# 10344
_c_statement(ctx: _CContext, state: _CState, frame: _CFrame,
             node: ast.stmt) -> tuple[_COutcome, ...]
# 9317
_c_state(ctx: _CContext) -> _CState
# 9331
_c_fork(ctx: _CContext, state: _CState) -> _CState
# 9324
_c_snapshot(ctx: _CContext, state: _CState) -> _CView
# 9511
_c_join(ctx: _CContext,
        alternatives: Iterable[_COutcome]) -> tuple[_COutcome, ...]
# 9392
_c_cell_write(ctx: _CContext, state: _CState,
              cell: _CCellRef, value: _CValue) -> bool
# 9306
_c_copy_dict(ctx: _CContext, source: dict[Any, Any]) -> dict[Any, Any]
# 9416
_c_object_read(ctx: _CContext, state: _CState | _CView,
               reference: _CRef) -> _CObject | None
# 9436
_c_object_write(ctx: _CContext, state: _CState,
                reference: _CRef, record: _CObject) -> bool
# 10623
_c_invoke(ctx: _CContext, state: _CState, frame: _CFrame,
          call: ast.Call, selected: _CValue,
          arguments: tuple[_CValue, ...],
          keywords: tuple[tuple[str, _CValue], ...]) -> tuple[_COutcome, ...]
# 10812
_c_review_outcomes(ctx: _CContext, outcomes: tuple[_COutcome, ...],
                   *, owned: bool) -> tuple[
    list[dict[str, object]], list[dict[str, object]],
    list[dict[str, object]], list[dict[str, object]]]
```

These are declaration transcripts, not new executable source.

## Return and completion boundaries

| Hook | Actual R1 return/completion |
| --- | --- |
| _c_eval / _c_statement / _c_invoke | Ordered exact tuple of _COutcome objects on ordinary completion; original exceptions may propagate. R1 controls include normal, return, raise and refused. A returned tuple is not itself proof of four distinct states. |
| _c_state | New mutable _CState wrapper, initially empty cell/object tables and a fresh version. |
| _c_fork | New mutable child wrapper sharing current tables/version; parent write token is revoked. Parent and child may have equal version, so version is not a state birth identity. |
| _c_snapshot | Immutable _CView of current tables/version; revokes the source state's writer token. It does not allocate a _CState or imply a copied table. |
| _c_join | Consumes its Iterable once; deduplicates by _COutcome object identity in encounter order and returns a tuple. It does not deduplicate by state identity or merge heaps. Do not pre-enumerate an arbitrary iterable to observe it. |
| _c_cell_write | False if activation bank or declared name is absent; True only after current-bank update and state-version update complete. Observe a committed logical write only after True. |
| _c_copy_dict | Returns source.copy() after the original 1+3*len(source) charge. A throwing charge is an attempted copy, not a completed copy. Exact dict length is available without visiting entries. |
| _c_object_read | Returns the original current record, or None if its object ID is missing. It supports both live state and historical view; None is not an empty/exhausted record. |
| _c_object_write | False if the object ID is absent; True only after record replacement and state-version update. Its return is bool, not None or a new state/record. |
| _c_review_outcomes | Four-element tuple: rows, blockers, sites, edges, in that order. Each element is a fresh list of dictionaries. These are export results, not state successors. |

The helper-depth check belongs to _c_invoke; observe the incoming helper_path and original error rather than supplying a new interpretation or retry. The R1 check uses len(helper_path)>64 and raises InventoryError with the exact helper-depth message.

## Safe scalar projection fields

Use exact known record types and exact scalar validation. Project only while the original arguments/results are call-local; retain no analyzer object. Reading these fields is not permission to call metered helpers, evaluate truth/equality, recursively traverse retained graphs, or inspect data through arbitrary user protocols.

- **Context (9290):** item_id:str, path:str, helper_path:tuple[tuple[str,int],...]. program, arena and budget are object references, not durable observation data. There is no deferred_depth field in R1. Match budget identity through the existing BudgetObserver epoch machinery.
- **Source/frame:** AST node type name and existing lineno/col_offset/end fields may be projected to primitive labels. _CFrame.activation_id is int|None; scope.kind and scope.path are strings; scope.node/captures/module/enclosing frames must not be retained. No AST walk is needed to obtain operation location.
- **State/view/reference:** _CState.version and _CView.version are ints; _CRef.object_id is int; _CCellRef.activation_id is int and name is str. Tokens/tables are not scalar evidence. Raw Python id(state) may be a transient adapter lookup key, never a durable branch identity.
- **Value/result:** _CValue is _CAtom|_CRef|_CChoice. _CAtom has kind:str, data:str|int|float|bool|None, reason:str|None. A safe literal projection requires exact _CAtom and kind=literal, followed by the observer's exact scalar/serialization checks. Unknown or symbolic data is not an actual value proof. _CChoice.alternatives is tuple[_CAtom|_CRef,...]; do not assume it has data or flatten it as an immediate iterator.
- **Outcome (9241):** control:str, exception_tag:str|None, explicit:bool, excluded_handlers:frozenset[str], plus state/result/issues/trace. Tuple counts and validated scalar labels can be projected; state, result wrappers, issue objects and trace graph cannot be retained.
- **Issue:** path, reason and category are strings; source coordinates come from its node. A legacy category/tag is diagnostic evidence, not proof of a catchable runtime exception.
- **Object-read results:** R1 _CObject is _CFunction|_CBound|_CNativeMethod|_CSequence|_CNamespace|_CInstance|_CEnvironment. Available scalar labels include function descriptor_kind/body_kind, sequence kind, namespace kind/origin, native-method operation, instance open_entry, and environment inherited/unresolved_reason. Exact existing tuple lengths may be counted without traversal. Captures, members, elements, receivers and templates remain live references; do not retain or recursively inspect them for this baseline adapter.

R1 _c_out constructs explicit=False and empty exclusions. There is no known-exception origin field. _CCallObservation.completed (9253 onward) has four fields per completion: (control, result, _CView, issues); it does not include the prospective R2 exception metadata. Existing blocker-backed raise controls must not be mislabeled as completed _c_raise_known events or matched-handler evidence.

## Complete state-allocation inventory

Whole-file AST/name-call inspection found exactly two _CState constructor calls:

| Constructor location | Enclosing factory |
| --- | --- |
| 9321 | _c_state: constructs the initial state and empty tables. |
| 9335 | _c_fork: constructs the child sharing existing tables/version. |

The only R1 calls to those factories are _process_review_rows at 11117 (_c_state) and 11193 (_c_fork). Snapshot/own-cells/own-objects/new-activation/object updates do not construct another _CState. Thus original-delegating wrappers on the two factories cover R1 state births. A later candidate requires a fresh allocation-site check; this finding must not be inherited merely because the names remain.

## Prospective roles absent on this baseline

No definitions exist for _c_identity_compare, _CBooleanUnknown, _c_raise_known, _c_handle_known_exception, _c_try, _c_resume_generator, _CGenerator or _CRange. _CContext has no deferred_depth, and R1 has no internal yield/stop resume-result channel. Record these roles as unavailable on the declared baseline, not successful zero work or an infrastructure failure. Missing original hooks or mismatched source shape is a different compatibility failure.

Method: frozen Git blob hashing and stdlib AST/source inspection under actual CPython 3.11.15 -I -S -B -P. No source, Model, test, analyzer or harness was imported/executed; no candidate/schema/API decision or source change was made. This inventory is an aid for the separately reviewed exact harness.