# Author evidence and limits (read after independent inventory)

Repeated key/source digest reads: final new serialization test fails on archived base and passes
on candidate. Existing provider counter now requires one serialization from each provider.
Falsifier: a warmed lookup serializes the table again, or a returned digest changes on valid input.

Admission: inherited private cache slots are absent from dataclass fields. Exact-field rebuilding
in decision_provider/model.py and v0a/runtime.py therefore recomputes identity. Tests alter a key
after warming and forge both caches with arbitrary objects. Falsifier: the owned digest reflects
the caller cache, an admitted malformed graph succeeds, or subclass hooks execute at admission.

Value/codec contract: fields, equality, hash, repr, replace, copy and pickle checked. Retained wire
re-encodes exactly and baseline/candidate full membership result objects match (1081 hits).
Falsifier: any byte, source/provider identity, row, default, refusal or action changes on valid input.

Integration: 17 pytest suites / 349 cases / zero skipped passed. Their receipt is working-tree
evidence (source_verified false), not a frozen-commit seal. The later change only adds the lookup
module to the completion test's copied files; all 18 export/completion cases then passed directly.
Those 18 cover eight export cases and ten completion cases, including real-host subset execution.
The earlier direct completion failure (true != false source verification) is preserved: the test
copied unchanged files and silently left the lookup module at base. The corrected copy list fixes
that coverage gap. No production orchestration change was made.

The initial green.log failure was the old negative control demanding 17 legacy serializations;
it is retained. green-final.log has 118 affected cases after updating that expected cost. The final
RED uses the same final test bytes against base-src.zip and fails the intended serialization check.

Performance: benchmark.py ran unchanged before/after; five batches, sizes 1/100/1326, no tracing
during timing. Memory uses separate tracemalloc. Observed 1326-entry lookup improves about 56x,
provider proposal about 43x; construction remains similar and retained allocation increases.
The retained parity diagnostic timings were taken alongside integration work and are not a matched
performance estimate. Whole result equality, not its timing, is the acceptance criterion there.

Limits: legacy scan remains linear, canonical_bytes itself is not cached, direct object.__setattr__
tampering is outside the frozen-value contract, and this work establishes no playing-strength gain.
Further indexing/import cleanup and API deletion are deferred. All execution used CPython 3.14.6;
older project metadata mentioning 3.11 is inherited and is not authority to run it in this lane.
