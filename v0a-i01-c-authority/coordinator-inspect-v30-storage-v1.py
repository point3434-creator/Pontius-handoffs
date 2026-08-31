"""Independent source-only inspection; issue no execution or integration claim."""
import ast
import hashlib
import json
from pathlib import Path

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
h = lambda raw: hashlib.sha256(raw).hexdigest()
pins = {
    "engineer-generator-v30-storage.py": "1a28fce14cfdd2ee30d9892b7d2719aba8ec152d99d1e3c915660648cf9756fd",
    "engineer-generator-v29-storage.py": "b53b905cd20dd97d7d09a3b81f955bf27498a572ce8a6d82e20f007993ab9466",
    "engineer-generator-v28-storage.py": "4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e",
    "engineer-generator-v30-storage-from-v29.diff": "d50c98213038bbedd0060c5136b8150b7e33832a64d406af8f33801863517fff",
    "engineer-generator-v30-storage-accounting-v1.json": "8d89ca2da1d66b5e52ee1eb6d12925b3972e7f96762869d185b098dd7581a094",
    "engineer-generator-v29-storage-accounting-v1.json": "5074f3509e47d1de642b30f5351dd953997397b4e29a841cc59ae92c6c7d292d",
    "tests-checks/v29-disabled-join-engineering-review-codex-a-v1.md": "f397975e37f00ea9512563e91dea9bc89ae7f9dda2ce96ab2f5ed5ba1dc610ad",
    "engineer-v30-enumerate-accounting-plan-v1.md": "a6fbc28533102f86341daac86cb76761517e2b2770421d29c6b8d94381bdf983",
}
raws = {name: (T / name).read_bytes() for name in pins}
assert all(h(raws[name]) == digest for name, digest in pins.items())
new, old = raws["engineer-generator-v30-storage.py"], raws["engineer-generator-v29-storage.py"]
insert = (b'                                join_meter.charge("disabled_join_input_pair_allocation")\n'
          b'                                join_meter.charge("disabled_join_input_pair_reference_copies", 2)\n')
assert new.count(insert) == 1 and new.replace(insert, b"", 1) == old
before, after = ast.parse(old), ast.parse(new)
selected = {"disabled_join_input_pair_allocation", "disabled_join_input_pair_reference_copies"}
sites = []
class Remove(ast.NodeTransformer):
    def visit_Expr(self, node):
        value = node.value
        if (isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute)
                and isinstance(value.func.value, ast.Name) and value.func.value.id == "join_meter"
                and value.func.attr == "charge" and value.args and isinstance(value.args[0], ast.Constant)
                and value.args[0].value in selected):
            assert not value.keywords
            units = ast.literal_eval(value.args[1]) if len(value.args) == 2 else 1
            sites.append({"name": value.args[0].value, "units": units, "line": node.lineno})
            return None
        return self.generic_visit(node)
stripped = Remove().visit(after)
assert len(sites) == 2 and ast.dump(stripped) == ast.dump(before)
assert {row["name"]: row["units"] for row in sites} == {"disabled_join_input_pair_allocation": 1, "disabled_join_input_pair_reference_copies": 2}
old_acc = json.loads(raws["engineer-generator-v29-storage-accounting-v1.json"])["categories"]
new_acc = json.loads(raws["engineer-generator-v30-storage-accounting-v1.json"])["categories"]
assert set(new_acc) - set(old_acc) == selected and len(old_acc) == 279
for name, value in old_acc.items():
    assert all(new_acc[name][key] == value[key] for key in ("metric", "operation", "origin")), name
    old_sites = [(row["function"], row["units"]) for row in value["source_sites"]]
    new_sites = [(row["function"], row["units"]) for row in new_acc[name]["source_sites"]]
    assert old_sites == new_sites, name
assert new_acc["disabled_join_input_pair_allocation"]["metric"] == "non-P"
assert new_acc["disabled_join_input_pair_reference_copies"]["metric"] == "P"
baseline = json.loads((T / "coordinator-preservation-baseline-v2.json").read_bytes())["paths"]
baseline["tools/generate_test_inventory.py"] = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
baseline["tests/test_inventory_and_profiles.py"] = "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
assert len(baseline) == 17 and all(h((W / name).read_bytes()) == pin for name, pin in baseline.items())
report = {"schema": "coordinator-v30-storage-inspection-v1", "pins": pins,
          "inverse_bytes_and_AST_match_v29": True, "new_sites": sites, "old_category_meanings_and_units_preserved": 279,
          "preserved_W_paths": baseline, "reviewed_v29_identity_order_pending_debt_and_staging_contract_unchanged": True,
          "payload_or_source_executed": False, "next_authorized_dispatch": "One new actual311 focused design run using frozen v5 tests; failed floor does not authorize dev/matrix/corpus.",
          "limits": ["Source-only review closes the identified pair-accounting omission, not runtime fitness.",
                     "v28 primitive evidence remains bounded; this adapter branch needs real analyzer results.",
                     "No semantic composition or source integration approved."]}
out = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
for name, content in (("coordinator-inspect-v30-storage-v1.py", Path(__file__).read_bytes()), ("coordinator-v30-storage-inspection-v1.json", out)):
    assert not (T / name).exists()
    with (T / name).open("xb") as stream:
        stream.write(content)
print(json.dumps({"source_sha256": h(new), "report_sha256": h(out), "static_only": True}))
