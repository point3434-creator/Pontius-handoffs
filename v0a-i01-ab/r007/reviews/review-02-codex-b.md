# Cold review B — v0a-i01-ab/r007

Defect verdict: **CLEAN**. No required correction remains in the declared
publication/accounting slice after this review's focused checks.

Design verdict: **SOUND**. Required-entry measurement gates, an incremental
stream owner, retained directory authority, and the separate post-publication
receipt fit the stated contract. The native owner is registered before probes,
and ownership is cleared before each close attempt. The design does not require
a general transaction engine or changes to sealed dependencies.

Specification assessment: PASS for the scoped required outcomes below.
Engineering assessment: PASS within the explicitly tested Windows boundaries;
not a broad release, operational, timing, or exhaustive native-fault verdict.

## Identity and independence

- Candidate: `ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1`.
- Ref: `refs/heads/review/v0a-i01-ab/r007`.
- Parent/base: `52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8`.
- Tree: `7f8e429d60434ec5979a4ffa0eead94dfb1d9b35`.
- Independently recomputed manifest:
  `c234b4271bd665e869689fb5d976e629703b678faeb3f55532a3615edc98b189`.
- Exactly five changed paths: `src/pontius/v0a/runtime.py`, `replay.py`,
  `trace.py`, `tests/test_v0a_replay.py`, and `tests/test_v0a_trace.py`.

The manifest was recomputed using the absolute Git executable, `diff-tree -r -z
--no-renames`, each frozen `cat-file blob` payload, lowercase SHA-256 rows,
two spaces, POSIX paths, LF endings, and whole-row byte sorting. The computed
bytes equal the packet's manifest file, not merely its claimed digest.
`checks/codex-b-identity-31115.json` and its output are the receipt.

This was an independent cold context. Inputs were the handoff/candidate/manifest,
frozen source and tests, ADR-0485 and the ADR-0484 brief, current CLAUDE.md and
workflow.md, and the named R2-04/R2-09/R2-10 required outcomes. No implementer
transcript, plan, self-report, or peer review was used. The independent inventory
was issued before opening deferred coverage:
`checks/codex-b-inventory.md`, SHA-256
`47e13214858aae51ef98fbe9bec9d6f1fad0cb2f1edb08b9598e80743be65259`.
The later coverage file matched its pin
`0c13a9f2b8f302d160e0b9f92690f640958fd6fb5377987c4233deae0e38d1b8`.

## Required outcomes and fresh evidence

| Required outcome | Evidence and result |
| --- | --- |
| R2-04: measure ordinary host construction, iteration/exhaustion, serializers, semantic work and writes through public bookkeeping; gate bodies if measurement cannot start | The changed replay suite passes required-entry and post-delivery-entry failures, iterator/exhaustion delays, serializer/semantic delays, retained decisions and source-cause sweeps. Independent profiling added exactly 0.125 s at each actual trace JSON serialization, native path acquisition, append and native-holder close. Both A and B charged every injected cost once to the expected terminal-at-entry category or separate publication interval. Response elapsed values remained zero under the constant source. |
| Terminal cut and later host completion are distinct | Independent real-file controls poisoned the next source read after successful `TraceWriter.finish`, and separately at outer finalization entry. In both cases the stored terminal remained structurally passed, while the host receipt was failed with primary `clock_invalid`, incomplete accounting and all four accepted decisions retained. The source failed exactly once. Publication duration was null in the first case and the completed 0.0 s interval in the second. Both destinations could be renamed after return, demonstrating release. |
| R2-09: required rows publish before the next input; first failure stops further actions | Independent observations at actual iterator resumption found every already accepted decision in the real file before further input: 24 observations for A and nine for B. Real native create-new refusal on an existing leaf retained exactly one A delivery and decision, returned `trace_write_failed`, yielded no receipt digest, preserved the original bytes, and released directory authority. Existing focused checks also cover clock loss after actual first append, retained incomplete files, and no second dispatch. |
| R2-10: stable local Windows directory authority and create-new leaf | Fresh native suites exercise parent replacement before leaf creation, existing junction root/component refusal, parent/file rename denial, foreign write denial, and repeated acquisition failures without process-handle growth or later retry. The independent host controls additionally launched a separate Python process: append and truncate opens against the owned file were both denied; parent rename was denied while owned and succeeded after completion. Resulting bytes and receipt SHA-256 matched exactly. |
| Owner-before-probe, monotonic failure and close-once behavior | Frozen source registers each holder in `TraceWriter._handles` before `NtCreateFile` fills it; disk/kind inspection follows acquisition. Failed append/finish cannot resume. Each holder is cleared before native close, the writer latches its close attempt, and cleanup drains retained close errors. Real failed-acquisition and locking/release controls passed; exceptional inspection and multiple-native-close schedules have the limits stated below. |
| Body/cleanup/clock cause conservation | Both changed suites pass real host body exceptions, rejected-input cleanup schedules, caught source occurrences, hostile exception-metadata controls and the observed clock-position sweeps. Native cleanup errors are retained before interval closing. Multiple actual native-close errors are source-inspected rather than represented as executed coverage. |
| Lawful complete controls and typed final nonterminal exhaustion | A and B succeed, with four and two accepted actions respectively, exact expected settlement, real-file publication and independent legal verification. The B suite covers all-in runout. Independent checks of all 20 proper A script prefixes return `event_order`, fail the receipt, preserve every acknowledged decision and produce a parseable failed terminal. |
| Preserve the r006 parser, independent legal checker and sealed contracts | Independent AST comparison from stored baseline/candidate blobs found all 19 selected parser definitions and all three independent verifier definitions unchanged. The strict parser and replay/tampering controls pass. The five-path diff leaves model, clock and all sealed dependency blobs unchanged. |

