"""Static verification of the prospective R2-E1 transition input pack.

This verifier parses source and harmless Model strings as AST only.  It never
compiles or executes either population and never imports the held candidate.
"""

from __future__ import annotations

import sys


_EXPECTED_FLOOR_EXECUTABLE = r"D:\Pontius-tools\py311\Scripts\python.exe"
if (
    sys.implementation.name != "cpython"
    or sys.version_info[:3] != (3, 11, 15)
    or sys.executable.replace("/", "\\").casefold()
        != _EXPECTED_FLOOR_EXECUTABLE.casefold()
    or not sys.flags.isolated
    or not sys.flags.ignore_environment
    or not sys.flags.no_site
    or not sys.flags.no_user_site
    or not sys.flags.safe_path
    or not sys.dont_write_bytecode
    or sys.flags.optimize != 0
):
    raise RuntimeError(
        "transition input verifier requires exact CPython 3.11.15 -I -S -B"
    )

# Every non-builtin import occurs only after the fail-closed interpreter and
# isolation preflight, so a wrong launch cannot execute shadow modules first.
import ast
import copy
import difflib
import hashlib
import json
from pathlib import Path


H = Path(r"D:\Pontius-handoffs")
T = H / "v0a-i01-c-authority"
C = T / "tests-checks"
W_SOURCE = Path(
    r"D:\Pontius-worktrees\codex-v0a-i01-c-core-v1\tools\generate_test_inventory.py"
)
OUTPUT = Path(r"D:\Pontius\coordinator-r2-e1-transition-input-verification-v1.json")

PINS = {
    "tests-checks/rewrite-r2-e1-transition-cases-v5.json":
        "946457a644ab777e3c0a66e84c5f942740cec027d03500582ff31b300c16d427",
    "tests-checks/rewrite-r2-e1-transition-spec-v5.md":
        "0851471493a93845668cb39d9e6a5d4584688d505a86a87cd7a63df69162243a",
    "tests-checks/rewrite-r2-e1-transition-source-model-map-v5.json":
        "0b0dddca5b661ef2622ec79554c7005bffeb60a24561cb44324796081ab7b241",
    "tests-checks/rewrite-r2-e1-transition-source-differences-v5.diff":
        "c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a",
    "tests-checks/rewrite-r2-e1-transition-handoff-v5.md":
        "9a8aadb05251a0ceb84e9fa1d833be4ab7b1350d86183022a20654fc2545cfd9",
}
PREDECESSOR_PINS = {
    "tests-checks/rewrite-r2-e1-transition-cases-v1.json":
        "15260811af2ff936f925d720639dfec5b367089544fd6e6150ef023382ae5063",
    "tests-checks/rewrite-r2-e1-transition-spec-v1.md":
        "af38727b3c01ff3a42088c29e8fa11c49e71c3d0e26e7133a35217c46055787e",
    "tests-checks/rewrite-r2-e1-transition-source-model-map-v1.json":
        "bdc26b40813cd4feab2d287ebff6181d5c925a274cf354f562beb5d4fcab2263",
    "tests-checks/rewrite-r2-e1-transition-source-differences-v1.diff":
        "c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a",
    "tests-checks/rewrite-r2-e1-transition-cases-v2.json":
        "04e202caae3f9203db9859966aea8794e07f30679472ffaeabd3c7b13006da4c",
    "tests-checks/rewrite-r2-e1-transition-spec-v2.md":
        "746a9e524c9959bb4c5621f0497b917835fda73c4e84c203a290ab82b87cef5d",
    "tests-checks/rewrite-r2-e1-transition-source-model-map-v2.json":
        "24a41515e2f59973a8673f202d5373f12978a4c2c43d4bdf4848d428325d8ec7",
    "tests-checks/rewrite-r2-e1-transition-source-differences-v2.diff":
        "c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a",
    "tests-checks/rewrite-r2-e1-transition-handoff-v2.md":
        "0105d58f6987a424ad11f5e25202c1e73f01bf24bbd37b0d0e5e92ea23fb165b",
    "tests-checks/rewrite-r2-e1-transition-cases-v3.json":
        "71c5e8efd0922b213a917a1709c271d3d0fa26ba0268d2d8a7f780e942550511",
    "tests-checks/rewrite-r2-e1-transition-spec-v3.md":
        "fd0e8e6b6a23aca5eed9b75baacab4dfbf552e1a8db11d6673d897873ec7ef64",
    "tests-checks/rewrite-r2-e1-transition-source-model-map-v3.json":
        "9ccb088c53a317ada694ead9287c1d5fe8f2376d3c2549d99ac1e6cbb731ea7a",
    "tests-checks/rewrite-r2-e1-transition-source-differences-v3.diff":
        "c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a",
    "tests-checks/rewrite-r2-e1-transition-handoff-v3.md":
        "d7ad6c1dc75c1e6b2e3b73a223e3d1c8188b6a755ece20d22a4557f47ce2454b",
    "tests-checks/rewrite-r2-e1-transition-cases-v4.json":
        "b2275042ddce8a2a415a5eb9a5a0303b07ef8d64210cccf22ea493601b93e5db",
    "tests-checks/rewrite-r2-e1-transition-spec-v4.md":
        "bf4ba88a299651f7e3167b3ee8ea2cb853767bd19fbd612a0fe500a1475947bc",
    "tests-checks/rewrite-r2-e1-transition-source-model-map-v4.json":
        "fabf97bd74f26c980c4bba8ef1a43d9fc68232889bbc5164c8e030b0db027888",
    "tests-checks/rewrite-r2-e1-transition-source-differences-v4.diff":
        "c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a",
    "tests-checks/rewrite-r2-e1-transition-handoff-v4.md":
        "d1eff592fd2bf4cc18e3f47a338daea959d9ae121d1940e8ffb55831ef7999f2",
}
BASE_PACK_PATH = C / "rewrite-r2-e1-cases-v1.json"
BASE_PACK_SHA = "59b8457a2323634d883fb2c9b0ff82a1e60cd980c5f2a4b50e627c8ca32cdb9b"
SOURCE_SHA = "7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d"
DESIGN_SHA = "eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845"
ORDER = [
    "T01-false-absent-nested",
    "T02-true-present-nested",
    "T03-true-postdelete-class",
    "C01-implicit-build-class",
    "I01-implicit-import",
]
PHASES = {
    "T01-false-absent-nested": (False, False),
    "T02-true-present-nested": (True, True),
    "T03-true-postdelete-class": (True, False),
    "C01-implicit-build-class": (False, False),
    "I01-implicit-import": (False, False),
}
STABLE_ID = "tests/test_structural_review.py::ReviewTests::test_static"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode()


