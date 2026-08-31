# R1 Task5 semantic closure review v2

Reviewer: codex/cold_review_a, acting as an engineering participant and prior test author.
Disposition: both v1 public semantic findings are closed by the bounded v2 source change. No introduced semantic blocker was found in this delta. No semantic objection to root-owned execution of the existing Gate A after the separate accounting/static/custody checks are satisfied. This is source-only engineering evidence, not a runtime pass, complete analyzer acceptance or cold implementation CLEAN.

## Frozen inputs and independent verification

- H commit: b1d15de062ac45c351f0254b358ee1e5fc35bdee.
- Manifest: rewrite-r1-task5-source-v2-manifest.sha256, SHA256 beb50fab0fe159249de1397529b78a71e2b176b8e3643ea64ccb37dbf1a1c15a.
- Source: rewrite-r1-task5-source-v2.py, SHA256 c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f, 1166485 bytes.
- Prior source: 810cbb934e20a13c9c4794e3574bcb6a248ddc8b4a84a56045f6370c1a066cea.
- Prior semantic review: rewrite-r1-task5-semantic-review-v1.md, 93f14ff8e628377ad121602033d78b861866b2e7283fbc8eb73f3a7c6457934a.
- Authorized correction disposition: bf45819fa1f8f95ce26a9b0a1df187bd9731350e3cb306a017a8aa94e05caed6.
- Eleven edit pairs: rewrite-r1-task5-edits-v2.json, d1be8b35c664f7cda35cb50e3053d605999c8a6c030ef362796ff9212def496e.
- Reserved-name table: 55ed71468da3c480e4805672b2b254e1bff5d6d0cf99a2c36ed0fbcfec202ceb; provenance note cc424e9f043ce7a195d0b37491fe99c6d61788a45d80e1dd0ae8a77659b348f0.
- Coordinator static result, retained as a separate input rather than reexecuted: 652488045b3cfac3901c4583b93f29da86e9ce0414926aea89c647ef324d4dcc.

Read-only Git cat-file inspection independently verified the manifest and all nineteen listed blobs against local immutable bytes and hashes. Own stdlib-only scripts under actual Python3.11.15 -I -S -B -P replayed all eleven replacements, requiring each original substring to occur exactly once; the resulting bytes exactly equal v2. The independently derived unified diff (headers Task5-v1 / Task5-v2) hashes to b87a1fd109f9d8d0f0fce6625d7a161b949af91d781093a1514adaf6673f5162.

AST comparison finds only _c_sink, _c_emit_sink and _process_review_rows changed. It finds three new helpers, _c_entry_namespace_supported, _c_extend_review_rows and _c_preflight_blocker, plus the frozen reserved-name constant. Replacing/removing those exact nodes reproduces the complete prior module AST. Literal AST extraction of the constant yields exactly the sorted 111-name table, without duplicates. No candidate/checker/Model/fixture/test was imported or executed. No production, test, generated, configuration or ledger bytes were changed.

All following line anchors refer to the exact v2 source.

## Closure matrix

| Requirement | Source evidence | Bounded result |
| --- | --- | --- |
| Do not manufacture a receiver while silently omitting customized entry protocols | _c_entry_namespace_supported 11062-11074; call at 11182-11185 before _CInstance allocation 11195 | Closed by explicit refusal |
| Preserve unproved subprocess result rather than inventing literal None | _c_sink 10769-10772 constructs unknown atom with reason and retains the same sink trace | Closed without a new return-object model |
| Preserve value uncertainty through forwarding and fact-dependent consumers | Existing cell/default/argument/return/reference paths and unchanged unknown consumers described below | No conversion back to proved None found |
| Keep new shared export/blocker helpers semantically equivalent | 11048-11059 and their exact module/item/preflight call sites | No semantic regression found; detailed accounting remains separate |
| Keep old semantic engine disconnected and source-census claims narrow | All unrelated AST is exact; v1 terminal-boundary proof still applies; disposition explicitly narrows internal labels | Preserved within R1 scope |

### Entry guard

The constant repeats the exact source-derived 111-name union. The guard iterates only namespace.members and rejects either a dunder spelling or membership in that frozen set. It does not depend on value identity, inferred harmless bodies, dynamic unittest introspection or fixture names. All four previously checked setup/teardown names remain included.

The guard is reached only after the selected stable item has a canonical unittest class and canonical direct function entry, and before the body budget, receiver allocation, method binding and invocation. Its failure creates a blocker and continues to the next item. Unsupported entry kinds and module fixture roots remain separately refused. Ordinary local class construction and arbitrary user helper/local names do not use the guard.

The canonical class namespace in this path starts separately and contains explicit constructed members. It does not enumerate a real Python class dictionary or inherited framework members, so generated class metadata and unmodified inherited TestCase methods are not mistaken for explicit user overrides. Previously unsupported custom bases/descriptors are not newly admitted by this change.

This closes the v1 bypass category with a conservative R1 entry refusal. It does not claim that every reserved name executes on every entry or that customization is universally unsafe.

### Unknown subprocess completion

At 10771-10772 the sink now returns an allocated unknown atom with reason "unproved subprocess result". The exact sink observation and source trace are retained. _c_out receives this real value, so its Python-None default path cannot turn it into a literal None.

The existing relevant paths retain the value:
- _c_store_name 10002-10016 installs the supplied atom unchanged in lexical cells or namespace storage; only actual Python None signifies deletion/unbound.
- _c_eval_many 9976-9999 retains operand references; _c_construct_function 10496-10521 captures evaluated default values; _c_invoke 10674-10718 uses selected argument/default values and returns explicit outcome values.
- Canonical sequence storage/extraction carries element values; _c_read_element 9963-9973 returns the stored atom without reconstructing it.
- Identity comparison 10278-10308 leaves unknown operands unproved, including either ordering against None. The existing If/not truth boundary refuses that unproved truth rather than selecting a branch.
- Member/subscript access, selected invocation and sink/environment/argv admission do not treat an unknown atom as a proved namespace, sequence, function, literal token or environment.

An ignored expression result remains admissible; ordinary function fallthrough still returns actual None, which is a distinct justified case. This correction does not promise precision for subprocess return objects or require blanket refusal merely for retaining or forwarding an unknown result.

### Shared helpers and failure order

_c_extend_review_rows performs the same list extension after charging the existing owning ctx budget. Module exports use the module ctx; item exports use the item body ctx. _c_preflight_blocker constructs the same item/path/node/reason row and appends it under the already existing preflight budget. The changed call sites preserve those inputs. No new budget, reset, refund, exception swallowing or semantic side path is introduced.

The terminal success/refusal result pairs now have an additional pre-return charge. Their values and policy decisions are unchanged. The helper-based charge changes may reach an unchanged cap earlier; that is a separately reviewed accounting/cost outcome, not permission to alter caps or semantic expectations.

## Limits carried forward

The nonsynthetic reached-call membership check remains intact. The later internal source labels remain coarse: they do not independently prove all per-site reachability, and module calls can be omitted from their observed set. The coordinator accepted narrowed evidentiary standing; no correction to this internal event model is claimed here.

The exact helper-depth text/convention, prior Task3 source-order corrections and detached terminal-policy boundary are unchanged from the v1 review. There is no new legacy resolver fallback in this delta. Gate A hidden-cell cases may explicitly refuse an unproved truth before a join; success on those expected refusals would not establish that the joined-cell mechanism executed.

Runtime behavior, complete original-cap accounting, population integrity and floor-before-development custody remain root-owned checks. This review ran none of them. The immutable Gate B missing-input-premise finding and broader R2/R3 requirements remain outside this bounded closure.
