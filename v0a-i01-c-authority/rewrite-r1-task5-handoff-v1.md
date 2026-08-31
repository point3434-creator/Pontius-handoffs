# R1 Task5 v1 authoring handoff and open review ledger

Engineering authoring/static checkpoint only. This is not a cold review, GREEN result, executed candidate, or release approval. Candidate source and NEW W are held unchanged pending the coordinator's combined final-review disposition. No candidate import, analyzer/Model execution, tests, payload, commit, or change outside the authorized generator occurred in this authoring lane.

## Custody and scope

- Accepted plan: rewrite-r1-implementation-plan-v1.md, SHA256 18f8124432880016d6dd0690ed4d3b582b8e202c5bdda21ae48a65efa0ae521d.
- Root plan disposition: rewrite-r1-plan-disposition-v1.md, SHA256 64fbb4b0690d5555c6eebd7b96d0e8129115df01d44c4441e95cb8d98dd177a8.
- Source GO followed retained floor RED receipt a9bddbae63bf96bfa85a853ada42e0dde8a9f4a27c785a8f4c08c38ce33c8529 and root verification 954ee9a908033e0c43d8c7588837e3588398174f3a9e67c034469fa11fe6bc80. The two baseline class cases failed; this authoring checkpoint does not supply a new runtime result.
- Base: rewrite-r1-base-generator.py, SHA256 29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692.
- Candidate: rewrite-r1-task5-source-v1.py, SHA256 810cbb934e20a13c9c4794e3574bcb6a248ddc8b4a84a56045f6370c1a066cea, 1162622 bytes. NEW W tools/generate_test_inventory.py is byte-identical.
- Task5 insertion: rewrite-r1-task5-insertion-v1.txt, SHA256 c4f4d1e32f2ba189346186a8fbdd8909a334ad5b8d2ca28f9d139e7bab90004a; 357 lines.
- Task5 exact edits: rewrite-r1-task5-edits-v1.json, SHA256 91047534611d3674e245793384b5984b435bc9302c444dafba0371a7acfadd3c; 19 replacement pairs.
- Task4-to-Task5 diff: rewrite-r1-task5-from-task4-v1.diff, SHA256 ea059f59eb808054c257fa7318218ae9a8fbf2d5e8f80fc4956e459ad1d16bc3.
- Full r010 diff: rewrite-r1-task5-from-r010-v1.diff, SHA256 e2505f97371ec25d33bbc1929aeec8dc0a5f701c5d8df5b5ba620489c7bbe0f1.
- Authoring checker: rewrite-r1-task5-static-check-v1.py, SHA256 ca3a20372130b79170ae7a8c0794544ef196500cc3c22e71a1cc139e6e4e61e8.
- Authoring proof: rewrite-r1-task5-static-v1.json, SHA256 c4615f5262c8e404608f4c75fb3184276929b76eef803942943b6697ced28bd8.
- Coordinator source freeze: H d224ea401898e462b327c43f129822dd52168782, manifest afc26d19bf76e44694b4e88254946aa2607bf4ece45965098a67ff946e148401.

Actual floor 3.11.15 with -I -S -B -P ran only the retained AST/hash checker. It proved exact Task4-plus-edits-plus-insertion reconstruction, UTF8/LF preservation, NEW W equality, other16 protected hashes, approved binder normalization, exact original-byte restoration after removing the core/restoring binder/restoring the old public-function name, and 2044 additions + 7 deletions = 2051 changed lines (449 remain below the initial 2500 boundary). Core span is 2003 lines. The proof's last new_helpers entry at line27714 is the old function temporarily renamed in the checker AST during normalization, not an additional new function; the actual source retains _legacy_process_review_rows_r010 there. Actual Task5 added public helpers are _c_sink10723, _c_emit_sink10774, _c_review_outcomes10810 and _process_review_rows10929.

## Canonical public path and preserved boundary

