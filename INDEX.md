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
| v0a-i01-impl | r001 | [Handoff](v0a-i01-impl/r001/handoff.md) | Slice A NOT CLEAN; seven consolidated findings; reproduced on 3.11/3.14; fix-round brief in disposition.md; Claude finalizes |
| v0a-i01-impl | r002 | [Disposition](v0a-i01-impl/r002/disposition.md) | NOT CLEAN; ten consolidated Important findings; 99 focused tests pass on actual 3.11/3.14; F3/F7 remain open; Claude finalizes the next reviewed candidate |
| v0a-i01-impl | r003 | [Disposition](v0a-i01-impl/r003/disposition.md) | FIX slice 1 NOT CLEAN; two residuals R2-01/03; R2-02/07/08 closed; second policy residual requires its own candidate and root-cause note |
| v0a-i01-impl | r004 | [Handoff](v0a-i01-impl/r004/handoff.md) | FIX round, R3-02 only (typed closure causes); 113 tests GREEN on 3.11/3.14; 414-position fault sweep; awaiting cold review |
| v0a-i01-value-boundaries | r001 | [Disposition](v0a-i01-value-boundaries/r001/disposition.md) | NEW-SURFACE audit: three Important admission contracts; V2 ticket route not established; separate from r003/r004 fix scopes |
| review-guidance | r001 | [Disposition](review-guidance/r001/disposition.md) | NOT CLEAN; concurrent proposal isolated from intended commit; archived |
| review-guidance | r002 | [Disposition](review-guidance/r002/disposition.md) | CLEAN; exact reviewed workflow committed and pushed as d1ed3cb; concurrent edits preserved; refs archived |

The existing task verdict ledger remains at
[its original location](../Pontius-worktrees/v0a-increment-1-preregistration-review/progress.md).
New-round verdicts are issued in v0a-i01-prereg/progress.md; old verdicts are not
copied or rewritten. Relative legacy links resolve on this D: workstation only;
those packet files are not claimed to be included in this repository's backup.

[Program dispositions](progress.md) contain round outcomes; review verdicts remain
in [the task ledger](v0a-i01-prereg/progress.md).
