from pathlib import Path
import ast
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
def one(old,new):
 global s
 assert s.count(old)==1,(s.count(old),old[:100])
 s=s.replace(old,new)
one('    callable_defaults: tuple[tuple[str, _FlowValue], ...] = ()\n    namespace_effects: bool = False\n','    callable_defaults: tuple[tuple[str, _FlowValue], ...] = ()\n    namespace_effects: bool = False\n    helper_refusal: str | None = None\n')
one('def _merge_flow_values(\n','''def _flow_without_helper_proof(value: _FlowValue) -> _FlowValue:
    return replace(value, helper_provenance=None, callable_defaults=(),
                   namespace_effects=False, helper_refusal=None)


def _merge_flow_values(
    name: str, values: Sequence[_FlowValue | None],
) -> _FlowValue:
    if not any(value is not None and (
        value.helper_provenance is not None or value.callable_defaults
        or value.namespace_effects or value.helper_refusal is not None
    ) for value in values):
        return _merge_legacy_flow_values(name, values)
    merged = _merge_legacy_flow_values(
        name, tuple(_flow_without_helper_proof(value) if value is not None else None
                    for value in values),
    )
    present = tuple(value for value in values if value is not None)
    complete = len(present) == len(values)
    proof = present[0].helper_provenance if complete and all(
        value.helper_provenance == present[0].helper_provenance for value in present
    ) else None
    defaults = tuple(dict(value.callable_defaults) for value in present)
    common = set(defaults[0]) if complete else set()
    for supplied in defaults[1:]:
        common.intersection_update(supplied)
    return replace(
        merged, helper_provenance=proof,
        callable_defaults=tuple((key, _merge_flow_values(
            key, tuple(supplied[key] for supplied in defaults),
        )) for key in sorted(common)),
        namespace_effects=any(value.namespace_effects for value in present),
        helper_refusal=next((value.helper_refusal for value in present
                             if value.helper_refusal is not None), None),
    )


def _merge_legacy_flow_values(
''')
one('        self.values.update(helper_seeds or {})\n','''        for name, seed in (helper_seeds or {}).items():
            self.values[name] = replace(
                self.values.get(name, seed), helper_provenance=seed.helper_provenance,
                namespace_effects=seed.namespace_effects,
            )
''')
one('''        if callable_value.namespace_effects:
            callable_value = _flow_unknown(
                "helper global or nonlocal effects are dynamically unresolved", sensitive=True,
            )
        if callable_value.helper_provenance is None and self._sensitive_helper_candidate(node):
            callable_value = _flow_unknown(
                "helper callable provenance is unresolved", sensitive=True,
            )
''','')
one('''        callable_name: str | None = None
        if merged_callable.kind == "qname":
''','''        refusal = merged_callable.helper_refusal
        if merged_callable.namespace_effects:
            refusal = "helper namespace effects are dynamically unresolved"
        if (merged_callable.helper_provenance is None
                and self._sensitive_helper_candidate(node)):
            refusal = refusal or "helper callable provenance is unresolved"
        if refusal is not None:
            self.flow.blockers_by_call.setdefault(key, refusal)
            self.flow.helper_calls.pop(key, None)
        callable_name: str | None = None
        if merged_callable.kind == "qname":
''')
one('''            try:
                callable_value = self._evaluate(node.func, values, record)
            except _ExpressionDoesNotComplete:
                if record:
                    self._snapshot_call(
                        node, values, _flow_unknown("callee lookup does not complete")
                    )
                raise
''','''            callable_value = self._evaluate(node.func, values, record)
''')
one('''    if all(value == returned[0] for value in returned):
        return returned[0]
''','''    if all(_flow_without_helper_proof(value) == _flow_without_helper_proof(returned[0])
           for value in returned):
        return _merge_flow_values("helper return", tuple(returned))
''')
one('''            provenance_entries[name] = _FlowValue(
                "qname", name, helper_provenance=_HelperProvenance(
                    kind, f"{relative_path}::{class_name}"
                )
            )
''','''            provenance_entries[name] = replace(
                provenance_entries.get(name, _flow_qname(name)),
                helper_provenance=_HelperProvenance(kind, f"{relative_path}::{class_name}"),
            )
''')
a=s.index('            provenance = base.helper_provenance\n',s.index('    def _evaluate('))
b=s.index('            if record:\n',a)
s=s[:a]+s[b:]
# Wrap each ordinary attribute result without evaluating its base twice.
tree=ast.parse(s)
method=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='_evaluate')
branch=next(n for n in ast.walk(method) if isinstance(n,ast.If) and ast.unparse(n.test)=='isinstance(node, ast.Attribute)')
lines=s.splitlines(keepends=True); offsets=[0]
for line in lines: offsets.append(offsets[-1]+len(line))
edits=[]
for n in ast.walk(branch):
 if isinstance(n,ast.Return) and n.value and n.lineno>branch.lineno+3:
  start=offsets[n.value.lineno-1]+n.value.col_offset
  end=offsets[n.value.end_lineno-1]+n.value.end_col_offset
  edits.append((start,end,'self._helper_member_value(node, base, '+s[start:end]+')'))
for a,b,value in sorted(edits,reverse=True): s=s[:a]+value+s[b:]
needle='    def _evaluate(\n'
new='''    def _helper_member_value(
        self, node: ast.Attribute, base: _FlowValue, value: _FlowValue,
    ) -> _FlowValue:
        provenance = base.helper_provenance
        if provenance is None:
            return value
        key = f"{provenance.key}::{node.attr}"
        definition = self.helper_registry.get(key)
        if provenance.kind == "module":
            exported = getattr(self.helper_registry, "exports", {}).get(key)
            return replace(value, helper_provenance=exported)
        if provenance.kind not in {"class", "instance"} or definition is None:
            return value
        if not definition.member_stable or definition.descriptor_kind is None:
            return replace(value, helper_refusal="helper descriptor member identity is unresolved")
        bound = definition.descriptor_kind == "classmethod" or (
            definition.descriptor_kind == "ordinary" and provenance.kind == "instance"
        )
        return replace(value, helper_provenance=_HelperProvenance("callable", key, bound),
                       namespace_effects=definition.namespace_effects)

'''
one(needle,new+needle)
p.write_text(s,encoding='utf-8',newline='\n')