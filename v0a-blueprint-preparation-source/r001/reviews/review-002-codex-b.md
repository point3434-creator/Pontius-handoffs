**Reviewer B — defect verdict: CLEAN. Design verdict: SOUND.** I found no required correction in the cumulative source change after reviewing all three named slices and their integration. This is a read-only source-review verdict; it establishes no current or historical execution result, performance result, final-gate completion, decision authorization, or push authorization.

This report binds exclusively to:

| Identity | Verified value |
|---|---|
| Task/round | `v0a-blueprint-preparation-source/r001` |
| Candidate commit | `d3717e7153bc2acad43672e954fbd53bcdd51fe7` |
| Parent/adopted base | `c9a8aa95a1c8f65bcfb15288cbc5e4492314e457` |
| Candidate tree | `0bc222b83110a9c0b66eddb9157d240fd5a8a074` |
| Complete changed-blob manifest SHA-256 | `5405d27ea6a72de5fbfb0f0cced81f9b34b71178e7914f85f2fb44c4fe0a42b1` |
| ADR-0513 source base B | `363c9fb669e19a30375537ee5e92ea338a840a2d` |
| B tree | `10cc82ff78a84ef901242b2f69540f6a74ec498b` |

I reviewed from `D:\Pontius\tmp\blueprint-preparation-implementation-20260907-001\cold-r001-b\snapshot`, using the packet’s `candidate.json` and `manifest.sha256`. I read no sibling review, implementer transcript, implementation report, or helper/report directory. I executed no tests, poker, profiling, experiment owner, or lifecycle work, and made no source or packet edits.

**Identity and scope verification.** `candidate.json` has exactly the prescribed nine fields, with the expected schema, task, round, date, and identity values. The detached checkout HEAD is the requested candidate. Git identifies its parent and tree exactly as stated above.

Using `C:/Program Files/Git/cmd/git.exe`, I enumerated the parent-to-candidate changes with rename detection disabled, read every candidate blob through `git cat-file blob`, independently SHA-256-hashed all 24 raw blobs, constructed the digest-first sorted whole-row manifest with the prescribed two-space separator and LF termination, and compared the complete resulting bytes with the packet manifest. The comparison was byte-for-byte equal and reproduced the stated manifest digest.

The scope is exactly 15 modifications and nine additions. Every resulting changed path has mode `100644`; there are no deletions, renames, or type changes. All changed raw blobs are LF-only and BOM-free. All changed Python blobs parsed successfully through static AST inspection; repository code was not imported or executed for that inspection.

All 15 prospective old-path Git blob pins in the adopted source contract match B. Each also matches the candidate’s adopted parent, establishing that the implementation starts from the exact opened versions. ADR-0513 and its adopted brief, design, source contract, and implementation plan remain unchanged.

The packet’s named `refs/heads/review/v0a-blueprint-preparation-source/r001` ref is absent from this fresh local snapshot. That limits local verification of the ref name; it does not create an ambiguity in this report’s binding, because the exact candidate commit, parent, tree, and raw manifest were independently verified.

**Independent path and invariant inventory.** I established the following inventory from the adopted requirements, changed-path enumeration, and frozen-source callers before assessing the implementation and test assertions.

