# Independent Tier C design review A

## Review identity

- Original design: `brief-design.md`
- Original SHA-256:
  `cae851310c2517106a3bddd7fba36fa154f751bc85b2e323d86fb69da9682022`
- Retained correction: `design-addendum-1.md`
- Correction SHA-256:
  `00a9acb667102562f3a4019f9359c0271216bc91f3ffb5d41c77ffcfb346f9f9`
- Source reviewed: authoring commit
  `5e56e4454f7b8ccb360d3e36245abc33318349bb`
- Review mode: independent read-only source inspection; no implementation and no
  test execution.

## Original finding retained

### I-1 — All-`CreateFileW` tokenization crosses an unfacaded CRT ownership seam

Severity: Important. Confidence: High. Status: resolved by the retained
addendum.

The original design says that native handles returned by both `CreateFileW`
and `NtCreateFile` receive synthetic tokens, while only the private
secure-filesystem module's `ctypes` binding receives a facade
(`brief-design.md`, lines 39-45).

The real writer necessarily calls `secure_filesystem.read_regular_snapshot`
after writing the staging file and again after publication
(`tools/generate_test_inventory.py`, lines 6797-6801 and 6855-6858).
On Windows that reader obtains a handle through `CreateFileW` and immediately
transfers that exact numeric value to the unfacaded
`msvcrt.open_osfhandle` (`tools/generate_dependency_baseline.py`, lines
842-864). Under the original rule, CRT would receive a synthetic token instead
of the native handle it must take ownership of.

Concrete failure scenario: the real writer reaches the staging snapshot;
`CreateFileW` succeeds but the facade substitutes a token; CRT attempts to
adopt that token and fails, or could target an unrelated native handle if an
undetected collision existed. The writer then aborts before the intended
consuming-close/reuse schedule. This would be a fixture false negative, not
evidence about the ownership invariant.

Required outcome: preserve the native handle across the
`CreateFileW -> msvcrt.open_osfhandle -> os.close` ownership chain, while still
virtualizing the directory and `NtCreateFile` handles used by the controlled
reuse schedules.

Resolution assessment: `design-addendum-1.md`, lines 8-15, closes the seam.
It tokenizes `CreateFileW` results only when the call contains
`FILE_FLAG_BACKUP_SEMANTICS` (`0x02000000`), which is present in the governed
directory open. The ordinary path-read open uses flags
`0x00200000 | 0x08000000`, so its native handle remains native through CRT
ownership and later `os.close`. `NtCreateFile` outputs remain tokenized. The
addendum also requires range separation for the native CRT handles, native
pass-through for their identity queries, and a real exact-byte snapshot
control with no adapter-owned residue. No broader native emulation is needed.

## Bounded design checks after the correction

### API forwarding

The amended split fits the APIs reached by the four allocation loops:

- directory `CreateFileW` results may be tokenized; ordinary path-read
  `CreateFileW` results remain native;
- `NtCreateFile` translates an object-attributes `RootDirectory` token and
  publishes a token for its live output handle;
- `NtSetInformationFile` translates both its direct handle and the embedded
  `RootDirectory` for rename/link information;
- `WriteFile`, `FlushFileBuffers`, `ReadFile`, `GetHandleInformation`,
  `GetFileInformationByHandle`, `GetFileInformationByHandleEx`, and
  `CloseHandle` translate direct token arguments and forward native arguments;
- the supplied signature/result/last-error preservation rule and explicit
  refusal of unknown APIs prevent an omitted call from silently succeeding.

Implementation review must confirm that temporary embedded-handle
translations are restored on every exit path and that a valid handle returned
alongside a failing `NtCreateFile` status is still entered in the token table
before the production owner inspects it.

### Identities and test sensitivity

The design keeps identity authority at the native boundary. File owners use
the native file identity returned through `GetFileInformationByHandleEx`;
directory owners use the existing directory identity calls; the round-9
hardlink case intentionally preserves file identity while absence of the
owned namespace entry resolves disposition. The adapter neither supplies an
identity nor changes an owner, disposition, or rollback state.

The close order is also suitable for the negative control: the first close
must reach Windows and succeed before the token is retired and reassigned. A
replayed close is not intercepted, so it reaches the replacement's native
handle. The implementation review must require the promised native
open/identity checks and replay-negative control to observe the underlying
resource, not merely the table's active/retired state. That requirement is
already explicit in the brief and does not require a new proof framework.

## Verdict

- Original design defect count: **C=0, I=1, M=0**.
- Resolution: **I-1 resolved** by
  `design-addendum-1.md` SHA-256
  `00a9acb667102562f3a4019f9359c0271216bc91f3ffb5d41c77ffcfb346f9f9`.
- Unresolved defect count for the amended design: **C=0, I=0, M=0**.
- Defect verdict: **PASS** for implementation.
- Design verdict: **SOUND**. The private, selectively routed facade now fits
  the four declared loops without intercepting CRT ownership or weakening the
  real writer, cleanup, namespace, resource, or identity boundaries.

This verdict is design-only. It does not establish implementation correctness,
test success, codec acceptance, source sealing, integration, or operating
authority.
