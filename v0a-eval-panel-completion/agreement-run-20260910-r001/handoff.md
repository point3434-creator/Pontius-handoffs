# Review request: retained agreement plan r001

Packet: v0a-eval-panel-completion/agreement-run-20260910-r001.

Claude drafted this retained agreement plan. **One opposing review is requested** under
`controller-review-policy-20260909`. Give the reviewer this packet path only. No author
verdict is supplied. Reviewing authorizes no invocation and no publication.

Round kind: NEW-SURFACE. It is the third and last retained phase of design step 7. No project
source changed; the source is the adopted commit
`1c7067448106cfa2aca3d57be879842d72293c61`, tree `3d2fe79d2af20125e322dd4a668335e789810863`.
Python 3.14.6 only.

## Scope of this round, and what closes it

The controller has bounded this round: address the recorded environment obligation and the
requirements specific to agreement, and do not turn it into a general infrastructure rewrite.
Consolidating the repeated launch logic into one small tested runner is agreed work, but it
comes *after* this phase and is not in scope here.

The controller has also set the rule for further rounds: a further round follows a **material
unresolved finding or changed executable behaviour**, not automatically every documentation
advisory. A verdict label does not by itself open a round. Record a Minor, state its remedy,
and let the finalizer carry it.

## Read contract

1. Read this file, `identity.json`, `candidate.json` and `manifest.sha256`. Recompute the
   manifest over raw bytes, whole-row byte order, LF joins and a trailing LF, excluding
   `handoff.md`, `candidate.json` and `manifest.sha256`. `authorization.md`,
   `authorization-template.txt` and `invocations/` sit outside the freeze; the template does
   so deliberately, because it names the manifest's own digest.
2. Read `invoke.sh`, `verify_plan_inputs.py`, `journal_attribution.py` and
   `plans/agreement.json`. Inspect the adopted Git blobs for the producer, consumer,
   ownership and cleanup paths. Worktree bytes are identity checks only.
3. Recompute the input and prerequisite pins. `inputs/` carries copies of the retained
   export outputs, the two prerequisite results and both resource decisions;
   `governing/brief.md` and `governing/design.md` are exact source-commit blobs. Read
   acceptance criteria 5 through 9 and design sections 4, 5 and step 7.
4. Write and hash your independent invariant inventory **before** opening `checks/`,
   `rehearsal/`, `coverage.md`, `design-note.md`, `measured-report.md`,
   `authorization-request.md` or `next-phase.md`. Do not revise it after sealing.
5. Then inspect those deferred inputs. Recompute meaningful assertions from the bytes; a
   passing label is not evidence.
6. Predecessor packets may be read afterwards to reconcile inherited obligations. Disclose
   any exposure to historical findings or verdicts, including in mandatory documents.

Never open any `progress.md`, `INDEX.md`, any memory index, any conversation history, or any
other reviewer's material. Use exclusive scratch and disclose your initial context probe.

No project invocation, no wrapper or check-script execution, no solve, export or agreement,
no worktree mutation, no commit, no push. Read-only Git and independent CPython 3.14.6
stdlib calculations are allowed. Both rehearsal snapshots are retained for read-only
inspection; do not run anything in them.

## Acceptance questions

- Does the plan bind the completed retained export by digest, with a valid full census,
  prerequisites, source and runtime identity, and the envelope the controller adopted?
- Is the witness bank valid under the frozen validator, is its holdout range genuinely
  disjoint, and does its rationale state the dependence assumption rather than claim the
  bound as a guarantee?
- Are the two changes from the export wrapper correct: the environment guard placed before
  any claim, and input digests read from the plan rather than duplicated as constants? Does
  either change weaken a property the export wrapper held?
- Are mode refusals, the atomic claim, checked records, attribution and exit precedence
  sound? Can any supported failure look successful?
- Do the executed assertions reject false outcomes? Is the raced rehearsal's claim evidence
  what it claims to be, namely contention at the atomic `mkdir` rather than serialisation
  through the pre-claim existence check?
- Do the census, control and resource claims follow from the raw captures and the result
  rather than from labels? Is the empty complement disclosed rather than presented as a
  passed off-pool control?
- Are the remaining operator duties and coverage limits explicit, and is authority withheld
  pending the controller's separate decision?

## Known deviations to weigh

- Lines over 100 columns in the wrapper, JSON and receipts where paths, digests or format
  strings require them; markdown and the helpers are within 100.
- The wrapper-level suite ran while the raced rehearsal's winner was still executing. It
  launches nothing and touches no checkout, and the disclosure is in `coverage.md`.
- The 48.9 MB rehearsal results stay in their snapshots, bound here by digest rather than
  copied, to keep the packet a reasonable size.
- One measurement failed and is reported rather than hidden: a live sampler of the parent
  process returned a void number because the venv `python.exe` is a launcher stub.
  `measured-report.md` records the diagnosis and gives a reconstruction instead.

## Report

Write `reviews/review-01-codex.md` with CLEAN or NOT CLEAN, separate specification and
engineering judgments, findings graded Critical / Important / Minor with file and line,
reachability, requirement and consequence, and your exposure and coverage disclosures. Save
your sealed inventory as `checks/review-01-inventory.md`. Preserve original findings and
labels. Reviewer publication is not authorized by this handoff; return the report for the
drafter's disposition.