| Named slice | Changed paths inspected | Invariants assessed |
|---|---|---|
| **1. Owned lookup, runtime and transport** | `src/pontius/blueprint_preparation/__init__.py`; `src/pontius/blueprint_preparation/lookup.py`; `src/pontius/v0a/runtime.py`; `tools/v0a_hand_adapter.py`; `tools/v0a_event_adapter.py`; `tools/v0a_table_host.py`; `tools/v0a_table_session.py`; `tests/test_blueprint_preparation.py`; `tests/test_blueprint_preparation_runtime.py`; `tests/test_blueprint_preparation_transport.py`; `tests/test_v0a_table_session.py` | Exact source ownership before caching; complete-key equality; cached canonical identity; input and returned-value alias separation; legacy provider configuration and proposal meanings; preparation inside hand-start accounting; atomic preparation publication; clock-first exception classification and ordered closure; both fallback routes; independent host policy; exact admission populations and session host pin. |
| **2. Current evaluator and boundaries** | `tools/v0a_evaluation_v3.py`; `tests/test_v0a_evaluation_v3.py`; the complete delta in `tools/check_stabilization_boundaries.py` | V3’s exact delta against B’s V2; fixed loader tuple positions and captured raw execution; exact additions and exceptions; preserved bounded reader, native identities, artifacts and schemas; current guards for all three evaluator origins; preparation’s incoming/outgoing edges; inert initializer; fixed historical launcher origin and CLI; repository-level invocation of the new policies. |
| **3. Historical execution and registration** | `tools/run_evaluation_history.py`; `tests/test_evaluation_history.py`; `tools/generate_test_inventory.py`; `tools/generate_evidence_manifests.py`; `tests/test-inventory.json`; `tests/test-profiles.toml`; `docs/architecture/historical-blobs.toml`; `tests/test_inventory_and_profiles.py`; `tests/test_evidence_manifest_generation.py`; `.github/workflows/ci.yml` | Fixed B ownership of exactly three historical suites; raw checkout and index validation; native executable/path checks; fresh D-local roots; scrubbed child environments; real launch and count/skip/exit propagation; failure retention and continuation; exactly 55 historical transitions; preservation of baseline assignments and capability restrictions; exactly three historical manifest rows; current and historical CI gate separation and failure propagation. |

The related unchanged source inventory included `immutable_blueprint.py`, `decision_provider/model.py`, `providers.py`, `selection.py`, and the provider codec; blueprint artifact and visible-state contracts; the betting kernel, legal decision spine and action-clock interfaces; runtime replay and trace consumers; the hand/event/host/session source-binding chain; the rehearsal driver, seeded dealer, V1/V2 evaluators and shared evaluation helper; dependency-baseline import resolution; profile generation and configuration consumers; and the historical manifest parser/hash convention.

I also inspected related existing test callers, including the four-input selector signature assertion, replay verification’s independence assertion, adapter source/refusal controls, runtime clock/provider controls, and host/session validation controls. Frozen-source search distinguishes the unrelated older `leaf_experiment.PreparedBlueprint` family from the new package. The new package’s incoming production import is the intended runtime edge.

**Required corrections, in severity order: none.** No Critical, Important, or other required correction remains from this review. Accordingly, there is no defect reproduction or correction-specific verification criterion to prescribe. The execution gates already required by the adopted contract remain pending and are not replaced by this verdict.

**Slice 1 assessment — owned lookup, runtime and transport.** The ownership mechanism is consistent with the approved design. In `lookup.py:34`, construction first requires an exact `ImmutableBlueprintActionSource`, then rebuilds its graph through the existing `own_value` contract. Constructor validation therefore operates on newly owned exact values before canonical bytes or index entries receive authority. The canonical byte calculation occurs once, and the SHA-256 is derived from those retained bytes.

The mapping at `lookup.py:39` uses entire `BlueprintDecisionKey` objects. It does not turn key digests into lookup authority. Dictionary collisions consequently retain full-key equality semantics. The mapping is read-only, the backing dictionary is not published through the public interface, and frozen slots reject ordinary assignment. Direct reflection into private state remains outside the expressly adopted Python boundary.

At `lookup.py:58`, lookup uses the unchanged key constructor and passive-action function, validates the chosen action, and returns owned action and key values. The provider preserves the `blueprint-v1` configuration digest and existing proposal labels. Its identity property returns an owned value, and its proposal path uses the observation’s decision digest. These paths do not return an internal stored action or provider identity.

The preparation suite contains meaningful literal and reference controls for finite sizes, first/last hits and misses, streets and legal actions, invalid entries, all key fields, controlled hash/digest collisions, malformed exact graphs, subclass hooks, source mutation, returned-value mutation, and provider identity. Its delegating serialization counter observes the real canonicalization method. The legacy provider is explicitly shown by the test logic to violate the same no-repeated-serialization assertion.

Runtime preparation at `runtime.py:686` occurs after the dispatch accounting boundary has opened. The existing pre-start digest property retains its behavior and does not construct the prepared object. Preparation finishes in a local variable; the prepared slot and digest are published together after the hand spine and visible cards have been successfully constructed.

The exception order at `runtime.py:688` preserves clock classifications before the general ordinary-exception branch. Ordinary preparation failure becomes `SOURCE_BINDING_MISMATCH` and reaches the existing `_HandFailure` closure path. That path records the initiating cause before attempting boundary release. Cancellation exceptions are not converted into successful initialization.

