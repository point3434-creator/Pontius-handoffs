from __future__ import annotations

import hashlib
from pathlib import Path
import sys

from pontius.blueprint_artifact import codec
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
from pontius.no_limit_betting import BettingAction


def forge(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for name in value.__slots__:
        object.__setattr__(clone, name, changes.get(name, getattr(value, name)))
    return clone


def expect_missing(value: object, field_path: str) -> None:
    try:
        encode_blueprint(value)
    except BlueprintArtifactError as error:
        assert field_path in str(error)
        assert "missing required field" in str(error)
    else:
        raise AssertionError(f"missing {field_path} was admitted")


def main() -> None:
    assert sys.get_int_max_str_digits() == 640
    assert hashlib.sha256(Path(codec.__file__).read_bytes()).hexdigest() == (
        "72539c0b977b3fb46d6a25e44f5a9355b957978cd305bce7c56c5b5d3470fde2"
    )
    fixture = Path("tests/fixtures/blueprint_artifact/raise_control.json").read_bytes()
    source = decode_blueprint(fixture)
    entry = source.entries[0]
    expect_missing(object.__new__(ImmutableBlueprintActionSource), "source.source_id")
    expect_missing(
        forge(source, entries=(entry, object.__new__(BlueprintActionEntry))),
        "entries[1].key",
    )
    expect_missing(
        forge(source, entries=(forge(entry, key=object.__new__(BlueprintDecisionKey)),)),
        "entries[0].key.street",
    )
    expect_missing(
        forge(source, entries=(forge(entry, action=object.__new__(BettingAction)),)),
        "entries[0].action.kind",
    )

    marker: list[str] = []

    class Trap(ImmutableBlueprintActionSource):
        def __getattribute__(self, name: str) -> object:
            marker.append(name)
            raise AssertionError("foreign hook invoked")

    try:
        encode_blueprint(object.__new__(Trap))
    except BlueprintArtifactError:
        pass
    else:
        raise AssertionError("foreign source subclass was admitted")
    assert marker == []

    action = forge(entry.action, raise_to=10**640)
    try:
        encode_blueprint(forge(source, entries=(forge(entry, action=action),)))
    except BlueprintArtifactError as error:
        assert "entries[0].action.raise_to" in str(error)
    else:
        raise AssertionError("over-limit exact action was admitted")

    astral = ImmutableBlueprintActionSource("artifact-🚀")
    restored = decode_blueprint(encode_blueprint(astral))
    assert restored == astral and restored.digest == astral.digest
    print("TYPED REFUSAL PASS source/entry/key/action; foreign hook untouched")
    print("MINIMUM-DIGIT CLOSURE PASS over-limit action refused; astral digest preserved")


if __name__ == "__main__":
    main()
