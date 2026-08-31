from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
def one(old,new):
 global s
 assert s.count(old)==1,(s.count(old),old[:70])
 s=s.replace(old,new)
one('''        self.invalid_helper_owners = set(invalid_helper_owners)
''','''        self.invalid_helper_owners = set(invalid_helper_owners) | set(
            getattr(self.helper_registry, "initial_member_mutations", ())
        )
''')
one('''        self.qualified_proofs: dict[str, _HelperProvenance] = {}
''','''        self.qualified_proofs: dict[str, _HelperProvenance] = {}
        self.initial_member_mutations: set[str] = set()
        self.initial_namespace_refusals: set[str] = set()
        self.module_dependencies: dict[str, set[str]] = {}
''')
a=s.index('    return registry\n',s.index('def _review_function_registry('))
s=s[:a]+'''    for relative_path, tree in parsed.items():
        budget = certificate_budgets[relative_path]
        aliases = _module_import_aliases(tree)
        assignments = _static_assignments(tree.body)
        dependencies = registry.module_dependencies.setdefault(relative_path, set())
        for candidate in _helper_initialization_nodes(tree, budget):
            if isinstance(candidate, (ast.Import, ast.ImportFrom)):
                modules = ([alias.name for alias in candidate.names]
                           if isinstance(candidate, ast.Import) else [candidate.module or ""])
                for module in modules:
                    proof = registry.qualified_proofs.get(module)
                    if proof is not None and proof.kind == "module":
                        dependencies.add(proof.key)
            target: ast.expr | None = None
            member: str | None = None
            if isinstance(candidate, ast.Attribute) and isinstance(candidate.ctx, (ast.Store, ast.Del)):
                target, member = candidate.value, candidate.attr
            elif isinstance(candidate, ast.Call) and _qualified_name(candidate.func) in {
                "setattr", "delattr",
            }:
                if len(candidate.args) >= 2:
                    target = candidate.args[0]
                    if isinstance(candidate.args[1], ast.Constant) and type(candidate.args[1].value) is str:
                        member = candidate.args[1].value
            elif isinstance(candidate, ast.Call) and _qualified_name(candidate.func) in {"exec", "eval"}:
                registry.initial_namespace_refusals.add(relative_path)
            elif isinstance(candidate, ast.Subscript) and isinstance(candidate.ctx, (ast.Store, ast.Del)):
                if isinstance(candidate.value, ast.Call) and _qualified_name(candidate.value.func) in {
                    "vars", "globals", "locals",
                }:
                    registry.initial_namespace_refusals.add(relative_path)
            if target is None:
                continue
            seen: set[str] = set()
            while isinstance(target, ast.Name) and target.id in assignments and target.id not in seen:
                budget.consume()
                seen.add(target.id)
                target = assignments[target.id]
            raw = _resolved_qualified_name(target, aliases) or ""
            proof = registry.qualified_proofs.get(raw) or registry.exports.get(
                f"{relative_path}::{raw}"
            )
            definition = registry.get(raw) or registry.get(
                f"{relative_path}::{raw.replace('.', '::')}"
            )
            if proof is None and definition is not None:
                key = f"{definition.relative_path}::"
                if definition.class_name is not None:
                    key += f"{definition.class_name}::"
                proof = _HelperProvenance("callable", key + definition.node.name)
            if proof is None:
                # An unknown initialized namespace might alias an imported owner.
                registry.initial_namespace_refusals.add(relative_path)
                continue
            if member is None or member in {
                "__class__", "__bases__", "__mro__", "__getattribute__", "__getattr__",
                "__dict__", "__globals__", "__code__", "__defaults__", "__kwdefaults__",
            }:
                registry.initial_member_mutations.add(proof.key)
            elif proof.kind in {"class", "instance"}:
                key = f"{proof.key}::{member}"
                if key in registry:
                    registry.initial_member_mutations.add(key)
            elif proof.kind == "module":
                exported = registry.exports.get(f"{proof.key}::{member}")
                if exported is not None:
                    registry.initial_member_mutations.add(exported.key)
''' +s[a:]
# Add only dependency-reachable unsupported initialization refusals, not unrelated corpus poison.
a=s.index('    rows: list[dict[str, object]] = []\n    blockers: list[dict[str, object]] = []\n',s.index('def _review_body('))
b=a+len('    rows: list[dict[str, object]] = []\n    blockers: list[dict[str, object]] = []\n')
s=s[:b]+'''    pending_modules = [relative_path]
    visited_modules: set[str] = set()
    while pending_modules:
        analysis_budget.consume()
        module = pending_modules.pop()
        if module in visited_modules:
            continue
        visited_modules.add(module)
        if module in getattr(helper_registry, "initial_namespace_refusals", ()):
            blockers.append(_review_blocker(
                item_id, relative_path, node,
                "imported helper namespace initialization is dynamically unresolved",
            ))
            break
        pending_modules.extend(getattr(helper_registry, "module_dependencies", {}).get(module, ()))
''' +s[b:]
p.write_text(s,encoding='utf-8',newline='\n')