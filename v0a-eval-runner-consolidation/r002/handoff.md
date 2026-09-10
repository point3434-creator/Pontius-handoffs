# Shared evaluation runner r002: focused repair review

Review the repair to r001 finding F1: signals received during final outcome publication could
be omitted while the launcher returned success. The controller authorized this repair after
the one cold Codex review. This packet is prepared for one focused opposing review; it is not
an adoption, commit, push or retained-run authorization. Do not dispatch multiple reviewers.

## Identity and read order

Verify `manifest.sha256`, then `identity.json` and its source override hashes. The candidate is
the seven files under `source/` applied to base Git commit
`1c7067448106cfa2aca3d57be879842d72293c61`. Unchanged dependencies are that commit's Git blobs,
available read-only in `D:/Pontius`. Do not use mutable checkout source as review authority.

The predecessor packet is `D:/Pontius/tmp/eval-runner-consolidation-review/r001/`, manifest
`58217adf85a8d4ac36165f1c6d5979c35aa87fac4c748e906b78e85449eef638`.
Only the shared launcher, its tests and its guide differ from those seven predecessor overrides.
No poker arithmetic, plan admission, protocol, input binding, claim or journal logic changed.

Read the source and guide and write/hash a compact independent inventory before opening the
disposition, predecessor report or checks. This is a focused repair review with F1 disclosed,
not a claim of finding-blind review. Disclose other contextual exposure. No memory, ledger,
unrelated packet, retained authorization, claim or run is needed.

## Questions

1. Does the transition out of deferral precede the final signal snapshot and occur inside the
   interruption exception boundary? Can a signal before or during publication still return 0?
2. Are previously deferred signals still recorded as incomplete, nonzero child exits preserved,
   previous signal handlers restored, and consumed claims never released or retried?
3. Does the exact regression reproduce F1 on the retained r001 launcher and exercise both
   SIGINT/SIGBREAK, child success/failure, and pre-open/fsync boundaries with real file writes?
4. Are limitations stated correctly when an interrupted write leaves existing outcome bytes?
   A file's precomputed fields cannot override the invocation's nonzero process status.

The packet includes exact RED source/test bytes and the final affected-suite GREEN receipt.
The source and report for the prior finding are preserved unchanged. Author repair verification
does not replace an independent review verdict. Review proportionality remains material defects
or changed executable behavior, not additional rounds solely for documentation advisories.

Use Python 3.14 only for proportionate existing checks in a private disposable snapshot. No
retained solve/export/agreement invocation, candidate edit, commit, push or publication is allowed.
Return one report and its inventory in a unique scratch directory, with precise evidence,
severity, falsifier, CLEAN / NOT CLEAN and SOUND / NOT SOUND verdicts and verification limits.
