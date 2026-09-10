# Retained export: completed

The controller-approved export ran once and completed on 2026-09-10. The authorization is
consumed. No second export or agreement is authorized by this result.

- Run ID: cf3bcdda9eed4031938c214959b1e10c
- Source: 1c7067448106cfa2aca3d57be879842d72293c61; source_verified=true.
- Plan SHA-256: c55f26f635f9512c5e5f4a57ab6d64f3327de0697253422e7230296a46fd1c5a
- Outcome: exit 0, evidence complete, phase_complete=true, cleanup_verified=true.
- Resource state verified; no reported errors; worker exit 0.
- Timing: 17 s wrapper, 16.236 s journal,
  12.577 s worker; coordinator wall 19.041 s.
- Peak worker Job memory: 788.0781 MiB, below 2,048 MiB.
  Parent memory was not measured and is outside that Job limit.
- Blueprint: 1,010,990 bytes; 37,586 bytes below the 1,048,576-byte cap.
- Membership: 1,081 distinct in-pool hits, zero disagreements, exact entries.
- The full pool has no off-pool complement; zero unsupported rows is not a default control.
- Teacher unchanged from the retained solve; blueprint digest equals the rehearsal's.

## Retained identity

teacher.json SHA-256:
c3ffab403eb7e939857cc31b0f21b255cefdffd8b0d26d078b703c1fe956b3e3

blueprint.json SHA-256:
666021c448c622caf235b304128d17de02823c12966c66510f5a1ec483814d17

result.json SHA-256:
00d9b9a003248011cabba58d22e0eb144e90599c150ddb6cf8780ec2e05879fb

runtimes.json SHA-256:
1963e99704e2d2976ee9f37eaf5e93d846183003038bfdfd7cece4a808fe898a

Absolute artifact paths, sizes and digests are in invocations/verification.json. The run
directory is experiments/results/runs/cf3bcdda9eed4031938c214959b1e10c/ under the permanent
D:/Pontius-worktrees/eval-panel-export-20260910 checkout. Exactly one journal row was added,
59 to 60; it is bound in invocations/export-journal-row.jsonl. The original journal prefix
and every pre-existing packet byte were verified unchanged. The frozen identity's earlier
preparation-status string is historical; this report records the completed invocation.

## Authority, retention and next phase

authorization.md records the controller's actual words, "I approve", and resolves them to
the current template, original manifest, addendum and 600 s / 2048 MiB worker envelope.
Approval was recorded before invocation; claim/start/end timestamps are retained.

The four run artifacts, journal, STATUS.md, plan and handoff packet are mirrored under
C:/PontiusBackup/Pontius-worktrees/eval-panel-export-20260910. The exact copied paths,
digests and verification result are in invocations/retention-mirror.json. The mirror
receipt itself is copied separately and excluded from its own mirror manifest.

The branch journal/STATUS and handoff records are local and uncommitted; no push occurred.
The next retained phase is agreement, whose plan must bind this retained teacher, blueprint
and result by absolute path and SHA-256. It needs its own witness bank, rehearsal, resource
decision, review and one-shot authorization. The next wrapper revision must disposition
follow-up-obligations.md's pre-claim environment check. No agreement or strategy-strength
claim follows from this export's exhaustive direct-provider membership result.
