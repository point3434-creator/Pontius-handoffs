# v28: operation-local disabled join proposal v1

Plan only. No source mutation, payload, cap change, helper1050 test/wording change,
or authorization to implement is implied.

Source: engineer-generator-v28-storage.py,
SHA256 4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e.
Root v28 verification a70eb13b0c3edb59d7944857a79d1d8c0d99aacbd715a7819c958f22e5fbf186:
51/53, helper65 now passes; helper1050 remains a recorded regex/category conflict;
generator70's exact-depth gate remains substantively red.
Root sharing verification a3d382e897e72d8c6e46c200418180823c9c1b727417e52dca9a42e68fc09801:
all36 measured joins had two exact disabled states, same meter/budget, 73 pending
entries each, but distinct published roots. Identical-root C stays out.
Common-history identity/change cardinalities were NOT measured by that observer.

## Selected scope

Add one adapter-local disabled join branch inside _merge_states. Do not change
NameVersion, NameCursor, radix/order/history algorithms, generic _join_name_versions,
transfer, cells, any authority map, or another resolver path. No new backend,
permanent certificate, global cache, mode discount, or consumption semantics.

Use existing names-only history to discover changed names. Still construct and
iterate the exact original all-parent legacy set union in its original order.
Do not turn this into a sparse-order callback scheme or claim an O(changes) whole
join. The intended saving is fewer unchanged-name index lookups and no detached
full-name bulk reconstruction; ordering and downstream full mapping reads remain.

## Gates and placement (source anchors in companion JSON)

1. Keep _merge_states22351-22396 initial result fork and every authority/binding
   join exactly. Keep empty/singleton behavior and enabled compatibility/cell plan.
2. Keep original state snapshots at22400-22403 before callbacks/result mutation.
   Only then consider this branch: exact ExecutionState result and inputs, exact
   immutable NameVersion snapshots, authority.enabled is exactly False throughout,
   same original budget and NameMeter (including meter.budget identity).
   Visit and charge every guard actually evaluated. Plain mappings, subclasses,
   mixed modes, mismatched budgets/meters keep the old full path.
3. Require each immutable input root's effective pending count equals its size.
   Reuse the existing pending-count helper and charge size/metadata reads. This
   excludes positive certificates which old disabled materialization would reset.
   Never infer this condition from disabled mode alone.
4. Obtain a common ancestor with existing _name_common_history14889-14905.
   If absent, retain full fallback. For each input, walk history back to that exact
   token; collect/deduplicate every token.changes name with actual visited-token,
   parent, name, dictionary-attempt/write/reference charges. Do NOT visit pending
   names: pending records are retained, not discharged by this operation.
5. Compute the original key views, set().union(*key_views), and all original union
   charges at22405-22410. If candidate-count >= unique-union size, retain the full
   fallback: there is no demonstrated unchanged-name region to exploit. This is
   only an implementation choice; never refuse an input or change admission caps.
   Common-history planning charges are real even when the old path is selected.

## Exact per-name algorithm

Create an unpublished cursor from name_inputs[0], preserving its exact Entry
objects, name order and pending flags. In original union order, charge each name
visit and candidate-membership attempt.

- A history-changed name uses the exact old supplied-value tuple, _merge_flow_values,
  _transferred_name_entry and name validation sequence; install the resulting Entry
  in the staged cursor. Missing values keep the old None translation. Both differing
  values and same-object writes remain candidates, because history records writes.
- For an unchanged-history name, perform ONE metered first-version entry lookup.
  Require exact NameEntry, entry.no_work is False, and exact FlowValue value.
  Then retain the existing entry without merge/transfer/replacement.
  If those local checks fail, execute the same original per-name path as above.
  Do not assume wrapper type or annotations prove arbitrary stored-value validity:
  repeated None is a concrete counterexample to an unguarded identity shortcut.

