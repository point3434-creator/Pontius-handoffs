"""Static source transformation only: create T candidate, never import it or write W."""
from pathlib import Path
import ast
import copy
import difflib
import hashlib
import json
import subprocess

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
WORKSPACE = Path(r"D:\Pontius")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
BASE_SHA = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
PROTO_SHA = "67acb279510924311266b985e15e95e53ae9d0a11d64a50d108f254a690deb2a"
R010_SHA = "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
R010_REF = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
PAYLOAD = {"adapter":"class _ExecutionState(MutableMapping[str, _FlowValue]):\n    \"\"\"Execution wrapper owning one private name cursor and branch authority.\"\"\"\n\n    def __init__(self, values: Mapping[str, _FlowValue], budget: _AnalysisBudget,\n                 *, parent: Mapping[str, _FlowValue] | None = None,\n                 local_names: Iterable[str] = (), enabled: bool = True) -> None:\n        self.authority = (parent.authority.fork() if isinstance(parent, _ExecutionState)\n                          else _AuthorityState(budget, enabled))\n        self.bindings = (parent.bindings.fork() if isinstance(parent, _ExecutionState)\n                         else _AuthorityMap(budget))\n        meter = (parent._names._meter if isinstance(parent, _ExecutionState)\n                 else _NameMeter(budget))\n        # Capture the caller's iterable once. Keep duplicate/order semantics for\n        # local-cell allocation, with a separate membership index for inheritance.\n        meter.charge(\"adapter_local_order_allocation\")\n        local_order = []\n        for name in local_names:\n            meter.charge(\"adapter_local_input_visits\")\n            meter.charge(\"adapter_local_order_reference_copies\")\n            local_order.append(name)\n        meter.charge(\"adapter_local_membership_allocation\")\n        meter.charge(\"adapter_local_membership_input_visits\", len(local_order))\n        meter.charge(\"adapter_local_membership_attempts\", len(local_order))\n        local_set = frozenset(local_order)\n        meter.charge(\"adapter_local_membership_reference_copies\", len(local_set))\n        for name in local_order if self.authority.enabled else ():\n            self.bindings[name] = (self.authority.identity(),)\n        if isinstance(parent, _ExecutionState) and values is parent and not local_order:\n            self._names = parent._names.fork()\n            return\n        self._names = _NameCursor(_NameVersion.empty(meter))\n        for name, value in values.items():\n            meter.charge(\"adapter_constructor_input_visits\")\n            inherited = _NAME_MISSING\n            if isinstance(parent, _ExecutionState):\n                meter.charge(\"adapter_local_membership_lookup\")\n                if name not in local_set:\n                    inherited = parent._names._entry(name)\n            if inherited is not _NAME_MISSING and inherited.value is value:\n                # Retain the exact parent's proof OR pending debt, without transfer.\n                _name_check_name(name)\n                self._names._replace_entry(name, inherited)\n            else:\n                self[name] = value\n\n    def __getitem__(self, name: str) -> _FlowValue:\n        _name_check_name(name)\n        entry = self._names._entry(name)\n        if entry is _NAME_MISSING:\n            raise KeyError(name)\n        return entry.value\n\n    def __len__(self) -> int:\n        return len(self._names)\n\n    def __iter__(self):\n        return iter(self.keys())\n\n    def __contains__(self, name: object) -> bool:\n        _name_check_name(name)\n        return self._names._entry(name) is not _NAME_MISSING\n\n    def get(self, name: str, default=None):\n        return self._names.get(name, default)\n\n    def items(self):\n        return self._names.ordered_items()\n\n    def keys(self):\n        return self._names.keys()\n\n    def values(self):\n        items = self._names.ordered_items()\n        meter = self._names._meter\n        meter.charge(\"adapter_values_tuple_allocation\")\n        def values():\n            for _name, value in items:\n                meter.charge(\"adapter_values_item_visits\")\n                meter.charge(\"adapter_values_reference_copies\")\n                yield value\n        return tuple(values())\n\n__PRESERVED_CELL_METHOD__\n\n__PRESERVED_TRANSFERRED_ENTRY_METHOD__\n\n    def _project(self, name: str, value: _FlowValue) -> None:\n        # Raw installation always clears certification, including identical values.\n        self._names.set(name, value)\n\n    def _project_pop(self, name: str, default=None):\n        entry = self._names._entry(name)\n        if entry is _NAME_MISSING:\n            return default\n        self._names.delete(name)\n        return entry.value\n\n    def __setitem__(self, name: str, value: _FlowValue) -> None:\n        entry = self._transferred_name_entry(value)\n        _name_check_name(name)\n        self._names._replace_entry(name, entry)\n        # Uncaptured module globals retain immutable provenance in the value\n        # map. A cell is allocated only by actual lexical capture; locals were\n        # allocated for this activation at entry, including not-yet-bound ones.\n        if self.authority.enabled:\n            identities = self.bindings.get(name, ())\n            self._write_cells(entry.value, identities)\n\n__PRESERVED_WRITE_CELLS_METHOD__\n\n    def __delitem__(self, name: str) -> None:\n        self._names.delete(name)\n        if self.authority.enabled:\n            identities = self.bindings.get(name, ())\n            for identity in identities:\n                deleted = _FlowValue(\"unbound\", reason=\"deleted cell\")\n                self.authority.cells[identity] = (deleted if len(identities) == 1 else\n                    _merge_flow_values(\"alternative cell delete\", (\n                        self.authority.cells.get(identity), deleted)))\n\n    def pop(self, name: str, default: object = None) -> object:\n        if name not in self:\n            return default\n        value = self[name]\n        del self[name]\n        return value\n\n    def setdefault(self, name: str, default: _FlowValue) -> _FlowValue:\n        if name not in self:\n            self[name] = default\n        return self[name]\n\n    def update(self, supplied: object = (), **keywords: _FlowValue) -> None:\n        if isinstance(supplied, _ExecutionState):\n            # Seal before adoption or destination mutation, including update(self).\n            captured = supplied._names.snapshot()\n            previous = self._names\n            self.authority = supplied.authority.fork()\n            self.bindings = supplied.bindings.fork()\n            if not len(previous):\n                self._names = _NameCursor(captured)\n            else:\n                if previous._meter is not captured._meter:\n                    # Foreign history stays with its original meter.\n                    self._names = _NameCursor(_NameVersion.empty(captured._meter))\n                    for name, value in previous.ordered_items():\n                        self._project(name, value)\n                for name, value in captured.ordered_items():\n                    self._project(name, value)\n            for name, value in keywords.items():\n                self[name] = value\n            return\n        items = supplied.items() if isinstance(supplied, Mapping) else supplied\n        for name, value in items:\n            self[name] = value\n        for name, value in keywords.items():\n            self[name] = value\n\n    def clear(self) -> None:\n        # Detach names/history only; this is not a sequence of captured-cell deletes.\n        self._names = _NameCursor(_NameVersion.empty(self._names._meter))\n\n    def copy(self) -> \"_ExecutionState\":\n        self.authority.budget.consume(4)  # Wrapper allocation and its three field references.\n        result = object.__new__(_ExecutionState)\n        result._names = self._names.fork()\n        result.authority = self.authority.fork()\n        result.bindings = self.bindings.fork()\n        return result\n","merge":"    def _merge_states(\n        self,\n        states: Sequence[Mapping[str, _FlowValue]],\n    ) -> dict[str, _FlowValue]:\n        if not states:\n            return _ExecutionState({}, self.budget, enabled=bool(self.helper_registry))\n        if len(states) == 1:\n            return self._fork_values(states[0])\n        result = self._fork_values(states[0])\n        for state in states[1:]:\n            if isinstance(state, _ExecutionState):\n                result.authority.join(state.authority)\n                if result.bindings.data is not state.bindings.data:\n                    for name, cells in state.bindings.items():\n                        result.bindings[name] = tuple(dict.fromkeys((\n                            *result.bindings.get(name, ()), *cells)))\n        compatible = result.authority.enabled\n        if compatible:\n            for state in states:\n                self.budget.consume()  # Actual compatibility input visit.\n                if (not isinstance(state, _ExecutionState)\n                        or not state.authority.enabled\n                        or state._names._meter is not result._names._meter\n                        or state.authority.budget is not result.authority.budget):\n                    compatible = False\n                    break\n        binding_plan: list[tuple[str, tuple[int, ...]]] = []\n        if compatible:\n            self.budget.consume(2)  # Plan list and overlap set.\n            seen: set[int] = set()\n            for name, cells in result.bindings.items():\n                participating = False\n                for state in states:\n                    self.budget.consume()  # Actual input visit; lookup charges its backing.\n                    if name in state:\n                        participating = True\n                        break\n                if not participating:\n                    continue\n                for identity in cells:\n                    self.budget.consume(2)  # Cell visit plus seen-identity lookup.\n                    if identity in seen or identity not in result.authority.cells:\n                        compatible = False\n                        break\n                    self.budget.consume()  # Remember this distinct existing cell.\n                    seen.add(identity)\n                if not compatible:\n                    break\n                self.budget.consume(4)  # Pair allocation, two fields and list reference.\n                binding_plan.append((name, cells))\n        # Capture all state names before callbacks or result projection changes.\n        # Plain Mapping inputs remain plain; no extra state conversion/transfer.\n        self.budget.consume(1 + 2 * len(states))  # Tuple, input visits and references.\n        name_inputs = tuple(\n            state._names.snapshot() if isinstance(state, _ExecutionState) else state\n            for state in states\n        )\n        if not compatible:\n            self.budget.consume(1 + len(states))  # Key-view argument tuple and references.\n            key_views = tuple(state.keys() for state in name_inputs)\n            self.budget.consume(2 + 2 * sum(len(state) for state in name_inputs))\n            names = set().union(*key_views)\n            self.budget.consume(len(names))  # Unique set references.\n            result.clear()\n            for name in names:\n                self.budget.consume()  # Actual name iteration.\n                result[name] = _merge_flow_values(\n                    name, tuple(state.get(name) for state in name_inputs))\n            return result\n\n        def merge_name(name: str, supplied: tuple[object, ...]) -> _NameEntry:\n            self.budget.consume(1 + 2 * len(supplied))  # Missing-value translation tuple.\n            values = tuple(None if value is _NAME_MISSING else value for value in supplied)\n            return result._transferred_name_entry(_merge_flow_values(name, values))\n\n        result._names = _NameCursor(_join_name_versions(\n            result._names._meter, name_inputs, merge_name))\n        # Distinct existing cells commute; every strong/weak write still occurs.\n        for name, cells in binding_plan:\n            self.budget.consume()  # Plan iteration; projected lookup charges its backing.\n            result._write_cells(result[name], cells)\n        return result\n"}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read_pin(name, digest):
    raw = (ROOT / name).read_bytes()
    assert sha(raw) == digest, name
    return raw