The replacement _process_review_rows owns scope compilation, module/class execution, entry preflight, entry activation, helper/cell/list evaluation, outcomes and sink observations. It never calls the old resolver, preclassifier, review-body, registry, source-flow, helper-return or legacy_process_review_rows engine. The old public function is retained solely under its renamed symbol for later compatibility disposition; this is not a claim that all old private APIs were removed.

Every ordinary source Call selects the callable/receiver before operands and records canonical references plus a call-entry view. Calls bind references/defaults with the existing matcher and create fresh own-local banks; closure destinations are captured cell identities read from the current state. Class namespace slots remain distinct from the enclosing nonclass lexical frame. Class normal completion installs the class; failed completion retains preceding outer effects without installing it. Return/control/issues/state remain paired in ordered outcomes. No generic projection hydration or authority reconciliation is present.

_c_sink is the sole _CSinkObservation constructor. It reads current argv and environment, accepts only the active-worker executable with exact scalar argv tokens, and refuses a -c token before making the detached observation. Observation keywords contain only scalar data; environment contains immutable additions/removals/error. _c_emit_sink constructs closed terminal AST values, creates an empty _ExecutionScopeVisitor without visiting it, and supplies empty alias/assignment maps plus captured environment to the unchanged _process_definition. No live canonical state/ref enters that renderer. Its child-program branch is excluded by _c_sink; unexpected children are an InventoryError. This is a source-path proof for the admitted terminal route, not blanket purity of _process_definition.

Original public receipt/digest and native writer remain byte/AST unchanged. The only old top-level changes are the approved metered matcher and exact old public-function rename. All five caps and _AnalysisBudget.__init__/consume remain unchanged.

## Category closure from Tasks1–4

| Category | Implemented boundary in held v1 | Evidence/limit |
|---|---|---|
| COW ownership | _c_snapshot/_c_fork revoke parent writers and bank writers; new wrappers own detached data; shared monotonic arena IDs | Task1 reviewed source; no hidden budget retained by tables/views |
| Impossible value join | _c_choice empty raises InventoryError; container guard precedes tuple-copy charge | Task1 v2 exact approved correction |
| Stable lexical declarations | _c_scope includes pattern string bindings and comprehension walrus binding-only traversal, excludes implicit iteration targets and child-body loads | No runtime comprehension/Match precision added |
| Name read destination | _c_read_name distinguishes unresolved route/refusal, missing retained cell/refusal, current-function unbound/UnboundLocalError and free/global NameError | No missing snapshot interpreted as failed open-instance lookup |
| Delete | _c_delete checks missing/unbound destination before write; failures do not silently become normal | Store algorithm otherwise unchanged |
| Truth | _c_truth proves scalar/native-sequence truth only; If/Not refuse opaque protocol consumption | Hidden joined pair may stop here; passing refusal is not join/cell execution proof |
| Source-order failure | Dictionary entries apply/validate each earlier expansion before later operands; Call stops at first unsupported expansion; Import preserves prior non-normal outcomes | No general kwargs/mapping expansion support |
| Environment overlay | Initial inherited environment then exact overrides admitted; repeated/later inherited expansion after additions explicitly refuses | No stale earlier override preserved |
| Function/class construction | Defaults/decorators/header effects occur in outer frame; annotations/typeparams/custom decorators and reached unsupported forms explicitly refuse | Deferred function creation does not execute body; invocation precision excluded |
| Helper call ownership | Captured cell/default refs plus fresh own-local allocation; current list owner for append | No crossmodule helper execution claim |
| Depth | Exact InventoryError('analysis helper depth exceeds 64') on existing >64 path guard | Synthetic entry occupies the initial path; helper65 readiness is static, not runtime proof |
| Matcher | Six allowed read wrappers and guarded charges normalize exactly to r010 | Explicit canonical proven_bound bool; expansions rejected before this budgeted matcher path |
| Outcome evidence | Trace predecessor edges and per-outcome visits; same sequential sink increments, alternative keys compared | Explicit/excluded-handler forwarding is an R2 obligation; no nondefault R1 producer |

