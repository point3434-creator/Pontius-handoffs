# R2-E1 transition inputs — coordinator disposition v1

Date: 2026-08-31  
Coordinator: codex/root

## Verdict

**ACCEPTED FOR HARNESS AUTHORING ONLY.** The five-case builtin-authority transition input family is internally consistent, independently reviewed, and statically verified on the exact CPython 3.11.15 floor. No Critical or Important input finding remains.

This disposition does not authorize a source repair, import or execution of the held candidate, sensitive-source execution, or a harness/controller run. The complete input and review chain must first be committed as one frozen H snapshot with a manifest SHA-256. A changed byte is a new round.

## Controlling inputs

- Pack `rewrite-r2-e1-transition-cases-v5.json`: `946457a644ab777e3c0a66e84c5f942740cec027d03500582ff31b300c16d427`
- Spec `rewrite-r2-e1-transition-spec-v5.md`: `0851471493a93845668cb39d9e6a5d4584688d505a86a87cd7a63df69162243a`
- Static source/Model map: `0b0dddca5b661ef2622ec79554c7005bffeb60a24561cb44324796081ab7b241`
- Source differences: `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a`
- V5 handoff: `9a8aadb05251a0ceb84e9fa1d833be4ab7b1350d86183022a20654fc2545cfd9`
- Governing repair design v3: `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`
- Held candidate source: `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`

V1-v4 remain immutable predecessors. V5 changes only lineage metadata and correctly records both v4 changes: T01/T02 route-closure requirements and the CPython 3.14.6 import citation narrowing from `L2941-L2951` to `L2942-L2951`. Every governed source, harmless Model, expected result, classification, phase, trace, argv, route requirement, and category contract is unchanged from v4.

## Independent review

- V5 input cold review: `rewrite-r2-e1-transition-input-v5-cold-review-v1.md`, SHA-256 `c97f6bef3e56766cd503a8e2bf7d20c4857051550ae1cf19e124e8a3ed234c07`, verdict CLEAN.
- Static verifier review: `rewrite-r2-e1-transition-input-verifier-review-v1.md`, SHA-256 `8b2e4d23e16a512a7bfe030633d410afee3482ee8abde5c504c34c992aa3c016`, verdict CLEAN for verifier SHA-256 `5d202545cd08b7af880114ec775c6fba77d00a12ccc775a2ab04d3a6700400d6`.
- Harness design metadata successor: `rewrite-r2-e1-transition-harness-design-review-v3.md`, SHA-256 `71911094b0eadc7001fbd23c277b9827f62241fa915061f6c8dae87e85093710`. It binds the v5 pins and makes no executable-design change from v2.

The verifier review found one deterministic stale prose assertion in an earlier draft. It required the v5 spec to repeat a literal 3.11 version string even though v5 inherits all four exact citations through pinned v4 bytes. The predicate was replaced with the exact v5 provenance statement; the complete 3.11.15 and 3.14.6 URLs remain checked in the pack and map. The corrected verifier received a fresh CLEAN review before execution.

## One static verification run

Command:

```text
D:\Pontius-tools\py311\Scripts\python.exe -I -S -B D:\Pontius\codex-verify-r2-e1-transition-inputs-v5.py
```

Result: exit 0. Output `coordinator-r2-e1-transition-input-verification-v1.json` SHA-256 `b1325bed39591a20c815ec88b04a3c214173d53ab01fe01c37aa10ce6ae4262c`.

The receipt records exact CPython 3.11.15, the expected absolute executable, isolated/ignored-environment/no-site/no-user-site/safe-path/bytecode-disabled/optimization-zero flags, all five current pins, every v1-v4 predecessor pin, exact public envelope, five ordered cases and phases, four refusal-route contracts, and byte preservation across v1-v5. The verifier parsed sensitive source and harmless Model strings as AST only. It did not import the candidate or execute any source, Model, analyzer, harness, or controller.

| Requirement or risk | Evidence | Result |
| --- | --- | --- |
| No masked transition category | T01/T02 explicit transition routes, C01/I01 implicit consumers, T03 exact clean route | Pass for input design |
| No lineage substitution | Exact v1-v5 pins and v4-to-v5 correction-only comparisons | Pass |
| No executable payload during input review | Verifier preflight, AST-only receipt flags, both independent non-execution statements | Pass |
| Release-floor hygiene | Exact CPython 3.11.15 executable and isolation flags in receipt | Pass |
| Frozen reviewer handoff | Pending H commit plus generated manifest | Not yet satisfied; required before dispatch |
| Runtime behavior and category closure | Future reviewed seven-record harness, floor RED/GREEN, and exact repaired-source hook proof | Not attempted by this disposition |

## Next authorized step after freeze

Author the new `rewrite-r2-e1-transition-probe-v1.py` / `rewrite-r2-e1-transition-control-v1.py` owner pair against the frozen v5 snapshot and the v3 harness-design memo. Reuse the reviewed E1 v2 custody shell. Review and freeze that pair separately before issuing one exact Python 3.11.15 RED dispatch. Python 3.14 remains prohibited until a complete floor GREEN exists after the bounded source repair.

Runtime GREEN alone will not close T01/T02/C01/I01. Final category closure also requires reviewed exact-source hook evidence for all four refusal routes and the retained E02/E03 anti-blanket baseline.
