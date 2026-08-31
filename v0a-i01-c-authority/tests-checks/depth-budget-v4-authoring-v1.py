"""Create-only v4 diagnostic text and static proof; never imports a payload."""
import sys
assert sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
import ast
import difflib
import hashlib
import json
from pathlib import Path

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
P3 = "engineer-depth-budget-probe-v3.py"
P4 = "engineer-depth-budget-probe-v4.py"
C3 = "tests-depth-budget-control-v3.py"
C4 = "tests-depth-budget-control-v4.py"
P3_SHA = "7aa9f188b2917fec149485501eafcc4d516d3104a10b026e5ec33262b24962ae"
C3_SHA = "91533776e028ad57513611940423cd1cb2c6d8c0d85f8cafd49f089ebfd9e2d7"
SOURCE_SHA = "1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951"
HELPER = "def raw_full_join_sharing(local):\n    \"\"\"Ephemeral raw reads; the returned signature contains only bool/int tuples.\"\"\"\n    inputs, states = local.get(\"name_inputs\"), local.get(\"states\")\n    versions = inputs if type(inputs) is tuple else ()\n    sources = states if type(states) in (list, tuple) else ()\n    exact_versions = bool(versions) and all(\n        type(value) is generator._NameVersion for value in versions)\n    exact_sources = bool(sources) and len(sources) == len(versions) and all(\n        type(value) is generator._ExecutionState for value in sources)\n    meter, resolver = local.get(\"meter\"), local.get(\"self\")\n    exact_meter = type(meter) is generator._NameMeter\n    budget = (vars(resolver).get(\"budget\")\n              if type(resolver) is generator._SourceOrderedResolver else None)\n    same_roots = exact_versions and all(\n        object.__getattribute__(value, \"_root\")\n        is object.__getattribute__(versions[0], \"_root\") for value in versions)\n    same_meter = exact_versions and exact_sources and exact_meter and all(\n        object.__getattribute__(value, \"_meter\") is meter for value in versions)\n    same_budget = exact_sources and exact_meter and budget is not None and (\n        object.__getattribute__(meter, \"budget\") is budget)\n    disabled = exact_sources\n    for source in sources:\n        if type(source) is not generator._ExecutionState:\n            disabled = same_meter = same_budget = False\n            continue\n        authority, cursor = vars(source).get(\"authority\"), vars(source).get(\"_names\")\n        if type(authority) is generator._AuthorityState:\n            disabled = disabled and vars(authority).get(\"enabled\") is False\n            same_budget = same_budget and vars(authority).get(\"budget\") is budget\n        else:\n            disabled = same_budget = False\n        same_meter = same_meter and type(cursor) is generator._NameCursor and (\n            object.__getattribute__(cursor, \"_meter\") is meter)\n    pending_rows = []\n    for version in versions:\n        size, pending, known = -1, -1, False\n        if type(version) is generator._NameVersion:\n            size = object.__getattribute__(version, \"_size\")\n            size = size if type(size) is int and size >= 0 else -1\n            root = object.__getattribute__(version, \"_root\")\n            if root is None:\n                pending, known = 0, True\n            elif type(root) is generator._NameRadixLeaf:\n                raw = object.__getattribute__(root, \"pending\")\n                if type(raw) is tuple:\n                    pending, known = len(raw), True\n            elif type(root) is generator._NameRadixBranch:\n                raw = object.__getattribute__(root, \"pending_count\")\n                if type(raw) is int and raw >= 0:\n                    pending, known = raw, True\n        pending_rows.append((size, pending, known, known and size >= 0 and pending == size))\n    all_pending = exact_versions and all(row[3] for row in pending_rows)\n    return (len(versions), len(sources), exact_versions, exact_sources, same_roots,\n            disabled, same_meter, same_budget, tuple(pending_rows), all_pending,\n            exact_versions and exact_sources and same_roots and disabled\n            and same_meter and same_budget and all_pending)\n\n\n"
SUMMARY = "        \"full_join_sharing_facts\": [\n            {\"input_count\": facts[0], \"source_count\": facts[1],\n             \"exact_name_version_inputs\": facts[2], \"exact_execution_state_sources\": facts[3],\n             \"published_roots_same_by_identity\": facts[4],\n             \"all_source_authorities_disabled\": facts[5],\n             \"same_meter\": facts[6], \"same_budget\": facts[7],\n             \"per_root_pending\": [\n                 {\"size\": row[0], \"pending_count\": row[1], \"pending_count_known\": row[2],\n                  \"all_pending\": row[3]} for row in facts[8]],\n             \"all_roots_pending\": facts[9], \"restricted_C_guard_facts\": facts[10],\n             \"attempts\": count}\n            for facts, count in entry[\"full_join_sharing\"].items()\n        ],\n"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read(name, expected):
    raw = (T / name).read_bytes()
    assert sha(raw) == expected
    assert b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8")

