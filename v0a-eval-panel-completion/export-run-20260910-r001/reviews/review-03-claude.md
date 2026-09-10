# Review 03 - finalization layer, export-run-20260910-r001

**Verdict: CLEAN.** No Critical, Important or Minor finding survives my own verification.
Three Advisory items are recorded below.

**Specification judgment: SOUND.** **Engineering judgment: SOUND, with one accepted
residual.** **Design verdict: SOUND.**

Reviewer: Claude, independent third pass, 2026-09-10. Packet drafter and finalizer: Codex.

## What this pass is, and what it is not

This is **not** a verdict-blind cold pass, and I do not describe it as one. The subject of
this review is the packet's own review-and-disposition record, so I read both review
verdicts, both dispositions and both addenda deliberately. What makes the pass independent
is that I carry no prior context about this project - context probe **CONTEXT_PROBE_NONE** -
and no relationship to the authors of any file here. I did not attempt to redo the cold pass
on manifest `9965a225...`; I verified the finalization layer built on top of it.

Every digest quoted below was recomputed by me from the current bytes with plain CPython
3.14.6 stdlib. No passing label was accepted as evidence. Facts are in
`inventory-03-claude.md`, written and hashed before any judgement here was formed.

Nothing in this document authorizes an invocation, publication, commit or push.

---

## 1. Preservation - the load-bearing fact, and it holds

All 47 members of manifest `9965a225729a5896818127c013122f62fb3ae323889fde8ab16ea35e3e43eb17`
still hash to their recorded values, and `manifest.sha256` itself is byte-unchanged (its own
digest equals the manifest digest, 4327 bytes, 47 rows, sorted, trailing LF). Zero
mismatches, zero missing.

Both review reports, both review inventories, `disposition.md`, `finalizer-addendum.md`,
`authorization-template.txt` and all three files of `finalization/` hash to the values
recorded in **both** finalization layers - two independently written records that agree with
each other and with the bytes on disk. Because `reviews/review-01-claude.md` and
`reviews/review-02-claude.md` are byte-identical to their recorded digests, no verdict label
can have been rewritten, softened or replaced: review 01 still reads NOT CLEAN with 2 Minor
at line 3, review 02 still reads CLEAN / SOUND / SOUND / SOUND with 4 Minor and 1 Advisory
at lines 3-4.

`finalization-02/preservation.json` enumerates 59 pre-existing files - the 47 members plus
the 12 files that existed outside the freeze before this round - and all 59 verify.
`all_preexisting_bytes_preserved: true` is true.

## 2. The reconstructed RED wrapper - derived, then compared

I did not read the packet's diff first. I recomputed the reconstruction's digest, derived
the difference from the frozen `invoke.sh` myself, and only then compared.

- `finalization-02/reconstructed-red-invoke.sh` is 9447 bytes and hashes to
  `8edd61520f838de99afde315a19065e3e1c5e0d08c63fa9975673af97a3a43b6`, which is exactly
  `checks/red-before-guard.json`.`source_sha256`. The RED receipt's executed bytes are
  therefore identified, not merely labelled.
- Replicating the slice definitions in `checks/focused-checks.py:53-55` and `:100` in my own
  code (the script was never executed): the reconstruction's `producer_guard` slice is the
  **empty string**, whose SHA-256 (`e3b0c442...`, the well-known empty digest) is precisely
  the `producer_guard` value the original receipt recorded. Its
  `exit_tail` slice is `b86dd771...`, also exactly as recorded, and byte-identical to the
  frozen wrapper's `exit_tail`. The frozen wrapper's own guard slice is `95ac5b97...`, which
  is what the GREEN receipt `checks/focused-checks.json` records. The RED/GREEN pair is
  therefore anchored on both sides.
- My `diff -u` output is textually identical to `finalization-02/red-to-frozen.diff` apart
  from the file-name header lines. The difference is `invoke.sh` lines 44-47 (`TEACHER`,
  `TEACHER_SHA`, `PRODUCER`, `PRODUCER_SHA`) and lines 85-88 (the fenced guard block) -
  four producer constants and the guard block, exactly as stated.
