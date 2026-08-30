# Cold review 01 - Codex A - v0a-i01-impl/r004

Defect verdict: **NOT CLEAN**. Specification: **FAIL** for R3-02.
Design verdict: **STRAINED** (advisory). Confidence: high for both reproduced findings.

Reviewer: Codex cold-a. Date: 2026-08-30. Tier-C independent pass.
Candidate: `0207430a37e1e5b31c8da8da7aa57da1bc5c88ee`.
Manifest: `ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef`.
Base: `b357d333fc2393b7fc7dcf31f30c86616208c817`.
Tree: `c5cf6cc281d2800727029737fd4ee05bd20ebbd3`.
Snapshot: `D:/pontius-snapshots/v0a-r004-cold-a-4ea61c5d8d494d66a1951cf78a019ee3/harness`.

I independently recomputed the sorted whole-row manifest from all ten frozen
changed blobs with absolute Git. It exactly equals the packet row file and
advertised digest. HEAD, parent and tree match. The ADR-0485 and brief blobs
also match the frozen base. Snapshot status was empty before and after checks.
No previous review, disposition, or another r004 reviewer's findings was used.

## Binding findings

### R4-A-01 - Important / Medium: trace-write failure is excluded from primary cause

Location: `src/pontius/v0a/replay.py:433-449`, especially lines 442-448;
observable receipt assembled at lines 603-619.

**Reproduced on 3.11 and 3.14.** Run fixture A with the real writer targeting an
already existing file under an ordinary disposable run root. The writer raises
its actual `TraceWriteError`; its implementation is not replaced. All four
mailbox acceptances and decisions remain present. The receipt is unsuccessful,
with `failure_reason=null` and `secondary_failures=[trace_write_failed]`.

The more decisive ordering control faults the real clock source at observation
137 (publication interval exit), or 138 (outer finalization), after that same
write failure. The receipt instead reports:

```text
actual:   primary=clock_invalid; secondary=[trace_write_failed]
required: primary=trace_write_failed; secondary=[clock_invalid]
```

The earlier write failure has been demoted beneath a later closure cause. The
code first collects causes in occurrence order, then explicitly removes all
`TRACE_WRITE_FAILED` values from the primary candidates.

**Contract.** Frozen ADR-0485 lines 269-284 defines secondary failures as later
typed causes and requires retaining the primary typed cause. Host success
requires publication, its measured interval, and finalization, not merely the
already determined betting outcome. Lines 361-362 and the brief's frozen
failure-outcome requirement support the same interpretation. The handoff's
interpretation is therefore rejected: a reporting failure must not replace an
existing first cause, but it is the first host failure when no prior cause
exists. This is cause selection within R3-02, not a writer-root safety audit.

**Required outcome.** Promote the first observed typed failure, including a
write failure when first; retain every subsequent failure in order. Preserve
known delivered actions and records. Verify write-only, write-then-publication
clock, write-then-finalization clock, and the reverse ordering through the real
host/writer path. The supplied probe is a deterministic RED for these cases.

### R4-A-02 - Important / Medium: aborting a rejected input loses its later clock cause

Location: `src/pontius/v0a/runtime.py:425-441`, particularly the catch at 438-441;
host cause ingestion is `src/pontius/v0a/replay.py:451-460`.

**Reproduced on 3.11 and 3.14.** Change only the first scripted opponent seat in
fixture A from 4 to 5. The real public event boundary rejects the wrong actor
with `event_order` after the first controlled action was accepted. Inject an
invalid sample, reversed sample, or an `OSError` from the source specifically
when the real `abort_transition_boundary` closes that rejected input. This is
observation 16, reached through `_release_boundary`, not a ledger double.

The host reports `failure_reason=event_order`, `secondary_failures=[]`, and
incomplete accounting. Runtime `closure_failures` is also empty. The required
later `clock_invalid` or `clock_reversed` is absent even though the actual
source fault happened. The first accepted envelope and decision survive.

**Mechanism and contract.** `_release_boundary` catches the clock error and
keeps only dead/incomplete flags. ADR-0485 lines 246-251 expressly includes
aborted transition boundaries in closure, while lines 269-279 requires the
receipt to preserve later typed failures without replacing the first cause.
This is another closure cause that must reach the host under R3-02; it is not a
re-review of event validation or the accounting formula.

**Required outcome.** Preserve the original `event_order` primary and the
actual later clock code secondary, without another clock observation or lost
delivery. An arbitrary source exception must retain its normalized
`clock_invalid` type. Verify all three fault modes at the real rejected-event
abort boundary. Merely appending to the current closure list is insufficient
if the host's eager drain then places this later cleanup fault before the
original dispatch failure.

## Design assessment - STRAINED, advisory only

The five terminal closure seams have a small, useful typed-cause collector.
However, runtime dispatch failures, runtime closure failures, and host failures
travel through different channels. The host reconstructs their order when it
receives them, and `split()` adds a type-based priority rule. The reproduced
omitted abort cause and write-before-clock inversion show why this shape invites
partial fixes even though the five normal terminal seams now work.