def read_pinned(relative: str, expected: str) -> bytes:
    raw = (T / relative).read_bytes()
    assert digest(raw) == expected, relative
    return raw


def ast_digest(node: ast.AST) -> str:
    return digest(ast.dump(node, include_attributes=False).encode())


def launch_call(tree: ast.AST) -> ast.Call:
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "subprocess"
        and node.func.attr == "run"
    ]
    assert len(calls) == 1
    return calls[0]


class NormalizeEnvironment(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call) -> ast.AST:  # noqa: N802
        copied = copy.deepcopy(node)
        for keyword in copied.keywords:
            if keyword.arg == "env":
                keyword.value = ast.Name(id="_ENV_SENTINEL", ctx=ast.Load())
        return copied


def function_named(tree: ast.AST, name: str) -> list[ast.FunctionDef]:
    return [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]


def assigned_name(statement: ast.stmt, expected: str) -> ast.expr:
    assert isinstance(statement, ast.Assign)
    assert len(statement.targets) == 1
    target = statement.targets[0]
    assert isinstance(target, ast.Name) and target.id == expected
    return statement.value


def assert_empty_list(value: ast.expr) -> None:
    assert isinstance(value, ast.List) and not value.elts


def assert_empty_dict(value: ast.expr) -> None:
    assert isinstance(value, ast.Dict) and not value.keys and not value.values


def assert_name(value: ast.expr, expected: str) -> None:
    assert isinstance(value, ast.Name) and value.id == expected


def assert_event(statement: ast.stmt, expected: str) -> None:
    assert isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
    call = statement.value
    assert not call.keywords and len(call.args) == 1
    assert isinstance(call.func, ast.Attribute) and call.func.attr == "append"
    assert isinstance(call.func.value, ast.Name) and call.func.value.id == "_events"
    assert isinstance(call.args[0], ast.Constant) and call.args[0].value == expected


def assert_capture(statement: ast.stmt, expected_name: str) -> None:
    assert isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
    call = statement.value
    assert not call.keywords and len(call.args) == 1
    assert isinstance(call.func, ast.Attribute) and call.func.attr == "append"
    assert isinstance(call.func.value, ast.Name)
    assert call.func.value.id == "_captured_functions"
    assert_name(call.args[0], expected_name)


def assert_value_error(statement: ast.stmt) -> None:
    assert isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
    call = statement.value
    assert_name(call.func, "ValueError")
    assert not call.args and not call.keywords


def assert_return_literal(statement: ast.stmt, expected: str) -> None:
    assert isinstance(statement, ast.Return)
    assert isinstance(statement.value, ast.Constant) and statement.value.value == expected


def assert_return_call(statement: ast.stmt, expected: str) -> None:
    assert isinstance(statement, ast.Return) and isinstance(statement.value, ast.Call)
    assert_name(statement.value.func, expected)
    assert not statement.value.args and not statement.value.keywords


def assert_context(value: ast.expr, expected_module_name: str) -> None:
    assert isinstance(value, ast.Dict)
    assert len(value.keys) == len(value.values) == 4
    keys = []
    for key in value.keys:
        assert isinstance(key, ast.Constant) and isinstance(key.value, str)
        keys.append(key.value)
    assert keys == ["_events", "_captured_functions", "__name__", "__builtins__"]
    assert_name(value.values[0], "_events")
    assert_name(value.values[1], "_captured_functions")
    assert isinstance(value.values[2], ast.Constant)
    assert value.values[2].value == expected_module_name
    assert_name(value.values[3], "_outer_builtin_context")


def assert_function_type(
    value: ast.expr, expected_driver: str, expected_runtime_name: str,
) -> None:
    assert isinstance(value, ast.Call)
    assert_name(value.func, "_FUNCTION_TYPE")
    assert not value.keywords and len(value.args) == 3
    code = value.args[0]
    assert isinstance(code, ast.Attribute) and code.attr == "__code__"
    assert_name(code.value, expected_driver)
    assert_name(value.args[1], "_context")
    assert isinstance(value.args[2], ast.Constant)
    assert value.args[2].value == expected_runtime_name


def assert_context_key_delete(statement: ast.stmt) -> None:
    assert isinstance(statement, ast.Delete) and len(statement.targets) == 1
    target = statement.targets[0]
    assert isinstance(target, ast.Subscript)
    assert_name(target.value, "_context")
    assert isinstance(target.slice, ast.Constant) and target.slice.value == "__builtins__"


def assert_context_key_replace(statement: ast.stmt) -> None:
    assert isinstance(statement, ast.Assign) and len(statement.targets) == 1
    target = statement.targets[0]
    assert isinstance(target, ast.Subscript)
    assert_name(target.value, "_context")
    assert isinstance(target.slice, ast.Constant) and target.slice.value == "__builtins__"
    assert_name(statement.value, "_inner_builtin_context")


def assert_name_delete(statement: ast.stmt, expected: str) -> None:
    assert isinstance(statement, ast.Delete) and len(statement.targets) == 1
    assert_name(statement.targets[0], expected)


def assert_plain_function(
    function: ast.FunctionDef, positional_names: list[str],
) -> None:
    arguments = function.args
    assert not function.decorator_list and function.returns is None
    assert not getattr(function, "type_params", ())
    assert not arguments.posonlyargs
    assert [argument.arg for argument in arguments.args] == positional_names
    assert not arguments.vararg and not arguments.kwarg
    assert not arguments.kwonlyargs
    assert not arguments.defaults and not arguments.kw_defaults
    assert all(argument.annotation is None for argument in arguments.args)


