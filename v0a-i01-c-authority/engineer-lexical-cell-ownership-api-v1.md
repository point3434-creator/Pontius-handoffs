# Lexical cell ownership API v1

Status: bounded engineering design and source inspection only. This is not a cold
review, an implementation lease, an executed result, or approval of a replacement.
No candidate, fixture, oracle, or diagnostic payload was imported or executed for
this note. No source/test/generated file changed. This note records the proposal
accepted in principle by the coordinator, with the requested key-consumer audit.
The class-frame author owns the combined class-successor plan; this note supplies
its single capture-ownership representation and guard interface.

## Pinned inputs and scope

All source anchors below refer to retained
D:/Pontius-handoffs/v0a-i01-c-authority/engineer-generator-v22.py,
SHA-256 61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3.
This source was rehashed during this inspection. The source is the retained
candidate, not an assumption about mutable W.

Other rehashed inputs under D:/Pontius-handoffs/v0a-i01-c-authority:

| Input | SHA-256 |
| --- | --- |
| stage0-design.md | 78bebca5279bf81e30181787f962d40c73826259d0bb3ffb1c7804804c1211e8 |
| engineer-class-composition-findings-repair-proposal-v1.md | 6bc11ee035a6388d73b954d1c5e9b6cd24e8815452fc56bb58197d4ae1b6c143 |
| engineer-class-proposal-challenge-v1.md | 14c406145d6eac98529a58c818987afc75f0bbfbc2c4521cc5708281ef6a09d4 |
| engineer-class-semantic-schedules-v2.md | 6f3c8c917f896cc1ffa352b054d4aeee73cb4a4dde85657c9da97a8996363913 |
| tests-checks/class-semantic-extension-cases-v1.json | 925ae5b9354377a5957f0c32c8bf5b58fea01612498b835abd6392f9cc87d268 |

The older proposal/challenge contain v19 anchors; this note independently maps the
relevant paths to exact v22. It changes none of the fixed twelve case schedules,
their separately authored oracles, or their 6-clean/5-refuse/1-permitted labels.
It does not add general module/global precision, an absent-global assumption,
general async/exception semantics, or a full class-flow rewrite. Existing budgets,
ordering, no-work transfer certificate, raw projection rules, and alternative-cell
weak writes remain requirements.

## One representation, using the existing stores

Introduce one private immutable, hashable, non-orderable lexical-origin key:
_LexicalCellId with one serial field. Use the existing per-analysis identity
counter to supply that serial. Its equality is lexical-token/serial equality;
it is not an int subclass and must not compare equal to a plain int carrying the
same serial. A descriptive _CellIdentity alias is int | _LexicalCellId.

Only actual local-cell allocation in _ExecutionState.__init__(local_names),
v22:14707-14708, may mint this token. The existing .cell(name) fallback at
14764-14770 continues to mint an unproved plain-int cell identity. A placeholder
does not become lexical because its value later becomes known, contains helper
provenance, is written/deleted, or is placed in a callable capture tuple.

Carry the exact key through the existing three structures:
ExecutionState.bindings[name], AuthorityRecord.cells, and AuthorityState.cells.
No new per-state ownership map, origin registry, or cell-value wrapper is needed.
Do not reconstruct tokens during fork, adoption, join, or closure forwarding.
No change is proposed to object authority_refs, AST result/observation IDs,
filesystem identities, or mutable-collection identities; those remain ints.

Token factory metering is explicit: retain the existing identity() consume and
serial increment, and additionally charge the one token allocation and one
retained serial-field reference. These two new units must be charged before
publishing a token into bindings; the existing binding/map operations retain
their current charges. A failed allocation/charge does not publish a partial
binding, refund work, reset counters, or increase a cap. No lexical tokens are
allocated by the helper-disabled path. Forks retain keys and pay only their
actual existing copy/reference work, rather than charging fresh token creation.
The serial remains scoped to the existing analysis-budget identity domain;
this proposal supplies no permission to mix unrelated analysis domains.

## Ownership requires the route as well as the token

A token proves that a lexical activation allocated a cell. It does not prove that
the current callee is entitled to use a same-spelled caller binding.

