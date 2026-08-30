# Cold B initial inventory — r006

Author: Codex independent cold reviewer B. Recorded before opening handoff.md,
coverage reports, any r006 review, or any other reviewer's probes.

Candidate: refs/heads/review/v0a-i01-impl/r006
Commit: c74b80628a89938ca585ef3240b5c267a7174d0f
Manifest: 2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f
Comparison: r005 a8582e6d6b53b55415dab79c4a54e252d00b74ad
Candidate parent/base metadata: b357d333fc2393b7fc7dcf31f30c86616208c817
Snapshot: D:/pontius-snapshots/v0a-r006-cold-b-9b68bc30697143659ff72e0007e9789e/harness

Authority read: candidate.json; frozen CLAUDE.md; workflow.md and amendment;
ADR-0485; increment-one brief; relevant PROJECT/STATUS/ARCHITECTURE sections;
r006/r005 runtime and replay delta; runtime ownership, witness and ledger source.
No implementer narrative or coverage matrix was used to derive this inventory.

## Independently derived required invariants

| Requirement/risk | Observable boundary and evidence planned |
| --- | --- |
| Frozen identity | Recompute every parent-to-candidate changed blob, with no rename detection, deletion sentinels, LF rows and whole-row sort; compare exact manifest bytes and digest; verify clone HEAD/tree and imported paths. Checkout CRLF can differ, normalized only in comparison memory. |
| First cause survives cleanup | A settlement/verification or publication body failure must precede a later invalid/reversed interval-close fault in the receipt/journal. Execute real ReplayHost.run and public HandRuntime ownership paths with deterministic sources. |
| Clock faults remain exact | Invalid and reversed sources retain their own typed cause; a dead witness is never repaired/retried; cleanup echoes must not be duplicated or mislabeled. Count source reads and inspect ordered failures. |
| Non-clock publication construction failure | A terminal construction/serialization failure returns a typed host outcome, null complete-publication digest, false success, and any later clock fault after its cause. No unhandled exception can bypass the receipt. |
| Positive, body-only and cleanup-only behavior | Successful settlement/publication remains successful; individual body and close faults each fail closed; a complete terminal cannot establish host success after later publication/finalization failure. |
| Operation ownership order | Owned body catches must run while their interval is open; all production call sites use the owned seam. A nested already-owned failure must not be classified twice or replace its true earlier cause. Test declared supported nesting, including interaction with the sealed ledger's single active preparation interval. |
| Accounting remains honest | Returned public preparation intervals are charged exactly once; settlement and publication are disjoint; failed closure yields null affected duration/incomplete accounting; no fabricated zero or witness subtraction. |
| Primary versus secondary multiplicity | Genuine later independent same-code failures remain separate, whereas propagation of one owned failure is not a new fault. Read journal production and receipt consumption together. |
| Test-oracle independence | Existing focused tests must exercise real host/runtime/witness/ledger boundaries, establish timing order independently, and assert receipt/journal meaning rather than merely helper-call shape. Review setup reachability before trusting GREEN. |
| Scope and compatibility | Only the three r005-to-r006 changed files are evaluated for this R2-03 fix, with related runtime/clock/ledger/model/trace contracts as needed; no deferred trace/policy/value work is admitted. |

## Related paths / concrete inspection map

- src/pontius/v0a/runtime.py: OperationFailed, classify, owned_bookkeeping,
  owned_publication, private interval contexts, record/_record_closure_failure,
  measurable, accounting/finalize_accounting; dispatch and settle callers.
- src/pontius/v0a/replay.py: real ReplayHost.run settlement/oracle block,
  TraceBuilder.close and write_trace call order, receipt construction,
  primary/secondary projection, optional-publication wrapper.
- src/pontius/v0a/clock.py: MonotonicWitness failure latching and exact code.
- src/pontius/action_clock.py: public start/stop preparation and finalize,
  active-interval exclusivity; inspected but never mutated.
- src/pontius/v0a/model.py: FailureCode vocabulary and host-facing record types.
- src/pontius/v0a/trace.py: terminal construction/write boundary and exceptions.
- tests/test_v0a_replay.py: changed cases and neighboring closure controls.
- Other focused v0a suites only as needed to trace callers and existing checks;
  no broad suite, experiment, GPU, historical owner, install, or source mutation.

## Execution contract

Run sequentially on D:/Pontius-tools/py311/Scripts/python.exe (CPython 3.11.15),
then D:/Pontius/.venv/Scripts/python.exe (CPython 3.14.6). Assert executable,
implementation and full version before production imports. Use -B -P, assigned
snapshot cwd and src-only PYTHONPATH, scrubbed child environment, and absolute
C:/Program Files/Git/cmd/git.exe / PONTIUS_GIT. All diagnostics and immutable
receipts remain checks/cold-b-* in this packet. Do not mutate snapshot source,
tests or configuration. A corrected probe/receipt receives a fresh vN filename.

This inventory records questions and intended evidence, not a CLEAN verdict.