def assert_plain_class(class_node: ast.ClassDef, *, unittest_case: bool) -> None:
    assert not class_node.decorator_list and not class_node.keywords
    assert not getattr(class_node, "type_params", ())
    if unittest_case:
        assert len(class_node.bases) == 1
        base = class_node.bases[0]
        assert isinstance(base, ast.Attribute) and base.attr == "TestCase"
        assert isinstance(base.value, ast.Name) and base.value.id == "unittest"
    else:
        assert not class_node.bases


for relative, expected in {**PINS, **PREDECESSOR_PINS}.items():
    read_pinned(relative, expected)

pack_raw = read_pinned(
    "tests-checks/rewrite-r2-e1-transition-cases-v5.json",
    PINS["tests-checks/rewrite-r2-e1-transition-cases-v5.json"],
)
map_raw = read_pinned(
    "tests-checks/rewrite-r2-e1-transition-source-model-map-v5.json",
    PINS["tests-checks/rewrite-r2-e1-transition-source-model-map-v5.json"],
)
spec_raw = read_pinned(
    "tests-checks/rewrite-r2-e1-transition-spec-v5.md",
    PINS["tests-checks/rewrite-r2-e1-transition-spec-v5.md"],
)
handoff_raw = read_pinned(
    "tests-checks/rewrite-r2-e1-transition-handoff-v5.md",
    PINS["tests-checks/rewrite-r2-e1-transition-handoff-v5.md"],
)
diff_raw = read_pinned(
    "tests-checks/rewrite-r2-e1-transition-source-differences-v5.diff",
    PINS["tests-checks/rewrite-r2-e1-transition-source-differences-v5.diff"],
)
pack = json.loads(pack_raw)
mapping = json.loads(map_raw)
v1 = json.loads(read_pinned(
    "tests-checks/rewrite-r2-e1-transition-cases-v1.json",
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-cases-v1.json"],
))
v2 = json.loads(read_pinned(
    "tests-checks/rewrite-r2-e1-transition-cases-v2.json",
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-cases-v2.json"],
))
v3 = json.loads(read_pinned(
    "tests-checks/rewrite-r2-e1-transition-cases-v3.json",
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-cases-v3.json"],
))
v4 = json.loads(read_pinned(
    "tests-checks/rewrite-r2-e1-transition-cases-v4.json",
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-cases-v4.json"],
))
v4_mapping = json.loads(read_pinned(
    "tests-checks/rewrite-r2-e1-transition-source-model-map-v4.json",
    PREDECESSOR_PINS[
        "tests-checks/rewrite-r2-e1-transition-source-model-map-v4.json"
    ],
))

base_raw = BASE_PACK_PATH.read_bytes()
assert digest(base_raw) == BASE_PACK_SHA
base = json.loads(base_raw)
base_case = next(case for case in base["cases"] if case["id"] == "E01-standard")
assert pack["adopted_input"] == base["adopted_input"]
assert pack["public_envelope"] == base["public_envelope"]
assert digest(canonical(pack["public_envelope"])) == (
    "8d4cdf6e791199ae5232437832ef4a39d0076451bf2227a66f69d9c6a31eef23"
)
envelope = pack["public_envelope"]
assert envelope["public_api"] == "derive_design_review"
assert envelope["stable_ids"] == [STABLE_ID]
assert envelope["item_universe"] == [["stable_id", STABLE_ID]]
assert envelope["source_relative_path"] == "tests/test_structural_review.py"
assert json.loads(envelope["inventory_document_bytes_utf8"]) == envelope["inventory_document"]
assert digest(envelope["inventory_document_bytes_utf8"].encode()) == (
    envelope["inventory_document_bytes_sha256"]
)

assert pack["schema"] == "pontius-builtin-context-transition-cases-v5"
assert pack["pack_name"] == "rewrite-r2-e1-transition-v5"
assert pack["execution_authorized"] is False
assert pack["planned_cases"] == pack["planned_projections"] == 5
assert pack["classifications"] == {"clean": 1, "refuse": 4}
assert [case["id"] for case in pack["cases"]] == ORDER
assert [case["id"] for case in v1["cases"]] == ORDER
assert [case["id"] for case in v2["cases"]] == ORDER
assert [case["id"] for case in v3["cases"]] == ORDER
assert [case["id"] for case in v4["cases"]] == ORDER
assert (
    pack["adopted_input"] == v1["adopted_input"] == v2["adopted_input"]
    == v3["adopted_input"] == v4["adopted_input"]
)
assert (
    pack["public_envelope"] == v1["public_envelope"] == v2["public_envelope"]
    == v3["public_envelope"] == v4["public_envelope"]
)
assert (
    pack["model_contract"] == v1["model_contract"] == v2["model_contract"]
    == v3["model_contract"] == v4["model_contract"]
)
assert pack["requirements"]["governing_design_sha256"] == DESIGN_SHA
assert pack["requirements"]["source_sha256"] == SOURCE_SHA
assert pack["requirements"]["source_AST_only"] is True
assert digest(W_SOURCE.read_bytes()) == SOURCE_SHA
assert pack["predecessor"] == {
    "disposition": "v1-v4 immutable and unexecuted; v5 corrects v4 lineage metadata only",
    "v4_changes": [
        "T01/T02 category-route closure requirements",
        "narrowed exact CPython 3.14.6 import citation from L2941-L2951 to L2942-L2951",
    ],
    "v4_handoff_sha256": PREDECESSOR_PINS[
        "tests-checks/rewrite-r2-e1-transition-handoff-v4.md"
    ],
    "v4_pack_sha256": PREDECESSOR_PINS[
        "tests-checks/rewrite-r2-e1-transition-cases-v4.json"
    ],
    "v4_source_diff_sha256": PREDECESSOR_PINS[
        "tests-checks/rewrite-r2-e1-transition-source-differences-v4.diff"
    ],
    "v4_source_model_map_sha256": PREDECESSOR_PINS[
        "tests-checks/rewrite-r2-e1-transition-source-model-map-v4.json"
    ],
    "v4_spec_sha256": PREDECESSOR_PINS[
        "tests-checks/rewrite-r2-e1-transition-spec-v4.md"
    ],
}

