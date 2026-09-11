# Lookup performance r001: independent bounded review

**Technical verdict: PASS within the declared frozen-graph and pure-check scope. No Critical or Important finding.** Specification and engineering-quality axes both pass for the candidate overlay. No material unresolved issue justifies another review round. This verdict grants no adoption, commit, push or retained-run authority.

**Coldness qualification:** This was a fresh independent Codex review, substituted for the opposing reviewer by explicit instruction, with one reviewer and no delegation. It was not a context-free cold session, and this report does not label the result an unqualified cold pass. The developer injected a memory summary about prior Pontius training/governance/research, a skill catalog and general tool/environment guidance. The parent supplied only the bounded review task and environment paths, then requested status updates. The user supplied a joke-response instruction. No memory file, prior conversation, prior review, ledger, unrelated scratch, or another reviewer's inventory was opened. The permitted source documentation was read before inventory sealing and contains author test/benchmark/parity claims; this exposure is explicitly disclosed. A broad frozen tree filename listing also exposed unrelated filenames, not contents. Packet hashing read uninterpreted raw check bytes before inventory, as required by the handoff manifest procedure.

## Frozen target and sealed inventory

- Packet: `D:/Pontius-handoffs/v0a-blueprint-lookup-performance/r001`.
- Declared read-only Git checkout: `D:/Pontius-worktrees/eval-runner-consolidation`.
- Base commit: `d4488fee970e10ac96a5b4a33f8d3fc9ff86c05b`.
- Base tree: `ca5fec797e3bd06a22ba3bcb8e14101321128b32`.
- Raw manifest SHA-256: `14ee03389d41e63fc3a4303fbc55df380cb778347c9d0ee06695a529d504f6fe`.
- Inventory: `D:/Pontius/tmp/lookup-r001-cold01-20260910/inventory.md`.
- Inventory SHA-256: `b689ca0be8447c4691086fe6742c0b24b9cb85a536013ab9ccac7f31b38be6f6`.

The manifest was recomputed from every packet file except itself, sorted as complete ASCII rows with LF termination, and compared byte-for-byte. All five declared override hashes match. All 454 archived source members match the frozen Git blobs, first by Git blob identity and then by raw byte comparison with `git cat-file`. Archive membership matches the complete frozen `src/` scope. Unchanged tests/tools were copied only from the declared commit. The scratch candidate contains the frozen source plus exactly the five declared overrides. The packet manifest and sealed inventory were rechecked unchanged at the end.

The inventory was sealed before opening `coverage.md` or interpreting anything in `checks/`. It remains immutable. Correction to inventory I08: cold source canonicalization sorts entries, so its general upper bound includes O(n log n) sorting, plus per-key serialization; the inventory's shorthand O(n) describes traversal but is not a complete worst-case bound. This correction does not alter an acceptance requirement or implementation verdict.

## Findings and contract assessment

There is no reproduced material defect. No Critical/Important finding is asserted, so no unsupported reachable-path allegation is being used to block the candidate.

The production delta is limited to the non-dataclass `_DigestCache` base, inherited by `BlueprintDecisionKey` and `ImmutableBlueprintActionSource`, and their two digest getters. Key/source canonical serializers, equality-based linear action lookup, legal-action checks and wire codec remain unchanged. Warmth does not enter dataclass fields, equality, hash, repr, replace or serialized value state.

Trust-boundary checks remain distinct from direct library behavior:

- `decision_provider/model.py:41` reconstructs exact known fields through `own_value`. `decision_provider/providers.py:26` owns the source before computing provider identity; proposals use that owned graph. `DecisionProposal` also owns returned actions.
- `v0a/runtime.py:86` reconstructs exact policy fields; `_admit_blueprint` at line 107 precedes public selection and runtime ownership. `v0a/replay.py:758` admits its source before independent replay lookup. Cached caller slots are not copied.
- `blueprint_artifact/codec.py:128` reconstructs and validates keys, and `_admit` at line 207 rebuilds the whole source. Artifact encoding ignores forged cache slots. New cache state does not authorize malformed fields or subclass hooks.
- `blueprint_preparation/lookup.py:34` owns input, computes canonical bytes and builds its existing full-key index. Its provider still has the legacy provider value contract. It is a separate prepared library/provider route, not a replacement for the legacy scan.
- `reference_hand_replay.py:382` invokes `spec.blueprint.action_for` directly and line 520 reads its digest. That consumer assumes the documented unmodified frozen graph. The change is compatible with this contract; it is not a mutation detector. Explicit `object.__setattr__` abuse of that caller-owned graph can leave stale identity, as the candidate documentation already states. Such abuse is not a newly supported operation or evidence that admission imports the cache.
- `full_width_reference_policy.py:356` constructs fresh keys and uses their digest as provenance; the cache adds no future/opponent-private fields. `eval_bridge` builds canonical entries and uses the exact artifact/provider interfaces covered by the parity diagnostic.

The completion test's private checkout copy list now includes `src/pontius/immutable_blueprint.py` at `tests/test_eval_completion_tool.py:220`, with `shutil.copyfile` at line 223 before its phase helper. This precisely fixes the stale-module integration setup. That check is static in this review; the host phases were not relaunched.

## Fresh evidence mapped to the inventory

