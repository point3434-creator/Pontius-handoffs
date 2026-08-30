# Independent cold A inventory - r003

Recorded 2026-08-30 before opening deferred coverage.md.
Candidate 30df7bce8da51715e6f1d7576892dd689421c516; expected manifest
21d9686c9918d9d0648fd98edf35219dfb5e0b4dc1dcfe5e4f28171b7d94e513.

Scope: r002 B-01 typed malformed-context refusal plus advisory test reflow.
No implementation, value/trace/publication expansion, operating budget, broad/GPU run,
source integration, or lifecycle authority.

Cold inputs read: r003 handoff/candidate/manifest, frozen source/tests, frozen ADR-0485
and ADR-0484, relevant frozen brief, current CLAUDE.md/workflow checklist, r002
disposition and named B report. Transparency: the complete named prior B report was
opened while obtaining B-01, exposing its other prior-round closure/advice sections.
Coordinator was informed and permitted continuation; no implementer material or
parallel r003 review/inventory was read. Deferred r003 coverage remains unopened.

Discovery: inspect the frozen diff, public selector and its actual callers, record
field definitions in no_limit_betting, key construction and immutable lookup, and the
acceptance split in ADR-0485. The changed implementation touches only runtime admission;
tests add a malformed-field control. Source-derived members below are not a coverage
claim from the implementer.

| Invariant / risk | Related paths / observable outcome | Planned evidence |
| --- | --- | --- |
| All malformed ordinary exact decisions fail typed before lookup | select_blueprint_action -> admitted selector -> key/lookup; all 9 LegalBettingDecision fields and all 5 RaiseBounds fields | Public-helper cases across deep/shallow tuple, wrong primitive type, missing bounds, malformed action-kind members; exact InvalidDecisionContextError and zero lookup calls |
| Traversal follows legal schema, not attacker depth | Scalar fields, action_kinds tuple length and members, optional bounds and every bound field | Deep nesting beyond interpreter recursion in each field; same-width action_kinds with nested child; no arbitrary configured depth limit |
| Exact type equality precedes caller behavior | Dataclass/container/scalar subclasses, truthy/equality/iteration hooks; bool/int and enum/string aliases | Normally constructed replacements and hook counters; no monkeypatching production or private writes |
| Genuine complete decisions remain valid | Raise-allowed preflop, no-raise all-in call, check context, all-in-only bounds, nonempty history | Owned copies of public kernel decisions and legal hit/miss controls |
| Policy source still owns lookup identity | Public helper admission, HandRuntime constructor and dispatch; exact nested source graph | Existing authority regression tests plus public observations of actual action_for receiver; source digest agreement |
| Outcome classes stay honest | Legal hit, missing match/passive, illegal matching entry, invalid context | Direct public selector and real mailbox runtime regression tests |
| Four-input isolation and sealed machinery unchanged | select_blueprint_action and private admitted selector signatures; immutable_blueprint and legal kernels | Signature check, stored-blob diff identity and focused existing suite |
| Floor and current runtime evidence are genuine | CPython 3.11.15 first, then 3.14.6; fresh D-local clone outside packet | -B -P, scrubbed env, snapshot cwd/src PYTHONPATH, absolute Git, module-origin assertions, retained exit/output receipts |

Related boundary limit: cards and betting are validated record types, unlike the
unvalidated decision/bounds records. Their copy remains recursive, so the added
RecursionError containment should preserve typed failure for any ordinarily accepted
malformed graphs without changing a valid-table/history operational limit. Broad
hostile introspection, mutated enum singletons, private field mutation, arbitrary
recursion-limit changes, and source monkeypatching are outside the contract.

Initial design assessment: schema-directed comparison against a fresh kernel decision
appears suited to this finite decision boundary. Verify before final verdict; the
unchanged owned-source design does not need expansion for a malformed scalar field.
