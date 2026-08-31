# Bounded v25 semantic successor plan v2

> For implementation after root authorization: use the executing-plans skill.
> Plan only. No source edit, candidate import or payload is authorized.

Author: codex/mapping_compatibility. Engineering design, not a cold review.

This immutable successor incorporates engineer-generator-v25-semantic-plan-v1.md,
SHA256 39807c39a14e6f2009ffa69f5f09604c8354c1043a09be6c63e5982412621c2d.
Its C03 diagnosis, construction inventory, class-frame limits and frozen
expectations remain binding. This document replaces the ambiguous iteration,
shape-loss, initialization and equality contracts in Tasks 2 and 3.
It is the normative clarification where the two documents differ.

Base remains engineer-generator-v23-semantic.py:
53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499
No v24/v26 storage source is an input to v25. W/main and all frozen packs stay
unchanged. No general class heap, descriptor/metaclass precision, new caps,
global-read refusal policy or deferred-body execution model is introduced.

## Updated evidence

All paths are under D:/Pontius-handoffs/v0a-i01-c-authority.

Root report coordinator-v26-r8-verification-v1.json:
181248855d1947c775d21728ed3ae5c2bb62b7deb15604154f88b95290e89bac
Only its R8 section is semantic evidence for this plan; its v26 storage section
is a different lane. R8 receipts are:
- tests-checks/class-comprehension-extension-v23-red01-311-receipt.json
  5c56ae9cc8a0c6a46be61e10ca7786505caa8173145878d18df0842ddc62add1
- tests-checks/class-comprehension-extension-v23-red01-314-receipt.json
  6df879fcdf435dda1ba5a234ab2f41eaf6f0358e028789985c5d68b11e1267e8

The root reports complete eight-Model/eight-analysis runs and equal case records
across slots. R01/R03/R05/R07 are wrong-clean in both; the other four satisfy
their unchanged labels. This author read and rehashed the report and checked
the receipts' retained v23 source pins, but did not rerun their snapshot audit
or any payload. R8 is now reproduced RED, not merely the unexecuted concern
described in plan v1. Native shape-loss remains a static obligation.

The 36 original expectations and R8's 4 refuse / 3 clean / 1 permitted labels
remain unchanged. Root's 34/36-per-slot report remains:
33a2257f5ec5ac31ec3f4b59342dc46e86bcab6451df1656ca7fd1931aa1d1a7
Source implementation still requires root's review and explicit authorization.

## 1. Retention edges and immediate iteration are different

_retained_deferred_values is only a retention/discovery walk. Its flattened
output MUST NOT serve directly as the list of generators executed by iteration.
The implementation must preserve the meaning of each retained edge.

Use a small immutable, identity-equal carrier in the existing obligation channel:

    @dataclass(frozen=True, slots=True, eq=False)
    class _DeferredResultCarrier:
        role: Literal["alternative", "element"]
        roots: tuple[_FlowValue, ...]

Represent it as a _FlowValue with kind="deferred_result_carrier" and this payload.
It grants no positive scalar, callable, class-member or iterable precision.
The existing helper_obligations and AuthorityRecord.retained channels hold
these carriers; no new heap or process-wide graph is introduced.

- "alternative": each root is a possible value of the immediate result.
- "element": each root is a possible contained/yielded element, not the current
  iterator object. Iterate the outer container without executing these roots.
- Class member tables remain named edges. They are not opened until the named
  member is selected. Selection creates an alternative edge to the actual
  retained member value, preserving any container wrapper around its children.
- Existing ordinary helper/capture obligations retain their old meaning.
  A helper that merely captures a generator is not itself that generator.

The consumer-facing helper is separate:

    _immediate_deferred_values(value, values) -> tuple[_FlowValue, ...]

It unwraps result alternatives, explicit merged-generator alternatives and
maybe-bound alternatives. It stops at ordinary known native containers.
For an element carrier, it forwards the roots when an element is produced;
it does not recursively consume them. A root that is itself a known container
is still a container even when reached through an alternative edge.

Required examples, without adding new clean language promises:

| Operation | Deferred action |
| --- | --- |
| list((pending,)) | Iterate tuple; forward pending as an element; do not run it. |
| for item in (pending,) | Bind item to pending; only a later use may consume it. |
| list(merged_generator_alternatives) | Inspect every possible immediate iterator. |
| tuple(opaque_selected_member) | Inspect selected result alternatives, not unread members. |
| known container subscript/pop result | Forward selected/may elements as result alternatives. |
| known container copy/list result | Keep element edges as element edges. |
| unknown escape that may consume | Preserve existing conservative escape policy and roots. |

