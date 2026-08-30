# Cold B initial invariant and related-path inventory - r003

Recorded independently before opening r003 coverage.md.
Candidate: 30df7bce8da51715e6f1d7576892dd689421c516
Manifest: 21d9686c9918d9d0648fd98edf35219dfb5e0b4dc1dcfe5e4f28171b7d94e513

Permitted source inspected: candidate runtime.py, changed hand-replay tests,
no_limit_betting LegalBettingDecision/RaiseBounds/legal_decision, and sealed
immutable_blueprint key and action_for. Requirements: ADR-0485 blueprint
outcomes and four-input boundary, ADR-0484 brief, current CLAUDE/workflow,
r002 disposition and B-01. The prior r002 review read returned its full text;
this additional prior-round exposure is disclosed. No implementer material,
r003 peer review/inventory or r003 coverage claim has been read.

Invariant: an ordinary exact but malformed LegalBettingDecision, including its
RaiseBounds, must fail as InvalidDecisionContextError before any real sealed
lookup. Caller-selected structure must not set recursive traversal depth.
The valid decision comes from a copied, validated exact betting state. Exact
field identity must precede equality or caller behavior. Preserve owned policy
authority, honest hit/miss/illegal-entry classification, and four inputs.

Independently enumerated categories / paths:

1. LegalBettingDecision has nine fields: street enum; acting_seat, stack,
   street_contribution, current_bet, to_call, call_amount exact integers;
   action_kinds exact tuple of BettingActionKind; raise_bounds exact RaiseBounds
   or None according to the derived legal state.
2. RaiseBounds has five fields: minimum_raise_to, maximum_raise_to,
   minimum_full_raise_to, maximum_contestable_raise_to exact integers;
   all_in_only exact bool. Exact dataclass constructors accept malformed values.
3. Exercise each decision and bounds field with a deeply nested exact tuple;
   cover tuples replacing scalar/enum/record/None and nesting inside same-width
   action_kinds. A shape check must reject a mismatched immediate type before
   its depth matters. Length mismatch and wrong tuple element must both reject.
4. Preserve semantic mismatches as typed refusal: same-type wrong scalars,
   bool/int/float aliases, wrong enum member, action kind order/width, wrong
   RaiseBounds member/absence. Attribute/equality hooks on subclasses must not
   execute. Exactness remains necessary after the copy-before-compare removal.
5. Legal-state partitions: ordinary raise allowed, no raise allowed, short
   all-in-only raise, and a valid context after a public action. Retain matching
   hit, empty-table call/check miss, unrelated-key miss and illegal matching
   entry controls through the real public helper, plus existing runtime tests.
6. Ownership paths: public selector -> _admit_blueprint -> owned source ->
   _select_admitted_blueprint_action -> copied cards/betting -> kernel-derived
   decision -> BlueprintDecisionKey.from_state -> sealed action_for. Real
   profiling can observe lookup without replacing it, proving invalid fields
   never reach selection and valid calls use owned source/derived decision.
7. Adjacent changed containment: _admit_blueprint normalizes RecursionError to
   TypeError; _select_admitted_blueprint_action normalizes it to typed context
   refusal. Preserve actual authority and outcome checks; no table/history
   operational depth limit or broad hostile-Python audit is introduced.
8. Integration/quality: only runtime.py and test_v0a_hand_replay.py may differ;
   sealed action_for, no_limit_betting and replay remain unchanged. Verify
   stored-blob manifest ordering/bytes, LF/BOM/width/whitespace, final public
   signature, focused suite discovery (new class occurs after main definition
   but before invocation), actual 3.11.15 then 3.14.6 snapshot runs.

Planned evidence: independently generated real-boundary category probe and
valid controls; predecessor narrow RED to establish sensitivity; candidate
GREEN; changed suite plus related contract/replay suites under exact snapshot
procedures. No production/test edits, broad/GPU/dependency run, lifecycle,
value/trace/publication correction, operating-bound or strategy claim.
