import importlib.util,json,pathlib,sys
checks=pathlib.Path(r'D:\Pontius-handoffs\v0a-i01-ab\r008\checks')
spec=importlib.util.spec_from_file_location('codex_a_probe_helpers',checks/'codex-a-07-binding-probes.py')
p=importlib.util.module_from_spec(spec);sys.modules[spec.name]=p;spec.loader.exec_module(p)
# A separately defined, side-effect-free Python binding oracle. No subprocess
# fixture body executes. These functions are ordinary language semantics only.
pure_helper='def _launch(self=None):\n    return "fixed"'
pure_static='@staticmethod\ndef _launch():\n    return "fixed"'
pure_class='@classmethod\ndef _launch(cls):\n    return "fixed"'
variants=[
 ('list-self-shadow',p.fixed,pure_helper,'[self._launch() for self in [None]]',True),
 ('set-self-shadow',p.fixed,pure_helper,'{self._launch() for self in [None]}',True),
 ('dict-self-shadow',p.fixed,pure_helper,'{0:self._launch() for self in [None]}',True),
 ('nested-comp-shadow',p.fixed,pure_helper,'[[self._launch() for self in [None]] for item in [0]]',True),
 ('comp-outer-receiver',p.fixed,pure_helper,'[self._launch() for item in [None]]',False),
 ('class-local-shadow',p.helper('@staticmethod','',value='"fixed"'),pure_static,'ReviewTests = None\nReviewTests._launch()',True),
 ('class-comp-shadow',p.helper('@staticmethod','',value='"fixed"'),pure_static,'[ReviewTests._launch() for ReviewTests in [None]]',True),
 ('class-loop-shadow',p.helper('@staticmethod','',value='"fixed"'),pure_static,'for ReviewTests in [None]:\n    ReviewTests._launch()',True),
 ('class-param-shadow',p.helper('@staticmethod','',value='"fixed"')+'\ndef _caller(self, ReviewTests=None):\n    ReviewTests._launch()',pure_static+'\ndef _caller(self, ReviewTests=None):\n    ReviewTests._launch()','self._caller()',True),
 ('classmethod-local-shadow',p.helper('@classmethod','cls',value='"fixed"'),pure_class,'ReviewTests = None\nReviewTests._launch()',True),
 ('class-local-unshadowed',p.helper('@staticmethod','',value='"fixed"'),pure_static,'ReviewTests._launch()',False),
 ('class-nested-capture',p.helper('@staticmethod','',value='"fixed"'),pure_static,'ReviewTests = None\ndef nested():\n    ReviewTests._launch()\nnested()',True),
]
for label,helper,pure,entry,invalid in variants:
 namespace={}
 pure_source='import unittest\n'+p.source(pure,entry).split('import subprocess, sys, unittest\n',1)[1]
 exec(compile(pure_source,'<independent-pure-binding-oracle>','exec'),namespace)
 oracle_error=None
 try: oracle_result=namespace['ReviewTests']('test_static').test_static()
 except Exception as error: oracle_error=type(error).__name__;oracle_result=None
 assert (oracle_error=='AttributeError') if invalid else oracle_error is None,(label,oracle_error)
 review=p.review(p.source(helper,entry));rows=[r for r in review['receipt']['expanded_rows'] if r['capability_kind']=='subprocess'];blockers=review['unresolved_dynamic_blockers']
 print(json.dumps({'confirmed_case':label,'pure_oracle_error':oracle_error,'expected_blocked':invalid,'blockers':blockers,'derived_argv':[r['argv'] for r in rows],'unexpected_approval':invalid and not blockers}),flush=True)