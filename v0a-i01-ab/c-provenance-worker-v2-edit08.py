from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tools\generate_test_inventory.py')
s=p.read_text(encoding='utf-8')
old='''        self.budget = budget

    def visit(self, node: ast.AST) -> None:
        self.budget.consume()
        super().visit(node)
'''
new='''        self.budget = budget
        self.pending: list[ast.AST] | None = None

    def visit(self, node: ast.AST) -> None:
        if self.pending is not None:
            self.pending.append(node)
            return
        self.pending = [node]
        try:
            while self.pending:
                candidate = self.pending.pop()
                self.budget.consume()
                super().visit(candidate)
        finally:
            self.pending = None
'''
assert s.count(old)==1
p.write_text(s.replace(old,new),encoding='utf-8',newline='\n')