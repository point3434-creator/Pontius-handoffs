Independent cold design review — Cold A

Reviewer: /root/blueprint_design_cold_a (Codex), 2026-09-07.
Round: v0a-blueprint-preparation-design/r001, initial Tier C documentation-only source-opening review.
Finalizer: /root.

Candidate commit: ddf652d00e68a84e1eef03d5bd4df37c5a022b79
Candidate manifest SHA-256: e68bf5eb2bf2338c9217717a960d79a5624abdb62b09c0914609fa6a3fc35aa4
Candidate tree: 0fb36b3958b88a50b9398009516cb62088ca5973
Base commit: 363c9fb669e19a30375537ee5e92ea338a840a2d
Base tree: 10cc82ff78a84ef901242b2f69540f6a74ec498b

**Defect verdict: CLEAN. Design verdict: SOUND.** Both verdicts bind only to the candidate commit and manifest above. No must-fix finding remains. Confidence is high for raw identity and prospective contract coherence, with implementation behavior and execution acceptance explicitly unverified.

The ownership-before-cache mechanism, full-key index, accounted hand-start integration, retained reference behavior, versioned evaluator, and fixed historical gate are implementable within the named exceptions. This is a design-review conclusion. It is not source implementation acceptance, a measured speed claim, source-opening adoption, or decision-commit authorization.

**Independence and allowed evidence**

I began with the permanent handoff, candidate.json, manifest and frozen candidate, then independently inspected the requirements and relevant base source. I read CLAUDE.md, docs/workflow.md, the relevant charter/architecture boundaries, ADR-0512, ADR-0513 and all five candidate authoring documents. I received no other reviewer's findings and read no implementation transcript. The working tree contains unrelated changes, so all candidate and base content was obtained from the pinned Git objects; working files were not substituted for evidence.

Only read-only source inspection, AST/JSON/TOML parsing, raw Git identity calculations and whitespace inspection were performed. No tests, owners, poker, profile, inventory-generation, status-generation or performance payloads were executed. No candidate files were modified.

**Requirement and seam inventory**

| Requirement or risk | Independent source evidence and design assessment |
| --- | --- |
| Cached identity must describe owned immutable lookup values | Base decision_provider/model.py:40-62 rebuilds a closed set of exact value types, including the complete blueprint graph. The design requires this rebuild before canonicalization/indexing and fresh returned action/key/identity values. This addresses caller/result alias mutation without claiming protection against arbitrary private-state reflection. |
| Canonical bytes, digest, provider identity and default behavior must retain their meanings | Base immutable_blueprint.py defines canonical table hashing, complete decision keys, hit/miss labels, passive fallback and legality. Base decision_provider/providers.py:23-44 supplies the preserved configuration and proposal contract. Reuse of the existing canonicalization and model types avoids a second artifact schema. The artifact codec remains sealed. |
| Lookup must use full visible/public keys and reject illegal hits | Base key construction includes all visible cards, full public betting history and the complete betting state. The proposed mapping uses equality on the entire key, not a key digest. The finite controls explicitly include differences in complete keys, controlled hash collisions, malformed graphs, duplicates and illegal matching entries. |
| The optimization must reach the real runtime in both modes | Base runtime.py:915-944 performs the admitted blueprint selection before optional baseline-provider selection. One prepared argument at this shared seam reaches blueprint-v1 and baseline fallback. The old public selector's default route can remain unchanged. |
| Preparation must be measured and failure ordering preserved | Base runtime.py:561-608 opens the transition boundary before hand-start processing and records an initiating _HandFailure before closure. Hand-start digest work is at 664-693. Preparation can be inserted there and published with successful initialization. Clock-first classification and the existing closure route are explicitly preserved; no ledger or preparation-bank source exception is requested. |
| Optimized selection must retain final binding and legality checks | Base runtime.py:145-199 independently rebuilds legal context, validates selection and classifies illegal matching entries. Lines 1165-1202 bind digest, query key, exact hit type and passive misses. The design retains these checks while replacing successful lookup work. |
| Independent reference behavior must remain available | Old source/provider/codec implementations remain unchanged. Base WireConsumer.provider_expected at tools/v0a_table_host.py:803-822 independently computes baseline fallback from an owned decoded blueprint and public state. The host's operating logic is excluded from permitted changes. Literal/reference controls cover both strategy routes. See the advisory precision note below. |
| Source admission must remain exact through adapters, host, session and evaluator | The hand/event/host tools inventory the whole package and have explicit additions/exceptions. The proposed B-relative two-file addition and scoped changed-blob sets are implementable. Base v2's two-element NEW tuple and three captured loader edges at 20 and 170-176 are explicitly retained in v3. The four corresponding session/checker/test host-pin sites are covered by the named exceptions. |
| Historical tests must remain unchanged and accurately identified | The three old source-dependent suites really admit their surrounding source tree, so a current package addition invalidates their old admission. The fixed B/tree launcher is a truthful historical gate, not a replacement for current v3 acceptance. The shared evaluation-contract suite remains current. |
| Historical registration must preserve unrelated assignments, capabilities and retained evidence | All 55 evaluator IDs are post-baseline current assignments at B. The proposed exact exceptions in both inventory branches can reclassify only these IDs while preserving the baseline lock. The existing parser accepts the proposed snapshot/selected-test row shape; the approved historical digest extension was independently reproduced. |
| Qualification must not create unmeasured limits or operating authority | Costs include owned copy, index, cached bytes and retained host reference work. Measurements are finite engineering observations with separate setup, warm lookup and memory results. The 14,000 ms cutoff, 15,000 ms wall, failed-attempt retention and separately authorized adoption remain explicit. |

