import sys
assert sys.version_info[:3] == (3, 11, 15), sys.version
assert sys.executable.replace("\\", "/").lower() == "d:/pontius-tools/py311/scripts/python.exe"
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
assert sys.dont_write_bytecode and sys.flags.optimize == 0

import ast
from collections import Counter
import difflib
import hashlib
import json
from pathlib import Path

BASE = Path("D:/Pontius-handoffs/v0a-i01-c-authority/tests-checks")
PINS = {
    "cursor-oracle-v1.py": "15a4741e2532a755fd45f01d4d999dd5d293846b8ae4e9d4e7abedf84c0a8d1e",
    "cursor-oracle-v2.py": "145fe1d59c48e23cdb426bcbe35edbecc3f941a81dc9780e8eeed849be5bc143",
    "cursor-oracle-cases-v1.json": "ecddd020ffb2a0d85e624aeb7fb544f631b302839f9a5f3542c998b36c37ac61",
    "storage-oracle-v2.py": "6a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba",
    "storage-oracle-cases-v2.json": "3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f",
    "indexed-storage-extension-oracle-v1.py": "135983d43d271add4875cda4ab5144f6aaaadff21928637985740229f3a3f006",
    "indexed-storage-extension-cases-v1.json": "795e893c4fbeee3963a3ea3cbbffdfacbea193f53063eb4848c8e9ac6d12984a",
    "indexed-storage-extension-spec-v1.md": "11d11003b3ce84d485df549e73a494e358db69cc6f5db6faea5dae8f50c330f9",
    "indexed-storage-p-boundary-clarification-v1.md": "cdc1f9aa5f66114d744e2bc66728f4a64f85032a7b25399a9c0a4c728cb28cb8",
}
raws = {}
for name, expected in PINS.items():
    raw = (BASE / name).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected, name
    assert b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf") and raw.endswith(b"\n"), name
    raws[name] = raw
