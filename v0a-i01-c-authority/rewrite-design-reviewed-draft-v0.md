# C core replacement — Stage 0 decision and brief

2026-08-31. Tier C, FIX within the existing A/B/C integration. Engineering design,
not a frozen implementation candidate or a cold verdict. The controller has
authorized the coordinator to choose full rewrite, partial rewrite, or continued
repair. The coordinator selects partial replacement of C's analyzer-state and
helper-authority core. Claude remains the integration checkpoint finalizer.

## Decision and limit

Keep accepted A/B and the working parts of C. Replace the internal representation
and the operations that currently reconcile captured FlowValue projections,
current authority records, live lexical cells, and deferred carriers. Repeated
source findings concern that reconciliation; the latest actual analyzer run also
still fails its generator-depth contract at the unchanged work cap. Neither fact
establishes that a rewrite will be faster. The first implementation checkpoint
must test that hypothesis through the public analyzer.

This supersedes the architectural choice in stage0-design.md to keep legacy
abstract values as an independent semantic representation alongside a separate
authority payload. It does not supersede its behavioral requirements, original
RED evidence, preservation requirements, or review gates. The v25/v30 proposals
and unfinished v31 scratch remain retained. Further layered repairs and the v5
diagnostic are held; no old result is relabeled.

Continuing the current patches retains the demonstrated synchronization burden.
Rewriting all of C would also disturb boundary enforcement, CI, admission output,
and native publication without evidence those components need replacement.
The selected boundary is the smallest one that removes the duplicate semantic
state; changing only the mapping backend would not do that.

## Base and permitted paths

Rejected r010 base: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358, manifest
8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb.
Implementation will use a new isolated codex/ worktree from that base, not the
current main checkout or the retained v20 worktree. A worktree is not created by
this brief. Candidate construction must name and hash every adopted input.

Production allowlist stays tools/generate_test_inventory.py,
tests/test_inventory_and_profiles.py, tests/test-inventory.json, and
tests/test-profiles.toml. Preserve the 13 other paths in
coordinator-preservation-baseline-v2.json byte for byte. The generated pair changes
only by ordinary generation after analysis passes. Main's CLAUDE.md and
docs/workflow.md edits belong to the user and remain untouched.

Keep parsing/discovery, exact argument-binding rules, capability schema and
approval digest, exception-partition rules, native transaction/Git writer,
boundary checker, CI configuration, and all five existing analysis limits.
Retain reusable pure evaluators only where their inputs and outputs cannot hold
an alternative copy of live helper state. Do not add a package extraction or a
general Python interpreter to this FIX.

## One state model

Use a typed value/reference model and one successor-owned state. Immutable
scalars carry their values. Mutable collections, namespaces, callable objects,
lexical cells, and deferred frames have explicit identities with one current
record per successor. Alternatives and unresolved dependencies are first-class
values, not an empty proof and not an overloaded secondary channel.

Share immutable lexical scope metadata at its proven lifetime. A call frame owns
its local bindings; lookup follows explicit local, closure, class, and module
rules instead of copying all ambient values into each child frame. A closure
retains the cell even when it is currently irrelevant or unbound. A default
retains the value/reference selected at definition time. Those are distinct
relationships within the same model.

All relevant operations use the same interfaces: read/bind/delete name,
read/write member or element, construct/capture/call/return, create/consume/escape
deferred work, and fork/join successors. A mutation changes the current object
record; another alias does not need a repair walk to see it. Extraction selects
its result before removal. Unknown alternatives and missing-store conditions
remain explicit. A failed or unimplemented read cannot fall back to a stale
legacy projection.

Historical call observations are immutable source-point observations. Selecting
a callee before evaluating its arguments must not freeze live closure-cell
contents too early or allow later rebinding to replace the selected callable.
Final evidence emission may consume a read-only projection, but that projection
must not re-enter execution as a second authority store.

Class execution has an explicit class namespace; methods resolve free variables
through lexical/module rules, not the class namespace. Definition/decorator and
default ordering, failed construction, and source-point installation remain
binding. Fork/join applies to normal, break, continue, return, and raise outcomes,
including existing handler tags and finally semantics. Deferred creation is not
consumption, and conservative refusal is not evidence of an executed effect.

## Removal and migration obligations

The replacement must eliminate the live dependence on _transfer_authority,
_AuthorityRecord.value reconciliation, independently authoritative FlowValue
helper fields, stale collection-result fallback, and carrier/projection repair
walks in the converted region. Replace _ExecutionState's generic MutableMapping
compatibility contract with explicit scope/state operations. The NameVersion,
NameCursor, radix/history/no_work machinery is not a product requirement.

Do not port all of those mechanisms merely because their isolated tests passed.
Any reused primitive keeps its old requirements; retired implementation-specific
tests and counter identities retain their evidence but do not force a new API.
Alias behavior, observable evaluation/order, snapshot stability, failure safety,
and actual-work accounting remain requirements regardless of representation.

