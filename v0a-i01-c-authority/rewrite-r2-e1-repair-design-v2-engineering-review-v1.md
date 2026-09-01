# R2-E1 repair design v2 engineering review v1

Review type: independent read-only engineering design review, not a cold review.
No candidate source, fixture, harness, or payload was changed or executed.

## Bound inputs

- Design v2 SHA-256:
  `98b8c09445425ed03d98c6293684c87c4ec94ddb126b3e996e590de17cae3fd1`
- Checkpoint-2 source SHA-256:
  `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`
- Checkpoint-2 source manifest SHA-256:
  `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`
- Canonical-write census SHA-256:
  `5640242a28caa83b61c08f1c2ac699823fcae53d38ce74b63dd4c579033e6efb`
- Verified E1 RED receipt SHA-256:
  `2040b896281e161f5fee285bc7c62506a867a1dc168feadc96f89ddd4fd4bd00`

## Verdict

**STRAINED / not ready for implementation.** The immutable function-owned proof and its
frame projection are the right-sized representation. The one `_CFunction` producer,
three `_CFrame` producers, and their proposed width charges are coherent. I found no
hidden state-table, snapshot, outcome, or call-summary copy caused by that field.

Two Important design gaps remain:

1. The six-name `_c_read_name` table does not govern CPython's implicit
   `__build_class__` and import-bytecode builtin consumers.
2. The class-body proof is proposed after base evaluation, although CPython captures the
   class-body function's builtins before evaluating bases.

The existing four E1 cases cannot falsify either gap or the v1 nested-creation laundering
rule. A successor design and the five-case transition family below should be frozen and
run against the pre-fix source before implementation.

## Source and accounting closure that is sound

The producer census is exact in the bound source:

- `_CFunction` has one producer at 10768. Its existing six-unit allocation/field charge
  at 10767 becomes seven for the retained boolean.
- `_CFrame` has exactly three producers: class at 10806, call at 10941, and module at
  11389. Each aggregate allocation/field charge gains one unit.
- Both records are frozen, slotted, and `eq=False`. They are retained through existing
  object/state references; no new structural equality or recursive comparison appears.
- `_c_snapshot`, `_c_fork`, `_c_join`, `_CState`, `_CView`, object/cell tables,
  `_COutcome`, `_CTrace`, and `_CCallObservation` need no field or copy change.

The proposed creation helper's existing `_c_namespace` call pays the object lookup. One
new namespace membership probe and, only on absence, one current-frame proof read match
the current semantic accounting convention. The function and call-frame placements are
source-ordered correctly: function proof is computed from the post-header/default state,
stored once, and copied from the selected function record at invocation.

The proposed explicit fallback cost is also coherent: one immutable classification
lookup for every absent module name; on a classified name, one frame-proof read and one
kind branch/comparison; then the unchanged atom, exception-record, or refusal costs.
The implementation must charge the operations its chosen table representation actually
performs rather than preserve these numbers if it uses a different representation.

One documentary correction is needed in the successor: CPython 3.11.15
`PyFunction_NewWithQualName` calls `_PyEval_BuiltinsFromGlobals`, not
`_PyDict_LoadBuiltinsFromGlobals`. The design's absent-key inheritance rule is still
correct: function construction retains a builtins object, and `_PyEval_GetBuiltins`
returns the active frame's builtins when a frame exists.

## Important R2-E1-D1: implicit builtin consumers bypass the gate

The bound analyzer handles `Import` and `ImportFrom` directly at 10565-10591. It creates
a symbolic value and stores the binding without passing through `_c_read_name`. It also
routes `ClassDef` directly to `_c_construct_class` at 10594-10595. Therefore the proposed
six-name table at 9947 cannot govern either operation.

CPython 3.11.15 consults the active frame's builtins in both places:

- `LOAD_BUILD_CLASS` fetches `__build_class__` from `BUILTINS()` and raises before class
  construction when it is missing.
- `IMPORT_NAME` reaches `import_name`, which gets `__import__` from
  `frame->f_builtins` and raises before import binding when it is missing.

For this checkpoint's admitted statement set, the complete builtin-authority consumer
census is therefore:

1. explicit absent-name fallbacks through `_c_read_name`: the existing six names;
2. implicit class construction: `__build_class__`;
3. implicit `Import` and `ImportFrom`: `__import__`.