Advisory technique: let each runtime operation return an occurrence-ordered
batch containing its original failure and any cleanup failures; let the host
append those batches and its own failures to one ordered sequence. Derive the
primary as the first item without failure-type ranking. This is a bounded
runtime/host failure-plumbing refactor plus compound-fault checks, not a new
framework or a redesign of betting, timing, trace acceptance, or writers. The
required behaviors above are binding; this implementation technique and its
rough scope are not acceptance gates unless the controller adopts them.

## Requirement-to-evidence map

| Requirement / risk | Direct evidence | Result |
| --- | --- | --- |
| Frozen identity and source resolution | Blob manifest, parent/tree/HEAD, module paths, clean status | PASS |
| Every ordinary clock observation reports its actual type | Fixture A: 138 reads; B: 72; invalid/reversed/source fault at each | PASS: 630 schedules per interpreter |
| Five terminal closure seams report causes | A reads 134-138; B reads 68-72, observed on actual runtime stack | PASS |
| Clock-before-mismatch and mismatch-before-clock order | Compound real host schedules, also followed by write failure | PASS |
| Write-first cause retains priority | Write-only and write before publication exit/finalization clock | FAIL: R4-A-01 |
| Rejected-event closure keeps later cause | Wrong actor plus real abort-boundary source fault, three modes | FAIL: R4-A-02 |
| No source resampling after death | Source rejects every post-fault invocation | PASS: zero source resamples |
| Delivered records survive terminal closure faults | Full decision tuple and mailbox envelope equality with successful control | PASS: 30 schedules per interpreter |
| Final receipts reject success on injected clock fault | Strong assertion in every sweep case; no success case skipped | PASS |

The five advertised terminal closure seams make no calls to an already failed
witness in the supplemental checks. In the wider dispatch sweep, 228 calls per
interpreter reach an already failed witness, which refuses them before calling
the source. Thus the evidence establishes zero source resampling, not a global
absence of calls to a failed witness. This existing dispatch cleanup observation
is disclosed rather than promoted into another binding contract in this FIX round.

A bare ledger `RuntimeError` has no frozen code. I found no normal ReplayHost
schedule making it the first fault: the witness normalizes source errors, and
ledger state refusals require earlier unfinished/dead state. This is a static
reachability assessment, not proof against arbitrary private-state corruption.

## Commands, receipts and limitations

Execution order was 3.11 first, then 3.14. Each subprocess used `-B -P`, snapshot
cwd, `PYTHONPATH=<snapshot>/src`, an allowlisted scrubbed environment, and
`PONTIUS_GIT=C:/Program Files/Git/cmd/git.exe`. Before repository imports the
probe asserted the exact executable, CPython implementation, full version string
and complete version tuple. All imported Pontius modules resolved below the
exclusive snapshot. No CuPy/Torch import or GPU work occurred; baseline NumPy
was present, so these checks do not claim an optional-dependency-free install.

- `checks/cold-a-run-probe-v3.ps1 -Slot 311`: 641 cases; six contract mismatches
  across the two findings; expected exit 1; 3.7649707 seconds.
- Same command with `-Slot 314`: same results; expected exit 1; 3.3687642 seconds.
- `checks/cold-a-run-record-preservation.ps1 -Slot 311`, then `-Slot 314`:
  30 closure schedules each, plus two controls; exit 0 on both.

Actual versions:

```text
D:/Pontius-tools/py311/Scripts/python.exe
3.11.15 (main, Jul 23 2026, 14:42:43) [MSC v.1944 64 bit (AMD64)]
D:/Pontius/.venv/Scripts/python.exe
3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)]
```

Receipt hashes (SHA-256):

```text
cold-a-probe-v3-311.log a4a9349fc96225dce8241e97894457410051d1ea0431dd30814c599cde7bfa16
cold-a-probe-v3-314.log 9ffaf284a51f9422446c9b2a705e94c7039c75ce662d2e293b0587d52424c360
cold-a-record-preservation-311.log 597840064aaa71def174d492df32e397b6939baa1b7aadf136c3350c5311d0e3
cold-a-record-preservation-314.log eda73d2dd34b91464ae93eb95f103a8292273fea1764c39bf58e075d59dea473
cold-a-independent-probe-v3.py d4e23b5b675d832791a56d62f8fb0788f30a3e418877fdacea39088dfbd0c2a5
cold-a-run-probe-v3.ps1 50fbe9122317f6e08a54dbcdfbca6f2a578314b88160f4f6a2f71fcedaa870f7
```

The initial `cold-a-probe-311.log` failed an overbroad probe assertion forbidding
baseline NumPy. `cold-a-probe-v2-311.log` then failed my incorrect trace-envelope
field name (`kind` instead of `record_type`). Both are retained unchanged as
probe defects; neither is candidate evidence. Corrected v3 completed every case.
The initial sandbox Git ownership refusal was resolved with scoped execution
under the snapshot owner, without changing Git configuration.

No source, tests or config were edited. No install, broad suites, experiment,
GPU, commit or push was performed. Existing focused suite receipts prepared by
the controller are independent and were not relied on for these causal probes.
R3-01 policy authority, the separate value/dataclass audit, trace acceptance,
aggregate accounting, progressive publication and writer-root safety are outside
this verdict. The cheapest falsifying checks are the preserved compound probes;
kill criterion is any missing or reordered actual host failure. Recommendation:
retain this round as NOT CLEAN and close these R3-02 behaviors in new frozen bytes.
