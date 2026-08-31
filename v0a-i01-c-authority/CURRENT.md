# C authority repair: current engineering state

2026-08-31. Navigation only. This page is not a frozen handoff, evidence seal,
acceptance result, or reviewer verdict. New reviews require a git snapshot ref
and its manifest SHA-256; no successor pair has been frozen yet.

Accepted A/B remains byte-identical to r007. The other three C integration paths
(CI, boundary checker, boundary tests) are unchanged. Main remains d1ed3cb;
no source integration, ceremonial commit, or main push has happened.
[Independent preservation check](coordinator-v19-preservation-v1.json) verifies
all thirteen preserved paths and the unchanged generated pair.

The latest frozen combined candidate is rejected r010:
29c02f6fbd5eb0b7ddc9e816ef28f570b9839358 /
8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb.
Its findings and reports remain immutable. The [separate repair design](stage0-design.md)
replaces the bounded callable-authority state/transfer representation.

Last completed behavioral checks: v19 source
3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1
passes the original 53 DesignReview tests and the new matrix's 192 schedules /
212 harmless projections on actual Python 3.11.15 first and 3.14.6 second.
[Hash-bound receipts](engineer-checks/release19-focused-evidence.json) document
focused engineering only; they are not corpus GREEN or cold approval.

Ordinary generation on v19 still reaches the unchanged 262144-unit analysis
limit. [Write06 receipt](coordinator-checks/c-authority-write06-311-receipt.json)
records exit 2 and no generated-file change. [The completed v19 diagnosis](tests-checks/budget-gen06-diagnosis-v1.md)
confirms 492 selected merge plans and 15780 net work units saved for those traced
merge operations, including fallback overhead. Full generation still refuses in
the same inventory-structure item. The dominant costs remain authority transfers,
map reads, copies, joins and forks. These totals stop at refusal; the savings are
not a whole-corpus before/after comparison or a performance acceptance claim.

The v19 edit preserves every transfer and cell write while batching eligible
binding lookups. [Prerepair reasoning](engineer-merge-batch-prerepair-v19.md) and
[exact v18 delta](engineer-generator-v19-from-v18.diff) remain engineering inputs.
Following repeated generation failures, the [bounded storage decision](coordinator-storage-disposition-v1.md)
accepts an isolated prototype of persistent names with exact legacy-order recipes.
Reuse is restricted to a proved context-independent no-work transfer; live-reference,
rebuilt and raw entries remain pending. No store-lineage cache is included. The
[independent proof](tests-checks/name-environment-transfer-proof-v1.md) states the
restriction and preserves every cell write and consumer analysis.

The [structural family](tests-checks/name-environment-report-v1.md) passes all 24
semantic expectations and 58 harmless projections on each actual interpreter.
All four zero-change comparisons demonstrate repeated ambient-name work; this is
structural RED, with no analyzer or oracle failure. [Coordinator verification](coordinator-name-environment-verification-v1.json)
checks the pinned evidence and identical cross-slot counters. The hidden tuple-return
sentinel demonstrates safe refusal, not precise joined-cell resolution.

The storage prototype is being checked against ordinary dictionaries and actual
legacy set-union ordering before production integration. Full ordering costs,
terminal reads and failure paths must be included. W remains exact v19; no new
production replacement is implemented or declared GREEN here. All five caps,
test contracts and accepted A/B remain fixed.

Remaining order: complete the bounded repair; ordinary generation; preservation
of all 2873 existing inventory entries and 141 canonical capability rows;
mechanical census refresh; nine focused targets on both interpreters; freeze the
successor pair; two fresh mutually blind cold reviews; the permitted CPU acceptance
wall. Only then does candidate-specific controller authorization permit Claude,
the checkpoint finalizer, to commit/push.

No guarded profile, GPU execution, source seal, research owner, rehearsal, or live
15-second action-wall claim is authorized by this repair.
