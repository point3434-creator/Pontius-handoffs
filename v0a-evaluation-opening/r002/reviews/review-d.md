# Independent adversarial Tier C review D - paired evaluation opening r002

Issuer: Codex /root/evaluation_review_d. Date: 2026-09-07. Round kind: FIX.
Review scope: complete frozen six-path prospective design/source-opening proposal.
Candidate: cb47f22c3bf140351564316344d6596a1a81d433
Manifest SHA-256: bf109d6dee99f76f860c5e0eeefa0c18c3bdcf82844cd6279dc4b04ca6789025
Base: e043f81ecec3ac16128720b42c3312bb41a4ed67
Tree: 09d9a3bce37071bab9e8679e9924221aba075dbf
Ref: refs/heads/review/v0a-evaluation-opening/r002

**Required C/I/M findings: 0/0/0. Defect verdict: CLEAN.**
**Specification: CLEAN at prospective contract scope. Engineering: CLEAN at design scope.**
**Design verdict: SOUND.** Confidence: high for documentary identity/closure;
implementation correctness is unverified because this candidate contains no evaluator.

No required correction survives this review. This is not source acceptance, adoption,
a test result, launch permission, a playing-strength finding or a hard-wall guarantee.

## Independence and exact evidence

Before opening the deferred claim or prior findings, I read the complete six frozen
files and recorded my own population, authority, source, native lifetime, deadline,
publication, schema/unknown, finite-control and registration inventory in
review-d-initial-inventory.md, SHA-256:
9f5c69e51d158af63795408c4d77d686df7fb41ac030f98efc14e21bbb833def.
I did not read other current reviewers' files or coordinator/author conversations.
Only the prior required-finding report explicitly allowed by coverage.md was read.

Read-only native Git rev-parse/show/diff-tree --no-renames/cat-file analysis used
C:/Program Files/Git/cmd/git.exe and command-local safe.directory for the exact
authoring repository. Final recomputation also used --no-replace-objects and
--no-optional-locks. Raw stdout byte streams went directly to .NET SHA-256; no
checkout line-ending conversion was used. Ref, candidate, sole parent and tree match.
The six changed paths are exactly STATUS.md, brief.md, design.md, source-contract.md,
ADR-0508 and the implementation plan. Whole digest-first rows reproduce the manifest
above and are byte-identical to packet manifest.sha256. All six blobs are LF-only,
BOM-free and without trailing whitespace. No source, tool, test, CI or governing-rule
bytes differ from B.

All nine B blob pins reproduced:

| B path | Blob |
| --- | --- |
| tools/check_stabilization_boundaries.py | 9cc2ae8d8e82ccc77648ade4eb79ae9c34c88a9f |
| tools/generate_test_inventory.py | 2ac1413b0f89fa848f1ee5df0814b58dcbfa15b8 |
| tests/test-inventory.json | c28445aa4b77a98cfd706672d955be4570b98a15 |
| tests/test-profiles.toml | 4469bf813b2e97116667c206784a7bc212f6eef5 |
| tests/test_inventory_and_profiles.py | e71a24322878361fb2feb44437d9210cff79c89e |
| .github/workflows/ci.yml | 3d873a2f75ff1b155bf3533583eddf971eb7790a |
| tools/v0a_seeded_deals.py | 2963004e38c6e66f76ae9ce3bd474063eee870fe |
| tools/v0a_table_session.py | a5e058260fa56e29f06e38074d59dc55f420c5ee |
| tools/v0a_table_host.py | 6ec8a162b053158203663c48e82314b10750f962 |

Independently reproduced external raw SHA-256 records:

- Prior disposition: 2f9d99f1aaca32252680a80b80e9b7a0ef1ad6d51b9482af0b42d849b1382c5f.
- Deferred coverage: 029259017cddf6335dcd5f1f5afc60c0bdcc1e92809877af91dff7fdd1d4a944.
- Permitted r001 review A: eb673537d43549968246acca86cfc7cf0a20c1dbbbf85306c1fb329f40c95395.

## Independent contract assessment

