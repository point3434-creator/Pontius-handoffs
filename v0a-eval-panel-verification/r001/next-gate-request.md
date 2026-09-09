# Decision prepared after the bounded verification correction

This document prepares the next controller decision; it authorizes no execution.
Candidate: 9fce4bfba3acf1c34938aa47f37f9743e5011cea.
Parent: d8d291cc1f813ce798f2d3a990b2a8bf2297e124.
Manifest: d05fd7b821fec534044eeb80acdf23a4fe09767373a67e4cde20bc5ba1bed088.

The correction's independent reviews and broad receipt must be complete and
accepted before this document is used as a run decision. Previous authorization
covered correction and correctness verification only. Claude's previously
assigned ceremonial commit turn for d8d291cc is not silently transferred here.

## Proposed retained prerequisite executions

One capacity invocation, followed only on successful nonempty capacity by one
preflight invocation. Each uses this exact candidate, a fresh dedicated retained
checkout at D:/Pontius-worktrees/eval-panel-prerequisite-20260909, its own locked
dev environment, CPython 3.14.6 and absolute PONTIUS_GIT with PATH absent.
If that destination exists, inspect before creation and do not overwrite it.

The plans and lifecycle controls are already prepared in
D:/Pontius-handoffs/v0a-eval-panel-completion/preparation-20260909/.
Its original prerequisite-run-plan.md still names d8d291cc; for the proposed
decision here, the reviewed source argument would be the full 9fce4bf hash above.
Plan bytes remain unchanged:

| Invocation | Plan SHA-256 | Time | Worker Job memory |
| --- | --- | --- | --- |
| Capacity | See capacity digest below | 600 seconds | 2048 MiB |
| Preflight | See preflight digest below | 3600 seconds | 2048 MiB |

Capacity: 6ad3e205058de941a695e04a966cb966d255369b0f910cfcee25a3426636bae1.
Preflight: d2e5c04cf5c4ba2543aca91b6705b5593464989a331bc0400a76a966e59253c5.

These are supervisor limits, not measured costs or total-parent memory caps.
Source admission, cleanup and final recording are additional lifecycle work.
All attempts, including interruption or failure, consume their invocation and
are retained with exact source, inputs, stdout/stderr, result and journal.
No retry, full-pool solve, teacher export or host agreement campaign is included.
Preflight measurements support a later explicit full-pool resource decision.
That measured decision is the accepted design's prerequisite to steps 4-7.