Call-environment construction must install incoming binding tuples only from the
invoked callable's retained capture records. Its subsequent constructor installs
fresh cells for the callee's own local_names. The current _call_environment
15133 forks all caller bindings and then overwrites recorded names at 15143;
that inherited remainder cannot establish the new ownership proof.

Name projections and cell bindings have different roles. Preserve required
legacy name/global projections separately, but do not leave unrelated caller
binding tuples available as a fallback for a missing callee capture. This rule
also applies when the registered-helper environment at 18595-18629 is built:
defining-module seeding must not acquire proof through the parent's unrelated
local binding table. Global behavior stays conservative.

This routing invariant provides owned-here versus forwarded evidence without
another field/map: constructor local_names allocated owned-here cells; every
other lexical token in a callee binding view arrived through that callable's
recorded captures. Nonlocal capture lookup reads the immediate nonclass
activation's binding view. A class frame can skip its own namespace to its
declared enclosing nonclass activation; a nested function may not search an
older ancestor or incidental caller to repair an omitted forwarded capture.

Therefore C03 remains discriminating. A factory must itself capture the
grandparent name required by its nested setter. If that requirement was omitted,
the factory call has no incoming binding for it, and the setter cannot mint a
proved destination. Keeping class_values.bindings reset at 23715 is intentional;
retaining outer bindings there would hide the missing-forwarding problem.

## Shared API and capture-scope retention

The common interfaces are conceptual names for the combined plan, not source
authored by this note:

- _captured_bindings(callable_value, live_state) obtains per-alternative capture
  entries and their completeness/refusal evidence, validates them before
  flattening, and supplies the callee binding view.
- _proved_nonlocal_destination(name, scope, binding_view, live_state) grants guard
  relief only for a name declared nonlocal by that callable's own scope, not
  global, with a nonempty destination tuple whose every element is a lexical
  token present in the live authority cell store.

The cell can contain unbound or maybe-unbound: destination existence and current
value are separate questions. Existing read/delete exception semantics still
decide whether the operation completes. Never infer origin from a value's kind,
reason text, helper identity, or tuple membership alone.

Reuse _FlowValue.callable_scope (9033), currently set to None at construction
18332, to retain the construction-time _LexicalBindingScope in each authority
record's value. This is the record's capture_scope input to the proof; it is not
itself a capture-completeness certificate. Reuse the existing scope traversal
work and immutable scope object where available. Do not add a full AST walk at
each guard/write or a scope store map. Current resolver.lexical_scope remains the
own-scope input inside the callee.

Validate every represented callable alternative before unioning its destinations.
An absent record, unknown/conflicting scope, absent required entry, an unproved
placeholder, or an absent retained cell cannot be omitted so that the remaining
tuple appears proved. Preserve the unproved alternatives or explicit dormant
unresolved-capture obligations through the existing helper_refusal /
helper_obligations mechanism. An incomplete call may explicitly refuse when
consumed; merely constructing or retaining a dormant callable must not produce
an immediate blanket blocker.

There is no _AuthorityRecord.join method in v22. The relevant record reconstruction
is _AuthorityState.join at 14018-14022. Its present ordered tuple union preserves
keys but can erase the distinction between an empty/missing capture on one
operand and a complete capture on another if completeness is checked only after
the union. Validate per-operand record coverage against that operand's store
before union, and preserve negative evidence in the joined record. Compatible
scope requirements must be retained; None/conflict must not be reconstructed
from the surviving cell tuples or the definition AST just to grant relief.
If the combined implementation introduces a separate capture_scope field instead
of the existing callable_scope field, this positional record constructor must
explicitly preserve/merge it; silently taking a default is unacceptable.

_merge_flow_values at 13467-13469 already retains callable_scope only when its
inputs preserve the relevant shared scope (its equality fast path also applies),
and helper_refusal is retained if any input has one at 13487-13488. Do not replace
these conservative outcomes with first-present scope or a union that treats
missing proof as success. Same-object record joins and distinct callable
authority_refs both need this rule. A scope field alone is insufficient to
represent a failed capture; keep the failed capture/obligation too.

## Capture construction and live contents

Replace the current load-only _callable_free_names traversal (18287-18304) with
the bounded lexical requirement computation in the combined plan. It must include
own nonlocal Store/Del destinations and transitive nested requirements, stopping
when an intermediate function supplies a local cell. It must respect scope
boundaries rather than collecting every descendant Store/Del or global name.
Unsupported lexical categories retain conservative behavior. Every new visited
node/entry is metered, and dormant function bodies are not repeatedly expanded
merely to rediscover the same capture requirement.

