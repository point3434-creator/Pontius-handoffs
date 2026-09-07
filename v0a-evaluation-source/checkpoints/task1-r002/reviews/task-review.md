# Task 1 independent FIX review

Reviewer: Codex /root/evaluation_contract_fix_review. Date: 2026-09-07.
Scope: task1-r002 pure-helper FIX checkpoint; not integrated Tier C acceptance.
Candidate b10363549ce6538574ffe34a6db691733ae2c20b; manifest 284d2ae2623aaff63084554765f3ff0d89be47b64f42749442dfb60a177bd0f9.

## Initial independent inventory, recorded before deferred coverage

Derived from accepted source-contract, Task 1 plan, issued I-01 and raw candidate source/FIX diff. Deferred coverage.md has not yet been opened.

Invariant: an event row rejected by schema, identity or cross-row conflict checks must have no effect on output-visible observations. The accepted prefix must remain intact; conflicts remain deficiencies, completion stays false, and scoring stays null. Admission includes related mutable aliases and later attribution consumers, not just the immediate failure append.

Independent related-path inventory:

1. Row decode, exact versioned wire fields, identity, readiness, terminal and status gates must precede event effects.
2. Decision validation and prior same-action decision equality; decision timing comparison against prior failure/decision timing must precede all effects.
3. Failed-row failure presence/schema, v1 null-decision rule, v2 same-frame decision/failure identity, code, delivery/action and timing equality; fully identified seen-copy conflict comparison must precede append or source merging.
4. Failure timing's same-hand/action conflict check must precede failures append, seen insertion, shared sources-list replacement, and timed insertion. Null identities must remain per-frame and cannot infer action timing/count attribution.
5. Nonfailed accepted/decided rows must validate event order, pending-action correspondence, action/street ordinals, no cause, completed finite time/accounting and deadline bounds before selected/legacy increments, decisions insertion, or timed assignment.
6. Common event commit updates selected, legacy, decisions and timed, then event/pending. Failure copy merging aliases failures entries through seen; inspect source-label leakage when a later decision conflicts.
7. Publication copies failures and selection/legacy/timing counters, then host-action matching reads decisions and mutates attributed and unattributed counts. Host-applied counts and hand/session causes are independent of rejected wire-row effects.
8. Ready/action/terminal/session-result rows also must validate before state admission; malformed-tail break preserves earlier accepted metrics. Final completion/settlement and reduce_trials must continue refusing incomplete/refused scoring.

Verification map: exact I-01 late failure timing scenario -> literal single expected failure; late decision timing conflict for both v1 legacy and v2 fallback -> unchanged selections and host attribution; existing-source alias conflict -> unchanged ordered source labels. Retain matching-copy, conflicting-copy, null identity, malformed/missing/truncated coverage, outer timeout and full-denominator controls. Inspect raw RED/GREEN and snapshot binding without executing payloads. Check FIX changes only helper/test and unchanged fixture, imports and finite population.

## Issued verdict

**CLEAN within the scoped Task 1 FIX checkpoint. Specification: PASS. Engineering quality: PASS. Design: SOUND. I-01 is closed; no required correction remains in this FIX category, and no changed-path regression was found.** This is neither a full integrated Tier C acceptance nor a source seal. The rejected anchor's issued NOT CLEAN verdict remains unchanged.

The inventory above was saved before reading coverage.md; its then-current SHA256 was 45b83805c3afea902b0939d3310d1a4aa916f85a60a3fa1479372baab35c9ca9. This final section completes the same newly created reviewer-owned draft without replacing that inventory.

## Exact candidate and scope binding

Independently resolved using native Git raw objects:

