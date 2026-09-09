# Coordinator note — cold reviews 01 and 02 of v0a-eval-panel-completion/r001

Coordinator: Claude (this session), 2026-09-09. Candidate
`449a2a3c1fa1f5a7f5f04adca32e499faaf81e13`, parent `beb84be5`, manifest `f58d6ed8…`.

## How the two passes were run

Both reviews were performed by independent Opus 5 agent sessions with no shared
context and no access to this coordinator session. Each received the packet path,
the handoff's rules restated, and a working approach — reviewer 01 bottom-up from the
frozen source, reviewer 02 top-down from the checkpoint brief and the accepted
brief/design — and nothing else: no prior findings, no lane history, no expectations.
The coordinator did not review the candidate itself: this session carries the lane's
history and is not cold. Each reviewer created an exclusive scratch directory under
`D:/Pontius/tmp` with a random suffix, wrote exactly two files there, and returned
their SHA-256 digests; the coordinator copied those bytes unchanged into
`reviews/review-NN-claude.md` and `checks/inventory-NN-claude.md` and re-verified
the digests after copying:

- `reviews/review-01-claude.md`: `726a8c6b3b7849acbe2e3c1e81b513ca34ec6a6ef7c0ea92637c0b2653eebdb2`
- `checks/inventory-01-claude.md`:
  `290949bacfaf50c43021bcf1f4a233245beba349dd3aaa25b8192e9d739783e9`
- `reviews/review-02-claude.md`: `2a8dd035afceee12…` (full digest in the ledger line)
- `checks/inventory-02-claude.md`: `d27bf264c12253cb…`

Verdicts: **01 CLEAN / SOUND; 02 CLEAN / SOUND.** Neither raised a Critical or
Important finding, so the adversarial verification stage (three lenses per material
finding) had nothing to verify. Their Minor items overlap: the full-pool prerequisite
digests are not verifiable from the packet's allowed inputs (01 M-01 / 02 F-01);
three RED observations exist only in tool history (02 F-02); the parent does not
reconcile primaries' wire-byte identity (01 M-02); `summarize.complete` tolerates
`unsupported` (01 M-03). Advisories cover the untested v2 frame path, three loaded
host-module copies, result-size growth for a full-H agreement run, the hygiene
receipt's provenance and mutation of the worktree, the missing `ready` event for
completion phases, fixed-name host-input files, and the `unsupported` label shared by
baseline and off-pool cases.

## Completeness critique (not a cold pass)

After both passes returned, a third agent received both inventory summaries and the
Minor/Advisory titles and was asked what both had missed, with the brief's Tier C
question put to it directly. Its report is `reviews/completeness-critique.md`. It found
**no new Critical or Important finding** and, checking every precondition of a `hit`
in the frozen `eval_agreement.py` and the parent's `complete()`, found **no path by
which missingness, a default or a failure becomes a hit, a completed count or a
full-coverage claim**. Its advisory reconciliation gaps (export `complete()` not
cross-binding membership digests to retained artifacts; the parent trusting worker
labels for `river_hand`/witness identity; admission shape-checking input bindings
without hashing bytes; early stop on the first non-hit primary) are recorded for the
finalizer. It also notes that reviewer 01's M-01 overreaches on one of three digests:
the decision digest is verifiable from `inputs/resource-decision.md`.

## Coordinator fact check on the prerequisite digests

The reviewers could not verify the `PREREQUISITES` constants
(`tools/v0a_eval_panel_completion.py:18-22`) because the retained run files lie
outside the packet. The coordinator executed those retained runs and holds their
bindings (`v0a-eval-panel-completion/prerequisite-run-20260909/invocations/
retained-files.txt`). All three constants match exactly:

- `capacity` `29f532a9…` = `experiments/results/runs/a89932e7…/result.json` (2,789 B)
- `preflight` `8a17325e…` = `experiments/results/runs/7ce5ab4f…/result.json` (20,722 B)
- `decision` `037a0de1…` = `prerequisite-run-20260909/resource-decision.md`

This is a coordinator observation, not part of either cold pass. It answers the
Minor's factual question; the Minor's process point — that the next packet freezing a
solve plan should pin these where a cold reviewer can check them — stands.

## Exposures, disclosed

- Both reviewers issued a directory listing of the packet (file names and sizes only)
  before writing their inventory; `reviews/` was empty at the time and `checks/` names
  are already enumerated in `supporting-files.json`. No contents were read.
- The harness injects this coordinator's auto-memory index into subagent system
  prompts. Reviewer 01 disclosed seeing one-line summaries that name earlier
  eval-panel rounds; reviewer 02 did not mention it but received the same harness
  prompt. Those lines describe prior rounds' states and verdicts, not this candidate;
  nothing from the memory files themselves was opened. This is inherited history of
  the kind the handoff says is preserved, but it is an exposure the reviewers did not
  choose, and it is recorded here so the controller and finalizer can weigh it. The
  coordinator will keep verdict language out of the memory index before the next
  concurrent review.
- No reviewer opened any `reviews/` directory, any other packet, the ledger, the
  index, any disposition or readiness file, or any other scratch directory; no project
  code was run; utility scripting used the handoff's interpreter only.

## What this does and does not establish

Two independent CLEAN / SOUND passes satisfy the handoff's Tier C review requirement
for this round. Nothing here is broad-suite clearance, adoption, or authorization for
the retained solve, export or agreement invocations; those remain the finalizer's and
the controller's gates, and each later phase needs its own bound plan and one-shot
authorization. The finalizer for this checkpoint is Codex.
