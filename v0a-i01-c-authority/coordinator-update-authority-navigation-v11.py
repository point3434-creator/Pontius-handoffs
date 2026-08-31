"""Update mutable navigation after v23 diagnostics and v24 port failure."""
from pathlib import Path
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
h = lambda raw: hashlib.sha256(raw).hexdigest()
current = T / "CURRENT.md"
before = current.read_bytes()
assert h(before) == "59d53d2e83188a9c3d9d2a48dce12ef5695a30d588393e2aff7a0eaaba0bee5e"
pins = {
    "coordinator-v23-semantic-verification-v2.json": "33a2257f5ec5ac31ec3f4b59342dc46e86bcab6451df1656ca7fd1931aa1d1a7",
    "coordinator-v24-port-red-verification-v1.json": "a6d29d7391f048f353bca409c37ec8342901a25ac2612a5be2f8a27b894c091b",
    "coordinator-class-comprehension-red-verification-v1.json": "29753b2f8ee8c413ad050b692a91db85055d088b252a16fb1a0f86c811bfbf8d",
}
assert {name: h((T / name).read_bytes()) for name in pins} == pins
source = before.decode()
anchor = "The previous v22 cursor adapter remains RED:"
assert source.count(anchor) == 1
storage = """The first production adapter, v24, is rejected for a porting error. Its
unchanged design suite completed53 methods on actual3.11 with137 failing and
742 error subtest outcomes. Those are cascading outcomes, not879 separate
defects: token namespacing renamed member attributes shared with global helper
names while their string-valued slots stayed unchanged. Object construction
fails before the intended cost comparison. [Root verification](coordinator-v24-port-red-verification-v1.json)
rehashes1766 files and records that the earlier root AST comparison repeated
the author's flawed conversion. The558 prototype passes did not test that port.

A bounded v26 correction is authorized for member naming only, with an
independent symbol-role and slot/member check before the same original suite.
No adapter production-fit claim follows, and no caps or tests may change.
This adapter is internal analyzer implementation work introduced during C's
repair, not an original v0a product feature. Its justification remains passing
the existing real analyzer/corpus gates within their existing limits.

"""
source = source.replace(anchor, storage + anchor)
start = source.index("A semantic-only v23 candidate is being authored")
end = source.index("The candidate is still not acceptable.", start)
source = source[:start] + """The six [comprehension witnesses](tests-checks/class-comprehension-boundary-spec-v1.md)
completed on v22 under both interpreters: all Models pass, with one wrong
safe refusal and two unsafe approvals. [Independent verification](coordinator-class-comprehension-red-verification-v1.json)
retains identical complete records and3541 rehashed files.

The frozen semantic-only v23 now passes34/36 fixed cases on each actual
interpreter: original10 all pass, class12 has one residual, Name8 all pass,
comprehension6 has one residual. [Root verification](coordinator-v23-semantic-verification-v2.json)
rehashes14166 files and confirms identical complete case records across slots.
The remaining unsafe approvals are C03 forwarded-grandparent-unsafe (factory
activation skipped before its returned closure is built) and Q05 deferred-cell-unsafe
(class completion drops the deferred member before attribute consumption).
Neither result is green or permission to integrate.

The [engineering inspection](tests-checks/class-comprehension-v23-engineering-review-codex-a-v1.md)
also identifies target receiver/index loads, merged deferred alternatives and
changed-empty-iterator guard paths. A fixed R01–R08 extension is frozen but has
not yet executed; those source concerns are not extra demonstrated failures.
A v25 semantic successor plan is being prepared; no source edit authorized yet.
The two existing wrong approvals already have replicated RED evidence.

The storage and semantic candidates stay separate. Only a coherent verified
candidate can be frozen for two new mutually blind cold reviewers and later
acceptance/integration. No combined source, new cold packet, main commit or main
push exists. W remains rejected v20; accepted A/B and other C are preserved.

""" + source[end:]
after = source.encode()
report = {"schema": "coordinator-navigation-v11", "before_sha256": h(before),
          "after_sha256": h(after), "evidence_pins": pins, "production_source_changed": False,
          "v23_passed_each_slot": 34, "v23_total_each_slot": 36,
          "v24_status": "rejected port construction error; production cost unmeasured"}
outputs = {"coordinator-update-authority-navigation-v11.py": Path(__file__).read_bytes(),
           "coordinator-navigation-v11.json": (json.dumps(report, indent=2) + "\n").encode()}
assert not any((T / name).exists() for name in outputs)
for name, raw in outputs.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
current.write_bytes(after)
print(json.dumps(report))
