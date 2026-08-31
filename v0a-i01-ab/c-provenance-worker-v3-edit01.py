from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tests\test_inventory_and_profiles.py')
s=p.read_text(encoding='utf-8')
needle='    def test_descriptor_defaults_preserve_real_python_argument_binding(self) -> None:\n'
new='''    def test_helper_effective_inputs_preserve_reached_owner_mutations(self) -> None:
        cases = (
            ('positional-default', 'def mutate(owner=ReviewTests):\\n    owner._launch = None\\nmutate()'),
            ('posonly-default', 'def mutate(owner=ReviewTests, /):\\n    owner._launch = None\\nmutate()'),
            ('kwonly-default', 'def mutate(*, owner=ReviewTests):\\n    owner._launch = None\\nmutate()'),
            ('explicit-positional', 'def mutate(owner):\\n    owner._launch = None\\nmutate(ReviewTests)'),
            ('explicit-keyword', 'def mutate(*, owner):\\n    owner._launch = None\\nmutate(owner=ReviewTests)'),
            ('global-owner', 'def mutate():\\n    ReviewTests._launch = None\\nmutate()'),
            ('local-owner', 'owner = ReviewTests\\ndef mutate():\\n    owner._launch = None\\nmutate()'),
            ('self-owner', 'def mutate():\\n    self._launch = None\\nmutate()'),
            ('container-default', 'def mutate(owners=(ReviewTests,)):\\n    owners[0]._launch = None\\nmutate()'),
            ('saved-default', 'owner = ReviewTests\\ndef mutate(target=owner):\\n    target._launch = None\\nsaved = mutate\\nowner = None\\nsaved()'),
            ('late-cell', 'owner = None\\ndef mutate():\\n    owner._launch = None\\nowner = ReviewTests\\nmutate()'),
            ('nested-invocation', 'def outer(owner=ReviewTests):\\n    def mutate():\\n        owner._launch = None\\n    mutate()\\nouter()'),
            ('before-raise', 'def mutate(owner=ReviewTests):\\n    owner._launch = None\\n    raise ValueError()\\ntry:\\n    mutate()\\nexcept ValueError:\\n    pass'),
        )
        for label, body in cases:
            with self.subTest(effective_input=label):
                target = 'self' if label == 'self-owner' else 'ReviewTests'
                actual, review = self._provenance_case(body + '\\nreturn ' + target + '._launch()')
                self.assertIs(actual, TypeError)
                self.assertTrue(review['unresolved_dynamic_blockers'])
                self.assertFalse([row for row in review['receipt']['expanded_rows']
                                  if row['capability_kind'] == 'subprocess'])
        for body in (
            'self._mutate()\\nreturn self._launch()',
            'old = self\\nsaved = self._mutate\\nself = None\\nsaved()\\nreturn old._launch()',
        ):
            with self.subTest(captured_receiver=body):
                actual, review = self._provenance_case(
                    body, helper='    def _mutate(self):\\n        self._launch = None\\n',
                )
                self.assertIs(actual, TypeError)
                self.assertTrue(review['unresolved_dynamic_blockers'])
                self.assertFalse([row for row in review['receipt']['expanded_rows']
                                  if row['capability_kind'] == 'subprocess'])

    def test_helper_effective_inputs_preserve_overrides_and_nonexecution(self) -> None:
        cases = (
            ('unused-default', 'def read(owner=ReviewTests):\\n    return 1\\nread()'),
            ('unused-keyword-default', 'def read(*, owner=ReviewTests):\\n    return 1\\nread()'),
            ('override', 'def mutate(owner=ReviewTests):\\n    if owner is not None:\\n        owner._launch = None\\nmutate(None)'),
            ('keyword-override', 'def mutate(*, owner=ReviewTests):\\n    if owner is not None:\\n        owner._launch = None\\nmutate(owner=None)'),
            ('captured-unrelated', 'owner = None\\ndef mutate(target=owner):\\n    if target is not None:\\n        target._launch = None\\nowner = ReviewTests\\nmutate()'),
            ('late-unrelated', 'owner = ReviewTests\\ndef mutate():\\n    if owner is not None:\\n        owner._launch = None\\nowner = None\\nmutate()'),
            ('dormant', 'def outer(owner=ReviewTests):\\n    def mutate():\\n        owner._launch = None\\n    return 1\\nouter()'),
            ('raise-before', 'def mutate(owner=ReviewTests):\\n    raise ValueError()\\n    owner._launch = None\\ntry:\\n    mutate()\\nexcept ValueError:\\n    pass'),
            ('invalid-posonly-keyword', 'def mutate(owner=ReviewTests, /):\\n    owner._launch = None\\ntry:\\n    mutate(owner=None)\\nexcept TypeError:\\n    pass'),
            ('invalid-duplicate', 'def mutate(owner):\\n    owner._launch = None\\ntry:\\n    mutate(ReviewTests, owner=None)\\nexcept TypeError:\\n    pass'),
        )
        for label, body in cases:
            with self.subTest(nonexecution=label):
                actual, review = self._provenance_case(body + '\\nreturn ReviewTests._launch()')
                self.assertEqual(actual, 'fixed')
                rows = [row for row in review['receipt']['expanded_rows']
                        if row['capability_kind'] == 'subprocess']
                self.assertEqual([row['argv'] for row in rows], [['-m', 'fixed']])
                self.assertFalse(review['unresolved_dynamic_blockers'])
        actual, review = self._provenance_case(
            'self._mutate()\\nreturn self._launch()',
            helper='    def _mutate(self):\\n        self.unrelated = None\\n',
        )
        self.assertEqual(actual, 'fixed')
        self.assertFalse(review['unresolved_dynamic_blockers'])

'''
assert s.count(needle)==1
p.write_text(s.replace(needle,new+needle),encoding='utf-8',newline='\n')