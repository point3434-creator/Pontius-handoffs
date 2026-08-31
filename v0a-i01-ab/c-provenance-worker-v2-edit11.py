from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
def one(old,new):
 global s
 assert s.count(old)==1,(s.count(old),old[:75])
 s=s.replace(old,new)
one('''    for definition in tree.body:
        budget.consume()
        if not isinstance(definition, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
''','''    source_aliases: dict[str, str] = {}
    for definition in tree.body:
        budget.consume()
        if isinstance(definition, (ast.Import, ast.ImportFrom)):
            source_aliases.update(_module_import_aliases(ast.Module(body=[definition], type_ignores=[])))
        if not isinstance(definition, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
''')
one('''        aliases = {name: target for name, target in
                   _module_import_aliases(tree, stop_before=definition).items()
                   if name in stable_imports}
''','''        aliases = {name: target for name, target in source_aliases.items()
                   if name in stable_imports}
''')
one('''        assignments = _static_assignments(tree.body)
        dependencies = registry.module_dependencies.setdefault(relative_path, set())
''','''        assignments = _static_assignments(tree.body)
        binding_counts = _helper_binding_counts(tree.body, budget)
        plain_classes = {node.name for node in tree.body if isinstance(node, ast.ClassDef)
                         and not node.bases and not node.keywords and not node.decorator_list
                         and all(isinstance(member, ast.Pass) for member in node.body)}
        dependencies = registry.module_dependencies.setdefault(relative_path, set())
''')
one('''            elif isinstance(candidate, ast.Subscript) and isinstance(candidate.ctx, (ast.Store, ast.Del)):
                if isinstance(candidate.value, ast.Call) and _qualified_name(candidate.value.func) in {
                    "vars", "globals", "locals",
                }:
                    registry.initial_namespace_refusals.add(relative_path)
''','''            elif isinstance(candidate, ast.Subscript) and isinstance(candidate.ctx, (ast.Store, ast.Del)):
                if isinstance(candidate.value, ast.Call):
                    namespace = _qualified_name(candidate.value.func)
                    if namespace in {"globals", "locals"}:
                        registry.initial_namespace_refusals.add(relative_path)
                    elif namespace == "vars" and len(candidate.value.args) == 1:
                        target = candidate.value.args[0]
                elif isinstance(candidate.value, ast.Attribute) and candidate.value.attr == "__dict__":
                    target = candidate.value.value
                if isinstance(candidate.slice, ast.Constant) and type(candidate.slice.value) is str:
                    member = candidate.slice.value
''')
one('''            raw = _resolved_qualified_name(target, aliases) or ""
            proof = registry.qualified_proofs.get(raw) or registry.exports.get(
''','''            if isinstance(target, ast.Call):
                factory = _resolved_qualified_name(target.func, aliases)
                root = (_qualified_name(target.func) or "").split(".")[0]
                if ((factory in {"types.ModuleType", "types.SimpleNamespace"}
                     and binding_counts.get(root) == 1 and root in aliases)
                        or (isinstance(target.func, ast.Name)
                            and target.func.id in plain_classes
                            and binding_counts.get(target.func.id) == 1)):
                    # These constructors allocate a fresh unrelated namespace.
                    continue
            raw = _resolved_qualified_name(target, aliases) or ""
            if (isinstance(target, ast.Name) and target.id in aliases
                    and binding_counts.get(target.id) == 1
                    and raw not in registry.qualified_proofs):
                # Exact external module objects use the existing protected-namespace
                # mutation path; their attribute slots are not registry helper owners.
                continue
            proof = registry.qualified_proofs.get(raw) or registry.exports.get(
''')
p.write_text(s,encoding='utf-8',newline='\n')