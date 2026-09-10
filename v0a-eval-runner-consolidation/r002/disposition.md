# Disposition of r001 F1

Accepted. The original cold verdict is NOT CLEAN / NOT SOUND and remains unchanged.
F1 is Medium / P2, high confidence. The author confirmed the reachable signal window against
the frozen source and the explicit interruption contract before making this repair.

The recorder previously copied its signal list and calculated a successful outcome while its
handler still deferred new signals. SIGINT arriving immediately before the final file write
could therefore be omitted and the invocation could return 0. The child had already exited.

The handler now has two phases. It defers through child execution and evidence collection,
then switches to raising KeyboardInterrupt before the final signal snapshot. The finalization
try block encloses that switch, snapshot, serialization, file write, summary and return.
An interruption unwinds publication, emits an explicit stderr diagnostic, and returns 99 after
a successful child or preserves a nonzero child exit. Previous handlers are restored on exit.

The regression uses real signal delivery through signal.raise_signal and the original writer.
It exercises SIGINT and SIGBREAK, child exits 0 and 7, and interrupts before file open and during
the final fsync. All eight subcases failed against the exact retained r001 launcher. They pass
with the repair. The assertions include restored handlers, consumed claims, refusal of a second
invocation, one launch only, and no outcome file for the pre-open interruption.

Fresh affected verification: 44 cases, zero skips, pytest exit 0 in 60.01 seconds. The 32 launcher,
10 completion and two protocol cases include both disposable real-host compatibility campaigns.
The existing full-manifest result belongs to r001; it was not rerun for this small repair.

An interruption during a write can leave partial or already-written JSON. The repair does not
overwrite it or infer success from it: invocation exit status remains authoritative, and the
diagnostic identifies the interrupted finalization. Multiple forced interruptions, hard kills
and machine failure still may prevent graceful recording; no atomic file-plus-process-return
transaction is claimed. The claim remains consumed in all such cases.

The exact prior report, RED launcher/test bytes, RED receipt, final GREEN receipt and source
identities are retained in this packet. Author status: repaired and verified on the stated
scope, pending opposing review and separate controller adoption. No retained invocation,
repository-work commit or push was performed.
