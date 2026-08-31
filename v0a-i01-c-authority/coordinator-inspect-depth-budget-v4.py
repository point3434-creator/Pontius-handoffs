"""Inspect the scalar-only sharing observer before one bounded dispatch."""
from pathlib import Path
import ast
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
h = lambda raw: hashlib.sha256(raw).hexdigest()
pins = {
    "engineer-depth-budget-probe-v3.py": "7aa9f188b2917fec149485501eafcc4d516d3104a10b026e5ec33262b24962ae",
    "engineer-depth-budget-probe-v4.py": "559b099f96a4fcfb9b88eb05338a45ad2184ca5e153a360ee0123e0ee7969379",
    "tests-depth-budget-control-v3.py": "91533776e028ad57513611940423cd1cb2c6d8c0d85f8cafd49f089ebfd9e2d7",
    "tests-depth-budget-control-v4.py": "d62807554ffd50b7552879c5a7eb8b4b940e729063ab041d36ee9e79b823c8a5",
    "engineer-depth-budget-v4-static-v1.json": "214f1558b94134a8480e327bd438f81eaeb0db527404a1edb3f082198844b721",
    "engineer-generator-v26-storage.py": "1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951",
}
raw = {name: (T / name).read_bytes() for name in pins}
assert all(h(raw[name]) == pin for name, pin in pins.items())
assert raw["tests-depth-budget-control-v3.py"].replace(
    pins["engineer-depth-budget-probe-v3.py"].encode(), pins["engineer-depth-budget-probe-v4.py"].encode()).replace(
    b"engineer-depth-budget-probe-v3.py", b"engineer-depth-budget-probe-v4.py") == raw["tests-depth-budget-control-v4.py"]
old, new = (ast.parse(raw[f"engineer-depth-budget-probe-v{v}.py"]) for v in (3, 4))
dump = lambda n: ast.dump(n, include_attributes=False)
old_funcs = {n.name: n for n in old.body if isinstance(n, ast.FunctionDef)}
new_funcs = {n.name: n for n in new.body if isinstance(n, ast.FunctionDef)}
assert set(new_funcs) - set(old_funcs) == {"raw_full_join_sharing"}
changed = {name for name in old_funcs if dump(old_funcs[name]) != dump(new_funcs[name])}
assert changed == {"observed_init", "record_bulk_shape", "summary"}
assert [dump(n) for n in old.body if not isinstance(n, ast.FunctionDef)] == [dump(n) for n in new.body if not isinstance(n, ast.FunctionDef)]
new_helper = new_funcs["raw_full_join_sharing"]
assert not any(isinstance(n, (ast.Global, ast.Nonlocal, ast.Import, ast.ImportFrom)) for n in ast.walk(new_helper))
assert not any(isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store) for n in ast.walk(new_helper))
calls = {ast.unparse(n.func) for n in ast.walk(new_helper) if isinstance(n, ast.Call)}
assert calls <= {"all", "bool", "len", "local.get", "object.__getattribute__", "pending_rows.append",
                 "tuple", "type", "vars", "vars(authority).get", "vars(resolver).get", "vars(source).get"}
for name, data in raw.items():
    if name.endswith(".py"):
        compile(data, str(T / name), "exec")
report = {"schema": "coordinator-depth-budget-v4-inspection-v1", "pins": pins,
          "changed_existing_probe_functions": sorted(changed), "control_only_probe_pin_and_name": True,
          "delegation_and_fixture_builders_unchanged": True, "allowed_raw_observer_calls": sorted(calls),
          "manual_review": "Read the complete new helper and both exact diffs. Full-join event observes versions after original snapshots, exact source/meter/budget identity and raw pending counts. Only bool/int signatures escape; no public Mapping reads, candidate callbacks, live state retention or changes. Exact existing corpus fixture and absent hash seed preserved.",
          "disposition": "Root may run one fresh generator70 diagnostic on v26 real311, 60s direct-child watchdog. No other payload or C implementation is authorized. Utility remains unknown until the completed data are verified.",
          "payload_executed_or_imported": False}
data = (json.dumps(report, indent=2) + "\n").encode()
for name, content in {"coordinator-depth-budget-v4-inspection-v1.json": data,
                      "coordinator-inspect-depth-budget-v4.py": Path(__file__).read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(content)
print(json.dumps({"report_sha256": h(data), "dispatch_scope": "one generator70 diagnostic"}))
