from __future__ import annotations
import json, os, sys
from dataclasses import fields
from pathlib import Path

SNAPSHOT = Path(sys.argv[1]).resolve()
SLOT = sys.argv[2]
EXPECTED = {
    "311": (Path(r"D:\Pontius-tools\py311\Scripts\python.exe"), (3, 11, 15)),
    "314": (Path(r"D:\Pontius\.venv\Scripts\python.exe"), (3, 14, 6)),
}
executable, version = EXPECTED[SLOT]
identity = {
    "executable": sys.executable, "implementation": sys.implementation.name,
    "full_version": sys.version, "version": list(sys.version_info[:3]),
    "cwd": str(Path.cwd()), "pythonpath": os.environ.get("PYTHONPATH"),
    "PONTIUS_GIT": os.environ.get("PONTIUS_GIT"),
}
print(json.dumps({"identity_before_payload_import": identity}), flush=True)
assert Path(sys.executable).resolve() == executable.resolve()
assert tuple(sys.version_info[:3]) == version and sys.implementation.name == "cpython"
assert Path.cwd().resolve() == SNAPSHOT
assert Path(os.environ["PYTHONPATH"]).resolve() == SNAPSHOT / "src"
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert os.environ["PONTIUS_GIT"] == r"C:\Program Files\Git\cmd\git.exe"

from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.model import (
    ActionEnvelope, ActionMailbox, DeliveryReceipt, HandAction,
    HandStartedEvent, OpponentActionEvent,
)
from pontius.v0a.runtime import HandRuntime
import pontius.v0a.runtime as runtime_module

assert Path(runtime_module.__file__).resolve().is_relative_to(SNAPSHOT / "src")
assert "cupy" not in sys.modules and "torch" not in sys.modules

class Clock:
    def __init__(self): self.value = 0
    def __call__(self):
        self.value += 1000
        return self.value

class SkipReceipt(DeliveryReceipt):
    def __post_init__(self): pass

class SkipEnvelope(ActionEnvelope):
    def __post_init__(self): pass

class SkipAction(HandAction):
    def __post_init__(self): pass

class SkipStart(HandStartedEvent):
    def __post_init__(self): pass

def start(controlled=3):
    return HandStartedEvent(
        hand_id="value-audit", event_index=0, button=0, controlled_seat=controlled,
        starting_stacks=(200,) * 6, small_blind=1, big_blind=2, private_cards=(0, 13),
    )

def kwargs(value):
    return {field.name: getattr(value, field.name) for field in fields(value)}

def rejects(cls, values):
    try:
        cls(**values)
    except (TypeError, ValueError) as exc:
        return type(exc).__name__
    raise AssertionError("base constructor accepted invalid probe")

def runtime(mailbox=None):
    box = ActionMailbox() if mailbox is None else mailbox
    return HandRuntime(
        blueprint=ImmutableBlueprintActionSource(source_id="value-audit"),
        mailbox=box, clock=Clock(),
    ), box

def dispatch_result(rt, box, event):
    try:
        outcome = rt.dispatch(event)
        return {
            "status": outcome.status,
            "failure": None if outcome.failure is None else outcome.failure.code.value,
            "selected": None if outcome.decision is None else outcome.decision.selected_action.kind,
            "event_index_recorded": (
                None if outcome.decision is None else outcome.decision.event_index
            ),
            "accepted": len(box.accepted), "runtime_count": rt.accepted_delivery_count,
        }
    except Exception as exc:
        return {"escaped": type(exc).__name__, "message": str(exc),
                "accepted": len(box.accepted), "runtime_count": rt.accepted_delivery_count}

results = []
rt, box = runtime()
baseline = dispatch_result(rt, box, start())
assert baseline["status"] == "decided" and baseline["accepted"] == 1
results.append({"case": "valid_baseline", **baseline})

class ReceiptMailbox(ActionMailbox):
    def __init__(self, variant):
        super().__init__()
        self.variant = variant
    def deliver(self, envelope):
        real = super().deliver(envelope)
        if self.variant == "valid_subclass":
            return SkipReceipt(real.hand_id, real.action_index)
        if self.variant == "wrong_integer":
            return DeliveryReceipt(real.hand_id, real.action_index + 1)
        value = True if self.variant == "bool" else float(real.action_index)
        return SkipReceipt(real.hand_id, value)

for variant in ("valid_subclass", "wrong_integer", "bool", "float"):
    if variant in ("bool", "float"):
        bad = True if variant == "bool" else 1.0
        parent = rejects(DeliveryReceipt, {"hand_id": "value-audit", "action_index": bad})
    else:
        parent = None
    box = ReceiptMailbox(variant)
    rt, _ = runtime(box)
    result = dispatch_result(rt, box, start())
    results.append({"case": "receipt_" + variant, "parent_rejects": parent, **result})

valid_envelope = ActionEnvelope("value-audit", 1, 3, "preflop", HandAction("call", None))
for label, change in [
    ("bad_seat", {"seat": True}), ("bad_street", {"street": "not-a-street"}),
    ("empty_id", {"hand_id": ""}),
]:
    values = kwargs(valid_envelope) | change
    parent = rejects(ActionEnvelope, values)
    envelope = SkipEnvelope(**values)
    box = ActionMailbox()
    try:
        receipt = box.deliver(envelope)
        result = {"returned": type(receipt).__name__, "receipt_index": receipt.action_index}
    except Exception as exc:
        result = {"escaped": type(exc).__name__, "message": str(exc)}
    results.append({"case": "envelope_" + label, "parent_rejects": parent,
                    "accepted": len(box.accepted), **result})

for label, change in [
    ("schema", {"schema_version": "not-the-event-schema"}),
    ("nonzero_index", {"event_index": 99}),
    ("bool_index", {"event_index": False}),
]:
    values = kwargs(start()) | change
    parent = rejects(HandStartedEvent, values)
    rt, box = runtime()
    results.append({"case": "start_" + label, "parent_rejects": parent,
                    **dispatch_result(rt, box, SkipStart(**values))})

for kind, amount in [("teleport", 6), ("fold", 7)]:
    values = {"kind": kind, "raise_to": amount}
    parent = rejects(HandAction, values)
    nested = SkipAction(**values)
    rt, box = runtime()
    first = dispatch_result(rt, box, start(controlled=0))
    assert first["status"] == "accepted"
    event = OpponentActionEvent("value-audit", 1, "preflop", 3, nested)
    outcome = dispatch_result(rt, box, event)
    history = rt.state.history
    results.append({
        "case": "nested_action_" + kind, "parent_rejects": parent,
        "container_exact_type": type(event) is OpponentActionEvent,
        "input_kind": kind, "input_raise_to": amount,
        "committed_kind": history[-1].action.kind.value,
        "committed_raise_to": history[-1].action.raise_to, **outcome,
    })

print(json.dumps({"candidate": "47d08d8c1556d776358e15811e3e98b859fd6a8b",
                  "manifest_sha256": "cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a",
                  "observations": results}), flush=True)
