# Cold review — v0a-i01-ab/r006

Tier C FIX: r005 T-01 all-outcome terminal consistency and T-02 exact wire event admission.
Implementer Codex; finalizer Claude. Frozen ref refs/heads/review/v0a-i01-ab/r006.
Commit 52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8; manifest 7e1575b18c7a9cf0c74bd956a54e899aad670349d198d7863ae1f67463583d7a.
Base 6cdf7b00dac653a9a295bbb86cdc3b5782317491; tree 8f5e35e5c266d8a8fa4c63e96550a4e9ef894216.

Permitted cold inputs: handoff/candidate/manifest, frozen source/tests, ADR0485 and
ADR0484 brief, current D:/Pontius/CLAUDE.md and docs/workflow.md, and required outcomes
T-01/T-02 in r005/disposition.md. Record an independent invariant/path inventory
BEFORE opening coverage.md (SHA256 8316fc9dc13bac5b66142f73ffc992b537f009736bde77694eb9eec7b0a6ee46).
Do not read plans, implementation reports/transcripts, sibling checks or peer reviews.

Scope only src/pontius/v0a/trace.py and tests/test_v0a_trace.py. Require typed refusal
of contradictory failed-terminal flags/settlement/reason/totals and invalid event
values, including descending private cards. Preserve honest failed prefixes and
compound source/adapter causes; the wire schema cannot reconstruct hidden chronology.
Parsing alone does not claim legal replay or final host receipt success. Preserve
existing successful replay, timing/count/digest and sealed contracts.

Publication/accounting and C remain separately owned open scope. In particular,
ReplayHost's premature scripted schedule with null failure reason is a known producer
issue owned by the upcoming publication round, not permission to weaken this reader.
The independent legal checker and settlement oracle are unchanged in this round.

Verify the manifest from frozen Git blobs. Run only focused permitted checks in fresh
D-local disposable clones, actual3.11.15 first then3.14.6, asserted executable/version,
-B -P, snapshot cwd/src PYTHONPATH, scrubbed environment and absolute PONTIUS_GIT.
No source edits, broad/GPU/install, capability or lifecycle execution. Write only your
own checks/inventory/review. Both defect and design verdicts are required. Findings
bind to this manifest; required corrections need concrete scenarios. Separate advice.
Request the exclusive task-ledger append slot only after report/hash are final.
