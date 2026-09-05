# v0a consolidation r004: bounded CPU acceptance and seal preparation

Issued 2026-09-04 by the coordinating Codex session.

Execution verdict: PASS for the explicitly listed CPU correctness wall on both
supported interpreter slots. No new required source correction was found.
Overall handoff status: acceptance evidence complete for that wall; controller
disposition and the actual source-seal record remain pending. This is not an
issued seal, an integration, a broad-profile result, or commit authorization.

## Identity and preservation

- Candidate: fe1e2fc68675c6c92a1263450b455011b5987207.
- Base: bb959371eec17e76ab46ee6e42f1bac49c26d54a.
- Tree: 27fa787e80f504f17233c29961d9df545f8eb7dd.
- Manifest: 6eb5ec280b6a8051e88d7659920ef74b46ea682a06dc80f688ed951d75f3f221.
- Frozen source: D:/Pontius/tmp/v0a-consolidation-r001-r004-frozen/repo.
- Working source: D:/Pontius-worktrees/v0a-consolidation-r001.

A fresh run of the retained identity checker independently recomputed the
manifest from frozen Git blobs using whole-row sorting. The ref, parent, tree,
all ten exact r007 imports, and the preserved dependency-baseline blob matched.
Receipt: identity-recheck/result.json and stdout.log under the floor root below.
Both complete acceptance runs verified all 17 working-source and snapshot
hashes before and after execution. The source HEAD remains bb95937; no candidate
file, index, ref, sealed file, dependency file, ADR, STATUS, or sdd/ ledger was
edited by this acceptance-preparation work. No commit or push was performed.

## Why this test population

ADR-0485's acceptance map requires permitted broader gates, actual 3.11 and
3.14, the existing CI hard gates, and the complete affected inventory suite.
ADR-0486 removes general analyzer repair from scope and grants no guarded/broad
profile authority. The chosen population is the existing CPU CI hard gates,
the four v0a suites, and six unchanged direct-kernel suites. These are ordinary
isolated correctness checks, not scientific owners or capability-approved
profile execution. The controller's proposed acceptance interpretation is
explicit in source-seal-decision-draft.md; repository-wide scope is not silently
claimed complete.

## Fresh execution results

Each interpreter used its own fresh D:-local clone detached at the exact r004
commit, whose checked-out candidate bytes matched the working-source hashes.
No dirty source overlay was needed. Every command used -B -P, snapshot cwd,
snapshot/src PYTHONPATH, scrubbed PYTHON/GIT_/PONTIUS_ variables, no user site,
absolute C:/Program Files/Git/cmd/git.exe, and D:-local TEMP/TMP/TMPDIR.
The normal Windows identity was used for native handle and hardlink contracts.
The entire floor run completed before the development run started.

| Population / command | Tests | CPython 3.11.15 | CPython 3.14.6 |
| --- | ---: | --- | --- |
| Four v0a suites: hand replay, trace, replay, contract faults | 182 | PASS | PASS |
| Inventory and profiles | 88 | PASS | PASS |
| Stabilization boundaries | 52 | PASS, 1 platform skip | PASS, 1 platform skip |
| Status generation; evidence errors/model, manifests, manifest generation | 91 | PASS | PASS |
| Orchestration imports and configuration; retained-evidence inventory | 60 | PASS | PASS |
| Action clock, preparation bank, V2 spine, betting, cards, blueprint | 53 | PASS | PASS |
| STATUS freshness; generator --check; public boundary command | n/a | exit 0 each | exit 0 each |
| Interpreter identity command | n/a | actual 3.11.15 | actual 3.14.6 |
| Total | 526 | 23 commands, 0 failures | 23 commands, 0 failures |

Each run contains 19 complete test suites: 525 non-skipped tests and one
existing POSIX directory-descriptor mutation skip on Windows. No test was
selected away or newly skipped for this acceptance. Expected negative-control
refusals and the 3.14 synthetic return-in-finally warning are not test failures.

Exact commands, executable paths, exits, durations, stdout and stderr are in:

