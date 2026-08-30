# Coordinator verification: v0a-i01-value-boundaries/r001

Reviewer: Codex /root, 2026-08-30. Additional pass, not a cold-review claim.
Verdict: NOT CLEAN. Two Important boundary contracts fail direct verification.

Candidate: 47d08d8c1556d776358e15811e3e98b859fd6a8b
Ref: refs/heads/review/v0a-i01-value-boundaries/r001
Manifest SHA-256:
cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 35a6667ca3785e750324b3c93103a8994a6d7d6a

This is a separate additional-contract audit of r003 bytes, not another verdict
on the earlier scope-frozen slice-1 fix round. No source, test or configuration
was edited. The user-reported seed finding was treated as a hypothesis; no
unavailable future implementation or seed-audit snapshot is being certified.

## C-01 - Important: nominal event membership does not establish validated input

Confidence: high. Real HandRuntime dispatch, unchanged kernels and mailbox.
Frozen locations: model.py:141-161, :179-201, :213-220;
runtime.py:380-400, :453-495, :497-525 and :915-946.

Ordinary subclasses override only __post_init__ with pass. Their inherited
constructors initialize normal dataclass fields while skipping the validators.
No object.__new__, object.__setattr__, private-state mutation, patched
production method or custom equality is used.

The runtime admits event subclasses by isinstance and does not repeat the
complete event validation before changing state or deciding. Each following
invalid value is rejected by the base constructor, but accepted by the
subclass constructor:

| Input | Real observed result |
| --- | --- |
| Hand-start schema not-the-event-schema | Real call emitted; status decided, no failure |
| Hand-start event_index=99 | Real call emitted; decision records index 99 |
| Hand-start event_index=False | Real call emitted, then an escaping TypeError |

For the boolean-index case, the real mailbox holds one accepted action and
runtime accepted_delivery_count is one, but dispatch returns no typed outcome:
DecisionRecord's later exact-integer validation raises after delivery.
This is validation occurring after an observable action, not just an object
that can be represented incorrectly.

The nested boundary also fails with an exact OpponentActionEvent. Its action
field accepts a HandAction subclass through isinstance. A subclass with
kind="teleport", raise_to=6 is constructed normally and passed inside that
exact event. The inherited to_betting_action falls through to a legal raise,
which the real spine commits. A separate kind="fold", raise_to=7 probe is
accepted and committed as fold while dropping the forbidden amount.

These inputs violate ADR-0485's literal event schema, zero initial index,
exact integer fields and closed action vocabulary. The unchanged kernel
correctly validates the legal betting action it receives; the adapter has
already changed malformed input into that action.

Required outcome: complete event and nested-action admission before any
transition or delivery, with a typed invalid_event result on invalid input.
Failure reporting must use only validated identifiers or allowed nulls, so
formatting a refusal cannot raise another validation exception.

Engineering direction: define one explicit admission boundary for the closed
event union and its nested values. Exact concrete-type checks plus declared
field invariants, or reconstruction into exact validated immutable values,
are viable options. An outer event type check alone is insufficient because
the nested-action probe uses an exact event. Preserve ADR-0485's outer-clock
start before validation; validation remains charged work inside the wall.

Verify the complete invalid-input equivalence class, including schema/index
constraints and nested action variants, with assertions for no state change,
no mailbox acceptance and an exact typed refusal. Keep real valid events and
legal action controls alongside each rejection.

## C-02 - Important: mailbox acceptance and acknowledgement trust skipped validation

Confidence: high. Real ActionMailbox storage and real HandRuntime delivery.
Frozen locations: model.py:281-319 and runtime.py:883-913.

Two sides of the value-only mailbox contract fail:

1. ActionMailbox.deliver accepts an ActionEnvelope subclass with seat=True or
   an invalid street and returns a real DeliveryReceipt. An empty hand ID is
   worse: the invalid envelope is inserted into accepted before constructing
   the receipt raises TypeError. The public accepted mapping retains the
   malformed envelope after that exception.
2. A mailbox subclass calls the real super().deliver first, then returns a
   DeliveryReceipt subclass overriding only __post_init__. action_index=True
   and action_index=1.0 are both accepted as the first integer action's valid
   acknowledgement. HandRuntime returns decided with no failure and one
   counted acceptance. The real delivery occurred; this probe does not rely
   on a mailbox lying about whether publication happened.

Both malformed receipt fields are rejected by DeliveryReceipt itself.
The runtime tests isinstance and value equality, so True == 1 and 1.0 == 1
pass without establishing the required exact integer identity.

Opposing controls matter: a valid-valued receipt subclass succeeds, and a
well-formed receipt with the wrong integer index returns delivery_ambiguous,
retains the real mailbox acceptance, and does not claim a known matching
acknowledgement. These controls isolate missing validation from matching logic
and from a dishonest delivery implementation.

Required outcome: validate the full envelope and nested action before mutation
of accepted state; establish a valid exact receipt identity before treating it
as known acceptance. Invalid acknowledgement after a delivery attempt remains
ambiguous and must not cause a retry.

Engineering direction: perform pure envelope validation and construct the
receipt before the mailbox's acceptance commit point. Centralize exact value
admission rather than using isinstance as a proxy for successful construction.
At the runtime acknowledgement boundary, require validated fields as well as
matching values. Keep the existing at-most-once and ambiguity semantics.

Verify invalid-envelope rejection with accepted still empty; test receipt
bool/float values against the real delivery path, plus wrong-key and valid-key
controls. Do not change the sealed game/spine code to repair these adapter
admission defects.

## Coverage, evidence and limits

checks/coordinator-probe.py contains 13 schedules: three opposing controls and
ten malformed-value cases. Each malformed case first proves that the normal
base constructor rejects the same fields, then uses an ordinary subclass at
the production boundary. Raw observations are byte-identical across actual
CPython 3.11.15 and 3.14.6 after their identity records are excluded.

Execution: checks/coordinator-run.py ran 3.11 first and then 3.14 in the fresh
disposable coordinator snapshot recorded in checks/snapshots.json. Payloads
used -B -P, snapshot cwd and src PYTHONPATH, a scrubbed environment and absolute
Git. Exact executable, CPython implementation and full version were recorded
and asserted before payload imports. CuPy and Torch remained absent.

Existing test_v0a_hand_replay.py (35) and test_v0a_contract_faults.py (22) pass
on both interpreters: 57 per slot. These are supporting regressions, not
evidence that the new negative scenarios pass. Diagnostic zero exits indicate
completed observations. No broad suite, GPU, experiment or performance
measurement was run.

The static census covers 20 frozen v0a classes in model/runtime/replay, four
V1/V2 spine output classes, and four blueprint-reference classes. Thirteen
model classes define __post_init__; the seven runtime/host/fixture classes do
not. V2 ticket/emission classes also have no __post_init__. Lack of a validator
is not classified as this skip mechanism, and invalid constructibility alone
is not a material finding.

The six model reporting/settlement record classes are inventoried but their
external serialization/parser admission is deferred to the existing trace
lane. Fixture trust and alternate oracle design are not reopened. Blueprint
authority belongs to its already isolated correction contract.

The coordinator source snapshot stayed Git-clean before and after all checks.
Its HEAD is the bound candidate, and the ten manifest files match frozen
blobs. Sealed dependencies were read only. This is an ordinary correctness
audit, not a release verdict, acceptance of a next submission, or permission
to rewrite a slice.