def create(name, raw):
    with (ROOT / name).open("xb") as stream:
        stream.write(raw)

def json_bytes(value):
    return (json.dumps(value, indent=2) + "\n").encode()

read_pin("coordinator-name-cursor-candidate-disposition-v1.md",
         "8cabe43873bddfc7871ff671c96eec85fccfc29cf774dd3c748167fc9dabae21")
read_pin("engineer-name-cursor-adapter-proposal-v1.md",
         "16e315f394baebf957350f33c90dd9cc8e96918817af4a0d64841f7b824116a2")
read_pin("coordinator-cursor-verification-v1.json",
         "beea083a71bcbb9e32df5e11a01e9e17af2ca4238958fe27e55661cce24972aa")
base_raw = read_pin("engineer-generator-v20.py", BASE_SHA)
previous_raw = read_pin("engineer-generator-v21.py",
                        "181993a34985a7eaa045744f662be20b9cee3b2e3c63752af15810ea47ef7ff6")
proto_raw = read_pin("engineer-name-cursor-prototype-v1.py", PROTO_SHA)
assert sha((W / "tools/generate_test_inventory.py").read_bytes()) == BASE_SHA

def git(repository, *arguments):
    return subprocess.run(
        [str(GIT), "-c", "core.hooksPath=NUL", "-c", "core.fsmonitor=false",
         "-c", "core.attributesFile=NUL", "-C", str(repository), *arguments],
        check=True, capture_output=True).stdout

