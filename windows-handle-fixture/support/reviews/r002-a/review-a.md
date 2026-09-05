# Cold implementation review A — Windows handle fixture FIX r002

## Binding and verdict

- Candidate: `c7de23de276c50463d831f3983fede82a5400ce8`
- Base: `5e56e4454f7b8ccb360d3e36245abc33318349bb`
- Tree: `014ee05a5014181bd63471247e5ee09607bb2346`
- Manifest SHA-256:
  `f5e06a5fa9d0fdf37888d29f8bfe6b395b6fc40a4c6f87258f66c95aa17421ed`
- Defect counts (Critical / Important / Minor): **0 / 0 / 0**
- Specification verdict: **PASS**
- Engineering-quality verdict: **PASS**
- Overall defect verdict: **CLEAN**
- Design verdict: **SOUND**

No required correction remains. The five r001 over-width expressions were
reflowed without executable-AST change. The only AST difference is the
mechanically rederived `string_sink_decoy_sha256` literal, whose frozen value
passed the real analyzer-backed self-census on the supported 3.11 floor.
Inventory and profile bytes are unchanged from r001, no newly added r002 line
exceeds 100 columns, and no codec, analyzer, writer, secure-filesystem, runtime,
CI, status, decision, or production path changed.

The task-local controlled-numeric-reuse design is unchanged in substance from
the r001 design already found sound. The facade remains bounded to the approved
test seam while the writer, resource acquisitions, ownership/cleanup paths,
native resources, namespace work, and facade-bypassing native oracles remain
real. Whitespace reflow and one derived expectation do not introduce a design
residual or justify reopening the settled design.

## Findings

None.

## Frozen identity and raw-blob scope

The review resolved raw Git objects in the packet's `authoring` checkout using
absolute `C:\Program Files\Git\cmd\git.exe`:

- `refs/heads/review/windows-handle-fixture/r002` resolves to the bound
  candidate.
- The candidate is a commit whose parent and tree match the bound base and tree.
- Base-to-r002 `diff-tree -r -z --no-renames` contains exactly two modified
  paths: `tests/test-inventory.json` and
  `tests/test_inventory_and_profiles.py`.
- r001-to-r002 `diff-tree` contains exactly one modified path:
  `tests/test_inventory_and_profiles.py`, at `+15/-6`.
- The r001 and r002 inventory blob object ID is identically
  `e36ac6213decc0e3dc9cc9f38559fcf9fa5bed6c`.
- The r001 and r002 profile blob object ID is identically
  `685a65c9cd8c0a8c7a347c94832cbc0370a6fd1a`.
- The source blob changes from
  `1103b6f3c523daa703496dd3249afa95db698a18` to
  `75fdc9bf532958bf5d0300488dc828a5d3a1d66a`.

Independent raw-blob hashing produced these digest/path pairs:

```text
inventory digest: 0b07a2ac105e6fce052f923322836b94a36a14d9c174b5d2cc085c7baa29664f
inventory path: tests/test-inventory.json
source digest: f9efa98ee407b035b1f971bf0191400287f0799130d63df235921cbd75f107df
source path: tests/test_inventory_and_profiles.py
```

Serializing both as whole-row-byte-sorted, two-space-separated, LF-terminated
rows reproduced the packet manifest exactly. Its SHA-256 is the bound manifest
digest. Each frozen blob also matches its corresponding `packets/r002/files`
overlay byte for byte.
The packet candidate JSON has exactly the workflow's required schema fields;
its file SHA-256 is
`d3c130a334c522fc611adaafe725f6b0ddccf65a3266c370bfe3dc7d861d655e`.

## Independent correction inventory and deferred claim

Before opening the deferred FIX claim, I recorded the governing invariant and
all six observed edit sites in `reviews/r002-a/initial-inventory.md`, SHA-256
`1d5c2f6e3a5c9b0acfa12ac5e241f7d6df4db6d9bc2158ebaac6d0d6cb260a22`.
The six sites are the five required expression reflows plus the one derived
census-digest literal. The raw r001-to-r002 diff exposed no other edit.

Only after that record was written did I hash and open
`correction-coverage.md`. Its SHA-256 matched the pinned
`c03afd7bf7370a395ce5a5f61336166dc0484a83d6aa3d0988b6b6cb4f67d96e`.
Its category, discovery method, members, limits, and falsifying observations
match the independent inventory. In particular, the claim requires an
all-added-lines width census, AST equivalence before normalizing the derived
digest, unchanged inventory/profile bytes, and execution of the frozen census;
all four are covered below.

## Static correction verification

The independent read-only probe `reviews/r002-a/verify_r002.py`, SHA-256
`f9de64608d77a4a1b39291b6417cb3bffaee8e5a3f5069959fb1a5fb1f0b5481`,
ran under CPython 3.11 with `-B -P` and exited 0. It established:

- parsing both frozen source blobs and replacing only the old/new census
  constant with one neutral placeholder produces identical complete AST dumps;
