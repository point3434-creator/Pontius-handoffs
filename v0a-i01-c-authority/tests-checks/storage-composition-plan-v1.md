# Storage composition coverage plan v1

Date: 2026-08-31. Author: Codex mapping_compatibility subagent.
Engineering coverage authoring only. This is not a presumed product RED, cold
review, acceptance verdict, execution authority, or production-integration approval.
Root must inspect the cases, probe and control before any control/payload invocation.
No production/worktree/test-method/generated-file changes are included.

## Frozen scope and files

T = D:/Pontius-handoffs/v0a-i01-c-authority.
Files are under T/tests-checks and were created once; old scopes/cases remain intact.

storage-composition-cases-v1.json
SHA-256 faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709
storage-composition-probe-v1.py
SHA-256 5dd945a7cbe4430c1433633653fbf18172e129075ac265d33617f6255c9d1997
storage-composition-control-v1.py
SHA-256 e1066d7e9a96dd1bdd4c27da7ae2ac3a9ab4cbbe01b5bdf43952dd7c806606a7

The four public source strings and four independently assembled harmless source
strings, their individual hashes, expectations, traces and dead events are frozen
together in the case pack. The pure programs are literal Model programs with local
objects and an event/return sink. They were not produced by transforming an
executable subprocess fixture. There are no oracle imports. Only the pure
oracle_source field can reach exec/compile in the probe. Sensitive source is
parsed as AST and passed as bytes only to derive_design_review.

The coverage rationale is retained in engineer-storage-coverage-inspection-v1.md,
SHA-256 b3394dc460e04e51fbe79268e3a2e6b1449e4200ffcfecc8a3bfe5d22234a90a.
No private numeric-ID equality or invented forward-reference test is added.

## Fixed expectations before any analyzer output

Exactly four cases, four harmless projections: two clean and two refuse. No
permitted-refusal category exists, and an unexpected result does not authorize
weakening any expectation.

- shared-list-consumed: the same list is bound to first and second; first appends a
  mutator and second extracts/invokes it. Harmless trace is
  [relay, store, callback, write], final TypeError, with sink absent.
  Public classification is refuse: at least one explicit blocker is required.
  Merely losing the row cannot satisfy the assertion.
- shared-list-dormant: the otherwise identical direct helper appends the callback
  but does not invoke second[0]. Trace [relay, store, sink], result fixed, with
  callback/write absent. Require no blockers and exact subprocess argv [-m, fixed].
- class-adoption-unsafe: an outer cell starts None; a class body calls the local
  nonlocal setter with ReviewTests; the saved direct reader is called afterward.
  Trace [change, read, write], final TypeError, sink absent. Require a blocker.
- class-adoption-safe: the same cell starts ReviewTests and the class-body setter
  installs None. Trace [change, read, sink], result outer, write absent.
  Require no blockers and exact subprocess argv [-m, outer]. The class-local
  module="inner" must not replace the enclosing module="outer".

The two clean expectations use represented behavior already protected by the
existing contract. Dormant native storage is not callback execution; the helper
body is direct, uses the known append operation, and returns no extracted callable.
There is no unsupported effective-result precision demand. The safe class case
uses direct local functions, a nonlocal cell, ordinary class namespace isolation
and a literal sink argument, without reflection, metaclass behavior, fabricated
identities, returned closures, or general async interpretation.

The unsafe cases check feasible reached writes independently from the TypeError.
Their harmless traces record the write event explicitly; TypeError alone is not
treated as evidence that a write occurred. Case-local class namespaces prevent
one projection's sink mutation from leaking to the next.

A failing harmless trace is an oracle/infrastructure failure, not product RED.
An analyzer exception or existing-cap refusal is recorded separately, not silently
converted into a semantic result. A semantic failure is retained against its exact
generator hash for diagnosis. There is no expectation change after observing it.

## Public probe behavior

The probe calls only derive_design_review with a one-test synthetic inventory.
It logs all public expanded rows/blockers, argv, complete expected/actual harmless
traces/results, source/oracle hashes and a public receipt digest per case.
It does not patch production functions or inspect cells/objects/certificates.

The probe verifies all five unchanged caps before and after the four calls:
helper depth64, child depth4, container4096, cardinality2147483647, work262144.
No budget increase, wall-time performance assertion or corpus headroom claim exists.

