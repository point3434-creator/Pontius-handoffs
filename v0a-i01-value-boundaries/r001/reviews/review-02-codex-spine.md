# Cold review 02 — Codex spine and value admission

Verdict: NOT CLEAN. Specification: FAIL for event/action admission and mailbox
envelope/receipt admission. Engineering: FAIL for the same reachable trust-boundary
mechanism. No material finding established for ControlledDecisionTicketV2 or
EmittedBettingActionV2 themselves.

Reviewer: Codex independent spine pass, 2026-08-30.
Round: v0a-i01-value-boundaries/r001, NEW-SURFACE audit, Tier C.
Candidate: 47d08d8c1556d776358e15811e3e98b859fd6a8b.
Manifest: cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a.
Base: b357d333fc2393b7fc7dcf31f30c86616208c817.
Snapshot: D:/pontius-snapshots/v0a-values-spine-621bb1725663439baa809b694e3a2f07/harness.

Authority: packet handoff; frozen ADR-0485 and v0a-increment-1 brief; committed
workflow at d1ed3cb; current CLAUDE.md permanent Python 3.11 tooling. No other
reviewer's report or implementer narrative was consulted. This report does not
amend the prior implementation-slice verdict and does not classify these new
findings as residuals.

## Findings

### S-01 — Important / High: runtime admits malformed event graphs and can change settlement after completion

Confidence: high; reproduced identically on CPython 3.11.15 and 3.14.6.

Locations: src/pontius/v0a/runtime.py:380, 465, 515, 596, 604, 626;
src/pontius/v0a/model.py:141, 149, 213. The initial isinstance check admits ordinary
subclasses; handlers do not rerun complete event validation, nested HandAction is
also admitted by isinstance, and the showdown handler retains event.strengths.

The concrete mechanism is ordinary inherited dataclass construction with an
overridden, empty __post_init__. Every input uses a normal constructor; there is
no object.__new__, object.__setattr__, state tampering, or production monkeypatch.

Direct observations, with the corresponding exact base constructor rejecting
the same fields:

- HandStartedEvent subclasses carrying schema_version="wrong-schema" or
  event_index=7 return accepted and initialize the real betting state.
- An OpponentActionEvent subclass with event_index=True is admitted for event 1
  and folds seat 3 in the real kernel.
- An exact OpponentActionEvent containing a HandAction subclass with kind="dance",
  raise_to=4 is accepted. HandAction.to_betting_action treats the unknown kind as
  a raise; real history contains RAISE to 4. Checking only the outer event's exact
  type would leave this example open.
- A StreetRevealedEvent subclass with a wrong schema advances the real runtime
  to flop and emits the controlled action.
- A malformed opponent action containing a string escapes dispatch as raw
  AttributeError, rather than a typed invalid_event outcome.
- At a genuine two-live-seat showdown reached using public events and real
  controlled decisions, a ShowdownResultEvent subclass containing the list
  [None, 1, 2, None, None, None] is accepted and hand_complete becomes true.
  settle() pays (0, 0, 4, 0, 0, 0). Mutating that caller-owned list's seat-1 rank to
  3 changes the next settle() payout to (0, 4, 0, 0, 0, 0), without another event
  or mutation of runtime fields. An empty strengths tuple is also accepted as
  complete and only fails later in settle().

This is a supported public HandRuntime.dispatch/settle path, not a claim about
invalid values merely being representable. The list mutation is ordinary
mutation of the original supplied list and specifically proves the immutable
admission invariant was not established. No complete-deal oracle is needed to
establish that one accepted terminal input must not change afterward; no
poker-strength claim is made.

Violated requirements: ADR-0485 exact event schema and field types, only named
actions, immutable values, six-entry showdown strengths, malformed-event typed
refusal, and no invalid event making a controlled decision. The independent host
oracle is not a substitute for these runtime admission requirements.

Required behavior: validate the full event graph before accepting or changing
betting/card/settlement state; malformed input must return typed invalid_event,
emit no action for that input, and never supply mutable retained state. Refusal
construction must also tolerate malformed identity metadata without throwing a
second validation exception.

Verification criterion: run these cases through real dispatch and settle,
including an exact outer event with an invalid nested action, all four event
variants, bool/int aliases, wrong schema/index, empty and mutable strength
containers, and malformed metadata during rejection. Assert no acceptance,
delivery, state transition, or mutable alias survives refusal.

