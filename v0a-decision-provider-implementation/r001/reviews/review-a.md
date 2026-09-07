# Independent cold Tier C source review A

Reviewer: Codex, independent agent `/root/source_review_a`.
Issued: 2026-09-06. Task: v0a-decision-provider-implementation/r001.
Round kind: NEW-SURFACE. Review scope: all 23 manifest paths and needed dependencies.

Candidate commit: `19227191696052837770ab68492705ffad60a87d`.
Base: `fc99ab1a02649b82ba3bc21e5db79cb9c6e25829`.
Tree: `faf50ff7e653ba03b1ba35d70b6fa78d38d661ca`.
Manifest SHA-256: `d44d7c9461edcac9c129b4b68e8dc067098621543a6c4523a8e61c9a5977d3dd`.

**Overall verdict: NOT CLEAN. Specification: FAIL. Engineering quality: FAIL.**
Required findings: Critical 0, Important 2, Minor 0. One demonstrated product/consumer
contract defect and one distinct coverage finding. No production changes were made.

**Design verdict: SOUND.** The owned observation, fixed registry, engine-owned selection,
and separate codec are proportionate to the approved scope. The demonstrated defect is a
missing authority binding in the existing consumer, and can be corrected locally by giving
that consumer the already admitted immutable fallback source. It does not justify replacing
the runtime or transport stack. The absence of postflop runtime controls needs evidence
closure; it is not evidence that the baseline rule implementation should be redesigned.

## Important A1: The host accepts invented fallback provenance and selection

Locations: `tools/v0a_table_host.py:796` (`provider_expected`) and
`tools/v0a_table_host.py:812` (`decision`), particularly the fallback legality check and the
expected fields ending with `fallback_blueprint_sha256`.

Confidence: high; reproduced on actual CPython 3.11.15 against the exact candidate.

The host holds only the fallback policy digest in `WireConsumer`. It verifies that the
reported fallback action is legal in the pre-action state, but does not compare either
`fallback_action` or `fallback_reason` with the admitted blueprint's actual lookup. Legality
and a matching digest therefore let a child assert a different fallback while the host
still labels the record verified. Selection/outcome consistency checks do not repair this:
a structurally consistent provider-error record has no proposal to challenge.

Concrete input/state to wrong outcome:

1. Use the real event child, empty admitted blueprint, six 200 stacks, button 0, blinds 1/2,
   controlled seat 3, and As/Ah. The real child supplies a raise-to-4 action and a record whose
   actual fallback is CALL with `passive_default`.
2. Keep readiness identities, observation digest, resulting state, received action, delivery,
   timing, and fallback blueprint digest unchanged. Replace `fallback_action` with raise-to-4
   and `fallback_reason` with `table_hit`. The real consumer accepts the record.
3. Additionally set `proposal=null`, `provider_outcome=error`,
   `selection_reason=provider_error`, and `selection_origin=blueprint_fallback`. The real
   consumer still accepts, retains one applied raise-to-4 action, and records the verified
   rendered reason `fallback_provider_error`.

The admitted empty blueprint has no table hit and would call. The resulting accepted record
falsely states both fallback provenance and why the observed action was selected. This is
an accounting/verification defect; the test does not claim an extra action or a failure to
retain the received action.

This violates the source contract's actual-lookup fallback fields, verification of fallback
identity and selection consistency at the host, and the whole-path requirement that a
provider action must not become an invented blueprint hit. The corruption seam is explicitly
authorized finite protocol input; the production consumer, legality checks, application, and
reason extraction all remain real. It does not rerun baseline policy as a strength oracle.

Required correction: retain/access the admitted immutable fallback blueprint at the host
consumer boundary, independently obtain its lookup for the host-owned visible pre-action
context, and bind both fallback action and table-hit/default reason to that result before
accepting the decision. Preserve a received action when this later verification refuses.
Apply the same check before and after action receipt and through standalone host/session
callers. Do not weaken proposal or failure consistency checks.

