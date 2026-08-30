# Slice C replay and bounded complete-deal correction

2026-08-30, Codex subagent abc_slice_c. Implementation handoff only; not a
frozen candidate, cold review, source seal, or acceptance claim for combined A/B/C.

## Identity and scope

Worktree: `D:/Pontius-worktrees/codex-v0a-i01-c-integration`.
Branch: `codex/v0a-i01-c-integration`.
Base: `6cdf7b00dac653a9a295bbb86cdc3b5782317491`,
`refs/heads/review/v0a-i01-ab/r005`.

Replayed exactly the seven paths authorized by `slice-c-integration-plan.md`.
The input is Claude's unfrozen `D:/Pontius-worktrees/v0a-slice-c`, not review
material. `slice-c-replay-capture.json` records each original SHA-256.
All seven input hashes were rechecked unchanged after implementation.
Only `tools/check_stabilization_boundaries.py` and
`tests/test_v0a_boundaries.py` changed after this byte-identical replay.

Exact final working-byte identities: `slice-c-final-working-identity.json` and
`slice-c-final-working-files.sha256`. Whole-row-sorted working-byte row digest:
`8abf34927f09fb4352fbe5ba1a6afdc966e01d1d1bab3c3c245ad2159fcd2e91`.
This is not a frozen-blob manifest.

Seven-path patch: `slice-c-integration.patch`, 3,315,148 bytes, SHA-256
`d15a8f53e6e72073f16218fdf20ccf4351d7e686d94098f9a22c1eae9e007040`.
The large patch includes the provisional one-line inventory JSON. Its seven
path headers were inspected; `git apply --check --reverse` passed against the
completed isolated working tree. Prefer copying exactly these seven files and
checking the raw hashes when integrating, to preserve the captured bytes.

## Behavioral correction

The original module allowlist admits `pontius.holdem_cards`, whose public
complete-deal type must remain host-only under ADR-0485. Keep every existing
module-edge rule and add an AST walk over the already captured bytes for all
non-host v0a sources. It refuses explicit `SixSeatHoldemDeal` from-imports,
including renamed imports; `Name` and `Attribute` references to that symbol;
and wildcard imports from `pontius.holdem_cards`. Relative from-imports use
the existing source-origin resolver, including package-initializer semantics.
The baseline parser normalizes malformed-byte/syntax refusals to BoundaryError.
Replay remains exempt. Comments, strings and `OneSeatCardState` remain allowed.
No source path is reopened for the new AST inspection.

This is trusted-component static dependency enforcement. It does not prove a
malicious-Python sandbox, reflective-name detection, or complete dataflow privacy.

## Test coverage and RED/GREEN

Generated cases preserve the complete repository module-path universe, retain
all six actual v0a module bodies, and replace unrelated module bodies with empty
bytes. This is a systematic module-resolution corpus, not a claim that every
synthetic case contains the full historical source. The separate repository
positive and two repository negative controls use complete real source bodies.
The negative repository controls copy source/tools/baseline into disposable
temporary roots; they never change the originating snapshot's source.

Across all five non-host origins (`__init__`, model, clock, runtime, trace):

- 230 forbidden cases: 12 absolute, relative, renamed, qualified, wildcard and
  bare-symbol forms; top-level, nested, TYPE_CHECKING, and deferred function
  contexts (wildcards stay in syntactically allowed module contexts).
- 135 approved visible-state/comment/string controls.
- 35 host-import refusals with complete module resolution.
- 15 malformed-source cases with normalized boundary refusals.
- 46 replay-host complete-deal positive controls.
- Two real repository negative mutations: runtime renamed import and initializer
  relative wildcard. The unchanged real repository must also pass.

The first overly repetitive full-history RED attempt was explicitly interrupted
for redundant parsing cost. Its log/receipt remain retained and are marked
incomplete by `slice-c-red-a7e513315f45-interrupted.json`; it is not the RED evidence.
The coordinator approved the bounded corpus distinction above before the fresh run.

