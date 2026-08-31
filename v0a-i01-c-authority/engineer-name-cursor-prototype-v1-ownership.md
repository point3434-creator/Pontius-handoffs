# Name-cursor prototype v1: static ownership and accounting map

Prepared after frozen cursor spec 29c0238aa24e0c6d4a9f3834d6f94b46c4bd6ed29f263f0c57511e1ee1b0bfd1 and casepack ecddd020ffb2a0d85e624aeb7fb544f631b302839f9a5f3542c998b36c37ac61. No oracle expectations were changed.

Prototype: engineer-name-cursor-prototype-v1.py, SHA256 67acb279510924311266b985e15e95e53ae9d0a11d64a50d108f254a690deb2a.
Static inventory: engineer-checks/name-cursor-prototype-v1-static.json, SHA256 43574d05da2f728933e7b8c4f4334b89997899787790f1f95c5774e68c4495b2.
Validation so far: syntax parsed and source/AST inspected only. The prototype has not been imported or executed. No semantic pass or cost improvement is claimed.
Production W remains exact rejected v20 e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679.

## Boundaries to inspect

| Source anchor | Ownership / behavior |
|---|---|
| Meter 17, Entry 44, _check_name 49 | AST-equivalent to reviewed storage prototype v2, including spent throwing charges, unchanged 0..262144 limit, immutable Entry and ordinary-string precondition. |
| _History 55 / _history 61 | Only parent token, changed-name tuple and depth; no map, cursor, Entry or value. |
| _Layer 69 / _seal_layer 74 | Sealed mappingproxy plus pending-name tuple. The original dictionary is private or staged until publication relinquishes its mutable cursor alias. |
| _lookup_layers 97 | Newest-first dictionary attempts, with tombstone stopping the search. Eight sealed layers; cursor checks its private tail first. |
| _compact 109 | Traverses complete old-to-new inputs into a fresh dictionary. Tombstones remove shadowed older entries; old snapshots retain their own layers. |
| _Order 139 / _realize_order 169 | Name-only recipes/memos. Exact legacy multistate union uses genuine dict_keys views and actual set().union. Staged memos are not published here. |
| _keys 290 | Returns genuine dict_keys backed by a never-mutated memo. Neither cursor publication nor compaction occurs. All charges precede memo commit. |
| _ordered_items 301 | Reads current entries, including private tail. Whole tuple and order memo stage together; successful cached reads return the actual immutable tuple with reference/read charges, without a dummy copy. |
| NameVersion 329 | Immutable public reference API plus completed memoization. set/delete use a temporary cursor and publication; fork remains a retained reference. |
| _prepare_publication 386 | Builds provisional layers/history/version/fresh tail without mutating the owner or publishing an order memo. An order-only join also produces a new snapshot. |
| _charge_publication_commit 421 / _commit_publication 429 | All required publication charges precede the only two commit writes: cursor._base and cursor._tail. |
| NameCursor 437 / _replace_entry 470 | Private delta owned by one cursor. Required metadata/write charges occur before mutation. Raw identical-value set creates pending Entry and invalidates the item memo. Overwrite preserves order; delete/reinsert appends. |
| snapshot 508 / fork 517 | Both use staged preparation. Fork constructs the returned independent cursor and pays its return/publication charges before committing the source cursor. No internal snapshot commit can survive a later fork charge failure. |
| _common_history 534 / _pending_names 553 | Ancestry tracks names only. Pending metadata is filtered through each newest effective entry, including overwrites and tombstones. |
| join 574 | Captures/validates immutable same-meter input tuple before callbacks, rejecting cursors. Changed and effective-pending names participate. Callback input order and final exact union order remain separate guarantees. |

## Accounting interpretation

The static JSON inventories all 145 charged category names and source locations. These are semantic storage operations, visited entries/metadata and explicit data-structure/reference allocations, not a claim to count Python opcodes or every interpreter-internal allocator event.

- Private operations: write_private_tail_attempts, lookup_private_tail_attempts, lookup_layer_visits and lookup_dictionary_attempts; actual private writes and copied key/value references; Entry and cursor fields.
- Publication frequency/size: snapshot_requests, cursor_fork_requests, publication_change_entry_visits (the actual private-tail key count), snapshot_publications and copied layer/history references. A no-change snapshot does not create another layer.
- Layer sealing: publication_tail_entry_visits is the existing category spelling used by _seal_layer for every dictionary it seals. It includes a compacted output dictionary as well as an ordinary private tail; do not interpret this category alone as original tail size. publication_change_entry_visits supplies the unambiguous original tail count.
- Full compaction: compaction_layer_visits and compaction_entry_visits count every physical input; dictionary attempts/writes/deletes, copied references and final sealing are also charged. compaction_publication_charge marks publication work.
- Pending/history: separate metadata visits, effective lookups, ancestry comparisons/parent reads and changed-name copies.
- Ordered access: recipe construction/realization, dictionary writes/copies, actual legacy union input/output work, view/pair/tuple construction, bounded-layer lookups and complete memo publication. Cached immutable item tuples are reused, not rebuilt and charged for fictitious copies.

Meter always retains a throwing requested charge. In a failed operation, snapshot_publications or compaction_publication_charge therefore does not independently prove completion. A successful public return plus the corresponding visit categories is needed for that claim.

## Safety limits and remaining evidence

Operation-level staging covers snapshot, fork, keys and ordered_items. Readers do not secretly seal a cursor. A BudgetExceeded during a prepared operation leaves original backing/history/memos untouched; this is a source-level argument awaiting independent failure/retry tests, not a reported test result.

Published data can legitimately retain overwritten values until compaction or release of a retained snapshot. History and order metadata retain names only. No global cache or authority store exists in this isolated primitive.

Publication can still occur after every assignment in a frequent-fork workload. Every ninth prospective sealed layer performs full compaction, with all actual work charged. The source makes no amortized refund, expanded limit, universal constant-write claim or production-fitness claim.

Root must inspect exact prototype, executable oracle and controller before any child runs. The old28 cases and independent16 extensions remain separate, immutable test inputs. Class-adoption semantics found on v19 are deliberately outside this storage experiment.
