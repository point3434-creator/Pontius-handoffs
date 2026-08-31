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
prior = (root / "rewrite-r1-task2-source-v1.py").read_bytes()
source = (root / "rewrite-r1-task3-source-v1.py").read_bytes()
insertion = (root / "rewrite-r1-task3-insertion-v1.txt").read_bytes()
task1 = (root / "rewrite-r1-task1-insertion-v2.txt").read_bytes()
assert sha(base) == "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
assert sha(prior) == "83418c6b172ca0699ca01caed5f78d401e4ec21317806bbf83dba6b466b6be01"
assert sha(source) == "1ecbde73fcd2159aef2a96538850a93fc4ec2bfa590352bc33d95581d12ccc45"
assert sha(insertion) == "dc46912541054186eada7cc2eea7ac1aa4c94b589bff19f35aa2fce90b75d69e"
assert source.count(insertion) == 1
start = source.index(b"# Canonical C core.")
end = source.index(b"@dataclass(slots=True)\nclass _PreclassifierExceptionalState:")
core = source[start:end]
assert source.replace(core, b"", 1) == base
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
assert ast.dump(remaining) == ast.dump(old_tree)
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
    source.decode().splitlines(True), fromfile="Task2-v1", tofile="Task3-v1"))
diff_path = root / "rewrite-r1-task3-from-task2-v1.diff"
with diff_path.open("xb") as stream:
    stream.write(diff.encode())
report = {"kind":"Task3 AST-only engineering preservation; no candidate execution",
          "runtime":list(sys.version_info[:3]), "source_sha256":sha(source),
          "insertion_sha256":sha(insertion), "task3_evaluator_lines":len(insertion.splitlines()),
          "total_added_lines":len(core.splitlines()),
          "removed_lines":0, "prior_and_original_exact":True, "original_ast_exact":True,
          "other_16_paths":preserved, "diff_sha256":sha(diff.encode()),
          "checker_sha256":sha(Path(__file__).read_bytes()),
          "new_helpers":[{"name":n.name,"line":n.lineno,"end_line":n.end_lineno}
                         for n in new_tree.body if isinstance(n,ast.FunctionDef)
                         and n.name in {v.name for v in fragment.body}]}
report_bytes = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
report_path = root / "rewrite-r1-task3-static-v1.json"
with report_path.open("xb") as stream:
    stream.write(report_bytes)
print(json.dumps({"source_sha256":sha(source),"static_sha256":sha(report_bytes),
                  "diff_sha256":sha(diff.encode()),"added":report["total_added_lines"]}))
