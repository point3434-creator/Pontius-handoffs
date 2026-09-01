# R2-E1 builtin-authority transitions: phase-exact five-case prospective scope v3

Author: codex/cold_review_a, engineering input author and prior E1 author, not a cold reviewer. These inputs authorize no Model, sensitive source, analyzer, harness, candidate, or controller execution.

V1 and v2 remain immutable and unexecuted. V3 preserves every source, harmless Model, classification, trace, required argv, and public envelope. It (1) retains v2's corrected message-only C01/I01 exception metadata, (2) splits module-key state into explicit pre-call and post-call fields for every case, and (3) binds the exact actual interpreter source versions 3.11.15 and 3.14.6. V2 pins: pack `04e202caae3f9203db9859966aea8794e07f30679472ffaeabd3c7b13006da4c`, spec `746a9e524c9959bb4c5621f0497b917835fda73c4e84c203a290ab82b87cef5d`, map `24a41515e2f59973a8673f202d5373f12978a4c2c43d4bdf4848d428325d8ec7`, handoff `0105d58f6987a424ad11f5e25202c1e73f01bf24bbd37b0d0e5e92ea23fb165b`. V3 pack `rewrite-r2-e1-transition-cases-v3.json` SHA-256 `71c5e8efd0922b213a917a1709c271d3d0fa26ba0268d2d8a7f780e942550511`; source differences SHA-256 `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a` are byte-identical to v1/v2.

Governing design: `rewrite-r2-e1-repair-design-codex-a-v3.md` SHA-256 `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`. Bound source: H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695`, manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`, source `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`. Authorizing retained RED: H `5444e5f3f338840a05157c683fdbf4d2fec66654`, evidence manifest `9e9e68f88f2544c8857d14c02e6a7439c48d76ff53cf22f15859643e5736992c`. Existing E01-E04 and all fixed populations remain unchanged.

| ID | Pre-call key | Post-call key | Creation and consumer | Independent harmless Model expectation | Public requirement |
| --- | --- | --- | --- | --- | --- |
| T01 | absent | absent | False outer; create inner after deletion; inner `ValueError()` | Outer and inner retain empty builtins; `NameError.name == "ValueError"` before launch | Explicit blocker; rows may remain |
| T02 | present | present | True outer; replace key with empty before call; inner `ValueError()` | Outer retains standard builtins; inner captures exact empty replacement; `NameError.name == "ValueError"` | Explicit blocker; rows may remain |
| T03 | present | absent | Proved module driver sets/deletes key before method creation; direct `ValueError()` | Method inherits standard builtins and reaches constructor then launch | Exact fixed argv and no blocker |
| C01 | absent | absent | False outer after deletion; nested `class Local: pass` | Missing implicit `__build_class__` gives message-only `NameError`, `.name is None`; launch unreachable | Explicit blocker; rows may remain |
| I01 | absent | absent | False outer after deletion; method-local `import os as launch_os` | Missing implicit `__import__` gives message-only `ImportError`, `.name is None`; launch unreachable | Explicit blocker; rows may remain |

“Pre-call” means immediately before invoking the Model's `_function`; “post-call” means after normal return or after the reviewed harness catches the expected exception. The harness must validate both phases. T03 deliberately starts with `_context["__builtins__"]` present and deletes it inside `_module_driver`; its old lone `module_key_present: false` described only the post-call state.

## Exact interpreter-source proof

CPython 3.11.15 implements missing `LOAD_BUILD_CLASS` with `PyErr_SetString(NameError, "__build_class__ not found")` at `https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L2547-L2566` and missing import with `PyErr_SetString(ImportError, "__import__ not found")` at `https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L6969-L6980`. The actual development interpreter version 3.14.6 uses the same message-only constructors at `https://github.com/python/cpython/blob/v3.14.6/Python/generated_cases.c.h#L8802-L8815` and `https://github.com/python/cpython/blob/v3.14.6/Python/ceval.c#L2941-L2951`. No `name` keyword is supplied, so `.name is None` for C01 and I01. This is static source proof; future execution must still observe and compare actual type, name, and exact message.

## T03 static correspondence

The T03 Model's `_module_driver` declares `global __builtins__`. Its assignment and deletion therefore update `_context`, in the same order as the sensitive module assignment/deletion before `ReviewTests` construction. `_method` is created only after deletion and has no closure variables. Model source order therefore supports pre-call-present/post-call-absent and the intended builtins fallback. Runtime function/global/builtin identities, trace, return, key phases, and public cleanliness remain future harness obligations.

## Category-route evidence

C01 and I01 are nonmasked in Model space because their exact expected exception type/message can only arise at the intended implicit operation. Public analyzer adjudication remains conservative: any explicit blocker is a safe required-refusal result, even if a row remains. But a blocker raised earlier at outer `ReviewTests` or method creation does not prove the implicit `LOAD_BUILD_CLASS` or `IMPORT_NAME` category has been analyzed. Any later category-closure claim must therefore include reviewed route/observer or source-proof evidence that the named consumer was reached. Without that evidence the case may be safely refused but the category remains unproved. This requirement does not demand executing sensitive source.

## Custody

All five programs retain sole stable ID `tests/test_structural_review.py::ReviewTests::test_static`, canonical public envelope, fixed launch argv, and sensitive-source AST-only handling. T01-T03 retain the exact launch call AST. C01 uses module-imported `os.environ`; I01 uses the method-local alias. The family remains five cases/five projections: four required refusal, one required clean. No harness/controller is included. Root owns independent review, freeze, and any future dispatch; pre-fix RED does not authorize source repair or actual3.14.6 replication.