### S-02 — Important / Medium: real mailbox stores invalid envelope identity before rejecting its receipt

Confidence: high; reproduced on both interpreters.

Location: src/pontius/v0a/model.py:311-319.

ActionMailbox.deliver checks isinstance(envelope, ActionEnvelope), then inserts it
into _accepted, then constructs the validating DeliveryReceipt. A normal
ActionEnvelope subclass with an empty __post_init__ and action_index=True is
therefore inserted under ("alias", True). The base DeliveryReceipt constructor
then raises TypeError. The public accepted property nevertheless shows the
stored envelope, and the next valid envelope for ("alias", 1) raises
MailboxRejectionError because True and 1 alias as dictionary keys.

A separate direct call with seat=99 returns a normal receipt and stores the
invalid envelope. The exact ActionEnvelope constructor rejects each bad value.

The consumer is the real exported ActionMailbox public method, with its real
accepted map and real receipt construction. This is not a fabricated mailbox
lying about delivery. It is also not an assertion that v0a currently accepts an
external ActionEnvelope through HandRuntime: runtime constructs its own concrete
envelope. The confirmed reach is the public mailbox admission API.

Violated invariant: delivery accepts a validated immutable envelope at most once
under a canonical exact identity. Failed admission must not consume an identity
or conceal an already-performed insertion behind a constructor exception.

Required behavior: reject invalid envelope graphs before modifying mailbox
state; validation failure must leave accepted unchanged and must not prevent a
later valid envelope for the same canonical identity. Preserve existing
at-most-once behavior for valid envelopes.

Verification criterion: call the real mailbox with invalid identity and invalid
nested/action/seat fields; inspect accepted after rejection; then deliver a valid
envelope and verify one success followed by duplicate refusal. Include the
True/1 alias rather than only plainly different integer identities.

### S-03 — Important / Medium: runtime accepts malformed receipt fields through equality aliases

Confidence: high; reproduced on both interpreters.

Location: src/pontius/v0a/runtime.py:915-926.

A forwarding mailbox first calls a genuine ActionMailbox.deliver(envelope), then
returns a normally constructed DeliveryReceipt subclass with empty __post_init__,
the same hand_id, and action_index=True. This is the first real controlled action,
whose valid index is 1. The runtime's isinstance and equality tests all pass;
dispatch returns decided without failure and accepted_delivery_count is 1.
The exact DeliveryReceipt constructor rejects action_index=True.

The real mailbox retains the exact delivered envelope. Consequently this probe
does not claim that a mailbox can prove a nonexistent delivery, and it does not
depend on malicious lying. It proves that an invalid receipt is admitted by the
runtime's supported mailbox callback interface despite the exact integer
identity contract. A boolean acknowledgment is treated as canonical action 1.

Required behavior: fully validate the returned receipt's value types before
identity comparison; malformed or mismatched acknowledgment must follow the
existing delivery_ambiguous path without retry. This case supplies no evidence
of action loss; the confirmed breach is false acceptance of a malformed
acknowledgment.

Verification criterion: use a forwarding adapter around the real mailbox,
return invalid bool/int-alias and malformed identity fields after genuine
acceptance, and assert typed ambiguity, no retry, and correct preservation of the
actual delivery. Keep the valid forwarding receipt control successful.

## Ticket and dependency reachability assessment

ControlledDecisionTicketV2 (legal_decision_spine_v2.py:82) and
EmittedBettingActionV2 (:88) have no __post_init__ at all. Invalid base instances
are directly representable without subclassing. It would be inaccurate to call
this a skipped validator.

The source and diagnostic checks establish:

1. HandRuntime does not accept an injected spine, ticket, or emitted-result
   parameter. _process_hand_started constructs LegalDecisionSpineV2.new_hand
   directly from event fields (runtime.py:470).
2. _decide_inner gets ticket from that concrete spine's
   open_controlled_decision (runtime.py:692); the sealed producer constructs the
   exact ticket from state.legal_decision and an actual ledger snapshot
   (legal_decision_spine_v2.py:257-270). v0a consumes ticket.decision immediately;
   it does not substitute ticket.deadline for the authoritative outer ledger.
