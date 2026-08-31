"""Root-reviewed finite comprehension harness, without payload execution."""
from pathlib import Path
import ast
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C = T / "tests-checks"
sha = lambda raw: hashlib.sha256(raw).hexdigest()
pins = {
    "class-comprehension-boundary-probe-v1.py": "b0232750b89fba7939a093e81e9e4b8a183d23371f6464eaa8d3443bedf49138",
    "class-comprehension-boundary-control-v1.py": "775157055e5a9b6234307ef552536a25bb6049fd76e001e352fc954eac258eba",
    "class-comprehension-boundary-cases-v1.json": "9df895eb5bd645a5e4ef05be0f7c0a3db76df458ca023bbfbd36407ee3496b71",
    "class-comprehension-boundary-spec-v1.md": "8a4220e2a9f41a4171c585f6f5fa36ace1e22fb38e8849f96cd29a490facea82",
    "class-comprehension-boundary-static-proof-v1.json": "f54e0635608a98b97214a190d4cc2c09856d9f39b3ae514ef78d36a7931d1fca",
    "class-name-boundary-probe-v1.py": "ee50ef24fc0acde4f0c2da3e190e2c786ccb9bfb351788e75b574f6d7ad80fb5",
}
for name, digest in pins.items():
    assert sha((C / name).read_bytes()) == digest, name
defs = lambda name: {node.name: node for node in ast.parse((C / name).read_bytes()).body
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
before, after = defs("class-name-boundary-probe-v1.py"), defs("class-comprehension-boundary-probe-v1.py")
dump = lambda node: ast.dump(node, include_attributes=False)
assert before.keys() == after.keys()
assert {name for name in before if dump(before[name]) != dump(after[name])} == {"load_pack", "oracle", "main"}
for name in ("class-comprehension-boundary-control-v1.py", "class-comprehension-boundary-probe-v1.py"):
    compile(ast.parse((C / name).read_bytes()), name, "exec")
pack = json.loads((C / "class-comprehension-boundary-cases-v1.json").read_bytes())
assert len(pack["cases"]) == 6
assert pack["classifications"] == {"clean": 2, "refuse": 3, "permitted-refusal": 1}
for case in pack["cases"]:
    assert sha(case["source"].encode()) == case["source_sha256"]
    assert sha(case["oracle_source"].encode()) == case["oracle_sha256"]
assert sha((T / "engineer-generator-v22.py").read_bytes()) == "61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3"
report = {
    "schema": "coordinator-class-comprehension-harness-inspection-v1",
    "payload_executed": False, "input_pins": pins,
    "public_review_ast_unchanged": True,
    "manual_review": [
        "Read all six sensitive-source/independent-Model pairs and specification; expectations independent of candidate.",
        "Read complete probe/controller: sensitive source remains AST-only; each harmless Model uses a fresh namespace.",
        "TypeError is caught outside test_static; exact trace/result and unreachable events distinguish intended failures.",
        "Explicit retained candidate SHA, actualfloor-first runtime,1767/1772 manifest and full raw-output custody.",
        "Developer replication permits only completed intact semantic RED, never incomplete/oracle/infrastructure failure.",
        "Predeclared6-case scope, oldcaps, scrubbed environment and60s directchildwatchdog remain unchanged.",
    ],
    "disposition": "No blocking issue found. Root may dispatch v22-red01 on actual311, then identical314 if floor completes intact.",
    "limits": "Engineering RED discovery, not final review or acceptance. No candidate source change is authorized by this harness.",
}
raw = (json.dumps(report, indent=2) + "\n").encode()
for name, content in {
    "coordinator-class-comprehension-harness-inspection-v1.json": raw,
    "coordinator-inspect-class-comprehension-control-v1.py": Path(__file__).read_bytes(),
}.items():
    with (T / name).open("xb") as stream:
        stream.write(content)
print(json.dumps({"report_sha256": sha(raw), "payload_executed": False}))