| Inventory | Evidence and result |
|---|---|
| I01 | Raw manifest, commit/tree, all 454 archive blobs and five override hashes verified. PASS. |
| I02-I03 | Existing canonical literal fixtures, key completeness, order-independent source identity, provider identity/proposal parity, and whole 1,081-hand parity. PASS. |
| I04 | Existing copy/deepcopy/pickle/replace/equality/hash/repr/fields tests; additional pure diagnostic verifies asdict, astuple and pickle bytes are invariant to cache warmth and pickle drops forged caches. PASS. |
| I05 | Existing malformed graph/subclass/stale/forged cache admission tests; pure artifact-encoder forged source/key cache diagnostic. PASS. |
| I06 | Consumer inspection above plus owned-input mutation tests. Direct unmodified-graph assumption remains explicit. PASS within contract. |
| I07 | Exact actions, first/last hit, misses, collisions, duplicate keys, stale contexts and illegal raises tested; runtime failures and fallback behavior exercised. PASS. |
| I08 | Sequential matched benchmark; separate memory measurement; serialization regression green on candidate and red on base. PASS for bounded work-cost claim. |
| I09 | Real caller tracing plus static integration private-copy verification; pure runtime/provider tests execute changed module. PASS for required copy/path criterion; full host execution not repeated. |
| I10 | 347 existing pure unittest cases against isolated candidate, zero failures/errors/skips; four changed Python files pass Ruff. PASS for executed scope. |

`tests.log` and `test-summary.json` contain the fresh test receipt. Fifteen of the author's affected suites (331 cases) ran, plus eight export and eight pure completion cases. The two omitted original suites are `test_blueprint_workload_session` (includes temporary Git commits) and `test_eval_protocol` (execution-host capture). Two completion methods were also omitted: `test_real_host_check_hit_default_and_changed_stack_are_distinct` and `test_supervised_three_phase_subset_and_bound_input_failures`. These exclusions are reported directly rather than counted as skips or passes. The author's prior 349/18-case receipts are not being relabeled fresh evidence.

The unchanged new serialization regression was run separately against frozen base and failed exactly with `AssertionError: identity reserialized after first read`. This is the expected negative control, not a candidate failure.

## Performance and compatibility observations

Python 3.14.6, sequential base then candidate, packet benchmark unchanged, five batches of 20 operations; tracing disabled throughout timings. At 1,326 entries:

| Operation | Base | Candidate |
|---|---:|---:|
| Legacy hit | 6.828590 ms | 0.118610 ms |
| BlueprintProvider proposal | 6.913565 ms | 0.157115 ms |
| Prepared hit | 0.029060 ms | 0.029330 ms |
| Provider construction | 31.556933 ms | 31.660533 ms |
| Full-graph construction + first identity, retained traced bytes | 468,976 | 618,927 |
| Same experiment, peak traced bytes | 834,498 | 845,114 |

The observed repeated lookup/proposal speedups are approximately 57.6x/44.0x. Additional retained allocation is 149,951 bytes in this fixture; peak increases 10,616 bytes. These are local observations, not confidence intervals, a latency SLA, or playing-strength evidence. Construction timings use prebuilt entries; the separate memory experiment constructs the full graph. First digest computation still serializes/hashes and sorts source entry identities. Warm source/key digest reads reuse one string each, with no retained canonical byte strings. Legacy lookup still scans O(n), and enumerating n lookups remains O(n squared), apart from per-key equality costs. Concurrent first-read redundant work is possible and was not stress-tested.

The in-memory retained-input diagnostic freshly passed on both base and candidate. All membership result objects compare equal: 1,081 hits, 0 disagreements, 0 unsupported; source identity and canonical SHA-256 both equal `38dc88b85d905f29b1212664aa5572179a42054d87ad5b0891219f1769971fe9`. The artifact re-encodes exactly to 1,010,990 bytes, SHA-256 `666021c448c622caf235b304128d17de02823c12966c66510f5a1ec483814d17`. Timing fields are intentionally excluded from equality and not treated as a matched performance measurement.

## Commands, artifacts and execution limits

All writes were confined to `D:/Pontius/tmp/lookup-r001-cold01-20260910`. The specified virtual-environment interpreter initially failed sandbox launch with Access denied; approved escalation successfully ran that same interpreter, CPython 3.14.6. No alternate Python version or package installation was used.

Reproducible scratch orchestration and receipts:

- `assemble.py`: raw Git/packet assembly and verification; final exit 0. An initial missing-bracket syntax error in this review helper was corrected before execution; it did not execute or change candidate code.
- `run_checks.py`: existing unittest suites, exit 0; `tests.log`, `test-summary.json`.
- `run_diagnostics.py`: four sequential packet diagnostic invocations, each exit 0; `benchmark-base.json`, `benchmark-candidate.json`, `retained-parity-base.json`, `retained-parity-candidate.json`, `diagnostics-summary.json` and child logs.
- Existing serialization regression on frozen base: exit 1, expected; `baseline-red.log`.
- Pure dataclass/pickle/encoder diagnostic: exit 0; `value-diagnostics.log`.
- `python -B -m ruff check --no-cache` on four changed Python files: exit 0; `ruff.log`.
- `git diff --no-index` confirmed the production delta; exit 1 indicates differences, not a failed source check. Git emitted an LF/CRLF advisory; raw-byte verification remained authoritative.

No production/packet/retained-record edits, Git commits, pushes, adoption, retained phase, execution-host phase, dependency installation, additional reviewer, or unrelated research run occurred. Frozen `AGENTS.md` was absent; the supplied user instruction remained applicable. No requirement for another review round was identified. The principal residual limits are the disclosed contextual coldness qualification, static-only verification of the corrected private-host copy step, finite synthetic benchmark, and absence of concurrency stress evidence.
