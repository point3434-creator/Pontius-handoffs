# Cold implementation review A — Windows handle fixture FIX r001

## Binding and verdict

- Candidate: `76309774b551a874b8f9c677bc59e51299cee0e4`
- Base: `5e56e4454f7b8ccb360d3e36245abc33318349bb`
- Tree: `f7d2451c20e417967864718b3d000a3eb60387e9`
- Manifest SHA-256:
  `755c34175c060a4f0ef55616c9e52e336989645763cb16c0fd5a26293a7a37a6`
- Defect counts (Critical / Important / Minor): **0 / 0 / 1**
- Specification verdict: **PASS**
- Engineering-quality verdict: **FAIL (Minor only)**
- Overall defect verdict: **NOTCLEAN**
- Design verdict: **SOUND**

The bounded per-module `ctypes` facade is the right shape for the controller's explicit rule-8
exception. Numeric reuse is controlled while acquisition, IO, identity, close, rollback,
namespace effects, owners, and cleanup-manager dispatch remain production/native. Replacement
survival is checked using captured native handles and original Win32 functions outside the token
facade. No production seam or general filesystem double was added. The sole required correction
is mechanical line-length cleanup.

## Finding

### M-01 — Five added lines exceed the repository's 100-column limit

Severity: **Minor**. Confidence: **High**.

Locations in frozen `tests/test_inventory_and_profiles.py`:

- line 21184: 107 columns
- line 21337: 104 columns
- line 21338: 103 columns
- line 21382: 101 columns
- line 21424: 106 columns

The changed file otherwise has LF-only bytes, no BOM, no trailing whitespace, and a final LF.
`pyproject.toml` sets Ruff `line-length = 100` and selects `E501`; workflow checklist item 10 also
requires changed files to be at most 100 columns. Both interpreter slots lack the `ruff` module,
so the attempted Ruff commands were classified as environment limitations, not candidate test
failures. A direct line census against the frozen packet blob establishes the violation.

Required correction: reflow only these five expressions without changing behavior, then
regenerate the mechanically consequent self-census if its source digest changes. Verification:
repeat the line census (and Ruff when available), then repeat the focused snapshot checks.

## Identity and source-scope evidence

The review used the frozen ref and packet blobs, not mutable authoring files.

- `git rev-parse refs/heads/review/windows-handle-fixture/r001` returned the bound candidate.
- `git rev-parse <candidate>^{tree}` returned the bound tree.
- `git rev-parse <candidate>^` returned the bound base.
- `git diff-tree -r --no-renames` returned exactly:
  `tests/test-inventory.json` and `tests/test_inventory_and_profiles.py`, both modified.
- Numstat was `+1/-1` for the generated one-line JSON and `+351/-100` for the test source.
- No production, codec, analyzer, runtime, CI, status, or decision path changed.
- Recomputed manifest-file SHA-256 matched the bound manifest digest. Its two sorted rows were:
  - `0b07a2ac105e6fce052f923322836b94a36a14d9c174b5d2cc085c7baa29664f`
    for `tests/test-inventory.json`;
  - `3fc1ee4390383ec8a5eb389563fb6ef039ab349a9a2117c78b2b2c87b289a992`
    for `tests/test_inventory_and_profiles.py`.
- Packet file raw Git object ids matched the frozen blobs:
  - JSON: `e36ac6213decc0e3dc9cc9f38559fcf9fa5bed6c`;
  - Python: `1103b6f3c523daa703496dd3249afa95db698a18`.
- The adapter occupies 176 nonblank lines, within the 200-line cap.

The diff files were used for navigation only; all identity, source, and behavior conclusions bind
to the raw frozen blobs above.

## Pre-coverage inventory and deferred-claim comparison

Before opening the FIX claim, I recorded the affected invariants and related paths in
`reviews/a/initial-inventory.md`, SHA-256
`b74670a7a838dc45b3d1a0bfd4306271643baea62f47fc47723de9725308a055`.
Only then did I hash and open `coverage.md`; its SHA-256 matched the pinned
`6c5ea08ff78251c40714f3d651fa9f2720d6a995ed4de99dadd5e0f1f281bb8e`.

The independent schedule inventory matched the claim:

| Family | Independently inventoried schedules | Result |
| --- | ---: | --- |
| Final3 writer role isolation | 5 | Match |
| Round7 pre-bound file owners | 6 | Match |
| Round9 disposition/same-inode reuse | 3 | Match |
| **Total** | **14** | **Match** |

The claim's API boundary also matched source inspection: directory `CreateFileW`, all governed
`NtCreateFile` outputs, first-handle arguments, `OBJECT_ATTRIBUTES.RootDirectory`, and rename/link
`RootDirectory` are routed; ordinary path-read `CreateFileW` handles remain native for CRT
ownership. Closed issued tokens resolve to invalid handle zero rather than falling through as a
native number. Publication failure raw-closes the acquisition, reassignment transfers one table
entry, successful close retires it, and context exit restores the module facade before reporting
unexpected live resources.

The candidate's built-in negative test stops at the first deliberately corrupted occurrence in
each helper/owner-class invocation. That is adequate for its shared assertion sites, and I closed
the residual schedule-specific sensitivity question with the independent 14-position replay
matrix described below. Every later schedule remained sensitive when earlier schedules were
allowed to complete normally.

## Executed behavior

