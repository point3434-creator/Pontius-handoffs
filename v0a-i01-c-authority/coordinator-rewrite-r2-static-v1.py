"""AST/hash-only R2 review aid. Never import or execute a candidate."""
import argparse
import ast
import copy
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-core-v1")
BASE = T / "rewrite-r1-base-generator.py"
BASE_SHA = "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
R1_BASE = T / "rewrite-r1-task5-source-v2.py"
R1_BASE_SHA = "c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f"
R2_MAXIMUM_CHANGED_LINES = 1500
FLOOR_EXE = Path(r"D:\Pontius-tools\py311\Scripts\python.exe")
PROTECTED = {'.github/workflows/ci.yml': 'ce3bcf3a2feed6f232d5af131a04e21ba82ed32794838e48297fc780c110a386', 'src/pontius/v0a/__init__.py': '86d349c4b79f150a4439df8d63c8d20854572895aaf7960f27647e7b1f198a8a', 'src/pontius/v0a/clock.py': '42bd18d36a6353dbbcc44df1113eafa40ee5581b3e2479761990ab5c21c074bb', 'src/pontius/v0a/model.py': '3936d0216cdfc1b79500aac22908edd5e724b8da341801fcbafefa7c27a58e18', 'src/pontius/v0a/replay.py': 'ccd18b6540af9799a9feca9cd9884b4871fec7434012e911e37abdc0b1373a53', 'src/pontius/v0a/runtime.py': '307115a9a50be0a80b0cbba997f26f385abcbe1abdc32bd749495eb4692084ee', 'src/pontius/v0a/trace.py': '4358b82b77defeb8bae3a40ab46f1cdfef61d49189b836577040e3e1e22081a1', 'tests/test-inventory.json': '6b866ea24975ee448511f72662f4d04e7f56eba026c0b797bbfa3f4dc7f4008d', 'tests/test-profiles.toml': '5862820a7c316dd9e4bbfe0997ba09f861f8cce257897da6a9a8da659e6912f1', 'tests/test_inventory_and_profiles.py': 'c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf', 'tests/test_v0a_boundaries.py': 'f81387bbf46dfeaf7de8dbcc4f47c2ff04ac06f23f9fd3d1bdd84bf2f210f807', 'tests/test_v0a_contract_faults.py': 'fa7b35f334ebdc232e3d1789db0923ca32ca28ffa0a0a4db741de3a7470cbcf8', 'tests/test_v0a_hand_replay.py': '0a46d155256c4d5727bf53cbc7d8b8ec811d37d777b5c3d7996d8b31ecd822c0', 'tests/test_v0a_replay.py': '1905b75cef434830cf60a7ddc0faf3b5f58cf3bee4947a9be408a017fa0d9c88', 'tests/test_v0a_trace.py': '6de564516a2b866b8b13789bcdff213062911a794bb726a9c9361e785a465d02', 'tools/check_stabilization_boundaries.py': '3dbf89f1a81661bc12fd7e7ea3625b1cb472d9d2f239496ff51ee348e859b4d6'}
EXPECTED_GUARDS = ["If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[BinOp(left=Call(func=Name(id='len', ctx=Load()), args=[Attribute(value=Name(id='call', ctx=Load()), attr='args', ctx=Load())], keywords=[]), op=Add(), right=Call(func=Name(id='len', ctx=Load()), args=[Attribute(value=Name(id='call', ctx=Load()), attr='keywords', ctx=Load())], keywords=[]))], keywords=[])), Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[BinOp(left=Constant(value=1), op=Add(), right=BinOp(left=Constant(value=2), op=Mult(), right=BinOp(left=Call(func=Name(id='len', ctx=Load()), args=[Attribute(value=Name(id='arguments', ctx=Load()), attr='posonlyargs', ctx=Load())], keywords=[]), op=Add(), right=Call(func=Name(id='len', ctx=Load()), args=[Attribute(value=Name(id='arguments', ctx=Load()), attr='args', ctx=Load())], keywords=[]))))], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[BinOp(left=BinOp(left=Constant(value=1), op=Add(), right=BinOp(left=Constant(value=4), op=Mult(), right=Call(func=Name(id='len', ctx=Load()), args=[Attribute(value=Name(id='arguments', ctx=Load()), attr='defaults', ctx=Load())], keywords=[]))), op=Add(), right=IfExp(test=Attribute(value=Name(id='arguments', ctx=Load()), attr='defaults', ctx=Load()), body=BinOp(left=Constant(value=1), op=Add(), right=BinOp(left=Constant(value=2), op=Mult(), right=Call(func=Name(id='len', ctx=Load()), args=[Attribute(value=Name(id='arguments', ctx=Load()), attr='defaults', ctx=Load())], keywords=[]))), orelse=Constant(value=0)))], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[BinOp(left=Constant(value=1), op=Add(), right=BinOp(left=Constant(value=2), op=Mult(), right=BinOp(left=Call(func=Name(id='len', ctx=Load()), args=[Name(id='positional', ctx=Load())], keywords=[]), op=Sub(), right=Constant(value=1))))], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[Constant(value=7)], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[BinOp(left=Constant(value=1), op=Add(), right=BinOp(left=Constant(value=3), op=Mult(), right=Call(func=Name(id='len', ctx=Load()), args=[Attribute(value=Name(id='arguments', ctx=Load()), attr='posonlyargs', ctx=Load())], keywords=[])))], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[BinOp(left=BinOp(left=Constant(value=2), op=Add(), right=BinOp(left=Constant(value=3), op=Mult(), right=BinOp(left=Call(func=Name(id='len', ctx=Load()), args=[Name(id='positional', ctx=Load())], keywords=[]), op=Add(), right=Call(func=Name(id='len', ctx=Load()), args=[Attribute(value=Name(id='arguments', ctx=Load()), attr='kwonlyargs', ctx=Load())], keywords=[])))), op=Add(), right=BinOp(left=Constant(value=2), op=Mult(), right=BinOp(left=BinOp(left=BinOp(left=Call(func=Name(id='len', ctx=Load()), args=[Name(id='positional', ctx=Load())], keywords=[]), op=Add(), right=Call(func=Name(id='len', ctx=Load()), args=[Attribute(value=Name(id='arguments', ctx=Load()), attr='kwonlyargs', ctx=Load())], keywords=[])), op=Sub(), right=Call(func=Name(id='len', ctx=Load()), args=[Name(id='positional_only', ctx=Load())], keywords=[])), op=Add(), right=IfExp(test=BoolOp(op=And(), values=[Name(id='bound', ctx=Load()), Attribute(value=Name(id='arguments', ctx=Load()), attr='posonlyargs', ctx=Load())]), body=Constant(value=1), orelse=Constant(value=0)))))], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[Constant(value=6)], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[Constant(value=6)], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[], keywords=[]))], orelse=[])", "If(test=Compare(left=Name(id='analysis_budget', ctx=Load()), ops=[IsNot()], comparators=[Constant(value=None)]), body=[Expr(value=Call(func=Attribute(value=Name(id='analysis_budget', ctx=Load()), attr='consume', ctx=Load()), args=[Constant(value=6)], keywords=[]))], orelse=[])"]
EXPECTED_WRAPPERS = ["Compare(left=Attribute(value=Name(id='parameter', ctx=Load()), attr='arg', ctx=Load()), ops=[NotIn()], comparators=[Name(id='positional_only', ctx=Load())])", "Compare(left=Attribute(value=Name(id='keyword', ctx=Load()), attr='arg', ctx=Load()), ops=[NotIn()], comparators=[Name(id='allowed_keywords', ctx=Load())])", "Compare(left=Attribute(value=Name(id='keyword', ctx=Load()), attr='arg', ctx=Load()), ops=[In()], comparators=[Name(id='supplied', ctx=Load())])", "Compare(left=Attribute(value=Name(id='parameter', ctx=Load()), attr='arg', ctx=Load()), ops=[In()], comparators=[Name(id='supplied', ctx=Load())])", "Call(func=Attribute(value=Name(id='positional_defaults', ctx=Load()), attr='get', ctx=Load()), args=[Attribute(value=Name(id='parameter', ctx=Load()), attr='arg', ctx=Load())], keywords=[])", "Compare(left=Attribute(value=Name(id='parameter', ctx=Load()), attr='arg', ctx=Load()), ops=[In()], comparators=[Name(id='supplied', ctx=Load())])"]
CAPS = {"MAXIMUM_ANALYSIS_HELPER_DEPTH": 64, "MAXIMUM_ANALYSIS_CHILD_DEPTH": 4,
        "MAXIMUM_ANALYSIS_CONTAINER_ELEMENTS": 4096,
        "MAXIMUM_ANALYSIS_CARDINALITY": 2147483647,
        "MAXIMUM_ANALYSIS_WORK_UNITS": 262144}
