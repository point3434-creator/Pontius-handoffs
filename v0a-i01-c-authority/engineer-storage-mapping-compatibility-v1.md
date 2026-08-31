# Engineering inventory: execution-state mapping compatibility

Date: 2026-08-31.
Status: engineering inspection only; not a cold review, acceptance verdict, frozen
candidate, capability approval, or production-integration authorization.
Reviewer: Codex mapping_compatibility subagent.
The reviewer received the storage design and cannot count as a future cold reviewer.

## Target and identity

Target working file:
D:/Pontius-worktrees/codex-v0a-i01-c-authority-v1/tools/generate_test_inventory.py

Predecessor: v19.
Independently read SHA-256:
3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1

All line numbers below refer to those exact predecessor bytes. This working-file
identity is not a frozen candidate commit/manifest pair.

Question: identify consumers that constrain replacing the dict-subclass
_ExecutionState with persistent immutable name versions and a MutableMapping
adapter. Preserve exact iteration order, transfer timing, raw projection behavior,
state overlay, authority adoption, and cell-write semantics.

Applicable process inputs: D:/Pontius/CLAUDE.md and D:/Pontius/docs/workflow.md.
Engineering design inputs:
engineer-environment-implementation-plan-v1.md and
coordinator-storage-disposition-v1.md in this handoff directory.

## Discovery method and limits

Read-only searches used rg over the complete generator for dictionary base-class
calls, dict constructors/type checks, Mapping checks, items/values/keys,
update/clear/copy/pop/setdefault/popitem, state identities and downstream call-state
consumers. Nearby function bodies were read to trace whether iteration mutates the
same name map, a separate fork, authority stores, or unrelated auxiliary state.

A standalone stdlib ast/pathlib/hashlib script parsed source bytes without importing
or executing the generator. It enumerated candidate mapping-method call sites and
recomputed the pinned SHA-256. The successful parser invocation used:
D:/Pontius-tools/py311/Scripts/python.exe -B -P -

An earlier parser-path attempt named the nonexistent py311/python.exe and did not
execute. A Git status read was refused for dubious ownership; no Git configuration
was changed and this inventory makes no clean-working-tree claim.

The inventory covers production consumers in this generator. It does not establish
behavior of external/private callers, arbitrary user-defined Mapping implementations,
reentrant instrumentation, concurrent mutations, or future consumers. No payload
imports, tests, analyzer execution, production edits, or commits were performed.
This report itself is the sole subsequently authorized write.

## Findings: iteration and Mapping consumers

No inspected production name-map consumer both advances a live values/items
iterator and overwrites that same name map. Snapshot-returning items/values would
be observationally safe at these sites if their order and captured values match.
This is a bounded source finding, not blanket permission to weaken the adapter's
Mapping/view contract.

1. Explicit snapshot mutation loops:
   15488, 16255, 16313, 16560, 16917, 17009, 17472, 18320,
   20932, 20958, 20978, 22411.
   Each already uses tuple(...items()) before replacing values in that map.
   Preserve the captured values; do not substitute later live replacements.

2. First-match alias scans:
   16703, 16717, 16878, 16924, 17510, 17572.
   Exact values iteration order determines which alias wins. There is no mutation
   of the scanned map while that scan advances. The local map is a distinct fork.
   The accepted identity-None guards at 16700, 16714, 17507 and 17569 do not authorize
   changing non-None alias selection.

3. Other direct items/values scans:
   13397, 13417, 14103, 16852, 17873, 17932, 23079, 25326.
   These are snapshot-safe as currently written. The constructor at 14103 writes a
   different destination. The invalidation called at 17873 changes
   invalid_helper_owners, not the iterated name map. The update fed by 17932 writes
   a separate environment. The filtered downstream call-state comprehension at
   25326 is read-only.

4. Key union at 21285:
   Preserve the actual legacy set().union(*(state.keys() for state in states))
   ordering. Sorted keys, tree order, and an insertion-ordered union are not
   equivalent substitutions. No state keys-view set algebra beyond this consumer
   was found.

