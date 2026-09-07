# Independent cold source review B

Reviewer: Codex, independent agent /root/source_review_b. Issued 2026-09-06.
Task: v0a-decision-provider-implementation/r001. Tier C, NEW-SURFACE.

Specification verdict: NOT CLEAN (FAIL).
Engineering-quality verdict: NOT CLEAN (FAIL).
Severity counts: 0 Critical, 2 Important, 0 Minor. Both Important findings require correction.
Design verdict: SOUND. The fixed provider package, engine-owned clock/application, separate codec,
and existing source-admitted host/session are appropriate boundaries. The findings are bounded
missing validation relationships; neither requires a new framework or replacement of the runtime.

## Binding and independence

Candidate commit: 19227191696052837770ab68492705ffad60a87d
Base: fc99ab1a02649b82ba3bc21e5db79cb9c6e25829
Tree: faf50ff7e653ba03b1ba35d70b6fa78d38d661ca
Ref: refs/heads/review/v0a-decision-provider-implementation/r001
Manifest SHA-256: d44d7c9461edcac9c129b4b68e8dc067098621543a6c4523a8e61c9a5977d3dd

I independently read the permitted handoff and frozen requirements, reviewed all 23 changed paths
and relevant unchanged dependencies, and recomputed the complete manifest from Git blob bytes.
The 23 whole-row byte-sorted, LF-terminated rows equal the published manifest byte for byte.
The resolved ref, tree and manifest all match the identities above. The ref remained unchanged at
my final static check. I did not read the implementer's history, progress or other review reports.
The coordinator supplied only a unique reproduction name and snapshot-runner instructions.

## B-01 - Important: a valid fallback digest does not bind the reported fallback action/reason

Location: tools/v0a_table_host.py:795-822, particularly 815-817; the WireConsumer construction
paths in the standalone host and session supply a policy hash, but not the admitted policy for
checking the claimed lookup. High confidence, reproduced through the real WireConsumer.

Requirement: source-contract.md requires fallback_action/fallback_reason to describe the real
admitted blueprint lookup, retains fallback identity separately, and requires the host to check
record identities and selection/outcome consistency. Workflow checklist 3 requires writer/reader
pairs to be checked against one authority. A legal action with an authentic policy digest is not
by itself the action selected by that policy.

Concrete scenario: obtain readiness, raise-to-4 action and successful provider decision from a real
baseline event-adapter child for bot seat 3, button 0, six 200 stacks, blinds 1/2, private As Ah, and
the checked-in empty blueprint. The actual fallback is CALL/passive_default. Preserve all genuine
readiness, source/config/blueprint digests, proposal, selected/applied/delivered raise and state
hashes. Change only fallback_action to FOLD and fallback_reason to table_hit. Feed the frames to
the real host consumer, with its independently built table and original admitted readiness.
WireConsumer.exchange returns successfully and retains one applied raise. The false statement
that the empty table selected a fold is accepted as part of the verified decision.

Cause: provider_expected binds only fallback_blueprint_sha256. decision validates legality of the
claimed fallback but does not compare either fallback_action or fallback_reason with an admitted
blueprint lookup. The codec accepts either bounded fallback reason. The same gap applies to a
nonempty blueprint where a different legal action or the wrong hit/default label is reported.
This is a receipt-integrity defect; this reproduction does not claim the unchanged honest runtime
itself selected the wrong fallback or that the already applied action should be retracted.

Required correction: verify the fallback action and hit/default reason against the actual admitted
immutable blueprint and pre-action visible context at the host boundary, preserving fixed policy
identity through the session. Refuse either mismatch while retaining any previously received action.
Do not rerun the baseline policy as an oracle. Advisory implementation direction: retain the
already admitted blueprint as consumer context and use the existing exact lookup for this check.

Required verification: the retained genuine-child positive control must still pass; independently
corrupt action and reason, including the reproduced combined corruption, and require refusal at
the real consumer. Cover both empty/default and nonempty/hit policies and provider-selected versus
fallback-selected records, with independent expected fallback values and observed applied-action
counts. Apply the same validation to constructed failure records before/after action receipt.

