# R2 identity harness v2 lifecycle handoff

R2-H1 addressed across acquisition through teardown. This is AST/hash evidence only, not an executed fault-injection or analyzer result. Root must review and freeze before dispatch; this author does not freeze/publish or run payloads.

All twelve v1 authoring artifacts are byte-preserved. Original BudgetObserver, MechanismObserver, reconciliation, public/Model/depth definitions, source/Models/population/spec/caps and seventeen payload files remain unchanged. The only prior probe definition changed is main; control changes are main/validate_result plus the shared lifecycle validator.

Acquisition is protected before first mutation. Teardown independently attempts both observers, then unconditionally restores captured hook/class-method identities. Original public exception capture is preserved; a propagated exception is never replaced by teardown diagnostics. Scalar lifecycle failures block admission, and failed rollback stops further cases after retaining the completed case record. Full raw floor replay requires lifecycle_ok too.

| Artifact | SHA-256 |
|---|---|
| rewrite-r2-identity-plan-v2.md | 4351e0f61ff81f6fbb1800df669a642501f10c40e72de80430d4d396b0b6e1db |
| rewrite-r2-identity-probe-v2.py | c654355be85a85fe53bb00c7e55201e6ccc969edb227d4159b26d415669bee38 |
| rewrite-r2-identity-control-v2.py | e9537417f951343d7128663234aa05c758a4f32d11ce957b740c145120330039 |
| rewrite-r2-identity-observer-map-v2.json | 5463f81a8c3714e0970585c6b4b2eb9dd2bd547105c4ae6a8f9f53f0a08d699c |
| rewrite-r2-identity-compatibility-v2.json | 314c49262b68d6aaf34da6b5184804b8267beaeda5d5266c074e2576b90b85a3 |
| rewrite-r2-identity-projector-proof-v2.json | 78797549a9c32fda45a2310b8ac79828b139b67ac9e1c6b8101a80c6c6d49e84 |
| rewrite-r2-identity-probe-from-v1-v2.diff | c87d0b2f760281a943d00234def71c8b668a017d8b28ad7403a2f4c4ebdc4e31 |
| rewrite-r2-identity-control-from-v1-v2.diff | 1aa953969c4cea2a248ff0f4258ac472ab050d526b45105c7e59c78c2adb0663 |
| rewrite-r2-identity-static-v2.json | 4886fe3e09ca6618da2784eef109727c561a5a2e83d6652b14333181ca183f6d |
