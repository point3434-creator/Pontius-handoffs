# Independent Tier C FIX review C — paired evaluation source opening r002

Issuer: Codex /root/evaluation_review_c. Date: 2026-09-07.
Review scope: all six frozen proposal paths, prospective design/source contract only.
Candidate: cb47f22c3bf140351564316344d6596a1a81d433.
Manifest SHA-256: bf109d6dee99f76f860c5e0eeefa0c18c3bdcf82844cd6279dc4b04ca6789025.
Base and sole parent: e043f81ecec3ac16128720b42c3312bb41a4ed67.
Tree: 09d9a3bce37071bab9e8679e9924221aba075dbf.
Ref: refs/heads/review/v0a-evaluation-opening/r002.

Required findings C/I/M: 0/0/0. Defect verdict: CLEAN.
Specification verdict: CLEAN for this source-opening proposal.
Engineering-quality verdict: CLEAN for this prospective design.
Design verdict: SOUND. Confidence: high in inspected contract/identity conclusions;
no claim of implemented or executable correctness.

No required material finding survives this review. The proposal remains inactive until
its exact separately authorized adoption. This review does not perform the proposal's
later status gates, authorize adoption, accept future source, or open a population.

## Independence and coverage procedure

I read the frozen handoff first, then governing CLAUDE.md and workflow/checklist,
relevant PROJECT evidence/publication rules, roadmap/architecture context, and all six
raw packet proposal files. I recorded the independent inventory before opening any
coverage or prior findings:

reviews/review-c-initial-inventory.md, SHA-256
507062843f6795b1d3987de0ebad4d653d0772a697cbba37bc9fa1f43da20274.

Only after that create-new record did I open coverage.md and the exact r001 review-a.md
linked there. I did not read any other reviewer report, author transcript, or coordinator
conversation. Accepted B source was inspected without importing or executing it.

The inventory covers authority/scope, population/order/reset, source/loader boundaries,
native lifetime, all deadline/publication phases, retention, versioned observations,
action/hand/session failure scopes, complete denominators, and finite proportionality.
The deferred claim covers the two corrected categories and their related missing/null/
conflicting/incomplete paths. It does not purport to cover all implementation behavior.
That is consistent with this documentation-only candidate. No missed material category
or unsupported claim of runtime closure was found.

## Prior required-finding disposition

A-I1 — CLOSED at prospective specification level.

Source-contract.md, Report extraction and honest denominators, now gives action_failures
its own exact output fields: hand_id, event_index, action_index, code, delivery_status,
sources and standing. The immutable B model permits nullable failure identity fields;
the contract preserves that uncertainty and does not merge unknown identities across
frames. The accepted host's WireConsumer.read/failure source confirms that v1 failed
an action event with null decision, while v2 may carry decision.failure_reason and a
matching event.failure. The contract correctly names those actual fields, coalesces
matching copies, and refuses conflicting identity/code/delivery/action/timing copies.

For the original delivery_rejected scenario, the new contract can express one observed
unverified action cause alongside child_failed at both hand and session scopes, with
no invented timing flag and no pair score. Missing/invalid failure rows add observation
deficiencies rather than zero cause counts; a later malformed row cannot erase the
preceding valid observed prefix. A complete result's empty action list is distinguished
from an incomplete prefix with no observed failures. The metric/source/unknown map,
design prose, Task 1 controls and ADR summary are consistent.

The named later controls cover the original scenario, null identity, missing/invalid
failure, truncated prefix, duplicate and conflicting copies, and independently reject
dropping, scope-folding or double-counting a cause. Those are required future controls,
not results claimed by this review.

A-I2 — CLOSED at prospective specification level.

Source-contract.md, Retained files and publication, now requires an exclusive pending
guard before either final file. Both result and completion must be written, flushed,
closed, reread, byte-compared, identity/source validated, and pass the final shared clock
check before publication commits. A parseable completion left after failed close or
late write remains blocked because every precommit failure retains the guard. Prepared
and result elapsed times explicitly describe earlier preparation, not the later check.

The public read_completed predicate requires absent guard, strict stable non-reparse
files and identities, exact result hash/size binding and an all-complete result. It
rechecks absence and identities after reading. Postcommit removal is explicitly one
empty-resource release, not retained-file cleanup. Delayed or ambiguous removal cannot
expose an unverified result: if the guard remains the reader refuses; if it was removed
the already verified result is consumable. A later CLI error cannot retroactively revoke
that commit. This is a coherent cooperative-writer contract and deliberately supplies
no visibility-by-deadline or power-loss durability promise.

