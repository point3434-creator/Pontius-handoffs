# Storage API clarification v1

Additive to engineer-storage-api-v1.md. No production integration or payload execution.

Meter.limit is writable for controlled failure/retry, constrained to0..262144. Adjusting it never resets/refunds used or counts. A failed ordered_items() publishes no newly computed order or pair caches; retrying the SAME immutable version with a permitted restored limit is supported. Empty/singleton join preserves the existing empty/fork control flow; only multistate join uses legacy set-union order.

Callback input tuple ordering is exact. Invocation order across different candidate names is not a contract of this storage-only primitive. The callback is pure and idempotent for equal input values. This does not authorize reordering production transfers or cell operations; those require their separate integration proof.

Name keys use ordinary string equality/ordering. Controlled string subclasses with ordinary comparison and a colliding hash can test dictionary/set ordering; arbitrary overridden equality/ordering is outside this primitive contract.
