# R2-E1 repair design v2 engineering review

Read-only engineering review. I did not edit or import the candidate, execute the analyzer or Models, author fixtures, or run a payload.

## Bound inputs

- Frozen source: H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695`, manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`, `rewrite-r2-checkpoint2-source-v1.py` SHA-256 `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`.
- Design under review: `rewrite-r2-e1-repair-design-codex-a-v2.md` SHA-256 `98b8c09445425ed03d98c6293684c87c4ec94ddb126b3e996e590de17cae3fd1`.
- Canonical write census: `rewrite-r2-e1-canonical-write-census-v1.md` SHA-256 `5640242a28caa83b61c08f1c2ac699823fcae53d38ce74b63dd4c579033e6efb`.
- Existing E01-E04 RED verification: `coordinator-r2-e1-red-verification-v1.json` SHA-256 `6d17bd8218f008e54d90fbadffc47feb57f5e0c1b2522021d8fc1c6841b2ded2`; independent engineering verification SHA-256 `27663f0557ecb179bb4d767c0ac4d0151e60f253c1c704f75dcd9687b35d691e`.
- Prospective transition coverage addendum: `rewrite-r2-e1-repair-design-v2-coverage-addendum-codex-a-v2.md` SHA-256 `b3da849d0ccedc2d675a98fa7d07a5ed90c3de3a204af961cef4e24b0bd824ec`.

## Verdict: STRAINED, bounded core sound but not implementation-ready

The immutable `_CFunction.builtin_fallback_proved` owner and `_CFrame` projection are the right representation. The rule “present globals key means unproved; absent key inherits the creating frame” matches CPython's function creation and prevents both deletion laundering and monotonic namespace poisoning. The field naturally survives aliases, bound methods, containers, forks, snapshots and call observations through the existing object reference.

Two category gaps must be closed before implementation:

1. The class-body proof must be captured before base-expression evaluation, not immediately before the current class-frame constructor after bases.
2. The proof must gate the two admitted implicit builtin consumers, `ClassDef` (`__build_class__`) and `Import`/`ImportFrom` (`__import__`), as well as the six explicit name fallbacks.

The existing E01-E04 family does not test nested creation. Static proof alone is insufficient for the corrected transition rule. The three transition schedules in the coverage addendum are necessary and nonredundant. Two additional unsafe schedules are the minimum behavioral evidence for the implicit consumers.

## CPython rule and source order

CPython v3.11.15 `PyFunction_NewWithQualName` selects builtins from the function's globals and stores the selected object in `func_builtins`; invocation does not recompute it from the caller. See [Objects/funcobject.c](https://github.com/python/cpython/blob/v3.11.15/Objects/funcobject.c) (`PyFunction_NewWithQualName`) and [Python/ceval.c](https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L5075-L5101) (`MAKE_FUNCTION`). `_PyEval_GetBuiltins` returns the current frame's `f_builtins` when a frame exists, which explains the absent-key inheritance rule.

