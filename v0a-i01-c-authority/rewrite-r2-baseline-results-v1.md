# R2 baseline r2-base01: complete RED observation

Actual CPython 3.11.15 ran the fixed twelve-case population once under frozen
harness H 1ffb59efd95c4a41b87b92de8fd56f26801ff918 / manifest
dcb016d9f4eb27d33d55ecba0d0a00ff87de1dccc76a90f095dc7230ac29a61d.
Source: c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f.
Run authorization: H 97eb904172dace05620e68aa62fb4e8e9132b8ab /
3971b873350204861bea09d78ee8b0148eed391c09e4a4e7217116d9686cf3e2.

Receipt SHA-256: 7b93ce869bca7697036e1f91bb31473d9c8f29dd51117c89f1544b4b1dda7382.
Independent raw-record/custody verification SHA-256:
4abd473dc5893eb06a35732fb5a59154620950fd0ab4937f2a465787c4d1151d.
Both files and all five original output files are retained with this result.

There were twelve public attempts, twenty-four matching Model projections,
eleven returned review receipts and one exact expected depth error. The process
exited 1. Observation is complete; semantic completion and success are false.
All 1778 snapshot files, frozen inputs and worktree watches rehashed correctly.
Budget, mechanism and lifecycle observation had no errors. Every case completed
the exact clean lifecycle and restored both observers. No diagnostic replay
limitation was exercised. No development run followed the failed floor.

| Case | Expected behavior met | Maximum requested units in one original epoch |
|---|---|---:|
| shared-list-consumed | yes, protected namespace refusal | 3565 |
| shared-list-dormant | yes, clean fixed action | 5681 |
| class-adoption-unsafe | yes, protected namespace refusal | 3826 |
| class-adoption-safe | yes, clean outer action | 6692 |
| hidden-cell-joined-reached | yes, unsupported truth refusal | 2797 |
| hidden-cell-joined-dormant | yes, permitted truth refusal | 2773 |
| helper65 | yes, exact helper-depth InventoryError | 22925 |
| generator70 | no, GeneratorExp refusal instead of exact deferred-depth error | 2892 |
| identity N8 D0 | no, unsupported truth protocol | 2939 |
| identity N64 D0 | no, unsupported truth protocol | 14951 |
| identity N8 D2 | no, unsupported Try statement | 2386 |
| identity N64 D2 | no, unsupported Try statement | 14286 |

All original epochs reconcile, including eight per original depth envelope and
four per other case. No epoch exceeds the 196608 requested-unit continuation
ceiling. These are early-refusal baseline costs, not evidence that a completed
R2 implementation has reserve or runtime headroom. The hidden-cell pair still
does not prove execution of an unknown branch join.

The same five cases fail the required mechanism gates. R1's absent identity,
known-exception and deferred-resume roles remain explicitly unavailable. Their
absence is not an observer error or a passing zero. The original helper-depth
origin was observed and matched its actual incoming-depth predicate.

This supplies the planned RED for bounded source work. No fixture, Model,
classification, public envelope, policy, limit or source changed during the run.
It is not whole-C acceptance, a performance comparison, or a live-hand result.