tracked = git(W, "ls-files", "-z").decode().split("\0")[:-1]
before = {name: sha((W / name).read_bytes()) for name in tracked}
r010_raw = git(WORKSPACE, "show", R010_REF + ":tools/generate_test_inventory.py")
assert sha(r010_raw) == R010_SHA
base, prototype = base_raw.decode(), proto_raw.decode()
base_tree, proto_tree = ast.parse(base), ast.parse(prototype)
base_lines = base.splitlines(keepends=True)

def top(tree, name):
    matches = [n for n in tree.body
               if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name == name]
    assert len(matches) == 1, name
    return matches[0]

def method(cls, name):
    matches = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == name]
    assert len(matches) == 1, name
    return matches[0]

def lines_of(node):
    return "".join(base_lines[node.lineno - 1:node.end_lineno]).rstrip("\n")

def canonical(node):
    return ast.dump(node, include_attributes=False)

name_map = {
    "MAXIMUM_SEALED_LAYERS": "_MAXIMUM_NAME_SEALED_LAYERS",
    "MISSING": "_NAME_MISSING", "_DELETED": "_NAME_DELETED",
    "Entry": "_NameEntry", "_check_name": "_name_check_name",
    "_History": "_NameHistory", "_history": "_name_history",
    "_Layer": "_NameLayer", "_seal_layer": "_name_seal_layer",
    "_lookup_layers": "_name_lookup_layers", "_compact": "_name_compact",
    "_Order": "_NameOrder", "_order": "_name_order",
    "_known_order": "_name_known_order", "_seal_order_table": "_name_seal_order_table",
    "_realize_order": "_name_realize_order",
    "_charge_cache_commit": "_name_charge_cache_commit",
    "_commit_order": "_name_commit_order", "_keys": "_name_keys",
    "_ordered_items": "_name_ordered_items", "NameVersion": "_NameVersion",
    "_Publication": "_NamePublication", "_prepare_publication": "_name_prepare_publication",
    "_charge_publication_commit": "_name_charge_publication_commit",
    "_commit_publication": "_name_commit_publication", "NameCursor": "_NameCursor",
    "_common_history": "_name_common_history", "_pending_names": "_name_pending_names",
    "join": "_join_name_versions",
}

