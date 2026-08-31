# Prospective R2 identity observer/controller specification v1

Design authoring only, 2026-08-31. No executable harness, candidate source, fixture, Model, expectation or payload is created or changed by this specification. The old R2 harness remains held and byte-exact. Root must review this spec, the independent inputs, and the eventual exact harness before dispatch.

## Bound inputs and run scope

| Input | SHA256 |
| --- | --- |
| R1 candidate rewrite-r1-task5-source-v2.py | c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f |
| R2 plan | d5491bc204b07ec0e1f861b7cfe03facab9b8c9907a38726f64d96c096fe0d4f |
| Root premise disposition | bdf3b13684d50318c48ddbe3af1682b6e298136e21af3d1ef76ffe7a3f52e6b4 |
| Plan addendum v1 | 1a1a6bc7f8ef4c56a72735670ff0bb65e883f3aa559abec7b4fec01af6991998 |
| tests-checks/rewrite-r2-identity-cases-v1.json | 4834971b9d63aa182c1207959721b6bb65f742a106541d96975945060134d9ea |
| tests-checks/rewrite-r2-identity-population-v1.json | 30295f39daafcf265103cd78f3de50393c9111633ca3d5f8515e3f77c9a1197a |
| tests-checks/rewrite-r2-identity-coverage-v1.json | 05e24952ff5672554012bfb784215d76e44f7d95b2f3dbd1e3c0f8672d13ec38 |
| Original population | 3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce |
| Predecessor R2 probe / control | abc1a22b76691ab8881e5301f532fad32171183abb11221debc93e7428e48310 / 54c4e61fd07173fbf2f52441ae1dbb94d6dbfcaf3f7d9ee0e385509ac73bd7ba |

Use the successor population's exact order: original Gate A6, original helper65, original generator70, then identity-scale-n8-s4-d0-normal, identity-scale-n64-s4-d0-normal, identity-scale-n8-s4-d2-exceptional, identity-scale-n64-s4-d2-exceptional. Twelve public attempts and24 harmless Model projections:8 unchanged Gate A projections and16 new identity projections. Expected successful analyzer completion remains ten ordinary receipts plus two exact depth errors.

Default dispatch is one complete twelve-case R1 baseline, then one complete twelve-case integrated R2 candidate, each subject to root approval and floor-first rules. Intermediate source checkpoints are AST/accounting reviews only. No case selector, checkpoint subset, automatic expansion or old v5 diagnostic dispatch is provided.

Keep both original Gate A public envelopes and their Model projectors exact. New identity records use the byte/AST-exact existing name-environment public envelope, inventory and stable test identity. Their separately reviewed Model projector must instantiate Model(region) using the pack's exact-string true/false/none/other discriminants and exact allowed builtins. It does not assign instance.choice or reuse the old integer-witness projector. Each projection has a fresh namespace. Serialize only the pack's region/trace/result/ambient_result/work_result fields, never selector object, repr or id. These Models do not seed the public analyzer.

The two depth attempts retain original c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf tests, original setUp/_review/include_probe envelope and its fixture/probe/test-child sources. Do not invoke whole multi-subtest methods. Reuse the already pinned builders without modification: helper65 source94b070b8fcf2e66c42e1a779558e830d7caae670366f9313faf0989c722818c6 and generator70 source635e682b2253cd44201e2afdb95c288b9973f5629ec4eeb3c5bfd078743eb5e3. Require original InventoryError relationship and exact regexes ^analysis helper depth exceeds 64$ and ^analysis deferred generator depth exceeds 64$. Each setUp's fresh generator instance receives and later restores its own observers. Sensitive sources remain AST-only.

## Delegation and scalar identity rules

Preserve the existing BudgetObserver and reconciliation block unchanged. It remains the sole account of original initialization and consume requests, exceptions, before/after work, origins and creation stacks. Mechanism wrappers delegate their original callable exactly once with identical arguments, result and exception. They never call a semantic helper to obtain evidence, consume work, change limits or suppress an exception. Original wrapper identities and code objects are restored and checked in finally.

All durable observation records contain only exact primitive scalars, strings and containers of those values. Call-local original arguments/results can be projected while the wrapper is active; no AST, state, frame, context, exception, generator, view, function-result cache or budget is retained in data after that call. Static original function references needed to restore wrappers are not runtime analyzer evidence.

Map each observed budget to the existing BudgetObserver epoch. Read counter deltas from that observer's scalar ledger, not by inventing another meter. Inclusive span deltas must be labeled inclusive and never summed as disjoint total cost. Wrapper frames may change raw parent-stack attribution; disclose that observation effect and retain raw origins. Whole requested-unit reconciliation remains independent of mechanism attribution.

