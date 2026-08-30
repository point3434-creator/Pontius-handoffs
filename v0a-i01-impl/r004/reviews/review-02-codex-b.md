# Cold review B: v0a-i01-impl/r004

Reviewer: Codex, independent cold reviewer B. Issued 2026-08-30.

Defect verdict: **NOT CLEAN / FAIL**. One required R3-02 correction remains.
Design verdict: **SOUND**. Confidence: high.

## Frozen target and review boundary

- Ref: `refs/heads/review/v0a-i01-impl/r004`
- Commit: `0207430a37e1e5b31c8da8da7aa57da1bc5c88ee`
- Manifest SHA-256:
  `ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef`
- Tree: `c5cf6cc281d2800727029737fd4ee05bd20ebbd3`
- Base: `b357d333fc2393b7fc7dcf31f30c86616208c817`
- Exclusive snapshot:
  `D:/pontius-snapshots/v0a-r004-cold-b-b7262e41033a459ea8aa6bfd0ecdd54f/harness`

I independently resolved the ref, snapshot HEAD/tree, ten changed blobs, whole-row
sorted manifest bytes, and manifest-file digest. They match the frozen pair. The
snapshot was clean before execution and after the review. The r003-to-r004 diff
contains only runtime.py, replay.py, and test_v0a_replay.py (251 additions, 34 deletions).

This is the frozen FIX review for R3-02: host closure causes, occurrence ordering,
no resampling after a closure clock fault, and preservation of accepted records.
R3-01, R2-04/05/06/09/10, and the separate dataclass audit are excluded. No other
review, coordinator probe, or implementation conversation was a review input.
I read the frozen CLAUDE.md, ADR-0485, relevant charter/architecture/roadmap sections,
and the applicable amended workflow. D:/Pontius/AGENTS.md is absent.

## Required correction B-01: preserve a reporting failure when it occurs first

**Important / Medium severity (P2); high confidence; reproduced.**

Location: `src/pontius/v0a/replay.py:433-449`, specifically the category filter at
lines 442-443. Related oracle: `tests/test_v0a_replay.py:309-327`.

The ordered collection records a trace-write failure before a subsequent
publication-stop or finalization clock fault. `split()` then removes every
`TRACE_WRITE_FAILED` from eligibility for primary. Consequently the receipt names
the later clock fault as primary and moves the earlier write failure into the
collection that ADR-0485 defines as later failures. A write-only failure instead
has no primary at all.

ADR-0485 lines 269-280 require an ordered array of **later** codes, preservation of
the first primary typed cause, and unsuccessful host completion when publication
or closure fails. Lines 437-442 say to retain the primary cause and keep a **later**
write failure from overwriting an **earlier** cause. These are temporal rules;
they do not give reporting failures a permanent secondary category. The host's
completion outcome is still undetermined until publication and finalization.
I therefore reject the interpretation explicitly proposed in the handoff.

Concrete public-path reproduction, on both required interpreters:

1. Construct `ReplayHost(FIXTURE_A, ...)` with the real empty immutable blueprint,
   real mailbox, and a deterministic source returning `call_count * 1000`.
2. Use a real temporary run root containing an already-occupied `trace.jsonl`.
3. Return `True` at source call 137, the publication interval's stop observation.
   All earlier calls are valid; the destination write has already failed.
4. `run()` returns this receipt fragment:

```json
{"passed": false, "failure_reason": "clock_invalid",
 "secondary_failures": ["trace_write_failed"]}
```

Required result: primary `trace_write_failed`, secondary `[clock_invalid]`.
The same order defect occurs with a reversed sample and at finalization call 138.
Without any clock fault, the occupied destination returns primary null and
secondary `[trace_write_failed]`; its primary must be `trace_write_failed`.

The destination remains byte-unchanged, all four deliveries and their full
records survive, and the hand stays unsuccessful. Thus the defect is bounded
failure provenance corruption, not action loss or a false host success.

`checks/cold-b-order-red.py:56` asserts the ADR-derived expected primary and fails
on the candidate on CPython 3.11.15 and 3.14.6, exit 1 in each immutable receipt.
This is an implementation/oracle defect, not an environment failure.

