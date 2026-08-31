"""Record the new floor result and its precise assertion limits; no source edit."""
from pathlib import Path
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
current = T / "CURRENT.md"
before = current.read_bytes()
assert hashlib.sha256(before).hexdigest() == "3408f46d3a809ca4eed7fd7bc2dce0766cd32bbbf06d4ddeae8242a49d505dbe"
note_path = T / "coordinator-v22-first-floor-disposition-v2.md"
assert not note_path.exists()
note = """# v22 first floor: assertion-scope correction

Append-only correction to coordinator-v22-first-floor-disposition-v1.md and
the interpretation field of coordinator-v22-focused-red-verification-v1.json.
Their result counts, raw receipt binding and independent integrity check stand.

The two failed assertions differ. Original test line 4949 accepts an
InventoryError whose text matches analysis.*(?:depth|budget). The observed
work-cap rejection has the expected exception type but neither category word;
that test does not specifically require depth to fire before work. Original
line 14551 requires exactly analysis deferred generator depth exceeds 64.
Only the latter fixes the rejection kind and priority that narrowly.

Both observed exceptions are analysis work units exceed 262144. Neither is
an unsafe authorization. No exception wording, assertion, cap or acceptance
contract has been changed. The next step remains measurement of the exact
helper1050 and generator70 source cases before choosing a repair.

The first retained v22 design run is still 51 passes, two failures, no errors.
No matrix, dev, public24 or corpus expansion is released for v22. No source
integration or main commit/push has occurred.
"""
with note_path.open("xb") as stream:
    stream.write(note.encode())
old = """This verifies storage semantics, retention and whole-operation retry staging;
it does not establish production fit. A [bounded T-only adapter draft](coordinator-name-cursor-candidate-disposition-v1.md)
is being prepared from exact v20. W remains unchanged; no installation or
payload execution is authorized by that drafting disposition.
"""
new = """This verifies storage semantics, retention and whole-operation retry staging;
it does not establish production fit. The retained v22 adapter passed static
inspection and then ran the original design53 on actual Python 3.11.15 in a
fresh snapshot: **51 passed, two failed, zero errors**. Its bounded chain32
case passes; helper1050 and generator70 reject at the unchanged work cap.
[Verified result](coordinator-v22-focused-red-verification-v1.json) binds all
1766 snapshot/payload files and the raw streams. [Assertion-scope correction](coordinator-v22-first-floor-disposition-v2.md)
distinguishes the helper test's depth-or-budget text requirement from the
generator test's exact depth64 requirement. Diagnosis comes next; matrix,
dev, public24 and corpus expansion are held. W remains v20; the v22 candidate
exists only as retained T bytes and its isolated test snapshot.
"""
text = before.decode()
assert text.count(old) == 1
after = text.replace(old, new).encode()
current.write_bytes(after)
copy = T / "coordinator-update-authority-navigation-v8.py"
with copy.open("xb") as stream:
    stream.write(Path(__file__).read_bytes())
report = {
    "current_before_sha256": hashlib.sha256(before).hexdigest(),
    "current_after_sha256": hashlib.sha256(after).hexdigest(),
    "correction_sha256": hashlib.sha256(note_path.read_bytes()).hexdigest(),
    "source_changed": False,
}
with (T / "coordinator-navigation-v8.json").open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2)
    stream.write("\n")
print(json.dumps(report))
