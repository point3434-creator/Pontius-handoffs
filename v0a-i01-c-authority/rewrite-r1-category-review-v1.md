# R1 category and public-path review

Reviewer: codex / cold_review_a, engineering participant. Read-only discovery and
coverage review for the fixed Gate A path; not a cold pass, implementation
approval, or architecture reassessment. No inspected source, test, Model or probe
was executed. No candidate or test changes and no new cases.

## Inputs and fixed population

The generator was read directly as a Git blob using the validated absolute Git
executable in owner context, with no safe.directory/configuration change:

- r010 commit: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358
- tools/generate_test_inventory.py: 1070711 bytes
- Generator SHA-256: 29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692
- rewrite-early-population-v1.json SHA-256: 3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce
- tests-checks/storage-composition-cases-v1.json SHA-256: faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709
- tests-checks/name-environment-cases-v1.json SHA-256: d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c
- rewrite-scope-clarification-v1.md SHA-256: 2e699aaf3b520539eca38233b1a758cbdefcdf67fea86aaa54a7699f926ea8c1

Gate A remains six public analyses and eight independent Model projections:
two required-clean, three required-refuse, one permitted-refusal. Source and
Model strings were inspected as data only. The population manifest pins each
source, Model, expected-data record, envelope and source path. The first four
cases use tests/test_storage_composition.py; the hidden-cell pair uses
tests/test_structural_review.py. Each envelope has its own one-item stable-ID
universe, canonical inventory, fixed baseline identifiers and no child probe.
Do not substitute the larger original DesignReviewTests envelope.

| Case | Required outcome and independent trace | Categories exercised |
| --- | --- | --- |
| shared-list-consumed | Explicit blocker; relay, store, callback, write, then TypeError; sink unreachable. | Two parameters alias one list; append callable with captured default; extract through other alias; invoke; current class member mutation; failed final call. |
| shared-list-dormant | Zero blockers, exact argv [-m,fixed]; relay, store, sink. Callback/write unreachable. | Same retained alias/default dependency without callback execution; lawful dormant storage; ordinary helper return and subsequent sink. |
| class-adoption-unsafe | Explicit blocker; change, read, write, then TypeError; sink unreachable. | Outer cell starts None; class-body helper sets it to ReviewTests; current closure read after class completion; class-local module must not leak outward. |
| class-adoption-safe | Zero blockers, exact argv [-m,outer]; change, read, sink; write unreachable. | Opposite cell transition to None; class-local module=inner cannot replace outer module; reached readonly helper cannot be blanket refused. |
| hidden-cell-joined-reached | Explicit blocker. False projection: set:none, body, sink -> fixed. True: set:review, body, write -> TypeError. | Returned reader/setter pair, shared activation cell, nonlocal write, unknown branch, possible reached mutation. |
| hidden-cell-joined-dormant | Explicit refusal OR zero blockers with exact argv [-m,fixed]. Both projections: selected set event, sink -> fixed; body/write unreachable. | Same returned references and branch effects with reader dormant. Optional effective-result precision remains optional. |

The last pair does not require precise tuple-return/join interpretation: an
explicit refusal can satisfy both existing classifications. Do not relabel it,
and do not claim that passing Gate A proves that precision. The two strict clean
controls prevent a blanket refusal strategy across the admitted path.

## Whole public path: required seam disposition

All anchors below are in the pinned r010 source. The concrete R1 plan should name
the replacement operation or pure reuse for every row, rather than replacing
only _SourceOrderedResolver while retaining a second live engine.

| Seam | Required R1 disposition |
| --- | --- |
| derive_design_review 26165 -> _process_review_rows 25677 | Preserve public source/inventory/item selection, receipt/schema and final outputs. Route the entire selected analysis through the canonical core, with no fixture-ID/source-shape dispatch to a second engine. |
| Module entry 25739-25776; _definition_time_protocol_resolver 25023; _definition_time_blockers 25095 | Construction/default/decorator expressions are semantic work. Replace their old resolver execution. Discovery may retain immutable syntax facts, but cannot execute dormant bodies to produce live helper summaries. Keep import-time/refusal policy and originating stage budget. |
| _review_function_registry 22851 | Separate immutable definition/scope/descriptor syntax and module relationships from live binding/current-member claims. Its per-source certificate budgets at 22860 are part of the complete accounting inventory. A registry spelling or old stability projection cannot override current canonical state. |
| _unittest_entry_preflight 25491 and receiver analysis 25461, called at 25936 | Keep entry/signature/descriptor admission. Its old receiver analysis executes the resolver at 25472-25487 and must not survive as an unnoticed legacy path. Preserve the independently created preflight budget at 25943. |
| _review_body 24106; helper-return work 24294; review-flow entry 24315 | Replace live FlowValue entry transport, helper effects and call execution; no dict projection at 24142 as a semantic bridge. _source_ordered_helper_return 22501 and _source_ordered_review_flow 22544 currently execute bodies and cannot be called for live results by the new path. |
| _ReviewFlow 12338; _snapshot_call 15747; helper effects 17577/17750; recursive review around 24629 and 24764 | One selected callable/receiver, ordered argument/default references and call-entry state. Nested helper calls return tagged value/effects/state/issues through that interface. Do not reexecute for reporting or round-trip live objects through literal AST/aliases. |
| _bind_helper_arguments 23210 | Reuse exact signature-matching rules only. Descriptor/bound selection comes from the canonical callable. Parameters/defaults transport references, including two parameters pointing to the same list; no spelling-based rebinding or new object per parameter. |
| _merge_states 20656; expression successors 15953; statements 20927/20977 | Preserve state/result/exception pairing and effects before failure. Strong writes to one proved cell; alternative writes retain all possibilities. Missing/unbound is explicit. Helper/class completion must not overwrite a current outer cell with an earlier snapshot. |
| _process_definition 23584 and invocation 24832 | This is NOT a pure whole-function renderer. It resolves argv/env/cwd from AST mappings; its -c branch 23723-23746 reenters the old resolver. For Gate A, canonical sink observations may feed the unchanged admitted -m policy/row shape; unsupported paths explicitly refuse. No live state may flow into old AST reconstruction. |
| Row normalization 25177, sorting 25977-26007, receipt/census 26174-26264 | Reuse finalized scalar/JSON-like evidence operations. Preserve multiplicity, capability IDs, blocker ownership, analyzed-site/helper-edge attribution, deny_all and digests. Row absence alone is never the required unsafe blocker. |

