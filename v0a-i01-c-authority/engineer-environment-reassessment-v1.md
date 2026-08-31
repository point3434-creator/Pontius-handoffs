# Environment representation reassessment v1

Date: 2026-08-31. Read-only engineering reassessment; no source edit authorized
or performed by this note. Exact v19 generator:
3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1.
This proposes a bounded replacement inside Stage0, not a general Python heap,
new language precision, cold-review verdict or approval to raise a budget.

## Finding and decision direction

The representation still reconstructs an entire module-sized name projection at
successor joins, even when only a few authority identities changed. Gen05 directly
attributes40027 transfer units to merge reinstallation and only305 to constructor
fallback. Gen04/05 separate this from the now-small observation compaction cost.
Root reports gen06 ordinary generation still refuses at the existing cap; its
new attribution is pending and is not inferred here. The 53 original design tests
and192-schedule matrix pass on both actual interpreters for v19; that does not
establish corpus readiness or this proposed design's soundness.

At exact-v19:21269, merge joins stores and then rematerializes names. At14178,
ExecutionState.copy physically copies the whole dict, although that name-copy
loop has no per-entry metering. At16140-16142, call snapshots repeatedly fork and
merge states; successor coalescing21518/21592 does the same for retained exits.
A change that removes transfer charges while retaining all those physical copies
must not be described as removing the structural cost.

Recommend one coherent mechanism: a persistent ordered name environment, coupled
to explicit normalization/adoption operations, with joins over changes from a
shared base. Values still refer to the existing identity-indexed object/cell
stores. The replacement boundary is the name table and its mutation/projection
seams, not the language evaluator, helper binder, parser, capability schema or
exception partition. This needs its own pre-edit implementation design and
structural RED; do not add another local cost heuristic while that is undecided.

## Proposed representation and obligations

A name-table version carries a shared immutable base, its ordered binding changes,
and explicit pending-normalization metadata. Fork shares the version; writes own
only their changed binding representation. A common-base join can reuse unchanged
registered entries and process changed or pending entries without visiting every
ambient global. Storage must preserve ordered-map assignment, deletion and
reinsertion exactly. A plain flat COW dictionary is insufficient: its first write
still copies N entries. An operation-journal/index representation is a bounded
implementation candidate, but it must demonstrate bounded lookup/compaction cost
and exact iteration order before selection; merely renaming a linked history as a
persistent map is not a solution. Do not promise O(changes) if reads or compaction
still perform unmeasured full traversals.

Keep operations distinct: semantic assignment performs full transfer and the old
cell writes; semantic deletion retains the old unbound/weak-delete behavior;
projection installation/removal changes names without inventing Python cell
writes; state adoption carries name, binding, authority and normalization roots
together. Clear is projection replacement, not a sequence of Python deletions.
Any uncertain/external entry owes full transfer. Shared current-value identity
alone never pays that debt.

Audit every direct projection seam. Constructor/copy/update/clear, captured-cell
hydration, parameter injection, post-helper refresh and merge bypass normal
setters. In particular dict.pop(environment,name,None) at18404 removes a projected
caller-local name without deleting its cell. Raw parameter or merged projections
must remain marked pending until the real normalization boundary; they cannot
inherit a blanket registered certificate. Scope-exit pop uses semantic deletion.
Existing clear/update adoption pairs must preserve their exact replacement versus
overlay behavior. Search all explicit dict operations and mutating APIs again;
a source guard can require classification, but behavioral checks remain authority.

Normalization validity belongs to an environment/store lineage, not only a value
object or name-map token. A fork shares that lineage; a proven monotonic store join
retains inherited records; adoption from another context must reestablish it.
Changed values and pending raw entries execute the complete transfer path, keeping
unresolved-reference obligations. Do not cache state-dependent callable effects.

Even identical name roots do not imply identical cells. After the name join,
retain all existing strong/weak writes for participating bound names. Transferring
changed/pending values keeps the old name order and object-allocation order.
Delayed cell writes commute only for distinct existing cells. Overlapping or
missing cells require the old ordered behavior; neither an identical-name shortcut
nor a new table may erase this requirement. Captures, defaults, branches, retained
aliases and historical snapshots remain bound to their original identities.

## Measurement and falsification before integration

Structural RED must use a generated family through the public analyzer boundary,
not only the item currently exhausting the cap. Vary irrelevant ambient globals N,
normal/exception successors S, actual changed names D and retained alias/cell shape.
Include D=0, a fixed small D, overlap, missing/unbound cells, and raw-projection
entry. Pair unsafe reached mutations with dormant/lawful controls and harmless
independent runtime traces. Do not execute inspected sensitive fixture bodies.
Show the predecessor's repeated full-copy/full-normalization scaling, then measure
the same family on the replacement. Also retain the real corpus RED and require
ordinary generation/canonical census GREEN; synthetic wins alone are insufficient.

Meter actual fork allocation, copied bindings/nodes, delta traversal, lookup
layers/nodes, materialization, joins and compaction. Never refund fallback work or
suppress budget exceptions. Performance acceptance must state which operation
scales with N, S or D, rather than freeze a convenient single-run number. Existing
caps remain unchanged. Verify public row/blocker behavior, all current authority
matrices, ordered delete/reinsert, raw entry, adoption and historical observation
on3.11.15 first and3.14.6 second. Any extra eager normalization or omitted cell write
is a semantic change requiring separate proof, not a free storage optimization.

## Alternatives and retained complexity

A name-generation token is smaller: copies share a token and every name mutator
invalidates it. It can identify equal maps, but cannot certify raw projections or
cell equivalence, and it leaves full dict-copy cost intact. It is a diagnostic or
bounded transitional option only if measured equal-token hits justify it; not the
recommended structural solution. Missing one bypass creates false equality, so its
routing audit and future guard are real costs. No token-only optimization is
implemented here.

Retain v15's restored helper-disabled analysis boundary, v16's correct expression
lifetime, and v17's snapshot-safe observation storage unless the replacement
subsumes that storage with equivalent evidence. Retain v18's direct fork allocation
and single-lookup writes. Replace its constructor-specific copying convention with
explicit adoption/normalization rules if needed. Retire v19's per-merge cost planner
once the structural replacement supersedes it; keep the shared unchanged cell-write
helper and all behavioral obligations. Accumulating both mechanisms indefinitely
would make authority ownership harder to inspect without proven benefit.

Do not proceed if correctness needs guessing normalized state, dropping actual
cell writes, altering key order, making unsupported syntax newly accepted, raising
caps, or introducing a general heap/effect interpreter. Also reject a storage design
whose honest copy/read/join accounting does not improve the structural family.
If preserving the legacy dict surface makes true sharing unbounded in scope, stop
for an architecture decision rather than claiming another point optimization closes
this category. No additional source work or GREEN follows from this note itself.
