"""Record completed cost/class RED evidence; navigation only, no source edit."""
from pathlib import Path
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
sha = lambda raw: hashlib.sha256(raw).hexdigest()
current = T / "CURRENT.md"
before = current.read_bytes()
assert sha(before) == "73eff5377b56557868f3a007292d2b44cd9738009f14a9be4025a62cc2fe22f7"
assert sha((T / "coordinator-v22-depth-budget-verification-v1.json").read_bytes()) == "0c65680c640e4c35bca18d8b2472838bfb1ad41cfef5a7a0dd24e46418815613"
assert sha((T / "coordinator-class-extension-red-verification-v1.json").read_bytes()) == "e00ca0a8d01b1812420a1fb345c702b4650549fc1f3853cf5d3da130996bb5e0"
baseline = json.loads((T / "coordinator-preservation-baseline-v2.json").read_bytes())
preserved = {}
for name, item in baseline["paths"].items():
    if name in {"tools/generate_test_inventory.py", "tests/test_inventory_and_profiles.py"}:
        continue
    expected = item if isinstance(item, str) else item["sha256"]
    assert sha((W / name).read_bytes()) == expected, name
    preserved[name] = expected
assert len(preserved) == 15
assert sha((W / "tools/generate_test_inventory.py").read_bytes()) == "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
assert sha((W / "tests/test_inventory_and_profiles.py").read_bytes()) == "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"

old = """generator test's exact depth64 requirement. Diagnosis comes next; matrix,
dev, public24 and corpus expansion are held. W remains v20; the v22 candidate
exists only as retained T bytes and its isolated test snapshot.
"""
new = """generator test's exact depth64 requirement. Both exact-case diagnostics are
now complete and [independently verified](coordinator-v22-depth-budget-verification-v1.json):
helper1050 exhausts its budget while registering helper_540; generator70
exhausts it while creating g48 during receiver preflight. No deep helper or
deferred execution is active. The first cost is repeated growing-prefix
publication/compaction; the second is full name-table rebuilding and ordering.
[Disposition](coordinator-v22-depth-budget-disposition-v1.md) preserves the
failed v1 probe and successful v2 diagnostic evidence without issuing a
product pass. An indexed-store/bulk-builder experiment is being specified;
no replacement source is authorized yet. Matrix, dev, public24 and corpus
expansion remain held. W remains v20; v22 exists only as retained T bytes and
isolated snapshots. All five caps and original assertions are unchanged.
"""
text = before.decode()
assert text.count(old) == 1
text = text.replace(old, new)
anchor = "All cases and issued evidence remain immutable.\n"
assert text.count(anchor) == 1
addition = """
The [fixed twelve-case extension](tests-checks/class-semantic-extension-cases-v1.json)
has now run on retained v19 under both actual interpreters. All twelve harmless
models pass and all analyzer calls complete, but ten semantic requirements
fail identically on each slot. All five required unsafe cases are incorrectly
clean. C01 also leaks the class-local module into the outer continuation;
C11 enters recursive review with the stale captured value and emits no row.
[Independent verification](coordinator-class-extension-red-verification-v1.json)
rehashes both full snapshots and compares all complete case records.

The [lexical ownership API](engineer-lexical-cell-ownership-api-v1.md) and
[class-frame plan](engineer-class-frame-api-plan-v1.md) are engineering inputs,
not source approval. They separate capture ownership from current cell contents,
route class exits through the existing successor model, and pair recursive
review with the recorded callable/call-state snapshot. The uncovered class
fallback/shadow and direct-declaration boundaries are being classified before
implementation; no new clean-support promise or weakened expectation is made.
No semantic source candidate has been written yet.
"""
after = text.replace(anchor, anchor + addition).encode()
current.write_bytes(after)
with (T / "coordinator-update-authority-navigation-v9.py").open("xb") as f:
    f.write(Path(__file__).read_bytes())
report = {"current_before_sha256": sha(before), "current_after_sha256": sha(after),
          "source_changed": False, "preserved_paths": preserved,
          "watch_source": "v20", "preserved_path_count": len(preserved)}
with (T / "coordinator-navigation-v9.json").open("x", encoding="utf-8", newline="\n") as f:
    json.dump(report, f, indent=2)
    f.write("\n")
print(json.dumps({k:v for k,v in report.items() if k != "preserved_paths"}))
