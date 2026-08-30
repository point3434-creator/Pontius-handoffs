# Cold A initial inventory - v0a-i01-ab/r002

Reviewer: Codex /root/ab_r002_cold_a. Date: 2026-08-30.
Candidate: 2f4287f68a83fac4225a05a91daffdb3f2977a43.
Manifest expected: 55f7ebf8827c79a6d6c70b1bf26508d87527b8c7113d2458fb4c3dfb5fed0957.
Recorded before opening coverage.md; no other review or implementer narrative read.

Independent authority invariant: only a closed immutable graph of trusted facts may
supply the policy identity, key comparison or selected action. Caller-defined hooks
must not run during runtime admission, helper admission, initial binding, lookup,
classification, trace-header identity or record identity.

Related paths independently discovered by frozen diff and blueprint call/field search:
- HandRuntime.__init__ -> _admit_blueprint -> recursive copy/constructors.
- select_blueprint_action's four-input public admission and internal owned selector.
- Source identity chain: source_id, entries tuple, entry/key/action exact records,
  key primitives and public-history atoms; canonical_bytes -> key.digest -> source.digest.
- Matching/legality chain: entry.key equality, selected action kind/amount, illegal-entry
  classification; immutable_blueprint.action_for and its dependencies remain sealed.
- Context graph: cards, betting, decision; nested history records/actions, raise bounds,
  sequences and scalar leaves; exact type comparison to independently derived legal decision.
- Hand start binding after outer boundary start; per-action selection digest comparison.
- ReplayHost header identity must come from the same admitted policy as decision records.
- Honest hit, miss, different-state miss and illegal matching entry; real mailbox delivery,
  complete-hand fixture controls, and hidden-completion invariance.

Verification matrix (planned evidence):
- Outer delegate, digest, canonical-bytes and action_for overrides -> reject before hooks
  or delivery -> existing focused tests plus independent public-boundary diagnostic.
- Nested entry/key/action/container/scalar/history substitutions -> no caller hooks,
  fail closed -> independent constructor-valid values at both public boundaries.
- Direct context subtypes and value/type mismatch -> InvalidDecisionContextError ->
  public helper diagnostic, including exact containers with invalid shapes/depth.
- Honest behavior and identical recorded/header policy binding -> real runtime/mailbox
  and ReplayHost fixture controls; no helper double as ownership proof.
- Measured initial digest and only sealed per-action full-table hash -> code-profile
  observation of real methods with deterministic clock, no production monkeypatch.
- Stored-blob manifest, scope and sealed dependencies -> absolute Git/hash receipt.
- Actual 3.11.15 then 3.14.6, -B -P, fresh D-local clone, snapshot src import resolution,
  scrubbed environment, no broad/GPU/install -> execution receipt.

Limits: this is policy-authority scope only. Event/mailbox/receipt admission, trace
schema/legal acceptance, publication/accounting and slice C are excluded. Malicious
introspection, private mutation and monkeypatching are not the threat model.
