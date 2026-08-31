# v24 storage-only radix adapter plan v1

Authoring plan for coordinator review; no candidate bytes or payload yet.
Output, only after root go: T/engineer-generator-v24-storage.py.
T = D:/Pontius-handoffs/v0a-i01-c-authority. W is never written by this task.

## Pinned inputs and bounded change

- Predecessor: engineer-generator-v22.py,
  61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3.
- Primitive: engineer-name-radix-prototype-v1.py,
  0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71.
- Disposition: coordinator-indexed-prototype-result-disposition-v1.md,
  bb293b7112f7d833aff1b8c72d134ae53d998bce5930c41a393dd930ff943d1e.
- W watch remains e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679.

Replace only the name primitive region, add the two complete-build adapter paths
below, and preserve every other outer/resolver method. Class/helper/cell ownership,
exception, recursion and rebinding semantics remain exact v22, not the separate v23.
No threshold change, mode exemption, new authority store, cap change or workload claim.

Port the reviewed primitive by identifier namespacing only. Keep existing _NameMeter
14086..14095 and its direct original consume delegation. Do not import prototype
Meter, BudgetExceeded or MAXIMUM_WORK. Existing sys/MappingProxyType imports suffice.
Map Entry/History/Order/Version/Cursor/Publication to the existing _Name* names;
new RadixLeaf/RadixBranch/LeafEdit/BranchEdit get _Name prefixes. Private functions
get _name_ prefixes, join becomes _join_name_versions, constants use _NAME_.
Remove the obsolete sealed-layer implementation, not its retained evidence.
Exact canonical AST equality against the prototype, after inverse namespacing,
is required before release. Leaf16/radix4/hash-width behavior is unchanged.

## Systematic v22 call-site inventory

AST enumeration found six direct _ExecutionState constructors:
-15104 resolver entry: prepared exact dict, parent/lexical locals/mode supplied.
-15111 plain-Mapping _fork_values: no parent, original full transfers remain.
-18613 registered helper environment: empty dict, inherited authority/bindings only.
-21968 empty merge: empty dict, resolver-selected mode.
-25530 review body: entry_values or{}, exact-parent shortcut possible.
-26037 local-helper body: ordered filtered-parent dict; omissions do not delete cells.

There are72 _fork_values call sites, all through15109..15111; keep each untouched.
State copy14869 keeps a fresh wrapper/cursor and authority/binding forks.
Constructor14686..14726 retains local iterable capture once, duplicate allocation
order, parent budget/mode/meter, inherited Entry identity and no-local shortcut.

Five raw _project calls:14853/14855 update;15147 captured-cell hydration;
19101 activation arguments;19165 caller refresh. One raw-pop19098.
These stay raw, pending even for identical-object writes, with no new transfer
or captured-cell deletion. The five calls and pop method are unchanged.

Fourteen state-capable update callers:16520,17404,17418,18260,18625,18698,
19766,19802,23269,23282,23320,23369,23419,23462.
Iterable overlays remain semantic; state update14839 snapshots first, adopts
authority/bindings, preserves destination-only order, and uses raw overlays.
Empty destination shares a sealed version through a new cursor.
Foreign-meter nonempty rebuild stays on its existing path; no foreign history.
15042 is a pre-entry builtin-dict update and remains unchanged.
Authority-only adoptions19157 and23738 remain untouched.

Two current _transferred_name_entry callers:14801 normal setter,22036 sparse merge.
Two current _write_cells callers:14809 normal setter,22043 sparse bound-write pass.
New bulk producers will call these same protected helpers directly for the work
currently routed through normal setter. No call is omitted because values match.

## Two complete unique-build boundaries

A. Constructor after authority/binding/local setup and exact-parent shortcut.
Keep initial empty cursor on the selected existing meter because the transfer
helper reads that meter. Use direct bulk only for type(values) is dict or
type(values) is _ExecutionState. Those items have unique names in stable order.
Other Mapping implementations/subclasses retain the old per-entry setter loop,
so duplicates, custom item iterators and their prior behavior are not redefined.

