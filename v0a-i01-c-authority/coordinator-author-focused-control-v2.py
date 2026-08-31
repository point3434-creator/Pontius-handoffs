"""Retain focused controller v2 for the independently reviewed test correction."""
from pathlib import Path
import ast
import copy
import difflib
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
h = lambda raw: hashlib.sha256(raw).hexdigest()
pins = {
    "tests-focused-control-v1.py": "2676cc5e58db5a1e70044610de1876c96e23b38cd1a55c4f22f47aaa59118eba",
    "tests-focused-wrapper-v1.py": "839e30c19b825defae4fea30ec899a43cd0ad346953215421b81478ffc20ca35",
    "tests-focused-population-v1.json": "8799fd0f5996b84397b42f12b84f19a120a3b99f4be76a78775a4e5666856362",
    "tests-candidate-v5.py": "48c4620bf5585a76d500b3c9bf4cad4559a04d4f544bc3808832d37b58b03add",
    "engineer-budget-assertion-candidate-review-v1.md": "faf1bdb169669c5e252cfe679e8e4ed0fb08f522a5a14d1c753d0c56664de10c",
}
raws = {name: (T / name).read_bytes() for name in pins}
assert {name: h(raw) for name, raw in raws.items()} == pins
population = json.loads(raws["tests-focused-population-v1.json"])
updated = copy.deepcopy(population)
for kind in ("design", "matrix"):
    updated[kind]["tests_sha256"] = pins["tests-candidate-v5.py"]
updated["scope"] = population["scope"] + " V2 uses reviewed tests-candidate-v5 for both suites: only the helper1050 depth-or-budget regex changes; every method, matrix case, model and classification remains unchanged."
normalized = copy.deepcopy(updated)
for kind in ("design", "matrix"):
    normalized[kind]["tests_sha256"] = population[kind]["tests_sha256"]
normalized["scope"] = population["scope"]
assert normalized == population
pop_raw = (json.dumps(updated, indent=2) + "\n").encode()
old = raws["tests-focused-control-v1.py"].decode().replace("\r\n", "\n")
source = old
replacements = [
    ('Only design53 or the immutable matrix192 is admitted. No mutable W input.', 'Only design53 or the immutable matrix192 is admitted. V2 pins the reviewed v5 test correction for both. No mutable W input.'),
    ('MATRIX_SHA = "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"', 'CANDIDATE_TESTS_SHA = "' + pins["tests-candidate-v5.py"] + '"'),
    ('POPULATION = ROOT / "tests-focused-population-v1.json"', 'POPULATION = ROOT / "tests-focused-population-v2.json"'),
    ('POPULATION_SHA = "' + pins["tests-focused-population-v1.json"] + '"', 'POPULATION_SHA = "' + h(pop_raw) + '"'),
    ('MATRIX = ROOT / "tests-candidate-v4.py"', 'CANDIDATE_TESTS = ROOT / "tests-candidate-v5.py"'),
    ('SCHEMA = "c-authority-focused-control-v1"', 'SCHEMA = "c-authority-focused-control-v2"'),
    ('PAYLOAD = ".focused-authority"', 'PAYLOAD = ".focused-authority-v2"'),
    ('    if arguments.kind == "matrix":\n        inputs["matrix_tests"] = {"path": str(MATRIX), "sha256": MATRIX_SHA}', '    inputs["candidate_tests"] = {"path": str(CANDIDATE_TESTS), "sha256": CANDIDATE_TESTS_SHA}'),
    ('prefix = "focused-" + arguments.label', 'prefix = "focused-v2-" + arguments.label'),
    ('"tests_sha256": MATRIX_SHA if arguments.kind == "matrix" else ORIGINAL_TESTS_SHA,', '"tests_sha256": CANDIDATE_TESTS_SHA,'),
    ('            if arguments.kind == "matrix":\n                (snapshot / TEST_RELATIVE).write_bytes(raw_inputs["matrix_tests"])', '            (snapshot / TEST_RELATIVE).write_bytes(raw_inputs["candidate_tests"])'),
]
for before, after in replacements:
    assert source.count(before) == 1, before
    source = source.replace(before, after, 1)
