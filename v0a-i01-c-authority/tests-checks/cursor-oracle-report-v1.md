# Owned cursor prototype: independent retained-result audit v1

The admitted prototype schedules pass: all six children completed the unchanged
34 compatibility runs and 28 cursor runs, for 372/372. The new cursor obligations
have direct evidence for snapshot/fork isolation, exact ordered views, effective
pending metadata, tombstones, bounded-history retention and operation-level
failure retries. This is engineering verification by the oracle author, not an
independent cold review or production acceptance. Whole-pipeline fit remains
unestablished.

The reviewed result source is engineer-name-cursor-prototype-v1.py SHA256
67acb279510924311266b985e15e95e53ae9d0a11d64a50d108f254a690deb2a.
Root configuration is afb9d33f3ec5110e822a0a7e44710fbe025940985ecf82ce7ffc533c084ab958.
The cursor oracle/case bytes remain 15a4741e2532a755fd45f01d4d999dd5d293846b8ae4e9d4e7abedf84c0a8d1e
and ecddd020ffb2a0d85e624aeb7fb544f631b302839f9a5f3542c998b36c37ac61.
The old oracle/cases remain 6a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba
and 3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f.

This auditor read records and recomputed hashes only: no prototype implementation
inspection, payload execution, source/test edit or budget change. Frozen scope
is coordinator-name-cursor-prototype-disposition-v1.md and cursor-oracle-spec-v1.md.
The companion cursor-oracle-run-proof-v1.json SHA256
21d32132376dfa1bfb1aa62c66408fa30527532ea911f0c7ae3586d4cb2151c8
retains complete receipt/log pins, source bindings, numeric comparisons,
signatures and verification details.

All six receipt hashes match the coordinator's exact pins. Log/stdout/stderr
hashes were recomputed, as were 57 retained payload-file hashes and six snapshot
manifest hashes. All 10623 retained before/after entry pairs match: 1770 per floor
snapshot and 1771 per development snapshot. The additional development entry is
its correct same-seed successful floor receipt. The tracked count remains1761.
This audit reconciled retained control maps; it did not rerun Git or freshly
rehash all tracked files. Nine current original input hashes were separately
checked against floor before/after bindings, including unchanged W source e61b3a....

Identity records name actual3.11.15 and actual3.14.6 with -S -B -P, snapshot cwd,
snapshot/src PYTHONPATH, scrubbed environment, D-local temp and absolute Git.
The coordinator reports serial order311 seeds0/1/17 followed by314 seeds0/1/17;
each development snapshot additionally binds its same-seed floor receipt. No
filesystem timestamp is used as proof of authorization or ordering.

Every expected case/phase identifier is present exactly once. All per-run phase,
event and category sums equal that run's meter.used, below262144. All six runs
have identical per-case charged totals and category totals. For each seed, the
complete original JSON case-record sequence also matches byte-for-byte between
runtimes, separately for old and new families. Different seeds change permitted
order records; the child builtin-dict/set oracle computes those expectations.

| Actual runtime / seed | Compatibility | Cursor | Combined |
|---|---:|---:|---:|
| 3.11.15 / 0 | 34 | 28 | 62 |
| 3.11.15 / 1 | 34 | 28 | 62 |
| 3.11.15 / 17 | 34 | 28 | 62 |
| 3.14.6 / 0 | 34 | 28 | 62 |
| 3.14.6 / 1 | 34 | 28 | 62 |
| 3.14.6 / 17 | 34 | 28 | 62 |

The16 cursor schedules generated16 pristine runs and12 injected-failure replays
per child. There were no skipped/unreachable schedules or unexpected refusals.
Empty/missing-key behavior, dense construction, retained siblings, immutable key
views/item tuples, overwrite and delete/reinsert behavior all match ordinary
dict expectations. All eight scheduled joins respect the required pending-name
callbacks; the old-pending-but-now-certified/deleted control needs zero callbacks
and gets zero. Each raw-identical installation requires x's callback and gets it.
Related/unrelated joins preserve input argument identities and exposed legacy
union order. Mutable-cursor and foreign-meter joins both raise ValueError before
any callback; the oracle did not prescribe that particular exception spelling.

The12 cursor failure replays per child (72 total) all match the pristine primitive
in exact retry units and category deltas. Every later validation/fork/write/
publication/read cost sequence and observable output also matches pristine.
Calibration excludes validation calls. Spent failed charges remain in the total;
limits were restored without refund. The36 old immutable failure replays also
retain exact pristine retry costs.

| Cursor target | Pristine/retry units | Failed units: first / middle / last |
|---|---:|---:|
| snapshot | 164 | 1 / 83 / 164 |
| fork | 172 | 1 / 87 / 172 |
| keys | 136 | 1 / 72 / 136 |
| ordered_items | 281 | 1 / 141 / 281 |

This preparation actually reaches compaction for snapshot/fork: each pristine
target and successful retry records13 compaction-entry visits. Middle failures
record7 and8 such visits; last failures charge the compaction-publication,
fresh-tail and version-allocation categories, with the fork case also reaching
its cursor/return charges. Those charged names alone do not prove successful
publication during the failed call. Exact pristine retry plus continuation is
the relevant public evidence that no partial publication became visible.
Keys/items do not compact or publish in their target operation; their late
failures reach their return-reference charge and still preserve pristine retry
and subsequent fork behavior. This remains three offsets per operation, not a
general rollback guarantee for semantic writes or arbitrary callbacks.

Both retention sentinels pass in all six children. The never-published old value
is released after private overwrites. The published old value remains alive and
readable through its deliberately retained original snapshot. After24 dirty
publications, successful compaction records27 entry visits (three compactions);
dropping the original snapshot then releases the obsolete value. Thus the test
does not confuse legitimate snapshot/layer ownership with history-only retention.
The separate tombstone schedule completes two compactions with22 entry visits,
keeps its victim absent through18 publications, and appends it on reinsertion.

