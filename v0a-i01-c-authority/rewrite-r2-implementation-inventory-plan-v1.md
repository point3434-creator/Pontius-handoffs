# R2 canonical-core implementation inventory and plan v1

Status: prospective engineering plan, not source authorization, implementation, cold review, or runtime evidence. The identity-premise successor inputs and their controller are not yet frozen. No production, candidate, tests, case packs, or controllers were changed or executed while preparing this note.

## Basis and retained scope

- Held R1 source: `rewrite-r1-task5-source-v2.py`, SHA256 `c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f`; NEW W must remain identical until separate GO.
- Prospective premise: `rewrite-r2-identity-partition-premise-proposal-v1.md`, SHA256 `fea749f9ad5b6f567016030bbe38a0e9e3f6641eb9af98f5c9ae1607bd28b475`.
- Original population: `rewrite-early-population-v1.json`, SHA256 `3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce`. Original R2 controller plan: `tests-checks/rewrite-r2-plan-v1.md`, SHA256 `ea2ca1217f133a708c763568cc7494a2ac600b4db351e00a696600836d53f5f7`. Both remain unchanged; their old four scale sources cannot be relabeled as the prospective identity experiment.
- Root reports Gate A GREEN on both interpreters, retained at H `a65a6c04ad7b87d19a4a91796ebb1607a88dda23`, manifest `ddc96dfb0aba036b480bf887217ab4f18871b2221248065923b88c923a43e008`, results SHA256 `40d28c2c1e6f8bdd458266a85bdb3a41525b969b15364c5add19da35637c6ede`. Six analyses/eight harmless Model projections passed per slot; four original budget epochs per analysis, maximum 6692. The hidden-cell pair refused unknown truth and does not prove joined-cell execution. I did not run or independently replay those receipts here.

Keep the six Gate A expectations and two original exact-depth cases. Prospectively replace only the four scale premises, preserving N=8/64, D=0/2, S=4, original branch bodies, ambient/work initialization and sink. Map old Model regions 0/1/2/3 to True/False/None/a fresh plain object. Latch the open selector once, inside the exceptional try after ambient/work initialization. Use `is True`, `is False`, `is None`, else. The latch is real fixed overhead, never subtracted from accounting. Required-clean labels need the newly frozen source premise; no generic inert-unknown or public input-domain API is introduced.

## Checkpoint 1: proved boolean decisions and four normal successors

Add one immutable `_CBooleanUnknown` alternative to `_CValue`. It means an unknown result whose builtin boolean type and inert truth test are proved by its producer. It is not a reason-tagged generic unknown.

`_c_identity_compare(ctx, left, right, op)` receives already evaluated operands and returns an exact literal bool where identity is proved, otherwise this new boolean value. Initially, exact answers cover canonical object identity and the None/True/False singletons; do not infer arbitrary literal identity from equal values or interning. Supported identity operations and logical negation of their result are the only new producers. Python identity comparisons do not invoke rich comparison or the selector's truth protocol. [Python identity comparisons](https://docs.python.org/3/reference/expressions.html#identity-comparisons)

Extend `_c_truth`, `_c_value_key`/choice handling, Unary Not, and the existing If dispatch. Exact truth stays exact; this proof type permits an ordered true/false split; generic unknown, open object truth and unsupported protocols still refuse. Do not infer the new fact from symbol names, strings, ordinary equality, or a subprocess result.

Each independently executed successor owns a distinct `_CState` wrapper. Existing `_c_fork` shares immutable table contents and `_c_join` retains ordered state/result/control/issue/trace alternatives; do not flatten values into a heap join. The ladder's false continuation reaches the next comparison, yielding four leaves from three decision sites. No predicate solver, selector-cell rewrite, or fabricated fourth decision is needed. This suffices for this partition; it does not establish general repeated-predicate correlation.

Expose small original-delegating decision/join seams for root-owned scalar observation. Required evidence is three reached identity decisions and four actual leaf outcomes feeding the common continuation in one public analysis. Four constant-specialized analyses, source counts, equal final argv, or the retained Gate A hidden pair are insufficient. Equal capability rows may still aggregate at the unchanged public row boundary; their alternative execution traces must remain distinct.

## Checkpoint 2: known exceptions preserve post-write states

Add `_CException` as an immutable canonical object record: a proved builtin type tag and retained argument references. Unshadowed builtin lookup can supply the four exception constructor identities and the small known builtin hierarchy required for matching; existing canonical local/module bindings always win. No custom exception-class model or matching by an unproved source spelling.

