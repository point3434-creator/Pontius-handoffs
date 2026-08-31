# R2 population v2 closure review v1

Reviewer: codex/mapping_compatibility, 2026-08-31. Bounded population-only engineering rereview; not a cold pass or runtime approval.

**Design verdict: SOUND. R2-I1 is closed; no surviving finding in this correction.**

Bound pair: H `2393d9b3680426f5a3169ddb19e7b542ce68531d`, parent `edaa1e6a41812b4a8f577a3c88072c8d71b932bb`, manifest `3ca45c9839ae6f7101d6405607260d766a18ed6ab260886c65a92bffb1a2471d`.

| Artifact | SHA256 |
| --- | --- |
| tests-checks/rewrite-r2-identity-population-v2.json | 8ab800c1361ca53f4f294bd32e308ecb7061e031b60d32dc74d7fdf52cc5ce3b |
| tests-checks/rewrite-r2-identity-population-v2-from-v1.diff | b11fe4ab0516b7e4eda3db8706b24e469b57accfa6f82f447944f7310e321588 |
| tests-checks/rewrite-r2-identity-population-v2-static-proof.json | 2e1137375263823cf82e3cbf158e9d2f2d1d812044ae745fdca0ce5677db9f1d |
| tests-checks/rewrite-r2-identity-population-v2-handoff.md | cdbeee9f1d0c4702377e2576f473649e28dc2e2b65df2eb3087274f2764fdfbd |

I independently read the six manifest-listed frozen blobs, reproduced their SHA256 values and sorted LF manifest, and verified matching local bytes. The two other manifest entries are previously issued reviews, checked for identity only.

The correction has exactly one semantic addition: `/envelopes/name_environment_public`. It equals the original `rewrite-early-population-v1.json` entry, canonical SHA256 `9c27bf22e70df68f996ef0d91b8763ef7e7467f148067be45aab500c92dc6b14`. Removing it and applying the unchanged JSON formatting reproduces every raw byte of population v1 (`30295f39daafcf265103cd78f3de50393c9111633ca3d5f8515e3f77c9a1197a`). Independently regenerated unified differences match the issued diff: 56 additions, zero deletions.

All twelve envelope references now resolve. All twelve case descriptors equal v1 exactly. Each of the eight original descriptors and its resolved envelope equals the original population; in particular, both hidden-cell cases retain their original name-environment envelope rather than being redirected to the identity Model(region) contract. The identity envelope and the original depth/storage envelopes remain unchanged.

The four identity case/source/Model pack, its coverage and source/Model difference artifact retain their previous frozen hashes. All eleven separately pinned original dependency files also match their retained raw hashes. The inverse comparison establishes that gates, order, classifications, witnesses, five caps, budget scope and all other population values are unchanged. No full prior case review was repeated.

Independent checks used actual CPython 3.11.15 with -I -S -B -P for JSON/hash/text comparison and absolute Git blob reads. No Model, builder, test, analyzer or candidate source was imported or executed. No existing artifact or production source was changed.

This closes only the missing-envelope finding in `rewrite-r2-inputs-engineering-review-v1.md` (`dc4dfc6537451c898116c03110743e7a1dd387c6e2a57b3f429a3e4f68e1dfaa`). Exact executable harness review and root authorization remain separate prerequisites; no runtime or source GO follows from this note.