At _with_callable_authority (18328-18342), the enclosing binding skeleton selects
cell IDs; the current successor authority supplies already-existing contents.
The unconditional copy from the old enclosing authority at 18339 must not
overwrite a cell changed by an earlier class-body action. Missing retained
lexical authority stays unresolved; absence is not permission to restore an
entry-time value. A genuinely new placeholder is created only in the current
state from the proper current lexical projection, remains unproved, and does
not mutate a historical skeleton. Defaults/decorators continue to use the
source-point class namespace, separately from method-body free-cell ownership.

Fork/adoption/join retain the key. Helper completion and class exit raw-hydrate
the correct outward name view from current cells; they do not replay semantic
assignment/transfer while projecting. The recursive _review_body entry at
26037-26041 needs the same capture-resolved view of its exact recorded historical
call state, not a fresh ambient caller state or a projection that discards capture
provenance. The class-frame plan owns namespace shadowing and successor
projection, including any class-local fallback reads; the token does not solve
those separate concerns.

## Guard integration and unchanged writes

Use the same proof at all relevant seams:

| v22 seam | Required use |
| --- | --- |
| _snapshot_call, 16873-16876 | Check the callable record-derived capture view, not ambient caller bindings, before relieving namespace-effect refusal. |
| _assign Name path, 21458-21465 | A proved lexical Name rebind does not enter unresolved namespace-rebound tracking. Globals/unproved destinations keep the guard. |
| _delete_target Name path, 21818-21845 | The same ownership decision; retain existing unbound/NameError behavior and deletion value. |
| helper completion, 19169-19177 | Only unresolved namespace rebounds are poisoned/propagated. Proven lexical updates use live-cell raw hydration at 19162-19166. |

The Attribute/Subscript/reflection helper namespace guards at 18538-18570 remain
unchanged. Rebinding a proved lexical Name is not a permission to mutate the
retained helper object, class, descriptor, __dict__, defaults, or globals.

Keep _write_cells 14811-14815 and delete 14817-14825 strong for a singleton and
weak for alternative tuples. Do not select the first cell, collapse alternatives
by serial, reorder them, or silently omit unproved alternatives. The merge planner
at 22002-22008 continues to reject overlapping/missing cells for its existing
optimization; token keys do not widen that optimization.

## Systematic cell-key consumer audit

Method: source-wide text searches for .cells, .bindings, .authority, .cell(),
identity allocation, AuthorityRecord/AuthorityState/AuthorityMap, integer
annotations/type checks, ordering/casts/formatting, and serializers; all matching
cell-key contexts were read. Unrelated names were classified explicitly below.
This is static source inspection, not a token implementation or execution.

