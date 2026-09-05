from __future__ import annotations

import json
from pathlib import Path

from pontius.blueprint_artifact.codec import (
    BlueprintArtifactError,
    decode_blueprint,
    encode_blueprint,
)
from pontius.immutable_blueprint import (
    BlueprintActionEntry,
    BlueprintDecisionKey,
    ImmutableBlueprintActionSource,
)
from pontius.no_limit_betting import BettingAction, BettingActionKind, BettingStreet


fixture = Path("tests/fixtures/blueprint_artifact/raise_control.json").read_bytes()
fixture_document = json.loads(fixture)


def encoded(document: object) -> bytes:
    return json.dumps(document, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def refused(document: object) -> None:
    refused_raw(encoded(document))


def refused_raw(raw: bytes) -> None:
    try:
        decode_blueprint(raw)
    except BlueprintArtifactError:
        return
    raise AssertionError("decoder admitted a malformed focused probe")


for kind, raise_to in (("fold", None), ("check", None), ("call", None), ("raise", 6)):
    document = json.loads(fixture)
    document["entries"][0]["action"] = {"kind": kind, "raise_to": raise_to}
    source = decode_blueprint(encoded(document))
    assert source.entries[0].action.kind.value == kind
    assert source.entries[0].action.raise_to == raise_to
    assert decode_blueprint(encode_blueprint(source)).digest == source.digest

for mutation in ("missing", "unknown"):
    document = json.loads(fixture)
    action = document["entries"][0]["action"]
    if mutation == "missing":
        del action["raise_to"]
    else:
        action["unknown"] = None
    refused(document)

history_raw = Path("tests/fixtures/blueprint_artifact/history_control.json").read_bytes()
for column, bad in ((0, "bad-street"), (2, "bad-kind"), (3, 1), (5, 1), (6, 2), (7, 3)):
    document = json.loads(history_raw)
    document["entries"][0]["key"]["public_history"][0][column] = bad
    refused(document)

maximum_text = "9" * 640
maximum = int(maximum_text)
for path in (
    ("entries", 0, "key", "stacks", 0),
    ("entries", 0, "key", "public_history", 2, 4),
    ("entries", 0, "action", "raise_to"),
):
    document = json.loads(history_raw if "public_history" in path else fixture)
    target = document
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = maximum
    admitted_raw = encoded(document)
    source = decode_blueprint(admitted_raw)
    assert decode_blueprint(encode_blueprint(source)).digest == source.digest
    over_limit = admitted_raw.replace(
        maximum_text.encode("ascii"), b"1" + b"0" * 640, 1
    )
    refused_raw(over_limit)

key = BlueprintDecisionKey(
    controlled_seat=3,
    private_hand=(1, 13),
    board=(),
    button=0,
    small_blind=1,
    big_blind=2,
    street=BettingStreet.PREFLOP,
    starting_stacks=(200,) * 6,
    stacks=(maximum, 199, 198, 200, 200, 200),
    total_contributions=(0, 1, 2, 0, 0, 0),
    street_contributions=(0, 1, 2, 0, 0, 0),
    folded=(False,) * 6,
    pending_seats=(3, 4, 5, 0, 1, 2),
    last_full_raise_size=2,
    acted_at_bet=(None,) * 6,
    public_history=(),
)
for kind, raise_to in (
    (BettingActionKind.FOLD, None),
    (BettingActionKind.CHECK, None),
    (BettingActionKind.CALL, None),
    (BettingActionKind.RAISE, maximum),
):
    source = ImmutableBlueprintActionSource(
        "review-a-exact-graph",
        (BlueprintActionEntry(key, BettingAction(kind, raise_to)),),
    )
    assert decode_blueprint(encode_blueprint(source)).digest == source.digest

print("focused codec edge probes PASS under configured decimal threshold")
