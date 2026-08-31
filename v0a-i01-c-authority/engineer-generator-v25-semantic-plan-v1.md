# Bounded v25 semantic successor plan

> For implementation after root authorization: use the executing-plans skill.
> All steps remain unchecked. This document authorizes no source edit or payload.

Author: codex/mapping_compatibility, engineering inspector and v23 author.
This is engineering diagnosis/design, not a cold review or an acceptance verdict.

**Goal:** Repair the two retained v23 wrong-clean outcomes and close the bounded
related deferred-obligation paths, preserving the 34 passing requirements per slot.

**Architecture:** Keep v23 lexical cells, class frames, namespace projection and
name storage. Activate reached factories that construct retained values. Keep
named class-member obligations in the existing authority records and carry their
negative deferred obligations to reached consumers, without interpreting a
general class namespace or executing deferred bodies.

**Tech stack:** Existing stdlib AST analyzer; Python 3.11.15 floor and 3.14.6 dev.
**Spec:** Root's v23 disposition, accepted class-name addendum v2, frozen C/Q/R
case packs, and the bounded instructions to this author. Root owns all dispatch.

## Pins and evidence limits

All paths below are relative to D:/Pontius-handoffs/v0a-i01-c-authority.

- Base: engineer-generator-v23-semantic.py
  SHA256 53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499
- Original authorization: coordinator-class-semantic-v23-disposition-v1.md
  SHA256 d5b1d838a1d5bbbf591dff8974c7c8d7fb8e0a033477573b9c8143d92d1dd72a
- Accepted class-name addendum v2:
  SHA256 de7b5417b2cc899710af0a32332360f31546b6264d1cb58896104a362568e93f
- Root verification: coordinator-v23-semantic-verification-v2.json
  SHA256 33a2257f5ec5ac31ec3f4b59342dc46e86bcab6451df1656ca7fd1931aa1d1a7
  It reports 14,166 independently rehashed files across eight retained runs;
  36 cases per interpreter, 34 passing, identical residuals C03 and Q05.
- A's source inspection: tests-checks/class-comprehension-v23-engineering-review-codex-a-v1.md
  SHA256 84461f44efa2da40cfc8729a0d80eb45c0266e4e88a67d88d9d7703c955d44cc
- Frozen R01-R08: tests-checks/class-comprehension-extension-cases-v1.json
  SHA256 eb5551c054fc89da28fd2e4db433f56f7a3dbbd4cdb70509070a89fe362c74fd
- R specification: tests-checks/class-comprehension-extension-spec-v1.md
  SHA256 ed292bcf0207aad474e8293cf055c17de6409b9d851f95a8b8225d4375848dc6
- C12: tests-checks/class-semantic-extension-cases-v1.json
  SHA256 925ae5b9354377a5957f0c32c8bf5b58fea01612498b835abd6392f9cc87d268
- Q6: tests-checks/class-comprehension-boundary-cases-v1.json
  SHA256 9df895eb5bd645a5e4ef05be0f7c0a3db76df458ca023bbfbd36407ee3496b71

Inspection used source/text search, existing JSON/log reading and byte hashes.
No candidate import, analyzer invocation, Model execution or sensitive-source
execution occurred. The author rechecked the v23 source, root verification, A
note and R pack/spec pins. The root verification's complete snapshot rehash was
not independently repeated by this author. R cases have no execution standing
in this document; source concerns below are not additional demonstrated REDs.

No W/main/test/fixture mutation, ledger, commit, storage-v24 change or payload is
authorized. All issued v23 bytes and the original 36 cases remain immutable.
The prospective source is a separate T-only v25 semantic file based on exact v23,
not v24. No storage algorithm, cap, runtime requirement or test expectation changes.
Preserve v23's contiguous name-storage region and all 17 other watched paths.
W generator remains e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679.

## Retained C03 diagnosis

The actual 3.11 C12 receipt is class-extension-v23-diag01-311-receipt.json
under tests-checks, SHA256:
7536482e030cb2d31267c06bd4ad537e1a82c9bdd3dfb427887d27af023f1e1a
Its stdout SHA256:
4dc32c72c5aab22067d6b4958e48342a30f6037230402355015a2663e74a9f21

C03 defines armed=False and a factory that defines a write-only nonlocal setter,
returns it, and is called from inside a class whose local bindings have reset.
The returned setter is called with True, then the outer reader runs. The harmless
trace is factory/set/read/write, followed by TypeError; sink is unreachable.
Required outcome is an explicit public refusal. v23 instead returns argv
[["-m", "outer"]] without blockers. C04 reverses the scalar polarities; its
fixed permitted-refusal outcome is currently a refusal. Expectations do not change.

