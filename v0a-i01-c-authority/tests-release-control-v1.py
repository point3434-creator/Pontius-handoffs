import ast
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
WORK = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
TEST = "tests/test_inventory_and_profiles.py"
EXPECTED = "c7f8d1ada3cdddc413f5074133cdbf2203ae9f62dfbb06798cddb984b1cb237f"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def create(path, content):
    data = content.encode("utf-8") if isinstance(content, str) else content
    assert b"\r" not in data and not data.startswith(b"\xef\xbb\xbf")
    with path.open("xb") as stream:
        stream.write(data)
    return digest(data)


assert sys.implementation.name == "cpython"
assert sys.version_info[:3] == (3, 11, 15)
assert Path(sys.executable).resolve() == Path(r"D:\Pontius-tools\py311\Scripts\python.exe").resolve()
assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path
data = (ROOT / "tests-candidate-v2.py").read_bytes()
assert digest(data) == EXPECTED
assert (WORK / TEST).read_bytes() == data
tree = ast.parse(data)
classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
new_class = next(n for n in classes if n.name == "AuthorityTransferMatrixTests")
new_methods = [{"name": n.name, "line": n.lineno} for n in new_class.body
               if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
all_methods = [n.name for c in classes for n in c.body
               if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
assert len(new_methods) == 7
assert len(all_methods) == 126
apply = json.loads((ROOT / "tests-checks/apply-v2.json").read_text())
assert apply["all_old_ast_unchanged"] and apply["old_source_prefix_unchanged"]
assert apply["tests_sha256"] == EXPECTED
slots = []
canonical = None
for slot in ("311", "314"):
    receipt_path = ROOT / ("tests-checks/red-v2-" + slot + "-receipt.json")
    receipt = json.loads(receipt_path.read_text())
    log = Path(receipt["log"]).read_bytes()
    assert digest(log) == receipt["log_sha256"]
    assert receipt["exit"] == 1
    assert receipt["tests_sha256"] == EXPECTED
    assert receipt["generator_sha256"] == (
        "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692")
    assert b"FAILED (failures=54)" in log
    assert b"ERROR:" not in log
    records = [json.loads(line) for line in log.splitlines() if line.startswith(b'{"matrix":')]
    assert len(records) == 176
    if canonical is None:
        canonical = records
    else:
        assert canonical == records, "slot outcomes differ"
    summaries = receipt["matrix_summaries"]
    assert len(summaries) == 7
    assert sum(s["planned"] for s in summaries) == 176
    for summary in summaries:
        assert summary["planned"] == summary["generated"] == summary["exercised"]
        assert not summary["oracle_errors"] and not summary["analyzer_errors"]
        assert not summary["unreachable_cases"]
    mismatches = [r for r in records if
                  (r["classification"] == "clean" and r["blockers"]) or
                  (r["classification"] == "refuse" and not r["blockers"])]
    assert len(mismatches) == 54
    issued = [r for r in mismatches if r["matrix"] == "issued-witnesses"]
    assert len(issued) == 16
    assert sum(r["classification"] == "clean" for r in records) == 96
    assert sum(r["classification"] == "refuse" for r in records) == 80
    slots.append({
        "slot": slot, "identity": receipt["identity"],
        "receipt_sha256": digest(receipt_path.read_bytes()),
        "log_sha256": receipt["log_sha256"], "exit": receipt["exit"],
        "case_count": len(records), "oracle_run_count": sum(len(r["witnesses"]) for r in records),
        "assertion_failures": len(mismatches),
        "missed_unsafe_blockers": sum(r["classification"] == "refuse" for r in mismatches),
        "refused_lawful_cases": sum(r["classification"] == "clean" for r in mismatches),
        "issued_witness_failures": len(issued), "matrix_summaries": summaries,
        "all_tracked_paths_unchanged": receipt["all_tracked_paths_unchanged"],
    })
proof = {
    "purpose": "Released tests and valid RED only; replacement production is not verified",
    "base": apply["base"], "tests_sha256": EXPECTED,
    "patch_sha256": apply["patch_sha256"], "old_method_count": 119,
    "new_method_count": 7, "total_method_count": 126, "new_methods": new_methods,
    "all_old_ast_unchanged": True, "old_source_prefix_unchanged": True,
    "expected_clean_cases": 96, "expected_refusal_cases": 80,
    "permitted_refusal_cases": 0, "planned": 176, "generated": 176,
    "exercised_per_slot": 176, "unreachable_cases": [],
    "slots": slots, "cases": canonical,
    "limitations": [
        "Finite admitted local/native authority schedules, not general Python soundness",
        "Existing 119 methods and prior 141 capability-row preservation not rerun here",
        "No replacement-generator execution or broad acceptance wall",
        "No tests of internal authority fields or absent-global lookup assumptions",
    ],
}
proof_path = ROOT / "tests-checks/release-v2-proof.json"
proof_hash = create(proof_path, json.dumps(proof, indent=2) + "\n")
family_lines = []
for summary in slots[0]["matrix_summaries"]:
    members = [r for r in canonical if r["matrix"] == summary["matrix_summary"]]
    count = len(members)
    failures = sum((r["classification"] == "clean" and bool(r["blockers"])) or
                   (r["classification"] == "refuse" and not r["blockers"]) for r in members)
    family_lines.append("| " + summary["matrix_summary"] + " | " + str(count) + " | "
                        + str(sum(r["classification"] == "clean" for r in members)) + " | "
                        + str(sum(r["classification"] == "refuse" for r in members)) + " | "
                        + str(failures) + " |")
body = """# Released authority-transfer matrix tests

Scope: new test class only in the separately authorized C authority FIX.
This release records valid RED against unchanged r010, not production GREEN.

Base: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.
Released test SHA-256: """ + EXPECTED + """.
Patch: tests-patch-v2.diff, SHA-256 """ + apply["patch_sha256"] + """.
Matrix proof: tests-checks/release-v2-proof.json, SHA-256 """ + proof_hash + """.

The worktree test file and tests-candidate-v2.py have identical bytes. The new
AuthorityTransferMatrixTests class is immediately before the existing main guard.
The original 119 test methods, all old ASTs/constants, and all earlier source
lines remain unchanged. Static AST discovery now finds 126 methods. No census
assertion, generated output, production file or budget was changed by this work.

| Family | Planned/generated/exercised per slot | Required clean | Required refusal | r010 failures |
| --- | ---: | ---: | ---: | ---: |
""" + "\n".join(family_lines) + """

All 176 schedules were generated and exercised on each slot, with zero unreachable
cases and zero runtime-oracle or analyzer exceptions. The logs explicitly record
proven unexecuted events within otherwise exercised schedules, rather than calling
these unreachable cases. Four schedules run both boolean runtime choices, making
180 independent harmless runtime projections per slot.

The 274-case suggestion was a planning upper bound, not a required Cartesian
product. The final backbone is 2 capture modes x 8 routes x 4 execution modes =
64 cases. The 24 live-rebind schedules, 4 activation-identity cases, 24 native alias
schedules, 16 dictionary/extraction schedules, 16 ordered-class schedules, 12
exception/join schedules and 16 issued witnesses total 176. Existing positional,
keyword/default/receiver binding, deferred and async matrices remain untouched;
duplicating them in the new transfer backbone would increase cost without
isolating a new transfer relation. The earlier estimate of about 182 was refined
by leaving six deferred combinations to the already-existing focused coverage.

All 80 unsafe schedules require an explicit public blocker; disappearing a row
does not satisfy that assertion. All 96 lawful schedules use represented local
functions/classes, finite native collections, literal writes and supported
completion paths, and require the exact fixed subprocess argv with no blocker.
The selected-callee-before-argument case additionally requires the previously
selected sink row after a later mutation. No schedule demands arbitrary external
call precision or assumes that an absent module-global lookup is known to fail.
There are no permitted-refusal-only cases in this release.

The pure renderer independently supplies an inert sink and event recorder; it
shares the declared operation schedule, not executable sensitive fixture bytes.
Only this harmless projection is compiled/executed. The separately assembled
subprocess source is passed as bytes to real derive_design_review. Expectations
were frozen before production edits were inspected. Logs bind each case to its
source hash, oracle hash, runtime traces, public rows, blockers and classification.

Actual CPython 3.11.15 ran first; actual CPython 3.14.6 ran second. Each ran seven
methods in the same fresh D-local exact-r010 clone with only this released test
overlay. The floor control used -I -S -B -P; payloads used -B -P, scrubbed
environment, snapshot cwd/src PYTHONPATH, D-local temporary paths, exact version
and executable assertions before repository imports, and validated absolute Git.
All 1761 tracked paths retained their before hashes after both runs.

Both slots produced identical case outcomes: 54 assertion failures, comprising
38 missed unsafe blockers and 16 refusals of lawful schedules; 122 cases passed.
All nine A witnesses and all seven B witnesses failed as expected. No setup,
oracle or analyzer exception is counted as product RED. Full logs and receipts
are preserved in tests-checks/red-v2-311* and tests-checks/red-v2-314*.

This is finite contract evidence, not a general Python interpreter claim.
Replacement GREEN, the complete existing suite, 141 prior capability rows, census
regeneration and any later review/acceptance wall remain with the parent/production
owner. Issued v1 draft additions remain untouched and were never applied/executed.
The v2 test bytes are now released and must not be edited by this test author.

New method discovery:
""" + "\n".join("- " + m["name"] + " (line " + str(m["line"]) + ")" for m in new_methods) + "\n"
release_path = ROOT / "tests-release-v2.md"
release_hash = create(release_path, body)
print(json.dumps({"proof": str(proof_path), "proof_sha256": proof_hash,
                  "release": str(release_path), "release_sha256": release_hash,
                  "tests_sha256": EXPECTED, "methods": new_methods}))

