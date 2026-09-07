# Independent whole-source Tier C review A

Reviewer: Codex, /root/evaluation_source_review_a. Issued 2026-09-07.
Round: v0a-evaluation-source/r001, NEW-SURFACE.

**CLEAN. Specification PASS. Engineering PASS. Design SOUND.**

No required correction remains on the reviewed source increment. These are source-review verdicts, not a declaration that Stage 5 acceptance, source sealing, or any evaluation invocation has occurred. The exact sixteen-command, two-interpreter acceptance sequence remains pending as the handoff states.

## Identity and independence

- Candidate: bca326c6bfedd71324a19c809f617e267cc9e0a2.
- Ref: refs/heads/review/v0a-evaluation-source/r001.
- Parent/base: 34616938c708b1ca306b9d8a17b9d98e2f9e451f.
- Tree: 5eec124adf1de52da1e36c50848c5d55f8866b75.
- Whole-row manifest SHA-256: 02f06a3ae8a7cefb5ba8f5a5abaf94f2a91a661a1d5f1ade3e1b3f8c4ae02860.
- Initial independent inventory: reviews/initial-a.md, SHA-256 87ddcbc98cbd168f4c0a6f648c4c0aae52f3e5042f2a420494c64dcad7d7e7aa.

I read handoff.md first. I recorded the census/assertion and registration expectations before opening the authored census explanations, source-audit.json or focused-evidence.json. I did not read implementation reports, transcripts, coordinator rationale, checkpoint reviews, or another current review. I used CLAUDE.md, workflow.md, adopted ADR-0508 and the brief/design/source-contract. The handoff's controller ruling increasing production allowance to 1250 lines was applied.

I independently resolved the native Git ref, commit, parent and tree. For each of the twelve manifest paths, I compared packet bytes against the named native Git blob and recomputed its SHA-256. The manifest's exact raw bytes equal the lexicographically sorted whole rows with two spaces and LF; its own digest matches the identity above. The native commit diff contains exactly the twelve permitted source paths. Inherited host, session and seeded-dealer blobs retain their specified B identities, including the session's literal host pin. No src/pontius or other inherited source changes occur.

## Required findings

None. No Critical, Important, or other required defect was established after inspecting the complete source surface, the controls and independent oracles, source bindings, and retained raw census/receipt evidence.

## Requirement and evidence assessment

| Brief criterion | Reviewed behavior and evidence | Source-review result |
| --- | --- | --- |
| 1. Canonical request fixes the ordered matrix before play | decode_request rejects unknown/duplicate keys, noncanonical bytes, bool integers, float/nonfinite values, excess depth/size, bad domains, repeated lineups and insufficient reserve. build_matrix fixes d/l/r order and alternating arms. Contract controls exercise literal order, all limits and malformed requests; execute saves all pair inputs and plan before run_trial. | PASS |
| 2. Reuse accepted deal recipe and opponent scripts unchanged | Exact inherited blobs and source closure are preserved. The sole dealer call is the admitted dealer.deal_for_hand(seed,d). The allowed opponent names match the four adopted scripts. Only the public session is launched; the wrapper creates no policy or poker engine. | PASS |
| 3. Identical pairs, all six relative positions, fresh stacks | build_matrix retains physical cards and one fixed button per deal, rotates controlled seats and assigns relative lineup members, resets six stacks to 200, and gives both arms the same saved input/hash. Literal matrix controls check seats [2,3,4,5,0,1], fixed button, lineup placement, deal blocks and bounds. The real 12-session matrix checks actual retained inputs, stacks and strategy order. | PASS |
| 4. Public admission/engine/provider/fallback/clock remain authoritative | admit_source verifies current candidate bytes plus inherited B blobs before fixed raw loading. Three private aliases load captured buffers only; parent use is confined to pure contract, dealer.deal_for_hand and host.Job. The child vector uses the unchanged session CLI with -B -P, exact cwd/src and sanitized environment. Static loader variants and real source/identity/poison-environment controls support this bounded boundary. | PASS |
| 5. Create-only reservation, intent and raw failure retention | Root/file collisions preserve prior owners. Request, plan, pair inputs and per-trial records use retained create-only paths; intent precedes process creation. Unknown launch and cleanup outcomes remain explicit. Failed units stop all later units, which remain present as unstarted rows. The two real successful-session retention controls prove later capture/result-retention failure clears scoring without rewriting the completed unit record or continuing. | PASS |
| 6. Honest observations, scopes and denominators | observe_trial strictly dispatches v1/v2 reports and frames, binds identities and table-conversion digest, checks settlement and host-applied action ordinals, and separates selection from application. Failed prefixes retain unverified action causes separately from hand/session causes, timing flags deduplicate by action, and null identities do not acquire fictitious attribution. reduce_trials requires complete planned pairs and returns no survivor aggregate. Literal arithmetic expects [3,-5] pair deltas and a -2/2 mean; real matrix arithmetic derives from retained host stacks. | PASS |
| 7. Native containment, capture caps, one deadline and publication commit | run_trial creates the process suspended, assigns the accepted kill-on-close Job before resume, drains both streams with exact byte caps, terminates and waits for inactive descendants, and refuses cleanup ambiguity. It checks full trial plus 5000 ms reserve before admission and again immediately before creation. publish keeps its guard through closed/read-back result and completion verification, saved-file/source revalidation and final shared-deadline check; only then is one guard removal attempted. The reader rechecks guard absence and stable identities. Native marker/handle and real file-operation controls exercise these behaviors. | PASS |
| 8. Finite independent correctness controls and supported-interpreter gate | The fixture contains one distinct literal full deal, synthetic schema examples and literal requests, 20335 bytes. Contract and boundary suites start zero poker sessions. Runner source contains one 12-session all-zero-seed public matrix plus two real single-session retention controls: 14 starts, below 24. Named negative mutants test matrix, denominator, action-cause, assignment and final-clock oracle sensitivity. Verified focused receipts show actual 3.11.15 success; the subsequent actual 3.11.15 then 3.14.6 integrated acceptance remains a required later gate. | PASS for source-review stage |