- Ref refs/heads/review/v0a-evaluation-source/task1-r002 -> b10363549ce6538574ffe34a6db691733ae2c20b.
- Candidate parent/base: 34616938c708b1ca306b9d8a17b9d98e2f9e451f.
- Candidate tree: 950554c9989329f69f36ec3081a4eff28ca36ca1.
- Reconstructed sorted whole digest/two-space/path/LF manifest: 284d2ae2623aaff63084554765f3ff0d89be47b64f42749442dfb60a177bd0f9, byte-identical to manifest.sha256.
- Rejected anchor: 55b1f5f75f7bcdf8061a2a02906a86769345715d; independently reconstructed anchor manifest c15299d1d6cbf53e0660fcd24e91f488e228735135b97a0ce467882eee089cb6.
- Issued I-01 review hash verified: 31774fe43923e0a9260dff18563e6e8976f81d7a6db391d38db0651e22d4e364.
- Deferred coverage hash verified: e060fa6ccd4fac3946b548b1c6d2deae69d0fce77fb3d33ed62dcb60e8818a29.

Candidate versus parent contains exactly three additions. Candidate versus rejected anchor changes only helper and test: 12 added/7 removed helper lines and 57 added/0 removed test lines. Fixture is unchanged. Native raw source.diff/review.diff match packet bytes, SHA256 5d847cf9792433d1f570e258e5739c2df103b5c6335222755b1e22968e3d31b1. FIX diff with --unified=10 matches packet bytes, SHA256 51824b28fc00538509d62dffd6037bab0ba7ec90102802e60ae0a5b46381d821. Initial default-context FIX hash differed (8a19464fab88525ea232f3e16e2f100efc930ac0bc62b74c3c65594ff3cb9fd8); inspecting hunk headers resolved this as context width, not candidate drift. No normalization was used for byte identity.

| Raw path | SHA256 | Bytes / LF lines |
| --- | --- | --- |
| tools/v0a_evaluation_contract.py | b62170553c20acce17bead44391904c53be43cf0cc59c0fd2fb9b47743e988ad | 35588 / 608 |
| tests/test_v0a_evaluation_contract.py | 6a3b8be9cd071738df37599b8f24c0de0698e5e4dd5622b527f227e0d48af45b | 26456 / 446 |
| tests/fixtures/evaluation/controls.json | 9204a8aec4a4d6558381b246385495201d64c33e67732e2d3ab21feed31c7eea | 20335 / 634 |

All three raw blobs equal packet files. The fixture contains the one literal deal with cards 0..16. The FIX adds no deal, import, launch, generator, decoder, matrix, reducer or publication surface. The production delta is five net lines and remains within the whole-asset budget, whose remaining native portion must still fit later.

## I-01 and related-path assessment

At helper lines 426-433, local decision validation is followed immediately by prior decision equality and timing equality. These checks now precede the failed-event branch's failure append and aliased source-label change, as well as common decision insertion and selection counts. At lines 445-450, failure timing conflict validation precedes the seen-copy comparison and any failure mutation. Same-frame decision/failure equality ensures the later failure and decision timing assignments agree. There is no remaining explicit row-validation require after the first failed-row observation mutation. On the nonfailed branch, pending correspondence, ordinals and completed timing/accounting checks finish before the common metric updates at lines 486-496.

Consequently a late conflicting row cannot add a failure, change an existing failure's sources, admit a decision, replace prior timing, increment a selection/legacy count, or influence the final decisions-to-host-action attribution loop. Earlier validated failure copies still merge sources; null identities remain per-frame; malformed tails still break with a retained prefix. Ready/action/hand_result/session_result state assignments remain after their validation and unchanged by this FIX. Existing failed-row event-order diagnostics and observed-prefix semantics were not broadened into a new schema audit.

The deferred coverage inventory agrees with the independently recorded inventory, including the less obvious seen-to-failures alias and final attribution consumer. Its discovery enumerates actual mutation/check/publication sites and its finite cases cover the demonstrated branches. The claim does not depend solely on successful state-shape assertions: tests call the real public observe_trial helper, and the RED exposes observable failures in the rejected implementation.

| Required behavior | Finite evidence | Assessment |
| --- | --- | --- |
| Exact v1 late timing conflict preserves first failure only | New test at line 296 asserts literal expected failure, conflict, refusal, all prefix metrics, no score | Closed |
| Rejected v1/v2 decisions cannot change selections or host attribution | New test at line 310 exercises both versions after failure-only prefix, with one literal host action left unattributed | Closed |
| Rejected decision cannot mutate prior failure sources through alias | New test at line 327 requires ordered sources remain [decision,failure] then [failure] | Closed |
| Matching-copy and null-identity semantics remain | Existing duplicate timing, source merge, failed-decision attribution, null identity and conflicting-copy tests unchanged and GREEN | No regression found |
| Missing/invalid/truncated coverage and scoring remain honest | Existing malformed prefix, missing decision, complete versions, cleanup and denominator checks unchanged and GREEN | No regression found in changed paths |

