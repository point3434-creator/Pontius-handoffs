# R1 Task5 semantic engineering review v1

Reviewer: codex/cold_review_a, acting as an engineering participant and prior test author.
Disposition: HOLD the frozen v1 for the two source-proved public semantic gaps below. This is not a cold review, runtime failure report, passing Gate A result, or implementation CLEAN. Root owns all payload dispatch.

## Exact target and independent inspection

- H commit: d224ea401898e462b327c43f129822dd52168782.
- Manifest: rewrite-r1-task5-source-v1-manifest.sha256, SHA256 afc26d19bf76e44694b4e88254946aa2607bf4ece45965098a67ff946e148401.
- Task5 source: rewrite-r1-task5-source-v1.py, SHA256 810cbb934e20a13c9c4794e3574bcb6a248ddc8b4a84a56045f6370c1a066cea, 1162622 bytes.
- Prior Task4 source: SHA256 3511f60a62fc9588f153ba3db6b05ac228a1ce235cb23a5316000ce7ba4e550c.
- Prior semantic reviews: Task3 623015f010c066784b13b11c35c3f17ce1918fdfa57c48fcaa917dc21ee834d1; Task4 acc373e272a438bc9c8ce88a33ed90149c640c8f613e26c5016238e4ef6f004e.
- Additional binder scope disposition remains c12b0455954e90e3ee4f9ecaba888079002c6374aa85615439a9e959228bea37.
- Controlling rewrite design: 701552c177840e4c5c0dd9c5985776256af5b31e7e997067dd662638a67c3ca8; R1 plan 18f8124432880016d6dd0690ed4d3b582b8e202c5bdda21ae48a65efa0ae521d; early population 3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce.

Read-only owner-context Git cat-file inspection verified the exact manifest and all fourteen listed H blobs against local bytes. A stdlib-only AST/hash script under actual Python3.11.15 -I -S -B -P independently compared Task4 and Task5. New helpers are _c_sink, _c_emit_sink and _c_review_outcomes; the old dispatcher is preserved exactly under _legacy_process_review_rows_r010. Changed prior definitions are _CCallObservation, _c_call, _c_delete, _c_eval, _c_eval_dict, _c_invoke, _c_read_name, _c_statement, _c_truth and _process_review_rows. All other module AST, including the public derive_design_review function, is exact.

The independently derived unified diff (headers Task4-v1 and Task5-v1) hashes to ea059f59eb808054c257fa7318218ae9a8fbf2d5e8f80fc4956e459ad1d16bc3. The initial comparison script incorrectly assumed the replaced dispatcher stayed at its old module position; correcting only that static comparison made the preservation assertion succeed. That script failure was not a product result.

No candidate, Model, sensitive fixture, source checker or test was imported or executed. No source/test/generated/ledger bytes were changed. Line anchors below refer to the frozen Task5 file unless explicitly called r010 or original tests.

## Required corrections

### 1. Manufactured unittest entry bypasses unproved receiver/framework protocols

At 10999-11040 preflight verifies class origin, selected function, direct-entry census, signature and only setUp/tearDown/setUpClass/tearDownClass. At 11045-11055 it allocates _CInstance directly, reads the selected class member and invokes it. Explicit user-defined constructor, attribute and runner protocols can otherwise be accepted as ordinary class functions at construction.

This bypass is semantic, not merely a future cross-module concern. Python entry construction and dispatch may reach __new__/__init__, custom attribute access or writes, __call__/run/debug, internal _call* dispatch and cleanup/default-result hooks before or around the selected body. A helper with effects reachable from such a hook is not represented by a direct body invocation, and v1 does not refuse the entry for the missing semantics. The finding is proved by the source route; no new unsafe runtime witness was authored or run.

Required bounded repair: before manufacturing a receiver, explicitly refuse a reached review entry with a user-defined protocol/framework surface the core cannot account for. A compact guard over explicit class namespace members can reject any dunder spelling plus a frozen union of unittest.TestCase class names and lifecycle instance-reserved fields from the two actual supported interpreter sources. Do not treat arbitrary user helper names or local variables as framework names. Do not extend the guard to blanket refusal of dormant local classes. The exact prospective source-derived union is a separate artifact and approval, not silently part of this frozen v1.

Category support:
- r010 _IMPLICIT_PROTOCOL_METHODS at 12523-12545 includes attribute-load hooks __getattribute__/__getattr__/__get__, store hooks __setattr__/__set__, delete hooks __delattr__/__delete__, and __call__.
- r010 namespace certificates at 22734-22795 exclude dynamic __getattribute__/__getattr__ classes from the supported class proof. Entry preflight at 25491-25674 covers entry decorators/signatures/defaults, properties and setup writes. The old source is an admission-category reference, not a proposed live fallback.
- Original tests 14615-14662 and 15213-15272 require constructor/protocol effects to be covered or refused; 15561-15582 covers aliased construction; 15608-15628 prevents assuming __init__ after a foreign __new__ result. The clean dormant-construction control at 15537-15559 remains binding. Invalid entry signatures at 15519-15535 already require explicit refusal.

