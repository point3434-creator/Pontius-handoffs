from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
def change(old,new,count=1):
 global s
 assert s.count(old)>=count, old[:100]
 s=s.replace(old,new,count)
change('    descriptor_kind: str | None = "ordinary"\n','    descriptor_kind: str | None = "ordinary"\n    binding_stable: bool = True\n    member_stable: bool = True\n')
change('@dataclass(frozen=True, slots=True)\nclass _FlowValue:', '''@dataclass(frozen=True, slots=True)
class _HelperProvenance:
    """Exact source definition identity; never inferred from a qname spelling."""

    kind: str
    key: str
    bound: bool = False


@dataclass(frozen=True, slots=True)
class _FlowValue:''')
change('    container_kind: str | None = None\n','    container_kind: str | None = None\n    helper_provenance: _HelperProvenance | None = None\n')
change('    receiver_attributes: dict[int, ast.Attribute] = field(default_factory=dict)\n','''    receiver_attributes: dict[int, ast.Attribute] = field(default_factory=dict)
    helper_calls: dict[int, _HelperProvenance] = field(default_factory=dict)
    values_by_call: dict[int, dict[str, _FlowValue]] = field(default_factory=dict)
    arguments_by_call: dict[int, dict[int, _FlowValue]] = field(default_factory=dict)
''')
change('        entry_values: Mapping[str, _FlowValue] | None = None,\n    ) -> None:', '''        entry_values: Mapping[str, _FlowValue] | None = None,
        helper_registry: Mapping[str, _ReviewFunction] | None = None,
        helper_seeds: Mapping[str, _FlowValue] | None = None,
    ) -> None:''')
change('        self.budget = budget or _AnalysisBudget()\n        self.module_assignments', '        self.budget = budget or _AnalysisBudget()\n        self.helper_registry = helper_registry or {}\n        self.module_assignments')
change('        self.values.update(entry_values or {})\n        for name in self.lexical_scope.local_names:', '        self.values.update(helper_seeds or {})\n        self.values.update(entry_values or {})\n        for name in self.lexical_scope.local_names:')
change('''                self.values.setdefault(
                    name,
                    _flow_unknown("function parameter is dynamically unresolved"),
                )''', '''                self.values[name] = (entry_values or {}).get(
                    name,
                    self._evaluate(module_assignments[name], self.values, False)
                    if name in module_assignments and helper_registry is not None
                    else _flow_unknown("function parameter is dynamically unresolved"),
                )''')
# Preserve raw flow state and evaluated callable identity at the same source point.
change('''        callable_value: _FlowValue,
    ) -> None:
        key = id(node)''','''        callable_value: _FlowValue,
        arguments: Mapping[int, _FlowValue] | None = None,
    ) -> None:
        key = id(node)''')
change('        self.flow.aliases_by_call[key] = _flow_aliases(merged_values)\n', '''        self.flow.values_by_call[key] = merged_values
        previous_arguments = self.flow.arguments_by_call.get(key, {})
        self.flow.arguments_by_call[key] = {
            expression: _merge_flow_values(
                "helper argument", (previous_arguments[expression], value)
            ) if expression in previous_arguments else value
            for expression, value in (arguments or {}).items()
        }
        self.flow.helper_calls.pop(key, None)
        if merged_callable.helper_provenance is not None:
            self.flow.helper_calls[key] = merged_callable.helper_provenance
        self.flow.aliases_by_call[key] = _flow_aliases(merged_values)
''')
# Member lookup consumes an exact owner certificate, not its spelling.
change('''            base = self._evaluate(node.value, values, record)
            if record:
                self._record_implicit_protocol_blocker(''', '''            base = self._evaluate(node.value, values, record)
            provenance = base.helper_provenance
            if provenance is not None and provenance.kind in {"class", "instance"}:
                key = f"{provenance.key}::{node.attr}"
                definition = self.helper_registry.get(key)
                if definition is not None:
                    if not definition.member_stable or definition.descriptor_kind is None:
                        return _flow_unknown(
                            "helper descriptor member identity is unresolved", sensitive=True
                        )
                    bound = definition.descriptor_kind == "classmethod" or (
                        definition.descriptor_kind == "ordinary"
                        and provenance.kind == "instance"
                    )
                    return _FlowValue(
                        "qname", key, helper_provenance=_HelperProvenance(
                            "callable", key, bound
                        )
                    )
            if record:
                self._record_implicit_protocol_blocker(''')
change('''        if isinstance(node, ast.Call):
            callable_value = self._evaluate(node.func, values, record)
            argument_values: list[_FlowValue] = []''','''        if isinstance(node, ast.Call):
            try:
                callable_value = self._evaluate(node.func, values, record)
            except _ExpressionDoesNotComplete:
                if record:
                    self._snapshot_call(
                        node, values, _flow_unknown("callee lookup does not complete")
                    )
                raise
            argument_values: list[_FlowValue] = []''')
