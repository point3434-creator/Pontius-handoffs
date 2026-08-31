# Diagnostic instrumentation repair v2

The first helper1050 diagnostic reached the unchanged work cap, then v1's
failure-stack description raised AttributeError on an _ExecutionState whose
copy had not installed authority yet. The saved exit2/integrity-true receipt is
instrumentation failure, not a complete product or cost verdict. v1 and its
evidence remain unchanged.

v2 changes only that frame descriptor: read the exact state's raw __dict__,
require authority presence and exact _AuthorityState type, read that object's
raw __dict__, and require a present exact bool enabled value. Missing or
unexpected fields become explicit scalar status markers. It never calls the
state Mapping/cursor API, reads authority stores, supplies a default mode,
changes budgets, or catches the original analyzer refusal.

Sibling diagnostic reads were audited: resolver fields already use raw
vars/get/type guards; budget fields are read after original initialization;
NameMeter's own budget exists before its delegated consume; operation hooks
inspect complete inputs and successful returned publication plans, not
partially built output states. AST descriptors concern completed parser nodes,
not execution-wrapper construction. No other probe path was changed.

The controller successor changes ONLY its fixed probe filename to v2. All
custody, CLI, summary, watchdog and floor-only behavior are byte-preserved.
Static AST comparison proves every other probe definition/top-level statement
unchanged; inverse replacement proves the exact controller delta.

No fixture, probe, controller or product payload was executed by the author.
Root must inspect both pins before a fresh snapshot run. Original two cases,
_review envelope, source/tests/W pins, all five caps and original delegation
remain unchanged.

- engineer-depth-budget-probe-v2.py: 8db7415b97750e8880b25351be76b6fdf75d767a03a3a589d739113a73b6cae0
- tests-depth-budget-control-v2.py: bbdc550c042fe62c8c19e838ffe35a9cabc09f22fdd4d941bdb0d9d0a41599a5
- engineer-depth-budget-probe-v2-from-v1.diff: b20853d6530eb9f4673d41c5a7a8972a8785ca9704eaba3696b6f3fa4e7b470a
- tests-depth-budget-control-v2-from-v1.diff: 3b4fac2cd2ea137626acceb34a0a123eab0a27c9f2a0c22e1958c5c01cdc552c
