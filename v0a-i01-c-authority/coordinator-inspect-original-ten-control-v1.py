"""Root inspection of original-ten harness; source/AST only, no payload."""
from pathlib import Path
import ast
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
sha = lambda raw: hashlib.sha256(raw).hexdigest()
pins = {
    "original-composition-ten-control-v1.py": "20f196243e078ef542628b6a400ab2266443c1b1d918327ee14004f98e564bb4",
    "original-composition-ten-probe-v1.py": "e2564b1d1d61c0a92e449f80eb5118eb72141b3fabd9022cf2b2881d1c56927e",
    "original-composition-ten-plan-v1.md": "3b330b732d99bdf02bae7b270a57f1d9cc0352fe1db573f5148c751084ad3f1a",
    "storage-composition-cases-v1.json": "faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709",
    "scalar-class-composition-cases-v1.json": "50e88cedf77f902012237ccd88700c911fa8f3681c8dada380cca6c3142659ac",
    "class-semantic-extension-control-v2.py": "d76b3d07b1b5f855a58050c876ddce57b60929302745fd8116eca109a77b2149",
    "class-semantic-extension-probe-v2.py": "40240ceb30d676a71182c68d03a09970296b604d6d3d136b4b2b9952aec25084",
}
for name, digest in pins.items():
    assert sha((C / name).read_bytes()) == digest, name
defs = lambda name: {node.name: node for node in ast.parse((C / name).read_bytes()).body
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
dump = lambda node: ast.dump(node, include_attributes=False)
control = defs("original-composition-ten-control-v1.py")
predecessor = defs("class-semantic-extension-control-v2.py")
changed = {name for name in control.keys() & predecessor.keys()
           if dump(control[name]) != dump(predecessor[name])}
assert changed == {"validate_result", "main"}
assert control.keys() - predecessor.keys() == {"load_cases"}
assert predecessor.keys() - control.keys() == {"route_check"}
probe = defs("original-composition-ten-probe-v1.py")
for original_file, original_name, successor_name in (
    ("storage-composition-probe-v1.py", "oracle", "storage_oracle"),
    ("class-composition-mechanism-probe-v1.py", "oracle", "scalar_oracle"),
    ("storage-composition-probe-v1.py", "public_review", "public_review"),
):
    original = defs(original_file)[original_name]
    original.name = successor_name
    assert dump(original) == dump(probe[successor_name]), successor_name
assert dump(control["load_cases"]) == dump(probe["load_cases"])
for name in ("original-composition-ten-control-v1.py", "original-composition-ten-probe-v1.py"):
    compile(ast.parse((C / name).read_bytes()), name, "exec")
classes = {"clean": 0, "refuse": 0}
for name in ("storage-composition-cases-v1.json", "scalar-class-composition-cases-v1.json"):
    for case in json.loads((C / name).read_bytes())["cases"]:
        classes[case["classification"]] += 1
        for field, digest_field in (("source", "source_sha256"), ("oracle_source", "oracle_sha256")):
            assert sha(case[field].encode()) == case[digest_field]
assert classes == {"clean": 5, "refuse": 5}
report = {
    "schema": "coordinator-original-ten-inspection-v1", "payload_executed": False,
    "input_pins": pins, "classifications": classes,
    "both_original_model_runners_and_public_review_ast_equal": True,
    "controller_changed_functions": sorted(changed),
    "manual_review": [
        "Read complete probe and controller deltas; both frozen case packs and original harmless runners preserved.",
        "No route observer/private-state reads; real public analyzer output determines semantic expectations.",
        "Exact identity+10cases+summary stream, all source pins, exact Boolean/integer completion types.",
        "Floor raw setup/stream/manifest/HEAD/status replay binds same candidate before developer comparison.",
        "Fresh1768/1773 manifests plus separately hashed manifest, scrubbed environment,60s directchildwatchdog.",
    ],
    "disposition": "No blocker found in bounded static review. Root may dispatch only after reviewing the named retained source.",
    "limits": "No execution yet. Completed intact semantic RED can replicate to314; incomplete/oracle/infrastructure failure cannot. Not a cold verdict.",
}
raw = (json.dumps(report, indent=2) + "\n").encode()
for relative, content in {
    "coordinator-original-ten-inspection-v1.json": raw,
    "coordinator-inspect-original-ten-control-v1.py": Path(__file__).read_bytes(),
}.items():
    with (T / relative).open("xb") as stream:
        stream.write(content)
print(json.dumps({"report_sha256": sha(raw), "payload_executed": False}))
