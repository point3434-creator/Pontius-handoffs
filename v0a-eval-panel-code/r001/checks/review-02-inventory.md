# Independent pre-check inventory: review 02, Codex

Recorded before opening any checks/ file, from the handoff, pinned requirements,
and frozen candidate source. No sibling review or ledger was opened.

Candidate: b1fdacf157649ca92d1aee3e39b7b0471edbcd5d
Base: f647a7989394f084875a040b20c41891168163ed
Manifest: 376dff405c15301a489ea3fde84abc3a41c2afa4c33c6ee67423477ca9e08b8e

| Invariant or risk | Observable requirement | Related frozen paths and evidence |
| --- | --- | --- |
| Identity and scope | Exactly seven changed paths; base and tree match | Git objects; manifest |
| Root replay | Kernel history, actors, state and own legal decision agree | eval_bridge; betting |
| Cards and ranges | Ascending distinct board; compatible 1081/990 universes | holdem_cards; river |
| Key completeness | All root fields come from actual replayed state | immutable_blueprint; spine |
| Capacity | Nested-prefix wire size; boundary digests and exact membership | artifact codec |
| Teacher | Two forced kernel settlements; exact totals; CHECK ties | betting; river; game |
| Reference | Singleton hero, raw unit deals, fixed CALL, domain for error bound | continuation |
| Float validation | Forced values, exact dyadic lattice and legal best map | evaluation |
| Plans | All required inputs frozen before work; finite budgets; fixed s=4 sample | panel tool |
| Phase stop | No full solve; first disagreement or resource exhaustion fails | run_plan; worker |
| Ownership | Suspended worker assigned before resume; all failures clean up | host Job; supervise |
| Run retention | One begin/finish; result and journal survive failed/interrupted work | execution |
| Run identity | Worker cwd equals run root; no duplicate admission/context | session; Source |
| Measurements | Separate operation costs, work counts, cold/warm and memory labels | panel tool |
| Tests | Independent negative controls at real claimed boundaries | new suites; harness; cases |
| Budget | Entire Slice A remains inside inherited budget or needs ruling | brief; source counts |

Dependencies to inspect beyond the direct inventory as required by actual calls:
blueprint codec readers/writers; immutable key validation; legal decision and card models;
continuation normalization/traversal; expected_utilities/best_response distributions;
settlement/terminal transition rules; native Job ownership and cleanup primitives;
execution context/admission and finish_run writer; status_generation consumers;
focused-test harness source-verification, source sealing and fixture resolution.

Particular failure traces to challenge independently:
missing/nonfinite or ill-typed resource values; omitted or altered sample/control inputs;
board/hero collisions; different stacks; malformed worker events; startup/assignment failure;
parent interruption before/after worker ownership; cleanup exceptions; output creation failure;
partial observations on budget exhaustion; false integer ties and wrong non-tie selected actions.

Review is static plus supplied executed receipts only. No project code, tests, solvers,
hosts, tools or measurements will be executed. Frozen base dependencies are authoritative;
source assertions alone do not establish real OS behavior or retained measurement results.