The original late/failed completion scenarios, partial/interrupted completion, normal
success, and delayed/failed/ambiguous release have real-file/public-reader controls
specified in both contract and plan. Brief, design, ADR and STATUS reflect the same
commit-versus-visibility boundary. No marker timestamp or process exit substitutes for
verification. No residual remains from A-I2 in the proposal as written.

## Whole-candidate specification and engineering assessment

| Requirement/risk | Fresh evidence and conclusion |
| --- | --- |
| Fixed population and paired comparability | d/l/r enumeration fixes at most 96 pairs and 192 trials. The button depends on d, not r. Original physical cards remain fixed, six controlled seats cover all relative positions, opponent mapping is fixed within each pair, both arms share the saved one-hand input, and all stacks reset to 200. This prevents policy-dependent later-hand dropout. |
| Order and denominators | Alternation uses pair ordinal before outcomes. Pair delta direction is baseline minus blueprint. Complete arithmetic uses integer sums and rational planned-pair means. Any incomplete pair/trial nulls the global aggregate; no survivor-only comparison is authorized. The plan includes independent literal matrix and arithmetic expectations. |
| Public child contract | Accepted B session Schedule.derive confirms one-hand v1 input to table conversion. Baseline uses v2 session/host/event namespaces and blueprint v1. Child argv, source/input/blueprint identity and strategy are fixed. Accepted session play_hand retains applied actions, nested captures and propagated failures. |
| Source and loader boundary | Old closure is pinned to B; the two new tools bind to current committed raw bytes. Child manifest is explicitly distinguished from wrapper manifest and matches the accepted host.Source subset. Host imports are inert definitions; raw-loading Job does not require constructing Source/Table or importing pontius. Public children retain their own admission. |
| Action and timing observation | Host-applied bot actions own execution counts. V2 selection origin/reason and nth-action equality own fallback attribution; legacy choices remain distinct. Accepted model/provider codec and host timing validation support the named versioned fields. Flags deduplicate per hand/action; outer timeout supplies no action-clock observation. Missing attribution and failed prefixes remain explicit. |
| Native ownership and retention | Accepted host.Job supplies kill-on-close creation, assignment, resume, active query, termination and close-once semantics. The wrapper contract requires suspended containment before execution, immediate resource registration, parallel bounded captures, stopped descendants, retained unknowns and stop-before-later-units. Native effects remain required real-boundary controls; this source reading does not establish OS behavior. |
| Deadlines and final consumer | Total deadline starts before generation; full trial plus cleanup reserve must fit twice before launch. Startup/capture/validation and final commit verification are included. Cleanup and visibility release do not grant extra payload or success after a failed precommit deadline. Cooperative writer and OS blocking exclusions are explicit. |
| Permissions and finite controls | Exactly two new tools, three suites and one fixture; six individually pinned registration exceptions. Old game/provider/host/session/generator source remains unchanged. The 24-session ceiling, one zero-seed matrix, two literal deals, real non-poker fixtures, exact acceptance list and supported-interpreter sequence are explicit. |
| Adoption and project fit | ADR-0508 is inert before exact adoption. Source seal and real population invocation remain separate. ADR-0505/0506 preserve legacy/provider semantics; ADR-0507 and the independently checked disposition hash preserve the consumed demo. No strength, operating budget, C10 completion or training claim follows. |

Design judgment SOUND: one outer runner and one pure contract preserve the accepted
engine boundary and reuse native ownership. The new metric map and transition table
make previously implicit boundary decisions directly reviewable. A generic scheduler,
second poker engine, new provider or generalized authorization layer would add scope
without protecting these finite invariants, and none is proposed.

Advisory implementation consideration, not a required finding: exact raw schema copying,
resource handling and publication are substantial within 1,200 production lines. Keep
the explicit limits and stop/redesign rule. The largest unknown is whether the future
implementation can meet all real-boundary obligations within those limits. This is not
evidence that the proposed shape cannot fit. No extra framework or gate is requested.

## Independent identities and permitted checks

