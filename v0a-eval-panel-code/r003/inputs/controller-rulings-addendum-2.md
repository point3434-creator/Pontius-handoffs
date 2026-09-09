# Controller ruling addendum 2 — 2026-09-09

Appended after the r003 freeze; the pinned inputs are unchanged.

## Slice A line budget raised again

Controller, verbatim: "we will up the budget no worries".

Context: r003's `checks/line-budget-and-hygiene.md` reports 792 production /
428 test lines for the first source checkpoint alone and projects 1,000–1,100
production lines for the whole slice once bridge completion (design steps 4–7)
lands. The first addendum recorded the drafter's reading of 800 / 500 after the
controller's earlier "whats a few lines of code"; that figure is now exceeded
by this checkpoint on its own.

Drafter's reading, flagged for the controller's confirmation: the whole-slice
budget is **1,200 production and 600 test lines**, counted as the brief counts
(whole slice; generated data, fixtures and the permutation payload excluded).
Each later freeze reports actual totals against that figure. The brief's rule
that an over-budget implementation returns to the controller before freeze is
unchanged; only the number moved, twice.

Not granted by this ruling: review assignment, retained measurement, full-pool
solve, ceremonial commit, or integration. Reviewers should treat the budget as
a controller decision, as both r001 reviews already did.

## Controller clarification (same day)

Controller, verbatim: "im not too worried as long as it doesnt balloon to 3000 or
something then i might".

Recorded as a **hard ceiling of 3,000 production lines for the whole slice**,
stated by the controller; the drafter's 1,200 / 600 remains the working figure
that each freeze reports against. Approaching the ceiling, not merely exceeding
the working figure, is what returns the slice to the controller.
