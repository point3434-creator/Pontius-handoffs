# Cold Tier-C review A: v0a-i01-ab/r007

Defect verdict: **CLEAN** for the frozen FIX scope. No required correction remains.
Specification verdict: **PASS** for R2-04, R2-09, and R2-10 within the stated limits.
Design verdict: **SOUND**. Public required-entry intervals, an incremental native
writer with one close-once owner, and the separate host completion receipt fit the
contract. No redesign is required by the permitted evidence.

Candidate: `ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1`.
Manifest: `c234b4271bd665e869689fb5d976e629703b678faeb3f55532a3615edc98b189`.
Parent/base: `52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8`.
Tree: `7f8e429d60434ec5979a4ffa0eead94dfb1d9b35`.
Reviewer: independent Codex A. Date: 2026-08-30.

## Independence and identity

The initial input was `handoff-inputs-addendum-01.md`. I read the exact requirements
extract, candidate/manifest, current CLAUDE/workflow, frozen source/tests, ADR-0484,
ADR-0485 and their brief. I did not open the original r002 disposition, original
r007 handoff, implementation transcripts/plans/reports, peer reviews/checks, or
coordination notes. The review used the code-verification skill.

`checks/codex-a-inventory.md` was published before opening `coverage.md`; its SHA256
is `1b13881e8ffc9a0d02acb818d8dafecd073e86efd28926aa021b2601f87ea64c`.
The requirements extract independently hashes to
`01a3c00fa24ba4b44e68ffd711095b1c222249dfd468af7b57343a98595068ad` and deferred coverage to
`0c13a9f2b8f302d160e0b9f92690f640958fd6fb5377987c4233deae0e38d1b8`.

Every executable receipt recomputes the manifest using frozen blob bytes, explicit
`--no-renames`, whole-row sorting, and LF rows, and compares the entire row file as
well as its digest. It also proves every checked-out changed blob equals its frozen
blob and is LF-only/BOM-free. The only changed paths are runtime.py, replay.py,
trace.py, test_v0a_replay.py and test_v0a_trace.py. The parser function region and
independent accepting-verifier region are text-identical to the parent after line
ending normalization. The trace export list adds TraceWriter. See
`checks/codex-a-preservation.txt`; tracked files in both snapshots stayed clean.

## Required outcomes and direct evidence

| Requirement | Observed result | Evidence |
| --- | --- | --- |
| R2-04: host event/decision/failure serialization, iterator work, semantic computation and writes are measured outside later response walls | Independent real-operation delays are charged to exact terminal-at-entry categories. All controlled response elapsed values stay zero under the static injected clock. Failure-row serialization is directly exercised as well as success paths. | Eight-control receipts, measured A/B/all-in/rejected-input cases; affected focused suites |
| Required measurement entry fails before ordinary work | Existing focused controls observe no iterator advancement when entry fails, and no file publication or further input when the post-delivery interval cannot open. The accepted decision remains retained. | IncrementalPublicationTests; both focused receipts |
| R2-09: required rows precede next input/action | Before every later dispatch, the independent observer reads the native destination and requires its decision count to equal the real mailbox's accepted count. A/B/all-in exercise 24/9/8 such boundaries. | Independent measured native controls |
| First required write failure stops the hand without erasing delivery | A real existing leaf refuses create-new after exactly one accepted action; the sentinel remains unchanged. Compound cleanup failures do not add another action. | Existing focused first-write test; independent existing-target native schedule |
| R2-10: stable directory authority, reparse refusal and create-new leaf | Real tests attempt parent rename and junction redirection before leaf acquisition, deny parent/leaf mutation while open, refuse junction roots/ancestors, preserve existing bytes, and release handles after failed acquisitions. | StableTraceWriterTests, both focused receipts |
| Owner before probe, close once, monotonic failure | Source registers each holder before native acquisition/probes. Independent OS-protected handles force genuine CloseHandle failures; each valid handle is attempted once, later public close calls perform no native retry, and no receipt succeeds. | trace.py:480-523, 585-612; native fault receipts |
| Body/cleanup/clock cause retention | Real create-new refusal, two genuine native close errors, then a source-clock error yield exactly three trace_write_failed entries followed by clock_invalid. Two close errors without a body failure remain two separate equal codes. | Independent native schedules |
| Terminal cut cannot prove later host completion | Completed terminal bytes and legal replay remain valid after a later native close failure; receipt passed is false and trace digest null. A closing-clock failure also nulls publication duration and makes accounting incomplete. | Independent native schedules; final-publication clock tests |
| Complete A/B/all-in and typed premature schedule failures | A/B payouts and all-in automatic runout pass independent legal replay; all 20 proper A script prefixes return EVENT_ORDER in the focused suite and retain deliveries. Rejected input also preserves the first delivery. | Independent controls; IncrementalPublicationTests |
| Preserve parser, legal verifier and sealed contracts | No parser/verifier function-region changes or out-of-scope blob changes; affected parser/admission/replay tests pass. | Manifest recomputation, preservation receipt, focused suites |

Independent delay accounting observed these exact public durations in seconds:

