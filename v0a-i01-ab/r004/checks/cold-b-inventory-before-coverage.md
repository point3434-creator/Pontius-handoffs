# Cold B independent inventory before coverage

Recorded 2026-08-30 from handoff, current CLAUDE/workflow, required-outcome
disposition, frozen ADR0485/ADR0484 brief and frozen source. Coverage.md,
implementer narratives and current peer reports have not been read.

Candidate c6adbcaa048988361d2388970eaca772711b797b; base
30df7bce8da51715e6f1d7576892dd689421c516; manifest
a810c89b7342fb1bcb4f1498fdcf53cd11a589b70424c7da48f6619a45da67cb.
Three changed blobs and sorted row-file identity independently verified with
actual CPython 3.11.15 first in fresh D-local detached clone; receipt
cold-b-identity-py311.json. No tests have yet run.

Discovery: enumerated model/runtime types, ingress helpers and their consumers;
followed dispatch -> four handlers -> decision/delivery and terminal settlement;
searched replay event producers and sealed kernel settle/live_seats consumers.
No trace/publication/C or independent policy-authority audit is opened.

| Contract | Surface and invariant | Independent executable observations planned |
| --- | --- | --- |
| V-01 | Four exact outer event types; schema/id/index; start seats/stacks/blinds/private cards; opponent street/seat/HandAction; reveal street/card tuple; showdown six immutable rank entries | Skipped-post-init subclasses of each variant with wrong schema, bool/float/index or mutable values; exact outer opponent with skipped nested HandAction; compare pre/post public state and mailbox; no action/completion effect; typed invalid_event; safe nullable identifiers |
| V-01 state | Common hand/index order; current actor/street; next reveal/overlap; showdown live seats exactly non-null; all live ranks one comparable domain before advancing to completion | Legally reach each boundary; invalid showdown missing-live/folded-nonnull/mixed-int-tuple, empty or mutable vector; rejection leaves state/conservation/deliveries unchanged; valid int and tuple controls settle to an independent equal-contribution payout calculation |
| V-01 timing | Admission inside outer start_transition_boundary; cause retained before boundary cleanup | Deterministic clock samples around rejection; preserve invalid_event then genuine cleanup clock failure order; no validation metadata callbacks on unadmitted objects |
| V-02 | ActionEnvelope -> admit_envelope -> prebuilt DeliveryReceipt -> duplicate check -> mailbox insertion | Malformed outer/nested values including bool/float index aliases, seats/streets; every rejected envelope leaves accepted empty; subsequent valid same logical key accepted exactly once; returned exact receipt; duplicate refusal without replacement |
| V-03 | Real mailbox deliver -> admit_receipt -> exact matching hand/action -> acknowledgement count | Forward genuine envelope into real ActionMailbox then return malformed subclass/bool/float/wrong-id/wrong-exact-index receipts; expect unknown delivery_ambiguous, one physical acceptance and no retry, no fabricated known count; valid exact receipt opposing control |
| Preservation | Sealed kernels/spine unchanged, internally owned policy graph and typed selection untouched; known accepted delivery and prior settlements still pass | Exact changed-path scope; focused frozen test_v0a_hand_replay.py; direct state chip sum and settlement payout controls; actual 3.11 then 3.14 module origins |

Closed graph surface in model: HandStartedEvent, OpponentActionEvent,
StreetRevealedEvent, ShowdownResultEvent, HandAction, ActionEnvelope,
DeliveryReceipt plus exact int/str/tuple and None. Reconstruction rejects
subclasses before inspecting their fields; graph values then use fixed class
constructors. FailureRecord consumes admitted event_index only, and hand_id
from owned runtime state. Runtime rank-domain/live-mask checks precede strength
retention and completion. Envelope receipt construction precedes insertion.

Limits: finite adversarial schedules, not arbitrary Python object forging,
private state mutation, class monkeypatching, or unbounded hostile-memory proof.
No broad suites, GPU, installs, lifecycle invocation, source edits or release
claim. The complete ordinary producer/consumer paths remain the evidence target.
