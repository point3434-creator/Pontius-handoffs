# R2-E1 builtin-authority transitions: five-case prospective scope

Author: codex/cold_review_a, engineering input author and prior E1 author, not a cold reviewer. These inputs are frozen before payload. This specification authorizes no Model, sensitive source, analyzer, harness, candidate, or controller execution.

Governing design: `rewrite-r2-e1-repair-design-codex-a-v3.md` SHA-256 `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`. Authorizing retained RED: H `5444e5f3f338840a05157c683fdbf4d2fec66654`, `rewrite-r2-e1-red-evidence-v1-manifest.sha256` SHA-256 `9e9e68f88f2544c8857d14c02e6a7439c48d76ff53cf22f15859643e5736992c`, source `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`. Existing E01-E04 pack `59b8457a2323634d883fb2c9b0ff82a1e60cd980c5f2a4b50e627c8ca32cdb9b` and its owner remain unchanged. New pack `rewrite-r2-e1-transition-cases-v1.json` SHA-256 `15260811af2ff936f925d720639dfec5b367089544fd6e6150ef023382ae5063`; exact source differences SHA-256 `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a`.

| ID | Creation and later transition | Sensitive reached consumer | Independent harmless Model outcome | Public requirement |
| --- | --- | --- | --- | --- |
| T01 | Empty module key before `ReviewTests`; false method; delete after class; create inner while key absent | Inner `ValueError()` then exact launch | Outer and inner retain the same empty builtins; `NameError(ValueError)` before launch | Explicit blocker; rows may remain |
| T02 | Create true method before override; set empty key after class; create inner while key present | Inner `ValueError()` then exact launch | Outer retains standard builtins; inner captures the exact empty replacement; `NameError(ValueError)` before launch | Explicit blocker; rows may remain |
| T03 | Set empty then delete before class in proved module frame | Direct method `ValueError()` then exact launch | Proved driver performs set/delete; resulting method inherits the exact standard builtins and reaches constructor then launch | Exact fixed argv and no blocker |
| C01 | False method created under empty key; delete after class | Nested `class Local: pass`, then launch using module-imported `os.environ` | Real nested class construction under retained empty builtins raises `NameError(__build_class__)` before launch | Explicit blocker; rows may remain |
| I01 | False method created under empty key; delete after class | Method-local `import os as launch_os`, then launch using `launch_os.environ` | Real import under retained empty builtins raises `ImportError` before launch | Explicit blocker; rows may remain |

## Sensitive source boundaries

All five programs preserve the byte-equivalent public envelope, sole stable ID `tests/test_structural_review.py::ReviewTests::test_static`, inventory document, item universe, public API, and fixed launch argv. T01-T03 retain the existing subprocess call AST exactly; indentation/location is ignored. C01 changes only the environment source to already module-imported `os.environ`; I01 changes it to the method-local alias `launch_os.environ`. Their remaining call contract is AST-identical after replacing the authorized `env` expression with one sentinel.

T01/T02 use a synchronous zero-argument nested function so no `__build_class__` refusal can mask the creation-proof transition. T03 consumes the resulting method proof directly, so a true helper cannot mask a false method. C01 contains neither `ValueError` nor explicit `__import__`; I01 contains neither `ValueError` nor explicit `__import__`. C01 and I01 stay separate so one implicit gate cannot mask the other. Top-level imports execute in the initially proved module frame before the explicit override. Sensitive bytes are supplied only to `derive_design_review` and must never be executed.

## Independent Model contract

Each pinned `oracle_source` only defines inert data/code, installs one outer code object into an exact controlled globals dictionary with `types.FunctionType` supplied as `_FUNCTION_TYPE`, and performs the specified dictionary transition. Authoring statically parses but never executes these Models.

A future reviewed harness must, before calling `_function`, prove exact function type, `_function.__globals__ is _context`, `_function.__builtins__ is _outer_builtin_context`, no closure/free variables, and the prescribed module-key presence. After T01/T02/T03 creates its inner function, it must prove exactly one captured function, that function's globals identity, and `inner.__builtins__ is _inner_builtin_context`. These identities are reported only as booleans/counts; no live object is serialized.

The harness may catch only the expected `NameError` or `ImportError` outside the Model body and must record type plus `.name` where present. T01/T02 require `NameError.name == "ValueError"`; C01 requires `NameError.name == "__build_class__"`; I01 requires `ImportError` with `.name is None`; T03 must return `"fixed"`. Any other exception, missing identity, missing/extra trace, or reached `launch` in a refusal case is oracle/infrastructure failure. The I01 code contains one real `import os as launch_os`, but the harness proves the captured builtin dictionary is empty before call, so the opcode fails at unavailable `__import__` before importer or external work. No Model uses subprocess, files, network, candidate code, or sensitive source.

## Adjudication and custody

The prospective family has five cases/five projections: four required refusal and one required clean. An explicit blocker is sufficient for a refusal even if a launch row remains; do not demand no row. T03 requires exactly the fixed argv and no blocker. Existing E01-E04, Gate A/B populations, expectations, caps, snapshots, and owners remain byte-exact and are not rerun or altered by this input release.

No harness/controller is included. Root must independently review/freeze any future adapter and dispatch. A future pre-fix RED is retained evidence only and does not authorize a development slot or actual3.14.6 replication. Source/Model/analyzer errors, incomplete results, custody failures, timeouts, or wrong exception types are not product RED.
