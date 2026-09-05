# v0a consolidation r004 candidate report

The controller-approved narrow replacement is implemented and frozen for
independent review. Focused checks have passing runs on both interpreters;
the initial 3.14 inventory run and a baseline diagnostic retain a Windows
handle-reuse fixture failure. This is not adoption or a source seal.

## Identity and scope

- Commit: fe1e2fc68675c6c92a1263450b455011b5987207.
- Base: bb959371eec17e76ab46ee6e42f1bac49c26d54a.
- Tree: 27fa787e80f504f17233c29961d9df545f8eb7dd.
- Ref: refs/heads/review/v0a-consolidation/r004, local and unpublished.
- Manifest: 6eb5ec280b6a8051e88d7659920ef74b46ea682a06dc80f688ed951d75f3f221.
- Frozen packet: D:/Pontius/tmp/v0a-consolidation-r001-r004-frozen/.

The manifest was independently recomputed from all 17 frozen blobs, using
whole-row digest-first sorting. All ten core files match r007 commit
ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1 byte-for-byte. All 17 files are LF-only,
BOM-free, UTF-8, have no trailing whitespace and have one final LF. No added
manual line exceeds 100 columns. The five manual files total 357 additions and
29 deletions against the base; the cap is 600 additions. Generated inventory
and profile artifacts and the ten exact imports are excluded from that budget.

Compared with r003, only tools/generate_test_inventory.py,
tests/test_inventory_and_profiles.py, and tests/test-inventory.json changed.
The profile bytes, registration/boundary/CI slice, and r007 imports did not.
The generator diff against the base is 25 additions and 6 deletions, including
the four registration entries. The descriptor/receiver-provenance extension is
withdrawn, not patched. The correction detects inconsistent default alignment,
returns a typed reason and records it before filtering at both consumers.

There are 182 registered v0a test IDs in four files. The public capability
review has zero v0a exact rows, seven alignment blockers at the real host_case
call sites, and 141 existing exact rows with unchanged population digest
d303a26e373f0b173a4283dcede5735fdae6b849fdb0cb0ffcddec9017e8012a.
Both profile capability digests remain 64 zeroes. The known-unsound baseline
analyzer remains parked under ADR-0486; no general soundness claim is made.

## Focused verification

All runs used disposable D:-local copies, -B -P, snapshot cwd/PYTHONPATH,
scrubbed environment, absolute PONTIUS_GIT and D:-local temporary directories.
The complete 3.11 floor run finished before the 3.14 run began.

| Check | CPython 3.11.15 | CPython 3.14.6 |
| --- | --- | --- |
| test_v0a_hand_replay.py | 45 tests, exit 0 | 45 tests, exit 0 |
| test_v0a_trace.py | 53 tests, exit 0 | 53 tests, exit 0 |
| test_v0a_replay.py | 62 tests, exit 0 | 62 tests, exit 0 |
| test_v0a_contract_faults.py | 22 tests, exit 0 | 22 tests, exit 0 |
| test_stabilization_boundaries.py | 52 tests, exit 0, one POSIX skip | Same |
| test_inventory_and_profiles.py | 88 tests, exit 0 | Initial exit 1; fresh confirmation 88, exit 0 |
| generate_test_inventory.py --check | Exit 0 | Exit 0 |
| check_stabilization_boundaries.py | Exit 0 | Exit 0 |
| Ordinary registration --write | Exit 0 | Exit 0; all 17 hashes unchanged afterward |
| Four retained comprehension comparisons | All match Python binding | All match Python binding |

The complete sets therefore collect 322 tests, with one platform skip per set.
No broad profile or hosted CI is claimed. The inventory suite intentionally
prints negative-control refusals; 3.14 additionally warns about a synthetic
return-in-finally control. Neither is a test failure.

Receipts under D:/Pontius/tmp/:

- v0a-consolidation-r001-r004-311-1788559375464/: full floor run, results.json,
  per-command stdout/stderr, source-sha256.json and compatibility diagnostic.
- v0a-consolidation-r001-r004-314-1788559688086/: full initial development run,
  isolated handle diagnostic, compatibility diagnostic and registration writer.
- v0a-consolidation-r001-r004-inventory-confirmation-314-1788560041611/: one
  fresh full inventory-suite confirmation, 88 tests, exit zero.
- v0a-consolidation-r004-work/: RED against r003 and baseline, focused GREEN,
  floor registration writer, capability export, and tested source hashes.

The RED test exercises the public review with sensitive and plain-return helper
bodies and a nested sensitive wrapper. It distinguishes an explicit blocker
from both a crash and an exact row; it also requires capability approval to
refuse. Existing supported binding controls remain green. Independent baseline
comparison of the four retained comprehension probes shows the extension's
false-exact results are absent on both interpreters. These finite controls do
not establish global Python binding soundness.

## Retained Windows fixture failure

Initial r004 3.14 inventory run: AtomicAndGitBoundaryTests.
test_windows_persistent_close_failures_are_truthful_and_retryable, readback
subcase, expected replacement handle 624 but the 4096-open search found none.
The test failed before establishing its intended reused-handle schedule.
The full run contains 88 tests and exactly that one failure.

A fresh exact-bb95937 diagnostic also failed the same assertion, in the
published_disposal subcase with expected handle 740. Its receipt is under
v0a-consolidation-r004-handle-baseline/handle-test-314/. One isolated candidate
run then passed, followed by the single full-suite confirmation above. No
fixture or ownership code was changed, and no failed run is relabeled GREEN.

Both complete fixture methods match baseline source text exactly:

- _round7_windows_file_owners_bind_before_caller_failure:
  322b5e738ef6d19400c4c26877fbef8f6c667beb7ce82348d8e18830e32cff03.
- test_windows_persistent_close_failures_are_truthful_and_retryable:
  05e419b239446799ea503b5f70a4b2fe229bc5f3c9b9d68ce913483579dc3d01.

This demonstrates inherited fixture instability, not an ownership-code repair.
The exact reason a particular process fails to reuse the selected numeric
handle is unestablished. A passing confirmation does not erase that limitation.

## Preservation and remaining gates

Three files were copied back to D:/Pontius-worktrees/v0a-consolidation-r001
only after all 17 old destination identities and all tested source identities
were checked. Every final source hash matches the frozen candidate. The source
branch is codex/v0a-consolidation-r001, HEAD stays at bb95937 and the index is
unchanged and empty of staged changes. The dependency baseline and inherited
kernels are unchanged. No prior frozen candidate, review, sdd/ file, ADR,
source seal, experiment, main integration, or push was changed.

Independent reviews are separate reports bound to this identity. The known
fixture instability remains visible in the handoff. Source-seal readiness,
broader acceptance execution and any decision commit require the remaining
workflow gates and explicit controller authority. Other lanes remain parked.
