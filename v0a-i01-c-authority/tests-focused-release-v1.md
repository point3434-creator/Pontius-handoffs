# Focused controller v1: root review release

Engineering infrastructure, not a cold review or an acceptance result. The
author has not executed this controller, bootstrap, syntax/import check, or any
new candidate payload. This release authorizes no dispatch by itself. Root
must inspect the final retained candidate and all three files before running
one serialized slot.

The controller accepts only the unchanged r010 DesignReviewTests class
(53 methods) or the released v4 AuthorityTransferMatrixTests class (8 methods,
192 schedules, 212 independently harmless projections). It has no probe,
generation, corpus, broad-wall, owner, GPU, install, navigation or ledger mode.
No W, primary source, test, generated output, budget cap or issued artifact was
changed.

## Frozen inputs

| Artifact, relative to T | SHA-256 | Bytes |
| --- | --- | ---: |
| tests-focused-control-v1.py | 2676cc5e58db5a1e70044610de1876c96e23b38cd1a55c4f22f47aaa59118eba | 33020 |
| tests-focused-wrapper-v1.py | 839e30c19b825defae4fea30ec899a43cd0ad346953215421b81478ffc20ca35 | 9701 |
| tests-focused-population-v1.json | 8799fd0f5996b84397b42f12b84f19a120a3b99f4be76a78775a4e5666856362 | 5809 |

T is D:/Pontius-handoffs/v0a-i01-c-authority. Original r010 commit is
29c02f6fbd5eb0b7ddc9e816ef28f570b9839358, with 1761 tracked paths.
The original generator raw SHA is
29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692.
Design uses original test bytes SHA
c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf.
Matrix uses only T/tests-candidate-v4.py SHA
06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd.

The final controller was created once from two T/tests-checks text source
parts to avoid Windows command length limits. These are unused authoring
records, not additional executable inputs:
focused-control-v1-authoring-part1.txt SHA
152c4d1fa3e633ccd9aa39412814e07f71e8df87aceb65fa9185fe3d3eb49cc0;
focused-control-v1-authoring-part2.txt SHA
2dbc34a70534f40dc38b1645ca38844ca53f48455b09c6a4bbcaea8dda5c57da.
All released files are UTF-8 without BOM, LF terminated, and now immutable.

## Root invocation contract

Start the controller with actual
D:/Pontius-tools/py311/Scripts/python.exe and -I -S -B -P. Required arguments:

- --label: unique lowercase alphanumeric/hyphen name, at most 64 characters.
- --slot: 311 or 314.
- --kind: design or matrix.
- --source-path: absolute regular retained .py input under T.
- --source-sha: root-reviewed full SHA-256 of that retained source.
- --control-sha: the exact controller SHA above.
- --watch-sha: separately root-pinned current SHA of
  D:/Pontius-worktrees/codex-v0a-i01-c-authority-v1/tools/generate_test_inventory.py.
- For 314 only, --floor-receipt and --floor-sha: absolute T JSON receipt and
  full SHA of the completed successful 311 run for the same kind, retained
  source path/hash, control, wrapper, population, tests and W-watch pin.

No candidate version is inferred from W. The source is copied from the
explicit retained T path. W is read solely for before/after hash monitoring;
its expected hash need not equal the candidate hash. Changing the W-watch
pin between slots requires a newly matching floor receipt. A floor receipt
also binds its retained stdout, stderr, convenience log and setup hashes;
a mere coordinator assertion or exit-zero line is insufficient.

Root must serialize dispatches. The controller contains no global lane lock,
automatic dev follow-up, retry loop, fallback source, acceptance widening or
automatic cleanup.

## Isolation and evidence contract

Controller lines 339 onward verify actual 3.11.15, executable and isolated
flags. Input paths must be absolute, ordinary files with no reparse ancestor.
A new UUID directory under D:/pontius-snapshots holds a detached r010 shared
clone and a sibling temp directory. The checked absolute Git executable is
C:/Program Files/Git/cmd/git.exe; hooks, templates, system/global Git config,
attributes and fsmonitor are constrained as in the established controls.

The initial checkout must be clean and contain exactly 1761 unique tracked
paths. All tracked raw hashes are recorded. Original source/tests are also
checked against their commit blobs. Only the retained candidate source and,
for matrix, the exact v4 tests are overlaid. Controller, bootstrap, population,
job and optional floor receipt copies are included in the pre-import manifest.
The manifest itself is included in the final before/after integrity map.

The payload uses actual 3.11.15 or 3.14.6 with -B -P, snapshot cwd,
PYTHONPATH=snapshot/src, no user site, no optimization, a scrubbed environment
and D-local TEMP/TMP. These focused tests retain the existing site behavior;
the payload does not use -S, whereas the controller does. Bootstrap validates
full patch/executable/flags/environment, all manifest bytes and project import
resolution before any repository import. Only the selected class is loaded
through unittest; tests, source and unittest assertions are not monkeypatched.

The bootstrap records actual identity, exact loaded IDs, each test start/end,
and a final unittest summary. A complete successful result requires exactly
53 or 8 started/completed methods, no skip, expected failure, unexpected
success, error or failure. Matrix stdout is additionally checked for exactly
192 unique case records, 212 witnesses, all eight exact family populations,
empty unreachable-case/oracle-error/analyzer-error lists, and unchanged
92 required-refuse / 81 required-clean / 19 permitted-refusal classifications.
The original matrix assertions still determine semantic correctness;
the controller only validates completion and record shape.

Every run creates exclusive setup/receipt/raw stdout/raw stderr/convenience
log files in T/tests-checks named focused-LABEL-KIND-SLOT. Existing names
are refused. Files and snapshots are retained on failure. The combined log is
LF normalized; the separate streams preserve exact original bytes.

The direct owned payload process has a 60-second watchdog. On timeout it is
killed, waited for, and recorded with actual return code, PID, elapsed time,
logical exit 124, last started/finished test and available matrix last-completed
case/projection counts. It makes no descendant-process termination claim.
A timeout is incomplete verification, never a product RED. Each setup or
integrity Git subprocess independently has a 60-second timeout; the controller
wall time is therefore not a single global 60-second deadline.

A real nonzero payload exit propagates unless an infrastructure/integrity
failure requires exit 2; timeout remains 124. A child exit 0 with missing,
invalid or incomplete evidence becomes exit 2. Final success requires all
tracked/payload bytes, HEAD/status/untracked population, and every original
input/W-watch hash unchanged. A passing process cannot hide a failed integrity
or verification result.

## Authoring checks and limits

Read-only PowerShell checks recomputed all three release hashes and verified
LF/no-CR bytes. Static method-name extraction from the retained original
r010 tests (raw c467...) matched all 53 design names. Static extraction from
unchanged v4 tests matched all eight matrix names. Existing v4 _exercise was
read to bind emitted record schemas and preserve independent harmless
oracles, required blocker/clean assertions and permitted refusals.

These are static authoring checks only. No Python parser or controller
self-test has run. The prototype six-slot pass does not validate this new
controller or any production candidate. Root must inspect and independently
validate the control before its first focused dispatch. Case records are
preserved for causal diagnosis; a focused unittest failure is not itself
labelled a demonstrated production defect by this infrastructure.