def once(text, before, after):
    assert text.count(before) == 1, before
    return text.replace(before, after, 1)

def dump(node):
    return ast.dump(node, include_attributes=False)

def create(name, raw):
    with (T / name).open("xb") as stream:
        stream.write(raw)

p3, c3 = read(P3, P3_SHA), read(C3, C3_SHA)
source = read("engineer-generator-v26-storage.py", SOURCE_SHA)
p4 = once(p3, '        "publication_costs": {}, "bulk_shapes": collections.Counter(),\n',
          '        "publication_costs": {}, "bulk_shapes": collections.Counter(),\n'
          '        "full_join_sharing": collections.Counter(),\n')
p4 = once(p4, "def record_bulk_shape(entry, frame):\n", HELPER + "def record_bulk_shape(entry, frame):\n")
p4 = once(p4, '        shape = ("full_join", len(names) if type(names) is set else None, None, counts)\n',
          '        shape = ("full_join", len(names) if type(names) is set else None, None, counts)\n'
          '        entry["full_join_sharing"][raw_full_join_sharing(local)] += 1\n')
p4 = once(p4, '        "creation_stack": entry["creation_stack"],\n',
          SUMMARY + '        "creation_stack": entry["creation_stack"],\n')
p4_raw = p4.encode("utf-8")
c4 = once(c3, 'PROBE_SHA = "' + P3_SHA + '"', 'PROBE_SHA = "' + sha(p4_raw) + '"')
c4 = once(c4, 'PROBE = ROOT / "' + P3 + '"', 'PROBE = ROOT / "' + P4 + '"')
c4_raw = c4.encode("utf-8")
old, new = ast.parse(p3), ast.parse(p4)
old_functions = {node.name: node for node in old.body if isinstance(node, ast.FunctionDef)}
new_functions = {node.name: node for node in new.body if isinstance(node, ast.FunctionDef)}
changed = sorted(name for name in old_functions if dump(old_functions[name]) != dump(new_functions[name]))
assert changed == ["observed_init", "record_bulk_shape", "summary"]
assert set(new_functions) - set(old_functions) == {"raw_full_join_sharing"}
assert set(old_functions) <= set(new_functions)
normalized = ast.parse(p4)
normalized.body = [old_functions[node.name] if isinstance(node, ast.FunctionDef)
                   and node.name in changed else node for node in normalized.body
                   if not (isinstance(node, ast.FunctionDef) and node.name == "raw_full_join_sharing")]
assert dump(normalized) == dump(old)
assert dump(old_functions["observed_consume"]) == dump(new_functions["observed_consume"])
assert dump(old_functions["install_hooks"]) == dump(new_functions["install_hooks"])
assert all(dump(old_functions[name]) == dump(new_functions[name])
           for name in ("helper1050_source", "helper65_source", "generator70_source"))
reverted_control = once(c4, 'PROBE_SHA = "' + sha(p4_raw) + '"', 'PROBE_SHA = "' + P3_SHA + '"')
reverted_control = once(reverted_control, 'PROBE = ROOT / "' + P4 + '"', 'PROBE = ROOT / "' + P3 + '"')
assert reverted_control == c3
# The new helper can call only raw builtin inspection/iteration operations.
helper_ast = new_functions["raw_full_join_sharing"]
calls = set()
for node in ast.walk(helper_ast):
    if isinstance(node, ast.Call):
        calls.add(ast.unparse(node.func))
