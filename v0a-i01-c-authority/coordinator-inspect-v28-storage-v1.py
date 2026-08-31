"""Static root inspection of exactly two bounded v26 successor edits."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import stat

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
h = lambda raw: hashlib.sha256(raw).hexdigest()
def read(path):
    assert path.is_absolute() and ".." not in path.parts
    for parent in (path, *path.parents):
        assert not getattr(parent.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path.read_bytes()
pins = {
    "engineer-generator-v26-storage.py": "1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951",
    "engineer-generator-v28-storage.py": "4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e",
    "engineer-generator-v28-storage-static-v1.json": "cd0fc65d3df53188d3f8aa909ca9a14fc7409c549d27113b34e2268f98c9fff4",
    "engineer-generator-v28-storage-handoff-v1.md": "c5fb62960cf6a74e2677eb6f842cbf20b4e966fac0b55a76fbf5a7def73a5b74",
    "engineer-v26-cost-remedy-plan-v1.md": "e32d45c914cf9422429f493b3dfec475e23d05d58f957dca896ec95b75bb2d93",
    "engineer-v26-cost-remedy-clarification-v2.md": "7a4e338e5ed990df6cfa2d850638833362036558f649ae626ea0e0472239fce5",
    "coordinator-v26-storage-inspection-v1.json": "37937253b7b483429607d1d54341c5cf9e80c0344b1cf123d3ee2145ebe52084",
    "coordinator-preservation-baseline-v2.json": "a2f848258a6f7622161e92962b594568400bc4582bb32461aedd3c41a85d768e",
}
raws = {name: read(T / name) for name in pins}
assert all(h(raws[name]) == pin for name, pin in pins.items())
old = ast.parse(raws["engineer-generator-v26-storage.py"])
new = ast.parse(raws["engineer-generator-v28-storage.py"])
dump = lambda n: ast.dump(n, include_attributes=False)
def named(tree):
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
a, b = named(old), named(new)
assert set(a) == set(b)
changed = {name for name in a if dump(a[name]) != dump(b[name])}
assert changed == {"_name_radix_freeze", "_SourceOrderedResolver"}
am, bm = named(a["_SourceOrderedResolver"]), named(b["_SourceOrderedResolver"])
assert set(am) == set(bm)
assert {name for name in am if dump(am[name]) != dump(bm[name])} == {"__init__"}
original_update = ast.parse("self.values.update(entry_values or {})").body[0]
position, = [i for i, n in enumerate(am["__init__"].body) if dump(n) == dump(original_update)]
following = am["__init__"].body[position + 1]
new_position, = [i for i, n in enumerate(bm["__init__"].body) if dump(n) == dump(following)]
assert [dump(n) for n in am["__init__"].body[:position]] == [dump(n) for n in bm["__init__"].body[:position]]
assert [dump(n) for n in am["__init__"].body[position+1:]] == [dump(n) for n in bm["__init__"].body[new_position:]]
guard = bm["__init__"].body[position:new_position]
assert guard and all(not isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef)) for n in guard)
assert ast.unparse(guard[-1].body[0].test) == "entry_values"
assert dump(guard[-1].orelse[0]) == dump(original_update)
fixed = copy.deepcopy(new)
fixed.body = [copy.deepcopy(a[n.name]) if isinstance(n, (ast.FunctionDef, ast.ClassDef))
              and n.name in changed else n for n in fixed.body]
assert dump(fixed) == dump(old)
compile(raws["engineer-generator-v28-storage.py"], str(T / "engineer-generator-v28-storage.py"), "exec")
baseline = json.loads(raws["coordinator-preservation-baseline-v2.json"])["paths"]
baseline["tools/generate_test_inventory.py"] = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
baseline["tests/test_inventory_and_profiles.py"] = "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
assert len(baseline) == 17 and all(h(read(W / name)) == pin for name, pin in baseline.items())
report = {"schema": "coordinator-v28-storage-inspection-v1", "pins": pins,
          "only_changed_top_level_nodes": sorted(changed), "only_changed_resolver_method": "__init__",
          "all_other_module_ast_equal": True, "constructor_prefix_suffix_exact": True,
          "all17_preserved_paths_rehashed": True, "candidate_executed_or_imported": False,
          "manual_review": "Read full exact delta and handoff against both approved plans. Freeze stages unpublished children, uses immutable old pending counts and evolving ranks, charges physical shifts/copies, and preserves suffix/new-branch path. Late borrow requires exact empty prepared mapping, exact internal entry/scope/registry and empty exact binding sets; no subsequent name loop executes, custom/falsey paths stay legacy, final existing parent fork remains. No C shortcut or semantic repair is included.",
          "disposition": "Run unchanged original design53 on actual311 in a fresh snapshot. No dev/matrix/corpus expansion or W/main install. Primitive freeze requirements remain pending regardless of design result; helper1050's assertion wording issue is separately recorded, not silently reclassified as pass."}
data = (json.dumps(report, indent=2) + "\n").encode()
for name, raw in {"coordinator-v28-storage-inspection-v1.json": data,
                  "coordinator-inspect-v28-storage-v1.py": Path(__file__).read_bytes()}.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({"report_sha256": h(data), "scope": "original design53 floor only"}))