- Controls (full values in `inventory-03-claude.md` section 5): deleting only the guard
  block gives `d4e4b50a...`, independently confirming the value review 02 reported; deleting
  only the four constants gives `110d870f...`; deleting both gives `8edd6152...`. The
  addendum's claim that removing only the guard "would not reproduce it" is correct.

One honest limit, which the addendum states itself: the reconstruction is identified by
digest agreement with the receipt, not by provenance - nobody can now witness that this file
is the one the RED run loaded. Digest identity is the strongest available evidence and the
addendum claims nothing more ("no new RED execution is claimed", "evidence material only and
must not be used as the launch wrapper").

A residual weakness worth naming, which no finding raised: with the guard slice empty, the
RED's three `producer-*` slice cases execute an empty program and exit 0 tautologically.
The RED shows that nothing catches a mismatch when the guard is gone; it is the GREEN run,
on slice `95ac5b97...`, that shows the guard itself is what catches it. The pair is sound
because both halves are digest-bound to real wrapper bytes. This is an observation, not a
finding.

## 3. Finalization manifests and evidence

`finalization/manifest.sha256` (5 members) and `finalization-02/manifest.sha256`
(10 members) both verify member-for-member, are byte-sorted, and correctly exclude
themselves. Every digest asserted in `finalization-02/evidence.json`,
`finalization-02/preservation.json` and `finalization-02/received-review.json` resolves to
the file it names. `finalization/evidence.json`'s claim-block assertion also verifies: the
slice from `mkdir -p "$OUT"` to (excluding) `START=$(now)` is 346 bytes and
`dbcbcb73b3a5e9435acd36a3c67d0775764cb9891a9ce25ab9a5e4d59fe325d4` in **both**
`invoke.sh` and `inputs/solve-wrapper-r004.sh`, so the inherited r004 race evidence really
does bear on the unchanged primitive. The predecessor loser capture `266af844...` really
does record `PRECONDITIONS ok`, then `mkdir ... File exists`, then the claim-refused
message - genuine post-precondition contention at the atomic `mkdir`, which the current
export capture does not show.

`finalization-02/received-review.json` faithfully records the review it claims to have
received. Verdict CLEAN, design SOUND, the reviewer's scratch paths, both digests, and all
five findings with id, severity, title, location, requirement, scenario, falsifying
observation, correction and confidence. I compared all five against the report text: nothing
is omitted, renamed, re-graded or truncated in a way that changes its meaning. A1 is
recorded as Advisory with confidence medium, as issued.

## 4. Faithfulness of the five corrections

I read each finding in `reviews/review-02-claude.md` and then the paragraph in
`finalizer-addendum-02.md` that answers it.

**M1 (race).** Faithful, and slightly sharper than the finding. The addendum states that the
loser stopped at the pre-existing-record check, that the 0/97 pair demonstrates
serialization "once the claim exists", and that the nine gate controls "do not force the
mkdir scheduling window". I verified 9 controls / 0 failures in
`checks/race-gate-controls.json`. It labels the r004 evidence as "separately identified
predecessor evidence, not a fresh export acquisition-race receipt". No overstatement.

**M2 (empty complement).** Faithful. I recomputed the membership observation in
`rehearsal/result.json`: 1081 rows, all `classification: hit`, all `in_pool: true`, all
`provider_reason: blueprint_hit`, `unsupported: 0`, no `blueprint_default` row. The
addendum's "unsupported=0 does not mean an off-pool default control passed" is exactly the
point of the finding, and the deferral to agreement's proper-subset artifact matches the
finding's own reading of design section 4.

**M3 (RED bytes).** Exceeds the requested remedy: the reviewer asked for retained bytes *or*
a prose statement, and got the bytes plus a full diff. It also volunteers a correction to
the reviewer's framing (four constants were removed as well as the guard). It discloses that
the reconstruction was made after review and was not available to the reviewer. No claim of
a new RED execution. Faithful.

**M4 (helper refusal branches).** Faithful, and it explicitly refuses the overclaim. The
four families it names - unparsable new row; absent/non-string/empty `output`; missing output
file; missing or mismatched sibling runtimes when `runtimes_sha256` is present - correspond
one-to-one to `journal_attribution.py:37, :44, :48, :57`, which I read. It carries forward
the finding's observation that none of the synthetic rows carried `runtimes_sha256`, states
"No additional synthetic tests were run here", and adds "this statement is not a claim of
executable coverage". `finalization-02/evidence.json` independently records
`additional_tests_run: false`. **No correction claims test coverage that was not added.**

**A1 (post-claim `set -u`).** Faithful on the mechanism and, importantly, does not pretend
the hazard is gone: "The frozen wrapper expands those environment variables after taking its
claim. Missing variables under set -u can therefore leave a consumed claim and start record
without a child or end record. ... Listing the prerequisite does not add a runtime guard or
change the wrapper." Its stated environment requirement is slightly *stronger* than the
mechanism strictly needs (it requires `SystemRoot` or `SYSTEMROOT` non-empty and `TEMP`/`TMP`
usable, where `set -u` alone would abort only on *unset*), which is the correct direction.

One deviation, disclosed here rather than by the finalizer: the review's literal correction
for A1 was to amend the operator instructions in `authorization-request.md`, and for M1/M2/M4
to amend `coverage.md`. Both files are frozen manifest members; editing either would have
broken manifest `9965a225...` and invalidated both reviews. The finalizer put the corrections
in the out-of-freeze addendum instead. That is the right call, and the addendum labels itself
as outside the freeze - but it means review 02's closing sentence ("all of which can be made
in `coverage.md` and `authorization-request.md`") was not achievable as written. This is an
imprecision in the review, not in the disposition. See Advisory A-01 for its one real
consequence.

**No correction overstates what was done, claims test coverage that was not added, or
quietly narrows the finding it answers.** Nothing in either finalization layer changes a
source, wrapper, helper, plan or resource value, and `changed_source` / `changed_wrapper` /
`changed_plan` are all recorded false and are all independently true.

## 5. The authorization template

`authorization-template-02.txt` is **538 bytes, one physical line plus a terminating LF**, no
CR anywhere. Every element resolves:

- source commit `1c7067448106cfa2aca3d57be879842d72293c61` = `identity.json.source_commit`,
  and a real commit whose tree matches `identity.json.source_tree`;
- the absolute `identity.json` path resolves to the file in this packet, unbroken;
- manifest digest `9965a225...` is the reviewed frozen manifest, recomputed;
- addendum digest `9d5f71ef45b8d170ce03aa38a8441a125146c295ad385591e17fc36f55417106` is the
  current `finalizer-addendum-02.md`, recomputed;
- "600 s / 2048 MiB worker Job envelope" matches `identity.json.proposed_resource`
  (`seconds: 600`, `memory_mib: 2048`, `worker_job_only: true`).

It therefore discharges review 01's M-01 in full: one line, complete path, manifest digest
present, no residual "you must also add the digest" instruction.

**Which is current: `authorization-template-02.txt`.** The two files differ in exactly one
respect - the addendum they bind (`finalizer-addendum.md` `db16f1eb...` versus
`finalizer-addendum-02.md` `9d5f71ef...`). Supersession is stated twice in current
documents (`finalizer-addendum-02.md`, "Approval wording (review 01 M-01)"; `disposition-02.md`,
"remains in force through the updated one-line authorization-template-02.txt"). So it is
determinable with certainty. It is **not** self-evident from the files themselves: neither
template carries an internal supersession marker, the two are near-identical in appearance,
and `handoff.md` - the packet's frozen entry document - predates both and points at neither.
That is Advisory A-01.

## 6. The adversarial question: was documentation the right remedy?

I answer this on the merits, not by deferring to the drafter's or the reviewer's grading.

**M1, M2, M4 - yes, clearly.** All three are disclosure defects: the artifacts are correct,
the packet's prose over-reads them. M1 does not touch the claim primitive (which I read at
`invoke.sh:106-109` and which is a plain atomic `mkdir` with no test-then-create window).
M2's underlying behaviour is right - a full pool has an empty complement, and the code takes
no default branch because there is nothing to default on. M4's four branches can only convert
`BOUND` into non-`BOUND`, which the wrapper maps to `EVIDENCE=incomplete`; no false success
is reachable through them, which I confirmed by reading `journal_attribution.py` and
`invoke.sh:136-140`. Adding tests would have been better than naming the gap, and the
addendum says plainly that no tests were added. Documentation is adequate.

