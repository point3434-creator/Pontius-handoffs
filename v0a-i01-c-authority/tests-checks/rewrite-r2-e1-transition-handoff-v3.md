# R2-E1 transition input handoff v3

Author: codex/cold_review_a, engineering input author, not cold reviewer.

Status: five prospective cases are statically issued. No Model, sensitive source, analyzer, candidate, harness, or controller was imported or executed. V1/v2 remain immutable and unexecuted. V3 is the controlling successor: it preserves their source/Model/classification/trace bytes, fixes key-phase metadata, and uses exact CPython 3.11.15/3.14.6 source provenance.

## Issued pins

- `rewrite-r2-e1-transition-cases-v3.json`: `71c5e8efd0922b213a917a1709c271d3d0fa26ba0268d2d8a7f780e942550511`
- `rewrite-r2-e1-transition-spec-v3.md`: `fd0e8e6b6a23aca5eed9b75baacab4dfbf552e1a8db11d6673d897873ec7ef64`
- `rewrite-r2-e1-transition-source-model-map-v3.json`: `9ccb088c53a317ada694ead9287c1d5fe8f2376d3c2549d99ac1e6cbb731ea7a`
- `rewrite-r2-e1-transition-source-differences-v3.diff`: `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a` (byte-identical to v1/v2)
- governing design: `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`
- held source: `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d` at H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695` / manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`
- authorizing RED: H `5444e5f3f338840a05157c683fdbf4d2fec66654` / evidence manifest `9e9e68f88f2544c8857d14c02e6a7439c48d76ff53cf22f15859643e5736992c`

## Static closure

- Exactly 5 cases / 5 projections: 4 required refusal, 1 required clean.
- Every sensitive-source and harmless-Model hash is unchanged from v1/v2; all ten strings were AST-parsed only.
- Key phases: T01 absent/absent; T02 present/present; T03 present/absent; C01 absent/absent; I01 absent/absent.
- Exact interpreter sources show C01 `NameError` and I01 `ImportError` are message-only with `.name is None` in both actual versions.
- T03's global assignment/delete and method-creation order is statically equivalent; actual identities, phase states, trace, and result remain future harness obligations.
- C01/I01 explicit blockers satisfy safe refusal. A claim that the intended implicit-consumer category is closed additionally requires evidence the named consumer was reached, preventing an earlier conservative blocker from masquerading as category precision.

Root owns independent review/freeze and any future adapter/dispatch. These bytes grant no payload or source-fix authorization.
