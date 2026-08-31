from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tests\test_inventory_and_profiles.py')
s=p.read_text(encoding='utf-8')
old="            'def nested():\\n    return self._launch()\\ndel nested\\nreturn nested()',\n"
new="            'def nested(module=\"first\"):\\n    return self._launch(module=module)\\nnested.__defaults__ = (\"changed\",)\\nreturn nested()',\n"+old
assert s.count(old)==1
s=s.replace(old,new)
needle='    def test_descriptor_defaults_preserve_real_python_argument_binding(self) -> None:\n'
new='''    def test_helper_provenance_imported_initialization_mutation_is_owner_scoped(self) -> None:
        process = (
            'subprocess.run([sys.executable, "-m", "fixed"], cwd=".", '
            'env={**__import__("os").environ, "SAFE": "1"}, timeout=5, check=False)'
        )
        support = ('import subprocess, sys\\nclass Support:\\n'
                   '    @staticmethod\\n    def launch():\\n        ' + process + '\\n')
        for member, expected_blocker in (('launch', True), ('unrelated', False)):
            with self.subTest(member=member):
                mutator = ('import tests.review_support as support\\n'
                           'support.Support.' + member + ' = None\\n')
                source = (
                    'import unittest\\nimport tests.review_support as support\\n'
                    'import tests.review_mutator\\n'
                    'class ReviewTests(unittest.TestCase):\\n'
                    '    def test_static(self): return support.Support.launch()\\n'
                    '    def test_denied(self): pass\\n'
                )
                namespace = {}
                exec(support.replace(process, 'return "fixed"'), namespace)
                setattr(namespace['Support'], member, None)
                if expected_blocker:
                    with self.assertRaises(TypeError):
                        namespace['Support'].launch()
                else:
                    self.assertEqual(namespace['Support'].launch(), 'fixed')
                review = self._review(sources={
                    'tests/test_review.py': source.encode('utf-8'),
                    'tests/review_support.py': support.encode('utf-8'),
                    'tests/review_mutator.py': mutator.encode('utf-8'),
                })
                self.assertEqual(bool(review['unresolved_dynamic_blockers']), expected_blocker)
                if not expected_blocker:
                    rows = [r for r in review['receipt']['expanded_rows']
                            if r['capability_kind'] == 'subprocess']
                    self.assertEqual([r['argv'] for r in rows], [['-m', 'fixed']])

'''
assert s.count(needle)==1
s=s.replace(needle,new+needle)
p.write_text(s,encoding='utf-8',newline='\n')