5. Ordinary dictionary receiver at 14348:
   self.values is still a plain dict and executes update(entry_values or {}),
   where entry_values may be an _ExecutionState. The adapter must work as a
   Mapping source through keys/getitem and preserve source key order.
   Conversion to _ExecutionState occurs at 14410.

No saved state view, runtime dict-type restriction on an execution state, or
state popitem/union API consumer was found. Other dict type tests and analyzed
Python dict-method names in the file are unrelated to execution-state storage.

## Dictionary bypasses and fork

Internal dictionary seams in _ExecutionState:
14096 (__init__), 14108 and 14122 (__setitem__), 14137 (__delitem__),
14162 (update), 14174 (clear), 14177 (__new__), 14178 (__init__).

External bypasses:
14453 (captured-cell raw hydration);
18404 (projection-only pop);
18407 (raw parameter binding);
18471 (post-helper raw cell projection);
21316 (raw merge-result clear);
21326 (raw installation after an explicit transfer).

These calls cannot operate on a non-dict adapter unchanged. Their replacement must
preserve whether transfer and semantic cell writes were deliberately bypassed.

copy at 14176-14181, consumed by _fork_values at 14415-14417, copies the name
projection and forks authority/bindings without per-name semantic assignment.
A generic MutableMapping implementation does not provide this complete contract.

String constants at 15981-15988 describe analyzed Python dict methods; they are
not state-storage bypasses and should remain unchanged.

## Update, deletion and adoption

State-to-state update at 14158-14165 overlays names while replacing the destination
authority and bindings with forks of the supplied state. Destination-only names
remain. Existing keys keep destination positions; new supplied keys append in
supplied order. Supplied entries are installed raw without transfer or cell writes;
keyword entries, if present, still use semantic assignment.

The concrete nonempty overlay consumer is probe.values.update(environment) at
18004. Constructor-created names absent from environment must survive. This must
not be implemented as unconditional whole-name-version replacement.

Generic iterable updates at 16710, 16724, 17566 and 17931 deliberately use
semantic assignment, including transfer and participating cell writes.

The following clear/update pairs are replacement paths, not nonempty overlays:
15825/15826, 19071/19072, 19107/19108, 22556/22557, 22569/22570,
22607/22608, 22656/22657, 22706/22707, 22749/22750.

clear at 14172-14174, including terminal clear at 15828, removes the projection
without performing Python semantic deletes or unbinding cells. Generic
MutableMapping.clear would need overriding because deletion-based clearing would
change this behavior.

Handler-alias pops at 21588 and 21590 are semantic deletion and must update cells.
Raw projection removal at 18404 must not update cells. The explicit state pop
implementation also controls the missing-name result; current consumers pass None.

Authority-only adoption at 18463 and 23026 must leave the name projection intact.
Raw hydration/projection at 14453 and 18471 and argument injection at 18407 must
preserve their existing transfer timing; a normalizing lookup is not equivalent.
Constructor inherited-value handling at 14104-14108 also deliberately installs
exact inherited values without another transfer.

## Residual hazards and required boundaries

- A retained view, or value overwrite between iterator advances, distinguishes a
  live dict view from a tuple snapshot. Current production sites do not establish
  a need for that behavior, but snapshot behavior is not full dict compatibility.
  Any broader adapter promise requires its own explicit compatibility evidence.
- Cached ordered pairs must match the correct version. Explicit tuple snapshots
  capture old values; a live view, if exposed, must not silently freeze old values.
- Default MutableMapping update/clear behavior does not preserve this state's
  specialized authority adoption, raw replacement, and semantic-deletion split.
- The remaining dict[...] annotations are static typing debt after a class-base
  change, not a discovered runtime dict-only constraint.
- This audit does not prove ordering across interpreters/hash seeds, normalization
  soundness, budget accounting, structural savings, or public analyzer behavior.

## Verdict

Defect verdict: no additional demonstrated production compatibility defect was
established by this static inventory beyond the explicitly identified replacement
seams. This is not CLEAN or an executable behavioral pass.

Design verdict: SOUND, conditional on preserving the listed ownership, ordering,
overlay, view and raw-operation boundaries. The current production consumers do
not force a live-view implementation, but this does not waive the accepted
prototype compatibility checks or subsequent public-boundary verification.
