"""Align the packaged spec filename and preserve exact evidence-field types."""
from pathlib import Path
import ast
import difflib
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
sha = lambda raw: hashlib.sha256(raw).hexdigest()
before = (T / "engineer-indexed-storage-control-v3.py").read_bytes()
assert sha(before) == "06b0ae9be2ea962b94b838171d4df3692f02f63119b65e404270b18883ee44bb"
source = before.decode()
replacements = [
    ('"accounting.json": inputs["accounting"], "indexed_spec.md": inputs["indexed_spec"],',
     '"accounting.json": inputs["accounting"],\n'
     '            "indexed-storage-extension-spec-v1.md": inputs["indexed_spec"],'),
    ('and floor.get("exit") == 0, "floor did not succeed")',
     'and type(floor.get("exit")) is int and floor["exit"] == 0\n'
     '                and floor.get("payload_started") is True\n'
     '                and floor.get("result_ok") is True, "floor did not succeed")'),
    ('and floor_completed == [{"kind": "completed", "ok": True}],',
     'and floor_completed == [{"kind": "completed", "ok": True}]\n'
     '                and floor_completed[0].get("ok") is True,'),
    ('and completed == [{"kind": "completed", "ok": True}],',
     'and completed == [{"kind": "completed", "ok": True}]\n'
     '            and completed[0].get("ok") is True,'),
]
for old, new in replacements:
    assert source.count(old) == 1, old
    source = source.replace(old, new)
tree = ast.parse(source)
compile(tree, "engineer-indexed-storage-control-v4.py", "exec")
wrapper = next(node.value.value for node in tree.body if isinstance(node, ast.Assign)
               and any(isinstance(target, ast.Name) and target.id == "WRAPPER"
                       for target in node.targets))
assert sha(wrapper.encode()) == "f55429bf5d3f404b5d9705957694b05c33b25b8c36b33433fcc8f166fb66ff2d"
after = source.encode()
diff = "".join(difflib.unified_diff(before.decode().splitlines(True), source.splitlines(True),
                                 fromfile="indexed-control-v3", tofile="indexed-control-v4"))
report = {"schema": "indexed-storage-control-authoring-v4", "payload_executed": False,
          "source_sha256": sha(after), "wrapper_sha256": sha(wrapper.encode()),
          "v3_disposition": "Unexecuted; correct spec basename and exact completion/exit types",
          "prototype_config_not_created": True}
for relative, raw in {
    "engineer-indexed-storage-control-v4.py": after,
    "engineer-indexed-storage-control-v4-from-v3.diff": diff.encode(),
    "coordinator-build-indexed-storage-control-v4.py": Path(__file__).read_bytes(),
    "engineer-checks/indexed-control-authoring-v4.json":
        (json.dumps(report, indent=2) + "\n").encode(),
}.items():
    with (T / relative).open("xb") as stream:
        stream.write(raw)
print(json.dumps(report))
