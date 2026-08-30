from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
def change(old,new):
 global s
 assert old in s, old[:100]
 s=s.replace(old,new,1)
change('    callable_defaults: tuple[tuple[str, _FlowValue], ...] = ()\n','    callable_defaults: tuple[tuple[str, _FlowValue], ...] = ()\n    namespace_effects: bool = False\n')
change('''            provenance = base.helper_provenance
            if provenance is not None and provenance.kind in {"class", "instance"}:''','''            provenance = base.helper_provenance
            if provenance is not None and provenance.kind == "callable":
                return _flow_unknown(
                    "helper callable attribute access is dynamically unresolved", sensitive=True,
                )
            if provenance is not None and provenance.kind in {"class", "instance"}:''')
change('''                            "callable", key, bound
                        )
                    )''','''                            "callable", key, bound
                        ), namespace_effects=bool(
                            _lexical_binding_scope(definition.node).global_names
                            or _lexical_binding_scope(definition.node).nonlocal_names
                        ),
                    )''')
change('''        key = id(node)
        if callable_value.helper_provenance is None''','''        key = id(node)
        if callable_value.namespace_effects:
            callable_value = _flow_unknown(
                "helper global or nonlocal effects are dynamically unresolved", sensitive=True,
            )
        if callable_value.helper_provenance is None''')
change('''                    installed = replace(installed, callable_defaults=tuple(captured_defaults))''','''                    installed = replace(
                        installed, callable_defaults=tuple(captured_defaults),
                        namespace_effects=bool(
                            _lexical_binding_scope(statement).global_names
                            or _lexical_binding_scope(statement).nonlocal_names
                        ),
                    )''')
change('''    for candidate in _metered_ast_walk(tree, budget):
        if isinstance(candidate, ast.Attribute) and candidate.attr in {''','''    for candidate in _metered_ast_walk(tree, budget):
        if isinstance(candidate, ast.ImportFrom) and any(
            alias.name == "*" for alias in candidate.names
        ):
            dynamic_namespace = True
        if isinstance(candidate, ast.Attribute) and candidate.attr in {''')
change('''            and not ({"__getattribute__", "__getattr__"} & member_counts.keys())''','''            and not ({"__getattribute__", "__getattr__"} & member_counts.keys())
            and not (mutations & {
                "__class__", "__bases__", "__mro__", "__getattribute__", "__getattr__",
            })''')
# Each module is an existing bounded analysis unit; do not aggregate the corpus cap.
change('''    registry: dict[str, _ReviewFunction] = {}
    certificate_budget = _AnalysisBudget()
    mutated_members: set[str] = set()
    for tree in parsed.values():
        for candidate in _metered_ast_walk(tree, certificate_budget):''','''    registry = _ReviewRegistry()
    certificate_budgets = {path: _AnalysisBudget() for path in parsed}
    mutated_members: set[str] = set()
    for path, tree in parsed.items():
        for candidate in _metered_ast_walk(tree, certificate_budgets[path]):''')
change('            tree, frozenset(mutated_members), certificate_budget,\n','            tree, frozenset(mutated_members), certificate_budgets[relative_path],\n')
# Register a bounded direct candidate index once, instead of scanning every alias at each call.
anchor='def _review_function_registry(\n'
addition='''class _ReviewRegistry(dict[str, _ReviewFunction]):
    def __init__(self) -> None:
        super().__init__()
        self.by_name: dict[str, list[_ReviewFunction]] = {}
        self._definitions: set[int] = set()

    def __setitem__(self, key: str, definition: _ReviewFunction) -> None:
        super().__setitem__(key, definition)
        if id(definition) not in self._definitions:
            self._definitions.add(id(definition))
            self.by_name.setdefault(definition.node.name, []).append(definition)


'''
change(anchor,addition+anchor)
change('''            for definition in self.helper_registry.values():
                self.budget.consume()''','''            candidates = (
                self.helper_registry.by_name.get(member, ())
                if isinstance(self.helper_registry, _ReviewRegistry)
                else self.helper_registry.values()
            )
            for definition in candidates:
                self.budget.consume()''')
# Module functions can also mutate caller-visible namespace bindings.
change('''            "qname", key, helper_provenance=_HelperProvenance(kind, key)
        )
    for name in stable_imports:''','''            "qname", key, helper_provenance=_HelperProvenance(kind, key),
            namespace_effects=bool(
                _lexical_binding_scope(definition.node).global_names
                or _lexical_binding_scope(definition.node).nonlocal_names
            ),
        )
    for name in stable_imports:''')
change('''            "qname", canonical, helper_provenance=_HelperProvenance(kind, canonical)
        )
    return seeds''','''            "qname", canonical, helper_provenance=_HelperProvenance(kind, canonical),
            namespace_effects=bool(
                _lexical_binding_scope(definition.node).global_names
                or _lexical_binding_scope(definition.node).nonlocal_names
            ),
        )
    return seeds''')
p.write_text(s,encoding='utf-8',newline='\n')
print('refused unsupported namespace effects and bounded certificate budgets per module')