The summary's projections=4 is the fixed number of attempted oracle projections;
valid completion additionally requires four case records with oracle_passed=true
and no oracle_errors. analyzed_cases separately counts completed public calls.
An invalid oracle prevents that case's analyzer call.

## Finite isolated control for root review

The new control is stdlib only, guarded by main, and has no payload work on import.
Invocation requires the exact control runtime:
D:/Pontius-tools/py311/Scripts/python.exe -I -S -B -P

Positional arguments are:
LABEL SLOT RETAINED_OVERLAY_SOURCE_PATH EXPECTED_OVERLAY_SHA256

There is no implicit worktree read and no default source pin. The overlay must be
an absolute regular non-reparse Python file under T and must match the supplied
lowercase SHA-256. Naming engineer-generator-v19.py additionally requires its
known v19 hash. A future retained v20 source is admitted only when root explicitly
supplies its reviewed path and exact hash. No future v20 hash is invented here.

Each slot creates a separate D:/pontius-snapshots/storage-composition-UUID directory,
clones the repository, detaches exact r010 commit
29c02f6fbd5eb0b7ddc9e816ef28f570b9839358, verifies a clean initial snapshot and
r010 generator SHA-256
29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692,
then overlays only tools/generate_test_inventory.py. No test overlay is needed:
the standalone probe imports the analyzer, not a test suite.

Every tracked path is hashed after overlay and before payload execution; all
hashes, HEAD and Git status are checked afterward. The copied probe/case pack and
retained inputs are also rehashed. Snapshot and all setup/log/receipt bytes remain
retained; no cleanup/deletion, owner, GPU, broad suite or generated-output run occurs.

Git uses only the checked absolute C:/Program Files/Git/cmd/git.exe with hooks,
global/system configuration, external attributes, fsmonitor and templates disabled.
Child environment is rebuilt from the minimal Windows/runtime fields; PYTHONPATH
is exactly snapshot/src and PONTIUS_GIT is absolute. No ambient Python/Git settings
are inherited. The payload is launched with -B -P and no optimization.

Before repository imports, the probe asserts the exact CPython patch/runtime path,
safe-path/no-bytecode/no-user-site flags, snapshot cwd, PYTHONPATH, absolute Git,
its own hash, case-pack hash, generator hash and expected pontius package origin.
The first JSON log record identifies the actual runtime.

The 311 slot is first. The 314 slot additionally requires --floor-receipt PATH and
--floor-sha256 SHA. The pinned floor receipt must bind the same overlay path/hash,
pack, probe and control; identify actual3.11.15; contain four observed cases and
valid oracles; and have intact infrastructure/preservation. A genuine semantic
failure with a completed exit1 is allowed for cross-slot comparison. An incomplete
or oracle-failed floor run does not permit 314.

The infrastructure watchdog is600 seconds, followed by bounded termination/kill
cleanup. It is only a hang guard. Expiry is infrastructure failure, never a
scientific timing result, accepted budget, or semantic RED. Interrupted/incomplete
runs keep setup/log/snapshot; absence of a valid receipt cannot pass a gate.

## Intended sequence after root inspection, not executed here

1. Baseline311: use a fresh label and explicit retained source
   T/engineer-generator-v19.py, SHA-256
   3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1.
2. Inspect retained baseline311 receipt and semantic/oracle classifications.
3. Baseline314: same source path/hash plus the baseline311 receipt path/hash.
4. After root reviews the integrated port and retains exact v20 bytes, repeat311
   then314 with its explicitly supplied source pin and fresh labels.
5. Compare complete public records, harmless traces and failure classifications.
   This family supplements public24/design53/matrix192/212 and the existing
   coordinatorjoin8/weakwrite3/lexical6/A19/B18-required-plus-one-excluded scope.

The control has no source-edit, test-edit, owner, broad-suite, install, commit or
push mode. It validates a single finite probe only. Any malformed input, changed
pin, extra path, incomplete identity, invalid oracle or inconsistent receipt is a
typed RuntimeError or an explicit infrastructure failure; no silent pass.

At plan issuance no control, analyzer, oracle or test payload has run. Static
authoring checks are source parsing, hashes, LF/BOM/width checks and fixed-data
inspection only. Root's review remains required before the first invocation.