## B-02 - Important: the codec accepts provider selection despite an established work cutoff

Location: src/pontius/decision_provider/codec.py:124-133. Related consumer:
tools/v0a_table_host.py:812-847. High confidence, reproduced through validate_decision.

Requirement: only a valid timely proposal may have provider_selected/provider origin. At an
established pre-emission work cutoff, select the prevalidated fallback and retain the observed
provider outcome with provider_late (or not_called/provider_skipped_cutoff). The record codec must
validate the exact schema's cross-field relationships. An eventual failed hand does not make a
contradictory selected-action receipt valid.

Concrete scenario: take the genuine premium preflop decision above, whose proposal, selected,
applied and delivered actions are raise-to-4 and whose actual blueprint fallback is CALL. Keep
provider_outcome=proposed, selection_reason=provider_selected and selection_origin=provider.
Give the record internally consistent completed timing at exactly 14,000,000,000 ns: emission and
last observation equal wall start plus that amount, compute seconds 0.0, uninstrumented seconds
14.0, work_cutoff_crossed=true, deadline_crossed=false. Set failure_reason=work_cutoff_exceeded.
validate_decision accepts the complete record. It therefore accepts a receipt saying the work
cutoff was established while still selecting the provider raise rather than the CALL fallback.

Cause: the validator enforces late/skipped implies cutoff, but omits the corresponding restriction
on provider-selected records when the pre-emission cutoff is established. Its completed-timing
failure check then accepts work_cutoff_exceeded. The failed-event host path reuses this validator
and lacks an additional selection-versus-cutoff check; this downstream observation is static,
while direct codec acceptance is the executed reproduction.

Required correction: enforce the selection/timing relationship for completed records with an
established cutoff and examine the related interrupted-record cases against actual runtime
semantics. Preserve provider outcome and the correct cutoff/deadline priority. Do not infer work
cutoff solely from total elapsed emission time: a provider selected before cutoff can legitimately
finish delivery later with work_cutoff_crossed=false under the inherited contract.

Required verification: reject the retained contradictory record through the codec and real failed
consumer exchange. Keep genuine late/skipped fallback records valid, with proposed/error/invalid
outcomes retained; keep provider-selected records valid when only delivery crosses 14 seconds.
Include exact/adjacent 14-second and 15-second controls and retain observed delivery/application.

## Coverage and evidence assessment

- Provider values/rules/selection: reviewed all five package files, exact scalar admission and owned
  nested graphs, recomputed legal context/digest shape, fixed configuration JSON, raise history,
  premium-before-playable order, call caps, visible-card evaluation, board-only river and proposal
  projection. Reviewed the 39 literal rule cases and independent digest/rank expectations. The
  unchanged card, betting, blueprint and evaluator dependencies support these contracts.
- Runtime/codec: traced the complete modified decision flow and unchanged emission/publication,
  failure, timing and receipt helpers. Existing tests cover real dispatch for all four action kinds,
  bounded provider faults, cutoff/deadline controls, identity changes, accepted/rejected/unknown
  delivery and post-delivery failure. The codec's cross-field protection remains incomplete as B-02.
- Source/adapter/host/session: reviewed all current admission sets, fixed provider edges, parent/
  child raw-byte manifest construction, readiness/version selection, action application before
  decision receipt, failure preservation, native child launch and session stack/button flow. The
  real-child positive prefix passed the reproduction. The three-deal session test uses literal
  blind-profit accounting. Record fallback binding remains incomplete as B-01.
- Registration: reviewed the boundary-checker and generator diffs, CI additions, session host-pin
  test refresh, all generated inventory/profile changes, and the supplied analyzer census. Parsed
  the complete old/new generated files independently: all 2,999 old inventory entries and 436 old
  payload records remain equal and in their old order. There are exactly 37 added test IDs and four
  added suite payloads. Existing profile capability hashes and all old payload grants are unchanged;
  current-profile membership adds only those four suite IDs. Old CI steps remain in order.

