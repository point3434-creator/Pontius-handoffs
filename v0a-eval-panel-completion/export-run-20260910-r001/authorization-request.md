# Proposed authorization: retained export

Prepared by Codex, 2026-09-10. Awaiting Claude's review and controller approval.
This document requests authority; it grants none. No retained export has been invoked.

The proposed invocation exports the retained full-pool teacher on the adopted source
`1c7067448106cfa2aca3d57be879842d72293c61`. Exact paths, commands and digests are in
`identity.json` and `plans/export.json`. The execution checkout is
`D:/Pontius-worktrees/eval-panel-export-20260910`, branch `codex/eval-panel-export`.
It is separate from the retained solve checkout and starts at the adopted source commit.
Only Python 3.14.6 is used, in the locked environment.

The two producer inputs are the retained solve's teacher and result, each bound by absolute
path and SHA-256. The wrapper checks both digests before taking its claim. The worker
validates their digests and the completed producer/artifact relationship when reading them.
The retained solve's three prerequisite bindings, board, full 1,081-hand permutation and
coverage remain in the plan. Its phase becomes export and its two input bindings are added.

## Separate resource proposal

Proposed export envelope: **600 seconds / 2,048 MiB worker Job memory**. These values require
their own approval here. The earlier solve authorization supplies no export authority.
The identical export plan and wrapper completed in the detached snapshot: 15 seconds
wrapper time, 11.265 seconds worker time and
787.8125 MiB peak worker Job memory. Parent memory was not
measured and is outside the Job limit. This is one observation, not a runtime guarantee.
The proposal retains margin for machine load; supervision enforces the declared worker bound.

## One-shot scope and failure handling

Retained mode refuses any set EXPORT_ROOT or REHEARSAL_PK, including an empty value.
Only an unset REHEARSAL defaults to 0; a set value must be exactly 0 or 1.
authorization.md must exist before retained preconditions. The operator must authenticate
its contents against this identity; existence alone does not authenticate a decision.
Atomic creation of invocations/claim.d reserves the attempt before claim/start records
and launch. A refusal before acquisition creates no new claim or child; an existing claim
remains consumed. Every failure after acquisition preserves the claim. No automatic retry.

After launch, a nonzero child status takes precedence even if evidence is incomplete.
With a zero-status child, incomplete evidence returns 99; complete evidence returns 0.
The script checks record writes and never substitutes an old journal row for a missing one.
It assumes exclusive ownership of this checkout and the adopted tool as journal producer.
The operator retains the run directory, captures, journal and status, resolves ambiguity,
and mirrors the retained files before treating the retention task as complete.

## Suggested approval, after review

I authorize one retained export invocation on 1c7067448106cfa2aca3d57be879842d72293c61
as bound in D:/Pontius-handoffs/v0a-eval-panel-completion/
export-run-20260910-r001/identity.json, with the proposed 600 s / 2048 MiB envelope.

The split path above is one path. Approval should also name the candidate manifest digest.
Record the actual approval verbatim before invoking the fixed wrapper. Run the wrapper
once with Bash --noprofile --norc, REHEARSAL unset and no root overrides. Preserve every
post-claim outcome. No second export, solve, agreement, source change or master integration
is requested. Agreement must bind future retained export outputs, never rehearsal copies.
