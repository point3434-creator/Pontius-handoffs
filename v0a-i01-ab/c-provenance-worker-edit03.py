from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
def change(old,new):
 global s
 assert old in s, old[:120]
 s=s.replace(old,new,1)
change('    member_stable: bool = True\n','    member_stable: bool = True\n    stable_imports: frozenset[str] = frozenset()\n')
start=s.index('def _helper_namespace_certificates(')
end=s.index('\ndef _review_function_registry(',start)
s=s[:start]+'''class _MeteredHelperBindings(_ExceptionBindingVisitor):
    """Reuse lexical binding semantics while charging every visited AST node."""

    def __init__(self, budget: _AnalysisBudget) -> None:
        super().__init__()
        self.budget = budget

    def visit(self, node: ast.AST) -> None:
        self.budget.consume()
        super().visit(node)


def _helper_binding_counts(
    statements: Sequence[ast.stmt], budget: _AnalysisBudget,
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for statement in statements:
        visitor = _MeteredHelperBindings(budget)
        visitor.visit(statement)
        for name in visitor.bound_names:
            budget.consume()
            counts[name] = counts.get(name, 0) + 1
    return counts


def _helper_namespace_certificates(
    tree: ast.Module,
    mutations: frozenset[str],
    budget: _AnalysisBudget,
) -> tuple[dict[int, bool], dict[int, bool], frozenset[str]]:
    """Linear, conservative certificate; aliases share member mutation refusal."""

    dynamic_namespace = False
    for candidate in _metered_ast_walk(tree, budget):
        if isinstance(candidate, ast.Attribute) and candidate.attr in {
            "__dict__", "__globals__", "__code__", "__defaults__", "__kwdefaults__",
        }:
            dynamic_namespace = True
        if isinstance(candidate, ast.Call):
            raw = _qualified_name(candidate.func)
            if raw is not None and raw.rsplit(".", 1)[-1] in {
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
        class_supported = (
            not definition.decorator_list and not definition.keywords
            and all(_qualified_name(base) in {"object", "unittest.TestCase"}
                    for base in definition.bases)
            and not ({"__getattribute__", "__getattr__"} & member_counts.keys())
        )
        for method in definition.body:
            budget.consume()
            if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                members[id(method)] = (
                    class_supported and not dynamic_namespace
                    and method.name not in mutations and member_counts.get(method.name) == 1
                )
    return binding, members, frozenset(stable_imports)


def _helper_provenance_seeds(
    relative_path: str,
    aliases: Mapping[str, str],
    registry: Mapping[str, _ReviewFunction],
    referenced_names: Iterable[str],
    stable_imports: frozenset[str],
    budget: _AnalysisBudget,
) -> dict[str, _FlowValue]:
    seeds: dict[str, _FlowValue] = {}
    for name in referenced_names:
        budget.consume()
        key = f"{relative_path}::{name}"
        definition = registry.get(key)
        if definition is None or not definition.binding_stable:
            continue
        kind = "class" if definition.class_name is not None else "callable"
        seeds[name] = _FlowValue(
            "qname", key, helper_provenance=_HelperProvenance(kind, key)
        )
    for name in stable_imports:
        budget.consume()
        definition = registry.get(aliases.get(name, ""))
        if definition is None or not definition.binding_stable:
            continue
        canonical = f"{definition.relative_path}::"
        if definition.class_name is not None:
            canonical += definition.class_name
            if definition.node.name != "__init__":
                continue
            kind = "class"
        else:
            canonical += definition.node.name
            kind = "callable"
        seeds[name] = _FlowValue(
            "qname", canonical, helper_provenance=_HelperProvenance(kind, canonical)
        )
    return seeds

''' + s[end:]
change('''    registry: dict[str, _ReviewFunction] = {}

    def register''','''    registry: dict[str, _ReviewFunction] = {}
    certificate_budget = _AnalysisBudget()
    mutated_members: set[str] = set()
    for tree in parsed.values():
        for candidate in _metered_ast_walk(tree, certificate_budget):
            if isinstance(candidate, ast.Attribute) and isinstance(candidate.ctx, (ast.Store, ast.Del)):
                mutated_members.add(candidate.attr)
                if candidate.attr in {"__code__", "__defaults__", "__kwdefaults__"} and isinstance(candidate.value, ast.Attribute):
                    mutated_members.add(candidate.value.attr)
            if isinstance(candidate, ast.Call) and _qualified_name(candidate.func) in {"setattr", "delattr"}:
                if len(candidate.args) >= 2 and isinstance(candidate.args[1], ast.Constant) and type(candidate.args[1].value) is str:
                    mutated_members.add(candidate.args[1].value)

    def register''')
