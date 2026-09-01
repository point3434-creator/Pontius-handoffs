# R2-E1 builtin authority repair design, codex A v2

Engineering design only; no source change, candidate import, analyzer execution, Model execution or new fixture. Author: codex/cold_review_a, an engineering participant and the E1 input/harness author, not a cold reviewer.

V1 SHA256 2e4eba3bd4af7fdcebbdf58de28997be90398ec76421fb0d1d8d3e05483bfd11 remains immutable and is superseded by this version. V1 incorrectly treated an absent module __builtins__ key as universal proof of the ordinary builtin dictionary. CPython falls back to the current frame's f_builtins when that globals key is absent. This version corrects the creation rule without changing the recommended representation or case scope. Primary source basis: CPython v3.11.15 PyFunction_NewWithQualName calls _PyDict_LoadBuiltinsFromGlobals, and _PyEval_GetBuiltins returns the current frame's f_builtins when a frame exists.

Bound source: H beff8193e9d5ce7316f5006fccc77ffcb5ca5695; source manifest ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b; rewrite-r2-checkpoint2-source-v1.py SHA256 7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d. Bound canonical census: rewrite-r2-e1-canonical-write-census-v1.md SHA256 5640242a28caa83b61c08f1c2ac699823fcae53d38ce74b63dd4c579033e6efb.

Retained RED evidence was produced and verified by root, not rerun here: coordinator-r2-e1-red-verification-v1.json SHA256 6d17bd8218f008e54d90fbadffc47feb57f5e0c1b2522021d8fc1c6841b2ded2 binds receipt 2040b896281e161f5fee285bc7c62506a867a1dc168feadc96f89ddd4fd4bd00. E01 and E04 are clean; E02 and E03 retain the launch row without a blocker although their independent Models raise NameError naming ValueError.

## Recommendation

Represent one immutable positive proof on every canonical function record: builtin_fallback_proved. It says only that this function selected the ordinary builtin environment when it was created. Project that proof into the dynamic _CFrame used to execute the function. Consult it only when an absent module name reaches a canonical builtin fallback.

Do not add a general custom-builtins interpreter. Any present module __builtins__ binding is unproved, regardless of its canonical value. An unproved function may still execute all supported operations that do not need an absent-name builtin fallback. A reached fallback produces the existing ordinary unsupported _c_fail result. This keeps dormant definitions and code using explicit module/lexical bindings free of blanket refusal.

## Why function provenance is the smaller sound history

The immutable _CFunction at 9148 is the lifetime owner of creation-time builtin authority. It already survives aliases, members, containers, returns, forks, snapshots and call history as an object-table record reached through _CRef. Later deletion or rebinding of the module key does not mutate that record.

A monotonic builtins_unproved bit on _CNamespace would also keep E03 unsafe if copied into functions, but it is unnecessarily broad:

- it would poison every function defined after an override was deleted, although creation in a proved module/outer frame with no module key inherits that proved frame;
- it would add a field and copy/charge obligation to every module and class namespace construction and every _c_namespace_write, not just function creation and execution;
- it would invite current-module lookup as a second truth beside the captured function record.

Creation-time module inspection combined with the current executing frame's proof is exact for the admitted model. A present module key makes the new function unproved. If the key is absent, the new function inherits the current frame's proof: module code with its initial proved frame can create a proved later function after deletion, while code executing in an already-unproved function cannot launder its captured environment by deleting the module key. An override present during definition makes that function unproved forever, including after E03 deletion.

## Concrete representation and flow

1. Add builtin_fallback_proved: bool as a required final field of _CFunction at 9148 and _CFrame at 9138. Do not provide a default: all producer sites must state the authority source.

2. Add one narrow helper such as _c_created_builtin_fallback_proved(ctx, state, frame). It reads frame.module through _c_namespace. If "__builtins__" is present, return false without interpreting the value. If absent, return frame.builtin_fallback_proved. The inherited frame value models CPython's _PyEval_GetBuiltins fallback and prevents deletion inside an unproved function from laundering a nested definition.

3. In _c_construct_function 10695, compute the proof from prior.state and the current frame after decorator/default evaluation and before _CFunction allocation. This source-order position matters: it observes the same successor from which the function object is created. A present module key wins as unproved; only an absent key inherits the current frame proof. Never inspect the later invocation caller.

4. In _c_call 10819, after the selected _CFunction record has been established, copy its proof into the new local _CFrame at 10941. Entry, bound method, recursive and ordinary helper calls all use this same site. The existing same-source cross-module refusal remains unchanged; this change does not add cross-module execution.

5. The implicit class-body frame at _c_construct_class 10776 is also function-like. Apply the same creation helper to the reached prior.state and current frame immediately before constructing the class frame at10806. Method records created in the body independently apply the rule from their own reached state/frame. A class-local spelling named __builtins__ is never module authority.

6. The initial module frame at11389 starts with builtin_fallback_proved true. Module execution begins in the ordinary environment represented by the public review setup. A later module assignment changes globals but does not retroactively replace that already-running frame's builtin environment.

7. Centralize the six absent-module fallback names behind one classified immutable table and one gate in _c_read_name 9947:
   - exception proof: ValueError, TypeError, KeyError, IndexError;
   - legacy symbol fallback: staticmethod, __import__.
   A real lexical, class or module binding still wins before this gate. If the name is in the table and frame.builtin_fallback_proved is false, return _c_fail at the reached Name site. If true, construct the existing proof/symbol exactly as today. An absent name outside the table follows the existing unresolved-name refusal. Any future builtin producer must be added to this same table/gate; no direct absent-module proof constructor is allowed elsewhere.

