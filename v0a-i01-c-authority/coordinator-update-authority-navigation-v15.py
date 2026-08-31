"""Update mutable navigation while retaining exact previous bytes."""
from pathlib import Path
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
h = lambda raw: hashlib.sha256(raw).hexdigest()
current = T / "CURRENT.md"
before = current.read_bytes()
assert h(before) == "8bacea70ec4512d85eea9b0a7c803f94e6cd7f5001074fd38f409915329d5550"
pins = {
    "coordinator-v28-primitive-311-verification-v1.json": "648ca365745b1d436a4245034f7172301c3d4236bb09a9b2995153573abb4ca9",
    "coordinator-v28-primitive-314-verification-v1.json": "bb6d58429de302b0c5ecebea380033b9c4dd623df4b242510db6fd1dec3d3b11",
    "coordinator-v28-testfix-verification-v2.json": "1de262da99ffebe65d74e34409b1a06b4401e2bc2dc9e2196469ea07d5e47b14",
    "engineer-budget-assertion-candidate-review-v1.md": "faf1bdb169669c5e252cfe679e8e4ed0fb08f522a5a14d1c753d0c56664de10c",
    "tests-checks/v25-authority-carrier-engineering-review-codex-a-v1.md": "7b0b322d2c91c6db51b1c9c7549b59413b89c2d02edb4fce6865d5eaede1627c",
    "tests-checks/v29-disabled-join-engineering-review-codex-a-v1.md": "f397975e37f00ea9512563e91dea9bc89ae7f9dda2ce96ab2f5ed5ba1dc610ad",
    "engineer-generator-v25-review-successor-plan-v1.md": "56c1b494349ea3b70af3eee2f26d9bf99fab72db1725b5b833b4af187be4ac34",
    "engineer-v30-enumerate-accounting-plan-v1.md": "a6fbc28533102f86341daac86cb76761517e2b2770421d29c6b8d94381bdf983",
}
assert all(h((T / name).read_bytes()) == pin for name, pin in pins.items())
baseline = json.loads((T / "coordinator-preservation-baseline-v2.json").read_bytes())["paths"]
baseline["tools/generate_test_inventory.py"] = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
baseline["tests/test_inventory_and_profiles.py"] = "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
assert len(baseline) == 17 and all(h((W / name).read_bytes()) == pin for name, pin in baseline.items())
# Full previously recorded user-owned file digests; no source mutation here.
main_user = {
    "CLAUDE.md": "af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76",
    "docs/workflow.md": "d9de38ede87fb619b3045a60ee7fab137ae23ba3b580c0a6d6b3ca14e567a170",
}
assert all(h((Path(r"D:\Pontius") / name).read_bytes()) == pin for name, pin in main_user.items())
after = '''# C authority repair: current checkpoint

2026-08-31. Navigation only. No new frozen review pair, cold verdict, acceptance
claim or main integration. Reviews bind to a git snapshot ref and manifest SHA-256.

## What the test counts establish

The original558 passes were93 finite storage checks repeated across two actual
interpreters and three seeds. They are useful primitive evidence, not558
independent production guarantees. [Original verification](coordinator-indexed-verification-allsix01.json).

The changed v28 production primitive has now passed the same unchanged93 checks
on actual3.11.15 and3.14.6 at seed0. All93 case records match exactly across slots.
[Floor verification](coordinator-v28-primitive-311-verification-v1.json) and
[dev verification](coordinator-v28-primitive-314-verification-v1.json) rehash1782
and1787 files. Fifteen of sixteen new charge categories were exercised;
radix_freeze_child_delete_operations was not. This is not exhaustive coverage.
The exact extraction preserves47 production nodes but uses the original test
Meter: constructor B, the production budget adapter, resolver and corpus remain
outside its claim. No extra cases or automatic six-run expansion were added.

The adapter is in-memory inventory-analyzer bookkeeping introduced during C repair,
not an original v0a product requirement. Its justification remains the actual
analyzer/corpus gates within unchanged limits. Counts alone do not approve it.

## Storage:52/53 on corrected tests; remaining depth gate stays hard

V28 contains the measured A+B repairs. Its original test run remains51/53 with two
failures. The helper1050 assertion independently allowed depth OR budget but failed
to recognize the canonical work-budget wording. A separately frozen one-literal
[v5 correction and independent review](engineer-budget-assertion-candidate-review-v1.md)
preserve every other assertion, fixture, cap and error. Nothing retroactively
changes the earlier verdict.

[V28 plus v5](coordinator-v28-testfix-verification-v2.json) now gives52/53 on
actual3.11.15. Generator70 still exhausts the262144 work cap before the exact required
generator-depth refusal. No dev/matrix/corpus expansion follows from that failure.

The identical-root shortcut had zero qualifying joins out of36 and was never
implemented. V29 instead adds only the reviewed operation-local disabled join:
common-history unchanged Entry identity may avoid duplicate merge/transfer work;
pending no_work=False debt, original union order, effects and fallback remain.
[Engineering review](tests-checks/v29-disabled-join-engineering-review-codex-a-v1.md)
found no additional semantic blocker, but a confirmed missing enumeration-pair
charge keeps v29 frozen and unexecuted. V30 authoring is authorized only for the
[two explicit accounting calls](engineer-v30-enumerate-accounting-plan-v1.md).
Root source inspection precedes a new focused run; no limit increase is allowed.

## Semantics: source review blocks v25; bounded successor authorized

V23 remains42/52 on the seven frozen semantic packs on both interpreters: ten
unsafe examples still wrongly approved, with all harmless Models completing.
The earlier38/44 and later4/8 reports remain separately retained.

V25 is frozen and unexecuted. The [independent engineering review](tests-checks/v25-authority-carrier-engineering-review-codex-a-v1.md)
found five source gaps: ordinary deferred-root retention, mixed owner completeness,
current collection-read dominance, typed refusal propagation, and new-work
accounting. Pair containment and graph traversal order also need correction.
These are source findings, not invented v25 runtime failures.

Root accepted the [category-first successor plan](engineer-generator-v25-review-successor-plan-v1.md)
for T-only v31 authoring. Shared retention/reached-consumption/read boundaries must
close the categories; explicit new-work accounting replaces informal estimates.
All52 fixed cases, required-clean labels, caps, storage boundary and identical-
FlowValue merge law remain binding. No new witness family, class heap or broad
analyzer precision is authorized. Source review precedes every payload dispatch.

## Preserved state and remaining acceptance

Accepted A/B remains r007. Other C paths and inventory/profile bytes are preserved.
W remains rejected v20. Main remains d1ed3cb with user-owned CLAUDE.md and
docs/workflow.md unchanged. The last frozen pair is rejected r010:
29c02f6fbd5eb0b7ddc9e816ef28f570b9839358 /
8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb.

Remaining: finish the bounded repairs; verify one coherent candidate against
focused and corpus gates; preserve capability rows and refresh the census;
freeze a new ref/manifest pair; obtain two fresh mutually blind cold reviews;
run permitted CPU acceptance; reach the named finalizer checkpoint before main
commit/push. No guarded suite, GPU or live15-second action-wall claim follows.

[Prior navigation](coordinator-navigation-v14-before-v15.md) retains the previous
checkpoint. Issued candidates, failed results and raw evidence remain immutable.
'''.encode()
report = {"schema": "coordinator-navigation-v15", "before_sha256": h(before), "after_sha256": h(after),
          "pins": pins, "preserved_W_paths": baseline, "main_user_owned_paths": main_user,
          "source_changed": False, "payload_running": False,
          "source_authoring": ["v30 two-call accounting successor", "v31 bounded semantic successor"],
          "prior_navigation_retained": "coordinator-navigation-v14-before-v15.md"}
outputs = {"coordinator-navigation-v14-before-v15.md": before,
           "coordinator-update-authority-navigation-v15.py": Path(__file__).read_bytes(),
           "coordinator-navigation-v15.json": (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()}
assert not any((T / name).exists() for name in outputs)
for name, content in outputs.items():
    with (T / name).open("xb") as stream:
        stream.write(content)
current.write_bytes(after)
print(json.dumps({"navigation_sha256": h(after), "old_navigation_retained": True, "source_changed": False}))
