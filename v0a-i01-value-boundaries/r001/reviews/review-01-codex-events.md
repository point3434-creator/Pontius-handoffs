# Independent event and mailbox value-boundary review

Reviewer: Codex events cold pass, 2026-08-30.
Verdict: NOT CLEAN / specification FAIL for the scoped public value admissions.
Confidence: high for the reproduced findings below.
Engineering judgment: bounded boundary-validation refactor; no whole-runtime or V2 rewrite justified.

Candidate: `47d08d8c1556d776358e15811e3e98b859fd6a8b`.
Manifest: `cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a`.
Ref: `review/v0a-i01-value-boundaries/r001` (alias of the supplied r003 bytes).
Base: `b357d333fc2393b7fc7dcf31f30c86616208c817`.
Snapshot: `D:/pontius-snapshots/v0a-values-events-3f1e008be6d04f5c8a99d05d9d8a2ef2/harness`.

This is a NEW-SURFACE audit, not a fix-round residual assessment. It makes no
claim about an unavailable seed audit, future candidate, or the separate r003
slice-1 disposition. No other reviewer findings were read. Authority is the
packet, frozen ADR-0485 and increment-one brief, ADR-0308 where needed for the
preserved spine, committed workflow at d1ed3cb, and current CLAUDE.md's permanent
Python tooling. The mutable workflow proposal was not adopted.

## E1 — Important / high impact: event admission trusts skipped construction validation

Locations: `src/pontius/v0a/runtime.py:381`, `:453`, `:497`, `:527`, `:569`,
`:597`, `:602`, `:622`, `:823`; `src/pontius/v0a/model.py:149`, `:219`.

The runtime accepts event subclasses with `isinstance`, then validates only the
state-dependent parts of each event. It does not establish the complete value
contract before applying the event. A normal subclass overriding only
`__post_init__` therefore bypasses the original constructor's exact fields.
Checking only the outer class would still leave the nested-action route below:
an exact base `OpponentActionEvent` accepts a `HandAction` subclass with the same
skipped validation.

Reproduced on both required interpreters through real HandRuntime and ActionMailbox:

- A HandStartedEvent subclass with an invalid schema, or start index 7, produces
  `decided` and a real accepted controlled action. The corresponding base
  constructors refuse both inputs. The first-event index and schema are not
  rechecked by the hand-start handler.
- After legitimate folds by seats 3, 4 and 5, an OpponentActionEvent subclass
  with index `4.0` and seat 0 passes index equality, folds seat 0, and causes the
  controlled small blind to act. The real mailbox accepts the controlled action.
  DecisionRecord construction then raises uncaught `TypeError: event index must
  be an exact integer`. Dispatch returns no typed failure despite one actual
  delivery; `accepted_delivery_count` is 1. This violates both malformed-input
  refusal and the rule that input failures emit no action from that input.
- An exact base OpponentActionEvent carrying `SkipAction('bogus', 4)` is accepted.
  The inherited conversion's catch-all branch constructs a legal raise-to-4,
  which the actual betting history records. `SkipAction('fold', 900)` similarly
  applies a fold while discarding the forbidden amount. `SkipAction('bogus', None)`
  instead lets an AssertionError escape dispatch. No conversion override or
  monkeypatch is involved.
- A StreetRevealedEvent subclass with an invalid schema, otherwise a legal flop,
  is accepted and causes a second real controlled action.
- At legal showdown, a ShowdownResultEvent subclass carrying an empty tuple is
  accepted and sets `hand_complete` true, but `settle()` then raises because six
  strengths were not supplied. A subclass carrying the ordinary caller-owned
  list `[None, 10, 20, None, None, None]` is also accepted. `settle()` initially
  pays `(0, 0, 4, 0, 0, 0)`. Assigning `strengths[1] = 30` in that caller-owned
  list, without touching runtime/private state, changes a second public
  `settle()` result to `(0, 4, 0, 0, 0, 0)`. The handler retained the mutable
  input alias. The base constructor rejects the list.

These are public state/decision/settlement effects, not merely examples of
representable invalid dataclasses. They establish one failed event-admission
contract across all four event families and the nested action.

