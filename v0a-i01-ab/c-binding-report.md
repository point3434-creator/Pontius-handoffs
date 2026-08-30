# C helper binding bounded implementation report

Status: focused GREEN on actual CPython 3.11.15 and 3.14.6. This report is not a
cold-review verdict, source freeze, combined-corpus generation or authorization.
Root retains ownership of final integrated generation, census, suites and review.

## Change and mechanism

Only tools/generate_test_inventory.py and tests/test_inventory_and_profiles.py
were edited in D:/Pontius-worktrees/codex-v0a-i01-c-integration. Existing C changes
in those files are preserved. c-binding-owned-delta.patch is the delta from the
two exact files handed to this worker; c-binding-*-before.py preserve that input.

The helper registry records descriptor provenance. Only bare, singly decorated,
unshadowed builtin staticmethod/classmethod are recognized. Module and class
namespace bindings are considered; wildcard imports remove trust. Qualified,
aliased, dynamic, stacked and shadowed descriptors fail closed. The existing
module import alias table is not used as descriptor provenance.

Defaults are paired with the full original positional signature before an implicit
receiver is removed. Binding is evaluated once and surviving keyword names come
from surviving parameters, protecting positional-only receivers. Static methods
retain their first ordinary parameter; ordinary class/cls calls retain an explicit
receiver, while class methods bind their receiver.

A focused fixed-argv negative exposed a second failure: argument-binding refusal
could disappear if body inspection still derived a constant capability. The caller
now retains the blocker whenever signature/descriptor binding returned None, even
if a body with literal argv produced a row. Unknown values otherwise retain the
existing body-inspection policy. No capability was granted or baseline changed.

## Contract checks

The new positive matrix executes only a pure return projection of the descriptor
fixture and compares public derive_design_review argv and timeout against real
Python descriptor invocation. The subprocess-bearing fixture is never executed.
Cases include static instance/class/cls access, ordinary required/defaulted receiver,
ordinary explicit receiver via class/cls, classmethod instance/class/cls access,
required/defaulted positional-only receivers and keyword-only default timeout.
Invalid excessive, duplicate, unknown, missing and positional-only keyword arguments
are TypeError in the pure Python projection and blocked by derivation, including
fixed-argv bodies. Eleven descriptor-provenance refusal controls are checked with
parameter-dependent and fixed argv.

The cls access fixtures use a classmethod helper called by an ordinary unittest
entry. A directly decorated unittest entry is intentionally refused by the existing
entry preflight; the initial positive fixture crossed that unrelated restriction.
The fixture was corrected without widening the preflight and rerun against the
saved pre-fix generator before validating the implementation (red03/green02).

Four existing focused checks cover registry ambiguity/argument failure, cross-file
helpers, source-order exception/decorator provenance, and decorator definition
points. Seven unittest methods total were run; subtest counts are not test IDs.

## Receipts and chronological evidence

All runners cloned fresh D-local snapshots at base
52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8, then overlaid exactly five publication-v3
files and seven C files. c-binding-<label>-snapshot.json records the twelve hashes,
snapshot and D-local TEMP, scrubbed environment, absolute PONTIUS_GIT and targets.
Every child uses -B -P; the payload asserts actual version/executable, safe-path,
bytecode disabled, src PYTHONPATH and test/generator import origins.

- red01: actual3.11 then3.14, exit1 each, 7 tests, 8 failures and17 errors. The
  generator was unchanged; the six default-binding crashes were the exact strict
  zip exception. Negative provenance fixtures initially shared that crash.
- red02: strengthened provenance fixtures use a required receiver to expose wrong
  approvals directly. Both slots exit1, 7 tests,19 failures and6 errors.
- red03: corrected cls forwarder fixtures against the exact saved pre-fix generator.
  Both slots exit1, 7 tests,18 failures and7 errors. The source and test hashes are
  recorded separately from all later bytes.
- green01: both slots exit1, 7 tests,3 failures (direct classmethod unittest entries
  refused by existing preflight); no exception. Superseded by corrected fixtures.
- green02: both slots exit0, 7 tests,zero failures/errors/skips.
- red04: fixed-argv negative controls before failure-propagation edit; both slots
  exit1, 7 tests,16 assertion failures,zero errors. These directly demonstrate an
  unsound approval for each invalid argument/provenance case with literal argv.
- green03: final bytes, both slots exit0, 7 tests,zero failures/errors/skips.
  3.11 focused duration0.940s; 3.14 duration2.291s. Full commands/exits/timestamps
  and output hashes are in c-binding-green03-receipts.json, with all output in the
  corresponding -311.txt and -314.txt files.

Git diff --check passes. Both owned files are BOM-free and LF-only. Added lines
are within100 columns; pre-existing longer lines are outside the delta.

## Explicit limits

Qualified/aliased descriptors are deliberately blocked, not analyzed by spelling.
The registry conservatively treats namespace bindings anywhere in the module/class
as uncertain, even if their order could prove a builtin at definition time. A
class-scope wildcard AST is a conservative refusal input, not executable Python.
Receiver spelling still follows the existing self/cls static model; this is not
a general proof of arbitrary receiver aliasing or dynamic attribute replacement.
No broad inventory suite, generation, census, GPU/optional dependency, install,
capability writer, source freeze, ledger, commit, push or main-file change occurred.