Required verification: keep the real positive exchange; add deterministic negatives for a
wrong-but-legal fallback action, false table hit/default provenance, and a fully consistent
provider-error/abstention/invalid fallback record built around the wrong legal action. A
nonempty blueprint control should establish true-hit behavior. Observe rejection through
the real consumer and exactly the already received application count. Retain this rejected
candidate's RED, then run integrated GREEN on the corrected frozen candidate under the
required fresh-snapshot procedure and both supported interpreters.

## Important A2: No new-provider runtime control reaches a postflop decision

Locations: `tests/test_decision_provider_runtime.py:11` and its complete test class;
`tests/test_decision_provider.py:73`; `tests/test_decision_provider_session.py:52` and
`tests/fixtures/decision_provider/session.json`.

Confidence: high for the coverage gap. This is not a demonstrated postflop product failure.

The rule suite constructs postflop observations and calls `provider.propose` directly.
The runtime suite dispatches only `HandStartedEvent` and `OpponentActionEvent`, with every
opponent event marked preflop; it never submits a street reveal. The transport baseline
controls likewise use opening preflop actions. The three session deals intentionally end
through preflop folds (their expected provider reasons are exactly two `premium_raise`
entries). The unchanged legacy replay/trace suites cannot exercise the new strategy branch.

Consequently no checked-in control establishes the new provider's observation admission,
selection, application, delivery, and record/codec path after a real runtime street change.
The implementation plan explicitly relies on the other runtime controls to cover postflop
because the session fixture does not use its board. The brief requires situation-dependent
baseline decisions including preflop and postflop, and the source contract's runtime controls
require the real dispatch/application/delivery path with independently observed records and
mailbox. Unit-only postflop rule checks do not establish that combined requirement.

Concrete unverified scenario: the controlled seat raises preflop, opponents legally call,
and a flop reveal plus opponent checks returns action to the controlled seat. With As/Ah
and a 2c/2d/7s flop, the fixed rule must make a fresh legal minimum postflop raise despite
the previous preflop raise. A runtime integration error that skips provider work on revealed
streets, binds the wrong visible digest, or carries the prior street's raise limit would
leave all current new-provider tests green. This names a missing observable scenario, not
an allegation that the present implementation necessarily makes that mistake.

Required correction: add bounded real runtime event sequences reaching postflop provider
choices, using independent literal expected actions, chip changes, street/action identities,
and mailbox observations. Cover the stated flop/turn/river distinctions and prior-street
raise reset at the runtime boundary without replaying the policy to compute expectations.
Keep the existing three-session-deal and total explicit-deal limits. A small number of
sequential public-event controls is sufficient; no broad random population is needed.

Required verification: first establish the coverage defect against this candidate, then
run the added independent checks on it. They may pass without a production change. If a
behavioral defect is exposed, retain deterministic RED before any production correction.
Verify the added controls fail when the postflop provider integration is deliberately
incorrect at the permitted seam, while the real engine still owns action and record
classification. Follow the source contract's actual-3.11-first snapshot rules.

## Independent inventory and cross-slice assessment

- Values/rules/selection: inspected all five new production files, all 39 rule fixtures,
  proposal and observation tests, and dependent blueprint/card/betting contracts. Exact
  types, owned graph reconstruction, digest composition, fixed configuration, rule ordering,
  legal minimum raises, turn subset evaluation, and board-only river logic agree with the
  approved definitions on static inspection. The built-ins receive only the one-seat view.
- Runtime/codec: inspected the complete changed decision flow plus inherited emission,
  publication, clock, trace timing validation, and failure consumers. Provider outcome is
  distinct from selection reason; observed late error/invalid results remain fallback;
  delivery records retain local application and distinguish accepted/unknown/rejected.
  Existing tests cover controlled cutoff/deadline edges and process-control exceptions.
  The material missing integration layer is A2; the report does not certify final acceptance.
- Adapter/host/session: inspected source admission, source inventories, provider readiness,
  v1/v2 writers and consumers, action/failure reception, session forwarding/rendering, and
  all transport/session controls. A1 is a demonstrated cross-boundary omission. Source
  checks retain raw committed bytes and package population checks. Real child source/pipe
  controls are present; their development receipts are supporting inputs, not final gates.
