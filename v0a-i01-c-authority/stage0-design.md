# C authority transfer: second-residual reassessment

Date: 2026-08-31. Status: pre-edit engineering disposition and coverage plan.
Task: v0a-i01-c-authority. Round kind: FIX, responding to the rejected r010 pair.
This is a separate contract-focused candidate. It does not reopen accepted A/B.

Rejected candidate: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.
Manifest: 8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb.
Issued findings: ../v0a-i01-ab/r010/reviews/r010-review-codex-a.md,
SHA-256 5e195c8bf1f38757a47725604c9e3f6a5f5f310c31bd6b4bdad8c24628987f90;
../v0a-i01-ab/r010/reviews/r010-review-codex-b.md,
SHA-256 15000025f5e128bb93c4af9cba336adeb448a71f8ecff5546fb95e47b84d91b1.

## Why the previous attempts missed

r008 was the first review of C's helper-identity contract. The r009 FIX retained
exact helper provenance and effective arguments, but discovered relevance from
incomplete roots: captured defaults, free variables and forwarded callbacks could
be omitted. r009's cold review established the first residual. Its successor
introduced callable/default/free-value/obligation metadata and a common reachable
authority walk. That corrected the supplied executions, but attached parts of
the proof to independently copied values and special return/cache paths.

r010 is the second residual. A-01 proves a returned callable loses a live cell
dependency while its current value is irrelevant. A-02 proves a collection method
result can discard authority present in its receiver. A-03 proves a method
definition is not installed as a source-point class binding before later
construction expressions. B-01 proves direct-local repair leaves older nested
aliases stale after a native-list store. Sixteen public false negatives reproduce
on both supported interpreters; ordinary focused suites remain green.

The shared mechanism is incomplete transfer of stateful authority, not merely
missing consumer names. The earlier inventories named many paths, but neither
representation forced each path to preserve the same object/cell relationship.
Current-value reachability also conflated "no relevant owner now" with "no live
dependency can matter later." Tests exercised several kinds individually while
omitting their temporal composition. This note does not claim that enumerating
another list alone repairs that weakness.

## Adopted replacement boundary

Replace the bounded helper-authority state/transfer slice inside
tools/generate_test_inventory.py. Keep the existing parser, legacy abstract
values, public capability schema, argument binder, exception partition and
finite budgets. This is an implementation choice within the user's request to
engineer clean A/B/C; it grants no experiment, guarded profile or final commit
authority. The workflow independently requires this reassessment before edits.

Use an identity-indexed authority state carried with execution successors.
Legacy value/kind/sensitivity and helper authority are separate concerns. Values
carry one coherent authority payload/reference; the authority model distinguishes
callable objects, namespace/collection objects, and activation-owned lexical
cells. Definition-time defaults retain their then-current value/object reference;
closures retain cell references, even when the cell currently contains None or
has not yet been bound. Lexical name sets and AST positions are classifications,
not unique identities for repeated runtime activations.

The invariant is: every admitted transfer preserves retained callable identity,
captured defaults, relevant live-cell dependencies and unresolved effects unless
an operation-specific proof discharges them. Unknown is not an empty proof.
Consumption that cannot establish safety produces an explicit blocker. Storing,
extracting or returning a dormant callable does not execute its body. All aliases
of a represented collection in the same successor read one current authority
record. A previously observed callee/argument snapshot remains frozen at its own
source point and is not rehydrated from later mutable state.

One transfer operation must connect construction, name/member/subscript reads,
container/method results, assignment, call/return forwarding and joins. Existing
legacy evaluators may retain their result logic, but may not independently erase
the helper payload. Removing extraction captures the result before modifying the
container. A returned function preserves its cell references independently of
whether an owner is currently reachable. Unsupported result precision preserves
an unresolved dependency for later refusal instead of silently publishing an
unblocked stale capability.

Function construction follows existing Python source order: evaluate decorator
expressions/defaults under their proper namespace and adopted annotation policy,
apply decorators in reverse, then install the effective binding after successful
completion. Each admitted class-body binding statement updates the live class
namespace before the next statement. Method body free names still refer to the
enclosing frame, not the class namespace. A decorator or default failure does not
install a function or execute a later construction effect.

Fork/join authority state with every normal, break, continue, return and raise
successor. Preserve exception tags, explicitness and excluded-handler partitions.
Projected or dormant analyses use isolated state and commit only effects justified
by the existing completion semantics. Allocate abstract identities per bounded
creation/activation; joins retain alternatives and missing/unbound uncertainty.
Charge allocation, edge traversal, copying and joins to the shared existing
budget. Do not raise a cap to make the design pass.

## Alternatives and transition risks

A local correction of the four reported methods is smaller initially, but leaves
multiple independent stores and current-value filtering in control of safety.
It retains the demonstrated reason the prior two fixes missed siblings. Rejected.

