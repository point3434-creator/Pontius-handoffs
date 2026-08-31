# R2 identity mechanism harness engineering review v2

Engineering closure review by mapping_compatibility, 2026-08-31. **SOUND for R2-H1 acquisition-through-teardown closure**, with the separately disclosed diagnostic-replay limitation below. This is not a final cold review, runtime result, fault-injection result, or production-source authorization.

## Exact reviewed pair

- H `1ffb59efd95c4a41b87b92de8fd56f26801ff918`; tree `5def226267155e2d72a88e9b24a76727760e5b38`.
- `rewrite-r2-identity-harness-v2-manifest.sha256`: `dcb016d9f4eb27d33d55ecba0d0a00ff87de1dccc76a90f095dc7230ac29a61d`.
- `tests-checks/rewrite-r2-identity-probe-v2.py`: `c654355be85a85fe53bb00c7e55201e6ccc969edb227d4159b26d415669bee38`.
- `tests-checks/rewrite-r2-identity-control-v2.py`: `e9537417f951343d7128663234aa05c758a4f32d11ce957b740c145120330039`.
- Compatibility `314c49262b68d6aaf34da6b5184804b8267beaeda5d5266c074e2576b90b85a3`; observer map `5463f81a8c3714e0970585c6b4b2eb9dd2bd547105c4ae6a8f9f53f0a08d699c`.
- Prior finding/review: `rewrite-r2-identity-mechanism-engineering-review-v1.md`, `9c09835e025bf33bcc7c526a0f3229844128fbf6b3fc07e1dc207c7c7e83a129`.
- Held candidate remains `c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f`.

Independently matched the manifest itself and all ten listed retained files to frozen Git blobs and declared hashes. Recomputed both exact predecessor diffs. Twenty-five preexisting probe definitions are byte-identical; only main changes, with new ObserverLifecycle and validate_lifecycle. Seventeen preexisting controller definitions are unchanged; its main/validate_result changes remain root's controller/custody review scope. Both original observer classes and shared mechanism/budget validators remain byte-identical. The new lifecycle validator is byte-identical between probe and controller. Original public-analysis try body and exception-handler ASTs are unchanged.

## R2-H1 closure

| Boundary | Static disposition |
| --- | --- |
| Capture before mutation, probe909–923 | ObserverLifecycle captures both original budget methods, twelve mechanism hooks and their code identities before any observer installation. Failure during this read-only capture phase propagates before a hook is mutated; it does not require fictitious rollback. |
| Construction/install/begin,942–974 | One protected acquisition try covers both observer constructors, budget installation/begin and mechanism partial installation. Any BaseException attempts close, adds scalar cleanup evidence when possible, then bare re-raises the primary acquisition error. Analysis-attempt counting occurs only after successful context entry. |
| Independent teardown,976–1014 | Mechanism restore/result and budget end/restore are separate attempts. A normal diagnostic failure does not skip the next cleanup. Nested finalizers independently restore captured original hook and class-method references, including partial installation, then verify reference and code identities. Returned observer reports and forced final identity checks remain distinct facts. |
| Body result/error,1016–1031 | __exit__ closes on both paths and returns False. Cleanup diagnostics do not replace a propagated body exception. Expected public exceptions already caught by the unchanged handler retain their type/message/depth classification; a cleanup failure separately blocks lifecycle admission. |
| Durable evidence,925–940/1033–1042 | Diagnostics retain strings/bools/containers, not exceptions or traceback objects. Original module/function/class/code references serve rollback only. No semantic reread, additional analysis call, original-budget charge, or new live-state retention is introduced. |
| Admission | validate_lifecycle requires acquisition, closure, both restored flags, no diagnostics and the exact25 completed normal stages. Incomplete capture/acquisition cannot create an analysis record or successful summary. After a completed case is printed, failed final identity restoration stops further analyses. Full admission also requires lifecycle_ok, separate from semantics/mechanism/accounting. |

The implementation closes the actual recoverable lifecycle gap. This conclusion does not require recovery from process death or an environment unable to execute cleanup/reporting.

## Disclosed dual-restoration diagnostic limit and root disposition

Probe main now aggregates mechanism_restorations from lifecycle.mechanism_restored: the final forced-original identity result. Controller validate_result still aggregates mechanism['original_methods_restored']: the observer's own intact/restoration report. If observer restoration reports failure but forced rollback succeeds, these differ. Summary replay can then reject the diagnostic stream rather than classify it as a fully reconciled lifecycle failure. This cannot create a successful mechanism/lifecycle result or development admission.

Root explicitly accepts this limit for the baseline-only dispatch: normal full observation requires both facts true; any mismatch is retained as incomplete/infrastructure/result-validation failure, with no semantic baseline claim and no source/development unlock. Stop if it occurs. This review does not certify cleanup-fault classification as a separate accepted product. The eventual successor GREEN adapter must preserve and reconcile the two named facts separately. Root directed no extra payload or harness round merely to relabel this already-rejected path.

## Method and limits

Read-only Git hashing, stdlib AST/source inspection under actual CPython3.11.15 -I -S -B -P, exact predecessor comparisons, and inspection of acquisition/normal-diagnostic/teardown branches. No candidate, Model, fixture, analyzer, observer, probe, controller or fault payload was imported/executed. No source/test/harness edit occurred. R2-H1 is source-closed; root retains all dispatch, custody/schema disposition and subsequent source-GO decisions.