pack_comparable = copy.deepcopy(pack)
v4_comparable = copy.deepcopy(v4)
for comparable in (pack_comparable, v4_comparable):
    comparable.pop("schema")
    comparable.pop("pack_name")
    comparable.pop("predecessor")
assert pack_comparable == v4_comparable

assert mapping["schema"] == "pontius-r2-e1-transition-static-source-model-map-v5"
assert mapping["pack_sha256"] == digest(pack_raw)
assert mapping["spec_sha256"] == digest(spec_raw)
assert mapping["source_diff_sha256"] == digest(diff_raw)
assert mapping["model_execution_authorized"] is False
assert mapping["sensitive_source_execution_authorized"] is False
assert mapping["runtime_evidence"] is False
assert mapping["planned_cases"] == mapping["planned_projections"] == 5
assert mapping["classifications"] == pack["classifications"]
assert mapping["source_sha256"] == SOURCE_SHA
assert mapping["governing_design_sha256"] == DESIGN_SHA
assert mapping["public_envelope_byte_equivalent"] is True
assert mapping["public_envelope_canonical_sha256"] == digest(canonical(envelope))
assert mapping["adopted_input"] == pack["adopted_input"]
assert len(mapping["cases"]) == 5
assert [row["id"] for row in mapping["cases"]] == ORDER
assert set(mapping["module_key_phase_expectations"]) == set(ORDER)
assert mapping["predecessor"] == {
    "v4_changes": [
        "T01/T02 category-route closure requirements",
        "narrowed exact CPython 3.14.6 import citation from L2941-L2951 to L2942-L2951",
    ],
    "v4_handoff_sha256": PREDECESSOR_PINS[
        "tests-checks/rewrite-r2-e1-transition-handoff-v4.md"
    ],
    "v4_pack_sha256": PREDECESSOR_PINS[
        "tests-checks/rewrite-r2-e1-transition-cases-v4.json"
    ],
    "v4_source_diff_sha256": PREDECESSOR_PINS[
        "tests-checks/rewrite-r2-e1-transition-source-differences-v4.diff"
    ],
    "v4_source_model_map_sha256": PREDECESSOR_PINS[
        "tests-checks/rewrite-r2-e1-transition-source-model-map-v4.json"
    ],
    "v4_spec_sha256": PREDECESSOR_PINS[
        "tests-checks/rewrite-r2-e1-transition-spec-v4.md"
    ],
    "v5_correction_only": "v4 lineage prose/metadata names both changes",
}

mapping_comparable = copy.deepcopy(mapping)
v4_mapping_comparable = copy.deepcopy(v4_mapping)
for comparable in (mapping_comparable, v4_mapping_comparable):
    for key in ("schema", "predecessor", "pack_sha256", "spec_sha256"):
        comparable.pop(key)
assert mapping_comparable == v4_mapping_comparable

source_proof = pack["requirements"]["exception_metadata_source_proof"]
assert source_proof == {
    "cpython_3_11_15_import_name":
        "https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L6969-L6980",
    "cpython_3_11_15_load_build_class":
        "https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L2547-L2566",
    "cpython_3_14_6_import_name":
        "https://github.com/python/cpython/blob/v3.14.6/Python/ceval.c#L2942-L2951",
    "cpython_3_14_6_load_build_class":
        "https://github.com/python/cpython/blob/v3.14.6/Python/generated_cases.c.h#L8802-L8815",
    "inference":
        "PyErr_SetString supplies only the message; no name keyword is set, so .name is None.",
}
assert mapping["exception_metadata_static_proof"] == {
    "C01": {
        "cpython_3_11_15": source_proof["cpython_3_11_15_load_build_class"],
        "cpython_3_14_6": source_proof["cpython_3_14_6_load_build_class"],
        "expected_message": "__build_class__ not found",
        "expected_name": None,
        "expected_type": "NameError",
        "future_harness_observation_required": True,
    },
    "I01": {
        "cpython_3_11_15": source_proof["cpython_3_11_15_import_name"],
        "cpython_3_14_6": source_proof["cpython_3_14_6_import_name"],
        "expected_message": "__import__ not found",
        "expected_name": None,
        "expected_type": "ImportError",
        "future_harness_observation_required": True,
    },
}

base_tree = ast.parse(base_case["source"], filename="<E01-sensitive-source-static-only>")
base_launch = launch_call(base_tree)
base_launch_digest = ast_digest(base_launch)
base_normalized_digest = ast_digest(NormalizeEnvironment().visit(base_launch))
assert mapping["base_launch_call_ast_sha256"] == base_launch_digest

v1_by_id = {case["id"]: case for case in v1["cases"]}
v2_by_id = {case["id"]: case for case in v2["cases"]}
v3_by_id = {case["id"]: case for case in v3["cases"]}
v4_by_id = {case["id"]: case for case in v4["cases"]}
map_by_id = {case["id"]: case for case in mapping["cases"]}
assert set(map_by_id) == set(ORDER)
reconstructed_diff: list[str] = []
case_facts: list[dict[str, object]] = []
EXPECTED_TRACES = {
    "T01-false-absent-nested": ["outer", "constructor"],
    "T02-true-present-nested": ["outer", "constructor"],
    "T03-true-postdelete-class": ["module", "constructor", "launch"],
    "C01-implicit-build-class": ["outer"],
    "I01-implicit-import": ["outer"],
}
EXPECTED_UNREACHABLE = {
    "T01-false-absent-nested": ["launch"],
    "T02-true-present-nested": ["launch"],
    "T03-true-postdelete-class": [],
    "C01-implicit-build-class": ["launch"],
    "I01-implicit-import": ["launch"],
}
OUTER_CAPTURE = {
    "outer_builtins_is_expected": True,
    "outer_globals_is_context": True,
}

