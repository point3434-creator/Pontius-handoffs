# Proposed completion r003 raw-frame correction

Status: concrete scope returned to the controller at the two-round boundary.
Base: 430ad75de79cec13d66ff3dc4981dd3770a371b7. Tier C FIX.
Codex drafts/finalizes; independent cold reviewers inspect the frozen packet.

Outcome: every retained stream rejected by the relevant frozen host framing/JSON
contract is excluded before chip or agreement credit. Valid streams preserve
their current classifications and exact settled chips.

Scope: src/pontius/eval_agreement.py and tests/test_eval_protocol.py; registration
only if a separate bounded test suite is needed. No host/session/codec/kernel,
solver, export, timing, ownership, runtime-policy or retained-experiment edits.
Stay inside the existing 3,000 whole-slice production-line ceiling.

1. Independently enumerate the host physical-frame and JSON admission predicates
   and classifier consumers. Pin their frozen blobs and write the discovered
   category/limits before editing. Compare positive acceptance languages, not
   merely assertions on decoded values. Distinguish public APIs from private
   implementation details; no sealed-source extraction without separate scope.
2. Turn the retained four-case diagnostic into a deterministic regression against
   the frozen base. Extend to related byte-size boundaries, LF/CR/BOM, Unicode
   separators, depth and numeric limits, duplicate keys and invalid decoding.
   Keep actual v1/v2 controls and actual premium divergence; do not replace a
   failing control with a constructed success. Retain exact RED bytes/receipts.
3. Add a bounded raw-frame admission step before parsed-object validation.
   Never normalize a host-invalid physical separator into an admissible frame.
   Parser refusal must produce an excluded outcome with a cause. Preserve the
   accepted reason-label exception at the later agreement layer.
4. Run focused byte-boundary regressions and all affected suites in a new
   source-verified Python 3.14.6 snapshot. Verify raw Git hygiene and line counts.
5. Freeze r003 with its own ref/manifest and deferred coverage. Supply no author
   reasoning or verdicts to reviewers before their independent inventories.
   Require two cold CLEAN passes and explicitly challenge raw input acceptance.
6. Only after review closure run the broad gate. Present the exact byte-identical
   adoption proposal for controller authorization, then commit/push if authorized.

Stop and return on another material residual or if matching the host admission
contract requires changing a sealed producer. No implicit fourth round, retained
solve/export/agreement, or bypass of per-commit authorization is part of this plan.
