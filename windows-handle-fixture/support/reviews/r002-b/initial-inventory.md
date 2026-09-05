# r002 review B — pre-coverage inventory

Recorded before opening `correction-coverage.md`.

## Bound target

- Candidate ref: `refs/heads/review/windows-handle-fixture/r002`
- Candidate commit: `c7de23de276c50463d831f3983fede82a5400ce8`
- Raw commit parent/base: `5e56e4454f7b8ccb360d3e36245abc33318349bb`
- Raw commit tree: `014ee05a5014181bd63471247e5ee09607bb2346`
- Rejected predecessor: `76309774b551a874b8f9c677bc59e51299cee0e4`
- Base-to-candidate paths: `tests/test-inventory.json` and
  `tests/test_inventory_and_profiles.py`, both modified.
- Predecessor-to-candidate paths: only
  `tests/test_inventory_and_profiles.py`, modified (`+15/-6`).

## Independent correction invariant and sites

The sole r001 finding was five added lines over 100 columns. The correction
must only reflow those expressions, preserve their parsed behavior, update the
mechanically consequent string-decoy source digest, and leave the checked-in
inventory blob unchanged from r001.

The frozen r001-to-r002 diff has exactly six semantic locations:

1. `_ControlledWindowsHandles.__exit__` near r002 lines 21184–21185: one
   formatted error message is split into two implicitly concatenated f-strings.
2. `test_windows_controlled_reuse_preserves_native_resources` near lines
   21337–21339: the three positional arguments to `assertEqual` are vertically
   reflowed.
3. The same control near lines 21340–21342: the sole argument to `assertFalse`
   is vertically reflowed.
4. `test_windows_controlled_reuse_detects_production_replay` near lines
   21386–21388: the same exception class and regex arguments to
   `assertRaisesRegex` are vertically reflowed.
5. `test_windows_controlled_reuse_releases_unpublished_and_leaked_handles`
   near lines 21430–21432: the same exception class and regex arguments to
   `assertRaisesRegex`, with the same `as caught` binding, are vertically
   reflowed.
6. `CheckedInInventoryTests` near line 29918: only
   `string_sink_decoy_sha256` changes, from
   `37b7508932c784b6898999b2c024eeb8e004aa492b10cf1a948a1028f3cc9ed2`
   to `c62e275fa42bcb8cc9bef4a382990793adc03ecc9d9db1b6fcd35aeb9b23372e`.

No r001-to-r002 change exists in `tests/test-inventory.json` or in any other
path. The correction risks are accidental argument/value/order changes,
context-manager rebinding, a changed error string, an unjustified census
literal, or hidden scope growth.

## Independent full changed-surface inventory

Relative to the authorized base, the Python test blob contains:

- the `_RoutedWindowsCall` callable facade and `_ControlledWindowsHandles`
  token/native ownership table;
- three Windows-only controls for real native resource preservation, real
  production replay sensitivity, and unpublished/leaked native-handle cleanup;
- the existing final3, round7, and round9 helpers parameterized with the
  adapter; their four allocator-dependent reuse loops replaced by controlled
  token reassignment after a successful native close;
- raw replacement-survival assertions in all three governed helper families;
- one scoped adapter context around those three helpers in the existing
  full-inventory path; and
- the mechanically consequent `string_sink_decoy_sha256` expectation.

The generated inventory blob differs from base only in discovery counts and
digests plus three added stable IDs, one for each new Windows control; there are
no removed or modified stable-ID entries. The independently inventoried
positive population is five final3 roles, six round7 families, and three
round9 families (14 total), with both file and directory owner paths in final3.

The required rule-8-exception boundary remains: real native acquisitions,
I/O, identities, closes, rollback/namespace work, production owners/writer,
and facade-bypassing replacement oracles; only numeric handle reuse is
controlled. Ordinary path-read `CreateFileW` handles must remain native for
CRT ownership. Every tokenized native acquisition must be singly owned,
closed-on-publication failure, retired only after successful native close,
and raw-closed/fail-closed on adapter exit.
