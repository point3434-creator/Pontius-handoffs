# Radix prototype v1: ownership, operation and accounting map

Author: Codex authority_cost_audit. T-only engineering implementation; no
prototype/oracle payload, production import, port, W write or threshold sweep.
Root inspection and separate execution authorization remain required.

Exact artifacts:
- engineer-name-radix-prototype-v1.py:
  0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71
- engineer-name-radix-accounting-v1.json:
  79f64e5e7bbb429bedd108654b69c8ab5893973ee742517b543129f762f68f2b
- engineer-name-radix-prototype-v1-from-cursor.diff:
  5055457bd014990b624d52fb9a21b014aab6a34c810138aa7949079bc9f9e38c
- engineer-name-radix-static-v1.json:
  6f3187a65319b12122f9f8b5ee4e631e323ce348d64685b6b71d37edebe53a01

## Representation and ownership

| Object / source line | Owner and invariant |
| --- | --- |
| _RadixLeaf73 | Frozen record owns a read-only proxy over an exclusively relinquished dict; effective pending tuple contains only its current raw/pending names. |
| _RadixBranch79 | Frozen bitmap + packed child tuple + exact pending count; no value-bearing parent or prior-version link. Empty slots do not own children. |
| _LeafEdit85 | Operation-local mutable copy of one touched leaf; reused for later writes to that same path in the current publication. Never stored in a returned root. |
| _BranchEdit94 | Operation-local base branch plus only changed child slots. Finalization copies actual surviving child references; untouched immutable siblings stay shared. |
| _History59 | Preserved names/token/depth-only history. It cannot retain prior roots, versions, Entries, cursors or values. |
| _Order387 | Preserved names-only recipes and immutable name-only cache. A known bulk cache is complete from creation and never cleared. |
| NameVersion577 | Meter, immutable current root, history, order, size and optional immutable items memo. Returned versions have no editors or caller-owned mutable dictionary. |
| NameCursor714 | Own private tail/order/items state over one immutable base. No cursor is shared by fork; immutable base/root data may be shared. |

The internal NameVersion initializer's storage argument changes from layers
to root. All reviewed public factory/read/edit/fork signatures remain, and
from_unique_entries is the sole new public operation. The Meter, Entry,
BudgetExceeded, name validation, history/common-history and all order/read
helpers are AST-identical to the cursor predecessor. Cursor methods other than
its two internal lookup/edit methods are AST-identical.

## Actual operation routes

| Route / anchors | Work and publication boundary |
| --- | --- |
| Lookup128 | One normalized hash, successive four-bit index routes, occupied child reads, then one leaf dict attempt. No order demand or publication. |
| Leaf copy179 | Explicitly visits and copies every touched old leaf entry into a new owned dict; no whole-root copy. |
| Split190–247 | Creates hashed records, partitions by occupied nibble groups, recursively creates private paths until leaf size16 or hash-width exhaustion. Every visited/routed/copied record is charged. |
| Edit248 | Applies private tail changes to temporary editors. Existing immutable leaves are copied once per publication; deletions remove current entries rather than leaving old data layers. |
| Freeze294 | Visits changed paths, scans16 branch positions, freezes edited leaves and child tuples, shares unchanged siblings and derives exact pending counts. It never writes old nodes. |
| Bulk326/595 | Consumes the unique-entry iterable once, validates each pair/name/Entry/proof/duplicate, builds name-only order and hashed records, then partitions directly. No immutable-set loop or predecessor absence lookup. |
| Pending369/830 | Walks effective current nodes; zero-pending subtrees are skipped via their count. It does not inspect stale entries from historic layers. |
| Publication673/785 | Builds history/root/version/fresh tail privately. After all return/commit charges succeed, only cursor base/tail are replaced. No earlier step changes a shared cache or owner. |
| Fork794 | Also constructs the independent child before the parent's publication commit, so a late allocation/charge failure cannot partly publish the parent. |
| Order538/549 | Exact preserved legacy union and delete/reinsert realization. All cache charges finish before memo writes; cursor reads include private edits without publication. |
| Join835 | Preserved input capture, meter validation, candidate/history rules and callback law. Unrelated-name and pending enumeration now use the effective index. Final exposed order is still the legacy union recipe. |

The transient editor may temporarily reference an old root through its base
branch while preparing publication. Those references do not enter the new
immutable root/history. After successful changed publication, the current base
contains only effective entries. Old snapshots still own their original values.
Replacing or deleting a value must release it once its last legitimate old
snapshot/other owner is dropped; that requires the independent retention checks,
not merely an assertion that a garbage collector ran.

## Meter classification

The JSON lists every literal charge category with source function/line/units
and one P or non-P classification. Its prototype SHA is exact. Unknown observed
categories must make accounting incomplete.

P counts explicit name/entry/index-child/history/order reference visits and
copies. Dictionary-operation dispatch, allocation, wrapper/proxy field copies,
node-shape/empty-slot/control inspections and public-return work remain non-P,
but stay fully in total C. For example a dictionary insertion request is one
non-P operation; separately recorded key/value reference copies are its P data
copies. These are different declared events, not two P names for one event.
This is the existing algorithm-work abstraction, not CPU opcode accounting.

Successful bulk calls must report bulk_input_visits=N,
bulk_uniqueness_attempts=N, bulk_order_writes=N. Copies and routes can exceed N
and remain charged. Input preparation by a caller/oracle is outside this
factory; a production adapter must additionally account for that real work.

Leaf dict attempts do not count CPython's hidden equality probes. The independent
closed collision keys report those separately. N16 can exercise collisions in
an ordinary leaf dictionary; N64 additionally reaches hash-width exhaustion.
radix_terminal_collision_* categories report that actual route, not an assumed
collision from a label. No keys are converted to plain str.
Collision leaf copying remains an explicit full-entry traversal. A collision
dictionary can require linear hidden comparisons for one charged dict attempt,
so the cap is not a strict wall-time bound.

snapshot_publications is a precommit charge and can itself throw. Only the
oracle's successfully returned snapshot/fork establishes completed publication.
A throwing charged request remains spent; no refund/reset or postcommit
throwing charge exists. Counts of attempted work must not be called commits.

## Static evidence and remaining gates

Author checks only parsed/read source; no module, fixture, oracle or prototype
was imported or run. Pins for predecessor, disposition, frozen specification,
case table, retained v22 and independent W v20 were verified before/after.
The static proof inventories protected ASTs, public methods, literal categories
and absence of layer/compaction paths or bulk immutable-set calls.

The independent combined scope is34 unchanged storage runs +28 cursor runs
with the explicitly disclosed neutral retention-trigger successor +31 extension
runs, not a claim that all old62 executable checks stayed byte-identical.
Root must inspect prototype/accounting/oracles/control before fresh serial
floor-first snapshots and seeds0/1/17. Actual cost, full retention, exact failed
operation retry/continuation and frozen growth falsifiers are all unverified.
No production fitness claim follows from this source handoff.

The fixed leaf size16 and nibble width4 are not admission limits. Hash-width
exhaustion uses a collision dictionary under the same original262144 meter.
If the experiment fails, retain the result and stop for the coordinator; do not
alter thresholds, expectations, caps or authority semantics to chase a pass.
The production bulk adapter and separate class repair remain future reviews.