change('                self._snapshot_call(node, values, callable_value)\n','''                self._snapshot_call(
                    node, values, callable_value,
                    {id(expression): value for expression, value in zip(
                        (*node.args, *(keyword.value for keyword in node.keywords)),
                        (*argument_values, *keyword_values), strict=True,
                    )},
                )
''')
# Source review entry points explicitly pass this optional provenance context.
change('''    entry_values: Mapping[str, _FlowValue] | None = None,
) -> _ReviewFlow:''','''    entry_values: Mapping[str, _FlowValue] | None = None,
    helper_registry: Mapping[str, _ReviewFunction] | None = None,
    helper_seeds: Mapping[str, _FlowValue] | None = None,
) -> _ReviewFlow:''')
change('''        sensitive_definition_markers,
        entry_values,
    )
    for name in resolver.exception_scope.entry_bound_names:''','''        sensitive_definition_markers,
        entry_values,
        helper_registry,
        helper_seeds,
    )
    for name in resolver.exception_scope.entry_bound_names:''')
# Registry certificates are conservative whole-module facts, not a Python heap.
anchor='def _review_function_registry(\n'
addition='''def _helper_namespace_certificates(
    tree: ast.Module,
) -> tuple[dict[int, bool], dict[int, bool]]:
    """Certify original bindings and slots; unsupported mutation loses proof."""

    budget = _AnalysisBudget()
    mutations: set[str] = set()
    dynamic_namespace = False
    for candidate in _metered_ast_walk(tree, budget):
        if isinstance(candidate, ast.Attribute):
            if isinstance(candidate.ctx, (ast.Store, ast.Del)):
                mutations.add(candidate.attr)
            if candidate.attr in {"__dict__", "__globals__"}:
                dynamic_namespace = True
        if isinstance(candidate, ast.Call):
            raw = _qualified_name(candidate.func)
            if raw is not None and raw.rsplit(".", 1)[-1] in {
                "setattr", "delattr", "vars", "globals", "locals", "exec", "eval",
            }:
                dynamic_namespace = True
    binding: dict[int, bool] = {}
    members: dict[int, bool] = {}
    for definition in tree.body:
        if not isinstance(definition, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        other_bindings = _descriptor_unavailable_names([
            statement for statement in tree.body if statement is not definition
        ])
        binding[id(definition)] = (
            definition.name not in other_bindings and not dynamic_namespace
        )
        if not isinstance(definition, ast.ClassDef):
            continue
        class_supported = (
            not definition.decorator_list and not definition.keywords
            and all(_qualified_name(base) in {"object", "unittest.TestCase"}
                    for base in definition.bases)
            and not any(isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
                        and member.name in {"__getattribute__", "__getattr__"}
                        for member in definition.body)
        )
        for method in definition.body:
            if not isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            budget.consume()
            other_members = _descriptor_unavailable_names([
                member for member in definition.body if member is not method
            ])
            members[id(method)] = (
                class_supported and not dynamic_namespace
                and method.name not in mutations and method.name not in other_members
            )
    return binding, members


def _helper_provenance_seeds(
    relative_path: str,
    aliases: Mapping[str, str],
    registry: Mapping[str, _ReviewFunction],
) -> dict[str, _FlowValue]:
    seeds: dict[str, _FlowValue] = {}
    prefix = f"{relative_path}::"
    for key, definition in registry.items():
        if not key.startswith(prefix) or "::" in key[len(prefix):]:
            continue
        if not definition.binding_stable:
            continue
        kind = "class" if definition.class_name is not None else "callable"
        seeds[key[len(prefix):]] = _FlowValue(
            "qname", key, helper_provenance=_HelperProvenance(kind, key)
        )
    for name, qualified in aliases.items():
        definition = registry.get(qualified)
        if definition is None or not definition.binding_stable:
            continue
        canonical = f"{definition.relative_path}::"
        if definition.class_name is not None:
            canonical += definition.class_name
            if definition.node.name != "__init__":
                # Imported descriptor values require separate binding proof.
                continue
            kind = "class"
        else:
            canonical += definition.node.name
            kind = "callable"
        seeds[name] = _FlowValue(
            "qname", canonical, helper_provenance=_HelperProvenance(kind, canonical)
        )
    return seeds


'''
change(anchor,addition+anchor)
change('''        assignments = _static_assignments(tree.body)
        descriptor_names =''','''        assignments = _static_assignments(tree.body)
        stable_bindings, stable_members = _helper_namespace_certificates(tree)
        descriptor_names =''')
change('''                    provenance.enclosing_names_by_node.get(id(node), frozenset()),
                )''','''                    provenance.enclosing_names_by_node.get(id(node), frozenset()),
                    binding_stable=stable_bindings.get(id(node), False),
                )''')
change('''                    _helper_descriptor_kind(constructor, unavailable_descriptors),
                )''','''                    _helper_descriptor_kind(constructor, unavailable_descriptors),
                    stable_bindings.get(id(node), False),
                    stable_members.get(id(constructor), not node.keywords),
                )''')
