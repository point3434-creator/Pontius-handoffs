import ast
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
WORK = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
TEST = "tests/test_inventory_and_profiles.py"
EXPECTED = "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
FAMILY = "joined-activation-alternatives"
METHOD = "test_authority_transfer_joined_activation_alternatives"
R010_GENERATOR = "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
ITER05_GENERATOR = "33f944158ca20df62724d83d44a680440c455653100ba28d67b69954849cd8a5"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def create(path, text):
    raw = text.encode("utf-8")
    assert b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf")
    with path.open("xb") as stream:
        stream.write(raw)
    return sha(raw)


assert sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15)
assert Path(sys.executable).resolve() == Path(r"D:\Pontius-tools\py311\Scripts\python.exe").resolve()
assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path
prior = (ROOT / "tests-candidate-v3.py").read_bytes()
assert sha(prior) == "59a7698d9dcf564a54cb98be2c5893f2c58e9d8adea1d03daf8ea0a38eef33db"
data = (ROOT / "tests-candidate-v4.py").read_bytes()
assert sha(data) == EXPECTED and (WORK / TEST).read_bytes() == data
footer = b'\n\nif __name__ == "__main__":\n    unittest.main()\n'
assert prior.endswith(footer) and data.startswith(prior[:-len(footer)])
old_tree, tree = ast.parse(prior), ast.parse(data)
new_class = next(n for n in tree.body
                 if isinstance(n, ast.ClassDef) and n.name == "AuthorityTransferMatrixTests")