**Raw identity results**

The frozen candidate's parent equals B; its recorded ref resolves to the candidate; both tree IDs match. With rename detection disabled, the exact delta is one modified STATUS.md and five added Markdown documents. There is no source, test, configuration, fixture, retained-evidence, or earlier-ADR change in this candidate.

Each packet blob is byte-identical to its raw candidate Git blob. Independently computed changed-file SHA-256 values are:

| Path | Raw SHA-256 |
| --- | --- |
| STATUS.md | f09877441f0ab3f271e0cdb4235ee44582dc0e1280a2a20a064552470227ca20 |
| docs/architecture/v0a-blueprint-preparation-r001/brief.md | 39a528d0a31ac8f4dd89fd6f2174ad0ae36199b53051108b74cff63ecdd3cb38 |
| docs/architecture/v0a-blueprint-preparation-r001/design.md | cd997f4e659998a6960c39656256a10f2511fcebcf5471c64f7fba7118167d8f |
| docs/architecture/v0a-blueprint-preparation-r001/source-contract.md | cff78ab31b6c76c541c54795028f97efb673862bb5a4ea3e8f6b942d09cdb698 |
| docs/decisions/ADR-0513-open-the-immutable-blueprint-preparation-source-round.md | a3460318bc77bc7923f806a9bc1c473563211de8d81987554e4cc03ce49e8650 |
| docs/superpowers/plans/2026-09-07-blueprint-preparation.md | a8cd6744ecce686eb8881b0e1a0d5b5caf59a39b1e29ccffb9582cf53fde3f0d |

The six lowercase-digest/two-space/POSIX-path/LF rows, sorted as entire rows, exactly reproduce packet manifest.sha256 and SHA-256 e68bf5eb2bf2338c9217717a960d79a5624abdb62b09c0914609fa6a3fc35aa4.

All fifteen old-path Git blob pins in source-contract.md:10-26 equal B's actual blobs. All six candidate blobs are LF-only and BOM-free, with no trailing whitespace. The five authored documents stay within 100 columns. Generated STATUS.md retains long generated link/table rows; its generator is unchanged and actual freshness remains a subsequent gate. git diff --check B candidate exited 0.

The historical suite pins also reproduce exactly:

- runner: Git edd186ccfd6764b93b8b973793d84bdb562e1130; SHA-256 9fa3adcd5b350bdcfccfaba251999579e8a37d9d2d63bc7d8789c982ffd3774a.
- boundary: Git f2b9534c896fa308e3e777ce3d86c3e5b3034d1d; SHA-256 4a7e323c021c1dace35345782873d8ac2a302eeb6bb7b00df7b9d3445c5f980c.
- v2: Git 477001e2407a9d097359622716b36183d37bb679; SHA-256 76121d42cb8646ea5d47e9f5076cec646a0ea0558c20921ec5b148aac93210cd.

