Reviewer A’s defect verdict is **NOT CLEAN**, solely because of one **Minor required correction** to preserved CI comment bytes. I found no Critical or Important behavioral defect in the reviewed source. The design verdict is **SOUND**.

This report binds to candidate `d3717e7153bc2acad43672e954fbd53bcdd51fe7`, manifest SHA-256 `5405d27ea6a72de5fbfb0f0cced81f9b34b71178e7914f85f2fb44c4fe0a42b1`, parent/adopted base `c9a8aa95a1c8f65bcfb15288cbc5e4492314e457`, and candidate tree `0bc222b83110a9c0b66eddb9157d240fd5a8a074`. The separately adopted source-opening contract uses B, `363c9fb669e19a30375537ee5e92ea338a840a2d`.

I conducted read-only source and manifest inspection. I did not execute tests, poker, profiling, experiment owners, lifecycle work, or repository generators. My inspection scripts used standard-library parsing and hashing of data obtained through the absolute native Git executable. I did not modify the checkout, packet, index, refs, or ledger. I did not inspect sibling reviews or implementation helper/report directories.

I read `CLAUDE.md`, `docs/workflow.md`, ADR-0513, the adopted preparation brief, design and source contract, and the implementation plan. I also inspected the relevant architecture, evidence protocol, unchanged source consumers and registration validators.

**Identity verification**

The packet’s `candidate.json` has the prescribed field set and identifies the supplied commit, parent and tree. The fresh checkout’s HEAD and its `origin/review/v0a-blueprint-preparation-source/r001` remote-tracking ref identify the candidate. The packet’s originating `refs/heads/review/...` ref is represented by that remote-tracking ref in this detached review clone.

I independently:

- Enumerated the candidate’s complete parent-to-candidate change population: **24 paths**, comprising the 15 permitted old paths and nine additions.
- Read every changed candidate blob through native Git and compared it byte-for-byte with its packet copy.
- Calculated each blob’s SHA-256, constructed the complete `<digest><two spaces><POSIX path><LF>` rows, sorted the whole rows, and compared the resulting bytes with `manifest.sha256`.
- Reproduced manifest SHA-256 `5405d27ea6a72de5fbfb0f0cced81f9b34b71178e7914f85f2fb44c4fe0a42b1`.
- Verified all **15 prospective exception base blob pins** against B.
- Verified the three historical selected-test Git OIDs and raw SHA-256 pins against B and confirmed that those test bytes remain unchanged in the candidate.
- Confirmed that all 24 changed blobs are LF-only, without a UTF-8 BOM or trailing whitespace. This does not mean every changed line satisfies a new line-length limit; large pre-existing generated lines remain present.

The historical test identities reproduced as follows:

| Suite | Tests | Raw Git blob at B | Raw SHA-256 |
|---|---:|---|---|
| Runner | 28 | `edd186ccfd6764b93b8b973793d84bdb562e1130` | `9fa3adcd5b350bdcfccfaba251999579e8a37d9d2d63bc7d8789c982ffd3774a` |
| Boundary | 19 | `f2b9534c896fa308e3e777ce3d86c3e5b3034d1d` | `4a7e323c021c1dace35345782873d8ac2a302eeb6bb7b00df7b9d3445c5f980c` |
| V2 | 8 | `477001e2407a9d097359622716b36183d37bb679` | `76121d42cb8646ea5d47e9f5076cec646a0ea0558c20921ec5b148aac93210cd` |

My independent path/invariant inventory, established from the contract before evaluating the implementation and expanded through source searches, was:

