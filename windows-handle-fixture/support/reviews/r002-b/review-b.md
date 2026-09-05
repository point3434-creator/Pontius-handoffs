# Tier C FIX review B — windows-handle-fixture/r002

## Binding and verdict

- Candidate: `c7de23de276c50463d831f3983fede82a5400ce8`
- Base: `5e56e4454f7b8ccb360d3e36245abc33318349bb`
- Tree: `014ee05a5014181bd63471247e5ee09607bb2346`
- Manifest SHA-256:
  `f5e06a5fa9d0fdf37888d29f8bfe6b395b6fc40a4c6f87258f66c95aa17421ed`
- Rejected predecessor: `76309774b551a874b8f9c677bc59e51299cee0e4`
- Deferred correction-coverage SHA-256:
  `c03afd7bf7370a395ce5a5f61336166dc0484a83d6aa3d0988b6b6cb4f67d96e`
- Defect counts (Critical / Important / Minor): **0 / 0 / 0**
- Specification verdict: **PASS**
- Engineering-quality verdict: **PASS**
- Defect verdict: **CLEAN**
- Design verdict: **SOUND**

No finding survives verification. The candidate makes the one authorized
mechanical correction: five overlong expressions are reflowed without a parsed
behavior change, and the sole mechanically consequent analyzer census digest
is updated. The controlled Windows-handle design is unchanged, so its bounded
test-only facade remains a sound fit for the controller's explicit rule-8
exception.

## Frozen identity and scope

Raw Git metadata independently established that the named ref resolves to the
candidate, whose sole parent is the named base and whose tree is the named
tree. Base-to-candidate `diff-tree -r -z --no-renames` names exactly two
modified paths:

- `tests/test-inventory.json`
- `tests/test_inventory_and_profiles.py`

Predecessor-to-candidate `diff-tree` names only
`tests/test_inventory_and_profiles.py` (`+15/-6`). The checked-in inventory
blob is byte-identical between r001 and r002. Thus the correction adds no path,
test registration, profile assignment, production byte, or generated-inventory
change.

The manifest was recomputed from raw candidate blobs using whole-row byte sort
and LF rows. The packet manifest bytes and digest matched exactly:

```text
0b07a2ac105e6fce052f923322836b94a36a14d9c174b5d2cc085c7baa29664f  tests/test-inventory.json
f9efa98ee407b035b1f971bf0191400287f0799130d63df235921cbd75f107df  tests/test_inventory_and_profiles.py
```

Both packet overlay files were byte-equal to their frozen Git blobs.

## Independent inventory and deferred-claim comparison

Before opening `correction-coverage.md`, I recorded the correction invariant,
all six semantic sites, the full base-to-candidate surface, and the unchanged
5+6+3 schedule population in `reviews/r002-b/initial-inventory.md`, SHA-256
`a14f2f7f5aa304331b7dfc2e464b3711dc860fd1b191a2fff0b86eda8c6cebcf`.
Only then did I hash and open the deferred claim; its digest matched the bound
value above.

The claim and independent inventory agree. The correction consists of:

1. splitting the adapter teardown message into two implicitly concatenated
   f-strings;
2. vertically reflowing one `assertEqual` call;
3. vertically reflowing one `assertFalse` call;
4. vertically reflowing the replay control's `assertRaisesRegex` call;
5. vertically reflowing the leak control's `assertRaisesRegex` call while
   retaining the same `as caught` binding; and
6. changing only `string_sink_decoy_sha256` from the r001 value to the newly
   derived value.

A whole-module AST comparison, excluding source-position attributes, became
exactly equal after normalizing that one census string constant. The textual
comparison produced five change groups: four single-site wraps, one adjacent
two-expression wrap group, and the digest literal. The predecessor inventory
blob was exactly preserved. This rules out hidden registration, argument,
ordering, binding, message-value, and fixture-behavior changes.

## Exactness and proportionality checks

- All 360 Python lines added from base are at most 100 columns; maximum 100.
- All 15 Python lines added by the r002 correction are at most 100 columns;
  maximum 91.
- Both changed candidate blobs are LF-only, BOM-free, final-LF-terminated, and
  free of trailing spaces or tabs.
- `git diff --check` passed for both base-to-r002 and r001-to-r002.
- The two adapter classes total 174 nonblank lines, within the 200-line cap.
- Relative to base, the inventory contains exactly the three authorized new
  Windows-control stable IDs, no removals, and no changed existing entries.

The focused checked-in discovery/analyzer test passed on both supported slots.
Because that test executes the unchanged analyzer and compares its exact
`analysis_census`, it independently confirms the new
`string_sink_decoy_sha256` rather than merely accepting a textual replacement.

## Focused runtime evidence

Both executions used `run-snapshot.ps1`, a unique fresh no-hardlink D:-local
snapshot, base checkout plus `packets/r002/files` overlay, snapshot-root cwd,
`python -B -P`, scrubbed environment, snapshot `PYTHONPATH`, and the absolute
regular/non-reparse Git executable in `PONTIUS_GIT`. The 3.11 floor ran first;
the 3.14 native run used the requested escalation.

The exact five-test payload was:

- `test_windows_controlled_reuse_preserves_native_resources`
- `test_windows_controlled_reuse_detects_production_replay`
- `test_windows_controlled_reuse_releases_unpublished_and_leaked_handles`
- `test_windows_persistent_close_failures_are_truthful_and_retryable`
- `test_working_discovery_binds_every_entry_and_introduced_id`

Results:

| Slot and snapshot | Result | Record SHA-256 |
| --- | --- | --- |
| CPython 3.11.15, `r002-review-b-focused-311` | 5 tests, `OK`, exit 0, 70.495 s | `34bceccf365f1f3ab43e0d805957e458074e3b5dd8eca62287f6b46d9561143a` |
| CPython 3.14.6, `r002-review-b-focused-314` | 5 tests, `OK`, exit 0, 52.571 s | `85aa0c2a919bad169c1e5e6c59aadca4c1e4086e9a02ceb12f1a491a1f9332ea` |

The payload covers real native acquisition/resource checks, the real writer
and cleanup-manager path over the existing 14 schedules, replay sensitivity,
publication/teardown cleanup, and the exact analyzer/inventory consequence.

## Requirement-to-evidence summary

| Requirement or risk | Fresh evidence | Result |
| --- | --- | --- |
| Correct only the five r001 E501 violations | Frozen textual inventory and line census | Pass |
| Preserve behavior except the derived census literal | Whole-module normalized AST equality | Pass |
| Justify the new census literal independently | Analyzer/discovery test on 3.11 and 3.14 | Pass |
| Preserve inventory and schedule population | Exact r001/r002 inventory equality; unchanged AST; focused real writer payload | Pass |
| No scope or production change | Raw base/r001/r002 `diff-tree` and blob identity | Pass |
| Preserve exactness and size limits | Width, newline, whitespace, and nonblank-line census | Pass |
| Preserve real native/writer/cleanup/oracle behavior | Five focused tests on both required interpreters | Pass |

## Deliberate limits

This review did not run the full inventory suite, the controller's 19-command
codec acceptance population, or any other broad suite. It did not reopen the
already-passed native fixture design beyond confirming that the correction did
not change it. It did not inspect design-review or implementation narratives,
edit candidate/source/generated bytes, commit, push, or exercise operating or
research authority. Review-only files are confined to `reviews/r002-b`; the
two disposable snapshots and runner records are retained under the task root.
