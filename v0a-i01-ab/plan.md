# v0a-i01-ab — Codex ownership and repair plan

Controller instruction, 2026-08-30: Codex engineers clean slices A/B while Claude works on C.
Implementer/finalizer for these correction drafts: Codex. Tier C.
This is implementation authority, not ceremonial source integration authority.

Starting frozen pair: v0a-i01-impl/r006, commit c74b80628a89938ca585ef3240b5c267a7174d0f,
manifest 2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f.
Worktree: D:/Pontius-worktrees/codex-v0a-i01-ab; branch codex/v0a-i01-ab.
Governance: ADR-0485, ADR-0484 brief, current docs/workflow.md and the immutable
implementation/value-audit dispositions. Existing root-cause histories are retained.

## Ownership and scope
Codex alone edits the six existing src/pontius/v0a modules and four existing
tests/test_v0a_{hand_replay,trace,replay,contract_faults}.py files.
Claude owns slice C: repository origin/import policy, inventory/profile declarations
and generation, boundary tests, census and CI. No new v0a module or test filename
is planned. C's final generated artifacts require the completed combined tree.
No legacy source, sealed ledger/spine/kernel/blueprint, dependency baseline,
retained evidence, primary working files or accepted ADR is changed.

## Separate correction boundaries
1. r001: R2-03 failure ownership only. Redesign provenance and error transport.
   Preserve the hand loop, first-cause order, known actions, exact multiplicity,
   public ledger measurement and the passing opposing controls.
2. A separate candidate: R2-01/R3-01 complete immutable policy authority,
   including nested input influence, with its existing root-cause note.
3. A separate candidate: V-01/V-02/V-03 exact event/envelope/receipt ingress.
4. Separate candidates for strict schema + independent accepting legal replay
   and for measured incremental stable-root publication/accounting. These are
   previously deferred B contracts, not r006 residuals.
Previously closed R2-02/R2-07/R2-08 remain regression obligations.
Each boundary freezes only its declared correction; changed bytes get a new round.
Combined A/B review follows, without claiming C acceptance or integration.

## r001 bounded design
Local str-call removal leaves occurrence identity and generator exception hooks
unresolved; replacing the hand loop discards correct, tested behavior. Instead:
- The v0a witness owns one exact, internally created clock failure object. Its
  identity represents the source occurrence; later refusals carry that same identity.
  Raw source exceptions are normalized without rendering or caller metadata access.
- Runtime retains a witness occurrence once, while independent body exceptions
  with the same code remain distinct. Typed code is not occurrence identity.
- Both owned operations share an explicit context-manager implementation. It records
  the body before closing the real interval and transports only a trusted constant
  failure signal. Remove generator wrappers on that propagation path.
- Classification uses real exception type ancestry, never caller __class__, str,
  traceback setters or overridden equality. Preserve the public receipt result.

r001 files: clock.py, runtime.py, replay.py, tests/test_v0a_replay.py.
Expected size: comfortably below 1,000 changed lines. No external dependency.
Seams: source/witness, runtime/outer ledger, oracle/host, writer/publication,
error/receipt. Only ordinary correctness identities and CPU tests execute.

## Verification and completion
Reproduce new exact-sequence and containment regressions against the frozen r006
tree before production edits; run real host A/B with actual source faults and
real writer PathLike admission. Include healthy and genuinely distinct equal-code
controls. Run release CPython3.11.15 first, then3.14.6, only in fresh D-local
snapshots with -B -P, exact cwd/src PYTHONPATH and absolute PONTIUS_GIT.
Freeze commit-derived manifests, retain command/exit/hash receipts, and obtain
two independent cold reviews per Tier-C correction. The coverage claim is deferred
until each cold reviewer records an independent inventory.
Broad or guarded execution follows repository approvals; no GPU, source seal,
rehearsal, research owner, operational budget, performance claim or ceremonial
source commit is authorized here. Final integration authorization is the final gate.