Changed paths inspected: src/pontius/decision_provider/{__init__,model,providers,selection,codec}.py;
src/pontius/v0a/runtime.py; tools/v0a_hand_adapter.py; tools/v0a_event_adapter.py;
tools/v0a_table_host.py; tools/v0a_table_session.py; tools/check_stabilization_boundaries.py;
tools/generate_test_inventory.py; tests/test_decision_provider.py;
tests/test_decision_provider_runtime.py; tests/test_decision_provider_transport.py;
tests/test_decision_provider_session.py; tests/fixtures/decision_provider/rules.json;
tests/fixtures/decision_provider/session.json; tests/test-inventory.json; tests/test-profiles.toml;
tests/test_inventory_and_profiles.py; tests/test_v0a_table_session.py; .github/workflows/ci.yml.

Independent static accounting: 872 added/removed production lines, 1,001 added new-test lines,
142 manual registration/binding lines and 4,712 fixture bytes. These are within the stated ceilings.
All changed blobs are LF-only, BOM-free and LF-terminated; added nongenerated lines obey width and
trailing-whitespace rules. Existing long lines in unchanged portions of two registration files are
inherited, not newly introduced. Compared with protected base B, 1,825 inherited blobs remain
identical; changes to old paths are exactly the 12 allowed exceptions plus the previously adopted
STATUS change. Host blob cb75727ef76ab1e2d7504eb8af8fa9aed232464f matches session/checker pins and
the refreshed mutation-test target. No old model/trace/clock/spine/kernel/evaluator or rehearsal
source/binding was changed in this candidate.

The supplied census records complete old-record preservation plus accounted new sites/blockers;
its expectation changes are mechanical and the analyzer implementation is unchanged. I did not
rerun the complete analyzer population or broad suites. Development receipts in focused-evidence
are not exact-candidate final acceptance, and I make no acceptance-GREEN claim from them.

## Fresh reproduction and retained artifacts

Coordinator-reserved run name: rb01. Runner invocation:

```powershell
& 'D:/Pontius/tmp/v0a-decision-provider-implementation-r001/run-snapshot.ps1' `
  -RunName rb01 -Slot 311 -ExactCandidate `
  -Candidate 19227191696052837770ab68492705ffad60a87d `
  -PythonArgs @('D:/Pontius/tmp/v0a-decision-provider-implementation-r001/packets/r001/reviews/review-b-repro.py')
```

Snapshot: D:/Pontius/tmp/v0a-decision-provider-implementation-r001/snapshots/rb01-311.
Actual CPython 3.11.15 identity/origin preflight passed, exit 0. Snapshot HEAD equals the candidate.
The runner used -B -P, scrubbed environment, snapshot cwd/src and absolute PONTIUS_GIT. The payload
checked the provider codec origin too. No candidate source was overlaid or edited.

Payload exit: 1 (intentional failing independent assertions after observing both invalid records
accepted). Genuine child-record exchange: accepted=true. Empty-blueprint fold/table-hit corruption:
accepted=true. Provider-selected plus completed work-cutoff corruption: accepted=true. The child
is a real event-adapter process. The host consumer is the actual implementation exercised through
its decoded-frame seam; transport scheduling at that seam is controlled, so this is not evidence
of an OS corruption rate or of complete native pipe behavior. The script retains the genuine raw
JSON prefix and concrete mutated-record output in the receipt. It does not use baseline policy
execution to generate expected fallback or timing outcomes.

Script: D:/Pontius/tmp/v0a-decision-provider-implementation-r001/packets/r001/reviews/review-b-repro.py
SHA-256: affc4246c9d54684856eff297426ed19be49546144815b3afeaf5587ba8531cb
Receipt: D:/Pontius/tmp/v0a-decision-provider-implementation-r001/run-records/rb01-311.json
SHA-256: e58008e6ce0ab4d23743e4a4e659e02dcf2fb835a45a41dc9f31859b045b66fd

No 3.14 repetition was needed to establish these deterministic 3.11 failures. No broad acceptance,
demo, random population, live play, training, source fix, cleanup, commit/push or child-agent work
was performed. Final acceptance remains gated on correction and both required CLEAN reviews.