The producer follows values.items() order. Each input performs the SAME local
membership and same-object parent Entry test. An inherited Entry preserves its
exact proof OR pending state, with no transfer/cell write. Every other value calls
_transferred_name_entry, validates the name, and performs every enabled binding
lookup and _write_cells in the existing per-name sequence. The producer emits
exact (name, Entry) tuples to _NameVersion.from_unique_entries.
Install the completed version through a fresh _NameCursor only on builder return.
An empty exact dict may retain the existing empty cursor; do not bulk-build empty
data merely to add another empty history/order object.

B. Full fallback _merge_states22020..22030.
Keep empty/singleton handling, initial fork, authority join, binding union,
compatibility/overlap/missing-cell checks and all input snapshots unchanged.
Keep exact builtin set().union(*key_views) construction and its iteration order.
Keep result.clear() before preparing names, so old name history is detached.
For each unique union name, preserve state.get input order, _merge_flow_values,
full _transferred_name_entry, name validation and every enabled strong/weak cell
write, including overlapping identities. Emit ordered (name, Entry) pairs and
install one completed direct-bulk version/cursor instead of per-name cursor writes.
Plain Mapping inputs stay plain; no extra conversion or transfer is introduced.
Disabled inputs still use this full path and remain pending; no inert certificate
is minted merely because disabled transfer returns its input.

The sparse path22033..22044 stays byte-identical: original callback, same pending/
changed normalization law, then EVERY participating distinct existing-cell write.
No new inputs enter sparse compatibility and no order fallback is relaxed.

## Why staged projection is sound, and its boundary

_transfer_authority14034..14083 and its recursion access only state.authority;
it does not read partially constructed names. _transferred_name_entry14772 reads
the same meter and four-fact certificate inputs. _write_cells14811 reads/writes
only authority.cells. _merge_flow_values uses supplied immutable FlowValues.
Constructor inheritance consults the separate parent, never partial self names.

Thus building the name index once can defer physical projection installation
while keeping ordered transfers, object registration and all cell effects.
No inter-name transfer/cell reordering is proposed. Name validation remains after
transfer and before cell writes. The unique-input proof rules out a later duplicate
reject changing successful behavior. The original objects/bindings/cells stay
fork-owned and all input versions stay immutable.

Failure atomicity remains the reviewed primitive's: no partial publication or
cache commit after failed bulk build. This does NOT invent rollback for whole
ExecutionState construction/authority effects; existing budget failures abort the
analysis. If a newly discovered caller observes partial self names during these
effects, stop and retain the old loop for that caller rather than weaken semantics.

## Honest producer and primitive cost

Forward every prototype charge unchanged. New producers charge actual source
visits, iterator/generator construction, yield tuple allocation and its two copied
references, inherited lookup/membership, input-value tuples and full builder/cursor
installation. Existing object/cell map charges stay at their current methods.
Full merge explicitly charges its actual per-state value-tuple traversal/references,
rather than hiding producer work behind a single bulk call.
No intermediate prepared list/dict or per-name immutable-set chain is constructed.
The bulk primitive itself performs all uniqueness attempts, key/hash/routing,
record/reference copies, pending/index/order/history construction and memo work.

Existing upstream resolver alias/local/module preparation and local-helper filtered
dict comprehension remain unchanged and are not claimed removed. Their existing
cost plus the new input traversal remains part of eventual whole-generator evidence.
General update/adoption is not repacked into another bulk operation in this round.

## Release checks and falsifiers

Issue create-only v24, exact v22 delta, full r010 diff, inverse checks, namespacing
map and static call/mutation inventory. Protect complete _AnalysisBudget,
all five caps, _transfer_authority, _write_cells, _transferred_name_entry,
_FlowValue, every authority store, all non-constructor ExecutionState methods,
and all resolver methods except the narrow full-fallback body.
Prove sparse merge and class/helper/exception/recursive code unchanged.

No production fitness follows from558 primitive checks: largest growing total
was217378/262144. Frequent real forks, many pending values, ordered materialization,
1050-helper declaration growth and70-generator preflight remain unproven workloads.
Root inspects exact candidate before any payload. A cap failure, changed semantic
result, lost witness, changed primitive AST or unaccounted producer work stops the
round for diagnosis; it does not authorize threshold tuning, discounts or v23 merge.