- the r001 base-to-candidate added-line scan independently reproduces the five
  violations at 101, 103, 104, 106, and 107 columns;
- every r001-to-r002 added line is at most 100 columns, with a maximum of 91;
- the r002 source is LF-only, BOM-free, final-LF-terminated, and has no trailing
  space or tab;
- inventory and profiles are byte-identical between r001 and r002;
- the r001-to-r002 path set contains only the declared test source, which also
  establishes that codec/analyzer and all production blobs are unchanged;
- the `_ControlledWindowsHandles` class remains below the 200-nonblank-line
  design cap (165 by the probe's inclusive AST class-span count).

## Fresh snapshot execution

Each execution used `run-snapshot.ps1` with a unique retained snapshot,
`-Overlay packets/r002/files`, the named interpreter slot, snapshot-root cwd,
`python -B -P`, snapshot `PYTHONPATH`, a scrubbed child environment, and the
absolute regular/non-reparse Git executable in `PONTIUS_GIT`. The floor ran
first. The runner's interpreter/module-resolution preflight passed before every
payload, resolving `pontius.immutable_blueprint` from that run's snapshot.

### CPython 3.11.15 focused native controls

Run name `r002-review-a-focused`, slot `311`:

1. `test_windows_controlled_reuse_preserves_native_resources`
2. `test_windows_controlled_reuse_detects_production_replay`
3. `test_windows_controlled_reuse_releases_unpublished_and_leaked_handles`
4. `test_windows_persistent_close_failures_are_truthful_and_retryable`

Result: **4 tests, OK, exit 0, 1.349 s**. Raw run-record SHA-256:
`2f5e87b7ef9c2b5eca727c2f61ff8fe733384b057707e71352fc41509fcc8830`.

### CPython 3.11.15 frozen analyzer/self-census

Run name `r002-review-a-census`, slot `311`:

- `CheckedInInventoryTests.`
  `test_working_discovery_binds_every_entry_and_introduced_id`

Result: **1 test, OK, exit 0, 48.929 s**. This executes the unchanged analyzer
against the frozen r002 source and validates the rederived
`c62e275fa42bcb8cc9bef4a382990793adc03ecc9d9db1b6fcd35aeb9b23372e`
expectation together with the surrounding census. Raw run-record SHA-256:
`8534f01a229cb1896ae0181d570884015da9975c366bfadd6331f3e112fbbb3d`.

### CPython 3.14.6 focused native controls

Run name `r002-review-a-focused`, slot `314`, with the required exact-slot
permission:

Result: **the same 4 tests, OK, exit 0, 2.837 s**. Raw run-record SHA-256:
`390b5e8e992e8ff69732e3b3cf4f72e6436a0754d7471028f6ed72901b61120e`.

Post-run read-only audits found only the two expected base-relative overlay
paths modified in each snapshot. Their source and inventory SHA-256 values
match the frozen manifest rows; the unchanged profile SHA-256 is
`0c2c457fd29a4c68ae1df29f64d2bc0141678762c0154dd960daca7f8d273682`.

## Requirement-to-evidence summary

- Reflow all five r001 E501 sites and no others behaviorally: **Pass** by raw
  r001-to-r002 diff plus normalized complete-AST equality.
- No newly added line over 100 columns: **Pass** by all-added-lines census;
  r002 maximum is 91.
- Derived census literal is mechanically correct: **Pass** by the real
  analyzer-backed frozen census test on 3.11.
- Inventory and profile bytes remain unchanged from r001: **Pass** by raw Git
  blob identity and byte comparison.
- Codec, analyzer, and production bytes remain unchanged: **Pass** by the exact
  one-path r001-to-r002 `diff-tree`.
- Approved real-writer/native-resource controls retain behavior: **Pass** by
  the four focused native controls on both supported slots.
- Packet, ref, and manifest identity is authentic: **Pass** by independent raw
  Git and raw-blob manifest recomputation.
- Exactness and size hygiene: **Pass** by LF/BOM/trailing/final-LF checks and
  the adapter cap.

## Limits and deliberately deferred gates

- This correction review is intentionally bounded to the r001 Minor finding;
  it does not reopen the settled fixture design or manufacture a behavioral RED
  for a whitespace-only correction.
- I did not read implementation narratives, design-review narratives, or any
  other r002 implementation review. The controller-authorized r001 review A and
  B reports were used only as the required-finding inputs for this FIX round.
- I did not modify candidate, packet, authoring, test, generated inventory,
  profile, production, codec, analyzer, or repository bytes. New writes are
  confined to `reviews/r002-a` plus runner-created snapshots and run records.
- I did not run the complete inventory suite or the 19-command codec acceptance
  population. Under the workflow and the controller's instruction, those broad
  gates run only after both Tier C reviews are CLEAN.
- This verdict establishes only the approved finite Windows fixture repair and
  its task-local rule-8 exception. It grants no general filesystem-double,
  operating, research, integration, commit, or push authority.
