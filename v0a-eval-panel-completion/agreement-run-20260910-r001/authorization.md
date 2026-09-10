# Controller authorization: one retained agreement invocation

Recorded 2026-09-10T20:06:00Z, before the wrapper was invoked and before any claim was
acquired.

Controller, verbatim, as a single line:

I authorize one retained agreement invocation on 1c7067448106cfa2aca3d57be879842d72293c61 as bound in D:/Pontius-handoffs/v0a-eval-panel-completion/agreement-run-20260910-r001/identity.json, reviewed manifest SHA-256 8485039b86efe61cdb9ea72d1ee3ea902beedfae562d2cc04511370d930c9663, wrapper SHA-256 d030bcba4b5f12da7a82a54e4293e70f8ed6f7cd0072301adfb57de7759ee229, with the adopted 2400 s / 3072 MiB worker Job envelope.

## Verified before launch

Every identity the authorization names was recomputed from the bytes and matched:

- Source commit `1c7067448106cfa2aca3d57be879842d72293c61`, the adopted head; the retained
  checkout `D:/Pontius-worktrees/eval-panel-agreement-20260910` is at that commit on branch
  `claude/eval-panel-agreement`, source scope clean, 59 journal rows, seven on-disk run
  directories equal to the seven tracked, CPython 3.14.6 with NumPy 2.5.2.
- Reviewed manifest `8485039b…` recomputed over the 65 members and equal to the named value.
- Wrapper `d030bcba…` equal to the `invoke.sh` on disk.
- Envelope 2,400 s / 3,072 MiB equal to the plan's own resource object, and to the per-phase
  resource decision the controller adopted on 2026-09-10.
- No `authorization.md` and no `invocations/` existed before this file was written.

## Scope

Exactly one retained agreement invocation, as requested in `authorization-request.md`.
Nothing else. Not authorized: a second agreement run, any change to the adopted source, any
integration into `master`, or anything in Slice B.

## Disclosed at the time of authorization, and not closed by it

- Two opposing reviews returned NOT CLEAN; every finding is accepted and dispositioned in
  `disposition.md`, and the controller closed the correction rounds after the last one.
  Neither review was verdict-blind or wholly history-free, and both said so.
- The here-string backing-storage failure behind review 02's Important finding could not be
  induced on this build by either the reviewer or the drafter; the guard is in place and the
  general mechanism is demonstrated, but that specific trigger is unreproduced.
- The full pool has no off-pool complement, so the default path is exercised by one synthetic
  control rather than a population, and no genuine host disagreement has ever been observed
  because teacher and host agree by construction.
- The worker Job limit bounds neither the parent process nor disk. The parent's live peak
  remains unmeasured for every phase of this campaign.
- Retaining all 98,304 witness draws dominates memory and result size and is redundant; it is
  carried to the Slice B interface rather than changed here.
