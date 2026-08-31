# R1 Task 3 semantic engineering review v1

Reviewer: codex/r010_cold_a. Source engineering review only; no candidate/fixture/Model execution and no implementation CLEAN or cold-review verdict.

Disposition: Task2's identified binding categories are corrected structurally. Task3 has the following open semantic/control findings, to resolve before treating the evaluator as sound. These are source proofs in an intermediate, not yet fully connected implementation; no public runtime false-negative is claimed.

## Frozen evidence

H a6510e250484e21e53ab85fac6027a4c309cda08. Manifest3599296998a7d85c5abf9a59ecfe917a9ca3997a7891abf45b13ac8d9fb68a96; source1ecbde73fcd2159aef2a96538850a93fc4ec2bfa590352bc33d95581d12ccc45; Task2 delta0e2cb50bc70ad9467e0c232e3ce0f5d33df53400c592a5a4358a84019dcce76e; prior source83418c6b172ca0699ca01caed5f78d401e4ec21317806bbf83dba6b466b6be01.

I independently verified all26 manifest entry hashes against the frozen Git commit, the manifest itself, scoped local immutable inputs and prior source. The raw delta regenerates exactly. AST comparison confirms17 new helpers and only the declared prior changes to _CProgram, _c_scope and _c_fact_tuple. This does not adopt the author's static self-report as a semantic verdict.

Controlling read-only context: rewrite-design-v1.md701552c177840e4c5c0dd9c5985776256af5b31e7e997067dd662638a67c3ca8, frozen GateA population3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce, and original test bytesc46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf.

## Open findings

1. Deletion and uncertain-name reads do not preserve failure categories (high confidence; _c_read_name9899–9917, _c_store_name9994–10008, _c_delete10066–10069).

   Delete is merely _c_store(...,None). An already-unbound function cell is rewritten to another unbound atom and returns normal. Missing module/class-local names are popped with a default and also return normal. Consequently later statements can execute after a deletion that must fail, or at least explicitly refuse if its exact failure is unsupported. Attribute writes to a class owner already refuse; that does not protect the ordinary class-local Name path.

   _c_read_name also treats an unresolved capture route as proved NameError, and gives the same tag to a current-function unbound local. Distinguish unresolved/missing authority (refusal), a proved current local unbound (UnboundLocalError), and applicable definite missing/free-cell errors. Do not invent an exact Python failure from absent analysis proof. Python specifies failure on deleting an unbound name and distinguishes unbound function locals from generic missing names: [del statement](https://docs.python.org/3.11/reference/simple_stmts.html#the-del-statement), [name resolution](https://docs.python.org/3.11/reference/executionmodel.html#resolution-of-names).

   Required direction: validate the resolved destination/current presence before deleting, preserve successful earlier deletions/effects, and stop the successor on definite failure or refusal. No general heap/deletion precision is requested.

2. Truth conversion silently bypasses possible user code (high confidence; _c_truth10072–10079, If and Not consumers in _c_statement/_c_eval).

   Every nonliteral canonical reference or symbol returns None from _c_truth. If interprets that as a harmless unknown boolean and forks; Not creates another unknown value. Neither operation examines current object kind or emits a refusal for possible __bool__/__len__ execution. The approved open unittest attribute such as self.choice is a specific unknown-boolean case; it cannot justify treating all canonical instance/reference truth tests as effect-free. Python truth testing can call these protocols: [object.__bool__](https://docs.python.org/3.11/reference/datamodel.html#object.__bool__).

   Required direction: distinguish proven safe truth values and the admitted unknown boolean from protocol-bearing/unproved values. Explicit refusal at reached truth conversion is sufficient when R1 does not support the protocol; do not silently omit its effects or add broad protocol precision. Existing original tests already retain __bool__/__len__ categories (for example15863,15977,16501), but no such fixture was run here.

3. Import sequencing can resume after a refused alias (high confidence; _c_statement10294 onward, Import/ImportFrom loop; _c_follow9886).

   Unlike other statement/operand loops, the import alias loop calls _c_store_name for every prior outcome without requiring prior.control == normal. A declared-global store may refuse, followed by a later alias's successful local store. _c_follow then takes the later normal control, allowing subsequent body statements to run. Prior issue records survive, so this source finding is not a demonstrated blocker-free public result; it is still incorrect refused-successor continuation and can misattribute later effects.

   Required direction: non-normal import outcomes must remain terminal for later aliases/statements, retaining their state/issues/trace unchanged, just as _c_statements and assignment/delete sequencing already do.

4. Batched dictionary/call operands cross expansion failure boundaries (high confidence; _c_eval_dict10082–10138, Call branch in _c_eval10141–10273).

   Dictionary construction evaluates all key/value expressions via _c_eval_many before processing any mapping expansion or entry restriction. Call construction similarly evaluates all keyword values before checking keyword.arg is None and refusing expanded keywords. An earlier known-invalid/unsupported expansion therefore permits later helper expressions to run. If a later helper refuses first, the earlier expansion is never even classified and the recorded cause/effects can belong to an expression that should not have run. Dictionary expansion inserts each supplied mapping into the display at its own position: [dictionary displays](https://docs.python.org/3.11/reference/expressions.html#dictionary-displays).

   Required direction: respect each construction/expansion boundary in order. Preserve the evaluated prefix and stop/refuse before later operands once R1 cannot admit that expansion. Exact mapping/expanded-keyword execution need not be added. This is not a request to change harmless-oracle expectations or general Python support.

## Corrected binding category

The new binding-only visitor collects NamedExpr target stores inside comprehension iterables/filters/results without treating normal comprehension iteration targets or body reads/calls as outer/eager. Nested ast.comprehension targets are skipped, lambda bodies remain isolated while their defaults are visited, and MatchAs/MatchStar names plus MatchMapping.rest now enter the containing scope's locals. Existing global/nonlocal subtraction remains in force. These address the source omissions from Task2 without requiring execution of dormant Match/comprehension syntax. The AST-key annotation mismatch is corrected and tuple input annotations now admit mappings.

Unsupported lambda/comprehension execution still falls through to an explicit reached-expression refusal. Function annotation/type-parameter construction is a later constructor obligation, not proven by this Task3 stage.

## Supported mechanisms and limits

- Callee selection precedes ordinary operands and selected.result is retained across operand effects. _c_eval_many evaluates operands in order and preserves non-normal outcomes; _c_statements, return and ordinary assignment stop subsequent execution correctly.
- Subscript reads fetch the current object record after evaluating the index, while retaining the already selected receiver reference. Tuple/list assignment captures the source element references before target stores; chained assignment evaluates its RHS once.
- Unknown admitted boolean If branches use separate _c_fork states. _c_join retains ordered outcome alternatives without collapsing their result/state association. This supports the intended GateA temporal model but is not runtime proof of the unwritten invocation/constructor path.
- Namespace updates replace the current record; explicit attribute mutation of a class owner emits a refusal. Class-body local Name stores remain distinct and may complete normally, as required by the fixed class-adoption controls.
- _c_out/_c_follow currently create implicit exceptions with empty handler-exclusion metadata. Task3 admits no Raise/Try handlers; preservation of explicit/excluded tags must be established before those forms are added, rather than claimed now.
- No extra syntax, test population or broad accounting judgment is part of this review. GateA's fixed6/8 can miss these categories; passing it would not close them by itself. _c_call and construction bodies are not yet supplied in this frozen stage, so their behavior is not assumed.

Root and writer received the findings before report issuance. All four remain source findings, not freshly executed RED cases. No new witness, candidate/source/test edit, private payload probe, test or Model execution occurred. Only this create-only review was written.