OLD_LIVE = {
    "_SourceOrderedResolver", "_SensitivePreclassifier", "_ExecutionState",
    "_AuthorityState", "_AuthorityMap", "_FlowValue", "_FlowEnvironment",
    "_source_ordered_review_flow", "_preclassified_sensitive_calls",
    "_source_ordered_helper_return", "_definition_time_protocol_resolver",
    "_unittest_receiver_attributes", "_review_body", "_runtime_call_bounds",
    "_execution_scope", "_review_function_registry", "_merge_states",
}
EXPECTED_READ_HELPER = """def _c_binding_read(budget: _AnalysisBudget | None, value: object) -> object:
    if budget is not None:
        budget.consume()
    return value
"""

def digest(data):
    return hashlib.sha256(data).hexdigest()

def dump(node):
    return ast.dump(node, include_attributes=False)

def expr(text):
    return ast.parse(text, mode="eval").body

def names(node):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {node.name}
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        return {n.id for target in targets for n in ast.walk(target)
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return {item.asname or item.name.split(".")[0] for item in node.names}
    return set()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def pinned_path(value, *, suffix, must_exist=True):
    path = Path(value)
    require(path.is_absolute() and ".." not in path.parts, "artifact path is not absolute/canonical")
    for item in ((path,) if must_exist or path.exists() else ()) + tuple(path.parents):
        require(not item.stat().st_file_attributes & 1024, "reparse artifact path: " + str(item))
    path = path.resolve(strict=must_exist)
    require(path.is_relative_to(T.resolve(strict=True)), "path is outside retained T")
    require(path.suffix == suffix, "unexpected artifact suffix")
    if must_exist:
        checked_file(path)
    return path

def hex_sha(value):
    require(type(value) is str and re.fullmatch("[0-9a-f]{64}", value) is not None,
            "SHA-256 must be64 lowercase hex characters")
    return value

def one_definition(tree, name):
    matches = [n for n in tree.body
               if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name]
    require(len(matches) == 1, "definition count differs for " + name)
    return matches[0]

def normalize_binder(node):
    node = copy.deepcopy(node)
    require(not node.args.kwarg, "unexpected binder **kwargs")
    require(node.args.kwonlyargs[-1].arg == "analysis_budget",
            "optional budget parameter is not last")
    require(isinstance(node.args.kw_defaults[-1], ast.Constant)
            and node.args.kw_defaults[-1].value is None, "budget default changed")
    require(dump(node.args.kwonlyargs[-1].annotation)
            == dump(expr("_AnalysisBudget | None")), "budget annotation changed")
    node.args.kwonlyargs.pop()
    node.args.kw_defaults.pop()
    guards, wrappers = [], []
    class Normalize(ast.NodeTransformer):
        def visit_If(self, item):
            if dump(item.test) == dump(expr("analysis_budget is not None")):
                require(not item.orelse, "budget guard has else")
                require(bool(item.body), "empty budget guard")
                for statement in item.body:
                    require(isinstance(statement, ast.Expr)
                            and isinstance(statement.value, ast.Call),
                            "budget guard contains a noncall")
                    call = statement.value
                    require(dump(call.func) == dump(expr("analysis_budget.consume"))
                            and len(call.args) <= 1 and not call.keywords,
                            "budget guard contains an unapproved call")
                    for child in ast.walk(call):
                        if isinstance(child, ast.Call) and child is not call:
                            require(isinstance(child.func, ast.Name)
                                    and child.func.id == "len"
                                    and len(child.args) == 1 and not child.keywords,
                                    "nested non-len charge expression")
                        require(not isinstance(child, (ast.ListComp, ast.SetComp,
                                ast.DictComp, ast.GeneratorExp, ast.NamedExpr,
                                ast.Lambda, ast.Await, ast.Yield, ast.YieldFrom)),
                                "charge expression performs extra work")
                guards.append(dump(item))
                return None
            return self.generic_visit(item)
        def visit_Call(self, item):
            if isinstance(item.func, ast.Name) and item.func.id == "_c_binding_read":
                require(len(item.args) == 2 and not item.keywords
                        and dump(item.args[0]) == dump(expr("analysis_budget")),
                        "binding read wrapper shape differs")
                wrappers.append(dump(item.args[1]))
                return self.visit(item.args[1])
            return self.generic_visit(item)
    Normalize().visit(node)
    require(guards == EXPECTED_GUARDS and len(guards) == 14,
            "approved consume guard sequence changed")
    require(wrappers == EXPECTED_WRAPPERS and len(wrappers) == 6,
            "approved read wrapper sequence changed")
    return node, {"guards": len(guards),
                  "consume_calls": 15,
                  "read_wrappers": wrappers}

def exact_bool(node):
    return ((isinstance(node, ast.Constant) and type(node.value) is bool)
            or (isinstance(node, ast.Compare) and len(node.ops) == 1
                and isinstance(node.ops[0], (ast.Is, ast.IsNot))
                and isinstance(node.left, ast.Name)
                and isinstance(node.comparators[0], ast.Constant)
                and node.comparators[0].value is None))

def call_inventory(tree, original_names, new_names, legacy_name):
    calls, budgets, binder, dependencies, direct_old, references = [], [], [], [], [], []
    terminal, visitors, dynamic_calls, execution_calls = [], [], [], []
    class Visit(ast.NodeVisitor):
        def __init__(self):
            self.scope = []
            self.top = None
            self.conditions = []
        def visit_Assign(self, node):
            previous = self.top
            if not self.scope and names(node) & new_names:
                self.top = sorted(names(node))[0]
            self.generic_visit(node)
            self.top = previous
        visit_AnnAssign = visit_Assign
        def visit_FunctionDef(self, node):
            previous = self.top
            if not self.scope:
                self.top = node.name
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()
            self.top = previous
        visit_AsyncFunctionDef = visit_FunctionDef
        def visit_ClassDef(self, node):
            previous = self.top
            if not self.scope:
                self.top = node.name
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()
            self.top = previous
        def visit_If(self, node):
            self.visit(node.test)
            self.conditions.append(ast.unparse(node.test))
            for child in node.body:
                self.visit(child)
            self.conditions.pop()
            self.conditions.append("not (" + ast.unparse(node.test) + ")")
            for child in node.orelse:
                self.visit(child)
            self.conditions.pop()
        def visit_Name(self, node):
            if (self.top in new_names or self.top == "_process_review_rows") and (
                    isinstance(node.ctx, ast.Load) and node.id in OLD_LIVE | {legacy_name}):
                references.append({"owner": ".".join(self.scope), "line": node.lineno,
                                   "name": node.id})
        def visit_Call(self, node):
            target = node.func.id if isinstance(node.func, ast.Name) else None
            owner = ".".join(self.scope) or "<module>"
            new = self.top in new_names or self.top == "_process_review_rows"
            row = {"owner": owner, "line": node.lineno, "target": target,
                   "args": [ast.unparse(a) for a in node.args],
                   "keywords": [{"name": k.arg, "value": ast.unparse(k.value)}
                                for k in node.keywords]}
            if target and target.startswith("_c_"):
                calls.append(row | {"owner_is_new": new,
                                    "target_defined": target in new_names})
            if target == "_AnalysisBudget":
                budgets.append(row | {"owner_is_new": new})
            if target == "_bind_helper_arguments":
                kw = {k.arg: k.value for k in node.keywords if k.arg is not None}
                supplied = kw.get("analysis_budget")
                metered = supplied is not None and not (
                    isinstance(supplied, ast.Constant) and supplied.value is None)
                correct = (not metered or
                           (dump(supplied) == dump(expr("ctx.budget"))
                            and "proven_bound" in kw and exact_bool(kw["proven_bound"])
                            and not any(k.arg is None for k in node.keywords)))
                binder.append(row | {"metered": metered,
                                     "explicit_ctx_budget_and_bool": correct})
            if new and target in {"eval", "exec", "compile", "__import__"}:
                execution_calls.append(row)
            if new and target in original_names:
                dependencies.append(row)
            if new and target in OLD_LIVE | {legacy_name}:
                direct_old.append(row)
            if new and target == "_process_definition":
                terminal.append(row | {"enclosing_if_conditions": list(self.conditions),
                    "proof_status": "manual terminal-only and -c exclusion review required"})
            if new and target == "_ExecutionScopeVisitor":
                visitors.append(row | {"enclosing_if_conditions": list(self.conditions),
                    "proof_status": "manual empty terminal view proof required"})
            if new and target is None:
                dynamic_calls.append({"owner": owner, "line": node.lineno,
                                      "callee_syntax": ast.unparse(node.func)})
            self.generic_visit(node)
    Visit().visit(tree)
    return {"new_c_direct_calls": calls, "analysis_budget_constructions": budgets,
            "binder_callers": binder, "existing_helper_dependencies": dependencies,
            "old_live_direct_calls": direct_old, "old_live_loaded_references": references,
            "terminal_policy_calls": terminal, "terminal_visitor_constructions": visitors,
            "attribute_or_indirect_calls": dynamic_calls,
            "new_dynamic_execution_calls": execution_calls}


def raw_line_changes(base, candidate):
    operations = difflib.SequenceMatcher(
        a=base.splitlines(keepends=True), b=candidate.splitlines(keepends=True),
        autojunk=False).get_opcodes()
    plus = sum(j2 - j1 for tag, i1, i2, j1, j2 in operations
               if tag in {"insert", "replace"})
    minus = sum(i2 - i1 for tag, i1, i2, j1, j2 in operations
                if tag in {"delete", "replace"})
    return {"added": plus, "deleted": minus, "sum": plus + minus,
            "pure_deleted": sum(i2 - i1 for tag, i1, i2, j1, j2 in operations
                                if tag == "delete"),
            "method": "raw-line SequenceMatcher(autojunk=False); all changed lines count"}


def raw_named_span(source, node):
    start = min([node.lineno] + [item.lineno for item in
                                getattr(node, "decorator_list", ())])
    return b"".join(source.splitlines(keepends=True)[start - 1:node.end_lineno])


def named_nodes(source):
    tree = ast.parse(source.decode("utf-8"), type_comments=True)
    rows, occurrences = [], {}

    def emit(node, scope, name):
        qualified = ".".join((*scope, name))
        ordinal = occurrences.get(qualified, 0) + 1
        occurrences[qualified] = ordinal
        raw = raw_named_span(source, node)
        rows.append({"key": qualified + "#" + str(ordinal), "name": qualified,
                     "occurrence": ordinal, "kind": type(node).__name__,
                     "line": node.lineno, "end_line": node.end_lineno,
                     "raw_sha256": digest(raw), "raw_bytes": len(raw),
                     "ast_sha256": digest(dump(node).encode("utf-8"))})

    def visit(node, scope=(), collect_bindings=True):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            emit(node, scope, node.name)
            for child in ast.iter_child_nodes(node):
                visit(child, (*scope, node.name), isinstance(node, ast.ClassDef))
            return
        if collect_bindings and isinstance(
                node, (ast.Assign, ast.AnnAssign, ast.Import, ast.ImportFrom)):
            for name in sorted(names(node)):
                emit(node, scope, name)
        for child in ast.iter_child_nodes(node):
            visit(child, scope, collect_bindings)

    visit(tree)
    return rows, sorted(name for name, count in occurrences.items() if count > 1)


def r2_named_node_inventory(r1, candidate):
    old_rows, old_duplicates = named_nodes(r1)
    new_rows, new_duplicates = named_nodes(candidate)
    before = {row["key"]: row for row in old_rows}
    after = {row["key"]: row for row in new_rows}
    changed, removed, added = [], [], []
    for key, row in before.items():
        if key not in after:
            removed.append(row)
        elif any(row[field] != after[key][field]
                 for field in ("kind", "raw_sha256", "ast_sha256")):
            changed.append({"before": row, "after": after[key],
                            "ast_changed": row["ast_sha256"] != after[key]["ast_sha256"],
                            "raw_changed": row["raw_sha256"] != after[key]["raw_sha256"]})
    for key, row in after.items():
        if key not in before:
            added.append(row)
    old_order = [row["key"] for row in old_rows if row["key"] in after]
    new_order = [row["key"] for row in new_rows if row["key"] in before]
    order_changed = old_order != new_order
    return {"r1_named_nodes": len(old_rows), "candidate_named_nodes": len(new_rows),
            "changed": changed, "removed": removed, "added": added,
            "changed_count": len(changed), "removed_count": len(removed),
            "added_count": len(added), "shared_relative_order_changed": order_changed,
            "shared_order_before": old_order if order_changed else [],
            "shared_order_after": new_order if order_changed else [],
            "duplicate_qualified_names_before": old_duplicates,
            "duplicate_qualified_names_after": new_duplicates,
            "manual_scope_review_required": True, "scope_approval_granted": False,
            "coverage": "All function/class definitions including nested definitions, "
                        "plus module/class bindings from Assign/AnnAssign/Import/ImportFrom; "
                        "function-local edits are covered by their enclosing definition.",
            "limitations": "Name plus occurrence matches are a review index, not identity proof. "
                           "Parent/child and same-line raw spans may overlap; do not sum them. "
                           "Unnamed edits remain visible in the full raw delta. "
                           "Prefix checks do not authorize a changed node."}


def r1_binder_bytes(r1, candidate):
    old = one_definition(ast.parse(r1.decode("utf-8"), type_comments=True),
                         "_bind_helper_arguments")
    new = one_definition(ast.parse(candidate.decode("utf-8"), type_comments=True),
                         "_bind_helper_arguments")
    old_raw, new_raw = raw_named_span(r1, old), raw_named_span(candidate, new)
    return {"baseline_sha256": R1_BASE_SHA, "old_span_sha256": digest(old_raw),
            "candidate_span_sha256": digest(new_raw), "byte_exact": old_raw == new_raw,
            "span": "whole raw UTF-8 lines including decorators and final newline"}


def checked_file(path):
    require(path.is_absolute() and ".." not in path.parts, "input path is not absolute/canonical")
    for item in (path, *path.parents):
        require(not item.stat().st_file_attributes & 1024, "reparse input path: " + str(item))
    require(path.is_file(), "input is not a regular file: " + str(path))
    return path

def inspect(base, candidate, cumulative_lines):
    before = ast.parse(base.decode("utf-8"), type_comments=True)
    after = ast.parse(candidate.decode("utf-8"), type_comments=True)
    old_names = set().union(*(names(n) for n in before.body))
    base_counts = {}
    for node in before.body:
        base_counts[dump(node)] = base_counts.get(dump(node), 0) + 1
    public = one_definition(after, "_process_review_rows")
    old_public = one_definition(before, "_process_review_rows")
    rename_matches = []
    for node in after.body:
        if isinstance(node, ast.FunctionDef) and node.name != "_process_review_rows":
            normalized = copy.deepcopy(node)
            normalized.name = "_process_review_rows"
            if dump(normalized) == dump(old_public):
                rename_matches.append(node)
    require(len(rename_matches) == 1, "old public body is not retained under one exact rename")
    legacy = rename_matches[0]
    require(legacy.name not in old_names, "old-body rename collides with existing binding")
    normalized_binder, binder_report = normalize_binder(
        one_definition(after, "_bind_helper_arguments"))
    require(dump(normalized_binder) == dump(one_definition(before, "_bind_helper_arguments")),
            "binder matching AST changed")
    require(dump(one_definition(after, "_c_binding_read"))
            == dump(ast.parse(EXPECTED_READ_HELPER).body[0]), "binding read helper changed")
    remaining, added, added_names = [], [], set()
    for node in after.body:
        if node is public:
            continue
        if node is legacy:
            normalized = copy.deepcopy(node)
            normalized.name = "_process_review_rows"
            remaining.append(normalized)
        elif isinstance(node, ast.FunctionDef) and node.name == "_bind_helper_arguments":
            remaining.append(normalized_binder)
        elif base_counts.get(dump(node), 0):
            remaining.append(node)
        else:
            bound = names(node)
            require(bool(bound) and not (bound & old_names) and not (bound & added_names),
                    "unapproved changed/rebound original top-level node at " + str(node.lineno))
            require(all(n.startswith(("_c_", "_C")) for n in bound),
                    "unexpected new top-level binding")
            require(isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Assign, ast.AnnAssign)),
                    "unexpected new top-level operation")
            added.append(node)
            added_names.update(bound)
    require(dump(ast.Module(body=remaining, type_ignores=after.type_ignores))
            == dump(before), "original top-level AST/order is not preserved")
    cap_rows = {}
    for name, expected in CAPS.items():
        matches = [n for n in after.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
        require(len(matches) == 1, "cap assignment count changed: " + name)
        value = ast.literal_eval(matches[0].value)
        require(type(value) is int and value == expected, "cap changed: " + name)
        cap_rows[name] = value
    old_budget = one_definition(before, "_AnalysisBudget")
    new_budget = one_definition(after, "_AnalysisBudget")
    require(dump(old_budget) == dump(new_budget), "budget class changed")
    raw_old = ast.get_source_segment(base.decode("utf-8"), old_budget).encode("utf-8")
    raw_new = ast.get_source_segment(candidate.decode("utf-8"), new_budget).encode("utf-8")
    require(raw_old == raw_new, "budget class source bytes changed")
    inventory = call_inventory(after, old_names, added_names, legacy.name)
    require(all(r["target_defined"] for r in inventory["new_c_direct_calls"]),
            "unresolved direct _c_ call")
    require(all(r["explicit_ctx_budget_and_bool"] for r in inventory["binder_callers"]),
            "budgeted binder caller lacks explicit ctx.budget/bool contract")
    require(not inventory["new_dynamic_execution_calls"],
            "new source directly requests dynamic Python execution")
    require(not inventory["old_live_direct_calls"]
            and not inventory["old_live_loaded_references"],
            "new source directly references a retained old live engine")
    return {"original_top_level_ast_preserved": True,
            "old_process_review_rows_rename": {"name": legacy.name, "line": legacy.lineno},
            "new_public_entry": {"line": public.lineno, "end_line": public.end_lineno},
            "added_top_level_nodes": [{"names": sorted(names(n)), "line": n.lineno,
                                      "end_line": n.end_lineno} for n in added],
            "binder": binder_report | {"consume_calls": 15, "normalizes_exactly": True},
            "caps": cap_rows, "budget_source_sha256": digest(raw_new),
            "implementation_lines": cumulative_lines | {
                "baseline_sha256": BASE_SHA, "ceiling": None, "informational_only": True},
            "inventory": inventory}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-path", required=True)
    parser.add_argument("--candidate-sha256", required=True, type=hex_sha)
    parser.add_argument("--worktree-sha256", required=True, type=hex_sha)
    parser.add_argument("--verifier-sha256", required=True, type=hex_sha)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    require(sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15)
            and sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode
            and sys.flags.safe_path and sys.flags.optimize == 0
            and checked_file(Path(sys.executable)).resolve(strict=True)
                == checked_file(FLOOR_EXE).resolve(strict=True),
            "run static verifier with exact floor executable, actual3.11.15 -I -S -B -P")
    output = pinned_path(args.output, suffix=".json", must_exist=False)
    require(output.parent.is_dir() and not output.exists(), "output must be fresh and create-only")
    report = {"schema": "pontius-rewrite-r2-static-v1",
              "scope": "AST/hash-only review aid; no candidate import or execution",
              "structural_checks_passed": False, "acceptance_proved": False,
              "manual_scope_review_required": True, "scope_approval_granted": False,
              "transitive_engine_exclusion_proved": False,
              "terminal_minus_c_exclusion_proved": False,
              "remaining_manual_obligations": [
                  "Every changed/removed R1 node and added R2 node needs checkpoint scope review; "
                  "_c_/_C names alone grant no permission.",
                  "Terminal _process_definition calls must exclude -c child execution on every path.",
                  "Any _ExecutionScopeVisitor use must be empty terminal evidence, not live analysis.",
                  "Explicit budgeted binder callers must reject expansions before matching.",
                  "Budget-construction owner/phase mapping and metering expressions require source review.",
                  "Direct-call inventory does not resolve aliases, dynamic calls or full transitive behavior.",
                  "Public semantic gates and custody/controller review remain required."]}
    watched, expected = {}, {}
    all_expected_verified = False
    try:
        source = pinned_path(args.candidate_path, suffix=".py")
        watch = W / "tools/generate_test_inventory.py"
        verifier = pinned_path(__file__, suffix=".py")
        expected = {BASE: BASE_SHA, R1_BASE: R1_BASE_SHA, source: args.candidate_sha256,
                    watch: args.worktree_sha256, verifier: args.verifier_sha256}
        expected.update({W / name: value for name, value in PROTECTED.items()})
        require(len(PROTECTED) == 16 and len(expected) == 21, "watched path identity collision")
        data = {}
        for path, want in expected.items():
            raw = checked_file(path).read_bytes()
            got = digest(raw)
            watched[str(path)] = got
            require(got == want, "input hash differs: " + str(path))
            data[path] = raw
        all_expected_verified = True
        for path in (BASE, R1_BASE, source, verifier):
            raw = data[path]
            require(not raw.startswith(b"\xef\xbb\xbf") and b"\r" not in raw,
                    "source input must be UTF-8 without BOM and LF-only: " + str(path))
            raw.decode("utf-8")
        report["candidate_path"] = str(source)
        report["candidate_sha256"] = args.candidate_sha256
        report["r010_baseline_sha256"] = BASE_SHA
        report["r1_baseline_sha256"] = R1_BASE_SHA
        report["worktree_watch_sha256"] = args.worktree_sha256
        report["verifier_sha256"] = args.verifier_sha256
        cumulative = raw_line_changes(data[BASE], data[source])
        r2 = raw_line_changes(data[R1_BASE], data[source])
        report["raw_line_changes"] = {
            "cumulative_from_r010": cumulative | {
                "baseline_sha256": BASE_SHA, "ceiling": None, "informational_only": True},
            "r2_from_accepted_r1": r2 | {
                "baseline_sha256": R1_BASE_SHA, "ceiling": R2_MAXIMUM_CHANGED_LINES,
                "within_ceiling": r2["sum"] <= R2_MAXIMUM_CHANGED_LINES}}
        report["r2_named_nodes"] = r2_named_node_inventory(data[R1_BASE], data[source])
        report["r1_binder_raw"] = r1_binder_bytes(data[R1_BASE], data[source])
        require(report["r1_binder_raw"]["byte_exact"], "binder source differs from accepted R1")
        report["result"] = inspect(data[BASE], data[source], cumulative)
        require(r2["sum"] <= R2_MAXIMUM_CHANGED_LINES,
                "R2 1500 raw added+deleted line ceiling exceeded")
        report["structural_checks_passed"] = True
    except Exception as error:
        report["error"] = {"type": type(error).__name__, "message": str(error)}
    finally:
        after = {}
        for path in watched:
            try:
                after[path] = digest(checked_file(Path(path)).read_bytes())
            except Exception as error:
                after[path] = {"error": type(error).__name__}
        report["expected_input_hashes"] = {str(path): value for path, value in expected.items()}
        report["expected_input_count"] = 21
        report["read_input_count"] = len(watched)
        report["all_expected_inputs_verified"] = all_expected_verified
        report["input_hashes_before"] = watched
        report["input_hashes_after"] = after
        report["all_read_inputs_preserved"] = bool(watched) and watched == after
        if not all_expected_verified or not report["all_read_inputs_preserved"]:
            report["structural_checks_passed"] = False
        report["runtime"] = {"version": list(sys.version_info[:3]), "executable": sys.executable,
                             "implementation": sys.implementation.name,
                             "isolated": bool(sys.flags.isolated), "no_site": bool(sys.flags.no_site),
                             "dont_write_bytecode": bool(sys.flags.dont_write_bytecode),
                             "safe_path": bool(sys.flags.safe_path), "optimize": sys.flags.optimize}
        raw = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
        with output.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        require(output.read_bytes() == raw, "output readback differs")
        print(json.dumps({"output": str(output), "sha256": digest(raw),
                          "structural_checks_passed": report["structural_checks_passed"],
                          "scope_approval_granted": False, "acceptance_proved": False}))
    return 0 if report["structural_checks_passed"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