3. v0a calls emit_controlled_action with candidate=None and validated fallback
   (runtime.py:748). The sealed method applies the action and constructs the exact
   emitted result itself (:391). Runtime uses its reason; it does not admit an
   externally supplied emitted result or selected action.
4. The standalone sealed APIs also take no ticket/result input:
   open_controlled_decision(self), and emit_controlled_action(self, *,
   candidate: BettingAction | None, fallback: BettingAction). They return these
   wrappers. Creating a malformed wrapper and reading its fields is not an
   admission path.
5. A fresh real sealed spine produced exact ControlledDecisionTicketV2,
   LegalBettingDecision, ActionClockSnapshot, and EmittedBettingActionV2 instances
   during the probe. Passing fabricated ticket/result objects to public
   HandRuntime.dispatch returned typed invalid_event.

Necessary dependency distinctions: LegalBettingDecision and RaiseBounds are
unvalidated frozen output records; ActionClockSnapshot,
PreparationWorkInterval, and CompletedStreetActionTiming are likewise produced
internally by the ledger. ActionClockIdentity, BettingAction, NoLimitBettingState,
OneSeatCardState, PreparedArtifactCredit, and PreparationUse have constructor
validators. The v0a path builds concrete state/card/action values through the
sealed factories; its ledgers and preparation bank are internally owned, and it
does not expose credit/use/ticket admission. Standalone public state/action
APIs have their own consumers, but no new material ticket admission failure was
established here. The policy-source residual is excluded, not silently counted
as a new ticket finding.

No ticket/spine rewrite or sealed validator edit is justified by this evidence.

## Frozen-value inventory and limits

| Value family | Constructor validation | Admission or production status |
| --- | --- | --- |
| Four v0a events; HandAction | __post_init__ present | Public event graph admission; S-01 proves bypass reaches real runtime |
| ActionEnvelope | __post_init__ present | Internally created by runtime; independently public mailbox input; S-02 |
| DeliveryReceipt | __post_init__ present | Produced by mailbox; externally returned through supported callback; S-03 |
| PreparationUseRecord, TimingRecord, DecisionRecord, FailureRecord, PotRecord, SettlementRecord | __post_init__ present | Runtime record/output values; inventoried, no separate trace-reader/publication audit |
| DispatchOutcome, AccountingTotals | No __post_init__ | Runtime outputs; no external runtime input of these values found |
| ScriptedAction, Fixture | No __post_init__ | Host configuration inputs; host creates concrete validated events/actions |
| OracleSettlement, HostCompletionReceipt, ReplayOutcome | No __post_init__ | Host/oracle outputs; inventoried only |
| ControlledDecisionTicketV2, EmittedBettingActionV2 | No __post_init__ | Concrete sealed outputs; no supported incoming wrapper path found |

The inventory does not certify every record/fixture constructor. Arbitrary
object forging, private-state mutation, production monkeypatching, malicious
mailbox delivery lies, trace parsing, trace publication, and deferred accounting
lanes are outside this pass. No inference about an unavailable future
implementation or seed audit is made.

## Requirement-to-evidence matrix

| Contract/risk | Observable evidence | Result |
| --- | --- | --- |
| Exact event types/schema/order/action fields | Wrong schema/start index/bool index accepted; unknown action becomes real raise | FAIL |
| Validated immutable terminal value | Mutable strengths alter public settlement after completion; empty vector accepted | FAIL |
| Malformed event typed refusal | Public dispatch raises AttributeError for skipped nested action validation | FAIL |
| Envelope admission and identity preservation | Real mailbox stores invalid bool key before receipt exception; valid index 1 then collides | FAIL |
| Exact receipt acknowledgment | Real delivery followed by bool receipt returns decided | FAIL |
| Claimed V2 __post_init__-skip injection | No validator exists; concrete producers and no incoming ticket/result API; fabricated wrappers refused by dispatch | No material finding |
| Frozen candidate and execution identity | Git blob-derived manifest recomputed; preimport executable/version assertions; imports in assigned snapshot | PASS for performed diagnostics |

Existing tests were inspected rather than treated as proof: the malformed-value
cases in test_v0a_hand_replay.py:241 construct exact base classes; its mailbox
test at :315 exercises a valid envelope and duplicate. Those controls miss
ordinary-subclass admission. Existing wrong-receipt coverage uses plainly
different identities, not bool/int aliases after real forwarding delivery.
No broad or existing full suite was executed in this pass.

