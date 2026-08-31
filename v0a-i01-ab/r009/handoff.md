# Cold review: v0a-i01-ab/r009

Round kind FIX; Tier C. Implementer Codex, original C drafter Claude;
checkpoint finalizer Claude. Candidate commit 8d240db477b8c141e6142e055dbfbedc75c6a2f8;
ref refs/heads/review/v0a-i01-ab/r009; manifest SHA-256 4f91aa7ce728c3eff6a7ad30a7c131985d5b86b615875df978d30ac39386aa51.
Main parent d1ed3cbda6107d61ea8e77133871720af04970cd. Review this frozen Git snapshot plus its
blob manifest, never a mutable worktree or chat narrative.

Initial allowed inputs: this handoff, candidate.json, manifest.sha256,
acceptance.md SHA256 81970ee7f14b028800e498b42be607060cefd34e5f7395e80af6ce9ecb96bf54, protocol-interpretation.md SHA256
529fece988fad57871d165b0347ca655eb51a8101462668cd5bb84e5e476a69a, pinned inputs/CLAUDE.md and inputs/workflow.md below,
and frozen source/tests/ADR-0485/ADR-0484/revised brief. Pinned current workflow
copies govern rather than older copies inside the source candidate.
r007 source ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1 is the ten-path A/B
preservation reference. Prior integration source 00db06624ab25f10cd181badccf92c87a78f17ee is the
FIX comparison only. Read code/blobs, not prior reviews, dispositions,
self-reports, status, checks, plans or implementation discussions.

The full17-path manifest is relative to main. Actual FIX delta:
tests/test-inventory.json, tests/test_inventory_and_profiles.py, tools/generate_test_inventory.py.
No new A/B or other C behavior enters this round. Independently reconstruct
the whole-row-sorted Git-blob manifest and applicable invariant/path inventory
BEFORE opening deferred coverage.md SHA256 a6c049cdc6681bb08218e2909d0150dc24352abe85bc6b9eea78047cf1f70f88.
Save and hash that inventory first. Never read peer checks/reports.
Implementation self-reports and coordination notes are excluded. Raw evidence
links in coverage may be assessed after inventory.

Use fresh D-local disposable candidate clones and the isolated snapshot policy:
actual3.11.15 FIRST then3.14.6; assert fullversion/executable before Pontius
imports, -B -P, snapshot-root cwd and src PYTHONPATH, scrubbed environment,
D-local TEMP/TMP and absolute validated PONTIUS_GIT. Run focused affected tests
and independent adversarial controls only. No full CI wall before two CLEAN
verdicts, guarded broad/GPU/install/capability/source-seal/rehearsal execution.
Sensitive fixture bodies are inspected, never executed as a binding oracle.
Do not repair frozen source; a changed byte requires a new candidate.

Execution helper ../snapshot-run-abc-v2.py SHA256
62bf07eb88845dfc30c3820aeb8c899ccfbe8111d811192485e2826a5ecfc20c may be
inspected as infrastructure. A fresh clone of this exact commit is permitted.
Independent focused probes may use a separately inspected wrapper satisfying
the same policy. Write only your assigned checks/report.

Reports require defect and design verdicts, with required corrections separate
from advisory engineering guidance. Use each label exactly once:
Reviewer ID: <assigned reviewer_id>
Candidate commit: <full commit above>
Manifest SHA-256: <full manifest above>
Defect verdict: <actual verdict>
Design verdict: <actual verdict>
Request an exclusive task-ledger slot after the final report/hash. Each issuer
appends their own verdict without reading a peer report.

After both fresh CLEAN verdicts, the coordinator may run only the enumerated
current-CI12+v0a5 CPU wall under ADR-0485 on both actual slots. Exact targets:
checks/permitted-cpu-wall.json. This is not a guarded-profile grant. Controller
approval must name this candidate before Claude's main finalization/push.

Pinned inputs\CLAUDE.md SHA256 af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76; origin raw SHA256 af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76.

Pinned inputs\workflow.md SHA256 d9de38ede87fb619b3045a60ee7fab137ae23ba3b580c0a6d6b3ca14e567a170; origin raw SHA256 d9de38ede87fb619b3045a60ee7fab137ae23ba3b580c0a6d6b3ca14e567a170.
