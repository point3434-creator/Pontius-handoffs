# R1 Task1 v2 handoff

Engineering checkpoint; evaluator remains unwired. No source import, primitive execution, test, payload or commit.

Source rewrite-r1-task1-source-v2.py SHA256 844b2d01a5854f1c8494dfc56877d17557a67cf53fef554445e4c20491351862.
Insertion rewrite-r1-task1-insertion-v2.txt SHA256 037714de1f39be40fb3f6ebb721686c403da6517d13c8bea3879013332723da0.
v1-to-v2 diff e92361ef79a8c5fd8510eda329c7914290badbc1283195a0efec7cdf8d8a183f.
r010-to-v2 diff 4cb12ebbc88e286f2407ebaaaa35e2765fddfb1f9befb3e6cbb8732d7ce7a6bd.
451 additions,0 deletions;2049 implementation lines remain.

The prior ledger rewrite-r1-task1-ledger-v1.md (7a660a6ead08338e840f6db0e9d6a1bcbc1258ef0ea3b271017746bd2c0bb592) remains applicable except these two approved corrections:

- Empty _c_choice now charges one reached-refusal visit and raises InventoryError('canonical alternative set is empty'). No unknown atom is allocated or charged. This is prewiring static contract closure, not a demonstrated product RED.
- The container size guard/charge precedes the tuple-copy visit charge. Admitted nonempty totals are unchanged; an oversized choice does not charge an unreached tuple copy before the container refusal.

No other source delta. The reusable v2 checker reads retained baseline/source/insertion; actual3.11.15 -I -S -B -P exited0 after AST-only parsing, exact two-replacement proof, original byte/AST restoration, other16 protected hashes, no new evaluator wiring/budget constructor. Checker SHA256151db03403e012b7705498f911a497f0ac68718dade5afb879bd4d8259557d7e.

Root independently acknowledged exact v2 and authorized sequential Tasks2-5 after checking proof coordinator-rewrite-r1-task1-v2-verification.json SHA256 d56b383874488e4ae2f0ea6d33220051b65a38d5e5bf0d276ec997ba18a43d4a. That authorization is not runtime verification. Task snapshots remain immutable; no payload is authorized here.