Non-stable module fixture roots deliberately refused at 10990-10992 are a separate R1 scope boundary. Their refusal does not establish safety of a stable unittest item whose manufactured receiver has custom entry hooks.

### 2. Subprocess observation fabricates a literal None result

_c_sink at 10769-10771 emits the sink observation but calls _c_out with no value. _c_out at 9871-9872 turns that absence into a literal None atom. The accepted subprocess functions do not establish this result: run returns a process result object, call/check_call integer status, and check_output bytes. Popen is present in the symbolic set, but the retained terminal policy currently refuses its timeout contract; this finding does not depend on admitting Popen.

The existing identity comparison at 10289-10299 can therefore prove an incorrect branch after an otherwise representable subprocess call. Assignment, return forwarding and later conditional execution can consume the invented fact and omit reachable effects while the first sink row remains clean. This is source proof, not a claimed executed false negative.

Required bounded repair: retain the exact sink observation, but use an unproved result value unless a supported return fact has independently been established. Reached use that needs such a fact must explicitly refuse. Discarding the result need not refuse; no CompletedProcess model or general subprocess protocol execution is required.

## Closed prior source categories and public path

- Destination read/delete handling: _c_read_name 9903 onward and _c_delete 10074 onward distinguish an absent retained cell (refusal), unbound current activation (UnboundLocalError), and free/module/class absence (NameError). Deletion checks absence before writing unbound/removing a name. Unsupported destinations retain refusal. This closes the earlier silent delete-success category in the admitted paths; no handler-precision extension is inferred.
- Truth: _c_truth reads current canonical sequence contents or exact supported literal atoms; If and not refuse an unproved truth protocol. Task3's implicit protocol omission is closed by refusal. In particular, open self.choice in the joined Gate A witnesses may be refused before either branch; that is not evidence that their join mechanics have executed.
- Sequential failure: import aliases now carry abrupt outcomes without performing later aliases. Dictionary expansion is checked at its actual key/expansion boundary, with current mapping state and prior effects retained. Unsupported starred arguments and keyword expansion refuse after the corresponding earlier operands and before later keyword operands. This closes the reviewed Task3 category without asserting general expansion support.
- Historical calls: _c_call snapshots state after operand evaluation and records the selected callee, captured arguments/defaults and caller frame. _c_review_outcomes reads the selected function from event.entry, not final names/current projections. Helper completion snapshots remain paired with outcome controls/issues. No old FlowValue authority is reconstructed.
- Return/effect pairing remains canonical; classes use a separate namespace and lexical captures; current aliases address the same canonical object/cell records. Task5 introduces no alternate legacy semantic interpreter. Same-file explicit helper globals retain the defining module; newly reached cross-module helper invocation explicitly refuses at 10664-10665.
- Helper depth: invocation restores the original InventoryError text at 10660-10661. The synthetic selected test adds the initial helper-path element, so direct test sink depth is zero, the first helper sink depth one, sixty-four nested helper entries are allowed, and the sixty-fifth is refused before its body. Recursive calls share ctx.budget. This is the static mapping, not a tested depth/budget result.

## Terminal evidence, occurrences and source-census limits

derive_design_review at 28219 now resolves the new _process_review_rows dispatcher. It constructs canonical module/preflight/body roots; stable entries that lack admitted canonical structure explicitly refuse. The renamed legacy dispatcher is not a rescue path.

The only terminal policy reuse from _c_emit_sink is detached exact argv/keywords/environment data plus empty aliases/assignments and an empty _ExecutionScopeVisitor never visited. The sink rejects every '-c' token at 10743-10744; therefore _process_definition's legacy child-analysis branch at 25719 is unreachable from this adapter. Captured environment bypasses legacy environment analysis. Its remaining literal policy/normalization/hash helpers do not receive live canonical state. This is a narrow R1 terminal boundary, not permission to admit a dynamic child or reconnect old resolver evaluation.

Trace traversal is per outcome. Shared trace prefixes are deduplicated by trace identity inside that outcome, not by source line; separately generated repeated sink events contribute repeated occurrences. Counts greater than one refuse unrepresentable multiplicity. Complete normal alternatives compare exact capability sets instead of treating differing definitions as sequential calls. These are source checks; no repeated-call or alternative payload ran.

_c_call 10584-10592 independently requires every nonsynthetic reached call to belong to its static scope sites. The later disposition pass at 10907-10919 has narrower evidentiary standing: an arbitrary global blocker labels all other sites 'blocked', and otherwise unseen sites are labeled 'proved_unreachable'. Moreover module calls are excluded from observed_calls at 10847-10849 even though their scopes can be recorded; actually reached module call nodes can receive that unreachable label. The labels are internal and not returned publicly. They must not be advertised as an independent semantic proof of every static site's reachability. Correct the label/classification or explicitly narrow the claim; this does not require another live-state interpreter or new fixture population.

R1 still refuses unimplemented reached syntax and unsupported entry kinds. Full class/comprehension/generator, exception-handler and later R2/R3 compatibility requirements are not declared complete by this source pass. Whole-operation metering and all Gate A runtime acceptance remain separate root-owned checks; this semantic report does not certify their closure.
