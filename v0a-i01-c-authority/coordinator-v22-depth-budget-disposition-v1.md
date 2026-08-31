# v22: both original budget failures mechanically located

The coordinator independently rehashed both complete diagnostic snapshots,
input/output files, runtime identity and all budget-epoch accounting. See
coordinator-v22-depth-budget-verification-v1.json for exact receipt/output pins.

The helper1050 case exhausts its first budget while registering helper_540,
before any helper body runs. Publication and full compaction use 211514 of
262145 charged units (80.69%). The current store repeatedly copies growing
prefixes after eight small publications.

The generator70 case exhausts epoch six while creating g48 in receiver
preflight, before deferred consumption. Ordering uses 89193 units, projected
assignment 67584, and lookup 37727. All 145 state merges use the full legacy
route; no sparse version join runs. This is a second storage cost pattern.

Neither trace measures deep execution or establishes a wall-time ratio.
All five caps and original budget methods are unchanged. Diagnostic exit zero
means evidence collection completed: v22 remains rejected by two original
design assertions. Matrix/dev/public24/corpus acceptance remain held.

A simple dict/COW replacement is not justified: real per-definition forks
would still copy growing dictionaries when honestly charged. An isolated
indexed-store and linear bulk-construction experiment is being specified,
with independent growth, collision, retention and failure-atomicity schedules.
No production source lease, W modification, cap change or integration follows
from these diagnostics. Class/capture semantic repair remains a separate lane.

The prior helper1050 diagnostic v1 failed in the probe's partial-state formatter;
its receipt/log remain retained. These v2 diagnostics correct only that probe
guard and its pinned controller filename; source and fixtures are unchanged.
