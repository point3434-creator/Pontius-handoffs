# v24 storage-only candidate handoff v1

Authoring is complete. This is a retained engineering candidate for coordinator
inspection, not a cold verdict, production-fit claim or execution permission.
The author ran only static source/data/hash checks. No candidate, prototype,
test, Model or generator payload was imported or executed. No run configuration,
W edit, generated/test change or semantic-v23 merge was made.

## Exact artifacts

All paths are under D:/Pontius-handoffs/v0a-i01-c-authority.

- engineer-generator-v24-storage.py: 1,150,388 bytes; SHA-256
  156ee88a99abb26edeaaf178841c72e89f2bdc15696c37ef91f4dcc54b767431
- engineer-generator-v24-storage-from-v22.diff:
  891d9efa90db1428fe96fb56eca40a5da7271c843f4c603e614de90b94ea71f2
- engineer-generator-v24-storage-from-r010.diff:
  ea618b085802781132f97718234f3a4dc44d6d6a0ce21334619b47ffc9b5f7a8
- engineer-generator-v24-storage-namespacing-v1.json:
  39858fc73cdd3b2279184de3838f1d70533aacc9d382a477494caf39bf07c38a
- engineer-generator-v24-storage-static-v1.json:
  1ba6352dc8a7130f361ef962cdee7816d348c3322bb6c4179b56de2a41dca29e

Exact predecessor v22:
61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3.
Exact reviewed radix prototype:
0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71.
Approved adapter plan:
3c75c841feaabdd15f1bcce99b729746d9f6e463f41c09eeb76da72a0622a819.
Root experiment disposition:
bb293b7112f7d833aff1b8c72d134ae53d998bce5930c41a393dd930ff943d1e.
r010 source was read via Git and verified to
29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692.

## Implementation and review anchors

Name primitives begin at14098. Forty-one definitions and six constants are copied
from the prototype by token-only identifier namespacing. Their canonical ASTs,
including a reverse-namespacing comparison, are exact. New nodes are
_NameRadixLeaf14132, _NameRadixBranch14137, _NameLeafEdit14142,
_NameBranchEdit14150. Bulk API is _NameVersion.from_unique_entries14626.
All _name_radix_* helpers retain prototype charges, thresholds, order/memo,
collision, pending metadata, lifetime and failed-publication semantics.
_NameMeter still delegates to the original _AnalysisBudget.consume unchanged.
No separate prototype Meter, BudgetExceeded or MAXIMUM_WORK is installed.

Constructor14933 keeps the complete prior setup/local capture/allocation and
exact-parent shortcut. Only after that shortcut, exact dict/exact _ExecutionState
inputs can use the new complete build. An empty input keeps the existing empty
cursor. Other Mapping inputs/subclasses run the exact previous loop.
constructor_entries14970 repeats the same parent lookup and same-object test.
Inherited Entries retain exact proof OR pending debt. Other entries execute full
transfer/certification, name validation and all current enabled binding/cell
writes. A completed bulk version becomes a new cursor at15001.

Full-fallback merged_entries22322 follows the unchanged builtin union-name order
and unchanged name_inputs ordering. Every name still merges its supplied values,
performs full transfer/certification, validates the name and performs every
strong/weak bound-cell write, including overlap. The completed version is
installed at22346. Physical intermediate per-name cursor insertion is removed;
no transfer/cell helper reads that partial projection.
The sparse merge suffix, compatibility plan, all original prefix work,
plain-Mapping handling and empty/singleton paths remain exact.

General semantic setters, raw projections/deletion, update/adoption, clear,
copy, values/keys/items and all other ExecutionState methods are unchanged.
All resolver methods except the narrow full-fallback body are byte-identical.
The separate class/exception/helper/recursive/rebinding semantics remain v22,
including its known class defects.

## Metering

Both producers charge actual source iterator/function/generator creation,
yield tuple allocation and its two references. Their five captured variables
are checked from compile-without-exec code metadata and charged for the retained
function/generator context. Constructor parent lookups, existing item visits,
local membership and all transfer/cell operations retain their original charges.
A dict items view and direct dict size read are charged only when performed.

Full merge charges its new value-generator/iterator/context and the actual
per-state tuple allocation, visits and copied references before the primitive.
The primitive then charges its own distinct input visits, validation, unique
order dictionary, records, hash/routing, pending/index/history/memo construction.
The final independent cursor and its destination reference are charged.
No unmetered preparatory list/dictionary or per-name immutable-set chain is used.

These are semantic storage-work units, not allocator-perfect accounting or CPU
instructions. Internal C dictionary equality probes remain separate from logical
attempt charges, as in the reviewed prototype. Removed layer/old private-insert
charges correspond to work no longer performed; no refund or exemption exists.

## Static evidence

- Source parses and compiles without execution; LF/no BOM.
- All41 primitive definitions and6 constants match the prototype canonically.
-465 protected definitions match v22, including all authority stores, _FlowValue,
  _AnalysisBudget, _NameMeter, _transfer_authority, _transferred_name_entry and
  _write_cells. All five analysis caps remain64/4/4096/2147483647/262144.
- Generic constructor loop and setup prefix are exact; both inherited parent
  lookup blocks have the original AST. Sparse merge suffix/prefix are exact.
- Reversing the three bounded source replacements recovers exact v22 bytes.
- Call inventory:6 constructors,72 forks,5 raw projections,1 raw pop unchanged;
 4 transfer-helper calls and4 cell-write calls include the2 new producers;
  exactly2 direct bulk calls.
- All1761 tracked W paths were hashed before/after and remain unchanged. W source
  remains e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679.
- Original candidate/prototype/plan pins were rechecked before create-only release.

## Outstanding validation and limits

Root must inspect this exact source before payload execution. The558 pure
primitive checks establish only the reviewed storage experiment, not adapter or
whole-generator fitness. Largest primitive growing total217378/262144 leaves
1050-helper declarations,70-generator preflight, frequent real forks and corpus
budgets unproven. Existing upstream resolver preparation is not claimed removed.
Whole-state authority-effect rollback is not newly promised; unchanged budget
failures abort analysis. No threshold, cap, disabled-mode discount or semantic
expectation was altered. Stop and diagnose any real supported-workload failure.
