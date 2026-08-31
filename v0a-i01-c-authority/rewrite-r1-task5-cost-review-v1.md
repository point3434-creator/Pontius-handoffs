# R1 Task5 final-source cost and ownership engineering review

Reviewer: Codex / authority_cost_audit. Read-only source inspection; not a cold review, analyzer test or acceptance verdict.

## Frozen target

- H commit d224ea401898e462b327c43f129822dd52168782.
- rewrite-r1-task5-source-v1-manifest.sha256: afc26d19bf76e44694b4e88254946aa2607bf4ece45965098a67ff946e148401.
- rewrite-r1-task5-source-v1.py: 810cbb934e20a13c9c4794e3574bcb6a248ddc8b4a84a56045f6370c1a066cea.
- Predecessor rewrite-r1-task4-source-v1.py: 3511f60a62fc9588f153ba3db6b05ac228a1ce235cb23a5316000ce7ba4e550c.
- Root's executed AST/hash-only report coordinator-rewrite-r1-task5-static-v1.json: 1de05b784c831317de9ce051fc7626abb4abd0772ddab0e8a7ec024df5d39f3c.

The source and manifest hashes were recomputed. I compared the retained sources, read all new terminal/orchestration code and changed evaluator/call sections, and performed narrow stdlib AST inventories. I did not invoke the final verifier or any analyzer/test/fixture/Model/controller. Root's verifier reports structural preservation and20 unchanged inputs,2044 added plus7 deleted lines (2051 total); I read that report and separately inspected the semantic terminal path below.

## Open accounting finding: newly added output plumbing

**T5-C1 — Important to the honest-work contract; high confidence except the explicitly identified hook-loop accounting interpretation.** The category is newly added preflight refusal/output aggregation work performed after an original budget owner already exists. Enumeration covered each new public orchestrator append/extend, its early refusal branches, and the terminal adapter's return boundary. This is not a request to remeter retained pure policy internals or invent another budget.

1. At10976-10978, the module-result blockers/sites/edges.extend calls copy the three returned lists without charging their visits or installed references. _c_review_outcomes pays for producing separate returned lists; that is not prepayment for these copies.
2. At11059-11063, the analogous body-result extends pay N total. Under the copy ledger used by list/tuple construction, copying N entries visits N and installs N references; the second component is absent. The author independently agreed these aggregation charges are incomplete.
3. After preflight is created10995, invalid class/method/duplicate/signature branches11001-11004,11008-11011,11021-11024 and11038-11041 allocate _review_blocker's four-field dictionary and append it without a corresponding construction/reference charge. The existing preflight owner can pay this work; no new epoch is needed.
4. _c_emit_sink10802-10807 returns a two-element tuple on policy refusal and success. Its success precharge is the dictionary allocation/copy plus added metadata; the new return tuple's allocation and two retained references are not charged. The author agreed no earlier prepayment covers either return. Compare the explicit five-unit four-element return tuple at10925.
5. At11034-11037, the fixture-hook loop pays one unit per name and then performs namespace.members membership. The contract distinguishes a visited name from its table probe, as the scope and binder helpers do. On that interpretation one component is missing per reached hook. This is part of the same preflight sweep, not an instruction to count Python iterator implementation objects.

The author confirmed the first four gaps and keeps v1 frozen. No source correction has been inspected here. Preserve source evidence; a successor should reconcile this whole small output/preflight category against the ledger, not only one reported append.

Input decoding/inventory selection and final unchanged _normalise_review_rows/sorting are not included in this finding. Their treatment is an explicit original-policy boundary, not evidence that every CPU operation in the public function is metered.

## Closure of earlier source findings

- **T3-E1, inherited environment ordering:** _c_eval_dict10111-10177 now evaluates one key/value or expansion pair at a time, checks the expansion before the next pair, and rejects inherited expansion after prior inheritance or accumulated additions. Earlier explicit overrides cannot survive a later admitted inherited expansion. Each expansion is read from its own successor; later expressions cannot retroactively alter that expansion snapshot. Final additions receive container(len(additions)) and the remaining ordered pair-copy charge. This closes the reviewed source mechanism without a general environment interpreter.
- **T4-C1, nondefault identity lookup:** _c_invoke10694-10696 charges the identity key only on the nondefault branch, in addition to the existing visit/lookup charge. Default lookups do not acquire that extra charge.
- **T4-C2, canonical depth error:** _c_invoke10661-10662 now raises InventoryError('analysis helper depth exceeds 64'). The synthetic unittest call starts with an empty helper_path and contributes the method entry;64 nested helper activations can be entered, and entry into the65th encounters a parent path length65 and the existing greater-than64 guard. That establishes the selected-method source mapping; it is not an executed helper65 result or a claim about every future entry category.
- Call observations now name caller_frame explicitly and retain helper_path; the record charge increased to11 for the ten-field observation.
- Cross-module helper invocation explicitly refuses before activation. No defining-module ownership is inferred from an unrelated caller frame.
- Starred and keyword expansion fail at their ordered boundary. The metered binder still has one canonical caller10668 supplying ctx.budget and exact bool proven_bound. The synthetic entry has no operands; reached expanded syntax does not reach the matcher.
- Nondefault explicit/excluded-handler fields remain outside this R1 subset. No new producer establishes broader exception/finally support.