For a class statement, the compiler emits `LOAD_BUILD_CLASS`, then creates the class-body function, then evaluates bases. See [Python/compile.c](https://github.com/python/cpython/blob/v3.11.15/Python/compile.c#L2611-L2626). `LOAD_BUILD_CLASS` reads `__build_class__` from the current frame builtins and fails before the body or bases if it is missing. See [Python/ceval.c](https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L2547-L2571). Therefore `_c_construct_class` must:

1. retain its existing unsupported-header refusal;
2. read/gate the outer `frame.builtin_fallback_proved` before `_c_eval_many(...node.bases)`;
3. at that same pre-base state compute the class-body function proof from module-key presence plus the outer frame proof;
4. carry that immutable scalar through every admitted base outcome and install it on the class frame.

Computing the class proof from `prior.state` after bases is late. It is currently latent because admitted base forms cannot perform the relevant write, but it is the wrong language boundary and would become a real defect as soon as an effectful admitted base is added.

For imports, `IMPORT_NAME` calls `import_name`, which reads `__import__` from `frame->f_builtins` before producing the imported value. See [Python/compile.c](https://github.com/python/cpython/blob/v3.11.15/Python/compile.c#L3687-L3694) and [Python/ceval.c](https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L6969-L7005). An unproved frame may have a usable custom importer, but this design deliberately does not interpret custom builtins, so conservative refusal is required.

## Complete current builtin-authority boundary

Whole-file inspection of the admitted canonical evaluator yields this finite set:

| Operation | Builtin-authority role | Required boundary |
| --- | --- | --- |
| `FunctionDef`/`AsyncFunctionDef` | Creates a function and captures creation-time builtin authority; does not execute its body. | Compute the record proof after admitted decorators/defaults and immediately before `_CFunction` allocation. Dormant creation remains allowed when proof is false. |
| `ClassDef` | Implicitly consumes current-frame `__build_class__`, creates a class-body function, then evaluates bases/body. | If outer frame proof is false, refuse before bases/body. If true, capture the separate class-body proof before bases as described above. |
| Absolute nonstar `Import`/`ImportFrom` | Implicitly consumes current-frame `__import__`. | For each reached admitted alias, read/gate frame proof before qualified-symbol creation or alias storage. Preserve earlier aliases and stop on the first refused outcome. Existing relative/star syntax refusal remains its own earlier admission boundary. |
| `Name` fallback for `ValueError`, `TypeError`, `KeyError`, `IndexError`, `staticmethod`, `__import__` | Explicit global/builtin lookup. | Ordinary lexical/class/module binding wins. Only absent module lookup enters the six-name classified table and frame-proof gate. |
| Literals, list/tuple/dict construction, attribute/subscript, exact identity, numeric negation, truth, assignment/delete, `If`, `Try`, `Raise`, call dispatch | No implicit lookup in the frame builtin mapping in the currently admitted model. Protocol uncertainty retains its existing refusal. | No new authority gate. |
| Unsupported `Assert`, loops, `With`, `Match`, comprehensions/lambda and other reached syntax | Either not admitted or already refused. | No precision expansion in E1. If admitted later, re-audit any implicit opcode rather than treating the current table as universal. |

Checkpoint 3 `GeneratorExp` is a future function-like authority owner. Its generator-function proof must be captured at creation and projected on resume; creation must not execute the body. Future explicit `range`/`sum` support must go through the classified name-fallback gate. No generator field or behavior belongs in this E1 source change.

## Producer and consumer closure

The proposed field touches one `_CFunction` producer and exactly three `_CFrame` constructors:

| Site | Required value |
| --- | --- |
| `_c_construct_function` / `_CFunction(...)` at frozen line 10768 | Creation helper result from the reached post-header state and current frame. |
| Module frame at 11389 | `True`. |
| Class frame at 10806 | Pre-base class-body proof, not a post-base recomputation. |
| Invoke frame at 10941 | `record.builtin_fallback_proved`, never caller/current-module recomputation. |

All `_CFunction` consumers remain compatible: `_c_read_member` binds the referenced record; `_c_call` reads defaults; `_c_invoke` is the sole execution projection; class namespace installation, preflight, `_c_review_outcomes`, call observations, aliases and containers retain the same `_CRef`. `_CFunction` and `_CFrame` use `eq=False`, so the boolean does not add hidden structural-comparison work. `_c_join` keeps outcome/state alternatives rather than flattening records, so no join rule or second authority truth is needed.

The explicit fallback table must be described as the sole **explicit-name** builtin proof table, not the sole builtin consumer. The class/import gates are separate because their bytecodes do not evaluate an `ast.Name` through `_c_read_name`.

## Work accounting

The design's retained-field and creation-helper charges reconcile:

- `_CFunction` record charge increases by one retained boolean field.
- All three `_CFrame` constructor charges increase by one retained field; the module aggregate must increase with it.
- Creation helper retains `_c_namespace`'s existing object read, adds the `"__builtins__"` membership probe, and reads the frame proof only on absence.
- Explicit absent-name lookup charges the classified-table lookup, matched proof read and kind branch in addition to the existing proof/value/refusal work.

The category closure adds actual work not listed in v2:

- Class: charge the reached outer-frame proof read and guard comparison before any base work. Charge the creation helper separately. If an implementation reuses the already-read `True` scalar for the helper's absent-key inheritance, charge only the operations actually performed; otherwise charge the second read honestly.
- Import: charge a frame-proof read and guard comparison for each reached admitted alias before symbol allocation/string construction/storage. A refused first alias must not precharge or execute later aliases.

No state/view/namespace/table/join field or COW algorithm changes are needed. The immutable fallback table itself is static syntax; per-analysis lookup and branch work remains metered. The successor ledger must update the exact cumulative delta from c8fc and stay within the unchanged R2 ceiling.

## Minimum honest pre-fix behavioral coverage

E01-E04 prove the original visible-key cases but do not force the new nested-creation rule. The three proposed schedules are sufficient and nonredundant for its four-state transition table:

- T01: false creating frame + absent key when nested function is created; required refusal. This detects deletion laundering.
- T02: true creating frame + present key; required refusal. This detects blindly copying the frame bit.
- T03: earlier present/delete, then true module/class frame + absent key creates the method; required clean exact launch. This rejects monotonic historical poisoning.

Pre-fix expectation is two REDs (T01/T02 wrongly clean) and one clean control (T03), but that is a source prediction, not runtime evidence. These three must be frozen and run before a fix; static proof alone does not establish the transition.

Two additional reached unsafe witnesses are required for the implicit consumers:

1. **Nested class / `__build_class__`:** import `os`, `subprocess`, `sys`, `unittest` at module entry; set module `__builtins__ = {}` while defining the method, then delete the key. In the unproved method, execute a nested class whose body contains the existing sink using module-imported `os.environ`. Real Python fails at `LOAD_BUILD_CLASS` before bases/body; current7ce can enter the body and report the launch. Required result: explicit refusal and no launch row. Using module-imported `os` prevents an explicit `__import__` fallback from masking the missing class gate.
2. **Local import / implicit `__import__`:** use the same unproved-method setup; inside it execute `import os as local_os`, then the sink using `local_os.environ`. Real Python fails the import before alias binding; current7ce creates the symbol and can report the launch. Required result: explicit refusal and no launch row.

Harmless Models should use real `FunctionType` creation with an empty builtin mapping and record only scalar events/exceptions. Sensitive sources remain AST-only. Existing E01 supplies the positive module-frame import/class path, and T03 supplies a positive function/frame proof plus exact launch. Five new schedules (T01-T03 plus the two implicit unsafe witnesses) are therefore the minimum if the successor static review proves both new gates are the same boolean predicate with the exact ordering above. If their implementations diverge by scope or helper, add one combined proved-method control containing a local import and nested class rather than relying on that static equivalence.

## Required disposition before source GO

Amend v2 additively to move class-body proof capture before bases and enumerate/gate `ClassDef` and `Import`/`ImportFrom`. Freeze and run the five-case pre-fix extension. Preserve E01-E04, all legacy refusal boundaries, caps, binder bytes and current custom-builtins noninterpretation. With those changes the representation is bounded and sound; without them the design can still authorize false-clean class/import effects from an unproved frame.
