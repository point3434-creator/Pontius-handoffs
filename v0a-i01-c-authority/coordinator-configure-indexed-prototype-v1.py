"""Pin reviewed pure-storage inputs; authorize only the first floor/seed0 child."""
from pathlib import Path
import ast
import difflib
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
sha = lambda raw: hashlib.sha256(raw).hexdigest()
entries = {
    "prototype": ("engineer-name-radix-prototype-v1.py", "0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71"),
    "old_oracle": ("tests-checks/storage-oracle-v2.py", "6a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba"),
    "old_cases": ("tests-checks/storage-oracle-cases-v2.json", "3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f"),
    "cursor_oracle": ("tests-checks/cursor-oracle-v2.py", "145fe1d59c48e23cdb426bcbe35edbecc3f941a81dc9780e8eeed849be5bc143"),
    "cursor_cases": ("tests-checks/cursor-oracle-cases-v1.json", "ecddd020ffb2a0d85e624aeb7fb544f631b302839f9a5f3542c998b36c37ac61"),
    "indexed_oracle": ("tests-checks/indexed-storage-extension-oracle-v2.py", "95ee5d3dd2e31ffd7ea6ecdd2f5e2b05dddb15e5a5ef1aa70ba8820bd82d2381"),
    "indexed_cases": ("tests-checks/indexed-storage-extension-cases-v1.json", "795e893c4fbeee3963a3ea3cbbffdfacbea193f53063eb4848c8e9ac6d12984a"),
    "accounting": ("engineer-name-radix-accounting-v1.json", "79f64e5e7bbb429bedd108654b69c8ab5893973ee742517b543129f762f68f2b"),
    "indexed_spec": ("tests-checks/indexed-storage-extension-spec-v1.md", "11d11003b3ce84d485df549e73a494e358db69cc6f5db6faea5dae8f50c330f9"),
}
control_sha = "7192e46cd855d767c96a06ba81ffaa97c97604e12042fad5e06e299f10a5e44c"
disposition_sha = "e8f75e760d0bb2a4b1c37c8b7cfb571624f60321b804080445c1f2b4d8e1eafa"
review_pins = {
    "engineer-indexed-storage-control-v4.py": control_sha,
    "coordinator-radix-prototype-disposition-v1.md": disposition_sha,
    "coordinator-radix-prototype-inspection-v1.json": "1bee12ba553d3b4a42155a2c67a19471601ef0dee159093312d8951394d97bd7",
    "engineer-indexed-storage-control-v4-review-codex-v1.md": "20cfa26f732abdf31effe4e9ceeb24cb8b9cae88690ccb861ea9e1310368078c",
    "tests-checks/indexed-storage-oracles-static-proof-v2.json": "8fddb6ca3fcaf432175aace69d1f7a3b7d8e4e1c7949ec3994ba53662ebed939",
    "tests-checks/indexed-storage-p-boundary-clarification-v1.md": "cdc1f9aa5f66114d744e2bc66728f4a64f85032a7b25399a9c0a4c728cb28cb8",
}
for name, digest in [*entries.values(), *review_pins.items()]:
    assert sha((T / name).read_bytes()) == digest, name
old = (T / "tests-checks/indexed-storage-extension-oracle-v1.py").read_bytes()
assert sha(old) == "135983d43d271add4875cda4ab5144f6aaaadff21928637985740229f3a3f006"
new = (T / entries["indexed_oracle"][0]).read_bytes()
tree = ast.parse(new)
compile(tree, entries["indexed_oracle"][0], "exec")
diff = "".join(difflib.unified_diff(old.decode().splitlines(True), new.decode().splitlines(True),
                                  fromfile="indexed-oracle-v1", tofile="indexed-oracle-v2"))
# Full v1 source was read; the retained v2 is restricted to collision-gate changes.
allowed_owners = {"Harness", "collision_case", "verify_indexed"}
defs = lambda raw: {node.name: ast.dump(node, include_attributes=False)
    for node in ast.parse(raw).body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
old_defs, new_defs = defs(old), defs(new)
assert old_defs.keys() == new_defs.keys()
assert {name for name in old_defs if old_defs[name] != new_defs[name]} == allowed_owners
config = {"schema": "indexed-name-storage-control-v1", "control_sha256": control_sha,
          "disposition_sha256": disposition_sha,
          **{key: {"path": name, "sha256": digest} for key, (name, digest) in entries.items()},
          "cursor_expected": {"planned_cases": 16, "planned_runs": 28},
          "indexed_expected": {"planned_cases": 16, "planned_runs": 31}}
config_raw = (json.dumps(config, indent=2, sort_keys=True) + "\n").encode()
report = {
    "schema": "coordinator-indexed-oracle-inspection-v1", "payload_executed": False,
    "config_sha256": sha(config_raw), "review_pins": review_pins,
    "manual_inspection": [
        "Read complete independent indexed oracle; public value identity/order and builtin reference laws retained.",
        "Read cursor-v2 diff: same 24-publication ownership schedule, neutral successful-publication trigger.",
        "Check fixed 16/31 schedules, full phase costs, 14 P/C growth inequalities and exact retry/continuation.",
        "Check weakref positive owner then release with no sentinel token registry retention.",
        "Close missing I07 terminal-collision precondition before execution; no expectation tuning.",
        "Controller v4 aligns spec basename and independently checked exact identity/completion types.",
    ],
    "retained_scope": "34 unchanged storage runs + 28 cursor-successor runs + 31 indexed runs = 93 per child",
    "limitations": "No execution yet; favorable pure-store results cannot establish production cost/semantic fitness.",
}
note = f"""# Indexed prototype: first floor dispatch

Coordinator, 2026-08-31. The reviewed input config is
engineer-indexed-storage-config-v1.json SHA{sha(config_raw)}.
Controller v4 SHA{control_sha}; prototype SHA{entries['prototype'][1]}.

Authorize one root-dispatched serial child labelled radix-v1-first01, actual
CPython3.11.15, hashseed0. Fresh exact-r010 D-local snapshot, -S -B -P,
scrubbed environment, full manifest and direct-child60s timeout apply.
Run the fixed three phases (34+28+31) and retain all failures/partial work.
The wrapper completes its predeclared phases even after a phase error.
Inspect this result before any other seed/runtime. No production/W port,
cap/threshold change, broad suite, final freeze, integration or main push.

Before results, P uses the retained wrapper/content clarification; every
charge remains in full C. I07 must exercise the terminal collision route.
Old cursor executable differs only at the declared neutral retention trigger
and reporting; do not describe all62 predecessor paths as byte-identical.
The oracle/controller authoring issues were closed before any payload. The
final metric schedule and case bytes are unchanged. No success is asserted.
"""
for relative, raw in {
    "engineer-indexed-storage-config-v1.json": config_raw,
    "coordinator-indexed-oracle-inspection-v1.json": (json.dumps(report, indent=2) + "\n").encode(),
    "coordinator-indexed-prototype-first-dispatch-v1.md": note.encode(),
    "coordinator-configure-indexed-prototype-v1.py": Path(__file__).read_bytes(),
}.items():
    with (T / relative).open("xb") as stream:
        stream.write(raw)
print(json.dumps({"config_sha256": sha(config_raw), "inspection_sha256": sha((T / "coordinator-indexed-oracle-inspection-v1.json").read_bytes()),
                  "dispatch_note_sha256": sha(note.encode()), "oracle_delta": diff}))
