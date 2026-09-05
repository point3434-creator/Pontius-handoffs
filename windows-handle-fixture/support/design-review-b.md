# Independent Tier C design review B

Review target:

- `brief-design.md` SHA-256
  `cae851310c2517106a3bddd7fba36fa154f751bc85b2e323d86fb69da9682022`
- `design-addendum-1.md` SHA-256
  `00a9acb667102562f3a4019f9359c0271216bc91f3ffb5d41c77ffcfb346f9f9`
- Existing source baseline: authoring HEAD
  `5e56e4454f7b8ccb360d3e36245abc33318349bb`

Review mode: read-only static source/design inspection. No fixture, test, or
production execution was performed, as required.

## Verdict

Defect verdict: **FINDINGS — NOT CLEAN**.

Finding counts (Critical / Important / Minor): **0 / 1 / 0**.

Design verdict: **STRAINED**. A private `secure_filesystem.ctypes` facade is a
bounded and suitable seam for deterministic numeric reuse, and addendum 1
correctly separates tokenized directory/NtCreateFile handles from native
CreateFileW handles transferred to the CRT. The shape nevertheless lacks an
explicit single-owner lifecycle for native handles held by the facade and an
independent raw-native observation boundary. Adding those two contracts is a
bounded correction; replacement or production redesign is not warranted.

## Important finding B-01 — adapter-held native handles lack total ownership
and an independent survival oracle

Severity: **Important**. Confidence: **High** (direct design omission and
source call-path inspection).

The brief requires native resources and independent resource checks, names
leaked native handles and a facade-hidden replay as principal risks, and says
only that the facade lasts through helper cleanup and is restored. Addendum 1
adds native/token range checks and a real CRT-transfer control. Neither frozen
document defines:

1. atomic transfer of each successfully acquired native handle into a
   close-once adapter owner, including rollback if token allocation,
   registration, range validation, or output-pointer publication fails;
2. fail-closed facade teardown that drains/raw-closes every still-owned native
   handle and verifies that no unexpected live mapping remains; or
3. a replacement survival/identity oracle that retains the underlying native
   handle and invokes the original raw Windows information APIs outside the
   facade's token translation.

This matters because the existing helpers observe replacement liveness and
identity through `_windows_governance_handle_is_open` and
`_windows_governance_handle_file_id`. Under the proposed facade, those calls
use the same translation table whose correctness they would appear to check.

Concrete failure scenario: native `CreateFileW` or `NtCreateFile` succeeds and
returns handle H; token registration, collision refusal, output-pointer
publication, or later test unwinding raises before a production owner can
close the token. Facade restoration discards the only H mapping, leaving the
native handle open. Separately, a stale or incorrect token mapping can direct
the production liveness/identity probes to a different open handle, allowing
the survival assertion to pass without establishing that the selected
replacement survived. The same self-reference can weaken the deliberately bad
replay control.

Required correction to the design:

- State that every successful native acquisition is immediately adopted by a
  close-once adapter owner before any fallible token work. Token publication
  transfers ownership only after registration succeeds; every pre-publication
  failure raw-closes H while preserving the primary error.
- State that facade exit performs deterministic raw-native cleanup of every
  adapter-owned live entry, restores `secure_filesystem.ctypes` in `finally`,
  and fails the control if an unexpected mapping/resource remains. Expected
  replacement cleanup must also be observed, not merely attempted.
- State that positive controls retain the native replacement value and use the
  original raw `GetHandleInformation` and full-width
  `GetFileInformationByHandleEx` (or an equivalent facade-bypassing native
  boundary) to establish its identity and survival after real writer cleanup.
  The negative control must make the deliberately replayed production close
  reach that replacement and then prove, through the same raw-native oracle,
  that the resource was actually closed. Adapter table state alone is not an
  oracle.

Verification criteria for implementation review:

- Inject one failure after native acquisition but before token publication;
  the raw native handle is closed and the primary/cleanup errors remain
  truthful.
- Each of the 14 existing role/family cases completes with the expected native
  replacement identity and survival observed outside facade translation.
- The bad-replay control closes that same native replacement and is detected by
  the raw-native survival check through the real writer/cleanup path.
- Every helper exit, including assertion/error exits, restores the private
  ctypes reference and leaves no unexpected adapter-owned live native handle.

## Scope and coverage assessment

The design otherwise preserves the required surface:

- all three named helpers remain in scope;
- all four allocation loops are accounted for: file and directory reuse in
  `_final3_windows_writer_reused_handles_are_role_isolated`, file reuse in
  `_round7_windows_file_owners_bind_before_caller_failure`, and hardlink/file
  reuse in `_round9_windows_disposition_absence_beats_same_inode_reuse`;
- the existing role/family lists retain 5 + 6 + 3 = 14 cases;
- addendum 1 keeps ordinary path-read CreateFileW handles native for
  `msvcrt.open_osfhandle`, tokenizes only BACKUP_SEMANTICS directory opens, and
  tokenizes NtCreateFile outputs;
- writer, ownership/rollback, files/namespaces, native IO/identity/close,
  codec, and analyzer boundaries remain unchanged by the stated scope; and
- the claims remain limited to deterministic production cleanup under
  simulated numeric reuse, not deterministic Windows allocator reuse or wider
  operating/research authority.

These points do not clear B-01 because native cleanup and oracle independence
are explicit acceptance conditions, not optional implementation details.
