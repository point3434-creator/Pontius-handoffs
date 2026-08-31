# Engineering inspection: storage-integration coverage

Date: 2026-08-31.
Author: Codex mapping_compatibility subagent.
Engineering-only, source-only coverage inventory. Not a cold review, behavioral
pass, defect reproduction, or authority to edit/run tests. No new tests were authored.
The only write authorized for this inspection is this create-only report.

## Identity and method

T = D:/Pontius-handoffs/v0a-i01-c-authority.
A/B probes reside at D:/Pontius-handoffs/v0a-i01-ab/r010/checks.

Production reasoning is bound to retained engineer-generator-v19.py, SHA-256:
3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1

Read the two engineering inventories, the frozen public24 source/oracle pack, the
matrix source, relevant preserved DesignReviewTests methods, and all named
supplemental probe sources. rg and stdlib AST parsing were used for discovery.
No target module was imported, no source program/oracle/test was executed, and no
production worktree was edited. Historical receipts identify sources and scope;
they are not fresh evidence for the port under construction.

Recomputed input SHA-256 values:

engineer-object-order-assessment-v1.md
748e19189c35865cf9d486c48557a7ed60d6c60c2893815f2b0c4961b779033d
engineer-storage-mapping-compatibility-v1.md
9617c9b5d9d502a707e124483586b59488f7b1ec670d3f375f0615132a762180
tests-checks/name-environment-cases-v1.json
d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c
tests-checks/name-environment-probe-v1.py
94a91ff970aa0df12c4334d72a2476ca5d58a4b76aa3a412c5440e93411806b4
tests-candidate-v4.py
06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd
coordinator-join-probe-v1.py
1d91f234169e17833c7a40c35674564a6b6daa687d658cb06d93dbecd7341995
engineer-alternative-write-probe-v1.py
af60abeef878d5c66bd4e17696a6bae7de59c072746018d5ba34df10ff0cc70b
engineer-lexical-probe-v1.py
42b891a13b0fb1dbbc3a2c8cf58824fb59e20260107c3a0fbae7a2ec53e0619c
A/B checks/codex-a-probe-targets-v2.py
b0171cf48c0905f558829173c549c85cee760786565fe88fe2a5f3cfd00d1669
A/B checks/codex-b-probes.py
d68762c9c55edff55325d02c4301096c0201471a7b27e84edfa48380656ff4ee

## What the existing suites establish when rerun successfully

Matrix192/212 denotes 192 schedules and 212 harmless runtime projections, not two
separate suites. Its classification split is 92 refuse, 81 clean, 19 permitted
refusal. The eight methods begin at 31854, 31913, 31956, 32009, 32034, 32069,
32131 and 32209 of tests-candidate-v4.py.

- public24: sixteen N/S/D scaling schedules; hidden reader/setter cell join reached
  and dormant; delete/reinsert both directions; direct parameter hydration unsafe
  and safe; default capture versus later cell rebinding. The hidden-cell dormant
  case permits refusal. Semantic assertions are public argv/blocker classifications.
  The old observer is specific to v19 copy/merge work and needs the already-required
  representation-correct accounting, including terminal ordered work.
- design53: substantial existing public behavior coverage, including source-point
  defaults and saved callables (20913), forwarding/order and aggregate defaults
  (21248), bound receiver and implicit protocol context (21322, 21578, 21701),
  native dormant versus consumed storage (21459), missing lexical proof (21490),
  class default/decorator bindings (21534), and legitimate helper nonlocal/global
  effects (21615). Earlier call-local environment/source-order tests begin at
  3928 and 4612. These are not private store-equality assertions.
- matrix: capture/default/live-cell routes (64), live rebinding/separate activations
  (28), native alias mutation (24), extraction before clear (16), class binding and
  construction failure (16), exception/join successors (12), issued witnesses (16),
  and joined activation alternatives (16).
- coordinatorjoin8 repeats cell/default x unsafe-first/safe-first/both-safe/
  both-unsafe activation selection with both harmless choices. The matrix also
  covers statement and conditional-expression selection. Both-safe permits refusal.
- weakwrite3 covers alternative-cell weak clear, alternative-object clear, and
  alternative-object store, then accesses an original alias. Each has one unsafe
  feasible choice and requires a blocker.
- lexical6 covers captured/deleted exception names and exact body/handler order;
  three required-clean and three required-refuse cases protect deletion timing.
- A19 covers late live cells through returns, dict extraction, earlier class
  methods in defaults/decorators, and lookup before arguments.
- Preserve B18 required plus one excluded. The B file contains 19 raw cases; its
  historical release16 summary reports 18 satisfied and default-unbound-first
  unsatisfied. The excluded absent-global assumption does not become a new port
  requirement. Preserve all issued bytes and the existing scope disposition.

## Falsifier-to-coverage assessment

Two raw aliases sharing one input object: native aliases are covered locally, and
single-parameter hydration is covered. No identified frozen schedule combines
the same mutable actual argument in two formals with a write through one followed
by consumption through the other. Scenario 1 below closes a public-behavior gap.

Multiple pending callable/default/receiver/aggregate entries: the matrix and
design tests cover these forms and their relevant effects separately. Reordering
independent registrations alone does not create a new observable requirement.
No mandatory synthetic mixed-pending test follows without a public discrepancy.