Independent injected-work observations, identical on both interpreters:

| Control | Preparation | Post-terminal | Separate publication |
| --- | ---: | ---: | ---: |
| A | 7.25 s | 0.625 s | 1.125 s |
| B | 4.0 s | 0.375 s | 1.125 s |

These are deterministic correctness injections, not measured production costs,
operating budgets, latency estimates or experimental results.

## Commands, environment and receipts

All payloads ran from the fresh shared-object disposable clone
`D:\Pontius-tmp\codex-b-r007-01a05090\snapshot`, detached at the candidate.
The clone's checkout was not edited. Test ordering was actual CPython 3.11.15
first, then actual CPython 3.14.6. Executables were respectively
`D:\Pontius-tools\py311\Scripts\python.exe` and
`D:\Pontius\.venv\Scripts\python.exe`.

`checks/codex-b-run.py` launches each child with `-B -P`; asserts CPython,
full expected version, executable, flags, cwd and exact snapshot `src` PYTHONPATH
before payload import; and asserts origins for the five v0a modules and seven
consumed internal modules. Environment is constructed from SystemRoot/WINDIR,
COMSPEC, PYTHONNOUSERSITE, exact PYTHONPATH, absolute PONTIUS_GIT, and D-local
TEMP/TMP only. No PATH-based Git lookup occurs. Git is
`C:\Program Files\Git\cmd\git.exe`. No global safe.directory change was made.

| Payload | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| `tests/test_v0a_replay.py -v` | 62 tests, exit 0 | 62 tests, exit 0 |
| `tests/test_v0a_trace.py -v` | 53 tests, exit 0 | 53 tests, exit 0 |
| `checks/codex-b-boundaries.py` | All independent checks passed, exit 0 | All independent checks passed, exit 0 |

Exact argv, scrubbed environment, origins, output paths and output hashes are in:

- `checks/codex-b-focused-31115.json`, SHA-256
  `e9a87d259835a6a0059792356ee9ded27612fa8bc69206b5fbb171f925dedd7a`.
- `checks/codex-b-focused-3146.json`, SHA-256
  `66a89fbc1970b2588dc39e326d5c2022941565d32b88a5922f29fe4499a9d11b`.
- `checks/codex-b-boundaries-31115.json`, SHA-256
  `ff98c8d3c5c422212c2ff5b71827359b9e2e722c2f300d85513267553509981d`.
- `checks/codex-b-boundaries-3146.json`, SHA-256
  `8a41a258a4453d01b515c42b3be8667c4ffe2e4a245d786c678f25cfb4c480ae`.

The independent diagnostic SHA-256 is
`a9afd8df41c8be6e3f2376b7edea7fff8da0b5b29329de41c498701224e18199`;
the launcher SHA-256 is
`74ccbeafef1cca4a2b84c586bd9c5dee2d9b3270dcc91517c78fd56886e79b93`.
Final read-only `git status --porcelain=v1 --untracked-files=all` in the snapshot
was empty; `git diff --check` against the pinned parent exited 0 with no output.
No executable test failure or silent retry occurred. Two initial read-command
syntax/working-directory mistakes were corrected before the recorded checks;
they supplied no acceptance evidence.

## Coverage comparison, limits and advice

The deferred claim's member inventory agrees with the independent inventory:
setup, iterator advancement and exhaustion, event retention/serialization,
runout/showdown, oracle/semantics, native acquisition, append, publication and
finalization. Its required-versus-optional distinction matches the code: optional
failed reporting does not permit resumed ordinary input or successful accounting.
I validated behavior independently rather than treating its GREEN counts as proof.

No required correction is imposed. Advisory: preserve the real delay and failure
controls as new host operations are added. The existing AST guard that bans two
legacy interval names supports review but cannot alone prove that every future
ordinary operation is measured.

The native success result is for the tested Windows local-volume path only.
No cross-platform native success is claimed. This review did not force
post-acquisition native inspection failure, WriteFile/FlushFileBuffers failure,
or multiple native CloseHandle failures; their exception/ownership paths were
source-inspected. No statement of exhaustive resource-fault coverage follows
from the passing acquisition and sharing controls. No private state corruption,
remote-filesystem behavior, crash durability or machine-wide adversary claim was
tested. The independent clock faults occur through the real source witness,
not a replacement ledger, writer or host helper.

No production source/test edit, broad suite, GPU operation, install, capability
exercise, lifecycle execution, source seal, authority grant, performance run,
rehearsal, evidence-repository commit or integration was performed. Slice C and
inventory/profile freshness are outside this review. This issued report is
append-only; the reviewer will request the exclusive task-ledger append slot
separately after hashing it.
