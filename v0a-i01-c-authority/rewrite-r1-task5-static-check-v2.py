import sys
assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode
assert sys.flags.safe_path
import ast, copy, difflib, hashlib, json
from pathlib import Path
root = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
work = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-core-v1")
sha = lambda data: hashlib.sha256(data).hexdigest()
base = (root / "rewrite-r1-base-generator.py").read_bytes()
prior = (root / "rewrite-r1-task5-source-v1.py").read_bytes()
source = (root / "rewrite-r1-task5-source-v2.py").read_bytes()
edit_bytes = (root / "rewrite-r1-task5-edits-v2.json").read_bytes()
assert sha(base) == "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
assert sha(prior) == "810cbb934e20a13c9c4794e3574bcb6a248ddc8b4a84a56045f6370c1a066cea"
assert sha(source) == "c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f"
assert sha(edit_bytes) == "d1be8b35c664f7cda35cb50e3053d605999c8a6c030ef362796ff9212def496e"
edits = json.loads(edit_bytes)
rebuilt = prior.decode()
for before, after in edits:
    assert rebuilt.count(before) == 1, before[:120]
    rebuilt = rebuilt.replace(before, after, 1)
assert rebuilt.encode() == source
assert (work / "tools/generate_test_inventory.py").read_bytes() == source
assert b"\r" not in source and not source.startswith(b"\xef\xbb\xbf")
start = source.index(b"# Canonical C core.")
end = source.index(b"@dataclass(slots=True)\nclass _PreclassifierExceptionalState:")
core = source[start:end]
binder_edits = json.loads((root / "rewrite-r1-task4-edits-v1.json").read_text())
assert sha((root / "rewrite-r1-task4-edits-v1.json").read_bytes()) == "e71ea54c3ef7a57719b6e56802ea3ebf6b20b9445a5c61567d29fd78d95659e0"
old_binder, new_binder = binder_edits[-1]
assert source.replace(core, b"", 1).replace(new_binder.encode(), old_binder.encode(), 1).replace(
    b"def _legacy_process_review_rows_r010(\n", b"def _process_review_rows(\n", 1) == base
old_tree, new_tree, core_tree = ast.parse(base), ast.parse(source), ast.parse(core)
added_names = set()
for node in core_tree.body:
    if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
        added_names.add(node.name)
    elif isinstance(node, ast.Assign):
        added_names.update(target.id for target in node.targets if isinstance(target, ast.Name))
def is_added(node):
    if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
        return node.name in added_names
    return isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and
           target.id in added_names for target in node.targets)
remaining = copy.deepcopy(ast.Module(body=[n for n in new_tree.body if not is_added(n)], type_ignores=[]))
legacy = next(n for n in remaining.body if isinstance(n, ast.FunctionDef) and
              n.name == "_legacy_process_review_rows_r010")
legacy.name = "_process_review_rows"
wrapped = []
guards = []
allowed = {ast.dump(ast.parse(text, mode="eval").body) for text in (
    "parameter.arg not in positional_only", "keyword.arg not in allowed_keywords",
    "keyword.arg in supplied", "parameter.arg in supplied", "positional_defaults.get(parameter.arg)")}
class NormalizeBinder(ast.NodeTransformer):
    def visit_If(self, node):
        if ast.dump(node.test) == ast.dump(ast.parse("analysis_budget is not None", mode="eval").body):
            assert not node.orelse
            guards.append(node.lineno)
            for statement in node.body:
                assert isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
                call = statement.value
                assert ast.dump(call.func) == ast.dump(ast.parse("analysis_budget.consume", mode="eval").body)
                for child in ast.walk(call):
                    if isinstance(child, ast.Call) and child is not call:
                        assert isinstance(child.func, ast.Name) and child.func.id == "len"
                    assert not isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp))
            return None
        return self.generic_visit(node)
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "_c_binding_read":
            assert len(node.args) == 2 and not node.keywords
            assert isinstance(node.args[0], ast.Name) and node.args[0].id == "analysis_budget"
            original = ast.dump(node.args[1])
            assert original in allowed
            wrapped.append(original)
            return node.args[1]
        return self.generic_visit(node)
binder = next(n for n in remaining.body if isinstance(n, ast.FunctionDef) and n.name == "_bind_helper_arguments")
assert binder.args.kwonlyargs[-1].arg == "analysis_budget"
assert isinstance(binder.args.kw_defaults[-1], ast.Constant) and binder.args.kw_defaults[-1].value is None
binder.args.kwonlyargs.pop()
binder.args.kw_defaults.pop()
NormalizeBinder().visit(binder)
assert len(wrapped) == 6 and len(guards) == 14
assert ast.dump(remaining) == ast.dump(old_tree)
read_helper = next(n for n in new_tree.body if isinstance(n, ast.FunctionDef) and n.name == "_c_binding_read")
expected_read = ast.parse("def _c_binding_read(budget: _AnalysisBudget | None, value: object) -> object:\n    if budget is not None:\n        budget.consume()\n    return value\n").body[0]
assert ast.dump(read_helper) == ast.dump(expected_read)
setup = json.loads((root / "coordinator-rewrite-r1-setup-v1.json").read_text())
preserved = {}
for name, expected in setup["base_paths"].items():
    if name != "tools/generate_test_inventory.py":
        preserved[name] = sha((work / name).read_bytes())
        assert preserved[name] == expected, name