The following mechanism is a source inference explaining the retained outputs,
not a new instrumented execution:

1. _helper_effect_shape at 19064-19085 uses the factory's own lexical declarations,
   while its metered walk sees descendant bodies. Own locals are {setter}; loaded
   names are {setter, value}; the child's armed Store is not a factory nonlocal
   Store. Thus has_stores=False.
2. _apply_helper_call_effects removes factory-local setter at 19591-19592.
   The child's parameter value is not a factory input. relevant is empty.
3. The ordinary no-work gate at 19613-19617 exits before interpreting the factory.
   No setter is constructed and no actual return authority is published at 19658.
4. The return bridge itself exists: Return at 22868, probe.return_values,
   results at 19658, _evaluate at 19732-19759, and _transfer at 15383. The latter
   promotes a sole actual callable only when the legacy result is unknown.
   A conflicting legacy result must retain alternatives, not invent precise proof.
5. The single-Return helper shortcut at 18710 does not cover this two-statement
   factory. C03 remains False and C04 remains True, matching their opposite outputs.

This is downstream of transitive lexical capture discovery. Do not reopen the
proved cell-origin design or infer a new capture from an arbitrary loaded value.

## Task 1: construction-aware reached activation

Prospective surface: _SourceOrderedResolver only, source anchors 15199,
19064-19085, 19557, 19613-19617. Extend the cached tuple to:

    tuple[frozenset[str], bool, bool]
    # loaded names, has stores, constructs retained value

The third bit is set during the existing metered walk for FunctionDef,
AsyncFunctionDef, Lambda or ClassDef. Descendant syntax may conservatively set
the bit; interpretation still follows existing reachability. This is a work
obligation, not a claim that a descendant body has run or a refusal reason.

- [ ] Update cache annotation, shape return and the sole unpack at 19557.
- [ ] Require the bit to be false in the ordinary no-work gate.
- [ ] Preserve the separate deferred-creation gate at 19603 and deferred return
  at 19605-19612: a generator/coroutine call does not execute its body merely
  because that body contains a definition.
- [ ] Preserve no-registry/prepass, invalid binding, recursive/depth guards,
  active-helper behavior and explicit projected-body behavior.
- [ ] Check all three application callers: projected effects at 19202, ordinary
  call at 20691, decorator application at 24334. Projected effects keep their
  existing nonpublishing contract; real decorators are reached calls.
- [ ] Keep the literal-only unproved-callable shortcut and single-Return shortcut
  separate. Neither may replace actual returned capture authority with a name.
- [ ] Function/lambda creation evaluates existing defaults/decorators/headers,
  never the new callable body. A reached class statement executes its class
  body under the existing class boundary; method bodies remain deferred.

No new full AST walk or new cached cross-activation proof is needed. Existing
work charging and helper-depth caps remain exact.

## Task 2: named class-member obligation carrier

Use the existing live object store, adding two default-empty immutable fields
to _AuthorityRecord at 13956; no general member-value map or separate heap:

    member_obligations: tuple[tuple[str, tuple[_FlowValue, ...]], ...] = ()
    member_wildcard: tuple[_FlowValue, ...] = ()

These are may-roots, not values proved to be returned by a member lookup.
They grant no callable identity, lexical destination proof, member existence,
MRO precision or descriptor-dispatch exemption.

Proposed private APIs and contracts:

    _with_class_member_authority(installed, class_values, frame, bases, values)
        -> _FlowValue
    _class_member_obligations(owner, member_name, values)
        -> tuple[_FlowValue, ...]
    _retain_class_member_write(owner, member_name_or_none, supplied, values)
        -> None
    _join_member_obligations(left, right, budget)
        -> tuple[tuple[str, tuple[_FlowValue, ...]], ...]

The initialization helper receives the completed _ClassFrame explicitly through
_finish_class_definition; its one caller supplies the frame already owned by
_flow_class_statement. The transfer boundary's new keyword arguments are exactly
member_obligations and member_wildcard, both defaulting to empty tuples.
In _retain_class_member_write, member_name_or_none=None means selection is unknown;
supplied=None represents deletion, which grants no new strong-removal proof.

- [ ] On normal class completion only, collect reached final class-local values
  carrying helper authority or deferred obligations. Use frame.scope.local_names,
  excluding global/nonlocal declarations; never sweep enclosing/module fallbacks.
  Existing final namespace handles definite overwrite/delete inside the class;
  maybe-bound values retain every possible root. Already escaped aliases remain
  independent roots. Keep existing method_authorities metadata unchanged.
