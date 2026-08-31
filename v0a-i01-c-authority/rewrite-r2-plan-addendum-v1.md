# R2 plan addendum v1: exception proof and generator entry boundaries

Status: prospective, normative clarification of `rewrite-r2-implementation-inventory-plan-v1.md`; not production/source GO or runtime evidence. The original plan and held source remain unchanged. This addendum resolves R2-P1 and the root's iterator/depth questions without adding fixtures or execution scope.

Pins: plan `d5491bc204b07ec0e1f861b7cfe03facab9b8c9907a38726f64d96c096fe0d4f`; held R1 source `c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f`; review `rewrite-r2-implementation-plan-cost-review-v1.md` SHA256 `4c3ce3b4e30ea60ee68449cfe0ba2656a4db4609fb1f65d02a9b960a84e0f259`, retained at H `90a1632ffce0ebff767a1103c3739b48c0546643`, manifest `e9ef227f1849ba8456f28a46de23f50b5bd56b76665b82a7c275394822eca940`. Root-adopted premise SHA256 `bdf3b13684d50318c48ddbe3af1682b6e298136e21af3d1ef76ffe7a3f52e6b4`; independent concrete successor cases/controller still precede baseline and source GO.

## R2-P1: no legacy tagged failure is promoted

The six existing `_c_fail(exception=...)` producer categories are inventoried below against exact held R1. **None is promoted to a catchable exception in R2.** Some narrower subcases could support a future proof, but that is not needed by this population. The original plan's instruction to route proved runtime-failure callers to known raises is narrowed accordingly.

| Existing producer | Held source lines | R2 disposition and proof deliberately not assumed |
| --- | --- | --- |
| Name read | 9903–9924 | Refused. Missing module entries may denote unmodeled real builtins; an old NameError tag is not absence proof. Even a separately provable unbound local/free-cell subcase remains refused in this increment. |
| Sequence access | 9961–9973 | Refused on failure. An exact current sequence plus proved integer outside its bounds could justify IndexError, but no implicit promotion is needed now. Unsupported receiver/index never supplies that proof. |
| Cell deletion | 10077–10086 | Refused on failure. Missing internal destinations are not Python absence; the narrower existing-unbound lexical-cell proof is deferred. |
| Namespace deletion | 10087–10092 | Refused on failure. No generalization from an internal missing key to class/module/member lookup or deletion semantics. |
| Noncallable selection | 10654–10657 | Refused. A proved exact noncallable literal could justify TypeError, but generic unknown, unsupported object and missing callable evidence cannot. The entire legacy failure category stays refused. |
| Binder rejection | 10669–10673 | Refused. Optional matcher None may mean unsupported binding shape, not a proved invalid Python call. No binder algorithm or signature-support expansion. |

Implement the boundary centrally: `_c_fail` produces uncatchable refused control and retained conservative issue/debt. A legacy diagnostic exception name may remain descriptive, but is never consumed by handler matching and must not become catchable outcome metadata. Existing member-lookup refusal (9930–9958), open-entry unknown facts, missing stores, unsupported syntax and work/depth errors receive no inferred exception proof.

Catchable source exceptions initially have only these producers:

