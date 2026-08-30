from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
def change(old,new):
 global s
 assert old in s, old[:100]
 s=s.replace(old,new,1)
change('    helper_provenance: _HelperProvenance | None = None\n','    helper_provenance: _HelperProvenance | None = None\n    callable_defaults: tuple[tuple[str, _FlowValue], ...] = ()\n')
change('    helper_calls: dict[int, _HelperProvenance] = field(default_factory=dict)\n','    helper_calls: dict[int, _HelperProvenance] = field(default_factory=dict)\n    defaults_by_call: dict[int, dict[str, _FlowValue]] = field(default_factory=dict)\n')
change('        self.helper_registry = helper_registry or {}\n','        self.helper_registry = helper_registry or {}\n        self._sensitive_helper_candidates: dict[str, bool] = {}\n')
anchor='    def _snapshot_call(\n'
addition='''    def _sensitive_helper_candidate(self, node: ast.Call) -> bool:
        raw = _qualified_name(node.func)
        if raw is None:
            return False
        member = raw.rsplit(".", 1)[-1]
        if member not in self._sensitive_helper_candidates:
            self._sensitive_helper_candidates[member] = any(
                definition.node.name == member
                and _helper_has_sensitive_closure(
                    definition, self.helper_registry, budget=self.budget,
                )
                for definition in self.helper_registry.values()
            )
        return self._sensitive_helper_candidates[member]

'''
change(anchor,addition+anchor)
change('''        key = id(node)
        self._call_states.setdefault(key, []).append(dict(values))''','''        key = id(node)
        if callable_value.helper_provenance is None and self._sensitive_helper_candidate(node):
            callable_value = _flow_unknown(
                "helper callable provenance is unresolved", sensitive=True,
            )
        self._call_states.setdefault(key, []).append(dict(values))''')
change('        self.flow.values_by_call[key] = merged_values\n','        self.flow.values_by_call[key] = merged_values\n        self.flow.defaults_by_call[key] = dict(merged_callable.callable_defaults)\n')
change('''            if candidate.attr in {"__dict__", "__globals__"}:
''','''            if candidate.attr in {
                "__dict__", "__globals__", "__code__", "__defaults__", "__kwdefaults__",
            }:
''')
# Defaults belong to the installed callable; closure cells still come from call state.
change('''                values[statement.name] = installed
                continue
            if isinstance(statement, ast.ClassDef):''','''                if not statement.decorator_list:
                    installed = replace(installed, callable_defaults=tuple(captured_defaults))
                values[statement.name] = installed
                continue
            if isinstance(statement, ast.ClassDef):''')
change('''                    value = _static_value(
                        expression,
                        local_definition.module_assignments
                        if is_default
                        else call_assignments,
                    )''','''                    evaluated = (
                        source_flow.defaults_by_call.get(id(call), {}).get(parameter)
                        if is_default else
                        source_flow.arguments_by_call.get(id(call), {}).get(id(expression))
                    )
                    literal = _flow_literal_expression(evaluated) if evaluated is not None else None
                    value = (
                        _static_value(literal, {}) if literal is not None
                        else _STATIC_UNRESOLVED
                    )''')
change('''                    value = _static_value(
                        literal if literal is not None else expression,
                        definition.module_assignments if is_default else call_assignments,
                    )''','''                    value = (
                        _static_value(expression, definition.module_assignments)
                        if is_default else
                        _static_value(literal, {}) if literal is not None
                        else _STATIC_UNRESOLVED
                    )''')
p.write_text(s,encoding='utf-8',newline='\n')
print('preserved callable defaults and deferred invalid-target sensitivity')