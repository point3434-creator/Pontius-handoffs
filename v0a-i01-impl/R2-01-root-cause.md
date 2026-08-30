# Root-cause note — R2-01 policy authority, before any fourth fix attempt

Author: Claude, 2026-08-30. Required by `docs/workflow.md` (second residual on
one contract: r001 F3 → r002 R2-01 → r003 R3-01). No source has been edited;
this note is the precondition for the next attempt, not the attempt.

**Design verdict: WRONG SHAPE.** The fix I had planned — exact-type admission —
is independently verified below to be insufficient. Shipping it would have been
this contract's fourth failure.

## 1. Why r002 and r003 are one error

Both attempts authenticated the *messenger* and inferred the *message*.

r002 cross-examined the returned `BlueprintSelection`: `source_digest` against a
digest bound at hand start, `key` against a key recomputed from the runtime's own
state, and, on a claimed miss, the action against `passive_blueprint_action`.
Every comparison except the recomputed key weighs two values that both derive
from the same untrusted object, so a self-consistent liar passes. A claimed
*hit* was never constrained at all, because the runtime had no independent
referent for "what the table holds".

r003 replaced output cross-examination with provenance:
`isinstance(blueprint, ImmutableBlueprintActionSource)` plus calling the sealed
unbound `ImmutableBlueprintActionSource.action_for(source, ...)` so an override
could not intercept. That moved the trust exactly one hop — to the attributes
the sealed body reads off `self`, namely `self.entries` and `self.digest`.

The shared error: **a type tag was treated as proof of construction.** The only
code that establishes this type's invariants is
`ImmutableBlueprintActionSource.__post_init__` (`immutable_blueprint.py:312-321`).
Nothing downstream re-establishes them, and both fixes assumed that possessing
the type implies that constructor ran. It does not. Both fixes were also pinned
to the shape of the previous escape — and so were their regression tests, which
is why the same contract has failed three times in the same direction.

## 2. The complete influence boundary

An accepted policy object reaches the runtime's beliefs through five channels;
nothing else about it is ever read.

| # | Channel | Status | Closed by exact type? |
| --- | --- | --- | --- |
| C1 | Type identity — `isinstance` falling back to a `__class__` property, foreign object entirely | CONFIRMED | **Yes** — `type(x) is T` reads `ob_type` and cannot be faked |
| C2 | Attribute resolution — MRO shadowing of `digest`/`canonical_bytes`, a property over a slot, `__getattribute__` | CONFIRMED (this is the r003 escape) | **Yes** — all require a subclass in the MRO |
| C3 | Slot *contents* on a genuine exact-type object — `T.__new__(T)` + `object.__setattr__`, or a `__post_init__`-skipping subclass then `__class__` swap | **CONFIRMED by me, below** | **No** |
| C4 | Behaviour of objects *inside* a validly constructed table — an entry whose key is an ordinary `BlueprintDecisionKey` subclass with `__eq__` returning `True` | **CONFIRMED by me, below** | **No** |
| C5 | Mutation timing — the admitted object's `entries` slot rebound after admission via `object.__setattr__` | STATIC (mechanism confirmed, not driven end to end) | **No** |

### My own verification

Receipt: `R2-01-verification.txt` in this packet, run against the r003 worktree
source. Two claims, both reproduced:

**C4 needs no bypass whatsoever.** A `WildcardKey(BlueprintDecisionKey)` whose
`__eq__` returns `True`, built with the real key's own field values, is accepted
by `BlueprintActionEntry.__post_init__` and
`ImmutableBlueprintActionSource.__post_init__` because both validate with
`isinstance` (`immutable_blueprint.py:260`, `:317`). The result is a genuine,
exact-type, publicly constructed source. `type(forged) is
ImmutableBlueprintActionSource` is `True`, and the sealed `action_for` returns
`table_hit=True` with `raise-to-6`. Exact-type admission accepts this object,
and the sealed lookup itself does the lying.

**C3 works by two independent routes.** `P.__new__(P)` followed by
`object.__setattr__` yields `type(bare) is P` with `__post_init__` never having
run, and the sealed `action_for` returns `table_hit=True, raise-to-6` on it.
Separately, a `__slots__ = ()` subclass that overrides `__post_init__` to do
nothing, then has `__class__` reassigned to the sealed type, also satisfies
`type(x) is P`. A fix aimed only at `__class__` reassignment leaves the other
route open.