## Real operations and oracle assessment

The native controls do not claim engine success from fake child reports. Their finite Python children run through the actual run_trial/Popen/Job path and deliberately produce malformed bytes, cap overflow, timeout, interruption or retained-file drift. Descendant controls open a real native process handle after observing the child's PID, release the trigger gate, and verify the retained handle no longer reports STILL_ACTIVE. The assignment-negative control makes the executable marker appear when assignment is deliberately bypassed, demonstrating that the independent marker oracle notices the incorrect boundary.

Publication tests use explicitly synthetic result records at the isolated publication seam. Their arithmetic is literal: baseline 56, blueprint 32, delta 24, denominator 6. The file wrappers operate on real exclusive files: short/partial writes retain actual bytes, flush/fsync occur, close occurs before the controlled close fault or lateness, and readback corruption is real. Precommit tests assert both retained guard and read_completed refusal, including a parseable completion marker after full bytes. Exact final clock 100 succeeds and 101 refuses. Postcommit tests separately exercise delayed removal, refusal while the guard remains, and real removal followed by an ambiguous error/interruption; the latter remains consumable. There is exactly one attempted release and no restoration or retry. The missing-final-clock mutant becomes consumable and breaks the independent refusal assertion.

The contract tests independently distinguish delivery_rejected from propagated child_failed at both outer scopes, assert one action cause with no timing flags, preserve allowed null identity, reject conflicting decision/failure copies and malformed tails, and preserve prior observations across later conflicts. Selected provider/fallback records do not become host-applied actions merely by existing. Missing attribution remains explicit. Failed or incomplete rows cannot produce net chips or a global aggregate. The literal report examples are schema/reducer fixtures, not a legal-poker oracle; legality and actual settlement remain the unchanged host's authority and the real matrix supplies the public integration check.

## Entire registration and census preservation

Reviewed manual registrations: .github/workflows/ci.yml, tools/check_stabilization_boundaries.py, tools/generate_test_inventory.py and tests/test_inventory_and_profiles.py. Reviewed generated artifacts: tests/test-inventory.json and tests/test-profiles.toml. Together with both new tools, all three suites and controls.json these are all twelve paths.

The manual delta is 138 added/removed lines. The generator's 299 top-level function/class ASTs are unchanged; its only source change is the three exact suite registrations. Existing CI gates remain, with three explicit new CPU steps. The boundary checker adds only the two origins, evaluation-specific import/loader policy and its invocation. The policy's checks are bounded structural controls, not a general dynamic-import soundness proof.

I compared generated records independently of source-audit.json. All 3041 old inventory entries retain exact parsed contents and original ordering. All 440 old payload records retain exact contents and ordering. The sole profile membership delta adds current:test_v0a_evaluation_boundary, current:test_v0a_evaluation_contract and current:test_v0a_evaluation_runner; all old profile members retain their ordering. There are 71 new test IDs, matching static class/method enumeration: 19 boundary, 24 contract, 28 runner. The stabilization list adds only the three paths. Both installed capability hashes remain 64 zeros; no capability tables/grants were installed. Baseline discovery, historical cases, interpreter slots, overlay records and existing profile budgets are preserved.

