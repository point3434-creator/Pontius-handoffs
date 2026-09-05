# r002 review A initial correction inventory

Recorded before opening `correction-coverage.md`.

Candidate: `c7de23de276c50463d831f3983fede82a5400ce8`

The r001 required correction is strictly exactness hygiene: reflow the five
identified over-100-column expressions in `tests/test_inventory_and_profiles.py`
without changing their executable meaning. The source-byte change may alter only
the mechanically derived `string_sink_decoy_sha256` expectation. The checked-in
inventory must remain byte-identical to r001, and no production, codec, analyzer,
runtime, CI, status, decision, or profile bytes may change.

Independent raw `r001..r002` inspection found six source edit sites:

1. `_ControlledWindowsHandles.__exit__`: one assertion-message f-string split
   into two adjacent f-strings.
2. `test_windows_controlled_reuse_preserves_native_resources`: the controlled
   reuse `assertEqual` arguments wrapped over multiple lines.
3. The same test: the retired-replacement `assertFalse` call wrapped over
   multiple lines.
4. `test_windows_controlled_reuse_detects_production_replay`: the
   `assertRaisesRegex` context-manager call wrapped over multiple lines.
5. `test_windows_controlled_reuse_releases_unpublished_and_leaked_handles`: the
   `assertRaisesRegex` context-manager call wrapped over multiple lines.
6. `CheckedInInventoryTests`: only the `string_sink_decoy_sha256` literal changed,
   from `37b750...9ed2` to `c62e27...372e`.

The frozen r001-to-r002 path set is one modified path,
`tests/test_inventory_and_profiles.py`, at `+15/-6`. There is no r001-to-r002
change to `tests/test-inventory.json`, `tests/test-profiles.toml`, writer,
secure-filesystem production code, codec, or analyzer. Verification must still
establish raw blob identity, equivalent executable AST after excluding the
mechanically derived census literal, no newly added line over 100 columns, exact
r001/r002 inventory-byte equality, unchanged codec/analyzer blobs, and fresh
focused Windows runs on CPython 3.11 before 3.14.
