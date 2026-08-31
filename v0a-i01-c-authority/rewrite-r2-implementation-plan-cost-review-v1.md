# R2 implementation plan engineering review v1

Author: codex/authority_cost_audit, 2026-08-31. Read-only participant review; not a cold verdict, source GO, or runtime result.

**Design verdict: SOUND for the bounded canonical-core extension, subject to the required exception-producer clarification below.** No replacement storage backend or wider interpreter is warranted by this plan. The1500-line fit and196608 per-epoch fitness remain unproved; the budget is a stop condition, not evidence that the implementation will fit.

## Binding and inspected inputs

- Frozen H commit903f76cc04ff1068963ba2ce69e02f05eb13d7ce; planning manifest d1a610cd7ffdfae792d402b1882dba7677b2baadc8c65397781da8d33da58a43.
- Plan rewrite-r2-implementation-inventory-plan-v1.md: d5491bc204b07ec0e1f861b7cfe03facab9b8c9907a38726f64d96c096fe0d4f.
- Root premise disposition: bdf3b13684d50318c48ddbe3af1682b6e298136e21af3d1ef76ffe7a3f52e6b4.
- Current core rewrite-r1-task5-source-v2.py: c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f.
- Identity proposal: fea749f9ad5b6f567016030bbe38a0e9e3f6641eb9af98f5c9ae1607bd28b475.

Rehashed the plan, disposition, manifest and current source. Inspected the plan in full and the current state/cell/object, call/snapshot, exception-producer, outcome/trace and terminal-review seams. No candidate/test/fixture/Model/controller execution or modification occurred. R1 GREEN and maximum6692 are root-reported prior evidence, not independently replayed here and not an R2 cost forecast.

## R2-P1: required exception-producer clarification

The move from terminal conservative refusal to catchable Python exceptions changes the consequence of an existing tag. An old _c_fail(exception=...) label is not itself a proof of the corresponding runtime exception.

The concrete hazard is _c_read_name9903-9924: missing module names currently become NameError, but only staticmethod and __import__ receive builtin fallback recognition. An unmodeled real builtin can therefore carry that R1 tag. Previously it remained an unconditional blocker; promoting it to a catchable exception can let a handler hide an unsupported lookup. Similarly, _c_invoke10670-10672 turns a matcher None into TypeError when vararg/kwarg are absent, although the optional matcher's unsupported-shape result is not automatically a proof that Python would raise TypeError.

Root agreed during review: unproved global/builtin lookup and uncertain binder rejection remain uncatchable refusal; only independently proved exceptions may be promoted. Freeze that rule in the plan addendum and account for the complete producer category before implementation:

| Current producer | Required proof/disposition |
| --- | --- |
| Name read9923-9924 | Proved unbound lexical cell can supply NameError/UnboundLocalError with the proper local/free distinction. Unproved global/builtin lookup remains refused. No general builtin table is required. |
| Sequence access9971-9972 | Exact current canonical sequence and exact integer outside its known bounds establish IndexError. An unsupported receiver/index remains refused. |
| Cell deletion10085-10086 | Proved existing lexical destination containing unbound establishes the corresponding runtime name error. Missing internal destination remains refused. |
| Namespace deletion10091-10092 | Require the exact owned namespace/deletion semantics before promoting absence. Do not generalize this proof to ordinary member lookup. |
| Noncallable selection10654-10656 | Only a proved noncallable exact literal supplies TypeError. Generic unknown, unsupported object or missing callable proof stays refused. |
| Binder rejection10670-10672 | Promote only a specifically established invalid Python binding. Otherwise preserve refusal; no general signature-support expansion is needed. |

Current member lookup9930-9958 uses unsupported/refused outcomes, with open entry absence remaining unknown. Do not manufacture AttributeError or another catchable error from its reason text. New explicit Raise and builtin-constructor paths require their own proved identities and current arguments. The known hierarchy must not turn an analysis-unsupported outcome into a recoverable source exception.

This is a must-fix prospective contract gap, not a new runtime RED. The existing plan's producer audit is the right location; the amendment narrows it without adding fixtures or source scope.

## API, debt and state ownership

The distinct immutable builtin-boolean proof is an appropriate boundary. Ordinary unknowns never inherit it. Identity operands are evaluated once; singleton/object identities can be exact, arbitrary equal literal values cannot. Three false-prefix decisions produce four independently owned wrappers without a predicate solver. No name-map reconstruction or flattened heap join is required.

