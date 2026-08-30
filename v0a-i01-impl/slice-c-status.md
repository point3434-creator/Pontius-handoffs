# Slice C status — admission, boundary policy, CI

Author: Claude, 2026-08-30. Worktree: `D:/Pontius-worktrees/v0a-slice-c`,
branch `v0a/slice-c`, based on the r006 candidate `c74b8062` so the v0a package
is present for the gate to classify. **Not frozen** — see the coordination
note below.

## Coordination with the A/B rework

Codex is reworking the six v0a modules and the four A/B test files under
`v0a-i01-ab`. Per the controller's coordination point, slice C may proceed now,
but **the final inventory and census regeneration must run on the finished
combined tree**, because the A/B test contents change what the census measures.

That splits this work cleanly:

| Part | Depends on A/B contents? | State |
| --- | --- | --- |
| Boundary classification and import policy (`tools/check_stabilization_boundaries.py`) | No | **Final** |
| `tests/test_v0a_boundaries.py` | No | **Final** |
| CI workflow steps | No | **Final** |
| `STABILIZATION_TEST_FILES` declaration | No (names only) | **Final** |
| `tests/test-inventory.json`, `tests/test-profiles.toml` | **Yes** | **Provisional — regenerate on the combined tree** |
| Census expectations in `tests/test_inventory_and_profiles.py` | **Yes** | **Provisional — refresh on the combined tree** |

I attempted to shrink the provisional surface by declaring only the new
boundary test, but the generator refuses any undeclared test file on disk
(`unreviewed stabilization test file: tests/test_v0a_contract_faults.py`), so
all five must be declared together and the census necessarily depends on A/B
contents.

## What is done

**Boundary gate: RED → GREEN.** Before the change the gate refused the package
outright — six modules "lack stabilization classification". Now it exits 0.

Five narrow changes, exactly as planned: `V0A_ORIGIN_PATHS` declaring the six
files by name (no wildcard, so an undeclared v0a file fails as an undeclared
evidence file does); origin classification extended to `src/pontius/v0a/`; the
legacy-edge new-module allowance extended to the classified namespace only; a
new `enforce_v0a_import_policy` encoding ADR-0485's allowlist; and the pinned
baseline asserted rather than regenerated.

The import policy carries the two structural rules from the ADR, not just the
allowlist: only the explicit-deal host may reach the river evaluator, and **no
policy module may import the host** — the isolation that keeps the complete
deal away from selection.

**Twelve boundary tests**, exercising the real checker functions with real
source bytes plus the whole-repository gate. Five mutations injected, all five
caught: classification disabled, namespace un-permitted, river opened to every
module, host-import ban removed, allowlist opened.

**Legacy baseline untouched** — blob still `5fe6ee47…`, exactly the ADR-0485
pin, with two tests asserting it (blob identity and a clean working tree) so a
future round cannot quietly regenerate it.

**Admission and census.** All five v0a test files declared; inventory and
profiles regenerated through the authorized writer; the full 87-test
`test_inventory_and_profiles.py` suite passes. Every census refresh is
mechanical and attributable:

| Expectation | Change | Cause |
| --- | --- | --- |
| declared-file tuple | +5 entries | the five v0a test files |
| `subprocess_direct_site_count` | 45 → 47 | two `subprocess.run` calls in the new boundary test |
| `max/min comparison dispatch…` | 35 → 36 | one site in the new boundary test |
| blocker total | 355 → 358 | the three above |
| `analyzed_sites_sha256` | refreshed | corpus now includes the five declared files |
| `string_sink_decoy_sha256` | refreshed | same corpus change |
| 13 line-bound `(path, line)` entries | +5 each | the five lines added to the test's own declared tuple |

Two traps worth recording. Adding *explanatory comments* next to a census
expectation shifted every decoy row below it and changed the decoy digest —
decoy rows are keyed by line number, so provenance has to live in this document
rather than inline. And the pre-existing `os.link` cross-drive failure in
`test_git_launch_and_raw_object_reads_are_identity_bound` is environmental:
TEMP must be on the same volume as the interpreter (`TEMP=D:\v0ctmp`).

**CI.** Five clone-safe v0a suites added after the existing gates with
`if: ${{ !cancelled() }}`, per ADR-0484's growth rule. No existing gate is
demoted; nothing v0a needs is archive- or device-dependent. A `\t` in the step
paths silently became a literal tab on first write — caught and repaired, and
the file is asserted tab-free.

## Verified now

| Gate | Result |
| --- | --- |
| `check_stabilization_boundaries.py` | exit 0 |
| `generate_test_inventory.py --check` | exit 0 |
| `test_inventory_and_profiles.py` | 87 pass |
| five v0a suites | all pass |
| baseline blob | `5fe6ee47…` unchanged |

Also discovered: the clean r006 tree already failed three inventory tests
because the v0a test files were present but undeclared. No v0a round ran that
suite, so it went unnoticed since slice A. Slice C is what closes it.

## Remaining before this can freeze

1. Codex's A/B rework lands.
2. Rebase or replay slice C onto the combined tree.
3. Re-run `generate_test_inventory.py --write` and refresh the census
   expectations against the final contents, using the same attribution table.
4. Dual-interpreter snapshot evidence, then freeze as its own round.
