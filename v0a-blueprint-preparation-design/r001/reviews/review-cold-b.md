**Cold-B independent Tier C design report: CLEAN / SOUND**

Reviewer: `/root/blueprint_design_cold_b`  
Date: 2026-09-07  
Round: `v0a-blueprint-preparation-design/r001`  
Candidate: `ddf652d00e68a84e1eef03d5bd4df37c5a022b79`  
Manifest SHA-256: `e68bf5eb2bf2338c9217717a960d79a5624abdb62b09c0914609fa6a3fc35aa4`  
Base: `363c9fb669e19a30375537ee5e92ea338a840a2d`  
Candidate tree: `0fb36b3958b88a50b9398009516cb62088ca5973`

No must-fix findings remain from this review. **Defect verdict: CLEAN. Design verdict: SOUND.** Both verdicts bind exclusively to the candidate and manifest above.

The proposed shape fits the contract: an owned value object prepares the existing canonical representation and a complete-key index; the real runtime uses that object within its existing accounting boundary; the host retains a separate reference lookup; and exact source admission and historical/current test routing have explicit, bounded changes. The larger registration surface follows from the existing sealed source contracts. The proposal identifies that cost and limits it without replacing the underlying evidence protocol.

Confidence is **high for the documentation and static implementability assessment**. This verdict does not establish implemented behavior, performance, generated-status freshness, or acceptance-test success. Those claims require their specified later gates.

**Independence and review scope**

I started from the permanent `handoff.md`, `candidate.json`, and `manifest.sha256`. I read the candidate’s six frozen documentation files, `CLAUDE.md`, the relevant workflow provisions, ADR-0512, and supporting baseline source. I recorded an initial requirement/seam inventory before assessing the implementation seams. No implementer transcript, implementer coverage report, or another reviewer’s findings entered this review.

The shared checkout contained unrelated working changes. All candidate and baseline conclusions below came from the named Git objects. Packet blob bytes were independently compared with those objects.

This was a documentation-only source-opening review. I ran no tests, poker payloads, experiment owners, profiles, or performance controls. I changed no candidate, source, test, registration, or retained-evidence bytes.

**Identity and exact scope**

Fresh calculations established:

- The review ref resolves to the named candidate.
- Its parent is exactly the named base.
- Its tree matches `candidate.json`.
- The base tree is `10cc82ff78a84ef901242b2f69540f6a74ec498b`.
- The diff contains exactly one modified `STATUS.md` and the five added documents below, with no deletions, renames, source changes, or other paths.
- All six permanent packet blobs equal the corresponding raw candidate Git blobs.
- Sorting complete `<lowercase SHA-256><two spaces><path><LF>` rows reproduces the packet manifest byte-for-byte and its declared digest.

The independently calculated raw SHA-256 values are:

| Candidate path | Raw SHA-256 |
|---|---|
| `STATUS.md` | `f09877441f0ab3f271e0cdb4235ee44582dc0e1280a2a20a064552470227ca20` |
| `docs/architecture/v0a-blueprint-preparation-r001/brief.md` | `39a528d0a31ac8f4dd89fd6f2174ad0ae36199b53051108b74cff63ecdd3cb38` |
| `docs/architecture/v0a-blueprint-preparation-r001/design.md` | `cd997f4e659998a6960c39656256a10f2511fcebcf5471c64f7fba7118167d8f` |
| `docs/architecture/v0a-blueprint-preparation-r001/source-contract.md` | `cff78ab31b6c76c541c54795028f97efb673862bb5a4ea3e8f6b942d09cdb698` |
| `docs/decisions/ADR-0513-open-the-immutable-blueprint-preparation-source-round.md` | `a3460318bc77bc7923f806a9bc1c473563211de8d81987554e4cc03ce49e8650` |
| `docs/superpowers/plans/2026-09-07-blueprint-preparation.md` | `a8cd6744ecce686eb8881b0e1a0d5b5caf59a39b1e29ccffb9582cf53fde3f0d` |

