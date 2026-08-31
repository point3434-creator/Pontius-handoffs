from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
def one(old,new):
 global s
 assert s.count(old)==1,(s.count(old),old[:100])
 s=s.replace(old,new)
one('    return bool(visitor.global_names or visitor.nonlocal_names)\n','    return bool(visitor.bound_names & (visitor.global_names | visitor.nonlocal_names))\n')
a=s.index('def _helper_namespace_certificates(');b=s.index('\ndef _helper_provenance_seeds(',a)
s=s[:a]+'''def _helper_initialization_nodes(
    tree: ast.AST, budget: _AnalysisBudget,
) -> Iterable[ast.AST]:
    pending = [tree]
    while pending:
        candidate = pending.pop()
        budget.consume()
        yield candidate
        if isinstance(candidate, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            pending.extend(candidate.args.defaults)
            pending.extend(value for value in candidate.args.kw_defaults if value is not None)
            pending.extend(getattr(candidate, "decorator_list", ()))
        else:
            pending.extend(ast.iter_child_nodes(candidate))


def _helper_namespace_certificates(
    tree: ast.Module, budget: _AnalysisBudget,
) -> tuple[dict[int, bool], dict[int, bool], frozenset[str]]:
    # Deferred bodies do not mutate their enclosing namespace at definition time.
    dynamic_namespace = False
    for candidate in _helper_initialization_nodes(tree, budget):
        if isinstance(candidate, ast.ImportFrom) and any(
            alias.name == "*" for alias in candidate.names
        ):
            dynamic_namespace = True
        if isinstance(candidate, ast.Attribute) and isinstance(
            candidate.ctx, (ast.Store, ast.Del)
        ):
            dynamic_namespace = True
        if isinstance(candidate, ast.Call) and _qualified_name(candidate.func) in {
            "setattr", "delattr", "vars", "globals", "locals", "exec", "eval",
        }:
            dynamic_namespace = True
    counts = _helper_binding_counts(tree.body, budget)
    stable_imports: set[str] = set()
    for statement in tree.body:
        budget.consume()
        if isinstance(statement, (ast.Import, ast.ImportFrom)):
            visitor = _MeteredHelperBindings(budget)
            visitor.visit(statement)
            stable_imports.update(name for name in visitor.bound_names if counts[name] == 1)
    if dynamic_namespace:
        stable_imports.clear()
    binding: dict[int, bool] = {}
    members: dict[int, bool] = {}
    for definition in tree.body:
        budget.consume()
        if not isinstance(definition, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        binding[id(definition)] = counts.get(definition.name) == 1 and not dynamic_namespace
        if not isinstance(definition, ast.ClassDef):
            continue
        member_counts = _helper_binding_counts(definition.body, budget)
        aliases = {name: target for name, target in
                   _module_import_aliases(tree, stop_before=definition).items()
                   if name in stable_imports}
        class_supported = (
            not definition.keywords
            and all(_resolved_qualified_name(base, aliases) in {"object", "unittest.TestCase"}
                    and not (isinstance(base, ast.Name) and base.id == "object"
                             and counts.get("object", 0)) for base in definition.bases)
            and all(_resolved_qualified_name(
                decorator.func if isinstance(decorator, ast.Call) else decorator, aliases,
            ) in {"unittest.skip", "unittest.skipIf", "unittest.skipUnless"}
                    and (_qualified_name(decorator.func if isinstance(decorator, ast.Call)
                                        else decorator) or "").split(".")[0] in stable_imports
                    for decorator in definition.decorator_list)
            and not ({"__getattribute__", "__getattr__"} & member_counts.keys())
        )
        for method in definition.body:
            budget.consume()
            if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                members[id(method)] = (
                    class_supported and not dynamic_namespace and member_counts.get(method.name) == 1
                )
    return binding, members, frozenset(stable_imports)

''' +s[b:]
one('''            "qname", key, helper_provenance=_HelperProvenance(kind, key),
''','''            "qname", name, helper_provenance=_HelperProvenance(kind, key),
''')
a=s.index('    for name in stable_imports:\n',s.index('def _helper_provenance_seeds'))
b=s.index('    return seeds\n',a)
s=s[:a]+'''    for name in stable_imports:
        budget.consume()
        target = aliases.get(name, "")
        proof = getattr(registry, "qualified_proofs", {}).get(target)
        if proof is None:
            continue
        definition = registry.get(proof.key)
        seeds[name] = _FlowValue(
            "qname", target, helper_provenance=proof,
            namespace_effects=definition.namespace_effects if definition is not None else False,
        )
''' +s[b:]
one('''        self._definitions: set[int] = set()
''','''        self._definitions: set[int] = set()
        self.exports: dict[str, _HelperProvenance] = {}
        self.qualified_proofs: dict[str, _HelperProvenance] = {}
''')
a=s.index('    mutated_members: set[str] = set()\n',s.index('def _review_function_registry'))
b=s.index('\n    def register(',a)
s=s[:a]+'''    effectful_functions: set[int] = set()
    for path, tree in parsed.items():
        for candidate in _metered_ast_walk(tree, certificate_budgets[path]):
            if isinstance(candidate, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                _helper_local_namespace_effects(candidate, certificate_budgets[path])
            ):
                effectful_functions.add(id(candidate))
''' +s[b:]
one('''            tree, frozenset(mutated_members), certificate_budgets[relative_path],
''','''            tree, certificate_budgets[relative_path],
''')
# Export proof is a separate finite graph. Raw legacy registry aliases remain discovery only.
a=s.index('    return registry\n',s.index('def _review_function_registry'))
s=s[:a]+'''    for relative_path, tree in parsed.items():
        budget = certificate_budgets[relative_path]
        module = ".".join(PurePosixPath(relative_path).with_suffix("").parts)
        registry.qualified_proofs[module] = _HelperProvenance("module", relative_path)
        registry.qualified_proofs[PurePosixPath(relative_path).stem] = (
            _HelperProvenance("module", relative_path)
        )
        for node in tree.body:
            budget.consume()
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            key = f"{relative_path}::{node.name}"
            definition = registry.get(key)
            if definition is None or not definition.binding_stable:
                continue
            proof = _HelperProvenance("class" if isinstance(node, ast.ClassDef) else "callable", key)
            registry.exports[key] = proof
            registry.qualified_proofs[f"{module}.{node.name}"] = proof
    for _ in range(len(parsed) + 1):
        changed = False
        for relative_path, tree in parsed.items():
            budget = certificate_budgets[relative_path]
            module = ".".join(PurePosixPath(relative_path).with_suffix("").parts)
            definitions = (registry.get(f"{relative_path}::{node.name}")
                           for node in tree.body if isinstance(
                               node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)))
            stable = next((definition.stable_imports for definition in definitions
                           if definition is not None), frozenset())
            for name, target in _module_import_aliases(tree).items():
                budget.consume()
                proof = registry.qualified_proofs.get(target)
                if name not in stable or proof is None:
                    continue
                key = f"{relative_path}::{name}"
                if key not in registry.exports:
                    registry.exports[key] = proof
                    registry.qualified_proofs[f"{module}.{name}"] = proof
                    changed = True
        if not changed:
            break
''' +s[a:]
one('''        entry_bound_unknown_names=(entry_values or {}).keys(),
''','''        entry_bound_unknown_names=(name for name, value in (entry_values or {}).items()
                                   if not (value.kind == "qname"
                                           and aliases.get(name) == value.value)),
''')
p.write_text(s,encoding='utf-8',newline='\n')