All quantities below are sums of independently capped meters, not one analysis
budget. The new28 consume102534 per child plus a separately recorded148-unit
foreign setup meter. The old34 consume194605. The largest individual meter is
54540, in fork-per-write64; no cap was increased or bypassed.

| New28 phase grouping | Charged units per child |
|---|---:|
| Construction | 807 |
| Private writes | 10427 |
| Regular publication | 5409 |
| Forks | 6745 |
| Preparation publication | 4816 |
| Preparation reads | 1664 |
| Joins | 1219 |
| Ordinary terminal keys/items | 4329 |
| Ordinary repeated keys/items | 74 |
| Pristine target plus successful retries | 3012 |
| Result validation plus continuation reads | 8584 |
| Retained-state audit | 53909 |
| Lookups, invalid boundaries and length validation | 399 |
| Failed attempts | 1140 |
| Total main meters | 102534 |

Dense-private64 costs3161 including65 writes (the later overwrite), one
publication, terminal/repeated reads and its retained audit. Its publication
visits64 original private-tail entries. Fork-per-write64 costs54540, including64
forks,64 publications, seven compactions and45574 units to read all retained
historical cursors. Both publish64 original change entries. The latter records
231 compaction-entry visits and10272 layer lookup attempts versus64 layer attempts
for dense-private64. Its publication_tail_entry_visits is288 because that broader
category includes compacted output sealing; it is not the original tail size.
publication_change_entry_visits=64 is the appropriate original-change count.
These schedules differ deliberately in history retained, so54540/3161 is not a
pure fork-cost ratio. Excluding historical audit and length validation, the
recorded remaining totals are8900 and2571 respectively; even that subtraction
is a diagnostic breakdown, not a prediction for production.

For the unchanged compatibility family, all34 same-seed totals decrease on the
cursor prototype. Every retained AVL receipt/log was rehashed against the prior
independent proof, and its full per-case cost signature matches across all six
old slots. The comparison therefore holds for each corresponding runtime/seed,
not just an aggregate over different seeds.

| Compatibility phase | AVL | Cursor | Difference |
|---|---:|---:|---:|
| meter_initialization | 0 | 0 | 0 |
| construction | 97938 | 70025 | -27913 |
| validation | 754 | 754 | 0 |
| joins | 34763 | 22572 | -12191 |
| terminal_order | 41107 | 33446 | -7661 |
| repeated_order | 2276 | 110 | -2166 |
| lookup_audit | 113 | 66 | -47 |
| retained_order_audit | 74423 | 56655 | -17768 |
| failed_order_attempt | 4458 | 3681 | -777 |
| ordered_retry | 8871 | 7296 | -1575 |
| Total | 264703 | 194605 | -70098 |

This is26.48% fewer charged units under the two declared accounting schemes.
It is not a runtime, memory or cross-representation physical-work ratio. Actual
dictionary attempts and copied references differ from AVL node allocations;
the oracle does not independently prove that every possible internal operation
is charged. Honest source-level accounting remains a separate review obligation.
Repeated items may return immutable cached tuples, so no dummy copies are
required just to reproduce AVL's old charges.

The preserved eight-grid current costs retain deferred terminal and historical
reads. These are identical across all six new slots.

| N/J/D | Construction | Join | Terminal | Repeated | Historical | Validation | Cursor total / AVL total |
|---|---:|---:|---:|---:|---:|---:|---:|
| n8-j2-d0 | 625 | 142 | 489 | 4 | 258 | 13 | 1531 / 1756 |
| n8-j2-d2 | 993 | 525 | 445 | 4 | 536 | 21 | 2524 / 3007 |
| n8-j4-d0 | 627 | 284 | 739 | 4 | 514 | 21 | 2189 / 2458 |
| n8-j4-d2 | 1263 | 950 | 719 | 4 | 1148 | 37 | 4121 / 4989 |
| n64-j2-d0 | 6834 | 142 | 3233 | 4 | 2722 | 13 | 12948 / 17183 |
| n64-j2-d2 | 7594 | 921 | 2517 | 4 | 4456 | 21 | 15513 / 22741 |
| n64-j4-d0 | 6836 | 284 | 4491 | 4 | 5442 | 21 | 17078 / 21357 |
| n64-j4-d2 | 7864 | 1346 | 4023 | 4 | 9436 | 37 | 22710 / 32535 |

Not every phase improves. Unchanged D=0 joins cost71 each versus36 in AVL, although
both remain independent of N in this grid. At N64/D0, historical reads rise
2470→2722 for J2 and4810→5442 for J4; N8/J4/D2 construction rises1248→1263.
All eight whole-case totals are still lower. These residual costs and frequent
publication must remain visible when assessing a production port.

One historical evidence-format correction is retained here without rewriting
old files: storage-oracle-proof-v1.json serialized large numeric hash_probe/
hash_alpha fields through JavaScript numbers, rounding those literals. Raw
receipts/logs preserve exact integers and all SHA pins remain valid. This audit
uses raw identity-bearing records and raw case-record hashes, not those rounded
numeric fields. Small budget counters and recorded results are unaffected.

Required prototype outcomes pass for the finite frozen cases. Advisory limits
remain: no production adoption/clear boundary, live-cell authority behavior,
ordinary corpus generation, complete wall or universal retention behavior was
exercised here. Colliding string subclasses, arbitrary callback effects and
concurrency remain outside this pack. These results do not broaden the old no-work certificate or full
fallback rules. A separate authorized port
still needs the existing design, authority matrix, public24 and ordinary
generation evidence under unchanged caps and ordering. This report grants no
source-port or release approval.