The runtime’s call at `runtime.py:943` passes the prepared slot to the concrete selector. Blueprint mode and baseline mode both obtain their mandatory fallback through that route, before provider selection. Exact context rebuilding, independent legal-decision derivation, illegal matching-entry classification, and final source-digest/key/action checks remain present. The internal wrapper preserves the existing four-input `_select_admitted_blueprint_action` interface required by its unchanged caller test.

The runtime tests exercise real dispatch, betting-state application, delivery, and ledger accounting. Their controlled seams schedule time, preparation failure, and provider abstention; they do not replace successful preparation, lookup, state application, or ledger closure. Exact and adjacent work/deadline cases retain the original cutoff meanings.

The hand/event/host diffs change source-admission declarations only. Their captured-source and subsequent recheck code remains unchanged. The host’s baseline fallback still calls the independently owned legacy source at `tools/v0a_table_host.py:810`; its policy oracle was not migrated to prepared lookup. The new host raw Git blob is:

`7beb178989b3ff98b684093ce4022667a1c61ece`

The session pin, checker expectation, and two permitted session-test literals consistently use that blob. The nonempty transport controls assert literal action sequences, per-hand settlements and carried stacks, fallback hit/miss meanings, default/explicit blueprint equivalence, child outcomes, and late source/origin refusals.

**Slice 2 assessment — current evaluator and boundaries.** I compared the entire candidate V3 blob against `B:tools/v0a_evaluation_v2.py`. The only differences are:

- `BASE` changes to B.
- The self path in the two-element `NEW` tuple becomes V3.
- `ADDED` names exactly the two preparation files and V3.
- `CHANGED` names exactly runtime and `OLD[1:5]`, the four hand/event/host/session tools.
- The source-population/equality predicate uses those exact additions and exceptions.

The bounded reader, native/file/handle/ancestor checks, raw loader body, lifecycle and publication code, artifact reader, schemas, identifiers, and helper/dealer/host tuple positions are otherwise byte-preserved from B’s V2. The V1/V2 source files and shared helper remain unchanged.

The current checker admits the exact new origins, restricts preparation to the specified dependencies, allows only runtime’s incoming production edge, and requires the package initializer to remain inert. The decision-provider and v0a policies were updated consistently with those edges. V3 receives the same evaluator import and captured-loader restrictions as V1/V2, with its own fixed self origin. The historical launcher receives a separate fixed-constant, fixed-CLI, standard-library guard.

The repository-level checker invokes the new policies alongside the preexisting classification, legacy-edge, cycle, orchestration, and identity-revalidation checks. I found no omitted integration call or incompatible incoming/outgoing rule in the frozen production graph.

The current V3 tests cover committed unexcepted-blob changes, extra committed package/flat modules, captured-source drift, late additions, real child source drift and retention, current checker refusals for all three evaluator origins, real twelve-trial artifact construction/readback, and the bounded-reader mutation cases. Historical evaluator success therefore cannot stand in for current V3 source admission or current checker acceptance.

**Slice 3 assessment — historical execution and registration.** The launcher is a fixed gate, not a generic executor. Its CLI exposes only the adopted source root, new run root, and suite selector. B, its tree, the three paths, and expected counts are fixed in source.

`checked_history` at `tools/run_evaluation_history.py:78` compares HEAD/tree, complete tracked index paths/modes/blob identities, and every tracked checkout file against raw B blobs. It additionally checks the actual `src` population and directories and verifies the three selected-test hashes. This is materially stronger than accepting a clean Git status. The launcher performs those checks before each selected suite and after the selected population.

Historical cloning uses `--no-hardlinks`, no overlay, and an exact detached B checkout. Path validation rejects reparse ancestry and enforces the new D-local run-root contract. Children use the active CPython with `-B -P`, snapshot cwd/src, scrubbed environment, and separate suite temporary directories. Intent, stdout/stderr, result, and summary artifacts preserve observable launch outcomes. Per-suite failures do not convert the remaining population into an empty pass; the loop continues, and completion requires every selected result to pass. The tests use real historical cloning and native children, including nonzero-exit and skip controls.

