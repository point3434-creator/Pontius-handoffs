# R2 population v2: add-only envelope correction

Standing: authoring handoff for static rereview and freeze, not runtime approval. I authored the predecessor inputs; this is not an independent cold review.

Authorization: H edaa1e6a41812b4a8f577a3c88072c8d71b932bb; rewrite-r2-design-and-input-review-v1-manifest.sha256 e995f1683ec844d7a9149f8e936a156482ad98d34b046a3e3c4b9863be85a9df; rewrite-r2-input-closure-finding-v1.md dbaad79b2127ac8abcf93ec376ec06148d2f3a6c3259a012c986e65aac292d3f.

Exactly one semantic addition was made: /envelopes/name_environment_public is copied from the unchanged original rewrite-early-population-v1.json (3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce). Its canonical descriptor hash is 9c27bf22e70df68f996ef0d91b8763ef7e7467f148067be45aab500c92dc6b14. The new identity_name_environment_public entry remains unchanged. Hidden-cell references are not redirected.

Issued create-only files:
- rewrite-r2-identity-population-v2.json: 8ab800c1361ca53f4f294bd32e308ecb7061e031b60d32dc74d7fdf52cc5ce3b (60878 bytes).
- rewrite-r2-identity-population-v2-from-v1.diff: b11fe4ab0516b7e4eda3db8706b24e469b57accfa6f82f447944f7310e321588 (2833 bytes; one hunk, 56 added lines, zero deletions).
- rewrite-r2-identity-population-v2-static-proof.json: 2e1137375263823cf82e3cbf158e9d2f2d1d812044ae745fdca0ce5677db9f1d (11962 bytes).

The authorizing manifest, finding, predecessor population and original early population were independently read through absolute validated Git at the authorization commit and compared byte-for-byte with local files before authoring. Source/case/Model strings were not evaluated.

Static result: all twelve case envelope references resolve. All twelve case descriptors are identical to v1. The eight original descriptors and their resolved envelopes equal the original population exactly under canonical serialization; this includes both hidden-cell cases, the two depth cases and four composition cases. Removing the added entry and applying the unchanged JSON formatting reproduces every byte of population v1.

All previous keys and values are preserved, including format schema and initial authoring provenance; this separate handoff supplies correction provenance. Gate A remains six analyses/eight Model projections; the complete successor population remains twelve analyses/twenty-four projections with two depth assertions. Caps, order, requirements, classifications, four new identity cases, source/Model differences, witnesses, coverage and all older packs remain unchanged.

Population v1 remains an issued predecessor with its known unresolved-reference defect. Do not repair it in place or infer runtime evidence from this successor. Controllers must pin the new population SHA after root freeze/rereview; this handoff does not authorize harness/source authoring or execution. The held candidate and existing harnesses were not read or changed by this correction.

All protected inputs were rehashed after the new files were written. No Model, analyzer, sensitive fixture, test, harness or candidate payload was imported or executed. No production/source/test/generated/ledger files were changed. Authoring is complete and stopped.
