# Name-storage prototype primitive API v1

T-only prototype contract, 2026-08-31. No production integration.

- `Meter(limit=262144)`: `.used`, `.counts`; `BudgetExceeded` preserves the spent/throwing charge.
- Frozen `Entry(value, no_work=False)` and singleton `MISSING`. `no_work` is caller-supplied proof metadata for this primitive experiment, not a production classifier.
- `NameVersion.empty(meter)`. All versions are immutable except completed internal memoization.
- `version.get(name, default=None)` returns the stored value/default; `len(version)` returns the name count. Names must be strings.
- `version.set(name, value, *, no_work=False)` returns a new version. Raw/default installation clears certification even for the same object. Overwrite preserves key order.
- `version.delete(name)` returns a new version or raises KeyError; delete/reinsert appends.
- `version.fork()` retains the immutable version in O(1); later version edits cannot affect it.
- `version.ordered_items()` returns an immutable tuple of `(name, value)` pairs in exact ordinary dictionary/legacy merge order. Repeated reads still meter actual visited entries.
- `join(meter, states, merge)` returns a version. `merge(name, tuple(values_or_MISSING_in_input_order))` returns Entry. Empty join is empty, singleton join is a fork. For two or more inputs, keys/order match `set().union(*(state.keys() for state in states))` exactly. Changed/pending candidates invoke merge; shared unchanged no_work entries may be retained.

The merge callback is required to preserve an unchanged value when all inputs supply that value; no-work reuse relies on this semantic merge law. Pending names still invoke it. Storage does not simulate authority transfer or cells. Production callback integration and narrow certificate construction remain separate coordinator-gated work.

Meter accounting includes real node/reference copies, path/history visits, lookups, order recipes/cache work and iteration. The hard default maximum remains262144. Oracle schedules may use lower limits to inject failure; no production caps are edited. Failed realization must publish no partial order/result cache.
