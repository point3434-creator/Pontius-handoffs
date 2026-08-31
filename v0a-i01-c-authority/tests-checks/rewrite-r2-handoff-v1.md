# Rewrite R2 Gate B harness authoring handoff v1

Frozen and UNEXECUTED. Preparing it does not authorize Gate B or advance R1.
Root reviews this harness and the R2 source plan/candidate separately after Gate A.

Probe rewrite-r2-probe-v1.py SHA256 abc1a22b76691ab8881e5301f532fad32171183abb11221debc93e7428e48310
Control rewrite-r2-control-v1.py SHA256 54c4e61fd07173fbf2f52441ae1dbb94d6dbfcaf3f7d9ee0e385509ac73bd7ba
Plan rewrite-r2-plan-v1.md SHA256 ea2ca1217f133a708c763568cc7494a2ac600b4db351e00a696600836d53f5f7
Observer map rewrite-r2-observer-map-v1.json SHA256 1dfd899dc7c7a1c9bbf1ff0ee17bc8b4fd4be1eadf3c81f759eb1b0176630228
Static proof rewrite-r2-static-v1.json and exact R1 predecessor diffs accompany them.

The fixed manifest selects12 public analyses,24 Models,10 normal receipts and
two original exact depth errors. All four original public/Model functions and
the budget observer/reconciliation definitions are unchanged. The two copied
existing builders match their source/AST pins; original test method, assertion,
builder and full envelope spans were rehashed. No builder or Model ran here.

Only original DesignReviewTests.setUp/_review execute in the future depth adapter,
on each freshly loaded case.generator. Whole multi-subtest methods and old
diagnostics never execute. Original child source/full universe remain. All actual
original budgets count.196608 is a postexecution per-epoch continuation check;
the262144 production cap and original consume implementation stay unchanged.

Root-owned future controller CLI uses the same arguments as R1:
LABEL SLOT RETAINED_SOURCE SOURCE_SHA --control-sha256 54c4e61fd07173fbf2f52441ae1dbb94d6dbfcaf3f7d9ee0e385509ac73bd7ba --worktree-sha256 APPROVED_CORE_W_SHA
For314 require --floor-receipt PATH --floor-sha256 SHA. The matching floor must
have intact custody, all semantics/Models, accounting and reserve success.
The current old-W watch staysv20. Source/candidate changes, payload invocations,
Gate B expansion or earlier dispatch are not authorized by this artifact.

Original ten payload/provenance files plus1761 tracked files are fully hashed;
dev adds the five pinned floor evidence files. All runs use new D-local r010
snapshots, original flags/environment/Git and60-second direct-child watchdog.
