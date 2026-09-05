# Windows handle fixture r001 handoff

Round kind: FIX. Tier C. Finalizer: controller assistant, subject to explicit
user authorization for any later decision commit/push. No operating authority.

- Ref: refs/heads/review/windows-handle-fixture/r001
- Commit: 76309774b551a874b8f9c677bc59e51299cee0e4
- Tree: f7d2451c20e417967864718b3d000a3eb60387e9
- Parent: 5e56e4454f7b8ccb360d3e36245abc33318349bb (frozen codec r002)
- Manifest: 755c34175c060a4f0ef55616c9e52e336989645763cb16c0fd5a26293a7a37a6
- Source repository: ../../authoring (HEAD remains parent; read frozen ref)
- Exact changed population: tests/test_inventory_and_profiles.py and
  tests/test-inventory.json. No production code change. Profiles unchanged.
- Requirements: ../../brief-design.md and both numbered design addenda.
- Deferred FIX coverage: ../../coverage.md, SHA-256
  6c5ea08ff78251c40714f3d651fa9f2720d6a995ed4de99dadd5e0f1f281bb8e.
  Open only after the reviewer records an independent invariant/site inventory.

The controller explicitly authorized controlled numeric reuse for these test
fixtures as a narrow exception to rule 8. Native resources and real production
writer/cleanup paths remain required. Not a native allocator-reuse proof.

Fresh reviewers A and B are independent of the design-review sessions and
implementation. Their reports live under ../../reviews/a and ../../reviews/b.
Broad acceptance is pending; a local frozen ref is not source adoption.
