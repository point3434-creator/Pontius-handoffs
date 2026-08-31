# Root disposition: operation-local disabled join

Recorded at the root coordinator's explicit request on2026-08-31. This note
records the coordinator's source GO; it is not the implementer's self-approval,
a runtime verdict, a general transfer exemption, or an integration authorization.

Approved plan: engineer-v28-disabled-join-plan-v1.md
d8faada0f14b1f7ffb0e0062ebd90e6fe196718b663cba93d39cd8246ff1b7fa.
Exact predecessor v28 4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e.
Retained v29 source b53b905cd20dd97d7d09a3b81f955bf27498a572ce8a6d82e20f007993ab9466.

## Normative clarification

For one all-disabled _merge_states operation, exact compatible state/snapshot
wrappers on the same original budget/NameMeter, with all effective entries pending,
may use a common names-only history to establish unchanged entries. An unchanged
exact Entry containing an exact FlowValue may be retained because identical-input
merge and disabled transfer are both identity operations. Retained Entry.no_work
must stay False. This creates no enduring certificate and does not discharge any
future enabled revalidation debt.

Every changed, atypical, incompatible, enabled or otherwise unproved path retains
the original merge/transfer behavior. The original snapshots, authority/binding
joins and ordered conditional cell writes remain. Every actual new guard, history
visit, candidate operation, name/order copy and publication is charged under the
unchanged five production caps. All-parent legacy union is computed once and its
exact eager iteration order is retained. False guards preserve the old full body.

## Bounded implementation

Only _SourceOrderedResolver._merge_states changes. Generic NameVersion/NameCursor
APIs, radix/history/order algorithms, transfer, cells and all other methods stay
source-exact. The implementation further restricts eligible source sequences to
exact list/tuple, authority/cursor/meter wrappers to exact types, and skipped names
to exact str; these unproved/custom cases fall back. Each potential skip rechecks
that result authority is disabled. Original conditional cell writes also remain
in the changed/atypical path.

No W/main edits, source execution, cap/error/test change or semantic-v25 composition
is authorized here. Root source inspection precedes any payload. The semantic lane
reports that its identical-object fast path is retained; combined-source evidence
must still verify that fact before composition, not assume it from this note.

The helper1050 assertion correction is independently reviewed as a distinct v5 test
candidate; neither its bytes nor any older failed receipt is changed by v29.