Do not treat Python id(state) as a durable branch identity. The preferred small adapter observes actual _c_state and _c_fork results and assigns monotonic per-case birth numbers; a new observed allocation replaces a reused raw-id entry. Fork records parent birth, child birth and event order. No state object is held. Static source inspection must confirm all state creation flows through these factories; otherwise state-path coverage is incomplete until the adapter is explicitly revised. Logical cell writes can then be reconstructed from completed writes and fork ancestry without rereading cell tables. Snapshot records do not invent value changes.

Adapter field shapes and return arities must be checked against each exact source before use. The roles below are a minimal interface, not permission to infer fields on an incompatible source. Missing new R2 roles on the declared R1 baseline produce unavailable coverage. Missing original BudgetObserver prerequisites or a mismatched pinned source is an infrastructure error.

## Natural observation seams

| Role / original-delegating seam | Scalars collected and completion rule |
| --- | --- |
| _c_eval / _c_statement | Source path, node kind/line/column, operation ordinal and nesting context; returned controls and state births. This supplies identity-decision, outer ladder, handler-body and deferred-element context without retaining nodes. |
| _c_identity_compare | Completed exact literal boolean versus distinct proved-boolean-unknown. Source site comes from enclosing evaluation. Attempt alone is not a completed comparison or split. Never inspect an unknown selector's equality/truth. |
| _c_state / _c_fork / _c_snapshot | Allocation/fork/snapshot attempts and completed returns; stable scalar birth/parent relationships. These counters do not imply any table was copied. |
| _c_join | Returned successor count, controls and state births under the active semantic context. Do not enumerate a supplied arbitrary iterable before original consumption. For a declared exact list/tuple input, a scalar input inventory may be taken at the reviewed boundary; distinguish supplied alternatives from the original returned tuple. |
| _c_cell_write | Actual supplied activation ID, name and safe literal projection, plus state birth and returned success. Commit a logical write only after the original returns true. No _c_cell_read or raw bank reread to reconstruct work0/work1. |
| _c_copy_dict | Exact dict length, caller role, budget epoch and attempted/completed copy counts and sizes. A throwing prepaid request is an attempted copy, not evidence that N entries were copied. No entry iteration by the observer. |
| _c_raise_known | Actual returned raised tag, explicit flag, origin path/line and successor birth. Constructors alone are not raised outcomes; legacy diagnostic exception tags remain outside this channel. |
| _c_handle_known_exception | Already-matched incoming tag/origin, handler site and input birth; returned successor controls/births and cleared/replaced exception metadata. It does not repeat matching. Handler call attempt, completed return and normal handled continuation are separate facts. |
| _c_resume_generator | Incoming active deferred depth and source/resume ordinal; actual internal yield/stop/raise/refused results. Observe original object-read/write results within this active span for exact admitted phase/cursor/range projections; never look up the object again. Body entry requires actual deferred-element evaluation, not merely invoking resume. |
| _c_invoke / terminal _c_review_outcomes | Original helper-depth context and originating exact helper-depth error; terminal known-raised outcomes escaping a public module/body review. Historical raised call summaries are not terminal escapes. |

The writer confirmed semantic roles in the pinned addendum: _c_identity_compare returns literal bool or _CBooleanUnknown; _c_handle_known_exception executes an already-matched handler; resume returns internal yield/stop/raise/refused; incoming ctx.deferred_depth is the active-body count. There are no telemetry-only production calls.

If exact availability cannot be observed from original record-read results and completed semantic operations, leave it unknown; do not reread stores or reconstruct the analyzer decision with helpers. The eventual source adapter must bind the original record/phase checks and deferred element site. A nonempty depth rejection is identified at the innermost originating exact InventoryError, with incoming depth64 and no element entry; outer propagation is not another rejection. Other work failures leave incomplete actions unknown. Exhausted/empty stop returns are distinguished from an entered body using actual admitted record evidence and absence of element entry. Running rejection precedes empty checks under the addendum.

## Required mechanism predicates

