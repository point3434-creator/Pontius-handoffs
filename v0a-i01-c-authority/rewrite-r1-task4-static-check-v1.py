import sys
assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode
assert sys.flags.safe_path
import ast, difflib, hashlib, json
from pathlib import Path
root = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
work = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-core-v1")
sha = lambda data: hashlib.sha256(data).hexdigest()
base = (root / "rewrite-r1-base-generator.py").read_bytes()
prior = (root / "rewrite-r1-task3-source-v1.py").read_bytes()
source = (root / "rewrite-r1-task4-source-v1.py").read_bytes()
insertion = (root / "rewrite-r1-task4-insertion-v1.txt").read_bytes()
task1 = (root / "rewrite-r1-task1-insertion-v2.txt").read_bytes()
assert sha(base) == "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
assert sha(prior) == "1ecbde73fcd2159aef2a96538850a93fc4ec2bfa590352bc33d95581d12ccc45"
assert sha(source) == "3511f60a62fc9588f153ba3db6b05ac228a1ce235cb23a5316000ce7ba4e550c"
assert sha(insertion) == "aa650698335073f3020fc97139fde68e9121409bd0d5fe1126accc903952dc31"
assert source.count(insertion) == 1
start = source.index(b"# Canonical C core.")
end = source.index(b"@dataclass(slots=True)\nclass _PreclassifierExceptionalState:")
core = source[start:end]
edits = json.loads((root / "rewrite-r1-task4-edits-v1.json").read_text())
assert sha((root / "rewrite-r1-task4-edits-v1.json").read_bytes()) == "e71ea54c3ef7a57719b6e56802ea3ebf6b20b9445a5c61567d29fd78d95659e0"
old_binder, new_binder = edits[-1]
assert source.replace(core, b"", 1).replace(new_binder.encode(), old_binder.encode(), 1) == base
rebuilt = prior.decode()
for before, after in edits:
    assert rebuilt.count(before) == 1
    rebuilt = rebuilt.replace(before, after, 1)
marker = "@dataclass(slots=True)\nclass _PreclassifierExceptionalState:"
assert rebuilt.replace(marker, insertion.decode() + marker, 1).encode() == source
assert (work / "tools/generate_test_inventory.py").read_bytes() == source
assert b"\r" not in source and not source.startswith(b"\xef\xbb\xbf")
old_tree, new_tree, fragment = ast.parse(base), ast.parse(source), ast.parse(insertion)
added_names = {n.name for n in ast.parse(core).body
               if isinstance(n, (ast.ClassDef, ast.FunctionDef))}
added_names.update({"_CValue", "_CObject"})
def is_added(n):
    if isinstance(n, (ast.ClassDef, ast.FunctionDef)):
        return n.name in added_names
    return isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in added_names
                                           for t in n.targets)
remaining = ast.Module(body=[n for n in new_tree.body if not is_added(n)], type_ignores=[])
wrapped = []
allowed = {
    ast.dump(ast.parse(text, mode="eval").body) for text in
    ("parameter.arg not in positional_only", "keyword.arg not in allowed_keywords",
     "keyword.arg in supplied", "parameter.arg in supplied",
     "positional_defaults.get(parameter.arg)")
}
class NormalizeBinder(ast.NodeTransformer):
    def visit_If(self, n):
        if ast.dump(n.test) == ast.dump(ast.parse("analysis_budget is not None",mode="eval").body):
            assert not n.orelse
            for statement in n.body:
                assert isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
                call = statement.value
                assert ast.dump(call.func) == ast.dump(ast.parse("analysis_budget.consume",mode="eval").body)
                for child in ast.walk(call):
                    if isinstance(child,ast.Call) and child is not call:
                        assert isinstance(child.func,ast.Name) and child.func.id == "len"
                    assert not isinstance(child,(ast.ListComp,ast.SetComp,ast.DictComp,ast.GeneratorExp))
            return None
        return self.generic_visit(n)
    def visit_Call(self,n):
        if isinstance(n.func,ast.Name) and n.func.id == "_c_binding_read":
            assert len(n.args)==2 and not n.keywords
            assert isinstance(n.args[0],ast.Name) and n.args[0].id=="analysis_budget"
            original = ast.dump(n.args[1])
            assert original in allowed
            wrapped.append(original)
            return n.args[1]
        return self.generic_visit(n)
