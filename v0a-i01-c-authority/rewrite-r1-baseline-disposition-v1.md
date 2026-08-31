# R1 baseline and source GO v1

Prepared against H commit f6d9d79e5b9820bffa946193983e193d896575d4,
preparation manifest ee8e0c23a53ed9aee251d9551b8319d248523585b7010ca628543df2d765d4d3.
The root accepted the independent harness reviewer's communicated no-blocker
verdict after the observer subhash provenance question was resolved. Its final
retained report is a companion record, not implementation CLEAN.

One baseline invocation r1-base01 ran on actual CPython3.11.15 using the issued
control9310da3c/probec0672ac6 and exact r010 generator29c49c61. No sensitive source
fixture executed; all eight separate harmless Models matched. The run completed
six public analyses with unchanged original caps, four budget epochs per case,
and no analyzer, observer or infrastructure error. Snapshot and original inputs
remained byte-exact. The independent root verification rehashed all1770 snapshot
files and all retained inputs/outputs before source GO.

- Receipt: tests-checks/rewrite-r1-gate-a-r1-base01-311-receipt.json,
  a9bddbae63bf96bfa85a853ada42e0dde8a9f4a27c785a8f4c08c38ce33c8529.
- Root verification: coordinator-rewrite-r1-r1-base01-311-verification-v1.json,
  954ee9a908033e0c43d8c7588837e3588398174f3a9e67c034469fa11fe6bc80.

| Case | Baseline outcome | Maximum epoch work |
| --- | --- | ---: |
| shared-list-consumed | Expected refusal | 578 |
| shared-list-dormant | Expected clean [-m,fixed] | 684 |
| class-adoption-unsafe | RED: wrongly clean [-m,outer] | 762 |
| class-adoption-safe | RED: wrongly refused | 520 |
| hidden-cell-joined-reached | Expected refusal | 1011 |
| hidden-cell-joined-dormant | Permitted refusal | 985 |

The class-adoption pair reproduces both directions of the temporal closure-cell
defect: the callable must retain a cell destination, then read its current
contents after the class-body setter executes. The replacement category includes
every name/cell/member/element read and write, function/default capture, class
scope, call boundary and paired return path enumerated by the design and category
review. These two reproductions do not define the category's complete membership.
The shared-list and hidden cases remain regression guards, not newly observed RED.
Refusal on the hidden pair does not prove precise branch/tuple execution.

No3.14 baseline ran: a RED floor does not unlock dev. GREEN must use exactly the
same population and reviewed controller, floor first then matching dev.

## Authorized implementation checkpoint

The controller's proceed instruction and accepted plan authorize the sole source
writer to implement Task1 in the prepared r010 core worktree. Root reviews the
exact retained state-primitives source and operation ledger before evaluator
wiring. Subsequent plan tasks remain within2500 added-plus-deleted implementation
lines for the first attempt. No tests, expectations, generated files, native
writer, A/B, CI or main checkout may change in this initial candidate.

Cost-review clarifications apply before code is issued:

- A dictionary copy visits n entries and retains2n key/value references, plus
  its allocation. This explicitly resolves the plan's ambiguous n-reference
  shorthand under its per-reference ledger. No duplicated charge categories.
- Never retag a shared table wrapper into child ownership. Detach a new wrapper
  and backing dictionary; check activation-bank ownership separately. Snapshot
  revocation must also stop the continuing parent from mutating retained views.
- Current operation context supplies the budget. Tables, banks and views never
  retain/select a budget from their construction; recursive calls share body
  ownership. All real COW copies remain charged.
- Call snapshots may force growing-table copies. Trace extension should retain
  predecessor edges rather than repeatedly flattening histories. Gate B, not a
  claim about COW, decides whether the representation's cost is acceptable.
- Binder normalization accepts only the optional budget parameter and no-else
  guards containing consume calls. Review charge expressions and placement too:
  exact materialized builtins, nonnegative units, actual reached operations.

No Gate B, broad suite, main integration or ceremonial commit is authorized by
this engineering record. The fixed later gates and Claude finalizer remain.
