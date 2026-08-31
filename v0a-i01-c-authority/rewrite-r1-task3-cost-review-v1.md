# R1 Task3 cost and ownership engineering review

Reviewer: Codex / authority_cost_audit. Read-only source inspection; not a cold review or a runtime verdict.

## Frozen target

- H commit: a6510e250484e21e53ab85fac6027a4c309cda08.
- Task3 manifest SHA-256: 3599296998a7d85c5abf9a59ecfe917a9ca3997a7891abf45b13ac8d9fb68a96.
- Source: rewrite-r1-task3-source-v1.py, SHA-256 1ecbde73fcd2159aef2a96538850a93fc4ec2bfa590352bc33d95581d12ccc45.
- Task2 delta SHA-256: 0e2cb50bc70ad9467e0c232e3ce0f5d33df53400c592a5a4358a84019dcce76e.
- Cost contract: rewrite-r1-implementation-plan-v1.md (18f8124432880016d6dd0690ed4d3b582b8e202c5bdda21ae48a65efa0ae521d), with dictionary-copy and current-context clarifications in rewrite-r1-baseline-disposition-v1.md (0259ec8773dd28217fd6d2a53fc60dc468e910fb4d6871b128aaa3d6c563af6c).

The source, delta and manifest hashes were independently recomputed. I read the full Task3 delta, the new evaluator helpers, the retained COW/trace primitives they call, and the Task2 binding correction. Public entry is still unwired; Task4 call/construction implementations are outside this snapshot.

## Finding requiring a bounded source-order disposition

**T3-E1 — Important before admitting this environment shape; high confidence, static evidence.** At source10105-10117, _c_eval_dict accumulates explicit additions and merely ORs the inherited flag when a later inherited mapping is expanded. Thus the expression shape {'K': 'literal', **os.environ} retains the explicit K override even though the later inherited source may overwrite K. A second inherited expansion after an explicit override has the same problem. This is an exact projection mismatch in the new environment record, not a claim that a public acceptance failure has been executed.

Keep the R1 shape small: refusing inherited expansion after accumulated additions, or repeated inherited expansion, is a bounded option. A correct general ordered environment merge is not required by this review. The old pure _environment_delta also has weak shape handling; this finding grants no authority to change that retained policy. The terminal adapter must not turn the new stale override into an accepted detached fact.

The related timing concern is conditional: _c_eval_dict first evaluates all operands, then resolves every expansion record from the final successor. If Task4 never admits environment mutation, that restriction makes the immutable-record case safe; later mutation support would require expansion-time snapshots. Do not expand R1 merely to solve that future case.

## Accounting and ownership inspection

No additional concrete semantic allocation/reference undercharge or COW ownership violation was found in the inspected Task3 helpers.

- _c_follow9886-9891 charges 1+2n for the concatenated issue tuple (allocation, n visits and n retained references), plus the separately charged fixed trace link and outcome. _c_trace_link retains two predecessor edges; it does not walk or duplicate their event histories.
- In _c_eval_many9968-9991, a value prefix of length n is extended with container(n+1) plus n+3: the new tuple allocation/references, n+1 copy visits, and temporary singleton allocation/reference are covered once. The five-unit pair/list append charge covers pair allocation/two fields plus append/reference. _c_fact_tuple covers the next pending tuple's allocation/visits/references.
- _c_eval_dict10082-10138 pays for operand-list allocation and appends, each mapping-entry visit/update and retained key/value, the final ordered tuple/pairs at 1+5n, and its four-field environment record. List/tuple records, native bound methods, call argument slices and keyword tuple/pairs have corresponding explicit construction charges.
- _c_statement10331-10351 forks each unknown-condition alternative from the unchanged parent. The second branch does not inherit the first branch's mutation; canonical write helpers still detach outer tables and activation banks as required. No new evaluator helper selects a historical budget or creates a replacement budget.
- Result/reference correlation is carried as (outcome, values), then through each successor's own state. Abnormal outcomes bypass later evaluated operands/statements. Their bookkeeping can continue and is charged, but sensitive later evaluation is not requested by these loops.
- The Task2 correction9556-9581/9621-9636 visits binding-only syntax and charges reached nodes/iterated edges and name-map operations. Comprehension targets remain excluded; first-iterable reads and outer walrus bindings are separate. Match captures use the existing charged insertion helper. Changing scope/signature key annotations to AST objects adds no runtime conversion. I found no new budget owner, implicit nested-record equality, or bulk unmetered name reconstruction in this correction.

These are semantic operation units, not Python opcode/allocator-perfect accounting. I did not import the superseded storage prototype's temporary-iterator P/C requirements into this contract.

## Explicit limits and cost risks

1. _c_follow rebuilds through _c_out, which sets explicit=False and excluded_handlers to an empty set. Frozen Task3 has no producer of nondefault values for either field, and R1 excludes explicit handler/finally execution. This is a preservation obligation before such a producer is added, not a demonstrated current public defect.
2. _c_eval_many repeatedly copies the accumulated argument/container prefix. A straight-line k-operand path therefore performs quadratic copied-reference work, which is honestly charged. _c_follow similarly pays for any accumulated issue tuples. This merits measurement under the already-frozen Gate B, not a speculative new storage structure or a claimed performance failure.
3. _c_eval_many's container check bounds the operand-value tuple. It is not by itself proof that a later union of expanded environment additions respects the native container bound. The final environment admission/conversion boundary must retain the existing size rule.
4. Task4 must return isolated successor states when it returns multiple outcomes and preserve call-entry views through canonical snapshots. This source-only inspection cannot establish that future wiring or whole-analyzer cost.

No candidate/test/fixture/Model/controller payload ran. No source, expected result, cap, generated file or worktree changed. Specification evidence is partial pending the environment disposition and full wiring; cost fitness remains unproved until the fixed public gates run. No CLEAN or release-readiness claim is made.

