from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tests\test_inventory_and_profiles.py')
s=p.read_text(encoding='utf-8')
needle='    def test_descriptor_defaults_preserve_real_python_argument_binding(self) -> None:\n'
new='''    def test_helper_provenance_precision_preserves_original_values_and_members(self) -> None:
        for body, tail in (
            ('code = self._launch.__code__\\nreturn self._launch()', ''),
            ('return self._launch()',
             'class Other:\\n    def change(self): self._launch = None\\n'),
            ('def nested():\\n    nonlocal self\\n    return self._launch()\\nreturn nested()', ''),
        ):
            with self.subTest(precision=body, unrelated=tail):
                actual, review = self._provenance_case(body, module_tail=tail)
                self.assertEqual(actual, 'fixed')
                rows = [r for r in review['receipt']['expanded_rows']
                        if r['capability_kind'] == 'subprocess']
                self.assertEqual([r['argv'] for r in rows], [['-m', 'fixed']])
                self.assertFalse(review['unresolved_dynamic_blockers'])
        for declaration in ('ReviewTests: object', 'ReviewTests = None\\ndel ReviewTests'):
            actual, review = self._provenance_case(
                declaration + '\\ntry:\\n    ReviewTests._launch()\\n'
                'except NameError:\\n    return self._launch(module="handled")'
            )
            self.assertEqual(actual, 'handled')
            rows = [r for r in review['receipt']['expanded_rows']
                    if r['capability_kind'] == 'subprocess']
            self.assertEqual([r['argv'] for r in rows], [['-m', 'handled']])
            self.assertFalse(review['unresolved_dynamic_blockers'])

    def test_helper_provenance_module_exports_and_skip_identity_are_exact(self) -> None:
        process = (
            'subprocess.run([sys.executable, "-m", "exported"], cwd=".", '
            'env={**__import__("os").environ, "SAFE": "1"}, timeout=5, check=False)'
        )
        for decorator, prefix, blocked in (
            ('', '', False),
            ('@unittest.skipUnless(True, "enabled")\\n', '', False),
            ('@unittest.skipIf(False, "enabled")\\n', '', False),
            ('@unittest.skip("disabled")\\n', '', False),
            ('@decorate\\n', 'def decorate(value): return value\\n', True),
        ):
            with self.subTest(decorator=decorator):
                support = (
                    'import subprocess, sys, unittest\\n' + prefix + decorator
                    + 'class Support:\\n    @staticmethod\\n    def launch():\\n        '
                    + process + '\\n'
                )
                source = (
                    'import unittest\\nimport tests.review_support as support\\n'
                    'class ReviewTests(unittest.TestCase):\\n'
                    '    def test_static(self):\\n        return support.Support.launch()\\n'
                    '    def test_denied(self): pass\\n'
                )
                namespace = {}
                exec(support.replace(process, 'return "exported"'), namespace)
                self.assertEqual(namespace['Support'].launch(), 'exported')
                review = self._review(sources={
                    'tests/test_review.py': source.encode('utf-8'),
                    'tests/review_support.py': support.encode('utf-8'),
                })
                if blocked:
                    self.assertTrue(review['unresolved_dynamic_blockers'])
                else:
                    rows = [r for r in review['receipt']['expanded_rows']
                            if r['capability_kind'] == 'subprocess']
                    self.assertEqual([r['argv'] for r in rows], [['-m', 'exported']])
                    self.assertFalse(review['unresolved_dynamic_blockers'])

'''
assert s.count(needle)==1
p.write_text(s.replace(needle,new+needle),encoding='utf-8',newline='\n')