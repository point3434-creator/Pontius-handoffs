"""Root static inspection and create-only config; no reviewed code execution."""
import ast
import hashlib
import json
from pathlib import Path
import stat
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
CONTROL = "tests-checks/v28-primitive-control-v1.py"
CONTROL_SHA = "64fcb3ef0aaaf57f63643b3e306fe0f0b65f47c4d5ba8c5fc107dbe68186fcac"
CONFIG = "tests-checks/v28-primitive-config-v1.json"
REPORT = "coordinator-v28-primitive-disposition-v1.json"
COPY = "coordinator-author-v28-primitive-config-v1.py"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def safe(path):
    assert path.is_absolute() and ".." not in path.parts
    for part in (path, *path.parents):
        info = part.lstat()
        assert not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path

def read(relative, wanted):
    raw = safe(T / relative).read_bytes()
    assert sha(raw) == wanted, relative
    return raw

def create(relative, raw):
    path = T / relative
    assert path.parent.is_dir() and not path.exists()
    with path.open("xb") as stream:
        stream.write(raw)

def serialized(obj):
    return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode()

def binding_name(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
        return node.name
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        return node.targets[0].id
    return None

def node_map(raw):
    result = {}
    for node in ast.parse(raw).body:
        name = binding_name(node)
        if name:
            result.setdefault(name, []).append(node)
    return result

def unique(nodes, name):
    result = nodes[name]
    assert len(result) == 1, name
    return result[0]

def segment(raw, node):
    lines = raw.decode().splitlines()
    first = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
    return "\n".join(lines[first - 1:node.end_lineno])

assert sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.safe_path
assert str(Path(sys.executable).absolute()).lower() == r"d:\pontius-tools\py311\scripts\python.exe"
for relative in (CONFIG, REPORT, COPY):
    assert not (T / relative).exists(), relative
control_raw = read(CONTROL, CONTROL_SHA)
nodes = node_map(control_raw)
literal = lambda name: ast.literal_eval(unique(nodes, name).value)
extra, derived = literal("EXTRA_INPUTS"), literal("FROZEN_DERIVED")
old = json.loads(read("engineer-indexed-storage-config-v1.json", "60485a4ea41ab146e89c4da4fb0bfd8cfad98c0908322025e62512dfd1ce97aa"))
review_sha = "31d1d6f88ce3fa35036c618f5b4ce866a0e72bbde98eb9d8dcb6daf5c81b8733"
read("tests-checks/v28-primitive-engineering-review-mapping-v1.md", review_sha)
read("tests-checks/v28-primitive-handoff-v1.md", "224d403846622eab3770ad893d7e5a95624c88a083ceb3486b3e60350dd29b84")
config = dict(old)
config.update(extra)
config.update(derived)
config["schema"] = literal("SCHEMA")
config["control_sha256"] = CONTROL_SHA
assert config["schema"] == "v28-production-primitive-control-v1"
assert len(extra) == 8
for key in ("old_oracle", "old_cases", "cursor_oracle", "cursor_cases", "cursor_expected", "indexed_oracle", "indexed_cases", "indexed_spec", "indexed_expected", "disposition_sha256"):
    assert config[key] == old[key], key
assert config["cursor_expected"] == {"planned_cases": 16, "planned_runs": 28}
assert config["indexed_expected"] == {"planned_cases": 16, "planned_runs": 31}
inputs = {}
for key, entry in config.items():
    if type(entry) is dict and set(entry) == {"path", "sha256"}:
        relative = Path(entry["path"])
        assert not relative.is_absolute() and not relative.drive and ".." not in relative.parts
        inputs[key] = read(entry["path"], entry["sha256"])
assert len(inputs) == 17 and len({config[key]["path"] for key in inputs}) == 17
production, extracted = node_map(inputs["candidate"]), node_map(inputs["prototype"])
support = node_map(inputs["support_reference"])
proof = json.loads(inputs["extraction_proof"])
names = [item["name"] for item in proof["primitive_nodes"]]
assert len(names) == len(set(names)) == 47
assert len([name for name in extracted if name.startswith("_Name") or name.startswith("_name_") or name.startswith("_NAME_") or name == "_join_name_versions"]) == 48
for name in names:
    left, right = unique(production, name), unique(extracted, name)
    assert ast.dump(left) == ast.dump(right), name
    assert segment(inputs["candidate"], left) == segment(inputs["prototype"], right), name
for name in ("MAXIMUM_WORK", "BudgetExceeded", "Meter"):
    assert ast.dump(unique(support, name)) == ast.dump(unique(extracted, name)), name
assert ast.literal_eval(unique(extracted, "MAXIMUM_WORK").value) == 262144
accounting, old_accounting = json.loads(inputs["accounting"]), json.loads(inputs["old_accounting"])
categories = accounting["categories"]
assert len(categories) == 213 and len(old_accounting["categories"]) == 197
for name, old_value in old_accounting["categories"].items():
    assert all(categories[name][field] == old_value[field] for field in ("metric", "operation")), name
baseline_raw = read("coordinator-preservation-baseline-v2.json", "a2f848258a6f7622161e92962b594568400bc4582bb32461aedd3c41a85d768e")
preserved = json.loads(baseline_raw)["paths"]
preserved["tools/generate_test_inventory.py"] = literal("SOURCE_SHA")
preserved["tests/test_inventory_and_profiles.py"] = "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
assert len(preserved) == 17
for relative, wanted in preserved.items():
    assert sha(safe(W / relative).read_bytes()) == wanted, relative
raw = serialized(config)
report = {
    "schema": "coordinator-v28-primitive-disposition-v1",
    "config": {"path": CONFIG, "sha256": sha(raw)},
    "control_sha256": CONTROL_SHA,
    "independent_engineering_review_sha256": review_sha,
    "input_hashes": {key: sha(value) for key, value in inputs.items()},
    "exact_production_nodes_independently_compared": 47,
    "exact_original_support_nodes": 3,
    "original_categories": 197, "new_categories": 16,
    "preserved_W_paths": preserved,
    "approved_next_dispatch": {"slot": "311", "seed": "0", "runs": 93},
    "source_imported_or_payload_executed": False,
    "limits": ["One selected floor invocation; no automatic six-run expansion.",
               "314 requires successful matching floor evidence and root review.",
               "Existing finite primitive obligations only; no constructor B, production-meter, resolver or corpus claim.",
               "Actual changed-category coverage remains to be inspected; no new cases are authorized."]
}
create(COPY, Path(__file__).read_bytes())
create(CONFIG, raw)
create(REPORT, serialized(report))
print(json.dumps({"config_path": str(T / CONFIG), "config_sha256": sha(raw), "report_sha256": sha(serialized(report)), "static_only": True}))