Required outcome: validate the complete event representation, its nested action
or strengths, and all immutable container requirements before any betting
transition, policy action, or completion marker. Malformed inputs must produce
the appropriate typed refusal, establish no new delivery, and never retain
caller-mutable values. Refusal must itself tolerate unvalidated identity fields:
`_reject` and `_from_failure` currently copy event_index into a validating
FailureRecord (`runtime.py:998`, `:1026`); merely changing `isinstance` to exact
class checks is insufficient unless malformed IDs/indices become permitted null
failure identity rather than another constructor exception.

Verification required: replay each demonstrated case through the real public
runtime, including an exact outer event with malformed nested action; assert no
state/action/completion acceptance for the rejected input and no escaped
exception. Exercise each event variant, each exact field type, and the nullable
failure identity path. For showdown, require a fixed six-entry immutable vector,
valid strength types, correct live/folded mask, and no caller mutation effect.

## E2 — Important / medium impact: mailbox commits malformed envelopes before validation

Location: `src/pontius/v0a/model.py:310` through `:319`, with nested admission
at `:286`.

ActionMailbox.deliver checks only `isinstance(envelope, ActionEnvelope)`, derives
the key and stores the supplied object, then constructs DeliveryReceipt. It
admits skipped-constructor envelope values and nested invalid actions.

Reproduced on both interpreters using ActionMailbox itself:

- Envelope subclasses with seat 99 or street `wrong` receive normal exact
  DeliveryReceipt acknowledgements and are publicly present in `accepted`.
- An exact base ActionEnvelope with nested `SkipAction('bogus', 4)` is also
  accepted and acknowledged. No envelope subclass is needed for this route.
- A skipped-constructor envelope with action_index `True` is stored first, then
  the base DeliveryReceipt constructor raises TypeError. The malformed envelope
  remains accepted. A subsequent valid envelope at action_index 1 is rejected
  as duplicate because Python's dictionary key equality aliases True and 1.

The final case is an observable admission/identity violation: validation failure
did not leave the mailbox untouched, and the malformed input occupied a valid
future action key. It does not depend on private mutation or a lying mailbox.
The runtime normally constructs an exact envelope itself, so these reproductions
establish the public ActionMailbox boundary; they do not claim the current
normal runtime independently emits these malformed outer envelopes.

Required outcome: every envelope and nested action must satisfy the frozen value
contract before accepted state changes. Invalid input must be a pre-acceptance
refusal and must not occupy any key or impede a later valid delivery. Normal
at-most-once semantics for a valid key must remain unchanged.

Verification required: invalid seat/street/action/index cases against the real
mailbox, asserting unchanged `accepted`; then deliver the corresponding valid
key exactly once and prove the second valid delivery refuses. Include bool/int
and float/int identity aliases. Receipt construction or validation must not be a
new fallible step after recording an otherwise unestablished acceptance.

## E3 — Important / medium impact, limited consequence: acknowledgement exactness is bypassable

Location: `src/pontius/v0a/runtime.py:903` through `:912`;
`src/pontius/v0a/model.py:291` through `:297`.

`_publish` admits DeliveryReceipt subclasses and compares identity fields using
ordinary equality. It does not establish the receipt's declared exact positive
integer action_index contract. A DeliveryReceipt subclass overriding only
`__post_init__` can carry `True` or `1.0`; both compare equal to action 1.

The probe uses an ActionMailbox subclass that first calls `super().deliver` and
then returns that ordinary receipt subclass. The envelope is genuinely accepted
by the real mailbox before the malformed receipt is returned. With either True
or 1.0, HandRuntime returns `decided`, reports no failure, and increments known
deliveries to 1. An exact index 2 in the same real-delivery arrangement correctly
returns `delivery_ambiguous` and does not increment the known count.

This proves malformed acknowledgement admission at the consumer, beyond invalid
constructibility. Its demonstrated consequence is the loss of required exact
receipt validation. The probe did deliver the right action: it does not prove
misdelivery, forged acceptance of an absent action, or any new payout error.