This is one semantic truth: the function record owns captured authority, while the frame field is its execution projection. It is not recomputed from the current module during the call.

## Admission-route closure

The proof helper observes the current module member map, so no syntax-specific hook or reserved-name ban is required.

| Admitted route | Result at a later function creation |
| --- | --- |
| Ordinary/chained assignment and exact destructuring | Key present, therefore unproved. |
| Module Name deletion | Previously created functions keep their recorded value. A later definition sees an absent key and inherits the executing frame proof; deletion cannot turn an unproved outer frame into proved authority. |
| Import or ImportFrom alias named __builtins__ | Key present, therefore unproved. |
| Function, async-function or class definition installed with that name | Key present, therefore unproved. |
| Literal None, empty/exact-string dictionary, sequence or symbolic admitted values | Presence alone is unproved; value interpretation is unnecessary. |
| Aliased mutation of a value under the key | The module key remains present; still unproved. |
| Function-local parameter/assignment/delete named __builtins__ | Cell route only; module membership and the function record do not change. |
| Class-local spelling | Class namespace only; it is not module builtin authority. |
| Declared module write from a nonmodule frame, relative/star imports, reflection and unsupported target forms | Existing refusal remains; no new admission. |

Ordered If/Try/helper outcomes retain separate _CState objects. _c_join only deduplicates outcome identity and does not merge object records, so each reached function ref retains the proof computed from its own state. _c_snapshot and _c_fork retain the immutable object table; copy-on-write preserves historical records. _CCallObservation already retains the selected ref and an entry _CView, so no duplicate provenance field is needed in call summaries or outcomes.

## Fallback and refusal behavior

The gate belongs after ordinary route/member lookup and before a fallback object is created. This yields these required distinctions:

- E01: no key at method creation, proof true, ValueError fallback remains admitted.
- E02: empty module map is present at method creation, proof false, reached ValueError fallback refuses before launch.
- E03: proof was recorded false before module deletion, so later invocation still refuses.
- E04: local assignment changes only a cell; method proof is true and fallback remains admitted.
- A module-defined ValueError or an alias captured before the override bypasses absent-name fallback and retains its existing value semantics.
- An unproved function that never reaches one of the six fallbacks is not refused merely for existing.
- staticmethod decorators and __import__ calls are governed by the same proof, not exception-only special cases.

Class-body fallback uses its class-frame proof. Module-body fallback uses the initial module-frame proof; assigning __builtins__ during that same already-running module body does not rewrite its execution frame.

## Exact work-accounting obligations

Use existing _AnalysisBudget.consume only; no cap, reserve or epoch changes.

- Creation proof check: _c_namespace pays its existing object read. Add one explicit unit for the "__builtins__" membership probe. When absent, add one unit for reading the current frame proof. Presence returns unproved without that read. It allocates nothing.
- _CFunction: add one unit to the current six-unit record/field charge for the retained boolean.
- _CFrame: add one retained-field unit at each of the exactly three constructor sites: module 11389, class10806 and call10941. Adjust their aggregate comments and charges.
- Fallback classification: retain one explicit unit for the immutable fallback-table lookup on every absent module name. On a matched fallback, add one unit for reading the frame proof and one for the classified kind branch/comparison. Existing _CExceptionType allocation, _c_atom work, or _c_fail issue/trace/outcome work remains separately charged.
- No _CState, _CView, namespace, cell/object table, capture, outcome, trace or call-observation field changes are required. Therefore there is no new fork/snapshot/join/table-copy work.
- If implementation chooses a representation other than the proposed immutable classified table, it must charge every actual lookup/comparison/allocation/reference rather than retain these numbers by assertion.

R2 cumulative raw SequenceMatcher(autojunk=False) accounting is 360 added+deleted lines before this fix, against the separate 1500-line R2 ceiling. The successor must report its exact delta from c8fc and cumulative count; no line-budget exception follows from this design. R1 binder bytes/normalization, all original budget caps, original expectations, protected16 and the 1761-file base remain exact.

## Required static and behavioral checks

Before dispatch:

- exact source/census/design pins and W watch match;
- exactly one _CFunction producer and exactly three _CFrame constructors supply the new required field;
- sole absent-module fallback table contains exactly the six existing names and both producer kinds;
- no _CExceptionType or staticmethod/__import__ absent-name producer bypasses the proof gate;
- proof is computed from prior.state after function header/default effects; present key means unproved, absent key inherits the current execution frame, and invocation never recomputes it from its caller/current module;
- local/class __builtins__ routes remain cell/class writes and no general reserved-name ban appears;
- sole namespace writer/caller census and all six legacy uncatchable diagnostic sites remain unchanged;
- every new membership/field/table/branch operation has the declared charge;
- R1 binder byte equality, protected16, caps and raw R2 line count pass the retained static aid.

Behavioral acceptance uses the already frozen E1 four-case family unchanged. A fixed candidate must pass complete, integrity-clean E01-E04 on actual3.11.15 before the matching actual3.14.6 slot is eligible. The existing Gate A/R2 focused populations and preservation/static gates remain independently required; this note adds no new cases or custom-builtins precision promise.

## Design verdict

Recommend direct immutable function provenance with a projected frame field, the corrected creation rule (present module key => unproved; absent key => inherit executing frame), and a single centralized fallback gate. It is category-complete for the admitted module binding/removal routes and all six existing fallback names, preserves later-deletion history without authority laundering through nested creation, keeps local spelling safe, and avoids module-wide monotonic over-refusal and namespace-copy cost.
