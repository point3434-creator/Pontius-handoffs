from pathlib import Path
p=Path(r'D:\Pontius-worktrees\codex-v0a-i01-c-provenance\tests\test_inventory_and_profiles.py')
s=p.read_text(encoding='utf-8')
needle='    def test_descriptor_defaults_preserve_real_python_argument_binding(self) -> None:\n'
new='''    def test_helper_effective_input_matrix_distinguishes_execution_and_effects(self) -> None:
        channels = (
            ('positional', 'def operate(owner):', 'operate(ReviewTests)', '', 'owner'),
            ('keyword', 'def operate(*, owner):', 'operate(owner=ReviewTests)', '', 'owner'),
            ('positional-default', 'def operate(owner=ReviewTests):', 'operate()', '', 'owner'),
            ('keyword-default', 'def operate(*, owner=ReviewTests):', 'operate()', '', 'owner'),
            ('closure', 'def operate():', 'operate()', 'owner = ReviewTests\\n', 'owner'),
            ('global', 'def operate():', 'operate()', '', 'ReviewTests'),
            ('receiver', 'def _operate(self):', 'self._operate()', '', 'self'),
        )
        for channel, signature, invocation, prefix, owner in channels:
            for mode in ('write', 'read', 'dormant-write', 'write-then-raise', 'raise-then-write'):
                with self.subTest(binding_channel=channel, effect_mode=mode):
                    mutation = owner + '._launch = None'
                    effect = 'unused = ' + owner if mode == 'read' else mutation
                    if mode == 'write-then-raise':
                        effect += '\\nraise ValueError()'
                    elif mode == 'raise-then-write':
                        effect = 'raise ValueError()\\n' + effect
                    invoked = mode != 'dormant-write'
                    call = invocation if invoked else 'pass'
                    if 'raise' in mode:
                        call = 'try:\\n    ' + call + '\\nexcept ValueError:\\n    pass'
                    helper = ''
                    if channel == 'receiver':
                        helper = '    ' + signature + '\\n' + textwrap.indent(effect, '        ') + '\\n'
                        body = call + '\\nreturn self._launch()'
                    else:
                        body = prefix + signature + '\\n' + textwrap.indent(effect, '    ')
                        body += '\\n' + call + '\\nreturn ReviewTests._launch()'
                    actual, review = self._provenance_case(body, helper=helper)
                    refused = mode in {'write', 'write-then-raise'}
                    self.assertEqual(actual, TypeError if refused else 'fixed')
                    self.assertEqual(bool(review['unresolved_dynamic_blockers']), refused)
                    rows = [row for row in review['receipt']['expanded_rows']
                            if row['capability_kind'] == 'subprocess']
                    self.assertEqual([row['argv'] for row in rows],
                                     [] if refused else [['-m', 'fixed']])

'''
assert s.count(needle)==1
p.write_text(s.replace(needle,new+needle),encoding='utf-8',newline='\n')