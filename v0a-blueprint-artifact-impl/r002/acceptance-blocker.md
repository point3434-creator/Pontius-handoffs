# Post-review acceptance blocker: native handle-reuse fixture

Frozen codec r002 is independently reviewed CLEAN by both reviewers, but full
acceptance is not passing. This note is a controller diagnostic record, not a
replacement review verdict or permission to alter the existing test.

Candidate: 5e56e4454f7b8ccb360d3e36245abc33318349bb.
Manifest: 6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5.
Unchanged source-opening base: c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98.

## Observed failure and source trace

The first complete post-CLEAN CPython 3.11.15 acceptance pass finishes 18/19
commands successfully. Command 10, tests/test_inventory_and_profiles.py, runs
88 methods and fails its readback subcase of
AtomicAndGitBoundaryTests.test_windows_persistent_close_failures_are_truthful_and_retryable.
At candidate line 26179 the assertion compares replacement=None with the selected
handle 8972. Receipt: run-records/broad-r002-10-311.json. Native permissions were
used; this is not the earlier sandbox hardlink-access failure.

The failing helper, _round7_windows_file_owners_bind_before_caller_failure, closes
the selected native handle, opens up to 4096 replacement handles while retaining
nonmatching handles, and requires that one replacement equal the selected numeric
handle. Failure occurs because this setup never obtains the required reuse.
The writer/test bodies governing that behavior are unchanged by the codec round;
their only file-level diffs are approved registration constants and later census
expectations. No codec API is invoked by this selected test.

The complete CPython 3.14.6 inventory-suite receipt also fails the same test
method, with two subcase failures: reused_writer_role='directory' in
_final3_windows_writer_reused_handles_are_role_isolated (line25886, replacement
None vs540, "native handle was not deterministically reused") and
prebound_owner_family='recovery' in the first helper (line26179, None vs15204).
Receipt: run-records/broad-r002-10-314.json, 88 methods in198.100seconds, exit1.
These are observed related reuse-setup paths; only the first helper received
the bounded trace diagnostic below. No stronger claim is made for the second.

## Fixed, bounded diagnostic comparison

All runs are fresh snapshots on exact CPython 3.11.15, -B -P, scrubbed environment,
native permissions. Baseline snapshots use no candidate overlay. No tested file
or installed dependency was edited. The diagnostic script only observes the test
process through sys.settrace; tracing can affect execution, so its result is not
an acceptance pass or a timing-independent reproduction claim.

| Run | Result |
| --- | --- |
| baseline-handle-reuse-diagnostic-311 | Original selected test PASS, 1 method. |
| candidate-handle-reuse-diagnostic-311 | Frozen r002 selected test FAIL in original, recovery and published_disposal subcases; replacement remains None. |
| baseline-atomic-class-diagnostic-311 | Original entire AtomicAndGitBoundaryTests class PASS, 38 methods. |
| candidate-handle-cause-diagnostic-311 | Traced frozen test FAIL; recovery and published observations each show close_attempts=1, replacement=None, replacement_blockers=4096. |
| baseline-handle-cause-diagnostic-311 | Same tracing on untouched base FAIL in readback; selected handle536, replacement=None, close_attempts=1, replacement_blockers=4096. |

The two traced runs used the identical diagnose-handle-reuse.py and unchanged
test behavior. The base's failing assertion is at line26176 (the registration
extension shifts the candidate's corresponding line by three).

This establishes that the failed reuse precondition can occur without the codec
changes. It does not prove why a particular process receives particular handles,
prove that production cleanup is correct under every schedule, or erase the
untraced candidate failures. No retries were used to claim acceptance success.

## Disposition

Retain r002, both clean reviews, every failed/successful receipt, and the unadopted
authoring test-format revision. Do not create a third codec correction, increase
4096, weaken/skip the assertion, waive the acceptance requirement, change the
analyzer or edit this sealed test's behavior under the registration exception.

Both complete acceptance populations are now finished: 18/19 commands pass on
each slot, 36/38 overall. All sixteen suites run 492 unittest methods per slot,
with one declared POSIX-only skip on this Windows host. Only the full inventory
suite fails. The independent post-run audit matches all twelve frozen files in
every one of the38 snapshots (456 file comparisons). See the packet's
acceptance-results.json for command exits and receipt hashes.

A separately authorized bounded repair of the existing native test setup is
the recommended next step, with its own scope and verification;
not a codec rewrite or another codec review loop. Source sealing/publication and
all operating permissions remain closed until the blocker is dispositioned.
