"""Prepare a pinned three-phase pure-storage controller; no payload execution."""
from pathlib import Path
import ast
import difflib
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
original = (T / "engineer-storage-control-v3.py").read_bytes()
sha = lambda raw: hashlib.sha256(raw).hexdigest()
assert sha(original) == "882016384c6b9bc4e6a4d9d81e829dee9eb95120942650f63006fea8f0ad1cbf"
source = original.decode().replace("\r\n", "\n")


def once(old, new):
    global source
    assert source.count(old) == 1, old
    source = source.replace(old, new)


source = source.replace("owned-name-cursor-control-v3", "indexed-name-storage-control-v1")
source = source.replace(".storage-cursor-prototype", ".storage-indexed-prototype")
source = source.replace('"cursor_control"', '"indexed_control"')
source = source.replace('"cursor-prototype-"', '"indexed-prototype-"')
source = source.replace('prefix = "cursor-"', 'prefix = "indexed-"')
once('DISPOSITION = ROOT / "coordinator-name-cursor-prototype-disposition-v1.md"',
     'DISPOSITION = ROOT / "coordinator-radix-prototype-disposition-v1.md"')
once('DISPOSITION_SHA = "973191b8b26c71132185d42203a720bdc5b28d4fd23fc1bc4b9c9ec4da46a7b7"',
     'DISPOSITION_SHA = "e8f75e760d0bb2a4b1c37c8b7cfb571624f60321b804080445c1f2b4d8e1eafa"')
once('SCHEMA = "indexed-name-storage-control-v1"', '''INDEXED_SPEC = {"path": "tests-checks/indexed-storage-extension-spec-v1.md",
                "sha256": "11d11003b3ce84d485df549e73a494e358db69cc6f5db6faea5dae8f50c330f9"}
INDEXED_CASES = {"path": "tests-checks/indexed-storage-extension-cases-v1.json",
                 "sha256": "795e893c4fbeee3963a3ea3cbbffdfacbea193f53063eb4848c8e9ac6d12984a"}
CURSOR_CASES = {"path": "tests-checks/cursor-oracle-cases-v1.json",
                "sha256": "ecddd020ffb2a0d85e624aeb7fb544f631b302839f9a5f3542c998b36c37ac61"}
SCHEMA = "indexed-name-storage-control-v1"''')
once('    wanted_files = 1771 if version == "3.14.6" else 1770',
     '    wanted_files = 1779 if version == "3.14.6" else 1774')
once('          "verified_files": len(manifest), "pontius_imported": False})',
     '          "verified_files": len(manifest), "pontius_imported": False,\n'
     '          "prototype_sha256": config["prototype"]["sha256"],\n'
     '          "accounting_sha256": config["accounting"]["sha256"]})')
once('    prototype = load("cursor_prototype_under_test", payload / "prototype.py")',
     '''    req(h(checked(payload / "prototype.py").read_bytes()) == config["prototype"]["sha256"],
        "prototype content pin")
    accounting_raw = checked(payload / "accounting.json").read_bytes()
    req(h(accounting_raw) == config["accounting"]["sha256"], "accounting content pin")
    accounting = json.loads(accounting_raw)
    req(accounting["schema"] == "pontius-indexed-storage-accounting-v1"
        and accounting["prototype_sha256"] == config["prototype"]["sha256"],
        "accounting source identity")
    prototype = load("indexed_prototype_under_test", payload / "prototype.py")''')
once('         config["cursor_expected"], config["cursor_cases"]["sha256"]),\n    )',
     '         config["cursor_expected"], config["cursor_cases"]["sha256"]),\n'
     '        ("indexed", "indexed_oracle.py", "verify_indexed", "indexed_cases.json",\n'
     '         config["indexed_expected"], config["indexed_cases"]["sha256"]),\n    )')
once('            summary = getattr(oracle, function_name)(prototype, case_path=payload / case_name)',
     '''            kwargs = {"case_path": payload / case_name}
            if phase == "indexed":
                kwargs.update(accounting_path=payload / "accounting.json",
                              accounting_sha256=config["accounting"]["sha256"])
            summary = getattr(oracle, function_name)(prototype, **kwargs)''')
