# v19 prerepair: batch sparse merge bindings without dropping cell writes

Date: 2026-08-31. Engineering plan before editing; not a cold review, release or
acceptance claim. Exact v18 predecessor generator:
d97ea66ef606144bb635f522856af3a5cd08819368af981a0a408c84c1e6cc99.
Scope remains the separate C authority transfer replacement.

Measured RED is tests-checks/red-budget-gen05-v4-311-receipt.json, SHA-256
0a9a8fc7f457e0e3f4ce128027058ef3afc2712302b1b2e2d3fc24b6bbc24a23.
The unchanged262144 cap fails at262145 in the fresh-action-width structure item,
now reaching _fraction_pair through historical semantic-key/hash helper effects.
Selected third-level attribution identifies40027 transfers directly from merge
name reinstallation, versus305 from constructor fallback. All setter binding
lookups together cost57598. The trace did not record name/binding cardinalities;
no performance number or planner utility is inferred from nonexistent counts.

Change only _merge_states materialization and extract the existing strong/weak
cell-write loop into _ExecutionState._write_cells, shared with normal assignment.
Keep every full _transfer_authority call. Transfer values in exactly the existing
names iteration order, retaining object-identity allocation order and projected
map insertion order. The sparse fast path then performs every original cell write
for participating bound names. The generic setter, update/environment paths and
all other transfers keep their current behavior.

Planning cost is explicit. Let N be projected names, K all binding-map entries,
B participating bound names, and E the sum of their cell-tuple lengths. A successful
plan adds C=3+2K+3B+4E work units before counting the unchanged transfers and cell
writes. The terms are: one planning check; two temporary dictionary/set allocations;
K binding-item visits plus K name-membership lookups; B plan writes plus B plan
visits and B projected-value lookups; E cell visits, E overlap lookups, E existing-
cell lookups and E seen-set insertions. Normal maps charge their own item and cell
lookups. Other new operations are charged explicitly at their actual execution.
Existing projection dictionary writes remain the same writes as the old setter.
No tuple of cell IDs is copied; the plan references existing immutable tuples.

Try discovery only when its lower bound3+2K is below N. Extend C as participating
entries are found and stop planning if C reaches N. Accept only a complete valid
plan with C<N, so charged additional successful-path work is strictly less than
the N binding lookups eliminated. This is an execution strategy, not a new limit,
refusal, cap increase or approximation. Disabled authority uses the old loop. A
failed plan retains charges for work actually done, then uses the old loop; no
budget is refunded or caught. Its potential fallback overhead remains a measured
risk for ordinary generation, not something hidden from the budget.

Safety conditions: every participating cell must already exist, and cell IDs must
be disjoint across all participating tuples. Overlap, missing cells or insufficient
savings uses the exact old setter loop before any transfer/projection occurs.
Missing-cell fallback preserves insertion order of the cell dictionary; updates
to existing distinct cells do not move entries. An overlap fallback preserves the
old last-writer behavior and alternative weak-merge ordering. Bindings for names
absent from the projected name set receive no writes, as before.

Why transfer can precede these writes: _transfer_authority reads/allocates object
records but does not read cells, bindings or projected names. _merge_flow_values
reads supplied immutable values, not the live store. Cell writes do not allocate
object identities. Therefore identical transfer order yields identical projections
and object IDs; delayed writes to distinct existing cells commute and leave the
same cell values. _write_cells retains the old one-cell strong update and multiple-
cell weak merge exactly. Every changed/new/external value still crosses transfer,
including its unresolved-reference refusal. No historical snapshot is mutated.

Falsifiers and verification: overlap must exercise fallback, not reordered writes;
missing/deleted cells must retain the original behavior; distinct alternative cells
must receive every weak write; source-point snapshots and external missing-reference
obligations must remain intact. Root will run ordinary isolated generation, then
required focused public checks on actual3.11.15 before3.14.6. This engineer runs no
payload. All five caps, observed storage/lifetime, old test bytes, generated files,
controller documents and accepted A/B/other-C bytes remain outside this edit.
