# Prospective Gate B identity-partition premise review v1

Reviewer: codex/cold_review_a, engineering participant and author of the original name-environment source/Model pack. This is a design review, not a cold review or runtime acceptance.

Design verdict: recommend adoption for a separately frozen prospective Gate B round, with the precise conditions below. No architectural blocker was found in the proposed source-level identity partition. This review does not authorize Gate B execution.

## Frozen inputs and existing evidence

- H commit: b1d15de062ac45c351f0254b358ee1e5fc35bdee.
- Manifest: rewrite-r1-task5-source-v2-manifest.sha256, SHA256 beb50fab0fe159249de1397529b78a71e2b176b8e3643ea64ccb37dbf1a1c15a.
- Proposal: rewrite-r2-identity-partition-premise-proposal-v1.md, SHA256 fea749f9ad5b6f567016030bbe38a0e9e3f6641eb9af98f5c9ae1607bd28b475.
- Original premise finding: rewrite-r2-open-input-contract-review-v1.md, SHA256 9a1a01504297769e58cce8603a46f3072ed2cd3b2c24bd37dfb073faf543e917.
- Original case pack: tests-checks/name-environment-cases-v1.json, SHA256 d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c.
- Original early population: rewrite-early-population-v1.json, SHA256 3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce.

The completed read-only inspection verified the proposal's local hash and its inclusion in the independently verified H manifest/blob pair. Own stdlib AST inspection of the four original scale records verified that N8/N64 branch trees and common return calls match within each normal/exceptional family. Each original source has three open choice loads and no choice store. Original labels, Models and results remain unchanged.

No candidate, sensitive fixture or Model was executed. No new fixture, Model, expectation, harness, public API or candidate source was authored. This artifact records the completed assessment; it introduces no further analysis.

## Exact prospective mapping and placement

Apply this mapping to both ambient sizes:

| Original region | New identity region | D0 work pair | D2 work pair | D2 exception |
| --- | --- | --- | --- | --- |
| choice 0 / branch:0 | selector is True | (0,0) | (1,-1) | ValueError |
| choice 1 / branch:1 | selector is False | (0,0) | (2,-2) | TypeError |
| choice 2 / branch:2 | selector is None | (0,0) | (3,-3) | KeyError |
| choice 3 / branch:3 | else; Model uses a fresh plain object | (0,0) | (4,-4) | IndexError |

Latch the open selector once after the existing ambient and work0/work1 initialization. In the normal family, put the latch immediately before the identity ladder. In the exceptional family, put it inside the original try, before that ladder. Preserve each branch body, original handled-exception tuple, common launch and event ordering. Record the one extra fixed local and lookup cost at both N sizes; do not subtract it or describe the new source as byte-compatible.

The new Model discriminants must distinguish True, False and None from integers and serialized tags. One newly created plain object witnesses the fourth region. Preserve original branch/raise/handled/sink traces, ambient values and work pairs under the table above.

## Proof boundary

Identity comparison itself returns an exact builtin bool without invoking the selector object's equality or truth protocol. The unknown selector need not be an inert scalar. All three predicates refer to one latched value; the ladder partitions it into four exhaustive, disjoint regions. The independent Models witness those regions, while the source operation and branch structure supply the general partition argument. Four harmless Models alone still do not supply an analyzer input-domain premise.

The initial open receiver lookup remains a separate admitted contract. The fixed source and canonical entry must retain ordinary open lookup; known descriptors, custom attribute hooks or effectful lookup must still be accounted for or refused. The identity operation does not prove its operand evaluation harmless.

R2 must distinguish a proved-builtin-boolean result with unknown value from a generic unknown value. Producer proof comes from the supported identity operation after operand effects complete, not a fixture ID, field name, reason string or silent scalar assumption. More general predicate correlation may remain conservative; this proposal does not require a general constraint solver.

## Mechanism, cost and evidence conditions

Use one unresolved public analysis for each new scale source. Four constant-specialized calls do not satisfy the experiment. Evidence must show the three decisions on their false-prefix paths, four feasible alternatives and the actual joins. D2 must additionally show the matching distinct work pairs and abrupt-to-handled successors. Observers must record actual events without retaining budgets/values, introducing semantic reads or manufacturing counts.

Four branch alternatives are not four sequential subprocess executions. Each concrete execution still reaches the common sink once; public occurrence accounting must preserve that distinction.

A sound D0 optimization may avoid materializing four identical states. Such behavior can be product-correct while leaving this particular four-state cost experiment's mechanism unmet. Report that outcome honestly rather than forcing redundant work or inferring execution from source syntax.

The engineering continuation criterion is at most 196608 actual requested work units in EVERY original budget epoch. This leaves 65536 units of headroom under the unchanged 262144 production cap; 196608 is the maximum, not the amount of remaining headroom. Include preparation, forks/copies, joins, terminal work and actual requests through final refusal. Invent no charge where a depth check raises without consume. Do not reset, split or refund budgets or tune the threshold after results. All original caps, exact-depth assertions and floor-before-development custody remain binding.

Freeze new source/Model/expectation/observer records with explicit old-to-new mapping and separate hashes before candidate support or execution. The original four records and all prior evidence remain immutable. Keeping twelve cases/twenty-four Model projections does not make the prospective round the old round. Gate A results do not approve Gate B or prove this branch/join mechanism.
