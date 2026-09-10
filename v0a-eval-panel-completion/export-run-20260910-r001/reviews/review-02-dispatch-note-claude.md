# Cold review 02 — dispatch note (coordinator: Claude)

The controller requested a cold pass after the finalizer recorded that review 01 counted as
independent reciprocal evidence but not as a cold pass. This note records how review 02 was
obtained and what I verified about it. It states no verdict of my own and authorizes
nothing; the report and its findings return to Codex for disposition.

## Provenance

One reviewer ran, and nothing else: no probe agent, prosecutor, critic, verifier or second
pass. It ran in a NEW Claude Code session, opened by the controller, after I renamed the
coordinator's memory index to `MEMORY.md.parked` so that a fresh session would take its
snapshot with no index present. This is necessary because the harness injects a
session-start snapshot of that index into every agent a session spawns; a pass dispatched
from the coordinator's own warm session could not have been cold.

Script: `D:/Pontius/tmp/eval-completion-r002-dispatch/cold-review-export-r001.js`, one role,
effort `high` because this is a new-surface round rather than a fix. The reviewer's prompt
named this packet's `handoff.md` as the governing read contract, and added to its
prohibition list the files that did not exist when that handoff was written: `reviews/`,
`checks/review-01-inventory.md`, `disposition.md`, `finalizer-addendum.md`,
`authorization-template.txt`, `finalization/`, both ledgers, `INDEX.md` and any memory file.
The subject of the review is the frozen 47-member candidate, manifest
`9965a225729a5896818127c013122f62fb3ae323889fde8ab16ea35e3e43eb17`, on source commit
`1c7067448106cfa2aca3d57be879842d72293c61`. The correction files added after the freeze were
therefore outside the reviewed set, which is what let the pass stay verdict-blind.

Exclusive scratch: `D:/Pontius/tmp/export-r001-cold`.

## Verdict as issued

**CLEAN**, design verdict **SOUND**, with 4 Minor findings and 1 Advisory. The label is
preserved as issued and is not reinterpreted here.

## What I verified as coordinator

- The reviewer's reported digests match the files it wrote:
  `review-02-claude.md` `125c4e18522067d355f5aa51e0ebc73d18ddb0ffdf2d3acca6d38ca6caeadddd`,
  `inventory-02-claude.md` `e62d1f04e0cf2834e608a04ef45473d65701ebeb109fedebc76f165479608875`.
  Both are copied into this packet byte for byte, without reflow or editorial change.
- All 47 manifest members still hash to their recorded values and the manifest digest is
  unchanged. The reviewer wrote nothing into the packet or the repository.
- No `authorization.md` and no `invocations/` exist. Nothing is committed, pushed or invoked.

## Disclosures the reviewer made, carried forward

- Context probe: `CONTEXT_PROBE_NONE`. It opened none of the prohibited files, and declined
  the predecessor records that its handoff step 6 would have permitted after sealing.
- Incidental path exposure: `checks/preservation-before.json` is a manifest member it had to
  read at step 5, and that file lists 53 absolute paths including `INDEX.md` and files under
  the solve packet. It saw path names and digests only, and no review, disposition or
  addendum path appears in that list.
- Output-location deviation: the packet's handoff asks for `reviews/review-01-claude.md` and
  `checks/review-01-inventory.md`. Those slots are occupied by the earlier report, so the
  commissioning prompt directed this pass to scratch under the 02 name instead, and
  forbade it from opening or writing inside `reviews/`. That instruction was mine, not the
  reviewer's choice, and it is why the report arrives through this note.
- Hygiene: the report and inventory are LF-only and BOM-free but exceed the project's
  100-column convention, because my commissioning prompt omitted that requirement. Reviewer
  bytes are retained exactly rather than reflowed.

## One finding I checked myself from the frozen bytes

Advisory A1 says a `set -u` expansion below the claim can consume the one-shot claim without
launching. I confirmed the mechanism rather than the grade. In `invoke.sh`, `set -u` is at
line 29, the atomic claim at line 109, the two record writes at lines 113 and 116, and the
launch line at 122 expands `${SystemRoot:-$SYSTEMROOT}`, `$TEMP` and `$TMP` with no guard
anywhere above. On a throwaway shell, unsetting both `SystemRoot` and `SYSTEMROOT`, or
unsetting `TEMP`, aborts with an unbound-variable error. So in a shell lacking those, the
claim and both records would be written and no child would start. The reviewer's own
mitigation stands: the condition has never occurred here, the predecessor solve launched
through the same construct, and the correction it proposes is documentation, naming the
required environment in the operator instructions rather than reopening the frozen wrapper.

I did not adjudicate any of the four Minors. Two of them, the race receipt exercising the
pre-claim existence check and the empty complement behind `unsupported: 0`, correspond to
what review 01 raised as a finding and an observation respectively; the other two, the
unretained RED wrapper and the four unexercised attribution refusal branches, are new.