| Named slice | Complete changed-path population | Invariants and related consumers inspected |
|---|---|---|
| **1. Owned lookup, runtime and transport** | `src/pontius/blueprint_preparation/__init__.py`; `src/pontius/blueprint_preparation/lookup.py`; `src/pontius/v0a/runtime.py`; `tools/v0a_hand_adapter.py`; `tools/v0a_event_adapter.py`; `tools/v0a_table_host.py`; `tools/v0a_table_session.py`; `tests/test_blueprint_preparation.py`; `tests/test_blueprint_preparation_runtime.py`; `tests/test_blueprint_preparation_transport.py`; `tests/test_v0a_table_session.py` | Own the complete input graph before caching; preserve canonical identity; index complete keys; isolate returned aliases; preserve exact context and legality checks; prepare within hand-start accounting; retain failure order and cancellation behavior; use preparation for both runtime fallback routes; preserve independent host evaluation and exact transport admission. Related source includes `immutable_blueprint.py`, `decision_provider/model.py`, `providers.py`, `selection.py`, `codec.py`, blueprint artifact codec, betting/card values, `v0a/replay.py`, clock/model/trace, and the legal decision spine. |
| **2. Current evaluator and boundaries** | `tools/v0a_evaluation_v3.py`; `tests/test_v0a_evaluation_v3.py`; `tools/check_stabilization_boundaries.py` | Preserve the sealed evaluator except for the admitted identity delta; admit exactly the specified old population, two package files and v3; retain raw loading and rechecks; preserve bounded reads and artifact semantics; enforce outgoing and incoming preparation edges, all three evaluator origins, the host pin, and the fixed historical launcher boundary. Related consumers include the dependency scanner, v1/v2, the shared evaluation contract, seeded dealer, host Job owner and session transport. |
| **3. Historical execution and registration** | `tools/run_evaluation_history.py`; `tests/test_evaluation_history.py`; `tools/generate_test_inventory.py`; `tests/test-inventory.json`; `tests/test-profiles.toml`; `tests/test_inventory_and_profiles.py`; `tools/generate_evidence_manifests.py`; `docs/architecture/historical-blobs.toml`; `tests/test_evidence_manifest_generation.py`; `.github/workflows/ci.yml` | Fix historical execution to B and the exact three suites; validate native executables and fresh D-local roots; compare complete tracked bytes and index modes/paths; preserve failures and execute subsequent selected gates; require exact counts and zero skips; reclassify exactly 55 IDs; preserve baseline locks and capability grants; extend history by exactly three rows and one snapshot; retain CI failure propagation. Related consumers include `tools/test_orchestration/configuration.py`, its model, the evidence manifest parser/model and unchanged configuration/boundary tests. |

The unrelated `PreparedBlueprint` type in `leaf_experiment.py` and its research consumers was distinguished from the new package. It does not add an incoming edge to this preparation implementation.

**Required correction, in severity order**

1. **Minor — restore three unintentionally re-encoded preserved CI comments.**

   Exact locations are [`.github/workflows/ci.yml:3`](D:/Pontius/tmp/blueprint-preparation-implementation-20260907-001/cold-r001-a/snapshot/.github/workflows/ci.yml:3), [line 30](D:/Pontius/tmp/blueprint-preparation-implementation-20260907-001/cold-r001-a/snapshot/.github/workflows/ci.yml:30), and [line 90](D:/Pontius/tmp/blueprint-preparation-implementation-20260907-001/cold-r001-a/snapshot/.github/workflows/ci.yml:90).

   At each location, B contains one em dash, Unicode `U+2014`, encoded as UTF-8 `e2 80 94`. The candidate contains the three-character sequence `U+00E2 U+20AC U+201D`, encoded as `c3 a2 e2 82 ac e2 80 9d`. These are actual raw-blob changes, not terminal rendering differences.

   **Concrete failure scenario:** comparing the candidate’s CI blob with the opened base shows unrelated re-encoding of preserved text while applying the finite historical-routing/current-suite change. Reading the file as UTF-8 displays corrupted punctuation. This falls outside the named CI routing and suite-addition work and conflicts with the source-opening discipline against incidental re-encoding of sealed bytes.

   **Required outcome:** restore these three comment lines byte-for-byte to B while retaining the intended CI launch changes.

   **Verification criteria:** inspect the corrected raw Git blob and confirm that these three lines equal B exactly, that the three unintended comment hunks disappear, and that the intended historical routing and five current-suite blocks remain intact. Recompute the successor packet’s changed-blob manifest. No behavioral test is necessary to establish this text correction.

   **Advisory implementation advice:** a UTF-8-preserving edit of the three affected spans is sufficient. No CI refactor or general encoding cleanup is warranted.

   This is a source-fidelity correction. I found no evidence that it changes YAML execution, gate selection, or failure propagation. It is the sole reason for the NOT CLEAN verdict.

