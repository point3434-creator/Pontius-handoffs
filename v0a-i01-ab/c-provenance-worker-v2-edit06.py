from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
def one(old,new):
 global s
 assert s.count(old)==1,(s.count(old),old[:90])
 s=s.replace(old,new)
one('    arguments_by_call: dict[int, dict[int, _FlowValue]] = field(default_factory=dict)\n','''    arguments_by_call: dict[int, dict[int, _FlowValue]] = field(default_factory=dict)
    invalid_helper_owners_by_call: dict[int, frozenset[str]] = field(default_factory=dict)
''')
one('''        helper_seeds: Mapping[str, _FlowValue] | None = None,
    ) -> None:
''','''        helper_seeds: Mapping[str, _FlowValue] | None = None,
        invalid_helper_owners: Iterable[str] = (),
    ) -> None:
''')
one('''        self.helper_registry = helper_registry or {}
''','''        self.helper_registry = helper_registry or {}
        self.invalid_helper_owners = set(invalid_helper_owners)
''')
one('''        self.flow.values_by_call[key] = merged_values
''','''        self.flow.values_by_call[key] = merged_values
        self.flow.invalid_helper_owners_by_call[key] = frozenset(
            self.invalid_helper_owners
        ) | self.flow.invalid_helper_owners_by_call.get(key, frozenset())
''')
one('''        refusal = merged_callable.helper_refusal
''','''        refusal = merged_callable.helper_refusal
        if (merged_callable.helper_provenance is not None
                and merged_callable.helper_provenance.key in self.invalid_helper_owners):
            refusal = "helper callable identity was mutated"
''')
one('''        key = f"{provenance.key}::{node.attr}"
        definition = self.helper_registry.get(key)
''','''        key = f"{provenance.key}::{node.attr}"
        if provenance.key in self.invalid_helper_owners or key in self.invalid_helper_owners:
            return replace(value, helper_refusal="helper namespace identity was mutated")
        definition = self.helper_registry.get(key)
''')
needle='    def _helper_member_value(\n'
new='''    def _invalidate_helper_identities(self, value: _FlowValue) -> None:
        pending = [value]
        while pending:
            self.budget.consume()
            current = pending.pop()
            if current.helper_provenance is not None:
                self.invalid_helper_owners.add(current.helper_provenance.key)
            if current.kind in {"sequence", "maybe_unbound"}:
                pending.extend(item for item in current.value if isinstance(item, _FlowValue))
            elif current.kind in {"mapping", "mapping_keys"}:
                pending.extend(item for pair in current.value for item in pair
                               if isinstance(item, _FlowValue))

    def _helper_namespace_store(
        self, target: ast.expr, values: dict[str, _FlowValue],
    ) -> None:
        if not isinstance(target, (ast.Attribute, ast.Subscript)):
            return
        owner = self._evaluate(target.value, values, False)
        proof = owner.helper_provenance
        reflective = isinstance(target.value, ast.Call) and _qualified_name(
            target.value.func
        ) in {"vars", "globals", "locals"}
        changed_member = isinstance(target, ast.Attribute) and proof is not None and (
            target.attr in {"__class__", "__bases__", "__mro__", "__getattribute__",
                            "__getattr__", "__dict__", "__code__", "__defaults__",
                            "__kwdefaults__", "__globals__"}
            or f"{proof.key}::{target.attr}" in self.helper_registry
        )
        if not reflective and not changed_member:
            return
        self.flow.standalone_blockers.append((
            target, "helper namespace mutation is dynamically unresolved",
        ))
        if reflective:
            for value in values.values():
                self._invalidate_helper_identities(value)
        else:
            self._invalidate_helper_identities(owner)

    def _helper_call_preserves_arguments(
        self, node: ast.Call, callable_value: _FlowValue,
        arguments: Sequence[_FlowValue], keywords: Sequence[_FlowValue],
    ) -> bool:
        proof = callable_value.helper_provenance
        if proof is None or proof.kind != "callable" or callable_value.helper_refusal:
            return False
        definition = self.helper_registry.get(proof.key)
        if definition is None:
            return False
        supplied = _bind_helper_arguments(
            node, definition, {}, receiver_kinds={}, proven_bound=proof.bound,
        )
        if supplied is None:
            return False
        by_expression = dict(zip(
            (id(arg) for arg in (*node.args, *(kw.value for kw in node.keywords))),
            (*arguments, *keywords), strict=True,
        ))
        tainted = {name for name, (expression, default) in supplied.items()
                   if not default and id(expression) in by_expression
                   and _flow_contains_helper_identity(by_expression[id(expression)], self.budget)}
        if not tainted:
            return True
        # A finite syntactic read-only certificate. Forwarding, storage or calling
        # through an owner is refused; no general object heap is inferred.
        candidates = tuple(_metered_ast_walk(definition.node, self.budget))
        for candidate in candidates:
            if isinstance(candidate, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
                value = candidate.value
                if value is not None and any(isinstance(part, ast.Name) and part.id in tainted
                                             for part in _metered_ast_walk(value, self.budget)):
                    targets = candidate.targets if isinstance(candidate, ast.Assign) else (
                        candidate.target,
                    )
                    for target in targets:
                        if not isinstance(target, ast.Name):
                            return False
                        tainted.add(target.id)
        for candidate in candidates:
            if isinstance(candidate, ast.Attribute) and isinstance(candidate.ctx, (ast.Store, ast.Del)):
                if any(isinstance(part, ast.Name) and part.id in tainted
                       for part in _metered_ast_walk(candidate.value, self.budget)):
                    return False
            if isinstance(candidate, (ast.Call, ast.Return)):
                inspected = ([*candidate.args, *(kw.value for kw in candidate.keywords)]
                             if isinstance(candidate, ast.Call) else [candidate.value])
                if isinstance(candidate, ast.Call) and isinstance(candidate.func, ast.Attribute):
                    inspected.append(candidate.func.value)
                if any(isinstance(part, ast.Name) and part.id in tainted
                       for expression in inspected if expression is not None
                       for part in _metered_ast_walk(expression, self.budget)):
                    return False
        return True

'''
one(needle,new+needle)
one('''                if any(_flow_contains_helper_identity(value, self.budget)
                       for value in (*argument_values, *keyword_values)):
                    self.flow.standalone_blockers.append((
                        node, "helper namespace escape is dynamically unresolved",
                    ))
''','''                if (any(_flow_contains_helper_identity(value, self.budget)
                        for value in (*argument_values, *keyword_values))
                        and not self._helper_call_preserves_arguments(
                            node, callable_value, argument_values, keyword_values,
                        )):
                    self.flow.standalone_blockers.append((
                        node, "helper namespace escape is dynamically unresolved",
                    ))
                    for value in (*argument_values, *keyword_values):
                        self._invalidate_helper_identities(value)
''')
one('''        subscript_owner: _FlowValue | None = None
''','''        self._helper_namespace_store(target, values)
        subscript_owner: _FlowValue | None = None
''')
a=s.index('    def _delete_target(');b=s.index('        if isinstance(target, (ast.Tuple, ast.List)):',a)
s=s[:b]+'''        self._helper_namespace_store(target, values)
'''+s[b:]
# Explicitly preserve binding rather than treating a starred target as absent.
a=s.index('    def _assign(');b=s.index('        if isinstance(target, ast.Name):',a)
s=s[:b]+'''        if isinstance(target, ast.Starred):
            self._assign(target.value, _flow_unknown("starred assignment is dynamically unresolved"), values)
            return
'''+s[b:]
one('''    helper_seeds: Mapping[str, _FlowValue] | None = None,
) -> _ReviewFlow:
''','''    helper_seeds: Mapping[str, _FlowValue] | None = None,
    invalid_helper_owners: Iterable[str] = (),
) -> _ReviewFlow:
''')
one('''        helper_registry,
        helper_seeds,
    )
''','''        helper_registry,
        helper_seeds,
        invalid_helper_owners,
    )
''')
one('''    receiver_kinds: Mapping[str, str] | None = None,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
''','''    receiver_kinds: Mapping[str, str] | None = None,
    invalid_helper_owners: Iterable[str] = (),
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
''')
one('''        helper_seeds=_helper_provenance_seeds(
''','''        invalid_helper_owners=invalid_helper_owners,
        helper_seeds=_helper_provenance_seeds(
''')
s=s.replace('''                closure_helper_key=local_key,
                analysis_budget=analysis_budget,
''','''                closure_helper_key=local_key,
                analysis_budget=analysis_budget,
                invalid_helper_owners=source_flow.invalid_helper_owners_by_call.get(id(call), ()),
''')
s=s.replace('''                closure_helper_key=helper_key,
                analysis_budget=analysis_budget,
''','''                closure_helper_key=helper_key,
                analysis_budget=analysis_budget,
                invalid_helper_owners=source_flow.invalid_helper_owners_by_call.get(id(call), ()),
''')
p.write_text(s,encoding='utf-8',newline='\n')
# Clarify only newly added known failed lookup controls; old assertions remain unchanged.
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tests\test_inventory_and_profiles.py')
s=p.read_text(encoding='utf-8')
s=s.replace("                self.assertTrue(review['unresolved_dynamic_blockers'], label)\n", "                if label in {'annotation-only', 'future-local', 'deleted'}:\n                    self.assertFalse(review['receipt']['expanded_rows'])\n                else:\n                    self.assertTrue(review['unresolved_dynamic_blockers'], label)\n",1)
old="                self.assertIn(actual, ('changed', UnboundLocalError))\n                self.assertTrue(review['unresolved_dynamic_blockers'])\n"
new="                self.assertIn(actual, ('changed', UnboundLocalError))\n                if actual is UnboundLocalError:\n                    self.assertFalse(review['receipt']['expanded_rows'])\n                else:\n                    self.assertTrue(review['unresolved_dynamic_blockers'])\n"
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s,encoding='utf-8',newline='\n')