This keeps changed/atypical callbacks in their original relative legacy order.
Names absent from every input need no deletion: the cursor begins from the first
input, so such names are absent there too. A name absent on only some paths is in
the union and in history changes; its original maybe-unbound merge still occurs.

Stage a known immutable order memo from the already computed union in exact order;
charge the complete iteration, dictionary writes/key references, memo and recipe.
Override the staged cursor order and invalidate its items cache, then use the
existing snapshot publication and install a fresh result cursor only on completion.
No all-parent order is dropped; no later re-realization cost is concealed.
Keep source snapshots, authority/binding joins, pending flags and unrelated old
views intact. Do not call result.clear() on this branch: creating an empty cursor
and detached history only to replace them would be needless work. The old full
fallback body stays unchanged.

## Why the restricted elision is sound, and what changes in the rule

History is names-only and records every cursor write/deletion/publication. A name
outside all changes since the common token has the same immutable Entry in all
inputs. Clear and detached bulk builds establish separate history roots, therefore
cannot fake this proof. No equality between different entries is used.

The local exact-FlowValue guard matters: that frozen dataclass has no custom
equality/truthiness method. _merge_flow_values13435-13436 on copies of the identical
FlowValue returns that object. By contrast, None returns an unknown and arbitrary
subclasses can override behavior, so they are not elided.

_transfer_authority14043-14045 returns its input immediately when disabled, before
budget consume, reference inspection, recursion, identity allocation or store
writes. _transferred_name_entry15116-15131 would then only allocate Entry(value,
False). Retaining the existing exact pending Entry has the same value and debt.
The original disabled full branch does not call _write_cells; every actual
authority/binding join was already retained. Changed names still invoke the
original transfer function, despite its no-op result, to keep the exception narrow.

The current literal "every joined name passes transfer" rule is stronger than this
semantic obligation. Implementation requires an explicit approved clarification:
only in this all-disabled operation, a history-identical exact FlowValue/pending
Entry may retain its original Entry because both merge and transfer are proved
identity operations. Every enabled, changed, atypical, incompatible or unproved
name keeps the existing transfer boundary. This is not an existing blanket
exemption, not an enabled certificate, and not permission to set no_work=True.
Later enabled adoption still sees False and owes the original revalidation work.

## Cost bound and utility limit

Let S be inputs, N union names, H walked history links, E visited changed-name
records (duplicates included), K union names requiring the original per-name path,
R the existing logical radix lookup cost, and P(K) actual changed-path publication
work. With valid unchanged FlowValues the branch performs N-K first-input lookups
plus S*K ordinary input lookups, rather than S*N. All union/order work remains
O(sum(input sizes)+N); preparation is O(H+E). It replaces the detached N-entry
builder by existing P(K), which is NOT assumed O(K): leaf splitting/collisions and
packed-child/reference copies remain charged. Ordinary radix height is bounded by
the existing hash width; Python dictionary internal collision probes remain the
previous separately disclosed accounting limitation, not one probe per charge.

The comparison is structural, not a runtime or completed-budget prediction.
History distance, real K and this path's actual utility are unmeasured. Repeated
history traversal and unavoidable _snapshot_call alias/assignment enumeration can
still dominate. If full fallback wins because history is absent or K is dense, do
not add another shortcut, metadata cache or cap increase automatically.

## Review/execution boundary

Before source GO, approve the operation-local transfer rule, inspect the exact
guard/fallback and order staging, and bind a candidate-specific static diff.
Preserve v28 A+B and all protected ASTs; keep semantic-v25 work separate.
The next integrated check remains the existing focused design population under
root control. Its untouched generator70 exact-depth gate is the relevant fitness
result; helper1050's separate regex conflict cannot be quietly relabeled green.
Existing mixed-mode/pending/order/ownership cases must remain unchanged. No extra
probe campaign is proposed. Stop if history completeness, local identity proof,
callback purity/order or pending debt cannot be maintained in the bounded adapter.
