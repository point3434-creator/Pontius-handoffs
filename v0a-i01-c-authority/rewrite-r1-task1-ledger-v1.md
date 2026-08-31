# R1 Task1 checkpoint and charge ledger v1

Engineering checkpoint only. Source GO followed the exact floor RED; no candidate
or primitive payload has run. Task1 adds451 lines and deletes0. Public evaluator,
binder, _AnalysisBudget and all five caps remain byte/AST unchanged. There are2049
lines left in the2500 added-plus-deleted first-attempt boundary. Tasks2-5 are held
for root/cost inspection.

Source: rewrite-r1-task1-source-v1.py
SHA256 ff889b1ee3595d23d2109d15d87f80d8f5c153b3db524aaef3eb53b1797dcab1.
Diff: rewrite-r1-task1-from-r010-v1.diff
SHA256 bdd2b7a0cd7c4985b26290e2a19592d6496e4ffa01607a316ab0bd32fb5438f1.
Exact insertion: rewrite-r1-task1-insertion-v1.txt
SHA256 e4260d423bc6fa5d7a66c527f30dd87cfb3be86392d01967bbac5c40cf23cd3c.

Plan/disposition:18f8124432880016d6dd0690ed4d3b582b8e202c5bdda21ae48a65efa0ae521d /
64fbb4b0690d5555c6eebd7b96d0e8129115df01d44c4441e95cb8d98dd177a8.
Baseline311 receipt:a9bddbae63bf96bfa85a853ada42e0dde8a9f4a27c785a8f4c08c38ce33c8529;
root verification:954ee9a908033e0c43d8c7588837e3588398174f3a9e67c034469fa11fe6bc80.
Two class-adoption semantic failures; no baseline314 was dispatched after RED.

## Implemented boundary

New types9079-9295 distinguish atoms/references/choices, lexical activation cells,
scope/capture/frame data, canonical object variants, COW tables, read-only views,
tagged outcomes, call/sink observations and predecessor trace nodes. Dataclass
equality is disabled. Missing managed objects/cells return None to the later
typed read boundary; they do not fabricate an unmanaged value or new cell.

Only _CContext stores an operation budget. Tables, banks, views, records and arena
cannot select a construction-time budget. Every primitive receives current ctx.
The shared arena is not copied by fork; activation, object and version identities
come from that source. Snapshot/fork replace the parent's write token; every
previously owned table AND activation bank therefore loses write ownership.
Table wrappers are frozen and never retagged; detachment allocates a new
dictionary/wrapper/token association. A child write cannot update a snapshot's
shared bank in place.

Records with Mapping fields are required to use owned immutable mappings from
_c_frozen_map when the constructing operations are added. Record construction
and their field/reference charges remain the responsibility of those future
operations; _c_new_object/_c_object_write explicitly charge insertion/replacement,
not an already-constructed record a second time. There are no such evaluator
callers yet. This is an obligation for Tasks2-5, not claimed completed coverage.

## Exact charge sites

Counts below are semantic allocation/reference/visit units through the unchanged
consume/container methods. Fixed field checks are part of their operation's
visit; this is not a CPU-instruction or Python allocator benchmark.

| Source/helper | Charges and ownership |
| --- | --- |
|9298 _c_identity|2 for next serial and retained arena field. No new budget.|
|9305 _c_copy_dict|1+3n: new dictionary, n visits,2n key/value retained references. Uses built-in owned dict.copy.|
|9310 _c_frozen_map|Dictionary-copy cost plus2 for proxy allocation/dictionary reference.|
|9316 _c_state|Identity2 plus14: token1, two dictionaries2, two wrappers6, state5.|
|9323 _c_snapshot|6: view allocation+3 fields, token allocation, replaced parent token field. No value enumeration.|
|9330 _c_fork|8: two tokens, parent field replacement, new state+4 fields. Neither shared wrapper is mutated.|
|9339/9348 ownership detachment|1 comparison; if shared, dictionary3n+1 plus4 for new wrapper+2 fields and state field.|
|9357 _c_new_activation|1 scope check, two identities4, values dictionary+unbound atom5,4 per local visit/insertion/key/value, bank4, publication/version4; table detach separate. Only function scopes allocate lexical cells.|
|9380 _c_cell_read|1 activation lookup; if present,1 name lookup. Missing returns None.|
|9391 _c_cell_write|Activation/name checks1 each; table ownership/copy;1 bank ownership comparison; if shared bank,3n+1 dictionary copy and6 for bank/table replacement. Identity2 and3 for value update/new ref/version. No missing-name creation.|
|9415 _c_object_read|1 lookup; missing remains None.|
|9422 _c_new_object|Two identities4, reference2, ownership/copy, new key/value/insertion/version4. Caller separately charges record construction.|
|9435 _c_object_write|1 membership; ownership/copy; identity2; existing-ID update/new record ref/version3. Missing returns False.|
|9449 _c_value_key|Ref/symbol key3; literal key4; unknown/unbound key4 including identity integer. Exact scalar types remain in literal key; unknowns do not collapse by reason.|
|9463 _c_choice|Work list/set2; each supplied/alternative visit; singleton wrapper2 where needed; key construction; lookup1+key width; new set/list entries4+key width. Final tuple has n visits plus container(n), then choice2. Empty alternatives become unknown in this v1; root/cost review rejected that as fail-closed behavior. Approved v2 will raise InventoryError and remove the nonexistent atom charge.|
|9495 _c_trace|Node allocation+3 fields=4. Receives an existing immutable child tuple; its constructing caller owns that tuple's charge. No prefix walk.|
|9503 _c_trace_link|Pair tuple+two retained edges=3, then trace4; preserves predecessor links without copying prefixes.|
|9510 _c_join|List/set2; per outcome visit/id/probe3; unique set/list insertion/reference4; final tuple1+2n. Deduplicates only identical outcome objects and preserves order/state/result/issues.|

Copying at a call observation may detach an entire object table on the next
write. That cost is charged, not claimed sparse. GateB remains the later measure.
The cell-bank partition avoids rebuilding unrelated local-name contents, but
its outer table copy is still paid. Allocation/reference charges for the still
unimplemented scope/binder/call/evaluator constructors must be checked at their
actual call sites before evaluator issuance.

## Static verification and inspection focus

Actual3.11.15 with -I -S -B -P parsed source AST only. Removing the insertion
reproduced every original byte and AST; new names do not collide; no new budget
constructor or old resolver call appears in the inserted code. The initial
attempt used nonexistent py311/python.exe, so no static script ran then; the
correct py311/Scripts/python.exe command passed. No candidate import occurred.

Retained checker: rewrite-r1-task1-static-check-v1.py,
4a95152183d44896d652fd9bad5d9f61eae5ca338356fd257c901f8440f9c86a.
It records original Temp/W input paths; exact inputs are retained separately by
the pins above. The proof JSON records its command, exit and definition spans.

Root/cost should inspect token revocation across both table and bank levels,
current ctx selection,3n dictionary copies, mutation publication after charging,
arena reuse across forks, immutable record-constructor obligations, choice/key
work and trace predecessor edges. This source is frozen for that checkpoint;
no evaluator wiring, tests, payload or commit is authorized by this note.

Post-freeze source review identified the empty-choice API defect before wiring. This is a static contract correction, not an executed product RED. Root approved a separate v2; v1 bytes remain unchanged. The other16 protected paths were rehashed against coordinator-rewrite-r1-setup-v1.json and match r010.