For each of the four new scale cases, one unresolved public analyzer invocation must demonstrate:
1. The three pinned identity sites are actually reached on their false-prefix path and complete as unknown builtin-boolean decisions; no constant specialization.
2. Actual true/false successor execution yields four distinct owned leaf states at the enclosing ladder join and before common continuation. Record the original join context and completed alternatives, not source branch counts.
3. The common sink is reached on each alternative, with one occurrence per feasible execution. Four alternatives are not four sequential executions. The public row policy may aggregate equal capabilities without erasing this mechanism record.
4. D2 additionally records the four completed work pairs (1,-1), (2,-2), (3,-3), (4,-4), corresponding actual known raises, and already-matched handler exits from those states. Reconstruct the pairs from completed write events/fork ancestry. Missing lineage or an unobserved write means incomplete coverage, never an assumed source value.

Only the independent coverage file supplies expected source sites and region mappings; the production analyzer receives no fixture label, region assumption or expected value. No mechanism is inferred from the16 Models. A sound D0 optimizer that removes state alternatives can be semantically correct while failing this declared experiment; do not manufacture work.

For generator70, record resume attempts, proved-empty/exhausted stops, actual body entries, completed yields/stops/known raises/refusals, maximum incoming/entered deferred depth and the single originating exact depth rejection. Its required result is the original depth error reached through actual nested consumption, not early unsupported element evaluation or work-cap exhaustion. No minimum yield count is invented: the depth error may occur before any nested element yields. Helper65 records its independent exact originating helper-depth rejection; a deferred error cannot substitute.

For all cases, known raised, handler attempts, normal handled exits, replacement handler raises and terminal escaped outcomes are separate counts. One raised value can appear in nested propagation records; do not sum those appearances into multiple executions. The original Gate A cases acquire no new mandatory branch or generator mechanism predicate.

## Budget, result and baseline schema

Keep an exact fourteen-record top-level stream: identity, twelve case records, final summary. Add mechanism availability/events/counters/verdict inside each case, not a new uncontrolled stream. The raw budget block is preserved. The successor schema/payload names must differ from the held original R2 harness.

Report independently: population/Model observation completeness; semantics and exact depth matches; mechanism availability/completeness/met predicates; accounting; per-epoch reserve; custody; restoration. A complete R1 RED stream can have unavailable mechanism and failed semantic/depth expectations without being an infrastructure crash. Conversely, unavailable is never successful zero work. A future R2 candidate missing a required role cannot pass mechanism coverage.

For every actual original epoch, reconcile initial work, all requested units and last observed work, including the throwing request. Apply196608 only after analysis as the engineering continuation predicate. Preserve262144 runtime work cap and all other caps. No average, selected stage, sum substitution, refund, reset, split or early stop at196608. Missing accounting makes reserve unavailable, not true. Original creation stacks/owners remain visible even if a new source location lacks a friendly phase label.

Scalar mechanism histograms and copy summaries are descriptive actual operations, not extra production charges or CPU/elapsed-time measurements. Retain attempted versus completed work. Any observation failure preserves original raw logs and marks coverage/accounting incomplete; it cannot manufacture a product pass. Observer overhead is disclosed and subject to the existing child watchdog.

## Custody, floor gating and authoring release

Adapt the existing controller, not a new framework. Require an explicit retained source path/SHA, exact new-core W watch and unchanged old-v20 W watch. Each slot uses a fresh D-local r010 clone/detach, private temp and a create-exclusive complete overlay manifest. Hash all1761 tracked paths and every declared overlay/provenance/control/run artifact before and after; derive the new total from the exact released payload list rather than reusing the old count. Original tests, public envelopes, builders and caps are explicit pins.

Retain actual interpreter pre-import identity/executable/patch checks, floor3.11.15 before dev3.14.6, seed0, -B -P child, scrubbed environment, snapshot/src PYTHONPATH, absolute regular non-reparse Git,60-second direct-child timeout and existing60-second Git setup/integrity timeouts. Outputs and prepared snapshots are single-use. Preserve partial raw stdout/stderr and explicit incomplete receipts after timeout, parsing or post-child custody failure.

Development admission replays a pinned successful floor receipt and its raw identity/case/summary/log/setup/manifest/input hashes. It must match source, probe/control/spec/observer adapter, both populations, all packs/coverage/Models/tests/builders, watches and environment contract; every semantic, mechanism, accounting, reserve, restoration and custody gate must be true. Failed baseline floor evidence does not authorize baseline dev. No duplicate/reused snapshot or automatic additional run.

Before executable authoring: root approves this spec and the separately reviewed four-case inputs/addendum. Before payload: release exact probe/control/observer-map/static proof, minimal predecessor diffs, Model-projector proof and source-bound hook compatibility inventory; independent review confirms no changed public/depth envelope and no expectation drift. An integrated source with incompatible natural interfaces requires an explicit adapter/spec successor, not guessed field access.

This specification supplies no executable code or dispatch authorization.

