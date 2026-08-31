# C provenance v3 bounded worker release

Released only tools/generate_test_inventory.py and tests/test_inventory_and_profiles.py
from D:/Pontius-worktrees/codex-v0a-i01-c-provenance. No source or test changes are pending
from this worker after the hashes below. Parent owns combined generation, census, full
inventory/profile gates, cold reviews and source freeze. This is engineering evidence,
not a cold-review verdict or a claim of full-population authorization.

## Outcome and mechanism

The explicit-argument-only escape certificate is replaced by one effective-input path.
It resolves exact local definition markers or registry callable identities, reuses the
existing FlowValue argument binder, applies supplied overrides before selected defaults,
and carries captured implicit receiver values separately from legacy qnames/summaries.
Local defaults keep definition-time values; free cells/globals use invocation context.
Registered globals come from their defining module, not unrelated caller locals.

A bounded nested SourceOrderedResolver analyzes reached callee effects. The current call
is captured after argument evaluation and before body effects. Reached member mutations
invalidate later lookups; global/nonlocal name changes affect bindings rather than erasing
objects retained by aliases. Reached cross-module global changes refuse explicitly without
writing a same-spelled caller local. Actual writes before raises persist; raises before
writes stop traversal, including an exact nested registered helper exception. Invalid
argument binding has no body effects. Ordinary legacy value/exception/census paths remain
covered by the unchanged old analyzer contracts.

Captured receiver/default metadata is met independently during merges. Shared helper
identity traversal also follows captured defaults and receivers, so passing a local
callable that retains an owner to an unproved callback cannot hide that owner escape.
Unknown effective owners needed for a discovered helper-member write refuse at the reached
store; this does not globally invalidate other same-named members.

Registered namespace-sensitive generators/coroutines stay deferred at creation. Their
unsupported consumption is represented using existing deferred-state refusal machinery;
this is not general registered-generator execution support. Legacy generator routing with
no helper namespace inputs/effects stays on its existing path. Source/body scanning and
nested effect work use existing finite budgets/depth limits; no cap was raised.

## Contract and scope

Stage0 was recorded before production edits in c-provenance-worker-v3-stage0.md,
SHA256 ddaf9b3ae39582a961fa73d8f4445a6357aa2ca6de36dc78ae01d19e05ca0087, and parent adopted it.
The subsequent generator-deferral and nested-exception controls enforce that same adopted
ordering/nonexecution contract. No A/B, other C, generated inventory/census expectation,
main, baseline, capability, Git ref, ledger or cold-review-report bytes were written.
Git status lists only the two owned paths; git diff --check exited0. Existing CRLF warning
from Git is informational; the worktree source bytes were not normalized by Git.

All189 pre-v3 class methods are AST-identical. Removing the four new DesignReviewTests
methods restores the complete v2 test-module AST exactly. The v2 module was independently
pinned by SHA256 af929697b3f6c8ddad823ff16bef63936f5b924cdf16992d8bc93679368ca961.

## Category-first evidence

The four new public-derivation tests execute only pure-return/exception projections.
Sensitive subprocess bodies are inspected, never launched. One generated matrix covers
seven binding channels (positional, keyword, positional default, keyword default, closure,
global and ordinary receiver) against read/write, invoked/dormant and raise-order modes
(35 opposing projections). Additional controls cover posonly defaults, containers, saved
callable/default capture, late cells, nested invocation, invalid duplicate/posonly keyword
binding, readonly/unused defaults, harmless explicit overrides, classmethod captured
receivers, registered defaults/global captures, reached global/nonlocal rebinding,
unsupported unstable module defaults, deferred classmethod creation, exact nested raises,
cross-module global mutation and captured-default callable escape. This is not an exhaustive
Cartesian product of Python object/descriptor/generator semantics.

Fresh floor RED receipts red01/red02/red03 pin the unchanged v2 generator and show14,28,4
failing subcases respectively. Later red04 records two real name-effect failures plus two
fixture-discovery errors; red05/red06 use the corrected container-alias fixture and isolate
unknown-default, name-effect, generator and nested-raise regressions. Red07/red08 isolate
cross-module global effects and captured-default callable escape. All failed receipts
remain append-only. Probe05 caught two existing exact generator-routing failures; no old
assertion changed, and subsequent full focused runs passed.

Final commands (the driver extracts all40 explicit method names from source AST and
invokes c-provenance-run.py, which creates a fresh r008 clone plus the exact two overlays):

    D:/Pontius-tools/py311/Scripts/python.exe -B -P D:/Pontius-handoffs/v0a-i01-ab/c-provenance-worker-v2-run-all.py v3-green01 311
    D:/Pontius-tools/py311/Scripts/python.exe -B -P D:/Pontius-handoffs/v0a-i01-ab/c-provenance-worker-v2-run-all.py v3-green01 314

Actual3.11.15 FIRST:40/40,0 failures/errors/skips,11.984s,exit0.
Actual3.14.6 SAME BYTES:40/40,0 failures/errors/skips,21.217s,exit0.
Each receipt retains actual interpreter/version/origin assertions, snapshot cwd/src
PYTHONPATH, scrubbed environment, D-local TEMP and absolute Git. Full expanded commands,
all RED/probe/GREEN summaries and hashes are in c-provenance-worker-v3-final-validation.json.

## Limits and remaining parent work

No generic Python heap, reflective namespace model, arbitrary returned-object inference,
or general registered-generator consumption support was added. Dynamic/unstable registered
defaults are not re-evaluated in the caller: a default needed for an unknown helper-owner
write refuses, while unused/read-only default controls remain clean. Unproved callable
escapes and unsupported effective argument shapes refuse. Cross-module global rebinding
is refused, not modeled as a complete mutable module heap. Accepted v2 descriptor,
namespace and dynamic-lookup exclusions remain. The old full36 analyzer contracts are
included in the final40; full corpus generation, counts, cross-file edges and all affected
inventory/profile suites have not been executed by this worker and remain parent-owned.
The final focus runs do not establish a whole-corpus budget result.

## Exact bytes and artifacts

Generator SHA256: 9031a42ded45bbd8af3afb3044c683be40ed45121c375b3de04e5bdf05b8c924
Tests SHA256: 526bab49b2a57e2f9237b28707dbfd03821f1132f1fa63bf3b9c2a561b69d0eb
Owned patch vs r008: c-provenance-worker-v3-final-owned.patch
SHA256 c14421be5d5e8520512ea54b1c6ec138b8a8cbe86c6a25e9c1a2e241f44be982
Increment vs released v2: c-provenance-worker-v3-final-increment.patch
SHA256 3c082853944e53cf74ed92d221f456432ae55f6e9b9558925433ad964d442681
Preservation: c-provenance-worker-v3-final-preservation.json
Validation: c-provenance-worker-v3-final-validation.json
Final receipts: c-provenance-v3-green01-311-receipt.json and -314-receipt.json