| Consumer/family in exact v22 | Key use and result |
| --- | --- |
| _AuthorityRecord.cells, 13857 | Immutable nested tuples. Record equality and tuple hashing/dedup require hash/equality, not integer operations. Widen its cell-key annotation. |
| _AuthorityMap, 13861-13916 | Any-key dict lookup, equality, set/delete, shallow dict copy, iteration/items/values, length and clear. No key ordering/casting/formatting. Token is suitable if immutable and hashable. |
| _AuthorityState.identity, 13985-13988 | The sole serial arithmetic is on next_authority_identity. Keep it on the raw int; wrap only the local-cell result. |
| _AuthorityState.fork, 13990-14005 | Forks maps or allocates disabled empty maps. Keys are retained unchanged; no numeric assumption. |
| _AuthorityState.join object records, 14011-14022 | Object IDs remain ints. Captured cell tuples use ordered dict.fromkeys and record replacement; token equality/hash suffice. Scope/completeness preservation requirements above are mandatory. |
| _AuthorityState.join cells, 14023-14029 | Iterates cell key/value pairs and performs keyed get/set. No sorting/arithmetic/int checks. Missing-operand completeness cannot be inferred from the resulting store alone. |
| _ExecutionState constructor, 14688-14725 | Forks binding map, allocates locals, and installs values. Names/local_order membership are string operations; only local allocation changes key kind. |
| _ExecutionState.cell, 14764-14770 | Reads/creates binding tuple and initializes the cell map. Fallback remains int/unproved; widen return annotation. |
| set/_write_cells, 14800-14815 | Tuple length selects strong versus weak write; keys only index maps. Widen _write_cells parameter annotation; behavior/order unchanged. |
| delete/pop/setdefault, 14817-14837 | Delete uses existing key tuples with map get/set; pop delegates deletion, setdefault delegates assignment. No numeric operations. |
| update/clear/copy, 14839-14874 | Adoption/fork carries bindings and authority; clear affects name history only. No key reconstruction. |
| _call_environment, 15131-15149 | Per-name ordered tuple dedup and cell-map get; f-string formats the capture NAME, not the cell key. Widen alternatives annotation and enforce capture-only routing/completeness. |
| _with_callable_authority, 18328-18342 | sorted(...) sorts free-name strings, not cell IDs. Cells are iterated, keyed, and retained in records. Change live-content import as specified; no key sorting. |
| _reachable_helper_authorities, 18345-18370 | Follows cells to _FlowValues by keyed get. seen/seen_authority here track value/object IDs, not cell keys; they remain int sets. |
| helper successor adoption/hydration, 19153-19166 | Forks current authority and looks up every retained binding key. No key conversion or ordering. |
| _merge_states binding union, 21972-21978 | Ordered dict.fromkeys tuple union; token equality/hash suffice. Do not reorder or omit cells. |
| _merge_states planner, 21989-22012 and 22040-22043 | Cell-key set membership and store presence checks, then existing writes. Widen binding_plan and seen annotations. No numeric sorting/arithmetic. |
| class namespace setup/completion, 23712-23738 | Replaces class binding map with empty map and adopts successor authority. No key conversion. Preserve separation; class-frame changes are separately planned. |
| _transfer_authority, 14034-14083 | Carries object authority_refs and creates object records, not lexical-cell keys. Its missing-ref obligation must stay intact. Object IDs remain ints. |
| FlowValue proof merge/stripping, 13424-13488 | Merges int object authority_refs and retains/clears callable_scope. It does not sort, stringify, or serialize captured cell keys. Scope/negative-evidence rules above apply. |
| Output serialization, 372-381 and call sites; literal repr at 13389,26002,26142 | Canonical JSON/TOML/public row paths do not receive AuthorityState.cells or AuthorityRecord.cells. Literal repr handles modeled source values, not cell keys. No production cell-key serializer was found. No new serializer is required. |

The six integer annotations to widen are exactly:
AuthorityRecord.cells 13857; ExecutionState.cell 14764;
ExecutionState._write_cells 14811; _call_environment.alternatives 15134;
_merge_states.binding_plan 21989; _merge_states.seen 21992.
The generic AuthorityMap already accepts Any keys.

Classified exclusions from the same searches:
- exception-classifier self.bindings at 10384-12334 holds string alias markers;
- deferred-generator state.bindings at 13235 and 17392 holds name/_FlowValue pairs;
- ObservedAuthorityMap int keys at 13928/13954 and results keys are AST identities;
- FlowValue.authority_refs 9037 and reachable-helper object-ID sets remain ints;
- source/name-store keys are strings; filesystem/process/governance identity
  tuples earlier in the file are unrelated and must not be widened.

Result: no runtime int-only sorting, formatting, arithmetic, serializer, or
type-check consumer of lexical-cell keys was found in exact v22. The existing
consumers accept opaque hashable keys, subject to the six annotation changes,
factory isolation/metering, and the semantic provenance constraints above.
This statement does not certify future external diagnostic serialization or
unreviewed replacement code. New instrumentation must count keys opaquely and
must not cast or sort mixed cell-key types.

## Handoff and limits

The mapping/class-frame author has been sent the same single-token/single-binding
view design and the per-operand join warning. Its final combined plan should
reference this note's issued hash and spell out the class-frame namespace/successor
API around it, without introducing a second ownership store. Source implementation
and payload dispatch remain coordinator decisions.

This audit supports the representation's compatibility with current consumers.
It does not prove capture discovery, class shadowing, source-point effects,
exception successor projection, recursive review, or corpus-budget acceptance.
The fixed twelve cases and prior frozen public/old suites retain their original
roles and expectations. No cap, message, assertion, or optional-precision label
is relaxed by this note.
