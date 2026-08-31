"""Record v26 fitness rejection and replicated R8 outcomes; navigation only."""
from pathlib import Path
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
h = lambda raw: hashlib.sha256(raw).hexdigest()
current = T / "CURRENT.md"
before = current.read_bytes()
assert h(before) == "65ffc56c09408ce5cb4714084aa40a57f1fdbf6d913a9bbaf99fab5dd13f654f"
pin = "181248855d1947c775d21728ed3ae5c2bb62b7deb15604154f88b95290e89bac"
assert h((T / "coordinator-v26-r8-verification-v1.json").read_bytes()) == pin
s = before.decode()
start = s.index("A bounded v26 correction is authorized")
end = s.index("The previous v22 cursor adapter remains RED:", start)
s = s[:start] + """The bounded v26 correction restored17 member attributes; all adapter work,
charges, algorithms and caps stayed unchanged. Its first real3.11 design run
now completes normally with50/53 methods passing and no errors. Three tests
still hit the work limit before the required depth refusal: helper1050,
helper65 and generator70. The helper65 case is an additional regression relative
to v22. [Independent verification](coordinator-v26-r8-verification-v1.json)
rehashes the run and confirms the original test bytes. The slot bug is fixed;
the adapter's production fitness remains rejected. No314/matrix/corpus expansion.

The next bounded cost step is an observer-only diagnosis of these exact three
fixtures, separating publication costs from full rebuilds, transfers and copies.
Its source/harness must be inspected before dispatch. No further optimization,
budget change or source integration is authorized by that diagnostic.
This adapter is internal analyzer work introduced during C's repair, not an
original v0a product feature. Its justification remains passing the existing
real analyzer/corpus gates within their existing limits.

""" + s[end:]
old = """also identifies target receiver/index loads, merged deferred alternatives and
changed-empty-iterator guard paths. A fixed R01–R08 extension is frozen but has
not yet executed; those source concerns are not extra demonstrated failures.
A v25 semantic successor plan is being prepared; no source edit authorized yet.
The two existing wrong approvals already have replicated RED evidence.
"""
assert s.count(old) == 1
s = s.replace(old, """also identifies target receiver/index loads, merged deferred alternatives and
changed-empty-iterator guard paths. The fixed R01–R08 extension now reproduces
all four unsafe approvals on both interpreters, while all four controls pass.
Every independent Model passes and every analyzer call completes. The same
[root verification](coordinator-v26-r8-verification-v1.json) compares complete
cross-slot records and rehashes the two full snapshots. Across36+8 fixed semantic
cases, v23 passes38/44 on each interpreter; six wrong approvals remain.

The v25 semantic plan has been reviewed independently. Before implementation,
its API must distinguish retaining a nested generator from actually consuming
it, and prevent old exact collection contents returning after shape loss.
No general class heap or new mutation precision is approved; dormant construction
and shallow container copying must stay dormant. Source authoring is not yet
authorized; the plan clarification and cost diagnostic remain in preparation.
""")
after = s.encode()
report = {"schema": "coordinator-navigation-v12", "before_sha256": h(before), "after_sha256": h(after),
          "verification_sha256": pin, "production_source_changed": False,
          "v26_original_design": "50/53,3work-limit failures,0errors", "v23_semantic_each_slot": "38/44,6unsafeapprovals"}
outputs = {"coordinator-update-authority-navigation-v12.py": Path(__file__).read_bytes(),
           "coordinator-navigation-v12.json": (json.dumps(report, indent=2) + "\n").encode()}
assert not any((T / name).exists() for name in outputs)
for name, raw in outputs.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
current.write_bytes(after)
print(json.dumps(report))
