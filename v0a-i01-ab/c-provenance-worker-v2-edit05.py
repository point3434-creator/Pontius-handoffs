from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
def one(old,new):
 global s
 assert s.count(old)==1,(s.count(old),old[:80])
 s=s.replace(old,new)
s=s.replace('    namespace_effects: bool = False\n','    namespace_effects: frozenset[str] = frozenset()\n')
one('                   namespace_effects=False, helper_refusal=None)\n','                   namespace_effects=frozenset(), helper_refusal=None)\n')
one('        namespace_effects=any(value.namespace_effects for value in present),\n','        namespace_effects=frozenset().union(*(value.namespace_effects for value in present)),\n')
one('''            if name in self.lexical_scope.parameter_names:
                self.values[name] = (entry_values or {}).get(
''','''            if name in self.lexical_scope.parameter_names:
                if helper_registry is None:
                    self.values.setdefault(
                        name, _flow_unknown("function parameter is dynamically unresolved"),
                    )
                    continue
                self.values[name] = (entry_values or {}).get(
''')
resolver_start=s.index('class _SourceOrderedResolver:')
prefix,s=s[:resolver_start],s[resolver_start:]
one('''        for name in self.lexical_scope.nonlocal_names:
            builtin_marker = next(
''','''        for name in self.lexical_scope.nonlocal_names:
            if name in (entry_values or {}):
                self.values[name] = entry_values[name]
                continue
            builtin_marker = next(
''')
s=prefix+s
one('''        if merged_callable.namespace_effects:
            refusal = "helper namespace effects are dynamically unresolved"
''','''        if any(name in merged_values and _flow_contains_helper_identity(
            merged_values[name], self.budget,
        ) for name in merged_callable.namespace_effects):
            refusal = "helper namespace effects are dynamically unresolved"
''')
one(''') -> bool:
    visitor = _MeteredHelperBindings(budget)
    for statement in node.body:
        visitor.visit(statement)
    return bool(visitor.bound_names & (visitor.global_names | visitor.nonlocal_names))
''',''') -> frozenset[str]:
    visitor = _MeteredHelperBindings(budget)
    for statement in node.body:
        visitor.visit(statement)
    return frozenset(visitor.bound_names & (visitor.global_names | visitor.nonlocal_names))
''')
one('    effectful_functions: set[int] = set()\n','    effectful_functions: dict[int, frozenset[str]] = {}\n')
one('''            if isinstance(candidate, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                _helper_local_namespace_effects(candidate, certificate_budgets[path])
            ):
                effectful_functions.add(id(candidate))
''','''            if isinstance(candidate, (ast.FunctionDef, ast.AsyncFunctionDef)):
                effectful_functions[id(candidate)] = _helper_local_namespace_effects(
                    candidate, certificate_budgets[path],
                )
''')
s=s.replace('id(node) in effectful_functions','effectful_functions.get(id(node), frozenset())')
s=s.replace('id(constructor) in effectful_functions','effectful_functions.get(id(constructor), frozenset())')
s=s.replace('id(method) in effectful_functions','effectful_functions.get(id(method), frozenset())')
s=s.replace('namespace_effects=definition.namespace_effects if definition is not None else False','namespace_effects=definition.namespace_effects if definition is not None else frozenset()')
p.write_text(s,encoding='utf-8',newline='\n')