These are static closure conclusions on this exact source; public behavior remains to be measured.

## Original budget-owner mapping

The only new _AnalysisBudget constructions are the four source sites in _process_review_rows:

| Site | Owner | Reused by |
| --- | --- | --- |
|10959|One certificate budget per parsed source|_c_scope/free-route/signature facts and shared program setup.|
|10966|One definition-protocol budget per source|Eager module/class construction, its helper calls, observations and unowned import-time reporting.|
|10995|One preflight budget per eligible selected method|Class/method lookup, duplicate entry/signature/hook validation. No method body runs to discover receiver names.|
|11042|One body budget per admitted selected method|Activation, all nested helpers, canonical state changes, observations, terminal conversion and body result aggregation.|

These correspond to the original certificate, definition protocol, selected-entry preflight and direct-body stages. I found no _AnalysisBudget construction in a new _c_* helper, no recursive owner replacement, reset/refund or table/view budget selection. The entered context10709-10710 retains ctx.budget and the same arena. Shared program facts are built once; retirement of old repeated walks does not incur artificial parity charges.

COW ownership remains through the canonical snapshot/fork/write helpers. Method entry forks the saved module state; call entry/post-result views revoke write ownership; object and activation-bank copies remain charged. The namespace/function/list/cell authority is not hydrated from detached report fields. Cost can still grow through snapshots and retained activation banks; no measured fitness or headroom follows from this source review.

## Terminal-only legacy policy proof

This review went beyond the absence of direct old-engine names:

1. The new source has exactly one _CSinkObservation constructor, at10769 in _c_sink. It requires the selected executable to be the exact sys.executable symbol. Every later argv token must be an exact literal string, and exact '-c' is rejected10743 before the observation is created.
2. The immutable observation retains a detached tuple of those exact strings. _c_emit_sink reconstructs those same tokens as ast.Constant values, with no rewrite that can introduce '-c'. Its only caller is _c_review_outcomes10878.
3. _c_emit_sink10798 calls _process_definition with non-None ctx.budget and a captured environment triple. Therefore that policy's fallback-budget and _environment_delta branches are not selected.
4. All retained old child-analysis routes in _process_definition are inside its exact '-c' in argv branch: _ExecutionScopeVisitor25735, _source_ordered_helper_return25760, _SourceOrderedResolver25773, recursive _process_definition25824 and _runtime_call_bounds25886. The admitted terminal argv cannot enter that branch.
5. The empty _ExecutionScopeVisitor10797 is constructed but never visited. Its initializer7868-7884 allocates eight empty containers and retains nine fields; together with the instance, the18-unit precharge matches this structural work. No live bindings or execution are reconstructed in that object. The captured environment avoids its legacy mutation-analysis use.
6. A nonempty children result is additionally an impossible-state InventoryError. That check is a secondary guard, not the proof that child analysis never executes.

The root's direct-call inventory has no direct route to retained live engines from new code. The argument above establishes this bounded terminal route, not an unrestricted whole-program transitive-callgraph theorem. Retained pure qualification/static-literal/capability/normalization policy helpers remain dependencies.

## Evidence limits and disposition

T5-C1 remains open before claiming complete accounting. The fixed Gate A still must execute on the exact corrected source through the reviewed snapshot controller, actual floor first and matching dev only after a successful floor. No payload or speed claim is made here.

R1 now explicitly refuses opaque implicit truth; the hidden pair's permitted/required refusal can therefore occur before joined-cell execution. Report that mechanism honestly. The original Gate B scale premise is held for a separate design disposition; this review neither assumes an inert scalar nor demands an R1 expansion to satisfy it. Existing classifications/Models/caps remain unchanged.

No source, worktree, test, expectation, cap or generated file was edited by this review. This note is the sole create-only output.

