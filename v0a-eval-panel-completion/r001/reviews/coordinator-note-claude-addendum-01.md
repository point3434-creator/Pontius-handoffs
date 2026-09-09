# Addendum 01 to the coordinator note — exact harness exposure

Appended 2026-09-09 after inspecting the three agent transcripts. The coordinator
note is unchanged; this is a new record.

What the harness injected: the coordinator's auto-memory index, as a system reminder,
into ALL THREE agents (reviewer 01, reviewer 02 and the completeness critic), not only
reviewer 01, who was the one to disclose it. The injected copy was a STALE snapshot from
this coordinator session's start, not the index as it stood at dispatch. The lines that
concern this lane, verbatim as delivered:

- "[Python 3.14 only] controller ruling 2026-09-09: drop 3.11, target CPython 3.14.6
  only, no backwards compatibility; README/briefs still say 3.11 (stale); collapsed the
  eval-panel I-01 finding to Minor."
- "[Cold-review procedure] how to run a Pontius handoff cold review without
  contaminating it: identity first, inventory before coverage.md/checks, never tail the
  ledger, write reports with the Write tool."
- "[Eval-panel lane state] design and impl design adopted (f647a79); code r001 NOT CLEAN
  (7 accepted findings), r002 withdrawn (fixture receipt), r003 = 7004285d frozen
  2026-09-09 awaiting Codex reviews; all 1,081 hands fit, T1 ~ 0.1 s/hand (dev
  diagnostic); 792/428 lines, slice projection 1,000-1,100 needs a controller number;
  run scrubbed-env suites BEFORE freezing."
- "[Checkpoint alternation] ..." (the alternation rule; no verdict content).

What that is and is not: none of it concerns candidate 449a2a3c or design steps 4-7,
which did not exist when those lines were written. It names one verdict on a candidate
three code rounds earlier (code r001, a different surface), a withdrawn round, a frozen
round awaiting review, one prior-round finding label, and two development-diagnostic
facts ("all 1,081 hands fit", "T1 ~ 0.1 s/hand") that the packet's own allowed input
inputs/resource-decision.md also states. The reviewers did not choose this exposure
and could not have refused it.

Consequence for the coordinator's earlier remedy: because the injected index was a
session-start snapshot, scrubbing verdict language from the index after dispatch does
not by itself guarantee a clean re-run within this session. Before any re-run is
counted as cold, the harness behaviour must be probed first.

Under docs/workflow.md the controller decides whether a disclosed exposure still counts
as a cold pass. The coordinator's own characterization: cold with respect to this
candidate; not cold with respect to lane history; "cold as ice" was the instruction and
this did not meet it.