Absolute native Git C:/Program Files/Git/cmd/git.exe was used with command-local
safe.directory for the exact authoring repo. Final identity/hash operations used
--no-replace-objects and --no-optional-locks. No persistent Git configuration changed.
Read-only show/rev-parse/diff-tree --no-renames/cat-file/ls-tree and targeted source reads
completed successfully. .NET consumed raw Git stdout bytes, avoiding checkout newline
conversion. Whole digest-first ordinal-sorted LF rows independently reproduce the
manifest and equal its file hash; each packet source file equals its candidate blob.

| Frozen path | Raw SHA-256 |
| --- | --- |
| docs/decisions/ADR-0508-open-the-paired-local-evaluation-source-round.md | 0146fed86742507ca4e5951423e8525906ef5835942109e2045b07ab83e70b5c |
| docs/architecture/v0a-evaluation-r001/design.md | 123cec2828db89063405beeaa6b70f130364d054cdab01198577498b79b88e27 |
| STATUS.md | 4b61a197df59d91c09b4865bee9ac98b82ed28d93d112739e550d851529838d7 |
| docs/architecture/v0a-evaluation-r001/brief.md | 4d4279494c4c30326fe7149ff696aca6afe2b187dfb9aa3385d6387adcae87ca |
| docs/superpowers/plans/2026-09-07-paired-local-evaluation.md | 6c031b7b21ba0c40e13f73da0e7798d0435ddd5ab30e4ed2083e6e36d658552e |
| docs/architecture/v0a-evaluation-r001/source-contract.md | cfc1752bfbd3db2182abcd911c0acb9aac86fb73e315dff77957f572ab3101b4 |

All nine base blob IDs independently resolve and remain unchanged at candidate:

- tools/check_stabilization_boundaries.py: 9cc2ae8d8e82ccc77648ade4eb79ae9c34c88a9f.
- tools/generate_test_inventory.py: 2ac1413b0f89fa848f1ee5df0814b58dcbfa15b8.
- tests/test-inventory.json: c28445aa4b77a98cfd706672d955be4570b98a15.
- tests/test-profiles.toml: 4469bf813b2e97116667c206784a7bc212f6eef5.
- tests/test_inventory_and_profiles.py: e71a24322878361fb2feb44437d9210cff79c89e.
- .github/workflows/ci.yml: 3d873a2f75ff1b155bf3533583eddf971eb7790a.
- tools/v0a_seeded_deals.py: 2963004e38c6e66f76ae9ce3bd474063eee870fe.
- tools/v0a_table_session.py: a5e058260fa56e29f06e38074d59dc55f420c5ee.
- tools/v0a_table_host.py: 6ec8a162b053158203663c48e82314b10750f962.

Other independently reproduced raw SHA-256 values:

- coverage.md: 029259017cddf6335dcd5f1f5afc60c0bdcc1e92809877af91dff7fdd1d4a944.
- Authorized prior r001 review-a.md: eb673537d43549968246acca86cfc7cf0a20c1dbbbf85306c1fb329f40c95395.
- D:/Pontius/tmp/v0a-baseline-watch-run-r001/final-disposition.json:
  2f9d99f1aaca32252680a80b80e9b7a0ef1ad6d51b9482af0b42d849b1382c5f.

The candidate has exactly the six declared documentation changes against B. The
permitted prior-to-current diff shows the correction stays within observation and
publication contracts and their corresponding permissions/controls; no source surface
or scientific population is added.

## Limits and recommendation

Known: the frozen proposal expresses the required boundary outcomes and identities
above. Unverified: generated STATUS freshness via its mandated commands, future source,
native execution, finite fixture counts at source freeze, line-budget compliance of
unwritten tools, and actual operational adequacy. Those later gates remain required.
No tests, CLI help, generator or poker imports, inventory/census payload, benchmark,
card/seed generation, implementation, evaluation, decision commit or push ran here.
Only my create-new review records were written.

Cheapest falsifiers after adopted implementation are the finite delivery_rejected
reducer control and late/full-marker-close real publication control, plus the one
prescribed full paired matrix. Kill criterion: required invariants cannot fit the
permitted source/fixture/round budgets, or these real-boundary controls fail without a
within-scope correction. That calls for the existing stop/redesign process.

Recommendation: this reviewer finds the proposal CLEAN and SOUND. Continue with the
other required independent review and authorized proposal acceptance sequence. Preserve
r001 as NOT CLEAN; this report closes its required findings only for the exact r002
commit/manifest pair. Original report hash is recorded externally in my create-new
review-c-ledger.md to avoid an impossible self-hash dependency.
