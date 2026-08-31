"""Replace mutable navigation with a concise current checkpoint; preserve its prior text."""
from pathlib import Path
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
h = lambda raw: hashlib.sha256(raw).hexdigest()
current = T / "CURRENT.md"
before = current.read_bytes()
assert h(before) == "72bfc37aacf1dd32d307d9537c50626cc031f645a2b5f2ddfaf65f4f059a80bf"
pins = {
    "coordinator-v26-depth-budget-verification-v1.json": "2e729e903ed0f0c869e88aa595d62bc0da5a2f3a47d29962f901a4865a87bf30",
    "coordinator-v26-r8-verification-v1.json": "181248855d1947c775d21728ed3ae5c2bb62b7deb15604154f88b95290e89bac",
    "engineer-generator-v25-semantic-plan-v1.md": "39807c39a14e6f2009ffa69f5f09604c8354c1043a09be6c63e5982412621c2d",
    "engineer-generator-v25-semantic-plan-v2.md": "e2ed7f88a6c081be3ec54556e47a327ce1ea2d336e55200e788857cfec099bb8",
}
assert all(h((T / name).read_bytes()) == pin for name, pin in pins.items())
after = """# C authority repair: current checkpoint

2026-08-31. Navigation only, not a frozen handoff, evidence seal, acceptance
result or reviewer verdict. Reviews bind to a git snapshot ref and manifest
SHA-256. No successor pair is frozen and no source is integrated into main.

## Decision: isolated passes do not establish integration readiness

The radix store passed558 check executions:93 per child across two actual
interpreters and three hash seeds. These are repeated finite property checks,
not558 independent production guarantees. [Root verification](coordinator-indexed-verification-allsix01.json)
rehashes10665 files and compares complete same-seed records across interpreters.
The experiments establish pure-store behavior, not analyzer fitness or speed.

This storage adapter is in-memory analyzer bookkeeping introduced during C's
repair, not an original v0a feature. Its justification is passing the existing
real analyzer and corpus gates within their existing limits. The adapter is
not a required product architecture, and none is installed in W or main.

V24's first port failed because global-name rewriting also renamed member
attributes without changing their slots. Root's first static comparison
repeated that mistake. The [retained failure](coordinator-v24-port-red-verification-v1.json)
is137 failing/742 error subtest outcomes across53 methods, not879 defects.
V26 corrects only17 attributes and now passes50/53 original design methods on
real3.11.15, with3 work-limit failures and0 errors. [Verification](coordinator-v26-r8-verification-v1.json)
confirms the original assertions remain unchanged. No dev/matrix/corpus expansion.

## Storage cost: three mechanisms measured, remedy not yet implemented

All three exact original fixtures completed observer-only diagnostics on real
3.11.15 in fresh snapshots. [Root verification](coordinator-v26-depth-budget-verification-v1.json)
rehashes5298 files, binds runtime identities and reconciles every budget epoch.
All still refuse at the unchanged262144-unit cap:

- helper1050: publication preparation uses199347 of262145 charged units;
  radix freezing alone uses144283. Only one3-name bulk constructor runs.
  Failure is at definition registration of helper_628, before helper execution.
- helper65: actual recursive entry reaches helper_50; repeated constructor
  preparation, lookup and ordering dominate. There are54 bulk-constructor
  attempts and51 dirty publications that build names from an empty base.
- generator70: disabled receiver preflight performs36 full joins, each with
  two73-name inputs. Lookup uses80486 units; full-join preparation40248 and
  radix bulk building27454. Publication preparation contributes only9806.

Publication totals overlap the component partition and must not be added to
it. The original absent hash seed is preserved; these are not strict cross-run
ratios or runtime benchmarks. Equal input sizes do not prove equal states.
The next design must address these actual operations rather than increase the
isolated test count. No new storage optimization, cap change or W lease is
authorized by diagnostic completion.

## Semantics: six wrong approvals remain; bounded v25 authoring underway

V23 passes38/44 fixed semantic cases on each actual interpreter. C03 loses a
forwarded closure by skipping its factory; Q05 drops a deferred class member.
The four R8 unsafe cases reproduce receiver/index binding, nested generator
join and changed-empty-iterator gaps. All Models pass and all analyzer calls
complete. The [replicated evidence](coordinator-v26-r8-verification-v1.json)
retains the four passing R8 controls; no required-clean label was weakened.

[Planv1](engineer-generator-v25-semantic-plan-v1.md) and normative
[planv2](engineer-generator-v25-semantic-plan-v2.md) have root and independent
engineering review. T-only source authoring is authorized from exact v23;
no payload or W/main edit follows from that authorization. The repair must:

- Retain generators through class members and joins without consuming dormant
  generators merely because a container is copied or iterated.
- Invalidate current authoritative collection shape after unknown mutation;
  stale exact contents must not reappear through either recovery path.
- Initialize member bundles before transfer shortcuts, preserve lexical and
  exceptional-exit semantics, and meter new traversal/comparison work.

Mechanical budget plumbing through existing merge callers is permitted for
new work. Any such change to storage methods must be disclosed; those methods
cannot then be called byte/AST-identical. Storage algorithms and effects stay
unchanged in this semantic lane. No general class heap or new precision is approved.

## Preserved state and remaining acceptance

Accepted A/B remains r007, byte-identical. Other C integration paths and the
generated inventory/profile pair remain preserved. W is still rejected v20;
main remains d1ed3cb. Its existing CLAUDE.md and docs/workflow.md edits are
user-owned and untouched. The latest frozen combined candidate remains rejected
r010:29c02f6fbd5eb0b7ddc9e816ef28f570b9839358 /
8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb.

Remaining: complete both bounded repairs; verify a coherent candidate against
focused and corpus gates; preserve existing inventory and capability rows;
refresh the mechanical census; freeze a new pair; obtain two fresh mutually
blind cold reviews; run the permitted CPU acceptance wall. Candidate-specific
authorization and the named finalizer checkpoint precede main commit/push.

No guarded profile, GPU execution, experiment owner or live15-second action-wall
claim is authorized. Earlier checkpoint details and links are retained in
[the prior navigation](coordinator-navigation-v12-before-v13.md); all issued
candidate, failure, raw evidence and review artifacts remain immutable.
""".encode()
report = {"schema": "coordinator-navigation-v13", "before_sha256": h(before), "after_sha256": h(after),
          "pins": pins, "production_source_changed": False, "payload_running": False,
          "semantic_authoring": "T-only v25 source authorized; no payload/W/main lease",
          "storage_authoring": "Measured remedy plan only, no optimization source authorized",
          "prior_navigation_retained": "coordinator-navigation-v12-before-v13.md"}
outputs = {"coordinator-navigation-v12-before-v13.md": before,
           "coordinator-update-authority-navigation-v13.py": Path(__file__).read_bytes(),
           "coordinator-navigation-v13.json": (json.dumps(report, indent=2) + "\n").encode()}
assert not any((T / name).exists() for name in outputs)
for name, raw in outputs.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
current.write_bytes(after)
print(json.dumps({"navigation_sha256": h(after), "old_navigation_retained": True, "source_changed": False}))