**M3 - the remedy went past documentation and is stronger for it.** Retaining the bytes turns
an inference into an identification. Correct.

**A1 - this is the one that deserves real argument, and I do not think documentation is a
clean remedy. I think it is an acceptable one, for reasons of cost rather than of design.**

From the frozen bytes: `set -u -o pipefail` is in force from `invoke.sh:29`. The atomic claim
is taken at `:109`. The claim record is written at `:111-113` and the start record at
`:114-116`. The launch line at `:122` is the *first* place `${SystemRoot:-$SYSTEMROOT}`,
`$TEMP` and `$TMP` are ever expanded, and there is no guard on any of the three anywhere
above it. Word expansion precedes execution, so in a shell lacking those variables the shell
aborts before `env -i` runs. The resulting state is: claim consumed, both records on disk, no
child, no `PHASE` line, no end record, exit 1. Only the controller can resolve it.

The case against documentation is that this is the only precondition in the whole wrapper
that is enforced by accident. Every other one - mode, root overrides, authorization presence,
checkout, HEAD, plan digest, prerequisite digests, helper digest, producer digests, Python
version, untracked runs, source cleanliness, pre-existing records - sits in the preconditions
block above the claim with its own exit code, and the wrapper's header states the contract in
those terms ("A refusal before successful claim acquisition creates no new claim and starts
no child"). A missing environment variable is deterministically checkable at zero cost with
the same idiom already used at `:61`, and the correction would be strictly monotone: any
environment that survives `:122` also survives such a check, so it cannot make a currently
succeeding run fail and cannot create a false success. It would convert a post-claim abort
into a pre-claim refusal - which is the invariant the entire design exists to protect.

The case for documentation is cost and materiality. The failure is fail-closed: nothing is
misreported, and the record left behind (start record with no end record, no `PHASE` line) is
distinguishable from a child exiting 1, so the controller can diagnose it. The outcome is not
a new class - it is one more member of the already-documented class of post-claim aborts
(power loss, a failed record write at `:113`/`:116`, a kill) that the controller must resolve
anyway. The condition is not reachable in the environment this will actually run in:
Windows Git-Bash supplies all three, the r004 solve launched through the identical construct,
and this packet's own rehearsal exercised the `$SYSTEMROOT` fallback. Against that, changing
`invoke.sh` changes its digest, which changes `identity.json`, which changes the frozen
manifest, which invalidates two completed reviews, both dispositions, the RED and GREEN
receipts (both digest-bound to wrapper bytes), the gate controls and the rehearsal binding.
That is a full re-preparation and re-review to close a hazard that has never occurred and
whose worst outcome is a wasted authorization.

**My position, plainly: a wrapper change is not warranted for this invocation, and I would
authorize as-is with the residual disclosed.** But it is warranted at the next legitimate
revision of this wrapper, and it should be carried forward as a design obligation rather than
left to the operator's discipline in perpetuity - because documentation moves a safety
property out of the artifact and into a human, which is precisely the move this packet
refuses to make everywhere else. The disposition is honest about this: addendum-02 says in
terms that listing the prerequisite "does not add a runtime guard or change the wrapper", and
that the operator "must preserve and escalate that outcome, never retry it as if no attempt
occurred". That honesty is what makes the documentation remedy acceptable rather than
papering-over. It would not be acceptable if the addendum implied the hazard was closed. It
does not.

## 7. Authority

Nothing in the finalization layer grants, implies or presupposes authorization.

- `authorization.md` does not exist in the packet; `invocations/` does not exist. I checked
  the filesystem directly.
- Both templates are labelled suggested wording. `finalizer-addendum-02.md`: "It is suggested
  wording only; authorization.md remains absent."
- `disposition-02.md`: "Review completion and this disposition authorize no invocation,
  commit or push", and its next gate is "controller authorization of one retained export and
  its separately proposed 600 s / 2048 MiB worker envelope".
- `identity.json.status` still reads "awaiting Claude review and controller authorization;
  not invoked".
- "Finalizer readiness: CLEAN / SOUND" appears in both `disposition-02.md` and the addendum.
  I examined this phrase specifically for authority creep. It is qualified in place - each
  occurrence is followed by the statement that the controller's separate one-shot
  authorization and envelope decision are still required - and "readiness" is not used
  anywhere as a substitute for approval. It does not presuppose authorization.
- The coldness acceptance is likewise bounded: `accepted_as_cold: true` sits beside
  `context_basis: "delivered external report"`, and both the addendum and the disposition say
  the finalizer "did not independently observe or replay that external session's initial
  context". Accepting the label without claiming to have witnessed it is the correct posture,
  and the dispatch note records the mechanism (a fresh session opened after the coordinator's
  memory index was parked). I did not verify that mechanism; it is outside the bytes.

The controller's approval remains open and unprejudiced.

## 8. Separate judgments

**Specification judgment: SOUND.** The finalization layer does what a post-review correction
layer must do: it changes nothing inside the reviewed freeze, records what it did change with
its own manifest and preservation list, restates each finding before answering it, refuses to
relabel either review, and withholds authority explicitly. Supersession between rounds is
stated rather than implied. The two verdicts are allowed to disagree without either being
rewritten, which is the correct handling of "the later CLEAN applies to the same reviewed
manifest; it does not rewrite the earlier one".

**Engineering judgment: SOUND, with one accepted residual.** The digest chain is complete and
every link recomputes. The one substantive engineering criticism is the A1 residual in
section 6: a cheap, monotone, pre-claim environment precondition would remove a post-claim
abort class, and the packet chose freeze stability over it. That trade is defensible and is
recorded honestly, but it is a trade, not a non-issue.

**Design verdict: SOUND.** The additive out-of-freeze layer with a per-round manifest,
preservation list and evidence record is the right shape for correcting a frozen packet, and
it composes: layer 02 verifies layer 01 rather than replacing it. Its one growth cost is
visible here - the packet root now carries two templates, two dispositions, two addenda and
two finalization directories, with no current-state pointer and a frozen entry document that
names none of them. That is a housekeeping strain, not a structural one; a third round would
make it worse.

## 9. Findings

All three are Advisory. None changes the verdict.

### A-01 (Advisory) - two authorization templates coexist with no internal marker

Copying the superseded one silently drops the A1 environment prerequisite.

- **Location.** `authorization-template.txt` (`0f6bb94c...`) and
  `authorization-template-02.txt` (`5b8f500d...`) in the packet root; `handoff.md`, which
  names neither.
- **Requirement.** This project records controller authorizations verbatim from the packet's
  suggested wording, and A1's entire remedy is delivered through the addendum that the
  authorization line binds by digest.
- **Scenario.** A controller opens the packet root, sees `authorization-template.txt`, and
  copies it verbatim - it is a valid-looking one-line template naming the right commit, the
  right manifest and the right envelope, with nothing in it saying it is superseded. The
  recorded authorization then binds `finalizer-addendum.md` (`db16f1eb...`), whose own text
  says the review "remains NOT CLEAN" and "No CLEAN verdict is issued", and which contains
  no launch-environment section at all. The operator prerequisite that answers A1 -
  `SystemRoot`/`SYSTEMROOT`, `TEMP`, `TMP` - exists only in `finalizer-addendum-02.md`, and
  falls out of the authorized chain.
- **Falsifying observation.** Diffing the two templates: they are identical except for the
  addendum filename and digest. Neither contains the word superseded. `handoff.md` predates
  both. Supersession is stated only in `finalizer-addendum-02.md` and `disposition-02.md`,
  neither of which a controller is compelled by any packet artifact to open first.
- **Smallest correction.** Not an edit to the superseded file (which would perturb
  `finalization/manifest.sha256`): a one-line current-state pointer at the packet root, or a
  single sentence at the top of `disposition-02.md` naming `authorization-template-02.txt`
  as the only template to copy and `authorization-template.txt` as superseded history.
- **Confidence.** High on the observation; medium on materiality, since the wrapper binds its
  checkout, packet, plan and input digests as constants and only checks that
  `authorization.md` exists, so a wrong template cannot misdirect the invocation.

### A-02 (Advisory) - round-02 preservation drops an authority assertion

`finalization-02/preservation.json` omits the `authorization_exists` key its predecessor carried.

- **Location.** `finalization-02/preservation.json` (top-level scalars:
  `all_preexisting_bytes_preserved`, `retained_export_invoked`) versus
  `finalization/preservation.json`, which additionally asserts `authorization_exists: false`.
- **Requirement.** The finalization layer's own convention that each round records the
  authority state it observed, so a later reader can establish from the record - not from the
  filesystem at some future date - that no authorization existed when the round was written.
- **Scenario.** A later reader auditing round 02 in isolation can confirm that no export was
  invoked but has no round-02 record that `authorization.md` was absent at that time; the
  fact survives only in the round-01 file and in `disposition-02.md` prose.
- **Falsifying observation.** The key is present in the layer-01 file and absent in the
  layer-02 file. I verified independently that `authorization.md` and `invocations/` do not
  exist, so the omission is a record gap, not a misstatement.
- **Smallest correction.** Restore the `authorization_exists: false` key in the round-02
  preservation record.
- **Confidence.** High.

### A-03 (Advisory) - the A1 residual should be a carried design obligation

Not only an operator instruction in an addendum.

- **Location.** `invoke.sh:29`, `:109`, `:111-116`, `:122`;
  `finalizer-addendum-02.md`, "Required launch environment (review 02 A1)".
- **Requirement.** The wrapper's stated contract that a refusal before acquisition consumes
  nothing, and the one-shot nature of the controller's authorization.
- **Scenario.** As argued in section 6: any future launch from a shell missing `SystemRoot`
  and `SYSTEMROOT`, or missing `TEMP` or `TMP`, consumes the claim and writes both records
  without starting a child. Documentation reduces the probability and does not change the
  cost, and the instruction lives in an addendum a future operator may not re-read.
- **Falsifying observation.** No guard on those three variables exists anywhere above
  `:122`; the expansion is the first reference to each. Every other precondition in the
  wrapper sits above the claim with its own exit code.
- **Smallest correction.** Do not reopen the freeze now. Record the pre-claim environment
  check as a required change at the next legitimate revision of this wrapper, in whatever
  artifact carries forward obligations to the next phase (`next-phase.md` is frozen, so this
  belongs in the disposition or the agreement-phase plan).
- **Confidence.** High on the mechanism; medium on whether it merits tracking beyond the
  addendum's existing paragraph, which is already explicit that no runtime guard was added.

## 10. Disclosures

- Context probe **CONTEXT_PROBE_NONE**; see `inventory-03-claude.md` for the exact contents
  of what was in context.
- Prohibited files: none opened. No `progress.md` at any level, no
  `D:/Pontius-handoffs/INDEX.md`, no memory index or memory file, no conversation transcript,
  no unrelated scratch. Directory listings showed no prohibited path.
- Predecessor packets: I opened exactly one file outside this packet,
  `.../solve-run-20260910-r004/checks/race-caller-b.txt`, to verify the inherited race
  evidence claim in `finalization/evidence.json`. No predecessor review, disposition, ledger
  or authorization was opened.
- Execution: no project invocation; no wrapper, check-script or `invoke.sh` run in any mode,
  including the reconstructed RED wrapper, which I treated as evidence throughout. No solve,
  export or agreement. No worktree mutation, no commit, no push. Git read-only
  (`cat-file -t`, `rev-parse`). Worktree bytes were used for the commit/tree identity check
  only. All writes went to `D:/Pontius/tmp/export-r001-final-review`.
- What this review does not establish: I did not verify that review 02's session was
  genuinely cold - that is outside the bytes and rests on the dispatch note. I did not re-run
  the cold pass on the 47 members, and this report is not a substitute for one. I did not
  execute or evaluate the export itself.

This report authorizes no invocation, publication, commit or push. It is returned for the
controller's decision.