If native construction returns an opaque container result, retain an element
carrier on that result rather than relabeling its nested generators as immediate
iterator alternatives. If extraction loses the index, all possible extracted
elements become result alternatives; no positive exact index is invented.

The same distinction applies to for/async-for, destructuring, comprehension
iteration, membership, starred expansion, tuple/list, next and generator methods.
Do not serially execute mutually exclusive alternatives. Do not globally expand
_flow_is_sensitive or a generic "contains generator" predicate to mean execution.

Known __iter__ / iterator acquisition only returns a carrier. Preserve the
existing unstarted-close exemptions, exact local-generator completion paths and
invalid-arity handling before any new reached-consumption refusal. An invalid
binding cannot execute a body. This adds no new close/throw precision for opaque
or mixed values. No blocker arises merely from constructing, storing or looking
up a dormant class/member/generator.

The existing class marker predicate remains:
class_scope_unresolved and (remaining != 0 or outer_iterator_changed).
Empty-and-unchanged stays dormant. Missing provenance is not an empty proof.

## 2. Shape loss changes the current authoritative record

Attaching roots to an unknown wrapper while leaving the old exact record usable
is forbidden. An ordinary callable may coexist with the marked generator, so
_has_callable_authority can still be true. Keep that predicate callable-only;
neither widening it nor adding a marker-only guard fixes stale exact recovery.

Refine the helper contracts:

    _invalidate_collection_result_shape(owner, values) -> None
    _current_exact_collection_value(owner, values) -> _FlowValue | None

Invalidation has this order:
1. Resolve the owner's current live authority alternatives in the current state.
2. Collect the current contained and already-retained may-roots with their roles.
   Use current records, not a stale projected owner to replace current contents.
3. Through the current state's existing COW object map, replace each affected
   record.value with shape-opaque unknown, preserving identity, native container
   kind, existing helper metadata and every retained root. Keep element edges
   as element edges. Sibling/historical maps and extracted aliases stay unchanged.
4. Update ordinary current projections using the same authority refs; keep the
   existing mutation-epoch recording and exception successor behavior.
5. Publish no partially constructed record if metering/refusal interrupts work.

_current_exact_collection_value reads current records only. Missing, invalidated,
mixed or incompatible current shapes return None; it never falls back to a stale
sequence/mapping projection. Exactness must hold for every retained alternative
used by the existing operation. This is not new multiple-owner precision.

Use that boundary at BOTH:
- _collection_authority_result's exact-result gate, v23:19342 onward;
- _evaluate's subscript recovery, v23:19735 onward.

Also check native exact element-store/retention callers against the same current
shape before applying a strong update. If shape is opaque, extraction is opaque
with all possible result roots. Known helper identity on another element cannot
restore the pre-mutation order. Existing conservative guards and exceptions stay.

Do not globally invalidate old exact native updates merely because the legacy
projection path calls _poison_mutable_collection afterward. Preserve that fact
explicitly and locally to the call:

    @dataclass(frozen=True, slots=True)
    class _NativeCollectionEffect:
        owner_refs: tuple[int, ...]
        mutable_identity: int | None
        shape_exact: bool

_retain_native_list_call returns this effect or None, replacing its old Boolean.
It issues shape_exact=True only after the existing validated exact native
retention operation completes on those live owners. A retained-only/opaque
fallback cannot issue that proof. _apply_helper_call_effects returns the effect
unchanged, extending its internal result union with this type.

The normal _evaluate_value call site distinguishes this call-local token from
a returned _FlowValue. Its later legacy projection poisoning may preserve current
record contents only when the token matches the same owners and denotes the
completed exact update. Otherwise authoritative shape invalidation occurs.
The two existing non-result callers (projection and decorator application) must
not publish the token as a helper return. No resolver-wide stale Boolean, AST-ID
cache, cross-call reuse or identity/value heuristic replaces this local fact.

Existing precise append/insert/extend/pop/clear behavior is preserved where its
original operation proves it. No new reverse/sort/unknown-index model is added.
The bounded correction retains obligations when that precision is unavailable.

## 3. Member initialization cannot vanish at transfer's early return

Plan v1 adds immutable member_obligations and member_wildcard fields to the
existing AuthorityRecord. Keep that representation and its may-only semantics.

