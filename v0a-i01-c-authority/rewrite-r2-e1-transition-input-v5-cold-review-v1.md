# R2-E1 transition input v5 cold review v1

Reviewer: codex/transition_v5_cold_review  
Date: 2026-08-31  
Method: independent, read-only static-byte review

## Verdict

**CLEAN.** No Critical or Important finding survives. The five v5 artifacts are
internally consistent, conform to the governing repair design, and truthfully
describe v5 as a lineage-only successor to v4. No Model, sensitive source,
analyzer, harness, or production candidate was executed.

Design verdict: **SOUND.** The five cases remain the minimum nonmasked matrix in
the governing v3 design: three creation transitions, one implicit class consumer,
and one implicit import consumer. The composite closure rule prevents an earlier
safe refusal from being mistaken for proof of the intended route.

## Bound inputs

- cases: `946457a644ab777e3c0a66e84c5f942740cec027d03500582ff31b300c16d427`
- spec: `0851471493a93845668cb39d9e6a5d4584688d505a86a87cd7a63df69162243a`
- source/Model map: `0b0dddca5b661ef2622ec79554c7005bffeb60a24561cb44324796081ab7b241`
- source differences: `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a`
- handoff: `9a8aadb05251a0ceb84e9fa1d833be4ab7b1350d86183022a20654fc2545cfd9`
- governing repair design v3:
  `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`

## Static evidence

1. Every target and v4 predecessor SHA-256 recomputed exactly. The map points to
   the current v5 pack/spec/diff/design, and the cases/map predecessor objects
   point to the exact v4 pack, spec, map, diff, and handoff bytes.
2. Structured and unified comparisons show that v5 changes no case source,
   harmless Model, expectation, classification, context, schedule, phase, trace,
   argv, unreachable event, public envelope, route requirement, or category
   contract from v4. Its JSON changes are schema/name, current cross-pins, and
   predecessor-lineage metadata; its prose restates the same contract.
3. The v3-to-v4 comparison confirms the corrected lineage. V4's substantive
   metadata changes were the T01/T02 route/category-closure addition (including
   the composite closure and explicit T03 no-extra-route encoding) and narrowing
   the CPython 3.14.6 import citation from `L2941-L2951` to `L2942-L2951`.
   Remaining changed fields are the necessary version, predecessor-pin, and
   preservation bookkeeping. V5 names both substantive changes.
4. All five sensitive-source strings and all five harmless-Model strings are
   byte-identical to v1, v3, and v4 where claimed. Their ten embedded SHA-256
   values recompute. The expectations and public classifications are identical
   to v3/v4: four refusals, one clean result, with phase pairs
   `false/false`, `true/true`, `true/false`, `false/false`, and `false/false`.
5. AST parsing only under exact CPython 3.11.15 confirms all ten strings are
   syntactically valid. Source import/function/class counts, Model import and
   `_FUNCTION_TYPE` counts, and every launch-call AST digest match the map.
6. The route contract is exact and duplicated consistently between pack and map:
   T01 and T02 require the full outer/create-inner/invoke-inner/fallback route;
   C01 requires reached nested `LOAD_BUILD_CLASS`; I01 requires reached method
   `IMPORT_NAME`; T03 needs no refusal-route evidence because exact clean argv and
   no blocker demonstrate its live path. Final closure also retains runtime GREEN,
   reviewed exact-source hook proof for all four refusal routes, and original
   E02/E03 anti-blanket evidence.
7. The public envelope is byte-equivalent to the adopted identity input. Its
   canonical LF-terminated digest, inventory-document digest, stable-ID digest,
   adopted pack digest, adopted source digest, and sink-line digest all recompute.
   The held source, source manifest, retained RED manifest, RED receipt, RED
   verification, and existing E1 pack pins also recompute; both referenced
   manifests validate every row.
8. Official tagged CPython bytes confirm all four citations and message-only
   constructors. In particular, 3.14.6 `_PyEval_ImportName` starts at line 2942
   and raises `ImportError("__import__ not found")` at lines 2949-2951. The
   3.11.15 class/import and 3.14.6 class citations likewise cover the exact
   missing-builtin branches. The stated `.name is None` remains the correct
   message-only inference and a future runtime observation, as the map says.
9. All five v5 files are UTF-8 without BOM, LF-only, and LF-terminated. The
   source-difference artifact is byte-identical across v1-v5.

## Limits and custody

This verdict covers the static input successor, not implementation behavior or
runtime GREEN. At review time H HEAD was
`adcda3f01661c2344cbec1f7c2f6ec97a03fc252`, and the transition artifacts v1-v5
were untracked. That matches the v5 handoff's statement that no H commit exists,
but it means this memo binds only the exact SHA set above until the coordinator
publishes the full predecessor chain in a frozen H snapshot. No dispatch should
precede that freeze.
