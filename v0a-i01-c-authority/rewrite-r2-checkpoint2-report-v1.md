# R2 checkpoint 2 handoff

Status: engineering source checkpoint, held for independent source/accounting review. No analyzer, Model, test, candidate import or candidate execution occurred. Checkpoint3 and runtime dispatch remain unauthorized to this lane.

This report binds the separately retained category ledger to the coordinator's frozen source pair:

- H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695`.
- `rewrite-r2-checkpoint2-source-v1-manifest.sha256`, SHA256 `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`.
- Source `rewrite-r2-checkpoint2-source-v1.py`, SHA256 `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`; 1,178,999 bytes. NEW W/tools/generate_test_inventory.py matches it and is held unchanged.
- `rewrite-r2-checkpoint2-category-ledger-v1.md`, SHA256 `01f5f188b17ce08a924e24eb5957eaa9bf09894d4349c6b37450e0d4557415b9`. It was issued while the coordinator froze the seven source/static artifacts; this report supplies the explicit frozen-pair association without altering that ledger.

## What changed

Checkpoint2 introduces distinct proved builtin exception classes, empty canonical exception instances, explicit known Raise, bounded Try/Except/else, and literal numeric negation. All six legacy diagnostic exception-tag producers now remain uncatchable refusals. Known raises retain current state, exception reference, origin and flags through helper completion; matching clears consumed active metadata without deleting issue/trace history. Only active escaping raises become terminal blockers.

Handler tuples require every flat member to carry builtin-class proof. An earlier matching member cannot skip a later invalid/unproved member; nested tuples refuse. Existing current bindings win over module fallback; symbolic spelling is not builtin proof. Class-proof identity remains conservative, and separate exception instances retain separate object IDs.

No generator, deferred-depth, general exception hierarchy, finally, TryStar, handler-name binding, broad numeric protocol, builtin registry, or new public input-facts API was added. Unsupported paths refuse under the approved bounded contract.

The exact checkpoint1-to-checkpoint2 delta is 242 added + 21 deleted = 263 lines. The cumulative delta from R1 c8fc is 314 added + 46 deleted = 360, within the fixed 1500-line R2 ceiling. There are 16 changed existing top-level nodes and 8 new nodes, enumerated in the static result. The binder, five caps, budget algorithms, context construction, ownership/copying algorithms, lexical facts, identity/truth helpers, class/function construction, sink/native writer and public entry policy remain unchanged.

## Verification retained

- `rewrite-r2-checkpoint2-static-check-v1.py`: `4a5f2d351f289cfc846c8de3fbc01b7cca24e5e15ffbfb208d50278ae4dd6380`.
- `rewrite-r2-checkpoint2-static-v1.json`: `7a77f53394954002607d6b8cb66984e856ca051f215e5bdbd722a9f9887ce0fc`.
- `rewrite-r2-checkpoint2-outcome-inventory-v1.json`: `1e44dc04620d2bef50815e10ba0809b7b81a06b475c455d87e2723ac324b1456`.
- `rewrite-r2-checkpoint2-edits-v1.json`: `3537edb006c728aced6e8e19f844451d87da89f53d1fc2ecd7855445ae178d66`.
- Exact checkpoint diff: `fec89fbb58d6dc5cf09f7276c10d7b43ee75499aaeaee847e7c78d400f23cb45`.
- Cumulative R1 diff: `d98024cf42d29d11475dae4e62b73f51ecaf20d38b2932ab73da9bb319d0e759`.

The retained checker was executed twice with actual CPython3.11.15 and `-I -S -B -P`; both exited0 without a failed assertion. The second execution captured the same JSON result for retention. These were AST/hash/data checks only, not analyzer or payload runs. Earlier draft checks also operated on source bytes/AST only.

Checks establish exact20-edit forward/reverse reconstruction to checkpoint1, syntax/style, cumulative size, retained protected core segments, one outcome constructor, unique class/instance/origin producers, all six unchanged tagged-failure call ASTs behind central refusal, nine-field completion summaries, metadata forwarding and no historical-completion terminal scan. Before/after source-install hashes and result-retention hashes confirm all16 protected W paths unchanged. The seven files listed in the coordinator's source manifest were rehashed again for this report. No claim is made about concurrent main-worktree documentation.

One authoring command exceeded the Windows command-line limit and failed at CreateProcess with error206, before any process started. It made no candidate or artifact change. Retaining operations/checker separately and using a bounded static/data installer resolved that authoring-only failure. No candidate assertion or runtime failure was hidden.

## Remaining limits and custody

New outcome and call-summary metadata carries real additional allocations, references and field reads even on nonexception paths. The category ledger identifies those charges and the unchanged full-table/bank COW costs. No cost discount, cap change, new budget epoch, or reserve claim is made.

This source checkpoint has not demonstrated that any frozen case now passes. The coordinator owns the full two-baseline preservation aid, independent source/accounting disposition, immutable publication, future generator checkpoint and reviewed full12 runtime sequence. All cases, Models, controllers and original expectations remain unchanged. The author stops here with W held at7ce.
