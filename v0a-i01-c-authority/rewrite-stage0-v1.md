# C core replacement — task brief

Tier C, FIX. 2026-08-31. The controller delegated the implementation strategy;
the coordinator chooses a partial rewrite. Claude remains the finalizer.

Base: rejected r010, commit 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358,
manifest 8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb.
Use a new isolated codex/ worktree; retain main and the old repair worktree.
This is a design checkpoint, not an implementation freeze or cold verdict.

**Scope.** Replace the inventory analyzer's overlapping value/authority/cell/
deferred representations with one state model and explicit operations, including
the helper-entry and recursive-review bridges that reconstruct executable state.
This supersedes only the representation choice in stage0-design.md; all existing
behavioral requirements and evidence remain binding. Hold v31 patching and the v5
diagnostic. Preserve accepted A/B, the boundary checker, CI, native writer,
capability approval/schema, and the original limits.

**Files.** Only tools/generate_test_inventory.py,
tests/test_inventory_and_profiles.py, and the ordinarily generated
tests/test-inventory.json / tests/test-profiles.toml may change. The other 13
paths in coordinator-preservation-baseline-v2.json and the user's main
CLAUDE.md / docs/workflow.md edits stay byte-exact.

**Acceptance.** (1) One authoritative current record per object/cell in each
successor, with correct aliases, captured defaults, live closures and historical
observations. (2) Source-order construction, class/lexical distinction,
exception/finally successors, and dormant/consumed/escaped work remain correct.
(3) Unknown authority refuses explicitly; supported clean cases stay clean.
(4) All existing fixed design, matrix, semantic, corpus, and inventory gates pass
on actual 3.11.15 then 3.14.6; no cap or capability grant changes. (5) One coherent
ref/manifest gets two fresh mutually blind cold reviews, permitted CPU acceptance,
and the finalizer checkpoint before candidate-specific main commit approval.

**Milestones.** R1: one real public-analyzer path through six existing temporal
cases (aliases, cells, class ordering; two clean, three refusal, one permitted
refusal). R2: rerun those and add the two exact depth contracts plus four existing
ambient-size cases. Gate B requires every original budget <=196608, a preselected
engineering reserve below the unchanged 262144 cap; this is not a new admission
cap or an improvement claim. R3: complete remaining contract/corpus checks and
remove the superseded core. R4: freeze, cold review, acceptance and finalization.
No old-engine fallback, fixture-specific routing, or isolated-map-only substitute.

**Seams and size.** Static AST semantics, abstract state/evidence rows, snapshot
controllers, and generated inventory. Writer/Git/locks, CI, and product A/B are
preservation seams. Each implementation increment is reviewable at about 3000
changed lines or less; R1's first attempt stops at 2500 for reassessment. Report
pure deletion separately. No total-line or calendar estimate is established.

**Test discipline.** Existing RED results remain. Freeze exact existing case and
controller inputs before running; sensitive fixtures stay AST-only. Real public
analyzer checks precede broad migration; a failed fitness attempt returns to
design without relaxing outcomes or accounting. A separate category/coverage
plan is required before implementation and stays outside initial cold inputs.

**Forbidden claims.** No complete hand, live 15000 ms result, faster runtime,
general Python soundness, new experiment/guarded/GPU authority, cold CLEAN verdict,
or successful integration follows from this brief. Detailed design and engineering
review accompany it; this brief is not an implementation plan or run authority.
