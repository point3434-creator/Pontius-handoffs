# R2 checkpoint 2 source and accounting engineering review

Verdict: STRAINED, with one Important source finding (R2-E1). The bounded outcome transport and new-work accounting otherwise reconcile. This is an engineering review, not cold acceptance or runtime evidence. No candidate, analyzer, test, Model, or harness was imported or executed; no production source was changed.

Controlling pair: H beff8193e9d5ce7316f5006fccc77ffcb5ca5695; rewrite-r2-checkpoint2-source-v1-manifest.sha256 SHA-256 ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b; source rewrite-r2-checkpoint2-source-v1.py SHA-256 7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d. Predecessor: checkpoint1 source 41b4de563da886a7c674d49b25acd4332ba208906b403ec244d1a4aea856ee05. Exact checkpoint diff: fec89fbb58d6dc5cf09f7276c10d7b43ee75499aaeaee847e7c78d400f23cb45.

The author category ledger 01f5f188b17ce08a924e24eb5957eaa9bf09894d4349c6b37450e0d4557415b9 and report ee4888d7c91d6d6a9735f5fbeb71ec7226bbfc93cada0dd5286771bd18018753 were read after deriving the independent source inventory. They are frozen at H 87e35c7d244265004f46835a9e7a7f14062589f6, explanation manifest SHA-256 5eea3e691cb9aac5f894eb246256e9fb53e7d3312a2d954c1a67f7fd447f73ec; that manifest was independently read from Git and rehashed. Their explicit source-pair association is retained in the report. Authorizing scope is rewrite-r2-source-checkpoint2-disposition-v1.md 5c0e09c4bdda13848f78827ef139a0776859ec4eaf59fd3da76a003fed340b5b; the R2 plan/addendum remain controlling.

## Important R2-E1: module builtin-context replacement is admitted but ignored by exception proof

Source-confirmed; behavioral public-path reproduction is pending and remains coordinator-owned. No executed mismatch is claimed here.

The sole _CExceptionType producer at9961-9965 treats absence of a module member named ValueError/TypeError/KeyError/IndexError as sufficient evidence of the genuine builtin class. That is insufficient when the module has replaced its __builtins__ context:

- Name assignment reaches _c_store_name:10051-10064 and _c_namespace_write:9799-9814. Module-scope writes have no reserved-builtin-context guard. The refusal at10061 applies to declared module writes from a nonmodule frame.
- Literal None is admitted at10272-10274; empty and exact-string dictionaries are admitted by _c_eval_dict:10199-10264. Therefore module __builtins__ replacements using None, an empty dictionary, or a string-valued dictionary survive this source-admission category.
- A dictionary containing a helper value is NOT an admitted witness:10240-10243 requires exact-string dictionary values. Do not use that example to claim this path was demonstrated.
- Entry preflight11415-11450 checks the selected class namespace. _c_entry_namespace_supported:11330-11342 does not inspect module __builtins__. No __builtins__ guard exists elsewhere in the frozen candidate.
- _CFunction:9148-9153 and helper entry10939-10965 retain no builtin-context provenance. _c_read_name can consequently issue genuine-builtin proof despite the function having a different builtin context.

