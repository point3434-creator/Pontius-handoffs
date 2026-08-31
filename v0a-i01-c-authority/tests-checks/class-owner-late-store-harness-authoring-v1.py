"""Adapt the reviewed R8 harness to frozen L8 by exact text edits; compile only."""
import sys
assert sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
import ast
import difflib
import hashlib
import json
from pathlib import Path
T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
PACK_SHA = "08fce0e37eaeb24192c4f227677d7625097748ccb2cbc79470df4699718a9b47"
SPEC_SHA = "d122e974986d3022b2a95a531b8ca7c92a25dd845b2dc006983bd43a68a205a1"
OLD_PACK_SHA = "eb5551c054fc89da28fd2e4db433f56f7a3dbbd4cdb70509070a89fe362c74fd"
OLD_SPEC_SHA = "ed292bcf0207aad474e8293cf055c17de6409b9d851f95a8b8225d4375848dc6"
OLD_PROBE_SHA = "231bcddb04eb5f3f93135c46bc03f1ed6275195949f4189a700d2f0eb3571426"
OLD_CONTROL_SHA = "34c16309d974e40909bc352d509308b19d2fa4fd42f06386d27430fcf07526e2"
P0 = "class-comprehension-extension-probe-v2.py"
C0 = "class-comprehension-extension-control-v2.py"
P1 = "class-owner-late-store-probe-v1.py"
C1 = "class-owner-late-store-control-v1.py"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pinned(name, digest):
    raw = (C / name).read_bytes()
    assert sha(raw) == digest and b"\r" not in raw
    return raw

def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")

def dump(node):
    return ast.dump(node, include_attributes=False)

def defs(text):
    return {node.name: node for node in ast.parse(text).body if isinstance(node, ast.FunctionDef)}

pack = json.loads(pinned("class-owner-late-store-cases-v1.json", PACK_SHA))
pinned("class-owner-late-store-spec-v1.md", SPEC_SHA)
old_probe = pinned(P0, OLD_PROBE_SHA).decode()
old_control = pinned(C0, OLD_CONTROL_SHA).decode()
edits = {"probe": [], "control": []}

def change(text, before, after, kind, count=None):
    actual = text.count(before)
    assert actual and (count is None or actual == count), (kind, before, actual)
    edits[kind].append({"before": before, "after": after, "occurrences": actual})
    return text.replace(before, after)

probe = old_probe
control = old_control
for kind in ("probe", "control"):
    value = probe if kind == "probe" else control
    for before, after in (
        ("class-comprehension-extension", "class-owner-late-store"),
        ("class_comprehension_extension", "class_owner_late_store"),
        (OLD_PACK_SHA, PACK_SHA), (OLD_SPEC_SHA, SPEC_SHA),
        ('{"clean": 3, "refuse": 4, "permitted-refusal": 1}', '{"clean": 4, "refuse": 4}'),
        ("class/comprehension boundary", "empty-class late-member alias"),
    ):
        value = change(value, before, after, kind)
    if kind == "probe":
        probe = value
    else:
        control = value
old_ids = next(node.value for node in ast.parse(old_probe).body
               if isinstance(node, ast.Assign) and any(
                   isinstance(target, ast.Name) and target.id == "CASE_IDS" for target in node.targets))
old_ids_text = ast.get_source_segment(old_probe, old_ids)
new_ids_text = "(\n" + "".join('    "' + case["id"] + '",\n' for case in pack["cases"]) + ")"
probe = change(probe, old_ids_text, new_ids_text, "probe", 1)
probe = change(probe, 'tuple("R" + str(n).zfill(2) for n in range(1, 9))',
               'tuple("L" + str(n).zfill(2) for n in range(1, 9))', "probe", 1)
before = '            == "53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499",\n'
after = '            == "53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499"\n' + (
        '            and pack["requirements"]["semantic_plan_v3_sha256"]\n'
        '            == "1d661231a472fc689af06ea993234f27ab88a65da950d83f1811c1f941d94723"\n'
        '            and pack["requirements"]["old_44_expectations_unchanged"] is True,\n')
probe = change(probe, before, after, "probe", 1)
probe_raw = probe.encode()
control = change(control, "class-owner-late-store-probe-v2.py", P1, "control", 1)
control = change(control, OLD_PROBE_SHA, sha(probe_raw), "control", 1)
control_raw = control.encode()

# Reversing every declared edit reconstructs the predecessor exactly.
for kind, current, old in (("probe", probe, old_probe), ("control", control, old_control)):
    for edit in reversed(edits[kind]):
        assert current.count(edit["after"]) == edit["occurrences"]
        current = current.replace(edit["after"], edit["before"])
    assert current == old
