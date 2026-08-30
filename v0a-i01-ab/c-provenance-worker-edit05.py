from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
def change(old,new):
 global s
 assert old in s, old[:100]
 s=s.replace(old,new,1)
change('    stable_imports: frozenset[str] = frozenset()\n','    stable_imports: frozenset[str] = frozenset()\n    namespace_effects: bool = False\n')
anchor='def _flow_may_be_unittest_receiver(value: _FlowValue) -> bool:\n'
addition='''def _flow_contains_helper_identity(value: _FlowValue, budget: _AnalysisBudget) -> bool:
    pending = [value]
    seen: set[int] = set()
    while pending:
        budget.consume()
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        if current.helper_provenance is not None:
            return True
        if current.kind in {"sequence", "slice", "maybe_unbound"}:
            pending.extend(item for item in current.value if isinstance(item, _FlowValue))
        elif current.kind == "mapping":
            pending.extend(item for _, item in current.value)
        elif current.kind == "mapping_keys":
            pending.extend(item for pair in current.value for item in pair)
        elif current.kind == "starred_argument" and isinstance(current.value, _FlowValue):
            pending.append(current.value)
    return False


'''
change(anchor,addition+anchor)
change('''                if any(value.helper_provenance is not None
                       for value in (*argument_values, *keyword_values)):''','''                if any(_flow_contains_helper_identity(value, self.budget)
                       for value in (*argument_values, *keyword_values)):''')
change('''        subscript_owner: _FlowValue | None = None
        subscript_index: _FlowValue | None = None''','''        if isinstance(target, (ast.Attribute, ast.Subscript)) and (
            _flow_contains_helper_identity(value, self.budget)
        ):
            self.flow.standalone_blockers.append((
                target, "helper namespace store is dynamically unresolved",
            ))
        subscript_owner: _FlowValue | None = None
        subscript_index: _FlowValue | None = None''')
# Gather lexical namespace effects in the same per-module mutation traversal.
old='''    mutated_members: set[str] = set()
    for path, tree in parsed.items():
        for candidate in _metered_ast_walk(tree, certificate_budgets[path]):
            if isinstance(candidate, ast.Attribute) and isinstance(candidate.ctx, (ast.Store, ast.Del)):
                mutated_members.add(candidate.attr)
                if candidate.attr in {"__code__", "__defaults__", "__kwdefaults__"} and isinstance(candidate.value, ast.Attribute):
                    mutated_members.add(candidate.value.attr)
            if isinstance(candidate, ast.Call) and _qualified_name(candidate.func) in {"setattr", "delattr"}:
                if len(candidate.args) >= 2 and isinstance(candidate.args[1], ast.Constant) and type(candidate.args[1].value) is str:
                    mutated_members.add(candidate.args[1].value)
'''
new='''    mutated_members: set[str] = set()
    effectful_functions: set[int] = set()
    for path, tree in parsed.items():
        pending: list[tuple[ast.AST, ast.AST | None]] = [(tree, None)]
        while pending:
            certificate_budgets[path].consume()
            candidate, owner = pending.pop()
            if isinstance(candidate, (ast.FunctionDef, ast.AsyncFunctionDef)):
                owner = candidate
            if isinstance(candidate, (ast.Global, ast.Nonlocal)) and owner is not None:
                effectful_functions.add(id(owner))
            if isinstance(candidate, ast.Attribute) and isinstance(
                candidate.ctx, (ast.Store, ast.Del)
            ):
                mutated_members.add(candidate.attr)
                if candidate.attr in {"__code__", "__defaults__", "__kwdefaults__"} and (
                    isinstance(candidate.value, ast.Attribute)
                ):
                    mutated_members.add(candidate.value.attr)
            if isinstance(candidate, ast.Call) and _qualified_name(candidate.func) in {
                "setattr", "delattr",
            }:
                if len(candidate.args) >= 2 and isinstance(candidate.args[1], ast.Constant):
                    if type(candidate.args[1].value) is str:
                        mutated_members.add(candidate.args[1].value)
            pending.extend((child, owner) for child in ast.iter_child_nodes(candidate))
'''
change(old,new)
change('                    stable_imports=stable_imports,\n','                    stable_imports=stable_imports,\n                    namespace_effects=id(node) in effectful_functions,\n')
change('''                    stable_members.get(id(constructor), not node.keywords),
                    stable_imports,
''','''                    stable_members.get(id(constructor), not node.keywords),
                    stable_imports,
                    id(constructor) in effectful_functions,
''')
change('''                        stable_members.get(id(method), False),
                        stable_imports,
''','''                        stable_members.get(id(method), False),
                        stable_imports,
                        id(method) in effectful_functions,
''')
s=s.replace('''namespace_effects=bool(
                            _lexical_binding_scope(definition.node).global_names
                            or _lexical_binding_scope(definition.node).nonlocal_names
                        )''','namespace_effects=definition.namespace_effects')
s=s.replace('''namespace_effects=bool(
                _lexical_binding_scope(definition.node).global_names
                or _lexical_binding_scope(definition.node).nonlocal_names
            )''','namespace_effects=definition.namespace_effects')
anchor='def _helper_binding_counts(\n'
addition='''def _helper_local_namespace_effects(
    node: ast.FunctionDef | ast.AsyncFunctionDef, budget: _AnalysisBudget,
) -> bool:
    visitor = _MeteredHelperBindings(budget)
    for statement in node.body:
        visitor.visit(statement)
    return bool(visitor.global_names or visitor.nonlocal_names)


'''
change(anchor,addition+anchor)
change('''                        namespace_effects=bool(
                            _lexical_binding_scope(statement).global_names
                            or _lexical_binding_scope(statement).nonlocal_names
                        ),''','''                        namespace_effects=_helper_local_namespace_effects(
                            statement, self.budget,
                        ),''')
p.write_text(s,encoding='utf-8',newline='\n')
print('completed metered container escape and namespace-effect metadata')