Required outcome: establish exact receipt field validity as well as matching
identity before declaring known acknowledgement. Malformed acknowledgement must
fail closed with delivery ambiguity, retain the already executed real delivery,
and never retry. A validated receipt with a wrong exact identity must remain
ambiguous; a normal matching base receipt must succeed.

Verification required: the same real mailbox subclass arrangement, with bool,
float and valid/wrong exact integer receipt fields, no absent-delivery double.

## Closed routes and inventory

| Surface / risk | Evidence and result |
| --- | --- |
| Valid hand-start and default mailbox | Real controlled action succeeds; positive control in both slots. |
| Nested raise bool or below legal minimum | Real kernel rejects as `invalid_event`; no state change or new delivery. |
| Reveal duplicate, private overlap, boolean card, list, wrong count | Real visible-card boundary returns `invalid_event`; no new delivery or betting transition. Constructor cannot check private overlap; the runtime correctly does. |
| Wrong receipt index 2 | Real delivery remains present, runtime returns `delivery_ambiguous`; this identity mismatch route is closed. |
| ControlledDecisionTicketV2 and EmittedBettingActionV2 | Real spine produces exact base outputs. Public `emit_controlled_action` accepts only candidate/fallback actions, not a ticket or deadline. Runtime obtains its ticket from its privately created real spine. No public ticket replacement route found; representability of these nonvalidating output records is not a finding. |
| Action-clock and preparation records | Inspected as necessary preserved dependencies. ADR-0308 identifies bank claim as the supported credit attachment route; the ledger attachment hook is private. No private ticket/credit injection was used or claimed. |
| model records | Inventoried PreparationUseRecord, TimingRecord, DecisionRecord, FailureRecord, PotRecord and SettlementRecord. Runtime constructs them as outputs; DecisionRecord's late exact check explains E1. Their separate trace-reader admission is outside this audit. |
| runtime records | AccountingTotals and DispatchOutcome are output records with no constructor validation. Invalid standalone construction does not establish a public admission defect in this scope. |
| replay values | Inventoried ScriptedAction, Fixture, OracleSettlement, HostCompletionReceipt and ReplayOutcome. ScriptedAction builds a base HandAction; ReplayHost builds base event values from fixtures. No generic claim of fixture validation or host-receipt security is made from this inventory. |
| ParsedTrace | Inventoried only; trace-reader, publication and accounting lanes were not reopened. |

Source searches found V2 ticket/output construction only in the sealed spine;
its emission signature and a real open/emit sequence were also executed. This
is meaningful negative evidence for the supplied mechanism, not a claim that
every possible Python object substitution or all sealed kernels were audited.

The existing EventValueContractTests test base constructors and a normal
mailbox. Those checks miss inherited-init subclass bypass and base outer values
with malformed nested subclasses. Existing acknowledgement tests cover missing,
wrong and matching receipts but do not prove exact numeric field admission.
These observations come from reading the tests, not from claiming an unexecuted
suite pass.

## Engineering guidance and size judgment

Demonstrated shared cause: nominal inheritance is being treated as proof that a
value's validation ran. Frozen dataclasses prevent ordinary field reassignment;
they neither make dynamic `self.__post_init__()` nonoverridable nor recursively
freeze caller-supplied containers. Repeating constructor checks in some later
records does not repair the earlier state transition.

Required behavior is described per finding above. The following design choices
are advisory:

1. Define one small explicit admission layer for each actual ingress: event,
   envelope, receipt. Use exact base types throughout the value graph if
   subclassing is intentionally unsupported. If subclasses remain supported,
   validate through non-overridable module-level routines and construct trusted
   base values before retaining or consuming them. Calling
   `value.__post_init__()` dynamically simply repeats the bypass.
2. Validate nested actions even when the containing event/envelope is an exact
   base instance. Validate exact tuples and their elements before retaining
   strengths. Do not silently reinterpret an unknown action as a raise.
3. Separate validation from effects: validated event before kernel transition,
   validated envelope and receipt construction before mailbox insertion,
   validated acknowledgement before accepting it as known. Preserve the
   existing no-retry and real-delivery preservation rules.
