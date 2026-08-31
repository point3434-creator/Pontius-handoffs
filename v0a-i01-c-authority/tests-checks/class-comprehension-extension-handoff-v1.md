# Class/comprehension R01–R08 harness handoff v1

Author: codex/cold_review_a, engineering witness/harness author.
This is not a cold review. No controller, probe, Model or analyzer payload was
executed by the author. Root owns source review and all future dispatch.

Frozen cases/spec precede any R-case candidate payload or repair:
- class-comprehension-extension-cases-v1.json
  eb5551c054fc89da28fd2e4db433f56f7a3dbbd4cdb70509070a89fe362c74fd (21682 bytes)
- class-comprehension-extension-spec-v1.md
  ed292bcf0207aad474e8293cf055c17de6409b9d851f95a8b8225d4375848dc6 (7762 bytes)

The approved population is exactly R01–R08: 8 schedules, 8 harmless projections,
4 required-refuse, 3 required-clean, 1 permitted-refusal. Sensitive source is
AST-only input to derive_design_review. The Models were separately authored.
The spec fixes event order, exact traces/results and unreachable events.
R05–R08 consume inside the class to avoid Q05's separate class-member transport
prerequisite. Same-identity marker OR is a static invariant inventory only;
native shape poisoning remains an unexecuted related risk, not a ninth case.

Use these reviewed-successor source files, all under T/tests-checks:
- class-comprehension-extension-probe-v2.py
  231bcddb04eb5f3f93135c46bc03f1ed6275195949f4189a700d2f0eb3571426 (14525 bytes)
- class-comprehension-extension-control-v2.py
  34c16309d974e40909bc352d509308b19d2fa4fd42f06386d27430fcf07526e2 (27747 bytes)

The source basis for discovery was retained v23:
T/engineer-generator-v23-semantic.py
53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499.
The case requirements honestly declare that inspection. No R-case analyzer
output determined the frozen expectations.

## Preserved predecessors and authoring correction

Original comp6 probe/control remain byte-identical:
b0232750b89fba7939a093e81e9e4b8a183d23371f6464eaa8d3443bedf49138 /
775157055e5a9b6234307ef552536a25bb6049fd76e001e352fc954eac258eba.

Extension v1 probe/control are retained and UNEXECUTED:
b17d4ba2754ce12158fb536d17762deb9f6e5ab4e745693309d56fef460f565e /
957bc82f2f81a70b9b9023d1bef333d8f90dca3472144392ae2c8c387ad21271.
Root found a copied projections:6 literal while the controller required eight.
This would have caused infrastructure failure; it was not dispatched, was not
a product RED, and is not relabeled as passing.

V2 corrects projections to eight and adds exact-int checks for pack planned
counts and classification counts; result planned_cases/case_count/projections/
analyzed_cases, classification counts and caps; and actual generator cap types
before/after analysis. The result analyzed_cases domain is 0..8. These enforce
the existing exact-type evidence contract. No source schedule, expectation,
classification or cap changed. V1's harness static recipe was retained but
never run; v2's static recipe supersedes it and explicitly detects the v1
projection mismatch while validating v2.

## Static evidence, not a payload result

Case correspondence:
- class-comprehension-extension-static-recipe-v1.txt
  c250f482b1c23b4f811703b4421453083277b21c681a5e2709fbda1d12423942
- class-comprehension-extension-static-proof-v1.json
  222a098a4916f9b5370dd851dd928227eb750589a1f6e621e4a3f4eedda1a0e4
- class-comprehension-extension-static-v1-receipt.json
  ebf8d98ed37a9706e80e118a95e458c88ecfcca552438d3c3425915cd3972f7d

The actual-3.11.15 -I -S -B -P static recipe exited 0. All eight test-body ASTs
match their Model bodies after removing only event-append statements and
renaming Model to ReviewTests. Class left/right attributes match. Target
receiver/index names are verified Load nodes, target iteration cardinalities
are literal 1/0, nested-generator origins and two conditional expressions are
checked, and empty-list creation/optional append/full-consumption order is
checked. Traces are declarations; they have not been executed by the author.

