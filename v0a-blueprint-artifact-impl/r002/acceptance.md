# Codec r002: implementation reviewed; final acceptance BLOCKED

The codec implementation has two independent CLEAN technical reviews. The
post-review acceptance population is NOT passing, so r002 is not source-sealed,
adopted, published, committed to the primary branch or authorized for operation.

## Candidate identity

- Commit: 5e56e4454f7b8ccb360d3e36245abc33318349bb.
- Base: c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98.
- Tree: dc18ed133504fe6c7677b494bcefba311cc73704.
- Manifest SHA-256:
  6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5.

Use this frozen Git object and files/ overlay, not the mutable authoring clone.
The unadopted later test-format revision is excluded; provenance-note.md,
provenance-clarification.md and the implementation issuer's separate clarification
retain the exact distinction. Both reviewers knew the limitation.

## Results

| Evidence | Result |
| --- | --- |
| Independent review A | Spec PASS, Quality PASS, C/I/M0/0/0, CLEAN, SOUND |
| Independent review B | Spec PASS, Quality PASS, C/I/M0/0/0, CLEAN, SOUND |
| Exact final codec suite, normal and min640 on both slots | 7/7 methods in each of four runs |
| Complete CPython3.11.15 acceptance | 18/19 commands pass; inventory suite fails |
| Complete CPython3.14.6 acceptance | 18/19 commands pass; inventory suite fails |
| Combined broad result | 36/38 commands pass; NOT accepted |
| Broad unittest population | 492 methods per slot, one POSIX-only skip per slot |
| Post-run source identity | All12 frozen files match in all38 snapshots,456 comparisons |
| Scope and budget | 290source lines,300test lines,1699fixture bytes,97manual registration lines |
| Registration | 2828old rows unchanged;23exact additions;zero capability grants |

The failures are subcases of the existing Windows
test_windows_persistent_close_failures_are_truthful_and_retryable, whose setup
expects the OS to reuse a selected numeric handle. The floor fails one readback
subcase; the development slot fails directory-role and recovery subcases. A
bounded trace observes4096 unsuccessful replacement attempts and reproduces the
same unmet setup precondition on the untouched base. Untraced baseline controls
also pass, so this is not a claim of timing-independent failure or an automatic
waiver. See acceptance-blocker.md for exact evidence and limits.

All other broad commands pass, including codec, real runtime/replay/reader,
source-boundary, status and standalone unchanged inventory generation checks.
The one skip is the existing POSIX directory-descriptor mutation test on Windows.
No test was edited, skipped or loosened to obtain these results. No broad rerun
was used to replace a failed result with green.

## Traceable records

- reviews/a/review.md SHA-256:
  e84ad0fffd6378f19ed4e7ccd20b599d381365d544f96fed86894fdf18846588.
- reviews/b/review.md SHA-256:
  af42a16c4fa2c9d0258ca37298532fd8875e9381f77864158594532713acda94.
- acceptance-results.json records every broad command, actual exit, count,
  snapshot-file comparison and receipt SHA-256. Its original absolute receipt
  paths are retained; identical portable copies are in evidence/ by basename.
- evidence/ also preserves the applicable four exact final codec receipts,
  historical behavioral REDs and bounded baseline/candidate diagnostics.
- manifest.sha256 binds the twelve raw changed Git blobs. The independent
  verify-frozen.py audit was rerun after all tests and still matches.

## Next boundary

Keep this reviewed codec fixed. The recommended next task is a separately
authorized bounded repair of the existing Windows test's reuse setup, retaining
its ownership invariant, followed by the required acceptance run. Do not create
a third codec correction or silently expand the registration-only exception to
test behavior. Do not increase4096, waive the failing gate, or reopen the parked
analyzer, freeze classifier, strategy, research or operating lanes in this round.

Primary HEAD remains c4af7f6 and its tracked tree/index are unchanged. No push,
remote publication, source seal, strategy-strength claim or operating run occurred.
