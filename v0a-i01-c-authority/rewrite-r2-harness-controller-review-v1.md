# R2 identity harness v1: controller and custody review

Reviewer: codex/root. Design verdict: STRAINED pending R2-H1 only.

Reviewed frozen H c00f7375a7be68daff773b4d8c6413467aa2e6be, manifest
a2e7a238c4b87b46d6e48dad9106b13c39012fb674a4c0373b54873510815b5d.
Controller bb68e24c1d01b4b04eb499274c6d714c329ea8eab56cfb3a11f4394b92d5d2a9;
probe 0c1d7065b21e7d45a002b2e83e3ada9e29a22e3129e9168378370f231500c5bb.
This is an engineering harness review, not a final cold review or execution result.

The controller binds actual floor Python 3.11.15, isolated authoring flags,
the retained c8fc R1 source, both worktree watches and the three frozen input
packs. Each dispatch creates a fresh detached r010 D-local snapshot. The only
tracked overlay is the generator. All 1761 tracked files and seventeen named
payload files are hashed before import; the child checks its actual interpreter,
flags, scrubbed environment, source, original budget consume segment, test blob
and input digests before loading the generator. The two original depth setUps
each select a fresh generator module for both observers.

The controller reconciles fourteen complete JSON lines, twelve attempts and
twenty-four Model projections. Exact original depth errors, public semantics,
accounting, requested-unit reserve, mechanism availability and restoration stay
separate. A complete baseline observation may be RED. Missing future mechanism
roles never admit GREEN. Development requires a matching successful floor and
replays its raw records, setup and current snapshot/input hashes. No development
run can follow this baseline-only adapter's expected RED.

Before/after tracked and untracked state, all snapshot files, manifest and retained
input/watch bytes are checked. Timeout or incomplete output retains raw and partial
records with an explicit failed receipt. No payload has run under this harness.

R2-H1 is confirmed: observer acquisition precedes the try/finally that restores
the budget observer. A mechanism construction/installation failure can escape
without that restoration. This does not permit a success receipt, but violates
the harness's cleanup guarantee. The correction must cover acquisition through
teardown for both observers, retain any original exception, and fail admission
on cleanup diagnostics. Fixing only one installation call is insufficient.

One create-only v2 harness correction is authorized. Preserve the frozen v1,
original BudgetObserver/reconciliation, public/Model/depth envelopes, population,
all limits and R1 source. Review the new frozen pair before baseline dispatch.
No production-source GO or payload authorization is issued by this review.

The accompanying independent receipt verifier uses only stdlib data/hash/Git
operations. It is for the eventual complete R1 baseline, not a GREEN certificate
for future R2 source. Its own source review is pending; no candidate, Model,
test module or harness has been imported by that verifier.
