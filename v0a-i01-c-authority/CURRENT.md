# C authority repair: current engineering state

2026-08-31. Navigation only. This page is not a frozen handoff, evidence seal,
acceptance result, or reviewer verdict. New reviews require a git snapshot ref
and its manifest SHA-256; no successor pair has been frozen yet.

Accepted A/B remains byte-identical to r007. The other three C integration paths
(CI, boundary checker, boundary tests) are also unchanged. Main remains d1ed3cb;
no source integration, ceremonial commit, or main push has happened.

The latest frozen combined candidate is rejected r010:
29c02f6fbd5eb0b7ddc9e816ef28f570b9839358 /
8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb.
Its findings and reports remain immutable. The [separate repair design](stage0-design.md)
replaces the bounded callable-authority state/transfer representation.

Last completed behavioral checks: v18 source
d97ea66ef606144bb635f522856af3a5cd08819368af981a0a408c84c1e6cc99
passes the original 53 DesignReview tests and the new matrix's 192 schedules /
212 harmless projections on actual Python 3.11.15 first and 3.14.6 second.
[Hash-bound receipts](engineer-checks/release18-focused-evidence.json) document
focused engineering only; they are not corpus GREEN or cold approval.

Ordinary generation on v18 still reaches the unchanged 262144-unit
analysis limit (write05); its specific attribution is being checked.
[The latest completed diagnosis, on v17](tests-checks/budget-gen04-diagnosis-v1.md)
attributes the remaining cost to state materialization, transfers, and binding
lookups. Observation compaction is now only 248 units in that failing budget.
Earlier generation failures and their exact source bytes remain retained;
[publication receipt](coordinator-budget-publication01.json) binds their backup.

Current engineering source v18 is d97ea66ef606144bb635f522856af3a5cd08819368af981a0a408c84c1e6cc99.
It removes redundant state-copy work while retaining transfers for changed values,
fresh local cells, strong/weak cell writes, all five caps, and the original test
contracts. [Prerepair reasoning](engineer-state-copy-prerepair-v18.md) and
[exact v17 delta](engineer-generator-v18-from-v17.diff) are engineering inputs.
Focused checks passed as described above; ordinary generation has not passed.
No corpus pass or successor review is implied by this page.

Remaining order: ordinary generation; preservation of all 2873 existing inventory
entries and 141 canonical capability rows; mechanical census refresh; nine focused
targets on both interpreters; freeze the successor pair; two fresh mutually blind
cold reviews; the permitted CPU acceptance wall. Only then does candidate-specific
controller authorization permit Claude, the checkpoint finalizer, to commit/push.

No guarded profile, GPU execution, source seal, research owner, rehearsal, or live
15-second action-wall claim is authorized by this repair.