| Check | Actual 3.11.15 | Actual 3.14.6 |
| --- | --- | --- |
| Fresh RED, new tests against exact copied checker | 18 methods, 232 expected subcase failures; 33.090s; exit 1 | Not required |
| GREEN `tests/test_v0a_boundaries.py` | 18 pass; 39.913s; exit 0 | 18 pass; 44.586s; exit 0 |
| GREEN `tests/test_stabilization_boundaries.py` | 48 run, 47 pass, 1 existing platform skip; 18.986s; exit 0 | 48 run, 47 pass, 1 existing platform skip; 20.236s; exit 0 |
| GREEN `tools/check_stabilization_boundaries.py` | exit 0 | exit 0 |

The skip is `test_posix_write_rejects_staged_entry_substitution_before_replace`,
reason `POSIX directory-descriptor mutation test`, on Windows. No v0a test skipped.
Every RED failure was `BoundaryError not raised` for required complete-deal
refusal: 230 generated cases plus both real repository mutations. All opposing
controls passed before the correction as well as after it.

Receipts and command/environment/overlay identities:

- `slice-c-red-936b13baca50-receipt.json`, and its named log.
- `slice-c-green-1b65b4f11285-receipt.json`, and all six named logs.
- Reproducible focused launcher: `slice-c-snapshot-checks.py`.

Each interpreter had a fresh D-local clone at the exact base plus seven overlays.
Before any payload, the wrapper asserted CPython and the full expected version,
`-B -P`, snapshot cwd and `PYTHONPATH=<snapshot>/src`; it recorded executable,
full version, path resolution, absolute Git and D-local TEMP. Environment was
scrubbed to required Windows variables plus deliberate path/temp/Git/Pythonpath
values; global/system Git config was disabled for payloads. Every Git launch
used `C:/Program Files/Git/cmd/git.exe`. Floor execution completed first.

## Preserved gates and checks

The legacy baseline remains at ADR-0485's pinned blob
`5fe6ee47f3380b65887b528efef05b72c8e6ac0a`; both new baseline identity tests pass.
The CI diff only adds the five v0a steps and explanatory comments. Existing hard
gates and the informational Ruff step are unchanged; all new steps retain
`if: ${{ !cancelled() }}`. The generator declaration adds the five v0a suites.

`git diff --check` passed. Checker, boundary tests and CI are LF-only, BOM-free,
final-LF terminated, <=100 columns, and free of trailing whitespace. Ruff was
not installed at the expected existing venv executable path; no install was made.
No current cold-review materials were opened. No broad profile, capability
writer, GPU work, historical owner, source seal, freeze, commit, push or ledger
write was performed. Worktree creation used scoped elevation and one-command
safe.directory arguments; no persistent Git configuration was changed.

## Required final combined inventory work (not run here)

1. Integrate these seven exact files with the final A/B host/publication bytes.
   Treat `tests/test-inventory.json`, `tests/test-profiles.toml` and existing
   census expectations as provisional. They remain byte-identical to the copied
   input and must not be cited as current generation evidence.
2. Capture final combined source/tests in a fresh D-local floor snapshot, using
   actual 3.11.15, `-B -P`, snapshot cwd/src PYTHONPATH, scrubbed environment,
   absolute Git, and D-local TEMP on the interpreter's volume. Run only the
   authorized `tools/generate_test_inventory.py --write` to regenerate the pair.
   Do not invoke `--write-design-capabilities` or alter approved scope/capability
   documents. Transfer only the writer's generated pair back to integration.
3. Derive the census from the completed combined corpus and mechanically refresh
   affected expectations in `tests/test_inventory_and_profiles.py`. Record every
   changed count, digest, blocker-reason count, and line-bound row with its cause.
   In particular inspect `test_working_discovery_binds_every_entry_and_introduced_id`
   and its analysis census/blocker expectations. Do not reuse the input status
   narrative's numeric claims as authority; use the actual generated outputs.
   Adding explanatory comments in that file changes line-bound digests, so keep
   provenance in the handoff report. Re-derive after any expectation edit until
   the bytes/census are stable.
4. From fresh snapshots of the final combined bytes, run `--check`, the full
   focused inventory/profile suite, all authorized A/B/C focused suites and the
   boundary gate, floor first then actual 3.14.6. Recheck generated-byte stability
   and unchanged legacy baseline. These integration gates are still required.
5. The coordinator then handles the new frozen candidate and two fresh independent
   cold reviews. This Slice C report supplies no ceremonial commit authorization.
