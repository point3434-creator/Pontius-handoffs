# v29 disabled-join engineering inspection

Reviewer: codex / r010_cold_a. This is a bounded engineering source inspection, not a cold review or acceptance result. No candidate, fixture, Model, test, or diagnostic payload was executed for this inspection. No source, test, expectation, cap, or issued artifact was changed.

## Frozen inputs and scope

- Candidate: `engineer-generator-v29-storage.py`, SHA-256 `b53b905cd20dd97d7d09a3b81f955bf27498a572ce8a6d82e20f007993ab9466`.
- Predecessor: `engineer-generator-v28-storage.py`, SHA-256 `4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e`.
- Delta: `engineer-generator-v29-storage-from-v28.diff`, SHA-256 `5d65d6c5b720bce21d4db79afbca603372711699fd364d21cce4adb9008d3c7f`.
- Governing disposition: `coordinator-disabled-join-operation-disposition-v1.md`, SHA-256 `320df60041e12736d19f40b7f7bdfdc39b064cd6d42f2c1696fd36c8fa42295e`.
- Plan: `engineer-v28-disabled-join-plan-v1.md`, SHA-256 `d8faada0f14b1f7ffb0e0062ebd90e6fe196718b663cba93d39cd8246ff1b7fa`.

The review covers only the 133-line insertion in `_merge_states` and the existing history, entry, transfer, and publication contracts necessary to assess it. Independent raw-text removal of those 133 inserted lines recovered the entire predecessor exactly. The final candidate hash was rechecked. Root and the author own the separate accounting reconciliation.

## Qualified correctness result

No additional semantic correctness blocker was found within this scope. The operation-local proof supports the proposed omission under the existing API-produced immutable root/history invariants. This does **not** clear v29 for execution or acceptance: the confirmed metering omission below remains unresolved.

1. **Unchanged entries are proved by lineage, not equal sizes.** The guards at 22435-22476 require exact execution states, authorities, cursors, versions and meter, the same original budget, disabled authorities, and pending count equal to each captured version's size. `_name_common_history` (14889) obtains an actual shared history token. Every change name on every intervening history path becomes a candidate. Existing `_replace_entry` (14826) records even identical-value overwrites, while publication (14755) records tail names including deletions. Therefore an existing name outside that union retains the same Entry object from the shared ancestor in every input. Detached bulk/clear histories do not acquire a false common ancestor. Deleted/reinserted names remain candidates.

2. **Skipped entries preserve the legacy result and its pending debt.** The per-name guard additionally requires an exact string key, exact Entry, `entry.no_work is False`, exact FlowValue, and still-disabled result authority. It excludes missing/None values and atypical entries. The legacy equal-input merge at 13434 returns that same FlowValue; disabled `_transfer_authority` at 14034 returns it before doing any authority work. The legacy `_transferred_name_entry` (15116) would wrap it with `no_work=False`. Retaining the identical existing Entry omits that equivalent wrapper construction without creating a positive certificate. Future enabled transfers remain pending. This argument relies on the current exact FlowValue dataclass and storage APIs, not arbitrary custom equality, tampered private roots, or merely equal-looking values.

3. **The eager union and meaningful operation order remain intact.** Existing input snapshots, key views and `set().union(*key_views)` execute before the branch. The new loop uses that very union's iteration order and constructs the known order memo from it. Every changed or unproved name still performs the original supplied tuple, value merge, full transfer, key validation, and conditional cell-write sequence at its original position. Only proved identity/no-effect entries are skipped. The staged cursor starts from the first input, whose keys are necessarily a subset of the union; deletions in only some alternatives enter the old merge path, and names absent everywhere require no residual deletion. No sorting or substitute key-order recipe is introduced.

4. **The new result is published only after successful staging.** Candidate dictionaries, the order table, the staged cursor and its publication are operation-local. The order memo, cursor snapshot, replacement cursor and final install charge all complete before `result._names` changes at 22545. Existing publication helpers stage and charge before commit. The insertion does not mutate a captured immutable version. The initial result fork, authority/binding joins, input snapshots and key-cache materialization are unchanged predecessor work; this is not a claim that the entire pre-existing merge is rollback-atomic. Their existing publication behavior and consumed budget on a later failure remain. The new staging does not refund charges or publish a partially built replacement result.

5. **Authority effects and fallback boundaries remain unchanged.** Initial authority and binding joins still run before this branch. All enabled, mismatched, no-common-history and dense-candidate cases take the unchanged fallback after any planning cost. Disabled transfer has no authority effect to omit, and disabled cell writes were already inactive. No recursive or retained transfer uses a new exemption, no durable no-work field is minted, and neither primitive join nor other methods were modified.

## Known source-only blocker and limits

Root reported, and the author confirmed, a distinct metering omission in the `enumerate(states)` guard loop at 22470: the yielded pair allocation and its two references lack their own charge. Existing iterator-allocation and input-visit categories have other declared meanings. This is a source accounting defect, **not** an observed runtime failure. The retained candidate must stay unexecuted until its explicit accounting successor is reviewed. This report does not independently certify all aggregate accounting categories.

Utility is not demonstrated by this inspection. The eager union/key reads are deliberately retained; the planner walks history and may fall back after paying that cost. A dense change set, including names deleted on all branches, can make fallback conservative. Those are performance limits, not evidence that the operation-local identity proof fails. No payload result, saved-unit claim, cross-runtime pass, or broader integration approval is asserted.

Repair obligation within the present evidence: reconcile the declared enumeration pair allocation/reference cost in a minimal immutable successor while preserving the reviewed guards, exact union order, pending debt, original effect boundaries and staged installation. No semantic relaxation, cap increase, or new witness is requested by this review.