For each of census-post1-test and census-post1-production I hashed all four raw inputs, verified analyzer/inventory/profile hashes against their named Git sources, and compared the entire paired interpreter documents after removing only the interpreter string. The baseline and candidate 3.11/3.14 documents each agree. Captures bind candidate snapshot 6f59993ba2e5229e2d8ffdbb8de4187b576450b4; native Git diff against this review candidate is empty, so the distinct commit is explicitly accounted for rather than treated as the same identity.

I derived an independent equal-line mapping from the native base census test and candidate bytes, then compared every old ordered row, including duplicate occurrences, rather than comparing sets or trusting comparison digests. Both complete populations preserve:

| Collection | Old rows | Candidate rows | Added |
| --- | ---: | ---: | ---: |
| Expanded permissions | 141 | 141 | 0 |
| Unresolved blockers | 678 | 693 | 15 |
| Analyzed sites | 407 | 413 | 6 |
| Helper edges/closure rows | 4329 | 4475 | 146 |
| Decoys with provenance | 592 | 593 | 1 |
| Exact item universe | 3073 | 3145 | 72 |
| Deny-all membership | 2982 | 3054 | 72 |

All 312 additions per comparison have independently recomputed row hashes and exact candidate source line/hash bindings. Initiating definitions/calls were checked where present. Six new direct subprocess sites correspond to the explicit runner/CLI/source-clone test calls; six capture_output blockers match those sites. Six mixed-receiver and three namespace-mutation occurrences arise from three NativeIdentityTests traversing their setup/disposable helpers, preserving occurrence multiplicity. The new decoy is the literal descendant child script. New helper edges belong to the exact newly registered items; the added universe/deny-all rows are the 71 tests plus the NativeTests class fixture. No new expanded grant appears. The existing grant digest remains d303a26e373f0b173a4283dcede5735fdae6b849fdb0cb0ffcddec9017e8012a. Thus the changed census literals follow the full populations and source-line shifts without weakening the old assertion chain.

## Retained executable evidence and checks performed

I executed no payload, test, generator, analyzer or evaluation. Read-only work used absolute native Git rev-parse/show/diff, raw file/hash inspection and stdlib JSON/TOML/AST comparison scripts. Those independent checks completed successfully. The initial commands with an absent Python path or insufficient Git safe.directory context did not run a payload; the correct absolute interpreter and per-command safe.directory option resolved the inspection setup.

I verified the following retained receipt hashes and compared every path listed in focused-evidence.json against native Git blobs from each receipt's snapshot and this packet:

- Contract: task1-fix01-green-311.json, SHA-256 9a35a50a866e7d45fcef66cb3c59ec3825cd34b9d76279393da35a5a543f809b; snapshot 2fe913fe95096cf9647fb2998ba856385ed0c99b. Actual 3.11.15, 24 tests, exit 0, OK.
- Runner: t2-f2-full01-311.json, SHA-256 a05538120a902eccc508f290d96fa0a3012f286be671b1f8a15923148ce5b67b; snapshot f30eb99d86bf67b1052583aefb5a338b05115b16. Actual 3.11.15, 28 tests, exit 0, OK.
- Boundary: bflat1-311.json, SHA-256 a6f3d2f8506f51c88f889baae40470f0ab5bb5c1d767a03de842e387389eb7b8; snapshot 01a6b96e503ecb922be55ccdb03b03c9815f4ca4. Actual 3.11.15, 19 tests, exit 0, OK.

These are the bounded source-bound focused runs declared by the handoff. They are not an exact-candidate two-interpreter broad acceptance record. The later acceptance order and authorization requirements remain intact.

Independent size/format checks found 1232 production lines (624 runner, 608 contract), 1656 test lines, 138 manual registration changed lines and a 20335-byte fixture. New Python files parse as AST, contain no CR or BOM and stay at or below 100 columns. These meet the adopted source surface and the handoff's revised production allowance.

## Design assessment and finite limits

**SOUND.** The pure request/planner/observer/reducer boundary and the outer source/native/retention boundary fit the protected invariants. Reusing the existing public CLI and native Job avoids a second engine or competing ownership implementation. The explicit guard-before-files and one irreversible final check make failure standing inspectable. Review found no structural cause requiring a replacement or bounded refactor.

Optional advice, not a required correction: preserve the distinction between publication-only synthetic fixtures and legal-engine integration when adding future controls, and keep the structural loader policy described as finite syntax enforcement. Neither should be promoted into a stronger soundness claim without new evidence.

This review covers the named finite schedules, literal schemas, existing public integration receipt and exact retained census populations. It does not establish all OS failure interleavings, dynamic-loader soundness under arbitrary edited programs, protection against an external malicious writer, power-loss durability, a hard or visibility-by-deadline wall, poker strength, profitability, or statistical generalization. No population is admitted by this review. Broad acceptance, source seal, invocation authorization, remote publication and administrative handoff upload were not performed. No source was edited, no subagent spawned and no commit or push made.
