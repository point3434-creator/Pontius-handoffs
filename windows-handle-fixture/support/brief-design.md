# Controlled Windows handle-reuse fixture repair

Tier C. Controller-authorized bounded repair; no production change.
The controller explicitly permits controlled handle-reuse simulation at the
Windows API boundary for these fixtures, while retaining the real writer,
ownership/cleanup execution, native resources, and independent resource checks.
This is a task-local exception to CLAUDE.md rule 8, not a general relaxation.

## Inputs and scope

Base: frozen codec r002 commit 5e56e4454f7b8ccb360d3e36245abc33318349bb,
manifest 6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5.
Use a separate no-hardlinks D-local clone; never mutable codec authoring bytes.
Allowed code surface: tests/test_inventory_and_profiles.py, specifically the
three handle-reuse helpers and their test-only adapter/negative controls.
Only mechanically consequent inventory/profile and self-census expectations
may change elsewhere within the test and its generated files. No analyzer,
codec, runtime, CI, status, decision, or existing packet modifications.
Only codec source acceptance waits on this task. No operating/research authority.

## Ground truth and acceptance

The production invariant is that cleanup after a consuming-but-raising close
must not close a replacement resource through the reused number. Windows must
actually perform acquisition, IO, identity, close, rollback, and namespace work.
Previously retained baseline and r002 receipts demonstrate failure to establish
the required same-number reuse within 4096 allocations; they remain failures.

Acceptance: all existing role/family cases execute with controlled reuse,
replacement resources remain natively open with the required identity, cleanup
ownership/rollback assertions remain, and deliberately replaying a close fails
the resource-survival check through the real writer path. Native tests outside
these three helpers remain native. Run focused controls, full inventory suite,
then the existing 19-command codec acceptance population, floor 3.11.15 first
and 3.14.6 second, fresh snapshots, -B -P, scrubbed environment, absolute Git.

## Mechanism and seams

A test-local handle table allocates synthetic tokens for native handles returned
by CreateFileW and NtCreateFile. The private secure-filesystem module receives
a ctypes facade, not a process-wide ctypes mutation. Its WinDLL functions map
tokens to live native handles, including RootDirectory in object attributes and
rename structures. Function signatures and return/error values are preserved.
Ordinary native handles from CRT operations pass through, with explicit range
collision refusal. Closed tokens never fall through as native handles.

Close delegates to Windows before retiring a token. A fixture may reassign a
fresh replacement resource to a retired token only after that close succeeded.
It never mutates a production owner, identity, disposition, or cleanup state.
Real OS allocation may reuse the old native number or choose another; neither
affects the deterministic token schedule. The adapter does not veto a replay:
a bad second close must reach the replacement and make its survival check fail.

Enumerated coverage: the four allocation loops in
_final3_windows_writer_reused_handles_are_role_isolated (file and directory),
_round7_windows_file_owners_bind_before_caller_failure, and
_round9_windows_disposition_absence_beats_same_inode_reuse. Their existing role
lists define the fixture population, not a claim of all Windows schedules.
The facade lasts through each helper's cleanup and is always restored. No
silently forced owner resolution or fabricated successful native return values.

## Risks, alternatives, and stop rule

Main risks: missed handle-bearing arguments; stale token/native collisions;
API last-error clobbering; a facade hiding a replay; leaked native handles;
analysis self-census churn. Check real resources and negative controls, not
just adapter bookkeeping. No dependency or production API change is needed.
Rejected: more retries, retry-until-green, weakening assertions, treating a
non-reused handle as ABA coverage, or a general fake filesystem.
The claim is deterministic production cleanup under simulated numeric reuse,
not deterministic behavior of Windows' handle allocator.

Budget: adapter at most 200 nonblank lines, no new proof framework; at most
three manual fixture helpers changed plus focused controls and mechanical
census regeneration. One implementation round and at most one correction;
stop for controller direction if the adapter needs broader native emulation,
production edits, weakened coverage, or a second residual on the same contract.
Two independent design checks and two fresh-context implementation reviews;
reviewers are disjoint between design and implementation. All candidates and
failures retained. No integration/source seal/commit/push is authorized.