old = raws["cursor-oracle-v1.py"].decode("utf-8")
new = raws["cursor-oracle-v2.py"].decode("utf-8")
extension = raws["indexed-storage-extension-oracle-v1.py"].decode("utf-8")
old_tree = ast.parse(old, filename="cursor-oracle-v1.py")
new_tree = ast.parse(new, filename="cursor-oracle-v2.py")
extension_tree = ast.parse(extension, filename="indexed-storage-extension-oracle-v1.py")
def definitions(tree):
    return {node.name: node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
old_defs, new_defs = definitions(old_tree), definitions(new_tree)
assert set(old_defs) == set(new_defs)
changed = sorted(name for name in old_defs
                 if ast.dump(old_defs[name], include_attributes=False)
                 != ast.dump(new_defs[name], include_attributes=False))
assert changed == ["retention_case", "verify_cursor"], changed
for name in set(old_defs) - set(changed):
    assert ast.dump(old_defs[name], include_attributes=False) == ast.dump(new_defs[name], include_attributes=False)
def ledger_calls(function):
    return [ast.dump(node, include_attributes=False) for node in ast.walk(function)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "call" and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "ledger"]
assert Counter(ledger_calls(old_defs["retention_case"])) == Counter(ledger_calls(new_defs["retention_case"]))
old_asserts = Counter(ast.dump(node, include_attributes=False)
                     for node in ast.walk(old_defs["retention_case"]) if isinstance(node, ast.Assert))
new_asserts = Counter(ast.dump(node, include_attributes=False)
                     for node in ast.walk(new_defs["retention_case"]) if isinstance(node, ast.Assert))
assert old_asserts <= new_asserts
old_pack = json.loads(raws["cursor-oracle-cases-v1.json"])
retention = next(case for case in old_pack["cases"] if case["kind"] == "retention_history")
assert retention["publications"] == 24
assert old_pack["planned_cases"] == 16 and old_pack["planned_runs"] == 28
pack = json.loads(raws["indexed-storage-extension-cases-v1.json"])
assert pack["planned_cases"] == len(pack["cases"]) == 16
assert pack["planned_runs"] == sum(case["runs"] for case in pack["cases"]) == 31
assert sum(case["family"] == "atomic" for case in pack["cases"]) == 5
assert pack["fault_offsets"] == ["first", "middle", "last"]
ext_defs = definitions(extension_tree)
entry = ext_defs["verify_indexed"]
assert [arg.arg for arg in entry.args.args] == ["api", "case_path", "accounting_path", "accounting_sha256"]
for name in ("growing_case", "hot_case", "collision_case", "bulk_case", "retention_case", "atomic_case"):
    assert name in ext_defs
prohibited = []
for node in ast.walk(extension_tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id in {"exec", "eval", "compile", "__import__"}:
            prohibited.append(node.func.id)
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        names = ([alias.name for alias in node.names] if isinstance(node, ast.Import)
                 else [node.module])
        if any(name.split(".")[0] in {"subprocess", "importlib", "pickle"} for name in names):
            prohibited.extend(names)
assert not prohibited
assert not any(isinstance(node, ast.If) for node in extension_tree.body), "unexpected autorun guard"
constants = {}
for node in extension_tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        try:
            constants[node.targets[0].id] = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            pass
assert constants["MAXIMUM"] == 262144
assert constants["CASE_SHA256"] == PINS["indexed-storage-extension-cases-v1.json"]
assert constants["SPEC_SHA256"] == PINS["indexed-storage-extension-spec-v1.md"]
parts = b"".join((BASE / ("indexed-storage-oracle-source-part" + str(i) + "-v1.txt")).read_bytes()
                 for i in (1, 2, 3))
assert parts == raws["indexed-storage-extension-oracle-v1.py"]
diffs = {
    "cursor-oracle-v2-from-v1.diff": "".join(difflib.unified_diff(
        old.splitlines(keepends=True), new.splitlines(keepends=True),
        fromfile="cursor-oracle-v1.py", tofile="cursor-oracle-v2.py")),
    "indexed-storage-extension-oracle-v1-from-empty.diff": "".join(difflib.unified_diff(
        [], extension.splitlines(keepends=True),
        fromfile="/dev/null", tofile="indexed-storage-extension-oracle-v1.py")),
}
outputs = {}
for name, text in diffs.items():
    data = text.encode("utf-8")
    with (BASE / name).open("xb") as stream:
        stream.write(data)
    outputs[name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
proof = {
    "schema": "pontius-indexed-oracle-static-proof-v1",
    "static_only": True, "oracle_or_prototype_imported": False, "payload_executed": False,
    "runtime": list(sys.version_info[:3]), "full_version": sys.version,
    "executable": sys.executable, "flags": {"isolated": True, "no_site": True,
        "safe_path": True, "dont_write_bytecode": True, "optimize": 0},
    "inputs": {name: {"sha256": PINS[name], "bytes": len(raw)} for name, raw in raws.items()},
    "parsed_sources": ["cursor-oracle-v1.py", "cursor-oracle-v2.py", "indexed-storage-extension-oracle-v1.py"],
    "cursor_changed_definitions": changed,
    "cursor_unchanged_definition_count": len(old_defs) - len(changed),
    "cursor_retention_ledger_calls_multiset_unchanged": True,
    "cursor_original_retention_assertions_preserved": True,
    "cursor_original_retention_publications": retention["publications"],
    "cursor_case_pack_unchanged": True, "old_storage_inputs_unchanged": True,
    "indexed_cases": 16, "indexed_runs": 31, "atomic_schedules": 5,
    "indexed_entrypoint": "verify_indexed(api, case_path, accounting_path, accounting_sha256)",
    "prohibited_dynamic_execution_or_process_imports": prohibited,
    "source_parts_exact_concatenation": True,
    "diffs": outputs,
    "scope_limit": "AST/data/hash inspection only; no runtime oracle or prototype behavior is established",
}
proof["static_control_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
data = (json.dumps(proof, indent=2) + "\n").encode("utf-8")
path = BASE / "indexed-storage-oracles-static-proof-v1.json"
with path.open("xb") as stream:
    stream.write(data)
print(json.dumps({"static_complete": True, "proof_path": str(path),
                  "proof_sha256": hashlib.sha256(data).hexdigest(), "diffs": outputs}), flush=True)