old_tree, new_tree = ast.parse(old), ast.parse(source)
compile(new_tree, "static-only-controller", "exec")
def defs(tree):
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
old_defs, new_defs = defs(old_tree), defs(new_tree)
assert old_defs.keys() == new_defs.keys()
changed = [name for name in old_defs if ast.dump(old_defs[name], include_attributes=False) != ast.dump(new_defs[name], include_attributes=False)]
assert changed == ["run"]
assert not any(isinstance(n, ast.Name) and n.id in {"MATRIX", "MATRIX_SHA"} for n in ast.walk(new_tree))
inverse = source
for before, after in reversed(replacements):
    assert inverse.count(after) == 1, after
    inverse = inverse.replace(after, before, 1)
assert inverse == old
delta = ''.join(difflib.unified_diff(old.splitlines(True), source.splitlines(True),
                                   fromfile="tests-focused-control-v1.py", tofile="tests-focused-control-v2.py")).encode()
report = {"schema": "coordinator-focused-control-v2-static-v1", "input_pins": pins,
          "control_sha256": h(source.encode()), "population_sha256": h(pop_raw),
          "changed_function": "run", "all_other_functions_ast_equal": True,
          "inverse_recovers_normalized_original_control": True,
          "population_only_test_pins_and_scope_changed": True,
          "wrapper_byte_unchanged": True, "payload_executed": False,
          "standing": "New frozen harness for reviewed assertion correction; root dispatch separate."}
note = f'''# Focused controller v2: reviewed test expectation correction

Controller SHA256 {h(source.encode())}; population SHA256 {h(pop_raw)}.
Wrapper remains v1 SHA256 {pins["tests-focused-wrapper-v1.py"]}.
Tests are exact v5 SHA256 {pins["tests-candidate-v5.py"]}.
Independent assertion review SHA256 {pins["engineer-budget-assertion-candidate-review-v1.md"]}.

The only test expectation change is the independently reviewed helper1050 regex.
Original design53 method identities, matrix192 schedules/212 Models, classifications
and all other assertions remain unchanged. The new test pin applies to both selected
suites; the wrapper still loads only the selected named class. Every earlier receipt
retains its original candidate/test pair and verdict.

The controller still verifies original r010 source/test blobs before applying the
two explicit overlays, then manifests every tracked and payload byte. New control
schema, payload directory and receipt prefix prevent cross-version floor reuse.
Identity-before-imports, actual runtimes, environment, watchdog, result assessment,
raw evidence replay and full before/after checks are unchanged. No guard, timeout,
test count, cap, source behavior or successful-floor requirement was relaxed.

First proposed dispatch is v28 storage on actual311 with v5 tests, to establish the
separate assertion correction before another storage change. Expectation: helper1050
now accepts its admissible canonical budget refusal, while generator70 remains red.
That is a diagnostic prediction, not an outcome to manufacture. Any result is kept;
failed floor does not authorize314/matrix/corpus. Root will inspect this exact delta
before dispatch. This file itself grants no payload or integration authority.
'''.encode()
outputs = {"tests-focused-control-v2.py": source.encode(), "tests-focused-population-v2.json": pop_raw,
           "tests-focused-control-v2-from-v1.diff": delta,
           "coordinator-focused-control-v2-static-v1.json": (json.dumps(report, indent=2) + "\n").encode(),
           "coordinator-focused-control-v2-handoff-v1.md": note,
           "coordinator-author-focused-control-v2.py": Path(__file__).read_bytes()}
assert not any((T / name).exists() for name in outputs)
for name, raw in outputs.items():
    with (T / name).open("xb") as stream:
        stream.write(raw)
print(json.dumps({name: h(raw) for name, raw in outputs.items()}))
