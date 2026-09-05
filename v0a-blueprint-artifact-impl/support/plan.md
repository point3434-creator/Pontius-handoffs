# Portable blueprint artifact implementation r001

Goal: execute ADR-0490's adopted r002 codec design, with no operating run.
Base: c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98.
Spec: authoring/docs/decisions/ADR-0490-open-the-portable-blueprint-artifact-source-round.md and the three adopted documents under authoring/docs/architecture/v0a-blueprint-artifact-r002/.

## Global constraints

All exact paths, budgets, base pins, schema, imports, scalar rules, controls and acceptance populations in the adopted specification bind. No design reopening, sealed-runtime changes, analyzer repair, new dependency, operating run, commit or push. One initial implementation and at most one bounded correction. Preserve every failed candidate. Two fresh independent Tier C implementation reviews remain required. The repository's more restrictive authorization and stopping rules override generic skill defaults.

## Task 1: Implement and register the codec as one bounded unit

Read this first as the requirements entry point, then read the binding specification completely: CLAUDE.md; ADR-0490; docs/architecture/v0a-blueprint-artifact-r002/design.md, source-opening-draft.md, coverage.md. ADR-0490 activates the retained proposal, whose old draft wording is historical. Read relevant existing types and tests before coding. Work only in D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/authoring on codex/blueprint-artifact-impl-r001.

- [ ] Write independent handwritten fixtures and focused tests first; observe meaningful RED before production implementation. Do not reduce mandated coverage to meet line budgets.
- [ ] Implement only the two codec functions and typed error in the two approved source files, with exact graph validation, symmetric numeric/scalar boundaries and deterministic bytes.
- [ ] Prove real loaded-policy runtime action, complete ReplayHost hand with independent expected policy reader, miss and illegal-hit behavior; no doubles for these contracts.
- [ ] Register the exact two source origins and tests through only the six pinned exceptions. Keep the generator unchanged except its two list additions; regenerate outputs mechanically. Attribute every census delta independently. Stop if analyzer changes or extra capability grants are needed.
- [ ] Run focused correctness on floor first in fresh D-local snapshots using scrubbed child environments, absolute PONTIUS_GIT, -B -P and snapshot PYTHONPATH. Confirm 3.14.6 and both -X int_max_str_digits=640 controls. The parent supplies a task-local execution helper; do not run test payloads in the primary checkout. Do not run the broad post-CLEAN population yet.
- [ ] Self-review exact scope and line budgets. Report actual commands/results, all changed paths, RED/GREEN, unresolved issues and census attribution. No commit, push, reviewer dispatch, subagents, ADR/status changes or publication.

Report: D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/task-1-report.md. Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED with a concise summary. Parent owns freezing, independent reviews, broad acceptance and user handoff. Stop before expanding any bound.

## Controller follow-through

- [ ] Bind immutable review copy, manifest and diff, retain implementation report.
- [ ] Obtain two independent fresh Tier C implementation reviews of the whole candidate; this single implementation unit's task and whole-candidate review coincide.
- [ ] At most one bounded correction, with new retained candidate and scoped re-review.
- [ ] After both CLEAN, execute reviewed direct CPU acceptance union on both slots, floor first.
- [ ] Present verified candidate and any blockers; seek specific commit/publication authority separately.