methods = [{"name": n.name, "line": n.lineno} for n in new_class.body
           if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
new_method = next(n for n in new_class.body if isinstance(n, ast.FunctionDef) and n.name == METHOD)
new_method_line = new_method.lineno
new_class.body.remove(new_method)
assert ast.dump(old_tree) == ast.dump(tree), "old test AST changed"
assert len(methods) == 8
old_proof_path = ROOT / "tests-checks/release-v3-proof.json"
assert sha(old_proof_path.read_bytes()) == (
    "e592af6fa848607c805e90a3252fb9b8f6b71e090f6f170468129934a4573655")
old_proof = json.loads(old_proof_path.read_text())
old_cases = {(r["matrix"], r["case"]): r for r in old_proof["cases"]}
assert len(old_cases) == 176
apply = json.loads((ROOT / "tests-checks/apply-v4.json").read_text())
assert apply["tests_sha256"] == EXPECTED and apply["all_old_ast_unchanged"]
by_baseline = {}
receipts = []
for baseline, expected_count, expected_failures, expected_generator in (
    ("iteration05", 16, 2, ITER05_GENERATOR), ("r010", 192, 39, R010_GENERATOR),
):
    canonical = None
    for slot in ("311", "314"):
        receipt_path = ROOT / ("tests-checks/red-v4-" + baseline + "-" + slot + "-receipt.json")
        receipt = json.loads(receipt_path.read_text())
        raw = Path(receipt["log"]).read_bytes()
        assert sha(raw) == receipt["log_sha256"]
        assert receipt["tests_sha256"] == EXPECTED
        assert receipt["generator_sha256"] == expected_generator
        assert receipt["exit"] == 1
        assert ("FAILED (failures=" + str(expected_failures) + ")").encode() in raw
        assert b"ERROR:" not in raw
        records = [json.loads(line) for line in raw.splitlines() if line.startswith(b'{"matrix":')]
        assert len(records) == expected_count
        if canonical is None:
            canonical = records
        else:
            assert canonical == records
        summaries = receipt["matrix_summaries"]
        assert sum(s["planned"] for s in summaries) == expected_count
        for summary in summaries:
            assert summary["planned"] == summary["generated"] == summary["exercised"]
            assert not summary["oracle_errors"] and not summary["analyzer_errors"]
            assert not summary["unreachable_cases"]
        failures = [r for r in records if
                    (r["classification"] == "refuse" and not r["blockers"]) or
                    (r["classification"] == "clean" and r["blockers"]) or
                    (r["classification"] == "permitted-refusal" and not r["blockers"]
                     and r["argv"] != [["-m", "fixed"]])]
        assert len(failures) == expected_failures
        if baseline == "iteration05":
            assert {r["case"] for r in failures} == {
                "cell/unsafe-first/statement", "cell/unsafe-first/conditional"}
            assert sum(r["classification"] == "refuse" for r in records) == 12
            assert sum(r["classification"] == "permitted-refusal" for r in records) == 4
        else:
            unchanged = [r for r in records if r["matrix"] != FAMILY]
            assert len(unchanged) == 176
            for r in unchanged:
                assert old_cases[(r["matrix"], r["case"])] == r
            assert not [r for r in failures if r["matrix"] == FAMILY]
        receipts.append({
            "baseline": baseline, "slot": slot, "identity": receipt["identity"],
            "generator_sha256": expected_generator, "receipt_sha256": sha(receipt_path.read_bytes()),
            "log_sha256": receipt["log_sha256"], "exit": receipt["exit"],
            "planned": expected_count, "generated": expected_count, "exercised": expected_count,
            "runtime_projections": sum(len(r["witnesses"]) for r in records),
            "failures": len(failures), "passing_schedules": expected_count - len(failures),
            "failure_ids": [{"matrix": r["matrix"], "case": r["case"]} for r in failures],
            "all_tracked_paths_unchanged": receipt["all_tracked_paths_unchanged"],
            "matrix_summaries": summaries,
        })
    by_baseline[baseline] = canonical
r010_new = {r["case"]: r for r in by_baseline["r010"] if r["matrix"] == FAMILY}
for r in by_baseline["iteration05"]:
    stable = lambda x: {k: v for k, v in x.items() if k not in {"argv", "blockers"}}
    assert stable(r) == stable(r010_new[r["case"]])
preservation = [{
    "matrix": r["matrix"], "case": r["case"], "classification": r["classification"],
    "source_sha256": r["source_sha256"], "oracle_sha256": r["oracle_sha256"],
    "entire_public_case_record_unchanged_on_r010": True,
} for r in old_cases.values()]
proof = {
    "purpose": "v4 joined-activation category release with separate iteration05 and r010 RED",
    "base": apply["base"], "tests_sha256": EXPECTED, "patch_sha256": apply["patch_sha256"],
    "previous_tests_sha256": sha(prior), "new_method": METHOD, "new_method_line": new_method_line,
    "new_method_count_since_v3": 1, "matrix_method_count": 8, "total_test_method_count": 127,
    "all_v3_ast_unchanged_except_added_method": True, "v3_source_prefix_unchanged": True,
    "preserved_v3_cases": preservation, "preserved_v3_case_count": 176,
    "new_family_planned": 16, "new_family_generated": 16, "new_family_exercised_per_slot": 16,
    "new_family_runtime_projections_per_slot": 32, "new_required_refusal": 12,
    "new_permitted_refusal": 4, "combined_required_clean": 81,
    "combined_required_refusal": 92, "combined_permitted_refusal": 19,
    "combined_planned": 192, "combined_generated": 192, "combined_exercised_per_slot": 192,
    "combined_runtime_projections_per_slot": 212, "unreachable_cases": [],
    "new_method_discovery": methods, "receipts": receipts, "cases_by_baseline": by_baseline,
    "same_new_schedule_source_oracle_witnesses_across_baselines": True,
    "infrastructure_attempts": [{
        "artifact": "tests-join-control-derive-v1.py",
        "outcome": "AssertionError: ambiguous AuthorityTransferMatrixTests text match",
        "effect": "No payload ran and no derived wrapper was issued; not product RED",
        "resolution": "Exact sys.argv match in preserved tests-join-control-derive-v2.py",
    }],
    "limitations": [
        "Iteration05 is an immutable generator overlay on r010, not the frozen r010 generator",
        "Only the new family was executed against iteration05",
        "Full matrix execution is distinct from the original119-suite/census/141row gates",
        "No production generator implementation was inspected or modified",
    ],
}
proof_path = ROOT / "tests-checks/release-v4-proof.json"
proof_hash = create(proof_path, json.dumps(proof, indent=2) + "\n")
text = """# Released authority-transfer matrix tests v4

This adds one joined-activation category method and preserves all v3 tests and
expectations. Issued v2/v3/addendum/raw evidence remain immutable. The worktree
test file equals this released artifact; this author has stopped editing.

Candidate: tests-candidate-v4.py.
Tests SHA-256: """ + EXPECTED + """.
Patch: tests-patch-v4.diff, SHA-256 """ + apply["patch_sha256"] + """.
Proof: tests-checks/release-v4-proof.json, SHA-256 """ + proof_hash + """.

New method: """ + METHOD + " (line " + str(new_method_line) + """).

The finite matrix is capture (cell/default) x allocation order (unsafe-first,
safe-first, both-safe, both-unsafe) x selection (statement if/conditional
expression): 16 schedules, each with both runtime choices, 32 pure projections.
Twelve schedules have a feasible unsafe selected callback and require explicit
blockers. Four both-safe schedules permit explicit refusal for optional effective
result precision; without a blocker they require the fixed sink row. They do not
require general callback or async interpretation.

The existing independent _program/_exercise helpers are unchanged. Pure projections
record body/write/sink and expected TypeError/fixed outcomes. Sensitive fixture
source bytes are passed only to derive_design_review, never executed. The two
factory activations use the same lexical callback body but distinct captured
owners; both selection forms must retain every feasible authority alternative.

| Verification baseline | Focus | Schedules / projections per slot | Fail / pass |
| --- | --- | ---: | ---: |
| Immutable iteration05 generator overlay | New family only | 16 / 32 | 2 / 14 |
| Frozen r010 generator | All eight matrix methods | 192 / 212 | 39 / 153 |

Iteration05 generator SHA-256:
""" + ITER05_GENERATOR + """.
Frozen r010 commit: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.
Frozen r010 generator SHA-256:
""" + R010_GENERATOR + """.

Both baselines ran actual CPython 3.11.15 first, then actual 3.14.6. Within each
baseline, the two slots produced identical per-case records. Iteration05 fails
cell/unsafe-first/statement and cell/unsafe-first/conditional: the unsafe runtime
valuation writes then raises TypeError, but public analysis emits fixed argv
without a blocker. The other fourteen category cases pass. The new sixteen cases
all pass their assertions on r010; its combined 39 failures are exactly v3's prior
39 failures. These results must not be conflated into one source baseline.

The proof records all 176 preserved v3 IDs individually. Their source hashes,
oracle hashes, classifications, traces and entire public result records match
the corresponding v3 r010 records exactly. Removing only the new method makes
the v4 AST identical to v3; its earlier source prefix is byte-identical. All old
119 methods, seven prior matrix methods, helpers, constants and original source
lines are unchanged. Static discovery now has 127 methods. Combined expectations
are 92 required-refuse, 81 required-clean and 19 permitted-refusal, totaling 192.

Every planned schedule was generated and exercised; no schedule was unreachable.
The logs separately record proved unexecuted write events in both-safe cases.
There were zero runtime-oracle or analyzer exceptions. The failed first wrapper
derivation is recorded as infrastructure only: no test payload ran then.

Each baseline used its own fresh D-local disposable r010 clone. For iteration05,
only hash-verified immutable coordinator-snapshot generator bytes and v4 tests
were overlaid; source was copied and hashed, not inspected. For r010, only v4 tests
were overlaid. Controls used -I -S -B -P; payloads used -B -P, exact executable and
patch assertions before repository imports, snapshot cwd/src PYTHONPATH, scrubbed
environment, D-local temporary files and validated absolute Git. All 1761 tracked
paths retained their before hashes after each run. Logs and receipts are under
tests-checks/red-v4-iteration05-{311,314}* and red-v4-r010-{311,314}*.

This release is bounded regression evidence, not replacement GREEN or permission
for a broader wall. Parent retains census/generated-output work, preservation of
the prior 141 capability rows, full-suite gates and later cold reviews. No
production source, budget, ledger or generated output was modified by this author.
"""
release_hash = create(ROOT / "tests-release-v4.md", text)
print(json.dumps({"tests_sha256": EXPECTED, "patch_sha256": apply["patch_sha256"],
                  "proof_sha256": proof_hash, "release_sha256": release_hash,
                  "new_method_line": new_method_line, "old_cases_preserved": 176,
                  "iteration05_failures_per_slot": 2, "r010_failures_per_slot": 39}))