- Floor: D:/Pontius/tmp/v0a-r004-cpu-acceptance-311-1788562021546/.
  results.json SHA-256:
  bfd918a728aca921806f9c050ae0f37e265f87202729177b4925224b1897f74e.
- Development: D:/Pontius/tmp/v0a-r004-cpu-acceptance-314-1788562329291/.
  results.json SHA-256:
  32e9545edb009f001a37651197424e0dc63961a590e26a6c27986815fbbcb448.

Runner: D:/Pontius/tmp/v0a-consolidation-r004-cpu-acceptance.ps1, SHA-256
dccae30b47eeef38b8c0c14479522c307743505a039cdb4993072c0fd8c3507a.
Its command population was fixed before the floor run. All commands ran once
per interpreter in this acceptance round; no failed run was retried here.

## Requirement-to-evidence map

| Requirement or risk | Evidence and result | Remaining boundary |
| --- | --- | --- |
| Preserve reviewed core | Ten Git blobs equal r007; 182 v0a cases pass twice | No new whole-core design review is claimed |
| Crash becomes typed blocker, no new grant | Both r004 cold reviews, public RED/GREEN record, full inventory suite | General analyzer soundness remains explicitly unclaimed |
| Registration is reproducible | Earlier ordinary --write receipts and fresh --check pass on both slots | No capability approval or guarded profile |
| Origin/import boundaries and inherited kernels | Boundary suite/command, baseline blob, six kernel suites pass | No new legacy outgoing edge or baseline regeneration |
| Existing CI hard gates are preserved and executable | Frozen CI diff and every direct hard-gate payload pass locally | No hosted Actions run, setup-uv run, or dependency install |
| Runtime and reader inputs are identifiable | Identical fixture/schema/API/origin materialization on both slots | An observed import list is not a dynamic-completeness proof |
| No contamination of history or candidate | Hash checks and read-only source inspection | No source seal, rehearsal, invocation, or evidence claim |

## Retained caveats and proposed disposition

The earlier r004 development inventory run failed the inherited numeric-handle
reuse fixture before its intended fault schedule was established. An exact
bb95937 baseline diagnostic independently failed the same assertion. The fixture
methods are unchanged. Those failed receipts remain failures, and the precise
cause of a process not reusing the selected number remains unestablished.

Both current complete acceptance runs execute all 88 inventory tests and pass;
so did the independent reviewers' complete normal-identity runs. This is current
passing evidence, not a fixture repair. Recommendation: carry the inherited
reliability issue visibly without reopening r004 or waiving its test. The
controller must accept that disposition; this report cannot grant a waiver.

The full original record is
D:/Pontius/tmp/v0a-consolidation-r004-candidate-report.md, SHA-256
982201efacfbe46626af694f6a92e4c98bc15ace95ac44fb56836c063f384c64.
It links the failed candidate receipt and fresh baseline diagnostic. The two
r004 CLEAN/SOUND reviews and B's append-only count correction are linked by
D:/Pontius/tmp/v0a-consolidation-r004-review-outcome.md, SHA-256
2dc24fbce80af1a789f7dcc9c0d763df298f676ab791480ad6d496b68e1e9c36.
That record also retains the reviewer process-stop coordination uncertainty;
final verdicts used complete normal-identity reruns, not partial output.

The preserved r007 core review/disposition is at
D:/Pontius-handoffs/v0a-i01-ab/r007/; its candidate is
ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1 and manifest is
c234b4271bd665e869689fb5d976e629703b678faeb3f55532a3615edc98b189.

## Next step, and work deliberately not done

Use the adjacent proposed decision to settle acceptance scope and the inherited
fixture disposition, then issue the exact source-seal record and present its
specific commit change set for authorization. The library-only API/argv boundary
must be explicit in that record; no launcher is added to r004 on inference.
Publication, governance metadata and generated STATUS are finalization work,
not completed by a CLEAN source review or this passing check set.

No hosted CI, informational Ruff run, native diagnostic instrumentation,
repository-wide guarded profile, POSIX run, GPU work, dependency install,
historical owner, rehearsal, or experiment was performed. No backup completeness,
timing distribution, operating budget, authoritative population, poker strength,
or strategy result is claimed. Every other lane remains parked.