| Requirement/risk | Primary evidence and result |
| --- | --- |
| Fixed reset pairs and denominator | Contract Public request and matrix plus B generator deal_for_hand and session Schedule: physical deal stays fixed, button depends on d only, all six seats rotate, lineups preserve clockwise order, 200 stacks reset. Arm order is predetermined. Null pair/global scores and explicit unstarted rows prevent survivor aggregation. Pass as design. |
| Closed source and module boundary | Contract Admission plus B host.Source and session.Admission: unchanged full B closure, new tools bound to current raw HEAD, fixed captured-byte loaders, distinct wrapper/child manifests, no parent game import, clean public child process. Session host pin and namespace lengths are compatible. Pass as contract. |
| Native lifetime and unknowns | B host.Job supports suspended assignment, resume, active-process accounting, termination and close-once behavior. Proposal registers ownership before fallible work, caps both streams, stops on first failed/unknown trial, and distinguishes intent-only unknown launch from unstarted work. Real descendant controls are required. Pass as design, not runtime proof. |
| Shared deadline and publication | Total deadline starts before cards/planning, complete trial plus reserve must fit twice before launch, and validation/publication share it. Guard precedes both files; both close/readback checks and source verification precede final clock commitment. Only committed guard release is later. Precommit failures remain unconsumable. Pass as contract. |
| Honest metric authority | B host.WireConsumer, v0a model/trace and provider codec support the copied v1/v2 schemas, applied bot ordinal matching, selection-origin distinctions and nullable failure fields. Child_failed propagation cannot replace action observation. Timing/outer timeout and missing/zero distinctions are explicit. Pass as contract. |
| Exact scope and finite controls | Six pinned registration exceptions preserve old engine/admission/analyzer contracts. Two tools, three suites, literal fixtures, named commands, <=24 new-suite session starts and independent literal oracles are bounded. Native faults keep real resource/publication paths. Pass as prospective permission. |
| Separate authority | Brief/ADR/STATUS/plan consistently require exact adoption before source implementation, later source seal, and separate population preregistration/launch authorization. Consumed prior demo is not reopened. Pass. |

Relevant unchanged dependencies were inspected from B, including generator recipe,
host Source/Job/WireConsumer, session Admission/Schedule/report propagation, v0a
FailureRecord and trace declarations, provider codec validation, boundary origin/import
registration, inventory registration/census expectations, profiles and CI. Applicable
CLAUDE/workflow/checklist, PROJECT evidence/publication rules and architecture boundaries
were applied. Static inspection of these records did not execute their payloads.

## Deferred coverage comparison and required-finding closure

My independent inventory includes both correction categories plus pairing/order,
source drift, launch/cleanup unknowns, permissions and finite controls. The deferred
claim's discovery follows the relevant public failure propagation and publication
paths. It describes prospective cases and exclusions honestly; it does not mislabel
unrun cases as exercised runtime evidence. No omitted material category was found.

A-I1 is closed at proposal scope. source-contract.md Report extraction now provides
an exact action_failures channel and source/standing rules. The concrete
no-timing delivery_rejected case retains one unverified action cause and both scoped
child_failed causes with no score. V2 decision.failure_reason maps to the actual codec;
v1 failed events do not invent a decision object. Fully identified duplicates coalesce,
null identities are not merged across frames, contradictions refuse, and absent or
invalid observations cannot become complete zero counts. Required later controls
include missing/invalid/truncated rows and drop/scope-fold/double-count counterexamples.

A-I2 is closed at proposal scope. source-contract.md Retained files and publication
now requires an existing guard during real result and completion write/flush/close/
readback, identity/source validation and the final deadline check. A complete-looking
marker after failed close or late write is blocked. Removal occurs once, only after
commit; a remaining guard refuses and ambiguous removal can expose only committed
bytes. The public reader rechecks absence and file identities. The other five paths
align with the narrow ephemeral removal permission and explicitly separate timely
verification from postcommit visibility. Real delayed-close/full-bytes failure and
postcommit release controls are required. No additional unchecked success marker or
precomputed timestamp is offered as proof.

The original r001 verdict remains unchanged; this new verdict binds only r002.
No runtime RED/GREEN closure is claimed or available at this documentation stage.

## Design judgment, uncertainty and recommendation

SOUND: one pure observer/planner and one outer owner preserve the accepted public
session/game boundary and avoid duplicating a poker engine or native Job implementation.
The metric authority map and explicit publication transitions make the two previously
missing contracts reviewable. Their repair does not require another runner, transport
framework or widening the six source exceptions.

Advisory implementation caution: duplicated exact v1/v2 schema validation and native
failure handling are substantial under the 1,200-line production ceiling. Budget fit
and real resource effects remain the largest unknown. Keep the existing map/transition
table authoritative and return for the already-required scope ruling if implementation
cannot fit; do not simplify away unknown states or extend the analyzer. This is not a
new gate or a required design correction.

Cheapest falsifying checks after adoption are the literal matrix/denominator controls,
non-timing action failure with duplicate/null/malformed variants, and real completion
close/readback failure at the deadline followed by read_completed. Kill criterion is
failure to preserve these contracts inside the authorized scope/budget, requiring the
existing redesign/reauthorization procedure.

Recommendation: this review permits progressing to the proposal's existing metadata
acceptance gates, subject to the other independent Tier C verdict. Exact controller
adoption remains required. No tests, CLI help, generator/poker imports, entropy,
card generation, evaluation, benchmark, inventory/census execution, implementation,
Git mutation or retained-artifact cleanup occurred in this review. Only my create-new
review records were written. Their report/ledger hashes are issued separately so these
original records need not contain impossible self-referential hashes.