class RenameNames(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id in name_map:
            node.id = name_map[node.id]
        return node

selected = []
for original in proto_tree.body:
    if isinstance(original, (ast.ClassDef, ast.FunctionDef)):
        if original.name in {"Meter", "BudgetExceeded"}:
            continue
    elif isinstance(original, ast.Assign):
        if any(isinstance(target, ast.Name) and target.id == "MAXIMUM_WORK"
               for target in original.targets):
            continue
    else:
        continue
    node = copy.deepcopy(original)
    if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
        assert node.name in name_map, node.name
        node.name = name_map[node.name]
    node = RenameNames().visit(node)
    selected.append(node)
mapped = ast.fix_missing_locations(ast.Module(body=selected, type_ignores=[]))
mapped_text = ast.unparse(mapped)
meter_text = lines_of(top(base_tree, "_NameMeter"))
new_storage = meter_text + "\n\n\n" + mapped_text + "\n\n\n"

old_execution = top(base_tree, "_ExecutionState")
adapter = PAYLOAD["adapter"]
for placeholder, name in (
    ("__PRESERVED_CELL_METHOD__", "cell"),
    ("__PRESERVED_TRANSFERRED_ENTRY_METHOD__", "_transferred_name_entry"),
    ("__PRESERVED_WRITE_CELLS_METHOD__", "_write_cells"),
):
    assert adapter.count(placeholder) == 1
    adapter = adapter.replace(placeholder, lines_of(method(old_execution, name)))
assert "__PRESERVED_" not in adapter

storage_start = base.index("_NAME_MISSING = object()")
execution_start = sum(len(line) for line in base_lines[:old_execution.lineno - 1])
execution_end = sum(len(line) for line in base_lines[:old_execution.end_lineno])
resolver = top(base_tree, "_SourceOrderedResolver")
old_merge = method(resolver, "_merge_states")
merge_start = sum(len(line) for line in base_lines[:old_merge.lineno - 1])
merge_end = sum(len(line) for line in base_lines[:old_merge.end_lineno])
changes = [
    ("name_storage", storage_start, execution_start, new_storage),
    ("execution_adapter", execution_start, execution_end, adapter),
    ("merge_states", merge_start, merge_end, PAYLOAD["merge"]),
]
candidate = base
replacements = []
for label, start, end, replacement in sorted(changes, key=lambda change: change[1], reverse=True):
    old = base[start:end]
    replacements.append({"label": label, "old": old, "new": replacement})
    candidate = candidate[:start] + replacement + candidate[end:]
candidate_raw = candidate.encode()
candidate_tree = ast.parse(candidate)

# Static pre-execution correction only: no byte beyond the two name checks.
expected_previous = previous_raw.decode()
corrections = [('                self._names._replace_entry(name, inherited)\n', '                _name_check_name(name)\n                self._names._replace_entry(name, inherited)\n'), ('        entry = self._transferred_name_entry(value)\n        self._names._replace_entry(name, entry)\n', '        entry = self._transferred_name_entry(value)\n        _name_check_name(name)\n        self._names._replace_entry(name, entry)\n')]
for old, new in corrections:
    assert expected_previous.count(old) == 1
    expected_previous = expected_previous.replace(old, new)
assert candidate_raw == expected_previous.encode(), "not exactly two restored name checks"
previous_delta = "".join(difflib.unified_diff(
    previous_raw.decode().splitlines(keepends=True), candidate.splitlines(keepends=True),
    fromfile="a/tools/generate_test_inventory.py", tofile="b/tools/generate_test_inventory.py"))
assert [line for line in previous_delta.splitlines() if line.startswith("+") and not line.startswith("+++")] == [
    "+                _name_check_name(name)", "+        _name_check_name(name)"]
assert not [line for line in previous_delta.splitlines() if line.startswith("-") and not line.startswith("---")]

inverse = candidate
for change in replacements:
    assert inverse.count(change["new"]) == 1, change["label"]
    inverse = inverse.replace(change["new"], change["old"], 1)
assert inverse.encode() == base_raw, "changed byte outside the three authorized regions"

namespace_proof = {}
for expected in selected:
    if isinstance(expected, (ast.ClassDef, ast.FunctionDef)):
        actual = top(candidate_tree, expected.name)
        assert canonical(actual) == canonical(expected), expected.name
        namespace_proof[expected.name] = {
            "canonical_ast_sha256": sha(canonical(actual).encode()), "line": actual.lineno}
    else:
        targets = [target.id for target in expected.targets if isinstance(target, ast.Name)]
        matches = [n for n in candidate_tree.body if isinstance(n, ast.Assign)
                   and [x.id for x in n.targets if isinstance(x, ast.Name)] == targets]
        assert len(matches) == 1 and canonical(matches[0]) == canonical(expected), targets

protected_names = [
    "_AnalysisBudget", "_transfer_authority", "_AuthorityMap", "_ObservedAuthorityMap",
    "_AuthorityState", "_AuthorityRecord", "_FlowValue", "_NameMeter",
]
protected = {}
for name in protected_names:
    old, new = top(base_tree, name), top(candidate_tree, name)
    assert canonical(old) == canonical(new), name
    protected[name] = sha(canonical(new).encode())
new_execution = top(candidate_tree, "_ExecutionState")
for name in ("cell", "_write_cells", "_transferred_name_entry", "pop", "setdefault", "values"):
    old, new = method(old_execution, name), method(new_execution, name)
    assert canonical(old) == canonical(new), name
    protected["_ExecutionState." + name] = sha(canonical(new).encode())

new_resolver = copy.deepcopy(top(candidate_tree, "_SourceOrderedResolver"))
for index, child in enumerate(new_resolver.body):
    if isinstance(child, ast.FunctionDef) and child.name == "_merge_states":
        new_resolver.body[index] = copy.deepcopy(old_merge)
        break
else:
    raise AssertionError("missing candidate merge")
assert canonical(new_resolver) == canonical(resolver), "unrelated resolver semantics changed"
for name in ("_review_body", "_process_review_rows", "_unittest_entry_preflight",
             "_unittest_receiver_attributes"):
    assert canonical(top(base_tree, name)) == canonical(top(candidate_tree, name)), name
    protected[name] = sha(canonical(top(candidate_tree, name)).encode())

cap_names = (
    "MAXIMUM_ANALYSIS_HELPER_DEPTH", "MAXIMUM_ANALYSIS_CHILD_DEPTH",
    "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS", "MAXIMUM_ANALYSIS_CARDINALITY",
    "MAXIMUM_ANALYSIS_WORK_UNITS",
)
def cap(tree, name):
    matches = [n for n in tree.body if isinstance(n, ast.Assign)
               and any(isinstance(x, ast.Name) and x.id == name for x in n.targets)]
    assert len(matches) == 1
    return matches[0]
caps = {}
for name in cap_names:
    assert canonical(cap(base_tree, name)) == canonical(cap(candidate_tree, name))
    caps[name] = ast.literal_eval(cap(candidate_tree, name).value)

full_diff = "".join(difflib.unified_diff(
    r010_raw.decode().splitlines(keepends=True), candidate.splitlines(keepends=True),
    fromfile="a/tools/generate_test_inventory.py", tofile="b/tools/generate_test_inventory.py"))
delta = "".join(difflib.unified_diff(
    base.splitlines(keepends=True), candidate.splitlines(keepends=True),
    fromfile="a/tools/generate_test_inventory.py", tofile="b/tools/generate_test_inventory.py"))

name_accesses = []
for n in ast.walk(candidate_tree):
    if isinstance(n, ast.Attribute) and n.attr == "_names":
        name_accesses.append({"line": n.lineno, "expression": ast.unparse(n)})
name_accesses.sort(key=lambda row: (row["line"], row["expression"]))
after = {name: sha((W / name).read_bytes()) for name in tracked}
assert before == after
assert after["tools/generate_test_inventory.py"] == BASE_SHA

namespace = {
    "candidate_sha256": sha(candidate_raw), "prototype_sha256": PROTO_SHA,
    "identifier_map": name_map,
    "excluded_prototype_definitions": ["Meter", "BudgetExceeded", "MAXIMUM_WORK", "imports", "module docstring"],
    "meter_bridge": "Existing _NameMeter AST unchanged; charge delegates original _AnalysisBudget.consume.",
    "mapping_method": "Top-level declaration names and ast.Name identifiers only; attributes, slots and string literals are unchanged.",
    "canonical_transplant_proof": namespace_proof,
}
static = {
    "candidate_sha256": sha(candidate_raw), "predecessor_sha256": BASE_SHA,
    "immediate_predecessor_sha256": sha(previous_raw),
    "immediate_predecessor_artifact": "engineer-generator-v21.py",
    "static_preexecution_correction": {
        "v21_installed_or_executed": False,
        "exactly_two_name_check_insertions": True,
        "no_removals_or_other_byte_changes": True,
        "semantic_setter_order": "full transfer/certification -> name validation -> install -> cell writes",
        "constructor_inherited_install_order": "inheritance lookup -> name validation -> Entry install",
    },
    "r010_ref": R010_REF, "r010_generator_sha256": R010_SHA,
    "validation": "stdlib AST parse/canonical comparisons only; candidate never imported or executed",
    "scope": "T-only candidate; no W writes, test edits, generated edits, class semantic repair, or payload",
    "inverse_recovers_exact_predecessor": True,
    "authorized_regions": [
        {"label": label, "predecessor_start_line": base[:start].count("\n") + 1,
         "predecessor_end_line": base[:end].count("\n"), "replacement_bytes": len(replacement.encode())}
        for label, start, end, replacement in changes],
    "protected_ast_sha256": protected, "analysis_caps": caps,
    "resolver_ast_unchanged_except_merge_states": True,
    "prototype_namespaced_ast_exact": True,
    "candidate_name_accesses": name_accesses,
    "tracked_path_count": len(tracked), "w_before": before, "w_after": after,
    "all_w_tracked_bytes_unchanged": True,
}
outputs = {
    "engineer-generator-v22.py": candidate_raw,
    "engineer-generator-v22.diff": full_diff.encode(),
    "engineer-generator-v22-from-v20.diff": delta.encode(),
    "engineer-generator-v22-from-v21.diff": previous_delta.encode(),
    "engineer-name-cursor-v22-namespacing.json": json_bytes(namespace),
    "engineer-checks/v22-cursor-candidate-static.json": json_bytes(static),
}
for name in outputs:
    assert not (ROOT / name).exists(), name
for name, raw in outputs.items():
    create(name, raw)
    print(json.dumps({"path": str(ROOT / name), "sha256": sha(raw), "bytes": len(raw)}))
print(json.dumps({"source_lines": len(candidate.splitlines()), "tracked_paths_preserved": len(tracked),
                  "all_prototype_declarations_ast_exact": True,
                  "all_other_resolver_semantics_unchanged": True}))
