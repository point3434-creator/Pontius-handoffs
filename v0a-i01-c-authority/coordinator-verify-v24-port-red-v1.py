"""Verify the failed first real adapter run; no candidate execution."""
from pathlib import Path
import ast
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
h = lambda raw: hashlib.sha256(raw).hexdigest()
receipt_path = C / "focused-v24-first01-design-311-receipt.json"
receipt_sha = "c9e6cb1e958bc6a8e15f0989841e5a1562dc3682286c07e7a6b44b95ee9339e1"
source_sha = "156ee88a99abb26edeaaf178841c72e89f2bdc15696c37ef91f4dcc54b767431"
raw = receipt_path.read_bytes()
assert h(raw) == receipt_sha
r = json.loads(raw)
assert r["source_sha256"] == source_sha and r["slot"] == "311" and r["kind"] == "design"
assert r["integrity"] is True and r["timed_out"] is False and r["success"] is False
assert type(r["exit"]) is int and r["exit"] == r["actual_process_returncode"] == 1
assert r["errors"] == [] and r["outcome"] == "focused_test_failure"
assert r["inputs_before"] == r["inputs_after"]
for item in r["inputs_before"].values():
    assert h(Path(item["path"]).read_bytes()) == item["sha256"]
snapshot = Path(r["snapshot"])
assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots"))
assert r["before"] == r["after"] and len(r["before"]) == 1766
for name, digest in r["before"].items():
    rel = Path(name)
    assert not rel.is_absolute() and ".." not in rel.parts
    assert h((snapshot / rel).read_bytes()) == digest, name
manifest = json.loads((snapshot / ".focused-authority/manifest.json").read_bytes())
assert len(manifest["files"]) == 1765 and manifest["tracked_count"] == 1761
assert all(r["before"][name] == digest for name, digest in manifest["files"].items())
assert (snapshot / ".git/HEAD").read_text().strip() == "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
outputs = {key: Path(item["path"]).read_bytes() for key, item in r["outputs"].items()}
assert all(h(outputs[key]) == item["sha256"] and len(outputs[key]) == item["bytes"] for key, item in r["outputs"].items())
assert outputs["log"] == (outputs["stdout"] + outputs["stderr"]).replace(b"\r\n", b"\n")
setup = json.loads(outputs["setup"])
assert setup["before"] == r["before"] and len(setup["original"]) == 1761
assert {name for name, value in setup["original"].items() if r["before"][name] != value} == {"tools/generate_test_inventory.py"}
rows = [json.loads(line)["focused_control"] for line in outputs["stdout"].splitlines() if line.startswith(b'{"focused_control"')]
identity, = [row for row in rows if row["event"] == "identity"]
summary, = [row for row in rows if row["event"] == "unittest_summary"]
assert identity == r["verification"]["identity"] and summary == r["verification"]["summary"]
assert identity["version"] == [3, 11, 15] and identity["source_sha256"] == source_sha
assert summary["tests_run"] == 53 and summary["complete_population"] is True
assert len(summary["started_ids"]) == len(summary["completed_ids"]) == 53
assert len(summary["failures"]) == 137 and len(summary["errors"]) == 742
assert summary["skips"] == summary["expected_failures"] == summary["unexpected_successes"] == []
assert "AttributeError: '_NameVersion' object has no attribute '_name_history'" in outputs["stderr"].decode()
source = (T / "engineer-generator-v24-storage.py").read_bytes()
assert h(source) == source_sha
classes = {node.name: node for node in ast.parse(source).body if isinstance(node, ast.ClassDef)}
mismatches = {}
for name in ("_NameVersion", "_NameCursor"):
    cls = classes[name]
    declaration, = [node for node in cls.body if isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "__slots__" for t in node.targets)]
    slots = set(ast.literal_eval(declaration.value))
    writes = {n.attr for n in ast.walk(cls) if isinstance(n, ast.Attribute)
              and isinstance(n.ctx, ast.Store) and isinstance(n.value, ast.Name) and n.value.id == "self"}
    mismatches[name] = sorted(writes - slots)
assert mismatches == {"_NameVersion": ["_name_history", "_name_order"], "_NameCursor": ["_name_order"]}
report = {
    "schema": "coordinator-v24-port-red-verification-v1", "receipt_sha256": receipt_sha,
    "source_sha256": source_sha, "files_rehashed": 1766, "interpreter": [3, 11, 15],
    "completed_test_methods": 53, "subtest_failures": 137, "subtest_errors": 742,
    "slot_assignment_mismatches": mismatches, "payload_executed_by_verifier": False,
    "interpretation": "Port construction fails before analyzer fitness can be evaluated. Counts are cascading subtest outcomes, not879 independent defects.",
    "root_review_correction": "Root's namespaced-AST comparison repeated the author's token conversion and therefore was not independent evidence of binding-preserving renaming. It missed attributes sharing spelling with module functions while string slots stayed unchanged.",
    "disposition": "Retain v24 rejected. v26 may correct member names only, preserving all adapter effects/costs/algorithms. Recheck slot/member symmetry and symbol-aware prototype equivalence, then rerun unchanged design53 on311. No314/matrix/corpus expansion yet.",
}
data = (json.dumps(report, indent=2) + "\n").encode()
for name, raw in {"coordinator-v24-port-red-verification-v1.json": data,
                  "coordinator-verify-v24-port-red-v1.py": Path(__file__).read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({"report_sha256": h(data), "files_rehashed": 1766, "mismatches": mismatches}))
