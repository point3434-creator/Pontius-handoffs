# v30 plan: enumerate-pair accounting only

Status: frozen plan; source authoring and payload are NOT authorized.
Root approval waits for the independent v29 correctness review.
No source, test, cap, oracle, or existing accounting meaning changes in this task.

Predecessor: engineer-generator-v29-storage.py
SHA256 b53b905cd20dd97d7d09a3b81f955bf27498a572ce8a6d82e20f007993ab9466.
Accounting: engineer-generator-v29-storage-accounting-v1.json
SHA256 5074f3509e47d1de642b30f5351dd953997397b4e29a841cc59ae92c6c7d292d.

## Retained source finding

At22469, disabled_join_input_iterator_allocations=2 covers the enumerate wrapper
and underlying ordinary list/tuple iterator. At22471,
disabled_join_input_visits=2 covers the state visit and captured-snapshot indexed
read. Neither includes the yielded pair and its two references under the adopted
semantic allocation model. The guard-function/closure charges at22432-22433 cover
only the function and its two captured references; they do not cover this pair.
The v29 accounting map contains no separate pair-allocation/reference site.
This is a confirmed accounting omission, not a demonstrated semantic result error.

## Exact proposed source delta

Retain enumerate and every existing line. Insert these two calls immediately after
the for line and before the existing input_visits charge/guard use:

    for index, state in enumerate(states):
        join_meter.charge("disabled_join_input_pair_allocation")
        join_meter.charge("disabled_join_input_pair_reference_copies", 2)
        join_meter.charge("disabled_join_input_visits", 2)

The first new call charges one logical pair allocation/materialization (non-P).
The second charges its two reference copies (P), consistent with the existing
items_pair_allocation/items_pair_reference_copies distinction.
No existing category is renamed, reduced, reinterpreted or repurposed.

The first loop-body boundary is after Python has yielded/unpacked the pair but
before the existing guard consumes its index/state. This is the insertion point
available without changing enumerate or the algorithm. These are semantic work
charges; no claim is made that CPython allocates a fresh heap tuple per iteration.
Each reached iteration gains three units; a failing charge keeps the original
consume-and-raise behavior, with no refund, retry, exception suppression or cap
adjustment. This plan predicts no fitness or runtime result.

## Approval and verification boundary

After explicit root source GO, create-only engineer-generator-v30-storage.py
starts from the exact v29 pin. Only the two-call insertion is permitted; retain
v29 and all earlier artifacts. Issue exact delta, new-category accounting entries,
and static proof that removing precisely those two calls recovers every v29 byte
and AST. All other source methods, existing charge sites/units, tests, limits,
oracles, source ordering and publication behavior must be unchanged.

Root inspects that successor before any dispatch. Do not replace enumerate, add
a different optimization, alter a fixture, or fold independent correctness-review
findings into this accounting-only candidate without a separate scoped decision.
No candidate source or runtime payload was imported/executed for this finding or
plan; the author performed only frozen-source and accounting-map reads.
