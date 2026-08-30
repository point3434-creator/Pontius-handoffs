# Codex A independent invariant/path inventory, before deferred coverage

Candidate: 52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8
Manifest: 7e1575b18c7a9cf0c74bd956a54e899aad670349d198d7863ae1f67463583d7a
Base: 6cdf7b00dac653a9a295bbb86cdc3b5782317491
Inputs so far: r006 handoff/candidate/manifest; r005 disposition required T-01/T-02;
current CLAUDE.md/workflow; frozen ADR0485, ADR0484 and its brief; frozen trace/model
and changed trace tests. Deferred coverage, self-report, peer checks/reports and
implementation plans/narratives have not been opened.

## Requirements and independent observations to verify

| ID | Invariant | Paths and planned public-boundary evidence |
| --- | --- | --- |
| I1 | Frozen identity comes from changed stored blobs, digest-first complete rows | Recompute parent/base/tree/ref, no-renames changed paths, SHA256 each cat-file blob, LF manifest bytes; verify exactly two changed paths |
| I2 | Every interrupted response or unknown delivery forces all three terminal flags false | Decisions plus paired accepted failure; interrupted pre-delivery/rejected/unknown failure; unknown delivery with no timing; sweep flag combinations on real host prefixes |
| I3 | Unsuccessful or incomplete terminal has no settlement, and an unsuccessful terminal retains a typed primary reason | Completed late delivery, input rejection, no established start, interrupted acceptance, unknown delivery, terminal-only settlement/clock failure; independently rebind prefix and semantic digests |
| I4 | Accounting-complete implies two available finite complete category totals; incompleteness must preserve independently completed categories | Mutate each total separately on failed and successful traces; retain valid null/non-null combinations when incomplete; do not infer unrecorded interval chronology |
| I5 | First established failure cause survives later faults; schema must not invent hidden source/adapter chronology | Failure-row/decision pairs and terminal-only causes; real source fault before acknowledged/rejected/throwing adapters; source vs host-only body order; do not require first-row equality when an earlier source failure is representable |
| I6 | Event wire domain matches exact admitted runtime event values | All four variants, common fields, exact key sets; seat/index/type/range boundaries; ascending distinct private pair; blind/stack constraints; nested action exactness; board reveal order/width/distinctness; strength int/nonempty integer tuple/null with comparable domain |
| I7 | Stronger primitive/schema checks do not become legal replay or host receipt assertions | Public parse_trace on value-valid but semantically changed events; preserve real successful A/B replay; existing parser timing/count/digest controls; known excluded premature host schedule issue stays separate |
| I8 | Sealed and unrelated source are unchanged, imports/test execution resolve frozen bytes | Focused suites only in fresh D-local snapshot; assert real 3.11.15 first, then 3.14.6; -B -P, src PYTHONPATH, scrubbed environment, absolute validated PONTIUS_GIT; blob hygiene checks |

## Related-path discovery and limits

Read changed _validate_event and _validate_terminal_consistency plus parse_trace's
primitive validators, paired decision/failure checks, interrupted identity count,
and digest projection. Event constructors in model.py define pure ingress domains;
trace retains extra minimum-big-blind and rank-comparability checks. TraceBuilder
and ReplayHost/runtime outcome production are related contracts to inspect only
where needed for genuine prefixes. Existing focused trace tests supply regression
surface, but independent checks will compute their own canonical digest projection.
No runtime/host edits, lifecycle owner, broad suite, GPU, network adapter, install,
capability, source-seal or publication acceptance is in scope. Parsing cannot prove
hidden fault occurrence order, legal replay, settlement oracle truth, or final host
receipt success. Scope stays T-01/T-02 and preservation of related reader contracts.