**Binding outcome:** the first observed typed failure is the receipt primary;
all later failures retain occurrence order without category promotion. An isolated
write failure has a non-null primary. Preserve earlier clock/mismatch causes when
the write occurs later, and preserve accepted action records and failed-host status.
Verify write-only, write-before-clock, clock-before-write, and
mismatch-before-write-before-clock paths through the actual writer and host.

## Engineering guidance and design judgment

The cause is demonstrated: `note()`/`drain()` retain the relevant sequence, but
`split()` applies an unsupported priority policy over that sequence. The existing
write-failure test asserts the same policy rather than deriving its oracle from
the ADR. The published mutation receipt even treats promoting a reporting failure
to primary as a caught mutation. Mutation sensitivity cannot validate that oracle.

Advisory implementation direction: keep one ordered cause sequence and project
its head/tail as primary/secondary, without filtering by failure kind. Retain the
current exception-based clock classification and no-query guards. A small local
correction and the public-path ordering controls above should suffice; a new
exception taxonomy, event bus, or generalized transaction layer is unnecessary.

**SOUND** means the bounded synchronous queue/cursor shape fits this contract.
The reproduced defect is a wrong precedence rule, not evidence that closure
requires an architectural replacement. This assessment applies only to R3-02;
it is not approval of the deferred writer/replay architecture.

## Requirement-to-evidence matrix

| Requirement/risk | Fresh evidence | Result |
| --- | --- | --- |
| Typed cause at any source observation | All 138 A and 72 B positions, three faults each | Pass: 630/630 |
| Failed clock never yields successful receipt | Same sweep, explicitly asserted | Pass |
| Source not sampled again after failure | Exact source count equals fault index throughout sweep | Pass |
| Dead witness not queried at five closure seams | Observed public witness, five seams each for A/B | Pass: 10/10 |
| Accepted envelopes and full decisions survive | Identity/action/seat/street checks through sweep | Pass |
| Clock/mismatch and reporting order | 44 public-host combinations per interpreter | Fail: B-01 |
| ADR interpretation of write-only failure | Actual occupied file; primary null | Fail: B-01 |
| Existing focused regression suites | 35 + 25 + 31 + 22 tests per interpreter | Pass: 113/113 |

The sweep faults invalid samples, reversed samples, and an OSError-raising source.
Its first reversed attempt necessarily has no earlier valid observation and uses
an invalid negative sample; subsequent reversed samples are strictly below the
prior valid value. Expected codes account for that distinction. No production
function was monkeypatched. The 44-case diagnostic records observations; its
exit 0 does not claim the disputed ordering passed. The separate RED assertion
makes the failed requirement executable.

## Separately recorded observation: terminal row, outside this counted fix

With only an invalid sample at A bookkeeping entry/exit (calls 134/135), the final
receipt correctly names `clock_invalid`, but the already-known fault is absent
from the terminal row: `passed=false`, `accounting_complete=false`, and
`failure_reason=null`. The runtime has retained the code before construction;
`replay.py:555-556` calls `split()` without first draining it. This concerns the
terminal's own failure reason under ADR-0485 lines 361-362 and 437-442, not the
successful new final-receipt cause propagation.

This observation is **not another required correction or counted residual in
this report**: the handoff restricts this FIX to host closure receipts and leaves
prior trace/accounting contracts deferred. It is retained for that separate
surface. Later publication/finalization failures after a successful terminal
are distinct: ADR-0485 explicitly requires the external receipt to decide host
completion. Neither case permits rewriting a published trace after the fact.

## Execution and evidence

Release CPython 3.11.15 ran first at
`D:/Pontius-tools/py311/Scripts/python.exe`, followed by development CPython 3.14.6
at `D:/Pontius/.venv/Scripts/python.exe`. Each child asserted its absolute actual
executable, full patch version, CPython implementation, flags, cwd, and environment
before payload imports. Module paths resolve to this snapshot's src tree.

