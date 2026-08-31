"""Record a source/assertion classification correction; change no source or test."""
import ast
import hashlib
import json
from pathlib import Path
import re

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
h = lambda raw: hashlib.sha256(raw).hexdigest()
receipt_raw = (T / "tests-checks/depth-budget-v26-cost01-helper1050-311-receipt.json").read_bytes()
assert h(receipt_raw) == "39c226dd9a619edc22da425d846a4e07319eb24bb42064f5e323392fb352015f"
receipt = json.loads(receipt_raw)
tests = (Path(receipt["snapshot"]) / "tests/test_inventory_and_profiles.py").read_bytes()
assert h(tests) == "c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf"
tree = ast.parse(tests)
def pattern_at(line):
    call, = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and n.lineno == line
             and isinstance(n.func, ast.Attribute) and n.func.attr == "assertRaisesRegex"]
    return ast.literal_eval(call.args[1])
helper_pattern = pattern_at(4949)
work_pattern = pattern_at(20585)
assert helper_pattern == "analysis.*(?:depth|budget)"
assert work_pattern == "^analysis work units exceed 262144$"
complete = receipt["verification"]["completion"]
observed = complete["refusal"]
assert observed == "analysis work units exceed 262144"
assert complete["budget_failures"] == 1 and complete["caps_unchanged"] is True
assert re.search(helper_pattern, observed) is None and re.search(work_pattern, observed) is not None
report = {"schema": "coordinator-helper1050-contract-clarification-v1",
          "standing": "Engineering source/contract clarification, not a cold review or changed acceptance verdict",
          "base_frozen_candidate": "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358",
          "base_manifest_sha256": "8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb",
          "original_tests_sha256": h(tests), "diagnostic_receipt_sha256": h(receipt_raw),
          "diagnostic_manifest_sha256": receipt["manifest_sha256"],
          "diagnostic_source_sha256": receipt["source_sha256"],
          "helper1050_allowed_pattern": helper_pattern, "separate_canonical_budget_pattern": work_pattern,
          "observed_refusal": observed, "helper1050_regex_matches": False,
          "canonical_work_budget_regex_matches": True,
          "correction": "Helper1050 permits depth or budget; it does not require reaching helper depth after1050definitions. A bounded work refusal is already observed, but the unchanged helper test does not recognize its canonical wording. The two exact-depth tests remain substantive depth-versus-work failures.",
          "disposition": "Keep current50/53 outcome and all failed artifacts. No source, error string, assertion, cap or expected label is changed. Any future recognition of the canonical budget category requires an explicit expectation reconciliation in a new candidate; never retroactively label this run green.",
          "payload_executed": False}
note = """# Correction: helper1050 permits a budget refusal

Engineering clarification only. Exact frozen-test, diagnostic-manifest and
receipt hashes are in coordinator-helper1050-contract-clarification-v1.json.

The original helper1050 assertion at4949 allows `analysis.*(?:depth|budget)`.
The existing work-cap error is `analysis work units exceed 262144`; a separate
original assertion at20585 requires that exact canonical wording. The retained
v26 diagnostic observes precisely this bounded refusal, with unchanged caps.
The first regex nevertheless rejects it because it contains neither literal
`depth` nor `budget`.

Root and an independent engineering reviewer confirm that this is an assertion/
error-category wording inconsistency. It is not evidence that1050definitions
must all be registered before a helper-depth refusal. Earlier descriptions
treating all three design failures as exact-depth obligations were too broad.

The helper65 and generator70 tests do require their exact depth refusals; their
premature work-budget failures remain substantive. The actual v26 suite outcome
is still50/53, with3failed assertions and0errors. No failed evidence becomes green.

No source, error message, test, label or cap is changed by this note. A future
expectation reconciliation could recognize the already canonical work-budget
category while retaining the exact allowed depth category. It must be explicit,
reviewed and issued as a new candidate, not hidden inside an optimization or
applied retroactively. The v28 freeze optimization still targets measured waste;
it must not be justified as a requirement that helper1050 reach depth specifically.
""".encode()
outputs = {"coordinator-helper1050-contract-clarification-v1.json": (json.dumps(report, indent=2) + "\n").encode(),
           "coordinator-helper1050-contract-clarification-v1.md": note,
           "coordinator-record-helper1050-contract-v1.py": Path(__file__).read_bytes()}
assert not any((T / name).exists() for name in outputs)
for name, raw in outputs.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({name: h(raw) for name, raw in outputs.items()}))
