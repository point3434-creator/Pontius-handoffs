# R2-E1 transition input handoff v4

Author: codex/cold_review_a, engineering input author, not cold reviewer.

Status: controlling metadata-only successor issued; no Model, sensitive source, analyzer, candidate, harness, or controller was imported or executed. V1-v3 remain immutable and unexecuted.

## Issued pins

- `rewrite-r2-e1-transition-cases-v4.json`: `b2275042ddce8a2a415a5eb9a5a0303b07ef8d64210cccf22ea493601b93e5db`
- `rewrite-r2-e1-transition-spec-v4.md`: `bf4ba88a299651f7e3167b3ee8ea2cb853767bd19fbd612a0fe500a1475947bc`
- `rewrite-r2-e1-transition-source-model-map-v4.json`: `fabf97bd74f26c980c4bba8ef1a43d9fc68232889bbc5164c8e030b0db027888`
- `rewrite-r2-e1-transition-source-differences-v4.diff`: `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a` (byte-identical to v1-v3)
- v3 controlling predecessor: pack `71c5e8efd0922b213a917a1709c271d3d0fa26ba0268d2d8a7f780e942550511`, spec `fd0e8e6b6a23aca5eed9b75baacab4dfbf552e1a8db11d6673d897873ec7ef64`, map `9ccb088c53a317ada694ead9287c1d5fe8f2376d3c2549d99ac1e6cbb731ea7a`, handoff `d7ad6c1dc75c1e6b2e3b73a223e3d1c8188b6a755ece20d22a4557f47ce2454b`
- governing design: `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`
- held source: `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d` at H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695` / manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`

## Static closure

- Exactly 5 cases / 5 projections: 4 required refusal, 1 required clean.
- Source, Model, public classification, key phases, traces, argv, exception expectations, and envelope are byte/structure-identical to v3.
- T01 route: outer invocation → inner creation → inner invocation → explicit `ValueError` fallback.
- T02 route: outer invocation under retained true proof → inner creation with present empty key → inner invocation → explicit `ValueError` fallback.
- C01/I01 retain their exact implicit-consumer route requirements. T03 has no additional route requirement because exact clean argv/no blocker proves its live path.
- Final category closure is composite runtime GREEN plus reviewed exact-source hook proof for all four refusal routes, with original E02/E03 evidence preventing blanket invocation/creation refusal.
- Exact interpreter proof remains bound to CPython 3.11.15 and actual 3.14.6.

Root owns independent review/freeze and any future adapter/dispatch. These bytes grant no payload or source-fix authorization.
