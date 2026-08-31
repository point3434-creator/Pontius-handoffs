"""Retain the failed evidence-reader premise and create its corrected successor."""
from pathlib import Path
import ast
import hashlib
import json

D = Path(r"D:\Pontius")
T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
before = (D / "codex-verify-v28-testfix-v1.py").read_bytes()
h = lambda raw: hashlib.sha256(raw).hexdigest()
assert h(before) == "37a5e349c051ba0d303fc7b3fc16ac5c0f2d05ec3f40e75bbcbfe9802bcf3b5e"
source = before.decode()
assert source.count('assert "line 14553" in stderr') == 1
source = source.replace('assert "line 14553" in stderr', 'assert \'AssertionError: "^analysis deferred generator depth exceeds 64$" does not match "analysis work units exceed 262144"\' in stderr')
source = source.replace('coordinator-v28-testfix-verification-v1', 'coordinator-v28-testfix-verification-v2')
source = source.replace('coordinator-verify-v28-testfix-v1.py', 'coordinator-verify-v28-testfix-v2.py')
source = source.replace('"payload_executed_by_verifier": False,', '"payload_executed_by_verifier": False,\n    "verifier_correction": "V1 stopped before report output on a mistaken physical traceback line assumption (14553 regex literal versus14551 with-statement). V2 binds the exact failure method and both canonical messages. No payload or evidence changed.",')
ast.parse(source)
compile(source, "static-only-verifier", "exec")
path = D / "codex-verify-v28-testfix-v2.py"
with path.open("xb") as stream:
    stream.write(source.encode())
note = {"schema": "coordinator-testfix-verifier-v1-failure", "failed_verifier_sha256": h(before),
        "failure": "AssertionError at expected traceback line14553; actual context-manager line14551, literal line14553.",
        "prior_checks": "Snapshot1766 files, inputs, raw outputs, identity, exact53 completion and one canonical generator-depth failure checked before this assertion.",
        "report_issued_by_v1": False, "payload_rerun": False, "raw_evidence_changed": False,
        "successor": path.name, "successor_sha256": h(source.encode())}
outputs = {"coordinator-verify-v28-testfix-v1.py": before,
           "coordinator-testfix-verifier-v1-failure.json": (json.dumps(note, indent=2) + "\n").encode(),
           "coordinator-correct-testfix-verifier-v2.py": Path(__file__).read_bytes()}
assert not any((T / name).exists() for name in outputs)
for name, raw in outputs.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({"successor": str(path), "sha256": h(source.encode()), "payload_rerun": False}))