Branch-origin reference alternatives: directly covered by matrix joined-activation
and coordinatorjoin8; weakwrite3 also guards against strong replacement of one
alternative. These checks must remain, including the unsafe-first cases.

Retained owners sharing a proof key: no public discrepancy was established from
first-owner selection alone. At v19 17667-17698, traversal continues into every
duplicate's receiver/default/retained/cell children even after owners.setdefault
keeps a prior representative. Immediate refusal at 17747-17754 and 18349-18364
uses the caller-supplied site/reason and invalidation keys, not a selected owner's
source origin. Thus a hypothetical first-owner change is not by itself a proved
change in public blocker origin or sensitivity. Retained callable-result effects
at 18021-18027 still require preservation/proof. Keep explicit refs and retained/
cell tuple order unchanged; do not demand a fabricated same-key test without a
parsed-source witness that distinguishes public rows, blockers, or reached effects.

Missing-store references: design21490 tests missing lexical proof, not a dropped
object-store record. No direct missing-store-reference schedule was identified.
Scenario 2 tests retention through legitimate helper plus class adoption and can
expose a lost record/cell as either false admission or invented refusal. Fabricated
forward IDs are outside the parsed-source contract and are not proposed as a gate.

Shared/overlapping cells: public24 shares a cell between reader/setter callbacks;
weakwrite3 and matrix joined activations exercise alternative cell sets. None of
these proves that two different projected name keys contain overlapping cell IDs.
A legitimate parsed-source path to that exact internal shape was not established.
Keep the conservative ordered fallback, but do not manufacture a private overlap
and call it a missing public contract. A real reachable witness remains relevant.

Retained snapshots before/after join: existing saved-default/saved-definition,
call-local environment and source-order tests cover retention behavior; public24
adds normal/exception joins. None uses literal identity equality. No separate
synthetic allocation-order assertion is warranted.

Raw same-object reinstallation of a certified no-work value: raw installation must
clear certification and preserve the next existing transfer boundary. For a value
satisfying the narrow proof, that transfer still returns the identical no-work
value. No semantic RED was established from omitting that transfer alone; the
direct obligation is transfer/accounting correctness. Supplementary observation
may audit it, but a private certificate assertion is not a public semantic oracle.

Mapping views: the prior source inventory found no live same-map overwrite
consumer. Generic view divergence is a bounded adapter-proof issue, not a new
public test requirement. Overlay/adoption behavior is covered partly by source-
ordered helper/class tests; Scenario 2 adds an observable preservation composition.

## Minimal proposed source scenarios, not executed tests

These are proposed additions for later bounded authoring/review, not assertions
that current production fails. Use the real derive_design_review boundary.
Sensitive fixture source must remain bytes-only; independently assemble harmless
programs with event sinks. Never execute the inspected subprocess body.

### Scenario 1: identical mutable actual bound to two parameters

Core source body:

    def mutate(owner=ReviewTests):
        owner._launch = None
    def relay(first, second):
        first.append(mutate)
        second[0]()
    items = []
    relay(items, items)
    return self._launch()

Independently harmless expected trace: relay, store, callback, write; final
TypeError because the final sink binding is None. Public expectation: explicit
blocker required, not merely row loss. A port that breaks alias sharing could
instead see an empty second list and silently discard the relevant callback.
No numeric object/cell identity is asserted.

Dormant control removes only second[0](). Expected harmless trace: relay, store,
sink; result fixed. This direct represented storage does not execute the callback;
require the fixed row without an invented callback-effect blocker. This is not a
request for precision through an unsupported returned/native-extracted callable.

### Scenario 2: class-body helper changes an outer captured cell

Core unsafe source body; use the existing module-parameter sink form:

    owner = None
    module = "outer"
    def read():
        if owner is not None:
            owner._launch = None
    def change(value):
        nonlocal owner
        owner = value
    class Local:
        module = "inner"
        change(ReviewTests)
    read()
    return self._launch(module=module)

Independent harmless expected trace: change, read, write; final TypeError.
Public expectation: explicit blocker. The read closure must observe the changed
cell after helper completion18463 and class completion23026. Preserving only the
outer name's stale None projection could falsely admit the final sink.

Safe counterpart initializes owner to ReviewTests and calls change(None).
Expected harmless trace: change, read, sink; result outer. Public expectation:
exact argv [-m, outer] and no blockers. This simultaneously catches lost retained
authority/cells causing an invented refusal and accidental adoption of class-local
module="inner". No returned closure, reflection, fabricated ID, or optional
effective-result precision is needed.

The existing hidden-cell join and activation cases should remain the join coverage
for this first increment. Add a joined class variant only if inspection or a real
failure shows that the straight-line adoption cases miss a distinct public path.

## Verdict and limits

Coverage verdict: PARTIAL for the new storage port; two small observable
compositions are useful additions. No product defect is claimed and no new
acceptance test is imposed solely by private ordering, allocation, or storage shape.

Design verdict: SOUND for a bounded storage replacement while preserving current
explicit tuple order, ownership/adoption, cell writes and the original public
contract. The first-owner and raw-certification concerns above remain static
proof/accounting obligations unless a public witness establishes more.

This inspection does not replace fresh floor-first runs, complete public output
comparison, corpus generation under unchanged caps, or subsequent blind reviews.
