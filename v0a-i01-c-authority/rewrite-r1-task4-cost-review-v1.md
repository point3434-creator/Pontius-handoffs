# R1 Task4 accounting and binder engineering review

Reviewer: Codex / authority_cost_audit. Read-only static inspection, not cold review or runtime acceptance.

## Frozen source and contract

- H commit c74092059ba4451d7f1983f2b737e2ea3fdbd40d.
- Task4 manifest SHA-256 23d7980e9dc34ac396bd4d7426e17ceb0d5c883291afd14eef88f80735645cb2.
- rewrite-r1-task4-source-v1.py SHA-256 3511f60a62fc9588f153ba3db6b05ac228a1ce235cb23a5316000ce7ba4e550c.
- Task3-to-Task4 delta SHA-256 b6fe1bcd5afdac2ade9b7914c529a9cc4c63b05d8d923bad88d26bc49ee395d1.
- Original binder source: rewrite-r1-base-generator.py SHA-256 29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692.
- Approved operation model: implementation plan18f8124432880016d6dd0690ed4d3b582b8e202c5bdda21ae48a65efa0ae521d and baseline clarifications0259ec8773dd28217fd6d2a53fc60dc468e910fb4d6871b128aaa3d6c563af6c.
- Coordinator's restricted binder-domain/next-correction disposition: rewrite-r1-task4-coordinator-disposition-v1.md SHA-256 c12b0455954e90e3ee4f9ecaba888079002c6374aa85615439a9e959228bea37.

I independently recomputed source/delta/manifest hashes and read the entire delta, the new call/construction helpers, the binder and its callers. The canonical public entry is not wired in this snapshot.

## Findings

**T4-C1 — Missing identity-key allocation charge; Important to the accounting contract, high confidence.** In _c_invoke10630-10631, consume(2) covers a supplied-entry visit and its selected dictionary lookup. The nondefault branch also materializes id(expression), which is not covered by those two units. The earlier actual-map construction10610-10613 pays for its ID-key integers, as do Task1 _c_value_key and _c_join. The default branch has no corresponding ID operation. Retain one additional unit only on the reached nondefault lookup. Root has requested this correction from the sole writer; no corrected source was inspected here.

**T4-C2 — Depth refusal behavior is not preserved; Important before the depth gate, high confidence.** _c_invoke10597-10598 returns a refused outcome with reason 'analysis helper recursion depth exceeds 64'. The original canonical depth boundary raises InventoryError('analysis helper depth exceeds 64'), and the frozen helper65 Gate B assertion requires that error. Keeping the numeric constant64 does not preserve the error behavior. Root has requested restoring the canonical exception in Task5; exact entry/helper-depth mapping still needs inspection after entry wiring. This review does not claim the guard's current greater-than comparison has already been proven against that mapping.

These are static source findings. Neither is an executed product failure, and neither is closed by the request to fix it.

## Independent binder normalization

An AST-only check on the pinned source:

1. Located the original and candidate _bind_helper_arguments definitions.
2. Removed only the optional analysis_budget keyword/default.
3. Removed14 exact no-else 'analysis_budget is not None' guards containing15 consume calls; rejected any other body shape.
4. Unwrapped exactly six _c_binding_read(analysis_budget, original_expression) calls, preserving their original expression AST.
5. Compared complete normalized function AST to the r010 function, without location attributes.

The ASTs are equal. The six reads are: the allowed-keyword comprehension's positional-only membership; keyword membership in allowed_keywords and supplied; positional supplied membership and positional_defaults.get; keyword-only supplied membership. Each target is the binder's own ordinary set/dict. _c_binding_read10395-10398 charges one completed read and returns that exact value. It does not rescan input, eagerly evaluate the other side of an original short circuit, select a new budget or alter matching.

The scalar conditional in the allowed-keyword allocation charge accounts for an already-bound positional-only receiver removed from positional. For valid parsed parameter names, k = remaining positional + keyword-only - original positional-only + removed positional-only receiver is the number of inserted allowed names. The starred tuple, set allocation, visits and installed references are charged separately from the six read wrappers.

Caller inventory in frozen Task4 is complete: _c_invoke10603 supplies ctx.budget and the exact bool expression receiver is not None; the two old _review_body callers26199/26325 omit analysis_budget. No other call supplies a non-None budget.

The initial any-Starred/any-expanded scans are charged by full lengths only after they both complete false. A standalone metered binder call rejected partway through those scans would not charge its visited prefix. Root explicitly approved the narrower current domain: _c_eval refuses reached Starred operands and expanded keywords before canonical invocation; vararg/kwarg signatures short-circuit before those scans; old private callers remain unmetered. Therefore this is a disclosed API precondition/future-caller obligation, not a requested R1 wrapper expansion or present reachable accounting defect. Final wiring must preserve this exact caller invariant, including synthetic unittest entry.

## Other cost and ownership observations

- _c_construct_function10401-10479 charges the parameter/default/decorator preparation lists, actual visits, capture/default tuple-pairs and five-field function record. It scans shared direct-site facts for unsupported deferred bodies, without executing those bodies or creating a new budget.
- _c_construct_class10482-10522 charges namespace/map/proxy/frame allocations and forwards current state through class-body execution. The class slot is installed only after a normal body result. There is no generic class heap or ambient-name projection introduced by this delta.
- _c_call10525-10557 takes canonical entry and post-outcome snapshots. Its summaries retain control/value/view/issues, not entire outcomes or their traces. This avoids a trace/observation ownership cycle. The four-field summary tuple plus list append is covered by8 per outcome; the final summary tuple, nine-field observation, trace event and returned outcome list have separate charges.
- _c_invoke10560-10653 reuses the caller's arena and ctx.budget in the entered context. No activation, view or copied map retains an older budget. Captures/defaults become ordinary copied maps with1+3n; activation and cell writes remain canonical operations. No nested dataclass equality was added.
- Native append charges container(n+1), copy visits and its replacement two-field sequence record, then writes through the selected receiver's current object record. It does not re-resolve the receiver name.
- Call snapshots revoke ownership and can make later writes copy growing object/cell tables. These copies remain fully charged by the retained helpers. Their cost is unproved; no speed improvement or Gate B reserve claim follows from source inspection.
- _c_call continues the Task3 explicit/excluded_handlers forwarding limitation by rebuilding through _c_out. Frozen Task4 still has no nondefault producer; later exception support must not lose those fields. R1 does not promise handlers/finally.

## Evidence boundary

Only stdlib source parsing/hashing and file reads ran; no candidate import, Model, fixture, test, probe or controller executed. No source, test, cap, generated file or worktree was changed. Task3 findings remain separately bound to their own frozen source. The writer's Task5 changes require their own exact delta inspection. The result is partial engineering evidence with two open corrections, not CLEAN or release readiness.