An intermediate candidate can support only a declared syntax subset, with
explicit refusal outside it. Within each selected public analysis there is one
engine: no fixture-name dispatch, silent fallback to the old engine, or success
assembled from two models. No intermediate candidate is integration-ready.
Unconverted legacy code may remain temporarily only with an enumerated, inspected
boundary; the final candidate removes dead superseded state machinery.

## Named implementation increments and early checkpoint

R1 — State and temporal behavior. Establish the canonical value/object/cell state,
scope lookup, call capture, current alias reads/writes, and minimal deferred
retention. Wire the real public analysis entry, not a stand-alone map benchmark.
Use existing reached/dormant alias and cell controls as the first behavioral
checkpoint. Include class-versus-closure source ordering before declaring the
state model fit; these were a source of residuals, not optional generalization.

R2 — Control flow and cost fitness. Migrate the necessary successor,
construction, deferred consumption, and helper-entry paths. Exercise the original
helper65 and generator70 exact depth refusals plus existing small/large ambient
name cases. Retain every original budget epoch and all preparation work. No cap
increase, refund, reset, charge discount, or hidden preparation is permitted.
The implementation plan must bind the finite existing case IDs, source hashes,
models, and unchanged expected outcomes before dispatch.

The continuation test requires correct public rows/blockers and exact required
depth results, no N-sized ambient-value reconstruction at unchanged forks or
joins, and explicit accounting of real allocations, reference/edge work, lookups,
copies, and failures. Ordinary owned maps and explicit sharing are the initial
storage choice; first-write copies are real work and must be charged. A proposed
196608-unit ceiling (75% of the existing 262144 cap) reserves engineering headroom
for the rest of the migration. Its sufficiency is unproved; it is not a new
runtime admission cap. It must be dispositioned and frozen before a fitness run,
not selected after looking at the result.

R3 — Complete the declared contract and retire the old core. Run the fixed design
checks, temporal matrix, all seven semantic packs, and original inventory tests.
Respect required-clean, required-refuse, and permitted-refusal categories from
the existing acceptance/addendum; harmless runtime behavior alone does not make
an unsupported shape required-clean. Run the first real repository generation
checkpoint before adding optional precision. Preserve original capability rows,
entry assignments, approval digests, and profile behavior; attribute any census
changes mechanically. Delete superseded live state/compatibility paths.

R4 — Freeze and acceptance. Freeze one coherent candidate ref plus manifest;
obtain two fresh mutually blind cold reviews, then run the permitted CPU
acceptance. Existing engineering participants are not cold reviewers for this
replacement. Submit the exact candidate to the named finalizer. Main integration
still requires the controller's candidate-specific commit authorization.

Sizing: this is an architectural replacement, not a small patch. The current
resolver/support surface spans many thousands of lines. Plan for multiple named
reviewable slices, each at most about 3000 changed lines; pure deletion must be
reported separately rather than concealed. R1's first attempt is bounded to
2500 changed implementation lines before reassessing its shape. Do not widen a
slice silently. No calendar or total-line reduction is claimed in advance.

## Acceptance and evidence discipline

The binding requirements are r010/acceptance.md in v0a-i01-ab, the original
Stage 0 behavioral contract, tests-scope-addendum-v1.md, and retained fixes to
test assertions. No failed result is converted into a new allowed behavior by
this design. All original 53 design checks, the current fixed matrix, and the
52-case semantic population remain later gates. Their counts do not establish
exhaustive correctness.

Run floor 3.11.15 first, then the same bytes on 3.14.6, only through reviewed
controllers in fresh disposable D-local snapshots. Sensitive inspected source
is AST-only. Harmless Models remain separate. Record actual executable and patch
version, source and controller hashes, environment, command, child completion,
and raw output. A setup failure, timeout, or missing output is incomplete
evidence. No optional dependency or guarded/GPU suite is authorized here.

Before implementation, retain a separate category/coverage plan identifying
source searches, affected transfer and consumption boundaries, live versus
historical roots, deferred obligations, and unknowns. It is engineering material,
not initial cold-review input. Public behavioral evidence is required; structural
tests alone cannot establish a closed defect class.

Stop a failed fitness attempt before broad migration. Record which invariant or
cost obligation failed and reassess the model; do not automatically add another
backend or expand the supported Python subset. This is the protection against
repeating the current patch accumulation under a new name.

Seams crossed: static AST semantics, abstract state and evidence rows, snapshot
test controllers, and ordinary inventory generation. Native transaction, Git,
lock ownership, CI and product A/B seams are preservation checks, not rewrite
targets. This brief proves no product hand, live 15000 ms wall, experiment
acceptance, faster runtime, cold CLEAN verdict, or successful integration.
