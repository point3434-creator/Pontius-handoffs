"""Complete raw floor replay before any indexed prototype dispatch."""
from pathlib import Path
import ast
import difflib
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
sha = lambda raw: hashlib.sha256(raw).hexdigest()
before = (T / "engineer-indexed-storage-control-v2.py").read_bytes()
assert sha(before) == "44caaf76756aec5d34eaa20ac7f25f2321e89d17306e06e4fe3b12fbf1bedf9b"
source = before.decode()
old = '''            floor_identities = [x for x in floor_records if x.get("kind") == "identity_before_payload_imports"]
            floor_results = [x for x in floor_records if x.get("kind") == "phase_result"]'''
new = old + '''
            floor_completed = [x for x in floor_records if x.get("kind") == "completed"]
            floor_setup = json.loads(floor_files["floor-setup.json"])
            req(type(floor_setup) is dict
                and all(key in floor and floor[key] == value
                        for key, value in floor_setup.items()), "floor setup/receipt differ")
            req(floor_records == floor.get("retained_control_records")
                and floor_identities == floor.get("identity_records")
                and floor_completed == floor.get("completed_records"),
                "floor raw identity/completion streams differ")
            req([x.get("kind") for x in floor_records] == [
                    "identity_before_payload_imports", "phase_result", "phase_result",
                    "phase_result", "completed"]
                and [x.get("phase") for x in floor_results] == ["storage", "cursor", "indexed"]
                and floor_completed == [{"kind": "completed", "ok": True}],
                "floor record order/completion")
            floor_identity = floor_identities[0]
            req(floor_identity.get("implementation") == "cpython"
                and floor_identity.get("cwd") == str(floor_snapshot)
                and floor_identity.get("environment") == floor_setup["environment"]
                and floor_identity.get("manifest_sha256") == floor_setup["manifest_sha256"]
                and floor_identity.get("verified_files") == len(floor["before"]) == 1774
                and floor_identity.get("prototype_sha256") == config["prototype"]["sha256"]
                and floor_identity.get("accounting_sha256") == config["accounting"]["sha256"]
                and floor_identity.get("pontius_imported") is False,
                "floor raw identity context")
            req(floor_setup["config"] == config
                and floor_setup["snapshot"] == str(floor_snapshot)
                and floor_setup["before"] == floor["before"]
                and floor_setup["input_hashes_before"] == wanted_hashes,
                "floor setup input context")'''
assert source.count(old) == 1
source = source.replace(old, new)
old = '''        req(len(completed) == 1 and completed[0].get("ok") is True,
            "child completion missing or false")'''
new = '''        req([item.get("kind") for item in records] == [
                "identity_before_payload_imports", "phase_result", "phase_result",
                "phase_result", "completed"]
            and completed == [{"kind": "completed", "ok": True}],
            "child record order/completion")'''
assert source.count(old) == 1
source = source.replace(old, new)
tree = ast.parse(source)
compile(tree, "engineer-indexed-storage-control-v3.py", "exec")
wrapper = next(node.value.value for node in tree.body if isinstance(node, ast.Assign)
               and any(isinstance(target, ast.Name) and target.id == "WRAPPER"
                       for target in node.targets))
assert sha(wrapper.encode()) == "f55429bf5d3f404b5d9705957694b05c33b25b8c36b33433fcc8f166fb66ff2d"
after = source.encode()
diff = "".join(difflib.unified_diff(before.decode().splitlines(True), source.splitlines(True),
                                 fromfile="indexed-control-v2", tofile="indexed-control-v3"))
report = {"schema": "indexed-storage-control-authoring-v3", "payload_executed": False,
          "source_sha256": sha(after), "wrapper_sha256": sha(wrapper.encode()),
          "v2_disposition": "Unexecuted; complete raw floor identity and completion replay added",
          "prototype_config_not_created": True}
for relative, raw in {
    "engineer-indexed-storage-control-v3.py": after,
    "engineer-indexed-storage-control-v3-from-v2.diff": diff.encode(),
    "coordinator-build-indexed-storage-control-v3.py": Path(__file__).read_bytes(),
    "engineer-checks/indexed-control-authoring-v3.json":
        (json.dumps(report, indent=2) + "\n").encode(),
}.items():
    with (T / relative).open("xb") as stream:
        stream.write(raw)
print(json.dumps(report))
