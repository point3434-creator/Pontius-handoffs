# Increment one — current state

As of 2026-08-30, after r005 review. Maintainer: Codex coordinator.
Navigation only: this page may change. It is not a handoff, acceptance evidence,
or a substitute for a frozen commit plus manifest SHA-256.

Latest reviewed implementation pair:
- v0a-i01-impl/r005
- Candidate: a8582e6d6b53b55415dab79c4a54e252d00b74ad
- Manifest: e9b0baf12e258d66a92169d38137cbf2f42317158b6515ac377f745bbc52093a
- [Disposition](r005/disposition.md): NOT CLEAN; design STRAINED.
- Scope: R2-03 only. Claude retains implementation finalization.

## Board

| Work | Standing | Next action |
| --- | --- | --- |
| Outer violation flags R2-02 | Closed by r003 scoped review | Preserve regression coverage |
| Complete settlement comparison R2-07 | Closed by r003 scoped review | Preserve regression coverage |
| Known delivery count R2-08 | Closed by r003 scoped review | Preserve regression coverage |
| Host failure closure R2-03 / R3-02 | Open after r005; third residual, two host-body mechanisms | Complete cause ownership before exceptional unwind; fresh isolated candidate |
| Policy authority R2-01 / R3-01 | Open; second residual from r003 | Root-cause note published; await its own frozen implementation candidate |
| Trace acceptance R2-05 / R2-06 | Deferred; not reviewed by r005 | Independent legal replay and strict schema correction slice |
| Publication/accounting R2-04 / R2-09 / R2-10 | Deferred; not reviewed by r005 | Measured work, incremental writes and stable writer-root slice |
| Event/envelope/receipt admission V-01 / V-02 / V-03 | Separate audit, three Important findings | Own bounded admission-validation slice; not an r005 residual |
| V2 ticket/result wrapper suspicion | No supported incoming wrapper defect established | No sealed-spine rewrite justified by this audit |

Original r002 board: three closed contracts, two open contracts, five deferred.
The three value-admission findings are additional contracts, not a change to
those ten dispositions. Closed scoped reviews do not mean the increment or a
whole candidate has been accepted/integrated.

## What r005 established

The append-only cause journal corrects both previous r004 mechanisms: first
writer failure stays primary, and a rejected-event abort retains its later clock
cause. All 119 focused tests pass per actual interpreter.

Two host-body cases remain: an oracle exception is recorded only after cleanup
and can be overtaken by its clock fault; a real shared-witness fault inside oracle
work can vanish because the typed catch assumes another seam already retained it.
Both independent reviewers and the coordinator reproduce these on 3.11.15/3.14.6.

Keep the journal. The bounded next change is ownership at operation boundaries,
before exceptional unwind; widen the test model beyond ledger-close calls.
No whole solver, hand or sealed-spine rewrite is supported by these findings.
The R2-03 pre-fix root-cause note exists; the new round should explain the newly
exposed host-body/origin gap without rewriting historical evidence.

## Workflow refinement

[coverage-guidance/r002](../coverage-guidance/r002/disposition.md) is CLEAN.
The primary workflow/templates now contain a small category/discovery declaration,
shared reviewer discovery and independent behavioral evidence guidance.
Missing evidence may be closed by a new check that already passes; demonstrated
behavioral defects retain RED/GREEN. No new ADR or approval stage.

These documentation edits remain uncommitted in the source working tree and
coexist with separate pending design language. The frozen documentation pair
excludes that unrelated language. The new coverage.md arrangement was not applied
as a retrospective gate to r005. Review-packet publication is not source
integration.

## Useful references

- [Implementation verdict ledger](progress.md)
- [r005 disposition and next-fix guidance](r005/disposition.md)
- [r004 disposition and residual history](r004/disposition.md)
- [Host cause root-cause note](R2-03-root-cause.md)
- [Policy root-cause note](R2-01-root-cause.md)
- [Separate frozen value audit](../v0a-i01-value-boundaries/r001/disposition.md)
- [Program dispositions](../progress.md)

The value audit binds r003 bytes:
candidate 47d08d8c1556d776358e15811e3e98b859fd6a8b,
manifest cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a.
Ordinary skipped-constructor subclasses were tested at real public boundaries.
The V2 wrappers have no __post_init__ and are internally produced; invalid
standalone construction alone was not treated as a defect.

## Execution and handoff rules to remember

Actual CPython3.11.15 first at D:/Pontius-tools/py311/Scripts/python.exe;
then CPython3.14.6 at D:/Pontius/.venv/Scripts/python.exe. Run from fresh
disposable snapshots with the recorded environment, never infer an interpreter
from a report label. No broad-suite or GPU approval is implied by these audits.

A next submission is a fresh frozen ref plus manifest SHA; changes mean a new
round. Keep correction contracts isolated and issued reports immutable.
Required behavior is binding; suggested techniques remain advisory unless
adopted. No source implementation was changed during these review passes.
