# Policy direct-context refusal correction plan

2026-08-30, Codex. Separate Tier-C FIX after r002's independent reports; do not
alter frozen r002 or blend this with value admission. Both independent reviews
have reproduced ordinarily constructed LegalBettingDecision values containing
unbounded nested exact tuples in nominally shallow scalar/enum fields. The generic
copy walks the malformed shape before comparing it, and RecursionError escapes.
Identity substitution is closed; this narrower refusal mechanism needs correction.

Chosen design: derive the trusted legal decision from the already-owned exact
betting state first. Compare the caller's decision against that finite authoritative
shape with exact recursive types, then use the trusted derived decision. This
rejects a tuple at a scalar/enum position immediately, with no caller hook, no
arbitrary input-depth budget and no redundant copy of the untrusted decision.
Retain typed containment for RecursionError at both remaining graph-admission
boundaries (source/context) so malformed recursive shape cannot leak from them.
Scope runtime.py and existing test_v0a_hand_replay.py only; expected <70 lines.
No lookup/table/hash/identity change, source dependency, policy input widening or C edit.

Category discovery: enumerate all fields of LegalBettingDecision and RaiseBounds
against real derived values. RED with dataclasses.replace for every scalar/enum/
tuple field containing 2,000-deep exact tuples, plus shallow wrong-kind opposing
cases and exact valid contexts; source/context generic admission exception edges
remain explicit. Expected outcome InvalidDecisionContextError before any selection,
with valid action preserved. No monkeypatch/private construction or operational limit.
Floor-first fresh snapshot RED/GREEN, separate frozen manifest and two cold passes.
No broad/GPU/source seal/ceremonial commit authority. Existing r002 scope/history
remains visible; this correction is coordinated internally, not returned to Claude.
