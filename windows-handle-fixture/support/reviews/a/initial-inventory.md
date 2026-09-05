# Review A pre-coverage invariant inventory

Recorded before opening `coverage.md` for FIX round `r001`.

Candidate identity expected from the cold-review request:

- ref `refs/heads/review/windows-handle-fixture/r001`
- commit `76309774b551a874b8f9c677bc59e51299cee0e4`
- parent/base `5e56e4454f7b8ccb360d3e36245abc33318349bb`
- tree `f7d2451c20e417967864718b3d000a3eb60387e9`
- manifest SHA-256 `755c34175c060a4f0ef55616c9e52e336989645763cb16c0fd5a26293a7a37a6`

Independently observed changed surface:

- `tests/test_inventory_and_profiles.py`, modified, `+351/-100`
- `tests/test-inventory.json`, modified, `+1/-1`
- No production, codec, analyzer, CI, status, or decision path differs from the base.
- Both packet files have the same raw Git object id and SHA-256 as the frozen blobs.

Affected invariants and related-path inventory:

1. The numeric reuse seam is confined to a module-local `ctypes` facade. It must not mutate
   process-wide `ctypes`, production owner state, disposition state, or cleanup state. The facade
   must be restored on normal exit and exceptional exit.
2. Only Windows directory `CreateFileW` acquisitions carrying
   `FILE_FLAG_BACKUP_SEMANTICS` and `NtCreateFile` outputs are tokenized. Ordinary no-follow
   path reads must remain native because `msvcrt.open_osfhandle` takes ownership of the real
   handle.
3. Every token denotes exactly one live native handle. Tokens are unique, retired tokens never
   fall through as native handles, token/native numeric ranges cannot collide, and reassignment
   transfers rather than duplicates the replacement ownership entry.
4. Handle-bearing arguments must be translated at every governed ABI site: ordinary first-handle
   arguments; `OBJECT_ATTRIBUTES.RootDirectory` for `NtCreateFile`; and
   `FILE_RENAME_INFORMATION.RootDirectory` for rename/link calls. Function signatures, native
   return values, status values, error values, IO, flush, rename/link/disposition behavior, and
   namespace effects remain native.
5. Close reaches native Windows before a token is retired. A failed native close remains owned.
   A wrapper that raises after a successful consuming close leaves a retired token eligible for
   deterministic reassignment. Cleanup must never replay that retired numeric value against the
   replacement.
6. Every successful native acquisition is either transferred unchanged to CRT or published as
   one live token. Publication/range-validation failure raw-closes the unpublished acquisition.
   Context teardown raw-closes every unexpected live acquisition but still fails the test, and
   reports fallback-close failures without losing the body failure as context.
7. Replacement survival is established against the captured native replacement handle through
   original `GetHandleInformation` and `GetFileInformationByHandleEx` functions, bypassing the
   token facade. The oracle checks both liveness and stable native identity. Explicit final
   cleanup must close the native resource and leave the table empty.
8. The negative control must introduce a replay while the real writer and cleanup-manager retry
   path runs, must actually close the captured native replacement through the production close
   helper, and must be rejected by the raw survival oracle rather than token bookkeeping.
9. All original controlled-reuse schedules must still execute:
   - writer roles: `staging`, `published`, `recovery`, `directory`, `deterministic_lock` (5);
   - pre-bound owner families: `staging`, `original`, `recovery`, `published`, `readback`,
     `published_disposal` (6);
   - disposition/same-inode families: `staging`, `published_disposal`, `recovery` (3).
   Total: 14.
10. Each schedule must retain its original ownership, identity binding, rollback/namespace,
    retry-manager, and artifact assertions while adding deterministic token reuse plus the raw
    native replacement-survival check. The hardlink schedules must use a real same-inode alias;
    the directory case must use a real directory replacement.
11. Tests outside the three governed helper methods remain on their prior native path. Inside the
    helpers, non-reuse controls retain their substantive behavior. Inventory/profile changes are
    mechanically consequent only.
12. The adapter stays within the 200-nonblank-line cap and introduces no production seam or proof
    framework. Changed bytes remain LF-only, BOM-free, trailing-whitespace-free, and within the
    repository's 100-column rule.
13. Required executable evidence is Windows-native, in retained fresh D:-local snapshots, with
    `python -B -P`, snapshot-root cwd, snapshot `PYTHONPATH`, scrubbed environment, and an
    absolute validated Git executable. CPython 3.11.15 runs before CPython 3.14.6.

Initial adversarial questions to resolve after this record:

- Does the replay mutant reach and independently sensitize all materially distinct owner paths,
  or does the first failing subtest terminate a multi-family helper before later schedules run?
- Does failed `NtCreateFile` output handling preserve native status/ownership semantics without
  publishing a stale or invalid output value?
- Do native final-close and teardown checks prove closure independently, including body-error and
  raw-close-failure paths, without self-confirmation through the token table?
- Do the 14 schedules execute exactly once under controlled reuse and preserve the original
  schedule-specific assertions?
