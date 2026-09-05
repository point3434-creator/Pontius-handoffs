# Review B addendum 001: inventory entry count correction

This addendum corrects only the inventory-entry attribution in the issued `review.md`, SHA-256 `f67b53dde991cd7867d14c5097cfadbeadd21a0885364e9d91fb60688803aad0`. The original report remains unchanged.

Candidate: `fe1e2fc68675c6c92a1263450b455011b5987207`.
Manifest: `6eb5ec280b6a8051e88d7659920ef74b46ea682a06dc80f688ed951d75f3f221`.

In the Fresh execution evidence section, replace the attribution **184 from the exact v0a suites** with **182 from the exact v0a suites**. The total of 187 added entries is correct:

- 182 v0a entries: 22 contract-fault, 45 hand-replay, 62 replay and 53 trace tests.
- 1 new inventory regression.
- 4 new boundary tests.

I independently verified this split by reading `tests/test-inventory.json` directly from the baseline and candidate Git blobs, comparing stable-ID membership, and grouping added entries by their exact `relative_path`. Baseline: 2,641 entries; candidate: 2,828 entries; difference: 187. The earlier scratch audit used substring matching on complete stable IDs, which also matched two boundary-test method names containing `test_v0a_`; that counting method caused the attribution error.

The CLEAN verdict, Spec PASS, Quality PASS, SOUND design verdict, finding counts, and all other conclusions remain unchanged. This is a report correction only; no source changes, additional test run, or review round occurred.
