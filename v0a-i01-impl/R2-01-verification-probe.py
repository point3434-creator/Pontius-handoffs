"""Independently verify the audit's two load-bearing claims (read-only)."""

import sys

sys.path.insert(0, r"D:\Pontius-worktrees\v0a-increment-1\src")

from pontius.holdem_cards import OneSeatCardState
from pontius.immutable_blueprint import (
    BlueprintActionEntry,
    BlueprintDecisionKey,
    ImmutableBlueprintActionSource,
)
from pontius.no_limit_betting import NoLimitBettingState, raise_to

STACKS = (200,) * 6


def context():
    betting = NoLimitBettingState.new_hand(
        button=0, starting_stacks=STACKS, small_blind=1, big_blind=2
    )
    cards = OneSeatCardState.preflop(controlled_seat=3, private_hand=(0, 13))
    return cards, betting, betting.legal_decision()


print("=" * 72)
print("CLAIM C4: a lying key passes the SEALED PUBLIC CONSTRUCTOR")
print("=" * 72)

honest = ImmutableBlueprintActionSource(source_id="honest-empty")
cards, betting, decision = context()
real_key = BlueprintDecisionKey.from_state(cards=cards, betting=betting, decision=decision)


class WildcardKey(BlueprintDecisionKey):
    """An ordinary subclass. No monkeypatching, no __class__ swap."""

    def __eq__(self, other):
        return True

    def __hash__(self):
        return 0


poison = WildcardKey(**{f: getattr(real_key, f) for f in real_key.__dataclass_fields__})
entry = BlueprintActionEntry(key=poison, action=raise_to(6))
forged = ImmutableBlueprintActionSource(source_id="honest-empty", entries=(entry,))

print(f"  constructed via the sealed public constructor : {type(forged) is ImmutableBlueprintActionSource}")
print(f"  exact-type admission would ACCEPT it          : {type(forged) is ImmutableBlueprintActionSource}")
selection = ImmutableBlueprintActionSource.action_for(
    forged, cards=cards, betting=betting, decision=decision
)
print(f"  sealed action_for returns table_hit           : {selection.table_hit}")
print(f"  action delivered                              : {selection.action}")
print(f"  its digest == honest empty table's digest     : {forged.digest == honest.digest}")
print(f"  digest-keyed lookup would find it?            : "
      f"{poison.digest == real_key.digest}  <-- the proposed remedy's discriminator")

print()
print("=" * 72)
print("CLAIM C3: exact type without the constructor ever running")
print("=" * 72)

P = ImmutableBlueprintActionSource
bare = P.__new__(P)
object.__setattr__(bare, "source_id", "never-validated")
object.__setattr__(bare, "entries", (entry,))
print(f"  type(bare) is the sealed type                 : {type(bare) is P}")
print(f"  __post_init__ ever ran                        : False (bypassed via __new__)")
try:
    sel2 = P.action_for(bare, cards=cards, betting=betting, decision=decision)
    print(f"  sealed action_for on it -> table_hit          : {sel2.table_hit}, {sel2.action}")
except Exception as error:  # noqa: BLE001
    print(f"  sealed action_for raised                      : {type(error).__name__}: {error}")


class Skipping(P):
    __slots__ = ()

    def __post_init__(self):
        return None


swapped = Skipping(source_id="skipped", entries=(entry,))
object.__setattr__(swapped, "__class__", P)
print(f"  after __class__ swap, type() is sealed type   : {type(swapped) is P}")

print()
print("=" * 72)
print("CONSEQUENCE for the proposed fix")
print("=" * 72)
print("  exact-type admission closes C1/C2 (subclass + duck-type) .. yes")
print("  exact-type admission closes C4 (lying key inside)        .. NO")
print("  digest-keyed lookup distinguishes the lying key          .. "
      f"{poison.digest != real_key.digest or 'digests equal - see below'}")