The successor must keep the six explicit names centralized and add operation-local proof
gates for the two implicit consumer classes. An unproved reached class or import should
take the existing conservative, uncatchable refusal path. This increment must not infer
that a custom mapping has either callable, and it must not promote a new catchable
`NameError` or `ImportError`.

Gate order is a semantic obligation:

- class proof must be checked before bases, namespace creation, body execution, or class
  installation;
- import proof must be checked before symbol creation, binding, or a downstream sink.

The work ledger must add the actual proof read and proof comparison/branch for each gate.
If implementation uses an operation-class table, its lookup is additional. A single
statement-level import proof read is sound because frame proof is immutable; a per-alias
implementation is also sound but must charge every read. Existing refusal construction
and trace/outcome costs remain separate. Attempted work interrupted by the budget cannot
be reported as a completed gate.

## Important R2-E1-D2: class-body capture is after the wrong effects

Design step 5 computes class proof from each `prior.state` immediately before the frame at
10806. In the current source, every such prior is produced by `_c_eval_many` over bases at
10783. This observes module mutations caused during base evaluation.

CPython's `compiler_class` emits `LOAD_BUILD_CLASS`, then makes the class-body function,
then loads the class name and evaluates bases. `MAKE_FUNCTION` creates the function from
the current globals and captured builtins. The class-body builtin authority is therefore
fixed before base expressions run.

The bounded correction is:

1. at class-statement entry, apply the implicit `__build_class__` proof gate;
2. compute the class-body proof from the incoming state and current frame;
3. evaluate bases with the existing logic;
4. install the retained boolean into each reached class frame.

The proof may be an ordinary local scalar across base outcomes. It must not be recomputed
from their post-base states. Its namespace lookup, membership probe, conditional frame
read, and gate work are paid once at the actual chosen placement. If the implementation
instead repeats any of them per outcome, every repetition is charged.

Primary-source basis:

- CPython 3.11.15 `Objects/funcobject.c`, `PyFunction_NewWithQualName`;
- CPython 3.11.15 `Python/ceval.c`, `LOAD_BUILD_CLASS`, `MAKE_FUNCTION`,
  `_PyEval_GetBuiltins`, and `import_name`;
- CPython 3.11.15 `Python/compile.c`, `compiler_class` steps 2-5.

## Minimum pre-fix behavioral transition family

The existing E01-E04 evidence proves direct module creation, retained false authority
after deletion, and local spelling. It does not prove nested creation or implicit
consumers. Static producer counts cannot replace these transitions: a candidate can
special-case direct module creation, inherit blindly inside functions, or leave the
implicit statement paths untouched while satisfying the producer census.

All five cases below are needed as the smallest E1-specific family:

| Case | Transition and observable result | Defect falsified |
| --- | --- | --- |
| T01 | Create an unproved outer function while the module key is present; delete the key; create and invoke a nested function that reaches an explicit fallback. It must refuse. | V1's `absent => proved` laundering rule. |
| T02 | Create a proved outer function while the key is absent; make the module key present before nested creation; the nested fallback must refuse. | Blind inheritance that ignores a current present key. |
| T03 | In the still-proved module frame, make the key present and then delete it before a new class/method is created; the later method fallback must remain clean. | Monotonic module poisoning and over-refusal after safe recovery. |
| T04 | From an unproved function after module-key deletion, reach a nested class. It must refuse before any base, body, class installation, or sink effect. | Missing `__build_class__` gate and wrong gate order. |
| T05 | From the same unproved/absent context, reach function-local `Import` or `ImportFrom`. It must refuse before binding or sink use. | Missing implicit `__import__` gate. |

Freeze harmless CPython Models and public analyzer expectations for all five before the
fix. On the bound source, T01, T02, T04, and T05 should be product REDs; T03 is the
positive transition control. A class case needs an observable base/body/install latch,
and the import case needs a binding/sink latch, so a late refusal cannot masquerade as
correct order.

These five are sufficient only together with static proof that the import gate is exactly
predicate-controlled and its proved branch retains the old body. That prevents a blanket
function-local import refusal without adding a sixth E1 fixture. The retained broader
positive paths still apply. Actual 3.11.15 must run first; the matching 3.14 slot remains
ineligible until the floor family is complete and clean.

## Disposition

Retain the immutable function/frame proof design and the stated producer-width charges.
Do not implement design v2 as written. Issue a successor that adds the complete implicit
consumer census, corrects class source order, accounts for the new gates, and binds the
five transition witnesses. No cap, reserve, exception-promotion, or custom-builtins
precision change is justified by this review.