CPython3.11.15 selects builtins when creating a function and stores that reference in func_builtins; removing or replacing the module entry afterward does not by itself replace the captured reference. This creation-time dependency was independently checked in [CPython function creation](https://raw.githubusercontent.com/python/cpython/v3.11.15/Objects/funcobject.c). Thus a guard that inspects only the current module map at later lookup would not establish the missing historical proof.

Impact: a new canonical exception constructor/handler can be selected without the required runtime builtin identity. This can change execution and handler selection and undermine fail-closed analysis. The coordinator independently identified and confirmed the same source category. Keep this checkpoint held for the bounded public reproduction and disposition; no fix, new builtin interpreter, or broader precision proposal is issued by this review.

## Transport and value-consumer inspection

- The sole outcome constructor is _c_out:9916, with ten fields. _c_follow:9936-9939 and _c_call:10863-10867 forward control, tag, reference, origin, explicit flag, and exclusions without resetting raised metadata. _c_match_known_handlers:10500-10505 restores the original active facts after a normal handler-type evaluation while retaining its resulting state/issues/trace.
- _c_handle_known_exception:10455-10462 starts the matched body from the raised successor's exact state. It creates a normal outcome with the retained issues/trace, clearing consumed active metadata. New abrupt handler results flow directly to output rather than sibling matching.
- The existing normal-only conversions in store completion, Return, class installation, and helper completion remain guarded. _c_eval_many, _c_statements, _c_join, COW tables, snapshots/forks and cell/object writes are unchanged. Abrupt helper outcomes pass through intact; no budget or context is retained in the new exception records.
- _CExceptionType has one producer. Its key normalization admits it explicitly; constructor and matcher consumers require exact type. Other existing value operations either safely carry the value or conservatively refuse/produce unknown identity; no new atom-only attribute assumption was found. Canonical key equality is not used as runtime identity proof.
- _CException has one allocation site at10881; _CExceptionOrigin has one at10427. Instance creation is normal and receives a fresh existing canonical object ID. Explicit Raise is the only _c_raise_known caller. The raised path creates no _CIssue.
- Nine-field completed tuples at10849-10852 retain the first four historical meanings, followed by tag/reference/origin/explicit/exclusions. The same observation remains immutable across outcome branches. No canonical .completed reader or terminal-history exception scan exists.
- _c_exception_matches visits every flat member needed to establish a matchable tuple; it does not return early after a prior match. Invalid/unproved/nested members return unsupported before any handler executes. Known exact tags are the four approved distinct classes, with no hierarchy expansion.
- _c_review_outcomes:11079-11092 exports only active escaping raises, using their immutable origin. Missing required active metadata raises InventoryError. Historical call events remain call/edge evidence and do not resurrect consumed exceptions. Existing per-outcome trace traversal and unrelated issue debt remain.
- All six legacy exception-keyword producer calls remain present at9972,10020,10134,10140,10909,10925. Their call ASTs are unchanged; central _c_fail:9924-9928 now always emits refused control plus unsupported issue debt, with no active tag/reference/origin. None is promoted into catchability.

## Accounting reconciliation

No additional material accounting gap was found in the bounded delta. Charges below are semantic allocations/references/visits, not CPU timing or allocator benchmarks.

| Boundary | Reconciled charge, before called-helper work |
| --- | --- |
| _CExceptionType creation/key | 2 for object+field; key4 for tag read+tuple+two references |
| Empty _CException | 4 for record+two references+tag read; existing ID/store/COW work remains |
| _c_out | 11 for object+ten fields; one more only when creating the default exclusion set |
| _c_follow | Four newly forwarded metadata reads; existing issue concatenation/trace link and widened _c_out additional |
| Each call completion summary | 18 = visit1 + nine-field tuple10 + append/reference2 + five newly retained metadata reads5; snapshot/final tuple separately charged |
| Each reconstructed call outcome | Previous2 + four added metadata reads =6; widened outcome allocation separate |
| _c_raise_known | Admission1; current record read if applicable; origin object/two fields+tag read4; no fabricated issue work |
| Handler dispatch/matching | Single proof dispatch1+tag/comparison2; tuple adds current read/kind check and2 visit/proof+2 tag/comparison per proved reached member |
| Routing and handler results | Charged lists, visits, form/type checks, five active-field reads, appends/references, pending extension2N, and original joins/evaluation/body work |
| Try/Raise/unary minus | Actual list/iteration/append work retained; exact numeric negation charged only on its admitted path |
| Terminal active exception | Control read1; three metadata reads;20 for new reason/origin reads plus existing blocker/key export work |

The nine-field summary accounting agrees with the author ledger. New metadata also increases normal-path costs. Original _AnalysisBudget construction and consume behavior, all fixed caps, ownership and whole-table/bank copying remain unchanged. No reserve/headroom claim is supported without the separately reviewed full-population run.

## Evidence and limits

All seven manifest entries were independently rehashed, and the manifest content was read from the exact frozen Git commit. A stdlib AST/hash-only inspection independently verified all20 edit pairs forward and inverse, byte-exact to the predecessor/source. The required SequenceMatcher(autojunk=False) count is242 additions+21 deletions=263; cumulative from R1 is314+46=360. Sixteen existing top-level nodes changed and eight were added; remaining named top-level ASTs are unchanged. All four _CContext construction ASTs and all13 _AnalysisBudget construction ASTs are unchanged; the budget class AST is unchanged.

The source census independently enumerated unique new record producers, six legacy tagged calls, every explicit _c_out control/metadata rebuild, class-proof mentions and absent completed-summary reads. The author ledger/report reconcile with these observations except that their builtin-fallback proof claim is qualified by R2-E1. No semantic fixture was created or executed; no runtime success, cold CLEAN verdict, or full call-graph acceptance is claimed.