- Registration: reviewed changes to the checker, generator, generated inventory/profiles,
  census assertions, CI, and session host-pin test. Independently parsed frozen generated
  artifacts: all 2,999 old inventory entries are exactly preserved, all 436 old payload
  records (including capability fields) are exactly preserved, and their order and every
  profile's old payload order remain unchanged. There are 37 new IDs in four suites.
  The census packet accounts for 28 new blockers, 17 new analyzed sites, 45 new helper edges,
  and one new decoy, with old-record line mapping. The published claim of identical analyzer
  outputs on both interpreters was inspected but not independently rerun in this review.

The five new files, four tests, two fixtures, and twelve allowed exceptions exhaust the
23 changed paths. Independently recomputed counts are 872 production added/removed lines,
1,001 new test lines, 142 manual registration added/removed lines, and 4,712 fixture bytes.
These fit the adopted ceilings. All candidate blobs are LF/BOM-clean; added nongenerated
lines pass width/whitespace checks and `git diff --check` returns 0. Existing overlong lines
in unchanged parts of the large analyzer tests/generator were not treated as new defects.
The session/checker host pin equals the candidate host blob
`cb75727ef76ab1e2d7504eb8af8fa9aed232464f`; the existing mutation test checks one occurrence
in session source before its replacement. Relative to source-contract base B, the only
additional differences beyond the 23 source paths are the six already adopted source-opening
documentation/status paths. Historical driver and other unspecified old source remain
outside the changed set.

## Identity and executed evidence

Read only the handoff's permitted cold inputs, frozen candidate blobs, and necessary
unchanged dependencies. No implementer transcripts/progress or another review were read.
The coordinator provided only a unique reproduction name and operational snapshot runner.
No child reviewer was spawned.

Independently enumerated changed paths with rename detection disabled and hashed raw
`git --no-replace-objects ... cat-file blob <candidate>:<path>` bytes. Whole-row byte sorting
and LF yield the manifest above, byte-identical to the packet's `manifest.sha256`. The
published ref and tree resolve to the stated candidate identities.

One bounded behavior reproduction was executed:

`run-snapshot.ps1 -RunName ra01 -Slot 311 -ExactCandidate -Candidate
19227191696052837770ab68492705ffad60a87d -PythonArgs
@('D:/Pontius/tmp/v0a-decision-provider-implementation-r001/review-a-repro-ra01.py')`

Snapshot: `D:/Pontius/tmp/v0a-decision-provider-implementation-r001/snapshots/ra01-311`.
Identity probe: actual CPython 3.11.15, exit 0, module origin in snapshot `src`.
Payload: `-B -P`, scrubbed environment, snapshot cwd, snapshot PYTHONPATH,
absolute `C:/Program Files/Git/cmd/git.exe` PONTIUS_GIT; exit 1 as intended RED.
Positive exchange accepted; both fabricated fallback exchanges incorrectly accepted.
The retained script asserts that those two exchanges must refuse. No cleanup or retry
was performed; the exact candidate snapshot remains clean after execution.

Retained script: `D:/Pontius/tmp/v0a-decision-provider-implementation-r001/review-a-repro-ra01.py`.
SHA-256: `96bf1f06b4f33f40015a3ab0af4e0dacebb113e420dbd0f8933590be1b52ada0`.
Retained receipt: `D:/Pontius/tmp/v0a-decision-provider-implementation-r001/run-records/ra01-311.json`.
SHA-256: `03a9dee12c3b5f8aa445698ca03ec1b0229a833f46e76044e0433d6930bef398`.

Pure stdlib Git-blob audit commands also verified identities, generated registrations,
counts, fixture population, pins, and whitespace. Two preliminary audit snippets had key
name/shape mistakes and were corrected without source execution or mutation; an initial
interpreter-path probe used the absent top-level python.exe before discovering Scripts.
Those tool errors are not product findings. The final identity/audit results above are
from the corrected successful commands.

No broad suite, final acceptance gate, demo, live play, training, source edit, commit, push,
cleanup, or ref retirement was performed. No 3.14 behavioral reproduction is claimed.
Final named acceptance remains downstream of both CLEAN source reviews and is not yet
established by this report.
