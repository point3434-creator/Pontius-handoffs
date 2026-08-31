import ast
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
WORK = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
TEST = "tests/test_inventory_and_profiles.py"
EXPECTED = "59a7698d9dcf564a54cb98be2c5893f2c58e9d8adea1d03daf8ea0a38eef33db"


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
expected_changes = {
    ("capture-route-execution", capture + "/" + route + "/" + mode)
    for capture in ("default", "cell")
    for route in ("return", "returned-nest", "flat-store")
    for mode in ("readonly", "raise-before")
}
expected_changes.update(
    ("live-cells-and-activations", "cell/False/" + returned + "/False")
    for returned in ("callback", "(callback,)[0]", '{"cb": callback}["cb"]')
)
assert len(expected_changes) == 15
data = (ROOT / "tests-candidate-v3.py").read_bytes()
assert sha(data) == EXPECTED and (WORK / TEST).read_bytes() == data
old_data = (ROOT / "tests-candidate-v2.py").read_bytes()
assert sha(old_data) == "c7f8d1ada3cdddc413f5074133cdbf2203ae9f62dfbb06798cddb984b1cb237f"
old_tree, tree = ast.parse(old_data), ast.parse(data)
old_class = next(n for n in old_tree.body
                 if isinstance(n, ast.ClassDef) and n.name == "AuthorityTransferMatrixTests")
new_class = next(n for n in tree.body
                 if isinstance(n, ast.ClassDef) and n.name == "AuthorityTransferMatrixTests")
