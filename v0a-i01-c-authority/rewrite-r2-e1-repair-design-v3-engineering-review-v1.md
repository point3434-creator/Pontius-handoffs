# R2-E1 repair design v3 engineering review v1

Review type: independent read-only engineering design review, not a cold review.
No source, input, Model, harness, or payload was changed or executed.

## Bound inputs

- Governing design v3 SHA-256:
  `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`
- Checkpoint-2 source SHA-256:
  `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`
- Checkpoint-2 source manifest SHA-256:
  `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`
- Creation-rule coverage addendum SHA-256:
  `b3da849d0ccedc2d675a98fa7d07a5ed90c3de3a204af961cef4e24b0bd824ec`
- Superseded-v2 engineering review SHA-256:
  `6d0351606ffa294e85e675df14f24f2fd224c61b921b7d18b69f1b46d9fce75d`

## Verdict

**SOUND and implementation-ready as a design.** V3 closes both Important findings from
the v2 review. I found no remaining representation, source-order, ownership, or
work-accounting design blocker.

This verdict does not admit a future candidate. The five prospective cases are not yet
frozen or executed, and every source charge, producer, predicate, and preserved path must
still pass the stated static proof before the floor run.

## Closure of the v2 findings

V3 now gives a complete builtin-authority consumer census for the admitted checkpoint-2
scope:

- six explicit absent-module names through `_c_read_name`;
- implicit `__build_class__` consumption at every admitted `ClassDef`;
- implicit `__import__` consumption once per `Import` alias and once per admitted
  `ImportFrom` statement.

The implicit gates read the executing frame proof directly. They cannot be satisfied by a
module member with the same spelling and do not route through `_c_read_name`. This matches
CPython 3.11.15 `LOAD_BUILD_CLASS` and `import_name`, and it keeps custom builtin mappings
outside the promised model.

V3 also corrects class source order. It gates `LOAD_BUILD_CLASS` and computes the
class-body creation proof from the incoming state before `_c_eval_many(node.bases)`, then
retains that scalar across base outcomes. CPython emits `LOAD_BUILD_CLASS` and creates the
class-body function before evaluating bases, so base effects can no longer rewrite the
captured proof. Methods still compute their own proof from the reached class-body state.

The ordinary function, call-frame, and initial module-frame placements remain sound. The
future checkpoint-3 obligations for `range`, `sum`, generator-record capture before the
eager outer iterable, and resume-frame projection are correctly identified as additions
to the same authority rather than a second mechanism.

## Work-accounting readiness

The design now identifies every new work owner and its frequency:

- one existing namespace/object read plus module-membership and conditional inherited
  proof reads at each creation-helper call;
- one retained-field unit at the sole `_CFunction` producer and each of the three current
  `_CFrame` producers;
- explicit fallback table lookup, matched proof read, kind decision, and unchanged
  producer/refusal work;
- a pre-base class proof decision plus separately charged class-body creation proof;
- one import proof decision per real `Import` alias and one per admitted `ImportFrom`
  statement;
- any actual container/tuple/reference used to retain class proof across outcomes, while
  a plain local scalar introduces no fabricated persistent-copy charge.

No `_CState`, `_CView`, namespace, cell/object table, snapshot, join, outcome, trace, or
call-observation field changes follow from the current proof field. The source census
remains one function producer and three frame producers, all frozen/slotted with no deep
record equality.

The phrases `read/branch` and `proof decision` are sufficiently concrete for source
authoring because the final integer charge follows the actual implementation: one cached
decision is charged once; separate reads/comparisons or repeated per-outcome work are each
charged. The candidate ledger must expand these into exact `consume` calls and prove the
stated frequencies. It may not use the design wording to collapse two operations that the
source actually performs or charge skipped work after a false gate.

## Coverage sufficiency

E01-E04 plus T01-T03 cover the full creation rule:

- proved frame / absent key -> proved;
- proved frame / present key -> unproved;
- unproved frame / absent key -> unproved;
- unproved frame / present key -> unproved;
- historical false proof survives deletion, while a new record under a still-proved
  frame can recover after deletion.

The separate nested-class and function-local-import witnesses are both necessary. One
cannot substitute for the other because the consumers bypass `_c_read_name` at different
source seams. A separate `ImportFrom` runtime case is not needed if the static proof shows
its distinct once-per-statement gate and the same exact frame-proof predicate.

The five prospective additions are sufficient only as the combined behavioral-plus-static
gate stated by v3. In particular, their outer `ReviewTests` class is created while the
module key is present but the module frame remains proved. A wrong early refusal based on
current module membership could otherwise mask the intended nested class or import
refusal. The static proof must therefore establish all of the following:

- the implicit predicate is exactly the executing-frame proof, with no module-membership
  or frame-kind condition;
- a true gate preserves the prior class/import body byte-for-byte except for declared
  accounting and proof plumbing;
- the false class gate precedes bases/body/install, and the false import gate precedes
  symbol/binding work;
- the two unsafe cases retain their base/body/install and binding/sink latches, so late
  refusal cannot be reported as correct ordering.

V3 already requires these source properties. Binding the eventual expected blocker site
is useful if the public envelope exposes it, but no sixth E1 case is required when the
exact predicate and true-path preservation checks are enforced. Actual 3.11.15 remains
the first behavioral slot; 3.14 stays ineligible until its matching floor result is clean.

## Disposition

V3 can govern the bounded repair. Retain its immutable function-like provenance,
operation-local implicit gates, pre-base class capture, five-case prospective family, and
actual-work accounting. Do not revive v1/v2 absence rules, current-module consumer gates,
custom-map interpretation, catchable implicit exceptions, cap changes, or blanket
function/class refusal.