Harness comparison:
- class-comprehension-extension-authoring-v1.json
  38818dd398ea4b8f0b84b7f819161660e7dc7f6c4e448b21b9933d0047af84a4
- class-comprehension-extension-authoring-v2.json
  e004f3e63f1016a7da16090fe61ffb5cc0c295492a8fc201fd8cf1481b39d59e
- class-comprehension-extension-harness-static-recipe-v2.txt
  4d938bee9b84f2d54d22f746db4a8ebef43209ef21a21ff58632ebc95960f1f8
- class-comprehension-extension-harness-static-proof-v2.json
  d88e6eceed3c43a99a1de55949dd01ec30b7871f76025309aae73967c0d29a15
- class-comprehension-extension-harness-static-v2-receipt.json
  7bb0efb20ad31c6edcdfeb1f842555fbd09e9a90b0a8f82ae5f38cb455cd8640

The static comparison exited 0 under actual 3.11.15 with -I -S -B -P.
It replayed the exact bounded replacement maps against pinned original bytes,
parsed and syntax-compiled source without executing it, compared unchanged
function ASTs, and checked summary constants by schema key. V2 planned_cases,
case_count and projections are integer 8; analyzed_cases is the integer counter.
Comparison domains and exact-int guard ASTs were checked separately, so a
remaining six-case count could not be hidden by an unrelated Python3.14.6
runtime literal. Public-review function AST is unchanged. Original runtime
slots, watch, Git path, base commit, caps and 60-second watchdog are unchanged.

Raw deltas, retained create-only:
- class-comprehension-extension-probe-v1-from-boundary-v1.diff
  3e64b196b6dbc9a864099120b19782c7d985d7b422d0ce5c07992809d8fb7a63
- class-comprehension-extension-control-v1-from-boundary-v1.diff
  1a016e4e185c78e1fee4c3de1b5b8069851156d539962c46d17accd761de9a5b
- class-comprehension-extension-probe-v2-from-v1.diff
  7c5dbb139b10b9382a78a1055d4150ca8a70db32ead105de28f3dd709c0b3566
- class-comprehension-extension-control-v2-from-v1.diff
  bb506566247eb4de3c875e7ab1f36ecf0d7b77d4c9ffaab0e79dcc412d74f8c7

## Root-only invocation and custody

T means D:/Pontius-handoffs/v0a-i01-c-authority. The controller itself uses
D:/Pontius-tools/py311/Scripts/python.exe with -I -S -B -P.
Its positional arguments remain:
LABEL SLOT RETAINED_SOURCE_ABSOLUTE SOURCE_SHA
with --control-sha256 34c16309d974e40909bc352d509308b19d2fa4fd42f06386d27430fcf07526e2.
SLOT is 311 or 314. A 314 invocation also requires --floor-receipt ABSOLUTE
and --floor-sha256 SHA for a completed, intact matching actual-311 run with
the same candidate/probe/control/cases/spec. A semantic RED is eligible for
diagnostic replication; oracle/analyzer/custody/incomplete failures are not.

The retained candidate path must be an explicit root-approved T source, not
implicit mutable W. W remains separately watched at v20
e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679.
The fresh disposable snapshot is rooted on r010
29c02f6fbd5eb0b7ddc9e816ef28f570b9839358 with 1761 tracked files. Only the
explicit generator overlay and pinned harness payload are introduced; no v4
test overlay is needed. Child imports use snapshot cwd, snapshot/src PYTHONPATH,
-B -P, scrubbed seed0 environment, D-local temp and validated absolute Git.
The original pre-import identity, full tree, manifest, byte pins, floor evidence
replay, direct-child watchdog, raw failure retention and post-run custody checks
are preserved. A zero process exit alone never establishes completeness or
semantic success.

Models have a fresh namespace per case. Their allowed builtins are
__build_class__, staticmethod, tuple, list and NameError. Only the final
TypeError is caught outside Model().test_static(); unexpected oracle exceptions
are retained as incomplete infrastructure evidence. Sensitive source is never
compiled/executed as an oracle. The probe has no private analyzer observer.

Root must finish its review before any dispatch. No broad/profile/GPU/owner
execution, candidate/W edits, expectation edits, ledger, commit or push is
authorized by this handoff. Issued files remain immutable.
