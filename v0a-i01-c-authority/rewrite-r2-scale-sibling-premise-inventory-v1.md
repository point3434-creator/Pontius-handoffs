# Scale-family open-input premise inventory v1

Reviewer: codex/cold_review_a, engineering participant and original case/Model pack author. Static category completeness only; not a cold review, runtime failure report or case rewrite.

Finding: all sixteen unchanged scale-* records have the same missing open self.choice equality premise. The four selected for prospective R2 are a subset of that affected category. R2 does not silently correct or relabel the twelve remaining siblings.

## Inputs and method

- Case pack: tests-checks/name-environment-cases-v1.json, SHA256 d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c.
- Original finding: rewrite-r2-open-input-contract-review-v1.md, SHA256 9a1a01504297769e58cce8603a46f3072ed2cd3b2c24bd37dfb073faf543e917.
- Prospective proposal: rewrite-r2-identity-partition-premise-proposal-v1.md, SHA256 fea749f9ad5b6f567016030bbe38a0e9e3f6641eb9af98f5c9ae1607bd28b475.
- Completed proposal review: rewrite-r2-identity-partition-premise-review-v1.md, SHA256 ed38152d0fd03fb0acf15d87e52494b88d343f41c1d032d89322a0dbd09607f8.
- Frozen handoff containing proposal: H b1d15de062ac45c351f0254b358ee1e5fc35bdee; manifest beb50fab0fe159249de1397529b78a71e2b176b8e3643ea64ccb37dbf1a1c15a.

Own stdlib-only AST inspection under actual Python3.11.15 -I -S -B -P enumerated every record whose ID starts scale-. It checked exactly sixteen records, each still classified clean. Each self.choice load in test_static is the left operand of an equality comparison against the expected integer literal: one comparison against0 for S2, three against0/1/2 for S4. There are eight records of each successor count, totaling32 such comparison sites.

No source contains a choice attribute store/delete, class-scope choice assignment, or an initializer/attribute-access/setup hook supplying a fact. The original common public envelope supplies source, inventory and item universe, not the witness choice value/type. Separate witness records use exact integers0 through S-1; their finite harmless Model projections do not establish a universal inert-equality/truth premise for the public analysis.

The following hashes cover exact decoded source strings encoded as UTF-8, without normalization. Lines refer to those decoded strings, not JSON physical lines.

## Exact affected records

| ID | JSON pointer | Comparison lines | Source SHA256 | Prospective disposition |
| --- | --- | --- | --- | --- |
| scale-n8-s2-d0-normal | /cases/0 | 17 | f639be320be70e99d1bcbb0010d76b906e31aef214241a98074caba8c8e59f8a | Later sibling obligation |
| scale-n8-s2-d0-exceptional | /cases/1 | 18 | b27ba3a8d231a5f5528f60fd9fd432c5bd2ff51e5fec7e9726d633d7949441ce | Later sibling obligation |
| scale-n8-s2-d2-normal | /cases/2 | 17 | 7c64c6fa77a570ab7ddc52dae8c52344af86773d541d0baf68f2db48e1c44f1d | Later sibling obligation |
| scale-n8-s2-d2-exceptional | /cases/3 | 18 | 64dc0cb6fa9053a9131634118140d5dc653e7373d9c5522877c3834d1d84756c | Later sibling obligation |
| scale-n8-s4-d0-normal | /cases/4 | 17, 19, 21 | 7a496280160092f1389045b0d640f9871f4080b1807db988d04725730fa8b1c7 | Selected R2 four |
| scale-n8-s4-d0-exceptional | /cases/5 | 18, 21, 24 | a064e3d40cd5bd26b8b94c58a149d6c231b65be187b0c3314e8df4d1bfdca633 | Later sibling obligation |
| scale-n8-s4-d2-normal | /cases/6 | 17, 20, 23 | 5728190cb6433c9fdc3709e00a8a26ec0a61d164322673ebaedf57e82d7d9966 | Later sibling obligation |
| scale-n8-s4-d2-exceptional | /cases/7 | 18, 22, 26 | 0e22e6aa9144d52d49c0c9a1a398b4fec9d7213b03e64b3af39278b92e3a2303 | Selected R2 four |
| scale-n64-s2-d0-normal | /cases/8 | 73 | a5323fd56ee878a973528e7e2101b8766bd537886c67bf25993d6c952fc003e6 | Later sibling obligation |
| scale-n64-s2-d0-exceptional | /cases/9 | 74 | 348d4bd76cb4456350ed0448de59f22c7f392fef3b15323cfaf2a3232970de76 | Later sibling obligation |
| scale-n64-s2-d2-normal | /cases/10 | 73 | c8a1efd2b42f75ab9511baf93f7ceb975d42ab84d3da940c02a846170e9f049d | Later sibling obligation |
| scale-n64-s2-d2-exceptional | /cases/11 | 74 | 1b8609b76d6dfa7882cb2223c45ed6de4da79ae7b808ccb673c3d2f42e0c2b7e | Later sibling obligation |
| scale-n64-s4-d0-normal | /cases/12 | 73, 75, 77 | 8cd92fb80500595801e3948c1cb9a7ac825334457139b70933307714ad09fe10 | Selected R2 four |
| scale-n64-s4-d0-exceptional | /cases/13 | 74, 77, 80 | bfffa30bbd845db1497344f2a7a3cb108c43e362f8da49851175a55e27441550 | Later sibling obligation |
| scale-n64-s4-d2-normal | /cases/14 | 73, 76, 79 | 1486585429cc676b5e3049e216a28ac9d66610d6b22704b24b7eae96fe413d41 | Later sibling obligation |
| scale-n64-s4-d2-exceptional | /cases/15 | 74, 78, 82 | a67c06db53e8804496c85cf9437e5fbfa9c68a235e27e0af69b454713167b33d | Selected R2 four |

## Scope disposition

Only scale-n8-s4-d0-normal, scale-n64-s4-d0-normal, scale-n8-s4-d2-exceptional and scale-n64-s4-d2-exceptional are selected for the separately frozen R2 identity-partition successor proposal. The other twelve affected scale records remain explicit later benchmark-premise correction obligations. Neither the proposal nor this inventory repairs their inputs, changes their clean labels, approves their use as an unresolved-input clean gate, or authorizes extra runtime work.

All sixteen original source/Model/expectation/result records remain immutable. Future sibling corrections need their own explicit old-to-new mapping and frozen evidence rather than quiet fixture replacement or a weakened analyzer rule. Strict refusal of unproved protocol effects remains preferable to an implicit scalar assumption.

No candidate, sensitive source, Model, test or owner was executed. No case, Model, expected result, harness, source, ledger or existing artifact was edited. This check adds category/protocol metadata only; it is not extra Gate A testing.
