# Design correction 1: retain native CRT file-handle ownership

Applies to brief-design.md SHA-256
cae851310c2517106a3bddd7fba36fa154f751bc85b2e323d86fb69da9682022.
The original brief is retained unchanged. Design reviewer A identified the
CreateFileW -> msvcrt.open_osfhandle transfer used by read_regular_snapshot.

Only CreateFileW calls with FILE_FLAG_BACKUP_SEMANTICS (0x02000000) receive
synthetic tokens. These are the directory opens in the governed path. Ordinary
path-read handles remain native and transfer directly to CRT ownership; no
msvcrt, os.open, or os.close facade is introduced. NtCreateFile outputs remain
tokenized. The adapter checks native/token range separation for all created
handles, including those handed to CRT, and forwards native CRT handles in
identity calls unchanged. A real read_regular_snapshot control verifies this
transfer, reading exact bytes and leaving no adapter-owned resource behind.

This narrows the API routing mechanism, without changing the controller's
approved scope, resource-survival contract, test population, or size budget.
