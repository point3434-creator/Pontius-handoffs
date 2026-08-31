"""Create-only controller derivation; compile-only, no payload dispatch."""
import ast
import difflib
import hashlib
import json
from pathlib import Path

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
def h(raw):
    return hashlib.sha256(raw).hexdigest()
def write(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
oldpath = T / "engineer-indexed-storage-control-v4.py"
oldraw = oldpath.read_bytes()
assert h(oldraw) == "7192e46cd855d767c96a06ba81ffaa97c97604e12042fad5e06e299f10a5e44c"
text = oldraw.decode()
def one(old, new):
    global text
    assert text.count(old) == 1, (old[:100], text.count(old))
    text = text.replace(old, new)
def all_text(old, new, count):
    global text
    assert text.count(old) == count, (old, text.count(old), count)
    text = text.replace(old, new)

extras = {
 "candidate": {"path": "engineer-generator-v28-storage.py", "sha256": "4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e"},
 "support_reference": {"path": "engineer-name-radix-prototype-v1.py", "sha256": "0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71"},
 "production_binding": {"path": "engineer-generator-v28-storage-binding-proof-v1.json", "sha256": "d786b9a609a37bf88ea18d6d6585d2ffb6cafd6ced908d23c1e086291ed8650c"},
 "production_accounting": {"path": "engineer-generator-v28-storage-accounting-v1.json", "sha256": "077c1b4779709672a79368ea1081ecd9cb0499c651851a571a80f075e983c45b"},
 "old_accounting": {"path": "engineer-name-radix-accounting-v1.json", "sha256": "79f64e5e7bbb429bedd108654b69c8ab5893973ee742517b543129f762f68f2b"},
 "extractor": {"path": "tests-checks/v28-primitive-extractor-v2.py", "sha256": "96f3e980751e0d4851b95340e894c9519b96241fc726d1fac30d324fd99d6d9f"},
 "extraction_proof": {"path": "tests-checks/v28-primitive-extraction-proof-v1.json", "sha256": "8b6269d44aecaca6a4df93947439e0f54090b4dedb673a6574c5781e580d6c45"},
 "extraction_plan": {"path": "tests-checks/v28-primitive-plan-v1.md", "sha256": "b9948d186f89e313f5eae829ab9fa4081f03b3260d4bb8f97237d70b4fbdd2ba"},
}
copies = {
 "candidate-static.py": "candidate", "meter-support-reference-static.py": "support_reference",
 "production-binding.json": "production_binding", "production-accounting.json": "production_accounting",
 "old-accounting.json": "old_accounting", "extractor.py": "extractor",
 "extraction-proof.json": "extraction_proof", "extraction-plan.md": "extraction_plan",
}
frozen = {
 "prototype": {"path": "tests-checks/v28-primitive-extracted-v1.py", "sha256": "bad767aab3b330666fbc4543224e28347a8cf93f8f69d5940c618737dbea2778"},
 "accounting": {"path": "tests-checks/v28-primitive-accounting-v1.json", "sha256": "4592e93634857015cd2befa227e7483db1b00895117881d919e6b0508cfa95ca"},
 "cursor_oracle": {"path": "tests-checks/cursor-oracle-v2.py", "sha256": "145fe1d59c48e23cdb426bcbe35edbecc3f941a81dc9780e8eeed849be5bc143"},
 "indexed_oracle": {"path": "tests-checks/indexed-storage-extension-oracle-v2.py", "sha256": "95ee5d3dd2e31ffd7ea6ecdd2f5e2b05dddb15e5a5ef1aa70ba8820bd82d2381"},
}
all_text("indexed-name-storage-control-v1", "v28-production-primitive-control-v1", 1)
all_text(".storage-indexed-prototype", ".storage-v28-primitive", 2)
all_text("indexed_control", "v28_primitive_control", 5)
all_text("1779", "1787", 1)
all_text("1774", "1782", 2)
one('prefix = "indexed-" + label', 'prefix = "v28-primitive-" + label')
one('checks = validate(ROOT / "engineer-checks")', 'checks = validate(ROOT / "tests-checks")')
one('folder = SNAPSHOTS / ("indexed-prototype-" + uuid.uuid4().hex)',
    'folder = SNAPSHOTS / ("v28-primitive-" + uuid.uuid4().hex)')
one('"""Three-phase pure indexed-storage control; authoring does not authorize execution.',
    '"""Three-phase v28 production-primitive control; no execution authorized by authoring.')
one('Root creates the fully pinned config only after reviewing every final input.',
    'Root creates the fully pinned config only after reviewing every final input.\n'
    'One invocation runs one selected slot/seed, never an automatic matrix.\n'
    'The complete candidate/support references are static-only; only verified extracted\n'
    'primitive nodes and original oracle code are imported in the isolated child.')
one('SCHEMA = "v28-production-primitive-control-v1"',
    'EXTRA_INPUTS = ' + repr(extras) + '\nEXTRA_COPIES = ' + repr(copies)
    + '\nFROZEN_DERIVED = ' + repr(frozen) + '\nSCHEMA = "v28-production-primitive-control-v1"')
one('"production_source_sha256": SOURCE_SHA, "disposition_sha256": DISPOSITION_SHA}',
    '"production_watch_sha256": SOURCE_SHA, "candidate_sha256": EXTRA_INPUTS["candidate"]["sha256"],\n'
    '             "disposition_sha256": DISPOSITION_SHA}')
one('req(type(config) is dict and set(config) == fields',
    'fields |= set(EXTRA_INPUTS)\n'
    '        req(type(config) is dict and set(config) == fields')
one('req(config["disposition_sha256"] == DISPOSITION_SHA, "config disposition")',
    'req(config["disposition_sha256"] == DISPOSITION_SHA, "historical disposition pin")\n'
    '        req(all(config[key] == value for key, value in {**EXTRA_INPUTS, **FROZEN_DERIVED}.items()),\n'
    '            "frozen production extraction or unchanged oracle inputs differ")')
one('req(type(expected["planned_runs"]) is int\n'
    '            and expected["planned_runs"] >= expected["planned_cases"], "cursor planned runs")',
    'req(type(expected["planned_runs"]) is int\n'
    '            and expected["planned_runs"] >= expected["planned_cases"], "cursor planned runs")\n'
    '        req(all(type(config["indexed_expected"][key]) is int\n'
    '                for key in ("planned_cases", "planned_runs")), "indexed population exact types")')
one('req(len(set(input_paths.values())) == 9, "input paths must be distinct")',
    'for key, entry in EXTRA_INPUTS.items():\n'
    '            path, raw = read_input(config[key], P(entry["path"]).suffix)\n'
    '            input_paths[key], inputs[key] = path, raw\n'
    '        req(len(set(input_paths.values())) == 17, "input paths must be distinct")')
one('wanted_hashes.update({"control": digest(control_raw), "config": config_sha,',
    'wanted_hashes.update({key: entry["sha256"] for key, entry in EXTRA_INPUTS.items()})\n'
    '        wanted_hashes.update({"control": digest(control_raw), "config": config_sha,')
one('**floor_files,\n        }',
    '**{name: inputs[key] for name, key in EXTRA_COPIES.items()},\n'
    '            **floor_files,\n        }')
# Identity is emitted before even the static-only verifier import.
one('"accounting_sha256": config["accounting"]["sha256"]})',
    '"accounting_sha256": config["accounting"]["sha256"],\n'
    '          "candidate_sha256": config["candidate"]["sha256"],\n'
    '          "extraction_proof_sha256": config["extraction_proof"]["sha256"]})')
one('prototype = load("indexed_prototype_under_test", payload / "prototype.py")',
    'verifier = load("static_extraction_verifier", payload / "extractor.py")\n'
    '    extraction = verifier.verify_extraction(*[checked(payload / name).read_bytes() for name in (\n'
    '        "candidate-static.py", "meter-support-reference-static.py", "production-binding.json",\n'
    '        "production-accounting.json", "old-accounting.json", "prototype.py",\n'
    '        "accounting.json", "extraction-proof.json")])\n'
    '    req(extraction["candidate_sha256"] == config["candidate"]["sha256"]\n'
    '        and extraction["extracted_sha256"] == config["prototype"]["sha256"]\n'
    '        and extraction["accounting_sha256"] == config["accounting"]["sha256"]\n'
    '        and extraction["proof_sha256"] == config["extraction_proof"]["sha256"]\n'
    '        and type(extraction["production_nodes_verified"]) is int\n'
    '        and extraction["production_nodes_verified"] == 47\n'
    '        and extraction["static_only"] is True, "static extraction verification")\n'
    '    emit({"kind": "static_extraction_verified", **extraction})\n'
    '    prototype = load("v28_extracted_primitive_under_test", payload / "prototype.py")')
# Floor replay binds fresh source/extraction and a real, successful floor process.
one('and floor.get("result_ok") is True, "floor did not succeed")',
    'and floor.get("result_ok") is True\n'
    '                and type(floor.get("process_returncode")) is int\n'
    '                and floor["process_returncode"] == 0\n'
    '                and "error" not in floor and "cleanup_error" not in floor\n'
    '                and not floor.get("timeout"), "floor did not succeed")')
one('floor_completed = [x for x in floor_records if x.get("kind") == "completed"]',
    'floor_completed = [x for x in floor_records if x.get("kind") == "completed"]\n'
    '            floor_extractions = [x for x in floor_records if x.get("kind") == "static_extraction_verified"]')
one('and floor_completed == floor.get("completed_records"),',
    'and floor_completed == floor.get("completed_records")\n'
    '                and floor_extractions == floor.get("extraction_records"),')
all_text('"identity_before_payload_imports", "phase_result", "phase_result",',
         '"identity_before_payload_imports", "static_extraction_verified", "phase_result", "phase_result",', 2)
one('floor_identity = floor_identities[0]',
    'req(len(floor_extractions) == 1, "floor extraction record population")\n'
    '            check_extraction_record(floor_extractions[0], config)\n'
    '            floor_identity = floor_identities[0]')
one('and floor_identity.get("pontius_imported") is False,',
    'and floor_identity.get("candidate_sha256") == config["candidate"]["sha256"]\n'
    '                and floor_identity.get("extraction_proof_sha256") == config["extraction_proof"]["sha256"]\n'
    '                and floor_identity.get("pontius_imported") is False,')
one('completed = [item for item in records if item.get("kind") == "completed"]',
    'completed = [item for item in records if item.get("kind") == "completed"]\n'
    '        extractions = [item for item in records if item.get("kind") == "static_extraction_verified"]\n'
    '        receipt["extraction_records"] = extractions\n'
    '        req(len(extractions) == 1, "extraction record population")\n'
    '        check_extraction_record(extractions[0], config)')
one('and identity.get("pontius_imported") is False, "payload identity context")',
    'and identity.get("candidate_sha256") == config["candidate"]["sha256"]\n'
    '            and identity.get("extraction_proof_sha256") == config["extraction_proof"]["sha256"]\n'
    '            and identity.get("pontius_imported") is False, "payload identity context")')
one('WRAPPER = r\'\'\'',
    'def check_extraction_record(record, config):\n'
    '    req(record.get("candidate_sha256") == config["candidate"]["sha256"]\n'
    '        and record.get("extracted_sha256") == config["prototype"]["sha256"]\n'
    '        and record.get("accounting_sha256") == config["accounting"]["sha256"]\n'
    '        and record.get("proof_sha256") == config["extraction_proof"]["sha256"]\n'
    '        and is_digest(record.get("current_runtime_proof_sha256"))\n'
    '        and type(record.get("production_nodes_verified")) is int\n'
    '        and record["production_nodes_verified"] == 47\n'
    '        and record.get("static_only") is True, "extraction verification pins/claims")\n\n\n'
    'WRAPPER = r\'\'\'')
# Exact integer cap evidence in both parent and bootstrap; never alter oracles.
all_text('req(summary.get("maximum_meter_limit") == 262144,',
         'req(type(summary.get("maximum_meter_limit")) is int\n'
         '        and summary.get("maximum_meter_limit") == 262144,', 2)
one('finite indexed-storage oracle timed out after 60 seconds',
    'finite v28 primitive oracle timed out after 60 seconds')
newraw = text.encode()
tree = ast.parse(text)
compile(text, "<v28-primitive-control-static>", "exec")
wrapper = next(ast.literal_eval(node.value) for node in tree.body
               if isinstance(node, ast.Assign) and any(isinstance(x, ast.Name) and x.id == "WRAPPER"
                                                       for x in node.targets))
compile(wrapper, "<v28-primitive-wrapper-static>", "exec")
assert len(extras) == 8 and len(copies) == 8
outpath = C / "v28-primitive-control-v1.py"
diffpath = C / "v28-primitive-control-v1-from-indexed-v4.diff"
extractdiffpath = C / "v28-primitive-extractor-v2-from-v1.diff"
proofpath = C / "v28-primitive-harness-static-v1.json"
assert not any(path.exists() for path in (outpath, diffpath, extractdiffpath, proofpath))
diff = "".join(difflib.unified_diff(oldraw.decode().splitlines(True), text.splitlines(True),
                                  fromfile=str(oldpath), tofile=str(outpath))).encode()
v1 = (C / "v28-primitive-extractor-v1.py").read_text()
v2 = (C / "v28-primitive-extractor-v2.py").read_text()
extractdiff = "".join(difflib.unified_diff(v1.splitlines(True), v2.splitlines(True),
    fromfile="v28-primitive-extractor-v1.py", tofile="v28-primitive-extractor-v2.py")).encode()
# Immutable old oracle, case, spec census directly from the original approved config.
oldconfig = json.loads((T / "engineer-indexed-storage-config-v1.json").read_bytes())
prior = {}
for key in ("old_oracle", "old_cases", "cursor_oracle", "cursor_cases", "indexed_oracle",
            "indexed_cases", "indexed_spec"):
    entry = oldconfig[key]
    actual = h((T / entry["path"]).read_bytes())
    assert actual == entry["sha256"]
    prior[key] = entry
for entry in {**extras, **frozen}.values():
    assert h((T / entry["path"]).read_bytes()) == entry["sha256"]
# Derive a manifest of untouched controller functions; main/wrapper are explicit delta.
oldtree = ast.parse(oldraw)
beforedefs = {node.name: node for node in oldtree.body if isinstance(node, ast.FunctionDef)}
afterdefs = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
same = sorted(name for name in beforedefs
              if ast.dump(beforedefs[name], include_attributes=False)
              == ast.dump(afterdefs[name], include_attributes=False))
proof = {
 "schema": "pontius-v28-primitive-harness-static-v1", "payload_executed": False,
 "predecessor_control_sha256": h(oldraw), "control_sha256": h(newraw),
 "wrapper_sha256": h(wrapper.encode()), "raw_control_diff_sha256": h(diff),
 "extractor_v2_diff_sha256": h(extractdiff), "candidate_sha256": extras["candidate"]["sha256"],
 "immutable_prior_inputs": prior, "extra_inputs": extras, "frozen_derived": frozen,
 "planned_phase_runs": [34, 28, 31], "total_runs_per_child": 93,
 "manifest_files_floor": 1782, "manifest_files_dev": 1787,
 "tracked_files_unchanged": 1761, "payload_files_floor": 21, "floor_evidence_files_dev": 5,
 "unchanged_parent_function_ASTs": same, "control_compiled_not_executed": True,
 "wrapper_compiled_not_executed": True, "new_record": "static_extraction_verified",
 "selected_slot_only": True, "root_config_and_dispatch_required": True,
 "limitations": ["Extracted primitive A only; production budget adapter and constructor B excluded.",
  "New16 category presence in source is not runtime branch coverage.",
  "Authoring v1 static accounting comparison failed before artifact creation; corrected in retained v2.",
  "Per-runtime full AST equality is checked locally; AST dump hashes are not normalized across runtimes."],
}
for path, raw in ((outpath,newraw),(diffpath,diff),(extractdiffpath,extractdiff),
                  (proofpath,(json.dumps(proof,indent=2,sort_keys=True)+"\n").encode())):
    write(path,raw)
print(json.dumps({"static_only":True, "payload_executed":False,
 "artifacts":{path.name: {"sha256":h(path.read_bytes()),"bytes":path.stat().st_size}
              for path in (outpath,diffpath,extractdiffpath,proofpath)},
 "wrapper_sha256":h(wrapper.encode()),"unchanged_controller_functions":same},indent=2))