One correction to the audit's framing, from my run: the forged source's digest
is *not* equal to an honest empty table's digest, because the entry does appear
in `canonical_bytes`. The r002 digest check fails to catch it only because the
bound digest is taken from the attacker-supplied object itself — the check is
self-referential, not weak.

## 3. What survives, and what is actually required

Exact-type admission kills C1 and C2 — the whole subclass and duck-type family,
including the r003 escape. It is worth keeping as a cheap outer gate. It does
not touch C3, C4 or C5, and **C4 is reachable through nothing but the sealed
public constructor**, so the contract would remain open.

The reviewers' stated fallback — "normalize into an exact validated immutable
source" — is also insufficient as written: reconstruction re-runs the same
`isinstance` checks, and `BlueprintActionEntry` and `BlueprintDecisionKey` are
themselves frozen slots dataclasses, so a poisoned key survives a full rebuild
and still compares equal to every real key.

`immutable_blueprint.py` is sealed under Iron rule 1. The entire fix must live
at the v0a boundary and must treat the sealed type's own construction-time
validation as untrustworthy for adversarial contents.

What the next attempt must do, once, at admission:

1. **Read slots unmediated** — `T.__dict__['entries'].__get__(x, T)`, never
   attribute access, and never `T.canonical_bytes(x)`, whose body re-enters
   `self.entries`.
2. **Validate contents to exact types, one level down** — `type(entry) is
   BlueprintActionEntry`, `type(entry.key) is BlueprintDecisionKey`,
   `type(entry.action) is BettingAction`, and `type(v) is int` / `is tuple` on
   the key's scalar fields. This is Iron rule 7 applied where it currently stops.
3. **Match by digest, never by `==`** — build `{entry.key.digest: entry.action}`
   at admission and look up the recomputed key's digest per action. A lying
   `__eq__` becomes inert because equality is never consulted; `json` serialises
   `int`/`tuple` subclasses by their underlying values, so the digest stays
   honest even when comparison does not.
4. **Own the storage** — use that snapshot for the digest binding, the lookup,
   and the classifier at `runtime.py:113-130`, and never read the caller's
   object again. This is what closes C5.

Cost is O(table) once at admission and O(1) per action. The sealed `action_for`
already rehashes the whole table on every call, so this is strictly cheaper than
today and satisfies the reviewers' "no second full-table rehash per action".

Note this changes the shape rather than adding a gate: the runtime stops asking
"is this object trustworthy?" and starts extracting facts it can verify, then
never consulting the source again. That is why the verdict is WRONG SHAPE and
not STRAINED.

## 4. The principle, and how to test the class rather than the example

**Never accept a fact about a value from the value itself. Reconstruct the fact
from unmediated bytes at the boundary, freeze the reconstruction, and use only
the frozen copy.** Type is provenance; invariants are content; a boundary must
establish both.

Four properties test the class, each writable without knowing the next escape:

- **Content, not provenance** — any object presented at admission, whatever its
  type, yields the same accept/reject decision as a freshly built source
  constructed from its unmediated slot bytes.
- **Answer traceability** — for every delivered action recorded as
  `table_hit`, an entry exists in the admission snapshot whose key digest equals
  the digest of the independently recomputed decision key, and whose action is
  byte-identical to the delivered one.
- **No untrusted `__eq__` on an evidence path** — no comparison in the selection
  path compares an attacker-supplied object with `==` or `!=`.
- **Post-admission immutability** — mutate the caller's object by every
  available route after admission; the delivered action is unchanged.

Answer traceability is the one that would have caught r002, r003, and every
vector in the table above.

## 5. Residual risk and open questions

Known residuals after the fix in §3: the exact-type field validation duplicates a
schema that lives in a sealed file and can drift out of sync, so digest-keyed
matching should be treated as the load-bearing half; and
`getattr(..., None)`/`getattr(..., ())` at `runtime.py:462` and `:120` turn a
raising property into a default, which currently fails closed by luck rather
than design.

Undetermined here, and worth its own work: whether the same `__post_init__`-skip
and `isinstance`-validation pattern defeats the **other frozen slots dataclasses
crossing the v0a boundary** — mailbox receipts, events, spine tickets — none of
which were audited; and whether any sealed consumer elsewhere already depends on
the `isinstance`-level laxity in `immutable_blueprint.py`, which would make
tightening at the v0a boundary a behavioural divergence worth recording.

I have not assessed whether the host is a genuine adversary in the deployed
configuration. The fix is justified regardless, because ADR-0485 states the
boundary as a contract, and a contract that only holds against cooperative
callers is not a boundary.
