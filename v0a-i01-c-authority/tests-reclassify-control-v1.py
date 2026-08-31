import ast
import hashlib
from pathlib import Path
import sys

assert sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15)
assert Path(sys.executable).resolve() == Path(r"D:\Pontius-tools\py311\Scripts\python.exe").resolve()
assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path
root = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
original = (root / "tests-additions-v2.py").read_text(encoding="utf-8")
first = '''                        classification="refuse" if mode == "write" else "clean",
                        unreachable=dead,'''
first_new = '''                        classification=(
                            "permitted-refusal"
                            if route in {"return", "returned-nest", "flat-store"}
                            and mode in {"readonly", "raise-before"}
                            else "refuse" if mode == "write" else "clean"
                        ),
                        unreachable=dead,'''
second = '''                            classification="refuse" if writes else "clean",
                        ))
        for capture in ("default", "cell"):'''
second_new = '''                            classification=(
                                "permitted-refusal"
                                if capture == "cell" and not upward and not rebound_before_return
                                else "refuse" if writes else "clean"
                            ),
                        ))
        for capture in ("default", "cell"):'''
assert original.count(first) == original.count(second) == 1
revised = original.replace(first, first_new).replace(second, second_new)
assert all(len(line) <= 100 for line in revised.splitlines())
old_tree, new_tree = ast.parse(original), ast.parse(revised)
old_class, = old_tree.body
new_class, = new_tree.body
changed_methods = []
for old, new in zip(old_class.body, new_class.body):
    if ast.dump(old) == ast.dump(new):
        continue
    assert isinstance(old, ast.FunctionDef) and isinstance(new, ast.FunctionDef)
    assert old.name == new.name
    old_keywords = [n for n in ast.walk(old) if isinstance(n, ast.keyword) and n.arg == "classification"]
    new_keywords = [n for n in ast.walk(new) if isinstance(n, ast.keyword) and n.arg == "classification"]
    changes = [(a, b) for a, b in zip(old_keywords, new_keywords) if ast.dump(a) != ast.dump(b)]
    assert len(changes) == 1
    changes[0][1].value = changes[0][0].value
    assert ast.dump(old) == ast.dump(new), "a change exceeded classification"
    changed_methods.append(old.name)
assert changed_methods == [
    "test_authority_transfer_capture_route_execution_matrix",
    "test_authority_transfer_live_cells_and_activation_identity",
]
raw = revised.encode("utf-8")
assert b"\r" not in raw
with (root / "tests-additions-v3.py").open("xb") as stream:
    stream.write(raw)
print(hashlib.sha256(raw).hexdigest())