functions = {n.name:n for n in new_tree.body if isinstance(n, ast.FunctionDef)}
for call in ast.walk(core_tree):
    if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
            and call.func.id.startswith("_c_") and call.func.id in functions):
        continue
    definition = functions[call.func.id]
    positional = definition.args.posonlyargs + definition.args.args
    assert not any(isinstance(a, ast.Starred) for a in call.args)
    provided = len(call.args) + sum(k.arg in {a.arg for a in positional} for k in call.keywords)
    assert len(positional) - len(definition.args.defaults) <= provided <= len(positional), (call.func.id, call.lineno)
    keyword_names = {a.arg for a in positional + definition.args.kwonlyargs}
    assert all(k.arg in keyword_names for k in call.keywords)
for node in ast.walk(core_tree):
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
        assert node.id not in {"_SourceOrderedResolver", "_SensitivePreclassifier", "_review_body",
            "_source_ordered_helper_return", "_legacy_process_review_rows_r010", "eval", "exec", "compile"}
public = functions["_process_review_rows"]
assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "extend"
               for n in ast.walk(public))
assert sum(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and
           n.func.id == "_c_extend_review_rows" for n in ast.walk(public)) == 7
assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and
               n.func.id == "_review_blocker" for n in ast.walk(public))
assert sum(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and
           n.func.id == "_c_preflight_blocker" for n in ast.walk(public)) == 5
assert sum(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and
           n.func.id == "_c_entry_namespace_supported" for n in ast.walk(public)) == 1
assert sum(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and
           n.func.id == "_CSinkObservation" for n in ast.walk(core_tree)) == 1
table_path = root / "rewrite-r1-unittest-entry-reserved-names-v1.json"
table_bytes = table_path.read_bytes()
assert sha(table_bytes) == "55ed71468da3c480e4805672b2b254e1bff5d6d0cf99a2c36ed0fbcfec202ceb"
table = json.loads(table_bytes)
reserved = next(n for n in core_tree.body if isinstance(n, ast.Assign) and
                any(isinstance(t, ast.Name) and t.id == "_C_UNITTEST_RESERVED_NAMES" for t in n.targets))
assert isinstance(reserved.value, ast.Call) and isinstance(reserved.value.func, ast.Name)
assert reserved.value.func.id == "frozenset" and len(reserved.value.args) == 1 and not reserved.value.keywords
names = ast.literal_eval(reserved.value.args[0])
assert list(names) == table["reserved_names"]
prior_functions = {n.name:ast.dump(n) for n in ast.parse(prior).body if isinstance(n, ast.FunctionDef)}
changed = [name for name,n in functions.items() if name in prior_functions and ast.dump(n) != prior_functions[name]]
diff = "".join(difflib.unified_diff(prior.decode().splitlines(True), source.decode().splitlines(True),
                                  fromfile="Task5-v1", tofile="Task5-v2"))
full_diff = "".join(difflib.unified_diff(base.decode().splitlines(True), source.decode().splitlines(True),
                                       fromfile="r010", tofile="R1-Task5-v2"))
added = sum(line.startswith("+") and not line.startswith("+++") for line in full_diff.splitlines())
deleted = sum(line.startswith("-") and not line.startswith("---") for line in full_diff.splitlines())
assert added + deleted <= 2500
report = {"scope":"AST/hash-only authoring check; no candidate import/execution",
          "runtime":list(sys.version_info[:3]), "source_sha256":sha(source),
          "prior_sha256":sha(prior), "edits_sha256":sha(edit_bytes),
          "checker_sha256":sha(Path(__file__).read_bytes()), "original_bytes_restored":True,
          "original_ast_normalized_exact":True, "binder_guards":len(guards), "binder_wrappers":len(wrapped),
          "other_16_paths":preserved, "added":added, "deleted":deleted, "changed_lines":added+deleted,
          "core_lines":len(core.splitlines()), "changed_prior_functions":changed,
          "added_symbols":sorted(added_names), "reserved_names_sha256":sha(table_bytes),
          "reserved_name_count":len(names), "diff_sha256":sha(diff.encode()),
          "full_diff_sha256":sha(full_diff.encode()), "acceptance_proved":False}
output = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
for filename, data in (("rewrite-r1-task5-from-v1-v2.diff", diff.encode()),
    ("rewrite-r1-task5-from-r010-v2.diff", full_diff.encode()), ("rewrite-r1-task5-static-v2.json", output)):
    with (root / filename).open("xb") as stream:
        stream.write(data)
print(json.dumps({"source_sha256":sha(source), "static_sha256":sha(output),
                  "diff_sha256":sha(diff.encode()), "full_diff_sha256":sha(full_diff.encode()),
                  "changed_lines":added+deleted, "changed_prior_functions":changed}))