The substantive findings for each slice are as follows.

**Slice 1 — owned lookup, runtime and transport**

At `lookup.py:34`, construction requires the exact legacy source type and rebuilds it with the unchanged `own_value` implementation before canonicalization or indexing. The rebuild reaches the source, entries, keys, actions and their nested values; legacy constructors revalidate malformed graphs and duplicate keys. Canonicalization occurs once per prepared object, and the index uses complete `BlueprintDecisionKey` objects with normal equality resolution of hash collisions.

At `lookup.py:51`, selection preserves legacy key construction, passive fallback ordering and legal-action validation. The returned key and action are freshly owned. Provider construction and proposal generation at lines 79–98 preserve `blueprint-v1`, the configuration digest recipe, the observation’s decision digest, and hit/default reasons. The identity property returns an owned value. The private mapping is read-only and ordinary assignment is refused. I found no caller-input or returned-result alias that changes the cached table while leaving its digest fixed within the contract’s stated boundary.

The runtime changes preserve admission and the pre-start digest property. Preparation occurs in `_process_hand_started` at `runtime.py:686`, after the dispatch boundary has opened. Preparation and spine/card construction precede publication of the digest and prepared slot. Clock exceptions retain their clock classification; ordinary preparation exceptions enter `_HandFailure(SOURCE_BINDING_MISMATCH)`. The existing dispatch closure records the initiating cause before aborting the boundary. Cancellation is not converted into a successful initialization.

The four-input admitted selector remains available at `runtime.py:146`. Its shared implementation at line 156 preserves exact context rebuilding, independently recomputed legal decisions, illegal-entry classification and output validation. The runtime’s call at line 943 supplies its prepared object. Both blueprint mode and baseline mode obtain their mandatory fallback through that call, with subsequent source-digest/key/default-action binding checks retained.

Transport changes are limited to the declared bases/additions and session host pin. The host’s actual fallback calculation remains the legacy `self.blueprint.action_for(...)` at `v0a_table_host.py:810`. The refreshed host blob is `7beb178989b3ff98b684093ce4022667a1c61ece`, consistently present in the session, checker and corresponding tests. The existing session test changes are the two matching pin literals.

The new tests contain substantive controls for finite table sizes, all streets, legal and illegal actions, complete-key differences, controlled collisions, source/result mutation, exact graph refusal, serialization counts, charged preparation, paired failure ordering, both runtime fallback routes, work/wall edges, and literal non-empty three-hand sessions. These are source-inspected controls; I make no claim that they have passed.

**Slice 2 — current evaluator and boundaries**

The complete raw diff of B’s `tools/v0a_evaluation_v2.py` against the candidate’s v3 consists of the base/self declarations, the exact `ADDED` and `CHANGED` declarations, and the admission predicate. I found no additional reader, lifecycle, subprocess, publication, cleanup, schema or ID change.

The v3 inventory includes B’s package population, the six fixed old tools, fixture, unchanged helper and v3. The predicate requires the exact three additions and permits old-blob changes only for runtime and the four hand/event/host/session tools. The two-element loader tuple and captured helper/dealer/host execution remain intact.

I inspected the entire checker delta together with its import-edge resolver and repository-level invocation. The preparation guard at `check_stabilization_boundaries.py:471` has both outgoing and incoming rules; the runtime and decision-provider policies contain the corresponding permitted edges. Origin classification rejects extra preparation files, and the initializer is required to remain inert. The evaluator guard at line 655 applies the fixed self-origin/loader checks to v1, v2 and v3. The history guard at line 734 fixes its origin, CLI and suite/base declarations. The new guards are called by `check_repository`.

The v3 tests independently address current admission, committed unexcepted mutations, extra package siblings, late captured-source drift, all three current evaluator guards, a real twelve-trial artifact round trip, and bounded-read growth/shrink/replacement/restored-size controls. V1/v2 and the shared contract helper remain byte-identical to B. Historical tests are therefore not being presented as validation of the changed current checker.

