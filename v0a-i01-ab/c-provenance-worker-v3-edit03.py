from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tests\test_inventory_and_profiles.py')
s=p.read_text(encoding='utf-8')
needle='    def test_descriptor_defaults_preserve_real_python_argument_binding(self) -> None:\n'
new='''    def test_helper_effective_inputs_cover_registered_defaults_and_class_receivers(self) -> None:
        for signature, effect, refused in (
            ('def mutate(owner=ReviewTests):', 'owner._launch = None', True),
            ('def mutate(*, owner=ReviewTests):', 'owner._launch = None', True),
            ('def mutate():', 'ReviewTests._launch = None', True),
            ('def mutate(owner=ReviewTests):', 'unused = owner', False),
        ):
            with self.subTest(registered=signature, effect=effect):
                actual, review = self._provenance_case(
                    'mutate()\\nreturn ReviewTests._launch()',
                    module_tail=signature + '\\n    ' + effect + '\\n',
                )
                self.assertEqual(actual, TypeError if refused else 'fixed')
                self.assertEqual(bool(review['unresolved_dynamic_blockers']), refused)
                rows = [row for row in review['receipt']['expanded_rows']
                        if row['capability_kind'] == 'subprocess']
                self.assertEqual([row['argv'] for row in rows],
                                 [] if refused else [['-m', 'fixed']])
        for effect, refused in (('receiver._launch = None', True),
                                ('receiver.unrelated = None', False)):
            with self.subTest(class_receiver=effect):
                actual, review = self._provenance_case(
                    'saved = self._mutate\\nself = None\\nsaved()\\nreturn ReviewTests._launch()',
                    helper='    @classmethod\\n    def _mutate(receiver):\\n        ' + effect + '\\n',
                )
                self.assertEqual(actual, TypeError if refused else 'fixed')
                self.assertEqual(bool(review['unresolved_dynamic_blockers']), refused)
                rows = [row for row in review['receipt']['expanded_rows']
                        if row['capability_kind'] == 'subprocess']
                self.assertEqual([row['argv'] for row in rows],
                                 [] if refused else [['-m', 'fixed']])

'''
assert s.count(needle)==1
p.write_text(s.replace(needle,new+needle),encoding='utf-8',newline='\n')