Every command used a unique retained D:-local snapshot, base checkout plus frozen packet-file
overlay, snapshot-root working directory, `python -B -P`, snapshot `PYTHONPATH`, scrubbed child
environment, and absolute `C:\Program Files\Git\cmd\git.exe` in `PONTIUS_GIT`. The CPython
3.11.15 floor ran before CPython 3.14.6.

### Focused candidate tests

The following four test methods passed together on each interpreter:

1. `test_windows_controlled_reuse_preserves_native_resources`
2. `test_windows_controlled_reuse_detects_production_replay`
3. `test_windows_controlled_reuse_releases_unpublished_and_leaked_handles`
4. `test_windows_persistent_close_failures_are_truthful_and_retryable`

- 3.11.15: 4 tests, `OK`, exit 0, 1.472 s. Record SHA-256
  `5a655d96af9489078ddee9ac1e2d98fe4b97a0a8a49f3684307f918812a0dc5b`.
- 3.14.6: 4 tests, `OK`, exit 0, 3.250 s. Record SHA-256
  `a41280cd923012d35b837035aa43b9e709936915065fb5d7ebc9a649a81e9c1a`.

### Independent 14-schedule runtime census

Probe `reviews/a/probe_schedule_census.py`, SHA-256
`7a228d0465bffce0bc67c21e50db1e030d58a6e22760cffff4699573cdeac6bb`, wrapped only the
adapter's reuse and raw-survival methods while calling the three real production-writer helpers.
It observed 5, 6, and 3 reuse events respectively; each had a paired raw-survival event and a
16-byte native file identity. Totals were 14 reuse and 14 survival checks on both interpreters.

- 3.11 record SHA-256:
  `2f869fc438814ffe22c5361b88b1609d90c46bdd49b665c6a95eba077cb432cb`.
- 3.14 record SHA-256:
  `e121d4cddad42276d37228e4e925f3b64f55390afef50027b25efd519486ff0d`.

### Independent per-schedule production-replay mutation

Probe `reviews/a/probe_replay_matrix.py`, SHA-256
`3ce62590149502bb20964bf659a8aabbdf685816e9f6110e7f71d69fa85aeb39`, allowed each earlier
schedule to finish normally and introduced the bad second close at each later ambiguous-close
occurrence in turn. For every one of the 14 named schedules, the cleanup-manager retry reached
the production owner reconciliation method, the production close helper actually closed the
captured native replacement, a direct native liveness query confirmed closure, and the helper's
facade-bypassing replacement oracle raised `native replacement was closed or changed`.

- 3.11: 14/14 mutants detected, exit 0. Record SHA-256
  `a72b1470f5aad0915fe5927f0362f133b0486df7324334b2e0fd2cf7877b91ca`.
- 3.14: 14/14 mutants detected, exit 0. Record SHA-256
  `a6dd0c4f13437ba81d2a99710c6251aeaa9e221f5f730120e64e0ed7ae70b92e`.

## Requirement-to-evidence summary

| Requirement or risk | Best fresh evidence | Result |
| --- | --- | --- |
| Deterministic numeric reuse without relying on the Windows allocator | 14-event runtime census; token equals retired number in helper assertions | Pass |
| Real acquisition, IO, identity, close, rollback, and namespace behavior | Source trace plus focused real-writer tests on Windows | Pass |
| Native/CRT path remains native and transfers ownership | Exact-byte `read_regular_snapshot` control on both slots; empty adapter at exit | Pass |
| No token/native collision or stale-token native fall-through | Range checks, issued-token resolution, resource control | Pass |
| Publication and teardown retain single ownership and fail closed | Source trace plus unpublished/leak controls on both slots | Pass |
| Raw replacement liveness and full native identity bypass facade | Captured original Win32 functions; 16-byte identity census; replay matrix | Pass |
| Bad replay is observable through real writer/cleanup execution | 14/14 per-schedule production-replay mutations on both slots | Pass |
| Original schedule population remains complete | Independent 5+6+3 runtime census on both slots | Pass |
| Only two allowed paths change; codec/analyzer untouched | Frozen `diff-tree`, manifest, and raw-blob recomputation | Pass |
| Mechanical inventory consequence | Three new stable IDs present; controller self-census gate remains separate | Partial pending controller gate |
| Exactness/style hygiene | LF/BOM/trailing checks pass; five E501 lines fail | Fail (Minor) |

## Limits and deliberately deferred gates

- I did not read design reviews, implementation narratives, other implementation reviews, or
  prior reviewer outputs.
- I did not edit the candidate, authoring checkout, production source, primary checkout, packet,
  or earlier evidence. Review-only probes and this report are confined to `reviews/a`; all
  snapshots and run records are retained.
- The two Ruff attempts failed because neither interpreter environment contains the `ruff`
  module. Their retained record SHA-256 values are
  `c9a180104b14cc04ae350b315ade6135d58201fe4f686f34638730097a86b198` (3.11) and
  `af89245ac34ac91cbe6f4f582b5b401f71174ceca39ac6b9eb93ae1967a56668` (3.14).
  This does not weaken the direct E501 evidence.
- I did not run the complete inventory suite or the 19-command codec acceptance population.
  Under the stated workflow, the controller runs those broad gates only after both Tier C
  implementation reviews are clean.
- This review establishes the approved finite Windows API/fixture scope only. It is not a general
  Windows allocator proof, arbitrary native-fault proof, codec review, or operating/research
  authorization.
