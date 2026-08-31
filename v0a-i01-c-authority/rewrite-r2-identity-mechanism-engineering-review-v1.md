# R2 identity mechanism harness engineering review v1

Engineering review by mapping_compatibility, 2026-08-31. **STRAINED: one required observer-lifecycle correction before baseline dispatch.** The baseline adapter and scalar replay shape are otherwise SOUND in the inspected scope. This is not a final cold review, production approval, or runtime result.

## Frozen pair and scope

- H: `c00f7375a7be68daff773b4d8c6413467aa2e6be`; tree `4ff7e8a61345146098af7ef46f056d0320876e29`.
- Manifest: `rewrite-r2-identity-harness-v1-manifest.sha256`, SHA256 `a2e7a238c4b87b46d6e48dad9106b13c39012fb674a4c0373b54873510815b5d`.
- Probe: `tests-checks/rewrite-r2-identity-probe-v1.py`, SHA256 `0c1d7065b21e7d45a002b2e83e3ada9e29a22e3129e9168378370f231500c5bb`.
- Controller: `tests-checks/rewrite-r2-identity-control-v1.py`, SHA256 `bb68e24c1d01b4b04eb499274c6d714c329ea8eab56cfb3a11f4394b92d5d2a9`.
- Compatibility: `tests-checks/rewrite-r2-identity-compatibility-v1.json`, SHA256 `6469769a98217daee063ff977f5d04ca4a3b5b426f5175bd75ab68aaccc466fb`.
- Observer map: `tests-checks/rewrite-r2-identity-observer-map-v1.json`, SHA256 `a685562866deec86553d8ca06b458269f06e3f015418401325e7c4d43c1a232b`.
- Held R1 source: `rewrite-r1-task5-source-v2.py`, SHA256 `c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f`.

Independent verification matched the manifest itself and every one of its ten retained files to frozen Git blobs and declared hashes. AST/source checks matched the twelve hook signatures/segments, six record layouts/segments, all two direct _CState constructors, and the map's source fingerprints. This review owns MechanismObserver, baseline compatibility, observer map and shared mechanism replay. Controller custody and input/Model/depth-envelope preservation have separate reviewers.

Normative basis: observer spec `4d4ed42a3fb132eb79c3a40bcb943268cbb2883a28152176c52d05c845791b52`; authoring disposition `34cb19a6ec98ea5b92219a50f9622f7aec2ed3c84139b4e78f7e7e9f02aed5ab`; frozen R1 hook inventory `2eaa321bf1f1dc97e567cf4ed3fa3418f9a57199a82bb967253de4be93d66a51`. The disposition changes only the old population pin to the corrected v2.

## R2-H1 — observer acquisition is outside guaranteed restoration

**Severity: required harness correction before execution; not a demonstrated production defect.**

Probe lines1151–1155 construct/install BudgetObserver, begin its case scope, and construct/install MechanismObserver before the try at1156. If begin, mechanism construction, or mechanism installation raises, the budget end/restore at1179–1182 is bypassed. MechanismObserver.install at867–883 rolls back its own partially installed hooks, but does not release the earlier budget observer. The frozen compatible source passes the static prerequisites; this finding concerns the explicit acquisition-failure path, not a claim that normal c8fc installation fails.

Close the whole lifecycle boundary, beginning before the first hook mutation: budget acquisition/partial installation, begin, mechanism construction/partial installation, body success/error, and both teardown paths. An error while collecting or restoring mechanism evidence must not prevent attempting budget cleanup; an error while ending the budget scope must not silently skip restoration. Preserve the primary failure and distinguish incomplete acquisition/restoration from an attempted or successful analysis. No invented case completion, successful restoration flag, or swallowed failure is acceptable. Preserve the original BudgetObserver/reconciliation implementation and semantic delegation; the correction belongs in bounded orchestration.

Root confirmed this finding and will require an immutable harness successor. No fix was made in this review.

## Positive static results

| Boundary | Checked result |
| --- | --- |
| Original delegation | wrap838–865 contains exactly one original(*args, **kwargs) call; ordinary return identity is preserved and the caught BaseException is re-raised. Observation failures are recorded separately. No retry, semantic helper call, consume request, or replacement result is introduced. |
| Scalar custody | Durable evidence uses scalar strings/integers/bools/None and containers of those projections. Arguments/results remain call-local; source frames are deleted after extracting the caller name. No state, AST, view, context, budget or exception is stored as evidence. Module/original-function/code references are installation/restoration controls. No cell/object-store reread reconstructs facts. |
| Active module and shapes | Each ordinary/depth attempt binds its actual active_generator. Exact _CAtom/_CRef/_CChoice, _CCellRef, _CState/_CView and _COutcome checks use that module's classes. _c_cell_write success is bool. _c_review_outcomes831–834 projects its supplied outcome tuple; it does not misread the returned four export lists as outcomes. |
| Births and lineage | The two source constructors are _c_state9321 and _c_fork9335, both wrapped. Each completed factory assigns a new monotonic birth, replacing the temporary id lookup on reuse. Snapshot is not a birth. Only successful writes become facts. Shared replay copies parent facts at each fork event's ordinal, before any later parent write. No live state is retained to prevent id reuse. |
| Helpers and unavailable roles | The first unwinding _c_invoke with the active module's exact helper-depth InventoryError supplies the originating event; replay requires incoming depth greater than64 and permits only one origin. Legacy exception tags remain diagnostic. The four absent R2 hooks are unavailable, not zero work or infrastructure failure, and cannot satisfy identity/deferred requirements. |
| Accounting and replay | Thirteen claimed unchanged probe spans, including BudgetObserver and budget reconciliation, are byte-identical to the predecessor. Controller budget reconciliation is also byte-identical. Probe/control validate_mechanism bodies are byte-identical. Copy attempts and completions are distinct; inclusive requested-unit spans are explicitly non-disjoint and not production work totals. |
| Evidence standing | Shared replay distinguishes observation completeness, semantic results, mechanism availability/met status, accounting, reserve and restoration. Four-leaf joins are only a limited observed baseline predicate. Sink helper normal returns are labeled as such, not actual source-sink occurrences. Known raises/handlers/resumes remain unavailable. A future R2 source needs its own reviewed adapter; this review does not certify those absent mechanisms. |

## Limits and disposition

Method: read-only Git byte/hash checks, stdlib AST/source inspection under actual CPython3.11.15 with -I -S -B -P, and direct comparison with the approved spec/disposition/hook inventory. No analyzer, fixture, Model, candidate, probe or controller was imported or executed. No runtime transparency, performance/headroom, successful baseline, or public semantic claim follows from these static checks. No additional finding emerged in this bounded lane. Keep v1 and held c8fc unchanged; inspect the lifecycle-only successor before root dispatch.
