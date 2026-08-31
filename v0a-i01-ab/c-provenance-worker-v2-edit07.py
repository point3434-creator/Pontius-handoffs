from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
s=s.replace('    def _delete_target(self, target: ast.AST) -> bool:\n        self._helper_namespace_store(target, values)\n','    def _delete_target(self, target: ast.AST) -> bool:\n')
a=s.index('    def _delete_target(',s.index('class _SourceOrderedResolver:'))
b=s.index('        if isinstance(target, (ast.Tuple, ast.List)):',a)
s=s[:b]+'        self._helper_namespace_store(target, values)\n'+s[b:]
s=s.replace('''        if (merged_callable.helper_provenance is None
                and self._sensitive_helper_candidate(node)):
''','''        if (merged_callable.helper_provenance is None
                and merged_callable.kind != "callable_constant"
                and self._sensitive_helper_candidate(node)):
''')
s=s.replace('''        callable_name: str | None = None
        if merged_callable.kind == "qname":
''','''        if merged_callable.kind == "callable_constant":
            self.flow.proved_non_sensitive_calls.add(key)
        callable_name: str | None = None
        if merged_callable.kind == "qname":
''')
p.write_text(s,encoding='utf-8',newline='\n')