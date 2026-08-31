# R1 Gate A core01 results

The fixed first checkpoint passes on actual CPython3.11.15 and3.14.6 using
the same frozen source. This clears R1 Gate A only. A/B/C integration, full
original coverage, depth/generator/branch cost checks and final cold reviews
remain incomplete. No main commit or broader payload is authorized here.

## Identity and executed checks

Source c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f, H b1d15de062ac45c351f0254b358ee1e5fc35bdee,
manifest beb50fab0fe159249de1397529b78a71e2b176b8e3643ea64ccb37dbf1a1c15a.
Closure reviews and the dispatch were retained at H 43dd0551efbc462263c9839ed19593c53e28eed6,
manifest36e2dde4401f5f2aa9d8da3b7f5d386b251dda52417a48fd283327559aa9db9b.

Each slot ran six unchanged public analyses and eight unchanged independent
Model projections. Each exited0, completed every case and met all expected
classifications. Both clean controls retained their exact argv. Four original
budget stages were observed per case; all counters reconcile on both slots.
The outcomes and work counts are identical across slots.

| Fixed case | Observed result, both slots | Largest epoch work |
| --- | --- | ---: |
| shared-list-consumed | explicit refusal | 3565 |
| shared-list-dormant | clean | 5681 |
| class-adoption-unsafe | explicit refusal | 3826 |
| class-adoption-safe | clean | 6692 |
| hidden-cell-joined-reached | explicit refusal | 2797 |
| hidden-cell-joined-dormant | explicit refusal | 2773 |

The class-adoption unsafe case now refuses its reached protected class write;
the safe case remains clean with exact argv [-m,outer]. These were the original
r010 baseline's two failed expectations. Shared-list dormant stays clean with
[-m,fixed]; consumed reaches the protected-write refusal. Both hidden-cell
cases refuse unproved truth at line17, before their branch/join. Their expected
refusals pass, but do not demonstrate joined-cell execution.

The maximum6692 is below the unchanged production cap262144. It is not a
physical runtime comparison, a cost-scaling result or a15-second hand result.
The original baseline's smaller counters are not a valid speed comparison to
a changed analysis and accounting implementation. Gate B's196608 continuation
criterion is a separate unexecuted experiment, not a retroactive Gate A gate.

## Custody and independent verification

- Floor receipt: tests-checks/rewrite-r1-gate-a-r1-core01-311-receipt.json,
  SHA 9a59c48f5bc83452c30588237aa1ca93ce024885a7c8b3b451ec581622f2bd1f.
- Development receipt: tests-checks/rewrite-r1-gate-a-r1-core01-314-receipt.json,
  SHA 543a15a932aaddd6caeb2fed870bd95dfbaf84352e1e1c2e0c17b16acc8ee82a.
- Root floor verification SHA 2011a4151ed3db5ea8fef6463b6f9e1b024fbe5885414e9120003d7e8112c930.
- Root development verification SHA 618755f700fb59049d1ba8794e7512b117e72f05bb4957954b7ae7e53ebb96cc.

The reviewed controller ran under actual3.11.15 -I -S -B -P and gave each child
a separate fresh D-local r010 clone/detach with only the pinned generator and
harness overlay. Children used actual configured interpreters, -B -P, snapshot
cwd, scrubbed environment, snapshot/src PYTHONPATH and hash seed0. Each emitted
identity before candidate import. The development leg was unlocked only by the
successful floor receipt with matching source/controller/Model pins.

Root independently rehashed1770 floor and1775 development snapshot files (the
latter includes five pinned floor evidence files), all original watched
inputs and every raw output; replayed the six source-bound result records,
eight projections, budget sums and exit/summary agreement; and verified the
snapshot Git base. The reports retain exact commands, environments, snapshots,
output hashes and all counters. No source, cap, expectation or original test
changed between runs. No broad or guarded/GPU suite was run.

The first result-summary writer stopped before any artifact/navigation write
because it incorrectly expected1770 files in the development snapshot too.
The independent receipt verifiers had already rehashed the actual1770/1775
files successfully. The retained v2 summary writer corrects this reporting
assumption; no receipt, source, expected result or payload was changed/rerun.

## Next boundary

R2 remains prospective. The old Gate B four-way cost sources have an open-input
comparison-premise defect, recorded without changing their original bytes or
labels. The separately frozen identity-partition proposal repairs that premise
through a source-level language guarantee. It still needs a concrete reviewed
support/measurement plan, new pinned source/Model records, preservation of the
six Gate A and two original depth cases, and a new frozen controller before use.
No blanket scalar assumption, old-engine fallback or cap increase is allowed.

The implementation remains2198 added-plus-deleted lines relative to r010,
within the first-attempt2500 limit. The named finalizer and exact-candidate
main integration authorization remain later gates. This file records a bounded
engineering result, not a new accepted research decision or release acceptance.