for case in pack["cases"]:
    case_id = case["id"]
    previous1 = v1_by_id[case_id]
    previous2 = v2_by_id[case_id]
    previous3 = v3_by_id[case_id]
    previous4 = v4_by_id[case_id]
    for field in (
        "classification", "context", "id", "oracle_sha256", "required_argv",
        "schedule_id", "source_sha256", "unreachable_events",
    ):
        assert (
            case[field] == previous1[field] == previous2[field]
            == previous3[field] == previous4[field]
        ), (case_id, field)
    assert (
        case["source"] == previous1["source"] == previous2["source"]
        == previous3["source"] == previous4["source"]
    )
    assert (
        case["oracle_source"] == previous1["oracle_source"]
        == previous2["oracle_source"] == previous3["oracle_source"]
        == previous4["oracle_source"]
    )
    for field in ("captures", "result", "trace"):
        assert case["expected"][field] == previous1["expected"][field], (case_id, field)
    for field in ("captures", "exception", "result", "trace"):
        assert case["expected"][field] == previous2["expected"][field], (case_id, field)
        assert case["expected"][field] == previous3["expected"][field], (case_id, field)
        assert case["expected"][field] == previous4["expected"][field], (case_id, field)
    assert digest(case["source"].encode()) == case["source_sha256"]
    assert digest(case["oracle_source"].encode()) == case["oracle_sha256"]
    assert case["required_argv"] == [["-m", "fixed"]]
    assert case["classification"] == ("clean" if case_id.startswith("T03") else "refuse")
    assert case["expected"]["trace"] == EXPECTED_TRACES[case_id]
    assert case["unreachable_events"] == EXPECTED_UNREACHABLE[case_id]
    expected_inner_count = 1 if case_id.startswith("T") else 0
    expected_captures = {
        **OUTER_CAPTURE,
        "inner_builtins_is_expected": True if expected_inner_count else None,
        "inner_count": expected_inner_count,
        "inner_globals_is_context": True if expected_inner_count else None,
    }
    assert case["expected"]["captures"] == expected_captures
    pre, post = PHASES[case_id]
    assert case["expected"]["pre_call_module_key_present"] is pre
    assert case["expected"]["post_call_module_key_present"] is post
    assert mapping["module_key_phase_expectations"][case_id] == {
        "pre_call_module_key_present": pre,
        "post_call_module_key_present": post,
    }

    source_tree = ast.parse(case["source"], filename=f"<{case_id}-sensitive-static-only>")
    model_tree = ast.parse(case["oracle_source"], filename=f"<{case_id}-model-static-only>")
    top_classes = [node for node in source_tree.body if isinstance(node, ast.ClassDef)]
    assert len(top_classes) == 1 and top_classes[0].name == "ReviewTests"
    assert_plain_class(top_classes[0], unittest_case=True)
    top_kinds = [type(node).__name__ for node in source_tree.body]
    expected_top_kinds = {
        "T01-false-absent-nested": ["Import", "Assign", "ClassDef", "Delete"],
        "T02-true-present-nested": ["Import", "ClassDef", "Assign"],
        "T03-true-postdelete-class": ["Import", "Assign", "Delete", "ClassDef"],
        "C01-implicit-build-class": ["Import", "Assign", "ClassDef", "Delete"],
        "I01-implicit-import": ["Import", "Assign", "ClassDef", "Delete"],
    }[case_id]
    assert top_kinds == expected_top_kinds
    if case_id in {
        "T01-false-absent-nested", "C01-implicit-build-class", "I01-implicit-import",
    }:
        assert_empty_dict(assigned_name(source_tree.body[1], "__builtins__"))
        assert_name_delete(source_tree.body[3], "__builtins__")
    elif case_id == "T02-true-present-nested":
        assert_empty_dict(assigned_name(source_tree.body[2], "__builtins__"))
    else:
        assert case_id == "T03-true-postdelete-class"
        assert_empty_dict(assigned_name(source_tree.body[1], "__builtins__"))
        assert_name_delete(source_tree.body[2], "__builtins__")
    top_import_names = {
        alias.name
        for node in source_tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    if case_id == "C01-implicit-build-class":
        assert top_import_names == {"os", "subprocess", "sys", "unittest"}
        expected_imports = ["os", "subprocess", "sys", "unittest"]
    else:
        assert top_import_names == {"subprocess", "sys", "unittest"}
        expected_imports = ["subprocess", "sys", "unittest"]
    top_import = source_tree.body[0]
    assert isinstance(top_import, ast.Import)
    assert [(alias.name, alias.asname) for alias in top_import.names] == [
        (name, None) for name in expected_imports
    ]
    methods = [node for node in top_classes[0].body if isinstance(node, ast.FunctionDef)]
    assert len(methods) == 1 and methods[0].name == "test_static"
    assert top_classes[0].body == methods
    assert_plain_function(methods[0], ["self"])

    call = launch_call(source_tree)
    env_keywords = [keyword for keyword in call.keywords if keyword.arg == "env"]
    assert len(env_keywords) == 1 and isinstance(env_keywords[0].value, ast.Dict)
    env_dict = env_keywords[0].value
    assert len(env_dict.keys) == len(env_dict.values) == 2
    assert env_dict.keys[0] is None
    assert isinstance(env_dict.keys[1], ast.Constant) and env_dict.keys[1].value == "SAFE"
    assert isinstance(env_dict.values[1], ast.Constant) and env_dict.values[1].value == "1"
    inherited_environment = env_dict.values[0]
    assert isinstance(inherited_environment, ast.Attribute)
    assert inherited_environment.attr == "environ"
    if case_id == "C01-implicit-build-class":
        assert isinstance(inherited_environment.value, ast.Name)
        assert inherited_environment.value.id == "os"
    elif case_id == "I01-implicit-import":
        assert isinstance(inherited_environment.value, ast.Name)
        assert inherited_environment.value.id == "launch_os"
    else:
        importer = inherited_environment.value
        assert isinstance(importer, ast.Call)
        assert isinstance(importer.func, ast.Name) and importer.func.id == "__import__"
        assert len(importer.args) == 1 and not importer.keywords
        assert isinstance(importer.args[0], ast.Constant) and importer.args[0].value == "os"
    raw_launch = ast_digest(call)
    normalized_launch = ast_digest(NormalizeEnvironment().visit(call))
    assert normalized_launch == base_normalized_digest
    if case_id.startswith("T"):
        assert raw_launch == base_launch_digest

    model_function_type_calls = [
        node for node in ast.walk(model_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "_FUNCTION_TYPE"
    ]
    assert len(model_function_type_calls) == 1
    model_imports = [
        node for node in ast.walk(model_tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    if case_id == "I01-implicit-import":
        assert len(model_imports) == 1 and isinstance(model_imports[0], ast.Import)
        assert [(item.name, item.asname) for item in model_imports[0].names] == [
            ("os", "launch_os")
        ]
    else:
        assert not model_imports
    forbidden = {"subprocess", "sys", "pontius", "exec", "eval", "compile", "open", "__import__"}
    assert not any(
        isinstance(node, ast.Name) and node.id in forbidden for node in ast.walk(model_tree)
    )

    outer = function_named(model_tree, "_outer_body")
    driver = function_named(model_tree, "_module_driver")
    assert len(outer) + len(driver) == 1
    model_module_name, model_runtime_name, model_driver_name = {
        "T01-false-absent-nested": (
            "transition_t01", "transition_t01_outer", "_outer_body"
        ),
        "T02-true-present-nested": (
            "transition_t02", "transition_t02_outer", "_outer_body"
        ),
        "T03-true-postdelete-class": (
            "transition_t03", "transition_t03_module_driver", "_module_driver"
        ),
        "C01-implicit-build-class": (
            "transition_c01", "transition_c01_outer", "_outer_body"
        ),
        "I01-implicit-import": (
            "transition_i01", "transition_i01_outer", "_outer_body"
        ),
    }[case_id]
    expected_model_module_types = (
        ["Assign", "Assign", "FunctionDef", "Assign", "Assign", "Assign", "Assign"]
        + ([] if case_id == "T03-true-postdelete-class" else [
            "Assign" if case_id == "T02-true-present-nested" else "Delete"
        ])
    )
    assert [type(node).__name__ for node in model_tree.body] == expected_model_module_types
    assert_empty_list(assigned_name(model_tree.body[0], "_events"))
    assert_empty_list(assigned_name(model_tree.body[1], "_captured_functions"))
    assert isinstance(model_tree.body[2], ast.FunctionDef)
    assert model_tree.body[2].name == model_driver_name
    assert_plain_function(model_tree.body[2], [])
    outer_builtins = assigned_name(model_tree.body[3], "_outer_builtin_context")
    if case_id in {
        "T02-true-present-nested", "T03-true-postdelete-class",
    }:
        assert_name(outer_builtins, "_STANDARD_BUILTINS")
    else:
        assert_empty_dict(outer_builtins)
    inner_builtins = assigned_name(model_tree.body[4], "_inner_builtin_context")
    if case_id in {"T01-false-absent-nested", "T03-true-postdelete-class"}:
        assert_name(inner_builtins, "_outer_builtin_context")
    elif case_id == "T02-true-present-nested":
        assert_empty_dict(inner_builtins)
    else:
        assert isinstance(inner_builtins, ast.Constant) and inner_builtins.value is None
    assert_context(
        assigned_name(model_tree.body[5], "_context"), model_module_name
    )
    assert_function_type(
        assigned_name(model_tree.body[6], "_function"),
        model_driver_name,
        model_runtime_name,
    )
    if case_id == "T02-true-present-nested":
        assert_context_key_replace(model_tree.body[7])
    elif case_id != "T03-true-postdelete-class":
        assert_context_key_delete(model_tree.body[7])

    if case_id in {"T01-false-absent-nested", "T02-true-present-nested"}:
        assert len(function_named(model_tree, "_inner")) == 1
        assert [type(node).__name__ for node in outer[0].body] == [
            "Expr", "FunctionDef", "Expr", "Return"
        ]
        model_inner = outer[0].body[1]
        assert isinstance(model_inner, ast.FunctionDef) and model_inner.name == "_inner"
        assert_plain_function(model_inner, [])
        assert [type(node).__name__ for node in model_inner.body] == [
            "Expr", "Expr", "Expr", "Return"
        ]
        assert isinstance(outer[0].body[-1], ast.Return)
        assert_event(outer[0].body[0], "outer")
        assert_event(model_inner.body[0], "constructor")
        assert_value_error(model_inner.body[1])
        assert_event(model_inner.body[2], "launch")
        assert_return_literal(model_inner.body[3], "fixed")
        assert_capture(outer[0].body[2], "_inner")
        assert_return_call(outer[0].body[3], "_inner")
        assert [type(node).__name__ for node in methods[0].body] == [
            "FunctionDef", "Expr"
        ]
        sensitive_inner = methods[0].body[0]
        assert isinstance(sensitive_inner, ast.FunctionDef) and sensitive_inner.name == "inner"
        assert_plain_function(sensitive_inner, [])
        assert [type(node).__name__ for node in sensitive_inner.body] == ["Expr", "Expr"]
        assert_value_error(sensitive_inner.body[0])
        assert isinstance(sensitive_inner.body[1], ast.Expr)
        assert sensitive_inner.body[1].value is call
        source_inner_call = methods[0].body[1]
        assert isinstance(source_inner_call, ast.Expr)
        assert isinstance(source_inner_call.value, ast.Call)
        assert_name(source_inner_call.value.func, "inner")
        assert not source_inner_call.value.args and not source_inner_call.value.keywords
        assert case["expected"]["captures"]["inner_count"] == 1
        assert case["expected"]["exception"] == {"name": "ValueError", "type": "NameError"}
    elif case_id == "T03-true-postdelete-class":
        assert len(driver) == 1 and len(function_named(model_tree, "_method")) == 1
        assert [type(node).__name__ for node in driver[0].body] == [
            "Global", "Expr", "Assign", "Delete", "FunctionDef", "Expr", "Return"
        ]
        assert [type(node).__name__ for node in methods[0].body] == ["Expr", "Expr"]
        assert_value_error(methods[0].body[0])
        assert isinstance(methods[0].body[1], ast.Expr)
        assert methods[0].body[1].value is call
        assert isinstance(driver[0].body[0], ast.Global)
        assert driver[0].body[0].names == ["__builtins__"]
        assert_event(driver[0].body[1], "module")
        driver_store = driver[0].body[2]
        assert isinstance(driver_store, ast.Assign)
        assert len(driver_store.targets) == 1
        assert isinstance(driver_store.targets[0], ast.Name)
        assert driver_store.targets[0].id == "__builtins__"
        assert_empty_dict(driver_store.value)
        driver_delete = driver[0].body[3]
        assert isinstance(driver_delete, ast.Delete)
        assert len(driver_delete.targets) == 1
        assert isinstance(driver_delete.targets[0], ast.Name)
        assert driver_delete.targets[0].id == "__builtins__"
        driver_method = driver[0].body[4]
        assert isinstance(driver_method, ast.FunctionDef) and driver_method.name == "_method"
        assert_plain_function(driver_method, [])
        assert [type(node).__name__ for node in driver_method.body] == [
            "Expr", "Expr", "Expr", "Return"
        ]
        assert_event(driver_method.body[0], "constructor")
        assert_value_error(driver_method.body[1])
        assert_event(driver_method.body[2], "launch")
        assert_return_literal(driver_method.body[3], "fixed")
        assert_capture(driver[0].body[5], "_method")
        assert_return_call(driver[0].body[6], "_method")
        assert case["expected"]["exception"] is None
        assert case["expected"]["result"] == "fixed"
    elif case_id == "C01-implicit-build-class":
        assert [type(node).__name__ for node in outer[0].body] == [
            "Expr", "ClassDef", "Expr", "Return"
        ]
        assert_event(outer[0].body[0], "outer")
        model_local = outer[0].body[1]
        assert isinstance(model_local, ast.ClassDef) and model_local.name == "Local"
        assert_plain_class(model_local, unittest_case=False)
        assert [type(node).__name__ for node in model_local.body] == ["Pass"]
        assert_event(outer[0].body[2], "launch")
        assert_return_literal(outer[0].body[3], "fixed")
        assert [type(node).__name__ for node in methods[0].body] == ["ClassDef", "Expr"]
        assert isinstance(methods[0].body[0], ast.ClassDef)
        assert methods[0].body[0].name == "Local"
        assert_plain_class(methods[0].body[0], unittest_case=False)
        assert [type(node).__name__ for node in methods[0].body[0].body] == ["Pass"]
        assert isinstance(methods[0].body[1], ast.Expr)
        assert methods[0].body[1].value is call
        nested = [node for node in ast.walk(outer[0]) if isinstance(node, ast.ClassDef)]
        assert len(nested) == 1 and nested[0].name == "Local"
        assert case["expected"]["exception"] == {
            "message": "__build_class__ not found",
            "name": None,
            "type": "NameError",
        }
        assert not any(
            isinstance(node, ast.Name) and node.id == "__import__"
            for node in ast.walk(source_tree)
        )
    else:
        assert case_id == "I01-implicit-import"
        assert [type(node).__name__ for node in outer[0].body] == [
            "Expr", "Import", "Expr", "Return"
        ]
        assert_event(outer[0].body[0], "outer")
        assert model_imports[0] is outer[0].body[1]
        assert_event(outer[0].body[2], "launch")
        assert_return_literal(outer[0].body[3], "fixed")
        assert [type(node).__name__ for node in methods[0].body] == ["Import", "Expr"]
        local_import = methods[0].body[0]
        assert isinstance(local_import, ast.Import)
        assert [(item.name, item.asname) for item in local_import.names] == [
            ("os", "launch_os")
        ]
        assert isinstance(methods[0].body[1], ast.Expr)
        assert methods[0].body[1].value is call
        assert case["expected"]["exception"] == {
            "message": "__import__ not found",
            "name": None,
            "type": "ImportError",
        }
        assert not any(
            isinstance(node, ast.Name) and node.id == "__import__"
            for node in ast.walk(source_tree)
        )

    row = map_by_id[case_id]
    assert row["source_sha256"] == case["source_sha256"]
    assert row["oracle_sha256"] == case["oracle_sha256"]
    assert row["classification"] == case["classification"]
    assert row["parsed_stable_id"] == STABLE_ID
    assert row["model_executed"] is False
    assert row["sensitive_source_executed"] is False
    assert row["model_inner_capture_required"] is case_id.startswith("T")
    assert row["launch_call_ast_sha256"] == raw_launch
    assert row["launch_contract_normalized_ast_sha256"] == normalized_launch
    assert row["model_function_type_constructor_count"] == 1
    assert row["model_import_count"] == len(model_imports)
    assert row["source_classdef_count"] == sum(
        isinstance(node, ast.ClassDef) for node in ast.walk(source_tree)
    )
    assert row["source_functiondef_count"] == sum(
        isinstance(node, ast.FunctionDef) for node in ast.walk(source_tree)
    )
    assert row["source_import_count"] == sum(
        isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(source_tree)
    )
    assert row["source_unchanged_from_v1"] is True
    assert row["model_unchanged_from_v1"] is True
    assert row["source_unchanged_from_v3"] is True
    assert row["model_unchanged_from_v3"] is True
    assert row["expected_unchanged_from_v3"] is True

    reconstructed_diff.extend(difflib.unified_diff(
        base_case["source"].splitlines(keepends=True),
        case["source"].splitlines(keepends=True),
        fromfile="E01-standard",
        tofile=case_id,
    ))
    case_facts.append({
        "id": case_id,
        "classification": case["classification"],
        "pre_call_module_key_present": pre,
        "post_call_module_key_present": post,
        "source_sha256": case["source_sha256"],
        "oracle_sha256": case["oracle_sha256"],
        "source_ast_parsed_only": True,
        "model_ast_parsed_only": True,
    })

assert "".join(reconstructed_diff).encode() == diff_raw
assert diff_raw == read_pinned(
    "tests-checks/rewrite-r2-e1-transition-source-differences-v1.diff",
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-source-differences-v1.diff"],
)
assert diff_raw == read_pinned(
    "tests-checks/rewrite-r2-e1-transition-source-differences-v2.diff",
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-source-differences-v2.diff"],
)
assert diff_raw == read_pinned(
    "tests-checks/rewrite-r2-e1-transition-source-differences-v3.diff",
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-source-differences-v3.diff"],
)
assert diff_raw == read_pinned(
    "tests-checks/rewrite-r2-e1-transition-source-differences-v4.diff",
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-source-differences-v4.diff"],
)

assert mapping["t03_static_driver_correspondence"] == {
    "driver_global_declaration": ["__builtins__"],
    "driver_statement_order": [
        "events.append(module)",
        "store __builtins__",
        "delete __builtins__",
        "create _method",
        "invoke _method",
    ],
    "inner_free_names": [],
    "model_executed": False,
    "runtime_identity_and_trace_validation_required": True,
    "sensitive_statement_order": [
        "store __builtins__",
        "delete __builtins__",
        "create ReviewTests",
        "invoke test_static later",
    ],
}

route_requirements = mapping["category_route_requirements"]
assert set(route_requirements) == {
    "T01-false-absent-nested", "T02-true-present-nested",
    "C01-implicit-build-class", "I01-implicit-import",
}
assert route_requirements == {
    case["id"]: case["category_route_requirement"]
    for case in pack["cases"]
    if "category_route_requirement" in case
}
assert route_requirements["C01-implicit-build-class"]["consumer"].startswith("LOAD_BUILD_CLASS")
assert route_requirements["I01-implicit-import"]["consumer"].startswith("IMPORT_NAME")
assert route_requirements["C01-implicit-build-class"] == {
    "category_closure_requires_consumer_reached": True,
    "consumer": "LOAD_BUILD_CLASS for nested Local",
    "public_contract_note": (
        "An explicit blocker is safe, but an earlier blocker alone does not prove this "
        "implicit-consumer category closed."
    ),
}
assert route_requirements["I01-implicit-import"] == {
    "category_closure_requires_consumer_reached": True,
    "consumer": "IMPORT_NAME for method-local import os as launch_os",
    "public_contract_note": (
        "An explicit blocker is safe, but an earlier blocker alone does not prove this "
        "implicit-consumer category closed."
    ),
}
assert route_requirements["T01-false-absent-nested"] == {
    "category_closure_requires_all_steps": True,
    "consumer": "explicit ValueError fallback in nested inner",
    "public_contract_note": (
        "Any explicit blocker is safe refusal, but an earlier blocker does not close the "
        "false-proof/absent-key nested-creation transition category."
    ),
    "required_reviewed_evidence": [
        "outer invocation", "nested inner creation", "nested inner invocation",
        "reached explicit ValueError fallback",
    ],
}
assert route_requirements["T02-true-present-nested"] == {
    "category_closure_requires_all_steps": True,
    "consumer": "explicit ValueError fallback in nested inner",
    "public_contract_note": (
        "Any explicit blocker is safe refusal, but an earlier blocker does not close the "
        "true-proof/present-empty-key nested-creation transition category."
    ),
    "required_reviewed_evidence": [
        "outer invocation under retained true builtin proof",
        "nested inner creation while module __builtins__ key is present and empty",
        "nested inner invocation", "reached explicit ValueError fallback",
    ],
}
assert mapping["category_closure_contract"] == pack["category_closure_contract"] == {
    "composite_final_evidence": [
        "runtime GREEN for the fixed public/Model expectations",
        "reviewed exact-source hook proof for every T01, T02, C01, and I01 route step",
        "original E02 and E03 evidence that invocation/creation is not blanket-refused",
    ],
    "public_blocker_safe_refusal": True,
    "safe_refusal_alone_closes_category": False,
    "t03_reason": (
        "Exact clean argv plus no blocker proves its live path; no refusal-route observer is needed."
    ),
    "t03_route_requirement": None,
}
assert mapping["t03_route_requirement"] == {
    "reason": "Exact clean argv plus no blocker proves its live path.",
    "required": False,
}

spec_text = spec_raw.decode()
handoff_text = handoff_raw.decode()
for expected_text in (
    digest(pack_raw), digest(diff_raw), DESIGN_SHA, SOURCE_SHA,
    "v3.14.6", "L2942-L2951", "Final closure",
    "four exact release citations are unchanged from v4",
    "T01/T02 category-route closure requirements",
    "narrowed exact CPython 3.14.6 import citation from `L2941-L2951` to `L2942-L2951`",
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-cases-v4.json"],
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-spec-v4.md"],
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-source-model-map-v4.json"],
    PREDECESSOR_PINS["tests-checks/rewrite-r2-e1-transition-handoff-v4.md"],
):
    assert expected_text in spec_text
for expected_text in (digest(pack_raw), digest(spec_raw), digest(map_raw), digest(diff_raw)):
    assert expected_text in handoff_text

report = {
    "schema": "coordinator-r2-e1-transition-input-verification-v1",
    "verified_pins": PINS,
    "verified_predecessor_pins": PREDECESSOR_PINS,
    "base_pack_sha256": BASE_PACK_SHA,
    "held_source_sha256": SOURCE_SHA,
    "governing_design_sha256": DESIGN_SHA,
    "public_envelope_exact": True,
    "public_envelope_canonical_sha256": digest(canonical(envelope)),
    "source_diff_byte_identical_across_v1_v2_v3_v4_v5": True,
    "source_and_model_bytes_unchanged_across_v1_v2_v3_v4_v5": True,
    "case_order": ORDER,
    "cases": case_facts,
    "category_route_requirements_static_only": route_requirements,
    "candidate_imported": False,
    "analyzer_executed": False,
    "harness_executed": False,
    "models_executed": False,
    "sensitive_sources_executed": False,
    "verifier_sha256": digest(Path(__file__).read_bytes()),
    "runtime": {
        "executable": sys.executable,
        "expected_executable": _EXPECTED_FLOOR_EXECUTABLE,
        "implementation": sys.implementation.name,
        "version": list(sys.version_info[:3]),
        "isolated": bool(sys.flags.isolated),
        "ignore_environment": bool(sys.flags.ignore_environment),
        "no_site": bool(sys.flags.no_site),
        "no_user_site": bool(sys.flags.no_user_site),
        "safe_path": bool(sys.flags.safe_path),
        "dont_write_bytecode": bool(sys.dont_write_bytecode),
        "optimize": int(sys.flags.optimize),
    },
}
encoded = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
with OUTPUT.open("xb") as stream:
    stream.write(encoded)
print(json.dumps({
    "output": str(OUTPUT),
    "sha256": digest(encoded),
    "verified_cases": len(case_facts),
    "models_executed": False,
    "sensitive_sources_executed": False,
}))