The exact local-recursive entry line is an anchor for the old bridge, not a
requirement to preserve its API. _runtime_call_bounds at 8372 and independent
sensitive-site classification are not permission to re-derive live callable
identity. Preserve their bounded policy/census obligations using canonical
outcomes; classify any reused algorithm explicitly. Original census disposition
checks at 24975-25008 require a row, blocker or proved unreachable outcome.

## Smallest permitted reuse and implementation guidance

Safe reuse candidates with closed immutable inputs: _canonical_lf 366,
_semantic_bytes 378, _review_blocker 7821, _capability_id 7835,
_normalise_review_rows 25177, source-location/definition metadata, exact signature
matching, checked cardinality and final receipt/approval code. Static lexical
scope at 9798 and exception metadata at 9986 can supply facts, not a parallel
current environment. The pure final process-definition dictionary at 23881-23901
shows the existing output fields to preserve.

Gate A's subprocess policy is active Python worker, argv -m plus fixed/outer,
cwd target, environment delta SAFE=1 with no removals, timeout 5000000000 ns,
completed return category, and no descendant permission. These fields must be
derived from the selected sink observation and unchanged policy, not hardcoded
for the case IDs. Canonical state must evaluate module/default and keyword values
in order; env recognition is a bounded supported policy, not an OS call.

Prioritize one end-to-end route: module/class construction -> method entry ->
local helper/default/cell/list operations -> outcome -> immutable sink observation
-> existing row/receipt shell. Keep class namespace separate while sharing the
proper enclosing cell identities. For the shared-list pair, storage preserves
callable references but does not execute them. For class-adoption, the setter
effect survives class completion and module=inner stays class-local.

Record every original budget owner/stage, including module protocol, registry
certificates, preflight, main review, helper preparation, binding and emission
work. Actual allocations, lookups, copies and reference edges remain charged.
Gate A uses the original caps; its reports must not silently apply Gate B's
196608 continuation criterion or restrict accounting to enabled helper work.

## Coverage limits without changing the population

R1 needs normal/return outcomes, possible lookup/call failure and the existing
unknown branch. Gate A has no explicit try/except/finally, comprehension,
generator consumption/depth, cross-file helper, multiple factory-activation
collision, complex decorator or child-program case. Its deferred coverage is
callable creation/storage versus invocation, not a completed generator model.
The separate frozen comprehension scope clarification remains binding when that
syntax is migrated; Gate A does not demonstrate it.

Likewise, the hidden-cell pair's legal refusal is not evidence that class scopes,
joined cells or escaped closures are fully supported. Preserve these limitations
in the R1 plan and later result. Do not add cases here or strengthen the existing
allowed outcomes to compensate.

## Existing retained evidence, with source identity

Read-only receipt summaries and pinned raw-log hashes were checked; no payload
was rerun. These references are under tests-checks and use frozen v19 source
3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1.

- storage-composition-storage-composition-v19-01-311-receipt.json:
  210890c5e24e2eb227a99fba0c5a859c131c53d77fa4cf41e6069d56275e001f
- storage-composition-storage-composition-v19-01-314-receipt.json:
  c094edd7cc9cebf3c684644f03a590e4ba22393f58ba9cbfbff51351ec6b849d

Both have four completed Models/analyses, intact infrastructure, and two semantic
failures: class-adoption-unsafe wrongly clean with [-m,outer], and the matched
safe case wrongly refused. Both shared-list controls pass. These are the existing
class-pair RED references, not evidence that all Gate A cases fail on r010.

- red-name-env-v19-311-311-receipt.json:
  7e72792ac56de1ca4d3db7f544803f08bcf0ed3e636e538beadd35350c22802a
- red-name-env-v19-314-314-receipt.json:
  1976c3156a0c38edb47e696cd344638903141a8265d6cf197ec80895b1de0e0b

Those exit1 results are structural repeated-work RED across the old 24-case
family, not semantic failures of the hidden-cell pair. Both hidden-cell cases
had explicit blockers and met their classifications; the dormant result used
permitted refusal. Do not use those exits as new r010 semantic RED.

The later original-composition-ten-v23-diag01 receipts record both-slot semantic
success for the four storage cases among ten existing cases. Their receipt
hashes are 57b0e9a5478f4f7f7c94ff46cc28f45ab0ca7b38b474149e124da3bdf900e5cd
and e74caa55ac367b5442ed34bb0e52b7a56ead23cfeaafeda24f5a202b8e90e63f.
This does not transfer acceptance to the new r010-based rewrite.

The root-owned Gate A controller must establish its exact frozen-r010 baseline
and later candidate evidence under its reviewed custody rules. This note does
not fabricate a six-case r010 result from older-source receipts. The mapping
engineer owns the concrete R1 plan/source; the cost engineer owns the controller;
root retains dispatch authority.