old_p, new_p = defs(old_probe), defs(probe)
old_c, new_c = defs(old_control), defs(control)
changed_p = sorted(name for name in old_p if dump(old_p[name]) != dump(new_p[name]))
changed_c = sorted(name for name in old_c if dump(old_c[name]) != dump(new_c[name]))
assert changed_p == ["load_pack", "main", "oracle"]
assert changed_c == ["main", "validate_result"]
assert set(old_p) == set(new_p) and set(old_c) == set(new_c)
assert dump(old_p["public_review"]) == dump(new_p["public_review"])
for value, name in ((probe, P1), (control, C1)):
    compile(value, name, "exec", dont_inherit=True)
    assert "class-comprehension-extension" not in value and "class_comprehension_extension" not in value
    assert not any(case["id"] in value for case in json.loads((C / "class-comprehension-extension-cases-v1.json").read_bytes())["cases"])
tree = ast.parse(probe)
constants = {target.id: node.value for node in tree.body if isinstance(node, ast.Assign)
             for target in node.targets if isinstance(target, ast.Name)}
assert ast.literal_eval(constants["CASE_IDS"]) == tuple(case["id"] for case in pack["cases"])
assert ast.literal_eval(constants["PACK_SHA"]) == PACK_SHA
assert ast.literal_eval(constants["SCHEDULE_SHA"]) == SPEC_SHA
summary_dict = next(node.value for node in ast.walk(new_p["main"])
                    if isinstance(node, ast.Assign) and any(
                        isinstance(target, ast.Name) and target.id == "summary" for target in node.targets))
summary_fields = {key.value: value for key, value in zip(summary_dict.keys, summary_dict.values)
                  if isinstance(key, ast.Constant) and isinstance(key.value, str)}
for field in ("planned_cases", "case_count", "projections"):
    node = summary_fields[field]
    assert isinstance(node, ast.Constant) and type(node.value) is int and node.value == 8
assert "summary count types" in control and "finite counts" in probe
assert '{"clean": 4, "refuse": 4}' in probe and control.count('{"clean": 4, "refuse": 4}') == 2
assert ast.literal_eval(constants["CAPS"]) == {
    "MAXIMUM_ANALYSIS_HELPER_DEPTH": 64, "MAXIMUM_ANALYSIS_CHILD_DEPTH": 4,
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS": 4096, "MAXIMUM_ANALYSIS_CARDINALITY": 2147483647,
    "MAXIMUM_ANALYSIS_WORK_UNITS": 262144}
outputs = {
    P1: probe_raw, C1: control_raw,
    "class-owner-late-store-probe-v1-from-R8-v2.diff": "".join(difflib.unified_diff(
        old_probe.splitlines(True), probe.splitlines(True), fromfile=P0, tofile=P1)).encode(),
    "class-owner-late-store-control-v1-from-R8-v2.diff": "".join(difflib.unified_diff(
        old_control.splitlines(True), control.splitlines(True), fromfile=C0, tofile=C1)).encode(),
}
proof = {
    "schema": "codex-a-class-owner-late-store-harness-static-v1",
    "standing": "Static authoring only; no controller, probe, candidate or Model executed",
    "predecessors": {P0: OLD_PROBE_SHA, C0: OLD_CONTROL_SHA},
    "case_pack_sha256": PACK_SHA, "spec_sha256": SPEC_SHA,
    "changed_probe_functions": changed_p, "changed_control_functions": changed_c,
    "edit_reversal_exact_bytes": True, "public_review_ast_identical": True,
    "runtime_custody_and_floor_gate_preserved_except_family_literals": True,
    "exact_8_summary_fields_and_case_ids_verified_statically": True,
    "classifications": {"clean": 4, "refuse": 4}, "original_caps_unchanged": True,
    "distinct_family_payload_output_prefix_and_result_schema": True,
    "no_private_analyzer_observer_added": True,
    "edits": edits,
    "outputs": {name: {"sha256": sha(raw), "bytes": len(raw)} for name, raw in outputs.items()},
    "compiled_only": True, "payload_executed": False}
outputs["class-owner-late-store-harness-static-proof-v1.json"] = encoded(proof)
assert all(not (C / name).exists() for name in outputs)
for name, raw in outputs.items():
    assert b"\r" not in raw and raw.endswith(b"\n")
    with (C / name).open("xb") as stream:
        stream.write(raw)
pinned(P0, OLD_PROBE_SHA)
pinned(C0, OLD_CONTROL_SHA)
pinned("class-owner-late-store-cases-v1.json", PACK_SHA)
pinned("class-owner-late-store-spec-v1.md", SPEC_SHA)
print(json.dumps({"created": {name: {"sha256": sha(raw), "bytes": len(raw)} for name, raw in outputs.items()},
                  "payload_executed": False}, sort_keys=True))

