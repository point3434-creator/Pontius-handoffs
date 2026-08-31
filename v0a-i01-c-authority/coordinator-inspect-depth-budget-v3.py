"""Read-only source inspection; retain a root dispatch decision, never import payloads."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import stat

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
h = lambda raw: hashlib.sha256(raw).hexdigest()
def read(path):
    assert path.is_absolute() and ".." not in path.parts
    for ancestor in (path, *path.parents):
        assert not getattr(ancestor.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path.read_bytes()

pins = {
    "engineer-depth-budget-probe-v3.py": "7aa9f188b2917fec149485501eafcc4d516d3104a10b026e5ec33262b24962ae",
    "tests-depth-budget-control-v3.py": "91533776e028ad57513611940423cd1cb2c6d8c0d85f8cafd49f089ebfd9e2d7",
    "engineer-depth-budget-probe-v2.py": "8db7415b97750e8880b25351be76b6fdf75d767a03a3a589d739113a73b6cae0",
    "tests-depth-budget-control-v2.py": "bbdc550c042fe62c8c19e838ffe35a9cabc09f22fdd4d941bdb0d9d0a41599a5",
    "engineer-depth-budget-v3-dispatch-spec-v1.md": "1b51a57c139f8c5f8743579ce56cf9c1d4b31b3b1ee7f4c5a9390e92d27ad640",
    "engineer-depth-budget-v3-static-v1.json": "45b0b5503145ed4be2f3874975681c24ed35e8561fb89d64ebe7fc1e15b75e8f",
    "engineer-generator-v26-storage.py": "1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951",
    "coordinator-preservation-baseline-v2.json": "a2f848258a6f7622161e92962b594568400bc4582bb32461aedd3c41a85d768e",
}
raws = {name: read(T / name) for name in pins}
assert all(h(raws[name]) == pin for name, pin in pins.items())
dump = lambda node: ast.dump(node, include_attributes=False)
def names(raw):
    return {node.name: node for node in ast.parse(raw).body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))}

old_probe, new_probe = (names(raws[f"engineer-depth-budget-probe-v{v}.py"]) for v in (2, 3))
for name in ("observed_init", "observed_consume", "frame_info", "install", "counted",
             "helper1050_source", "helper65_source", "generator70_source", "publication_preparation"):
    assert name in new_probe
for name in ("helper1050_source", "generator70_source", "frame_info", "install", "stage_scope"):
    assert dump(old_probe[name]) == dump(new_probe[name]), name
consume = copy.deepcopy(new_probe["observed_consume"])
# The sole delegation delta is the reviewed scalar-event block inside NameMeter observation.
meter_block, = [node for node in consume.body if isinstance(node, ast.If)
                and dump(node.test) == dump(ast.parse("frame.f_code is name_meter_code", mode="eval").body)]
assert isinstance(meter_block.body[-1], ast.If)
assert "bulk_input_iterator_requests" in ast.unparse(meter_block.body[-1].test)
meter_block.body.pop()
assert dump(consume) == dump(old_probe["observed_consume"])
control_asts = {v: ast.parse(raws[f"tests-depth-budget-control-v{v}.py"]) for v in (2, 3)}
old_control, new_control = (names(raws[f"tests-depth-budget-control-v{v}.py"]) for v in (2, 3))
stable_controls = ["require", "digest", "is_sha", "checked", "retained", "pinned",
                   "json_bytes", "create", "save", "environment_for", "git", "names",
                   "hashes", "records", "arguments"]
for name in stable_controls:
    assert dump(old_control[name]) == dump(new_control[name]), name
def constant(tree, name):
    node, = [n for n in tree.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
    return ast.literal_eval(node.value)
wrapper_old, wrapper_new = (constant(control_asts[v], "WRAPPER") for v in (2, 3))
assert wrapper_old.replace('("helper1050", "generator70")', '("helper1050", "helper65", "generator70")') == wrapper_new
assert constant(control_asts[3], "TIMEOUT") == 60
assert constant(control_asts[3], "CASES") == ("helper1050", "helper65", "generator70")
assert "PYTHONHASHSEED" not in ast.unparse(new_control["environment_for"])
assert "_name_compact" not in raws["engineer-depth-budget-probe-v3.py"].decode()
assert "plan.compacted" not in raws["engineer-depth-budget-probe-v3.py"].decode()

test_path = Path(r"D:\pontius-snapshots\focused-authority-1133dca7c2674491988f1779c196f98a\snapshot\tests\test_inventory_and_profiles.py")
test_raw = read(test_path)
assert h(test_raw) == "c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf"
design = names(test_raw)["DesignReviewTests"]
method, = [n for n in design.body if isinstance(n, ast.FunctionDef)
           and n.name == "test_round4_analysis_budget_red_contracts_are_independent"]
matches = [(owner.body, i) for owner in ast.walk(method) if isinstance(getattr(owner, "body", None), list)
           for i, n in enumerate(owner.body) if isinstance(n, ast.Assign)
           and any(isinstance(t, ast.Name) and t.id == "helper_lines" for t in n.targets)]
(original_statements, start), = matches
builder = new_probe["helper65_source"]
assert [dump(n) for n in original_statements[start:start+3]] == [dump(n) for n in builder.body[:-1]]
assert "range(65)" in ast.unparse(builder) and "index == 64" in ast.unparse(builder)
for label in ("helper1050", "helper65", "generator70"):
    assert constant(control_asts[3], "FIXTURE_SHAS")[label] == json.loads(raws["engineer-depth-budget-v3-static-v1.json"])["fixed_cases"][label]["fixture_sha256"]
for name, raw in raws.items():
    if name.endswith(".py"):
        compile(raw, str(T / name), "exec")
compile(wrapper_new, "reviewed-diagnostic-wrapper", "exec")

baseline = json.loads(raws["coordinator-preservation-baseline-v2.json"])["paths"]
baseline["tools/generate_test_inventory.py"] = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
baseline["tests/test_inventory_and_profiles.py"] = "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
assert len(baseline) == 17
assert all(h(read(W / name)) == pin for name, pin in baseline.items())
report = {"schema": "coordinator-depth-budget-v3-inspection-v1", "pins": pins,
          "old_two_fixture_builders_ast_equal": True, "helper65_original_builder_ast_equal": True,
          "original_consume_delegation_exact_after_scalar_event_removal": True,
          "unchanged_control_functions": stable_controls, "wrapper_only_adds_helper65": True,
          "all_17_preserved_paths_rehashed": True, "payload_executed_or_imported": False,
          "inspection_correction": "Initial unissued static verifier assumed the helper65 builder was a top-level method statement. It failed before any output or payload; corrected to find its unique enclosing subtest body and compare the exact contiguous construction AST.",
          "manual_review": "Read complete probe, complete changed controller and both predecessor diffs. Raw publication fields and bulk counts inspect exact builtins/private scalar fields only; original operations delegate once. Component sums are disjoint; preparation deltas are inclusive and must never be added to them. Failed publication costs become final only after unwind. No new seed or budget behavior.",
          "disposition": "Authorize root-serialized three exact fixture diagnostics on real311, fresh detached snapshots and retained raw receipts, 60s direct child watchdog each. No other tests, optimization, dev slot, W or main integration."}
data = (json.dumps(report, indent=2) + "\n").encode()
for name, raw in {"coordinator-depth-budget-v3-inspection-v1.json": data,
                  "coordinator-inspect-depth-budget-v3.py": Path(__file__).read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({"report_sha256": h(data), "scope": "three diagnostics only", "candidate_imported": False}))