assert calls == {"local.get", "type", "bool", "all", "len", "vars",
                 "vars(resolver).get", "object.__getattribute__", "vars(source).get",
                 "vars(authority).get", "pending_rows.append", "tuple"}
assert not any(isinstance(node, (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal))
               for node in ast.walk(helper_ast))
# Verify that the exact source event is after snapshot publication, without executing it.
source_tree = ast.parse(source)
resolver = next(node for node in source_tree.body if isinstance(node, ast.ClassDef)
                and node.name == "_SourceOrderedResolver")
merge = next(node for node in resolver.body if isinstance(node, ast.FunctionDef)
             and node.name == "_merge_states")
snapshot_line = next(node.lineno for node in ast.walk(merge)
                     if isinstance(node, ast.Assign) and any(
                         isinstance(target, ast.Name) and target.id == "name_inputs"
                         for target in node.targets))
bulk_line = next(node.lineno for node in ast.walk(merge)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "_NameVersion"
                and node.func.attr == "from_unique_entries")
assert snapshot_line < bulk_line
for name, text in ((P4, p4), (C4, c4)):
    compile(text, name, "exec", dont_inherit=True)
wrapper = next(node.value.value for node in ast.parse(c4).body
               if isinstance(node, ast.Assign) and any(
                   isinstance(target, ast.Name) and target.id == "WRAPPER" for target in node.targets))
compile(wrapper, "embedded-wrapper", "exec", dont_inherit=True)
outputs = {
    P4: p4_raw, C4: c4_raw,
    "engineer-depth-budget-probe-v4-from-v3.diff": "".join(difflib.unified_diff(
        p3.splitlines(True), p4.splitlines(True), fromfile=P3, tofile=P4)).encode("utf-8"),
    "tests-depth-budget-control-v4-from-v3.diff": "".join(difflib.unified_diff(
        c3.splitlines(True), c4.splitlines(True), fromfile=C3, tofile=C4)).encode("utf-8"),
}
proof = {
    "schema": "codex-a-depth-budget-v4-static-v1",
    "standing": "Engineering authoring/static inspection only; no payload execution or product verdict",
    "predecessors": {P3: P3_SHA, C3: C3_SHA},
    "source_sha256": SOURCE_SHA,
    "changed_existing_probe_functions": changed,
    "added_probe_function": "raw_full_join_sharing",
    "probe_rest_of_top_level_ast_equal": True,
    "original_consume_observer_ast_equal": True,
    "hook_installer_ast_equal": True,
    "all_three_fixture_builders_ast_equal": True,
    "control_only_probe_sha_and_basename_changed": True,
    "embedded_wrapper_byte_equal": True,
    "raw_helper_call_forms": sorted(calls),
    "source_name_inputs_snapshot_assignment_line": snapshot_line,
    "source_full_join_bulk_call_line": bulk_line,
    "observer_entrypoint": "Existing bulk_input_iterator_requests charge at full-join from_unique_entries",
    "new_retained_values": "Only bool/int scalar signatures and tuples thereof; no root/state/budget/FlowValue/frame retained",
    "pending_count": "Raw exact tuple length for leaf; raw exact nonnegative int for branch; None root zero; unknown sentinel -1",
    "no_new_gate_seed_fixture_cap_or_environment_behavior": True,
    "compile_only": True, "candidate_or_fixture_or_probe_or_controller_executed": False,
    "outputs": {name: {"sha256": sha(raw), "bytes": len(raw)} for name, raw in outputs.items()},
}
proof_raw = (json.dumps(proof, indent=2, sort_keys=True) + "\n").encode("utf-8")
outputs["engineer-depth-budget-v4-static-v1.json"] = proof_raw
assert all(not (T / name).exists() for name in outputs)
for name, raw in outputs.items():
    assert b"\r" not in raw and raw.endswith(b"\n")
    create(name, raw)
assert read(P3, P3_SHA) == p3 and read(C3, C3_SHA) == c3
assert read("engineer-generator-v26-storage.py", SOURCE_SHA) == source
print(json.dumps({"created": {name: {"sha256": sha(raw), "bytes": len(raw)}
                              for name, raw in outputs.items()},
                  "payload_executed": False}, sort_keys=True))