| Real native host case | Preparation | Post-terminal | Terminal publication |
| --- | ---: | ---: | ---: |
| A | 437 | 74 | 164 |
| B | 207 | 56 | 164 |
| Automatic all-in runout | 146 | 56 | 164 |
| Rejected input with failure serialization | 57 | 0 | 164 |

These are deliberately injected correctness costs, not performance measurements.
The observer does not replace serializers, ledgers, writers, native APIs, or host
helpers. It advances the permitted deterministic clock at real operation entries.
Suspended-generator destruction after the receipt is formed is outside this cost
oracle's publication interval and is not mislabeled as input advancement.

## Execution and receipts

Actual CPython **3.11.15 ran first**, using
`D:\Pontius-tools\py311\Scripts\python.exe` and fresh shared local clone
`D:\Pontius-review-codex-a-r007-20260830`. Actual CPython **3.14.6** then used
`D:\Pontius\.venv\Scripts\python.exe` and a separate fresh clone
`D:\Pontius-review-codex-a-r007-py314-20260830`. Both were detached at the candidate.

Each process used `-B -P`, snapshot-root cwd, exact snapshot/src PYTHONPATH,
PYTHONNOUSERSITE=1, D-local TEMP/TMP, and only SYSTEMROOT/WINDIR plus these explicitly
set variables. PATH/PYTHONHOME were absent. Git was always the absolute
`C:\Program Files\Git\cmd\git.exe`; executable/version/flags/environment and
pontius/runtime/replay/trace/clock origins were asserted before test payloads.
No global safe.directory configuration was changed.

| Command mode | 3.11.15 receipt | 3.14.6 receipt | Result per interpreter |
| --- | --- | --- | --- |
| focused | checks/codex-a-focused-311-v2.txt | checks/codex-a-focused-314.txt | 115 tests, zero failures/errors/skips, exit 0 |
| adversarial | checks/codex-a-adversarial-311-final-v2.txt | checks/codex-a-adversarial-314-final-v2.txt | 8 independent controls, exit 0 |

Reproduction launcher is `checks/codex-a-launch-v7.ps1`, with required parameters
Snapshot, Python, Version, Mode, and a new Receipt path. It launches
`checks/codex-a-run-v7.py`; adversarial mode imports
`checks/codex-a-adversarial-v6.py`. Focused mode loads only the two affected suites.
The focused terminal sweep independently reports 244 normal and 31 rejected-input
clock positions across invalid/reversed/exception sources, plus 24 input-primary
controls. These counts are fresh execution results, not adopted self-report claims.

Earlier append-only receipts expose reviewer harness errors rather than hiding
retries: the first runner omitted importlib.util; the first all-in fixture wrongly
asked an already all-in big blind to check; the first compound-close observer
wrongly asserted that an unacquired holder must contain a handle; and the first
failed-input cost observer counted post-receipt generator destruction as input
advancement. The latter has a retained diagnostic receipt. Corrected checks use
new filenames, and all final checks pass without any production/source change.

## Coverage comparison and limits

The deferred claim's category and discovery walk agree with the independently
recorded inventory. Its public entry gates, retained deliveries, streaming rows,
terminal cut and stable ancestry claims were directly challenged. I did not use
its self-reported GREEN counts as acceptance evidence or open linked reports.
Its stated native-multiple-close limit was extended independently here:

- Windows SetHandleInformation set HANDLE_FLAG_PROTECT_FROM_CLOSE on one or two
  actually acquired handles. The untouched production CloseHandle calls returned
  false with error 6 and raised the observed TraceWriteErrors.
- Schedules cover one failure, two failures, two followed by closing-clock failure,
  and real acquisition-body refusal followed by two cleanup failures and clock
  failure. A separate late public close causes no repeated native attempt.
- The check removes only its own protection flags and reclaims its explicitly
  saved still-open handles after observing the receipt. This cleanup is not a
  claim that production can recover an ambiguously failed close safely.

This is not exhaustive higher-order failure coverage. Three or more failed native
closes, arbitrary subsets of ancestor handles, disk-full/short-write/flush-device
errors, failure of every post-acquisition native probe, abrupt process death, and
filesystems other than this local Windows D: environment were not exercised.
No helper-double result is offered as proof for these missing native schedules.
Source ownership order and the real exercised schedules support the bounded
verdict; the remaining limits do not demonstrate an unmet required outcome.

## Required corrections and advisory guidance

Required corrections: **none**. No Critical/Important finding or blocking coverage
finding survived verification. There is therefore no correction scenario to hand
back to the implementer.

Advisory engineering guidance: retain the current explicit boundary between
pre-publication accounting and the external receipt. If future changes add native
resource kinds or more close sites, extend the real fault schedules and preserve
occurrence identity instead of deduplicating typed codes. This is maintenance
advice, not a new acceptance gate or authorization to redesign.

No broad suite, GPU work, package installation, guarded capability/authority path,
lifecycle/owner invocation, production edit, or ceremonial commit was performed.
Slice C/inventory freshness and integration remain outside this review.