All fifteen prospective old-file Git blob pins in `source-contract.md:12–26` match B. The source-opening exception is expressly prospective, tied to those versions and permitted changes, and contingent on separate ADR-0513 adoption. The submitted candidate itself preserves the sealed source and retained evidence.

All six changed raw blobs are LF-only and BOM-free, without trailing whitespace. The five authored documents meet the 100-column convention. `STATUS.md` retains the generated layout, including its long link and table rows. `git diff --check B C` completed successfully.

**Requirement-to-evidence assessment**

| Requirement or risk | Independent evidence and assessment |
|---|---|
| Ownership before cached identity | `design.md:11–22` requires an exact source and the existing `decision_provider.model.own_value` rebuild before canonicalization or indexing. Baseline `model.py:41–61` rebuilds only known exact types and invokes their constructors. This provides a concrete route to reject subclasses/malformed graphs and remove caller-owned aliases. |
| Unchanged canonical bytes and digest | Baseline `immutable_blueprint.py:323–346` defines the existing source canonicalization and digest. The proposal caches those bytes and hashes them once rather than defining a new representation. Source ID, entry order, keys, actions, provider configuration and exact-byte comparison controls are explicitly included. |
| Complete-key lookup and legal behavior | The proposed index uses the entire `BlueprintDecisionKey`; ordinary hash collisions still require complete equality. Baseline `BlueprintDecisionKey` includes the visible cards, public betting state and history. `design.md:24–29` preserves `from_state`, passive default ordering and the legacy legal-action validator, with fresh returned key/action values. |
| Direct provider compatibility | Baseline `decision_provider/providers.py:23–44` supplies a small, explicit identity/proposal contract. `design.md:31–36` preserves its label, configuration digest, observation requirement, decision digest and hit/default labels. The new provider does not require editing the sealed factory or baseline rules. |
| Actual runtime use in both modes | Baseline `runtime.py:914–944` computes the mandatory fallback before choosing the provider route. Adding the prepared argument to that existing selector therefore reaches both blueprint selection and baseline fallback. `design.md:59–64` preserves exact context reconstruction, independently derived legality, illegal-entry classification and final binding checks. |
| Accounted setup and failure closure | Baseline `runtime.py:570–608` opens and closes the transition boundary; `655–697` performs hand initialization and computes the current digest. Preparing at the named point is implementable inside the measured interval. The proposal explicitly addresses clock-first classification, ordinary preparation failures, coordinated publication and the existing closure path. |
| Independent host oracle | Baseline `tools/v0a_table_host.py:803–822` computes fallback through the legacy source. The replay validator independently uses the legacy source at `src/pontius/v0a/replay.py:850–870`. Their policy evaluation remains sealed. Host changes are limited to source-admission declarations. |
| Exact source admission and loader preservation | Hand/event/host currently inventory the package and their fixed tool chains. V2 also compares a closed whole-package population. The specified B-relative sets, exact additions and changed-blob exceptions match those mechanisms. Preserving the two-element self/helper tuple keeps the evaluator’s fixed loader indices implementable. |
| Boundary checker integration | The named checker file owns origin classification, incoming provider edges, runtime restrictions, session host-pin checks and evaluator loader guards. It is already among the fifteen exceptions. The specified prepared imports and sole runtime incoming production edge can be admitted there without editing sealed provider/runtime-model files or allowing a broad module prefix. |
| Honest historical test assignment | The three old suites statically contain 28, 19 and 8 tests. Their exact AST-derived stable-ID sets equal the B inventory sets, and all 55 entries are post-baseline additions. The proposal identifies both generator branches that currently enforce current ownership and limits the historical exception to those IDs. |
| Historical manifest and parser compatibility | The proposed three selected-test rows reproduce the specified seed digest. Baseline manifest parsing accepts the added snapshot/row shape, and the configuration model requires exactly the matching phase/commit/test-path closure. No parser/schema change is necessary for this extension. |
| Current acceptance remains current | `source-contract.md:117–120` explicitly requires current v3 source binding, real child completion and current import-policy refusals for all three evaluator origins. The old boundary checker is expressly insufficient. The shared contract suite stays on current source. |
| Bounded authority and measurements | ADR-0513 and the source contract separate design adoption, implementation, later source sealing and finite cost observations. They preserve consumed owners, existing cutoffs, retained failures and reporting limits. Construction/index/cached-byte costs and the host’s retained reference cost are included. |

