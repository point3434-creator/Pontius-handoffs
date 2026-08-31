"""Retain a proposed one-assertion correction; do not install or execute it."""
from pathlib import Path
import ast
import copy
import difflib
import hashlib
import json
import re

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
h = lambda raw: hashlib.sha256(raw).hexdigest()
before = (T / "tests-candidate-v4.py").read_bytes()
assert h(before) == "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
old = '"analysis.*(?:depth|budget)"'
new = '"^analysis (?:helper depth exceeds 64|work units exceed 262144)$"'
assert before.count(old.encode()) == 1
after = before.replace(old.encode(), new.encode(), 1)
old_tree, new_tree = ast.parse(before), ast.parse(after)
compile(new_tree, "static-only-candidate", "exec")
old_nodes = [n for n in ast.walk(old_tree) if isinstance(n, ast.Constant) and n.value == old[1:-1]]
new_nodes = [n for n in ast.walk(new_tree) if isinstance(n, ast.Constant) and n.value == new[1:-1]]
assert len(old_nodes) == len(new_nodes) == 1
method, = [n for n in ast.walk(old_tree) if isinstance(n, ast.FunctionDef) and n.name == "test_analysis_budgets_contain_deep_helpers_and_invalid_ranges"]
assert old_nodes[0] in tuple(ast.walk(method))
new_nodes[0].value = old_nodes[0].value
assert ast.dump(old_tree, include_attributes=False) == ast.dump(new_tree, include_attributes=False)
pattern = new[1:-1]
checks = {message: re.search(pattern, message) is not None for message in (
    "analysis helper depth exceeds 64", "analysis work units exceed 262144",
    "analysis helper depth exceeds 63", "analysis work units exceed 262145",
    "analysis arbitrary budget issue", "prefix analysis work units exceed 262144 suffix",
    "analysis deferred generator depth exceeds 64")}
assert list(checks.values()) == [True, True, False, False, False, False, False]
note = f'''# Proposed helper1050 budget-assertion correction

This is a new reviewable test candidate, not a relabeling of any prior failed run.
Original r010 and tests-candidate-v4 bytes remain immutable. No W/main change,
payload, analyzer cap or production error wording change is made here.

Source: tests-candidate-v4.py SHA256 {h(before)}.
Candidate: tests-candidate-v5.py SHA256 {h(after)}.

The helper1050 test explicitly accepts an analysis depth OR budget refusal, but
its regex does not match the canonical work-budget error. The original separate
budget-boundary test explicitly requires that exact canonical message. The
contradiction and both source anchors are retained in
coordinator-helper1050-contract-clarification-v1.json.

Only this assertion's regex changes, from:
`analysis.*(?:depth|budget)`
to:
`^analysis (?:helper depth exceeds 64|work units exceed 262144)$`

This recognizes the two precise admissible outcomes for this helper-chain
fixture. It does not accept arbitrary errors mentioning a budget, change the
1050-definition source, skip its execution, or raise the existing 64-depth and
262144-work limits. The independent helper65 and generator70 exact-depth
assertions remain byte-for-byte unchanged, as do all other test AST nodes and
the existing fixed matrix. The regex-only static check is not a payload verdict.

Category: bounded-analysis refusal classification. Enumeration: the one old
depth-or-budget regex, both production canonical error paths, the separate
exact work-budget assertion, and both exact-depth fixtures. This closes an
inconsistent assertion; it makes no claim that storage or analyzer semantics
are repaired. Review this delta before adapting any frozen focused controller.
All earlier design runs retain their recorded failures and original manifests.
'''.encode()
report = {"schema": "coordinator-budget-assertion-candidate-static-v1",
          "before_sha256": h(before), "candidate_sha256": h(after),
          "only_changed_ast_constant": {"method": method.name, "before": old[1:-1], "after": pattern},
          "all_other_test_ast_equal": True, "pure_regex_checks": checks,
          "payload_executed": False, "installed": False,
          "standing": "Proposed narrow consistency correction; independent review pending."}
delta = ''.join(difflib.unified_diff(before.decode().splitlines(True), after.decode().splitlines(True),
                                   fromfile="tests-candidate-v4.py", tofile="tests-candidate-v5.py")).encode()
outputs = {"tests-candidate-v5.py": after,
           "tests-candidate-v5-from-v4.diff": delta,
           "coordinator-budget-assertion-candidate-v1.md": note,
           "coordinator-budget-assertion-candidate-static-v1.json": (json.dumps(report, indent=2) + "\n").encode(),
           "coordinator-author-budget-assertion-candidate-v1.py": Path(__file__).read_bytes()}
assert not any((T / name).exists() for name in outputs)
for name, raw in outputs.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({name: h(raw) for name, raw in outputs.items()}))