change('''                        _helper_descriptor_kind(method, unavailable_descriptors),
                    )''','''                        _helper_descriptor_kind(method, unavailable_descriptors),
                        stable_bindings.get(id(node), False),
                        stable_members.get(id(method), False),
                    )''')
# The binder accepts already-proved descriptor binding without re-reading roots.
change('''    receiver_kinds: Mapping[str, str],
) -> dict[str, tuple[ast.expr, bool]] | None:''','''    receiver_kinds: Mapping[str, str],
    proven_bound: bool | None = None,
) -> dict[str, tuple[ast.expr, bool]] | None:''')
change('''    bound = _helper_is_bound(
        call, definition, aliases, receiver_kinds=receiver_kinds
    )''','''    bound = proven_bound if proven_bound is not None else _helper_is_bound(
        call, definition, aliases, receiver_kinds=receiver_kinds
    )''')
# Caller entries seed identities; ordinary lexical flow performs all invalidation.
old='''    body_receiver_kinds = dict(receiver_kinds)
    receiver_bindings = _ExceptionBindingVisitor()
    for statement in node.body:
        receiver_bindings.visit(statement)
    for name in receiver_bindings.bound_names:
        body_receiver_kinds.pop(name, None)
'''
new='''    body_receiver_kinds = dict(receiver_kinds)
    provenance_entries = dict(entry_values or {})
    if class_name is not None:
        for name, kind in receiver_kinds.items():
            # A recursive caller supplies source-point values, including lost proof.
            if entry_values is not None and name in entry_values and (
                entry_values[name].helper_provenance is not None
                or entry_values[name].reason != "unittest entry parameter is unresolved"
            ):
                continue
            provenance_entries[name] = _FlowValue(
                "qname", name, helper_provenance=_HelperProvenance(
                    kind, f"{relative_path}::{class_name}"
                )
            )
'''
change(old,new)
change('''        entry_values=entry_values,
    )
    _append_implicit_protocol_analyzed_sites(''','''        entry_values=provenance_entries,
        helper_registry=helper_registry,
        helper_seeds=_helper_provenance_seeds(relative_path, aliases, helper_registry),
    )
    _append_implicit_protocol_analyzed_sites(''')
# Local recursive expansion must have exact definition-point identity.
change('''            if local_key in active_helpers:
''','''            if exact_local_node is None:
                blockers.append(_review_blocker(
                    item_id, relative_path, call,
                    "local helper callable provenance is unresolved",
                ))
                continue
            if local_key in active_helpers:
''')
change('''                receiver_kinds=body_receiver_kinds,
            )
            local_assignments''','''                receiver_kinds={},
                proven_bound=False,
            )
            local_assignments''')
change('''                receiver_kinds={
                    name: kind for name, kind in body_receiver_kinds.items()
                    if name not in _lexical_binding_scope(local_node).parameter_names
                },
            )''','''                receiver_kinds={},
                entry_values={
                    name: value for name, value in source_flow.values_by_call[id(call)].items()
                    if name not in _lexical_binding_scope(local_node).local_names
                },
            )''')
# Prefer proved identity; candidate spelling alone can only produce a blocker.
change('''        if helper is not None:
            helper_key, definition = helper
            helper_edges.append(''','''        proof = source_flow.helper_calls.get(id(call))
        if proof is not None and proof.kind == "callable":
            proved_definition = helper_registry.get(proof.key)
            if proved_definition is not None:
                helper = (proof.key, proved_definition)
        if helper is not None:
            helper_key, definition = helper
            if proof is None or proof.kind != "callable" or proof.key != helper_key:
                if _helper_has_sensitive_closure(
                    definition, helper_registry, budget=analysis_budget,
                ):
                    blockers.append(_review_blocker(
                        item_id, relative_path, call,
                        "helper callable provenance is unresolved",
                    ))
                continue
            helper_edges.append(''')
change('''                receiver_kinds=body_receiver_kinds,
            )
            argument_failure = supplied_arguments''','''                receiver_kinds={},
                proven_bound=proof.bound,
            )
            argument_failure = supplied_arguments''')
# Pure evaluated arguments support named expressions without reevaluation.
change('''                    value = _static_value(
                        expression,
                        (
                            definition.module_assignments
                            if is_default
                            else call_assignments
                        ),
                    )''','''                    evaluated = source_flow.arguments_by_call.get(id(call), {}).get(
                        id(expression)
                    ) if not is_default else None
                    literal = _flow_literal_expression(evaluated) if evaluated is not None else None
                    value = _static_value(
                        literal if literal is not None else expression,
                        definition.module_assignments if is_default else call_assignments,
                    )''')
# Top-level unittest inputs are unknown except the proved descriptor receiver.
change('entry_values[name].reason != "unittest entry parameter is unresolved"','entry_values[name].reason != "unittest entry parameter is dynamically unresolved"')
p.write_text(s,encoding='utf-8',newline='\n')
print('applied central provenance first implementation')