once('            check(summary, expected, case_sha, version, seed)\n',
     '''            check(summary, expected, case_sha, version, seed)
            if phase == "indexed":
                req(summary.get("accounting_sha256") == config["accounting"]["sha256"]
                    and summary.get("prototype_sha256") == config["prototype"]["sha256"],
                    "indexed summary input pins")
                req(summary.get("accounting_complete") is True
                    and summary.get("fitness_passed") is True,
                    "indexed accounting or finite fitness incomplete/failed")
''')
once('                  "old_oracle", "old_cases", "cursor_oracle", "cursor_cases", "cursor_expected"}',
     '                  "old_oracle", "old_cases", "cursor_oracle", "cursor_cases", "cursor_expected",\n'
     '                  "indexed_oracle", "indexed_cases", "indexed_expected", "accounting", "indexed_spec"}')
once('        expected = config["cursor_expected"]\n',
     '''        req(config["indexed_cases"] == INDEXED_CASES and config["indexed_spec"] == INDEXED_SPEC
            and config["cursor_cases"] == CURSOR_CASES, "frozen successor/extension inputs")
        req(config["cursor_expected"] == {"planned_cases": 16, "planned_runs": 28}
            and config["indexed_expected"] == {"planned_cases": 16, "planned_runs": 31},
            "fixed finite populations")
        expected = config["cursor_expected"]
''')
once('                            ("cursor_cases", ".json")):',
     '                            ("cursor_cases", ".json"), ("indexed_oracle", ".py"),\n'
     '                            ("indexed_cases", ".json"), ("accounting", ".json"),\n'
     '                            ("indexed_spec", ".md")):')
once('        req(len(set(input_paths.values())) == 5, "input paths must be distinct")',
     '''        req(len(set(input_paths.values())) == 9, "input paths must be distinct")
        accounting = json.loads(inputs["accounting"])
        req(accounting.get("schema") == "pontius-indexed-storage-accounting-v1"
            and accounting.get("prototype_sha256") == config["prototype"]["sha256"],
            "accounting map must bind this prototype")''')
once('            "prototype", "old_oracle", "old_cases", "cursor_oracle", "cursor_cases")}',
     '            "prototype", "old_oracle", "old_cases", "cursor_oracle", "cursor_cases",\n'
     '            "indexed_oracle", "indexed_cases", "accounting", "indexed_spec") }')
once('        if slot == "314":\n            floor_relative, floor_sha = sys.argv[6:8]',
     '        floor_files = {}\n        if slot == "314":\n            floor_relative, floor_sha = sys.argv[6:8]')
once('            setup["floor_receipt"] = {"path": str(floor_path), "sha256": floor_sha}\n'
     '            input_paths["floor_receipt"] = floor_path\n'
     '            input_hashes["floor_receipt"] = floor_sha',
     '''            req(floor["before"] == floor["after"]
                and floor["manifest_after_sha256"] == floor["manifest_sha256"],
                "floor manifest receipt differs")
            floor_snapshot = validate(P(floor["snapshot"]))
            req(floor_snapshot.is_relative_to(SNAPSHOTS), "floor snapshot root")
            req(hashes(floor_snapshot, floor["before"]) == floor["before"], "floor files changed")
            req(digest(validate(floor_snapshot / PAYLOAD / "manifest.json", regular=True).read_bytes())
                == floor["manifest_sha256"], "floor manifest changed")
            floor_files["floor-receipt.json"] = floor_raw
            for key in ("setup", "stdout", "stderr", "log"):
                item = floor["outputs"][key]
                path = validate(P(item["path"]), regular=True)
                req(path.is_relative_to(ROOT), "floor output root")
                raw = path.read_bytes()
                req(digest(raw) == item["sha256"], "floor output changed: " + key)
                floor_files["floor-" + key + (".json" if key == "setup" else ".txt")] = raw
                input_paths["floor_" + key] = path
                input_hashes["floor_" + key] = item["sha256"]
            floor_records = []
            for line in floor_files["floor-stdout.txt"].splitlines():
                obj = json.loads(line)
                if isinstance(obj, dict) and isinstance(obj.get("indexed_control"), dict):
                    floor_records.append(obj["indexed_control"])
            floor_identities = [x for x in floor_records if x.get("kind") == "identity_before_payload_imports"]
            floor_results = [x for x in floor_records if x.get("kind") == "phase_result"]
            req(len(floor_identities) == 1
                and floor_identities[0]["version_info"] == [3, 11, 15]
                and P(floor_identities[0]["executable"]).resolve() == SLOTS["311"][0].resolve()
                and floor_identities[0]["hash_seed"] == seed, "actual floor identity")
            req(floor_results == floor["phase_results"] and len(floor_results) == 3,
                "floor result streams differ")
            for result, want, case_key in zip(floor_results,
                    ({"planned_cases": 28, "planned_runs": 34}, expected, config["indexed_expected"]),
                    ("old_cases", "cursor_cases", "indexed_cases"), strict=True):
                req(result.get("ok") is True, "floor phase failed")
                check_summary(result["summary"], want, config[case_key]["sha256"], "3.11.15", seed)
            setup["floor_receipt"] = {"path": str(floor_path), "sha256": floor_sha}
            input_paths["floor_receipt"] = floor_path
            input_hashes["floor_receipt"] = floor_sha''')