AST method enumeration and the checked-in inventory agree on 28 runner, 19 boundary and 8 v2 IDs. Each is introduced after the locked baseline and currently assigned current. Independent LF-sorted stable-ID digests are:

- runner: a108bd12aacade38f9989e87d5fb2fe3c332835e1f55b4bc7baa9be667cdd2c9
- boundary: dd15a8e31b1bc5b823a98991063af478dc15a95e158d7bff874d711d2e938284
- v2: 3e8ca7d9ae28ced9d24fe8e4c7dd72d573bf02890e9725bfeb90af004cee83cd
- combined 55: 4bd6d5c08bfd6b3ad498ea4facd69a2de52521adc7b27f80275496798e6e8e08

The parsed 167 existing historical rows reproduce both old entries/approved-seed digests, 812ce6b5e2573219f75f1fce08d1e117b7fdf930efeab3e31f228eea40499c89. Adding exactly the three B-derived selected_test records, phase v0a_evaluation_legacy and governing decision ADR-0512, produces 170 rows and digest 7311fbe67c736ae1d7c72e15aa438db8aee6efc063de3459d95abadbaa0754c8. One appended snapshot gives the stated 12-snapshot total. This was a pure calculation; the production generator was not imported or executed.

**Must-fix findings**

None.

**Advisory precision and implementation guidance**

1. Low severity, non-blocking: design.md:73-76 should be read with the host's actual mode distinction. The independent fallback recomputation is the baseline-v2 WireConsumer path. For blueprint-v1, the unchanged host checks legal state transitions, trace consistency and settlement, but does not separately recompute the blueprint policy action: host.py:1020-1030 passes identity/blueprint only for baseline, and exchange():887-905 echoes the selected action into the blueprint-mode expected row. Avoid describing the host alone as a policy oracle for both modes. The required literal/reference tests in source-contract.md:163-185 and the common runtime fallback seam make the present design adequate without opening host operating code.

2. Non-blocking implementation guidance: enforce both new preparation edges in the existing overlapping guards: runtime to preparation in enforce_v0a_import_policy, and preparation to decision_provider.model in enforce_decision_provider_import_policy. Adding a new package guard alone will not override either existing refusal. The exact checker exception already permits these named edges; other origins must retain their refusals.

3. Non-blocking implementation guidance: the history launcher should explicitly configure raw-LF checkout behavior when cloning/checking out B. The repository uses checkout line-ending conversion, while the proposed launcher correctly requires working bytes equal to raw Git blobs. Its raw census, not git status, is the acceptance evidence.

These points introduce no additional authority, file opening or acceptance waiver.

**Evidence procedure and residual limits**

Read-only Git operations used the absolute executable C:/Program Files/Git/cmd/git.exe: status --short; diff/diff-tree with the explicit base and candidate; rev-parse; ls-tree; cat-file blob; grep; and diff --check. Pure calculations used D:/Pontius-tools/py311/Scripts/python.exe -B -I - with only standard-library AST, hashlib, JSON, pathlib, subprocess and TOML parsing. Pin, manifest, historical-row and ID calculations completed successfully with exit 0. A PATH interpreter discovery produced no python result; calculations then used the known absolute 3.11 slot. No acceptance payload was launched from the working tree or elsewhere.

The largest remaining unknown is whether the implementation fulfills the real timing/failure and native source/transport contracts while preserving the old gates on both actual interpreter versions. The cheapest useful falsifiers after opening adoption are a real-method serialization counter on the prepared table, a real HandRuntime non-empty fallback/control with independently scheduled clock cost, and a real v3 child whose wrong fallback is refused by the unchanged baseline host. The source contract already requires these categories.

The kill criteria are the brief's unexpected source/capability population or clock-semantic change, any remaining protected-invariant defect, or its workflow/round-budget stop. Continue only through the candidate's required second independent Tier C review and subsequent unchanged status generation/check plus all twelve status tests in fresh exact-candidate D-local snapshots, actual 3.11.15 before 3.14.6. Those gates and separately authorized decision adoption remain outstanding and are not conferred by this report.