A bounded rewrite of every embedded live FlowValue graph can repair aliases, but
must distinguish live roots from historical call snapshots, walk returns/defaults/
receivers/deferred frames/caches, and separately introduce live cell identities.
Missing a root recreates this defect; rewriting a historical root changes evidence.
It has a larger completeness burden than one object/cell state. Not selected.

A full generator extraction or general Python heap interpreter is outside scope
and unnecessary. The selected replacement is medium-sized: state plumbing and
shared transfers, with public behavioral tests. Main transition risks are branch
leakage, activation identity collisions, stale caches, duplicated effects, erasing
an already-captured callee during later mutation, blanket dormant refusals,
incorrect exception reachability and budget growth. These are required checks,
not reasons to relax the contract. If implementation cannot stay in this boundary,
record the concrete obstacle and reassess before expanding it.

## Discovery inventory and verification plan

Discovery used source searches for every authority field, FlowValue constructor/
merge, mutable collection identity update, return bridge, resolver creation,
state copy/successor, and definition binding; both issued reviewers' source
inventories were compared after their independent reports were immutable.
Affected mechanisms are proved at the four findings. Other rows below are
integration/coverage obligations, not additional claimed product defects.

- Value/identity/budget definitions: frozen source 9010-9069 and 9678/9798.
- Unknown/member/container flow and merging: 12436-12488, 13326-13366,
  13422-13483. Legacy sensitivity must not stand in for helper authority.
- Historical observations: _ReviewFlow 12338-12368 and _snapshot_call
  15747-15837, including callee-before-argument capture.
- Resolver/successor state: 13847-14050, exception capture 15938-15971,
  state joins and auxiliary save/restore 20656-20808, statement flow
  20855-21020. Audit all direct dict copies within the resolver.
- Callable capture/effects/return bridge: 17208-17927. Replace current-value
  filtering and direct-local alias repair, not just their demonstrated callers.
- Expression/call transfer: _evaluate/_evaluate_value from 17957, native
  method fallback 19538-19621, assignment 20156-20211, return 20983-21010.
- Function/class source-point construction: 22104-22436.
- Deferred resume/projection save/restore: 16284-16577, 16815-16966.
- Compatibility boundary: flow entry 22501/22544, registry/provenance
  22799/22833, review body 24106 and public derive_design_review 26165.

Before editing production source, retain deterministic RED against r010 through
the real public API. Issued A's nineteen-case probe has nine failures and ten
lawful controls on both slots. Issued B's observation corpus has seven confirmed
unsafe cases on both slots; exclude its unsupported absent-global assumption
from required expectations. These original bytes and raw receipts remain intact.
Additional generated tests must run against r010 first; record case identities,
oracle traces and results, including passing controls and any unreachable cases.

Generate bounded operation schedules from capture mode (default/live cell),
transfer route (direct/nested/returned/aliased), source-point operations
(construction/store/read/extract/rebind/consume), and execution context
(normal/branch/handler/finally/failed-before-effect). Include aliases before and
after retention, append/extend/insert, dictionary get/pop/popitem, return before
later rebind, repeated calls to the same factory, extraction before container
clear, class method bindings before defaults/decorators, and historical callee
capture before a later mutation. Pair reached writes with dormant and readonly
controls. Explicit temporal compositions supplement pairwise coverage; neither
the matrix nor source routing asserts exhaustive Python-language soundness.

Expected outcomes come from contract requirements and separately built harmless
runtime programs with event traces. Never execute the source containing subprocess
or optional/GPU sinks. An unsafe retained execution requires a blocker, not merely
row loss. Supported lawful controls require exact expected rows and no blocker.
Unproved Python constructs may refuse, but must not be mislabeled as executed
mutations. Preserve old test bodies and their semantic assertions.

GREEN requires every existing analyzer contract plus new matrices, on actual
3.11.15 first and 3.14.6 second in disposable D-local snapshots. Then verify all
141 original canonical capability rows/spec digest, all old inventory assignments,
unchanged profile bytes and no widened budget/baseline/CI. Attribute any changed
blocker/corpus assertions from a fresh census before editing mechanical literals;
ordinary generation alone updates inventory/profile outputs. Freeze a new pair,
publish final coverage as deferred review input and obtain two fresh mutually
blind reviews before the enumerated CPU acceptance wall.

## Ownership and preservation

Production FIX allowlist: tools/generate_test_inventory.py,
tests/test_inventory_and_profiles.py, tests/test-inventory.json,
tests/test-profiles.toml. Engineering uses a new isolated worktree starting at
r010. No production edit is made to r010, accepted snapshots or the main checkout.
The thirteen A/B/other-C preserved paths stay byte-identical. Keep controller
CLAUDE/workflow edits and the legacy dependency-baseline blob untouched.

The separate C task/round will declare only this contract for behavioral review;
the full combined snapshot may carry preserved paths only with explicit blob
checks. Any integration pair presented for finalization must bind the exact
reviewed bytes and their preserved dependencies. Claude remains finalizer, with
fresh candidate-specific controller authorization only after required gates.
