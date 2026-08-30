# C helper binding final handoff

Status: RELEASED for root integration, with nine focused unittest methods GREEN
on actual CPython 3.11.15 then 3.14.6 from fresh disposable D-local snapshots.
This is not a cold-review verdict, combined generation result or source freeze.

This supersedes the green03 checkpoint report c-binding-report.md and its hashes.
The prior report's receiver-spelling exclusion is closed by the root's adopted
c-binding-receiver-clarification.md, recorded before the receiver-context change.
No previous receipt, snapshot, report or patch was overwritten by this handoff.

## Files and scope

Only tools/generate_test_inventory.py and tests/test_inventory_and_profiles.py
changed in D:/Pontius-worktrees/codex-v0a-i01-c-integration. All original C changes
are preserved. c-binding-final-owned-delta.patch contains this worker's exact delta
from c-binding-generator-before.py and c-binding-tests-before.py. The original
handoff included two unrun new tests; they were expanded rather than overwritten
with unrelated behavior. Five non-owned C files match their initial hashes exactly;
c-binding-final-validation.json records these hashes and the two final owned hashes.

## Implemented invariant

Descriptor identity comes from bounded registry metadata. Only a single bare
builtin staticmethod/classmethod without a module/class binding or wildcard
import is accepted. Qualified, aliased, shadowed, stacked and dynamic decorators
produce an explicit refusal. The stale module alias table is not trusted as
builtin provenance. Defaults align with the complete original signature before
removing a receiver, and allowed keywords come from surviving parameters. Binding
is calculated once; no truncating default zip or analyzer rewrite was introduced.

Receiver binding uses the caller's proven descriptor and declared receiver name,
not the spellings self/cls. Ordinary instance receiver cls and classmethod receiver
self produce the same capabilities as independent Python execution. Known context
is carried through local lexical helpers, removed when locally shadowed/reassigned,
and given to class helpers only when the actual binding consumed their receiver.
An explicitly supplied unbound receiver does not establish an instance. Unknown
receiver context remains blocked, including fixed-argv bodies.

A binding refusal remains a blocker even when inspecting a helper body derives a
literal subprocess capability. This closes the demonstrated fixed-argv hole for
invalid call signatures and unknown descriptor provenance. No capability grant or
baseline change was made.

## Verification

The runner c-binding-run.ps1 creates a fresh local clone at
52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8, overlays exactly five publication-v3 files
and seven C files, and executes only named focused methods. Per-label snapshot
JSON records all twelve hashes, root/TEMP paths, targets and scrubbed environment.
The payload asserts version, executable, -B/-P flags, src PYTHONPATH, D-local TEMP,
absolute Git, test origin and generator origin before tests execute. Sensitive
subprocess fixture source is inspected only. Independent Python execution uses a
pure return projection and never launches a fixture subprocess.

- red02: unchanged generator, actual3.11/3.14 exit1;19 assertion failures and6
  strict-default-zip errors across7 methods. Provenance negatives directly detect
  incorrect approval rather than sharing the defaults crash.
- red03: corrected cls forwarding fixture against exact saved pre-fix generator;
  both exit1,18 failures and7 errors across7 methods. Directly decorated unittest
  entries remain intentionally refused by existing preflight; that boundary was
  not expanded to make positive tests pass.
- red04: fixed-argv refusal controls before caller failure-propagation edit; both
  exit1,16 assertion failures and zero errors across7 methods.
- red05: opposing ordinary-cls/classmethod-self cases before receiver-context edit;
  both exit1,6 assertion failures and zero errors across8 methods.
- green05 FINAL: nine methods, zero failures/errors/skips on each interpreter;
  CPython3.11.15 exit0 (1.184s focused runtime), then3.14.6 exit0 (2.943s).
  Commands, identities, timestamps and output hashes are recorded in
  c-binding-green05-receipts.json; outputs are c-binding-green05-311.txt and
  c-binding-green05-314.txt; overlay identity is c-binding-green05-snapshot.json.

Five new/expanded methods cover descriptor/default matrices, opposing receiver
names, unknown/reassigned/unbound/nested receiver contexts, invalid static arguments,
and unproven descriptor provenance. Positive expected argv comes from real pure
Python descriptor invocation; invalid projections raise TypeError/AttributeError.
Negative controls include literal argv. Four existing methods cover helper registry
and argument binding, cross-file helper resolution, exception/decorator source order,
and decorator definition points. Existing nested helper closure behavior remains
GREEN. The final extra unknown-context cases extend coverage; no production code
changed after green04, and all are exercised by final green05.

Git diff --check for both owned files passes. They are LF-only and BOM-free;
all added lines are at most100 columns. Existing wider lines were left untouched.

## Limits and handoff

The provenance check deliberately refuses qualified/aliased descriptors and
conservatively treats any module/class binding as uncertain even if more detailed
source-order analysis could establish a builtin. A class-scope wildcard AST is a
refusal-only parser input, not executable Python. Arbitrary object/receiver aliases,
reflection, dynamic attribute replacement and the existing unittest entry-preflight
contract were not expanded. This is a bounded binder/registry/caller correction,
not a claim that the analyzer models all Python behavior.

No inventory generation/census, broad suite, GPU/optional dependency, install,
capability writer, source freeze, ledger, commit, push or main-file change occurred.
Root owns fresh combined generation, census and full existing inventory-suite
integration checks before C freeze and independent cold review. This worker has
released both owned files and will make no further changes without root instruction.