- [ ] Register these roots through _transfer_authority, extending that central
  boundary with a class-member initialization argument. Transfer children before
  publication; register a class with nonempty members even when it has no methods.
  No separate object identity allocator is introduced.
- [ ] _class_member_obligations consults every current authority alternative,
  selects only the requested name plus wildcard, and follows retained class
  carriers in opaque results. Missing retained-store provenance keeps the existing
  unresolved-authority obligation; never reconstruct cells from an old snapshot.
- [ ] Attribute evaluation at 20102-20176 attaches selected roots to the legacy
  result's helper_obligations. It does not promote that opaque member result into
  a precise callable, generator, scalar or descriptor. No blocker is emitted merely
  for installation, assignment to an alias, or attribute lookup.
- [ ] Forks share immutable records. The explicit constructor in AuthorityState.join
  at 14124 joins member tables as ordered may-unions and unions wildcards.
  Missing/empty operands cannot erase another operand's roots. Object alternatives
  retain their separate authority refs; no first-owner-only selection.
- [ ] Preserve roots across descriptor rewrites, helper proof stripping/rejoining,
  raw state adoption, return/carrier transport and retained-store fallback.
  Existing object/cell ownership and caller observed/results remain unchanged.

Association and lifetime rules:

| Boundary | Rule |
| --- | --- |
| Normal class end | Retain final reached local may-roots on the installed class only. |
| Raised class exit | Do not install a class or its member table; project existing outer effects. |
| Unrelated known attribute | Do not attach another named member's roots. |
| Unknown selection | Keep all matching roots; wildcard only when association is lost. |
| Class-body overwrite/delete | Final namespace decides; extracted aliases retain roots. |
| Post-install mutation | Retain old/incoming roots and existing guards; no new precise heap. |
| Existing descriptor/protocol edits | Keep behavior and unrelated carried obligations. |
| Class rebinding/deletion | Detach the name; aliases keep the record; no global cleanup. |
| Inheritance | Keep base named may-roots; no new MRO or shadow precision. |

No new strong post-install overwrite/delete precision is proposed without an
existing admitted clean contract requiring it. In particular, do not invent
general setattr, delattr, __dict__, metaclass or descriptor behavior to discharge
this plan. Where dispatch already refuses, keep that refusal and retain roots.
Where an opaque mutation loses the association, later unsupported consumption
must refuse rather than silently lose it. Dormant construction remains dormant.

## Task 3: deferred-obligation survival and reached consumers

Retaining a generator inside helper_obligations alone is insufficient in v23.
The current kind gate at 18204 excludes opaque and merged-container carriers;
the helper-authority walkers at 18837 and 19298 also do not recognize this marker.

Proposed private APIs:

    _retained_deferred_values(value, values) -> tuple[_FlowValue, ...]
    _class_generator_requires_refusal(state) -> bool
    _retain_deferred_result_roots(owner, replacement, values) -> _FlowValue

The first is a metered, cycle-safe graph walk over the supplied result, unkeyed
helper_obligations, current authority records/retained edges, and existing
sequence/mapping/merged/starred wrappers. It preserves all alternatives.
It does NOT open a class's unread named-member table. Member selection is the
only route from that table to a result's unkeyed obligations.

- [ ] Before an existing reached iterator-consumption/unknown-escape boundary
  accepts an opaque result, inspect its retained deferred roots. Extend actual
  consumer dispatch, not _flow_is_sensitive into a construction-time poison bit.
  A present marker is not automatically a refusal: use its remaining/epoch state.
- [ ] Cover full tuple/list, direct and merged next, generator method consumption,
  starred expansion, yield-from, membership, destructuring, for/async-for and
  comprehension iterator boundaries. Preserve existing invalid arity and exact
  local-generator completion/exception behavior. Mere construction, storage,
  lookup and iterator acquisition must not be reclassified as body execution.
- [ ] Opaque unsupported consumption records an explicit blocker, with existing
  conservative normal/exception handling; it does not execute the deferred body
  under class locals or a consuming helper's unrelated bindings.
- [ ] Keep ordinary helper ownership and negative deferred roots distinct.
  An imported/global read or unproved placeholder does not acquire blanket
  helper_refusal merely because it lacks lexical destination proof.

Single marker predicate, used by both sensitivity and direct consumption:

    state.class_scope_unresolved and (
        state.remaining != 0 or _deferred_generator_outer_iterator_changed(state)
    )

