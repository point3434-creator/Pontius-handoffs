# R2-E1 builtin-authority transitions: lineage-corrected five-case scope v5

Author: codex/cold_review_a, engineering input author and prior E1 author, not a cold reviewer. This release authorizes no Model, sensitive source, analyzer, harness, candidate, or controller execution.

V1-v4 remain immutable and unexecuted. V5 is a create-only lineage correction bound to all five v4 artifacts: pack `b2275042ddce8a2a415a5eb9a5a0303b07ef8d64210cccf22ea493601b93e5db`, spec `bf4ba88a299651f7e3167b3ee8ea2cb853767bd19fbd612a0fe500a1475947bc`, map `fabf97bd74f26c980c4bba8ef1a43d9fc68232889bbc5164c8e030b0db027888`, diff `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a`, and handoff `d1eff592fd2bf4cc18e3f47a338daea959d9ae121d1940e8ffb55831ef7999f2`. V4 introduced exactly two metadata changes: (1) T01/T02 category-route closure requirements and (2) a narrowed exact CPython 3.14.6 import citation from `L2941-L2951` to `L2942-L2951`. V5 retains the corrected `L2942-L2951` citation.

V5 changes no governed source, Model, expectation, classification, pre/post module-key phase, trace, argv, exception metadata, public envelope, category-route requirement, or category-closure contract from v4. V5 pack `rewrite-r2-e1-transition-cases-v5.json` SHA-256 `946457a644ab777e3c0a66e84c5f942740cec027d03500582ff31b300c16d427`; source differences SHA-256 `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a` remain byte-identical to v1-v4.

Governing design: `rewrite-r2-e1-repair-design-codex-a-v3.md` SHA-256 `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`. Bound source: H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695`, manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`, source `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`. Authorizing retained RED: H `5444e5f3f338840a05157c683fdbf4d2fec66654`, evidence manifest `9e9e68f88f2544c8857d14c02e6a7439c48d76ff53cf22f15859643e5736992c`.

## Preserved route and category contract

- T01 category closure still requires reviewed evidence of outer invocation, nested inner creation, nested inner invocation, and reached explicit `ValueError` fallback.
- T02 category closure still requires outer invocation under retained true proof, inner creation while module `__builtins__` is present and empty, inner invocation, and reached explicit `ValueError` fallback.
- C01/I01 retain their exact implicit-consumer route requirements.
- T03 retains no extra route requirement because exact clean argv plus no blocker proves its live path.
- Any explicit blocker remains safe public refusal, but earlier refusal alone does not close a refusal-route category.
- Final closure remains composite runtime GREEN plus reviewed exact-source hook proof for all four refusal routes, together with original E02/E03 evidence against blanket invocation/creation refusal.

## Exact interpreter citations

The four exact release citations are unchanged from v4. In particular, the actual CPython 3.14.6 import citation is `https://github.com/python/cpython/blob/v3.14.6/Python/ceval.c#L2942-L2951`. The C01/I01 message-only exception expectations and `.name is None` remain unchanged.

## Custody

The family remains exactly five cases/five projections: four required refusal and one required clean. Existing E01-E04 and all fixed populations remain unchanged. No harness/controller is included. Root owns independent review, freeze, and any future dispatch; these bytes grant no source-fix or payload authorization.
