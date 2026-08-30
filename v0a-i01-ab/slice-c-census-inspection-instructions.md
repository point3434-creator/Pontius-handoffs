# Read-only final-snapshot test census inspection

Prepared for the coordinator; not run against the final corpus here. The helper
and launcher received syntax-only checks, not execution validation. They modify
no source, generated pair, capability record, or Git configuration. The helper
writes JSON to stdout; the launcher saves it with create-new semantics outside
the snapshot. It rejects reparse directory ancestors for source/temp/output paths;
concurrent arbitrary namespace mutation is outside this cooperative helper scope.
No generator CLI or test assertion is invoked or patched.

After all A/B/C bytes are settled and the authorized generator has refreshed the
inventory/profile pair, use that fresh D-local disposable clone. Its `.git` must
be a directory, not a linked-worktree file. Set the following to real existing
paths; use a new output filename for every observation. Execute in PowerShell 7:

```powershell
$Snapshot = 'D:\Pontius-worktrees\<final-disposable-clone>'
$Temp = 'D:\Pontius-worktrees\<final-disposable-parent>\temp'
& 'D:\Pontius-handoffs\v0a-i01-ab\slice-c-run-census-inspection.ps1' `
  -SnapshotRoot $Snapshot -ExpectedVersion '3.11.15' -TempRoot $Temp `
  -OutputPath 'D:\Pontius-handoffs\v0a-i01-ab\slice-c-combined-census-311-01.json'
```

The launcher selects the actual declared slot, scrubs the environment, uses
`-B -P`, sets cwd to the snapshot and `PYTHONPATH=<snapshot>/src`, configures
absolute Git and D-local TEMP/TMP, and disables global/system Git configuration.
The helper verifies these conditions before exact-path import of the snapshot's
real generator. Run actual 3.11.15 first. After its result is inspected, repeat
with `-ExpectedVersion '3.14.6'` and a distinct output path, using the separately
captured final 3.14 snapshot where applicable.

The helper matches
`CheckedInInventoryTests.test_working_discovery_binds_every_entry_and_introduced_id`:

- Secure captured test sources with `include_support_modules=False`, exactly
  equivalent to that test's `_working_sources(root)` corpus. This deliberately
  differs from the generator publication path's support/probe-inclusive corpus.
- Item universe from the actual inventory assignments, lifecycle fixtures, and
  profile payload probe IDs, following the test's `core/current/gpu` membership
  rules. It does not substitute the generator's `_item_universe` helper.
- The real `derive_design_review` with the pinned baseline commit/tree and the
  current inventory bytes; no monkeypatches, approvals, or capability grants.
- Captures and final revalidation of test sources, generator/sibling, inventory,
  and profiles. Source raw/canonical hashes and runtime identity are reported.

Use `analysis_census`, `expanded_row_count`, `blocker_count`,
`blocker_reason_counts`, and `blocker_locations_by_reason` to inspect mechanical
expectation deltas. Each location list retains production order and duplicates,
matching the test's list comprehensions. `review` contains full expanded rows,
deny-all rows, blockers, existing derivation receipt, and their digests. The
presence of capability-shaped review data is inspection only, never approval.

Retain each JSON output and attribute every expectation change. After editing
expectations, recapture the changed test bytes and rerun inspection under a new
output name: line-bound and string-decoy digests may change. Then run the actual
inventory/profile suite and generator `--check` under the required snapshot
procedure. This helper does not establish freshness or acceptance by itself.