Compute the epoch-change fact before the empty-state early return at 18395.
Only proved empty/unchanged is dormant; no inference from equal values or private
numeric IDs is permitted. Missing carrier/store provenance remains conservative.
Do not add a new cross-call epoch-precision model or recover an unproved lexical view.

Merge/copy invariant: every possible marked state remains represented until
existing semantics prove it unreachable or empty/unchanged. Negative evidence
cannot disappear when value precision is lost.

- [ ] In _merge_legacy_flow_values at 13742-13819, flatten direct and already
  merged generator alternatives before joining; retain non-generator/wrapped
  alternatives rather than retaining only the newest direct generators.
- [ ] Same-identity merge explicitly ORs class_scope_unresolved. Preserve existing
  remaining, supported and iterator-identity/version conservatism.
- [ ] _record_deferred_generator_consumption must handle the existing
  deferred_generator_container_merged wrapper and selected opaque obligations.
  Do not serially execute mutually exclusive alternatives or invent correlations.
- [ ] Check replace/copy, transfer, class installation, native retention and
  extraction against the same invariant, including proof stripping.

Native shape-loss obligation, still not an additional reproduced RED:
_poison_mutable_collection at 18162 and result recovery at 19735/19329 must not
discard marked roots. _retain_deferred_result_roots attaches them before losing
shape and keeps them in the existing retained channel. A shape-invalidated owner
must not regain exact pre-mutation contents from its authority record merely
because a retained root exists. Its extraction remains opaque with all may-roots.
Exact existing append/insert/extend/pop/clear authority paths retain their existing
contracts; this plan adds no precise reverse, sort, unknown index or unknown
mutation semantics. Do not globally invalidate the established exact native
helper path while repairing marker-only opaque results.

## Task 4: actual comprehension target bindings

At 15579-15587, allocate implicit locals only for actual bound Name targets.
Use the existing bound-target semantics (Name, destructuring, Starred); attribute
receivers and subscript receiver/index expressions remain Load expressions.
Do not blindly walk all Names under a target. Charge actual traversal/allocation.

Preserve first-iterable evaluation in the class frame, eager body/target execution
in the enclosing nonclass view with current cells, shared effect/exception
projection, ordinary nonclass comprehensions and all original caps. This is not
new descriptor or target-evaluation precision.

## Frozen validation and release boundaries

| Requirement | Frozen evidence / next check |
| --- | --- |
| Factory/returned closure | C03 required-refuse; C04 permitted-refusal unchanged. |
| Class named member carrier | Existing Q05 required-refuse; Q06 permitted-refusal unchanged. |
| Target Load versus binding | R01/R03 refuse; R02/R04 clean. |
| Nested merge retention | R05 refuse; R06 permitted-refusal. |
| Changed empty versus dormant iterator | R07 refuse; R08 clean. |
| Preserved semantic scope | Original10 + C12 + Name8 + Q6, all 36 fixed expectations each slot. |
| Native shape loss | Static obligation only; no extra RED or private-ID test claimed. |

- [ ] Root reviews this plan and retains the R01-R08 RED run/replication before
  implementation. An unexpected clean result is investigated against its fixed
  public witness; no expectation changes or weaker permitted-refusal labels.
- [ ] After explicit authorization, author only a new T v25 source from pinned v23,
  exact v23 delta, allowed-node/storage/cap preservation report and touched-category
  inventory. No v24 storage overlay is included.
- [ ] Root inspects issued source before any payload. Preserve all 34 passing
  requirements and fix both residuals on both real runtimes. R8 adds fixed
  4 refuse / 3 clean / 1 permitted, not a revised 36-case baseline.
- [ ] Reuse inspected finite floor-first controls: fresh D-local r010 snapshot,
  manifest, explicit source path+SHA and independent W watch, actual interpreter
  proof before import, snapshot cwd and PYTHONPATH=src, scrubbed seed0 env/Git,
  -B -P, 60-second direct watchdog, full failure custody and matching dev receipt.
  No broad/owner/guarded/GPU runs or author-side payload.
- [ ] Meter every added traversal, allocation, retained edge and join. No work,
  width, helper-depth, language-support or timeout cap increase; no quadratic
  unmetered rescans hidden behind the new carrier fields.

The final implementation review must name any remaining unsupported consumed
path explicitly. Passing the finite cases would not establish general class heap,
descriptor, metaclass, TryStar, global-write precision, deferred execution precision
or recovery of correlations the existing flow merge has already discarded.
