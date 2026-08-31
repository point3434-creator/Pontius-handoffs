# v22 cursor candidate: static correction and source return

Status: T-only candidate ready for coordinator source review. No W installation,
candidate import, candidate execution, repository test, generated-file write, or
commit was performed. v21 remains retained, never installed or executed; v22
supersedes it only as the proposed candidate. W remains exact v20.

## Authority and correction

This follows coordinator-name-cursor-candidate-disposition-v1.md
(8cabe43873bddfc7871ff671c96eec85fccfc29cf774dd3c748167fc9dabae21),
the accepted adapter proposal, and the coordinator's explicit instruction to
retain v21 and issue v22 with exactly two restored name checks.

Static inspection found a private/public primitive boundary mistake before
execution: public cursor.set validates names, while private cursor._replace_entry
expects the caller to supply an already validated name. The production adapter
has two direct installations, inherited constructor entries and semantic setter
entries. v21 had omitted the original adapter name validation at those seams.

v22 adds only _name_check_name(name) immediately before each of those two
installations. The setter still performs the full transfer/certification first,
then name validation, installation, and all original strong/weak cell writes.
The inherited constructor path retains the exact parent's Entry proof or pending
debt and validates the name before installation. No primitive declaration changes.

The direct-install category was enumerated from all _replace_entry calls and
all adapter raw/semantic accesses. Primitive join installation consumes names
already validated in immutable input versions. Raw set/delete retain public
primitive validation. General item/contains/get reads retain their original
checks. The correction does not strengthen the prototype's ordinary string
comparison contract or add a str-subclass exclusion.

## Port and preservation

The production transplant retains the reviewed prototype's immutable NameVersion,
owned NameCursor, sealed delta dictionaries, names-only history/order recipes,
eight-layer structural compaction, and staged snapshot/ordered-read publication.
Only identifier names are adapted; Attribute.attr, strings, slots, and declaration
AST bodies remain exact. Existing production _NameMeter is unchanged and delegates
the original _AnalysisBudget.consume; no production cap is changed.

The adapter captures arbitrary local_names exactly once, retains local order and
duplicates for original allocation semantics, and uses the exact-parent/empty-local
shortcut only. Construction otherwise uses a private cursor. Forks publish through
the reviewed primitive. State adoption captures the source before destination
mutation, including self-update; foreign-meter history is not reused. Raw same-value
writes remain pending. Authority-only adoption sites remain untouched.

Full merge fallbacks keep the literal legacy set-union order and every flow merge,
full transfer, name validation, and cell write; plain Mapping inputs remain plain.
Compatible sparse joins receive sealed input snapshots. Only existing distinct
participating cells permit delayed writes; overlap/missing-cell cases keep fallback.
No disabled-mode exception is introduced. Frequent forks, retained order/history,
compaction, and terminal materialization remain metered work.

Static verification uses stdlib parsing and canonical AST comparisons only.
The exact inverse of the three authorized replacement regions recovers v20 bytes.
All namespaced prototype declarations are AST-exact. _AnalysisBudget, full
_transfer_authority, old authority/observation stores, _FlowValue, _NameMeter,
cell(), _write_cells(), _transferred_name_entry(), pop(), setdefault(), values(),
and all five admission caps are unchanged. Restoring only the old _merge_states
node makes the entire resolver AST identical to v20: class/helper effects,
rebinding, recursion, exceptions, and unrelated interpreter logic are unchanged.
All 1,761 tracked W files were hashed before and after and are byte-identical.

The immediate predecessor proof additionally asserts v22 equals v21 plus precisely
two insertion lines, with no removal or other changed byte.

## Evidence limits and ownership

The earlier 372 successful primitive checks support storage compatibility and
failure staging only. No production correctness, corpus budget fitness, latency,
or completion claim follows from this static candidate. Existing design/matrix,
composition, structural-cost and ordinary-generation gates remain coordinator work.
The separate class-body adoption blocker found on v19 is intentionally unchanged.

No W source lease was taken. The coordinator owns installation and further runs.
Candidate/source ownership is returned for review; no further edits are in flight.

## Exact artifact pins

- `engineer-generator-v20.py`: `e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679`.
- `engineer-generator-v21.py`: `181993a34985a7eaa045744f662be20b9cee3b2e3c63752af15810ea47ef7ff6`.
- `engineer-generator-v22.py`: `61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3`.
- `engineer-generator-v22.diff`: `6b48562cdf792b6d1acccc98dc3cb4b896488db9ca7d15357e919aa7ac03d070`.
- `engineer-generator-v22-from-v20.diff`: `ddd2a5f46ea045fd792655bc95b9a0952da9059b211065ca60653e4441e66d26`.
- `engineer-generator-v22-from-v21.diff`: `a5596dc2f3fc19cf94b7f565a711468de9c6a79c275c9cb1da2ed9f7fa60e287`.
- `engineer-name-cursor-v22-namespacing.json`: `82d680741a124658627b838999fb28d96a11813637a8297c845e0b2ba2e2bd69`.
- `engineer-checks/v22-cursor-candidate-static.json`: `8fd6a7c28aa57c3c9841ad6a33253af1d7261fde57f7bce41b97f215c19e43c0`.
- `engineer-build-cursor-candidate-v22.py`: `52de7cb41c68900b85386366ac20d73ba97e98f049bf192347f54baad6bce7ac`.

## Candidate source anchors

- `_NameMeter`: line 14086.
- `_name_check_name`: line 14107.
- `_NameVersion`: line 14372.
- `_NameCursor`: line 14471.
- `_join_name_versions`: line 14605.
- `_ExecutionState`: line 14682.
- `_ExecutionState.__init__`: line 14685.
- `_ExecutionState._transferred_name_entry`: line 14772.
- `_ExecutionState._project`: line 14789.
- `_ExecutionState._project_pop`: line 14793.
- `_ExecutionState.__setitem__`: line 14800.
- `_ExecutionState.__delitem__`: line 14817.
- `_ExecutionState.update`: line 14839.
- `_ExecutionState.clear`: line 14865.
- `_ExecutionState.copy`: line 14869.
- `_SourceOrderedResolver`: line 14903.
- `_SourceOrderedResolver.__init__`: line 14904.
- `_SourceOrderedResolver._merge_states`: line 21963.
