# Controller rulings in force for this handoff

Direct user instructions, quoted; not inferred review outcomes.

## Carried from the design lane (2026-09-08)

"go with T1 as primary, s=4, accept all six" — T1 (exact best response to the
declared passive villain) is the primary teacher; stack depth `s = 4`; brief
criteria 4–6 amended as recorded in `v0a-eval-panel-design/r001/disposition.md`;
composition and pairing helpers in the library, worker in `tools/`. T2's
determinization remains open by ruling 4.

## Runtime (2026-09-09)

"I decided to drop Python 3.11 and just use 3.14; I have no need for backwards
compatibility." CPython 3.14.6 is the only supported runtime. The repository
now says so (`README.md`, `.python-version` 3.14.6, `pyproject.toml`
`>=3.14,<3.15`). The adopted implementation design still contains the stale
"3.11.15 before 3.14.6" wording (impl r002 review M-01); the controller deferred
that textual correction and instructed that it be disregarded. No 3.11 run is
required or authorized for this candidate.

## Acceptance of the implementation design (2026-09-09)

The controller accepted `v0a-eval-panel-impl/r002` (recorded in the handoffs
repository at `613f986`) and Codex adopted it as `f647a79` on
`codex/v0a-eval-panel-impl`, the base of this candidate.

## Authorization to implement the first source checkpoint (2026-09-09)

"if you ready we ready amaze us" — authorization to implement design steps 1–3
(capacity helpers, per-hand teacher and singleton reference, preflight tool with
one-run ownership) as the first source checkpoint of Slice A. The controller
had earlier said "run gc" and similar operational instructions; none of those
bear on this candidate.

## What is not authorized

No retained capacity or preflight measurement (the development diagnostic in
`checks/` is explicitly non-evidentiary), no full-pool solve, no export or host
agreement, no ceremonial commit, no integration, and no extension of the
Slice A review-round budget, which the brief records as consumed by the two
specification rounds. Assigning reviewers to this candidate is itself the
reauthorization the brief requires; the drafter has not assumed it.
