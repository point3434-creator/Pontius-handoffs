# Publication design amendment after independent Stage0 review

2026-08-30. Reviewer ab_r002_cold_b assessed this separately after issuing its
r002 verdict: SOUND with required implementation clarifications. Adopt all six.

1. Add required-measurement entry for ordinary host work. Failed entry raises the
trusted owned-operation signal before next(iterator), serialization or dispatch can
run. Existing optional operation semantics remain for terminal failure reporting;
no successful accounting is inferred from an unopened interval. Initialize outer
ledger through a public runtime entry before first measured header work.
2. Native owner opens a local drive root then each ancestor/destination parent
relative to its already owned directory handle, with no reparse and sharing READ
only (deny WRITE/DELETE). Retain every directory authority through creation, all
appends and final close; do not rely on path rechecks or benign native-open probe.
Admission refusal when a foreign write/delete handle conflicts is fail-closed.
Test actual rename attempts before creation and after first row; reparse inputs
must refuse without outside writes. No CRT/file-object conversion: use native
synchronous WriteFile and explicit handle holders, owned before probes.
3. Required measured work includes iterator advancement/exhaustion, header/events,
all-in/showdown construction, row serialization/writes, prefix/semantic/full
hashing, bytes assembly, file open/flush/close. Compute pre-cut semantic values
before sampling totals; full trace hash belongs to terminal publication. Use
public returned intervals and terminal-at-entry, never self-subtraction repair.
4. Writer states NEW/OPEN/FAILED/FINISHED/CLOSE_ATTEMPTED separate permission to
append/finish from one-shot resource closure. Partial/ambiguous write latches FAILED;
no retry/append/finish then. Preserve incomplete file. Terminal may be built in
memory after file failure, but receipt digest stays null. Close attempt clears
ownership before native close and never replays an ambiguous numeric handle.
5. Host retains body failure via owned interval before a later cleanup operation;
close every owned handle once even when another close fails, retaining diagnostics.
Creation object exists before acquisition; failures do not lose the owner. No
retry/delete/overwrite on failure. Convenience write_trace uses same protocol.
6. Host receipt success requires writer finish+close, final measured publication
exit and runtime finalize. Successful terminal bytes alone cannot confer success.

The native read-only plan probe confirmed absolute Nt directory open accepts
OBJ_DONT_REPARSE on actual3.11; it proves no race/resource correctness. Final native
correctness requires adversarial real-handle path/junction/rename tests on both
interpreters. Other platforms fail explicitly unless an equivalent safe backend
is implemented; no silent path-based fallback. No cross-platform success claim.
