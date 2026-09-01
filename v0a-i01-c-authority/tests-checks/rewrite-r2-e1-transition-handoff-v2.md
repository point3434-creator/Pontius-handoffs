# R2-E1 transition input handoff v2

Author: codex/cold_review_a, engineering input author, not cold reviewer.

Status: five prospective cases are statically issued; no Model, sensitive source, analyzer, candidate, harness, or controller was imported or executed. V1 remains immutable and unexecuted. V2 supersedes it only because C01's message-only `NameError` has `.name is None`; I01's matching message is now pinned too.

## Issued pins

- `rewrite-r2-e1-transition-cases-v2.json`: `04e202caae3f9203db9859966aea8794e07f30679472ffaeabd3c7b13006da4c`
- `rewrite-r2-e1-transition-spec-v2.md`: `746a9e524c9959bb4c5621f0497b917835fda73c4e84c203a290ab82b87cef5d`
- `rewrite-r2-e1-transition-source-model-map-v2.json`: `24a41515e2f59973a8673f202d5373f12978a4c2c43d4bdf4848d428325d8ec7`
- `rewrite-r2-e1-transition-source-differences-v2.diff`: `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a` (byte-identical to v1)
- governing design: `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`
- held source: `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d` at H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695` / manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`
- authorizing RED: H `5444e5f3f338840a05157c683fdbf4d2fec66654` / evidence manifest `9e9e68f88f2544c8857d14c02e6a7439c48d76ff53cf22f15859643e5736992c`

## Static closure

- Population: exactly 5 cases / 5 projections; 4 required refusal and 1 required clean.
- All five sensitive-source and harmless-Model SHA-256 values are unchanged from v1. Sources and Models were AST-parsed only.
- C01: CPython 3.11.15 and 3.14.0 use message-only `NameError("__build_class__ not found")`; expected `.name` is `None`.
- I01: both versions use message-only `ImportError("__import__ not found")`; expected `.name` is `None`.
- T03: static AST order and `global __builtins__` establish set/delete before method creation; runtime identity, trace, and public cleanliness remain future harness obligations.
- A future harness must observe actual exception type, name, and message and must treat mismatch as oracle/infrastructure failure.

Root owns independent review/freeze and any future harness or dispatch. These bytes grant no payload or source-fix authorization.
