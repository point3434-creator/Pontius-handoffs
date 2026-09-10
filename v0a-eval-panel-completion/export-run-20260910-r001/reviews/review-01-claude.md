# Independent review 01 — Claude

**Verdict: NOT CLEAN. Findings: 0 Critical, 0 Important, 2 Minor.**

**Specification judgment:** the plan binds the correct completed retained solve, the full
1,081-hand census and the exact retained teacher, with valid prerequisites, source and
runtime identity, and it proposes its envelope separately rather than inheriting the solve
decision. Every changed wrapper binding is internally consistent. Both findings are in the
packet's documentation of its own authorization and coverage, not in the invocation path.

**Engineering judgment:** operationally sound for the bound retained export under the
disclosed ownership assumptions. I found no path by which a supported failure can look
successful, and no way for the proposed invocation to consume its claim on anything but the
bound bytes. Neither finding can cause a wrong invocation; both are corrected by editing
prose. The controller may reasonably authorize as-is with them disclosed.

This report authorizes no invocation, publication or commit.

## Independence, exposure and inventory

Probe: not applicable. This is not a fresh session and I state so plainly rather than
claim a probe result. This session drafted the four solve packets and the campaign note
that prescribes what the export phase must bind, and it read both ledgers repeatedly during
that work. It has no exposure to the drafter's reasoning for this candidate and no review of
it existed. This is therefore an independent review of Codex's candidate, and not a cold
pass in the project's sense; the controller decides whether it qualifies.

Prohibitions observed during the pass: no `reviews/` directory, no ledger at either level,
no `INDEX.md`, no memory index, no other reviewer's material was opened. Ledger exposure
predates the pass and is disclosed rather than cured. No project phase, wrapper, check
script or rehearsal was executed; `checks/rehearse.py` was read, never run. Worktree bytes
were used for identity only. Only read-only Git and CPython 3.14.6 stdlib calculations were
used, plus the frozen `eval_bridge` module imported read-only to re-derive the permutation
and universe digests.

Inventory: `checks/review-01-inventory.md`, sealed 2026-09-10T06:28:49Z, SHA-256
`2aca0a33263630121239389899cd0aaedb75b277150091b851b20079801f5197`, written and hashed
after steps 1 to 3 and before `checks/`, `rehearsal/`, `coverage.md`,
`authorization-request.md` or `next-phase.md` were opened. Not revised after sealing.

## Findings

### M-01 — Minor: the suggested approval sentence is unusable verbatim and omits a binding

Location: `authorization-request.md:48-52`.
Requirement: this project records controller authorizations verbatim and applies them to a
named packet; the same paragraph states that approval "should also name the candidate
manifest digest".

The suggested sentence splits one absolute path across a line break between
`v0a-eval-panel-completion/` and `export-run-20260910-r001/identity.json`, and it names no
manifest digest. Line 52 then tells the reader both things: that the split is one path, and
that approval should also name the manifest digest the sentence does not contain. A
controller who copies the suggestion verbatim, which is the practice this project follows,
records an authorization with a line-broken path and without the digest that binds the
reviewed bytes.

Reachability: certain, on the ordinary path where the controller uses the suggested wording.
Consequence: the recorded authorization is weaker than the packet intends, and a later
reader cannot tell from it which frozen bytes were approved. It cannot misdirect the
invocation, because the wrapper binds the checkout, packet, plan and input digests as
constants and only checks that `authorization.md` exists.

Correction: make the suggested sentence a single line containing the packet path and the
manifest digest `9965a225729a5896818127c013122f62fb3ae323889fde8ab16ea35e3e43eb17`, and
drop the instruction that the sentence does not itself satisfy.

### M-02 — Minor: the observed race demonstrates serialization, not the atomic claim window

Location: `checks/race-caller-b.txt:1`; `checks/race-observed.json`; claim asserted in
`coverage.md:20-22`; code at `invoke.sh:100` and `invoke.sh:109`.

The losing caller was refused at the pre-existing-record precondition, `invoke.sh:100`,
with "an invocation was already started (claim.d exists)". It never reached the atomic
`mkdir` at `invoke.sh:109`. The observed race therefore evidences that a second caller is
refused once a claim exists, which is the easy half, and not that two callers passing the
read-only preconditions concurrently can produce only one claim, which is the property the
atomic `mkdir` exists to provide.

Reachability: this is a coverage gap, not a defect. The claim block is byte-identical to the
predecessor wrapper, where a real race did lose at `mkdir`, so the property is inherited
rather than unevidenced. `coverage.md:20-22` states only statuses, capture count and journal
rows, so nothing is overclaimed; the nine race-gate controls test the acceptance predicate,
including rejection of a failed winner, which is the right lesson from the predecessor round.

Consequence: a reader of this packet alone could take the atomic claim to have been
exercised here. Correction: label the observed race as serialization through the existing
record, and cite the predecessor's `mkdir` race for the concurrent-acquisition property, or
schedule the two callers to pass preconditions before either claims.

## What I verified independently, and how

Recomputed rather than read from any receipt or label.

- **Identity.** Manifest recomputed over raw bytes in whole-row byte order with LF: 47
  members, digest `9965a225…`, byte-identical to the stored file and equal to
  `candidate.json`. `plans/export.json` `c55f26f6…`, `invoke.sh` `c70c9dea…`,
  `journal_attribution.py` `a20e760a…`, the last byte-identical to the predecessor helper.
