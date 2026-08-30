# Cold review: v0a-i01-impl/r001 (slice A — hand core)

Candidate ref: `refs/heads/review/v0a-i01-impl/r001`
Candidate commit: `2d059f90fb6cec27e4090ad0432c68759a760960`
Manifest SHA-256: `fc090d962a914b41dec932f21a6c8421499191ccac9dca40363a078cbba95b0c`
Base commit: `b357d333fc2393b7fc7dcf31f30c86616208c817`
Tree: `7672cad16e0624db73e38095cf3d70d74144b8da`
Tier: C — the runtime realizes ADR-0307/0308 action-clock semantics.
Finalizer: Claude (first drafter this checkpoint). Reviewer: Codex.

The full commit and manifest bind identity; this path and the index only
locate them. The ref is local in D:/Pontius and its linked worktrees and has
**not** been pushed. Read the candidate's Git blobs, never mutable working
files, and independently recompute the manifest from every path changed
against the base under the whole-row byte sort (digest first, not path).
Changed bytes or changed scope require a new round; r001 is immutable.

An earlier informal read of this slice happened against unfrozen working
files and was stopped by the controller. It has no standing. Nothing was
edited between that read and this freeze — the frozen blob digests equal the
overlay digests in `checks/slice-a-receipts.json` — but findings must be
reissued against this pair to bind.

## Scope

- `src/pontius/v0a/__init__.py`
- `src/pontius/v0a/model.py`
- `src/pontius/v0a/clock.py`
- `src/pontius/v0a/runtime.py`
- `tests/test_v0a_hand_replay.py`

Slice A is the hand core only. Trace serialization, semantic projection,
replay, the explicit-deal host with fixtures A/B, the independent settlement
oracle, terminal accounting with the host completion receipt, boundary-policy
classification, inventory admission, and the CI gate are slices B and C —
their absence is scope, not a finding.

## Pinned inputs

At the base commit: `docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md`
(the frozen contract), `docs/briefs/v0a-increment-1-brief.md`,
`docs/workflow.md` (checklist v1, now eleven items), `CLAUDE.md`,
`docs/workflow-amendment-2026-08-30.md`, and the sealed APIs those documents
identify — `action_clock`, `legal_decision_spine_v2`, `immutable_blueprint`,
`no_limit_betting`, `holdem_cards`, `preparation_bank`.

Implementer materials in this packet: `../slice-a-self-report.md` and
`checks/slice-a-receipts.json`. The self-report is the implementer's own
account and is **not** a cold input to your verdict — read it only after
forming independent findings, or to check a specific claim.

## Review contract

Review the whole candidate against ADR-0485 and the brief. Weigh in
particular: whether the outer wall genuinely starts at the event boundary and
covers transition work; whether emission time is the sealed ledger's own
sample rather than a fresh read, and whether the enforced equality between
recorded nanoseconds and the closing snapshot is sound; whether the
ready-to-emit checkpoint places the cutoff exactly where the contract says,
and whether the 14–15 s reserve stays lawful emission time; whether the
blueprint outcome split matches the contract exactly (miss → passive default;
illegal matching entry or invalid context → typed failure with no emission;
an entry for another state is a miss); whether delivery rejection, ambiguity,
and post-acceptance clock failure preserve exactly what is known and never
retry; whether interrupted timing can ever assert a false flag or a
fabricated measurement; and whether any policy-selection path can reach the
complete deal, the host, or the future schedule.

The implementer flags one open item for your ruling: the guard rejecting an
opponent event that names the controlled seat is unreachable as a distinct
branch (the controlled decision runs inline, so the controlled seat is never
pending between dispatches) and is subsumed by the wrong-actor check with the
same typed code. It survived mutation. Keep it as defence in depth with its
comment, or delete it as dead code under checklist item 6 — your call, stated
as a finding either way.

CLEAN requires that no material finding survive verification. Every Critical
or Important finding binds to this commit/manifest pair, cites exact frozen
locations, states a concrete failing scenario, and names the smallest
correction without implementing it. Do not run experiment owners, create
lifecycle identities, or execute anything from the primary checkout; tests
run only from fresh disposable D:-local snapshots under `-B -P` with a
scrubbed environment and absolute `PONTIUS_GIT`.

Return attributed findings to `reviews/review-<NN>-<reviewer>.md` in this
packet and append one verdict line to `../progress.md`. A correction is a new
record, never an overwrite. Ceremonial-commit authorization is a separate,
ungranted gate held by the controller.
