# V25 semantic scope addendum v3: reserve negative class ownership

Engineering proposal for root review; no payload or reservation implementation.
Author: codex/mapping_compatibility. This is not a cold review.

Base v23: 53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499.
Plan v1: 39807c39a14e6f2009ffa69f5f09604c8354c1043a09be6c63e5982412621c2d.
Normative v2: e2ed7f88a6c081be3ec54556e47a327ce1ea2d336e55200e788857cfec099bb8.

Root identified a real conflict during authorized T-only authoring: an installed
class with an empty initial member bundle has no record, so a later store cannot
be transported through old direct, contained and captured aliases. Updating
visible names after that store would not cover the alias graph. This addendum
replaces v2's empty-bundle fast-path assumption for enabled normal class creation.
It preserves the 44 frozen expectations, dormant-body rule, existing caps,
storage algorithms and all positive class/descriptor/metaclass limits.

## Enabled normal construction

Proposed internal changes:

- Add reserve_class_owner=False to _transfer_authority. Only normal enabled
  _finish_class_definition/_with_class_member_authority requests True.
- Add class_member_owner: bool=False to the existing immutable _AuthorityRecord.
  This is a negative-transport owner tag, not a member-existence, class-value,
  lexical-cell, callable, MRO or descriptor proof.
- Reserve the ordinary existing-store object identity before binding/returning
  the new class even if both member tuples are empty. Use store.identity() and
  the existing COW object map; no second allocator, index, global cache or heap.
- Initialization and reservation run before the live-reference shortcut. Existing
  live records retain their ID and receive the tag plus ordered member may-union.
  A new class gets one record. Decorated unresolved classes retain their existing
  reached decorator refusal; the tag does not discharge that refusal.
- Same-ID AuthorityState.join OR-retains the owner tag and explicitly joins the
  named/wildcard roots. Identity-only record comparisons remain as in v2.
  Missing IDs retain unresolved-store evidence; they are not allocated as a new
  copy of the old object.

Every alias created after this boundary already carries the same authority ref:
a name assignment, sequence/mapping element, callable capture/default, helper
return and historical projection retain that ref. Current-state lookup resolves
the record through the active successor, so a later store reaches each live
alias without scanning names or replacing their values. Forked historical states
keep their prior COW record. No exact private ID becomes a public assertion.

## Later stores and member selection

Add a bounded _class_member_owner_ids(owner, values) helper for writes. It walks
only immediate owner alternatives, their current authority records and retained
result-alternative carriers, with separate role-aware value/authority visited
sets. It must not open ordinary container elements or callable captures as though
they were the receiver. In particular, writing an attribute of a container does
not mutate a class merely contained inside it. An instance is not silently
identified with its class for stores; existing instance/descriptor dispatch
limits remain conservative.

For each reachable tagged owner, _retain_class_member_write preserves old roots
and adds the supplied root under the known member name, or the wildcard when
selection is unknown. Empty initial bundles no longer skip this update.
These remain ordered may-unions: no new precise overwrite/delete or member-value
model. Existing namespace/reflective guards still run. A known unrelated member
does not acquire another member's roots; unknown selection keeps may-alternatives.

Read selection consults current tagged records, including selected opaque owner
alternatives. It exports matching named roots plus wildcard as result alternatives.
It does not expose unread names. Installation, storing, aliasing and lookup do
not execute a retained generator body and add no new refusal merely because it
is dormant. Actual iteration/unknown escape uses v2's separate role-aware consumer:
list((pending,)) still iterates only the outer tuple; later consuming pending
must see the stored obligation. Extracted aliases keep their own retained edge.

Added work is charged to the existing operation budget: owner allocation/tagged
record and returned wrapper, actual map COW, every visited edge/ref/attempt, ordered
dedup and copied tuple entries. Different-but-equal records can cost extra writes;
this cost remains visible under unchanged caps. No new work epoch is introduced.

## Disabled and unresolved-origin boundary: explicit decision needed

Disabled prepass remains disabled: no reserve flag, no class store, no body
execution to obtain identity. It may produce an implicit_class projection through
_source_ordered_helper_return (v23:24475 onward). Enabled actual class-factory
activation now supplies its real return authority, but that observation does not
prove that every disabled-origin/imported entry has a live record.

Source inspection does NOT establish an existing universal refusal for ordinary
Bare.pending storage on an unregistered class. _helper_namespace_store
(v23:19028 onward) refuses reflective writes, proof-known protected/registered
members, and active unresolved owners whose member name is in the registry.
Those conditions do not cover every ordinary member name. It would be inaccurate
to label this boundary already refused.

Proposed bounded fallback, awaiting root disposition: when an enabled reached
namespace store would add new retained callable/deferred may-roots to a class
whose ownership cannot be resolved completely, emit the existing unsupported
namespace-store refusal category instead of inventing a fresh alias identity.
This is an explicitly new application of that category to unresolved origin,
not a claim that the old guard already covered it. Enabled classes with reserved
owners keep dormant stores unrefused. Missing/mixed owner alternatives cannot be
discarded merely because another alternative has a tagged record.

No reservation change is implemented by this document. Root must accept or
refine the unresolved-origin fallback before that portion is authored. The
independent alias/later-store witness family is being authored separately;
no result-driven expectation changes or payload execution occurred here.
