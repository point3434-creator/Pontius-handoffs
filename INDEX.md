# Pontius handoffs

Navigation only. A candidate's full commit and manifest SHA-256 bind its identity.
Private origin: https://github.com/point3434-creator/Pontius-handoffs.git.
Packet commits use the installed post-commit push hook; remote identity must
still be checked after each publication rather than inferred from hook success.

| Task | Round | Packet | State |
| --- | --- | --- | --- |
| v0a-i01-prereg | r001 | [Legacy reports](../Pontius-worktrees/v0a-increment-1-preregistration-review/r1-candidate.json) | Rejected; preserved in its original location |
| v0a-i01-prereg | r002 | [Legacy handoff](../Pontius-worktrees/v0a-increment-1-preregistration-review/r2-handoff.md) | Three independent CLEAN reviews; later notes assessed separately |
| v0a-i01-prereg | r003 | [Legacy candidate](../Pontius-worktrees/v0a-increment-1-preregistration-review/r3-candidate.json) | Preserved; a generated-link check failed |
| v0a-i01-prereg | r004 | [Handoff](v0a-i01-prereg/r004/handoff.md) | Rejected: manifest row ordering; source bytes unchanged |
| v0a-i01-prereg | r005 | [Handoff](v0a-i01-prereg/r005/handoff.md) | Integrated and pushed as 111807b; three CLEAN reviews; scoped checks pass on 3.11/3.14; review refs safely retired |
| v0a-i01-impl | — | [Plan](v0a-i01-impl/plan.md) | Opened 2026-08-30; Claude drafts/finalizes, Codex reviews; no round frozen yet |

The existing task verdict ledger remains at
[its original location](../Pontius-worktrees/v0a-increment-1-preregistration-review/progress.md).
New-round verdicts are issued in v0a-i01-prereg/progress.md; old verdicts are not
copied or rewritten. Relative legacy links resolve on this D: workstation only;
those packet files are not claimed to be included in this repository's backup.

[Program dispositions](progress.md) contain round outcomes; review verdicts remain
in [the task ledger](v0a-i01-prereg/progress.md).