once('            "wrapper.py": WRAPPER.encode("utf-8"),\n',
     '            "wrapper.py": WRAPPER.encode("utf-8"),\n'
     '            "indexed_oracle.py": inputs["indexed_oracle"],\n'
     '            "indexed_cases.json": inputs["indexed_cases"],\n'
     '            "accounting.json": inputs["accounting"], "indexed_spec.md": inputs["indexed_spec"],\n'
     '            **floor_files,\n')
once('        if slot == "314":\n            files["floor_receipt.json"] = floor_raw\n', "")
once('        req(len(results) == 2 and [item.get("phase") for item in results] == ["storage", "cursor"],',
     '        req(len(results) == 3 and [item.get("phase") for item in results] == ["storage", "cursor", "indexed"],')
once('            results, ({"planned_cases": 28, "planned_runs": 34}, expected),\n'
     '            ("old_cases", "cursor_cases"), strict=True,',
     '            results, ({"planned_cases": 28, "planned_runs": 34}, expected, config["indexed_expected"]),\n'
     '            ("old_cases", "cursor_cases", "indexed_cases"), strict=True,')
once('            check_summary(item.get("summary"), want, config[case_key]["sha256"], version, seed)\n',
     '''            check_summary(item.get("summary"), want, config[case_key]["sha256"], version, seed)
            if case_key == "indexed_cases":
                summary = item["summary"]
                req(summary.get("accounting_sha256") == config["accounting"]["sha256"]
                    and summary.get("prototype_sha256") == config["prototype"]["sha256"],
                    "indexed summary inputs")
                req(summary.get("accounting_complete") is True
                    and summary.get("fitness_passed") is True, "indexed fitness/accounting failed")
''')
source = source.replace("Root-inspected finite cursor control", "Three-phase pure indexed-storage control")
source = source.replace("finite cursor oracle timed out", "finite indexed-storage oracle timed out")
compile(source, "engineer-indexed-storage-control-v1.py", "exec")
tree = ast.parse(source)
wrapper = next(n.value.value for n in tree.body if isinstance(n, ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == "WRAPPER" for t in n.targets))
compile(wrapper, "indexed-wrapper.py", "exec")
raw = source.encode()
path = T / "engineer-indexed-storage-control-v1.py"
with path.open("xb") as f:
    f.write(raw)
diff = "".join(difflib.unified_diff(original.decode().replace("\r\n", "\n").splitlines(True),
                                  source.splitlines(True), fromfile="cursor-control-v3", tofile="indexed-control-v1"))
with (T / "engineer-indexed-storage-control-v1-from-cursor-v3.diff").open("xb") as f:
    f.write(diff.encode())
with (T / "coordinator-build-indexed-storage-control-v1.py").open("xb") as f:
    f.write(Path(__file__).read_bytes())
report = {"schema": "indexed-storage-control-authoring-v1", "payload_executed": False,
          "source_sha256": sha(raw), "wrapper_sha256": sha(wrapper.encode()),
          "prototype_config_not_created": True, "planned_runs_per_child": 93,
          "scope": "Fixed34 storage +28 cursor successor +31 indexed extension"}
with (T / "engineer-checks/indexed-control-authoring-v1.json").open("x", encoding="utf-8", newline="\n") as f:
    json.dump(report, f, indent=2)
    f.write("\n")
print(json.dumps(report))