1. A selected, canonically proved unshadowed ValueError, TypeError, KeyError or IndexError builtin constructor, called with no arguments, produces its canonical exception instance. Explicit Raise of that proved instance produces a known raised outcome. Current bindings/aliases, not source spelling, establish the constructor identity; unknown/global placeholders cannot substitute. Other constructor forms and unsupported raise forms refuse.
2. The **new** current canonical generator record in phase `running` proves rejection of another resume with ValueError. This proof is independent of every legacy tag. It applies before cursor-exhaustion inspection, including when the running body is evaluating its last available item. [Python generator methods](https://docs.python.org/3/reference/expressions.html#generator-iterator-methods)

Only these known raised outcomes enter the handler matcher. Required four-type tuple matching uses proved current builtin class identities; it does not require a general builtin registry or new arbitrary-class hierarchy. Unsupported/unproved handler lookup remains an uncatchable refusal. A future implicit exception producer requires its own enumerated semantic proof and scope review; this addendum grants none.

## Typed debt, historical observations and handler successors

`_c_raise_known` creates catchable tag/value/origin/explicit metadata with no unconditional `_CIssue` event. `_c_out`, `_c_follow`, `_c_call` completion summaries, `_c_invoke` and `_c_join` carry that metadata and the actual successor state. Existing unsupported issues and prefix traces are never discarded.

A small semantic `_c_handle_known_exception(ctx, raised, frame, handler)` boundary runs an already-matched handler from that exact post-raise state and returns its actual outcomes. Handler selection stays in `_c_try`; this helper must not repeat matching or reconstruct cells. Successful handling clears only the consumed exception's active metadata, preserving the four D2 work-pair states and unrelated debt. Any new abrupt handler outcome carries its own metadata.

Terminal review reports a known exception only if it escapes in the final outcome. A historical call observation saying that an inner call raised is not a second escaping exception and must not reintroduce a blocker after an outer handler consumes it. Refused outcomes bypass handlers entirely.

These seams permit original-delegating scalar observation of tag, explicit flag, origin path/line, selected handler and returned control without adding telemetry-only production calls. Raw current scalar work values can be observed without calling metered readers. Observers retain no AST, state, object record, context or budget.

## First iterator: exact bounded native range only

The admitted call is a canonically proved builtin `range(n)` with exactly one positional argument, no keywords/expansion, and **the argument itself** an exact builtin int with `0 <= n <= 4096` under the existing container bound. Bool, negative int, unknown values, multiple arguments and custom integer conversions remain unsupported. This is not an extent computed by `max(0,n)`.

Its canonical range record proves start=0, stop=n, step=1. The generator's private range cursor begins at zero. No Python iterator, range expansion or materialized tuple is stored; actual record/scalar operations are charged, and no nonexistent n-element allocation/copy is charged. Wider range contracts are not implied.

A generator expression initially has one synchronous Name-target clause, no filters, created in a function activation. Its first iterable must evaluate to this exact canonical range value. Another generator as the first iterable, an ordinary container, unknown iterable or implicit iterator protocol refuses at creation **without resuming that value**. The required generator70 nesting is sum(previous_generator) in the element over range(1), not a generator-as-first-input chain.

The first-iterable expression is evaluated once in the enclosing frame and the supported cursor acquired at creation. Creation does not increment deferred depth or evaluate the element. If creation occurs inside an already active body, it inherits that caller depth unchanged. No body sensitivity scan or helper execution is substituted for deferred evaluation. [Python generator expressions](https://docs.python.org/3/reference/expressions.html#generator-expressions)

## Resume/depth transitions

`_CContext.deferred_depth` counts currently active generator bodies in this operation chain. Generator records retain no depth/context/budget. Ordinary helpers preserve the caller's deferred depth while retaining their independent helper-depth accounting.

`_c_resume_generator(ctx, state, ref, site)` returns ordinary ordered `_COutcome` values with internal controls `yield`, `stop`, `raise` or `refused`. The builtin sum consumer consumes yield/stop internally; these controls do not escape as ordinary source call completions.

| Current record/proof | Transition and depth behavior |
| --- | --- |
| Missing, incompatible or unproved generator/range record | Refuse; never treat missing evidence as empty/exhausted. |
| running | Known ValueError, before testing remaining range entries; no second body entry or depth increment. |
| exhausted | Return stop, without a new body entry or fabricated depth charge. |
| created/suspended with exact cursor >= stop | Replace with exhausted if needed, then stop. Exact cursor/range evidence proves this branch; do not evaluate the target/element or enter depth merely to report exhaustion. |
| created/suspended with exact cursor < stop | Before cursor advancement, target binding or body evaluation, test incoming active depth. At 64, propagate exact InventoryError(`analysis deferred generator depth exceeds 64`). Otherwise enter with depth+1, mark running, pull this proved native range item, advance the cursor and bind/evaluate in the implicit frame. All real pull/bind/body work belongs to that active entry and the same original budget. |
| Element evaluation completes normally | Replace the current successor's record with suspended/current advanced cursor, return yield with that post-body state, and return to the caller context/depth. Each alternative successor performs its own replacement. |
| Element evaluation yields a known source exception | Replace that successor's generator with exhausted/closed-to-further-body-execution, propagate its known raised outcome, and return to caller depth. An outer matching handler receives this post-state. |
| Element evaluation refuses, or an analysis work/depth InventoryError aborts | Refusal/error propagates unchanged. Do not manufacture normal exhaustion or a catchable Python exception; no normal source continuation may resume that abandoned analysis outcome. |

The depth guard therefore follows a nonexecuting availability proof but precedes the next available item being consumed. Empty range(0) and previously exhausted records have explicit proof and do not enter a body; no claim is made for unsupported or merely unknown emptiness. Internal pulls create no synthetic source Call observations. Real range/sum calls retain their existing observations and snapshot costs.

The active-depth adapter can observe incoming context depth and raw exact phase/cursor fields; empty/exhausted resumes are not attempted body entries. Original InventoryError propagation remains untouched. Runtime source validation must confirm the eventual adapter uses actual admitted-entry conditions, not a source-count estimate.

The helper65 guard/message remains independent and unchanged. No early unsupported g0 body refusal may replace generator70's actual nested-consumption depth error.

## Boolean identity and execution schedule limits

`_CBooleanUnknown` proves builtin boolean type only. Analyzer structural equality, `_c_value_key` equality, or equality of two independently produced boolean-proof records does **not** prove their runtime identity. Only the admitted singleton or canonical object-identity proofs can yield an exact identity answer; other identity results stay proved-but-unknown bool. The enclosing evaluator supplies source-site context for observation.

The separate 1500 additions-plus-deletions R2 stop limit remains. No storage backend expansion, caps change, test change or broader exception/iterator precision is authorized.

Default runtime schedule is **one full twelve-case baseline and one full twelve-case integrated candidate**, with floor-to-development rules unchanged. Identity/normal-branch, exception/handler and generator-depth checkpoints between them are source/AST/accounting reviews only. A focused runtime subset requires its own frozen scope and root authorization; the plan's intermediate-checkpoint wording is not such authorization. Missing new mechanism seams on the R1 baseline are recorded as unavailable/not reached, not successful zero work or infrastructure failure.

This addendum was authored from static source/review inspection only. W remains held at exact c8fc; no payload, imports, source edits or implementation were performed.