## Accounting map and known gaps

Operation context supplies the current phase owner. There is one scope-certificate budget per source, a module-definition budget per source, an entry-preflight budget and an entry-body budget. All helper calls in that body reuse its owner; no helper reset/refund/new epoch is introduced. This describes the proposed ownership mapping, not a claim of unchanged legacy ordinal cost. Actual stage counts/cost fitness require the frozen public harness.

Task1 ledger rewrite-r1-task1-ledger-v1.md SHA256 7a660a6ead08338e840f6db0e9d6a1bcbc1258ef0ea3b271017746bd2c0bb592 and its v2 correction c45d652344b9e408ac2b49f3b8e7760e0149076ff0f20a53be5599c6d00a9749 remain the primitive basis: n-entry dictionary copies charge 3n+1 for visits, key/value references and allocation; table/bank copy charges remain real. Tuple/list copy charges distinguish visits from retained references. Linear scope/name scans and whole-table COW are paid and remain fitness risks.

Matcher guards charge only reached allocations/loops. Positional copy is 1+2N; default map/slice and allowed-key construction are separately charged; set/dict probes and positional_defaults.get use the six approved _c_binding_read wrappers. The nondefault supplied-value lookup now pays the additional id(expression) identity-key unit. Original any() short-circuit matching remains exact: canonical callers reject expansions before matching; unsupported expanded standalone budgeted matcher calls are outside that restricted accounting domain. Original unbudgeted private callers are not changed. No flat charge is claimed for unreached scan elements.

Task5 introduces these work families: detaching argv/keyword/environment values; allocating terminal syntax; traversing linked trace nodes/edges; building row/blocker/census/helper-edge dictionaries; source-site dispositions; aggregating per-module/per-entry output. Local consume sites are explicit. The following FINAL REVIEW FINDINGS ARE OPEN in held v1 and are not prepaid elsewhere:

1. Module output extends have no charge; entry output extends charge N but also retain N destination references, requiring 2N under the selected ledger.
2. Four early preflight blocker dictionary/append paths lack their added-work charge under the existing preflight owner.
3. _c_emit_sink's two-element result tuple lacks allocation+two-reference charge on success and refusal paths.
4. Entry preflight presently checks signature and four fixture names but does not yet reject all unsupported constructor/attribute/framework hooks before manufacturing an instance. The independent semantic reviewer is finalizing the bounded namespace admission rule.
5. _c_sink currently returns the default None abstract result. That is unjustified for general subprocess APIs. The accepted narrow direction is an unproved result whose unsupported consumption refuses, while discarded results remain harmless.

These are source-proved review concerns, not executed product REDs. No v2 changes have been applied in this handoff. The coordinator owns combined correction scope after both reviews finish.

## Acceptance and remaining limits

The fixed GateA population remains six analyses/eight harmless Model projections: two required-clean, three required-refuse and one permitted-refusal. Required clean rows remain exact shared-list-dormant [-m,fixed] and class-adoption-safe [-m,outer], without blockers. No fixture keys or special self.choice facts were added. The hidden pair's opaque truth may conservatively refuse and supplies no precise branch/join evidence.

Only the six selected public cases are the initial gate, not a declaration that all original contracts already migrated. R1 excludes general Try/exception correlation, generator/comprehension runtime, crossfile helpers, custom protocols/descriptors/metaclasses, non-stable-id fixture/probe entry, and child-program analysis with explicit reached refusals where encountered. A future requirement cannot be discharged merely by optional refusal. The newly identified original GateB open-self.choice benchmark premise remains unchanged/held by the coordinator; no inert-unknown assumption was added. Original test/private API compatibility and broad migration remain later dispositions.

Source is held. No performance, GREEN, end-to-end semantic, no-regression, or release-readiness claim is made.