The before/after comparison is supplemented by literal failure content, source-label expectations, empty selection counts and one unattributed action. It is not merely comparing two unanchored invocations. Timing metrics are also compared; the existing timing-duplicate control supplies nonzero flags. This finite evidence does not prove every malformed schema combination or resource-exhaustion behavior.

## Raw RED/GREEN receipt and snapshot evidence

RED receipt SHA256: 2b76e882dacdbfc076c7c1b4df4d28413a9e89aea4f4ea1a2e7cd49562f9c6d0.
Snapshot HEAD f44fcd825d02388c5b4c9b4b7729d40e569dc5a5, tree c49741ab82bc2a4eeaf812f20f5bd2e6e586e8a6. Diff-tree against the rejected anchor contains only the test-file modification. The helper SHA256 is 4197281f2cd8780a106fabd26abf55c320fd19ae4417d25fc1f1db8b8d9eacf7 and fixture hash is unchanged, both equal rejected raw blobs; test hash equals corrected candidate. The raw receipt reports 24 tests, exit 1 and eight assertion failures, all from the three new tests: extra failure twice asserted, one source alias, v1 legacy/attribution and v2 selection/applied-selection/attribution. All preexisting tests pass.

GREEN receipt SHA256: 9a35a50a866e7d45fcef66cb3c59ec3825cd34b9d76279393da35a5a543f809b.
Snapshot HEAD 2fe913fe95096cf9647fb2998ba856385ed0c99b, tree 950554c9989329f69f36ec3081a4eff28ca36ca1, exactly the candidate tree. Every snapshot raw blob and checked-out file hash equals the corrected candidate's corresponding raw file. The raw receipt reports 24 tests, exit 0, OK in 0.045 seconds, including all six existing named negative source mutants. RED's checked-out file hashes were also verified against its raw blobs.

Both receipts include successful actual CPython 3.11.15/-B/-P/cwd probes and explicit test argv, interpreter and snapshot identities. These retained receipt observations, freshly bound to immutable source here, are used as the permitted execution evidence. I did not rerun payload tests. The receipt format itself does not serialize the full environment; I make no separate fresh execution-environment certification beyond its recorded probes and source binding. Full integrated snapshot/environment acceptance and actual 3.14.6 remain later gates.

## Engineering judgment and limits

SOUND for this bounded correction: validation-before-mutation removes the concrete cause with no rollback machinery, mutable-state copies or new framework. The common decision preflight protects both branch-specific failures and downstream attribution. The existing pure-helper/public-subprocess separation remains appropriate. Future event-row changes must keep every rejecting validation before the observation commit; that is the relevant maintenance obligation, not a reason to require a larger rewrite now.

Read handoff first, applicable CLAUDE/workflow, accepted source-contract, Task 1 brief/plan, ADR-0508 and relevant design sections; inspected complete raw helper, fixture, test and exact FIX diff. No implementer reports, transcripts or external rationale were read. The required rejected review and subsequently opened frozen coverage are the permitted inputs. Read-only Git used only C:/Program Files/Git/cmd/git.exe --no-replace-objects with command-local safe.directory equal to the exact authoring/snapshot repository. Checks used rev-parse, diff-tree, cat-file blob, raw diff, SHA256, direct byte comparison and a read-only tracked status check (clean). An early PowerShell revision-list construction split the caret into its own argument and failed; the corrected explicit strings resolved parent/tree successfully. No source changes, payload tests, poker, generator, census, deletion, subagents, commits or pushes occurred.

Native wrapper ownership/publication, registration/census, full accepted-B schema integration, both independent integrated Tier C reviews and all sixteen acceptance commands are outside this scoped checkpoint and remain unpassed here. This verdict closes I-01 only for the bound candidate and its related FIX paths.