binder = next(n for n in remaining.body if isinstance(n,ast.FunctionDef) and n.name=="_bind_helper_arguments")
assert binder.args.kwonlyargs[-1].arg=="analysis_budget"
assert isinstance(binder.args.kw_defaults[-1],ast.Constant) and binder.args.kw_defaults[-1].value is None
binder.args.kwonlyargs.pop()
binder.args.kw_defaults.pop()
NormalizeBinder().visit(binder)
assert len(wrapped)==6
assert ast.dump(remaining)==ast.dump(old_tree)
read_helper=next(n for n in new_tree.body if isinstance(n,ast.FunctionDef) and n.name=="_c_binding_read")
expected_read=ast.parse("def _c_binding_read(budget: _AnalysisBudget | None, value: object) -> object:\n    if budget is not None:\n        budget.consume()\n    return value\n").body[0]
assert ast.dump(read_helper)==ast.dump(expected_read)
for n in ast.walk(fragment):
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
        assert n.func.id not in {"eval", "exec", "compile", "_SourceOrderedResolver",
                               "_SensitivePreclassifier", "_AnalysisBudget", "_review_body"}
setup = json.loads((root / "coordinator-rewrite-r1-setup-v1.json").read_text())
preserved = {}
for name, expected in setup["base_paths"].items():
    if name == "tools/generate_test_inventory.py":
        continue
    preserved[name] = sha((work / name).read_bytes())
    assert preserved[name] == expected, name
functions = {n.name:n for n in new_tree.body if isinstance(n,ast.FunctionDef)}
for call in ast.walk(ast.parse(core)):
    if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
            and call.func.id.startswith("_c_") and call.func.id in functions):
        continue
    definition = functions[call.func.id]
    positional = definition.args.posonlyargs + definition.args.args
    assert not any(isinstance(a,ast.Starred) for a in call.args)
    provided = len(call.args) + sum(k.arg in {a.arg for a in positional}
                                  for k in call.keywords)
    required = len(positional) - len(definition.args.defaults)
    assert required <= provided <= len(positional), (call.func.id, call.lineno, provided)
diff = "".join(difflib.unified_diff(prior.decode().splitlines(True),
    source.decode().splitlines(True), fromfile="Task3-v1", tofile="Task4-v1"))
diff_path = root / "rewrite-r1-task4-from-task3-v1.diff"
with diff_path.open("xb") as stream:
    stream.write(diff.encode())
report = {"kind":"Task4 AST-only engineering preservation; no candidate execution",
          "runtime":list(sys.version_info[:3]), "source_sha256":sha(source),
          "insertion_sha256":sha(insertion), "task4_construction_lines":len(insertion.splitlines()),
          "binder_normalizes_exactly":True,"binding_read_wrappers":wrapped,
          "core_lines":len(core.splitlines()),
          "total_added_lines":sum(l.startswith("+") and not l.startswith("+++") for l in difflib.unified_diff(base.decode().splitlines(),source.decode().splitlines())),
          "removed_lines":sum(l.startswith("-") and not l.startswith("---") for l in difflib.unified_diff(base.decode().splitlines(),source.decode().splitlines())), "prior_and_original_exact":True, "original_ast_exact":True,
          "other_16_paths":preserved, "diff_sha256":sha(diff.encode()),
          "checker_sha256":sha(Path(__file__).read_bytes()),
          "new_helpers":[{"name":n.name,"line":n.lineno,"end_line":n.end_lineno}
                         for n in new_tree.body if isinstance(n,ast.FunctionDef)
                         and n.name in {v.name for v in fragment.body}]}
report_bytes = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
report_path = root / "rewrite-r1-task4-static-v1.json"
with report_path.open("xb") as stream:
    stream.write(report_bytes)
print(json.dumps({"source_sha256":sha(source),"static_sha256":sha(report_bytes),
                  "diff_sha256":sha(diff.encode()),"added":report["total_added_lines"]}))
