# Cold review — v0a-i01-ab/r005

Tier C FIX: R2-05 independent accepting replay and R2-06 strict trace admission,
plus the related independently computed settlement-oracle correction described below.
Implementer Codex; finalizer Claude. Frozen ref refs/heads/review/v0a-i01-ab/r005.
Commit 6cdf7b00dac653a9a295bbb86cdc3b5782317491; manifest 83798245d9feac931479478e81c850ac4de277a2903a7523f5745320738cd21f.
Base c6adbcaa048988361d2388970eaca772711b797b; tree 89ae2190fa69c6974750ae032a7afec3ca106f18.

Permitted cold inputs: this handoff/candidate/manifest, frozen source and tests,
ADR0485 + ADR0484 brief, current D:/Pontius/CLAUDE.md and docs/workflow.md, and
R2-05/R2-06 required outcomes from v0a-i01-impl/r002/disposition.md. Write an
independent invariant/path inventory BEFORE opening coverage.md (SHA256 007168c11b2554994ec24b1b6c821e17636f85b75257a84258c1304ac68c53d7).
No implementer transcript, plan, draft/self-report, or current peer findings.

Only trace.py/replay.py/test_v0a_trace.py/test_v0a_replay.py change. Require complete
nested canonical schema validation and typed refusal; exact prefix/semantic binding;
external source/config/policy expectations; independent legal event/decision replay,
including chance, selection and settlement; correct timing/failure/count consistency.
Parsing alone must not claim legal or host success. Preserve valid controls and
fail-closed behavior, current value/policy/cause contracts and sealed dependencies.

Additional oracle required outcome: a legal state with contributions(0,1,2,15,15,5),
folded0/1/2/5 and equal winning ranks at3/4 yields one38-chip pot for(3,4), payout
(0,0,0,19,19,0). Check independently; production pot assembly is not an oracle.
This is a new discovered dependency, not a claimed residual of earlier comparison fixes.

No writer/accounting/Slice C correction is claimed here. Those remain separately
owned; do not treat their known open scope as a residual of this trace-only round.
Verify manifest from stored blobs. Fresh D-local clone outside packet, real3.11.15
first then3.14.6, -B -P, snapshot cwd/src PYTHONPATH, scrubbed environment and absolute
PONTIUS_GIT. No source edits/broad/GPU/install. Write own checks/review only. Reports
need separate required findings, advisory guidance and design verdict, bound to this
manifest. Request exclusive task-ledger slot only after report/hash are final.
