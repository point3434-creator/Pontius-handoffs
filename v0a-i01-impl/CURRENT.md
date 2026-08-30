# Increment one — current state

As of 2026-08-30, after r004 review. Maintainer: Codex coordinator.
Navigation only: this page may change. It is not a handoff, acceptance evidence,
or a substitute for a frozen commit plus manifest SHA-256.

Latest reviewed implementation pair:
- v0a-i01-impl/r004
- Candidate: 0207430a37e1e5b31c8da8da7aa57da1bc5c88ee
- Manifest: ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef
- [Disposition](r004/disposition.md): NOT CLEAN; design STRAINED.
- Scope: R3-02 only. Claude retains implementation finalization.

## Board

| Work | Standing | Next action |
| --- | --- | --- |
| Outer violation flags R2-02 | Closed by r003 scoped review | Preserve regression coverage |
| Complete settlement comparison R2-07 | Closed by r003 scoped review | Preserve regression coverage |
| Known delivery count R2-08 | Closed by r003 scoped review | Preserve regression coverage |
| Host failure closure R2-03 / R3-02 | Open after r004; second residual, two mechanisms | Written root-cause note before next isolated fix; bounded ordered-cause refactor recommended |
| Policy authority R2-01 / R3-01 | Open; second residual from r003 | Root-cause note published; await its own frozen implementation candidate |
| Trace acceptance R2-05 / R2-06 | Deferred; not reviewed by r004 | Independent legal replay and strict schema correction slice |
| Publication/accounting R2-04 / R2-09 / R2-10 | Deferred; not reviewed by r004 | Measured work, incremental writes and stable writer-root slice |
| Event/envelope/receipt admission V-01 / V-02 / V-03 | New separate audit, three Important findings | Own bounded admission-validation slice; not an r004 residual |
| V2 ticket/result wrapper suspicion | No supported incoming wrapper defect established | No sealed-spine rewrite justified by this audit |

Original r002 board: three closed contracts, two open contracts, five deferred.
The three value-admission findings are additional contracts, not a change to
those ten dispositions. Closed scoped reviews do not mean the increment or a
whole candidate has been accepted/integrated.

## What r004 established

The five normal terminal clock-closure seams report their typed causes.
113 focused tests per interpreter pass. Both independent passes and coordinator
fault campaigns confirm meaningful progress, while real compound schedules fail:
a first write failure is demoted, and a clock failure during rejected-event
abort disappears. Preserve these REDs and the passing controls.

## Useful references

- [Implementation verdict ledger](progress.md)
- [r003 disposition and residual history](r003/disposition.md)
- [r004 disposition and next-fix obligations](r004/disposition.md)
- [Policy root-cause note](R2-01-root-cause.md) — published implementer analysis,
  not approval of a new design/candidate
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
