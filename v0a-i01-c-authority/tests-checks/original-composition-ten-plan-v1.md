# Original ten composition replay plan v1

Engineering harness authoring only. Root reviews the exact probe, controller and
static provenance before dispatch. No payload, configuration, candidate edit,
worktree edit, test edit, generated output, commit or push is authorized by this note.

## Frozen original scope

T = D:/Pontius-handoffs/v0a-i01-c-authority. All files below are in T/tests-checks.
This replay reads the original packs separately; it does not write a merged pack.

- storage-composition-cases-v1.json, SHA-256
  faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709:
  original four cases, in their original order, two clean and two refuse.
- scalar-class-composition-cases-v1.json, SHA-256
  50e88cedf77f902012237ccd88700c911fa8f3681c8dada380cca6c3142659ac:
  original six cases, in their original order, three clean and three refuse.

Total: ten cases and ten independently authored harmless projections, five clean
and five refuse. No permitted-refusal category, new source, transformed model,
changed trace, changed dead-event assertion, or weakened expected argv is added.
A refuse case must produce an explicit public blocker; losing its row is insufficient.
A clean case must have no blockers and exactly its frozen subprocess argv.

The storage oracle function is retained from storage-composition-probe-v1.py;
the scalar oracle is retained from class-composition-mechanism-probe-v1.py.
Only their function names change for dispatch. Their exact Model namespace,
builtins, event handling and exception-to-result behavior remain unchanged.
The scalar runner retains ValueError; no additional builtins are exposed.
Each model starts a fresh namespace, so mutations cannot leak between cases.
The public_review function is retained from the original storage probe, with its
one-test inventory, stable ID and derive_design_review call unchanged.
Sensitive source remains AST-only input to the public analyzer. Only the separately
pinned harmless oracle_source is compiled and executed.

## Harness and custody

New files are original-composition-ten-probe-v1.py and
original-composition-ten-control-v1.py. Deltas against the reviewed class12 v2
harness and static provenance are retained separately with their final hashes.
No route observer, budget wrapper, private state read or production monkeypatch
is needed. All five existing analyzer caps are checked before and after the ten
calls: helper64, child4, container4096, cardinality2147483647, work262144.

The controller requires actual D:/Pontius-tools/py311/Scripts/python.exe 3.11.15
with -I -S -B -P. CLI is LABEL SLOT RETAINED_SOURCE_ABSOLUTE SOURCE_SHA
--control-sha256 SHA, plus --floor-receipt ABSOLUTE --floor-sha256 SHA for314.
The candidate must be a regular non-reparse direct child of T named
engineer-generator-*.py. Root explicitly supplies its reviewed exact SHA.
There is no implicit candidate selection, future v23 hash or worktree source input.

The independent worktree watch remains:
D:/Pontius-worktrees/codex-v0a-i01-c-authority-v1/tools/generate_test_inventory.py
SHA-256 e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679.
It is checked before and after; this harness never installs into that worktree.

Every invocation creates a fresh UUID parent under D:/pontius-snapshots, a fresh
temp directory and an r010 detached clone at
29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.
The initial generator must be
29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692.
Exactly1761 tracked paths are hashed; only the generator is overlaid.
Payload files are the probe, two original packs, controller, this plan, retained
source and run metadata: seven files, yielding1768 manifest entries on311.
314 adds five raw pinned floor evidence files, yielding1773 entries.
The manifest itself is separately hashed. All tracked/payload/retained input
bytes, HEAD and exact expected Git status are checked after the child.
Root serializes invocations; outputs are create-only and snapshots are never reused.

Child runtime is actual3.11.15 first, then actual3.14.6 if root dispatches it.
Child uses -B -P, no optimization, no user site, minimal scrubbed environment,
PYTHONPATH exactly snapshot/src, fixed PYTHONHASHSEED0 and validated absolute Git.
The first JSON record is runtime/environment/manifest/source/probe identity before
the repository import. Every manifest file and Pontius resolution is checked.
The direct child has a60second watchdog and bounded10second kill/reap. Git calls
also have60second watchdogs. This is infrastructure containment, not a strict
scientific time wall or a descendant-process guarantee.

314 requires a hash-pinned, intact, completely observed actual311 receipt with
the same candidate path/hash, probe, controller, both packs, plan and watch.
Raw setup, stdout, stderr and log are rehashed and replayed; actual floor runtime,
stream shape, ten records, all ten harmless witnesses, summary, flags and exit
are checked independently of receipt assertions. The floor snapshot is rehashed.
A completed semantic RED exit1 may advance for cross-slot comparison, as in the
original composition diagnostic protocol. It is never treated as GREEN.
An incomplete run, analyzer error, failed witness, custody error or timeout cannot
authorize314. Each314 invocation still creates a separate fresh snapshot.

Every case logs frozen source/model hashes, expected/actual traces and result,
unreachable events, expected argv, all public rows/blockers, receipt digest and
semantic verdict. Result validation recomputes witnesses/verdicts/counts from the
pinned original packs and raw records. Unknown or reordered JSON records,
non-JSON stdout, wrong exact Boolean/integer types and inconsistent exits fail closed.
Analyzer exceptions remain errors; no cap refusal is reclassified as a semantic pass.

Setup/stdout/stderr/log/receipt are retained even on post-dispatch failure.
Creation of output handles is a pre-dispatch operation; an OS failure during
reservation may leave partial empty files but cannot start a payload.
A receipt is successful only when the scope completed, custody stayed intact,
all ten semantic results passed, and the child exited exact integer0.

## Review and dispatch boundary

Static checks may parse source, compare protected function ASTs, recompute hashes,
inspect fixed JSON and produce diffs. They do not import the generator or probe,
run Models, create a run configuration or snapshot, or launch a test/analyzer.
Root independently reviews exact retained outputs before the first invocation.
A future candidate outcome does not alter any pack or expectation.
