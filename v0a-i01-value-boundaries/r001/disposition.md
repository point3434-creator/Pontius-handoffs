# v0a-i01-value-boundaries/r001 disposition

Coordinator: Codex /root, 2026-08-30.
NOT CLEAN: three Important admission contracts, consolidated from two independent
cold passes and the coordinator's additional verification.

Candidate: 47d08d8c1556d776358e15811e3e98b859fd6a8b
Ref: refs/heads/review/v0a-i01-value-boundaries/r001
Manifest SHA-256: cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 35a6667ca3785e750324b3c93103a8994a6d7d6a

This NEW-SURFACE audit freezes an alias of implementation r003. It does not
amend the r003 slice-1 verdict, expand r004's R3-02-only fix scope, or count as
a residual of either round. Manifest bytes and all ten changed blobs verify.
No implementation authority or release/acceptance verdict is issued.

## Consolidated contracts

| ID | Required correction | Evidence and attribution |
| --- | --- | --- |
| V-01 | Establish the complete immutable event graph before accepting an event | Events E1, spine S-01, coordinator C-01 |
| V-02 | Validate the complete envelope before the mailbox acceptance commit | Events E2, spine S-02, coordinator C-02 envelope branch |
| V-03 | Establish exact receipt fields before declaring matching acknowledgement | Events E3, spine S-03, coordinator C-02 acknowledgement branch |

The coordinator grouped the two mailbox sides under one heading in its issued
report. This disposition separates their distinct consumers and verification
obligations; no original report is rewritten and no extra defect is invented.

V-01 is high impact. Ordinary subclasses overriding only __post_init__ bypass
construction checks and reach real public dispatch. Wrong schemas and indices
are accepted; an exact outer event with an invalid nested action becomes a
legal raise; malformed indices can allow a real action and then cause an
uncaught validation exception. Both independent reviewers also reached legal
showdown and supplied a caller-owned strength list: changing that list after
acceptance changes subsequent public settlement payouts. Empty strengths can
mark the hand complete before settlement raises.

V-02 is medium impact on the exported ActionMailbox API. The real mailbox
accepts malformed seats/streets and nested actions. A boolean action index is
inserted before the receipt constructor raises; the retained True key then
blocks the valid integer key 1. The normal runtime constructs its own envelope;
this audit does not claim that it produces these malformed outer envelopes.

V-03 is medium impact with a deliberately limited consequence. A forwarding
mailbox performs genuine delivery, then returns an ordinary skipped-validation
receipt with action_index=True or 1.0. Equality accepts either as integer 1.
The observed defect is malformed acknowledgement acceptance, not fabricated
delivery or an observed wrong payout. Wrong exact integer acknowledgements
correctly remain ambiguous; those opposing controls are retained.

## Required outcomes for a separately frozen fix

- Invalid event graphs produce typed refusal before state/action/completion
  effects. Validate nested actions and immutable strength containers as well
  as the outer event. Refusal metadata uses validated identifiers or allowed
  nulls; reporting invalid input must not itself throw.
- Invalid envelopes leave mailbox acceptance state unchanged and cannot
  occupy a key or block its subsequent valid use. Keep valid at-most-once
  delivery and duplicate refusal.
- Invalid acknowledgement follows delivery_ambiguous without retry. Preserve
  the actual attempted delivery; do not infer exact identity from equality.

GREEN must exercise real dispatch, settlement and mailbox boundaries, not just
constructors: all four event variants, exact outer objects with invalid nested
values, bool/float aliases, wrong schemas/indices, empty/mutable strengths,
safe rejection metadata, malformed envelopes followed by valid delivery, and
real forwarded delivery followed by invalid receipts. Retain valid controls.

## Engineering recommendation

Use one bounded value-admission slice across model/runtime with explicit
validation at the three actual ingresses. Prefer a closed set of exact value
types with complete nested checks, or deliberate normalization into validated
exact immutable values. Blindly reconstructing with existing isinstance-based
nested validators is insufficient. Calling value.__post_init__ dynamically
repeats the bypass.

Keep event validation inside the existing measured outer transition, before
effects. Prepare a valid envelope and receipt before the mailbox insertion
commit point. Validate receipt fields before matching them. A shared boundary
matrix should assert state, delivery, exceptions and alias preservation, so a
future fix removes this failure class instead of chasing one subclass at a time.

A bounded admission refactor is warranted. A whole runtime or sealed-spine
rewrite is not justified: it would add timing/transition risk without evidence
of a failing ticket admission contract. Preserve sealed APIs, legal semantics,
privacy, timing boundaries, blueprint-only behavior and no-retry rules.
These are engineering choices; required observable outcomes above are the gates.

## What the audit did not find

ControlledDecisionTicketV2 and EmittedBettingActionV2 have no __post_init__;
calling their situation a skipped validator is inaccurate. They are produced
by the concrete internally owned spine and immediately consumed. No supported
incoming wrapper route was found; fabricated wrappers passed to dispatch were
refused. Invalid standalone construction is not proof of an admission defect.

The census inventories 20 v0a classes, four V1/V2 spine outputs and four
blueprint-reference classes. It does not certify every constructor or consumer.
Trace parsing/publication/accounting and the separate policy-authority contract
remain outside scope. Arbitrary object forging/private mutation and a mailbox
merely lying about delivery were excluded.

## Evidence and review records

Actual CPython 3.11.15 ran first, then 3.14.6, in three fresh disposable D-local
snapshots. Commands use -B -P, snapshot cwd/src PYTHONPATH, scrubbed environment,
absolute Git, and recorded/asserted interpreter identity before payload imports.
All snapshots remained clean.

- Events cold pass: 25 final direct probes per interpreter. An earlier diagnostic
  assertion error is preserved; the corrected v2 probe and both reruns govern.
- Spine cold pass: 12 direct observations per interpreter.
- Coordinator: 13 direct schedules and 57 existing focused tests per interpreter.
- Probe overlap is intentional; these counts are not unique coverage totals.
  Diagnostic exit zero confirms observations, not product correctness.

Issued reports:
- reviews/review-01-codex-events.md — SHA-256 3eaec538a8561404441421601d762b312fde4abcfe6cc88e152c88fd1e2eaa83
- reviews/review-02-codex-spine.md — SHA-256 6d3cc0f6cb3bee5bd31f07fbabbb174e193e537fe55de6dee5f55012496462c5
- reviews/review-03-codex-coordinator.md — SHA-256 6223f4db4a8a06d8b4455f67fb9790ed7d5d382a8e65cc7b3aee9b5158f39df3

Each reviewer issues their own task-ledger line. The coordinator records this
single consolidated program disposition. Source, tests, sealed dependencies,
STATUS.md and active implementation candidates remain untouched.