Use `_c_raise_known(ctx, state, site, exception, explicit=...)` to create a catchable raised outcome with an origin, without an unsupported issue or unconditional blocker trace. Empty calls of ValueError, TypeError, KeyError and IndexError are the required constructor path. Keep a compact exception origin on the outcome so an escaping exception can produce the existing public blocker at terminal review.

The propagation inventory is mandatory:

| Seam | Required change |
| --- | --- |
| `_c_fail` (9876 area) | Keep unsupported issues as control=refused, never catchable. Its proved runtime-exception callers route to the known-raise constructor instead of creating an unconditional exception issue. Inventory name/delete/index/call failures, not only explicit Raise. |
| `_c_out` / `_c_follow` (9862–9895) | Carry exception tag/value/origin, explicit flag and exclusions; do not silently reset them. Concatenate existing unsupported debt and link existing traces unchanged. |
| `_c_statement`, new `_c_try` | Explicit Raise selects a current proved exception. A handler consumes only the matching raised outcome and starts from that exact post-write state. Unsupported/refused outcomes bypass handlers. Normal completion clears the consumed exception metadata, not unrelated issues. |
| `_c_call` / `_c_invoke` (10579 onward) | Preserve abrupt metadata through caller return and immutable completion summaries; retain call-entry/post-state observations and selected callable/arguments. No normal-return conversion for a raise. |
| `_c_join` / `_c_review_outcomes` | Preserve each exception/state pairing. Emit an escaping-known-exception blocker once at the terminal boundary. A handled exception leaves no unconditional `_CIssue` in its prefix trace. |

