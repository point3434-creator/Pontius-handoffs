# R2 checkpoint 2 exception transport checklist

Engineering preparation only; no checkpoint 2 candidate has been inspected. These are review obligations for the approved narrow addition, not defects asserted against checkpoint 1. No candidate, test, Model, or harness was imported or executed.

Bound source pair: handoff commit c119b3f2c452982cc595b156c276d5d904bbc94b; manifest rewrite-r2-checkpoint1-v1-manifest.sha256 SHA-256 a6399d62ee23b42673766e857af047feb3abdfcab914053813eccec4cb9b9b90; source rewrite-r2-checkpoint1-source-v1.py SHA-256 41b4de563da886a7c674d49b25acd4332ba208906b403ec244d1a4aea856ee05. Source anchors below refer to those frozen bytes.

Controlling design: rewrite-r2-implementation-inventory-plan-v1.md SHA-256 d5491bc204b07ec0e1f861b7cfe03facab9b8c9907a38726f64d96c096fe0d4f and rewrite-r2-plan-addendum-v1.md SHA-256 1a1a6bc7f8ef4c56a72735670ff0bb65e883f3aa559abec7b4fec01af6991998. Scope is four empty builtin constructors (ValueError, TypeError, KeyError, IndexError), proved explicit Raise, and admitted Try/handlers. No general exception heap/hierarchy, finally, TryStar, cause, bare re-raise, or except-name binding is implied.

## Review checklist

1. **Prove builtin identity before construction or matching.** A symbolic spelling such as _CAtom(kind="symbol", data="ValueError") is insufficient: imports and qualified symbolic names can have the same spelling. Establish a distinct canonical proof through the current unshadowed builtin fallback; ordinary bindings take precedence, aliases retain the proof, and generic imports remain unproved. Only the approved empty call constructs a normal immutable exception instance. Preserve evaluation order and prior debt for rejected argument forms. Construction is not raising. A proved explicit Raise activates value, tag, explicitness, and source origin. Do not broaden class-form Raise or matching through name strings.

2. **Audit the entire outcome reconstruction category.** _COutcome currently carries state/result/control/exception_tag/explicit/excluded_handlers/issues/trace. Its sole direct constructor is _c_out:9886, which currently initializes False and an empty frozenset. _c_follow:9900-9905 and _c_call:10665-10666 reconstruct outcomes using only the old subset. Every new active field must survive these wrappers and any successor constructor; changing only the dataclass and _c_raise_known would lose transport. A handler consumes metadata on its branch-owned outcome, never by mutating a shared object. A newly raised handler result owns its new metadata. Normal/return outcomes must not accidentally retain active raised metadata, while an active raise must not be normalized into a successful result.

3. **Preserve existing abrupt-control gates.** _c_store:10058-10059, _c_eval_dict:10216-10223, Return at10475-10477, and _c_invoke:10763-10765 reconstruct only their admitted normal/return results; abrupt paths pass through. _c_eval_many:9992-9997 and _c_statements:10364 onward stop normal chaining on abrupt control. Keep this discipline when adding handlers. The final completed pipeline at11247-11258 still uses _c_follow before joining/terminal projection; it is another metadata transport boundary, not permission to reinterpret a raised result.

4. **Keep historical call summaries separate from active exceptions.** _CCallObservation.completed:9258-9268 currently declares four-field entries (control, result, view, issues); _c_call:10648-10657 constructs them. If extended, update the annotation, producer, and all readers together and charge the actual widened tuple/reference work. The old fixed-width charge cannot cover added fields without reconciliation. The same immutable call observation is linked into multiple result branches: never mark its completion “handled” for one branch. Current canonical code has no .completed reader; terminal handling uses entry/selected/caller-frame information. A new consumer must not turn a historical raised completion into unconditional escape debt or treat every sibling completion as active on one path.

5. **Handle from the exact raised successor state.** _c_handle_known_exception(ctx, raised, frame, handler) must start from raised.state, including the writes that preceded that raise. Matching uses current canonical bindings after the raise, rather than try-entry values or source spelling. Preserve pairing between state, tag, and origin for each alternative; do not join states before matching. Enter only the first admitted matching handler. Handling clears consumed active metadata while preserving prefix effects, unrelated issues, trace, and stored exception aliases. A new raise/refusal during handler processing replaces control appropriately. Refused analysis outcomes bypass handlers. Keep the supported else behavior and existing COW/arena ownership; no exception record retains a live context or budget.

6. **Do not promote any legacy diagnostic tag.** The addendum deliberately keeps all six old producer sites uncatchable (table below), even where an individual subcase might later be provable. _c_fail:9896 currently selects raise when passed a tag; the new central behavior must retain refusal/debt for those sites. A tag alone is not evidence of a Python runtime exception: missing names may be unmodeled builtins, and binder rejection may mean unsupported analysis shape. Original InventoryError work/depth failures remain analysis failures with unchanged caps and propagation.

7. **Separate terminal escape from history and unconditional debt.** _c_review_outcomes:10859 onward scans each final outcome's trace. _CIssue at10887-10891 becomes a blocker unconditionally. Consequently a catchable known raise must not also produce an unconditional _CIssue that survives successful handling. _CCallObservation at10892-10918 contributes call census/helper edges from its historical entry, not a new active raise. Only a final escaping active known exception should yield its escaping blocker. Preserve unrelated prior issues, calls, sinks, and per-alternative trace traversal. Do not replace the per-outcome visited set with a global set that erases feasible alternatives.

8. **Meter the added work under the existing owner.** Charge actual new exception/outcome fields, origin and completion tuples, retained references, handler visits/matching operations, and new copies under the current ctx.budget. Keep existing call snapshots and COW invalidation: storing an exception can force a real table copy. No new epoch, refund, disabled-mode discount, cap change, or predicted headroom. This is a source checkpoint; later full-population runtime remains a separate release decision.

## Complete legacy tagged producer census

AST-only enumeration of calls to _c_fail having an exception keyword found exactly six sites:

| Frozen source anchor | Diagnostic tag expression | Checkpoint 2 disposition |
| --- | --- | --- |
| _c_read_name:9933 | UnboundLocalError if local, otherwise NameError | Uncatchable refusal |
| _c_read_element:9981 | IndexError | Uncatchable refusal |
| _c_delete:10095 | UnboundLocalError if local, otherwise NameError | Uncatchable refusal |
| _c_delete:10101 | NameError | Uncatchable refusal |
| _c_invoke:10702 | TypeError only for literal selected atom; otherwise None | Uncatchable refusal |
| _c_invoke:10718 | TypeError only when signature has no vararg/kwarg; otherwise None | Uncatchable refusal |

The same AST census found one direct _COutcome constructor (_c_out:9886), one direct _CCallObservation constructor (_c_call:10657), and explicit control/tag _c_out reconstruction in _c_fail:9896, _c_follow:9904, Return:10475, and _c_call:10665. Source reading additionally covered normal-only wrappers and terminal projection. This census is a review aid, not a claim of a complete transitive semantic proof.

Verdict: the narrow design is reviewable without expanding exception semantics. The main closure obligations are canonical builtin provenance, complete metadata transport, exact post-write handler state, and separation of active escape from historical/unconditional debt. Runtime correctness, original-population compatibility, and cost fitness remain unverified.\n