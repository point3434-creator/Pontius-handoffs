# v0a-i01-prereg/r005 — cold review 02 (Claude)

Issuer: Claude Fable 5, controller-side reviewer. Date: 2026-08-30.
Independence: I reviewed r2 cold (verdict CLEAN, legacy ledger line
`claude/cold_review_c`) and reviewed this round against git blobs only. I did
not read `reviews/review-01-codex-a.md`, any r3/r4 findings, or implementer
transcripts before issuing this verdict.

## Binding

- Candidate: `98328440d4425fed1dbc7eb30b26b5f785709f05`
  (ref `refs/heads/review/v0a-i01-prereg/r005`, tree `f13e21e0…`,
  base `ca0b2e41…` = the mainline commit the freeze was cut from)
- Manifest SHA-256:
  `d972987187b78a2ac5fdb6dbaa74cd7b23e1ce7fdd3a73fae5ed96a0f532da17` —
  independently recomputed from `diff-tree`/`cat-file` blob bytes with
  whole-row lexicographic sorting per docs/workflow.md; matches
  `candidate.json`, and the packet's `manifest.sha256` bytes equal the true
  rows exactly (the self-verifying property holds).
- Scope: exactly `STATUS.md`, `docs/decisions/ADR-0485-…md`,
  `docs/workflow-amendment-2026-08-30.md`.
- Pinned inputs verified: `inputs/workflow.md` hashes `c70581f3…` and is
  byte-identical to the live master blob (commit 448296a);
  `inputs/controller-rulings.md` hashes `98b371e8…` as declared.

Round history note: r004 published the same commit with a **path-sorted**
manifest file, whose digest (`402514df…`) does not reproduce under the
workflow convention (whole-row sort — digest-first). I reported that defect;
r005 corrects it with the same candidate bytes. The per-file digests were
correct in both rounds; only the sort key was wrong.

## Verification performed

Mechanical, from my own fresh disposable snapshot detached at the candidate
(scrubbed environment, snapshot `PYTHONPATH`, absolute `PONTIUS_GIT`,
`python -B -P`, CPython 3.14.6): `pontius.status_generation --check` reports
current (exit 0) and `tests/test_status_generation.py` passes 12/12 — the
candidate `STATUS.md` is the generator's honest projection including the
revised ADR-0485, and machine-checked continuity holds. STATUS depends only
on `docs/decisions/`, so this remains true when the blobs are staged onto
post-448296a master.

Substantive: I reviewed the full r2→r005 delta line by line against the
brief, checklist v1, ADR-0482/0484, and the sealed APIs, on top of my
whole-candidate r2 review.

## Delta assessment

The delta strengthens the contract in exactly the places my r2 review noted:

- **Ready-to-emit checkpoint** (closes my r2 note N1): cutoff enforcement now
  reaches the last pre-emission point — after adapter validation and envelope
  construction, before V2 emission — with "no new policy choice or decision
  work follows that checkpoint" and the explicit rule that an endpoint
  between 14 and 15 seconds alone is not a work-cutoff violation. That is
  the correct reserve semantics against the sealed constants
  (15.0/1.0, work exhaustion at 14.0), and V2's legality/application path
  plus mailbox acknowledgement are correctly classed as emission work: with
  `candidate=None` no choice exists there.
- **`private_cards` ↔ `private_hand` mapping** stated explicitly (closes N2).
- **Terminal accounting rework** (closes N4, stronger than r2): all
  non-response time now aggregates ordered public `PreparationWorkInterval`
  outputs — no witness-subtraction substitute — classified exactly once by
  whether betting was terminal at interval entry; terminal-row totals run
  through a defined pre-publication cut; the terminal row's own
  construction/serialization/write is measured as one final outer
  preparation interval reported separately as
  `terminal_publication_compute_seconds` in a host completion receipt with
  exact fields (`run_id`, `hand_id`, `trace_sha256`,
  `terminal_publication_compute_seconds`, `accounting_complete`, `passed`,
  `failure_reason`, `secondary_failures`). The receipt lives outside the
  trace it describes, the trace digest covers the completed file or is null,
  `secondary_failures` preserves later codes without displacing the primary
  cause, and trace-only replay is honestly denied the power to establish
  host completion. I verified feasibility against the sealed ledger: all
  three closers return `PreparationWorkInterval` with public
  `compute_seconds`; the outer ledger (a separate instance from V2's) can
  legally remain open past betting termination and refuses charging after
  `finalize()`, matching the required ordering.
- **Null-not-zero discipline** extended per category to the redefined totals;
  the new delay and terminal controls (distinguish >14 s decision work from
  lawful reserve use from >15 s endpoints; positive settlement/publication
  work; publication-clock failure rejects host success despite a complete
  terminal row) match the brief's delay-injection demands.
- **CodeRabbit** removed from the Tier-C sequence per the controller's
  ruling; `docs/workflow-amendment-2026-08-30.md` records the retirement
  without relabeling any historical unrun/failed sweep, and its
  circular-requirement meta-rule is properly guarded (no evidence edits,
  reruns, tuning, fabrication, or waived correctness; blockers stay).
- The Decision section now records the bootstrap-sequencing adoption while
  still explicitly withholding ceremonial-commit authorization; the change
  boundary honestly lists three files.

## Findings

No Critical or Important finding survives verification.

- **M1 (Minor).** The amendment sentence "The original workflow remains
  preserved at the accepted ADR-0478 SHA-256: `2ea6b7c8…`" reads on its
  surface as a current-state claim about `docs/workflow.md`; on
  post-integration master that file hashes `c70581f3…` (the controller's
  separately authorized handoff-packet amendment, commit 448296a, which
  post-dates this candidate's base). No automated gate consumes the
  sentence, this round genuinely does not modify the workflow file, and the
  packet's pinned inputs document both hashes — so not material. Suggested
  disposition: record that the cited hash identifies the ADR-0478-accepted
  bytes, unmodified by this amendment, while the live workflow advances by
  its own authorized commits; fix the wording in bytes only if a further
  round opens anyway.
- **Note.** The controller quotation in the amendment is attested by
  `inputs/controller-rulings.md` as a direct instruction; that provenance is
  the coordinator's record and the controller can object in disposition.
- **Carried note from r2.** `run_id` charset/length pinning remains deferred
  to source seal (excluded from the semantic projection, so identity-safe);
  unchanged and still acceptable.

## Verdict

**CLEAN** at candidate `98328440` / manifest `d9729871…`. Fit for the
first-drafter's finalization under the controller's alternation rule and,
on the controller's explicit authorization, the ceremonial commit
"Preregister the blueprint-only v0a hand contract" — staging the candidate
blobs byte-identically onto master.