change('        stable_bindings, stable_members = _helper_namespace_certificates(tree)\n','''        stable_bindings, stable_members, stable_imports = _helper_namespace_certificates(
            tree, frozenset(mutated_members), certificate_budget,
        )
''')
change('                    binding_stable=stable_bindings.get(id(node), False),\n','                    binding_stable=stable_bindings.get(id(node), False),\n                    stable_imports=stable_imports,\n')
change('                    stable_members.get(id(constructor), not node.keywords),\n','                    stable_members.get(id(constructor), not node.keywords),\n                    stable_imports,\n')
change('                        stable_members.get(id(method), False),\n','                        stable_members.get(id(method), False),\n                        stable_imports,\n')
change('''        helper_seeds=_helper_provenance_seeds(relative_path, aliases, helper_registry),''','''        helper_seeds=_helper_provenance_seeds(
            relative_path, aliases, helper_registry, referenced_names,
            (helper_registry.get(f"{relative_path}::{class_name or node.name}") or
             _ReviewFunction(relative_path, node, aliases, {}, None)).stable_imports,
            analysis_budget,
        ),''')
# Track candidate history only for refusal, never as positive authority.
change('        self._sensitive_helper_candidates: dict[str, bool] = {}\n','''        self._sensitive_helper_candidates: dict[str, bool] = {}
        self._helper_alias_candidates: set[str] = {
            name for name, value in (helper_seeds or {}).items()
            if value.helper_provenance is not None and value.helper_provenance.kind == "callable"
        }
''')
start=s.index('    def _sensitive_helper_candidate(')
end=s.index('    def _snapshot_call(',start)
s=s[:start]+'''    def _sensitive_helper_candidate(self, node: ast.Call) -> bool:
        raw = _qualified_name(node.func)
        if raw is None:
            return False
        if raw in self._helper_alias_candidates:
            return True
        member = raw.rsplit(".", 1)[-1]
        if member not in self._sensitive_helper_candidates:
            sensitive = False
            seen: set[int] = set()
            for definition in self.helper_registry.values():
                self.budget.consume()
                if id(definition) in seen:
                    continue
                seen.add(id(definition))
                if definition.node.name == member and _helper_has_sensitive_closure(
                    definition, self.helper_registry, budget=self.budget,
                ):
                    sensitive = True
                    break
            self._sensitive_helper_candidates[member] = sensitive
        return self._sensitive_helper_candidates[member]

''' + s[end:]
change('''        if isinstance(target, ast.Name):
            if value.kind == "environment":''','''        if isinstance(target, ast.Name):
            if value.helper_provenance is not None and value.helper_provenance.kind == "callable":
                self._helper_alias_candidates.add(target.id)
            if value.kind == "environment":''')
# Refuse unmodeled exposure of an exact owner/callable to another call.
change('''            if record:
                self._record_implicit_protocol_blocker(
                    node,
                    callable_value,''','''            if record:
                if any(value.helper_provenance is not None
                       for value in (*argument_values, *keyword_values)):
                    self.flow.standalone_blockers.append((
                        node, "helper namespace escape is dynamically unresolved",
                    ))
                self._record_implicit_protocol_blocker(
                    node,
                    callable_value,''')
p.write_text(s,encoding='utf-8',newline='\n')
print('metered certificates and refused stale imports, alias loss and namespace escape')