methods = [{"name": n.name, "line": n.lineno} for n in new_class.body
           if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
old_tree.body.remove(old_class)
tree.body.remove(new_class)
assert ast.dump(old_tree) == ast.dump(tree)
changed_methods = []
for old, new in zip(old_class.body, new_class.body):
    if ast.dump(old) == ast.dump(new):
        continue
    assert isinstance(old, ast.FunctionDef) and old.name == new.name
    old_keywords = [n for n in ast.walk(old) if isinstance(n, ast.keyword)
                    and n.arg == "classification"]
    new_keywords = [n for n in ast.walk(new) if isinstance(n, ast.keyword)
                    and n.arg == "classification"]
    pairs = [(a, b) for a, b in zip(old_keywords, new_keywords) if ast.dump(a) != ast.dump(b)]
    assert len(pairs) == 1
    pairs[0][1].value = pairs[0][0].value
    assert ast.dump(old) == ast.dump(new)
    changed_methods.append(old.name)
assert changed_methods == [
    "test_authority_transfer_capture_route_execution_matrix",
    "test_authority_transfer_live_cells_and_activation_identity",
]
apply = json.loads((ROOT / "tests-checks/apply-v3.json").read_text())
assert apply["tests_sha256"] == EXPECTED
assert apply["all_old_ast_unchanged"] and apply["old_source_prefix_unchanged"]
old_proof_path = ROOT / "tests-checks/release-v2-proof.json"
assert sha(old_proof_path.read_bytes()) == (
    "3094815a0a0006df09c9c33e08e092664f1c68b4b99d3df882aa6fa15511f620")
old_records = json.loads(old_proof_path.read_text())["cases"]
old_by_id = {(r["matrix"], r["case"]): r for r in old_records}
slots = []
canonical = None
changes = []
for slot in ("311", "314"):
    receipt_path = ROOT / ("tests-checks/red-v3-" + slot + "-receipt.json")
    receipt = json.loads(receipt_path.read_text())
    log = Path(receipt["log"]).read_bytes()
    assert sha(log) == receipt["log_sha256"]
    assert receipt["exit"] == 1 and b"FAILED (failures=39)" in log and b"ERROR:" not in log
    assert receipt["tests_sha256"] == EXPECTED
    assert receipt["generator_sha256"] == (
        "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692")
    records = [json.loads(line) for line in log.splitlines() if line.startswith(b'{"matrix":')]
    assert len(records) == 176
    actual_changes = []
    for row in records:
        key = (row["matrix"], row["case"])
        before = old_by_id[key]
        without = lambda r: {k: v for k, v in r.items() if k != "classification"}
        assert without(before) == without(row), "source/oracle/result changed: " + repr(key)
        if row["classification"] != before["classification"]:
            assert key in expected_changes
            assert before["classification"] == "clean"
            assert row["classification"] == "permitted-refusal"
            actual_changes.append({
                "matrix": row["matrix"], "case": row["case"],
                "before": "clean", "after": "permitted-refusal",
                "source_sha256": row["source_sha256"], "oracle_sha256": row["oracle_sha256"],
            })
    assert {(r["matrix"], r["case"]) for r in actual_changes} == expected_changes
    if canonical is None:
        canonical, changes = records, actual_changes
    else:
        assert canonical == records and changes == actual_changes
    summaries = receipt["matrix_summaries"]
    assert len(summaries) == 7 and sum(s["planned"] for s in summaries) == 176
    for summary in summaries:
        assert summary["planned"] == summary["generated"] == summary["exercised"]
        assert not summary["oracle_errors"] and not summary["analyzer_errors"]
        assert not summary["unreachable_cases"]
    mismatches = [r for r in records if
                  (r["classification"] == "clean" and r["blockers"]) or
                  (r["classification"] == "refuse" and not r["blockers"])]
    assert len(mismatches) == 39
    assert sum(r["classification"] == "refuse" for r in mismatches) == 38
    assert sum(r["classification"] == "clean" for r in mismatches) == 1
    safe_failure, = [r for r in mismatches if r["classification"] == "clean"]
    assert (safe_failure["matrix"], safe_failure["case"]) == (
        "ordered-class-binding", "construction-failure/decorator/True")
    assert sum(r["matrix"] == "issued-witnesses" for r in mismatches) == 16
    assert sum(r["classification"] == "clean" for r in records) == 81
    assert sum(r["classification"] == "refuse" for r in records) == 80
    assert sum(r["classification"] == "permitted-refusal" for r in records) == 15
    slots.append({
        "slot": slot, "identity": receipt["identity"], "exit": receipt["exit"],
        "receipt_sha256": sha(receipt_path.read_bytes()), "log_sha256": receipt["log_sha256"],
        "planned": 176, "generated": 176, "exercised": 176,
        "oracle_run_count": sum(len(r["witnesses"]) for r in records),
        "assertion_failures": 39, "missed_unsafe_blockers": 38,
        "required_clean_refusals": 1, "issued_witness_failures": 16,
        "all_tracked_paths_unchanged": receipt["all_tracked_paths_unchanged"],
        "all_v2_case_bytes_oracles_traces_public_results_equal": True,
        "matrix_summaries": summaries,
    })
proof = {
    "purpose": "Corrected expectation release and valid frozen-r010 RED; no replacement GREEN",
    "base": apply["base"], "tests_sha256": EXPECTED, "patch_sha256": apply["patch_sha256"],
    "previous_tests_sha256": sha(old_data), "old_method_count": 119,
    "new_method_count": 7, "total_method_count": 126, "new_methods": methods,
    "only_new_test_ast_changes": "two classification keyword expressions",
    "changed_methods": changed_methods, "changed_case_ids": changes,
    "all_old_ast_unchanged": True, "old_source_prefix_unchanged": True,
    "all176_source_oracle_hashes_traces_results_unchanged_from_v2": True,
    "required_clean_cases": 81, "required_refusal_cases": 80,
    "permitted_refusal_cases": 15, "planned": 176, "generated": 176,
    "exercised_per_slot": 176, "unreachable_cases": [], "slots": slots, "cases": canonical,
    "scope_addendum_sha256": "76db37e2edaa05f058e8514d9209c6d5f2f057a8860417a5bf6da39f24602e22",
    "limitations": [
        "Finite contract matrix, not general Python callback or async support",
        "No replacement production inspection or execution",
        "No full old119 suite, generated census or141row preservation check in this test-only release",
    ],
}
proof_path = ROOT / "tests-checks/release-v3-proof.json"
proof_sha = create(proof_path, json.dumps(proof, indent=2) + "\n")
rows = []
for summary in slots[0]["matrix_summaries"]:
    members = [r for r in canonical if r["matrix"] == summary["matrix_summary"]]
    counts = [sum(r["classification"] == c for r in members)
              for c in ("clean", "refuse", "permitted-refusal")]
    rows.append("| " + summary["matrix_summary"] + " | " + str(len(members)) + " | "
                + " | ".join(map(str, counts)) + " |")
body = """# Released authority-transfer matrix tests v3

This release corrects only the fifteen classifications accepted in
tests-scope-addendum-v1.md. All issued v2 files, addendum and evidence remain
unchanged. The v3 worktree test file is released; this author has stopped editing.

Base: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.
Candidate: tests-candidate-v3.py.
Tests SHA-256: """ + EXPECTED + """.
Patch: tests-patch-v3.diff, SHA-256 """ + apply["patch_sha256"] + """.
Proof: tests-checks/release-v3-proof.json, SHA-256 """ + proof_sha + """.

Only two classification keyword expressions changed from v2. The exact fifteen
case-ID changes are recorded individually in the proof, each with before/after
classification and unchanged sensitive-source/oracle hashes. All 176 emitted case
records match v2 exactly after removing classification: schedules, source bytes,
pure projections, runtime traces, public argv, blockers and unreachable events are
identical. All 80 required-refuse and remaining 81 required-clean expectations stay
binding, including construction-failure/decorator/True.

| Family | Planned/generated/exercised per slot | Required clean | Required refuse | Permitted refusal |
| --- | ---: | ---: | ---: | ---: |
""" + "\n".join(rows) + """

There are seven new methods and 176 finite schedules, with 180 harmless runtime
projections per slot. No schedule is unreachable; logs separately record unexecuted
events within exercised schedules. All old 119 methods, ASTs, constants and source
prefix remain unchanged; static method discovery remains 126. The only new-test
AST changes are the two approved classification expressions. Parent handles all
census/generated outputs; no generator, budget or production path was edited here.

The exact permitted set is capture-route-execution
{default,cell}/{return,returned-nest,flat-store}/{readonly,raise-before} (12),
plus live-cells-and-activations
cell/False/{callback,(callback,)[0],{"cb": callback}["cb"]}/False (3).
These accept explicit blockers; without blockers they still require the exact
fixed sink argv. Runtime safety alone does not mandate optional effective-result
precision. No dormant control, unsafe witness or proved decorator nonexecution
expectation was weakened.

RED was run on a fresh disposable D-local r010 clone, overlaid only with v3 test
bytes; unchanged frozen generator SHA-256
29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692.
Actual CPython 3.11.15 ran first and actual CPython 3.14.6 second. The control used
-I -S -B -P, payloads -B -P, exact executable/patch identity before repository
imports, scrubbed environment, snapshot cwd/src PYTHONPATH, D-local temporary
paths, and validated absolute Git. All 1761 tracked paths retained their hashes.

Both runs produced exactly 39 assertion failures: 38 missing unsafe blockers and
the one required clean decorator-nonexecution case. All A9+B7 witnesses remain
RED. The other 137 schedules pass the corrected expectations. All 176 schedules
were exercised, with zero oracle errors or analyzer exceptions. No infrastructure
error is counted as product RED. Full logs and receipts:
tests-checks/red-v3-311.txt and red-v3-311-receipt.json;
tests-checks/red-v3-314.txt and red-v3-314-receipt.json.

This is corrected test release and frozen-r010 RED evidence, not replacement
GREEN. No production implementation was inspected or executed. The full old suite,
141 original capability rows, generated census/profile preservation, later cold
reviews and any acceptance wall remain separate parent-owned gates.

Method discovery:
""" + "\n".join("- " + m["name"] + " (line " + str(m["line"]) + ")" for m in methods) + "\n"
release_sha = create(ROOT / "tests-release-v3.md", body)
print(json.dumps({"tests_sha256": EXPECTED, "patch_sha256": apply["patch_sha256"],
                  "proof_sha256": proof_sha, "release_sha256": release_sha,
                  "changed_case_count": len(changes), "failures_per_slot": 39,
                  "methods": methods}))

