# R2-E1 transition input verifier — independent static review v1

Reviewer: `codex/transition_verifier_review`  
Date: 2026-08-31  
Verdict: **CLEAN** — no Critical, Important, or Moderate finding survives review.

## Reviewed verifier

- Path: `D:\Pontius\codex-verify-r2-e1-transition-inputs-v5.py`
- SHA-256: `5d202545cd08b7af880114ec775c6fba77d00a12ccc775a2ab04d3a6700400d6`

The review binds only to those exact verifier bytes. Any changed byte is a new review input.

## Bound v5 inputs

| Artifact | SHA-256 |
| --- | --- |
| `rewrite-r2-e1-transition-cases-v5.json` | `946457a644ab777e3c0a66e84c5f942740cec027d03500582ff31b300c16d427` |
| `rewrite-r2-e1-transition-spec-v5.md` | `0851471493a93845668cb39d9e6a5d4584688d505a86a87cd7a63df69162243a` |
| `rewrite-r2-e1-transition-source-model-map-v5.json` | `0b0dddca5b661ef2622ec79554c7005bffeb60a24561cb44324796081ab7b241` |
| `rewrite-r2-e1-transition-source-differences-v5.diff` | `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a` |
| `rewrite-r2-e1-transition-handoff-v5.md` | `9a8aadb05251a0ceb84e9fa1d833be4ab7b1350d86183022a20654fc2545cfd9` |

## Scope and result

This was a read-only static review of the verifier and the pinned v5 inputs. It checked:

- the non-assert, `sys`-only pre-import guard for exact CPython 3.11.15, the absolute floor executable, `-I -S -B`, safe path, ignored environment, disabled user/site imports, bytecode suppression, and `optimize == 0`;
- exact v1-v5 artifact pins, v5 schemas and names, predecessor claims, and the v4-to-v5 correction-only comparisons;
- the public envelope, adopted input, source and design identities, map row identities, phase table, case order, classifications, traces, captures, exceptions, and required argv;
- complete direct AST structure for every sensitive source and harmless Model, including imports, function and class headers, builtin-context setup and mutation, `_FUNCTION_TYPE` construction, events, captures, `ValueError` consumers, launch placement, environment routes, returns, and T03 statement order;
- the four refusal-route requirements, the T03 null route requirement, and the composite category-closure contract; and
- create-exclusive output through `open("xb")` only after all evidence predicates have passed.

The exact v5 pack, public envelope, Model contract, requirements, cases, routes, and category contract are preserved from v4 except for the declared v5 lineage metadata. The v5 lineage accurately records both v4 metadata changes: the T01/T02 route-closure requirements and the narrowed CPython 3.14.6 import-source citation.

## Review history

An earlier v5 verifier draft retained a stale spec predicate requiring the literal substring `v3.11.15`. The pinned v5 spec instead inherits the four exact interpreter citations through the pinned v4 predecessor and explicitly says that those citations are unchanged. That stale predicate would have failed deterministically before output, despite otherwise correct inputs.

Disposition: **accepted and corrected**. The stale substring requirement was removed and replaced with an exact check for the v5 provenance statement `four exact release citations are unchanged from v4`. The pack and map still bind the full exact CPython 3.11.15 and 3.14.6 source URLs. The corrected verifier was reviewed again at SHA-256 `5d202545cd08b7af880114ec775c6fba77d00a12ccc775a2ab04d3a6700400d6`; no finding remains.

Earlier unexecuted drafts also received fail-closed and coverage corrections before this verdict: optimizer bypass was blocked, non-built-in imports were moved behind the isolation guard, the exact floor and predecessor chain were pinned, v4's incomplete lineage claim was superseded by v5, and source/Model checks were expanded from selected examples to the complete relevant AST category. None of those superseded drafts is approved by this memo.

## Non-execution statement

I did not execute the verifier, any harmless Model, any sensitive source, the held candidate, the analyzer, a harness, or a controller. I did not import any of them. I did not edit the verifier or any governed input. The prospective verifier output `D:\Pontius\coordinator-r2-e1-transition-input-verification-v1.json` was absent at the final static check. This memo is the only file created by this review action.

## Limits

This CLEAN verdict establishes static verifier correctness for the exact bytes and pins above. It does not provide runtime evidence, observe function identities, phases, traces, exceptions, or public results, establish that future route hooks were reached, close the four refusal categories, authorize a source repair, or authorize payload execution. Those remain obligations of the separately reviewed harness and future authorized round. The coordinator must still freeze the review handoff under the repository protocol; this memo does not substitute mutable working files for a frozen Git snapshot and manifest.
