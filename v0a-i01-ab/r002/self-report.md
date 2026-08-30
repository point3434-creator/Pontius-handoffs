# r002 policy correction self-report

Commit 2f4287f68a83fac4225a05a91daffdb3f2977a43; manifest 55f7ebf8827c79a6d6c70b1bf26508d87527b8c7113d2458fb4c3dfb5fed0957.
Exact graph admission reconstructs owned policy values. Selection preserves the
sealed lookup, validates exact context, and binds header/decisions to that source.
The previous subclass acceptance test is now a rejection control. A timing test
now observes the actual visible-card transition because substituting its class
would intentionally fail the new exact-type boundary.

RED/commands/exits/hashes: ../policy-checks/red-v3-311-receipt.json.
Four new tests report 32 failed subcases against rejected source; the earlier
subclass-acceptance expectation also fails. Final focused GREEN receipts:
../policy-checks/freeze-check-311-receipt.json and freeze-check-314-receipt.json;
39 hand,25 trace,45 replay,22 fault tests =131 each. Earlier green-v1 retained:
only the subclass-based timing double failed; replacing that observer preserves
its actual elapsed-time requirement. Earlier RED versions retained as superseded.

checks/freeze-verification.json ties executed final overlays to frozen blobs.
Four changed files, 270 insertions/80 deletions, diff --check passes. No primary
files, sealed dependency, C surface or real index changed; review ref pushed.
No claim of broad acceptance, performance, source seal or source integration.
