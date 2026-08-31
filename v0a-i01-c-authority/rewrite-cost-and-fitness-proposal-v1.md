# Partial C replacement: work budget and early fitness proposal v1

Design only, 2026-08-31. Root selected replacement of analysis-state/helper-authority, preserving the surrounding generator. This note proposes the cost boundary and an early continuation gate; it authorizes no source, fixture, harness or payload. Diagnostic v5 remains unexecuted. The authoritative state/API specification belongs to the parallel semantic design.

## Required behavior versus replaceable machinery

Keep current object/cell identity and alias coherence; source-point and historical snapshot stability; binding-observable order; lexical unbound/missing alternatives; captured defaults versus live cells; dormant/deferred obligations without premature execution; exception/control-flow successors; and fail-closed consumption. Keep all five analysis limits, particularly the original per-budget work cap262144, and original error contracts. Unknown authority is not an empty proof.

The projection adapter, MutableMapping/NameVersion/NameCursor APIs, radix/AVL/layer storage, no_work flag, history, order recipes and caches are replaceable implementation choices. Current first-matching-alias scans make order observable (v30:17782/17796); removing them requires equivalent alias behavior.

Prototype P counted variable-cardinality entry/reference visits/copies; C was full Meter work. The8x growth/hot and6x bulk inequalities, fixed factory counters, subclass-collision exercise and primitive APIs were candidate-specific fitness checks. Preserve their evidence, but do not rebuild an obsolete API to reproduce its counters. Exact retry category sequences and radix activation are replaceable; published-snapshot/failure correctness, actual-work accounting and absence of stale value retention are not. Any reused primitive retains its existing requirements.

## Representation and accounting strategy

Use the semantic design's typed state and explicit operations. Share stable scope/name metadata at its proved lifetime; use ordinary owned maps for changing facts and identity references for live cells/objects. This proposes no new persistent-map backend.

Remove module-sized projection reconstruction at construction/fork/join/observation boundaries. Import legacy data once at an explicit boundary, preserving every owed transfer, then keep the slice inside the new API. Propagate actual changed bindings/identities and preserve successor isolation. No refcount ownership guesses, mutable dictionaries shared as immutable, or unbounded overlays.

Charge every actual first-write COW copy, including cell/object maps. If those dominate, reassess the partition instead of discounting copies or adding a tree. Mandatory N-key ordered reads remain charged; they do not justify repeated N-value copying/transfer.

Keep all preparation, capture, transfer, forks/joins, lookups/order, deferred resume, results and failures on their original budget. Charge actual allocations, edges/records visited, references copied, dictionary attempts and retained snapshots; visited sets cost work and retain all live alternatives. Review the new category-to-operation map before results. No refunds/resets, state-dependent helper caching, hidden producer preparation or omitted terminal reads. Full totals are primary; inclusive call costs overlap phase partitions. A dictionary-attempt unit does not claim to count internal C-level comparisons.

Target shape: O(N) stable metadata preparation once per actual scope; no N-ambient-value reconstruction at unchanged forks/D=0 joins; actual changed edges/bindings at joins; O(N) ordered reads when required. Entry conversion, shadowing and adoption still owe all effectful transfer/cell writes. This is a design obligation, not a measured theorem.

## Known baseline, not a prediction

- Verified v26 generator70 epoch6 reached262144+1 before deferred consumption. It performed36 full joins of two73-name inputs, each producing73 names:2628 full-output name positions. Disjoint charges included lookup80486, full-build preparation40248 and radix bulk27454. This proves repeated preparation in that candidate, not the cause of v30's remaining failure.
- Verified v26 helper65 had54 bulk-constructor attempts and51 growing same-size parent/source shapes5..55. The v28 late entry-preservation change restored its exact-depth test. This is evidence that changing the operation boundary can matter without another backend.
- Current v30 focused-v2 result is52/53; generator70 still returns the work-cap refusal. Its new branch has not been measured. Do not infer eligibility, useful headroom or current dominating categories.
- All558 isolated radix checks passed their own frozen contracts. They did not establish analyzer fitness. Budget-consumption ratios are not runtime ratios, and previous hash-seed-absent traces are not exact cross-run counterfactuals.

## First vertical slice and stop gate

Build a continuous path through the public analyzer: source setup/preflight, binding/capture, joins, deferred consumption and public rows/blockers. Keep parser, binder, review envelope and capability schema. All surrounding work remains counted; selected operations must use the replacement, without old-authority fallback.

Proposed early population: ten existing cases, no new source bodies or expectations:
1. Original generator70 exact deferred-depth64 case, with the original _review envelope.
2. Original helper65 exact helper-depth64 case.
3. Public24: scale-n8-s4-d0-normal and scale-n64-s4-d0-normal.
4. Public24: scale-n8-s4-d2-exceptional and scale-n64-s4-d2-exceptional.
5. Public24: hidden-cell-joined-reached and hidden-cell-joined-dormant.
6. Original composition: shared-list-consumed and shared-list-dormant.

Paired N sizes challenge ambient reconstruction; reached/dormant pairs reject lost authority or premature execution. Root must bind existing case/model/controller pins and the finite population before implementation/dispatch. This is not an executable population release.

Stop BEFORE completing the remaining C migration if any of these occurs:
- Any original expected row/blocker, alias/cell/deferred outcome or exact-depth assertion differs; a work-cap refusal does not substitute for the required depth result.
- Any original budget exceeds196608 units (75% of262144), including all setup and the final depth-refusal point, or the owned child times out. This is proposed engineering reserve for continuing the rewrite, not a changed runtime admission cap. Passing at262000 does not demonstrate useful headroom.
- Operation records show an N-sized ambient value copy/normalization per unchanged fork or D=0 join. Required key-order enumeration is reported separately, not hidden; if it alone defeats the reserve, the design has not demonstrated fit.
- Any needed cost is unaccounted, an old-engine fallback supplies the selected behavior, or failure/retention semantics require relaxing a binding contract.

No post-result threshold tuning or automatic next backend. A semantic failure or missed reserve returns to design. After release-interpreter success, repeat the same gate on dev before widening. Passing permits integration work, not release acceptance. Ordinary frozen-repository generation and all existing acceptance gates remain required; schedule the first corpus checkpoint before optional generalization.

## Evidence pins

All files are under D:/Pontius-handoffs/v0a-i01-c-authority.
- v30 source:1a28fce14cfdd2ee30d9892b7d2719aba8ec152d99d1e3c915660648cf9756fd.
- Current focused receipt tests-checks/focused-v2-v30-first01-design-311-receipt.json:ae46f1f92f9f7de5e554f5cc1f51694a4bd69d6856acce12e099389319a6391d.
- coordinator-v26-depth-budget-verification-v1.json:2e729e903ed0f0c869e88aa595d62bc0da5a2f3a47d29962f901a4865a87bf30.
- coordinator-v28-design-verification-v1.json:a70eb13b0c3edb59d7944857a79d1d8c0d99aacbd715a7819c958f22e5fbf186.
- coordinator-indexed-verification-allsix01.json:3e3af131f3c4839bb26e993f7d188f0c92d129f129b3edbc392b1a04f1f7151b.
- tests-checks/name-environment-cases-v1.json:d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c.
- tests-checks/storage-composition-cases-v1.json:faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709.
- Original test blob:c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf.