I independently parsed the three B test blobs and compared their stable IDs with the generator’s exact allowlists and generated inventory:

| Historical suite | B-derived IDs | Independently reproduced sorted-ID digest |
|---|---:|---|
| `tests/test_v0a_evaluation_runner.py` | 28 | `a108bd12aacade38f9989e87d5fb2fe3c332835e1f55b4bc7baa9be667cdd2c9` |
| `tests/test_v0a_evaluation_boundary.py` | 19 | `dd15a8e31b1bc5b823a98991063af478dc15a95e158d7bff874d711d2e938284` |
| `tests/test_v0a_evaluation_v2.py` | 8 | `3e8ca7d9ae28ced9d24fe8e4c7dd72d573bf02890e9725bfeb90af004cee83cd` |

All three current test blobs equal their B blobs. Their Git blob IDs and raw SHA-256 values match the adopted source contract and new historical rows.

The complete inventory comparison establishes:

- Old entries: **3,120**; candidate entries: **3,180**.
- Removed old IDs: **0**.
- Changed existing entries: **exactly 55**, all in the three specified evaluator files.
- The only changed field in those 55 entries is `assignment`.
- Other existing entries, including baseline assignments, are unchanged.
- Historical entries increase from **137 to 192**.
- The 60 new IDs consist of 55 tests in the five new suites and five added registration/manifest tests.

The exact exception exists in both `_profile_for` and the post-baseline branch. The generated historical case has B’s commit/tree, exactly three payloads, no overlays, 55 pass expectations, and the specified positive vector with zero owner/scientific calls. Historical payloads retain the development-only profile policy. Both capability digests remain zero, and no capability definitions, call definitions, or bindings were introduced.

I independently reproduced both historical manifest digests:

- Original 167 rows: `812ce6b5e2573219f75f1fce08d1e117b7fdf930efeab3e31f228eea40499c89`.
- Candidate 170 rows: `7311fbe67c736ae1d7c72e15aa438db8aee6efc063de3459d95abadbaa0754c8`.

Every original row and snapshot is preserved. The extension is exactly one B snapshot and three `selected_test` records under `v0a_evaluation_legacy`, governed by ADR-0512. The generator appends the snapshot after existing entries, preserving the existing v7 indices. No historical parser/schema change or unrelated retained-manifest change appears in the candidate.

The CI delta routes the three old evaluator gates through the fixed historical launcher and adds separate D-local current snapshots for the five new suites. The added blocks check Git command failures and propagate the final child exit. Existing downstream failure visibility remains through `!cancelled()` conditions. Hosted execution, interpreter results, and local rehearsal of those exact blocks remain unobserved in this review.

**Integration and design judgment.** The shape is **SOUND**. A small owned lookup primitive removes repeated table work without changing the sealed blueprint, codec, provider rules, or host oracle. Runtime owns the preparation lifetime and accounting. V3 preserves historical evaluator behavior through an exact copy with a narrow admission delta. The fixed historical launcher and explicit registration changes assign the old tests to the source they actually validate.

The additional four-input selector wrapper is a reasonable compatibility accommodation for the existing frozen caller contract. The launcher remains bounded to three suites and does not introduce a general execution framework. I found no structural failure mode that warrants a replacement or redesign of any slice.

**Advisory only.** Three preexisting CI comments at `.github/workflows/ci.yml:3`, `:30`, and `:90` acquired mojibake where an em dash previously appeared. This has no effect on gate behavior and is not a required correction in this report. If editorial cleanup is undertaken in a subsequently authorized candidate, restoring those original comment bytes would remove unrelated diff noise. This advice authorizes no edit to the frozen candidate.

The remaining verification is the already-adopted acceptance population: current and historical gates on the required interpreters, complete generated census comparison including analyzer sites/blockers and decoys, CI-block rehearsal, and the separately scheduled cost observations. I have not promoted the updated census expectations into a claim that either interpreter has reproduced them. No success, latency bound, speedup, memory result, or operating authority follows from the source-review verdict.

Reviewer B (Codex) | commit=d3717e7153bc2acad43672e954fbd53bcdd51fe7 | manifest_sha256=5405d27ea6a72de5fbfb0f0cced81f9b34b71178e7914f85f2fb44c4fe0a42b1 | defect=CLEAN | design=SOUND