# r006 coordinator addendum: scope adjudication

Codex /root, 2026-08-30. Append-only correction to
reviews/review-03-codex-coordinator.md; no issued bytes changed.

Candidate: c74b80628a89938ca585ef3240b5c267a7174d0f
Manifest SHA-256: 2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f

Effective verdict: NOT CLEAN, with two Important mechanisms of R2-03,
R6-C02 and R6-C03. R6-C01 is advisory only, not a required finding.
Design remains STRAINED.

The original observations for R6-C01 are reproducible and preserved, but the
required scope judgment was too broad. OperationFailed explicitly documents
that an owned operation's typed cause has already been journalled
(runtime.py:56-57). Fabricating a marker without doing that contradicts its
documented meaning. Export supports importing/catching it; export alone does
not promise arbitrary signal construction. Neither ADR-0485 nor the callback
API establishes cross-runtime propagation of that signal as supported.
The foreign-runtime example therefore also lacks a demonstrated supported-use
precondition for a binding finding.

Following a post-verdict scope consultation with cold B, the coordinator adopts
this narrower interpretation. This consultation was not part of either cold
pass and does not modify B's issued report or ledger. The marker observations
remain useful advice to bind provenance to an owner/occurrence, but no third
fix gate is imposed from them. Same-runtime nested preparation behavior also
remains non-counted because the sealed ledger does not promise nesting.

R6-C02 remains required: ordinary body errors are accepted by the generic
exception boundary, and the adapter needlessly formats their messages while
trying to return a failure receipt. A built-in ValueError can legitimately
carry an arbitrary argument; presentation failure must not prevent the promised
host outcome. Both cold reviewers independently confirm the formatting escape.
The coordinator's classification/__class__ observations widen the tested error
inspection family and inform the same adapter guidance, not another contract.

R6-C03 remains required: one actual clock fault plus a refusal from the already
dead witness is recorded as two faults. This uses the supported real witness
and public oracle seam, requires no forged marker, and directly breaks cause
conservation. Cold B discovered it and the coordinator reproduced it on A/B
and both interpreters.

The final disposition carries the two required mechanisms, the advisory marker
weakness, and the existing change-of-implementer condition separately. The
original report's count of three Important mechanisms is superseded by this
addendum. Observation captures and hashes are unchanged.