**Slice 3 — historical execution and registration**

The launcher fixes B, its tree, the three suite paths and counts in source. Its CLI exposes only source root, run root and the closed suite choice. It creates a fresh D-local run root, uses `--no-hardlinks` without overlays, checks the detached identity, compares the full tracked tree’s raw bytes and index modes/paths, and rejects extra files/directories in the admitted `src` population. It repeats the historical check before each suite and after all suites.

Suite execution uses the active interpreter with `-B -P`, snapshot cwd/src, a scrubbed environment and separate temporary directories. Intent and output/result records are retained. A failed suite does not prevent subsequent selected suites from being attempted. The result predicate requires a successful exit, expected test count and zero skips; launch exceptions produce failed result rows.

The generated inventory comparison established:

- **3,120 → 3,180 total IDs**, with **no removed ID**.
- Exactly **55 existing rows changed**, and their only changed field is `assignment`.
- Those rows are precisely the B-derived runner/boundary/v2 IDs: **28/19/8**.
- Their ID digests reproduce the three locked digests in the registration tests.
- The other **60 additions** comprise the five new suites and five new registration/manifest tests.
- Existing baseline assignments remain unchanged.

Both inventory classification branches contain the exact historical exception. The generated profiles replace the three current evaluator payloads with historical payloads and add the five current suites. The new historical case owns exactly the 55 IDs, uses B, has no overlays, and specifies passed/body-entered 55 with zero assertion/setup failures, owner calls and scientific calls. Existing development-only historical profile policy and both zero capability digests remain unchanged. I inspected the unchanged configuration/model consumers for compatibility with these assignments and historical selected-test records.

For the historical manifest, I independently parsed and compared the old/new records and recomputed their canonical semantic hashes:

- All **167 old rows** and **11 old snapshots** remain unchanged.
- Exactly **three selected-test rows** and **one B snapshot** are added.
- The old digest reproduces as `812ce6b5e2573219f75f1fce08d1e117b7fdf930efeab3e31f228eea40499c89`.
- The new approved digest reproduces as `7311fbe67c736ae1d7c72e15aa438db8aee6efc063de3459d95abadbaa0754c8`.
- Current-file, current-absence and retained-v7 manifests remain byte-identical to B.

CI routes the three old evaluator steps through the launcher and adds five current-suite blocks using fresh D-local snapshots. The changed launch blocks check clone/checkout failures and return the child’s exit code. Existing downstream `!cancelled()` behavior remains. The three comment encoding changes identified above are unrelated to those operational changes.

**Integration and design assessment**

The integration preserves separate policy and evidence responsibilities: the child uses the prepared table; the host computes the reference fallback independently; v3 identifies the new source implementation without changing artifact semantics; the historical launcher owns the old source-dependent gates; and the current checker validates the new origins. I found no unexplained production import edge, missing source-admission exception, inconsistent host pin, broadened capability grant, or extra historical manifest row.

The design is **SOUND**. The optimization is small and local, owns data before caching, and preserves the independent host check and existing accounting boundaries. The sealed evaluator copy and fixed historical launcher introduce maintenance cost, but that cost is explicitly justified by the approved contract and remains bounded. The discovered comment corruption does not indicate a structural design problem. No replacement or refactor is required by this review.

Confidence is high in the raw identity, scope and static comparisons reported above. Execution remains unobserved. In particular, this review does **not** establish successful current or historical gates, a complete executed analyzer census comparison on both interpreters, hosted CI success, native timing behavior, or performance/memory improvements. Those remain the prescribed post-review work. The changed census expectations were source-reviewed; the analyzer was not run.

The immediate closure criterion is the narrow raw-byte correction above and its successor identity verification. This review authorizes no decision commit, push, operating invocation or cost claim.

Reviewer A | commit=d3717e7153bc2acad43672e954fbd53bcdd51fe7 | manifest_sha256=5405d27ea6a72de5fbfb0f0cced81f9b34b71178e7914f85f2fb44c4fe0a42b1 | defect=NOT CLEAN | design=SOUND