**Historical pin and manifest calculations**

The historical test pins independently match B:

| Suite | Tests / inventory IDs | Git blob | Raw SHA-256 |
|---|---:|---|---|
| `tests/test_v0a_evaluation_runner.py` | 28 / 28 | `edd186ccfd6764b93b8b973793d84bdb562e1130` | `9fa3adcd5b350bdcfccfaba251999579e8a37d9d2d63bc7d8789c982ffd3774a` |
| `tests/test_v0a_evaluation_boundary.py` | 19 / 19 | `f2b9534c896fa308e3e777ce3d86c3e5b3034d1d` | `4a7e323c021c1dace35345782873d8ac2a302eeb6bb7b00df7b9d3445c5f980c` |
| `tests/test_v0a_evaluation_v2.py` | 8 / 8 | `477001e2407a9d097359622716b36183d37bb679` | `76121d42cb8646ea5d47e9f5076cec646a0ea0558c20921ec5b148aac93210cd` |

Parsing the existing historical manifest and independently applying its documented canonical row convention reproduced:

- Existing population: **11 snapshots, 167 rows**.
- Existing entries/approved-seed digest: `812ce6b5e2573219f75f1fce08d1e117b7fdf930efeab3e31f228eea40499c89`.
- Population after precisely the three proposed B-selected-test additions: **170 rows**, with one additional snapshot.
- Proposed entries/approved-seed digest: `7311fbe67c736ae1d7c72e15aa438db8aee6efc063de3459d95abadbaa0754c8`.

No existing row was changed in that calculation.

**Advisory implementation considerations**

These are implementation guidance, not additional approval gates or required design corrections:

- Preserve the exact distinction between “prepare completed” and “hand initialization published.” Construct the prepared value locally and publish it with the digest at the existing successful state-publication point. The new failure controls should observe runtime state and the real ledger rather than infer success from constructor bookkeeping.
- The checker changes must account for both ends of `blueprint_preparation.lookup → decision_provider.model`. The existing provider incoming-edge policy is independently enforced. The source contract authorizes this edge; treating it solely as a new package’s outgoing allowlist would leave an avoidable integration failure.
- Configure historical cloning to produce raw stored bytes, then perform the required comparisons. A successful checkout or clean Git status does not establish raw-byte equality when line-ending conversion or filters are active.
- Keep the history launcher fixed to its three suites. Its size estimate is a planning estimate; expanding it into a general historical executor would exceed the design’s stated purpose and reopen the proportionality question.

**Verification record and remaining limits**

The substantive read-only checks used the absolute Git executable `C:/Program Files/Git/cmd/git.exe`: `rev-parse`, `diff-tree`/`diff --name-only --no-renames`, `cat-file blob`, `show`, `ls-tree`, `grep`, and `diff --check`.

Static SHA-256, JSON/TOML and AST calculations ran through `D:/Pontius-tools/py311/Scripts/python.exe -B -P -`, using standard-library code that read Git blobs. It did not import repository production or test modules. The final consolidated identity/scope/pin/hygiene/ID calculation and the separate historical-seed calculation both exited **0**.

The largest remaining unknown is whether the eventual implementation preserves the required behavior through the real runtime and transport boundaries while removing repeated table work. The cheapest falsifying controls are the specified real-method serialization counter, returned/input-alias mutation tests, and one accounted hand start followed by real decisions in both modes. An unexplained source-population expansion, altered accounting semantics, or weakened existing oracle remains a stop condition under the proposed contract.

The design’s post-review status-generation check and twelve status tests have not run as part of this review. Runtime correctness, native historical launch behavior, current source admission, floor/newest interpreter acceptance and finite measurements remain future evidence. This review authorizes neither source implementation nor a decision commit.

The complete report is returned here for the coordinator to store append-only as `reviews/review-cold-b.md`; I created no files.
