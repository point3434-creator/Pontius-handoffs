# Publication/accounting correction — Stage0 draft

2026-08-30, Codex. Separate Tier-C FIX R2-04/R2-09/R2-10 after trace/legal
correction. Root drafts; requires read-only plan review before production edits.
Scope runtime.py, replay.py, trace.py and existing four focused test files as
necessary to replace timing observers. No C/manifest/inventory/CI or sealed edit.
Expected 800-1,400 changed lines; split if size discovery requires it.

Invariants: each non-response host interval closes once through the real public
outer ledger; terminal-at-entry determines its category. Serialization and required
row writes finish before next input; first write failure after delivery stops input,
preserves deliveries/incomplete bytes and never claims complete trace publication.
Terminal construction/serialization/write is a distinct final interval, then finalize.
Stable directory authority governs creation; no pathname check/use reparse escape.

Shape: one owned incremental TraceWriter with append/finish/close state. Lazily
create destination at first post-dispatch flush (header and first outcome rows);
keep one descriptor for all following row writes. No path reopen, overwrite, retry,
or delete-on-failure. All-bytes/short-write checks and explicit close-once ownership.
Keep write_trace convenience function using this same writer, no second protocol.
In-memory path uses the same serialized rows without a fake filesystem claim.

Host: factor feed to one dispatch/outcome-record/serialize/flush sequence. Required
rows serialized/flushed under owned_bookkeeping after dispatch closure and before
next event acquisition. Measure event construction, header construction, semantic
computation and settlement/oracle work as explicit public-ledger intervals; exclude
separately declared pre-run fixture/tool setup and post-receipt reporting. Initialize
outer ledger before first host interval so header work is measurable; first dispatch
reuses it. Preserve policy identity binding inside first dispatch. Check cause journal
after each real interval and stop input on any fault. Separate terminal reporting may
continue fail-closed when source is dead, but cannot claim measured accounting.
Build semantic digest under bookkeeping before reading terminal's accounting totals.
Close writer inside final publication before finalize; body/cleanup failures retained
by occurrence and order with no unsafe exception rendering. Never replace prior cause.

Windows stable creation: stdlib ctypes NtCreateFile with relative ObjectName and
RootDirectory directory handle, OBJ_DONT_REPARSE and FILE_CREATE; directory authority
admitted with no-reparse native open, retain parent authority until child handle owned.
Check actual file/directory attributes and every necessary NTSTATUS/WinError. Avoid
mixing os.stat/FileIdInfo identities. Reject non-local/device/alternate-stream/path
aliases not supported by safe protocol; do not silently follow or fallback. Investigate
whether an absolute NT path containing the DOS-device symbolic link needs component
opening rather than OBJ_DONT_REPARSE at that outermost name. No assumption becomes
acceptance without real Windows tests. Other platforms either equivalent dir_fd
no-follow walking or explicit unsupported typed refusal; Windows is acceptance host.
Sources: https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntcreatefile
and https://learn.microsoft.com/en-us/windows/win32/api/ntdef/ns-ntdef-_object_attributes.

Category discovery: enumerate header/event/decision/failure/semantic/settlement/terminal
host work and all writer open/append/finish/close failure points; observer expectations
come from actual public ledger intervals, not runtime totals. RED on rejected source:
real serializer/syscall profile cost absent from totals; destination absent after first
decision; real existing-file refusal permits second action; real parent rename+junction
replacement between checked parent and creation writes outside root. Opposing controls:
normal relative/nested/absolute destination, existing leaf unchanged, missing directory,
root/child/leaf junctions, first failure preserves accepted delivery and stops next input,
partial/incomplete file refused by parser/checker, correct separate terminal cut and
higher-order source/body/cleanup cause sequences. Use observed real public operations,
not helper doubles or private bookkeeping. Native resource ownership checks must
exercise actual handles, including failures; finite schedules, no exhaustive claim.

No operational limits/performance/GPU/source-seal/rehearsal/research owner or ceremonial
source integration authorized. All floor-first focused runs use fresh D-local snapshots;
frozen candidate and independent Tier-C reviews follow. Preserve r001/2 and value closure.