- **Pinned inputs.** All eight `inputs/` copies are byte-identical to their real sources,
  including the retained solve teacher `c3ffab40…`, result `e6db93c0…`, runtimes and journal
  row, the three prerequisites, and the predecessor wrapper. `governing/brief.md` and
  `governing/design.md` are byte-identical to the frozen blobs at the source commit.
- **Admission.** I evaluated all 35 predicates of entry `validate_plan` and completion
  `validate` against the plan bytes: key set without `witness_bank`, declared root, prefix,
  universe digest and count, seeded permutation re-derived from `pool_seed`, `declared-full`
  with `pool_count` equal to `HERO_COUNT`, the three prerequisite digests equal to the frozen
  `PREREQUISITES` constants, the capacity result's permutation digest equal to the re-derived
  order, preflight `sample_complete`, and `inputs` exactly `{teacher, producer_result}`.
  All 35 pass.
- **Producer binding.** I evaluated `teacher_input`'s predicates against the retained bytes:
  teacher hands equal the planned pool prefix, board and document permutation equal the plan,
  producer status completed, phase `solve`, `cleanup_verified` and `phase_complete` true,
  coverage, `pool_count` and exact `prerequisites` dict equality, permutation digest
  re-derivation, and the producer's `teacher.json` artifact row bound with
  `retention == "complete"`. All hold.
- **Executed slices.** The producer-guard slice extracted from `invoke.sh` between its
  markers hashes to `95ac5b97…`, and the exit tail from `# Precedence:` hashes to
  `b86dd771…`, both equal to `checks/focused-checks.json`. The RED receipt carries a
  different wrapper digest and an empty guard slice, and fails exactly the three guard cases;
  the retained harness-extraction receipt carries the correct wrapper with a different guard
  slice and four failures. The RED and error receipts are what they claim to be.
- **Rehearsal.** 42 independent checks against the raw captures and the preserved snapshot,
  all pass: the four packet copies are byte-identical to the snapshot's retained files and to
  `retained-files.txt`; the end record's exit, evidence, attribution, row counts, wall and
  digests match the captures; the result's status, phase, coverage, `phase_complete`,
  `cleanup_verified`, `resource_state_verified`, empty errors and worker exit are as stated;
  the receipt's worker seconds and peak memory equal the result's; the encoding and
  membership blocks equal the result's own reports; `source_id` is `t1:` plus the teacher
  digest; the wire is 1,010,990 bytes, 37,586 under the cap, and its digest equals the
  retained blueprint bytes; membership is exhaustive over 1,081 hands with 1,081 hits, no
  disagreement and no unsupported, every row an in-pool hit with equal prepared and provider
  actions and `blueprint_hit` reason; artifacts are exactly the two expected names, both
  retained complete; the exported teacher copy is byte-identical to the retained solve
  teacher; the journal row names the result and reports `source_verified` true.
- **Focused checks.** The 31 cases assert what their names claim, and the runner exits
  nonzero on any failure. The mode guard covers unset, `0`, `1`, empty, `2`, `yes`, `00`,
  a leading space and a trailing newline. The attribution cases run the real unchanged helper
  and compare the copied row bytes, not only status and label, which closes a limitation the
  predecessor round's reviewer recorded. The exit tail is executed over all eight products of
  child status and evidence state, checking both the code and the incomplete-evidence
  message, including a child that itself exits 99.
- **Preservation.** All 53 predecessor files recorded in `checks/preservation-before.json`
  still hash to their recorded values; none is missing. The packet is untracked, no
  `authorization.md` exists, and no `invocations/` records exist.
- **Checkout.** The retained export checkout is at the adopted commit on
  `codex/eval-panel-export`, source scope clean with only an untracked `plans/`, its
  `plans/export.json` equal to the pinned digest, 59 journal rows, seven on-disk run
  directories equal to the seven tracked at HEAD, CPython 3.14.6 with NumPy 2.5.2.

## Observations, not findings

- **The off-pool path is unexercised by this phase, correctly.** Because the pool is the
  entire compatible universe, `validate_membership` can produce no `unsupported`
  classification and never reaches the `blueprint_default` reason. The design anticipates
  this and defers off-pool discrimination to the agreement phase's test-only controls. The
  receipts and `coverage.md` state hits and unsupported plainly, so nothing is overclaimed.
- **Envelope.** The proposal of 600 s and 2,048 MiB rests on one observation, 15 s wrapper,
  11.265 s worker and 787.8 MiB peak worker Job memory, which the packet states as one
  observation rather than a guarantee, and it discloses that parent memory is unmeasured and
  outside the Job limit. The completion validator constrains the envelope to the recorded
  decision only when the phase is `solve`, so this phase does require its own approval, and
  the packet correctly asks for it.
- **Guard harness fidelity.** The focused checks reimplement `sha` and `stop` around the
  extracted slices. The exit codes are faithful; only the `PRECONDITION` message prefix
  differs from the wrapper's. This does not affect any asserted outcome.
- **Snapshot retained.** Keeping the rehearsal worktree for review answers the predecessor
  rounds' limitation that a removed snapshot leaves the rehearsal inspectable only through
  captures. I used it to confirm the packet copies byte for byte.

## Coverage limits I did not close

I did not execute any check, wrapper, rehearsal or project phase, so every executed outcome
in this packet is verified by recomputation from its retained artifacts rather than by
re-running it. The compound post-launch write-failure and interrupted-cleanup paths are
unchanged from the predecessor and are not re-exercised here, as `coverage.md` states.
Parent memory remains unmeasured. Nothing in this packet establishes host agreement, teacher
strength, equilibrium quality or transfer to other boards or budgets, and the agreement
phase must bind the retained export's outputs rather than the snapshot copies.