All payload commands use `-B -P`, snapshot cwd, exact snapshot/src PYTHONPATH,
and absolute `C:/Program Files/Git/cmd/git.exe` as PONTIUS_GIT. The child environment
is cleared, then admits only Windows essentials, packet-local TEMP/TMP, and
explicit Python/Git settings; no PATH lookup is available. Owner-context Git
resolved the sandbox ownership mismatch without changing safe.directory.

Executed via the captured launchers, in order:

- `cold-b-run.ps1`: 3.11.15, label `py311-focused`; identity plus four suites, exit 0.
- `cold-b-probe-run.ps1`: 3.11.15, label `py311-probes`, WithProbes; exit 0.
- `cold-b-run.ps1`: 3.14.6, label `py314-focused-and-probes`, WithProbes; exit 0.
- `cold-b-red-run.ps1`: 3.11.15, label `py311-red`, WithProbes; intended RED exit 1.
- `cold-b-red-run.ps1`: 3.14.6, label `py314-red`, WithProbes; intended RED exit 1.

Full argv, identity, environment keys, timings, stdout, stderr, and exits are in
the receipt files below. The wrappers deliberately fail when a payload fails;
the RED wrapper failures faithfully preserve the failed assertion.

SHA-256 of immutable diagnostic inputs and captures, relative to `checks/`:

```text
cold-b-bootstrap.py
5f069bb1bd66c16c6f02206b8376e6f9de648b2771084d338422dadb9ece082d
cold-b-run.ps1
8ebccb4c5b96d447a9e7dadcffa3aa1003be2603f758df6bdcba409f51969e5d
cold-b-probes.py
492a877ac08c240359cfb05910722961f6307e596da8f1585504fb0f62443d25
cold-b-probe-run.ps1
6ea019682b4f1fbb8faad50be9dcb663c09be50474f63ad0040bf638dc1b8414
cold-b-order-red.py
946bbefda4cdf0f13821a287ebdcd32f8c25c39fc8727a94c145570fed8bd7fd
cold-b-red-run.ps1
703cfce5e2d21908c0aa97d7f489615c9feaf86aa32aa4d1db8d2a1f81b46097
cold-b-py311-focused-receipts.json
6e388f3965cb0418d12b3e6bc929eeeae5dfaecd7b25386aaabf4a93e6eb0791
cold-b-py311-probes-receipts.json
04ed68ec0dc9bd4ee362ed465aeec24b86cc21e85f8f36eacde8c774adddfa71
cold-b-py314-focused-and-probes-receipts.json
fc8ce96b6c61df1bcbd7ba8d56931f08b45de8eb05e9bb4f8070548aa6805613
cold-b-py311-red-receipts.json
53d955d0840531cb674991ce98778cef3d2507620921168ac0275ddfe88c0d78
cold-b-py314-red-receipts.json
bd1c647531d64f02c8d9501bd8fcb92ab5406b7f07b5d1755c4b2743bde717cc
```

Receipt JSON captures retain their original physical CRLF; their hashes bind
those bytes. Scripts and this report are LF-only. Do not normalize issued captures.
The coordinator was informed and owns publication-byte preservation.

## Limits and disposition

Specification verdict: FAIL on B-01. Engineering-correctness verdict: FAIL on the
same bounded precedence defect; design SOUND. No Critical or High finding.
The existing green suites are opposing evidence for broad regression, but they
encode the disputed write-only oracle and do not falsify the counterexample.

The largest remaining in-scope uncertainty is whether an ordinary public host
schedule can produce a bare ledger RuntimeError before another named cause.
I found none; source clock errors are normalized by the real witness. No new
failure code is requested on speculation. Coverage is deterministic correctness
coverage of the frozen controls, not a timing, campaign, or strength claim.

No source, test, configuration, sealed record, lifecycle identity, or snapshot
byte was changed. No broad suite, optional GPU workload, owner, commit, push,
implementation fix, or Claude contact occurred. Acceptance remains blocked by
B-01; publish a fresh candidate for its correction and rerun the bounded RED
control against that candidate before requesting acceptance.
