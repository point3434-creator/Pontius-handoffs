"""Record six passing pure-store trials and continuing class repair; navigation only."""
from pathlib import Path
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
sha = lambda raw: hashlib.sha256(raw).hexdigest()
current = T / "CURRENT.md"
before = current.read_bytes()
assert sha(before) == "3bef658b804a56dcf91e2d626dead32bdeea938c81ace1a24d454827a8365a6a"
proof_raw = (T / "coordinator-indexed-verification-allsix01.json").read_bytes()
assert sha(proof_raw) == "3e3af131f3c4839bb26e993f7d188f0c92d129f129b3edbc392b1a04f1f7151b"
proof = json.loads(proof_raw)
assert proof["completed_runs"] == 558
assert all(run["same_seed_cross_slot_records_equal"] is True for run in proof["runs"] if run["slot"] == "314")
assert sha((T / "coordinator-class-name-boundary-red-verification-v1.json").read_bytes()) == "74f243ebf84c11a38ecb66b5f3ff61f4e5a36eb2c9166bb91ce155c18642ff22"
preserved = {name: digest for name, digest in json.loads((T / "coordinator-preservation-baseline-v2.json").read_bytes())["paths"].items()
             if name not in {"tools/generate_test_inventory.py", "tests/test_inventory_and_profiles.py"}}
assert len(preserved) == 15
assert {name: sha((W / name).read_bytes()) for name in preserved} == preserved
assert sha((W / "tools/generate_test_inventory.py").read_bytes()) == "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
assert sha((W / "tests/test_inventory_and_profiles.py").read_bytes()) == "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
source = before.decode()
start = source.index("The replacement owned-cursor prototype")
end = source.index("The added composition checks", start)
latest = """The isolated radix-store/bulk-builder replacement passed **558 checks**:
34 unchanged storage runs, 28 cursor-successor runs and 31 indexed-extension
runs per child, on actual Python3.11.15 and3.14.6 with seeds0/1/17. The
[coordinator verification](coordinator-indexed-verification-allsix01.json)
rehashed10665 files including manifests; same-seed complete records match
across interpreters. All14 preregistered P/C growth comparisons pass per child,
as do collision activation, direct obsolete-value release and15 injected
indexed-operation retries per child. The old cursor retention trigger was
explicitly made representation-neutral before results; do not call all62
predecessor executable checks byte-identical.

[Source/accounting inspection](coordinator-radix-prototype-inspection-v1.json)
and [independent oracle inspection](coordinator-indexed-oracle-inspection-v1.json)
preceded dispatch. This establishes finite pure-store behavior, **not production
fitness or wall-time speed**. The adapter must preserve full authority transfer,
cell writes and real input-preparation costs, then pass the original analyzer
gates. No radix implementation is installed in W or main.

The previous v22 cursor adapter remains RED:51/53 original design tests pass,
with helper1050 and generator70 exhausting the unchanged work budget. Both
[exact-case diagnostics](coordinator-v22-depth-budget-verification-v1.json)
locate failure in preparation, not deep execution. This is why the replacement
uses touched indexed paths and a direct unique-entry bulk builder. The original
caps and assertions remain unchanged; ordinary generation is still unverified
on the replacement. W remains rejected v20.

"""
source = source[:start] + latest + source[end:]
start = source.index("The [lexical ownership API]")
end = source.index("The candidate is still not acceptable.", start)
semantic = """The [eight Name-boundary cases](tests-checks/class-name-boundary-cases-v1.json)
also completed on retained v19 under both actual interpreters. All harmless
Models pass; four semantic requirements fail identically: two safe cases are
refused, an unsafe direct class nonlocal write is incorrectly approved, and
the safe module-write case misses its required conservative refusal.
[Independent verification](coordinator-class-name-boundary-red-verification-v1.json)
retains the exact per-case results and3541 rehashed files.

A semantic-only v23 candidate is being authored under the
[coordinator disposition](coordinator-class-semantic-v23-disposition-v1.md).
It addresses lexical ownership/current-cell separation, normal and exceptional
class exits, Name routing, and historical callable/call-state pairing. The
class-only eager comprehension boundary is within that scope; unproved deferred
class-generator consumption must explicitly refuse. Six additional independent
[comprehension witnesses](tests-checks/class-comprehension-boundary-spec-v1.md)
are preregistered but unexecuted. No semantic candidate payload has run.

The storage and semantic edits remain separate until independently inspected
and checked. Original10 composition, class12, Name8 and comprehension6 checks
will precede focused analyzer/corpus gates. Only a coherent verified candidate
can be frozen for two new mutually blind cold reviewers and later integration.

"""
source = source[:start] + semantic + source[end:]
after = source.encode()
disposition = """# Radix prototype: completed finite experiment

Coordinator, 2026-08-31. The fixed prototype/config/oracles completed all
six preregistered children: actual3.11.15 then3.14.6, seeds0/1/17. All558
runs pass. Coordinator report3e3af131f3c4839bb26e993f7d188f0c92d129f129b3edbc392b1a04f1f7151b
independently rehashes10665 files including manifests. All same-seed complete
case records agree across interpreters.

Each child retained34 old storage +28 cursor-successor +31 indexed runs.
All14 fixed P/C growth comparisons pass. I07 actually reaches the hash-width
collision route; seed0 reports709 charged terminal operations and121228
observer equality calls. These quantities are distinct. Obsolete overwritten
and deleted values release after one changed publication when the legitimate
old snapshot owner is removed. Fifteen indexed first/middle/last failures per
child retain their spent work, then match pristine retry and continuation costs.

The largest growing-case total is217378/262144 units. Seed0 four bulk builds
plus first ordering cost120844 units, within the frozen6x growth comparison.
These are algorithm-work measurements, not timing benchmarks or proof of fit
for the real1050-helper/generator/corpus workloads. No cap or threshold changed.

The experiment now supports authoring a separate storage-only production
adapter from retained v22, after its exact transfer/cell/input-preparation
boundary is enumerated. It does not authorize W writes, bypasses, cold approval,
integration, a main commit, or reuse of experimental identities. The class
semantic repair stays separate. Preserve all failed predecessor evidence.
"""
report = {"current_before_sha256": sha(before), "current_after_sha256": sha(after),
          "source_changed": False, "preserved_paths": preserved,
          "watch_source": "v20", "completed_pure_store_runs": 558,
          "disposition_sha256": sha(disposition.encode())}
outputs = {
    "coordinator-indexed-prototype-result-disposition-v1.md": disposition.encode(),
    "coordinator-update-authority-navigation-v10.py": Path(__file__).read_bytes(),
    "coordinator-navigation-v10.json": (json.dumps(report, indent=2) + "\n").encode(),
}
assert not any((T / name).exists() for name in outputs)
for name, raw in outputs.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
current.write_bytes(after)
print(json.dumps({key: value for key, value in report.items() if key != "preserved_paths"}))
