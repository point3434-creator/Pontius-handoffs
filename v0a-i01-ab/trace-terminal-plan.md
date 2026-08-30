# Parser all-outcome admission follow-up — Stage0

2026-08-30, Codex coordinator. FIX T-01/T-02 from r005 disposition. Isolated new
worktree from r005; only trace.py and test_v0a_trace.py. No publication, replay
algorithm, model, sealed kernel, event schema field or authority change.

Root cause/category: terminal admission treated success as the only cross-record
variant. Failure records were typed but their implications were skipped. Separately,
hand-maintained event predicates diverged from the existing exact value contract.
Enumeration: all four event constructors; every terminal field and cross-record
consumer; success/completed-failure/interrupted/unknown/no-start variants, each
with and without recorded failure rows. Compare source searches to ADR0485 field
and failure tables. Tests must enumerate this outcome matrix, not just four reports.

Shape: keep raw canonical JSON and exact key admission. Build exact event values
with the existing pure known constructors (nested exact HandAction) rather than
repeat their primitive/order constraints; normalize constructor failures to typed
TraceInvalidError. Keep stream position, starting-stack legal minimum, and mixed
rank-domain checks where their structural context belongs. Board order is untouched.

Extract a compact _validate_terminal_consistency helper called unconditionally
from parse_trace after types/counts/timing/decision-failure pairing. Table of rules:
- passed requires complete + accounting_complete + settlement, no failure or
  interruption, null reason, timely decisions and present numeric category totals.
- interrupted or unknown delivery requires all three flags false.
- failed or incomplete implies null settlement; failure reason cannot be erased.
- accounting_complete implies both complete numeric totals, even on failed hands.
- recorded first failure must remain consistent with terminal primary reason.
  Verify actual compound clock/body schedules before choosing an exact relation;
  do not invent chronology absent from recorded data or overwrite real first cause.
Host-only closure failures may have no failure row, so do not require a row for
all terminal reasons. Failed accounting can retain a completed category's finite
total; do not force both null merely because the aggregate flag is false.

RED first: genuine accepted-interrupted, unknown-after-real-delivery, rejected
nondelivery, late-completed, invalid-event and host-only write/settlement failures;
all terminal flag combinations and independently rebound cause/settlement/total
mutations. Ascending/descending/duplicate/bool/out-of-range private pair, board
reveal-order positives. Preserve unmodified traces and every clock-fault position
of normal and rejected-input host paths. Positive controls prevent blanket failure
refusal. Explicit per-case expected rule, not deriving expected behavior from helper.
GREEN both actual interpreters, then new frozen pair and two fresh cold contexts.
No source edits until separate non-cold Stage0 review assesses this shape.
