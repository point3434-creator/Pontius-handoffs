# R2-E1 builtin-authority transitions: category-complete five-case scope v4

Author: codex/cold_review_a, engineering input author and prior E1 author, not a cold reviewer. This release authorizes no Model, sensitive source, analyzer, harness, candidate, or controller execution.

V1-v3 remain immutable and unexecuted. V4 is a create-only metadata successor to v3 pack `71c5e8efd0922b213a917a1709c271d3d0fa26ba0268d2d8a7f780e942550511`, spec `fd0e8e6b6a23aca5eed9b75baacab4dfbf552e1a8db11d6673d897873ec7ef64`, map `9ccb088c53a317ada694ead9287c1d5fe8f2376d3c2549d99ac1e6cbb731ea7a`, diff `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a`, and handoff `d7ad6c1dc75c1e6b2e3b73a223e3d1c8188b6a755ece20d22a4557f47ce2454b`. It changes no sensitive source, harmless Model, public classification, module-key phase, trace, required argv, exception expectation, or public envelope byte. It adds category-route requirements for T01 and T02 and retains the v3 C01/I01 requirements. V4 pack `rewrite-r2-e1-transition-cases-v4.json` SHA-256 `b2275042ddce8a2a415a5eb9a5a0303b07ef8d64210cccf22ea493601b93e5db`; source differences SHA-256 `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a` remain byte-identical to v1-v3.

Governing design: `rewrite-r2-e1-repair-design-codex-a-v3.md` SHA-256 `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`. Bound source: H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695`, manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`, source `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`. Authorizing retained RED: H `5444e5f3f338840a05157c683fdbf4d2fec66654`, evidence manifest `9e9e68f88f2544c8857d14c02e6a7439c48d76ff53cf22f15859643e5736992c`.

| ID | Public expectation | Additional evidence required to close the category |
| --- | --- | --- |
| T01 | Required refusal; any explicit blocker is safe | Reviewed evidence of outer invocation, nested inner creation, nested inner invocation, and reached explicit `ValueError` fallback |
| T02 | Required refusal; any explicit blocker is safe | Reviewed evidence of outer invocation under retained true proof, inner creation while module `__builtins__` is present and empty, inner invocation, and reached explicit `ValueError` fallback |
| T03 | Exact clean argv and no blocker | None: its clean result proves the live path |
| C01 | Required refusal; any explicit blocker is safe | Reviewed evidence that nested `LOAD_BUILD_CLASS` for `Local` was reached |
| I01 | Required refusal; any explicit blocker is safe | Reviewed evidence that method-local `IMPORT_NAME` for `os as launch_os` was reached |

An earlier blocker can satisfy conservative public safety for any refusal case, but it cannot establish the intended transition or implicit-consumer category. Category closure is therefore a composite claim: runtime GREEN for the fixed public/Model expectations, plus reviewed exact-source hook proof for every T01/T02/C01/I01 route, plus the original E02/E03 evidence that invocation and creation are not blanket-refused. This does not change public refusal adjudication and does not authorize execution of sensitive source.

## Preserved phase and interpreter facts

Module-key phases remain T01 absent/absent, T02 present/present, T03 present/absent, C01 absent/absent, and I01 absent/absent, where the pair is pre-call/post-call. Exact CPython sources remain:

- 3.11.15 `LOAD_BUILD_CLASS`: `https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L2547-L2566`
- 3.11.15 import: `https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L6969-L6980`
- 3.14.6 `LOAD_BUILD_CLASS`: `https://github.com/python/cpython/blob/v3.14.6/Python/generated_cases.c.h#L8802-L8815`
- 3.14.6 import: `https://github.com/python/cpython/blob/v3.14.6/Python/ceval.c#L2942-L2951`

The message-only C01 `NameError` and I01 `ImportError` expectations therefore retain `.name is None`; a future harness must compare actual type, name, message, key phases, identities, traces, and public results.

## Custody

The family remains exactly five cases/five projections: four required refusal and one required clean. Existing E01-E04 and all fixed populations remain unchanged. No harness/controller is included. Root owns independent review, freeze, and future dispatch; these bytes grant no source-fix or payload authorization.
