Issuer: /root/cold_review_r3_b

NOT CLEAN — one Important finding survives. Confidence: high.

**[P2] The workflow-amendment link breaks when copied into generated STATUS.**  
Candidate locations: `STATUS.md:27` and its source, `docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md:36`.

The ADR uses `../workflow-amendment-2026-08-30.md`. The unchanged status generator copies its Decision section verbatim (`src/pontius/status_generation.py:362–366`), so the generated root-level STATUS resolves that link outside the repository.

Concrete scenario: in a fresh snapshot rooted at `D:/disposable-v0a-candidate`, clicking the link resolves to `D:/workflow-amendment-2026-08-30.md`; the frozen amendment actually resides at `D:/disposable-v0a-candidate/docs/workflow-amendment-2026-08-30.md`. The existing `test_maintained_local_markdown_links_resolve` includes STATUS and rejects this missing destination (`tests/test_documentation_integrity.py:12–15,33–44`). This introduces a documentation-integrity gate failure and breaks the front-door reference to the prospective rules.

Minimal direction: use a location-independent plain repository path in the ADR’s copied Decision section, retain any clickable relative link outside that section, and regenerate STATUS through the authorized generator. No sealed generator change is needed.

Identity independently verified:

- Commit: `953b8703ef93fe261a6857b57bca196b2b8ded9b`
- Parent: `ca0b2e41bbf5d9fc1649de20379299331de6591a`
- Manifest: `f5e5d7a3071518e139e8bdffdbe0f813a510ae80c477fdd9a88fb537be4d6fff`
- Exactly the three declared changed paths.
- Original workflow digest and the declared brief/baseline blob identities match.

Full changed-blob SHA-256 rows:

```text
6365d6fc153278741a71e0e81c5e93e5d60f40a0bf079985b51d45564ead86fd  STATUS.md
894af7522303529f3ca11db43225889d5d5d37e2ef2bdf379f6a6dc7c039f23b  docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md
c0fcc666ae44113e05e2aee410cdaf0ad1136bfc2101a07be7f96dc2b34ac63c  docs/workflow-amendment-2026-08-30.md
```

No additional material specification finding survived review of privacy, blueprint outcomes, event/replay semantics, public-ledger accounting, publication failures, authority limits, and public-API feasibility.

This is static specification evidence only. No runtime, test, owner, or generator was executed; no files were edited. Specific ceremonial-commit authorization remains absent.
