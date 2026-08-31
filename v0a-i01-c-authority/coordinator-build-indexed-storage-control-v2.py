"""Complete output custody and explicit identity verification before any dispatch."""
from pathlib import Path
import ast
import difflib
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
sha = lambda b: hashlib.sha256(b).hexdigest()
before = (T / "engineer-indexed-storage-control-v1.py").read_bytes()
assert sha(before) == "dc0f841b1061fbce47e3980acfa0a9428c96b16c3ce3a7c857962a4595d08de4"
text = before.decode()
old = '''        req(len(identities) == 1 and identities[0].get("verified_files") == len(before),
            "missing/duplicate pre-import identity")'''
new = old + '''
        identity = identities[0]
        req(identity.get("implementation") == "cpython"
            and identity.get("version_info") == [int(p) for p in version.split(".")]
            and P(identity["executable"]).resolve() == exe.resolve(), "actual payload runtime")
        req(identity.get("cwd") == str(snapshot) and identity.get("environment") == env
            and identity.get("hash_seed") == seed and identity.get("manifest_sha256") == manifest_sha
            and identity.get("prototype_sha256") == config["prototype"]["sha256"]
            and identity.get("accounting_sha256") == config["accounting"]["sha256"]
            and identity.get("pontius_imported") is False, "payload identity context")'''
assert text.count(old) == 1
text = text.replace(old, new)
old = '''        receipt["success"] = (
            receipt.get("result_ok") is True and receipt["integrity_ok"]'''
new = '''        receipt["outputs"] = {
            key: {"path": str(paths[key]), "sha256": digest(paths[key].read_bytes())}
            for key in ("setup", "stdout", "stderr", "log")
        }
''' + old
assert text.count(old) == 1
text = text.replace(old, new)
old = '''            setup["floor_receipt"] = {"path": str(floor_path), "sha256": floor_sha}'''
new = '''            indexed_summary = floor_results[-1]["summary"]
            req(indexed_summary.get("accounting_complete") is True
                and indexed_summary.get("fitness_passed") is True
                and indexed_summary.get("accounting_sha256") == config["accounting"]["sha256"]
                and indexed_summary.get("prototype_sha256") == config["prototype"]["sha256"],
                "floor indexed fitness/accounting")
''' + old
assert text.count(old) == 1
text = text.replace(old, new)
compile(text, "engineer-indexed-storage-control-v2.py", "exec")
tree = ast.parse(text)
wrapper = next(n.value.value for n in tree.body if isinstance(n, ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == "WRAPPER" for t in n.targets))
compile(wrapper, "indexed-wrapper.py", "exec")
after = text.encode()
with (T / "engineer-indexed-storage-control-v2.py").open("xb") as f:
    f.write(after)
diff = "".join(difflib.unified_diff(before.decode().splitlines(True), text.splitlines(True),
                                  fromfile="indexed-control-v1", tofile="indexed-control-v2"))
with (T / "engineer-indexed-storage-control-v2-from-v1.diff").open("xb") as f:
    f.write(diff.encode())
with (T / "coordinator-build-indexed-storage-control-v2.py").open("xb") as f:
    f.write(Path(__file__).read_bytes())
report = {"schema": "indexed-storage-control-authoring-v2", "payload_executed": False,
          "source_sha256": sha(after), "wrapper_sha256": sha(wrapper.encode()),
          "v1_disposition": "Unexecuted; missing output map would block developer-floor custody",
          "prototype_config_not_created": True}
with (T / "engineer-checks/indexed-control-authoring-v2.json").open("x", encoding="utf-8", newline="\n") as f:
    json.dump(report, f, indent=2)
    f.write("\n")
print(json.dumps(report))
