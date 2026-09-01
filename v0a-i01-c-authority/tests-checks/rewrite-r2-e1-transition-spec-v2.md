# R2-E1 builtin-authority transitions: corrected five-case prospective scope v2

Author: codex/cold_review_a, engineering input author and prior E1 author, not a cold reviewer. These inputs authorize no Model, sensitive source, analyzer, harness, candidate, or controller execution.

This create-only successor preserves every source, harmless Model, classification, trace, required argv, and public envelope from immutable unexecuted v1. It corrects only C01/I01 exception metadata. V1 pins: pack `15260811af2ff936f925d720639dfec5b367089544fd6e6150ef023382ae5063`, spec `af38727b3c01ff3a42088c29e8fa11c49e71c3d0e26e7133a35217c46055787e`, source/Model map `bdc26b40813cd4feab2d287ebff6181d5c925a274cf354f562beb5d4fcab2263`, source diff `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a`. V2 pack `rewrite-r2-e1-transition-cases-v2.json` SHA-256 `04e202caae3f9203db9859966aea8794e07f30679472ffaeabd3c7b13006da4c`; its source-difference artifact SHA-256 `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a` is byte-identical to v1.

Governing design: `rewrite-r2-e1-repair-design-codex-a-v3.md` SHA-256 `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`. Bound source: H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695`, manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`, source `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`. Authorizing retained RED: H `5444e5f3f338840a05157c683fdbf4d2fec66654`, evidence manifest `9e9e68f88f2544c8857d14c02e6a7439c48d76ff53cf22f15859643e5736992c`. Existing E01-E04 and all other fixed populations remain unchanged.

| ID | Creation and later transition | Sensitive reached consumer | Independent harmless Model expectation | Public requirement |
| --- | --- | --- | --- | --- |
| T01 | Empty module key before `ReviewTests`; false method; delete after class; create inner while key absent | Inner `ValueError()` then exact launch | Outer and inner retain the same empty builtins; `NameError.name == "ValueError"` before launch | Explicit blocker; rows may remain |
| T02 | Create true method before override; set empty key after class; create inner while key present | Inner `ValueError()` then exact launch | Outer retains standard builtins; inner captures the exact empty replacement; `NameError.name == "ValueError"` before launch | Explicit blocker; rows may remain |
| T03 | Set empty then delete before class in proved module frame | Direct method `ValueError()` then exact launch | Driver set/delete precedes method creation; method inherits standard builtins and reaches constructor then launch | Exact fixed argv and no blocker |
| C01 | False method created under empty key; delete after class | Nested `class Local: pass`, then launch using module-imported `os.environ` | Missing implicit `__build_class__` raises message-only `NameError`; `.name is None`; launch is unreachable | Explicit blocker; rows may remain |
| I01 | False method created under empty key; delete after class | Method-local `import os as launch_os`, then launch using `launch_os.environ` | Missing implicit `__import__` raises message-only `ImportError`; `.name is None`; launch is unreachable | Explicit blocker; rows may remain |

## Static exception-metadata basis

CPython 3.11.15 implements missing `LOAD_BUILD_CLASS` with `PyErr_SetString(NameError, "__build_class__ not found")` at `https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L2547-L2566` and missing import with `PyErr_SetString(ImportError, "__import__ not found")` at `https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L6969-L6980`. CPython 3.14.0 has the same message-only constructors at `https://github.com/python/cpython/blob/v3.14.0/Python/generated_cases.c.h#L8802-L8823` and `https://github.com/python/cpython/blob/v3.14.0/Python/ceval.c#L2812-L2823`. Because these calls do not supply a `name` keyword, the statically expected `.name` is `None` for both C01 and I01. This is source proof, not Model runtime evidence.

A future reviewed harness must observe and compare the actual exception `type`, `.name`, and exact `str(error)`. C01 requires `NameError`, `name is None`, message `__build_class__ not found`; I01 requires `ImportError`, `name is None`, message `__import__ not found`. Unexpected type/name/message, a reached launch marker, or any extra/missing trace event is oracle/infrastructure failure.

## T03 driver correspondence

The T03 Model's `_module_driver` declares `global __builtins__`; its assignment and deletion therefore update the controlled `_context`, matching the sensitive program's module assignment/deletion. `_method` is created only after deletion, has no closure/free variables, and is required to share `_context` while retaining the standard builtin context captured by the executing driver. This establishes the intended source-order correspondence statically. It does not claim runtime proof: the future harness must validate outer/inner globals and builtin identities, module-key absence, exact trace, return value, and public result.

## Unchanged boundaries and adjudication

All five programs retain the sole stable ID `tests/test_structural_review.py::ReviewTests::test_static`, canonical public envelope, fixed launch argv, and sensitive-source AST-only rule. T01-T03 retain the exact launch call AST. C01 uses already module-imported `os.environ`; I01 uses the method-local alias. C01 contains no explicit builtin consumer that could mask `LOAD_BUILD_CLASS`; I01 contains no explicit `__import__` call that could mask `IMPORT_NAME`.

The family remains five cases/five projections: four required refusal and one required clean. A blocker suffices for refusal even if a row remains. T03 requires the exact fixed argv and no blocker. No harness/controller is included. Root owns independent review, freeze, and any future dispatch; a pre-fix RED does not authorize development or actual3.14.6 replication.