Initialization is two explicit internal phases:
1. _with_class_member_authority gathers and transfers final reached member roots
   using the completed class frame, preserving the member/result/container roles.
2. Pass the completed member bundle to _transfer_authority. Its initialization
   branch runs BEFORE the existing live-authority-refs early return at 14156.
   It must either initialize the newly registered class record or preserve/merge
   the bundle into each existing live record through current-state COW.

An existing bundle may not be ignored just because authority_refs are live.
Missing refs preserve the existing unresolved-store obligation and the incoming
member bundle; they do not rehydrate old cells. Disabled authority/prepass remains
unchanged and does not execute dormant bodies to obtain a bundle.

The initialization operation is idempotent under exact retained-root identity,
not under source-line/kind matching. Construction with empty bundles remains the
old fast path. Ordinary transfer without initialization keeps the old fast path.
Normal class completion alone installs members; raised completion does not.

The rest of plan v1's bounded association policy is unchanged: final class-body
namespace handles local overwrite/delete; no new strong post-install class heap;
unknown mutations preserve named/wildcard may-roots and existing guards.
Unrelated named members do not acquire each other's obligations.

## 4. Ordered unions, comparison costs and cycle visits

Every new may-union preserves operand and edge order, keeps the first occurrence
of the SAME retained root, and retains distinct authority alternatives.
Dedup keys include FlowValue object identity and its authority-ref tuple.
Neither source location/kind, equal scalar contents nor authority tuple alone
can collapse distinct wrappers with different negative evidence.

Apply the same conservative ordered dedup to retained-edge unions at the touched
join, so repeatedly joining the same root does not multiply it. Do not sort by
private allocation identity, and make no exact-ID equality a public test contract.
Charge each visited operand, member, root, ref and allocation, including duplicate
checks and output copying. Shared unchanged records/bundles may stay shared.

Generated _AuthorityRecord equality would recursively traverse the added fields
at AuthorityState.join:14120 and AuthorityMap.__setitem__:13985. Avoid that new
implicit work with an AuthorityRecord-only identity fast path:
- Same record object: constant-cost unchanged path.
- Different record objects: explicitly merge/write and charge actual work.
- Non-record map values: retain the existing equality behavior.

Do not use generated record equality later as a supposedly free dedup check.
Different but equal records may cause extra merges/COW copies; this is a disclosed
cost risk to measure under unchanged caps, not a reason to hide work or add caps.
New carrier payloads use eq=False, so equality of an outer FlowValue cannot
silently descend their retained graphs. Explicit carrier operations own the walk.
Existing _merge_flow_values/other baseline equality is not claimed fully metered
by this bounded change; do not describe it as a whole-analyzer equality audit.

Graph traversal is iterative and scoped to one current state/operation:
- Track visited FlowValue objects and visited authority IDs separately.
- Immediate-iteration walks key visits by edge role too: visiting a value as an
  element must not suppress a later visit as an immediate alternative.
- Track carrier objects as needed; distinct generator-state objects sharing the
  same source identity remain distinct alternatives.
- Charge the edge/visit attempt before a seen-set shortcut.
- Never cache these visits across successor states, publication or mutation.
- Walks inspect retained data only; they neither execute callbacks nor publish
  generator consumption. No arbitrary callback purity/reentrancy is assumed.

## 5. Implementation checklist after root authorization

- [ ] Preserve plan v1's C03 construction flag and every deferred/binding/depth gate.
- [ ] Preserve the class/lexical/global-read/prepass and exceptional-exit limits.
- [ ] Implement role-preserving retention and immediate-iteration dispatch together.
- [ ] Implement current-record invalidation and both exact-recovery gates together.
- [ ] Connect call-local native exact-update tokens at all affected result callers.
- [ ] Initialize member bundles before live-ref transfer shortcuts.
- [ ] Use explicit ordered unions and AuthorityRecord identity fast paths.
- [ ] Preserve named edges, alternative edges and element edges through each copy.
- [ ] Inspect exact v23 delta and storage/cap/other-path preservation before payload.
- [ ] Root runs fixed36 plus R8 with unchanged floor-first controls and expectations.

No additional public case is invented by this clarification, and no existing
required-clean result is weakened to permitted refusal. The known-container
examples and mixed callable/marker stale-shape example are design falsifiers,
not claims of newly executed payloads. All prior source/evidence bytes remain
immutable. V25 authoring and dispatch remain separate root decisions.
