# Controller rulings relevant to this handoff

Date: 2026-09-08. These are direct user instructions, not inferred review
outcomes. They were given after the design pass surfaced six decisions the
implementer could not settle alone.

The controller's words: "go with T1 as primary, s=4, accept all six".

The six decisions accepted, as they were put:

1. Brief criterion 4 amended: hero and villain private cards come from
   `tools/v0a_seeded_deals.py` output under a recorded seed; the board is the
   declared teacher board; a deal whose private cards collide with the board is
   rejected by that rule alone, before play, and counted.
2. Brief criterion 5 amended: every compared policy plays the identical
   `(hero hand, villain hand, board)` triple, and the hand-swap triple is also
   played; the matched pair is the unit of analysis. Seat rotation is not
   available in the teacher game.
3. Brief criterion 6 amended: boards are the sampling clusters; a single-board
   result is conditional on that board; Slice B runs four declared boards.
4. Teacher: T1, the exact best response to the declared opponent
   (`evaluation.best_response`, pure by construction), is primary. T2, the CFR
   average strategy, is secondary. T2's determinization rule remains open and
   must be declared in the preregistration before any T2 export.
5. Stack depth `s = 4` for both slices; `s = 6` is a declared later variant.
6. Placement: deal composition and pairing arithmetic in the library with a
   test; worker and orchestration under `tools/`; the helper may import
   `deal_for_hand` from the sealed dealer tool, which is unchanged.

The controller also instructed: "do 1-3, freeze it for cold review" — create
the worktree and branch, place the two documents, and freeze the round.

These rulings settle the design questions they name. They do not authorize
implementation, any experiment invocation, any run of the host or solvers, a
ceremonial commit, or a change to any sealed surface. Ceremonial-commit
authorization remains a separate gate after review.
