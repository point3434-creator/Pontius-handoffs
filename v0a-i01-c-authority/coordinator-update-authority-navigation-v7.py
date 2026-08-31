"""Refresh navigation from pinned completed evidence; no source changes."""
from pathlib import Path
import hashlib
import json
import os
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
CURRENT_SHA = "61bca3a8288d33a40dfb4b8354c34f77397263b275146cc287d0369d5fd48fc4"
PINS = {
    "coordinator-cursor-verification-v1.json": "beea083a71bcbb9e32df5e11a01e9e17af2ca4238958fe27e55661cce24972aa",
    "coordinator-class-adoption-finding-v1.md": "9c1368b7bd5a86970ffe17a21ae3b8707c61be20f6bf1c7bfd179cbd82e40e6d",
    "tests-checks/class-composition-original-class2-v19-mechanism01-311-receipt.json": "9c26c08e8fab39c11e0c49ccd952274b0a31eb98899b51d2bd3f419cf9ad0f32",
    "tests-checks/class-composition-original-class2-v19-mechanism01-314-receipt.json": "b8429565b8179962c00e3207c6669d294ceb678bf255b9f09250d1cb26e31314",
    "tests-checks/class-composition-scalar-class6-v19-mechanism01-311-receipt.json": "9c86569d53b6664bf5a6f1912607255c253412dac70d2bd74bfb1dda454b6be9",
    "tests-checks/class-composition-scalar-class6-v19-mechanism01-314-receipt.json": "97ff9ac31ad8a1eb3f75f3dcde461e1c2ff392ed1d705481cd5e9b45f156ff2d",
    "coordinator-name-cursor-candidate-disposition-v1.md": "8cabe43873bddfc7871ff671c96eec85fccfc29cf774dd3c748167fc9dabae21",
}


def h(raw):
    return hashlib.sha256(raw).hexdigest()


assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
current = T / "CURRENT.md"
raw = current.read_bytes()
assert h(raw) == CURRENT_SHA
for name, pin in PINS.items():
    assert h((T / name).read_bytes()) == pin, name
block = """## Latest checkpoint: two separate repairs, no integration

The replacement owned-cursor prototype passed all 372 checks: 204 unchanged
immutable-storage runs and 168 new cursor runs, across actual Python 3.11.15
and 3.14.6 with seeds 0, 1 and 17. [Coordinator verification](coordinator-cursor-verification-v1.json)
rehashes all six snapshots, the input artifacts and same-seed public records.
This verifies storage semantics, retention and whole-operation retry staging;
it does not establish production fit. A [bounded T-only adapter draft](coordinator-name-cursor-candidate-disposition-v1.md)
is being prepared from exact v20. W remains unchanged; no installation or
payload execution is authorized by that drafting disposition.

The added composition checks found an independent semantic defect on retained
v19. Both original class cases fail on both interpreters: an unsafe case is
approved and its safe counterpart is refused. The original shared-list pair
passes. [Initial finding](coordinator-class-adoption-finding-v1.md) preserves
the unchanged expectations and the initial, explicitly provisional diagnosis.

The subsequent [two-case trace](tests-checks/class-composition-original-class2-v19-mechanism01-311-receipt.json)
and [six-case extension](tests-checks/class-composition-scalar-class6-v19-mechanism01-311-receipt.json)
correct that initial lead: write-only nonlocal setters omit their captured
destination because discovery considers only Name loads. The setter changes
its private projection while the caller's cell retains the old value.
Class-body execution also continues past an explicit raise. Earlier protected
namespace rebinding guards cause additional safe-case refusals. A projection
refresh alone therefore cannot close this category.

Both trace scopes completed on both interpreters with intact infrastructure
and correct harmless oracles. The scalar extension fails four of its six
requirements on each slot (both normal cases and both safe exception cases).
The two unsafe exception cases are refused; that alone does not establish
correct exception semantics. A separate semantic repair must address captures,
normal and exceptional class exits, and precise versus unresolved rebinding.
All cases and issued evidence remain immutable.

The candidate is still not acceptable. Accepted A/B and other C paths remain
preserved; the class defect and ordinary-generation budget failure are both
open. The detailed prior engineering evidence follows.

"""
needle = "Accepted A/B remains byte-identical"
text = raw.decode("utf-8")
assert text.count(needle) == 1 and "## Latest checkpoint:" not in text
updated = text.replace(needle, block + needle, 1).encode("utf-8")
copy = T / "coordinator-update-authority-navigation-v7.py"
receipt = T / "coordinator-navigation-v7.json"
assert not copy.exists() and not receipt.exists()
report = {
    "previous_current_sha256": CURRENT_SHA, "current_sha256": h(updated),
    "input_pins": PINS, "source_changes": False, "new_frozen_pair": False,
}
for path, value in ((copy, Path(__file__).read_bytes()),
                    (receipt, (json.dumps(report, indent=2) + "\n").encode())):
    with path.open("xb") as stream:
        stream.write(value)
        stream.flush()
        os.fsync(stream.fileno())
current.write_bytes(updated)
assert h(current.read_bytes()) == report["current_sha256"]
print(json.dumps(report, indent=2))