## Concrete engineering guidance and bounded rewrite assessment

The shared cause is reliance on a virtual constructor hook to establish
invariants later assumed by isinstance-based consumers. A frozen dataclass
prevents ordinary field assignment; it does not establish exact fields or deep
immutability for every accepted subclass. Equality also does not establish
integer identity: True == 1.

Advisory implementation choices, separate from the required behaviors above:

- Put module-owned, nonvirtual admission validation at each actual boundary.
  Either define a closed set of exact v0a value types and verify nested members,
  or validate fields and construct canonical exact immutable values. Do not
  coerce booleans to integers or silently reinterpret malformed action kinds.
  Calling event.__post_init__ dynamically would repeat the bypass.
- Keep ingress validation inside the outer transition timing interval while
  running it before card/betting/settlement mutation. Map invalid metadata to
  safe typed failure fields so refusal itself cannot raise.
- For mailbox delivery, perform full validation and construct the canonical
  receipt before the dictionary insertion, then commit one validated identity.
  This closes the demonstrated partial-acceptance failure; it is not a claim of
  a new cross-thread synchronization requirement.
- Validate receipt fields before comparing identity; retain the existing
  ambiguous-delivery/no-retry distinction after callback execution.
- Maintain a boundary matrix whose negative controls are passed to the real
  dispatch/mailbox APIs, including exact outer values with subclassed nested
  values. Pair each rejection with state, delivery, and alias-preservation
  assertions rather than only checking constructor exceptions.

A bounded refactor of v0a event/action/envelope/receipt admission is warranted:
it can centralize one exact/deep-validation policy and one refusal path across
the three contracts. Merely changing the outer event isinstance test leaves
the exact-event/invalid-nested-action example; merely validating the receipt
after insertion leaves S-02. A full runtime replacement or sealed-spine rewrite
would add transition and timing risk without addressing an identified need.
Preserve the sealed APIs, blueprint-only behavior, public event ordering,
ready-to-emit timing boundary, canonical delivery identity, and no-retry rule.
Any future authorized correction needs its own frozen candidate and these
baseline RED probes followed by public-boundary GREEN evidence on both
interpreters. This guidance grants no implementation authority.

## Execution receipts

The created diagnostic script performs normal subclass construction, real
runtime/kernel transitions, public settle calls, and real mailbox operations.
Its assertions deliberately verify reproduced failures; exit 0 means the
diagnostic observations were confirmed, not that the product is clean.

- checks/spine-boundary-probe.py
  SHA-256 e5e5865e7b765a32cad2909e9ac65e0bff067169a27988b6be4c4dc41572f5f9.
- checks/spine-run.ps1
  SHA-256 34b1cfbd6010b383636c2faf6b14bec54a879ee2563c4dc8349519f8eedb6989.
- checks/spine-py311-boundary-receipt.txt
  SHA-256 f494126bd51a7f489974fd62639f35ab419a2f9bbee5a5e498c7d686728ed84e.
  First run, exit 0, 12 recorded observations.
  D:/Pontius-tools/py311/Scripts/python.exe:
  3.11.15 (main, Jul 23 2026, 14:42:43) [MSC v.1944 64 bit (AMD64)].
- checks/spine-py314-boundary-receipt.txt
  SHA-256 ea50c90ddf55e48d40cbfc483baeeb2fcda8f9719448f1618d31a3b061d62cd9.
  Second run, exit 0, identical 12 observations.
  D:/Pontius/.venv/Scripts/python.exe:
  3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)].

Each receipt records the exact command, script hashes, environment key list,
absolute executable, CPython implementation/full version, resolved module paths,
candidate/manifest identity, probe output, and exit. Both use -B -P, snapshot cwd,
exact snapshot/src PYTHONPATH, a cleared/whitelisted environment, and absolute
C:/Program Files/Git/cmd/git.exe. Executable/version/flags are asserted before
production imports. The Git-derived manifest matches the packet bytes; snapshot
status is asserted clean before and after execution.

Only create-only checks/report artifacts were written. No source, test, config,
sealed dependency, retained evidence, lifecycle, installation, GPU, broad-suite,
commit, push, or implementation action was performed.