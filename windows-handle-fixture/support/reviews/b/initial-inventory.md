# Reviewer B blind invariant inventory

Recorded before opening `coverage.md`.

Candidate identity independently observed from the frozen repository:

- base `5e56e4454f7b8ccb360d3e36245abc33318349bb`
- commit `76309774b551a874b8f9c677bc59e51299cee0e4`
- tree `f7d2451c20e417967864718b3d000a3eb60387e9`
- changed paths: `tests/test_inventory_and_profiles.py` and
  `tests/test-inventory.json` only
- blob-derived manifest SHA-256
  `755c34175c060a4f0ef55616c9e52e336989645763cb16c0fd5a26293a7a37a6`

## Invariant

After a consuming-but-raising close, production cleanup must never replay the
retired numeric handle onto the native replacement now represented by that
number. The controlled number may be synthetic at the private ctypes boundary,
but acquisition, I/O, identity, disposition, rename, close, rollback, and
namespace behavior remain native. A pass therefore requires the replacement's
captured native handle and identity to survive the real writer/cleanup path;
adapter bookkeeping is not an oracle.

## Related paths found independently

The changed source replaces four native allocation loops:

1. file-handle reuse in
   `_final3_windows_writer_reused_handles_are_role_isolated`, for staging,
   published, recovery, and deterministic-lock owners;
2. directory-handle reuse in that same helper;
3. file-handle reuse in
   `_round7_windows_file_owners_bind_before_caller_failure`, for staging,
   original, recovery, published, readback, and published-disposal families;
4. same-inode hardlink handle reuse in
   `_round9_windows_disposition_absence_beats_same_inode_reuse`, for staging,
   published-disposal, and recovery families.

All three helpers are reached through
`test_windows_persistent_close_failures_are_truthful_and_retryable` while the
private secure-filesystem module's `ctypes` binding is replaced by the facade.

The facade must route these handle-bearing calls used by the real paths:

- `CreateFileW`: tokenize directory opens carrying
  `FILE_FLAG_BACKUP_SEMANTICS`; leave ordinary file-read handles native for
  `msvcrt.open_osfhandle` ownership transfer;
- `NtCreateFile`: translate its `OBJECT_ATTRIBUTES.RootDirectory` token and
  publish a successful native output as a token;
- `NtSetInformationFile`: translate the primary handle and the embedded
  `RootDirectory` for rename/link information classes 10 and 11;
- `CloseHandle`, `GetHandleInformation`,
  `GetFileInformationByHandle`, `GetFileInformationByHandleEx`, `ReadFile`,
  `WriteFile`, and `FlushFileBuffers`: translate the primary handle;
- `ReplaceFileW`: forward unchanged because it is path-bearing, not
  handle-bearing.

The acquisition boundary must reject the token/native range collision and
raw-close an acquired native handle if validation or publication fails. A
retired token must resolve only to invalid handle zero unless explicitly
reassigned; it must never fall through as an OS handle. Reassignment must move,
not copy, one ownership entry. A delegated close retires an entry only after
native success. Native failures and their last-error/NTSTATUS results must be
observable unchanged by production.

The independent oracles are the original pre-facade
`GetHandleInformation`, `GetFileInformationByHandleEx`, and `CloseHandle`
functions applied to captured native handles. Teardown must restore the module
binding, raw-close every remaining adapter-owned native handle, fail on any
unexpected live entry even when fallback close succeeds, and retain a body
exception as cause. The real `read_regular_snapshot` path is the affected CRT
transfer control.

## Initial challenge points

- Check error preservation for every failing forwarded Win32 call, including
  `CreateFileW` and `CloseHandle`, and refusal before native dispatch for
  retired/unknown synthetic values.
- Check publication failure both for directory `CreateFileW` and
  `NtCreateFile` output handles, including output-pointer neutralization.
- Check that the mutation control actually reaches the real cleanup path and
  a raw native survival oracle rather than failing from token bookkeeping.
- Check whether its four mutation rows are sufficient for the positive
  role/family population or leave a materially distinct cleanup mechanism
  untested.
- Check that successful ordinary `CreateFileW` handles are never table-owned
  and transfer to CRT exactly once.
- Check deterministic teardown after body failure and raw-close failure, with
  facade restoration and the primary error relationship preserved.