The exception inventory covers the important propagation seams: _c_out, _c_follow, _c_call completion summaries, _c_invoke, join, try and terminal review. Current _c_follow9890 resets abrupt metadata via _c_out, so the proposed all-seam correction is necessary. A matching handler must clear only the handled exception metadata, retain post-write state and unrelated unsupported debt, and avoid leaving an unconditional exception _CIssue in the immutable trace. Unsupported/refused paths remain uncatchable. Intermediate calls may record a raised completion, but that historical fact alone must not re-emit an escaped-exception blocker after a later handler consumes it.

Implementation checks, not new scope: handler selection uses current successor values and first matching supported handler; a handler lookup failure supersedes the pending exception while preserving earlier effects. The four exceptional branches must remain paired with their own work values and handler outcomes. A distinct state wrapper is required even when its shared tables initially match another branch.

## Generator boundary

The proposed record/frame/cell design is coherent and remains within the existing object store. It avoids an embedded resolver, native Python iterator, current-value environment or historical budget. Shared immutable scope facts are compiled once; actual capture destinations are read through the current state at resumption. The eager first iterable stays in the enclosing frame and the target/body in the implicit frame; updating all lexical-kind predicates together is essential.

Make the phase transitions explicit in the eventual source ledger: created/suspended, running, exhausted, and the disposition after a proved body exception. Each transition replaces the current immutable record in its own successor; never mutate a shared cursor or frame payload. A running alias cannot enter again. A yielded outcome carries the updated cursor and post-body cells; exhaustion differs from unsupported execution. The active deferred depth belongs only to the operation context, survives ordinary helper entry, and returns with its caller context after resume. It is neither helper depth nor a construction-time property retained in the generator.

Creation must not evaluate the element or run a sensitivity prepass. Internal cursor steps create no synthetic source calls; actual range/sum calls retain their existing observations. Original generator70 must reach the active-depth64 refusal before the deepest element executes; helper65 retains its independent exact helper error. Both original full public depth envelopes remain binding. Empty/exhausted generators do not enter a body merely to manufacture depth.

## Honest cost and observation readiness

The physical cost qualifications are adequate and are essential to the verdict. Fork8 and join3+9S are primitive bounds only. D2 detaches whole written banks, including ambient locals, and possibly the outer activation table. _c_call snapshots10593/10607 revoke ownership; a tiny generator cursor/status update may copy the entire object table. Trace prefixes are visited per outcome, operand/issue prefixes are copied, and four common continuations retain their actual terminal work. No fit prediction follows from R1's small six-case maximum.

The proposed scalar measurement is feasible without changing production semantics, but its exact adapter is still a required pre-dispatch artifact:
- Baseline R1 lacks new decision/resume seams. Record those mechanisms as unavailable/not reached, not as successful zero work; retain all original budget failures and semantic results. Absence is not infrastructure failure.
- Original-delegating wrappers may observe actual helper inputs/results and raw exact record fields after the real operation, then retain only scalar labels/counts. They must not call _c_cell_read, _c_object_read, truth evaluation, matching or resumption again.
- Decision/site context and completed joins must distinguish actual four leaf outcomes from unrelated helper joins. D2 evidence needs current write/raise/handler pairing; source syntax and final equal argv do not establish it.
- Record attempted budget requests separately from completed operations, including failure unwinding. Retain per-owner epochs, copied table/bank sizes, snapshots/forks, outcome and trace visits. Do not retain live states/budgets or mistake reused raw object IDs for durable branch identities.

The exact observer/controller, successor cases/Models and original-envelope correspondence must be reviewed and frozen before baseline, as the root disposition already requires. Every epoch remains subject to the unchanged production262144 cap and prospective196608 continuation ceiling. The1500 additions-plus-deletions bound is plausible enough for one attempt, but exception propagation and generator scope integration compete for that space; stop at the bound instead of compressing code, omitting semantics/accounting, or adding a backend.

## Disposition

Proceed only through the stated staged source checkpoints after R2-P1 is retained, the independent successor population and observer/controller are frozen, and root has the bounded baseline. No other must-fix architectural gap was found in this plan. Generator transition details and observer identity/custody are explicit implementation/review obligations, not permission to expand the increment. Runtime fitness, whole-family acceptance, general exceptions/comprehensions and integration remain unproved.