4. Build failure identity from independently validated optional fields. This
   keeps the refusal path total on malformed input instead of raising while
   trying to describe the first problem.
5. Parameterize boundary checks over ordinary post-init-skipping subclasses,
   exact outer values with bad nested subclasses, bool/int and float/int
   equality aliases, wrong schemas, malformed tuples and caller-owned lists.
   Assert public state, mailbox membership, outcome and payout invariants;
   constructor-only tests are insufficient.

Prefer this bounded admission refactor across model/runtime. A single local
`isinstance` replacement is too narrow: E1's exact outer event and E2's exact
outer envelope can still carry bad nested actions, and failure construction can
still fail. A whole-runtime replacement would also disturb preserved clocks,
legal rules, delivery ordering and settlement behavior without evidence that
those components need replacement. No sealed V2 change is justified by an
output-only ticket finding that was not established. Preserve CPU-only imports,
visible-state privacy, clock placement, typed failures and at-most-once delivery;
freeze a new candidate and prove RED/GREEN at those real boundaries if fixes are
authorized.

Largest remaining uncertainty: unexecuted malformed-field combinations and
separate deferred consumers. Cheapest falsifier of the proposed closure: rerun
the demonstrated cases plus an exact base outer event containing the skipped
nested action; check no dispatch escape, state change or new delivery. Kill
criterion for a fix: any malformed event still applied, any mutable accepted
strengths, any malformed envelope occupying a key, or any malformed receipt
establishing known acknowledgement. No claim of protection against malicious
Python introspection is needed or made.

## Evidence receipts and limitations

Executed in order, with snapshot cwd, exact snapshot/src PYTHONPATH, `-B -P`,
cleared child environment except SystemRoot/WINDIR/TEMP/TMP/COMSPEC and the four
explicit Python/Git settings, and absolute `C:/Program Files/Git/cmd/git.exe`:

1. `D:/Pontius-tools/py311/Scripts/python.exe -B -P <checks/events-probe.py>
   D:/Pontius-tools/py311/Scripts/python.exe 3.11.15` — exit 1. Retained diagnostic
   defect: the script expected a reveal constructor to know runtime-private
   overlap. This was a probe assertion error, not a target failure. All preceding
   observations remain in `checks/events-py311-receipt.json`; none are required
   without the subsequent complete run.
2. `D:/Pontius-tools/py311/Scripts/python.exe -B -P <checks/events-probe-v2.py>
   D:/Pontius-tools/py311/Scripts/python.exe 3.11.15` — exit 0, 25 cases.
3. `D:/Pontius/.venv/Scripts/python.exe -B -P <checks/events-probe-v2.py>
   D:/Pontius/.venv/Scripts/python.exe 3.14.6` — exit 0, the same 25 cases.

`<checks/...>` means the absolute corresponding path under this r001 packet.
The JSON receipts preserve exact argument arrays, environment, stdout, stderr,
exit and script hash. Full version and absolute executable were printed and
asserted before target imports:

- CPython `3.11.15 (main, Jul 23 2026, 14:42:43) [MSC v.1944 64 bit (AMD64)]`.
- CPython `3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)]`.

Final probe SHA-256:
`b5d14bcd68117a6ef5095ea64a575c2774463dc5a0ff11957dffc0ca387343c1`.
Final receipts: `checks/events-py311-v2-receipt.json` and
`checks/events-py314-v2-receipt.json`.

Each complete run independently reconstructed the sorted commit-blob manifest
and matched the packet's exact bytes, asserted HEAD and module paths, and
asserted clean snapshot status before and after. Each records 15 distinct breach
demonstrations grouped into the three findings, nine closed-route checks, and
one normal control. Exit zero means the expected candidate observations were
reproduced; it is not a clean or green implementation verdict.

No source, tests, configuration, sealed files or lifecycle artifacts changed.
No GPU, optional package, install, broad suite, production monkeypatch, private
state tampering, arbitrary __new__/__setattr__, implementation commit or push
was performed. Only packet diagnostic scripts/receipts and this attributed
report were created. No policy-authority residual, deferred trace/publication/
accounting issue, release-readiness verdict or timing/strategy claim is issued.