Use current canonical handler-type values after the body raises. First matching supported handler wins; an unsupported handler expression/type explicitly refuses, while an evaluated known handler-lookup failure supersedes the original exception. Python matching permits a type or tuple of types, including compatible bases. [Python try statement](https://docs.python.org/3/reference/compound_stmts.html#the-try-statement)

Admit bounded try/except with the tuple of four proved builtin classes; ordinary else can reuse the statement pipeline for body-normal paths. Finally, TryStar, handler-name binding, explicit causes, bare reraising and custom exception classes remain reached unsupported syntax in this increment. Do not claim recovery of correlations not present in the ordered outcomes.

Add Unary USub only for exact admitted numeric literals, with one operand evaluation and no user numeric protocol. Preserve D2's four pairs: (1,-1)/ValueError, (2,-2)/TypeError, (3,-3)/KeyError, (4,-4)/IndexError. Scalar observations must show each write pair, typed raise and matched-handler successor before the common launch.

## Checkpoint 3: canonical deferred generator depth

Add a bounded native range record and a generator object record in the existing canonical object table. `_CGenerator` retains its compiled implicit scope/template, lexical frame/cell destinations, first-iterator state, cursor and phase. It never retains a context, budget, Python iterator, ambient value projection, or old-state authority mirror. Current store records govern aliases and resumption.

Extend the existing `_c_scope` compiler once: the eager first iterable belongs to the enclosing scope; target bindings and deferred body sites belong to an implicit lexical scope. Reuse capture routing and the same stable metadata owner. Update the lexical-scope predicates at activation allocation, capture lookup and name routing together. Preserve the existing containing-scope walrus binding-only classification. The initial execution admission is one synchronous generator clause with a Name target and no filters, created in a function activation; unsupported shapes/placements refuse without claiming new class/comprehension precision.

Creation evaluates the first iterable once and acquires its supported iterator, then allocates the generator activation/record without evaluating the element or scanning its body for sensitivity. The language evaluates the first iterable immediately and defers the remaining generator work. [Python generator expressions](https://docs.python.org/3/reference/expressions.html#generator-expressions)

Proposed operation boundaries:

- `_c_make_generator(ctx, state, frame, node, first_iterator)`: construct the canonical deferred object and capture only required destinations. An unsupported eager iterator protocol refuses at creation. Unsupported element operations refuse only when reached.
- `_c_resume_generator(ctx, state, generator_ref, site)`: read the current record; return ordered yielded/stopped/raised/refused outcomes with their states. Bind the target through existing cell writes, evaluate the element through `_c_eval`, and replace cursor/status through existing object writes. Exhaustion is not inferred from an unsupported result. Running-alias reentry is a known exception.
- `_c_sum_generator(...)`: support the proved builtin consumer, admitted arity and an immediate generator iterator; accumulate only proved numeric yielded values. Do not flatten element-contained generators or add synthetic source calls for cursor steps. Unsupported consumers/results refuse at the reached boundary.

Builtin range/sum identity is obtained only through canonical unshadowed lookup. The required range path is one exact bounded integer argument, including empty range; no new general iteration/container interpreter. Original source range and sum calls retain their real call observations.

Add an active deferred-depth field to the operation context, propagated through ordinary helper entry without changing helper depth. Before entering a nonempty generator body, depth already 64 raises exactly `InventoryError("analysis deferred generator depth exceeds 64")`; exhausted/empty iterators do not enter that body. Nested resumes share the same original body budget and allocator. No fresh epoch, helper-depth substitution, body prepass or early sensitivity refusal may stop the depth70 chain.

Preserve the existing helper guard and exact `InventoryError("analysis helper depth exceeds 64")`. The original helper65 and generator70 envelopes retain their full original fixture/probe setup and include_probe behavior. In generator70, the chain must actually descend before the deepest cp.arange body would execute; replacing the expected depth error with an unsupported blocker or work-cap error fails the contract.

## Owners, accounting and bounded size

Stable scope/templates are built once under the existing certificate budget. Module construction, entry preflight and body work retain their existing owners. All operation helpers receive the current context; no table, generator or view selects a budget from construction. Original `_AnalysisBudget.__init__`/`consume`, all five caps, binder matching semantics, public schema, native writer and terminal policy remain unchanged.

Charge every new value/record/outcome/cursor/summary allocation and installed reference, each lookup/visit, tuple copy, handler comparison and real resume step. Guard before unreached work. Extend the existing ledger explicitly rather than using a flat discount or new hidden budget. No special scalar charge is invented when a depth guard makes no original work request.

Physical costs remain material:

- `_c_fork` (9331) is 8 units with no value traversal; `_c_join` (9511) is 3+9S for S distinct supplied outcomes, excluding their construction. These are primitive bounds, not whole-analysis claims.
- The first post-fork cell write may copy the outer activation table (1+3B) and the whole selected bank (1+3L), including N ambient locals. D2 is not O(D) copying.
- `_c_call` entry/outcome snapshots (10593/10607) revoke write ownership. Range header calls and nested sum calls may repeatedly force whole object-table/bank copies before generator installation, binding or cursor updates.
- Linear source-site search, per-outcome shared-prefix trace traversal, issue tuple copies and operand-prefix copies remain charged. Four alternative continuations legitimately multiply terminal work. Never deduplicate evidence across alternatives with a global visited set.

No cost headroom is predicted. Retain actual copied table/bank sizes, snapshot/fork/outcome counts and trace visits through root-approved scalar observations; do not add metered reads or retain live state in observers. Every original budget epoch must remain at or below the proposed experiment's 196608 continuation limit, with production cap 262144 unchanged.

Proposed separate R2 authoring ceiling: 1500 additions plus deletions from held R1, subject to root approval. Target roughly 200 for identity/branch changes, 400 for exception/control propagation, 700 for generator scope/resume integration and 200 for shared plumbing. These are planning allowances, not earned quotas. Retained R1's 2198 changed lines are a separate completed increment. Stop before exceeding the R2 ceiling or adding a backend, generic heap join, protocol interpreter or old-engine fallback.

## Review and RED/GREEN sequence

1. Root/independent engineering review this plan; freeze the four premise-corrected sources, separately reasoned Models, exact region mapping, successor population and mechanism observer/controller. Original cases and prior evidence remain immutable.
2. Root runs the bounded baseline against held R1 with the new frozen inputs. Retain actual semantic/coverage failures. A failed floor is retained evidence, not permission to bypass floor-to-dev rules.
3. After separate source GO, issue immutable checkpoints in order: known boolean/normal branches; known exceptions/handlers; deferred depth; integrated whole Gate B. Each includes exact delta, touched-helper inventory and new-work ledger. No hidden backend or fixture-keyed dispatch.
4. Root inspects before each authorized focused dispatch, then runs the full twelve-case population with unchanged Gate A controls and original depth envelopes. Floor must satisfy all semantic, mechanism, accounting and custody checks before development-slot replay.
5. Stop on missing four-state/handler evidence, pre-consumption generator refusal, lost alias/state isolation, depth/error mismatch, reserve failure, missing accounting or a fixed required-clean conflict. Report the concrete mechanism; do not weaken expectations, add input assumptions, change caps or silently broaden precision.

This plan does not establish runtime fitness, general exception/comprehension support, cross-module closure behavior, or wider path correlation. Its purpose is a small public-analyzer extension with observable branch and deferred execution, using the one canonical state already installed for R1.